# document-review plugin

AI-driven contract and document review pipeline. Parses PDF, DOCX, and XLSX documents (or ZIP archives of them), loads structured clauses into SQLite and ChromaDB, then provides semantic and keyword search, criteria-based evaluation, adversarial verification, and a full audit trail.

## Installation

Add the marketplace, then install the plugin:

```
/plugin marketplace add sixfeetup/2026-allthings-ai-presentation
/plugin install document-review
```

## Skills

The plugin provides six skills that form a complete document review pipeline:

### document-loader (`/load-document`)

Extracts, parses, and loads documents from a ZIP archive or single file into SQLite + ChromaDB. Supports PDF, DOCX, and XLSX formats. Creates a structured clause database with section numbers, titles, body text, and topic flags.

### document-search (`/search-document`)

Searches loaded clauses using combined semantic (ChromaDB vector search) and keyword (SQLite LIKE) search. Supports filtering by section pattern, topic flag, and source document. Every search is logged to the audit trail.

### document-eval (`/eval-document`)

Evaluates loaded documents against a criteria markdown file. Each `##` heading in the criteria file becomes one evaluation criterion. Produces a structured findings report with severity ratings (CRITICAL / HIGH / MEDIUM / LOW / CLEAR), evidence quotes, and source references.

### document-audit (`/audit-document`)

Displays the append-only audit trail of all pipeline actions: loads, searches, evaluations. Useful for provenance tracking and verifying which evidence supports which findings.

### audlog (`/audlog`)

Compact audit timeline viewer and manual entry tool. View the last N entries as a formatted table, or add manual notes, decisions, and handoff markers to the audit trail.

### cowork-review (`/cowork-review`)

Orchestrates the full multi-agent review pipeline end-to-end: load documents, run focused IP evaluation, run broad red-flag scan, perform adversarial verification of findings, draft a professional response memo, and display the audit trail. Designed for both single-agent and cowork (multi-instance) use.

## Prerequisites

- **uv** -- used to manage Python dependencies inline (no virtualenv setup needed)
- Python packages (managed automatically by `uv run --with`):
  - `pymupdf` -- PDF parsing
  - `python-docx` -- DOCX parsing
  - `openpyxl` -- XLSX parsing
  - `chromadb` -- vector store for semantic search
  - `sentence-transformers` -- embedding model for ChromaDB

## MCP Server

The plugin includes an MCP server (`bin/document-mcp-server.py`) that exposes the pipeline as MCP tools for use with Claude Desktop, Cowork, or any MCP-compatible client.

To run the MCP server standalone:

```bash
uv run --with 'mcp,pymupdf,python-docx,openpyxl,chromadb,sentence-transformers' \
  plugins/document-review/bin/document-mcp-server.py
```

The server provides these tools over stdio: `load_document`, `search_document`, `audit_document`, `list_criteria_files`, `get_document_stats`, and `read_criteria_file`.

### Claude Desktop integration

**Upload the plugin (MCP + skills):** Open Claude Desktop → **Customize** → **Browse Plugins** → **Upload Plugin**, then select this directory (`plugins/document-review`). Claude Desktop will read the `.claude-plugin/plugin.json` manifest and register the MCP server automatically.

**Upload skills individually:** To add skills without the full plugin, go to **Customize** → **Browse Plugins** → **Upload Plugin** and select an individual skill directory from `plugins/document-review/skills/`:

- `skills/document-loader` — `/load-document`
- `skills/document-search` — `/search-document`
- `skills/document-eval` — `/eval-document`
- `skills/document-audit` — `/audit-document`
- `skills/audlog` — `/audlog`
- `skills/cowork-review` — `/cowork-review`

Each skill directory contains a `SKILL.md` that Claude Desktop will recognize.

**Via manual MCP config:** Add the following to `~/Library/Application Support/Claude/claude_desktop_config.json` and restart Claude Desktop:

```json
{
  "mcpServers": {
    "document-review": {
      "command": "uv",
      "args": [
        "run",
        "--with", "mcp,pymupdf,python-docx,openpyxl,chromadb,sentence-transformers",
        "/absolute/path/to/plugins/document-review/bin/document-mcp-server.py"
      ]
    }
  }
}
```

## Data

The pipeline stores all data under `demo/data/`:

- `demo/data/documents.db` -- SQLite database with `clauses` and `audit_log` tables
- `demo/data/chroma/` -- ChromaDB vector store for semantic search

This data directory is created automatically on first load and should not be committed.
