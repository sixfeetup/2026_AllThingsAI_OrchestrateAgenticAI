# Implementation Plan: Conference Demo

**Branch**: `001-conference-demo` | **Date**: 2026-03-11 | **Spec**: [spec.md](/Users/whit/work/2026-allthings-ai-presentation/.claude/worktrees/demo-init/specs/001-conference-demo/spec.md)
**Input**: Feature specification from `/specs/001-conference-demo/spec.md`

## Summary

Create a runnable, rehearsal-friendly demo workspace rooted in `demo/` that supports the three-segment conference story with deterministic cutovers, Postgres-backed prepared state, a shareable vulnerable `Dockerfile` specimen, and a source-of-truth explainer plan. Implementation should prioritize operator speed under stress while keeping `demo/plan.md` as the canonical description and preserving fallback-first delivery.

## Technical Context

**Language/Version**: Shell scripts (`zsh`/POSIX bash compatible where practical), Python 3 via `uv` for helper automation, Markdown/HTML for runbooks and explainers  
**Primary Dependencies**: `uv`, Codex CLI, Ralph CLI, Make, Postgres, repo-local markdown and HTML artifacts  
**Storage**: PostgreSQL for demo state; filesystem for prepared artifacts, plans, explainers, and generated outputs  
**Testing**: Script smoke checks, Markdown/doc consistency checks, manual rehearsal validation, targeted command verification via `make`  
**Target Platform**: macOS presenter machine with terminal access and local CLIs installed  
**Project Type**: Demo workspace plus documentation/runbook tooling  
**Performance Goals**: Operator can reach the next required artifact in under 10 seconds during rehearsal; fallback artifacts open in under 30 seconds after cutover  
**Constraints**: Must tolerate partial network failure; must keep README scannable under stress; must prefer predetermined state after live proof steps; must remain publishable or sanitizable later  
**Scale/Scope**: Three live demo segments, one canonical plan, one explainer source-of-truth, one Postgres-backed data path, one vulnerable Dockerfile specimen, a small set of launcher/install scripts

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- Narrative fit: Pass. The work directly strengthens the promised conference talk by turning the demo into a recoverable three-act runbook with visible evidence for the claims.
- Slide-source alignment: Pass with sync obligations. `presentation/content/09-join-the-fray.md`, [presentation/content/13-its-a-trap.md](/Users/whit/work/2026-allthings-ai-presentation/.claude/worktrees/demo-init/presentation/content/13-its-a-trap.md), and [presentation/content/14-jetpacks.md](/Users/whit/work/2026-allthings-ai-presentation/.claude/worktrees/demo-init/presentation/content/14-jetpacks.md) remain the narrative source; derivative artifacts include [demo/plan.md](/Users/whit/work/2026-allthings-ai-presentation/.claude/worktrees/demo-init/demo/plan.md), [demo/README.md](/Users/whit/work/2026-allthings-ai-presentation/.claude/worktrees/demo-init/demo/README.md), [demo/explainers-plan.md](/Users/whit/work/2026-allthings-ai-presentation/.claude/worktrees/demo-init/demo/explainers-plan.md), and the feature spec artifacts.
- Evidence trail: Pass. Evidence will live in `demo/plan.md`, `demo/README.md`, `demo/explainers-plan.md`, `presentation/explainers/`, Postgres loader/scaffold assets in `demo/`, the vulnerable `Dockerfile`, and spec-kit outputs in `specs/001-conference-demo/`.
- Delivery safety: Pass. Each segment is planned around one live proof step followed by predetermined state, with explainers and prepared artifacts as explicit fallbacks.
- Reproducibility: Pass with implementation work remaining. New assets must be generated from tracked scripts and Markdown plans under `demo/` with `Makefile` entry points for repeatability.

## Project Structure

### Documentation (this feature)

```text
specs/001-conference-demo/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   └── demo-workspace-contract.md
└── tasks.md
```

### Source Code (repository root)

