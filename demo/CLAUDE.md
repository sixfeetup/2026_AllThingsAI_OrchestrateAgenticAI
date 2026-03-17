# Contract Review Demo

This directory contains a contract review pipeline demo for a conference talk
on building agentic AI systems with Claude Code.

## Quick Start

```bash
# Reset and load the demo contract
make reset

# Or step-by-step:
make contract   # generate the PDF
make load       # parse + load into SQLite/ChromaDB
make search Q="intellectual property"   # test a search
```

## Available Skills

| Skill | Trigger | What it does |
|-------|---------|-------------|
| contract-loader | `/load-contract` | Parse PDF, load into SQLite + ChromaDB |
| contract-search | `/search-contract <query>` | Semantic + keyword search |
| contract-eval | `/eval-contract [criteria]` | Evaluate against criteria file |
| contract-audit | `/audit-contract` | Show audit trail |

## Available MCP Tools

The `contract-review` MCP server exposes the same pipeline as tools:
- `load_contract` — parse and load a PDF
- `search_contract` — dual semantic + keyword search
- `audit_contract` — view audit trail
- `get_contract_stats` — clause counts and flag distribution
- `list_criteria_files` / `read_criteria_file` — browse eval criteria

## Agent Templates

Agent templates in `.agents/` define specialized roles:
- **data-loader-agent** — ingestion and data quality
- **contract-eval-agent** — systematic clause analysis
- **data-investigator-agent** — exploratory forensic analysis
- **verification-agent** — red team / adversarial review
- **response-drafter-agent** — draft professional response memo

## Cowork Workflow

For multi-agent review using Claude Desktop or cowork:

1. **Load phase**: Use `load_contract` tool to ingest the PDF
2. **Eval phase**: Apply criteria files via `search_contract` + LLM judgment
3. **Verify phase**: Challenge findings with adversarial perspective
4. **Draft phase**: Produce response memo from verified findings
5. **Audit phase**: Review the full trail with `audit_contract`

Each phase can be handled by a different Claude instance or agent role.

## Data Stores

- `data/contracts.db` — SQLite (clauses + audit_log tables)
- `data/chroma/` — ChromaDB vector store
- Both are ephemeral — `make clean` removes them

## Constraints

- All deps via `uv run --with` (never pip)
- Everything runs locally (no external services)
- The contract is fake (L&LL LLC) — demo-safe
