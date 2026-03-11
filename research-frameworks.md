# Research: Deterministic Slide Deck Generation from Markdown

## Survey of Frameworks and Best Practices

**Date:** 2026-03-11
**Context:** This project uses a custom Python build pipeline (`build.py`) that compiles
`content/*.md` files with YAML frontmatter into a single self-contained HTML deck. This
research evaluates how established frameworks handle the same concerns, with focus on
what makes builds reproducible and what causes drift between source and output.

---

## Framework Comparison

### 1. remark.js

**Architecture:** Pure client-side — a single HTML file loads `remark-latest.min.js` from CDN
(or bundled locally) and renders markdown at runtime in the browser. No build step.

| Concern | How remark.js handles it |
|---------|--------------------------|
| **Images** | Standard markdown `![alt](url)`. No asset pipeline or optimization. Images must be manually managed alongside the HTML file. |
| **Speaker notes** | `???` separator in markdown. Press `P` for presenter mode with notes + next-slide preview. Identical to our current `???` convention. |
| **Theming** | Plain CSS. No built-in themes — you write CSS directly in the HTML file or import a stylesheet. Simple but no guardrails. |
| **CI/CD builds** | No build step to automate. The HTML file *is* the artifact. CI can only validate markdown syntax or serve the file. |
| **Content validation** | None built-in. No frontmatter parsing, no schema enforcement. |

**Reproducibility profile:** Excellent by default — there's nothing to build. The markdown
*is* the presentation. Drift risk comes from CDN version changes (`remark-latest.min.js`
vs pinned version). Pinning the JS version eliminates all non-determinism.

**Key insight:** The simplest path to determinism is eliminating the build step entirely.
Client-side rendering means the source file IS the artifact.

---

### 2. reveal.js / reveal-md

**Architecture:** reveal.js is an HTML presentation framework; reveal-md wraps it to accept
markdown input and produce standalone HTML output.

| Concern | How reveal.js handles it |
|---------|--------------------------|
| **Images** | Standard markdown/HTML images. `reveal-md --static` copies adjacent assets into the output directory automatically. No image optimization. Absolute file paths not supported — must use relative paths or absolute URLs. |
| **Speaker notes** | Lines after `Note:` in markdown. Built-in speaker view with timer, next-slide preview, and notes. Configurable via `data-separator-notes` regex. |
| **Theming** | Rich built-in theme system (black, white, league, solarized, etc.). Custom themes via CSS. Per-presentation overrides via YAML frontmatter. `--theme` flag or `--css` for injection. |
| **CI/CD builds** | `reveal-md slides.md --static _static` produces a standalone directory. Can be deployed to any static host. No official GitHub Action but straightforward to script. |
| **Content validation** | YAML frontmatter for per-slide config (separator, theme, transitions). No schema validation. No linting integration. |

**Reproducibility profile:** Moderate. The `--static` export bundles all dependencies, but
output includes timestamps and non-deterministic ordering in some cases. The npm dependency
tree (reveal.js version, plugin versions) must be locked. reveal-md's output structure
can shift between versions.

**Key insight:** YAML frontmatter per-presentation is a clean pattern for overriding defaults
without CLI flags. The `--static-dirs` flag for explicit asset inclusion prevents missing-image
drift.

---

### 3. Marp (Marp CLI + Marpit)

**Architecture:** CLI tool that converts Marp-flavored markdown to HTML, PDF, PPTX, or images.
Uses a headless browser (Chrome/Edge/Firefox) for PDF/image rendering.

| Concern | How Marp handles it |
|---------|---------------------|
| **Images** | Standard markdown images. `--allow-local-files` flag required for local assets (security default). Background images via `![bg](url)` directive — unique to Marp. Image scaling via `--image-scale` for high-DPI output. |
| **Speaker notes** | HTML comments `<!-- notes -->` become speaker notes. `--pdf-notes` flag includes them in PDF output. `--notes` exports notes as plain text. |
| **Theming** | 3 built-in themes (default, gaia, uncover). Custom themes via plain CSS with `@theme` metadata. Themes loaded via `--theme` flag or `--theme-set` for directories. |
| **CI/CD builds** | Official GitHub Action (`marp-team/marp-cli-action`). `marp-slides-template` repo provides a complete GitHub Pages workflow. Parallel file processing (5 concurrent by default, configurable). |
| **Content validation** | Marp-specific frontmatter (`marp: true`, `theme:`, `paginate:`). No built-in linting, but community uses markdownlint with Marp-specific `.markdownlint.json` to suppress rules like MD033 (inline HTML). |

