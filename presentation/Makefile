SHELL := /bin/zsh
CONTENT := $(sort $(wildcard content/*.md))
OUTPUT  := output/deck.html
BUILD   := build.py

.PHONY: build open clean watch list

## build — render content/*.md into output/deck.html
build: $(OUTPUT)

$(OUTPUT): $(CONTENT) $(BUILD)
	uv run $(BUILD)

## open — build and open in browser
open: $(OUTPUT)
	open $(OUTPUT)

## clean — remove built output
clean:
	rm -f $(OUTPUT)

## watch — rebuild on content changes (requires fswatch)
watch:
	@echo "Watching content/ for changes..."
	fswatch -o content/ $(BUILD) | xargs -n1 -I{} make build

## list — show slide order
list:
	@for f in content/*.md; do \
		printf "  %s  %s\n" "$$(basename $$f .md)" \
			"$$(head -10 $$f | grep '^# ' | head -1 | sed 's/^# //')"; \
	done
