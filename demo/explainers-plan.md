---
title: Demo Explainers Plan
status: draft
audience: internal
purpose: explainer-source-of-truth
---

# Demo Explainers Plan

This document defines the visual explainers needed for the conference demo and serves as the source of truth for building them.

## Purpose

The explainers should do three jobs:

1. carry the story when a live step needs a fallback
2. make complex workflows legible to the audience quickly
3. provide shareable artifacts for the post-talk demo workspace

## Operating Rules

- Every explainer must support a specific demo moment, not just exist as general decoration.
- Explain both the human and agent roles when the workflow would otherwise look like terminal noise.
- Prefer prepared explainers for dense comparisons, checklists, task graphs, and layered review output.
- Each explainer should have a clear trigger in the demo runbook and an explicit fallback role if the live step stalls.
- The explainer set should stay small enough to rehearse comfortably.

## Explainer Inventory

### 1. Demo Flow Overview

Status:

- existing concept

Purpose:

- show the three demo segments as one escalating story
- orient the audience before or during transitions

When used:

- before the live demos begin or during transitions between segments

Recommended format:

- visual flow overview

Primary content:

- OGL content crisis
- contract/security review
- jetpacks / orchestration
- human roles and AI roles at a glance

Fallback value:

- lets the presenter recover the narrative if timing slips or a segment is shortened

Suggested output:

- `presentation/explainers/demo-flow-overview.html`

### 2. OGL Damage Report Overview

Status:

- needed

Purpose:

- summarize what content was found, what matched protected terms, and what needs replacement

When used:

- after the ingest/search step in demo segment 1

Recommended format:

- data table plus compact summary cards

Primary content:

- source corpus scope
- counts of affected entities
- representative examples
- replacement-name outcome

Fallback value:

- becomes the stage-safe replacement if ingest or query behavior is slow

Suggested output:

- `presentation/explainers/ogl-damage-report.html`

### 3. Security Audit Findings

Status:

- needed

Purpose:

- show the results of the deterministic local audit against the vulnerable `Dockerfile`

When used:

- in demo segment 2 after the buildpack artifact is introduced

Recommended format:

- audit table with severity/status badges

Primary content:

- finding summary
- why each finding matters
- what should be remediated now versus later

Fallback value:

- guarantees a credible security result even if model access degrades

Suggested output:

- `presentation/explainers/security-audit-findings.html`

### 4. Adversarial Review Comparison

Status:

- needed

Purpose:

- compare the primary review path with optional second-opinion or adversarial review

When used:

- late in demo segment 2 if the second review is shown

Recommended format:

- comparison table

Primary content:

- primary reviewer findings
- adversarial reviewer findings
- overlaps
- unique catches
- operator takeaway

Fallback value:

- preserves the “no-miss review” message if multi-provider live review is skipped

Suggested output:

- `presentation/explainers/adversarial-review-comparison.html`

### 5. Spec-to-Plan Hand-Off

Status:

- needed

Purpose:

- show how findings become structured spec work rather than disappearing into chat history

When used:

- at the end of demo segment 2 when moving into speckit

Recommended format:

- pipeline or staged workflow explainer

Primary content:

- finding
- clarification
- plan
- tasks
- implementation

Fallback value:

- keeps the workflow legible if the live speckit step is shortened or pre-baked

Suggested output:

- `presentation/explainers/spec-to-plan-handoff.html`

### 6. Jetpacks Orchestration View

Status:

- needed

Purpose:

- make the multi-agent build flow understandable without forcing the audience to read scrolling terminal output

When used:

- during demo segment 3

Recommended format:

- orchestration diagram with role cards

Primary content:

- spec input
- planner/tester/implementer/reviewer roles or hats
- predetermined-state cutover
- result artifact

Fallback value:

- supports either live orchestration or a recording

Suggested output:

- `presentation/explainers/jetpacks-orchestration.html`

## Priority Order

Build in this order:

1. Security Audit Findings
2. Jetpacks Orchestration View
3. OGL Damage Report Overview
4. Spec-to-Plan Hand-Off
5. Adversarial Review Comparison
6. Demo Flow Overview

Rationale:

- segment 2 carries the most risk and needs the strongest explainer backup
- segment 3 is hard to read live without visual help
- segment 1 benefits from a clean fallback but can survive with simpler output

## Naming and Storage

- Source of truth for explainer definitions: this file
- Generated explainers should live under `presentation/explainers/`
- `demo/README.md` should link to the current explainer set
- If an explainer becomes obsolete, remove it from this file or mark it explicitly as retired

## Open Questions

- Which explainers are mandatory for the first rehearsal?
- Which explainers need static screenshots in addition to HTML?
- Do we want one combined “segment 2 dashboard” or separate explainers for audit, comparison, and spec hand-off?
