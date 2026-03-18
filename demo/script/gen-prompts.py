#!/usr/bin/env python3
"""Parse terminal.md and generate prompts.json for the /atai navigator.

Usage:
    python3 script/gen-prompts.py [script/terminal.md] [script/prompts.json]
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

DEMO_DIR = Path(__file__).resolve().parent.parent
DEFAULT_INPUT = DEMO_DIR / "script" / "terminal.md"
DEFAULT_OUTPUT = DEMO_DIR / "script" / "prompts.json"

# Map known prompt prefixes to their run commands
RUN_MAP = {
    "/load-document": "uv run .agents/bin/document-load.py",
    "/search-document": "uv run .agents/bin/document-search.py",
    "/eval-document": "uv run --with 'chromadb,sentence-transformers' .agents/bin/document-eval.py",
    "/audit-document": 'sqlite3 -header -column data/documents.db "SELECT id, timestamp, action, actor, detail FROM audit_log ORDER BY id"',
    "/cowork-review": "uv run --with 'pymupdf,python-docx,openpyxl,chromadb,sentence-transformers' .agents/bin/document-pipeline.py --skip-load",
}

# Map !shortcut commands to their run commands
BANG_MAP = {
    "!bitrot": "uv run .agents/bin/bitrot-simulator.py",
}


def classify_prompt(text: str) -> tuple[str, str | None]:
    """Return (type, run_command) for a prompt."""
    stripped = text.strip()

    # Bang commands (!bitrot, etc.)
    for prefix, base_cmd in BANG_MAP.items():
        if stripped.startswith(prefix):
            args = stripped[len(prefix):].strip()
            return ("script", f"{base_cmd} {args}".strip())

    # Skill/script invocations
    for prefix, base_cmd in RUN_MAP.items():
        if stripped.startswith(prefix):
            raw_args = stripped[len(prefix):].strip()
            if prefix == "/audit-document":
                return ("script", base_cmd)
            elif prefix == "/cowork-review":
                return ("script+assess", base_cmd)
            elif prefix in ("/eval-document",):
                clean_args = raw_args.replace("--adversarial", "").strip()
                if "--adversarial" in raw_args:
                    return ("script+assess", f"{base_cmd} {clean_args}".strip())
                return ("script+assess", f"{base_cmd} {clean_args}".strip())
            else:
                # Quote args that contain spaces and aren't already quoted
                if " " in raw_args and not raw_args.startswith('"'):
                    raw_args = f'"{raw_args.strip(chr(34))}"'
                return ("script", f"{base_cmd} {raw_args}".strip())

    # File references
    if stripped.startswith("@assets/"):
        filepath = stripped.split("\n")[0].lstrip("@").strip()
        if "compare" in stripped.lower():
            return ("file+compare", f"read {filepath}")
        return ("file", f"read {filepath}")

    # Agent references
    if "agent" in stripped.lower() and ".agents/" in stripped:
        match = re.search(r'\(\.agents/([^)]+)\)', stripped)
        if match:
            return ("agent", f"read .agents/{match.group(1)}")

    return ("freeform", None)


def parse_terminal_md(path: Path) -> list[dict]:
    """Parse terminal.md into a list of prompt entries."""
    text = path.read_text()
    prompts = []
    num = 0

    # Find all step sections
    step_pattern = re.compile(
        r'^## (?:Step (\S+)|If Time Permits\s*—\s*Step (\S+):?)\s*—?\s*(.+?)(?:\s*\(~[\d:]+\))?\s*$',
        re.MULTILINE
    )

    sections = []
    for m in step_pattern.finditer(text):
        step_num = m.group(1) or m.group(2)
        title = m.group(3).strip().rstrip(")")
        title = re.sub(r'\(~[\d:]+\)', '', title).strip()
        start = m.end()
        sections.append((step_num, title, start))

    for i, (step_num, title, start) in enumerate(sections):
        end = sections[i + 1][2] if i + 1 < len(sections) else len(text)
        section_text = text[start:end]

        # Find fenced code blocks
        code_blocks = re.findall(r'```\n(.*?)```', section_text, re.DOTALL)

        is_optional = "if time permits" in text[max(0, start - 200):start].lower()

        if not code_blocks:
            # Talk/slide step
            num += 1
            entry = {
                "num": num,
                "step": step_num,
                "title": title,
                "prompt": f"(talk) {title}",
                "type": "talk",
                "run": None,
            }
            if is_optional:
                entry["optional"] = True
            prompts.append(entry)
            continue

        substep = 0
        for block in code_blocks:
            block = block.strip()
            if not block:
                continue

            num += 1
            substep += 1
            step_label = f"{step_num}.{substep}" if len(code_blocks) > 1 else step_num
            prompt_type, run_cmd = classify_prompt(block)

            # Generate subtitle for multi-block steps
            if len(code_blocks) > 1 and substep > 1:
                subtitle = f"{title} ({substep})"
            else:
                subtitle = title

            entry = {
                "num": num,
                "step": step_label,
                "title": subtitle,
                "prompt": block,
                "type": prompt_type,
                "run": run_cmd,
            }
            if is_optional:
                entry["optional"] = True
            prompts.append(entry)

    return prompts


def main():
    input_path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_INPUT
    output_path = Path(sys.argv[2]) if len(sys.argv) > 2 else DEFAULT_OUTPUT

    if not input_path.exists():
        print(f"Input not found: {input_path}", file=sys.stderr)
        sys.exit(1)

    prompts = parse_terminal_md(input_path)

    output_path.write_text(json.dumps(prompts, indent=2) + "\n")

    print(f"Generated {len(prompts)} prompts → {output_path}", file=sys.stderr)
    for p in prompts:
        opt = " [optional]" if p.get("optional") else ""
        print(f"  #{p['num']:2d}  Step {p['step']:<6s}  {p['type']:<14s}  "
              f"{p['prompt'][:55]}...{opt}", file=sys.stderr)


if __name__ == "__main__":
    main()
