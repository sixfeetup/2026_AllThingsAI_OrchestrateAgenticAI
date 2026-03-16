SHELL := /bin/zsh

CONTRACT_PDF := assets/contracts/bigco-msa.pdf
GEN_SCRIPT   := assets/gen-contract.py

.PHONY: contract clean

## contract — generate the fake contract PDF with planted issues
contract: $(CONTRACT_PDF)

$(CONTRACT_PDF): $(GEN_SCRIPT)
	uv run --with fpdf2 $(GEN_SCRIPT) $(CONTRACT_PDF)

## clean — remove generated artifacts
clean:
	rm -f $(CONTRACT_PDF)
