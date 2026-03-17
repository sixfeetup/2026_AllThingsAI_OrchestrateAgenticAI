# Contract Review Demo

This directory contains a document review pipeline demo for a conference talk
on building agentic AI systems with Claude Code.

## Quick Start

```bash
# Verify archive exists and load documents
make document   # checks for the zip archive
make load       # extract, parse, and load into SQLite/ChromaDB

# Or restore cached data instantly:
make load-cached

# Test a search
make search Q="submission requirements"
```

## Document Source

The demo uses a real government RFP package:
`assets/1-RFP 20-020 - Original Documents.zip`
containing 17 documents (3 PDFs, 4 DOCX, 3 DOC, 4 XLSX, 1 XLS).

## Available Skills

| Skill | Trigger | What it does |
|-------|---------|-------------|
| contract-loader | `/load-document` | Extract zip, parse multi-format documents, load into SQLite + ChromaDB |
| contract-search | `/search-document <query>` | Semantic + keyword search across all loaded documents |
| contract-eval | `/eval-document [criteria]` | Evaluate against criteria file across full document package |
| contract-audit | `/audit-document` | Show audit trail |

## Available MCP Tools

The `contract-review` MCP server exposes the same pipeline as tools:
- `load_contract` — extract and load a document archive
- `search_contract` — dual semantic + keyword search across all documents
- `audit_contract` — view audit trail
- `get_contract_stats` — clause counts and flag distribution
- `list_criteria_files` / `read_criteria_file` — browse eval criteria

## Agent Templates

Agent templates in `.agents/` define specialized roles:
- **data-loader-agent** — ingestion, multi-format extraction, and data quality
- **contract-eval-agent** — systematic cross-document analysis
- **data-investigator-agent** — exploratory forensic analysis
- **verification-agent** — red team / adversarial review
- **response-drafter-agent** — draft professional response memo

## Cowork Workflow

For multi-agent review using Claude Desktop or cowork:

1. **Load phase**: Use `load_contract` tool to ingest the document archive
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
- The document archive is a real government RFP — handle with appropriate care
