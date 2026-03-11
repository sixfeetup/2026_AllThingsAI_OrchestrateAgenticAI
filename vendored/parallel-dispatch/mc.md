---
name: mc
description: "MultiClaude — dispatch and manage parallel Claude agents via the multiclaude daemon. Use /mc to start workers, check status, send messages, review PRs, manage repos, and view logs. Wraps the `multiclaude` CLI binary."
argument-hint: <work|status|review|msg|repo|start|stop|attach|logs|cleanup> [args]
---

# MultiClaude (mc)

Dispatch and manage parallel Claude agents via the **`multiclaude` daemon** — a persistent orchestrator that manages agent lifecycles, worktrees, messaging, and PR workflows.

> **Note**: This skill wraps the `multiclaude` binary at `~/.local/bin/multiclaude`. For the lighter Agent-tool-native approach (no daemon), use `/c^2` instead.

**Binary**: `~/.local/bin/multiclaude`

## Command Mapping

Map `/mc` subcommands to `multiclaude` CLI calls. Run them via Bash.

### `mc work "<task>"` (aliases: `w`, bare string)

Create a worker agent to handle a task.

```bash
multiclaude worker "<task>" [--repo <repo>] [--branch <branch>] [--push-to <branch>]
```

- If user specifies `@repo`, pass it as `--repo <name>`
- The daemon handles worktree creation, branch setup, and agent lifecycle
- Report the worker name and status after creation

**Examples:**
- `/mc work "add input validation to the signup form"`
- `/mc work @prime "fix the auth bug"` → `multiclaude worker "fix the auth bug" --repo prime`
- `/mc "fix flaky test"` (bare string = work)

### `mc swarm "<goal>"` (aliases: `fan`, `s`)

Decompose a high-level goal into independent work units and launch them concurrently.

There is no native `multiclaude swarm` command — this is skill-level orchestration that uses `multiclaude worker` under the hood.

**Workflow:**

1. **Decompose** the goal into 2–10 independent work units. Each unit must be fully self-contained (no cross-worker dependencies during execution). Workers must NOT touch the same files — if overlap is detected, merge the units or sequence them.
2. **Save the plan** to `.claude/swarm-plans/<YYYY-MM-DD>-<slug>.md` in the current repo before launching anything. Present the plan to the user and wait for confirmation (or let them edit).
3. **Launch all independent workers concurrently** using `multiclaude worker "<task>"` for each unit. If any units have dependencies, hold dependent units until their prerequisites complete.
4. **Track progress** using `multiclaude status` and `multiclaude message list`. Poll periodically and report as workers complete.
5. **Report results** with a final summary table: worker name, status, PR link.

**Plan file format** (saved to `.claude/swarm-plans/<YYYY-MM-DD>-<slug>.md`):

```markdown
# Swarm Plan: <slug>
Date: <YYYY-MM-DD HH:MM>
Goal: <user's goal>

## Work Units

| # | Worker | Scope | Description |
|---|--------|-------|-------------|
| 1 | name | files/dirs | what it does |
| ...

## Dependencies
- Units 1, 2, 3 are fully independent (no file overlap)
- Unit 4 depends on Unit 1 completing first (shared file X)

## Expected Outcomes
- N PRs with passing tests
- <specific deliverables>
```

**Behavior notes:**
- Plan is saved BEFORE workers launch so the user can review or edit it
- Each worker prompt must be fully self-contained — include all context the worker needs (file paths, requirements, acceptance criteria)
- No file overlap between workers. If two units need the same file, either merge them into one unit or sequence them (launch the second after the first completes)
- Worker names in the plan should be descriptive slugs (e.g., `add-validation`, `fix-auth-tests`)
- Pass `--repo <name>` if the user specifies a target repo
- Final report includes PR links harvested from `multiclaude status` output

**Examples:**
- `/mc swarm "add comprehensive input validation to all API endpoints"` → decomposes by endpoint, launches parallel workers
- `/mc fan "refactor the auth module: split into oauth, session, and token submodules"` → 3 workers, one per submodule
- `/mc s "add tests for the billing, notifications, and reporting modules"` → 3 independent test-writing workers

### `mc status` (aliases: `st`, `ls`)

Show system status overview.

```bash
multiclaude status
```

