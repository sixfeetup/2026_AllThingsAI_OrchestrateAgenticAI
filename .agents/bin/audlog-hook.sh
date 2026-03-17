#!/usr/bin/env bash
# audlog-hook.sh — PostToolUse hook that logs tool calls to the audit trail.
#
# Called by Claude Code after each tool use. Receives tool info via env vars:
#   TOOL_USE_ID, TOOL_NAME, TOOL_INPUT, TOOL_OUTPUT (JSON strings)
#
# Only logs interesting events (Bash commands, skill invocations).
# Silently no-ops if the DB doesn't exist or the insert fails.

set -euo pipefail

DB="demo/data/contracts.db"

# Bail if no DB yet (contract hasn't been loaded)
[ -f "$DB" ] || exit 0

# Only log tool calls we care about
case "${TOOL_NAME:-}" in
  Bash)
    # Extract the command from TOOL_INPUT JSON
    cmd=$(echo "${TOOL_INPUT:-}" | python3 -c "
import sys, json
try:
    d = json.load(sys.stdin)
    print(d.get('command', '')[:120])
except: pass
" 2>/dev/null)
    [ -z "$cmd" ] && exit 0

    # Skip noisy commands (ls, echo, say, cat, etc.)
    case "$cmd" in
      ls*|echo*|say*|cat*|head*|tail*|pwd*|cd*|which*|readlink*) exit 0 ;;
    esac

    action="tool"
    detail="Bash: $cmd"
    ;;
  Skill)
    skill=$(echo "${TOOL_INPUT:-}" | python3 -c "
import sys, json
try:
    d = json.load(sys.stdin)
    print(d.get('skill', ''))
except: pass
" 2>/dev/null)
    [ -z "$skill" ] && exit 0
    args=$(echo "${TOOL_INPUT:-}" | python3 -c "
import sys, json
try:
    d = json.load(sys.stdin)
    print(d.get('args', '')[:80])
except: pass
" 2>/dev/null)
    action="skill"
    detail="/$skill $args"
    ;;
  Agent)
    desc=$(echo "${TOOL_INPUT:-}" | python3 -c "
import sys, json
try:
    d = json.load(sys.stdin)
    print(d.get('description', '')[:80])
except: pass
" 2>/dev/null)
    action="agent"
    detail="Agent: $desc"
    ;;
  Edit|Write)
    fp=$(echo "${TOOL_INPUT:-}" | python3 -c "
import sys, json
try:
    d = json.load(sys.stdin)
    print(d.get('file_path', '').split('/')[-1])
except: pass
" 2>/dev/null)
    action="edit"
    detail="${TOOL_NAME}: $fp"
    ;;
  *)
    exit 0
    ;;
esac

# Escape single quotes for SQL
detail="${detail//\'/\'\'}"

sqlite3 "$DB" "INSERT INTO audit_log (action, detail, actor) VALUES ('$action', '$detail', 'claude-hook')" 2>/dev/null || true
