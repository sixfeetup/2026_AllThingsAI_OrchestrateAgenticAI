# render-deck

Render slide markdown into an HTML presentation deck.

## Triggers

- `/render-deck`
- `/deck`

## What it does

Builds `presentation/output/deck.html` from markdown slide files
in `presentation/content/`. Each `.md` file is one slide with YAML
frontmatter (type, image, layout) and markdown body.

## Usage

### Build and open

```sh
cd presentation && make open
```

Or equivalently:

```sh
uv run presentation/build.py --open
```

### Just build (no browser)

```sh
cd presentation && make build
```

### List slide order

```sh
cd presentation && make list
```

### Watch for changes

```sh
cd presentation && make watch
```

## Slide markdown format

Each file in `presentation/content/` follows this pattern:

```markdown
---
type: content-slide
image: ../images/photo.jpg
image_alt: description
image_layout: split
footer: "05"
---

# Slide Title

> "Quote text"

- Bullet point

:::grid
:::card Card Title
Card body.
:::
:::grid
```

### Frontmatter fields

| Field | Values | Required |
|-------|--------|----------|
| `type` | `title-slide`, `content-slide`, `dark-slide`, `divider-slide` | yes |
| `image` | relative path to image | no |
| `image_alt` | alt text | no |
| `image_layout` | `split`, `inline`, `divider` | no |
| `section_number` | `I`, `II`, etc. (divider slides) | no |
| `footer` | slide number string | no |

### Body syntax

| Syntax | Renders as |
|--------|-----------|
| `# Title` | h1 (title slides) or h2 |
| `> quote` | blockquote with quote class |
| `- item` | bullet-list |
| `*text*` | tagline (title slides) or italic |
| `_text_` | subtitle |
| `— Author` | quote-attribution |
| `` ```python `` | code-block with syntax hints |
| `:::grid` / `:::card` | feature-grid with cards |

## Workflow

When the user asks to edit slide content:

1. Edit the relevant `presentation/content/NN-slug.md` file
2. Run `cd presentation && make open` to rebuild and preview
3. Iterate

When adding a new slide:
1. Create `presentation/content/NNb-slug.md` (or renumber)
2. Rebuild

When reordering slides:
1. Rename files to change sort order (files sort lexicographically)
2. Rebuild
