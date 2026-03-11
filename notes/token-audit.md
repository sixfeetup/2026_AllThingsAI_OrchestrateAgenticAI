# Token Audit — LLM Invocation Map

_Every point in the Agents of Legend presentation project where an LLM/agent is invoked._

---

## Ranked Table: Token Sinks (Cost x Frequency)

Ordered by **effective token burn** = unit cost x typical frequency during development/rehearsal.

| Rank | Invocation Point | Trigger | Unit Cost | Frequency | Determinism | Effective Burn | Non-LLM Alternative |
|------|-----------------|---------|-----------|-----------|-------------|----------------|---------------------|
| 1 | **/deck-watch (@@directives + slide regen)** | `/loop 90s /deck-watch` | HIGH | HIGH (every 90s when active) | LOW — interprets `@@` freeform | **CRITICAL** | Template vars + `sed` for substitution; reserve LLM for ambiguous directives only |
| 2 | **Manual slide editing via Claude Code** | Ad-hoc user prompts in Claude Code | MEDIUM | HIGH (dozens/day during dev) | MEDIUM — edits are scoped | **HIGH** | Edit in VS Code / vim directly; use Claude only for generating new content |
| 3 | **Demo 2 rehearsal — Contract/Security swarm** | Live or rehearsal run | VERY HIGH (3 APIs) | LOW-MEDIUM (2-5 rehearsals) | LOW — 3 models, variable | **HIGH** | Pre-bake all outputs once; rehearse from pre-baked files; only go live once at venue |
| 4 | **/mc or /c^2 swarm dispatches** | `/mc swarm` or `/c^2 swarm` | VERY HIGH (N agents) | LOW-MEDIUM (dev tasks) | LOW — each agent independent | **HIGH** | Single-agent sequential work; traditional PR review; `gh pr review` |
| 5 | **Demo 1 rehearsal — OGL Content Crisis** | Live or rehearsal run | HIGH (PDF parsing + generation) | LOW-MEDIUM (2-5 rehearsals) | LOW | **MEDIUM-HIGH** | Pre-extract names once, cache in JSON; only call LLM for name *replacement* generation |
| 6 | **/visual-explainer** | `/visual-explainer` | MEDIUM-HIGH | LOW (4 pages total) | LOW — generates unique HTML | **MEDIUM** | Mermaid CLI + hand-coded HTML; draw.io export; Figma embed |
| 7 | **Demo 3 rehearsal — multiclaude TDD** | Live or rehearsal run | HIGH (TDD loops) | LOW (1-2 rehearsals) | LOW | **MEDIUM** | Pre-record asciinema; rehearse from recording; one live attempt at venue only |
| 8 | **/gen-image and generate_images.py** | `/gen-image` or `python generate_images.py` | HIGH (image gen) | VERY LOW (run once) | LOW — images vary | **LOW-MEDIUM** | Stock photos (Unsplash, Pexels); SVG illustrations; Midjourney (cheaper per image) |
| 9 | **/frontend-slides** | `/frontend-slides` | HIGH | VERY LOW (not used; project uses build.py) | LOW | **LOW** | N/A — already using build.py instead |
| 10 | **build.py** | `make build` / `uv run build.py` | **ZERO** | VERY HIGH | **FULL** — deterministic | **ZERO** | N/A — already non-LLM |

---

## Detailed Findings

### 1. /deck-watch — `@@` Directive Processing + Slide Regeneration

**Skill file:** `~/.claude/skills/deck-watch/SKILL.md`

**How it works:**
- Triggered via `/loop 90s /deck-watch` — polls every 90 seconds
- On each tick: runs `check-changes.sh` (md5 hash comparison)
- If changes detected: reads `plan.md`, `README.md`, `quotes.md`, all `presentation/content/*.md`
- Scans all files for `@@` directives (freeform instructions like `@@ add a slide about testing`)
- Interprets directives, modifies slide files, removes processed `@@` lines
- Regenerates slides by diffing `plan.md` structure against existing slides
- Runs `make build`

