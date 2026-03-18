#!/usr/bin/env python3
"""MCP server exposing document review tools over stdio.

Usage:
    uv run --with 'mcp,pymupdf,python-docx,openpyxl,chromadb,sentence-transformers' document-mcp-server.py

Exposes the contract pipeline (parse, load, search, audit) as MCP tools
so Claude Desktop, Cowork, or any MCP client can drive the review workflow
without needing Claude Code CLI.
"""
from __future__ import annotations

import json
import sqlite3
import subprocess
import sys
from pathlib import Path

from mcp.server.fastmcp import FastMCP

SCRIPT_DIR = Path(__file__).resolve().parent
# From plugins/document-review/bin/ -> repo root is three levels up
DEMO_DIR = SCRIPT_DIR.parent.parent.parent / "demo"
DEFAULT_DB = DEMO_DIR / "data" / "documents.db"
DEFAULT_CHROMA = DEMO_DIR / "data" / "chroma"
PARSE_SCRIPT = SCRIPT_DIR / "document-parse.py"
LOAD_SCRIPT = SCRIPT_DIR / "document-load.py"
SEARCH_SCRIPT = SCRIPT_DIR / "document-search.py"
DEFAULT_DOCUMENT = DEMO_DIR / "assets" / "1-RFP 20-020 - Original Documents.zip"

server = FastMCP(
    "document-review",
    instructions=(
        "Contract review pipeline tools. Use these to parse, load, search, "
        "and audit contract documents. Typical workflow: load a contract PDF, "
        "search for relevant clauses, evaluate against criteria, then review "
        "the audit trail."
    ),
)


@server.tool()
def load_document(document_path: str = "") -> str:
    """Parse a document (PDF, DOCX, XLSX, or ZIP archive) and load clauses into SQLite + ChromaDB.

    Args:
        document_path: Path to the document file or ZIP archive. Defaults to the demo RFP archive.
    """
    if not document_path:
        document_path = str(DEFAULT_DOCUMENT)
    doc = Path(document_path)
    if not doc.exists():
        return f"Error: document not found at {document_path}"
    result = subprocess.run(
        [sys.executable, str(LOAD_SCRIPT), str(doc),
         "--db", str(DEFAULT_DB), "--chroma", str(DEFAULT_CHROMA)],
        capture_output=True, text=True,
    )
    output = result.stderr.strip()
    if result.returncode != 0:
        return f"Error loading document: {output}"
    return f"Document loaded successfully.\n\n{output}"


@server.tool()
def search_document(
    query: str, section: str = "", flag: str = "",
    source: str = "", full: bool = False, top: int = 10,
) -> str:
    """Search loaded document clauses using semantic + keyword search.

    Args:
        query: Search query (e.g. "intellectual property", "termination").
        section: Filter by section number pattern (e.g. "4.*").
        flag: Filter by topic flag (e.g. "ip", "payment").
        source: Filter by source document filename (e.g. "RFP 20-020 Document.pdf").
        full: Show full clause body instead of snippet.
        top: Number of results to return.
    """
    if not DEFAULT_DB.exists():
        return "Error: No contract loaded. Use load_document first."
    cmd = [sys.executable, str(SEARCH_SCRIPT), query,
           "--db", str(DEFAULT_DB), "--chroma", str(DEFAULT_CHROMA),
           "--top", str(top), "--json"]
    if section:
        cmd.extend(["--section", section])
    if flag:
        cmd.extend(["--flag", flag])
    if source:
        cmd.extend(["--source", source])
    if full:
        cmd.append("--full")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        return f"Search error: {result.stderr.strip()}"
    try:
        hits = json.loads(result.stdout)
    except json.JSONDecodeError:
        return result.stdout
    if not hits:
        return f"No results found for: {query}"
    lines = [f"Found {len(hits)} results for: {query}\n"]
    for h in hits:
        sec = h["section_number"]
        title = h.get("section_title", "")
        score = h.get("score", 0)
        source_file = h.get("source_file", "")
        body = h.get("body", "")
        snippet = body if full else body[:200].replace("\n", " ")
        label = f"{title}: {snippet}" if title else snippet
        src_tag = f" [{source_file}]" if source_file else ""
        lines.append(f"  [{sec}]{src_tag} (score: {score:.2f}) {label}")
    return "\n".join(lines)


