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

Everything under `companions/` is **derived** guidance. `MANIFEST.md` records the
authority/derived mapping and the drift-control procedure. **If a companion ever conflicts with
an authority text, the authority text wins** — fix the companion, never the authority text.

## Setup and checks

There is no build, install step, or test suite. The single quality gate is repo hygiene:

- `pre-commit run --all-files` — also enforced in CI (`.github/workflows/hygiene.yml`).
- Optional local install: `pipx install pre-commit && pre-commit install`.

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
   `directive_version: "project-profile-directive-v1.3"` and
   `audit_spec_target: "agentic-audit-spec-v3.1"` are version identifiers emitted into a profile
   snapshot. Do **not** rename them to match the published filenames.
5. **Runtime outputs are not repo files.** A real run writes `profile/<date>/...` and
   `audit/<date>/...` *inside the target project being audited*, never here. `.gitignore` excludes
   them. Do not create, "restore," or flag those paths as missing in this repo.

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
  `CHANGELOG.md` records package history and authority-text lineage.
- Before any release, run the `MANIFEST.md` drift check (5 steps). This package is expected to
  pass its own conventions/drift check (see `MANIFEST.md`).

## Done means

- Hygiene passes (`pre-commit run --all-files`), or the exact blocker is reported.
- Companions still declare the authority versions recorded in `MANIFEST.md`; cross-references resolve.
- No unrelated reformatting. The final report names changed files, commands run, and any risks.

## Orientation

- New to the methodology? Read `companions/explainer.md` (plain language).
- Running the audit on a project? `companions/kickoff-prompt.md` is the copy/paste prompt; it
  points at the two authority texts.
- A real applied run is linked from `examples/README.md`.
