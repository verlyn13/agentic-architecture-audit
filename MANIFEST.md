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
| `profile-directive.md` | Profile snapshot authority | Project Profile Discovery Directive v1.5, 2026-06-09 |
| `audit-spec.md` | Audit authority | Agentic Architecture Audit Specification v3.4, 2026-06-09 |

## Derived companions

| File | Role | Must target |
| --- | --- | --- |
| `companions/kickoff-prompt.md` | Copy/paste operational prompt for audit agents | Audit Spec v3.4 and Profile Directive v1.5 |
| `companions/explainer.md` | Operator-facing explainer | Audit Spec v3.4 and Profile Directive v1.5 |
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
Section-number references are resolved against the **specific** authority text a line names,
so a reference attributed to the wrong authority is caught, not just an unknown number.
Steps 4–5 remain human review.

**Identifier convention:** self-audit fitness-function and finding ids (`FF-NNN`, `F-NNN`)
are **per-cycle** identifiers — each audit cycle starts its own namespace. Any live, undated
surface that outlives its cycle (README, configs, instruction files, commit messages) must
cycle-qualify them, e.g. `2026-06-07/FF-004` (the drift linter) vs `2026-06-08/FF-001` (its
self-test). Dated artifacts carry their cycle context and keep bare ids: cycle outputs,
`CHANGELOG.md` entries, and ADRs (dated by their Status/Source header and frozen once
merged — never retro-edited).
(Adopted 2026-06-10 via `adr/0003-cross-application-review-dispositions.md`; the spec-level
durable-id rule remains a queued proposal.)

This package is expected to pass the profile directive's Phase D (conventions) drift check.

## Release provenance

A release or self-audit must record which claims were verified through which evidence lane
— repo-local, GitHub-hosted, or unavailable — rather than asserting "protected `main`,
green CI, signed commits" as one verified fact. The checklist, with the per-lane facts and
the verifying commands, lives in [`CONTRIBUTING.md`](CONTRIBUTING.md) under "Releasing and
provenance verification."
