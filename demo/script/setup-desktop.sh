#!/usr/bin/env bash
# setup-desktop.sh — One-command setup for the Claude Desktop demo.
#
# Auto-detects paths based on where this script lives. Run from anywhere:
#   bash /path/to/demo/script/setup-desktop.sh
#
# What it does:
#   1. Verifies prerequisites (uv, claude CLI, Claude Desktop)
#   2. Writes MCP server config to Claude Desktop (absolute paths)
#   3. Copies skills into Claude Desktop's global skills folder
#   4. Generates paste-ready agent templates for Verifier + Drafter windows
#   5. Loads document data (from cache if available)

set -euo pipefail

GREEN='\033[0;32m'
YELLOW='\033[0;33m'
CYAN='\033[0;36m'
BOLD='\033[1m'
RESET='\033[0m'

ok()   { echo -e "  ${GREEN}✓${RESET} $1"; }
warn() { echo -e "  ${YELLOW}⚠${RESET} $1"; }
step() { echo -e "\n${GREEN}==>${RESET} $1"; }

# --- Resolve absolute paths from script location ---
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
DEMO_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
PROJECT_ROOT="$(cd "$DEMO_DIR/.." && pwd)"
MCP_SCRIPT="$PROJECT_ROOT/.agents/bin/document-mcp-server.py"
SKILLS_SRC="$DEMO_DIR/.claude/skills"
AGENTS_DIR="$DEMO_DIR/.agents"
DESKTOP_CONFIG="$HOME/Library/Application Support/Claude/claude_desktop_config.json"
DESKTOP_SKILLS="$HOME/Library/Application Support/Claude/skills"

echo -e "${BOLD}Document Review Demo — Desktop Setup${RESET}"
echo ""
echo "  Project root:  $PROJECT_ROOT"
echo "  Demo dir:      $DEMO_DIR"
echo "  MCP script:    $MCP_SCRIPT"

# -------------------------------------------------------------------
step "1/6 — Verify prerequisites"

command -v uv >/dev/null 2>&1 || { echo "uv not found. Install: curl -LsSf https://astral.sh/uv/install.sh | sh"; exit 1; }
ok "uv found"

command -v claude >/dev/null 2>&1 || { warn "claude CLI not found (optional for Desktop-only setup)"; }
[ -z "${_claude_missing:-}" ] && ok "claude CLI found"

if [ -d "/Applications/Claude.app" ]; then
    ok "Claude Desktop found"
else
    warn "Claude Desktop not found at /Applications/Claude.app"
    echo "    Install: brew install --cask claude"
fi

# -------------------------------------------------------------------
step "2/6 — MCP server config"

if [ ! -f "$MCP_SCRIPT" ]; then
    warn "MCP server script not found at: $MCP_SCRIPT"
    echo "    The MCP tools won't work until this file exists."
else
    ok "MCP server script found"
fi

# Project-level .mcp.json (for Claude Code — uses relative path)
if [ -f "$DEMO_DIR/.mcp.json" ]; then
    ok "Project .mcp.json exists"
else
    warn ".mcp.json not found — creating..."
    cat > "$DEMO_DIR/.mcp.json" << 'EOF'
{
  "mcpServers": {
    "document-review": {
      "command": "uv",
      "args": [
        "run", "--with", "mcp,pymupdf,chromadb,sentence-transformers",
        "../.agents/bin/document-mcp-server.py"
      ]
    }
  }
}
EOF
    ok "Project .mcp.json created"
fi

# Claude Desktop global config (uses absolute path)
mkdir -p "$(dirname "$DESKTOP_CONFIG")"

if [ -f "$DESKTOP_CONFIG" ] && grep -q "document-review" "$DESKTOP_CONFIG" 2>/dev/null; then
    ok "Claude Desktop config already has document-review server"
else
    warn "Adding document-review MCP server to Claude Desktop config..."
    if [ -f "$DESKTOP_CONFIG" ]; then
        python3 -c "
import json, sys
config_path, script_path = sys.argv[1], sys.argv[2]
with open(config_path) as f:
    config = json.load(f)
config.setdefault('mcpServers', {})['document-review'] = {
    'command': 'uv',
    'args': ['run', '--with', 'mcp,pymupdf,chromadb,sentence-transformers', script_path]
}
with open(config_path, 'w') as f:
    json.dump(config, f, indent=2)
