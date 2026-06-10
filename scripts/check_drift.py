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
     the CURRENT authority versions/dates.
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

Exit 0 = clean; exit 1 = drift found (each failure is printed). Stdlib only.
"""

from __future__ import annotations

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


def self_test() -> int:
    """In-memory checks for the authority-aware §-reference resolver (self-audit 2026-06-08/FF-001).

    Guards the 2026-06-08/F-001 regression directly: a §-reference attributed to one authority
    text but naming a section that exists only in the other must be caught, while
    correctly-attributed, bare, ambiguous, and ignore-marked references must pass.
    Wired into pre-commit as its own hook so the negative test can never silently rot.
    """
    sections = {
        "audit-spec.md": {"0", "10", "11.3", "11.6", "11.12"},
        "profile-directive.md": {"0", "5", "11", "13"},
    }
    sections["__merged__"] = sections["audit-spec.md"] | sections["profile-directive.md"]
    cases = [
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
    ok = True
    for line, expect, note in cases:
        flagged = bool(unresolved_section_refs(line, sections))
        if flagged != expect:
            ok = False
        print(f"  [{'PASS' if flagged == expect else 'FAIL'}] expect={expect!s:5} got={flagged!s:5} :: {note}")
    print("2026-06-08/FF-001 self-test PASSED" if ok else "2026-06-08/FF-001 self-test FAILED")
    return 0 if ok else 1


def main() -> int:
    if "--self-test" in sys.argv:
        return self_test()
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

    if failures:
        print(f"\n2026-06-07/FF-004 drift check FAILED — {len(failures)} issue(s):")
        for f in failures:
            print(f"  - {f}")
        return 1
    print("2026-06-07/FF-004 drift check passed — companions and cross-references are consistent.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
