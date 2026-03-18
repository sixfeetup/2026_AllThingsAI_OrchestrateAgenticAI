#!/usr/bin/env bash
# Build the document-review plugin from demo skills & agents.
#
# Source of truth: demo/.claude/skills/ and demo/.agents/bin/
# Output: plugins/document-review/ and plugins/document-review.zip
#
# The plugin is an exact copy of the demo pipeline, with two adjustments:
#   1. Path depth in Python scripts (.parent count) — because plugin/bin/
#      is 4 levels below the repo root vs 3 in the demo
#   2. Skill markdown paths — rewritten from demo-relative to project-root
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
DEMO="$REPO_ROOT/demo"
PLUGIN="$REPO_ROOT/plugins/document-review"

# ---- config -----------------------------------------------------------

# Bin scripts to include (from demo/.agents/bin/)
BIN_SCRIPTS=(
    document-load.py
    document-parse.py
    document-search.py
    document-mcp-server.py
    document-eval.py
    document-pipeline.py
)

# Skill mapping: demo_dir → plugin_dir
declare -A SKILL_MAP=(
    [load-document]=document-loader
    [search-document]=document-search
    [eval-document]=document-eval
    [audit-document]=document-audit
    [audlog]=audlog
    [cowork-review]=cowork-review
)

# Python dependencies (from demo/pyproject.toml)
PYTHON_DEPS=(
    pymupdf
    chromadb
    sentence-transformers
    mcp
    python-docx
    openpyxl
)

# ---- clean + scaffold -------------------------------------------------

echo "Building document-review plugin from demo sources..."
echo "  Source:  $DEMO"
echo "  Output:  $PLUGIN"

# Stash plugin.json and README.md before cleaning
tmp_stash="$(mktemp -d)"
for f in .claude-plugin/plugin.json README.md; do
    if [[ -f "$PLUGIN/$f" ]]; then
        mkdir -p "$tmp_stash/$(dirname "$f")"
        cp "$PLUGIN/$f" "$tmp_stash/$f"
    fi
done

rm -rf "$PLUGIN"
mkdir -p "$PLUGIN/.claude-plugin" "$PLUGIN/bin" "$PLUGIN/skills"

# Restore stashed files or generate defaults
if [[ -f "$tmp_stash/.claude-plugin/plugin.json" ]]; then
    cp "$tmp_stash/.claude-plugin/plugin.json" "$PLUGIN/.claude-plugin/plugin.json"
else
    cat > "$PLUGIN/.claude-plugin/plugin.json" <<'PJSON'
{
  "name": "document-review",
  "description": "AI-driven contract and document review pipeline with semantic search, criteria-based evaluation, adversarial verification, and full audit trail.",
  "version": "0.1.0",
  "author": { "name": "Six Feet Up" }
}
PJSON
fi

if [[ -f "$tmp_stash/README.md" ]]; then
    cp "$tmp_stash/README.md" "$PLUGIN/README.md"
fi
rm -rf "$tmp_stash"

# ---- copy bin scripts (with path-depth adjustment) ---------------------
#
# Demo scripts live at demo/.agents/bin/ — 3 .parent calls reaches demo/
# Plugin scripts live at plugins/document-review/bin/ — need 4 .parent
# calls to reach repo root, then descend into demo/
#
# Concrete transforms:
#   .parent.parent.parent / "data"  →  .parent.parent.parent.parent / "demo" / "data"
#   SCRIPT_DIR.parent.parent        →  SCRIPT_DIR.parent.parent.parent / "demo"

echo "  Copying bin scripts..."
for script in "${BIN_SCRIPTS[@]}"; do
    src="$DEMO/.agents/bin/$script"
    if [[ ! -f "$src" ]]; then
        echo "    WARNING: $script not found in demo/.agents/bin/"
        continue
    fi

    # Rule order matters — specific patterns first to avoid double-transform
    sed \
        -e 's|\.parent\.parent\.parent / "data"|.parent.parent.parent.parent / "demo" / "data"|g' \
        -e 's|^DEMO_DIR = SCRIPT_DIR\.parent\.parent$|DEMO_DIR = SCRIPT_DIR.parent.parent.parent / "demo"|' \
        "$src" > "$PLUGIN/bin/$script"

    # Preserve executable bit
    [[ -x "$src" ]] && chmod +x "$PLUGIN/bin/$script"
    echo "    $script"
