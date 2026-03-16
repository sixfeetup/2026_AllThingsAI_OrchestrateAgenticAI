#!/usr/bin/env python3
"""Add 'That's roughly...' cultural equivalent column to context-window-explainer.html.

Fixes prior botched inline edit: removes stray <em> tag from CSS block,
reorders columns so cultural equivalent comes before Notes.
"""

from path import Path

REPO = Path(__file__).parent.parent.parent
HTML_FILE = REPO / "presentation" / "explainers" / "context-window-explainer.html"

# Cultural equivalents by size-badge class
EQUIV = {
    "size-badge--2m": "All of Harry Potter + LOTR",
    "size-badge--1m": "The King James Bible",
    "size-badge--200k": "Goblet of Fire",
    "size-badge--128k": "To Kill a Mockingbird",
}


def detect_tier(line: str) -> str | None:
    """Return the tier key if line contains a size-badge span."""
    for key in EQUIV:
        if key in line:
            return key
    return None


def fix_css_corruption(lines: list[str]) -> list[str]:
    """Remove any stray <em>/<td> tags that ended up inside CSS blocks."""
    return [l for l in lines if not (
        "<em>" in l and "font-style:italic" in l and "<td" in l
        and any(lines[max(0, i-3):i] for i in range(len(lines))
                if ".type-badge" in lines[max(0, i-3):i+1].__repr__())
    )]


def main():
    text = HTML_FILE.read_text()
    lines = text.split("\n")

    # Step 1: Remove any stray <td style="font-style:italic"><em>...</em></td>
    # lines that are inside CSS (between <style> and </style>)
    in_style = False
    clean_lines = []
    removed = 0
    for line in lines:
        if "<style>" in line:
            in_style = True
        if "</style>" in line:
            in_style = False
        if in_style and "<td" in line and "<em>" in line:
            removed += 1
            continue
        clean_lines.append(line)
    if removed:
        print(f"  removed {removed} stray tag(s) from CSS block")

    # Step 2: Remove any existing cultural equivalent <td> cells from table rows
    # (from the prior botched edit — these are after the Notes td)
    filtered = []
    for line in clean_lines:
        if 'font-style:italic' in line and '<em>' in line and '<td' in line:
            removed += 1
            continue
        filtered.append(line)
    clean_lines = filtered
    if removed:
        print(f"  cleaned {removed} total stray cultural cells")

    # Step 3: Ensure header has the column (add before Notes if missing)
    # Find the header row and check
    result = []
    for i, line in enumerate(clean_lines):
        result.append(line)
        # After "Type" th, insert "That's roughly..." th before Notes th
        if "<th>Type</th>" in line:
            # Check if next non-whitespace line is already our column
            next_content = clean_lines[i + 1].strip() if i + 1 < len(clean_lines) else ""
            if "roughly" not in next_content:
                indent = "              "
                result.append(f"{indent}<th>That's roughly...</th>")

    clean_lines = result

    # Step 4: Insert cultural equivalent td after type-badge td, before notes td
    result = []
    i = 0
    inserted = 0
    while i < len(clean_lines):
        line = clean_lines[i]
        result.append(line)

        # Detect a size-badge line (the Context column td)
        tier = detect_tier(line)
        if tier:
            # Advance past the type-badge td (next 1-2 lines)
            i += 1
            while i < len(clean_lines):
                result.append(clean_lines[i])
                if "type-badge" in clean_lines[i]:
                    # Insert cultural equivalent td right after
                    indent = "              "
                    result.append(f'{indent}<td><em>{EQUIV[tier]}</em></td>')
                    inserted += 1
                    break
                i += 1

        i += 1

    print(f"  inserted {inserted} cultural equivalent cells")

    HTML_FILE.write_text("\n".join(result))
    print(f"  wrote {HTML_FILE}")


if __name__ == "__main__":
    main()
