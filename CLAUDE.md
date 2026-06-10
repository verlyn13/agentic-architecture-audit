# CLAUDE.md — working in this repository

@AGENTS.md

The canonical, cross-agent instructions are in `AGENTS.md` (imported above) — read them first.
This file adds only Claude Code-specific notes. **If this file conflicts with `AGENTS.md`,
`AGENTS.md` wins.** The `@AGENTS.md` import line is load-bearing: the drift linter validates
`@`-imports, so do not reword or remove it.

## Claude Code notes

- **Plan first** for multi-file or structural changes; for a single companion edit, proceed but
  still verify hygiene (`pre-commit run --all-files`).
- **Permission budget** (`.claude/settings.json`): read-only tools and `pre-commit run` are
  pre-approved; `git commit`/`push`/`tag` and `gh pr` always prompt; `--no-verify`, force-push,
  `rm -rf`, and `.env`/secret reads are denied. Plan around the prompts — any commit/PR step
  needs the operator present.
- **Authority texts** (`audit-spec.md`, `profile-directive.md`) are edited only to cut a new
  version. A warn-only `PreToolUse` hook (`.claude/hooks/guard-authority-texts.sh`) reminds you at
  edit time. Use a fresh subagent or `/code-review` for any structural or authority-text change —
  and `SECURITY.md` scopes `scripts/check_drift.py` and the CI/pre-commit config as
  security-sensitive, so give those the same escalation.
- **Cutting an authority version?** Draft the ADR with the cut; keep its Status line `Proposed`
  until the operator approves. Observe ADR 0001's drafting carve-outs: tool-neutral naming
  (standards may be named normatively, vendor config paths only as examples) and id hygiene
  (cycle-qualify FF ids; never reuse a bare id that collides with the spec's worked examples).
- **Editing `.pre-commit-config.yaml`:** preserve both local hooks (`drift-check` and
  `drift-check-selftest`) — the self-test is a separate hook precisely so the negative test
  cannot silently rot.
- **Read-only by default** when running the audit on a target — including this repo itself. A real
  run writes only the dated `profile/<date>/` and `audit/<date>/` artifacts (gitignored), never
  source.
- **On context compaction**, preserve: changed files, the hygiene command, the authority versions,
  and any unresolved drift.
- Personal, uncommitted settings belong in `.claude/settings.local.json` (gitignored).
