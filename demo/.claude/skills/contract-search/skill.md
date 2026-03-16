# contract-search

Search loaded contract clauses using semantic and keyword search.

## Triggers

- `/search-contract <query>`
- User asks to "search", "find", or "look up" something in the contract

## Instructions

1. Run the search script:
   ```bash
   uv run --with 'chromadb,sentence-transformers' .agents/bin/contract-search.py "<query>" [options]
   ```

2. Available options:
   - `--section "4.*"` — filter results by section number pattern
   - `--flag ip` — filter by topic flag (ip, payment, termination, staffing, etc.)
   - `--full` — show complete clause body instead of snippet
   - `--top N` — number of results (default: 10)
   - `--json` — output as JSON for further processing

3. Present results to the user with section numbers and relevance scores.

4. If the user asks a follow-up question about a specific clause, use
   `--section` to narrow results, or use `--full` to show the complete text.

## Prerequisites

- Contract must be loaded first (use `/load-contract` if `demo/data/contracts.db` doesn't exist)

## Constraints

- Always quote the query string to handle spaces
- The search combines semantic (ChromaDB) and keyword (SQLite) results automatically
- Each search is logged to the audit trail
