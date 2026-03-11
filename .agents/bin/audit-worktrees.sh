#!/bin/zsh
# Audit all git worktrees: show novel commits and dirty files.
# Usage: ./presentation/audit-worktrees.sh

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

echo "Worktree Audit"
echo "=============="
echo ""

git -C "$REPO_ROOT" worktree list --porcelain | grep '^worktree ' | sed 's/^worktree //' | while read -r wt; do
    # Skip the main worktree
    [[ "$wt" == "$REPO_ROOT" ]] && continue

    branch=$(git -C "$wt" branch --show-current 2>/dev/null || echo "(detached)")
    label=$(basename "$wt")

    # Check for open PR
    pr_info=$(gh pr list --head "$branch" --json number,state,title --jq '.[0] | "#\(.number) \(.state) — \(.title)"' 2>/dev/null || echo "no PR")

    # Count commits ahead of origin/main
    ahead=$(git -C "$wt" rev-list --count "origin/main..$branch" 2>/dev/null || echo "?")

    # Dirty files count
    dirty=$(git -C "$wt" status --short 2>/dev/null | wc -l | tr -d ' ')

    # Verdict
    if [[ "$ahead" == "0" && "$dirty" == "0" ]]; then
        verdict="SAFE TO REMOVE"
    else
        verdict="HAS CONTENT"
    fi

    printf "%-40s  branch: %-30s\n" "$label" "$branch"
    printf "  commits ahead: %-4s  dirty files: %-4s  → %s\n" "$ahead" "$dirty" "$verdict"
    printf "  PR: %s\n" "$pr_info"
    echo ""
done
