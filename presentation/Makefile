SHELL   := /bin/zsh
CONTENT := $(sort $(wildcard content/*.md))
OUTPUT  := output/deck.html
DIST    := ../dist/deck.html
BUILD   := build.py
IMAGES  := ../images

# Pass --root to build.py when ROOT is set (e.g. make build ROOT=/some/path)
BUILD_FLAGS := $(if $(ROOT),--root $(ROOT))

.PHONY: build open clean reset-content watch list deploy serve

## build — render content/*.md into output/deck.html + dist/deck.html
build: $(OUTPUT)

$(OUTPUT): $(CONTENT) $(BUILD)
	uv run $(BUILD) $(BUILD_FLAGS)

## open — build and open in browser
open: $(OUTPUT)
	open $(OUTPUT)

## clean — remove built output
clean:
	rm -f $(OUTPUT) $(DIST)

## reset-content — remove only committed content/*.md files (safe for uncommitted work)
reset-content:
	@echo "Removing committed content files..."
	cd .. && git ls-files --error-unmatch presentation/content/*.md 2>/dev/null | \
		xargs -I{} sh -c 'git diff --quiet -- "$$1" && git diff --cached --quiet -- "$$1" && rm "$$1" && echo "  rm $$1"' _ {}
	@echo "Done. Unmodified committed files removed; dirty/untracked files preserved."

## deploy — build, copy referenced images, commit and push gh-pages
deploy: $(OUTPUT)
	@echo "Syncing referenced images to dist/..."
	mkdir -p ../dist/images
	grep -o 'src="images/[^"]*"' $(DIST) | sed 's/src="images\///;s/"//' | sort -u | \
		while read f; do cp "$(IMAGES)/$$f" "../dist/images/$$f"; done
	@echo "Committing to gh-pages..."
	cd ../dist && \
		git add -A && \
		(git diff --cached --quiet || \
		git commit -m "deck: $$(date +%Y%m%d-%H%M)") && \
		git push origin gh-pages
	@echo "Deployed to gh-pages."

## serve — local preview server from dist/
serve: $(OUTPUT)
	@echo "Serving at http://localhost:8000"
	cd ../dist && python3 -m http.server 8000

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
