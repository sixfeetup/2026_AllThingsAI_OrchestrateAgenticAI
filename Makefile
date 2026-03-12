SHELL := /bin/zsh

.PHONY: install-vendored-skills link-vendored-skills install-speckit-aliases codex-local codex-demo

## install-vendored-skills — copy vendored repo skills into Codex's local skills dir
install-vendored-skills:
	./demo/scripts/install-vendored-skills.sh --copy

## link-vendored-skills — symlink vendored repo skills into Codex's local skills dir
link-vendored-skills:
	./demo/scripts/install-vendored-skills.sh --link

## install-speckit-aliases — create top-level sk-* symlink aliases for speckit skills
install-speckit-aliases:
	./demo/scripts/install-vendored-skills.sh --aliases

## codex-local — launch Codex for this repo with Ralph MCP wired in
codex-local:
	./agent/scripts/codex-local-ralph-mcp.sh

## codex-demo — launch Codex in repo-local demo mode
codex-demo:
	./agent/scripts/codex-demo-mode.sh
