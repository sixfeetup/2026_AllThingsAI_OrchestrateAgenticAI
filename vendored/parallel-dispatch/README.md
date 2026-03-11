# Parallel Dispatch Skills

Parallel AI agent orchestration for dividing work across independent workers. These are the two complementary skill definitions that powered the construction of this presentation: `/c^2` (Claude-squared) and `/mc` (MultiClaude).

## Files

- **`c2.md`** -- Claude-squared (`/c^2`). Agent-tool-native parallel dispatch. Dispatches workers in isolated git worktrees using Claude Code's built-in Agent tool. Commands: `work`, `swarm`, `status`, `gather`, `msg`, `repo`. Lightweight, no daemon required.

- **`mc.md`** -- MultiClaude (`/mc`). Daemon-based parallel dispatch. Wraps a persistent `multiclaude` binary that manages agent lifecycles, worktrees, messaging, and PR workflows. Commands: `work`, `swarm`, `status`, `review`, `msg`, `repo`, `start/stop/attach/logs/cleanup`. Heavier weight, suited for long-running research workers.

## Historical Importance

These skills were used at every major junction in building this presentation. The project literally demonstrates its own thesis: using AI agents to build a talk about AI agent orchestration.

### PRs #1-6: First swarm

`/c^2 swarm` dispatched 6 workers simultaneously to polish slides in a show-don't-tell pass, add visual explainer links, and generate images. All 6 PRs were reviewed and merged in one batch. This was the first proof that parallel agent dispatch could meaningfully accelerate a creative workflow.

### PRs #8-10: Second swarm

`/c^2 swarm` created workers for gap analysis deliverables: an eventual consistency slide, a playbook slide with explainer content, and a demo assets directory. Each worker independently identified what was missing, created the content, and opened a PR.

### PR #12: Help modal

A `/c^2 swarm` worker added the "?" key accessibility modal to the slide deck, making keyboard shortcuts discoverable for conference attendees.

### Research workers

`/mc` launched long-running research agents:
- **`happy-elephant`** -- Pipeline audit worker that analyzed the existing build pipeline for determinism gaps.
- **`zealous-rabbit`** -- Framework survey worker that compared slide framework options and transition approaches.

These tasks benefited from mc's daemon lifecycle management: the daemon kept the agents alive across terminal disconnects, provided log streaming, and handled cleanup of worktrees after completion.

## c^2 vs mc

| Dimension | c^2 | mc |
|-----------|-----|-----|
| Architecture | Agent tool native (no daemon) | Persistent daemon binary |
| Startup cost | None -- uses Claude Code's built-in subagent | Requires `multiclaude start` |
| Best for | Quick swarms of 2-10 workers | Long-running research, complex lifecycle management |
| Worker isolation | Git worktree per worker (automatic) | Git worktree per worker (daemon-managed) |
| Messaging | Filesystem-based (`~/.claude/mc-messages/`) | Daemon-managed message queue |
| Lifecycle | Tied to coordinator session | Survives terminal disconnects |
| Observability | `status`/`gather` commands | `attach`, `logs`, `diagnostics` commands |

Both systems share the same fundamental design: each worker operates in an isolated git worktree, produces a PR as its deliverable, and communicates via filesystem-based messaging. The coordinator never touches the same files as the workers.

## Key Design Decisions

- **Worktree isolation**: Every worker gets its own complete copy of the repo via `git worktree`. Workers never conflict on file access. No locks, no merge conflicts during execution.

- **Filesystem-based messaging**: Workers and coordinators communicate through files in `~/.claude/mc-messages/`. No network required, no server to run. Messages are timestamped markdown files that humans can read directly.

- **PR-as-deliverable**: Every worker's output is a GitHub pull request. This makes review natural -- the coordinator (or a human) reviews each PR independently. Failed workers produce no PR; successful workers produce a reviewable, mergeable unit of work.

- **No cross-dependencies between swarm units**: The coordinator decomposes work so that no two workers touch the same files. This is enforced at planning time, not runtime. If two tasks need the same file, they are merged into one work unit or sequenced.

- **Self-contained worker prompts**: Each worker receives all the context it needs at launch time. Workers cannot ask the coordinator questions during execution (messaging is for course corrections, not Q&A). This means the coordinator must do thorough research before dispatching.
