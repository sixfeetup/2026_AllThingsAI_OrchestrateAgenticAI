# Research: Conference Demo

## Decision 1: Canonical demo documentation split

**Decision**: Keep `demo/plan.md` as the canonical demo description and `demo/README.md` as the quick-scan operator runbook.

**Rationale**: The presenter needs one source of truth for planning changes and a separate document optimized for stress-case execution. Mixing those concerns would make both weaker.

**Alternatives considered**:

- Keep everything in one README: rejected because it degrades scanability during a live demo.
- Make the root `plan.md` canonical for the demo workspace: rejected because the demo workspace needs a local source of truth that can evolve independently.

## Decision 2: Demo data path and prepared state

**Decision**: Use Postgres as the only supported demo database, prefer pgvector when the demo needs retrieval-backed context management, and cut over to a separately loaded Postgres state after any live ingest or ETL proof step.

**Rationale**: This preserves determinism while still letting the audience see that the ingest path is real. Postgres also matches the clarified requirement and is more credible for a shareable demo workspace than an ad hoc local store.

**Alternatives considered**:

- SQLite for convenience: rejected because it conflicts with the clarified Postgres requirement.
- A separate vector database for retrieval: rejected because it adds avoidable complexity and splits the demo data path.
- Trust state generated live on stage: rejected because it introduces unnecessary timing and recovery risk.

## Decision 3: Security audit execution shape

**Decision**: Run the security audit as layered execution: deterministic local checks first, one primary model explanation second, optional adversarial or secondary review last.

**Rationale**: This gives the demo a guaranteed floor even if network or provider access degrades, while still preserving the “no-miss review” story through cross-checking when conditions allow.

**Alternatives considered**:

- Fully live multi-provider swarm as the primary path: rejected because it places too much risk on external dependencies.
- Local checks only: rejected because it weakens the agentic orchestration story.

## Decision 4: Survivability and recovery path

**Decision**: Demonstrate destructive prompt-injection recovery through PostgreSQL WAL-backed recovery, preferably point-in-time recovery or an equivalent rollback path with explicitly bounded data loss.

**Rationale**: This creates a credible survivability story. The audience sees not only that failure can happen, but that the environment was designed to recover quickly without pretending recovery is free or lossless.

**Alternatives considered**:

- Full rebuild from scratch: rejected because it is too slow and weakens the “resilient environment” message.
- Manual restore with no explicit recovery primitive: rejected because it feels hand-wavy and is less auditable.

## Decision 5: Visual explainers as first-class artifacts

**Decision**: Maintain a dedicated explainer source-of-truth in `demo/explainers-plan.md` and build explainers into `presentation/explainers/` according to demo risk priority.

**Rationale**: The explainers are not decorative; they are fallback and comprehension artifacts. Treating them as first-class planned outputs improves rehearsal quality and reduces slide/demo drift.

**Alternatives considered**:

- Create explainers ad hoc when needed: rejected because it increases rehearsal risk and weakens provenance.
- Store explainer definitions only in notes: rejected because they would be too easy to overlook.

## Decision 6: Repo-local Codex and MCP behavior

**Decision**: Use repo-local launcher scripts to inject `ralph mcp serve` into Codex sessions for this repo instead of modifying the user’s global Codex MCP server list.

**Rationale**: Codex reliably honors `-c mcp_servers.*` overrides, while repo-local config autodiscovery for MCP was not observed. Wrapper scripts give deterministic behavior without polluting global settings.

**Alternatives considered**:

- Add a global MCP server entry: rejected because the user asked for repo-local behavior.
- Depend on repo-local `.codex/config.toml`: rejected because local testing did not show Codex loading MCP servers from that file automatically.
