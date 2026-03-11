# Contract Testing for Slide Content

Research into static validation approaches that eliminate the need for
LLM-based content checking. Each section covers: what to validate,
implementation approach, complexity, and LLM calls eliminated.

---

## 1. YAML Frontmatter Schema Validation

### What exists today

`build.py` reads frontmatter with `yaml.safe_load()` and passes values
through without validation. Invalid `type`, misspelled `image_layout`,
or missing `footer` are silently accepted and produce broken output.

### Current frontmatter fields (observed across all 18 slides)

| Field            | Required? | Valid values                                              |
|------------------|-----------|-----------------------------------------------------------|
| `type`           | Yes       | `title-slide`, `content-slide`, `dark-slide`, `divider-slide` |
| `footer`         | No*       | String (slide number), absent only on title/question slides |
| `image`          | No        | Relative path `../images/filename`                         |
| `image_alt`      | If image  | Non-empty string                                           |
| `image_layout`   | If image  | `split`, `inline`, `divider`                               |
| `section_number` | No        | String (Roman numeral), divider slides only                 |

*`footer` is absent on 01-title.md and 16-questions.md (both `title-slide` type).

### Implementation approach

**Option A: JSON Schema validated in build.py (recommended)**

Add a JSON Schema definition and validate each slide's frontmatter
during build. Python's `jsonschema` library is mature and lightweight.

```python
# slide_schema.json (or inline dict in build.py)
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "type": "object",
  "required": ["type"],
  "properties": {
    "type": {
      "enum": ["title-slide", "content-slide", "dark-slide", "divider-slide"]
    },
    "footer": { "type": "string" },
    "image": { "type": "string", "pattern": "^\\.\\./images/.+" },
    "image_alt": { "type": "string", "minLength": 1 },
    "image_layout": { "enum": ["split", "inline", "divider"] },
    "section_number": { "type": "string" }
  },
  "if": {
    "properties": { "image": { "type": "string" } },
    "required": ["image"]
  },
  "then": {
    "required": ["image_alt"]
  },
  "additionalProperties": false
}
```

Integration point: after `parse_frontmatter()` in `build()`, call
`jsonschema.validate(meta, schema)`. Build fails fast on invalid slides.

**Option B: Pydantic model**

Define a `SlideMeta` dataclass/Pydantic model. More Pythonic but adds a
heavier dependency. JSON Schema is simpler for this use case.

### Complexity

Low. ~50 lines of schema + ~10 lines of validation code in `build.py`.
One new dependency (`jsonschema`) or zero if using manual validation.

### LLM calls eliminated

Replaces any LLM-based "check if slide frontmatter is valid" review.
Estimated **1-2 LLM calls per PR** that touches slides — every PR
modifying slide files currently needs manual or LLM review to catch
frontmatter typos.

---

## 2. Slide Body Linting (markdownlint)

### What exists today

A `.markdownlint.json` config exists in `presentation/` that disables
7 rules (MD013, MD024, MD026, MD033, MD036, MD041, MD049). The Makefile
has a `lint` target: `npx --yes markdownlint-cli 'content/*.md'`.

This provides basic markdown hygiene but no slide-specific conventions.

### Slide-specific rules needed

| Convention                           | How to enforce                               |
|--------------------------------------|----------------------------------------------|
| Max 7 bullets per slide              | Custom markdownlint rule or build.py check   |
| Exactly one `# Heading` per slide    | Custom rule or build.py check                |
| No `####` or deeper headings         | MD025 variant or build.py check              |
| Grid syntax must be balanced         | build.py check (not markdown-native)          |
| `_subtitle_` and `*tagline*` usage   | build.py check                               |

### Implementation approach

**For standard markdown rules:** Extend `.markdownlint.json` with
stricter settings. Example additions:

```json
{
  "MD025": true,
  "heading-depth": { "max": 3 }
}
```

