# Demo Scripts

Presenter scripts for the "Orchestrate Agentic AI" conference talk.

## Files

| File | Purpose |
|------|---------|
| [predemo.md](predemo.md) | Pre-show setup checklist — run the night before and 15 min before your slot |
| [terminal.md](terminal.md) | Demo script for running entirely in Claude Code CLI |
| [hybrid.md](hybrid.md) | Demo script using Claude Desktop (Step 0 + cowork) and Claude Code (Steps 1-9) |
| [hybrid-setup.md](hybrid-setup.md) | Step-by-step setup for Claude Desktop + MCP + cowork windows |
| [setup-terminal.sh](setup-terminal.sh) | Install deps for terminal demo (brew, uv, python, claude CLI, venv, model) |
| [setup-desktop.sh](setup-desktop.sh) | Add Claude Desktop + MCP on top of terminal setup |

## Which script to use

**[terminal.md](terminal.md)** — safest option. Everything runs in Claude Code with deterministic
slash commands. Most rehearsed, most predictable.

**[hybrid.md](hybrid.md)** — more impressive. Uses Claude Desktop for the "OH NO" moment
and the cowork pipeline segment. Higher impact but requires more rehearsal
and a working Claude Desktop + MCP server setup.

Both scripts assume [predemo.md](predemo.md) has been completed first.

## Related docs

- [Presentation outline](../../presentation/outline.md) — slide source of truth (slides 0-17)
- [Demo spec](../spec.md) — what the demo is designed to do
- [Demo plan](../plan.md) — technical architecture
- [Playbook](../assets/playbook.md) — attendee take-home
- [Cowork concept note](../../notes/cowork-demo-concept.md) — analysis of all-Desktop vs hybrid approach
- [Bitrot research](../assets/prebaked/bitrot-research.md) — context degradation data for Step 6.5
- [Naive review](../assets/prebaked/naive-review.md) — prebaked bad output for Step 0 / 5.5

## Timing

Both scripts target **~18 minutes** of demo time within a ~45 minute talk slot.
The remaining time is slides (intro, concepts, wrap-up).
