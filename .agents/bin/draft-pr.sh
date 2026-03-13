#!/usr/bin/env bash
# Draft PR for a branch. Usage: draft-pr.sh <branch> [base]
set -euo pipefail

BRANCH="${1:?Usage: draft-pr.sh <branch> [base]}"
BASE="${2:-main}"
REPO_ROOT="$(git -C "$(dirname "$0")/../.." rev-parse --show-toplevel)"
cd "$REPO_ROOT"

# Check if PR already exists
EXISTING=$(gh pr list --head "$BRANCH" --json number,url --jq '.[0].url // empty' 2>/dev/null || true)
if [[ -n "$EXISTING" ]]; then
  echo "PR already exists: $EXISTING"
  exit 0
fi

# Ensure remote is up to date
if ! git ls-remote --exit-code origin "$BRANCH" &>/dev/null; then
  echo "Pushing $BRANCH to origin..."
  git push -u origin "$BRANCH"
fi

# Gather context
COMMITS=$(git log "$BASE".."$BRANCH" --oneline)
STAT=$(git diff "$BASE"..."$BRANCH" --stat)
COMMIT_COUNT=$(echo "$COMMITS" | wc -l | tr -d ' ')
FILE_COUNT=$(git diff "$BASE"..."$BRANCH" --name-only | wc -l | tr -d ' ')

# Build title from branch name
TITLE=$(echo "$BRANCH" | sed 's|.*/||; s/-/ /g; s/\b\(.\)/\u\1/g')

# Create draft PR
gh pr create \
  --head "$BRANCH" \
  --base "$BASE" \
  --draft \
  --title "$TITLE" \
  --body "$(cat <<EOF
## Summary

- ${COMMIT_COUNT} commits, ${FILE_COUNT} files changed
- Branch: \`$BRANCH\`

### Commits
\`\`\`
$COMMITS
\`\`\`

### Changed files
\`\`\`
$STAT
\`\`\`

---
Generated with [Claude Code](https://claude.com/claude-code)
EOF
)"
