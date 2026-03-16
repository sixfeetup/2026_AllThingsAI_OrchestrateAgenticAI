SHELL := /bin/zsh

CONTRACT_PDF := assets/contracts/bigco-msa.pdf
GEN_SCRIPT   := assets/gen-contract.py
DB           := data/contracts.db
CHROMA       := data/chroma
PARSE_SCRIPT := ../.agents/bin/contract-parse.py
LOAD_SCRIPT  := ../.agents/bin/contract-load.py
SEARCH_SCRIPT := ../.agents/bin/contract-search.py

.PHONY: contract load search test clean reset help

## help — show available targets
help:
	@grep '^## ' Makefile | sed 's/^## //'

## contract — generate the fake contract PDF with planted issues
contract: $(CONTRACT_PDF)

$(CONTRACT_PDF): $(GEN_SCRIPT)
	uv run --with fpdf2 $(GEN_SCRIPT) $(CONTRACT_PDF)

## load — parse and load contract into SQLite + ChromaDB
load: $(CONTRACT_PDF)
	uv run --with 'pymupdf,chromadb,sentence-transformers' $(LOAD_SCRIPT) $(CONTRACT_PDF)

## search — search loaded contract (usage: make search Q="intellectual property")
search:
	@test -f $(DB) || (echo "Run 'make load' first" && exit 1)
	uv run --with 'chromadb,sentence-transformers' $(SEARCH_SCRIPT) "$(Q)"

## test — run parser smoke tests
test: $(CONTRACT_PDF)
	uv run --with pymupdf ../.agents/bin/test-parse.py

## clean — remove all generated artifacts
clean:
	rm -f $(CONTRACT_PDF)
	rm -rf data/

## reset — regenerate PDF and reload
reset: clean contract load
