# document-loader

Extract, parse, and load documents from a ZIP archive (or single file) into SQLite + ChromaDB.

## Triggers

- `/load-document <path-to-archive-or-file>`
- User asks to "load", "ingest", or "import" a document or archive

## Instructions

1. If the path is a ZIP archive, extract all documents first.

2. Run the loader to parse and populate both data stores:
   ```bash
   uv run --with 'pymupdf,chromadb,sentence-transformers,python-docx,openpyxl' plugins/document-review/bin/document-load.py "<path>"
   ```

3. Report results to the user:
   - Number of documents extracted (if ZIP)
   - Number of clauses/sections parsed
   - Format breakdown (PDFs, DOCX, XLSX, etc.)
   - Any parse warnings or skipped files
   - Confirm both SQLite (`demo/data/documents.db`) and ChromaDB (`demo/data/chroma/`) are populated

## Default path

If no path is given, use: `assets/1-RFP 20-020 - Original Documents.zip`

## Constraints

- Always use `uv run --with` to manage dependencies — never `pip install`
- The data/ directory is created automatically; do not commit it
- If the path is relative, resolve it from the current working directory
- Quote paths with spaces
- If loading fails, check that the archive exists and is readable before retrying
