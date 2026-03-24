# Document Review Plugin

Multi-agent document review pipeline for contracts, RFPs, and complex documents.

## Quick Start

```
/load-document <path-to-archive-or-file>
/eval-document [criteria-file]
/cowork-review [archive-path]       # full pipeline in one pass
```

## Plugin Structure

```
.claude-plugin/plugin.json    Plugin manifest
agents/                       Agent definitions (markdown with frontmatter)
skills/                       Skills with SKILL.md + co-located scripts
hooks/hooks.json              Lifecycle hooks (SessionStart, PostToolUse)
.mcp.json                     MCP server config
scripts/                      Shared utility scripts
bin/                          Plugin-level executables (MCP server)
```

## Agents

| Agent | Role |
|-------|------|
| data-loader-agent | Ingest documents into SQLite + ChromaDB |
| document-eval-agent | Evaluate against structured criteria |
| data-investigator-agent | Forensic deep-dive investigation |
| verification-agent | Adversarial review of findings |
| response-drafter-agent | Draft professional response memos |
| session-auditor-agent | Audit the review process |

## Skills

| Skill | Trigger |
|-------|---------|
| load-document | `/load-document <path>` |
| search-document | `/search-document <query>` |
| eval-document | `/eval-document [criteria-file]` |
| audit-document | `/audit-document` |
| audlog | `/audlog [view\|add]` |
| cowork-review | `/cowork-review [archive-path]` |
| say | Auto — audio notifications on macOS |

## Review Pipeline

1. **Load** — parse documents into data stores
2. **Evaluate** — apply criteria, rate severity, cite evidence
3. **Investigate** (optional) — open-ended forensic search
4. **Verify** — adversarial challenge of findings
5. **Draft** — professional response memo
6. **Audit** — full provenance trail

## Data

Runtime data (SQLite + ChromaDB) is stored in `${CLAUDE_PLUGIN_DATA}` when installed as a plugin, or local `data/` during development. The data directory is gitignored.

## Dependencies

Python packages are declared inline in each script via [PEP 723](https://peps.python.org/pep-0723/) metadata and resolved automatically by `uv run`. The sentence-transformer embedding model is warmed on session start by the SessionStart hook. No requirements.txt or venv needed — each script is self-contained.
