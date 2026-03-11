# Research: Static Tooling Alternatives to LLM-Dependent Pipeline Steps

**Date:** 2026-03-11
**Context:** The presentation pipeline (`build.py` + `template.html` + `Makefile`) compiles
`content/*.md` files with YAML frontmatter into a single self-contained HTML deck. This
research surveys deterministic, non-LLM alternatives for each pipeline step.

**Related research:** `notes/research-frameworks.md` (framework comparison by zealous-rabbit)

---

## 1. Slide Generation: Can something replace build.py?

### Current state

`build.py` is a ~670-line custom Python markdown-to-HTML compiler. It uses **no LLM** — it is
already fully deterministic. It handles 10 custom markdown extensions not found in any
off-the-shelf framework:

- `:::grid` / `:::card` / `:::` container blocks
- `???` speaker notes separator
- `@@` directive scanning/stripping
- `[explainer: Title](url)` link syntax
- `_text_` as subtitle (not emphasis) on title/divider slides
- `*text*` as tagline (not emphasis) on title slides
- `—` attribution prefix for quotes
- Custom YAML frontmatter fields (`type`, `image_layout`, `section_number`, `footer`)
- Image layout composition (`split`, `inline`, `divider`)
- Simple Python syntax highlighting in code blocks

### Alternatives assessed

| Tool | Can it replace build.py? | Drop-in difficulty | Token savings | Tradeoffs |
|------|-------------------------|-------------------|--------------|-----------|
| **Marp CLI** | Partial | 4/5 (hard) | None (build.py is not LLM) | Marp uses `markdown-it` plugin architecture. Grid/card, explainer links, tagline/subtitle distinction, and `@@` directives would all need custom `markdown-it` plugins. Speaker notes use HTML comments (`<!-- -->`) not `???`. Marp adds PDF/PPTX export which build.py lacks. |
| **remark.js** | Partial | 3/5 (medium) | None | Already uses `???` for notes (same convention). No build step — client-side rendering. But no grid/card, no frontmatter-driven layout, no image layout composition. Would need custom CSS and significant markdown restructuring. |
| **reveal-md** | Partial | 4/5 (hard) | None | `reveal-md --static` produces standalone HTML. Notes use `Note:` prefix. Grid layouts need custom CSS. Frontmatter support exists but fields are different. The `---` slide separator conflicts with YAML frontmatter `---`. |
| **Slidev** | No | 5/5 (very hard) | None | Vue 3 + Vite stack is a completely different architecture. Would gain interactivity but lose determinism and simplicity. Deep npm dependency tree. Not a practical replacement. |
| **Darkslide** | Partial | 3/5 (medium) | None | Python-based, uses Jinja2 templates. Closest architectural match. But uses RST/Markdown without custom extensions. Would need forking to add grid/card support. Last meaningful update was years ago. |
| **Pyremark** | Partial | 3/5 (medium) | None | Puts markdown into Jinja2 template, outputs remark.js HTML. Close match for current architecture but inherits remark.js limitations on custom syntax. |

### Verdict

**build.py is already the right tool.** It uses no LLM, has minimal dependencies (`pyyaml`),
and handles all custom extensions natively. Replacing it with an off-the-shelf framework
would require writing the same amount of custom plugin code, plus adapting to a different
architecture. The only gains would be PDF/PPTX export (Marp) or interactivity (Slidev),
neither of which is a current requirement.

**If replacement were ever desired**, Marp CLI with custom `markdown-it` plugins is the
closest match, because it uses the same markdown-to-HTML paradigm with a plugin architecture
designed for custom containers.

---

## 2. Content Validation: Can static tools replace "does this look right?" checks?

### Current state

The pipeline already has some validation:
- `build.py` scans for unresolved `@@` directives (lines 120-143)
- `build.py` validates image references exist on disk (lines 146-201)
- `markdownlint` runs via `make lint` with presentation-specific `.markdownlint.json`

