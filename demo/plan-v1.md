# Demo Runbook

This directory is the staging area for the conference demo workspace. It should grow into the runnable, shareable artifact for the live presentation.

## Local Helpers

- Install vendored repo skills into Codex: `make install-vendored-skills`
- Symlink vendored repo skills into Codex: `make link-vendored-skills`
- Create short `sk-*` aliases for speckit skills: `make install-speckit-aliases`

## Demo Shape

The live demo has three segments:

1. OGL content crisis
2. contract analysis and security audit
3. jetpacks / multi-agent implementation

Rule of thumb:

- each segment gets one visible live step
- the next consequential step should usually use predetermined state
- prepared artifacts are part of the design, not an admission of failure

## Segment 1: OGL Content Crisis

Slide cue: `Join the fray`

Story beat:

- BizOps understands the dual threat: lose content or face legal action
- the team stands up a database
- the coding agent searches source material, cross-references content, reports damage, and proposes replacements

Operator steps:

1. Set the scene: the phone call just came in and we need to quantify the blast radius.
2. Open the demo workspace and show the source material briefly.
3. Show the ingest or ETL action live enough for the audience to see that the workflow is real.
4. Cut over to a separately loaded Postgres database for the actual cross-reference and reporting steps.
5. Run or reveal the damage report from the loaded database.
6. Generate replacement names live if the time budget allows.
7. Wrap by stating that the team now has a quantified impact report.

Predetermined state:

- a Postgres database is already loaded with the content needed for the report step
- if ingest is shown live, its output is illustrative and not trusted for the next step

Fallback:

- use pre-baked report output or a recording of the ingest flow

## Segment 2: Contract Analysis and Security Audit

Slide cue: `It's a TRAP!`

Story beat:

- the team ingests a contract artifact
- security is treated as a requirement, not a bolt-on
- the system produces explainers, checklists, and adversarial review
- findings feed into a spec-driven workflow

Operator steps:

1. Transition to the new problem: more work landed, but the contract contains risk.
2. Ingest the contract artifact live.
3. Introduce the vulnerable buildpack artifact, which is just a `Dockerfile`.
4. Run deterministic local security checks against the `Dockerfile` and related demo artifacts.
5. Feed the artifact and deterministic findings to the primary model for explanation and prioritization.
6. If available, show adversarial or second-opinion review as a bonus layer rather than the critical path.
7. Show prepared explainers, checklist output, and findings overlays.
8. Transition from findings into spec generation, clarification, and planning.
9. Wrap by reinforcing that security enables speed when baked in early.

Predetermined state:

- the contract and vulnerable `Dockerfile` are staged before the talk
- visual explainers and checklists are pre-generated
- if any live audit step stalls, switch to prepared findings immediately

Fallback:

- open prepared HTML or markdown outputs
- skip secondary providers first
- preserve the deterministic local audit plus one explained finding as the minimum viable outcome

## Segment 3: Jetpacks / Working Together

Slide cue: `Jetpacks for everybody`

Story beat:

- the audience sees agents as composable building blocks
- the system turns a small feature spec into implementation activity
- orchestration patterns are the point, not raw terminal output

Operator steps:

1. Transition: now that we know how to review, we build.
2. Show a small, bounded feature spec.
3. Start one visible live orchestration step, such as a multiclaude or similar agent kickoff.
4. Explain the roles: planner, tester, implementer, reviewer, or equivalent hats.
5. Cut over to prepared repo or worktree state for the payoff.
6. Show passing tests, implementation progress, or a PR/result artifact.
7. Optionally show a second orchestrator path as a contrast, not a requirement.
8. Wrap by tying the result back to the idea that agents become environments for other agents.

Predetermined state:

- the feature spec is prepared ahead of time
- the payoff state is pre-seeded so the demo can land on time

Fallback:

- use a recording or prepared outputs for the orchestration run

## External Dependencies

### Tier 1: mandatory

- primary model/provider for the main visible AI step
- presentation machine
- local CLI tooling
- rendered slides and prepared artifacts

### Tier 2: optional enhancements

- secondary model providers
- extra orchestrators
- local model path if it is good enough to demonstrate but not trusted as primary

### Tier 3: local operational dependencies

- auth state
- 1Password or other credential access
- Postgres
- containers
- seeded repos and worktrees

### Tier 4: eventual sharing constraints

- secrets
- provider-specific configuration
- proprietary data
- machine-specific assumptions

## Concrete Demo Requirements

- the demo database is always Postgres
- the fake buildpack artifact is just a `Dockerfile`
- the security audit should prefer layered execution:
  1. deterministic local checks
  2. one primary model explanation
  3. optional adversarial second opinion

## Near-Term Buildout

This directory will likely need:

- a task runner, with `Makefile` preferred
- Postgres scaffolding
- seeded demo state loaders
- pre-baked outputs for each segment
- the vulnerable `Dockerfile`
- minimal runbooks for setup, live use, and fallback
