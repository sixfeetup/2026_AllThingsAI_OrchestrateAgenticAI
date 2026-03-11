# deck-watcher

Watch plan.md and related files, regenerate slide content, and rebuild the presentation deck.

## Triggers

- `/deck-watch`

## Intended use

```
/loop 90s /deck-watch
```

This runs the watcher every 90 seconds. On each tick it checks for changes, processes any `@@` directives, regenerates slide markdown, and rebuilds the deck.

## Watched files

All paths relative to repo root:

| File | Role |
|------|------|
| `plan.md` | Primary source — presentation outline and structure |
| `README.md` | Context — abstract, event details, constraints |
| `quotes.md` | Reference — quotable material to draw from |
| `presentation/content/*.md` | Current slides — may have manual edits to preserve |

## Algorithm

### Step 1: Check for changes

Run `presentation/check-changes.sh`. If it exits non-zero (no changes), respond with a single line:

```
deck-watch: no changes detected
```

And stop. Do not read files or do any further work.

### Step 2: Read sources

If changes were detected, read these files:
- `plan.md`
- `README.md`
- `quotes.md`
- All files in `presentation/content/*.md` (current slide state)

### Step 3: Process `@@` directives

Scan **all watched files** for lines containing `@@`. The pattern is:

```
@@ {instruction text}
```

or variants like:

```
<@@ instruction text >
{@@ instruction text}
@@ instruction text
```

These are inline instructions from the author. They take **priority over everything else**.

**Processing rules:**

1. Collect all `@@` directives from all files, noting which file and line they came from
2. Interpret each directive as an instruction that may affect slide content. Examples:
   - `@@ add a slide about testing` → create a new content file
   - `@@ split this into two slides` → split the nearest slide
   - `@@ a slide with a picture for each` → generate a visual slide with images
   - `@@ remove the code example` → delete a content file
   - `@@ use the Kent Beck quote here` → pull from quotes.md
3. Execute the directives by modifying `presentation/content/*.md` files
4. After processing, **remove the `@@` line** from the source file (edit it out)
5. If a directive is ambiguous, make your best interpretation and leave a comment in the affected slide: `<!-- deck-watch: interpreted "@@..." as ... -->`

### Step 4: Regenerate slides from plan

Compare `plan.md` structure against current `presentation/content/*.md` files.

**Mapping rules:**
- Each major section (`##`) in plan.md maps to one or more slides
- Preserve slide `type` (title-slide, content-slide, dark-slide, divider-slide) from existing files when the section hasn't fundamentally changed
- Preserve `image` and `image_layout` frontmatter from existing files unless the plan contradicts them
- Pull relevant quotes from `quotes.md` when they fit a slide's theme
- Use `README.md` for context (time constraints, abstract, event details)
- Respect the slide markdown format documented in `presentation/README.md`

**What to change vs preserve:**
- If a plan section is **new** (no matching slide exists) → create a new content file with the right sequence number
- If a plan section is **removed** → delete the content file
- If a plan section is **modified** → update the content file, preserving images and type unless clearly wrong
- If a slide has **no corresponding plan section** but is structural (title, closing, divider) → preserve it
- When renumbering is needed, renumber all files to maintain clean NN-slug.md ordering

**Content style:**
- Concise slide text — bullets not paragraphs
- Quotes as blockquotes with attribution
- Feature grids for 3-4 related concepts
- Code blocks for demo/technical slides
- Keep the RPG/quest metaphor consistent with plan.md's tone

### Step 5: Build

After all content files are updated, run:

```sh
cd presentation && make build
```

Report the result:

```
deck-watch: rebuilt — N slides, M modified, K new, J removed
```

## Edge cases

- **First run** (no existing slides): Generate all slides fresh from plan.md
- **Empty plan.md**: Do nothing, report warning
- **Conflicting `@@` directives**: Process in file order (plan.md first, then README.md, then quotes.md)
- **Build failure**: Report the error, do not retry
- **Manual slide edits**: Preserve them unless plan.md explicitly contradicts

## File layout

```
presentation/
  check-changes.sh     # change detection (md5 hash comparison)
  .watch-state          # stored hash (gitignored)
  content/*.md          # slide sources (modified by this skill)
  output/deck.html      # built output
```

## Example session

```
> /loop 90s /deck-watch
deck-watch: no changes detected
deck-watch: no changes detected
deck-watch: changes detected in plan.md
deck-watch: processing 1 @@ directive from plan.md:77
  @@ "a slide with a picture for each" → adding team portrait slide
deck-watch: regenerating slides...
  updated: 03-the-party.md
  created: 04-team-portraits.md
  renumbered: 05-decision-frameworks.md (was 04)
deck-watch: rebuilt — 23 slides, 1 modified, 1 new, 0 removed
```
