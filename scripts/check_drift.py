#!/usr/bin/env python3
"""Companion + version drift linter (self-audit 2026-06-07/FF-004).

Automates the manual MANIFEST.md drift check ("## Drift check", 5 steps) so companions
can never silently drift from the authority texts. Run by pre-commit (a local hook) and
therefore by CI as well, since `.github/workflows/hygiene.yml` runs `pre-commit run
--all-files`.

The authority-text headers are the single source of truth: the current versions/dates are
PARSED from `audit-spec.md` and `profile-directive.md`, never hard-coded. Everything else is
checked against them.

Checks (all deterministic; calibrated NOT to false-positive on the authority texts' own
version-lineage sections or on CHANGELOG.md history):

  1. Authority self-consistency  — each authority text's H1 title agrees with its
     **Version:** line.
  2. MANIFEST authority table     — matches the headers (version + date), exactly.
  3. Current targets declared     — MANIFEST's derived table and both companions declare
     the CURRENT authority versions/dates, and AGENTS.md quotes the directive's current
     `directive_version` / `audit_spec_target` schema-identifier literals.
  4. No conflicting versions      — in consumer files (companions, MANIFEST, README), every
     v3.x token equals the spec version and every v1.x token the directive version.
  5. No stale filenames           — the pre-rename filenames appear only in CHANGELOG.md.
  6. Section refs resolve         — §N / §N.N prose references resolve to a numeric
     heading; when a line names exactly one authority text, the ref must resolve
     against THAT text (so `profile directive §11.12` fails — §11.12 is an audit-spec
     section). Self-checkable with `--self-test`.
  7. Phase labels are attributed  — lettered profile phases are not described
     as audit phases.
  8. Links resolve                — repo-relative Markdown links and CLAUDE.md @imports point
     at files that exist.
  9. Ids are cycle-qualified      — a bare FF-/F- per-cycle id (three digits, no
     YYYY-MM-DD/ qualifier) is flagged on every tracked surface except the authority
     texts, CHANGELOG.md, adr/, and examples/, which carry their own cycle context.
 10. Companion hash binding       — MANIFEST.md's "Content-hash binding" lines match the
     current sha256 of both authority texts; an authority cut re-syncs the derived files
     and then re-attests the lines (`--print-bindings` emits the current correct lines).

Exit 0 = clean; exit 1 = drift found (each failure is printed). Stdlib only.
"""

from __future__ import annotations

import hashlib
import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]

# Files that legitimately contain historical version/filename references.
HISTORICAL = {"CHANGELOG.md", "audit-spec.md", "profile-directive.md"}

# Files that state the CURRENT authority targets and must never carry a conflicting version.
CONSUMERS = ["companions/kickoff-prompt.md", "companions/explainer.md", "MANIFEST.md", "README.md"]

# Pre-rename filenames (CHANGELOG.md records the rename); they must appear nowhere else.
OLD_FILENAMES = [
    "agentic-audit-spec-v3.md",
    "project-profile-directive.md",
    "audit-spec-friendly-explainer.md",
    "audit-kickoff-prompt.md",
    "audit-directive-set-manifest.md",
]

SECTION_REF_IGNORE = "drift-check: ignore-section-ref"
SECTION_REF_RE = re.compile(r"§\s*(\d+(?:\.\d+)?)")
SECTION_HEADING_RE = re.compile(r"^#{1,6}\s+(?:Phase\s+)?(\d+(?:\.\d+)?)(?=[\s.`—–-]|$)")
# Authority names as written in prose, used to bind a §-reference to the specific
# authority it cites (2026-06-08/FF-001). Deliberately matches only the CANONICAL identifiers:
# `audit[\s-]spec` (also "Audit Specification") and `profile[\s-]?directive` (also the
# `*-directive.md` filename). Ambiguous short forms ("the spec", "the directive") and the
# long form "Project Profile Discovery Directive" do NOT match and fall through to the
# merged existence check — by design: the bare word "directive" appears next to spec
# §-refs in audit-spec.md's own lineage/changelog prose, so binding on it would
# false-positive and break the gate. The intended fallback is pinned in self_test().
AUTHORITY_NAME_RE = {
    "audit-spec.md": re.compile(r"audit[\s-]spec", re.I),
    "profile-directive.md": re.compile(r"profile[\s-]?directive", re.I),
}
AUDIT_LETTER_PHASE_RE = re.compile(r"\baudit(?:'s)?\s+Phase\s+([A-I])\b", re.I)

