# Content Generation Tools

Tools for generating all non-text content in this presentation project: images, HTML visualizations, demo data, and reference material.

These files are vendored snapshots of the skills and scripts that were used during development. They document the toolchain that produced the visual and data assets for the talk.

## Files

| File | Source | Purpose |
|------|--------|---------|
| `visual-explainer.md` | `~/.claude/skills/visual-explainer/skill.md` | Claude skill for generating self-contained HTML explainer pages |
| `gen-image.md` | `~/.claude/skills/gen-image/skill.md` | Claude skill for image generation via Gemini or Codex (DALL-E) |
| `aix.md` | `~/.claude/skills/aix/skill.md` | Claude skill for 1Password API key caching |
| `generate_images.py` | `images/generate_images.py` | Batch Gemini image generation script with 6 themed prompts |
| `dl.py` | `demo-assets/dl.py` | D&D archive PDF downloader for demo scenario data |

## Historical Importance

### `/visual-explainer` -- HTML explainer pages

Produced the 4 standalone HTML explainer pages that serve as supplementary material for the presentation:

- **system-overview.html** -- A comprehensive guide to the entire build system (slide pipeline, watcher, directives, skills).
- **playbook.html** -- The operational playbook for the talk's narrative arc.
- **demo-plan.html** -- The live demo sequence plan.
- **checklist-progress.html** -- Progress tracking for presentation readiness.

These pages are accessible from the help modal (press `?` in the deck) and from presenter notes. They are fully self-contained HTML files with no external dependencies beyond CDN fonts -- they can be opened directly in any browser. The skill supports Mermaid diagrams, CSS Grid layouts, Chart.js, and multiple aesthetic presets (Blueprint, Editorial, Paper/ink, etc.), with strong anti-"AI slop" guardrails baked into the skill definition.

### `/gen-image` + `/aix` -- The image pipeline

The image generation workflow was:

1. Run `/aix env` to cache `GEMINI_API_KEY` (and other keys) from 1Password to `/tmp/ai-keys.env`, avoiding repeated biometric prompts during a session.
2. Run `/gen-image "prompt" --output images/slug.png` to generate an image via Gemini's image generation API.
3. The generated image lands in `images/` and is referenced by slide markdown files.

This pipeline was used for the initial batch image pass and for individual slide images added throughout development. Gemini was the default backend (faster response, free tier available). The Codex/DALL-E backend was available as a fallback.

### `generate_images.py` -- Batch image generator

A single script to create all 6 themed presentation images in one run. Each prompt was carefully crafted to match the RPG/quest metaphor that frames the entire talk:

- **title-epic-orchestrator.png** -- A lone figure on a peak with a glowing task graph constellation (title slide).
- **quest-artifacts.png** -- Legendary artifacts including Docker crystals and database scrolls (quest/tooling slide).
- **critical-d20.png** -- An iridescent d20 showing a natural 20, with code in the background (critical success metaphor).
- **skills-hologram.png** -- A holographic character sheet with tech skills like "Bash Scripting" and "Git Orchestration."
- **trap-detected-wizard.png** -- A wizard with a HUD highlighting traps in a contract (security/compliance slide).
- **jetpack-carpet-legion.png** -- People on circuit-woven flying carpets heading toward a cloud city (adoption/scaling slide).

Uses the `google.genai` Python SDK with skip-if-exists logic so it can be re-run safely without regenerating images that are already present.

### `dl.py` -- Demo scenario data

Populated the live demo scenario by downloading D&D reference PDFs from americanroads.us/dungeons.html into `demo-assets/DnD_Archive/`. These Open Gaming Licensed materials simulate the "OGL crisis" that the talk's narrative is built around -- the fictional L&LL LLC scenario where a company needs to audit its OGL-licensed content after a licensing change. The downloaded PDFs served as realistic input data for the live demo.

## Key Design Decisions

- **Self-contained HTML**: All explainer pages are single `.html` files with no external assets except CDN-loaded Google Fonts. They can be shared, opened offline, and embedded without a build step.
- **Gemini as default backend**: Faster response times and a usable free tier made Gemini the pragmatic choice over DALL-E for iterative image generation during development.
- **1Password integration**: The `/aix` skill wraps `op run` to cache API keys in an ephemeral file (`/tmp/ai-keys.env`, mode 600, cleared on reboot). This avoids hardcoding keys or repeated biometric prompts while keeping credentials out of the repository.
- **Batch generation with skip-if-exists**: `generate_images.py` checks whether each output file already exists before calling the API, making it safe to re-run after partial failures or when adding new prompts.
- **RPG-themed prompts**: Every image prompt was written to reinforce the talk's quest/RPG metaphor, creating visual coherence across the slide deck.