**Token analysis:**
- **Input tokens per tick (with changes):** ~15-25K (all watched files)
- **Output tokens per tick:** ~2-10K (modified slide content)
- **Frequency:** Every 90 seconds during active editing sessions (could be 40+ invocations/hour)
- **Determinism:** LOW — `@@` directives are freeform natural language; slide regeneration involves creative interpretation

**Why it's #1:** Even though individual cost is moderate, the 90-second loop makes this the single largest token sink during active development. A 2-hour editing session could burn 80+ invocations.

**Concrete alternatives:**
- **For `@@` directives:** Define a structured directive syntax (e.g., `@@ADD slide_title`, `@@DELETE 04`, `@@MOVE 07 TO 03`) that a Python script can parse deterministically. Reserve LLM for `@@FREEFORM` directives only.
- **For slide regeneration:** Use a diffing tool to detect structural changes in `plan.md` and apply them mechanically. Only invoke LLM when *new content* needs to be written.
- **For the loop:** Switch to event-driven (file watcher like `fswatch`) with debounce, instead of polling every 90s regardless.

---

### 2. Manual Slide Editing via Claude Code

**How it works:**
- User types natural language instructions in Claude Code terminal
- Claude reads files, modifies markdown, writes changes
- Each interaction is a full LLM round-trip

**Token analysis:**
- **Input tokens per edit:** ~5-15K (file contents + conversation context)
- **Output tokens per edit:** ~1-5K (edits + explanation)
- **Frequency:** HIGH — dozens of interactions per editing session
- **Determinism:** MEDIUM — edits to specific files are somewhat predictable

**Concrete alternatives:**
- Use VS Code / vim for mechanical edits (typos, reordering bullets, changing frontmatter)
- Batch multiple related edits into a single Claude prompt instead of one-at-a-time
- Use Claude only for *generating new content* or *creative restructuring*
- Consider a "slide lint" script that catches common issues without LLM

---

### 3. Demo 2 — Contract/Security Review Swarm

**How it works:**
- Ingests contract PDF via Claude Code
- Generates visual explainer HTML (`/visual-explainer`)
- Runs security skills (Claude)
- Dispatches adversarial swarm via `/c^2` to Codex + Gemini + Claude
- Generates spec via speckit

**Token analysis:**
- **Claude tokens per run:** ~50-100K (contract parsing + analysis + HTML generation)
- **Codex tokens per run:** ~20-40K (adversarial review)
- **Gemini tokens per run:** ~20-40K (adversarial review)
- **Total per rehearsal:** ~100-200K tokens across 3 APIs
- **Frequency:** 2-5 full rehearsals before the talk
- **Determinism:** LOW — three different models produce different outputs

**Why it's ranked high despite low frequency:** Single-run cost is extreme. 3 APIs multiplied by multi-agent orchestration.

**Concrete alternatives:**
- **Pre-bake once, rehearse from files.** Run the full swarm exactly once. Save all outputs. Rehearse transitions using saved files.
- **Replace adversarial swarm with rule-based checks.** A Python script checking for common contract red flags (indemnification clauses, IP assignment, non-compete) covers 80% of the demo narrative.
- **Single-model review.** Skip Codex + Gemini legs; use Claude-only with different system prompts for "adversarial" perspective.

---

### 4. /c^2 and /mc Worker Prompts (Development Use)

**Skill files:** `~/.claude/skills/c2/SKILL.md`, `~/.claude/skills/mc/SKILL.md`

**How they work:**
- `/c^2 swarm` or `/mc swarm` — decomposes goal into subtasks, spawns N parallel Claude agents
- Each agent gets its own worktree, runs autonomously, creates PRs
- `/mc` uses a persistent daemon; `/c^2` uses the Agent tool directly

**Token analysis:**
- **Tokens per worker:** ~20-50K (full agent session including code reading + writing)
- **Workers per swarm:** 2-6 typically
- **Total per swarm:** ~50-300K tokens
- **Frequency:** LOW-MEDIUM during active development
- **Determinism:** LOW — each agent takes its own path