# Bare per-cycle self-audit ids (MANIFEST.md "Identifier convention", adopted via ADR
# 0003): an FF-/F- id carrying no YYYY-MM-DD/ cycle qualifier. Surfaces that carry their
# own cycle context are exempt: the authority texts (their worked-example namespace),
# CHANGELOG.md (dated headings), adr/ (dated by their Status/Source headers), and
# examples/ (a third-party namespace). Template forms (FF-NNN) have no digits and never
# match.
BARE_ID_IGNORE = "drift-check: ignore-bare-id"
BARE_ID_RE = re.compile(r"(?<!\d\d\d\d-\d\d-\d\d/)\bFF?-\d{3}\b")
BARE_ID_EXEMPT_FILES = {"audit-spec.md", "profile-directive.md", "CHANGELOG.md"}
BARE_ID_EXEMPT_DIRS = ("adr/", "examples/")

# Derived files content-hash-bound to the authority texts (P-013 via ADR 0003): each
# MANIFEST.md "Content-hash binding" line attests the exact authority-text bytes the
# derived file was last synced against, and is re-attested at every authority cut.
HASH_BOUND_DERIVED = [
    "companions/kickoff-prompt.md",
    "companions/explainer.md",
    ".agents/skills/run-agentic-audit/SKILL.md",
]
BINDING_LINE_RE = re.compile(
    r"^(?P<derived>\S+) @ audit-spec\.md=sha256:(?P<spec>[0-9a-f]{64})"
    r" profile-directive\.md=sha256:(?P<directive>[0-9a-f]{64})$"
)

failures: list[str] = []


def fail(check: str, msg: str) -> None:
    failures.append(f"[{check}] {msg}")


def read(rel: str) -> str:
    return (REPO / rel).read_text(encoding="utf-8")


def tracked_files(*globs: str) -> list[str]:
    """Tracked files matching the globs (excludes gitignored profile/ and audit/)."""
    try:
        out = subprocess.run(
            ["git", "ls-files", "--", *globs],
            cwd=REPO, capture_output=True, text=True, check=True,
        ).stdout
        return list(dict.fromkeys(line for line in out.splitlines() if line))
    except Exception:  # pragma: no cover - fallback if git is unavailable
        return list(dict.fromkeys(str(p.relative_to(REPO)) for g in globs for p in REPO.glob(g)))


def parse_authority() -> dict[str, str]:
    """Source of truth: versions + dates parsed from the authority-text headers."""
    spec = read("audit-spec.md")
    directive = read("profile-directive.md")

    def grab(text: str, pattern: str, what: str) -> str:
        m = re.search(pattern, text, re.M)
        if not m:
            fail("setup", f"could not parse {what} from header")
            return ""
        return m.group(1)

    return {
        "spec_ver": grab(spec, r"^\*\*Version:\*\*\s*(v\S+)", "spec version"),
        "spec_date": grab(spec, r"^\*\*Specification date:\*\*\s*(\S+)", "spec date"),
        "dir_ver": grab(directive, r"^\*\*Version:\*\*\s*(v\S+)", "directive version"),
        "dir_date": grab(directive, r"^\*\*Directive date:\*\*\s*(\S+)", "directive date"),
    }


def check_1_title_agreement(a: dict[str, str]) -> None:
    for rel, ver in (("audit-spec.md", a["spec_ver"]), ("profile-directive.md", a["dir_ver"])):
        title = read(rel).splitlines()[0]
        if ver and ver not in title:
            fail("1-title", f"{rel} H1 title {title!r} does not contain its version {ver}")


def check_2_manifest_authority(a: dict[str, str]) -> None:
    man = read("MANIFEST.md")
    expected = [
        f"Agentic Architecture Audit Specification {a['spec_ver']}, {a['spec_date']}",
        f"Project Profile Discovery Directive {a['dir_ver']}, {a['dir_date']}",
    ]
    for e in expected:
        if e and e not in man:
            fail("2-manifest", f"MANIFEST.md authority table missing exact entry: {e!r}")


