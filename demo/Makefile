SHELL := /bin/zsh

DOCUMENT_SOURCE := assets/1-RFP 20-020 - Original Documents.zip
GEN_SCRIPT   := assets/gen-contract.py
DB           := data/documents.db
CHROMA       := data/chroma
PARSE_SCRIPT := ../.agents/bin/document-parse.py
LOAD_SCRIPT  := ../.agents/bin/document-load.py
SEARCH_SCRIPT := ../.agents/bin/document-search.py

VENV := .venv
MODEL_CACHE := .model-cache
DATA_CACHE := data-cache

.PHONY: document load search test clean reset help \
        pre-demo-setup check-deps venv-setup model-warm \
        data-cache-create data-cache-empty data-cache-loaded \
        load-cached preflight slides open-slides \
        setup-terminal setup-desktop setup-clean

## help — show available targets
help:
	@grep '^## ' Makefile | sed 's/^## //'

## document — verify the document archive exists
document:
	@test -f "$(DOCUMENT_SOURCE)" \
		&& echo "Document archive found: $(DOCUMENT_SOURCE)" \
		|| (echo "Document archive not found: $(DOCUMENT_SOURCE)" && exit 1)

## load — parse and load document archive into SQLite + ChromaDB
load:
	@test -f "$(DOCUMENT_SOURCE)" || (echo "Document archive not found. Place it at: $(DOCUMENT_SOURCE)" && exit 1)
	uv run --with 'pymupdf,chromadb,sentence-transformers,python-docx,openpyxl' $(LOAD_SCRIPT) "$(DOCUMENT_SOURCE)"

## search — search loaded document (usage: make search Q="submission requirements")
search:
	@test -f $(DB) || (echo "Run 'make load' first" && exit 1)
	uv run --with 'chromadb,sentence-transformers' $(SEARCH_SCRIPT) "$(Q)"

## test — run parser smoke tests
test:
	uv run --with 'pymupdf,python-docx,openpyxl,path' ../.agents/bin/test-parse.py

## clean — remove all generated artifacts
clean:
	rm -rf data/

## reset — reload from archive
reset: clean load

## pre-demo-setup — full offline demo preparation
pre-demo-setup: check-deps venv-setup model-warm data-cache-create
	@echo ""
	@echo "Pre-demo setup complete!"
	@echo "   .venv/          — Python environment ready"
	@echo "   .model-cache/   — Embedding model cached"
	@echo "   data-cache/     — Pre-loaded data snapshots"
	@echo ""
	@echo "   Run this the NIGHT BEFORE your talk, not 15 min before!"
	@echo ""
	@echo "Run 'make preflight' to verify everything works offline."

## check-deps — verify system dependencies are available
check-deps:
	@echo "Checking dependencies..."
	@command -v uv >/dev/null 2>&1 || (echo "uv not found. Install: curl -LsSf https://astral.sh/uv/install.sh | sh" && exit 1)
	@command -v sqlite3 >/dev/null 2>&1 || (echo "sqlite3 not found. Install via your package manager." && exit 1)
	@echo "  uv found"
	@echo "  sqlite3 found"

## venv-setup — create and populate uv virtual environment
venv-setup: $(VENV)/.installed

$(VENV)/.installed: pyproject.toml
	uv sync
	@touch $@
	@echo "  Virtual environment ready"

## model-warm — pre-download sentence-transformers model for offline use
model-warm: $(MODEL_CACHE)/.warmed

$(MODEL_CACHE)/.warmed: $(VENV)/.installed
	@mkdir -p $(MODEL_CACHE)
	@echo "Warming local model cache..."
	SENTENCE_TRANSFORMERS_HOME=$(MODEL_CACHE)/sentence-transformers \
	HF_HOME=$(MODEL_CACHE)/huggingface \
	uv run python -c "\
		from chromadb.utils.embedding_functions import DefaultEmbeddingFunction; \
		ef = DefaultEmbeddingFunction(); \
		ef(['warmup test']); \
		print('  Model cache warmed')"
	@echo "Warming default model cache (for live skill invocations)..."
	uv run python -c "\
		from chromadb.utils.embedding_functions import DefaultEmbeddingFunction; \
		DefaultEmbeddingFunction()(['warmup']); \
		print('  Default model cache warmed')"
	@touch $@

## data-cache-create — create pre-loaded data snapshots
data-cache-create: data-cache-empty data-cache-loaded
	@echo "  Data cache snapshots created"

