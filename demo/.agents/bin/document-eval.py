#!/usr/bin/env python3
"""Evaluate loaded documents against a criteria file.

Usage:
    uv run --with 'chromadb,sentence-transformers' document-eval.py <criteria-file> [options]

Reads a criteria markdown file (## headings = criteria), searches the loaded
documents for relevant clauses, and outputs a structured findings report.

The LLM still does the judgment — this script gathers the evidence.
"""
from __future__ import annotations

import argparse
import json
import re
import sqlite3
import sys
from pathlib import Path

DEFAULT_DB = Path(__file__).resolve().parent.parent.parent / "data" / "documents.db"
DEFAULT_CHROMA = Path(__file__).resolve().parent.parent.parent / "data" / "chroma"


def parse_criteria(path: Path) -> list[dict]:
    """Parse a criteria markdown file into structured criteria."""
    text = path.read_text()
    criteria = []
    # Split on ## headings (not ### subheadings)
    parts = re.split(r'^## ', text, flags=re.MULTILINE)
    for part in parts[1:]:  # skip preamble before first ##
        lines = part.strip().split('\n')
        name = lines[0].strip()
        body = '\n'.join(lines[1:]).strip()

        # Extract subsections
        what_to_look_for = ""
        why_it_matters = ""
        red_flags = ""

        for section_match in re.finditer(
            r'### (What to look for|Why it matters|Red flag indicators)\s*\n(.*?)(?=\n### |\Z)',
            body, re.DOTALL
        ):
            heading = section_match.group(1)
            content = section_match.group(2).strip()
            if heading == "What to look for":
                what_to_look_for = content
            elif heading == "Why it matters":
                why_it_matters = content
            elif heading == "Red flag indicators":
                red_flags = content

        # Build search keywords from the criterion name + key phrases
        search_terms = name
        if what_to_look_for:
            # Extract key noun phrases for better search
            key_phrases = re.findall(
                r'\*\*(.*?)\*\*', what_to_look_for
            )
            if key_phrases:
                search_terms += " " + " ".join(key_phrases[:3])

        criteria.append({
            "name": name,
            "what_to_look_for": what_to_look_for,
            "why_it_matters": why_it_matters,
            "red_flags": red_flags,
            "search_terms": search_terms,
            "full_body": body,
        })
    return criteria


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

    words = query.lower().split()[:6]  # limit to avoid overly narrow matching
    if not words:
        return []

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
        body_lower = row["body"].lower()
        title_lower = (row["section_title"] or "").lower()
        matched = sum(1 for w in words if w in body_lower or w in title_lower)
        score = matched / len(words) * 0.8

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
    """Merge and deduplicate results."""
    by_key: dict[str, dict] = {}
    for hit in semantic + keyword:
        key = f"{hit['section_number']}:{hit.get('source_file', '')}"
        if key not in by_key or hit["score"] > by_key[key]["score"]:
            by_key[key] = hit
        elif key in by_key and hit["source"] != by_key[key]["source"]:
            by_key[key]["score"] = min(1.0, by_key[key]["score"] + 0.1)

    results = sorted(by_key.values(), key=lambda x: x["score"], reverse=True)
    return results[:top_k]


def get_doc_stats(db_path: Path) -> dict:
    """Get document statistics."""
    if not db_path.exists():
        return {"documents": 0, "clauses": 0}

    conn = sqlite3.connect(str(db_path))
    clause_count = conn.execute("SELECT COUNT(*) FROM clauses").fetchone()[0]
    doc_count = conn.execute(
        "SELECT COUNT(DISTINCT source_file) FROM clauses"
    ).fetchone()[0]
    conn.close()
    return {"documents": doc_count, "clauses": clause_count}


def log_eval(db_path: Path, criteria_file: str, criteria_count: int):
    """Log evaluation to audit trail."""
    if not db_path.exists():
        return
    conn = sqlite3.connect(str(db_path))
    conn.execute(
        "INSERT INTO audit_log (action, detail, actor) VALUES (?, ?, ?)",
        ("eval", json.dumps({
            "criteria_file": criteria_file,
            "criteria_count": criteria_count,
        }), "document-eval"),
    )
    conn.commit()
    conn.close()


def clean_body(body: str) -> str:
    """Strip the section number prefix from clause body."""
    if "\n" in body:
        return body.split("\n", 1)[1]
    return body


