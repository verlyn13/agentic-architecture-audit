# AGENTS.md — working in this repository

Canonical, **cross-agent** instructions for any coding agent (Claude Code, Codex, Cursor,
Copilot, Devin, Gemini CLI, …). Tool-specific files import or defer to this one — e.g.
`CLAUDE.md` imports it. **If a tool-specific file conflicts with this file, this file wins.**

This repo publishes the **Agentic Architecture Audit**: a two-stage, evidence-first audit
methodology for AI-assisted codebases. It is a **documentation package, not an application** —
there is no build, no `src/`, no runtime. The prose is the product.

## What has authority

Two files are **authority texts**. Their content is canonical and stable:

- `audit-spec.md` — Agentic Architecture Audit Specification (version declared in its header).
- `profile-directive.md` — Project Profile Discovery Directive (version declared in its header).

Everything under `companions/` is **derived** guidance, as is the portable cross-agent skill
`.agents/skills/run-agentic-audit/SKILL.md` (a thin wrapper that defers to
`companions/kickoff-prompt.md` and carries no independent version — when the procedure
changes, update the kickoff prompt and keep the skill thin). `MANIFEST.md` records the
authority/derived mapping and the drift-control procedure. **If a companion ever conflicts with
an authority text, the authority text wins** — fix the companion, never the authority text.

Authority-text cuts are recorded as ADRs in `adr/` (numbered, kebab-case, following the
established header and section order). Reversing a recorded decision requires a superseding
ADR.

## Setup and checks

There is no build, install step, or test suite. The single quality gate is repo hygiene:

- `pre-commit run --all-files` — also enforced in CI (`.github/workflows/hygiene.yml`).
- Optional local install: `pipx install pre-commit && pre-commit install`.
- The gate includes the companion/version drift linter (`python3 scripts/check_drift.py`,
  self-audit 2026-06-07/FF-004) and its negative self-test (`python3 scripts/check_drift.py
  --self-test`, 2026-06-08/FF-001); both run directly with plain `python3` when diagnosing a
  failure. A drift failure means a **content** fix (versions, section refs, links), never a
  formatting fix.
- The linter scans **git-tracked** markdown only — `git add` a new file, then lint, before
  trusting a clean result. Two commit-blocking rules to know up front: a line that names
  exactly one authority text binds every section reference on that line to that text's real
  headings, and a lettered (profile-directive) phase described as an audit phase is flagged.
  The full convention — lettered phases belong to the profile directive, numbered phases to
  the audit spec, never attribute one text's phase style to the other — holds in both
  directions, but only the lettered-as-audit direction is mechanically gated.

## Editing discipline (read before changing anything)

1. **Do not rewrite the authority texts.** They are revised deliberately and version-bumped in
   their own headers; a revision is a considered event, not a cleanup. Genuine errors aside, do
   not reword, restructure, or "improve" `audit-spec.md` or `profile-directive.md` without an
   explicit instruction to cut a new version of that text. (A warn-only edit-time hook reminds
   you; `CODEOWNERS` requests review.)
2. **Filenames are stable; versions live inside.** Never rename the authority or companion files.
   Versions are declared in headers and carried by signed git tags, never in filenames.
3. **Cross-references are canonical and repo-relative.** Root files by bare name (`audit-spec.md`,
   `profile-directive.md`, `MANIFEST.md`); companions with the prefix
   (`companions/kickoff-prompt.md`, `companions/explainer.md`). Keep it consistent —
   inconsistency is exactly the drift this package teaches you to catch.
4. **The YAML schema identifiers are not filenames.** In `profile-directive.md`,
   `directive_version` (currently `"project-profile-directive-v1.5"` — it tracks the
   directive's header version at each cut) and `audit_spec_target` (pinned at
   `"agentic-audit-spec-v3.1"` — the deliberate consumption baseline, per ADR 0002) are
   version identifiers emitted into a profile snapshot. Do **not** rename them to match the
   published filenames, and do **not** "fix" the directive body's v3.1 baseline references
   as drift — they are intentional even though the spec header reads a later version.
5. **Runtime outputs are not repo files.** A real run writes `profile/<date>/...` and
   `audit/<date>/...` *inside the target project being audited*, never here. `.gitignore` excludes
   them. Do not create, "restore," or flag those paths as missing in this repo. (A self-run
   targets this repo, so dated artifacts may exist on disk here — they are legitimate prior-run
   evidence to read, never to commit or delete.)
6. **Review inputs stay untracked.** Improvement/review reports (e.g.
   `improvement-report-<date>-*.md`) are input evidence per `MANIFEST.md` ("Not bundled"):
   keep them out of git (`.gitignore` covers the pattern) and transcribe accepted items
   through an ADR. Do not commit or delete them during a "cleanup".

## Conventions

- **Line endings:** LF everywhere, enforced by `.gitattributes`, `.editorconfig`, and pre-commit.
  Never hand-fix EOLs; discard any pure-EOL diff.
- **Commits:** Conventional Commits (`type(scope): description`), **signed**. A commit-message
  template is provided in `.gitmessage` (wire it once per clone with
  `git config commit.template .gitmessage`).
- **Hooks / CI:** `.pre-commit-config.yaml` runs at commit time; `.github/workflows/hygiene.yml`
  re-runs it on every push and PR. **Never use `--no-verify` or any hook-bypass.**

## Git workflow

- **`main` is protected:** no force-pushes, no deletions, and the hygiene check must pass.
- Work on a branch (`type/short-description`) and open a PR; let CI go green before merging.
- **Do not push to `main` directly, and do not commit or push unless the human asked you to.**
- Use the PR template; keep changes atomic and reviewable.

## Versioning and releases

- A change to an **authority text** bumps the package **minor** or **major**.
- A **companion-only** edit bumps the **patch**.
- Every release is a **signed** git tag whose message names the contained authority versions.
  `CHANGELOG.md` records package history and authority-text lineage. A release also syncs
  `CITATION.cff` (version + date-released) and, for an authority cut, ships the ADR.
- Before any release, run the `MANIFEST.md` drift check (5 steps) and record release
  provenance per evidence lane — the checklist lives in `CONTRIBUTING.md` ("Releasing and
  provenance verification"). This package is expected to pass its own conventions/drift
  check (see `MANIFEST.md`).

## Done means

- Hygiene passes (`pre-commit run --all-files`), or the exact blocker is reported.
- Companions still declare the authority versions recorded in `MANIFEST.md`; cross-references resolve.
- No unrelated reformatting. The final report names changed files, commands run, and any risks.

## Orientation

- New to the methodology? Read `companions/explainer.md` (plain language).
- Running the audit on a project? `companions/kickoff-prompt.md` is the copy/paste prompt; it
  points at the two authority texts.
- A real applied run is linked from `examples/README.md`.
- The published repository is `verlyn13/agentic-architecture-audit`; the local directory name
  (`audit-spec`) is not the repo slug — do not derive GitHub URLs from it.
