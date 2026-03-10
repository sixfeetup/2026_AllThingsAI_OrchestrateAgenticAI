# /// script
# requires-python = ">=3.11"
# dependencies = ["pyyaml"]
# ///
"""
Build presentation deck from markdown slide files.

Reads presentation/content/NN-slug.md files in order,
parses YAML frontmatter + markdown body, and renders
a single self-contained HTML deck to presentation/output/deck.html.

Usage:
    uv run presentation/build.py
    uv run presentation/build.py --watch    # rebuild on file changes
    uv run presentation/build.py --open     # open in browser after build
"""
import re
import sys
import html as html_mod
from pathlib import Path

import yaml


# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
SCRIPT_DIR = Path(__file__).resolve().parent
CONTENT_DIR = SCRIPT_DIR / "content"
OUTPUT_DIR = SCRIPT_DIR / "output"
TEMPLATE_FILE = SCRIPT_DIR / "template.html"
OUTPUT_FILE = OUTPUT_DIR / "deck.html"


# ---------------------------------------------------------------------------
# Markdown-to-slide-HTML parser
# ---------------------------------------------------------------------------
def parse_frontmatter(text: str) -> tuple[dict, str]:
    """Split YAML frontmatter from body."""
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            meta = yaml.safe_load(parts[1]) or {}
            body = parts[2].strip()
            return meta, body
    return {}, text.strip()


def escape(text: str) -> str:
    return html_mod.escape(text)


def render_code_block(lines: list[str], lang: str = "") -> str:
    """Render a fenced code block with syntax highlighting hints."""
    code = "\n".join(lines)
    # Simple keyword highlighting for Python
    if lang in ("python", "py", ""):
        kw = (
            r"\b(async|await|def|class|return|import|from|for|in|if|else|"
            r"elif|while|with|as|try|except|finally|yield|raise|not|and|or)\b"
        )
        escaped = escape(code)
        escaped = re.sub(
            r"(#.*?)$",
            r'<span class="comment">\1</span>',
            escaped,
            flags=re.MULTILINE,
        )
        escaped = re.sub(
            r'(".*?"|\'.*?\')',
            r'<span class="string">\1</span>',
            escaped,
        )
        escaped = re.sub(
            kw, r'<span class="keyword">\1</span>', escaped
        )
        return f'<div class="code-block reveal">{escaped}</div>'
    return f'<div class="code-block reveal"><code>{escape(code)}</code></div>'


def render_grid(cards: list[tuple[str, str]]) -> str:
    """Render a feature-grid with feature-cards."""
    inner = ""
    for title, body in cards:
        inner += (
            f'<div class="feature-card">'
            f"<h3>{escape(title)}</h3>"
            f"<p>{escape(body)}</p>"
            f"</div>\n"
        )
    return f'<div class="feature-grid reveal">\n{inner}</div>'


