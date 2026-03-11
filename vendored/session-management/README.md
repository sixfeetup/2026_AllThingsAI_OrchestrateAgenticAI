# Session Management Skills

Human-AI collaboration workflow tools: notifications, backgrounding, memory persistence, and session lifecycle management.

These skills were the connective tissue of the presentation project's development workflow. They handled the practical realities of working with an AI agent over many sessions — staying aware of task completion, keeping the UI responsive, remembering what happened, and closing out cleanly.

## Skills

| Skill | File | Trigger |
|-------|------|---------|
| `/say` | `say.md` | Automatic on milestones, blockers, questions |
| `/bg` (alias `/&`) | `bg.md` | User prefix on nearly every command |
| `/end-session` | `end-session.md` | User says "end session" (hook-triggered) |
| `/finished` | `finished.md` | User says `/finished` or chains from `/end-session` |

## Historical Importance

### `/say` — Audio Notifications

The `/say` skill used macOS text-to-speech to notify the user at key moments: "Done. Deck deployed.", "Hey, I have a question.", "Swarm complete. 5 of 5 workers landed PRs." The audio cue made asynchronous collaboration practical — the user could walk away from the terminal and come back when they heard the notification.

The memory directive "Have fun with the voices" led to using different macOS TTS voices for personality. Zarvox (a robotic voice) was used for swarm completion announcements. Different voices signaled different event types, turning a simple notification mechanism into something with character.

### `/bg` — Background Job Management

The most-used prefix in the entire project. Nearly every user command started with `/bg` (or `/&`) to dispatch work to the background and keep the conversational UI responsive. It became the default interaction pattern: fire a command, do something else, come back when notified (via `/say`).

This skill is an alias for the built-in `/job` skill, adding terse subcommands: `run`, `ls`, `status`, `log`, `stop`, `wait`. The combination of `/bg` for dispatch and `/say` for notification created a lightweight async workflow that shaped how the entire project was built.

### `/end-session` — Session Wrap-Up and Memory Persistence

Born from this project. The user described the concept as a user story — "notes for future-you and future-me" — and then asked it to be turned into a skill. This is meta-tooling: a skill created by the project to improve the project's own workflow.

The skill scans the conversation for corrections, new conventions, architectural decisions, solved problems, and user preferences, then writes them to auto-memory (`MEMORY.md`). Corrections are highest priority — if the user corrected the agent during a session, the old memory is wrong and gets fixed before anything new is written.

It includes a `UserPromptSubmit` hook configured in `~/.claude/settings.json` that detects the phrase "end session" in natural language and auto-invokes the skill. This is significant: instead of requiring a slash command, the user just types conversationally and the tooling responds. The hook-based trigger demonstrates natural language invocation of structured workflows.

### `/finished` — Transcript Finalization

Handles the mechanical cleanup of session transcripts in `notes/ai-notes/`. Locates the current session's transcript file, adds a summary section at the top, and stamps it with a completion timestamp. Optionally chained from `/end-session` — after memory is persisted, the user can also close out the written record.

## Key Design Decisions

- **Audio notifications for async awareness.** The `/say` skill turned a text-only interface into one with ambient awareness. The user did not need to watch the terminal — they listened for it.

- **Background-first interaction pattern.** By defaulting to `/bg` for nearly every command, the project established that the human should never be blocked waiting for the agent. The agent works; the human is notified when it matters.

- **Persistent memory across sessions via auto-memory.** The `/end-session` skill ensures that knowledge accumulates across sessions rather than being lost when a conversation ends. Each session's corrections, conventions, and decisions carry forward.

- **Hook-based trigger for natural language invocation.** The `UserPromptSubmit` hook on "end session" demonstrates that skills do not need to be invoked with slash commands. Natural language triggers make the tooling feel like collaboration rather than command-line usage.

- **Separation of memory and transcript.** `/end-session` handles what the agent should remember (structured knowledge in MEMORY.md). `/finished` handles what the human should be able to read later (narrative transcript with summary). Two different audiences, two different skills.