def missing_agents_literals(directive_text: str, agents_text: str) -> list[str]:
    """The directive's schema-identifier literals that AGENTS.md fails to quote verbatim.

    AGENTS.md item 4 explains `directive_version` (tracks the directive's header version
    at each cut) and `audit_spec_target` (the pinned consumption baseline, per ADR 0002)
    and must quote both current literals, so a cut that changes either literal is forced
    to update AGENTS.md in the same revision. AGENTS.md is deliberately NOT in CONSUMERS:
    check 4 would false-positive on the intentional v3.1 baseline pin it documents.
    """
    missing = []
    for key in ("directive_version", "audit_spec_target"):
        m = re.search(rf'^\s*{key}:\s*"([^"]+)"', directive_text, re.M)
        if m is None:
            missing.append(f"{key}: literal not parseable from profile-directive.md")
        elif f'"{m.group(1)}"' not in agents_text:
            missing.append(f'{key}: AGENTS.md does not quote the current literal "{m.group(1)}"')
    return missing


def check_3_current_targets(a: dict[str, str]) -> None:
    man = read("MANIFEST.md")
    for e in (f"Audit Spec {a['spec_ver']}", f"Profile Directive {a['dir_ver']}"):
        if e and e not in man:
            fail("3-targets", f"MANIFEST.md derived table missing target: {e!r}")
    spec_decl = f"Specification {a['spec_ver']} ({a['spec_date']})"
    dir_decl = f"Directive {a['dir_ver']} ({a['dir_date']})"
    for rel in ("companions/kickoff-prompt.md", "companions/explainer.md"):
        text = read(rel)
        for decl in (spec_decl, dir_decl):
            if decl and decl not in text:
                fail("3-targets", f"{rel} does not declare current target {decl!r}")
    for problem in missing_agents_literals(read("profile-directive.md"), read("AGENTS.md")):
        fail("3-targets", problem)


def check_4_no_conflicting_versions(a: dict[str, str]) -> None:
    families = [(r"v3\.\d+", a["spec_ver"], "spec"), (r"v1\.\d+", a["dir_ver"], "directive")]
    for rel in CONSUMERS:
        text = read(rel)
        for pattern, current, name in families:
            for tok in set(re.findall(pattern, text)):
                if current and tok != current:
                    fail("4-version", f"{rel} references {name} {tok} but current is {current}")


def check_5_old_filenames() -> None:
    for rel in tracked_files("*.md", "CITATION.cff"):
        if rel in HISTORICAL:
            continue
        text = read(rel)
        for old in OLD_FILENAMES:
            if old in text:
                fail("5-rename", f"{rel} references pre-rename filename {old!r} (allowed only in CHANGELOG.md)")


def authority_sections() -> dict[str, set[str]]:
    """Per-authority numeric heading sets, plus their merged union (`__merged__`)."""
    out: dict[str, set[str]] = {}
    for rel in ("audit-spec.md", "profile-directive.md"):
        secs: set[str] = set()
        for line in read(rel).splitlines():
            m = SECTION_HEADING_RE.match(line)
            if m:
                secs.add(m.group(1))
        out[rel] = secs
    out["__merged__"] = out["audit-spec.md"] | out["profile-directive.md"]
    return out


def unresolved_section_refs(line: str, sections: dict[str, set[str]]) -> list[tuple[str, str]]:
    """§-references on `line` that do not resolve, as (section, authority-label) pairs.

    If the line names exactly one authority text, every §-reference on it must resolve
    against THAT text's headings — so `profile directive §11.12` is caught, because
    §11.12 exists only in `audit-spec.md` (2026-06-08/FF-001). If the line names both authorities
    or neither, fall back to existence across the merged set (the prior behavior); that
    keeps correctly-attributed lines such as `§11.12 of audit-spec.md` and bare refs
    green. Lines carrying the ignore marker are skipped entirely.
    """
    if SECTION_REF_IGNORE in line:
        return []
    named = [rel for rel, rx in AUTHORITY_NAME_RE.items() if rx.search(line)]
    if len(named) == 1:
        valid, label = sections[named[0]], named[0]
    else:
        valid, label = sections["__merged__"], "either authority text"
    return [
        (m.group(1), label)
        for m in SECTION_REF_RE.finditer(line)
        if m.group(1) not in valid
    ]


def check_6_section_refs_resolve() -> None:
    sections = authority_sections()
    if not sections["__merged__"]:
        fail("6-section", "could not extract any numeric authority headings")
        return

    for rel in tracked_files("*.md", "**/*.md"):
        for lineno, line in enumerate(read(rel).splitlines(), start=1):
            for section, label in unresolved_section_refs(line, sections):
                fail("6-section", f"{rel}:{lineno} references §{section}, which is not a section of {label}")