def render_body(body: str, meta: dict) -> str:
    """Convert markdown body to slide inner HTML."""
    lines = body.split("\n")
    chunks: list[str] = []
    i = 0

    slide_type = meta.get("type", "content-slide")
    is_title = slide_type == "title-slide"
    is_divider = slide_type == "divider-slide"

    while i < len(lines):
        line = lines[i]

        # --- Fenced code block ---
        fence_match = re.match(r"^```(\w*)$", line)
        if fence_match:
            lang = fence_match.group(1)
            code_lines = []
            i += 1
            while i < len(lines) and not lines[i].startswith("```"):
                code_lines.append(lines[i])
                i += 1
            i += 1  # skip closing ```
            chunks.append(render_code_block(code_lines, lang))
            continue

        # --- Grid/card blocks ---
        if line.strip() == ":::grid":
            cards = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith(":::grid"):
                card_match = re.match(r"^:::card\s+(.+)$", lines[i].strip())
                if card_match:
                    card_title = card_match.group(1)
                    card_body_lines = []
                    i += 1
                    while i < len(lines) and lines[i].strip() != ":::":
                        if lines[i].strip():
                            card_body_lines.append(lines[i].strip())
                        i += 1
                    i += 1  # skip closing :::
                    cards.append((card_title, " ".join(card_body_lines)))
                else:
                    i += 1
            i += 1  # skip closing :::grid
            chunks.append(render_grid(cards))
            continue

        # --- Heading ---
        h_match = re.match(r"^#\s+(.+)$", line)
        if h_match:
            title_text = h_match.group(1)
            if is_title:
                chunks.append(
                    f'<h1 class="reveal">{escape(title_text)}</h1>'
                )
            elif is_divider:
                chunks.append(
                    f'<h2 class="reveal">{escape(title_text)}</h2>'
                )
            else:
                chunks.append(
                    f'<h2 class="reveal">{escape(title_text)}</h2>'
                )
            i += 1
            continue

        # --- Blockquote ---
        if line.startswith(">"):
            quote_lines = []
            while i < len(lines) and lines[i].startswith(">"):
                quote_lines.append(lines[i].lstrip("> ").strip())
                i += 1
            quote_text = " ".join(quote_lines)
            chunks.append(
                f'<blockquote class="quote reveal">'
                f"{escape(quote_text)}"
                f"</blockquote>"
            )
            continue

        # --- Bullet list ---
        if line.startswith("- "):
            list_items = []
            while i < len(lines) and lines[i].startswith("- "):
                list_items.append(lines[i][2:].strip())
                i += 1
            items_html = "\n".join(
                f'<li class="reveal">{escape(item)}</li>'
                for item in list_items
            )
            chunks.append(f'<ul class="bullet-list">\n{items_html}\n</ul>')
            continue

        # --- Tagline (italic with *) on title slides ---
        tag_match = re.match(r"^\*(.+)\*$", line.strip())
        if tag_match:
            text = tag_match.group(1)
            if is_title:
                chunks.append(f'<p class="tagline reveal">{escape(text)}</p>')
            else:
                chunks.append(
                    f"<p class=\"reveal\" "
                    f'style="font-style: italic;">'
                    f"{escape(text)}</p>"
                )
            i += 1
            continue

        # --- Subtitle (italic with _) ---
        sub_match = re.match(r"^_(.+)_$", line.strip())
        if sub_match:
            text = sub_match.group(1)
            if is_title:
                chunks.append(
                    f'<p class="subtitle reveal">{escape(text)}</p>'
                )
            elif is_divider:
                chunks.append(
                    f'<p class="subtitle reveal" '
                    f'style="color: rgba(255,255,255,0.7);">'
                    f"{escape(text)}</p>"
                )
            else:
                chunks.append(
                    f'<p class="subtitle reveal">{escape(text)}</p>'
                )
            i += 1
            continue

        # --- Attribution line (starts with —) ---
        attr_match = re.match(r"^—\s*(.+)$", line.strip())
        if attr_match:
            chunks.append(
                f'<p class="quote-attribution reveal">'
                f"— {escape(attr_match.group(1))}</p>"
            )
            i += 1
            continue

        # --- Plain paragraph ---
        if line.strip():
            para_lines = []
            while i < len(lines) and lines[i].strip() and not any([
                lines[i].startswith("#"),
                lines[i].startswith(">"),
                lines[i].startswith("- "),
                lines[i].startswith("```"),
                lines[i].startswith(":::"),
                lines[i].startswith("*") and lines[i].endswith("*"),
                lines[i].startswith("_") and lines[i].endswith("_"),
                lines[i].startswith("—"),
            ]):
                para_lines.append(lines[i].strip())
                i += 1
            if para_lines:
                text = " ".join(para_lines)
                chunks.append(
                    f'<p class="reveal" style="font-size: var(--body-size); '
                    f'color: rgba(255,255,255,0.6);">{escape(text)}</p>'
                )
            continue

        # --- Empty line, skip ---
        i += 1

    return "\n".join(chunks)


def wrap_with_image(inner_html: str, meta: dict) -> str:
    """Wrap rendered body HTML with image layout if specified."""
    image = meta.get("image")
    layout = meta.get("image_layout", "")
    alt = escape(meta.get("image_alt", ""))

    if not image:
        return inner_html

    img_tag = f'<img src="{escape(image)}" alt="{alt}" class="slide-image"'

    if layout == "split":
        # Extract heading from inner_html to keep it outside the split
        heading = ""
        rest = inner_html
        h_match = re.match(r"(<h[12][^>]*>.*?</h[12]>)\s*", inner_html)
        if h_match:
            heading = h_match.group(1)
            rest = inner_html[h_match.end():]

        slide_type = meta.get("type", "")
        shadow = ""
        if slide_type in ("dark-slide", "divider-slide"):
            shadow = (
                ' style="border-radius: 12px; '
                'box-shadow: 0 8px 24px rgba(0,0,0,0.4);"'
            )

        return (
            f"{heading}\n"
            f'<div class="split-layout reveal">\n'
            f'<div class="split-text">\n{rest}\n</div>\n'
            f'<div class="split-image">\n'
            f"{img_tag}{shadow}>\n</div>\n</div>"
        )

    if layout == "inline":
        # Insert image right after heading
        heading = ""
        rest = inner_html
        h_match = re.match(r"(<h[12][^>]*>.*?</h[12]>)\s*", inner_html)
        if h_match:
            heading = h_match.group(1)
            rest = inner_html[h_match.end():]
        return (
            f"{heading}\n"
            f'{img_tag} style="width: 100%; object-fit: cover; '
            f"border-radius: 8px; "
            f'margin-bottom: clamp(0.3rem, 0.5vw, 0.5rem);"'
            f' class="slide-image inline reveal">\n'
            f"{rest}"
        )

    if layout == "divider":
        return (
            f"{inner_html}\n"
            f'{img_tag} class="slide-image reveal" '
            f'style="margin-top: clamp(0.5rem, 1vw, 1rem);">'
        )

    # Default: append image below content
    return f"{inner_html}\n{img_tag}>"