What's **not** validated:
- Frontmatter schema (invalid `type:` values silently pass through)
- Required frontmatter fields (a slide with no `footer:` produces no warning)
- Content completeness (empty slide bodies, missing speaker notes)
- Cross-slide consistency (numbering gaps, duplicate footers)

### Alternatives assessed

#### a) Frontmatter schema validation

| Tool | Drop-in difficulty | Token savings | Tradeoffs |
|------|-------------------|--------------|-----------|
| **JSON Schema + `pyyaml`** (custom Python) | 1/5 (easy) | High — eliminates LLM "check frontmatter" tasks | Write a ~50-line Python script with a JSON Schema file. Validates `type` enum, required fields, `image_layout` enum, `footer` format. Runs in CI. Already have `pyyaml` as a dependency. |
| **`@github-docs/frontmatter`** (npm) | 2/5 (easy) | High | npm package from GitHub's docs team. Uses revalidator for JSON Schema validation. Requires Node.js. Supports required/optional fields, type/length/pattern validation. |
| **`remark-lint-frontmatter-schema`** (npm) | 2/5 (easy) | High | Remark plugin that validates frontmatter against JSON Schema. Integrates with `remark-cli` for CI. More ecosystem buy-in than a standalone script. |
| **`frontmatter-json-schema-action`** (GitHub Action) | 1/5 (trivial) | High | GitHub Action by mheap. Validates YAML frontmatter against a JSON Schema. Zero local tooling needed — CI only. |

**Recommendation:** Use a custom Python script with JSON Schema. Fits the existing Python-only
toolchain, adds ~50 lines to the codebase, eliminates all LLM-based frontmatter review.

