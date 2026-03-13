#!/usr/bin/env python3
"""Rebuild presentation/content/*.md slide files from presentation/outline.md."""

import re
import textwrap
from path import Path

REPO = Path(__file__).parent.parent.parent
OUTLINE = REPO / "presentation" / "outline.md"
CONTENT_DIR = REPO / "presentation" / "content"


def slugify(text: str, max_len: int = 40) -> str:
    """Lowercase, spaces to hyphens, strip special chars, max length."""
    slug = text.lower().strip()
    slug = re.sub(r"[^a-z0-9\s-]", "", slug)
    slug = re.sub(r"[\s]+", "-", slug)
    slug = slug.strip("-")
    return slug[:max_len].rstrip("-")


def parse_outline(text: str) -> list[dict]:
    """Parse outline.md into a list of slide dicts."""
    # Split on top-level headings: # [optional NN] title
    slide_pattern = re.compile(r"^# (?:(\d+)\s+)?(.*)", re.MULTILINE)
    matches = list(slide_pattern.finditer(text))

    slides = []
    for i, m in enumerate(matches):
        original_num = m.group(1) or ""
        title = m.group(2).strip()

        # Extract everything after the heading line until the next heading
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        body_raw = text[start:end].strip()

        # Check for YAML frontmatter block (--- ... ---) at the start
        frontmatter = None
        rest = body_raw
        fm_match = re.match(r"^---\n(.*?\n)---\n?(.*)", body_raw, re.DOTALL)
        if fm_match:
            frontmatter = fm_match.group(1).strip()
            rest = fm_match.group(2).strip()

        # Split on ??? for speaker notes
        if "\n???" in rest:
            parts = rest.split("\n???", 1)
            body = parts[0].strip()
            notes = parts[1].strip() if len(parts) > 1 else ""
        elif rest.startswith("???"):
            body = ""
            notes = rest[3:].strip()
        else:
            body = rest
            notes = ""

        slides.append({
            "original_num": original_num,
            "title": title,
            "frontmatter": frontmatter,
            "body": body,
            "notes": notes,
        })

    return slides


def build_slide_md(slide: dict, seq_num: int) -> str:
    """Build the final markdown content for a slide file."""
    nn = f"{seq_num:02d}"
    title = slide["title"]

    # Build frontmatter
    if slide["frontmatter"]:
        fm_lines = slide["frontmatter"]
        # Ensure footer is present
        if "footer:" not in fm_lines:
            fm_lines += f'\nfooter: "{nn}"'
    else:
        if seq_num == 0:
            fm_lines = f'type: title-slide\nfooter: "{nn}"'
        else:
            fm_lines = f'type: content-slide\nfooter: "{nn}"'

    # Body: if empty, use title text
    body = slide["body"]
    if not body.strip():
        body = title

    # Assemble
    parts = [f"---\n{fm_lines}\n---\n"]
    parts.append(f"# {title}\n")
    parts.append(f"{body}\n")

    if slide["notes"]:
        parts.append(f"???\n")
        parts.append(f"{slide['notes']}\n")

    return "\n".join(parts)


def main():
    text = OUTLINE.read_text()
    slides = parse_outline(text)

    # Delete all existing files in content dir
    if CONTENT_DIR.exists():
        for f in CONTENT_DIR.files("*.md"):
            f.remove()
        for f in CONTENT_DIR.files("*.md~"):
            f.remove()
    else:
        CONTENT_DIR.makedirs_p()

    # Write new slide files with sequential numbering
    for seq_num, slide in enumerate(slides):
        nn = f"{seq_num:02d}"
        slug = slugify(slide["title"])
        filename = f"{nn}-{slug}.md"
        filepath = CONTENT_DIR / filename
        content = build_slide_md(slide, seq_num)
        filepath.write_text(content)
        print(f"  wrote {filename}")

    print(f"\n{len(slides)} slides written to {CONTENT_DIR}")


if __name__ == "__main__":
    main()