**Reproducibility profile:** Good for HTML output. PDF output depends on browser version —
Chrome 120 and Chrome 125 may render differently. Browser version is the primary source of
non-determinism. The `--browser-path` flag helps pin a specific browser binary.

**Key insight:** Marp's biggest contribution to reproducibility is the official GitHub Action
and template repo — the CI/CD story is first-class. The browser dependency for PDF is the
main drift risk. For HTML-only output, builds are highly deterministic.

---

### 4. Slidev

**Architecture:** Vue 3 + Vite-based SPA. Markdown slides are compiled to Vue components at
build time. Rich interactive features (live coding, Monaco editor, animations).

| Concern | How Slidev handles it |
|---------|----------------------|
| **Images** | Standard markdown images, plus Vue component embedding. Assets in `public/` directory are served as-is. Vite's asset pipeline handles hashing and bundling. |
| **Speaker notes** | HTML comments `<!-- notes -->` per slide. Built-in presenter mode with timer, notes, and slide overview. `--without-notes` flag strips them from production builds. |
| **Theming** | Theme gallery with installable npm packages. UnoCSS (Tailwind-like) for utility classes. Per-slide layout customization via frontmatter. Windi CSS support. |
| **CI/CD builds** | `slidev build` produces static SPA in `dist/`. Official docs include GitHub Actions, Netlify, Vercel, and Docker deployment recipes. `--base` flag for sub-path deployment. Glob support for multi-deck builds. |
| **Content validation** | `slidev format` normalizes markdown structure (not content). Open feature request (#1749) for `slidev check` command with markdownlint integration — currently "p2-nice-to-have", not implemented. |

**Reproducibility profile:** Moderate-to-poor. Vite's build includes content hashing (good for
cache busting, bad for diffing outputs). The npm dependency tree is deep (Vue, Vite, UnoCSS,
Shiki, etc.) — lockfile discipline is essential. Build output changes between Vite versions
even with identical source. CSS utility class generation order can vary.

**Key insight:** Slidev is the most feature-rich but the least deterministic. The deep
dependency tree means lockfile + Node version pinning are critical. The `slidev format`
command is a useful pattern — normalizing source before build reduces one category of drift.
Docker builds with pinned images help, but don't fully solve the Vite output variability.

---

### 5. mdx-deck

**Architecture:** React + MDX. Slides written in MDX (markdown + JSX). Uses Gatsby/webpack
under the hood. Theme UI + Emotion for styling.

| Concern | How mdx-deck handles it |
|---------|-------------------------|
| **Images** | Standard markdown images plus React `<Image>` component with background image support. `<BackgroundImage>` component for full-bleed slides. Webpack handles asset bundling. |
| **Speaker notes** | `<Notes>` React component. Presenter mode via `Option+P` with next-slide preview and timer. |
| **Theming** | Theme UI system — deeply customizable. Multiple built-in themes. Component-level overrides. CSS-in-JS via Emotion. |
| **CI/CD builds** | `mdx-deck build` produces static HTML+JS bundle. Standard React/webpack build process. No official CI recipes. |
| **Content validation** | None. MDX parsing will fail on invalid JSX, which provides some structural validation but no content-level checks. |

**Reproducibility profile:** Poor. webpack builds are notoriously non-deterministic without
careful configuration. The project's maintenance has slowed significantly — last meaningful
updates were 2020-2021. Dependency rot is a real concern. Theme UI + Emotion + webpack
creates a deep, shifting dependency surface.

**Key insight:** mdx-deck demonstrates the power of mixing markdown with components (React),
but the maintenance trajectory is a warning. For long-lived presentations, framework health
matters as much as features. The JSX-in-markdown pattern is powerful but increases the
blast radius of dependency changes.

---

## Cross-Cutting Analysis

### What Makes Builds Reproducible

| Factor | Best practice | Who does it well |
|--------|--------------|-----------------|
| **Minimal dependencies** | Fewer deps = fewer sources of drift | remark.js (zero build deps) |
| **Pinned versions** | Lockfiles, pinned CDN URLs, Docker images | Marp (official GH Action pins versions) |
| **No browser dependency** | HTML output avoids browser rendering variance | Marp HTML, remark.js, our build.py |
| **Deterministic asset paths** | No content hashing in output paths | remark.js, reveal-md static export |
| **Source normalization** | Format/lint source before build | Slidev (`slidev format`), markdownlint |
| **Template separation** | Template + content = output (no hidden state) | Our build.py, Marp themes |
| **Explicit asset manifests** | Declare which images are needed, validate they exist | None do this well |

### What Causes Drift Between Source and Output

