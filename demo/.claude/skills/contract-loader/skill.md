# contract-loader

Parse a contract PDF and load it into SQLite + ChromaDB for search and analysis.

## Triggers

- `/load-contract <path-to-pdf>`
- User asks to "load", "ingest", or "import" a contract

## Instructions

1. Run the parser to extract clauses from the PDF:
   ```bash
   uv run --with pymupdf .agents/bin/contract-parse.py <path> -o /tmp/parsed-clauses.json
   ```

2. Run the loader to populate both data stores:
   ```bash
   uv run --with 'pymupdf,chromadb,sentence-transformers' .agents/bin/contract-load.py <path>
   ```

3. Report results to the user:
   - Number of clauses extracted
   - Number of pages covered
   - Any parse warnings
   - Confirm both SQLite (`demo/data/contracts.db`) and ChromaDB (`demo/data/chroma/`) are populated

## Constraints

- Always use `uv run --with` to manage dependencies — never `pip install`
- The data/ directory is created automatically; do not commit it
- If the PDF path is relative, resolve it from the current working directory
- If loading fails, check that the PDF exists and is readable before retrying
