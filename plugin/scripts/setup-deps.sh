#!/usr/bin/env bash
# setup-deps.sh — SessionStart hook that warms the sentence-transformer
# embedding model cache on first run.
#
# Python package dependencies are declared inline in each script via
# PEP 723 metadata and resolved automatically by `uv run`.

set -euo pipefail

PLUGIN_ROOT="${CLAUDE_PLUGIN_ROOT:-.}"
DATA_DIR="${CLAUDE_PLUGIN_DATA:-./data}"
STAMP_FILE="${DATA_DIR}/model-warmed.txt"

mkdir -p "$DATA_DIR"

# Only warm on first run (model cache persists in ~/.cache)
if [ -f "$STAMP_FILE" ]; then
    exit 0
fi

# Warm the embedding model cache (uv reads deps from the script's PEP 723 block)
uv run "${PLUGIN_ROOT}/skills/load-document/warm-model-cache.py" 2>/dev/null || true

echo "warmed" > "$STAMP_FILE"
