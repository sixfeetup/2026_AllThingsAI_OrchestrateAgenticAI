#!/usr/bin/env bash
# contain-demo.sh — Move demo-specific scripts into demo/.agents/bin/
# and fix all path references so the demo is self-contained.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
DEMO_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
PROJECT_ROOT="$(cd "$DEMO_DIR/.." && pwd)"

SRC="$PROJECT_ROOT/.agents/bin"
DST="$DEMO_DIR/.agents/bin"

mkdir -p "$DST"

# --- 1. Move demo-specific scripts ---
DEMO_SCRIPTS=(
  document-parse.py
  document-load.py
  document-search.py
  document-mcp-server.py
  test-parse.py
  warm-model-cache.py
  bitrot-simulator.py
  verify-demo.sh
  audlog-hook.sh
)

echo "Moving demo scripts from $SRC → $DST"
for f in "${DEMO_SCRIPTS[@]}"; do
  if [ -f "$SRC/$f" ]; then
    mv "$SRC/$f" "$DST/$f"
    echo "  moved: $f"
  else
    echo "  skip (not found): $f"
  fi
done

# --- 2. Fix skill references: .agents/bin/ → ../.agents/bin/ is WRONG ---
# Skills run from demo/ as cwd. Scripts are now at demo/.agents/bin/.
# So the correct relative path from demo/ is: .agents/bin/
# That's what skills already say — but some had the wrong prefix. Let's standardize.

echo ""
echo "Fixing skill references..."

# load-document: .agents/bin/document-load.py (already correct for demo/ cwd)
# document-search: .agents/bin/document-search.py (already correct)
# document-eval: .agents/bin/document-search.py (already correct)
# These are ALREADY correct now that scripts live in demo/.agents/bin/
echo "  skills: .agents/bin/ refs are now correct (scripts moved to demo/.agents/bin/)"

# Fix document-audit: demo/data/ → data/
sed -i '' 's|demo/data/documents\.db|data/documents.db|g' \
  "$DEMO_DIR/.claude/skills/document-audit/skill.md"
echo "  fixed: document-audit/skill.md (demo/data/ → data/)"

# Fix audlog: demo/data/ → data/
sed -i '' 's|demo/data/documents\.db|data/documents.db|g' \
  "$DEMO_DIR/.claude/skills/audlog/skill.md"
echo "  fixed: audlog/skill.md (demo/data/ → data/)"

# Fix document-eval: demo/assets/ → assets/
sed -i '' 's|demo/assets/|assets/|g' \
  "$DEMO_DIR/.claude/skills/document-eval/skill.md"
echo "  fixed: document-eval/skill.md (demo/assets/ → assets/)"

# Fix document-search: demo/data/ → data/
sed -i '' 's|demo/data/|data/|g' \
  "$DEMO_DIR/.claude/skills/document-search/skill.md"
echo "  fixed: document-search/skill.md (demo/data/ → data/)"

# --- 3. Fix Makefile: ../.agents/bin/ → .agents/bin/ ---
echo ""
echo "Fixing Makefile..."
sed -i '' 's|\.\./\.agents/bin/|.agents/bin/|g' "$DEMO_DIR/Makefile"
echo "  fixed: Makefile (../.agents/bin/ → .agents/bin/)"

# --- 4. Fix .mcp.json: ../.agents/bin/ → .agents/bin/ ---
echo ""
echo "Fixing .mcp.json..."
sed -i '' 's|\.\./\.agents/bin/|.agents/bin/|g' "$DEMO_DIR/.mcp.json"
echo "  fixed: .mcp.json (../.agents/bin/ → .agents/bin/)"

# --- 5. Fix setup-desktop.sh: PROJECT_ROOT → DEMO_DIR for MCP script ---
echo ""
echo "Fixing setup-desktop.sh..."
sed -i '' 's|MCP_SCRIPT="\$PROJECT_ROOT/\.agents/bin/|MCP_SCRIPT="$DEMO_DIR/.agents/bin/|' \
  "$DEMO_DIR/script/setup-desktop.sh"
# Also fix the preflight reference
sed -i '' "s|'../\.agents/bin/document-mcp-server\.py'|'.agents/bin/document-mcp-server.py'|" \
  "$DEMO_DIR/Makefile"
echo "  fixed: setup-desktop.sh MCP_SCRIPT path"

# --- 6. Fix session-auditor-agent: demo/data/ → data/ ---
echo ""
echo "Fixing agent templates..."
sed -i '' 's|demo/data/documents\.db|data/documents.db|g' \
  "$DEMO_DIR/.agents/session-auditor-agent.md"
echo "  fixed: session-auditor-agent.md (demo/data/ → data/)"

# --- 7. Fix CLAUDE.md references ---
echo ""
echo "Fixing CLAUDE.md..."
sed -i '' 's|\.agents/bin/document-mcp-server\.py|demo/.agents/bin/document-mcp-server.py|' \
  "$DEMO_DIR/CLAUDE.md"
echo "  fixed: CLAUDE.md MCP server path"

echo ""
echo "Done. Demo is now self-contained under demo/."
echo ""
echo "Verify:"
echo "  ls $DST/"
echo "  grep -r '\\.\\./.agents/bin' $DEMO_DIR/ --include='*.md' --include='*.sh' --include='*.json' --include='Makefile'"
