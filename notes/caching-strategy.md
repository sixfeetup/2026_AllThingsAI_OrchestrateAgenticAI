# Caching Strategy for LLM Outputs

Research into caching LLM outputs so identical inputs don't re-invoke the model.

## Current State

The project has **no LLM calls in its build pipeline**. `build.py` is a pure
Python markdown-to-HTML renderer with zero API calls. The only LLM integration
is `images/generate_images.py`, which calls Google Gemini for image generation
and already has a skip-if-exists pattern.

This means: **there are currently zero LLM tokens to save**. The caching
strategies below are written for the scenario where LLM calls are introduced
(e.g., AI-assisted content generation, slide summarization, speaker note
generation, or @@ directive auto-resolution).

---

## 1. Content-Addressable Storage

**Concept:** Hash the input (slide markdown + prompt template) to produce a
cache key. Store the LLM output keyed by that hash. On subsequent runs, check
the cache before calling the model.

### Recommended Implementation

```python
import hashlib
import json
from pathlib import Path

CACHE_DIR = Path(".cache/llm")

def cache_key(prompt: str, model: str, slide_content: str = "") -> str:
    """SHA-256 of the full input to the LLM."""
    payload = json.dumps({
        "prompt": prompt,
        "model": model,
        "content": slide_content,
    }, sort_keys=True)
    return hashlib.sha256(payload.encode()).hexdigest()

def cached_llm_call(prompt: str, model: str, content: str = "") -> str | None:
    """Return cached result or None."""
    key = cache_key(prompt, model, content)
    cache_file = CACHE_DIR / f"{key}.json"
    if cache_file.exists():
        return json.loads(cache_file.read_text())["output"]
    return None

def store_llm_result(prompt: str, model: str, content: str, output: str) -> None:
    """Write LLM result to content-addressable cache."""
    key = cache_key(prompt, model, content)
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    (CACHE_DIR / f"{key}.json").write_text(json.dumps({
        "prompt": prompt,
        "model": model,
        "content": content,
        "output": output,
        "key": key,
    }, indent=2))
```

### Design Decisions

- **SHA-256 over MD5:** Collision-resistant; future-proof. MD5 is fine for
  change detection (`check-changes.sh`) but not for cache identity.
- **JSON-serialized input:** Deterministic via `sort_keys=True`. Includes model
  name so cache is invalidated on model change.
- **Flat file storage:** No database needed. `.cache/llm/` directory with one
  JSON file per cached result. Add to `.gitignore`.
- **Cache includes metadata:** Storing the original prompt alongside the output
  enables debugging and auditing.

### Estimated Token Savings

Assuming a hypothetical workflow that processes 17 slides with ~500-token
prompts:

| Scenario | Tokens per build | With cache (no changes) | Savings |
|----------|-----------------|------------------------|---------|
| Speaker note generation | ~17,000 | 0 | 100% |
| Slide summarization | ~8,500 | 0 | 100% |
| Single slide edit rebuild | ~17,000 | ~1,000 | 94% |

---

## 2. Incremental Rebuilds (Slide-Level Hashing)

**Current state:** `check-changes.sh` hashes ALL watched files into a single
MD5. This is all-or-nothing: any change to any file triggers a full rebuild.

### Recommended Extension

Replace the single combined hash with per-file hashes stored in a JSON state
file:

```bash
# check-changes.sh v2 concept
# State file: presentation/.watch-state.json
# Format: {"01-title.md": "abc123...", "02-backstory.md": "def456..."}
```

Python implementation for `build.py`:

```python
import json
import hashlib
from pathlib import Path

STATE_FILE = Path("presentation/.build-cache.json")

def load_state() -> dict:
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text())
    return {}

def save_state(state: dict) -> None:
    STATE_FILE.write_text(json.dumps(state, indent=2))

def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def changed_slides(md_files: list[Path]) -> list[Path]:
    """Return only slides whose content has changed since last build."""
    state = load_state()
    changed = []
    new_state = {}
    for f in md_files:
        h = file_hash(f)
        new_state[f.name] = h
        if state.get(f.name) != h:
            changed.append(f)
    save_state(new_state)
    return changed
```

### How This Integrates with the Build

The build is currently monolithic: all slides are rendered and concatenated into
a single HTML file. Incremental rebuilds would work as follows:

1. **Slide-level caching:** Cache each slide's rendered HTML keyed by its source
   hash. On rebuild, only re-render changed slides.
2. **Assembly remains full:** The final concatenation step always runs (it's
   fast — pure string concat), but individual `build_slide()` calls are skipped
   for unchanged slides.

