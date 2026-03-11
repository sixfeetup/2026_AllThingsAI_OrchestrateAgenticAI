---
title: Demo Spec Clarifications
status: draft
audience: internal
purpose: working-notes
---

# Demo Spec Clarifications

Working draft for decisions that should feed back into the formal spec and plan.

## Current Defaults

### 0. Canonical plan location

- The canonical demo plan inside the demo workspace lives at `./demo/plan.md`.
- `./demo/README.md` should serve as the operator-facing index and link hub optimized for quick use under stress.
- If higher-level repo documents reference the demo workspace, they should point readers to `./demo/plan.md` first.

### 1. `./demo` scope

- `./demo` is the future home of the runnable demo workspace.
- Keep presenter-facing assets here: task runner, scripts, seeded state loaders, canned outputs, scaffolding, and the runbook.
- Avoid mixing loose research notes into `./demo` unless they are directly consumed by the demo flow.
- Assume anything under `./demo` may eventually be shared after the presentation, so it should be publishable or easy to sanitize.

### 2. Live action vs predetermined state

- Each demo segment should include at least one visible live step for credibility.
- The next consequential step should usually run against predetermined state rather than state produced by the live step.
- Live steps prove the workflow exists.
- Predetermined state keeps the on-stage path deterministic.
- The operator guide should name the exact cutover artifact or loaded state for each segment.

Examples:

- Demo 1: show ingest or ETL live, then query a separately loaded database.
- Demo 2: show contract intake live, then continue from prepared findings and visual artifacts.
- Demo 3: show agent kickoff live, then continue from a prepared repo or worktree state.

## External Dependency Framing

### Tier 1: Mandatory for the core story

- Primary model/provider used for the main visible agent interactions
- Presentation machine and local CLI/tooling
- Slide deck and pre-rendered assets

### Tier 2: Optional enhancements

- Secondary model providers for adversarial review
- Additional orchestrators or coding agents
- Conference network when a local fallback is acceptable
- Local model usage as an "also and" capability rather than the primary path

### Tier 3: Local operational dependencies

- Authentication state for CLIs and browser sessions
- 1Password or other credential retrieval paths
- Local database instances
- Containers and local service orchestration
- Pre-seeded repos, worktrees, and cached assets

### Tier 4: Shareability constraints

- Secrets embedded in scripts or shell history
- Provider-specific configuration that should not be published
- Proprietary or unsanitized sample data
- Machine-specific paths and assumptions

## Concrete Demo Decisions

### Database

- The demo database is always Postgres.
- ETL and ingest steps should target Postgres, even if a prior exploratory path used another local store.
- If we show population live, the next meaningful query should still point at a separately prepared, already loaded Postgres database.
- The task runner should eventually support standing up or connecting to the demo Postgres instance reproducibly.

### Vulnerable Buildpack Artifact

- We need a fake buildpack artifact in the demo workspace.
- The fake buildpack is just a `Dockerfile`, not a larger buildpack implementation.
- It should contain at least one intentional, explainable vulnerability that the demo can reliably surface.
- The vulnerability should be obvious enough to demonstrate detection and reasoning, but realistic enough not to feel toy.
- The artifact should be safe to share after the talk.

Candidate properties:

- outdated package or base image
- insecure default configuration
- embedded secret or credential smell
- known vulnerable dependency pinned to a specific version

### Local Model Path

- Local model usage is currently an optional enhancement, not the primary dependency.
- It may become a stronger fallback if we find a coding model and agent path that are reliable enough.
- If used, the local path should have cheat cards or constrained prompts so the operator burden stays low.

## Questions To Resolve

- Which demo steps must be truly live versus merely introduced live?
- Which third-party providers are acceptable on the critical path?
- How much auth setup can remain in the presenter workflow before it becomes too fragile?
- What Postgres scaffolding belongs in `./demo` now versus later?
- What vulnerability should the fake buildpack include for the clearest stage narrative?
