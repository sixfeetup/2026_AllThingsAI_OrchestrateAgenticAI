# Build Pipeline (Vendored)

These three files form the core build pipeline for the AllThings AI conference
presentation. They are the first non-content artifacts created in the project
and have been iterated on more than any other component. Every bug fix, feature
addition, and workflow improvement in the project's history touched at least one
of these files -- most often `build.py`.

## What the Pipeline Does

The pipeline compiles individual markdown slide files
(`presentation/content/NN-slug.md`) into a single self-contained HTML deck
(`presentation/output/deck.html`). Each slide file uses YAML frontmatter for
metadata (type, image, layout) and a markdown body for content. The compiled
deck is wrapped in a branded HTML/CSS/JS template shell sourced from
`presentation/template.html`.

## Files

### `build.py` -- The Slide Compiler

A single-file Python script (only dependency: `pyyaml`) that:

- Reads all `presentation/content/*.md` files in sorted order
- Parses YAML frontmatter and markdown body from each
- Converts markdown elements (headings, lists, blockquotes, code fences,
  grid/card blocks, explainer links) into styled HTML `<section>` elements
- Splits speaker notes on the `???` separator (Remark.js convention)
- Scans for and strips `@@` directives (inline AI instructions)
- Wraps slides in the template shell (CSS, JS, branding)
- Rewrites image paths for output depth (`../images/` becomes `../../images/`)
- Writes to both `output/deck.html` and `dist/deck.html` (for gh-pages)

### `check-changes.sh` -- Change Detection

An MD5-hash-based watcher that computes a combined hash of `plan.md`,
`README.md`, `quotes.md`, and all `presentation/content/*.md` files. State is
persisted in `presentation/.watch-state`. Returns exit 0 on change (or first
run) and exit 1 when nothing has changed. The `/deck-watch` skill invokes this
every 90 seconds to decide whether a rebuild is needed.

### `Makefile` -- Build Orchestration

Makefile targets that tie everything together:

- **build**: `uv run build.py` to compile the deck
- **open**: build then open in browser
- **clean**: remove built output
- **reset-content**: safely remove only committed content files
- **deploy**: build, sync referenced images to `dist/`, commit and push to
  the `gh-pages` branch
- **serve**: local preview server from `dist/`
- **watch**: filesystem-watch rebuild loop (via `fswatch`)
- **list**: print slide order

## How They Work Together

```
check-changes.sh  -->  deck-watch skill triggers  -->  build.py compiles
                                                        |
                                                  Makefile orchestrates
                                                   build / deploy / serve
```

1. `check-changes.sh` detects that source files have been modified.
2. The `/deck-watch` skill (run via `/loop 90s`) calls check-changes and, on
   change, processes `@@` directives, regenerates slide files from `plan.md`,
   and then runs `make build`.
3. `make build` invokes `uv run build.py`, which reads content, compiles HTML,
   and writes the output deck.
4. `make deploy` pushes the built deck and referenced images to the `gh-pages`
   branch for public hosting.

## Historical Importance

These scripts were the backbone of the project from day one. Key moments in
their evolution:

- **Initial slide generation** (commit 43df8a4): basic conversion of markdown
  slide files into an HTML deck. This was the first working pipeline.
- **Visual explainer link support** (d3c288e): added `[explainer: Title](url)`
  syntax so slides could link out to interactive demos.
- **Show-don't-tell editorial pass** (2b473e1): integrated editorial workflow
  changes that required build.py to handle new content patterns.
- **Reverse plan flow** (b5154ed): reworked how plan.md drives slide generation,
  reversing the earlier content-first approach.
- **Quote rendering fixes** (multiple commits): visibility on dark slides,
  splitting multiple blockquotes on blank `>` lines, rendering markdown links
  inside quotes, HTML escaping edge cases.
- **`@@` directive processing**: added scanning and stripping of `@@` lines so
  inline AI instructions could live in slide files without appearing in output.
- **Image path rewriting**: `../images/` rewritten to `../../images/` for
  `output/` depth and to `images/` for `dist/` (gh-pages).
- **Deploy pipeline**: the `deploy` Makefile target automates syncing only
  referenced images and committing to the gh-pages worktree.

## Key Design Decisions

- **Single-file Python compiler**: no framework, no static site generator. Just
  `build.py` with `pyyaml`. This keeps the pipeline fast, transparent, and easy
  to modify from a Claude Code session.
- **YAML frontmatter for slide metadata**: each slide carries its own type,
  image, layout, and footer in frontmatter -- no separate config file needed.
- **`???` separator for speaker notes**: follows the Remark.js convention so
  notes can coexist with slide content in a single file.
- **`@@` as inline AI instruction syntax**: directives like `@@ add a slide
  about X` can be dropped into any watched file. The watcher processes them
  before the build, then strips them so they never appear in output.
- **`uv run` everywhere**: no virtualenv management. `uv` handles the Python
  environment and dependencies inline via PEP 723 script metadata.