Also useful:
- `multiclaude worker list [--repo <repo>]` — list active workers
- `multiclaude message list` — show pending inter-agent messages

Render the output in a clean table for the user.

### `mc review <pr-url>`

Spawn a review agent for a pull request.

```bash
multiclaude review <pr-url>
```

The daemon creates a dedicated review agent that checks out the PR, runs analysis, and posts review comments.

### `mc msg "<recipient>" "<message>"` (aliases: `m`, `tell`, `send`)

Send a message to another agent.

```bash
multiclaude message send <recipient> "<message>"
```

Also useful:
- `multiclaude message list` — see pending messages
- `multiclaude message read <message-id>` — read a specific message
- `multiclaude message ack <message-id>` — acknowledge a message

### `mc repo` (aliases: `repos`, `r`)

Manage tracked repositories.

| Subcommand | CLI |
|---|---|
| `mc repo list` | `multiclaude repo list` |
| `mc repo init <url> [name]` | `multiclaude repo init <url> [name]` |
| `mc repo use <name>` | `multiclaude repo use <name>` |
| `mc repo rm <name>` | `multiclaude repo rm <name>` |
| `mc repo current` | `multiclaude repo current` |
| `mc repo history` | `multiclaude repo history [--repo <repo>] [-n <count>]` |

### `mc start`

Start the multiclaude daemon.

```bash
multiclaude start
```

Also: `multiclaude daemon status` to check if it's running.

### `mc stop`

Stop the daemon and all agents.

```bash
multiclaude stop-all [--clean] [--yes]
```

Pass `--clean` to also remove worktrees. Always confirm with the user before passing `--yes`.

### `mc attach <agent-name>`

Attach to an agent's tmux window to watch it work.

```bash
multiclaude agent attach <agent-name> [--read-only]
```

Default to `--read-only` unless the user asks to interact.

### `mc logs [agent-name]`

View agent output logs.

```bash
multiclaude logs [<agent-name>] [-f|--follow]
```

Also:
- `multiclaude logs list [--repo <repo>]` — list log files
- `multiclaude logs search <pattern>` — search across logs
- `multiclaude logs clean --older-than <duration>` — clean old logs

### `mc agents`

List or manage agent definitions.

```bash
multiclaude agents list [--repo <repo>]
multiclaude agents spawn --name <name> --class <class> --prompt-file <file> [--repo <repo>]
multiclaude agents reset [--repo <repo>]
```

### `mc workspace` (aliases: `ws`)

Manage workspaces (named worktree environments).

```bash
multiclaude workspace list
multiclaude workspace add <name> [--branch <branch>]
multiclaude workspace connect <name>
multiclaude workspace rm <name>
```

### `mc config`

View or modify repository configuration.

```bash
multiclaude config [repo] [--mq-enabled=true|false] [--mq-track=all|author|assigned] [--ps-enabled=true|false]
```

### `mc cleanup`

Clean up orphaned resources (stale worktrees, dead agents).

```bash
multiclaude cleanup [--dry-run] [--verbose] [--merged]
```

Default to `--dry-run` first, show what would be cleaned, then confirm with the user before running for real.

### `mc refresh`

Sync agent worktrees with the main branch.

```bash
multiclaude refresh [--all]
```

### `mc repair`

Repair state after a crash.

```bash
multiclaude repair [--verbose]
```

### `mc diagnostics`

Show system diagnostics (useful for debugging).

```bash
multiclaude diagnostics [--json]
```

### `mc bug`

Generate a diagnostic bug report.

```bash
multiclaude bug [description]
```

## Behavior Notes

- **Bare string = work.** If the user writes `/mc "do something"` without a subcommand, treat as `work`.
- **Keep it terse.** This is a dispatch tool. Run the command, show the output, done.
- **Parse output for the user.** The CLI output can be verbose — extract the key info (worker name, status, PR links) and present it cleanly.
- **Daemon must be running.** If a command fails because the daemon isn't running, offer to start it with `multiclaude start`.
- **Confirm destructive ops.** Always confirm before `stop-all --yes`, `cleanup` (without `--dry-run`), or `repo rm`.
- **JSON mode available.** Many commands support `--json` for machine-readable output. Use it when you need to parse results programmatically.
- **Use `multiclaude --json`** to get the full command tree if you're unsure about a subcommand's syntax.
