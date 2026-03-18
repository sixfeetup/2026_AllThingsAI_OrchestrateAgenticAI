# search-document

Search loaded document clauses using semantic and keyword search across all documents.

## Triggers

- `/search-document <query>`
- User asks to "search", "find", or "look up" something in the documents

## Instructions

1. Run the search script:
   ```bash
   uv run --with 'chromadb,sentence-transformers' plugins/document-review/bin/document-search.py "<query>" [options]
   ```

2. Available options:
   - `--section "4.*"` — filter results by section number pattern
   - `--flag scope` — filter by topic flag (scope, requirements, pricing, timeline, etc.)
   - `--source "filename"` — filter by source document within the archive
   - `--full` — show complete clause body instead of snippet
   - `--top N` — number of results (default: 10)
   - `--json` — output as JSON for further processing

3. Present results to the user with section numbers, source file, and relevance scores.

4. If the user asks a follow-up question about a specific clause, use
   `--section` or `--source` to narrow results, or use `--full` to show the complete text.

## Prerequisites

- Documents must be loaded first (use `/load-document` if `data/documents.db` doesn't exist)

## Constraints

- Always quote the query string to handle spaces
- Results span all loaded documents — note the source file for each result
- The search combines semantic (ChromaDB) and keyword (SQLite) results automatically
- Each search is logged to the audit trail
