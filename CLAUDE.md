# CLAUDE.md — working in this repository

@AGENTS.md

The canonical, cross-agent instructions are in `AGENTS.md` (imported above) — read them first.
This file adds only Claude Code-specific notes. **If this file conflicts with `AGENTS.md`,
`AGENTS.md` wins.**

## Claude Code notes

- **Plan first** for multi-file or structural changes; for a single companion edit, proceed but
  still verify hygiene (`pre-commit run --all-files`).
- **Authority texts** (`audit-spec.md`, `profile-directive.md`) are edited only to cut a new
  version. A warn-only `PreToolUse` hook (`.claude/hooks/guard-authority-texts.sh`) reminds you at
  edit time; the project permission budget lives in `.claude/settings.json`. Use a fresh subagent
  or `/code-review` for any structural or authority-text change.
- **Read-only by default** when running the audit on a target — including this repo itself. A real
  run writes only the dated `profile/<date>/` and `audit/<date>/` artifacts (gitignored), never
  source.
- **On context compaction**, preserve: changed files, the hygiene command, the authority versions,
  and any unresolved drift.
- Personal, uncommitted settings belong in `.claude/settings.local.json` (gitignored).
