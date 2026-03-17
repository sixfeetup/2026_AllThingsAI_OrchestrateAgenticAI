# /// script
# requires-python = ">=3.11"
# dependencies = ["pyyaml"]
# ///
"""
Build a Reveal.js presentation from outline.md.

Reads presentation/outline.md (pandoc-style markdown with ::: notes blocks
and <demo> blocks), and generates a self-contained Reveal.js deck using
CDN resources and Six Feet Up brand styling.

Output: presentation/output/deck-reveal.html

Usage:
    uv run presentation/build-reveal.py
    uv run presentation/build-reveal.py --root /path/to/repo
    uv run presentation/build-reveal.py --open
"""
import argparse
import re
import sys
import html as html_mod
from datetime import datetime
from pathlib import Path

import yaml


# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
SCRIPT_DIR = Path(__file__).resolve().parent


def _resolve_paths(root: Path | None = None) -> dict:
    repo_root = root.resolve() if root else SCRIPT_DIR.parent
    pres_dir = repo_root / "presentation"
    output_dir = pres_dir / "output"
    return {
        "repo_root": repo_root,
        "pres_dir": pres_dir,
        "outline": pres_dir / "outline.md",
        "output_dir": output_dir,
        "output_file": output_dir / "deck-reveal.html",
    }


def escape(text: str) -> str:
    return html_mod.escape(text)


# ---------------------------------------------------------------------------
# Markdown parsing
# ---------------------------------------------------------------------------
def parse_frontmatter(text: str) -> tuple[dict, str]:
    """Split YAML frontmatter from body."""
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            # Replace tabs with spaces — YAML forbids tabs for indentation
            yaml_text = parts[1].replace("\t", "    ")
            meta = yaml.safe_load(yaml_text) or {}
            body = parts[2].strip()
            return meta, body
    return {}, text.strip()


def split_notes_from_body(body: str) -> tuple[str, str]:
    """Extract ::: notes ... ::: blocks from body.

    Returns (visible_body, notes_text).
    """
    notes_pattern = re.compile(
        r"^::: notes\s*\n(.*?)^:::\s*$",
        re.MULTILINE | re.DOTALL,
    )
    m = notes_pattern.search(body)
    if m:
        notes_text = m.group(1).strip()
        visible = body[:m.start()] + body[m.end():]
        return visible.strip(), notes_text
    return body, ""


def parse_outline(outline_path: Path) -> tuple[dict, list[dict]]:
    """Parse outline.md into deck metadata and a list of slide dicts.

    Each slide dict has keys: title, body, notes, slide_type.
    """
    text = outline_path.read_text()
    deck_meta, text = parse_frontmatter(text)

    # Split on lines that start with '# ' (level-1 heading)
    slide_chunks: list[str] = []
    current: list[str] = []

    for line in text.split("\n"):
        if re.match(r"^# ", line):
            if current:
                slide_chunks.append("\n".join(current))
            current = [line]
        else:
            current.append(line)
    if current:
        slide_chunks.append("\n".join(current))

    slides: list[dict] = []
    for idx, chunk in enumerate(slide_chunks):
        chunk = chunk.strip()

        # Extract title from first # heading
        title = ""
        h_match = re.match(r"^# (.+)$", chunk, re.MULTILINE)
        if h_match:
            title = h_match.group(1)

        # Remove the title line from body
        body = re.sub(r"^# .+\n?", "", chunk, count=1).strip()

        # Extract notes
        body, notes = split_notes_from_body(body)

        slide_type = "title" if idx == 0 else "content"
        slides.append({
            "title": title,
            "body": body,
            "notes": notes,
            "slide_type": slide_type,
        })

    return deck_meta, slides


