#!/usr/bin/env bash

set -euo pipefail

# Launch Codex in a repo-scoped "demo mode".
# This keeps demo-specific config local to the repo and avoids mutating
# the user's global Codex configuration.
#
# Current behavior:
# - enables the Ralph MCP server via `ralph mcp serve`
# - pins Codex to this repository root
#
# To generalize later:
# - source extra config from a repo-local TOML or env file
# - add other demo-only MCP servers
# - add model/profile overrides for rehearsal vs stage use

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"

RALPH_BIN="${RALPH_BIN:-$HOME/.cargo/bin/ralph}"

if [[ ! -x "$RALPH_BIN" ]]; then
  echo "error: ralph binary not found or not executable at ${RALPH_BIN}" >&2
  echo "set RALPH_BIN=/path/to/ralph if it lives elsewhere" >&2
  exit 1
fi

exec codex \
  -C "$REPO_ROOT" \
  -c "mcp_servers.ralph.command=\"${RALPH_BIN}\"" \
  -c 'mcp_servers.ralph.args=["mcp","serve"]' \
  "$@"
