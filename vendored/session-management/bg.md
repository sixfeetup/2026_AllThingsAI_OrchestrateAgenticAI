---
name: "&"
description: "Alias for /job — run and manage background shell jobs. Use /& <command> to run in background, /& ls to list, /& stop <id> to kill."
argument-hint: <command|ls|status|stop|log|wait> [args]
---

# & (Background Job Alias)

This is an alias for the `job` skill. Route all input directly to the job skill's logic.

Parse the user's argument using the same subcommand rules as `/job`:

- `/& <command>` — same as `/job run <command>` (launch in background)
- `/& ls` or `/& ps` — same as `/job list`
- `/& status <id>` or `/& s <id>` — same as `/job status <id>`
- `/& log <id>` or `/& l <id>` — same as `/job log <id>`
- `/& stop <id>` or `/& kill <id>` — same as `/job stop <id>`
- `/& wait <id>` or `/& w <id>` — same as `/job wait <id>`

Behavior is identical to `/job` in every way. See the `job` skill for full documentation.

Keep responses terse — this is a utility, not a conversation.
