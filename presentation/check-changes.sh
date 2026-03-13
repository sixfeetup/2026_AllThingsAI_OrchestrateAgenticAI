#!/usr/bin/env bash
# Check if watched presentation files have changed since last run.
# Exit 0 = changes detected, exit 1 = no changes.
# Stores hash in .watch-state (gitignored).
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
STATE_FILE="$SCRIPT_DIR/.watch-state"

# Files to watch
WATCHED=(
  "$REPO_ROOT/presentation/outline.md"
  "$REPO_ROOT/README.md"
  "$REPO_ROOT/notes/quotes.md"
)

# Add all slide content files
for f in "$REPO_ROOT/presentation/content/"*.md; do
  [ -f "$f" ] && WATCHED+=("$f")
done

# Also check plan.md and quotes.md at root if they exist
for f in "$REPO_ROOT/plan.md" "$REPO_ROOT/quotes.md"; do
  [ -f "$f" ] && WATCHED+=("$f")
done

# Compute combined hash of all watched files
CURRENT_HASH=""
for f in "${WATCHED[@]}"; do
  if [ -f "$f" ]; then
    CURRENT_HASH+="$(md5 -q "$f" 2>/dev/null || md5sum "$f" | cut -d' ' -f1)"
  fi
done
CURRENT_HASH=$(echo -n "$CURRENT_HASH" | md5 -q 2>/dev/null || echo -n "$CURRENT_HASH" | md5sum | cut -d' ' -f1)

# Compare with stored state
if [ -f "$STATE_FILE" ]; then
  PREV_HASH=$(cat "$STATE_FILE")
  if [ "$CURRENT_HASH" = "$PREV_HASH" ]; then
    exit 1  # no changes
  fi
fi

# Store new hash and signal changes
echo "$CURRENT_HASH" > "$STATE_FILE"
exit 0