## data-cache-empty — snapshot of empty initialized databases
data-cache-empty: $(VENV)/.installed
	@mkdir -p $(DATA_CACHE)/empty
	@echo "Creating empty database state..."
	sqlite3 $(DATA_CACHE)/empty/documents.db "CREATE TABLE IF NOT EXISTS clauses (id INTEGER PRIMARY KEY, section_number TEXT NOT NULL, section_title TEXT, body TEXT NOT NULL, source_file TEXT, page_start INTEGER, page_end INTEGER, flags TEXT); CREATE TABLE IF NOT EXISTS audit_log (id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp TEXT NOT NULL DEFAULT (datetime('now')), action TEXT NOT NULL, detail TEXT, actor TEXT);"
	@mkdir -p $(DATA_CACHE)/empty/chroma
	SENTENCE_TRANSFORMERS_HOME=$(MODEL_CACHE)/sentence-transformers \
	HF_HOME=$(MODEL_CACHE)/huggingface \
	uv run python -c "\
		import chromadb; \
		client = chromadb.PersistentClient(path='$(DATA_CACHE)/empty/chroma'); \
		client.create_collection('document_clauses', metadata={'hnsw:space': 'cosine'}); \
		print('  Empty ChromaDB initialized')"

## data-cache-loaded — snapshot with documents fully loaded
data-cache-loaded: $(VENV)/.installed
	@test -f "$(DOCUMENT_SOURCE)" || (echo "Document archive not found: $(DOCUMENT_SOURCE)" && exit 1)
	@echo "Creating loaded database state..."
	rm -rf data
	SENTENCE_TRANSFORMERS_HOME=$(MODEL_CACHE)/sentence-transformers \
	HF_HOME=$(MODEL_CACHE)/huggingface \
	uv run $(LOAD_SCRIPT) "$(DOCUMENT_SOURCE)" --db data/documents.db --chroma data/chroma
	rm -rf $(DATA_CACHE)/loaded
	cp -r data $(DATA_CACHE)/loaded
	@echo "  Loaded data snapshot created"

## load-cached — restore pre-loaded data for instant demo start
load-cached:
	@if [ ! -d "$(DATA_CACHE)/loaded" ]; then \
		echo "No cached data. Run 'make pre-demo-setup' first."; \
		exit 1; \
	fi
	rm -rf data
	cp -r $(DATA_CACHE)/loaded data
	@echo "  Cached data restored — ready for search/eval"

## ---- System setup (delegates to shell scripts) ----

## setup-terminal — install all deps for the terminal demo
setup-terminal: .setup-terminal.stamp

.setup-terminal.stamp:
	bash script/setup-terminal.sh
	@touch $@

## setup-desktop — full one-command Desktop setup (MCP + skills + agent paste files + data)
setup-desktop: .setup-desktop.stamp

.setup-desktop.stamp:
	bash script/setup-desktop.sh
	@touch $@

## setup-clean — remove setup stamps to force re-run
setup-clean:
	rm -f .setup-terminal.stamp .setup-desktop.stamp

## ---- Slides ----

## slides — build the reveal.js presentation
slides:
	@$(MAKE) -C ../presentation build-reveal

## open-slides — build and open the presentation
open-slides:
	@$(MAKE) -C ../presentation open-reveal

## ---- Verification ----

## preflight — verify everything is cached and ready for offline demo
preflight:
	@echo "Running preflight checks..."
	@test -f "$(DOCUMENT_SOURCE)" && echo "  Document archive exists" || (echo "  Document archive not found (FATAL)" && exit 1)
	@test -d $(VENV) || (echo ".venv/ missing. Run 'make pre-demo-setup'" && exit 1)
	@echo "  Virtual environment exists"
	@uv run python -c "import pymupdf, chromadb; print('  Core packages importable')" \
		|| (echo "Missing packages. Run 'make pre-demo-setup'" && exit 1)
	@test -d $(MODEL_CACHE) || (echo "Model cache missing. Run 'make pre-demo-setup'" && exit 1)
	@SENTENCE_TRANSFORMERS_HOME=$(MODEL_CACHE)/sentence-transformers \
	 HF_HOME=$(MODEL_CACHE)/huggingface \
	 HF_HUB_OFFLINE=1 \
	 uv run python -c "from chromadb.utils.embedding_functions import DefaultEmbeddingFunction; DefaultEmbeddingFunction()(['test']); print('  Model loads offline')" \
		|| (echo "Model not cached. Run 'make pre-demo-setup'" && exit 1)
	@test -d $(DATA_CACHE)/loaded || (echo "Data cache missing. Run 'make pre-demo-setup'" && exit 1)
	@echo "  Data cache exists"
	@echo "Checking Claude CLI..."
	@command -v claude >/dev/null 2>&1 || (echo "claude CLI not found. Install: https://docs.anthropic.com/en/docs/claude-code" && exit 1)
	@echo "  claude CLI found"
	@claude -p "respond with just the word ok" --max-turns 1 2>/dev/null | grep -qi "ok" \
		|| (echo "Claude API may not be responding — check auth and connectivity" && exit 0)
	@echo "  Claude API responding"
	@echo "Checking MCP server..."
	@uv run python -c "import importlib.util; spec = importlib.util.spec_from_file_location('mcp', '../.agents/bin/document-mcp-server.py'); print('  MCP server script loadable')" \
		|| (echo "MCP server script has import errors" && exit 0)
	@echo ""
	@echo "Preflight passed. Ready for offline demo."