# ---------------------------------------------------------------------------
# Markdown-to-HTML conversion (lightweight, no external deps)
# ---------------------------------------------------------------------------
def md_to_html(text: str) -> str:
    """Convert markdown text to HTML for Reveal.js slides.

    Handles: headings (##-######), bullet lists, blockquotes,
    fenced code blocks, images, <demo> blocks, inline formatting,
    and plain paragraphs.
    """
    lines = text.split("\n")
    chunks: list[str] = []
    i = 0

    while i < len(lines):
        line = lines[i]

        # --- <demo> block ---
        if line.strip() == "<demo>" or line.strip().startswith("<demo>"):
            demo_lines: list[str] = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith("</demo>"):
                demo_lines.append(lines[i])
                i += 1
            if i < len(lines):
                i += 1  # skip </demo>

            items: list[str] = []
            for dl in demo_lines:
                stripped = dl.strip()
                if stripped.startswith("- "):
                    items.append(stripped[2:])
                elif stripped:
                    items.append(stripped)
            if items:
                li_html = "\n".join(f"<li>{escape(item)}</li>" for item in items)
                inner = f"<ul>\n{li_html}\n</ul>"
            else:
                inner = ""
            chunks.append(f'<div class="demo-block">\n{inner}\n</div>')
            continue

        # --- Fenced code block ---
        fence_match = re.match(r"^```(\w*)$", line)
        if fence_match:
            lang = fence_match.group(1)
            code_lines: list[str] = []
            i += 1
            while i < len(lines) and not lines[i].startswith("```"):
                code_lines.append(lines[i])
                i += 1
            i += 1  # skip closing ```
            lang_attr = f' data-trim data-noescape class="{lang}"' if lang else ""
            code_text = escape("\n".join(code_lines))
            chunks.append(f"<pre><code{lang_attr}>{code_text}</code></pre>")
            continue

        # --- Heading (## through ######, skip # which is slide separator) ---
        h_match = re.match(r"^(#{2,6})\s+(.+)$", line)
        if h_match:
            level = len(h_match.group(1))
            chunks.append(f"<h{level}>{inline_md(h_match.group(2))}</h{level}>")
            i += 1
            continue

        # --- Blockquote ---
        if line.startswith(">"):
            quote_lines: list[str] = []
            while i < len(lines) and lines[i].startswith(">"):
                quote_lines.append(lines[i].lstrip("> ").strip())
                i += 1
            quote_text = " ".join(ql for ql in quote_lines if ql)
            chunks.append(f"<blockquote>{inline_md(quote_text)}</blockquote>")
            continue

        # --- Bullet list ---
        if line.strip().startswith("- "):
            list_items: list[str] = []
            while i < len(lines) and lines[i].strip().startswith("- "):
                list_items.append(lines[i].strip()[2:])
                i += 1
            li_html = "\n".join(f"<li>{inline_md(item)}</li>" for item in list_items)
            chunks.append(f"<ul>\n{li_html}\n</ul>")
            continue

        # --- Image ---
        img_match = re.match(r"^!\[([^\]]*)\]\(([^)]+)\)\s*$", line.strip())
        if img_match:
            alt = escape(img_match.group(1))
            src = escape(img_match.group(2))
            chunks.append(f'<img src="{src}" alt="{alt}" style="max-height: 50vh;">')
            i += 1
            continue

        # --- Plain paragraph ---
        if line.strip():
            para: list[str] = []
            while i < len(lines) and lines[i].strip() and not any([
                re.match(r"^#{1,6}\s", lines[i]),
                lines[i].startswith(">"),
                lines[i].strip().startswith("- "),
                lines[i].startswith("```"),
                lines[i].strip() == "<demo>" or lines[i].strip().startswith("<demo>"),
                re.match(r"^!\[", lines[i].strip()),
            ]):
                para.append(lines[i].strip())
                i += 1
            if para:
                chunks.append(f"<p>{inline_md(' '.join(para))}</p>")
            continue

        # --- Empty line ---
        i += 1

    return "\n".join(chunks)


def inline_md(text: str) -> str:
    """Convert inline markdown (bold, italic, code, links) to HTML."""
    # Escape HTML first
    text = escape(text)
    # Bold: **text** or __text__
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"__(.+?)__", r"<strong>\1</strong>", text)
    # Italic: *text* or _text_
    text = re.sub(r"\*(.+?)\*", r"<em>\1</em>", text)
    text = re.sub(r"(?<!\w)_(.+?)_(?!\w)", r"<em>\1</em>", text)
    # Inline code: `text`
    text = re.sub(r"`(.+?)`", r"<code>\1</code>", text)
    # Links: [text](url)
    text = re.sub(
        r"\[([^\]]+)\]\(([^)]+)\)",
        r'<a href="\2" target="_blank">\1</a>',
        text,
    )
    return text


def notes_to_html(notes: str) -> str:
    """Convert speaker notes (may contain <demo> blocks) to HTML."""
    if not notes:
        return ""
    # Convert the notes markdown, then wrap in <aside>
    html = md_to_html(notes)
    return f'<aside class="notes">\n{html}\n</aside>'