" "$DESKTOP_CONFIG" "$MCP_SCRIPT"
        ok "Merged into existing Desktop config"
    else
        cat > "$DESKTOP_CONFIG" << DEOF
{
  "mcpServers": {
    "document-review": {
      "command": "uv",
      "args": ["run", "--with", "mcp,pymupdf,chromadb,sentence-transformers", "$MCP_SCRIPT"]
    }
  }
}
DEOF
        ok "Created Desktop config"
    fi
    warn "Restart Claude Desktop for changes to take effect"
fi

# -------------------------------------------------------------------
step "3/6 — Install skills"

mkdir -p "$DESKTOP_SKILLS"

if [ -d "$SKILLS_SRC" ]; then
    cp -r "$SKILLS_SRC"/* "$DESKTOP_SKILLS/"
    INSTALLED=$(ls -d "$DESKTOP_SKILLS"/*/ 2>/dev/null | wc -l | tr -d ' ')
    ok "Copied $INSTALLED skills to $DESKTOP_SKILLS"
    for skill_dir in "$DESKTOP_SKILLS"/*/; do
        skill_name=$(basename "$skill_dir")
        echo "      - $skill_name"
    done
else
    warn "Skills source not found at $SKILLS_SRC"
fi

# -------------------------------------------------------------------
step "4/6 — Generate agent paste files"

PASTE_DIR="$DEMO_DIR/generated"
mkdir -p "$PASTE_DIR"

# Verifier
if [ -f "$AGENTS_DIR/verification-agent.md" ]; then
    cp "$AGENTS_DIR/verification-agent.md" "$PASTE_DIR/paste-verifier.md"
    ok "Generated: $PASTE_DIR/paste-verifier.md"
else
    warn "verification-agent.md not found"
fi

# Drafter
if [ -f "$AGENTS_DIR/response-drafter-agent.md" ]; then
    cp "$AGENTS_DIR/response-drafter-agent.md" "$PASTE_DIR/paste-drafter.md"
    ok "Generated: $PASTE_DIR/paste-drafter.md"
else
    warn "response-drafter-agent.md not found"
fi

# -------------------------------------------------------------------
step "5/6 — Load document data"

if [ -f "$DEMO_DIR/data/documents.db" ]; then
    COUNT=$(sqlite3 "$DEMO_DIR/data/documents.db" "SELECT COUNT(*) FROM clauses" 2>/dev/null || echo "?")
    ok "Data already loaded ($COUNT clauses)"
elif [ -d "$DEMO_DIR/data-cache/loaded" ]; then
    echo "  Restoring from cache..."
    rm -rf "$DEMO_DIR/data"
    cp -r "$DEMO_DIR/data-cache/loaded" "$DEMO_DIR/data"
    COUNT=$(sqlite3 "$DEMO_DIR/data/documents.db" "SELECT COUNT(*) FROM clauses" 2>/dev/null || echo "?")
    ok "Data restored from cache ($COUNT clauses)"
else
    warn "No data found. Run 'make load' or 'make pre-demo-setup' from $DEMO_DIR"
fi

# -------------------------------------------------------------------
step "6/6 — Summary"

echo ""
echo -e "${BOLD}Setup complete. Resolved paths:${RESET}"
echo ""
echo "  MCP server script:     $MCP_SCRIPT"
echo "  Desktop MCP config:    $DESKTOP_CONFIG"
echo "  Desktop skills dir:    $DESKTOP_SKILLS"
echo "  SQLite database:       $DEMO_DIR/data/documents.db"
echo "  ChromaDB store:        $DEMO_DIR/data/chroma/"
echo ""
echo -e "${BOLD}Next steps:${RESET}"
echo ""
echo "  1. Restart Claude Desktop"
echo "  2. Open a conversation → ask \"what tools do you have?\""
echo "     You should see: load_document, search_document, audit_document, etc."
echo ""
echo -e "  3. ${CYAN}Window A — Verifier${RESET}"
echo "     Open a new conversation. Paste the contents of:"
echo "     ${BOLD}$PASTE_DIR/paste-verifier.md${RESET}"
echo "     into the system instructions (Project settings → Custom instructions)"
echo ""
echo "     Quick copy:  ${CYAN}cat \"$PASTE_DIR/paste-verifier.md\" | pbcopy${RESET}"
echo ""
echo -e "  4. ${CYAN}Window B — Drafter${RESET}"
echo "     Open another new conversation. Paste the contents of:"
echo "     ${BOLD}$PASTE_DIR/paste-drafter.md${RESET}"
echo "     into the system instructions"
echo ""
echo "     Quick copy:  ${CYAN}cat \"$PASTE_DIR/paste-drafter.md\" | pbcopy${RESET}"
echo ""
