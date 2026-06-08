#!/usr/bin/env python3
"""FF-004 — companion + version drift linter.

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
  6. Section refs resolve         — §N / §N.N prose references resolve to a
     numeric heading in the authority texts.
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


def authority_sections() -> set[str]:
    sections: set[str] = set()
    for rel in ("audit-spec.md", "profile-directive.md"):
        for line in read(rel).splitlines():
            m = SECTION_HEADING_RE.match(line)
            if m:
                sections.add(m.group(1))
    return sections


def check_6_section_refs_resolve() -> None:
    valid = authority_sections()
    if not valid:
        fail("6-section", "could not extract any numeric authority headings")
        return

    for rel in tracked_files("*.md", "**/*.md"):
        for lineno, line in enumerate(read(rel).splitlines(), start=1):
            if SECTION_REF_IGNORE in line:
                continue
            for m in SECTION_REF_RE.finditer(line):
                section = m.group(1)
                if section not in valid:
                    fail("6-section", f"{rel}:{lineno} references unresolved section §{section}")


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


def main() -> int:
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
        print(f"\nFF-004 drift check FAILED — {len(failures)} issue(s):")
        for f in failures:
            print(f"  - {f}")
        return 1
    print("FF-004 drift check passed — companions and cross-references are consistent.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
