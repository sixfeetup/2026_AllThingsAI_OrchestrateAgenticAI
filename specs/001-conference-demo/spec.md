# Feature Specification: Conference Demo

**Feature Branch**: `001-conference-demo`  
**Created**: 2026-03-11  
**Status**: Draft  
**Input**: User description: "Spec out the conference demo for the Agents of Legend presentation, including the three live demo segments, operator flow, prep requirements, and fallback behavior."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Deliver a credible live contract-review demo (Priority: P1)

As the presenter, I need the talk's primary live demo to show a realistic high-stakes review workflow so attendees believe the overall thesis that agent orchestration can make AI reviews more reliable and auditable.

**Why this priority**: The talk promise depends most heavily on a convincing "no-miss review" moment. If this story works, the audience sees the core value even if other demo segments are shortened.

**Independent Test**: Can be fully tested by rehearsing the contract-review segment from start to finish and confirming it demonstrates document intake, structured review output, multi-agent cross-checking, and a fallback path without breaking the narrative.

**Acceptance Scenarios**:

1. **Given** the presenter starts the contract-review segment, **When** the demo runs normally, **Then** the audience sees a realistic artifact reviewed through a structured, auditable workflow with clearly explained findings.
2. **Given** one or more live review steps fail or run slowly, **When** the presenter switches to prepared fallback materials, **Then** the audience still receives the same key findings and narrative without confusion.
3. **Given** the segment concludes, **When** the presenter transitions back to the talk, **Then** the audience understands how the review workflow maps to reliability, governance, and engineering use cases.

---

### User Story 2 - Show breadth across the full demo arc (Priority: P2)

As the presenter, I need the demo plan to connect the opening content-crisis segment, the contract/security segment, and the implementation segment so the audience sees a coherent progression from triage to review to delivery.

**Why this priority**: The talk is stronger when the demos feel like one story instead of unrelated tricks. This creates continuity across business, security, and engineering concerns.

**Independent Test**: Can be fully tested by rehearsing the three demo segments in sequence and confirming each segment has a clear setup, payoff, and transition to the next segment.

**Acceptance Scenarios**:

1. **Given** the presenter starts the first demo segment, **When** the segment is introduced, **Then** the audience understands the business problem and the role of the AI-assisted team.
2. **Given** the presenter moves between demo segments, **When** each transition occurs, **Then** the audience can understand why the next segment follows from the prior one.
3. **Given** the final implementation segment completes, **When** the presenter summarizes the demo arc, **Then** the audience can connect the patterns shown back to the talk's stated promises.

---

### User Story 3 - Operate the demo confidently under stage conditions (Priority: P3)

As the presenter, I need a clear run-of-show, preparation checklist, and time-boxed fallback rules so I can stay in control during a live conference slot with limited time and unpredictable conditions.

**Why this priority**: A stage demo fails more often from operator uncertainty than from any single tool issue. Clear operating rules reduce risk and keep timing disciplined.

**Independent Test**: Can be fully tested by running a rehearsal against the prep checklist and confirming that every segment has a preflight state, a time budget, and an explicit cutover rule.

**Acceptance Scenarios**:

1. **Given** the presenter prepares before the session, **When** the preflight checklist is followed, **Then** all required demo materials, artifacts, and fallback assets are ready.
2. **Given** a demo segment exceeds its allotted time, **When** the cutover threshold is reached, **Then** the presenter can switch to a prepared fallback without deciding ad hoc.
3. **Given** the venue network or a tool fails unexpectedly, **When** the presenter uses the operating guide, **Then** the talk still lands its intended message within the scheduled time.

### Edge Cases

