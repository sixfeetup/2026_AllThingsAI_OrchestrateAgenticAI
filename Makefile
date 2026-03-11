SHELL := /bin/zsh

.PHONY: install-vendored-skills link-vendored-skills install-speckit-aliases

## install-vendored-skills — copy vendored repo skills into Codex's local skills dir
install-vendored-skills:
	./demo/scripts/install-vendored-skills.sh --copy

## link-vendored-skills — symlink vendored repo skills into Codex's local skills dir
link-vendored-skills:
	./demo/scripts/install-vendored-skills.sh --link

## install-speckit-aliases — create top-level sk-* symlink aliases for speckit skills
install-speckit-aliases:
	./demo/scripts/install-vendored-skills.sh --aliases
