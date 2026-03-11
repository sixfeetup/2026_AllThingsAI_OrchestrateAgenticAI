# End Session

Write notes for future-you and future-me before closing out.

**Trigger:** When the user types `/end-session`, says "end session", or asks to wrap up.

## Workflow

### 1. Review the session

Scan the conversation for:
- **Corrections**: Anything the user corrected you on (wrong assumptions, bad patterns, preferences you got wrong). These are the highest priority — fix incorrect memories immediately.
- **New conventions**: Coding patterns, tool preferences, workflow habits confirmed across multiple interactions or explicitly stated by the user.
- **Architectural decisions**: Important choices made about project structure, dependencies, or design that future sessions need to know.
- **Solved problems**: Debugging insights, workarounds, or fixes that took significant effort to discover. Save these so you don't repeat the investigation.
- **User preferences**: Communication style, tool choices, or workflow preferences the user demonstrated or stated.

### 2. Update auto-memory

Read the project's `MEMORY.md` (in the auto-memory directory shown in your system prompt). Then:

- **Update or add** entries based on what you found in step 1. Organize by topic, not chronologically.
- **Remove or correct** any entries that turned out to be wrong this session.
- **Keep it under 200 lines** — lines after 200 are truncated. If approaching the limit, consolidate or move detailed notes to topic-specific files (e.g., `debugging.md`, `patterns.md`) and link from MEMORY.md.
- **Don't duplicate** existing CLAUDE.md instructions or things already in memory.
- **Skip session-specific state** — no "currently working on X" or "PR #7 is open." Only stable, reusable knowledge.

### 3. Update project docs (if warranted)

If the session produced changes that affect how the project works (new build steps, changed conventions, new skills), check if any project docs need updating:
- `CLAUDE.md` — project conventions Claude should follow
- `README.md` — only if the user has one and it's now stale
- Skill files — if you discovered a skill needs tweaking

Only update docs that are genuinely stale. Don't touch docs for trivial changes.

### 4. Summarize for the user

Tell the user:
- What memories were added, updated, or removed (brief list)
- Any docs that were updated
- One sentence on what future-Claude will know that current-Claude didn't at the start

Keep this short — 5-10 lines max. The user is wrapping up, not starting a new task.

### 5. Optionally chain to /finished

If the project uses the `/finished` skill (check if `~/.claude/skills/finished/skill.md` exists), ask the user if they also want to finalize the transcript. Don't auto-run it — just mention it's available.

## Rules

- **Never invent memories.** Only save things that actually happened or were explicitly stated this session.
- **Corrections override everything.** If the user corrected you, the old memory is wrong. Fix it before writing new ones.
- **Prefer updating over adding.** Check existing entries first. A single well-maintained entry beats three overlapping ones.
- **Be honest about gaps.** If nothing notable happened this session, say so and skip the memory update. Don't pad with obvious or generic observations.