1. **Browser rendering differences** (PDF/image output via headless Chrome)
2. **npm dependency updates** changing CSS generation, bundling, or output format
3. **Non-deterministic build tools** (webpack chunk IDs, Vite content hashes, CSS ordering)
4. **Implicit state** (OS fonts, locale, timezone affecting date rendering)
5. **CDN version drift** (loading `latest.min.js` instead of pinned version)
6. **Template/theme updates** separate from content changes
7. **Missing asset validation** — nothing checks that referenced images exist

### Content Validation Patterns

No framework provides strong content validation out of the box. The best practice across
the ecosystem is:

1. **markdownlint** in CI — with presentation-specific rule overrides (allow duplicate
   headings, inline HTML, etc.)
2. **Frontmatter schema validation** — custom scripts or JSON Schema to validate YAML
   metadata (slide type, required fields, etc.)
3. **Asset existence checks** — grep image references from markdown, verify files exist
4. **Directive/placeholder scanning** — detect unresolved placeholders (our `@@` pattern
   in build.py is ahead of the curve here)
5. **Build comparison** — diff output HTML between builds to detect unexpected changes

---

## Relevance to This Project

Our current `build.py` already implements several best practices:

| Practice | Status in build.py |
|----------|-------------------|
| Markdown source of truth | ✅ `content/*.md` with YAML frontmatter |
| Deterministic ordering | ✅ `sorted()` glob of numbered files |
| Template separation | ✅ `template.html` separate from content |
| Speaker notes | ✅ `???` separator (remark.js convention) |
| Placeholder detection | ✅ `@@` directive scanning with warnings |
| Minimal dependencies | ✅ Only `pyyaml`, runs via `uv run` |
| No browser dependency | ✅ Pure Python string-based HTML generation |
| Dual output (dev + deploy) | ✅ `output/` and `dist/` with path adjustment |

### Gaps worth noting (not recommendations to implement):

- **No image existence validation** — referenced images could be missing without error
- **No frontmatter schema enforcement** — invalid `type:` values silently pass through
- **No output diffing** — no way to detect unexpected output changes in CI
- **No CSS/theme versioning** — template.html changes aren't tracked separately from content

### Patterns worth borrowing:

- **Marp's `--pdf-notes` and `--notes` flags** — exporting speaker notes separately is
  useful for rehearsal and accessibility
- **Slidev's `format` command** — normalizing markdown source before build prevents
  whitespace-driven output changes
- **reveal-md's YAML frontmatter for config** — already in use; consider validating it
- **markdownlint in CI** — with presentation-specific `.markdownlint.json`

---

## Summary Table

| Framework | Determinism | Maintenance | CI/CD Story | Image Handling | Notes Support | Best For |
|-----------|------------|-------------|-------------|----------------|---------------|----------|
| **remark.js** | ⭐⭐⭐⭐⭐ | Low activity | N/A (no build) | Basic | `???` separator | Maximum simplicity |
| **reveal.js** | ⭐⭐⭐ | Active | Good (reveal-md) | Auto-copy on export | `Note:` prefix | Rich features + ecosystem |
| **Marp** | ⭐⭐⭐⭐ | Active | Excellent (official GH Action) | `--allow-local-files` | HTML comments | CI/CD-first workflows |
| **Slidev** | ⭐⭐ | Very active | Good (docs for all hosts) | Vite asset pipeline | HTML comments | Developer presentations |
| **mdx-deck** | ⭐ | Dormant | Poor | webpack bundling | `<Notes>` component | React-heavy teams (legacy) |
| **Our build.py** | ⭐⭐⭐⭐ | Project-specific | Makefile + gh-pages | Path rewriting | `???` separator | This presentation |

---

## References

- [remark.js](https://remarkjs.com/) / [GitHub](https://github.com/gnab/remark)
- [reveal.js](https://revealjs.com/) / [reveal-md](https://github.com/webpro/reveal-md)
- [Marp](https://marp.app/) / [Marp CLI](https://github.com/marp-team/marp-cli) / [GH Action](https://github.com/marketplace/actions/marp-cli-action)
- [Slidev](https://sli.dev/) / [GitHub](https://github.com/slidevjs/slidev) / [Build docs](https://sli.dev/guide/hosting)
- [mdx-deck](https://github.com/jxnblk/mdx-deck)
- [markdownlint](https://github.com/DavidAnson/markdownlint)
- [Slidev validation issue #1749](https://github.com/slidevjs/slidev/issues/1749)
- [Reproducible Builds](https://reproducible-builds.org/docs/deterministic-build-systems/)