**Concrete alternatives:**
- **Sequential single-agent work** for most tasks (cheaper, more predictable)
- **Traditional code review** via `gh pr review` for review tasks
- **Reserve swarms** for genuinely parallelizable, independent tasks only
- **Limit worker count** — 2 workers often gives 80% of the benefit of 5

---

### 5. Demo 1 — OGL Content Crisis

**How it works:**
- Claude Code searches 18 D&D PDFs (~170MB) for OGL-protected names
- Cross-references against `sample-content-db.json`
- Generates damage report
- Generates replacement name suggestions

**Token analysis:**
- **Input tokens:** ~30-60K (PDF text extraction is token-heavy)
- **Output tokens:** ~5-10K (report + names)
- **Frequency:** 2-5 rehearsals
- **Determinism:** LOW for name generation; MEDIUM for extraction

**Concrete alternatives:**
- **Pre-extract names** via a Python script using `PyMuPDF` or `pdfplumber` — zero LLM tokens
- **Cache extraction results** in `ogl-reference-terms.json` (already exists!)
- **Cross-reference via Python** — JSON lookup, no LLM needed
- **Only use LLM for replacement name generation** — the creative part that actually benefits from it

---

### 6. /visual-explainer

**Skill file:** `~/.claude/skills/visual-explainer/SKILL.md`

**How it works:**
- Claude reads reference files (css-patterns.md, templates, animation patterns)
- Generates self-contained HTML with CSS variables, animations, Mermaid diagrams
- Optionally embeds AI-generated images via `surf-cli`

**Token analysis:**
- **Input tokens:** ~10-20K (reference files + source content)
- **Output tokens:** ~5-15K (full HTML page)
- **Pages in this project:** 4 (system-overview, demo-plan, playbook, checklist-progress)
- **Frequency:** LOW — generated once, rarely regenerated
- **Determinism:** LOW — each generation produces unique HTML/CSS

**Concrete alternatives:**
- **Mermaid CLI** (`mmdc`) for diagrams — renders to SVG/PNG deterministically
- **Hand-coded HTML** using the existing `template.html` CSS as a base
- **draw.io / Excalidraw** for architecture diagrams, exported as SVG
- **Hugo/Docusaurus** for structured doc pages

---

### 7. Demo 3 — Jetpacks / multiclaude TDD

**How it works:**
- `multiclaude` spawns agents for TDD: one writes tests, one implements, one reviews
- `ralph-orchestrator` runs hat-based loop iterations
- Both call Anthropic API continuously during execution

**Token analysis:**
- **Tokens per run:** ~50-100K (multiple agents in TDD loop)
- **Frequency:** 1-2 rehearsals (demo plan recommends pre-recording)
- **Determinism:** LOW

**Concrete alternatives:**
- **Pre-record everything** (already the plan — asciinema recordings)
- **Only attempt one live run** at the venue; fallback to recording
- **Use a minimal test case** to limit agent iterations

---

### 8. /gen-image and generate_images.py

**Skill file:** `~/.claude/skills/gen-image/SKILL.md`
**Script:** `images/generate_images.py`

**How it works:**
- `generate_images.py` calls Gemini API (`gemini-3.1-flash-image-preview`) with 6 detailed prompts
- `/gen-image` skill wraps Gemini or Codex/DALL-E for one-off generation
- Images saved to `images/` and `images/attic/` (16 alternatives generated)

**Token analysis:**
- **Gemini tokens per image:** ~1-2K input (prompt), image generation cost is separate
- **Financial cost:** Image generation pricing, not standard token pricing
- **Frequency:** VERY LOW — images already generated and committed
- **Determinism:** LOW — images vary per generation

**Concrete alternatives:**
- **Stock photography** (Unsplash, Pexels) — free, instant, deterministic
- **SVG illustrations** — already used for some images (spelljammer, its-a-trap)
- **Midjourney** — better quality per generation, may be cheaper for batch
- **Stable Diffusion local** — free after setup, no API calls