@server.tool()
def audit_document() -> str:
    """Display the audit trail of all contract analysis actions."""
    if not DEFAULT_DB.exists():
        return "Error: No contract loaded."
    conn = sqlite3.connect(str(DEFAULT_DB))
    conn.row_factory = sqlite3.Row
    rows = conn.execute(
        "SELECT id, timestamp, action, actor, detail "
        "FROM audit_log ORDER BY id"
    ).fetchall()
    conn.close()
    if not rows:
        return "Audit log is empty."
    lines = ["# Audit Trail\n"]
    for row in rows:
        detail = row["detail"] or ""
        try:
            detail = json.dumps(json.loads(detail), indent=2)
        except (json.JSONDecodeError, TypeError):
            pass
        lines.append(
            f"**[{row['id']}]** {row['timestamp']} | "
            f"action={row['action']} | actor={row['actor']}\n"
            f"```json\n{detail}\n```\n"
        )
    return "\n".join(lines)


@server.tool()
def list_criteria_files() -> str:
    """List available criteria files for contract evaluation."""
    criteria_dir = DEMO_DIR / "assets" / "criteria"
    if not criteria_dir.exists():
        return "Error: Criteria directory not found."
    files = sorted(criteria_dir.glob("*.md"))
    if not files:
        return "No criteria files found."
    lines = ["# Available Criteria Files\n"]
    for f in files:
        content = f.read_text()
        headings = [l.strip("# ").strip() for l in content.split("\n") if l.startswith("## ")]
        lines.append(f"**{f.name}** ({len(headings)} criteria)")
        for h in headings:
            lines.append(f"  - {h}")
        lines.append("")
    return "\n".join(lines)


@server.tool()
def get_document_stats() -> str:
    """Get summary statistics about the loaded contract."""
    if not DEFAULT_DB.exists():
        return "Error: No contract loaded."
    conn = sqlite3.connect(str(DEFAULT_DB))
    conn.row_factory = sqlite3.Row
    total = conn.execute("SELECT COUNT(*) as cnt FROM clauses").fetchone()["cnt"]
    pages = conn.execute(
        "SELECT MIN(page_start) as mn, MAX(page_end) as mx FROM clauses"
    ).fetchone()
    rows = conn.execute("SELECT flags FROM clauses WHERE flags IS NOT NULL").fetchall()
    conn.close()
    flag_counts: dict[str, int] = {}
    for row in rows:
        try:
            for flag in json.loads(row["flags"]):
                flag_counts[flag] = flag_counts.get(flag, 0) + 1
        except (json.JSONDecodeError, TypeError):
            pass
    lines = [
        "# Document Statistics\n",
        f"- **Total clauses:** {total}",
        f"- **Pages:** {pages['mn']} to {pages['mx']}",
        "",
        "## Flag Distribution",
    ]
    for flag, count in sorted(flag_counts.items(), key=lambda x: -x[1]):
        lines.append(f"  - {flag}: {count} clauses")
    return "\n".join(lines)


@server.tool()
def read_criteria_file(filename: str) -> str:
    """Read a criteria file's contents.

    Args:
        filename: e.g. "ip-and-ownership.md"
    """
    criteria_dir = DEMO_DIR / "assets" / "criteria"
    filepath = criteria_dir / filename
    if not filepath.exists():
        available = [f.name for f in criteria_dir.glob("*.md")]
        return f"Error: '{filename}' not found. Available: {', '.join(available)}"
    return filepath.read_text()


if __name__ == "__main__":
    server.run(transport="stdio")
