#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Run the full document review pipeline: load, eval, audit.

Usage:
    uv run document-pipeline.py [archive] [--criteria FILE ...] [--db PATH] [--chroma PATH]

Chains load → eval (per criteria file) → audit summary in one command.
The LLM applies judgment to the evidence output; this script gathers it all.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sqlite3
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
SKILLS_DIR = SCRIPT_DIR.parent
PLUGIN_DIR = SKILLS_DIR.parent


def _data_dir() -> Path:
    """Resolve the data directory: CLAUDE_PLUGIN_DATA env var, or local data/."""
    env = os.environ.get("CLAUDE_PLUGIN_DATA") or os.environ.get("DOCUMENT_REVIEW_DATA")
    if env:
        return Path(env)
    return PLUGIN_DIR / "data"


DEFAULT_ARCHIVE = PLUGIN_DIR / "assets" / "1-RFP 20-020 - Original Documents.zip"
DEFAULT_DB = _data_dir() / "documents.db"
DEFAULT_CHROMA = _data_dir() / "chroma"
DEFAULT_CRITERIA = [
    PLUGIN_DIR / "assets" / "criteria" / "ip-and-ownership.md",
    PLUGIN_DIR / "assets" / "criteria" / "general-red-flags.md",
]

LOAD_SCRIPT = SKILLS_DIR / "load-document" / "document-load.py"
EVAL_SCRIPT = SKILLS_DIR / "eval-document" / "document-eval.py"


def banner(stage: int, total: int, title: str):
    print(f"\n{'='*60}", file=sys.stderr)
    print(f"  Stage {stage}/{total} — {title}", file=sys.stderr)
    print(f"{'='*60}\n", file=sys.stderr)


def run_load(archive: Path, db: Path, chroma: Path) -> bool:
    """Run the load script."""
    cmd = [
        "uv", "run", str(LOAD_SCRIPT), str(archive),
        "--db", str(db), "--chroma", str(chroma),
    ]
    result = subprocess.run(cmd, capture_output=False)
    return result.returncode == 0


def run_eval(criteria: Path, db: Path, chroma: Path) -> str | None:
    """Run the eval script, return its stdout."""
    cmd = [
        "uv", "run", str(EVAL_SCRIPT), str(criteria),
        "--db", str(db), "--chroma", str(chroma),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"  Eval failed: {result.stderr}", file=sys.stderr)
        return None
    # Print progress to stderr
    if result.stderr:
        print(result.stderr, file=sys.stderr, end="")
    return result.stdout


def get_audit_summary(db: Path) -> str:
    """Get audit trail summary."""
    if not db.exists():
        return "No audit data."

    conn = sqlite3.connect(str(db))
    total = conn.execute("SELECT COUNT(*) FROM audit_log").fetchone()[0]
    by_action = conn.execute(
        "SELECT action, COUNT(*) as c FROM audit_log GROUP BY action ORDER BY c DESC"
    ).fetchall()

    recent = conn.execute(
        "SELECT id, timestamp, action, actor, detail FROM audit_log ORDER BY id DESC LIMIT 10"
    ).fetchall()
    conn.close()

    lines = [f"**{total} total entries**\n"]
    lines.append("| Action | Count |")
    lines.append("|--------|-------|")
    for action, count in by_action:
        lines.append(f"| {action.upper()} | {count} |")

    lines.append("\n### Recent Entries\n")
    lines.append("| # | Time | Action | Actor | Detail |")
    lines.append("|---|------|--------|-------|--------|")
    for row in reversed(recent):
        id_, ts, action, actor, detail_json = row
        time_part = ts.split(" ")[1] if " " in ts else ts
        # Parse detail JSON for summary
        try:
            detail = json.loads(detail_json)
            if action == "load":
                summary = f"{detail.get('clause_count', '?')} clauses from {detail.get('document_count', '?')} docs"
            elif action == "search":
                summary = f"\"{detail.get('query', '?')[:40]}\" → {detail.get('results', '?')} hits"
            elif action == "eval":
                summary = f"{detail.get('criteria_file', '?')} ({detail.get('criteria_count', '?')} criteria)"
            else:
                summary = str(detail)[:50]
        except (json.JSONDecodeError, TypeError):
            summary = str(detail_json)[:50] if detail_json else "—"
        lines.append(f"| {id_} | {time_part} | {action.upper()} | {actor} | {summary} |")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Full document review pipeline",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("archive", nargs="?", default=str(DEFAULT_ARCHIVE),
                        help=f"Document archive (default: {DEFAULT_ARCHIVE.name})")
    parser.add_argument("--criteria", "-c", nargs="*",
                        help="Criteria files (default: ip-and-ownership.md + general-red-flags.md)")
    parser.add_argument("--db", default=str(DEFAULT_DB))
    parser.add_argument("--chroma", default=str(DEFAULT_CHROMA))
    parser.add_argument("--skip-load", action="store_true",
                        help="Skip load step (data already loaded)")
    args = parser.parse_args()

    db = Path(args.db)
    chroma = Path(args.chroma)
    archive = Path(args.archive)

    criteria_files = [Path(c) for c in args.criteria] if args.criteria else DEFAULT_CRITERIA
    total_stages = (0 if args.skip_load else 1) + len(criteria_files) + 1  # +1 for audit

    stage = 0

    # --- Load ---
    if not args.skip_load:
        stage += 1
        banner(stage, total_stages, "Load Documents")
        if not archive.exists():
            print(f"Archive not found: {archive}", file=sys.stderr)
            sys.exit(1)
        ok = run_load(archive, db, chroma)
        if not ok:
            print("Load failed.", file=sys.stderr)
            sys.exit(1)
    else:
        print("Skipping load (--skip-load).", file=sys.stderr)

    # --- Evals ---
    all_evidence = []
    for criteria_path in criteria_files:
        stage += 1
        banner(stage, total_stages, f"Evaluate: {criteria_path.name}")
        if not criteria_path.exists():
            print(f"  Criteria file not found: {criteria_path}", file=sys.stderr)
            continue
        output = run_eval(criteria_path, db, chroma)
        if output:
            all_evidence.append(output)

    # --- Audit ---
    stage += 1
    banner(stage, total_stages, "Audit Trail")
    audit_summary = get_audit_summary(db)

    # --- Compose output ---
    print("# Document Review Pipeline — Evidence Report\n")
    print(f"**Archive:** {archive.name}")
    print(f"**Criteria files:** {', '.join(c.name for c in criteria_files)}")
    print()

    for evidence_block in all_evidence:
        print(evidence_block)
        print()

    print("---")
    print("## Audit Trail\n")
    print(audit_summary)

    print(f"\nPipeline complete. {len(all_evidence)} eval(s), "
          f"{len(criteria_files)} criteria file(s).", file=sys.stderr)


if __name__ == "__main__":
    main()