def build_slide(meta: dict, body: str) -> str:
    """Build a complete <section> slide element."""
    slide_type = meta.get("type", "content-slide")
    footer = meta.get("footer", "")
    section_number = meta.get("section_number", "")
    label = ""

    # Try to extract label from first heading
    h_match = re.search(r"^#\s+(.+)$", body, re.MULTILINE)
    if h_match:
        label = h_match.group(1)

    inner_html = render_body(body, meta)
    inner_html = wrap_with_image(inner_html, meta)

    # Section number for divider slides
    section_num_html = ""
    if section_number:
        section_num_html = (
            f'<span class="section-number">'
            f"{escape(str(section_number))}</span>\n"
        )

    # Brand mark for title slides
    brand_mark = ""
    if slide_type == "title-slide":
        brand_mark = '<div class="brand-mark decorative"></div>\n'

    # Footer
    footer_html = ""
    if footer:
        footer_html = (
            f'\n<span class="slide-footer">{escape(footer)}</span>'
        )

    aria = f' aria-label="{escape(label)}"' if label else ""

    return (
        f'<section class="slide {slide_type}"{aria}>\n'
        f"{brand_mark}"
        f"{section_num_html}"
        f'<div class="slide-content">\n'
        f"{inner_html}\n"
        f"</div>"
        f"{footer_html}\n"
        f"</section>"
    )


# ---------------------------------------------------------------------------
# Template: extract CSS + JS shell from template.html
# ---------------------------------------------------------------------------
def load_template_shell() -> tuple[str, str]:
    """Return (head_html, tail_html) — everything before and after slides."""
    if not TEMPLATE_FILE.exists():
        # Fallback: read from current deck.html if template doesn't have
        # the right structure, use a minimal shell
        return _minimal_shell()

    text = TEMPLATE_FILE.read_text()

    # Find first <section and last </section> to split
    first_section = text.find("<section")
    last_section_end = text.rfind("</section>")
    if first_section == -1 or last_section_end == -1:
        return _minimal_shell()

    last_section_end = text.find("\n", last_section_end) + 1

    head = text[:first_section].rstrip() + "\n\n"
    tail = "\n" + text[last_section_end:].lstrip()
    return head, tail


def _minimal_shell() -> tuple[str, str]:
    """Fallback minimal HTML shell if template isn't usable."""
    # Read from the existing deck.html instead
    deck = SCRIPT_DIR / "deck.html"
    if deck.exists():
        text = deck.read_text()
        first = text.find("<section")
        last_end = text.rfind("</section>")
        if first != -1 and last_end != -1:
            last_end = text.find("\n", last_end) + 1
            return (
                text[:first].rstrip() + "\n\n",
                "\n" + text[last_end:].lstrip(),
            )
    # Absolute fallback
    return (
        "<!DOCTYPE html>\n<html><head>"
        "<title>Deck</title></head><body>\n\n",
        "\n</body></html>\n",
    )


# ---------------------------------------------------------------------------
# Main build
# ---------------------------------------------------------------------------
def build():
    md_files = sorted(CONTENT_DIR.glob("*.md"))
    if not md_files:
        print("No markdown files found in", CONTENT_DIR)
        sys.exit(1)

    slides_html = []
    for md_file in md_files:
        text = md_file.read_text()
        meta, body = parse_frontmatter(text)
        slide_html = build_slide(meta, body)
        slides_html.append(
            f"    <!-- {md_file.name} -->\n    {slide_html}"
        )
        print(f"  {md_file.name} -> {meta.get('type', 'content-slide')}")

    head, tail = load_template_shell()
    OUTPUT_DIR.mkdir(exist_ok=True)
    full_html = head + "\n\n".join(slides_html) + tail

    # Adjust image paths: content/*.md uses paths relative to
    # presentation/ (e.g. ../images/) but output/deck.html is one
    # level deeper, so we need ../../images/
    full_html = full_html.replace('src="../images/', 'src="../../images/')

    OUTPUT_FILE.write_text(full_html)
    print(f"\n  Built {len(slides_html)} slides -> {OUTPUT_FILE}")


if __name__ == "__main__":
    if "--open" in sys.argv:
        build()
        import subprocess
        subprocess.run(["open", str(OUTPUT_FILE)])
    else:
        build()
