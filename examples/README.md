# Examples

This methodology is best understood through a real run, not a synthetic one.

## shelltutor — applied audit cycle (2026-05-21)

[`shelltutor`](https://github.com/verlyn13/shelltutor) is a public project that carries
a real run of this audit. The cycle dated 2026-05-21 produced ranked findings, those
findings were triaged and closed, and seven fitness functions (`FF-001`..`FF-007`) were
adopted into the project's CI. A real run beats a synthetic one, so this links to the
project rather than duplicating its output here.

## What a run produces

A discovery pass runs first. `profile-directive.md` writes `profile/<date>/`:

- `project_profile.yaml` — the machine-readable snapshot the audit consumes.
- `profile-discovery.md` — the discovery narrative and verification record.
- `profile-diff.md` — only when a previous profile exists.

The audit then writes `audit/<date>/`:

- `SUMMARY.md` — the one-page entry point, written last.
- `00-scope.md` … `10.5-finding-smoke-test.md` — the per-phase artifacts.
- `10-findings.md` — ranked findings (`F-NNN`), each with a citation: path, line range,
  evidence excerpt, and the command that produced it.
- `10-fitness-functions.md` — proposed CI rules (`FF-NNN`) so the same problem can't return.
- `00-reference-anchors.json` — pinned protocol, semantic-convention, and companion-doc
  versions used during the run.

The chat is a control plane; the files under `audit/<date>/` are the audit. Read
`SUMMARY.md` first.
