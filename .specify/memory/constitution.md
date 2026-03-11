<!--
Sync Impact Report
Version change: template -> 1.0.0
Modified principles:
- Principle 1 -> I. Audience-First Narrative
- Principle 2 -> II. Slides Are Source of Truth
- Principle 3 -> III. Demo Claims Require Evidence
- Principle 4 -> IV. Rehearsable and Recoverable Delivery
- Principle 5 -> V. Asset Provenance and Reproducibility
Added sections:
- Delivery Constraints
- Workflow and Quality Gates
Removed sections:
- None
Templates requiring updates:
- ✅ .specify/templates/plan-template.md
- ✅ .specify/templates/spec-template.md (no change required after review)
- ✅ .specify/templates/tasks-template.md (no change required after review)
- ✅ README.md (no change required after review)
- ✅ .specify/templates/commands/*.md (directory absent; no update required)
Follow-up TODOs:
- None
-->
# Agents of Legend Presentation Constitution

## Core Principles

### I. Audience-First Narrative
Every change MUST strengthen a coherent talk for a live conference audience rather
than optimize for internal completeness. Slides, demos, notes, and supporting
artifacts MUST make the problem, the orchestration approach, and the practical
takeaways legible to attendees within the allotted session time. Content that is
interesting but does not support the promised talk arc MUST be trimmed or moved to
speaker notes.

### II. Slides Are Source of Truth
The canonical talk outline lives in `presentation/content/`, and any plan, checklist,
explainer, or note that depends on slide content MUST be kept consistent with it.
When narrative structure changes, derivative artifacts such as `plan.md`,
`checklist.md`, and explainers MUST be updated in the same change or explicitly
flagged as stale. This keeps rehearsal, review, and delivery aligned.

### III. Demo Claims Require Evidence
Every substantive claim about reliability, security, orchestration, or review quality
MUST be backed by a repository artifact that can be shown, rehearsed, or inspected.
Acceptable evidence includes runnable demo assets, checklists, explainers, source
material, or documented outputs in the repo. The talk MUST not depend on hand-wavy
assertions, invisible setup, or unverifiable "trust me" transitions.

### IV. Rehearsable and Recoverable Delivery
Live segments MUST be designed for predictable execution under conference conditions.
Each demo sequence MUST have a fallback path such as a prebaked artifact, screenshot,
or explainer that preserves the teaching point if live execution fails. Changes that
increase operator risk, hidden state, or recovery time MUST include a clear mitigation.

### V. Asset Provenance and Reproducibility
Presentation assets, generated artifacts, and demo inputs MUST remain attributable and
rebuildable from the repository. Scripts, templates, and source materials SHOULD be
preferred over one-off manual edits, and generated outputs SHOULD be traceable to their
inputs. If a result cannot be regenerated exactly, the repo MUST at least document the
source and the expected use of the artifact.

## Delivery Constraints

- The presentation MUST continue to address both business/legal review concerns and
  engineering workflow parallels, because that dual-domain framing is part of the talk
  promise captured in `README.md` and `checklist.md`.
- Content MUST stay scoped to practical orchestration patterns: context engineering,
  checklists, routing, validation, trust boundaries, and no-miss reviews.
- New material SHOULD reuse the repo's established visual and narrative language unless
  an intentional section break calls for a distinct treatment.
- Risky security or governance examples MUST be presented with explicit containment or
  verification steps rather than implied safety.

## Workflow and Quality Gates

- Any feature or content plan created with spec-kit MUST include a constitution check
  covering narrative fit, slide-source alignment, evidence for claims, demo fallback,
  and reproducibility impact.
- Changes to `presentation/content/` MUST be reviewed against `plan.md` and
  `checklist.md`; if they diverge intentionally, the divergence MUST be documented.
- Demo-oriented changes SHOULD be validated by the relevant local build or rendering
  path when one exists, such as the presentation build tooling in `presentation/`.
- Reviews MUST prioritize behavioral regressions in the talk itself: broken narrative
  transitions, unsupported claims, stale explainers, and demo steps that cannot be
  rehearsed reliably.

## Governance

This constitution governs presentation planning, demo design, and supporting repo
artifacts. Amendments MUST document the rationale, the impacted principles or sections,
and any template or guidance files that need syncing. Versioning follows semantic
versioning for governance: MAJOR for incompatible principle changes or removals, MINOR
for new principles or materially expanded requirements, and PATCH for clarifications
that do not change project obligations. Compliance review is required for any planning
or implementation work created through spec-kit workflows, and unresolved deviations
MUST be called out explicitly in the relevant plan or review.

**Version**: 1.0.0 | **Ratified**: 2026-03-11 | **Last Amended**: 2026-03-11