**For slide-specific rules:** Add a `validate_body()` function in
`build.py` that runs after parsing. This is better than markdownlint
custom rules because the conventions (grid syntax, `???` separator,
`_subtitle_`) are project-specific and not standard markdown.

```python
def validate_body(body: str, filename: str) -> list[str]:
    """Check slide body against conventions."""
    warnings = []
    visible, notes = split_notes(body)
    lines = visible.strip().split("\n")

    # Count bullets
    bullets = [l for l in lines if l.startswith("- ")]
    if len(bullets) > 7:
        warnings.append(f"{filename}: {len(bullets)} bullets (max 7)")

    # Count top-level headings
    h1s = [l for l in lines if re.match(r"^# ", l)]
    if len(h1s) != 1:
        warnings.append(f"{filename}: {len(h1s)} H1 headings (expected 1)")

    # No deep headings
    deep = [l for l in lines if re.match(r"^#{4,} ", l)]
    if deep:
        warnings.append(f"{filename}: heading deeper than H3")

    return warnings
```

### Complexity

Low-Medium. The markdownlint config changes are trivial. The
`validate_body()` function is ~30 lines and integrates into the existing
build pipeline alongside `validate_images()`.

### LLM calls eliminated

Replaces "check that slides follow formatting conventions" reviews.
Estimated **1-3 LLM calls per PR** — any PR adding or modifying slides
currently requires style review that could be automated.

---

## 3. Speaker Notes Validation

### What exists today

`split_notes()` splits on `???` but doesn't validate presence or
content. A slide with no `???` section silently gets empty notes.
PR #20 added speaker notes to 8 slides that were missing them —
that fix was found by manual/LLM review.

### What to validate

| Check                        | Rule                                          |
|------------------------------|-----------------------------------------------|
| `???` section exists         | Required on all slides                         |
| Minimum content              | At least 2 non-empty lines after `???`         |
| No placeholder text          | Reject "TODO", "TBD", "PLACEHOLDER"            |

### Implementation approach

Add to `build.py` alongside `validate_images()`:

```python
def validate_notes(md_files: list[Path]) -> list[str]:
    """Ensure all slides have speaker notes."""
    warnings = []
    for md_file in md_files:
        text = md_file.read_text()
        _, body = parse_frontmatter(text)

        if "???" not in body:
            warnings.append(f"  ✗  {md_file.name}: missing speaker notes (no ??? section)")
            continue

        _, notes = split_notes(body)
        non_empty = [l for l in notes.split("\n") if l.strip()]
        if len(non_empty) < 2:
            warnings.append(
                f"  ⚠  {md_file.name}: speaker notes too short "
                f"({len(non_empty)} lines, minimum 2)"
            )

        # Check for placeholder text
        if re.search(r"\b(TODO|TBD|PLACEHOLDER|FIXME)\b", notes, re.IGNORECASE):
            warnings.append(f"  ⚠  {md_file.name}: speaker notes contain placeholder text")

    return warnings
```

### Complexity

Low. ~20 lines. Drops directly into the existing validation pattern in
`build()`.

### LLM calls eliminated

Directly replaces the work done in PR #20 (adding missing speaker
notes detection). Estimated **1 LLM call per PR** that adds slides —
the "do all slides have speaker notes?" check is currently manual or
LLM-assisted.

---

## 4. Image Reference Checking

### What exists today

`validate_images()` in `build.py` already handles this well:

- Checks frontmatter `image:` fields against disk
- Checks markdown `![](path)` syntax in body
- Handles `_web.jpg` → `.png` fallback with helpful "run make web-images" message
- Reports warnings (not errors) so build continues

This was added in PR #22.

### What could be improved

| Enhancement                       | Value                                    |
|-----------------------------------|------------------------------------------|
| Make missing images a build error | Fail fast instead of warning              |
| Validate `image_alt` is not empty | Accessibility contract                    |
| Check image dimensions/format     | Ensure web-optimized images are used      |

### Implementation approach

The existing code is solid. To make it a hard error:

```python
# In build(), after validate_images():
if any("✗" in w for w in image_warnings):
    print("\nBuild FAILED: missing image references.")
    sys.exit(1)
```

The `image_alt` check belongs in the frontmatter schema (section 1
above) — if `image` is present, require `image_alt`.

### Complexity

Already done (Low for enhancements). The core validation exists.
Upgrading warnings to errors is a 3-line change.

### LLM calls eliminated

PR #22 already automated this. The enhancement to make it a hard error
would prevent **0-1 additional LLM calls** — the savings here are
already realized.

---

## 5. Slide Ordering Contracts

### What exists today

`build.py` uses `sorted(CONTENT_DIR.glob("*.md"))` which gives
lexicographic order. Files are named `NN-slug.md` with some
fractional numbers (`04.1`, `11.5`, `14.5`).

Current slide numbering (from the filesystem):

```
01, 02, 03, 04, 04.1, 05, 06, [07 missing], 08, 09, 10, 11, 11.5,
12, 13, 14, 14.5, 15, 16
```

There is no `07-*.md` file. The `footer` values (slide numbers shown
to audience) are independently assigned and don't match filenames:

```
01: no footer    05: "4"     09: "8"      13: "12"
02: "1"          06: "5"     10: "9"      14: "13"
03: "2"          08: "7"     11: "10"     14.5: "15"
04: "3"          04.1: "6"   11.5: "12"   15: "14"
16: no footer                12: "11"
```

### What to validate

| Check                                | Rule                                    |
|--------------------------------------|-----------------------------------------|
| No duplicate filenames               | Automatic (filesystem enforces)          |
| No duplicate footer values           | Warn/error on collision                  |
| Footer values are sequential         | Optional — some slides intentionally skip|
| No large gaps in file numbering      | Warn if gap > 2                          |
| Footer present on non-title slides   | Schema handles this (section 1)          |

### Implementation approach

Add to `build.py`:

```python
def validate_ordering(md_files: list[Path]) -> list[str]:
    """Check slide ordering and footer numbering."""
    warnings = []
    footers: dict[str, str] = {}  # footer_value -> filename

    for md_file in md_files:
        text = md_file.read_text()
        meta, _ = parse_frontmatter(text)
        footer = meta.get("footer", "")

        if footer:
            if footer in footers:
                warnings.append(
                    f"  ✗  Duplicate footer '{footer}': "
                    f"{footers[footer]} and {md_file.name}"
                )
            footers[footer] = md_file.name

    # Check for gaps in integer footers
    int_footers = sorted(int(f) for f in footers if f.isdigit())
    for i in range(len(int_footers) - 1):
        gap = int_footers[i + 1] - int_footers[i]
        if gap > 2:
            warnings.append(
                f"  ⚠  Footer gap: {int_footers[i]} -> {int_footers[i+1]} "
                f"(gap of {gap})"
            )

    return warnings
```

### Complexity

Low. ~25 lines. The duplicate footer check is the most valuable part.

### LLM calls eliminated

Currently slide ordering is verified by eyeballing `make list` output
or asking an LLM to review. Estimated **0-1 LLM calls per PR** — this
is a low-frequency concern but catches nasty bugs (duplicate slide
numbers in the rendered deck).

---

## 6. Quote Format Validation

### What exists today

`build.py` parses blockquotes (`>` lines) and attribution lines
(`— Author`) separately. There's no validation that quotes have
proper attribution or that attribution format is consistent.

### Observed quote patterns in the deck

```markdown
# Pattern 1: Quote + attribution (most common)
> "Quoted text here."
> — Author Name

# Pattern 2: Multi-paragraph quote
> "First paragraph."
>
> "Second paragraph."
> — Author Name

# Pattern 3: Quote without attribution (slide 09)
> "Roll for initiative!"

# Pattern 4: Multiple quotes in one slide (slide 13)
> "Quote one." — DevSecOps proverb
>
> "Quote two." — Gary Gygax
```