```python
SLIDE_CACHE_DIR = Path(".cache/slides")

def build_slide_cached(md_file: Path) -> str:
    """Build slide HTML, using cache if source hasn't changed."""
    content = md_file.read_text()
    h = hashlib.sha256(content.encode()).hexdigest()
    cache_file = SLIDE_CACHE_DIR / f"{md_file.stem}-{h}.html"

    if cache_file.exists():
        return cache_file.read_text()

    meta, body = parse_frontmatter(content)
    body = strip_directives(body)
    html = build_slide(meta, body)

    SLIDE_CACHE_DIR.mkdir(parents=True, exist_ok=True)
    cache_file.write_text(html)
    return html
```

### Invalidation Triggers

The slide cache must be invalidated when:

| Change | Invalidates |
|--------|-------------|
| Slide markdown changed | That slide only |
| `template.html` changed | All slides (CSS/JS shell) |
| `build.py` changed | All slides (rendering logic) |
| Prompt template changed | Slides using that prompt |

Include `build.py` and `template.html` hashes in the global cache key:

```python
def global_cache_version() -> str:
    """Hash of build infrastructure — change invalidates all caches."""
    parts = [
        file_hash(Path("presentation/build.py")),
        file_hash(Path("presentation/template.html")),
    ]
    return hashlib.sha256("".join(parts).encode()).hexdigest()[:12]
```

### Compatibility with check-changes.sh

`check-changes.sh` is used for the `make watch` target to decide whether to
trigger a rebuild. This can remain as-is (coarse-grained gate), while the
per-slide caching operates within `build.py` (fine-grained optimization). The
two are complementary:

```
check-changes.sh: "Did anything change?" (fast gate)
     └── build.py: "Which slides changed?" (fine-grained skip)
```

---

## 3. @@ Directive Caching

**Current state:** @@ directives are currently placeholders that are either
stripped or warned about. There is no automatic resolution mechanism.

### If Auto-Resolution Were Added

If @@ directives were resolved via LLM calls, caching would work as follows:

```python
def resolve_directive(directive: str, context: str) -> str:
    """Resolve a @@ directive, using cache if available."""
    key = cache_key(
        prompt=f"resolve directive: {directive}",
        model="claude-sonnet-4-6",
        content=context,
    )
    cached = cached_llm_call(
        prompt=f"resolve directive: {directive}",
        model="claude-sonnet-4-6",
        content=context,
    )
    if cached:
        print(f"  Cache hit for {directive}")
        return cached

    result = call_llm(directive, context)
    store_llm_result(
        prompt=f"resolve directive: {directive}",
        model="claude-sonnet-4-6",
        content=context,
        output=result,
    )
    return result
```

### Cache Key Considerations for Directives

A directive's cache key should include:

1. **The directive text itself** (`@@generate_summary`)
2. **The surrounding slide content** (context the LLM sees)
3. **The model version** (different models produce different outputs)
4. **The prompt template version** (if using a template)

If the directive is `@@generate_summary` and the slide content hasn't changed,
the cache hit rate should be ~100%.

### Directive Resolution Modes

```
--resolve-directives       # Resolve all @@ directives (default: skip)
--force-resolve            # Ignore cache, re-resolve all
--resolve-changed-only     # Only resolve directives in changed slides
```

---

## 4. Image Caching (Formalizing the Pattern)

**Current state in `generate_images.py`:**

```python
if os.path.exists(path):
    print(f"Skipping {filename}, already exists.")
    continue
```

This is a good start but has limitations:

1. **No prompt change detection:** If the prompt changes, the old image is still
   used (the filename is the key, not the prompt content).
2. **No corruption detection:** A truncated or corrupt file is treated as valid.
3. **No cache invalidation:** Deleting the file is the only way to regenerate.

### Recommended Formalization

Add a manifest file that tracks prompt-to-file mappings:

```python
MANIFEST_FILE = Path("images/.image-manifest.json")

def image_manifest() -> dict:
    if MANIFEST_FILE.exists():
        return json.loads(MANIFEST_FILE.read_text())
    return {}

def needs_regeneration(filename: str, prompt: str) -> bool:
    """Check if image needs regeneration based on prompt hash."""
    manifest = image_manifest()
    path = Path("output_images") / filename
    if not path.exists():
        return True

    prompt_hash = hashlib.sha256(prompt.encode()).hexdigest()
    entry = manifest.get(filename, {})
    if entry.get("prompt_hash") != prompt_hash:
        return True  # Prompt changed

    # Optional: check file size > 0 for corruption detection
    if path.stat().st_size == 0:
        return True

    return False

def update_manifest(filename: str, prompt: str) -> None:
    manifest = image_manifest()
    manifest[filename] = {
        "prompt_hash": hashlib.sha256(prompt.encode()).hexdigest(),
        "generated_at": datetime.now().isoformat(),
        "model": MODEL_NAME,
    }
    MANIFEST_FILE.write_text(json.dumps(manifest, indent=2))
```

### Web Image Caching (Makefile)

The `make web-images` target converts PNGs to `_web.jpg` via `sips`. This could
also use timestamp or hash comparison:

```makefile
# Current: always regenerates
# Improved: skip if _web.jpg is newer than source .png
images/%_web.jpg: images/%.png
	sips -s format jpeg -s formatOptions 80 \
	     --resampleWidth 1400 "$<" --out "$@"
```

Make's built-in timestamp comparison already handles this if expressed as a
proper dependency rule (which it currently isn't — the existing target uses a
`for` loop).

---

## 5. Lessons from CI/CD Caching Systems

### GitHub Actions Cache

The current workflow (`deploy.yml`) does no caching. Opportunities:

```yaml
# Cache uv dependencies
- uses: actions/cache@v4
  with:
    path: ~/.cache/uv
    key: uv-${{ runner.os }}-${{ hashFiles('**/pyproject.toml') }}

# Cache built slide HTML fragments
- uses: actions/cache@v4
  with:
    path: .cache/slides
    key: slides-${{ hashFiles('presentation/content/*.md', 'presentation/build.py', 'presentation/template.html') }}

# Cache generated images (if ever generated in CI)
- uses: actions/cache@v4
  with:
    path: images/output_images
    key: images-${{ hashFiles('images/generate_images.py') }}
```

### Key Patterns from Turborepo / Nx

| Pattern | Application Here |
|---------|-----------------|
| **Input hashing** | Hash slide content + build script + template = cache key |
| **Task graph** | Slides are independent; can be cached/rebuilt independently |
| **Remote cache** | Not needed — this is a single-developer presentation project |
| **Affected detection** | `git diff --name-only` to find changed slides |
| **Output fingerprinting** | Hash the output HTML to detect no-op builds |

### Turborepo-Style Pipeline Definition

If this project grew to have LLM-assisted generation, the pipeline would look
like:

```
content/*.md ──┐
               ├── [hash inputs] ── cache check ── build_slide() ── cache store
template.html ─┘
                                         │
                                    [if cache miss]
                                         │
                                    call LLM ── store result
```

### Nx-Style Affected Commands

```bash
# Only rebuild slides affected by changes since last commit
uv run build.py --affected=$(git diff --name-only HEAD~1 -- presentation/content/)
```

---

## 6. Consolidated Recommendations

### Priority 1: No-Op (Current State is Fine)

The build pipeline has **no LLM calls**, so there are **no tokens to save**.
The current architecture is efficient:

- `build.py` renders 17 slides in <1 second (pure Python, no I/O bottleneck)
- `check-changes.sh` prevents unnecessary rebuilds
- `generate_images.py` skips existing images
- CI deploys only on changes to relevant paths

**Do not add caching infrastructure unless LLM calls are introduced.**

### Priority 2: If LLM Calls Are Added

Implement in this order:

1. **Content-addressable LLM cache** (Section 1) — highest impact, simplest to
   add. A `cached_llm_call()` wrapper around any API call.

2. **Slide-level hashing** (Section 2) — extend `build.py` to track per-slide
   hashes and skip unchanged slides. Useful even without LLM calls if the build
   grows more expensive.

3. **Image manifest** (Section 4) — upgrade `generate_images.py` to track
   prompt hashes, not just file existence. Low effort, prevents stale images.

4. **CI caching** (Section 5) — add `actions/cache` for uv dependencies.
   Minimal but saves ~10s per CI run.

5. **Directive caching** (Section 3) — only relevant if @@ auto-resolution is
   built. Follows naturally from the content-addressable cache.

### Priority 3: Things NOT to Do

- **Don't add Redis or a database.** File-based caching in `.cache/` is
  sufficient for a single-developer presentation project.
- **Don't add remote caching (Turborepo-style).** No team to share cache with.
- **Don't add cache warming or prefetching.** The dataset (17 slides) is too
  small to benefit.
- **Don't cache template rendering.** `build.py` runs in <1s. Caching would add
  complexity without meaningful speedup.

---

## Estimated Token Savings Summary

| Feature | Without Cache | With Cache | Savings |
|---------|--------------|------------|---------|
| No LLM calls (current) | 0 tokens | 0 tokens | N/A |
| Speaker note generation (hypothetical) | ~17K/build | ~1K/build* | ~94% |
| Directive resolution (hypothetical) | ~5K/build | ~300/build* | ~94% |
| Image generation (Gemini) | ~3K/build | 0/build | 100%** |

\* Assumes 1 of 17 slides changed per build.
\** Already cached via skip-if-exists; manifest would add prompt-change
detection.

---

## File Layout

```
.cache/                    # Gitignored
├── llm/                   # Content-addressable LLM output cache
│   ├── a1b2c3...json      # Cached LLM response
│   └── d4e5f6...json
├── slides/                # Per-slide rendered HTML cache
│   ├── 01-title-abc123.html
│   └── 02-backstory-def456.html
└── version                # Global cache version (build.py + template hash)

images/
└── .image-manifest.json   # Prompt hash -> filename mapping

presentation/
└── .build-cache.json      # Per-file content hashes for incremental builds
```