def check_7_phase_labels() -> None:
    for rel in tracked_files("*.md", "**/*.md"):
        for lineno, line in enumerate(read(rel).splitlines(), start=1):
            m = AUDIT_LETTER_PHASE_RE.search(line)
            if m:
                fail(
                    "7-phase",
                    f"{rel}:{lineno} attributes lettered Phase {m.group(1).upper()} to the audit; "
                    "lettered phases belong to the profile directive",
                )


def check_8_links_resolve() -> None:
    link_re = re.compile(r"\]\(([^)]+)\)")
    for rel in tracked_files("*.md"):
        base = (REPO / rel).parent
        text = read(rel)
        for target in link_re.findall(text):
            target = target.split(" ", 1)[0].strip()              # drop optional link titles
            if re.match(r"^(https?:|mailto:|#)", target):
                continue
            path = target.split("#", 1)[0]                        # drop anchors
            if not path:
                continue
            if not (base / path).exists():
                fail("8-link", f"{rel}: broken repo-relative link -> {target}")
    # CLAUDE.md @imports
    for rel in tracked_files("CLAUDE.md", "**/CLAUDE.md"):
        for m in re.findall(r"^@(\S+)", read(rel), re.M):
            if not (REPO / m).exists():
                fail("8-link", f"{rel}: @import does not resolve -> {m}")


def bare_cycle_ids(line: str) -> list[str]:
    """Bare per-cycle FF-/F- ids on `line`; lines carrying the ignore marker pass."""
    if BARE_ID_IGNORE in line:
        return []
    return BARE_ID_RE.findall(line)


def check_9_bare_cycle_ids() -> None:
    for rel in tracked_files():
        if rel in BARE_ID_EXEMPT_FILES or rel.startswith(BARE_ID_EXEMPT_DIRS):
            continue
        try:
            text = read(rel)
        except UnicodeDecodeError:  # pragma: no cover - no binary surfaces today
            continue
        for lineno, line in enumerate(text.splitlines(), start=1):
            for token in bare_cycle_ids(line):
                fail(
                    "9-bare-id",
                    f"{rel}:{lineno} cites the per-cycle id {token} bare; cycle-qualify it "
                    f'(YYYY-MM-DD/{token}, per MANIFEST.md "Identifier convention") or, if it '
                    f"is genuinely cycle-free, mark the line with {BARE_ID_IGNORE!r}",
                )


def authority_hashes() -> dict[str, str]:
    """sha256 of each authority text's bytes — the binding targets for check 10."""
    return {
        rel: hashlib.sha256((REPO / rel).read_bytes()).hexdigest()
        for rel in ("audit-spec.md", "profile-directive.md")
    }


def binding_line(derived: str, h: dict[str, str]) -> str:
    """The canonical wire format for one binding line (the format BINDING_LINE_RE parses)."""
    return (
        f"{derived} @ audit-spec.md=sha256:{h['audit-spec.md']}"
        f" profile-directive.md=sha256:{h['profile-directive.md']}"
    )


def stale_hash_bindings(manifest_text: str, current: dict[str, str]) -> list[str]:
    """Missing, stale, duplicate, or unrecognized MANIFEST.md binding lines (P-013, ADR 0003).

    Every file in HASH_BOUND_DERIVED needs exactly one line of the form
    `<derived> @ audit-spec.md=sha256:<64hex> profile-directive.md=sha256:<64hex>`
    whose hashes equal the current authority hashes. A mismatch means an authority text
    changed without that derived file being re-synced and re-attested. Duplicate lines
    for one derived file fail (a stale line must never be masked by a fresher one below
    it), and a binding-shaped line for a file outside the bound set fails (it would look
    mechanically checked while never being checked).
    """
    rows: dict[str, tuple[str, str]] = {}
    problems = []
    for raw in manifest_text.splitlines():
        m = BINDING_LINE_RE.match(raw.strip())
        if not m:
            continue
        derived = m.group("derived")
        if derived in rows:
            problems.append(f"{derived}: duplicate binding line — keep exactly one per derived file")
        rows[derived] = (m.group("spec"), m.group("directive"))
        if derived not in HASH_BOUND_DERIVED:
            problems.append(
                f"{derived}: binding line for a file outside the bound set — add it to "
                "HASH_BOUND_DERIVED in scripts/check_drift.py or remove the line"
            )
    for derived in HASH_BOUND_DERIVED:
        if derived not in rows:
            problems.append(f'{derived}: no binding line in MANIFEST.md "Content-hash binding"')
            continue
        for label, recorded in zip(("audit-spec.md", "profile-directive.md"), rows[derived]):
            if recorded != current[label]:
                problems.append(
                    f"{derived}: bound to a stale {label} hash — re-sync the derived file, "
                    "then re-attest (python3 scripts/check_drift.py --print-bindings)"
                )
    return problems


