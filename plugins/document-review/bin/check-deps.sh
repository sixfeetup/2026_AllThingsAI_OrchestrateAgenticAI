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
