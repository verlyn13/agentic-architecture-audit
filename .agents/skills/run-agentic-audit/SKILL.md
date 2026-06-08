---
name: run-agentic-audit
description: Run the Agentic Architecture Audit on a codebase — this package's two-stage, evidence-first methodology (profile discovery, then the eleven-phase audit). Use when asked to audit a repo's agentic architecture, run this audit or spec, profile a project for the audit, or produce profile/<date> and audit/<date> artifacts.
---

# Run the Agentic Architecture Audit

A portable, cross-agent (`.agents/skills`) entry point for running this package's audit on a
target codebase. It is read natively by Codex, Cursor, Copilot, Claude, and Antigravity.

**This skill is a thin wrapper — the authority is the spec, not this file.** It points at the
canonical texts and states the non-negotiables; it deliberately does not restate the methodology.
If this skill ever conflicts with `audit-spec.md`, the spec wins.

## When to use

- "Run the agentic architecture audit / this audit on `<repo>`."
- "Profile this project for the audit" (stage 1 only).
- "Produce the audit findings / `SUMMARY.md` for `<repo>`."

Do **not** use this for fixing or refactoring a repo — the audit is read-only (see below).

## How to run (follow the canonical texts; do not paraphrase them)

1. **Read `audit-spec.md` in full** before acting. It is ~1900 lines and is authoritative.
2. **Stage 1 — profile.** Ensure a profile snapshot exists at `profile/<date>/`. If it is
   missing, run the Project Profile Discovery Directive (`profile-directive.md`) first. The audit
   **halts** if invoked without a profile — that is by design, not an error.
3. **Stage 2 — audit.** Use `companions/kickoff-prompt.md` as the operating prompt. It is the
   copy/paste SOP and points at the two authority texts. Work phase by phase (0 → 10.5 → 11).
4. New to the methodology? Read `companions/explainer.md` first.

## Non-negotiables (enforced by the spec; this is only a reminder checklist)

- **Evidence-first** — every finding cites path + lines + evidence + method. No citation → reject it.
- **Artifacts are the record** — write `audit/<date>/` files; the final chat message is a one-line
  pointer to `SUMMARY.md`. Do not summarize the audit in chat.
- **Read-only** — do not edit source, propose refactors, or "fix things." Remediation is a
  separate directive that runs after the audit ships.
- **Findings vs. fitness functions** stay separate (`F-NNN` vs `FF-NNN`); never merge the IDs.
- **Smoke-test (Phase 10.5)** every finding against the current branch before writing `SUMMARY.md`.
- **Never** use `--no-verify` or any hook-bypass.

## Source of truth

Derived from `companions/kickoff-prompt.md` and the authority texts; it targets the versions
declared in `MANIFEST.md`. Keep this skill thin: when the procedure changes, change the kickoff
prompt and the spec — never let a divergent copy live here.
