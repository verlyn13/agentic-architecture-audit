# Manifest

**Status:** Drift-control manifest for the Agentic Architecture Audit package.

This manifest records the intended relationship among the files in this package and
the procedure that keeps them from drifting apart. The authority texts are the profile
directive and the audit specification. The companion documents are derived guidance and
must be updated when the authority texts change. **If a companion document conflicts with
an authority text, the authority text wins.**

## Authority texts

| File | Role | Current target |
| --- | --- | --- |
| `profile-directive.md` | Profile snapshot authority | Project Profile Discovery Directive v1.4, 2026-06-07 |
| `audit-spec.md` | Audit authority | Agentic Architecture Audit Specification v3.3, 2026-06-08 |

## Derived companions

| File | Role | Must target |
| --- | --- | --- |
| `companions/kickoff-prompt.md` | Copy/paste operational prompt for audit agents | Audit Spec v3.3 and Profile Directive v1.4 |
| `companions/explainer.md` | Operator-facing explainer | Audit Spec v3.3 and Profile Directive v1.4 |
| `.agents/skills/run-agentic-audit/SKILL.md` | Cross-agent skill entry point for running the audit | Defers to `companions/kickoff-prompt.md` (no independent version) |

## Versioning

The package version (see `CHANGELOG.md` and the git tags) tracks the directive set as a
whole. Each authority text also declares its own version inside its header.

- A change to an authority text bumps the package **minor** or **major**.
- A companion-only edit bumps the package **patch**.
- Every release is tagged. The tag message names the contained authority versions.

## Not bundled

| Item | Treatment |
| --- | --- |
| Research brief used for the 2026 modernization of the directive set | Input evidence only, not an authority text; intentionally not bundled. |
| Supporting source material from the original working directory | Not bundled and not consumed by a run unless separately transcribed or cited. |

Project agents should not treat the research inputs as operational authority during a run.

## Drift check

Before publishing a new package revision:

1. Confirm `profile-directive.md` and `audit-spec.md` declare the intended versions and dates.
2. Confirm `companions/kickoff-prompt.md` and `companions/explainer.md` declare the same
   target authority versions.
3. Search all markdown files for stale prior-version references, old filenames, and
   outdated section numbers.
4. Confirm companion documents do not introduce rules that contradict the authority texts.
5. If an authority text changes behavior, update this manifest, the companions, and
   `CHANGELOG.md` in the same revision.

Steps 1–3 and cross-reference resolution are **automated** by `scripts/check_drift.py`, a
pre-commit hook that also runs in CI (the hygiene workflow runs `pre-commit run --all-files`).
Steps 4–5 remain human review.

This package is expected to pass the profile directive's Phase D (conventions) drift check.