def check_10_hash_bindings() -> None:
    for problem in stale_hash_bindings(read("MANIFEST.md"), authority_hashes()):
        fail("10-hash-bind", problem)


def print_bindings() -> int:
    """Emit the current, correct MANIFEST.md binding lines (used to re-attest at a cut).

    The emitted lines REPLACE the previous ones in MANIFEST.md — duplicates fail check 10.
    """
    h = authority_hashes()
    for derived in HASH_BOUND_DERIVED:
        print(binding_line(derived, h))
    return 0


def self_test() -> int:
    """In-memory negative tests for the resolver and the gate-hardening rules.

    Group 1 covers the authority-aware §-reference resolver (self-audit
    2026-06-08/FF-001). It guards the 2026-06-08/F-001 regression directly: a
    §-reference attributed to one authority text but naming a section that exists only
    in the other must be caught, while correctly-attributed, bare, ambiguous, and
    ignore-marked references must pass. Groups 2-4 cover the 2026-06-10 gate-hardening
    rules (ADR 0003 follow-through): the bare-cycle-id rule (check 9), the AGENTS.md
    schema-identifier literal check (check 3), and the content-hash binding (check 10).
    NOT covered (exercised only by the live checks): phase-label attribution (check 7),
    stale-filename matching (check 5), link/@import resolution (check 8), and the
    heading extractor feeding check 6.
    Wired into pre-commit as its own hook so the negative tests can never silently rot.
    Test ids are assembled by concatenation so this file never carries a bare id itself.
    """
    ok = True

    def run(group: str, cases: list[tuple[object, object, str]]) -> None:
        nonlocal ok
        print(f"  -- {group}")
        for got, expect, note in cases:
            if got != expect:
                ok = False
            print(f"  [{'PASS' if got == expect else 'FAIL'}] expect={expect!s:5} got={got!s:5} :: {note}")

    sections = {
        "audit-spec.md": {"0", "10", "11.3", "11.6", "11.12"},
        "profile-directive.md": {"0", "5", "11", "13"},
    }
    sections["__merged__"] = sections["audit-spec.md"] | sections["profile-directive.md"]
    ref_cases = [
        ("the profile directive §11.12 mapping", True, "wrong-authority: spec-only section cited as directive"),
        ("the default mapping from §11.12 of `audit-spec.md`", False, "real consumer line; spec section, spec named"),
        ("audit spec §13 is the rule", True, "wrong-authority: directive-only section cited as spec"),
        ("a bare §11.12 reference", False, "no authority named -> merged fallback"),
        ("profile directive §13 says so", False, "directive section, directive named"),
        ("profile directive §11.12 and audit-spec.md §11.12", False, "both named -> merged fallback"),
        ("this cites §99.9, which is nowhere", True, "genuinely unresolved section"),
        ("keep §11.12 here  drift-check: ignore-section-ref", False, "explicit ignore marker"),
        # Pinned intentional boundaries: ambiguous short forms and the long-form name are
        # NOT bound to an authority — they fall through to the merged existence check.
        ("the directive §11.12 mapping", False, "short form 'the directive' is ambiguous -> merged fallback (intentional)"),
        ("the spec §13 says so", False, "short form 'the spec' is ambiguous -> merged fallback (intentional)"),
        ("Project Profile Discovery Directive §11.12", False, "long-form name not bound -> merged fallback (intentional)"),
    ]
    run(
        "§-reference resolver (2026-06-08/FF-001)",
        [(bool(unresolved_section_refs(line, sections)), expect, note) for line, expect, note in ref_cases],
    )

    ff, f_id = "FF-" + "004", "F-" + "012"
    run("bare-cycle-id rule (check 9)", [
        (bool(bare_cycle_ids(f"the {ff} linter")), True, "bare FF id -> flagged"),
        (bool(bare_cycle_ids(f"the 2026-06-07/{ff} linter")), False, "cycle-qualified id -> passes"),
        (bool(bare_cycle_ids(f"finding {f_id} reopened")), True, "bare F id -> flagged"),
        (bool(bare_cycle_ids(f"keep {ff} here  {BARE_ID_IGNORE}")), False, "explicit ignore marker"),
        (bool(bare_cycle_ids("template forms FF-NNN / F-NNN")), False, "template letters, never digits"),
    ])

    directive_stub = '  directive_version: "project-profile-directive-v9.9"\n  audit_spec_target: "agentic-audit-spec-v3.1"\n'
    quotes_both = 'stub: `"project-profile-directive-v9.9"` and `"agentic-audit-spec-v3.1"`'
    stale_one = 'stub: `"project-profile-directive-v9.8"` and `"agentic-audit-spec-v3.1"`'
    run("AGENTS.md literal currency (check 3)", [
        (len(missing_agents_literals(directive_stub, quotes_both)), 0, "both literals quoted -> passes"),
        (len(missing_agents_literals(directive_stub, stale_one)), 1, "stale directive_version literal -> flagged"),
        (len(missing_agents_literals(directive_stub, "no literals here")), 2, "both literals missing -> flagged"),
        (len(missing_agents_literals("no parseable keys", quotes_both)), 2, "unparseable directive -> flagged, not skipped"),
    ])

    cur = {"audit-spec.md": "a" * 64, "profile-directive.md": "b" * 64}
    stale = {"audit-spec.md": "f" * 64, "profile-directive.md": cur["profile-directive.md"]}

    def binding_block(stale_for: str = "", drop: str = "") -> str:
        return "\n".join(
            binding_line(derived, stale if derived == stale_for else cur)
            for derived in HASH_BOUND_DERIVED
            if derived != drop
        )

    kickoff = HASH_BOUND_DERIVED[0]
    masked = binding_line(kickoff, stale) + "\n" + binding_block()  # stale row above a fresh one
    run("content-hash binding (check 10)", [
        (len(stale_hash_bindings(binding_block(), cur)), 0, "all bindings current -> passes"),
        (len(stale_hash_bindings(binding_block(stale_for=kickoff), cur)), 1, "one stale authority hash -> flagged"),
        (len(stale_hash_bindings(binding_block(drop=kickoff), cur)), 1, "missing binding line -> flagged"),
        (len(stale_hash_bindings("", cur)), len(HASH_BOUND_DERIVED), "no binding block -> every derived file flagged"),
        (len(stale_hash_bindings(masked, cur)), 1, "duplicate row -> flagged even when the later row is fresh"),
        (len(stale_hash_bindings(binding_block() + "\n" + binding_line("companions/rogue.md", cur), cur)), 1,
         "binding line outside the bound set -> flagged"),
        (bool(BINDING_LINE_RE.match(binding_line(kickoff, cur))), True,
         "print-bindings format round-trips through the parser"),
    ])

    print(
        "drift-linter self-test PASSED (2026-06-08/FF-001 resolver + 2026-06-10 gate-hardening rules)"
        if ok
        else "drift-linter self-test FAILED"
    )
    return 0 if ok else 1


def main() -> int:
    if "--self-test" in sys.argv:
        return self_test()
    if "--print-bindings" in sys.argv:
        return print_bindings()
    authority = parse_authority()
    if authority["spec_ver"] and authority["dir_ver"]:
        print(
            f"Source of truth: spec {authority['spec_ver']} ({authority['spec_date']}), "
            f"directive {authority['dir_ver']} ({authority['dir_date']})"
        )
    check_1_title_agreement(authority)
    check_2_manifest_authority(authority)
    check_3_current_targets(authority)
    check_4_no_conflicting_versions(authority)
    check_5_old_filenames()
    check_6_section_refs_resolve()
    check_7_phase_labels()
    check_8_links_resolve()
    check_9_bare_cycle_ids()
    check_10_hash_bindings()

    if failures:
        print(f"\n2026-06-07/FF-004 drift check FAILED — {len(failures)} issue(s):")
        for f in failures:
            print(f"  - {f}")
        return 1
    print("2026-06-07/FF-004 drift check passed — companions and cross-references are consistent.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
