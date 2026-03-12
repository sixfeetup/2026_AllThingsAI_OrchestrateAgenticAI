#!/usr/bin/env bash

set -euo pipefail

# Launch Codex with a repo-scoped MCP server configuration for Ralph.
# This avoids mutating the user's global MCP config while still making
# `ralph mcp serve` available whenever Codex is started through this wrapper.
#
# To generalize later:
# - accept multiple named MCP servers from a local config file
# - detect the ralph binary dynamically if it moves
# - support additional repo-local Codex config overlays

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
