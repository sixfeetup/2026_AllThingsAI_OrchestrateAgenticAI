#!/usr/bin/env bash
# setup-terminal.sh — Install everything needed for the terminal-only demo.
#
# Installs: Homebrew, uv, Python 3.11+, sqlite3, Claude Code CLI,
#           demo venv, embedding model cache.
#
# Usage:  bash demo/script/setup-terminal.sh
# After:  cd demo && make pre-demo-setup && make preflight

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
step "1/6 — Homebrew"
if command -v brew >/dev/null 2>&1; then
    ok "Homebrew found"
else
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    eval "$(/opt/homebrew/bin/brew shellenv 2>/dev/null || /usr/local/bin/brew shellenv 2>/dev/null)"
    ok "Homebrew installed"
fi

# -------------------------------------------------------------------
step "2/6 — uv"
if command -v uv >/dev/null 2>&1; then
    ok "uv found ($(uv --version))"
else
    brew install uv
    ok "uv installed"
fi

# -------------------------------------------------------------------
step "3/6 — Python 3.11+"
PY_OK=$(uv run python -c "import sys; print('ok' if sys.version_info >= (3,11) else 'no')" 2>/dev/null || echo "no")
if [ "$PY_OK" = "ok" ]; then
    ok "Python $(uv run python -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')"
else
    uv python install 3.12
    ok "Python 3.12 installed"
fi

# -------------------------------------------------------------------
step "4/6 — sqlite3"
if command -v sqlite3 >/dev/null 2>&1; then
    ok "sqlite3 found"
else
    brew install sqlite3
    ok "sqlite3 installed"
fi

# -------------------------------------------------------------------
step "5/6 — Claude Code CLI"
if command -v claude >/dev/null 2>&1; then
    ok "Claude Code CLI found"
else
    command -v npm >/dev/null 2>&1 || brew install node
    npm install -g @anthropic-ai/claude-code
    ok "Claude Code CLI installed"
fi

# -------------------------------------------------------------------
step "6/6 — Demo environment + model cache"
cd "$DEMO_DIR"

if [ -f pyproject.toml ]; then
    uv sync
    ok "Demo venv synced"
else
    uv run --with 'pymupdf,chromadb,sentence-transformers,python-docx,openpyxl,mcp,fpdf2,path,pyyaml' \
        python -c "print('all packages importable')"
    ok "Deps cached"
fi

echo "  Downloading embedding model (~90MB on first run)..."
uv run python -c "
from chromadb.utils.embedding_functions import DefaultEmbeddingFunction
DefaultEmbeddingFunction()(['warmup'])
" 2>/dev/null
ok "Model cached"

# -------------------------------------------------------------------
echo ""
echo -e "${GREEN}Terminal setup complete!${RESET}"
echo ""
echo "  Next steps:"
echo "    cd demo"
echo "    make pre-demo-setup    # data snapshots + offline cache"
echo "    make preflight         # verify everything works"
echo ""
