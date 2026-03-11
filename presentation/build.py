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
    uv run presentation/build.py --root /path/to/repo
    uv run presentation/build.py --watch    # rebuild on file changes
    uv run presentation/build.py --open     # open in browser after build
"""
import argparse
import re
import sys
import html as html_mod
from pathlib import Path

import yaml


# ---------------------------------------------------------------------------
# Paths — defaults based on script location; overridable via --root
# ---------------------------------------------------------------------------
SCRIPT_DIR = Path(__file__).resolve().parent

# These module-level variables are set by _init_paths() before any build work.
REPO_ROOT: Path
CONTENT_DIR: Path
OUTPUT_DIR: Path
DIST_DIR: Path
TEMPLATE_FILE: Path
OUTPUT_FILE: Path
DIST_FILE: Path


def _init_paths(root: Path | None = None) -> None:
    """(Re)compute derived paths from *root* (the repository root)."""
    global REPO_ROOT, CONTENT_DIR, OUTPUT_DIR, DIST_DIR
    global TEMPLATE_FILE, OUTPUT_FILE, DIST_FILE

    REPO_ROOT = root.resolve() if root else SCRIPT_DIR.parent
    pres_dir = REPO_ROOT / "presentation"
    CONTENT_DIR = pres_dir / "content"
    OUTPUT_DIR = pres_dir / "output"
    DIST_DIR = REPO_ROOT / "dist"
    TEMPLATE_FILE = pres_dir / "template.html"
    OUTPUT_FILE = OUTPUT_DIR / "deck.html"
    DIST_FILE = DIST_DIR / "deck.html"


# Initialise with defaults so import-time usage (tests, REPL) still works.
_init_paths()


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


_DIRECTIVE_RE = re.compile(r"@@\S.*|!\[.*?\]\(@@.*?\)")
_MD_IMAGE_RE = re.compile(r"!\[.*?\]\((.+?)\)")


def scan_directives(text: str, filename: str) -> list[str]:
    """Find unresolved @@ directives and warn about them."""
    found = []
    for i, line in enumerate(text.split("\n"), 1):
        if "@@" in line:
            directive = line.strip()
            found.append(f"  ⚠  {filename}:{i}  {directive}")
    return found


def strip_directives(body: str) -> str:
    """Replace @@ directive lines with HTML TODO markers (hidden in output)."""
    lines = body.split("\n")
    out = []
    for line in lines:
        if "@@" in line:
            # Skip pure directive lines — don't render them
            continue
        out.append(line)
    return "\n".join(out)


def validate_images(
    md_files: list[Path],
) -> list[str]:
    """Check that all image references in slides point to existing files.

    Scans both YAML frontmatter ``image:`` fields and markdown ``![](...)``
    syntax.  Returns a list of human-readable warning strings (empty = all OK).
    Also flags ``_web.jpg`` references where only the source ``.png`` exists.
    """
    warnings: list[str] = []

    for md_file in md_files:
        text = md_file.read_text()
        meta, body = parse_frontmatter(text)

        refs: list[tuple[str, str]] = []  # (raw_ref, source_label)

        # Frontmatter image: field
        fm_image = meta.get("image")
        if fm_image:
            refs.append((fm_image, "frontmatter 'image'"))

        # Markdown ![alt](path) in body
        for m in _MD_IMAGE_RE.finditer(body):
            refs.append((m.group(1), f"line reference"))

        for raw_ref, source in refs:
            # Refs use ../images/FILENAME — images live at presentation/images/
            # (the build rewrites src paths in output HTML, so ../images/ from
            # content/ doesn't resolve literally on disk).
            m_img = re.match(r"\.\./images/(.+)$", raw_ref)
            if m_img:
                pres_dir = REPO_ROOT / "presentation"
                ref_path = (pres_dir / "images" / m_img.group(1)).resolve()
                if not ref_path.exists():
                    # Fallback to legacy repo-root images/ location
                    ref_path = (REPO_ROOT / "images" / m_img.group(1)).resolve()
            else:
                ref_path = (CONTENT_DIR / raw_ref).resolve()

            if not ref_path.exists():
                # Check for _web.jpg -> .png fallback hint
                stem = ref_path.stem  # e.g. "foo_web"
                if stem.endswith("_web") and ref_path.suffix in (".jpg", ".jpeg"):
                    source_png = ref_path.parent / (
                        stem.removesuffix("_web") + ".png"
                    )
                    if source_png.exists():
                        warnings.append(
                            f"  ⚠  {md_file.name}: {source} references "
                            f"'{raw_ref}' which does not exist, but source "
                            f"'{source_png.name}' found — run 'make web-images'"
                        )
                        continue
                warnings.append(
                    f"  ✗  {md_file.name}: {source} references "
                    f"'{raw_ref}' — file not found"
                )

    return warnings


def split_notes(body: str) -> tuple[str, str]:
    """Split slide body from speaker notes on '???' separator."""
    parts = re.split(r"^\?\?\?\s*$", body, maxsplit=1, flags=re.MULTILINE)
    if len(parts) == 2:
        return parts[0].strip(), parts[1].strip()
    return body, ""


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

        # --- Heading (any level) ---
        h_match = re.match(r"^(#{1,6})\s+(.+)$", line)
        if h_match:
            level = len(h_match.group(1))
            title_text = h_match.group(2)
            if is_title and level == 1:
                chunks.append(
                    f'<h1 class="reveal">{escape(title_text)}</h1>'
                )
            elif level <= 2:
                chunks.append(
                    f'<h2 class="reveal">{escape(title_text)}</h2>'
                )
            else:
                chunks.append(
                    f'<h3 class="reveal">{escape(title_text)}</h3>'
                )
            i += 1
            continue

        # --- Blockquote ---
        if line.startswith(">"):
            # Collect all > lines, splitting into separate quotes on blank > lines
            all_quote_lines: list[str] = []
            while i < len(lines) and lines[i].startswith(">"):
                all_quote_lines.append(lines[i].lstrip("> ").strip())
                i += 1
            # Split into separate blockquotes on empty lines
            quotes: list[list[str]] = [[]]
            for ql in all_quote_lines:
                if ql == "":
                    if quotes[-1]:  # only split if current group is non-empty
                        quotes.append([])
                else:
                    quotes[-1].append(ql)
            for q_lines in quotes:
                if not q_lines:
                    continue
                quote_text = " ".join(q_lines)
                # Render markdown links: [text](url)
                safe = escape(quote_text)
                safe = re.sub(
                    r'\[([^\]]+)\]\(([^)]+)\)',
                    r'<a href="\2" target="_blank" rel="noopener">\1</a>',
                    safe,
                )
                chunks.append(
                    f'<blockquote class="quote reveal">'
                    f"{safe}"
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

        # --- Explainer link: [explainer: Title](url) ---
        explainer_match = re.match(
            r"^\[explainer:\s*(.+?)\]\((.+?)\)\s*$", line.strip()
        )
        if explainer_match:
            title = explainer_match.group(1)
            url = explainer_match.group(2)
            chunks.append(
                f'<a class="explainer-link reveal" '
                f'href="{escape(url)}" target="_blank">'
                f"{escape(title)} \u2197</a>"
            )
            i += 1
            continue

        # --- Plain paragraph ---
        if line.strip():
            para_lines = []
            while i < len(lines) and lines[i].strip() and not any([
                re.match(r"^#{1,6}\s", lines[i]),
                lines[i].startswith(">"),
                lines[i].startswith("- "),
                lines[i].startswith("```"),
                lines[i].startswith(":::"),
                lines[i].startswith("*") and lines[i].endswith("*"),
                lines[i].startswith("_") and lines[i].endswith("_"),
                lines[i].startswith("—"),
                re.match(r"^\[explainer:", lines[i].strip()),
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

    # Split speaker notes from visible content
    visible_body, notes_text = split_notes(body)

    # Try to extract label from first heading
    h_match = re.search(r"^#\s+(.+)$", visible_body, re.MULTILINE)
    if h_match:
        label = h_match.group(1)

    inner_html = render_body(visible_body, meta)
    inner_html = wrap_with_image(inner_html, meta)

    # Extract quotes from inner_html so they can be positioned
    # absolutely at the bottom of the slide (outside .slide-content)
    quote_html = ""
    quote_pattern = re.compile(
        r'(<blockquote class="quote[^"]*"[^>]*>.*?</blockquote>'
        r'(?:\s*<p class="quote-attribution[^"]*"[^>]*>.*?</p>)?)',
        re.DOTALL,
    )
    qm = quote_pattern.search(inner_html)
    if qm:
        quote_html = f'\n<div class="slide-quote">{qm.group(0)}</div>'
        inner_html = inner_html[:qm.start()] + inner_html[qm.end():]

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

    # Speaker notes
    notes_html = ""
    if notes_text:
        notes_lines = [escape(l) for l in notes_text.split("\n") if l.strip()]
        notes_html = (
            '\n<aside class="speaker-notes">'
            + "<br>".join(notes_lines)
            + "</aside>"
        )

    aria = f' aria-label="{escape(label)}"' if label else ""

    return (
        f'<section class="slide {slide_type}"{aria}>\n'
        f"{brand_mark}"
        f"{section_num_html}"
        f'<div class="slide-content">\n'
        f"{inner_html}\n"
        f"</div>"
        f"{quote_html}"
        f"{notes_html}"
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
    deck = REPO_ROOT / "presentation" / "deck.html"
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
    all_directives: list[str] = []
    for md_file in md_files:
        text = md_file.read_text()
        meta, body = parse_frontmatter(text)

        # Scan for unresolved @@ directives
        directives = scan_directives(body, md_file.name)
        all_directives.extend(directives)

        # Strip @@ lines so they don't render as visible text
        body = strip_directives(body)

        slide_html = build_slide(meta, body)
        slides_html.append(
            f"    <!-- {md_file.name} -->\n    {slide_html}"
        )
        print(f"  {md_file.name} -> {meta.get('type', 'content-slide')}")

    # Report unresolved directives
    if all_directives:
        print(f"\n  {len(all_directives)} unresolved @@ directive(s):")
        for d in all_directives:
            print(d)

    # Validate image references
    image_warnings = validate_images(md_files)
    if image_warnings:
        print(f"\n  {len(image_warnings)} image reference issue(s):")
        for w in image_warnings:
            print(w)

    head, tail = load_template_shell()
    OUTPUT_DIR.mkdir(exist_ok=True)
    raw_html = head + "\n\n".join(slides_html) + tail

    # --- Write to presentation/output/ (paths relative to output/) ---
    output_html = raw_html.replace(
        'src="../images/', 'src="../../images/'
    )
    OUTPUT_FILE.write_text(output_html)
    print(f"\n  Built {len(slides_html)} slides -> {OUTPUT_FILE}")

    # --- Write to dist/ for gh-pages (images/ is a sibling) ---
    if DIST_DIR.exists():
        dist_html = raw_html.replace(
            'src="../images/', 'src="images/'
        )
        DIST_FILE.write_text(dist_html)
        print(f"  Also wrote -> {DIST_FILE}")


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build presentation deck from markdown slide files."
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
    return parser.parse_args(argv)


if __name__ == "__main__":
    args = _parse_args()
    _init_paths(args.root)
    build()
    if args.open_browser:
        import subprocess
        subprocess.run(["open", str(OUTPUT_FILE)])
