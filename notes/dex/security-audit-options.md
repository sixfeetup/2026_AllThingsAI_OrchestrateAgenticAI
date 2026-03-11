---
title: Security Audit Options
status: draft
audience: internal
owner: dex
---

# Security Audit Options

Working note for deciding how to run the security audit portion of the demo.

## Goal

We need an audit flow that is:

- credible on stage
- fast enough for a live segment
- resilient to provider or network issues
- easy to explain
- compatible with a shareable post-talk demo workspace

## Recommended Default

Use a layered audit:

1. local deterministic checks first
2. one primary model-guided review second
3. optional adversarial second opinion last

This gives us a stable baseline even if model access degrades.

## Suggested Audit Shape

### Layer 1: deterministic local checks

Run local checks against the vulnerable `Dockerfile` and related artifacts.

Purpose:

- guarantees we always have something to show
- gives concrete findings quickly
- creates anchors the model can explain rather than invent

Examples of checks:

- Dockerfile linting
- base image age or known-risk check
- secret-pattern scan
- package/version smell detection

### Layer 2: primary model review

Send the artifact plus local findings to one primary model for explanation and prioritization.

Purpose:

- explains impact in human terms
- connects technical findings to security posture
- shows the value of agentic orchestration rather than raw scanning

Stage rule:

- this is the main live AI moment
- if it is slow or fails, switch to prepared output immediately

### Layer 3: adversarial or comparative review

Optionally send the same artifact to another model or agent path.

Purpose:

- shows cross-checking
- reinforces the “no-miss review” story
- useful if the first model misses something or frames it poorly

Stage rule:

- never make this mandatory for the demo to land
- it is a bonus, not the backbone

## Decision Options

### Option A: mostly local, AI explains

Flow:

- run local checks
- feed findings plus artifact to one model
- show prepared second-opinion output if desired

Pros:

- lowest live risk
- easiest to rehearse
- easiest to share later

Cons:

- less flashy than a fully live swarm

Recommendation:

- best default

### Option B: primary live model plus backup outputs

Flow:

- run a live model-centered audit
- keep local checks and prepared outputs ready underneath

Pros:

- more dramatic
- still recoverable

Cons:

- more timing and network risk

Recommendation:

- acceptable if the primary model path is very well rehearsed

### Option C: full multi-model adversarial swarm

Flow:

- multiple providers review the same artifact live

Pros:

- strongest theater
- best demonstration of cross-checking

Cons:

- highest dependency risk
- hardest to time-box
- easiest path to demo failure

Recommendation:

- do not put this on the critical path

## Suggested Demo Position

For the current talk, use Option A as the planned path.

That means:

- local deterministic audit is always available
- one primary model is the live reasoning layer
- adversarial or multi-model review is optional and can be pre-baked

## Artifact Guidance

Use a single vulnerable `Dockerfile` as the core specimen.

It should support:

- deterministic local findings
- model explanation of severity and remediation
- an easy bridge to the broader contract/security/orchestration story

## Risks To Explicitly Plan Around

- conference network loss
- provider auth/session expiry
- quota or rate-limit failures
- secret retrieval friction
- local container or database startup issues
- model latency that breaks the time budget

## Open Questions

- Which deterministic checker set do we want in the demo path?
- Which primary model/provider is trusted enough for the main live review?
- Do we want the adversarial pass to be live, pre-baked, or omitted?
- Should the local model path be positioned as a real fallback or just an extra?
