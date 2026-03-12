# Demo Workspace Contract

## Purpose

Define the minimum stable contract for the conference demo workspace so collaborators can add assets without breaking the operator path.

## Canonical documents

- `demo/plan.md` is the canonical demo description.
- `demo/README.md` is the stress-case operator guide.
- `demo/explainers-plan.md` is the source of truth for visual explainers.

## Required workspace behaviors

1. The workspace must support three named demo segments:
   - OGL content crisis
   - contract/security review
   - jetpacks / orchestration
2. The workspace must treat Postgres as the only supported demo database.
3. The workspace must include or reference a vulnerable `Dockerfile` specimen for the security segment.
4. The workspace must provide prepared artifacts or explainers for each segment’s fallback path.
5. The workspace must preserve the distinction between:
   - canonical planning documents
   - operator-facing docs
   - generated explainers and outputs

## Directory expectations

### `demo/`

- presenter-facing runbooks
- workspace-local plans
- task runner entry points
- scaffolding, seed loaders, and specimens
- prepared artifacts intended to travel with the demo

### `presentation/explainers/`

- generated HTML explainers used in the talk or fallback paths

### `specs/001-conference-demo/`

- planning artifacts created through the spec-kit workflow

## Change rules

1. If the demo story changes, update `demo/plan.md` first.
2. If operator behavior changes, update `demo/README.md`.
3. If a new explainer is added or removed, update `demo/explainers-plan.md`.
4. If a new artifact becomes necessary to support a live claim, it must be tracked in the repo or explicitly documented as generated output.
