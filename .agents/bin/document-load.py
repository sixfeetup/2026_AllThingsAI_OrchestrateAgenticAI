#!/usr/bin/env python3
"""Load parsed document clauses into SQLite and ChromaDB.

Usage:
    uv run --with 'pymupdf,python-docx,openpyxl,chromadb,sentence-transformers' document-load.py <path> [--db <db-path>] [--chroma <chroma-dir>]

Accepts a single document (PDF/DOCX/XLSX) or a ZIP archive of documents.
Calls document-parse.py internally, then loads results into both stores.
"""
from __future__ import annotations

import argparse
import json
import sqlite3
import subprocess
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

PARSER_SCRIPT = Path(__file__).resolve().parent / "document-parse.py"
DEFAULT_DB = Path(__file__).resolve().parent.parent.parent / "demo" / "data" / "documents.db"
DEFAULT_CHROMA = Path(__file__).resolve().parent.parent.parent / "demo" / "data" / "chroma"


def init_db(db_path: Path) -> sqlite3.Connection:
    """Create tables and return connection."""
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(db_path))
    conn.execute("""
        CREATE TABLE IF NOT EXISTS clauses (
            id             INTEGER PRIMARY KEY,
            section_number TEXT NOT NULL,
            section_title  TEXT,
            body           TEXT NOT NULL,
            source_file    TEXT,
            page_start     INTEGER,
            page_end       INTEGER,
            flags          TEXT
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS audit_log (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL DEFAULT (datetime('now')),
            action    TEXT NOT NULL,
            detail    TEXT,
            actor     TEXT
        )
    """)
    conn.commit()
    return conn


def load_sqlite(conn: sqlite3.Connection, clauses: list[dict], source: str):
    """Load clauses into SQLite, replacing any existing data."""
    conn.execute("DELETE FROM clauses")
    for i, c in enumerate(clauses, 1):
        conn.execute(
            "INSERT INTO clauses (id, section_number, section_title, body, "
            "source_file, page_start, page_end, flags) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (i, c["section_number"], c.get("section_title", ""),
             c["body"], c.get("source_file", ""),
             c["page_start"], c["page_end"],
             json.dumps(c.get("flags", []))),
        )

    # Build format breakdown for audit log
    source_files = set(c.get("source_file", "") for c in clauses)
    source_files.discard("")
    format_counts: Counter[str] = Counter()
    for sf in source_files:
        ext = Path(sf).suffix.lower()
        format_counts[ext] += 1

    conn.execute(
        "INSERT INTO audit_log (action, detail, actor) VALUES (?, ?, ?)",
        ("load", json.dumps({
            "source": source,
            "clause_count": len(clauses),
            "document_count": len(source_files),
            "format_breakdown": dict(format_counts),
            "source_files": sorted(source_files),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }), "document-load"),
    )
    conn.commit()


def load_chroma(chroma_dir: Path, clauses: list[dict]):
    """Load clauses into ChromaDB with sentence-transformer embeddings."""
    import chromadb

    chroma_dir.mkdir(parents=True, exist_ok=True)
    client = chromadb.PersistentClient(path=str(chroma_dir))

    # Delete existing collection if present
    try:
        client.delete_collection("document_clauses")
    except Exception:
        pass

    collection = client.create_collection(
        name="document_clauses",
        metadata={"hnsw:space": "cosine"},
    )

    # Prepare documents — combine title + body for embedding
    ids = []
    documents = []
    metadatas = []
    for i, c in enumerate(clauses):
        if not c["body"].strip():
            continue  # skip empty section headers
        ids.append(str(i))
        title = c.get("section_title", "")
        doc = f"{c['section_number']} {title}\n{c['body']}" if title else f"{c['section_number']}\n{c['body']}"
        documents.append(doc)
        metadatas.append({
            "section_number": c["section_number"],
            "section_title": title,
            "source_file": c.get("source_file", ""),
            "page_start": c["page_start"],
            "page_end": c["page_end"],
            "flags": json.dumps(c.get("flags", [])),
        })

    # ChromaDB handles batching internally
    collection.add(ids=ids, documents=documents, metadatas=metadatas)
    return len(ids)


def main():
    parser = argparse.ArgumentParser(description="Load contract into SQLite + ChromaDB")
    parser.add_argument("input_path", help="Path to document file or ZIP archive")
    parser.add_argument("--db", default=str(DEFAULT_DB),
                        help=f"SQLite database path (default: {DEFAULT_DB})")
    parser.add_argument("--chroma", default=str(DEFAULT_CHROMA),
                        help=f"ChromaDB directory (default: {DEFAULT_CHROMA})")
    args = parser.parse_args()

    input_path = Path(args.input_path)
    if not input_path.exists():
        print(f"Error: file not found: {input_path}", file=sys.stderr)
        sys.exit(1)

    # Parse document(s)
    print(f"Parsing {input_path}...", file=sys.stderr)
    result = subprocess.run(
        [sys.executable, str(PARSER_SCRIPT), str(input_path)],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        print(f"Parse failed: {result.stderr}", file=sys.stderr)
        sys.exit(1)

    # Print parser stderr (progress messages) to our stderr
    if result.stderr:
        print(result.stderr, file=sys.stderr, end="")

    clauses = json.loads(result.stdout)
    print(f"  Parsed {len(clauses)} clauses total", file=sys.stderr)

    # Load into SQLite
    db_path = Path(args.db)
    print(f"Loading into SQLite ({db_path})...", file=sys.stderr)
    conn = init_db(db_path)
    load_sqlite(conn, clauses, str(input_path))
    count = conn.execute("SELECT COUNT(*) FROM clauses").fetchone()[0]
    print(f"  {count} rows in clauses table", file=sys.stderr)
    conn.close()

    # Load into ChromaDB
    chroma_dir = Path(args.chroma)
    print(f"Loading into ChromaDB ({chroma_dir})...", file=sys.stderr)
    embedded = load_chroma(chroma_dir, clauses)
    print(f"  {embedded} documents embedded", file=sys.stderr)

    print("\nDone.", file=sys.stderr)


if __name__ == "__main__":
    main()
