#!/usr/bin/env bash

set -euo pipefail

MODE="copy"
CREATE_ALIASES=0
FORCE=0
DEST=""

usage() {
  cat <<'EOF'
Usage: install-vendored-skills.sh [--copy|--link] [--aliases] [--force] [--dest PATH]

Install all vendored skills from .agents/skills into Codex's skills directory.
Optionally create top-level sk-* aliases for the speckit skills.

Options:
  --copy        Copy skills into the destination (default)
  --link        Symlink skills into the destination
  --aliases     Create sk-* symlink aliases for speckit skills
  --force       Replace existing destination directories or symlinks
  --dest PATH   Override destination (default: $CODEX_HOME/skills or ~/.codex/skills)
  --help        Show this help text
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --copy)
      MODE="copy"
      ;;
    --link)
      MODE="link"
      ;;
    --aliases)
      CREATE_ALIASES=1
      ;;
    --force)
      FORCE=1
      ;;
    --dest)
      shift
      DEST="${1:-}"
      if [[ -z "$DEST" ]]; then
        echo "error: --dest requires a value" >&2
        exit 1
      fi
      ;;
    --help|-h)
      usage
      exit 0
      ;;
    *)
      echo "error: unknown option: $1" >&2
      usage >&2
      exit 1
      ;;
  esac
  shift
done

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"
SOURCE_ROOT="${REPO_ROOT}/.agents/skills"
DEST_ROOT="${DEST:-${CODEX_HOME:-$HOME/.codex}/skills}"

if [[ ! -d "$SOURCE_ROOT" ]]; then
  echo "error: source skill directory not found: $SOURCE_ROOT" >&2
  exit 1
fi

mkdir -p "$DEST_ROOT"

installed=0
skipped=0
aliases_installed=0
aliases_skipped=0

for skill_dir in "$SOURCE_ROOT"/*; do
  [[ -d "$skill_dir" ]] || continue

  skill_name="$(basename "$skill_dir")"
  target="${DEST_ROOT}/${skill_name}"

  if [[ -e "$target" || -L "$target" ]]; then
    if [[ "$FORCE" -eq 1 ]]; then
      rm -rf "$target"
    else
      echo "skip  ${skill_name} (already exists at ${target})"
      skipped=$((skipped + 1))
      continue
    fi
  fi

  if [[ "$MODE" == "link" ]]; then
    ln -s "$skill_dir" "$target"
    echo "link  ${skill_name} -> ${target}"
  else
    cp -R "$skill_dir" "$target"
    echo "copy  ${skill_name} -> ${target}"
  fi

  installed=$((installed + 1))
done

create_alias() {
  local alias_name="$1"
  local target_name="$2"
  local alias_target="${DEST_ROOT}/${alias_name}"
  local skill_target="${DEST_ROOT}/${target_name}"

  if [[ ! -e "$skill_target" && ! -L "$skill_target" ]]; then
    echo "skip  ${alias_name} (missing target ${skill_target})"
    aliases_skipped=$((aliases_skipped + 1))
    return
  fi

  if [[ -e "$alias_target" || -L "$alias_target" ]]; then
    if [[ "$FORCE" -eq 1 ]]; then
      rm -rf "$alias_target"
    else
      echo "skip  ${alias_name} (already exists at ${alias_target})"
      aliases_skipped=$((aliases_skipped + 1))
      return
    fi
  fi

  ln -s "$skill_target" "$alias_target"
  echo "alias ${alias_name} -> ${skill_target}"
  aliases_installed=$((aliases_installed + 1))
}

if [[ "$CREATE_ALIASES" -eq 1 ]]; then
  create_alias sk-spec speckit-specify
  create_alias sk-clarify speckit-clarify
  create_alias sk-plan speckit-plan
  create_alias sk-tasks speckit-tasks
  create_alias sk-impl speckit-implement
  create_alias sk-analyze speckit-analyze
  create_alias sk-check speckit-checklist
  create_alias sk-issues speckit-taskstoissues
  create_alias sk-constitution speckit-constitution
fi

echo
echo "Installed: ${installed}"
echo "Skipped:   ${skipped}"
if [[ "$CREATE_ALIASES" -eq 1 ]]; then
  echo "Aliases installed: ${aliases_installed}"
  echo "Aliases skipped:   ${aliases_skipped}"
fi
echo "Destination: ${DEST_ROOT}"
