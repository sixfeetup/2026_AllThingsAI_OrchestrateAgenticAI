#!/bin/zsh
# Check if watched files have changed since last run.
# Exit 0 = changed (or first run), Exit 1 = no changes.
#
# Watched files: plan.md, README.md, quotes.md, presentation/content/*.md
# State stored in: presentation/.watch-state

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
STATE_FILE="$REPO_ROOT/presentation/.watch-state"

# Build hash of all watched files
current_hash=$(cat \
    "$REPO_ROOT/plan.md" \
    "$REPO_ROOT/README.md" \
    "$REPO_ROOT/quotes.md" \
    "$REPO_ROOT"/presentation/content/*.md \
    2>/dev/null | md5 -q)

if [[ -f "$STATE_FILE" ]]; then
    previous_hash=$(cat "$STATE_FILE")
    if [[ "$current_hash" == "$previous_hash" ]]; then
        exit 1  # no changes
    fi
fi

# Save new state and signal change
echo "$current_hash" > "$STATE_FILE"
exit 0