---

### 9. /frontend-slides

**Skill file:** `~/.claude/skills/frontend-slides/SKILL.md`

**Not actively used** in this project — the project uses its own `build.py` pipeline.

**If it were used:**
- Generates complete HTML/CSS/JS presentations from scratch
- Reads 4 reference files (template, CSS, animation patterns, style presets)
- Includes a 5-phase workflow with "style discovery" (3 preview generations)

**Token analysis:** HIGH per invocation, but frequency is ZERO for this project.

---

### 10. build.py — The One That Doesn't Use LLM

**Script:** `presentation/build.py` (644 lines of Python)

**What it does:**
- Parses YAML frontmatter + markdown body
- Renders custom markdown syntax to HTML (headings, bullets, code blocks, grids, quotes)
- Validates image references
- Scans for unresolved `@@` directives (warns but does not process them)
- Wraps output in template CSS/JS shell
- Writes to `presentation/output/deck.html` and `dist/deck.html`

**Token cost: ZERO.** Pure Python, no API calls, fully deterministic.

**This is the model:** Everything that can be deterministic should be deterministic. `build.py` proves that the rendering pipeline doesn't need LLM. The question is: how much of the *content* pipeline can follow this pattern?

---

## Summary: Where Tokens Go and Where They Don't Need To

### The Three Categories

**Must be LLM** (creative, genuinely benefits from language model):
- New slide content generation
- `@@` freeform directive interpretation
- Demo name replacement generation
- Adversarial contract review (the *creative* adversarial perspective)

**Could be deterministic** (currently LLM but shouldn't be):
- `@@` structured directives (add/remove/move/reorder slides)
- Slide regeneration when plan structure changes (diffing + templating)
- PDF name extraction (regex/NLP, not generative)
- DB cross-referencing (JSON lookup)
- Mechanical slide edits (typos, frontmatter changes)
- Demo rehearsal runs after the first (use cached outputs)

**Already deterministic** (good):
- `build.py` rendering pipeline
- `make build` / `make deploy` / `make web-images`
- `check-changes.sh` (md5 hashing)
- Image validation
- File watching / change detection

### Token Reduction Opportunities (Estimated Savings)

| Change | Estimated Token Savings | Effort |
|--------|------------------------|--------|
| Switch deck-watch to event-driven (no empty polls) | 30-50% of deck-watch tokens | LOW — use `fswatch` |
| Structured `@@` directives parsed by Python | 40-60% of deck-watch tokens | MEDIUM — new parser |
| Pre-bake demo outputs, rehearse from files | 80-90% of demo rehearsal tokens | LOW — already planned |
| Limit swarm workers to 2 | 50-70% of swarm tokens | LOW — config change |
| Extract PDF names via Python script | 100% of Demo 1 extraction tokens | MEDIUM — `pdfplumber` script |
| Batch manual edits into single prompts | 30-50% of manual editing tokens | LOW — workflow change |

### Total Estimated Project Token Distribution

```
/deck-watch (active editing)      ████████████████████░░░░░░░░  35%
Manual Claude Code edits           ██████████████░░░░░░░░░░░░░░  25%
Demo rehearsals (all 3)            ███████████░░░░░░░░░░░░░░░░░  20%
/c^2 and /mc swarms                ████████░░░░░░░░░░░░░░░░░░░░  12%
/visual-explainer                  ███░░░░░░░░░░░░░░░░░░░░░░░░░   5%
/gen-image                         █░░░░░░░░░░░░░░░░░░░░░░░░░░░   2%
build.py                           ░░░░░░░░░░░░░░░░░░░░░░░░░░░░   0%
/frontend-slides                   ░░░░░░░░░░░░░░░░░░░░░░░░░░░░   0%
```

---

_Audit completed 2026-03-11. Covers all skills, scripts, and manual workflows in the Agents of Legend presentation project._
