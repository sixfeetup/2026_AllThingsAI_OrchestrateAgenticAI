# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Is

Conference presentation repo for **"Orchestrate Agentic AI: Context, Checklists, and No-Miss Reviews"** — a 45-minute talk by Calvin Hendryx-Parker for AllThings AI 2026. The talk covers context engineering, agentic workflows, and a live contract-review demo using coding agents.

Deployed deck: https://super-tribble-8w5zrvy.pages.github.io/

## Build Commands

All presentation commands run from the `presentation/` directory via Make (which calls `uv run build.py`):

```sh
make build        # render content/*.md → output/deck.html
make open         # build + open in browser
make watch        # auto-rebuild on changes (requires fswatch)
make list         # show slide order with titles
make lint         # markdownlint on content/*.md
make web-images   # generate _web.jpg from source PNGs (uses sips)
make clean        # remove output
make serve        # local preview from dist/ on :8000
```

Build requires `uv` (astral-sh) with Python >=3.11. The only Python dependency is `pyyaml`.

## Slide System Architecture

The deck is a **custom markdown-to-HTML pipeline** — no reveal.js or similar framework.

### Content → Build → Output flow

1. **`presentation/content/NN-slug.md`** — one file per slide, sorted lexicographically. Each has YAML frontmatter + markdown body.
2. **`presentation/build.py`** — parses frontmatter, converts markdown to slide HTML, validates image refs, warns on unresolved `@@` directives.
3. **`presentation/template.html`** — CSS/JS shell (Six Feet Up branding: Montserrat + Oswald fonts, teal palette). The build inserts rendered slides between the first and last `<section>` tags.
4. **`presentation/output/deck.html`** — built output (gitignored).

### Slide frontmatter fields

```yaml
type: title-slide | content-slide | dark-slide | divider-slide
image: ../images/photo.jpg       # optional
image_alt: description            # optional
image_layout: split | inline | divider  # optional
section_number: II                # divider slides only
footer: "05"                      # slide number, bottom-right
```

### Slide body conventions

- `???` separates visible content from speaker notes
- `:::grid` / `:::card Title` / `:::` for card grids
- `> quote` for blockquotes, `— Attribution` for attribution lines
- `*italic text*` renders as tagline on title slides
- `_italic text_` renders as subtitle
- `[explainer: Title](explainers/file.html)` renders as a pill/button link
- `@@directive@@` lines are stripped from output; build warns about unresolved ones

### Adding/reordering slides

- Name files `NN-slug.md` — insert with `03b-new.md` or renumber
- `presentation/scripts/renumber-slides.sh` — renumbers all slides sequentially, updates footer values
- Images go in `presentation/images/`; reference as `../images/filename` from content files

## Explainers

Self-contained HTML pages in `presentation/explainers/` linked from slides. These are standalone visual aids (context window explainer, system overview, demo plan, etc.).

## Demo

The `demo/` directory contains the live demo plan and assets:
- `demo/outline.md` — demo script and flow
- `demo/assets/` — D&D Archive PDFs (OGL source material), sample contracts, prebaked outputs
- The demo scenario involves "Safe House Games" needing IP overlap analysis using coding agents

## Agent Tooling

- `.agents/bin/` — utility scripts (audit-renumber, audit-worktrees, draft-pr, rebuild-slides, slide-image-audit)
- `.agents/skills/` — speckit skill definitions (analyze, checklist, clarify, plan, specify, tasks, etc.)
- `.codex/prompts/` — OpenAI Codex prompt equivalents for the speckit skills
- `.specify/` — speckit templates and scripts for spec-driven development workflow

## Notes Directory

`notes/` contains research, talk development, and refinement docs. Key files:
- `notes/talk.md` — narrative outline with speaker notes
- `notes/whitmo/` — presenter's working notes, refinement docs, role definitions
- `expectations.md` — extracted promises from the pitch (explicit and implicit commitments to the audience)
- `presentation/checklist.md` — delivery checklist tracking what must be covered/demonstrated/delivered

## CI/CD

GitHub Actions deploys to GitHub Pages on push to `main` when `presentation/**` changes. The workflow runs `uv run build.py`, rewrites image paths for flat `_site/` layout, and deploys.

## Hooks

- `PostToolUse` hook runs `.agents/bin/audlog-hook.sh` on every tool use (audit logging)
- `UserPromptSubmit` hook on "end session" triggers the `/end-session` skill
