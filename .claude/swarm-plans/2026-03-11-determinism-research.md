# Swarm Plan: determinism-research
Date: 2026-03-11 22:30
Goal: Research how to make this project more deterministic and less model/agent dependent (minimize token use for impact)

## Work Units

| # | Worker | Scope | Description |
|---|--------|-------|-------------|
| 1 | token-audit | Audit current pipeline | Map every point where an LLM is invoked, estimate token cost per operation, identify the most expensive/least-deterministic steps. Produce a ranked list of "token sinks" with alternatives. |
| 2 | static-tooling | Research static alternatives | For each LLM-dependent step, research deterministic alternatives: template engines (Jinja2, Marp, Slidev), linters (markdownlint), schema validators, static site generators. Focus on drop-in replacements. |
| 3 | caching-strategy | Research caching and memoization | How to cache LLM outputs so identical inputs don't re-invoke the model. Content-addressable storage, hash-based cache keys, incremental rebuilds. Look at how CI pipelines solve this. |
| 4 | contract-testing | Research contract/schema enforcement | How to define slide schemas (JSON Schema, frontmatter validators, custom linters) so that content correctness is checked statically, not by asking an LLM "does this look right?" |

## Dependencies
- All 4 units are fully independent (no file overlap, pure research)
- Each produces a markdown research document in their worktree

## Expected Outcomes
- 4 research documents with concrete recommendations
- A synthesis plan (post-swarm) combining findings into an actionable roadmap
- Focus: highest token savings for least implementation effort
