# Data Model: Conference Demo

## DemoSegment

**Purpose**: Represents one live section of the conference demo.

**Fields**:

- `name`: stable segment name
- `slide_cue`: slide title or anchor used during delivery
- `story_goal`: audience-facing purpose of the segment
- `time_budget`: allotted runtime for the segment
- `live_proof_step`: the one visible live action that establishes credibility
- `cutover_rule`: the condition that triggers fallback or predetermined-state use
- `fallback_outcome`: the minimum successful teaching outcome

**Relationships**:

- has many `PreparedArtifact`
- may depend on one or more `PreparedState`
- may surface one or more `DependencyRisk`
- may use one or more `VisualExplainer`

## PreparedState

**Purpose**: Represents a known-good state loaded ahead of time so a demo can continue deterministically.

**Fields**:

- `name`: state identifier
- `backing_system`: Postgres, repo/worktree, file tree, or equivalent
- `source_step`: the live or offline workflow that originally produced it
- `trust_level`: whether it is stage-trusted for continuation
- `refresh_path`: how to regenerate or reload it

**Relationships**:

- belongs to one or more `DemoSegment`
- may be materialized by one or more `WorkspaceAsset`

## PreparedArtifact

**Purpose**: Represents a prebaked output used either as evidence or as a fallback.

**Fields**:

- `name`: artifact identifier
- `artifact_type`: markdown, HTML, screenshot, recording, report, or similar
- `location`: tracked repo path
- `primary_use`: evidence, fallback, transition aid, or explainer
- `refresh_path`: script or manual generation path

**Relationships**:

- belongs to one or more `DemoSegment`
- may correspond to a `VisualExplainer`

## VisualExplainer

**Purpose**: Represents a prepared HTML explainer defined in the explainer plan.

**Fields**:

- `name`: explainer name
- `purpose`: stage value
- `when_used`: trigger point in the runbook
- `format`: flow, comparison table, audit view, orchestration map, or similar
- `output_path`: generated HTML path
- `priority`: build order

**Relationships**:

- may satisfy one or more `PreparedArtifact`
- supports one or more `DemoSegment`

## DependencyRisk

**Purpose**: Represents an external or local dependency that can fail during delivery.

**Fields**:

- `name`: dependency identifier
- `tier`: mandatory, optional enhancement, local operational, or sharing constraint
- `failure_mode`: what can go wrong
- `mitigation`: planned response
- `stage_impact`: effect on the audience-facing outcome

**Relationships**:

- may affect one or more `DemoSegment`

## WorkspaceAsset

**Purpose**: Represents a tracked file, script, scaffold, or specimen within the demo workspace.

**Fields**:

- `path`: repo-relative location
- `asset_role`: plan, runbook, script, scaffold, specimen, loader, or output
- `canonical_status`: whether it is source of truth, derivative, or generated
- `shareability`: shareable as-is, sanitizable, or internal-only

**Relationships**:

- may implement or document `PreparedState`
- may generate or store `PreparedArtifact`
- may be referenced by one or more `DemoSegment`
