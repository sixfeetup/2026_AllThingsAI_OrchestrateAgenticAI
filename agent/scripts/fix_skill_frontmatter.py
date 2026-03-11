#!/usr/bin/env python3
"""
Repair local Codex SKILL.md files that are missing required YAML frontmatter.

What this does:
- reads a list of target SKILL.md files
- detects whether a file already starts with YAML frontmatter
- if not, prepends a minimal frontmatter block with `name` and `description`

How to make this more general later:
- discover skills automatically from a directory instead of using a fixed list
- infer richer metadata from the markdown body or a sidecar config file
- validate the resulting frontmatter against a schema before writing changes
"""

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass

from path import Path


@dataclass(frozen=True)
class SkillMetadata:
    path: Path
    name: str
    description: str


DEFAULT_SKILLS = [
    SkillMetadata(
        path=Path("/Users/whit/.codex/skills/podman/SKILL.md"),
        name="podman",
        description="Use Podman instead of Docker for container operations on this machine.",
    ),
    SkillMetadata(
        path=Path("/Users/whit/.codex/skills/say/SKILL.md"),
        name="say",
        description="Use macOS say for audible notifications when user attention is needed.",
    ),
    SkillMetadata(
        path=Path("/Users/whit/.codex/skills/k8s/SKILL.md"),
        name="k8s",
        description="Apply the project's standard Kubernetes and kind operating patterns.",
    ),
    SkillMetadata(
        path=Path("/Users/whit/.codex/skills/jq/SKILL.md"),
        name="jq",
        description="Use jq and yq for structured JSON and YAML processing.",
    ),
    SkillMetadata(
        path=Path("/Users/whit/.codex/skills/uv-python/SKILL.md"),
        name="uv-python",
        description="Use uv for Python environments, dependencies, and command execution.",
    ),
]


def has_frontmatter(text: str) -> bool:
    return text.startswith("---\n") or text == "---" or text.startswith("---\r\n")


def build_frontmatter(name: str, description: str) -> str:
    return (
        "---\n"
        f"name: {name}\n"
        f"description: {description}\n"
        "---\n\n"
    )


def repair_skill(skill: SkillMetadata, dry_run: bool) -> str:
    if not skill.path.exists():
        return f"missing {skill.path}"

    content = skill.path.read_text()
    if has_frontmatter(content):
        return f"ok      {skill.path}"

    updated = build_frontmatter(skill.name, skill.description) + content
    if not dry_run:
        skill.path.write_text(updated)

    return f"fixed   {skill.path}"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Add minimal YAML frontmatter to selected local Codex skill files."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Report what would change without modifying files.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    for skill in DEFAULT_SKILLS:
        print(repair_skill(skill, dry_run=args.dry_run))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