Example schema for this project:

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["type", "footer"],
  "properties": {
    "type": {
      "enum": ["title-slide", "content-slide", "dark-slide", "divider-slide"]
    },
    "footer": { "type": "string" },
    "image": { "type": "string" },
    "image_alt": { "type": "string" },
    "image_layout": { "enum": ["split", "inline", "divider"] },
    "section_number": { "type": "string" }
  },
  "additionalProperties": false
}
```

#### b) Content completeness checks

| Check | Implementation | Drop-in difficulty |
|-------|---------------|-------------------|
| Missing speaker notes | Python: check for `???` in each .md file | 1/5 (trivial) |
| Empty slide body | Python: check body length after frontmatter strip | 1/5 (trivial) |
| Footer numbering gaps | Python: extract all `footer` values, check sequence | 1/5 (trivial) |
| Unresolved `@@` directives | Already in build.py | N/A |
| Image existence | Already in build.py | N/A |

All of these are simple Python checks that can be added to build.py or a separate
`validate.py` script. None require an LLM.

#### c) markdownlint custom rules

markdownlint supports custom rules via the `customRules` option. For this project,
useful custom rules would be:

- **Require `???` separator**: Warn if a slide file has no speaker notes section
- **Validate `:::` block nesting**: Ensure `:::grid` blocks are properly closed
- **Check `[explainer:]` link targets**: Verify referenced HTML files exist

Custom rules are JavaScript functions that receive the document AST. Drop-in difficulty
is 2/5 (easy) but requires Node.js.

### Verdict

**Frontmatter validation is the highest-value, lowest-effort win.** A JSON Schema + 50-line
Python validator eliminates an entire class of "does this look right?" LLM checks. Content
completeness checks are similarly trivial. These are the highest token-savings opportunities
in the pipeline.

---

## 3. Template Engines: Can Jinja2/Mustache/Nunjucks replace build.py's HTML generation?

### Current state

`build.py` generates HTML through direct string concatenation with f-strings. The
`template.html` file provides the CSS/JS shell, and `build.py` splits it at the first/last
`<section>` tag to inject slide content.

### Alternatives assessed

| Engine | Language | Drop-in difficulty | Token savings | Tradeoffs |
|--------|---------|-------------------|--------------|-----------|
| **Jinja2** (Python) | Python | 2/5 (easy) | Low | Natural fit — same language as build.py. Would replace f-string HTML generation with `.html` template files. Gains: template inheritance, macros for repeated patterns (cards, quotes), auto-escaping. Loses: nothing — strictly better for HTML generation. |
| **Mustache** (multi-lang) | Python/JS/etc | 3/5 (medium) | Low | Logic-less templates. Forces separation of data from presentation. But the slide rendering logic (grid parsing, code highlighting, image layout) has conditional branches that Mustache can't express — would need a preprocessing step. |
| **Nunjucks** (JS) | JavaScript | 4/5 (hard) | Low | Mozilla's Jinja2 port for JavaScript. Feature-equivalent to Jinja2 but requires Node.js. No advantage over Jinja2 for a Python project. |

### Verdict

**Jinja2 would improve code quality but doesn't save tokens.** The HTML generation in
build.py is already deterministic and LLM-free. Migrating to Jinja2 templates would make
the slide HTML easier to read and modify (especially for designers), but it's a refactoring
exercise, not a static-tooling substitution.

If adopted, the migration path would be:
1. Create `templates/slide.html`, `templates/card.html`, `templates/quote.html`
2. Replace f-string generation in `render_body()`, `build_slide()`, `wrap_with_image()`
3. Use Jinja2 macros for repeated patterns
4. Keep the markdown parsing logic in Python (Jinja2 handles rendering, not parsing)

---

## 4. Image Generation: Alternatives to LLM-generated images

### Current state

The project uses a mix of:
- AI-generated images (e.g., `Gemini_Generated_Image_*.png`)
- Manually sourced images (e.g., `ralph.jpg`, `kent-v-genie-*.jpg`)
- Web-optimized JPEGs generated from PNGs via `make web-images` (`sips` command)

Image generation is currently **fully manual** — there is no automated pipeline. The
`make web-images` target only handles format conversion, not content creation.

### Alternatives assessed

#### a) Local AI image generation

| Tool | Drop-in difficulty | Token savings | Tradeoffs |
|------|-------------------|--------------|-----------|
| **Stable Diffusion WebUI (A1111)** | 3/5 (medium) | Med — replaces Gemini image prompting | Local generation via API (`--api` flag). Requires GPU (or very slow on CPU). Can script with `curl` to A1111 API. Produces consistent results with fixed seeds. No per-image cost. |
| **ComfyUI** | 3/5 (medium) | Med | Node-based workflow. More reproducible than A1111 (workflows are JSON DAGs). API support. Same GPU requirement. |
| **SDXL Turbo / LCM** | 2/5 (easy) | Med | Faster inference (1-4 steps). Good enough for presentation illustrations. Can run on Apple Silicon via MLX or `diffusers`. |
| **Flux (Black Forest Labs)** | 3/5 (medium) | Med | State-of-the-art quality. Flux.1-schnell is fast and open. Heavier model than SDXL. |

#### b) Stock photo APIs (deterministic, no generation)

| Service | API | Cost | Drop-in difficulty | Tradeoffs |
|---------|-----|------|-------------------|-----------|
| **Unsplash** | REST JSON | Free (50 req/hr demo, 5000/hr production) | 1/5 (trivial) | 3M+ high-res photos. Attribution required but no licensing fee. Python library `python-unsplash`. Could script a `make fetch-images` target. |
| **Pexels** | REST JSON | Free (200 req/hr) | 1/5 (trivial) | 1M+ photos/videos. No attribution required. Official Python library. |
| **Pixabay** | REST JSON | Free (100 req/min) | 1/5 (trivial) | 4M+ images. CC0 license. |

#### c) Pre-generated image libraries

| Approach | Drop-in difficulty | Token savings | Tradeoffs |
|----------|-------------------|--------------|-----------|
| **Curated image directory** | 1/5 (trivial) | High — no generation needed | Manually select and commit all images upfront. Most deterministic. Already partially in place (`images/` directory). |
| **Brand asset library** | 1/5 (trivial) | High | Six Feet Up likely has brand imagery. Use it directly. |
| **Icon/illustration libraries** (Heroicons, unDraw, etc.) | 1/5 (trivial) | High | SVG illustrations. Consistent style. No generation. unDraw offers customizable illustrations. |

### Verdict

**The current approach (pre-generated + committed images) is already the most deterministic
option.** The only LLM-dependent step is the initial creation of AI-generated images, which
is a one-time cost per image, not a recurring pipeline step.

For future images, the best static alternatives are:
1. **Stock photo APIs** (Unsplash/Pexels) for photographic content — trivial to integrate,
   free, and deterministic once downloaded
2. **SVG illustration libraries** (unDraw, Heroicons) for diagrammatic content — consistent
   style, no generation
3. **Local Stable Diffusion** (SDXL Turbo via `diffusers`) for custom illustrations — one-time
   generation with fixed seeds for reproducibility, no per-image API cost

---

## Summary: Token Savings by Area

| Area | Current LLM dependence | Static alternative | Token savings | Effort |
|------|----------------------|-------------------|--------------|--------|
| **Slide generation** | None (build.py is pure Python) | N/A — already static | None | N/A |
| **Frontmatter validation** | LLM reviews "does this look right?" | JSON Schema + Python validator | **High** | ~50 lines |
| **Content completeness** | LLM checks for missing notes, empty slides | Python checks in build.py or validate.py | **High** | ~30 lines |
| **markdownlint** | Already static | Already in place (`make lint`) | N/A | N/A |
| **Template rendering** | None (f-strings are deterministic) | Jinja2 (optional refactor) | **Low** | ~200 lines |
| **Image creation** | Gemini/AI for initial generation | Stock APIs or local SD | **Med** | Varies |
| **Image optimization** | None (`make web-images` uses `sips`) | N/A — already static | None | N/A |

### Top recommendations (by effort-to-value ratio)

1. **Add frontmatter JSON Schema validation** — highest value, lowest effort. Eliminates
   a recurring LLM review task with a 50-line script.
2. **Add content completeness checks** — check for missing `???` notes, empty bodies,
   footer gaps. 30 lines of Python.
3. **Use stock photo APIs for future images** — Unsplash/Pexels are free, trivial to
   integrate, and eliminate the need for LLM image generation prompting.
4. **Consider Jinja2 for template rendering** — nice-to-have refactor, not urgent.
   Improves maintainability but doesn't save tokens.

---

## References

- [Marp CLI](https://github.com/marp-team/marp-cli) / [Marpit plugins](https://marpit.marp.app/usage?id=extend-marpit-by-plugins)
- [remark.js](https://remarkjs.com/) / [remark-directive](https://github.com/remarkjs/remark-directive)
- [reveal-md](https://github.com/webpro/reveal-md)
- [Slidev](https://sli.dev/)
- [Darkslide](https://github.com/ionelmc/python-darkslide)
- [Pyremark](https://wcchin.github.io/pyremark_slides/)
- [markdownlint custom rules](https://github.com/DavidAnson/markdownlint/blob/main/doc/CustomRules.md)
- [@github-docs/frontmatter](https://www.npmjs.com/package/@github-docs/frontmatter)
- [remark-lint-frontmatter-schema](https://github.com/JulianCataldo/remark-lint-frontmatter-schema)
- [frontmatter-json-schema-action](https://github.com/mheap/frontmatter-json-schema-action)
- [Jinja2](https://pypi.org/project/Jinja2/)
- [Stable Diffusion WebUI API](https://github.com/AUTOMATIC1111/stable-diffusion-webui/wiki/API)
- [Unsplash API](https://unsplash.com/developers)
- [Pexels API](https://www.pexels.com/api/)
- [unDraw](https://undraw.co/)
