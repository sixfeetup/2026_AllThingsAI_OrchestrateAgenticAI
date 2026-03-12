---
title: Demo Workspace
status: draft
audience: internal
purpose: conference-demo-staging
---

# Demo Runbook

This directory is the staging area for the runnable conference demo workspace.

## Canonical Entry Point

- The canonical demo description for this workspace lives at [`plan.md`](./plan.md).
- Use this README as the operator-facing index and runbook for fast use under stress.
- Older drafts can stay nearby, but `./plan.md` is the source of truth for the current demo plan.

## Local Helpers

- Install vendored repo skills into Codex: `make install-vendored-skills`
- Symlink vendored repo skills into Codex: `make link-vendored-skills`
- Create short `sk-*` aliases for speckit skills: `make install-speckit-aliases`
- Launch Codex for this repo with Ralph MCP enabled: `make codex-local`
- Launch Codex in repo-local demo mode: `make codex-demo`

## Demo Shape

The live demo currently has three main segments:

1. OGL content crisis
2. contract analysis and security audit
3. jetpacks / multi-agent implementation

Rule of thumb:

- each segment gets one visible live step
- the next consequential step should usually use predetermined state
- prepared artifacts are part of the design, not an admission of failure

## Current Runbook

### Segment 1: OGL Content Crisis

Slide cue: `Join the fray`

1. Set the scene: the phone call just came in and we need to quantify the blast radius.
2. Open the demo workspace and briefly show the source material.
3. Show the ingest or ETL action live.
4. Cut over to a separately loaded Postgres database for the cross-reference and reporting step.
5. Show the damage report.
6. Generate replacement names if time allows.
7. Wrap with a quantified impact summary.

### Segment 2: Contract Analysis and Security Audit

Slide cue: `It's a TRAP!`

1. Transition to the next problem: more work landed, but the contract contains risk.
2. Ingest the contract artifact live.
3. Introduce the vulnerable buildpack artifact, which is just a `Dockerfile`.
4. Run deterministic local security checks.
5. Feed the artifact and findings to the primary model for explanation.
6. Show adversarial or second-opinion review only if it helps and the budget permits.
7. Show prepared explainers, checklists, and findings overlays.
8. Transition from findings into spec generation, clarification, and planning.

### Segment 3: Jetpacks / Working Together

Slide cue: `Jetpacks for everybody`

1. Transition: now that we know how to review, we build.
2. Show a small, bounded feature spec.
3. Start one visible live orchestration step.
4. Explain the agent roles or hats.
5. Cut over to prepared repo or worktree state for the payoff.
6. Show passing tests, implementation progress, or a PR/result artifact.
7. Wrap by tying the result back to orchestration as the message.

## Concrete Decisions So Far

- the demo database is always Postgres
- the fake buildpack artifact is just a `Dockerfile`
- the contract/security segment should use layered audit behavior:
  1. deterministic local checks
  2. one primary model explanation
  3. optional adversarial second opinion
- `./plan.md` is the canonical entry point for the demo workspace

## Near-Term Buildout

This directory will likely need:

- a task runner, with `Makefile` preferred
- Postgres scaffolding
- seeded demo state loaders
- pre-baked outputs for each segment
- the vulnerable `Dockerfile`
- minimal runbooks for setup, live use, and fallback

## Maintenance Notes

- When the demo plan changes, update [`plan.md`](./plan.md) first.
- Keep this README optimized for quick scanning, navigation, and stress-case execution.
- If we later update constitution or skill guidance, point those documents at [`plan.md`](./plan.md) as the canonical demo entry point.

## Workspace Index

### Core demo docs

- [Canonical demo plan](./plan.md)
- [Prior demo plan draft](./plan-v1.md)
- [Spec clarifications](./spec-clarifications.md)
- [Explainers plan](./explainers-plan.md)

### Repo-level planning and specs

- [Talk outline and slide-driven plan](../plan.md)
- [Talk promises and expectations](../expectations.md)
- [Conference demo spec](../specs/001-conference-demo/spec.md)
- [Spec quality checklist](../specs/001-conference-demo/checklists/requirements.md)

### Notes and working memos

- [Security audit options](../notes/dex/security-audit-options.md)
- [Original demo execution notes](../notes/demo-plan.md)
- [Refinement demo script notes](../notes/whitmo/refinement-docs/demo-script.md)
- [Audit verification framework](../notes/whitmo/refinement-docs/audit-verification-framework.md)
- [Orchestration task graph notes](../notes/whitmo/refinement-docs/orchestration-task-graph.md)

### Explainers and visuals

- [Demo plan explainer](../presentation/explainers/demo-plan.html)
- [Checklist progress explainer](../presentation/explainers/checklist-progress.html)
- [Playbook explainer](../presentation/explainers/playbook.html)
- [System overview explainer](../presentation/explainers/system-overview.html)

### Scripts and helpers

- [Vendored skill installer](./scripts/install-vendored-skills.sh)
- [Skill frontmatter repair helper](../agent/scripts/fix_skill_frontmatter.py)
- [Repo-local Codex launcher with Ralph MCP](../agent/scripts/codex-local-ralph-mcp.sh)
- [Repo-local Codex demo-mode launcher](../agent/scripts/codex-demo-mode.sh)
