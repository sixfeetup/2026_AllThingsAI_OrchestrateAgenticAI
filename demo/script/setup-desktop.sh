#!/usr/bin/env bash
# setup-desktop.sh — Add Claude Desktop + cowork deps on top of terminal setup.
#
# Run setup-terminal.sh first, then this script.
#
# Installs: Claude Desktop (via Homebrew cask)
# Configures: MCP server for Claude Desktop
#
# Usage:  bash demo/script/setup-desktop.sh
# After:  See demo/script/hybrid-setup.md for window configuration

set -euo pipefail

GREEN='\033[0;32m'
YELLOW='\033[0;33m'
RESET='\033[0m'

ok()   { echo -e "  ${GREEN}✓${RESET} $1"; }
warn() { echo -e "  ${YELLOW}⚠${RESET} $1"; }
step() { echo -e "\n${GREEN}==>${RESET} $1"; }

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
DEMO_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

# -------------------------------------------------------------------
step "1/4 — Verify terminal setup"
command -v uv >/dev/null 2>&1 || { echo "Run setup-terminal.sh first."; exit 1; }
command -v claude >/dev/null 2>&1 || { echo "Run setup-terminal.sh first."; exit 1; }
ok "Terminal deps present"

# -------------------------------------------------------------------
step "2/4 — Claude Desktop"
if [ -d "/Applications/Claude.app" ]; then
    ok "Claude Desktop found"
else
    command -v brew >/dev/null 2>&1 || { echo "Homebrew required. Run setup-terminal.sh first."; exit 1; }
    brew install --cask claude
    ok "Claude Desktop installed"
fi

# -------------------------------------------------------------------
step "3/4 — MCP server config"
if [ -f "$DEMO_DIR/.mcp.json" ]; then
    ok ".mcp.json exists"
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
    ok ".mcp.json created"
fi

# Verify MCP server script can be loaded
cd "$DEMO_DIR"
uv run python -c "
import importlib.util
spec = importlib.util.spec_from_file_location('mcp', '../.agents/bin/document-mcp-server.py')
" 2>/dev/null && ok "MCP server script loadable" || warn "MCP server script has issues"

# -------------------------------------------------------------------
step "4/4 — Verify data is loaded"
if [ -f "$DEMO_DIR/data/documents.db" ]; then
    ok "Data already loaded"
elif [ -d "$DEMO_DIR/data-cache/loaded" ]; then
    echo "  Restoring from cache..."
    cp -r "$DEMO_DIR/data-cache/loaded" "$DEMO_DIR/data"
    ok "Data restored from cache"
else
    warn "No data loaded. Run 'make pre-demo-setup' or 'make load' first"
    echo "  (Claude Desktop MCP tools need data to be loaded before use)"
fi

# -------------------------------------------------------------------
echo ""
echo -e "${GREEN}Desktop setup complete!${RESET}"
echo ""
echo "  Next steps:"
echo "    1. Open Claude Desktop"
echo "    2. Open the demo/ directory as a project"
echo "    3. Verify MCP tools appear (ask 'what tools do you have?')"
echo "    4. See demo/script/hybrid-setup.md for window configuration"
echo ""
