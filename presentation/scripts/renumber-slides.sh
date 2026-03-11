#!/bin/zsh
# Renumber slide files sequentially starting from 00 (title).
# Updates both filenames and YAML footer values.
#
# Usage: cd presentation && ./renumber-slides.sh
#        Or: ./presentation/renumber-slides.sh  (from repo root)

set -euo pipefail

CONTENT_DIR="$(cd "$(dirname "$0")" && pwd)/content"
TMPDIR=$(mktemp -d)
trap 'rm -rf "$TMPDIR"' EXIT

# Collect .md files in current sort order (skip backup files)
files=()
for f in "$CONTENT_DIR"/*.md; do
    [[ "$f" == *"~" ]] && continue
    files+=("$f")
done

if (( ${#files[@]} == 0 )); then
    echo "No slides found in $CONTENT_DIR"
    exit 1
fi

echo "Renumbering ${#files[@]} slides..."

# Pass 1: copy to tmpdir with new names to avoid conflicts
n=0
for f in "${files[@]}"; do
    base=$(basename "$f")
    # Strip existing numeric prefix: "04.1-slug.md" → "slug.md", "11.5-slug.md" → "slug.md"
    slug=$(echo "$base" | sed -E 's/^[0-9]+(\.[0-9]+)?-//')
    new_name=$(printf "%02d-%s" "$n" "$slug")
    cp "$f" "$TMPDIR/$new_name"

    # Update footer in the copy
    if (( n == 0 )); then
        # Title slide: remove footer if present
        sed -i '' '/^footer:/d' "$TMPDIR/$new_name"
    else
        num=$(printf "%02d" "$n")
        if grep -q '^footer:' "$TMPDIR/$new_name"; then
            sed -i '' "s/^footer: .*/footer: \"$num\"/" "$TMPDIR/$new_name"
        else
            # Insert footer after the last frontmatter field (before closing ---)
            sed -i '' "/^---$/,/^---$/ { /^---$/! { /^---$/! s/^---$/footer: \"$num\"\n---/; }; }" "$TMPDIR/$new_name" 2>/dev/null || true
        fi
    fi

    old_num=$(echo "$base" | sed -E 's/^([0-9]+(\.[0-9]+)?).*/\1/')
    printf "  %4s → %02d  %s\n" "$old_num" "$n" "$slug"
    (( n++ ))
done

# Pass 2: remove old files, move new ones in
for f in "${files[@]}"; do
    rm "$f"
done
mv "$TMPDIR"/*.md "$CONTENT_DIR/"

echo "Done. $n slides renumbered (00 through $(printf '%02d' $((n-1))))."
