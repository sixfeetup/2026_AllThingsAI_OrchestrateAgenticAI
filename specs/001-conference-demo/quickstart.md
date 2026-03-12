# Quickstart: Conference Demo Workspace

## Goal

Get from a clean checkout to a rehearsal-ready demo workspace with the canonical plan, operator README, and repo-local Codex launchers in place.

## 1. Verify the current planning artifacts

1. Read [demo/plan.md](/Users/whit/work/2026-allthings-ai-presentation/.claude/worktrees/demo-init/demo/plan.md) for the canonical demo description.
2. Read [demo/README.md](/Users/whit/work/2026-allthings-ai-presentation/.claude/worktrees/demo-init/demo/README.md) for the operator-facing runbook.
3. Read [demo/explainers-plan.md](/Users/whit/work/2026-allthings-ai-presentation/.claude/worktrees/demo-init/demo/explainers-plan.md) for the required explainer set.

## 2. Prepare local Codex ergonomics

1. Install the vendored skills if needed:

   ```bash
   make install-vendored-skills
   make install-speckit-aliases
   ```

2. Launch Codex for this repo with Ralph MCP enabled:

   ```bash
   make codex-demo
   ```

## 3. Build out the demo workspace in implementation order

1. Add `demo/Makefile` with stable entry points for setup, seed, audit, and fallback opening.
2. Add Postgres scaffolding under `demo/postgres/`.
3. Add the vulnerable `Dockerfile` specimen under `demo/specimens/`.
4. Add prepared artifact locations under `demo/artifacts/`.
5. Build the explainers defined in `demo/explainers-plan.md`, starting with Segment 2 assets.

## 4. Rehearsal expectations

1. Each segment must have one visible live proof step.
2. Each segment must cut over to predetermined state for its consequential follow-up step.
3. Each segment must have at least one prepared fallback artifact that can be opened in under 30 seconds.
4. Update `demo/README.md` when operator friction is discovered during rehearsal.

## 5. Exit criteria for this feature

- `demo/plan.md` remains the canonical source of truth.
- `demo/README.md` remains stress-friendly.
- The demo uses Postgres as its data path.
- The vulnerable buildpack is represented by a shareable `Dockerfile`.
- The required explainers exist in plan form and are ready to be implemented in priority order.
