# Orchestrate Agentic AI: Context, Checklists, and No-Miss Reviews

Slide deck for AllThings AI 2026 by Calvin Hendryx-Parker.
Content lives in markdown, built into a single HTML file.

Deployed deck: https://super-tribble-8w5zrvy.pages.github.io/

## Structure

```
presentation/
  outline.md          # slide content (pandoc-style markdown with YAML frontmatter)
  build.py            # markdown -> HTML renderer (content/*.md pipeline)
  build-reveal.py     # outline.md -> Reveal.js deck renderer
  template.html       # CSS/JS shell (Six Feet Up brand)
  deck.html           # legacy hand-built deck
  Makefile            # build tasks
  images/             # slide images (PNGs + generated _web.jpg variants)
  explainers/         # self-contained visual explainer HTML pages
  themes/             # Reveal.js SCSS themes (Six Feet Up variants)
  scripts/            # renumber-slides.sh, check-changes.sh
  output/             # rendered deck (gitignored)
```

## Two build pipelines

**Reveal.js (primary)** — builds from `outline.md`:

```sh
make build-reveal   # render outline.md -> output/deck-reveal.html
make open-reveal    # build + open in browser
```

**Content pipeline** — builds from individual `content/*.md` files:

```sh
make build          # render content/*.md -> output/deck.html
make open           # build + open in browser
make list           # show slide order with titles
```

Use `FROM_OUTLINE=1 make build` to read `outline.md` through the content pipeline instead.

## All Make targets

```sh
make build            # render content/*.md -> output/deck.html (+ dist/deck.html)
make open             # build + open in browser
make build-reveal     # render outline.md -> output/deck-reveal.html (Reveal.js)
make open-reveal      # build Reveal.js deck + open in browser
make watch            # auto-rebuild on content changes (requires fswatch)
make list             # show slide order with titles
make lint             # markdownlint on content/*.md
make web-images       # generate _web.jpg from source PNGs (uses sips, 1400px wide)
make deploy           # build, sync images, commit + push gh-pages
make serve            # local preview server from dist/ on :8000
make clean            # remove output
make reset-content    # remove only committed content/*.md (preserves dirty/untracked)
```

Build requires `uv` (astral-sh) with Python >=3.11. The only Python dependency is `pyyaml`.

## Slide markdown format

Slides in `outline.md` use pandoc-style markdown with `<!-- slide: N -->` markers.
The `content/*.md` pipeline uses YAML frontmatter per file:

```markdown
---
type: content-slide          # title-slide | content-slide | dark-slide | divider-slide
image: ../images/photo.jpg   # optional
image_alt: description       # optional
image_layout: split          # split | inline | divider (optional)
section_number: II           # divider slides only
footer: "05"                 # slide number shown bottom-right
---

# Slide Title

- Bullet one
- Bullet two

> "Quote"

::: notes
presenter notes
:::

:::grid
:::card Card Title
Card body text.
:::
:::
```

## Explainer links

Slides can link to self-contained visual explainer HTML pages:

```markdown
[explainer: How Agents Coordinate](explainers/agent-coordination.html)
```

This renders as a styled pill/button that opens the explainer in a new tab.
Place explainer HTML files in `presentation/explainers/`.

## CI/CD

GitHub Actions deploys to GitHub Pages on push to `main` when `presentation/**`
changes. The workflow runs `uv run build.py`, rewrites image paths for a flat
`_site/` layout, and deploys via `actions/deploy-pages`.