def main():
    parser = argparse.ArgumentParser(description="Evaluate documents against criteria")
    parser.add_argument("criteria", help="Path to criteria markdown file")
    parser.add_argument("--db", default=str(DEFAULT_DB))
    parser.add_argument("--chroma", default=str(DEFAULT_CHROMA))
    parser.add_argument("--top", type=int, default=8,
                        help="Results per criterion (default: 8)")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    args = parser.parse_args()

    criteria_path = Path(args.criteria)
    if not criteria_path.exists():
        print(f"Criteria file not found: {args.criteria}", file=sys.stderr)
        sys.exit(1)

    db_path = Path(args.db)
    chroma_dir = Path(args.chroma)

    if not db_path.exists():
        print("Database not found. Run /load-document first.", file=sys.stderr)
        sys.exit(1)

    # Parse criteria
    criteria = parse_criteria(criteria_path)
    stats = get_doc_stats(db_path)

    print(f"Evaluating {len(criteria)} criteria from {criteria_path.name}", file=sys.stderr)
    print(f"Searching {stats['clauses']} clauses across {stats['documents']} documents\n",
          file=sys.stderr)

    # Evaluate each criterion
    all_findings = []
    for i, criterion in enumerate(criteria, 1):
        print(f"  [{i}/{len(criteria)}] {criterion['name']}...", file=sys.stderr)

        # Run searches with multiple query strategies
        queries = [criterion["search_terms"]]
        # Also search with just the criterion name for broader coverage
        if criterion["search_terms"] != criterion["name"]:
            queries.append(criterion["name"])

        all_hits = []
        for q in queries:
            semantic = search_chroma(chroma_dir, q, args.top)
            keyword = search_sqlite(db_path, q, args.top)
            all_hits.extend(semantic)
            all_hits.extend(keyword)

        results = merge_results(all_hits, [], args.top)

        # Build finding with evidence
        evidence = []
        for r in results:
            if r["score"] >= 0.25:  # relevance threshold
                evidence.append({
                    "section": r["section_number"],
                    "source_file": r["source_file"],
                    "score": round(r["score"], 2),
                    "body": clean_body(r["body"]),
                    "title": r["section_title"],
                })

        finding = {
            "criterion_number": i,
            "criterion_name": criterion["name"],
            "what_to_look_for": criterion["what_to_look_for"],
            "red_flags": criterion["red_flags"],
            "evidence": evidence,
            "source_files": sorted(set(
                e["source_file"] for e in evidence if e["source_file"]
            )),
            "sections": [e["section"] for e in evidence],
        }
        all_findings.append(finding)

    # Log the eval
    log_eval(db_path, str(criteria_path), len(criteria))

    # Output
    output = {
        "criteria_file": str(criteria_path),
        "criteria_count": len(criteria),
        "documents_searched": stats["documents"],
        "clauses_searched": stats["clauses"],
        "findings": all_findings,
    }

    if args.json:
        print(json.dumps(output, indent=2))
    else:
        # Markdown report
        ## @@ use a template
        print(f"# Document Evaluation — Evidence Gathered")
        print(f"")
        print(f"**Criteria file:** {criteria_path.name}")
        print(f"**Documents searched:** {stats['documents']}")
        print(f"**Clauses searched:** {stats['clauses']}")
        print(f"**Criteria evaluated:** {len(criteria)}")
        print()

        for f in all_findings:
            print(f"---")
            print(f"## {f['criterion_number']}. {f['criterion_name']}")
            print()
            if f["source_files"]:
                print(f"**Source files:** {', '.join(f['source_files'])}")
                print(f"**Relevant sections:** {', '.join(f['sections'][:6])}")
            print()
            print(f"**What to look for:** {f['what_to_look_for'][:200]}...")
            print()
            print(f"### Evidence ({len(f['evidence'])} relevant clauses)")
            print()
            for j, e in enumerate(f["evidence"][:5], 1):
                print(f"**{j}. Section {e['section']}** ({e['source_file']}, "
                      f"relevance: {e['score']})")
                # Show first 300 chars of body
                snippet = e["body"][:300].replace("\n", " ")
                print(f"> {snippet}...")
                print()

    print(f"\nDone. {len(criteria)} criteria evaluated.", file=sys.stderr)


if __name__ == "__main__":
    main()