### What to validate

| Check                              | Rule                                     |
|------------------------------------|------------------------------------------|
| Quotes use curly/straight quotes   | Consistent style (currently straight `"`) |
| Attribution uses em-dash `—`       | Not hyphen `-` or en-dash `–`            |
| Attribution line follows quote     | Warn if `—` line is orphaned             |
| Quote text is non-empty            | No bare `>` followed by attribution       |

### Implementation approach

```python
def validate_quotes(body: str, filename: str) -> list[str]:
    """Check quote formatting conventions."""
    warnings = []
    lines = body.split("\n")

    for i, line in enumerate(lines):
        stripped = line.strip()

        # Attribution should use em-dash, not hyphen or en-dash
        if re.match(r"^>\s*[-–]\s+", stripped):
            warnings.append(
                f"{filename}:{i+1}: attribution uses wrong dash "
                f"(use '—' em-dash, not '-' or '–')"
            )

        # Orphaned attribution (— without preceding >)
        if re.match(r"^—\s", stripped):
            # Check if previous non-empty line is a blockquote
            prev = ""
            for j in range(i - 1, -1, -1):
                if lines[j].strip():
                    prev = lines[j].strip()
                    break
            if not prev.startswith(">"):
                warnings.append(
                    f"{filename}:{i+1}: attribution line not preceded "
                    f"by blockquote"
                )

    return warnings
```

### Complexity

Low. ~25 lines. Simple regex checks against known patterns.

### LLM calls eliminated

Quote formatting is a common PR review comment. Estimated **0-1 LLM
calls per PR** — small but the validation is nearly free to implement.

---

## Summary: Implementation Priority

| Contract                  | Complexity | LLM calls saved/PR | Priority |
|---------------------------|------------|---------------------|----------|
| 1. Frontmatter schema    | Low        | 1-2                 | **High** |
| 2. Slide body linting    | Low-Med    | 1-3                 | **High** |
| 3. Speaker notes check   | Low        | 1                   | Medium   |
| 4. Image reference check | Done       | (already saved)     | Done     |
| 5. Slide ordering        | Low        | 0-1                 | Medium   |
| 6. Quote format          | Low        | 0-1                 | Low      |

### Aggregate impact

With contracts 1-3 and 5-6 implemented, an estimated **3-8 LLM review
calls per PR** are eliminated. Over a typical development cycle with
~20 content PRs, that's **60-160 LLM calls** replaced by deterministic
checks that run in <1 second.

### Recommended implementation order

1. **Frontmatter schema** — highest value, prevents the most common
   class of silent build failures
2. **Speaker notes validation** — trivial to add, prevents the exact
   bug fixed in PR #20
3. **Slide body linting** — catches style drift, especially bullet
   count and heading conventions
4. **Slide ordering** — duplicate footer detection is a subtle but
   important catch
5. **Quote formatting** — low priority but nearly free
6. **Image references** — already implemented, just upgrade warnings
   to errors for missing files

### Integration strategy

All validators follow the same pattern as `validate_images()`:

1. Accept `list[Path]` of slide files
2. Return `list[str]` of warning/error messages
3. Called in `build()` after slides are parsed
4. Print results with clear prefixes (`✗` = error, `⚠` = warning)
5. Exit non-zero on errors (not warnings)

This keeps all validation in `build.py` — no external tools, no extra
dependencies (except optionally `jsonschema`), and instant feedback on
every build. Add a `make validate` target that runs build with a
`--strict` flag to fail on warnings too.

### What this does NOT cover

- **Content quality** — "is this slide's message clear?" still needs
  human or LLM judgment
- **Visual rendering** — "does this look right in the browser?" needs
  screenshot comparison or manual review
- **Narrative flow** — "do the slides tell a coherent story?" is
  inherently subjective

These are the right boundaries: contracts handle structure and format,
humans/LLMs handle meaning and aesthetics.