done

# ---- transform and copy skills ----------------------------------------
#
# Demo skills use paths relative to demo/ (CWD).
# Plugin skills must use paths relative to project root.

echo "  Transforming skills..."
for demo_dir in "${!SKILL_MAP[@]}"; do
    plugin_dir="${SKILL_MAP[$demo_dir]}"
    src="$DEMO/.claude/skills/$demo_dir/skill.md"

    if [[ ! -f "$src" ]]; then
        echo "    WARNING: $demo_dir/skill.md not found"
        continue
    fi

    mkdir -p "$PLUGIN/skills/$plugin_dir"

    sed \
        -e 's|\.agents/bin/|plugins/document-review/bin/|g' \
        -e 's|\bdata/documents\.db|demo/data/documents.db|g' \
        -e 's|\bdata/chroma/|demo/data/chroma/|g' \
        -e 's|\bdata/chroma)|demo/data/chroma)|g' \
        -e 's|\bdata/review-report\.md|demo/data/review-report.md|g' \
        -e 's|\bassets/criteria/|demo/assets/criteria/|g' \
        -e 's|\bassets/1-RFP|demo/assets/1-RFP|g' \
        "$src" > "$PLUGIN/skills/$plugin_dir/SKILL.md"

    echo "    $demo_dir/ → $plugin_dir/SKILL.md"
done

# ---- generate dependency check script ----------------------------------

cat > "$PLUGIN/bin/check-deps.sh" <<'DEPS'
#!/usr/bin/env bash
# Verify prerequisites for the document-review plugin.
set -euo pipefail

ok=true

echo "Checking document-review plugin dependencies..."

# uv
if command -v uv >/dev/null 2>&1; then
    echo "  [ok] uv $(uv --version 2>/dev/null | head -1)"
else
    echo "  [!!] uv not found — install: curl -LsSf https://astral.sh/uv/install.sh | sh"
    ok=false
fi

# Python >= 3.11
if command -v python3 >/dev/null 2>&1; then
    py_ver="$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')"
    if python3 -c 'import sys; exit(0 if sys.version_info >= (3,11) else 1)'; then
        echo "  [ok] Python $py_ver"
    else
        echo "  [!!] Python $py_ver found, need >= 3.11"
        ok=false
    fi
else
    echo "  [!!] python3 not found"
    ok=false
fi

# sqlite3
if command -v sqlite3 >/dev/null 2>&1; then
    echo "  [ok] sqlite3"
else
    echo "  [!!] sqlite3 not found"
    ok=false
fi

# Python packages (test import via uv)
pkgs=(pymupdf chromadb sentence-transformers python-docx openpyxl)
deps_inline="pymupdf,chromadb,sentence-transformers,python-docx,openpyxl"
if uv run --with "$deps_inline" python3 -c "
import pymupdf, chromadb, docx, openpyxl
print('  [ok] Python packages importable')
" 2>/dev/null; then
    :
else
    echo "  [!!] Some Python packages failed to import."
    echo "       Packages needed: ${pkgs[*]}"
    echo "       They will be installed automatically by 'uv run --with' on first use."
    echo "       To pre-install: uv pip install ${pkgs[*]}"
fi

echo ""
if $ok; then
    echo "All prerequisites met."
else
    echo "Some prerequisites are missing — see above."
    exit 1
fi
DEPS
chmod +x "$PLUGIN/bin/check-deps.sh"
echo "  Generated bin/check-deps.sh"

# ---- package zip -------------------------------------------------------

echo "  Packaging zip..."
(cd "$REPO_ROOT/plugins" && zip -qr document-review.zip document-review/)
ZIP_SIZE=$(du -h "$REPO_ROOT/plugins/document-review.zip" | cut -f1 | xargs)
echo "  Created plugins/document-review.zip ($ZIP_SIZE)"

echo ""
echo "Done. Plugin built from demo sources."
echo ""
echo "To verify prerequisites: bash $PLUGIN/bin/check-deps.sh"
