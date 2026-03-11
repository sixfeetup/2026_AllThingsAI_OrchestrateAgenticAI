# Watch Loop: Continuous Integration for Presentations

This directory contains vendored copies of the Claude Code skills that powered the watch loop -- the continuous integration system that was the heartbeat of this presentation's development workflow.

## What is the watch loop?

The watch loop is a 90-second recurring cycle that monitors source files, processes inline directives, regenerates slides from the presentation plan, and rebuilds the HTML deck. One command starts it:

```
/loop 90s /deck-watch
```

From that point on, the author edits `plan.md` (or any watched file) and the deck rebuilds itself. No manual build step. No context switching. Just write and watch the results appear.

## The skills

### `deck-watch.md` (vendored)

The core watcher skill, invoked as `/deck-watch`. On each 90-second tick it runs a five-step algorithm:

1. **Check for changes** -- runs `check-changes.sh`, which computes an MD5 hash of all watched files and compares it to a stored `.watch-state` file. If nothing changed, it exits immediately with a one-line message and does no further work.
2. **Read sources** -- loads `plan.md`, `README.md`, `quotes.md`, and all current slide files from `presentation/content/*.md`.
3. **Process `@@` directives** -- scans every watched file for lines containing `@@`, interprets them as author instructions (e.g., `@@ add a slide about testing`), executes them by modifying slide files, then removes the `@@` line from the source.
4. **Regenerate slides** -- compares the plan structure against existing slides, creating new ones, updating changed ones, removing deleted ones, and renumbering as needed.
5. **Build** -- runs `cd presentation && make build` to produce `presentation/output/deck.html`.

### `render-deck.md` (vendored)

The manual build-and-open skill, invoked as `/render-deck` or `/deck`. Wraps `cd presentation && make open` (or `uv run build.py --open`). Used constantly during development for one-off rebuilds, previewing changes, and iterating on individual slides. Documents the slide markdown format, frontmatter fields, and body syntax.

### `loop.md` (not vendored -- bundled with Claude Code)

The `/loop` skill is a built-in Claude Code capability that schedules recurring prompts via `CronCreate`. Usage: `/loop 90s /deck-watch` sets up a cron job that invokes the `/deck-watch` skill every 90 seconds. This is the scheduler that makes the watch loop possible. Since it ships with Claude Code, no source is vendored here.

## Historical importance

The watch loop was THE workflow innovation of this project. It transformed presentation development from a tedious manual cycle (edit, remember to rebuild, check browser, repeat) into a continuous flow where the author simply writes and the system keeps up.

### Key moments in the watch loop's evolution

**Hash-based change detection.** Early on, the system needed a way to avoid doing expensive work (reading all files, regenerating slides, running the build) on every 90-second tick when nothing had changed. The solution was `check-changes.sh`: a shell script that computes an MD5 hash of all watched files and compares it to a stored `.watch-state` file. If the hash matches, the watcher exits in under a second. This made the 90-second interval practical -- most ticks are no-ops.

**The `@@` directive system.** This was the most distinctive innovation. The author could leave inline instructions anywhere in any watched file:

```markdown
## Testing Strategy

@@ add a slide about property-based testing with the hypothesis library

- Unit tests for core logic
- Integration tests for API layer
```

On the next tick, the watcher would find the `@@` line, interpret it as an instruction, create or modify the appropriate slide, and remove the directive from the source file. The `@@` syntax was chosen because it is visually distinct, unlikely to appear in normal markdown content, and easy to scan for. This turned every source file into a two-way communication channel between the author and the AI.

**Integration with `/loop` for cron-based scheduling.** The `/loop` skill provided the timer. Running `/loop 90s /deck-watch` registered a cron job that fires the watcher every 90 seconds. The 90-second interval was a deliberate choice -- fast enough that changes feel responsive, slow enough to avoid burning tokens on rapid-fire rebuilds while the author is mid-thought.

**The full development cycle.** In steady state, the workflow looked like this:

1. Author edits `plan.md` (adds a section, rewords a bullet, drops in an `@@` directive)
2. Within 90 seconds, `deck-watch` detects the hash change
3. It reads all sources, finds and processes any `@@` directives
4. It regenerates slide markdown files to match the updated plan
5. It runs `make build` to produce the HTML deck
6. The deck updates in the browser (or the author refreshes to see it)

This cycle ran continuously throughout development. The author could focus entirely on content and structure while the build system handled everything else.

### Key design decisions

- **Hash-based change detection, not filesystem events.** Using MD5 hashes instead of `fswatch`/`inotify` made the system portable and simple. No daemon to manage, no platform-specific code, no missed events. The tradeoff (up to 90 seconds of latency) was acceptable for presentation work.

- **`@@` as a directive syntax.** The double-at-sign is visually distinctive and extremely unlikely to appear in normal markdown, code blocks, or quoted text. It reads naturally as an annotation or aside. The convention of removing directives after processing keeps source files clean.

- **Preservation of manual edits.** The regeneration step explicitly preserves slide frontmatter (type, image, layout) and structural slides (title, closing, dividers) unless the plan directly contradicts them. This meant the author could hand-edit a slide and trust that the watcher would not overwrite the changes on the next tick.

- **Five-step algorithm with early exit.** The most common case (no changes) is also the cheapest. The watcher checks the hash first and skips everything else if nothing changed. This kept token usage low during idle periods.

## Usage

To start the watch loop:

```
/loop 90s /deck-watch
```

To manually rebuild and open the deck:

```
/render-deck
```

or

```
/deck
```

To leave an instruction for the watcher:

```
@@ add a slide about compliance automation
```

Place the `@@` line anywhere in `plan.md`, `README.md`, `quotes.md`, or any slide file. The watcher will process it on its next tick and remove the line afterward.