- A live step partially succeeds and produces incomplete output that could confuse the audience unless the presenter has a defined rule for continuing or cutting over.
- A required artifact opens slowly or in the wrong state, forcing the presenter to recover without losing the narrative thread.
- The presenter must shorten the talk in real time because of schedule pressure and needs to know which demo elements are essential versus optional.
- Multiple failures occur in the same segment, requiring a single fallback asset that preserves the learning objective without relying on additional live steps.
- An attendee asks how the demo evidence maps to governance, auditability, or engineering practice, and the presenter needs visible outputs that support that claim.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The demo experience MUST define the purpose, audience takeaway, and narrative role of each of the three demo segments.
- **FR-002**: The demo experience MUST identify one primary segment that proves the talk's core promise about reliable, auditable AI-assisted review.
- **FR-003**: The demo experience MUST provide a step-by-step operator flow for each segment, including the segment start condition, the intended live actions, and the expected audience-visible outcome.
- **FR-004**: The demo experience MUST define a rehearsal-ready time budget for each segment and for the overall live demo portion of the talk.
- **FR-005**: The demo experience MUST list all assets and prerequisites that must be prepared before the talk for each segment.
- **FR-006**: The demo experience MUST define at least one fallback path for each segment that preserves the segment's key learning objective if live execution degrades or fails.
- **FR-007**: The demo experience MUST define explicit cutover rules that tell the presenter when to abandon a live step and use a fallback asset instead.
- **FR-008**: The demo experience MUST preserve narrative continuity across the three segments so they read as one escalating story rather than isolated demonstrations.
- **FR-009**: The demo experience MUST make the roles of humans and AI agents legible to the audience during each segment.
- **FR-010**: The demo experience MUST show how security, review rigor, or validation are incorporated into the demo rather than treated as an afterthought.
- **FR-011**: The demo experience MUST include a concise mapping from demo outputs to the promises made in the talk abstract and outline.
- **FR-012**: The demo experience MUST identify which outputs should be available as prepared artifacts so the talk can still succeed under poor stage conditions.
- **FR-013**: The demo experience MUST distinguish essential live moments from optional embellishments so the presenter can shorten the demo without losing the argument.
- **FR-014**: The demo experience MUST be understandable by collaborators helping rehearse or support the talk, even if they did not create the plan.
- **FR-015**: The demo experience MUST define which steps rely on predetermined state, which steps may be shown live for effect, and where the operator must switch to a separately prepared state for the next action.
- **FR-016**: The demo experience MUST enumerate risks introduced by third-party services, network connectivity, authentication, credential access, and account quotas, along with mitigation plans for each.
- **FR-017**: The demo experience MUST identify which capabilities are required from external or local models and agents so the presenter can judge whether a local-only fallback is viable.
- **FR-018**: The demo experience MUST organize demo materials so they can mature into a reusable, shareable demo workspace after the presentation.
- **FR-019**: The demo experience MUST treat the vulnerable buildpack artifact as a single shareable `Dockerfile` specimen with an intentional, explainable issue suitable for live review.

### Key Entities *(include if feature involves data)*

- **Demo Segment**: A discrete live portion of the talk with a narrative purpose, time budget, operator flow, and fallback strategy.
- **Prepared Artifact**: A pre-generated output, screenshot, recording, or document that can replace a live step while preserving the teaching outcome.
- **Prepared State**: A known-good artifact or environment snapshot that is loaded ahead of time so a later step can proceed deterministically even if an earlier live step was only demonstrated.
- **Operator Flow**: The presenter's run-of-show for a segment, including setup, live actions, transition cues, and cutover decisions.
- **Dependency Risk**: A failure mode tied to network access, external services, authentication, credentials, quotas, or model availability that can affect the live demo.
- **Talk Promise**: A claim made in the abstract, outline, or session framing that the demo must visibly support.

## Assumptions

- The talk will continue to use three demo segments aligned to the current slide narrative: content crisis, contract/security review, and implementation workflow.
- The contract/security review segment remains the highest-value proof point for the audience because it most directly supports the "no-miss review" claim.
- Prepared artifacts are acceptable as long as the audience can still see the same findings and the presenter is transparent about the fallback.
- The presenter needs a plan optimized for a live conference slot rather than a workshop or hands-on session.
- Demo assets will accumulate in a dedicated demo workspace that may later be shared publicly, so the structure should support reruns and handoff.
- Some apparently live actions will be illustrative only; the subsequent step may intentionally run against a separately loaded, known-good state to reduce stage risk.
- The "fake buildpack" used in the security/review demo is represented by a `Dockerfile` rather than a fuller platform artifact.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A rehearsal can be completed end-to-end with all three demo segments fitting within the allocated live-demo time budget and with explicit cutover decisions documented for any segment that overruns.
- **SC-002**: For each demo segment, at least one prepared fallback artifact exists and can deliver the same key audience takeaway in under 30 seconds after a live failure is recognized.
- **SC-003**: In rehearsal review, collaborators can correctly identify the purpose, key outcome, and fallback plan of each segment without additional explanation.
- **SC-004**: The contract/security review segment visibly demonstrates the talk's reliability and auditability claim well enough that a reviewer can point to concrete outputs supporting those claims.
- **SC-005**: The final demo plan makes explicit links to the major promises in the talk materials, with no major promised theme left unsupported by a demo moment or prepared artifact.
- **SC-006**: For every segment, rehearsal notes identify the predetermined state being used, the point at which live execution stops being trusted, and the exact state or artifact used after cutover.
- **SC-007**: Reviewers can inspect the demo plan and find documented mitigations for all major external-service, credential, authentication, and connectivity risks without relying on tribal knowledge.