```text
demo/
├── README.md
├── plan.md
├── explainers-plan.md
├── spec-clarifications.md
├── scripts/
│   └── install-vendored-skills.sh
├── postgres/                  # planned: local DB scaffold and seed loaders
├── artifacts/                 # planned: prepared outputs and fallback files
└── specimens/
    └── Dockerfile             # planned: vulnerable buildpack specimen

agent/
└── scripts/
    ├── codex-demo-mode.sh
    ├── codex-local-ralph-mcp.sh
    └── fix_skill_frontmatter.py

presentation/
├── content/
└── explainers/

specs/001-conference-demo/
└── ...
```

**Structure Decision**: Use the existing repo as a documentation-first demo workspace. `demo/` becomes the operator-facing and eventually shareable runtime area, `presentation/explainers/` holds generated visual artifacts, and `specs/001-conference-demo/` captures the implementation planning trail.

## Phase 0: Research Summary

Research findings are recorded in [research.md](/Users/whit/work/2026-allthings-ai-presentation/.claude/worktrees/demo-init/specs/001-conference-demo/research.md). The key decisions are:

1. Treat `demo/plan.md` as the canonical demo description and `demo/README.md` as the stress-case operator document.
2. Use Postgres as the single supported demo database and never rely on state produced by a live ingest step for the next consequential action.
3. Keep the security audit layered: deterministic local checks first, one primary model explanation second, optional adversarial review third.
4. Define visual explainers in a dedicated source-of-truth file and build the highest-risk explainers first.
5. Use repo-local Codex launcher wrappers instead of mutating global Codex MCP configuration for demo-specific behavior.

## Phase 1: Design

### Data Model

The feature’s planning entities are documented in [data-model.md](/Users/whit/work/2026-allthings-ai-presentation/.claude/worktrees/demo-init/specs/001-conference-demo/data-model.md). The model centers on `DemoSegment`, `PreparedState`, `PreparedArtifact`, `VisualExplainer`, `DependencyRisk`, and `WorkspaceAsset`.

### Contracts

The demo is primarily internal to the repo, but it exposes a stable workspace contract for collaborators and future sharing. That contract is documented in [contracts/demo-workspace-contract.md](/Users/whit/work/2026-allthings-ai-presentation/.claude/worktrees/demo-init/specs/001-conference-demo/contracts/demo-workspace-contract.md).

### Quickstart

The first-pass implementation and rehearsal workflow is documented in [quickstart.md](/Users/whit/work/2026-allthings-ai-presentation/.claude/worktrees/demo-init/specs/001-conference-demo/quickstart.md).

## Phase 2: Implementation Strategy

### Workstreams

1. Workspace foundations
   Create the `demo/` layout, task runner, Postgres scaffold, and canonical runbook structure.
2. Segment 1 assets
   Add ETL inputs, preloaded Postgres state, fallback reports, and a simple explainer/report path.
3. Segment 2 assets
   Add the vulnerable `Dockerfile`, deterministic security audit path, prepared findings, and high-priority explainers.
4. Segment 3 assets
   Add the bounded feature-spec demo inputs, predetermined repo/worktree payoff state, and orchestration explainers or recordings.
5. Launch/runtime integration
   Finalize repo-local Codex launchers, skill installers, and any demo-oriented helper commands.
6. Rehearsal hardening
   Validate timing, cutovers, fallback assets, and README usability under pressure.

### Sequencing

1. Build the `demo/` workspace and `Makefile`.
2. Add Postgres scaffolding and seed/load conventions.
3. Create the vulnerable `Dockerfile` specimen and deterministic audit path.
4. Build the explainers defined in `demo/explainers-plan.md`, starting with Segment 2.
5. Add prepared artifacts and recordings needed for cutovers.
6. Rehearse and tighten the README/runbook based on actual operator friction.

## Post-Design Constitution Check

- Narrative fit: Still passes. The plan keeps the demo centered on the talk’s promised arc.
- Slide-source alignment: Still passes. No slide edits are required yet, but all derived documents point back to the slide-driven narrative.
- Evidence trail: Improved. The plan now names concrete repo artifacts for each major claim and demo transition.
- Delivery safety: Improved. Predetermined-state cutovers, explainers, and repo-local launch wrappers reduce stage risk.
- Reproducibility: Improved. The plan converges on tracked scripts, `Makefile` entry points, and source-of-truth docs rather than ad hoc terminal choreography.

## Complexity Tracking

No constitution violations currently require justification.
