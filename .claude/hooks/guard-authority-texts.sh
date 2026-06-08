#!/usr/bin/env bash
# PreToolUse guard — WARN-ONLY, never blocks (always exits 0).
#
# Reminds an agent that audit-spec.md and profile-directive.md are AUTHORITY TEXTS:
# they are revised only as deliberate version-cut events, not casual cleanups
# (see AGENTS.md "Editing discipline"). This converts that prose rule into an
# active reminder at edit time without ever blocking a legitimate version bump.
#
# Reads the PreToolUse JSON payload on stdin; emits a reminder to stderr when the
# target path is an authority text. Parsing failures are harmless: worst case is
# no reminder. It must NEVER exit non-zero, or it would block the tool call.

input="$(cat 2>/dev/null || true)"

# Best-effort extraction of the edited file path (Edit/Write/MultiEdit use file_path).
path="$(printf '%s' "$input" \
  | grep -oE '"file_path"[[:space:]]*:[[:space:]]*"[^"]*"' 2>/dev/null \
  | head -1 \
  | sed -E 's/.*"([^"]*)"$/\1/' 2>/dev/null || true)"

case "$path" in
  *audit-spec.md|*profile-directive.md)
    echo "AUTHORITY-TEXT GUARD: '${path}' is an authority text. Edits are deliberate" >&2
    echo "version-cut events — bump its header version and update MANIFEST.md + CHANGELOG.md" >&2
    echo "in the same change. This is a reminder, not a block (see AGENTS.md)." >&2
    ;;
esac

exit 0
