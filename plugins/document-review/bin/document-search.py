#!/usr/bin/env python3
"""Search loaded document clauses via semantic + keyword search.

Usage:
    uv run --with 'chromadb,sentence-transformers' document-search.py <query> [options]

Options:
    --section PATTERN   Filter by section number (e.g. "4.*" or "12.*")
    --flag TAG          Filter by flag (e.g. "ip", "staffing")
    --source FILENAME   Filter by source document filename
    --full              Show full body text instead of snippet
    --top N             Number of results (default: 10)
    --db PATH           SQLite database path
    --chroma PATH       ChromaDB directory path
"""
from __future__ import annotations

import argparse
import fnmatch
import json
import sqlite3
import sys
from pathlib import Path

DEFAULT_DB = Path(__file__).resolve().parent.parent.parent.parent / "demo" / "data" / "documents.db"
DEFAULT_CHROMA = Path(__file__).resolve().parent.parent.parent.parent / "demo" / "data" / "chroma"


def search_chroma(chroma_dir: Path, query: str, top_k: int) -> list[dict]:
    """Semantic search against ChromaDB."""
    import chromadb

    client = chromadb.PersistentClient(path=str(chroma_dir))
    try:
        collection = client.get_collection("document_clauses")
    except Exception:
        return []

    results = collection.query(query_texts=[query], n_results=top_k)

    hits = []
    for i in range(len(results["ids"][0])):
        meta = results["metadatas"][0][i]
        hits.append({
            "section_number": meta["section_number"],
            "section_title": meta.get("section_title", ""),
            "body": results["documents"][0][i],
            "score": 1.0 - (results["distances"][0][i] if results["distances"] else 0),
            "source": "semantic",
            "source_file": meta.get("source_file", ""),
            "page_start": meta.get("page_start", 0),
            "page_end": meta.get("page_end", 0),
            "flags": json.loads(meta.get("flags", "[]")),
        })
    return hits


def search_sqlite(db_path: Path, query: str, top_k: int) -> list[dict]:
    """Keyword search against SQLite."""
    if not db_path.exists():
        return []

    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row

    # Split query into words for LIKE matching
    words = query.lower().split()
    conditions = " AND ".join(
        "(LOWER(body) LIKE ? OR LOWER(section_title) LIKE ?)"
        for _ in words
    )
    params = []
    for w in words:
        like = f"%{w}%"
        params.extend([like, like])

    rows = conn.execute(
        f"SELECT * FROM clauses WHERE {conditions} LIMIT ?",
        params + [top_k * 2],
    ).fetchall()
    conn.close()

    hits = []
    for row in rows:
        # Score based on how many query words appear
        body_lower = row["body"].lower()
        title_lower = (row["section_title"] or "").lower()
        matched = sum(1 for w in words if w in body_lower or w in title_lower)
        score = matched / len(words) * 0.8  # max 0.8 for keyword

        hits.append({
            "section_number": row["section_number"],
            "section_title": row["section_title"] or "",
            "body": row["body"],
            "score": score,
            "source": "keyword",
            "source_file": row["source_file"] or "",
            "page_start": row["page_start"],
            "page_end": row["page_end"],
            "flags": json.loads(row["flags"] or "[]"),
        })
    return hits


def merge_results(semantic: list[dict], keyword: list[dict],
                  top_k: int) -> list[dict]:
    """Merge and deduplicate results, keeping highest score per section+source_file."""
    by_key: dict[str, dict] = {}

    for hit in semantic + keyword:
        key = f"{hit['section_number']}:{hit.get('source_file', '')}"
        if key not in by_key or hit["score"] > by_key[key]["score"]:
            by_key[key] = hit
        elif key in by_key and hit["source"] != by_key[key]["source"]:
            # Boost score when both sources agree
            by_key[key]["score"] = min(1.0, by_key[key]["score"] + 0.1)

    results = sorted(by_key.values(), key=lambda x: x["score"], reverse=True)
    return results[:top_k]


def log_search(db_path: Path, query: str, result_count: int):
    """Log search to audit trail."""
    if not db_path.exists():
        return
    conn = sqlite3.connect(str(db_path))
    conn.execute(
        "INSERT INTO audit_log (action, detail, actor) VALUES (?, ?, ?)",
        ("search", json.dumps({"query": query, "results": result_count}),
         "document-search"),
    )
    conn.commit()
    conn.close()


def format_table(results: list[dict], full: bool) -> str:
    """Format results as a readable table."""
    if not results:
        return "No results found."

    lines = []
    lines.append(f"{'Section':>10}  {'Score':>5}  {'Src':>4}  {'Source File':<25}  {'Flags':<20}  {'Title / Body'}")
    lines.append("-" * 110)

    for r in results:
        sec = r["section_number"]
        score = f"{r['score']:.2f}"
        src = r["source"][:4]
        source_file = (r.get("source_file") or "")[:25]
        flags = ", ".join(r["flags"])[:20]
        if full:
            # Strip the "N.N\n" prefix that we prepended for embedding
            body = r["body"]
            if "\n" in body:
                body = body.split("\n", 1)[1]
            text = f"{r['section_title']}\n{body}" if r["section_title"] else body
        else:
            title = r["section_title"]
            body = r["body"]
            if "\n" in body:
                body = body.split("\n", 1)[1]
            snippet = body[:200].replace("\n", " ")
            text = f"{title}: {snippet}" if title else snippet
        lines.append(f"{sec:>10}  {score:>5}  {src:>4}  {source_file:<25}  {flags:<20}  {text}")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Search document clauses")
    parser.add_argument("query", help="Search query")
    parser.add_argument("--section", help="Filter by section pattern (e.g. '4.*')")
    parser.add_argument("--flag", help="Filter by flag (e.g. 'ip')")
    parser.add_argument("--source", help="Filter by source document filename")
    parser.add_argument("--full", action="store_true", help="Show full body")
    parser.add_argument("--top", type=int, default=10, help="Number of results")
    parser.add_argument("--db", default=str(DEFAULT_DB))
    parser.add_argument("--chroma", default=str(DEFAULT_CHROMA))
    parser.add_argument("--json", action="store_true", help="Output JSON")
    args = parser.parse_args()

    db_path = Path(args.db)
    chroma_dir = Path(args.chroma)

    # Run both searches
    semantic = search_chroma(chroma_dir, args.query, args.top * 2)
    keyword = search_sqlite(db_path, args.query, args.top * 2)
    results = merge_results(semantic, keyword, args.top)

    # Apply filters
    if args.section:
        results = [r for r in results
                   if fnmatch.fnmatch(r["section_number"], args.section)]
    if args.flag:
        results = [r for r in results if args.flag in r["flags"]]
    if args.source:
        pattern = args.source.lower()
        results = [r for r in results
                   if pattern in (r.get("source_file") or "").lower()]

    # Log the search
    log_search(db_path, args.query, len(results))

    # Output
    if args.json:
        print(json.dumps(results, indent=2))
    else:
        print(format_table(results, args.full))
        print(f"\n{len(results)} results for: {args.query}", file=sys.stderr)


if __name__ == "__main__":
    main()