# ---------------------------------------------------------------------------
# Reveal.js HTML template
# ---------------------------------------------------------------------------
def build_reveal_html(deck_meta: dict, slides: list[dict]) -> str:
    """Assemble the full Reveal.js HTML document."""
    title = deck_meta.get("pagetitle", deck_meta.get("title-prefix", "Presentation"))
    author = deck_meta.get("author", "")
    date = deck_meta.get("date", "")

    sections: list[str] = []
    for slide in slides:
        slide_body = md_to_html(slide["body"]) if slide["body"] else ""
        notes_html = notes_to_html(slide["notes"])

        if slide["slide_type"] == "title":
            inner = f'<h1>{inline_md(slide["title"])}</h1>\n{slide_body}'
        else:
            inner = f'<h2>{inline_md(slide["title"])}</h2>\n{slide_body}'

        section = f"<section>\n{inner}\n{notes_html}\n</section>"
        sections.append(section)

    slides_html = "\n\n".join(sections)

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="author" content="{escape(author)}">
    <title>{escape(title)}</title>

    <!-- Fonts: Montserrat + Oswald from Google Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500;600;700;800;900&family=Oswald:wght@300;400;500;600;700&display=swap" rel="stylesheet">

    <!-- Reveal.js core CSS -->
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@5.1.0/dist/reveal.css">
    <!-- Reveal.js highlight plugin CSS -->
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@5.1.0/plugin/highlight/monokai.css">

    <style>
        /* ===========================================
           SIX FEET UP BRAND THEME FOR REVEAL.JS
           =========================================== */

        :root {{
            /* Brand colors */
            --sfu-teal-deep:    #1a6b7a;
            --sfu-teal:         #2a8a9a;
            --sfu-teal-mid:     #3d9eae;
            --sfu-teal-light:   #6dbdcc;
            --sfu-ice:          #b4d4dd;
            --sfu-ice-pale:     #dceef2;

            /* Neutrals */
            --sfu-black:        #1a1a1a;
            --sfu-charcoal:     #2d2d2d;
            --sfu-gray:         #6b7280;
            --sfu-gray-light:   #e5e7eb;
            --sfu-white:        #fafbfc;
        }}

        .reveal {{
            font-family: 'Montserrat', sans-serif;
            font-size: 32px;
            color: var(--sfu-white);
        }}

        .reveal .slides {{
            text-align: left;
        }}

        .reveal .slides section {{
            background: var(--sfu-charcoal);
            padding: 2em;
        }}

        /* First slide (title) gets teal accent */
        .reveal .slides section:first-child {{
            background: linear-gradient(135deg, var(--sfu-teal-deep) 0%, var(--sfu-charcoal) 100%);
        }}

        /* Headings */
        .reveal h1, .reveal h2, .reveal h3, .reveal h4 {{
            font-family: 'Oswald', sans-serif;
            font-weight: 600;
            text-transform: none;
            color: var(--sfu-ice);
        }}

        .reveal h1 {{
            font-size: 2.2em;
            color: var(--sfu-white);
            margin-bottom: 0.4em;
        }}

        .reveal h2 {{
            font-size: 1.6em;
            color: var(--sfu-ice);
            margin-bottom: 0.4em;
        }}

        .reveal h3 {{
            font-size: 1.1em;
            color: var(--sfu-teal-light);
        }}

        /* Body text */
        .reveal p {{
            font-size: 0.85em;
            line-height: 1.6;
            color: rgba(255, 255, 255, 0.8);
        }}

        /* Lists with diamond bullets */
        .reveal ul {{
            list-style: none;
            padding-left: 1.2em;
        }}

        .reveal ul li {{
            margin-bottom: 0.4em;
            font-size: 0.85em;
            line-height: 1.5;
            color: rgba(255, 255, 255, 0.85);
        }}

        .reveal ul li::before {{
            content: '\\25C6';
            color: var(--sfu-teal);
            display: inline-block;
            width: 1em;
            margin-left: -1.2em;
            font-size: 0.7em;
            vertical-align: middle;
        }}

        /* Blockquotes */
        .reveal blockquote {{
            border-left: 4px solid var(--sfu-teal);
            background: rgba(42, 138, 154, 0.1);
            padding: 0.8em 1.2em;
            font-style: italic;
            color: var(--sfu-ice);
            margin: 0.8em 0;
            width: auto;
        }}

        /* Code blocks */
        .reveal pre {{
            background: var(--sfu-black);
            border-radius: 8px;
            border: 1px solid rgba(42, 138, 154, 0.3);
            font-size: 0.55em;
            width: 100%;
        }}

        .reveal code {{
            font-family: 'Menlo', 'Consolas', 'Monaco', monospace;
        }}

        .reveal p code {{
            background: rgba(42, 138, 154, 0.15);
            padding: 0.1em 0.3em;
            border-radius: 4px;
            font-size: 0.9em;
            color: var(--sfu-teal-light);
        }}

        /* Images */
        .reveal img {{
            border: none;
            box-shadow: none;
            max-height: 50vh;
        }}

        /* Links */
        .reveal a {{
            color: var(--sfu-teal-light);
            text-decoration: underline;
        }}

        .reveal a:hover {{
            color: var(--sfu-ice);
        }}

        /* Slide number */
        .reveal .slide-number {{
            font-family: 'Montserrat', sans-serif;
            font-size: 14px;
            color: var(--sfu-gray);
        }}

        /* Progress bar */
        .reveal .progress {{
            color: var(--sfu-teal);
            height: 4px;
        }}

        /* Demo block */
        .demo-block {{
            position: relative;
            background: rgba(217, 158, 46, 0.12);
            border-left: 4px solid #d99e2e;
            border-radius: 0 8px 8px 0;
            padding: 1.5em 1.2em;
            padding-top: 2em;
            margin: 0.8em 0;
            font-family: 'Menlo', 'Consolas', 'Monaco', monospace;
            font-size: 0.7em;
            line-height: 1.6;
            color: rgba(255, 255, 255, 0.85);
        }}

        .demo-block::before {{
            content: 'DEMO';
            position: absolute;
            top: 0.4em;
            left: 0.8em;
            font-family: 'Oswald', sans-serif;
            font-size: 0.65em;
            font-weight: 700;
            letter-spacing: 0.15em;
            text-transform: uppercase;
            color: #d99e2e;
            opacity: 0.9;
        }}

        .demo-block ul {{
            list-style: none;
            padding-left: 1em;
            margin: 0;
        }}

        .demo-block ul li::before {{
            content: '\\25C6';
            color: #d99e2e;
            display: inline-block;
            width: 1em;
            margin-left: -1em;
            font-size: 0.7em;
            vertical-align: middle;
        }}

        /* Speaker notes styling */
        .reveal aside.notes {{
            font-family: 'Montserrat', sans-serif;
        }}

        /* Controls */
        .reveal .controls {{
            color: var(--sfu-teal);
        }}

        /* Background */
        body {{
            background: var(--sfu-black);
        }}
    </style>
