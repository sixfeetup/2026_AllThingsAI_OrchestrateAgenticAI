# Tasks: Conference Demo

**Input**: Design documents from `/specs/001-conference-demo/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Tests are lightweight for this feature. Prefer script smoke checks, markdown/doc validation, and rehearsal validation tasks rather than a heavy automated test suite.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- Demo workspace: `demo/`
- Presenter/runbook docs: `demo/*.md`
- Helper scripts: `demo/scripts/`, `agent/scripts/`
- Generated explainers: `presentation/explainers/`
- Planning artifacts: `specs/001-conference-demo/`
- Exploratory/internal diagrams and notes: `notes/`

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Establish the demo workspace structure and operator entry points

- [ ] T001 Create `demo/Makefile` with stable targets for setup, Postgres bootstrap, audit execution, and fallback opening in `demo/Makefile`
- [ ] T002 [P] Create initial demo workspace directories for runtime assets in `demo/postgres/.gitkeep`, `demo/artifacts/.gitkeep`, and `demo/specimens/.gitkeep`
- [ ] T003 [P] Add demo workspace usage notes and command references to `demo/README.md`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core demo infrastructure that MUST be complete before any user story can be delivered cleanly

**⚠️ CRITICAL**: No user story work should be considered rehearsal-ready until this phase is complete

- [ ] T004 Create Postgres scaffold and seed/load conventions for the demo workspace in `demo/postgres/README.md`
- [ ] T005 [P] Add initial Postgres bootstrap, pgvector setup, or helper scripts for local demo setup in `demo/postgres/`
- [ ] T006 Define prepared artifact storage conventions and naming rules in `demo/artifacts/README.md`
- [ ] T007 [P] Add a vulnerable buildpack Dockerfile specimen placeholder with documented intent in `demo/specimens/Dockerfile`
- [ ] T008 Update `demo/plan.md` with the agreed initial PoC cloud boundary for Notion, Google Cloud Storage, object-triggered eventing, isolated OpenTofu, and safe CI/CD separation in `demo/plan.md`
- [ ] T009 Update `specs/001-conference-demo/plan.md` and `specs/001-conference-demo/research.md` to reflect the 2026-03-12 PoC clarification in `specs/001-conference-demo/plan.md` and `specs/001-conference-demo/research.md`
- [ ] T010 [P] Add WAL-backed recovery notes or helper scripts for survivability rehearsal in `demo/postgres/`

**Checkpoint**: Demo workspace foundations exist, Postgres is scaffolded, the PoC infrastructure boundary is documented, and user-story delivery can proceed

---

## Phase 3: User Story 1 - Deliver a credible live contract-review demo (Priority: P1) 🎯 MVP

**Goal**: Make the contract/security segment rehearsable, evidence-backed, and survivable under stage conditions

**Independent Test**: Rehearse the contract/security segment using the runbook and confirm it can show a vulnerable `Dockerfile`, deterministic audit findings, one model-guided explanation path, and a prepared fallback explainer without relying on live improvisation

### Implementation for User Story 1

- [ ] T011 [US1] Implement the vulnerable `Dockerfile` specimen with one intentional, explainable issue in `demo/specimens/Dockerfile`
- [ ] T012 [P] [US1] Add deterministic local audit instructions and expected findings for the specimen in `demo/specimens/README.md`
- [ ] T013 [US1] Create the Segment 2 prepared findings artifact contract in `demo/artifacts/security-audit-findings.md`
- [ ] T014 [P] [US1] Build the Security Audit Findings explainer defined in the explainer plan at `presentation/explainers/security-audit-findings.html`
- [ ] T015 [P] [US1] Build the Spec-to-Plan Hand-Off explainer at `presentation/explainers/spec-to-plan-handoff.html`
- [ ] T016 [US1] Add the survivability scenario runbook for fabricated prompt injection and WAL-backed recovery in `demo/README.md`
- [ ] T017 [P] [US1] Create the survivability recovery artifact or note with bounded data-loss expectations in `demo/artifacts/survivability-recovery.md`
- [ ] T018 [US1] Record the contract/security dependency risks and cutover rules in `demo/spec-clarifications.md`
- [ ] T019 [US1] Validate the contract/security segment against the runbook and capture rehearsal notes in `notes/dex/security-audit-options.md`

**Checkpoint**: User Story 1 should be independently demonstrable with a local audit path, a prepared fallback, and a clear operator flow

---

## Phase 4: User Story 2 - Show breadth across the full demo arc (Priority: P2)

**Goal**: Connect the OGL, contract/security, and jetpacks segments into one coherent narrative with matching artifacts

**Independent Test**: Walk through the three segment descriptions in order and confirm each transition, artifact handoff, and explainer cue is understandable without extra narration

### Implementation for User Story 2

- [ ] T020 [US2] Add Segment 1 prepared Postgres-state documentation and ETL handoff notes in `demo/postgres/README.md`
- [ ] T021 [P] [US2] Create the OGL damage report prepared artifact in `demo/artifacts/ogl-damage-report.md`
- [ ] T022 [P] [US2] Build the OGL Damage Report Overview explainer at `presentation/explainers/ogl-damage-report.html`
- [ ] T023 [P] [US2] Build the Demo Flow Overview explainer at `presentation/explainers/demo-flow-overview.html`
- [ ] T024 [US2] Update `demo/README.md` so Segment 1 and Segment 3 transitions explicitly reference their predetermined states and fallback assets
- [ ] T025 [US2] Align `demo/plan.md` with the current three-segment operator flow and canonical transition language in `demo/plan.md`
- [ ] T026 [US2] Add or update the segment-level evidence trail in `checklist.md`

**Checkpoint**: User Stories 1 and 2 should now present a coherent end-to-end demo arc with visible continuity and fallback support

---

## Phase 5: User Story 3 - Operate the demo confidently under stage conditions (Priority: P3)

**Goal**: Reduce operator risk through clear commands, launchers, durable local setup, and fast retrieval of the right artifact under pressure

**Independent Test**: Starting from the repo root, use the documented helpers to launch Codex, access the correct docs, and retrieve the next fallback artifact for each segment in under 30 seconds

### Implementation for User Story 3

- [ ] T027 [US3] Add a stress-case command flow section with exact `make` targets and retrieval paths to `demo/README.md`
- [ ] T028 [P] [US3] Extend `demo/Makefile` with targets for opening explainers and prepared artifacts in `demo/Makefile`
- [ ] T029 [P] [US3] Build the Jetpacks Orchestration explainer at `presentation/explainers/jetpacks-orchestration.html`
- [ ] T030 [P] [US3] Build the Adversarial Review Comparison explainer at `presentation/explainers/adversarial-review-comparison.html`
- [ ] T031 [US3] Update the repo-local Codex launcher documentation for stage use in `demo/README.md`
- [ ] T032 [US3] Add a concise preflight checklist for credentials, auth boundaries, rollback safety, and recovery prerequisites to `demo/README.md`
- [ ] T033 [US3] Capture a simplified rehearsal/status recap diagram or note for operator review in `notes/dex/`

**Checkpoint**: All three user stories should be independently usable, and the operator path should be fast enough for live demo conditions

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Final consistency, validation, and cleanup across the entire demo workspace

- [ ] T034 [P] Validate all links and source-of-truth references across `demo/README.md`, `demo/plan.md`, `demo/explainers-plan.md`, and `specs/001-conference-demo/`
- [ ] T035 [P] Run smoke checks for the new helper commands, recovery helpers, and launchers using `make` targets and wrapper scripts from the repo root
- [ ] T036 Verify generated explainers open correctly and are stored in the correct repo locations under `presentation/explainers/` or `notes/`
- [ ] T037 Re-run the talk/demo checklist review and mark current delivery state in `checklist.md`
- [ ] T038 Prepare a new checkpoint commit once the implementation tasks above are complete

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies; can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion; blocks all user-story work
- **User Story 1 (Phase 3)**: Depends on Foundational completion; this is the MVP path
- **User Story 2 (Phase 4)**: Depends on Foundational completion and benefits from User Story 1 artifacts
- **User Story 3 (Phase 5)**: Depends on Foundational completion and should integrate with earlier story artifacts
- **Polish (Phase 6)**: Depends on all targeted user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational; no dependency on other stories
- **User Story 2 (P2)**: Can start after Foundational, but should reference the finished Segment 2 artifacts from US1 for narrative consistency
- **User Story 3 (P3)**: Can start after Foundational, but works best once the key artifacts from US1 and US2 exist

### Parallel Opportunities

- T002 and T003 can run in parallel
- T004 through T007 can be split across multiple contributors once the workspace layout exists
- Within US1, T012, T014, T015, and T017 can run in parallel after T011/T013 establish the specimen and findings
- Within US2, T021, T022, and T023 can run in parallel
- Within US3, T028, T029, and T030 can run in parallel
- In Phase 6, T034 and T035 can run in parallel before final validation

---

## Parallel Example: User Story 1

```bash
# Build the local audit support and explainers for Segment 2 in parallel:
Task: "Add deterministic local audit instructions in demo/specimens/README.md"
Task: "Build presentation/explainers/security-audit-findings.html"
Task: "Build presentation/explainers/spec-to-plan-handoff.html"
Task: "Create demo/artifacts/survivability-recovery.md"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational
3. Complete Phase 3: User Story 1
4. Stop and rehearse the contract/security segment independently

### Incremental Delivery

1. Foundation first: workspace, Postgres/pgvector scaffold, WAL-backed recovery path, specimen path, and clarified PoC boundary
2. Add User Story 1: make the contract/security demo real and survivable
3. Add User Story 2: connect the full demo arc and segment transitions
4. Add User Story 3: tighten operator ergonomics, launcher flow, and fast fallback access
5. Polish: validate links, commands, explainers, and checklist state

### Parallel Team Strategy

With multiple contributors:

1. One person handles workspace foundations and `demo/Makefile`
2. One person handles the Segment 2 specimen/audit/explainers
3. One person handles Segment 1 and Segment 3 prepared artifacts/explainers
4. Regroup for README, checklist, and final rehearsal validation

---

## Notes

- [P] tasks touch different files and can be split safely
- Story labels map directly to the spec’s user stories
- Rehearsal validation is part of delivery, not postscript
- Keep diagrams/explainers in `notes/` unless they are for the presentation or demo itself
- Use `demo/plan.md` as the canonical source of truth whenever implementation details drift
