# Agentic Architecture Audit

A two-stage, evidence-first audit for AI-assisted codebases. You hand it to a coding
agent. It reads your project carefully and reports what is actually there, with file
paths and line numbers, versus what you think is there. It changes nothing.

There are two authority texts.

1. **profile-directive.md** runs first. It produces a dated snapshot of what the repo
   claims to be. Stack, bounded contexts, conventions, agent surfaces, authority baselines.
2. **audit-spec.md** runs second. It tests those claims in eleven phases, from domain
   vocabulary and bounded contexts through contracts, state and memory, authority
   boundaries, observability, prompts, and evals.

The split is deliberate. An agent asked to discover and judge at once will confirm its
own expectations. So one pass states the claims and a separate pass tests them.

Every finding must cite a file, a line range, an excerpt, and the command that produced
it. Findings are ranked by severity, confidence, strategic weight, and reversibility.
The output includes fitness functions: automated rules for CI so the same problem
can't come back.

## Run order

1. Copy this package into or near the target project.
2. Run `profile-directive.md` against the project. Review the snapshot it produces.
3. Start the audit agent with `companions/kickoff-prompt.md`.
4. Read `audit/<date>/SUMMARY.md` first. The detail is there when you want it.

New to this? Start with `companions/explainer.md`. It's the plain-language version.

## Repository layout

| File | Role |
| --- | --- |
| [`profile-directive.md`](profile-directive.md) | **Authority** — Project Profile Discovery Directive v1.5. Run first. |
| [`audit-spec.md`](audit-spec.md) | **Authority** — Agentic Architecture Audit Specification v3.4. Run second. |
| [`AGENTS.md`](AGENTS.md) | Canonical, cross-agent instructions for working in this repo (`CLAUDE.md` imports it). |
| [`CONTRIBUTING.md`](CONTRIBUTING.md) | How to contribute: the quality gate, change workflow, and release/provenance discipline. |
| [`SECURITY.md`](SECURITY.md) | Security scope and private vulnerability reporting. |
| [`companions/explainer.md`](companions/explainer.md) | Plain-language explanation of what the audit does. |
| [`companions/kickoff-prompt.md`](companions/kickoff-prompt.md) | Copy/paste prompt for the audit agent. |
| [`MANIFEST.md`](MANIFEST.md) | Drift control: authority versions and companion targets. |
| [`CHANGELOG.md`](CHANGELOG.md) | Package history and authority-text lineage. |
| [`CITATION.cff`](CITATION.cff) | How to cite this methodology. |
| [`LICENSE`](LICENSE) | Apache-2.0. |
| [`examples/`](examples/README.md) | A real, public run of this audit. |
| [`scripts/check_drift.py`](scripts/check_drift.py) | Drift linter (FF-004): companion/version consistency + link resolution, enforced in CI. |
| [`.agents/skills/`](.agents/skills/run-agentic-audit/SKILL.md) | Portable cross-agent skill: run the audit (a thin wrapper that defers to the kickoff prompt). |

The root holds exactly what has authority. `companions/` makes the authority/derived
distinction physical — a core idea of the package itself.

## Versions

Authority versions are declared inside each text and tracked in `MANIFEST.md`.
Releases are tagged. If a companion document conflicts with an authority text, the
authority text wins.

I developed this by auditing my own agent-built projects. It gets revised when a real
run exposes a weakness. The changelog records those lessons.

Apache-2.0.