</head>
<body>
    <div class="reveal">
        <div class="slides">
{slides_html}
        </div>
    </div>

    <!-- Reveal.js core and plugins from CDN -->
    <script src="https://cdn.jsdelivr.net/npm/reveal.js@5.1.0/dist/reveal.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/reveal.js@5.1.0/plugin/notes/notes.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/reveal.js@5.1.0/plugin/highlight/highlight.js"></script>

    <script>
        Reveal.initialize({{
            hash: true,
            slideNumber: true,
            transition: 'slide',
            plugins: [RevealNotes, RevealHighlight]
        }});
    </script>
</body>
</html>
'''


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(
        description="Build Reveal.js deck from outline.md"
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=None,
        help="Repository root directory (default: parent of presentation/)",
    )
    parser.add_argument(
        "--open",
        action="store_true",
        dest="open_browser",
        help="Open the built deck in the default browser",
    )
    args = parser.parse_args()

    paths = _resolve_paths(args.root)

    if not paths["outline"].exists():
        print("outline.md not found at", paths["outline"])
        sys.exit(1)

    print(f"  Reading {paths['outline']}")
    deck_meta, slides = parse_outline(paths["outline"])
    print(f"  Parsed {len(slides)} slides from outline.md")

    html = build_reveal_html(deck_meta, slides)

    paths["output_dir"].mkdir(exist_ok=True)
    paths["output_file"].write_text(html)
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"  Built Reveal.js deck -> {paths['output_file']}  [{ts}]")

    if args.open_browser:
        import subprocess
        subprocess.run(["open", str(paths["output_file"])])


if __name__ == "__main__":
    main()
