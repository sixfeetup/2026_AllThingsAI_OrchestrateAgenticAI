#!/usr/bin/env python3
"""Parse a contract PDF into structured JSON clauses.

Usage:
    uv run --with pymupdf contract-parse.py <pdf-path> [--output <json-path>]

Outputs a JSON array of clause objects to stdout (or file if --output given).
"""

from __future__ import annotations

import argparse
import json
import re
import sys

import fitz  # PyMuPDF


# Patterns for line classification
# Section heading: "4. INTELLECTUAL PROPERTY" (number, dot, space, ALL CAPS title)
SECTION_RE = re.compile(r"^(\d+)\.\s+([A-Z][A-Z &,\-/]+)$")
# Clause number alone on a line: "2.1" or "12.10"
CLAUSE_BARE_RE = re.compile(r"^(\d+\.\d+)$")
# Clause number with inline text: "12.10 Force Majeure. Neither Party..."
CLAUSE_INLINE_RE = re.compile(r"^(\d+\.\d+)\s+(.+)")
# Exhibit sub-heading with text: "A.1 Overview"
SUB_INLINE_RE = re.compile(r"^([A-Z]\.\d+)\s+(.+)")
# Exhibit sub-heading bare: "A.1"
SUB_BARE_RE = re.compile(r"^([A-Z]\.\d+)$")
# Exhibit heading: "EXHIBIT A: Statement of Work #1"
EXHIBIT_RE = re.compile(r"^EXHIBIT\s+([A-Z])[.:]\s*(.*)", re.IGNORECASE)
# Preamble heading
PREAMBLE_RE = re.compile(r"^PREAMBLE$")
# TOC heading
TOC_RE = re.compile(r"^TABLE OF CONTENTS$")
# Signature block
SIGNATURE_RE = re.compile(r"^IN WITNESS WHEREOF", re.IGNORECASE)
# Page header/footer
HEADER_RE = re.compile(r"^CONFIDENTIAL\s*[-—–]")
FOOTER_RE = re.compile(r"^Page \d+/\d+$")

# Heuristic keyword → flag mapping
FLAG_KEYWORDS: dict[str, list[str]] = {
    "ip": ["intellectual property", "work product", "assignment", "license",
           "copyright", "patent", "trademark", "moral rights", "pre-existing ip"],
    "termination": ["termination", "terminate", "term of", "expiration",
                    "renewal", "auto-renew"],
    "payment": ["fee", "payment", "invoice", "compensation", "rate",
                "reimburse", "expense"],
    "confidentiality": ["confidential", "non-disclosure", "trade secret",
                        "proprietary"],
    "liability": ["liability", "indemnif", "damages", "limitation of",
                  "consequential"],
    "staffing": ["staffing", "personnel", "team", "headcount", "resource"],
    "compliance": ["compliance", "regulatory", "gdpr", "ccpa", "privacy",
                   "data protection", "audit"],
    "noncompete": ["non-compet", "non-solicitation", "restrictive covenant"],
    "insurance": ["insurance", "coverage", "policy"],
    "governance": ["governance", "escalation", "change management",
                   "change control"],
}


def assign_flags(text: str) -> list[str]:
    """Assign topic flags based on keyword matching."""
    lower = text.lower()
    return sorted(
        flag for flag, keywords in FLAG_KEYWORDS.items()
        if any(kw in lower for kw in keywords)
    )


def _flush(current: dict | None, clauses: list[dict]):
    """Append current clause to list if it exists."""
    if current is not None:
        current["body"] = current["body"].strip()
        clauses.append(current)


def _new_clause(section_number: str, section_title: str, body: str,
                page: int) -> dict:
    return {
        "section_number": section_number,
        "section_title": section_title,
        "body": body,
        "page_start": page,
        "page_end": page,
    }


def extract_clauses(pdf_path: str) -> list[dict]:
    """Extract structured clauses from a contract PDF."""
    doc = fitz.open(pdf_path)

    # Collect all lines with their page numbers
    lines: list[tuple[int, str]] = []  # (page_1indexed, text)
    for page_num in range(len(doc)):
        page = doc[page_num]
        text = page.get_text("text")
        for line in text.split("\n"):
            stripped = line.strip()
            if stripped:
                lines.append((page_num + 1, stripped))
    doc.close()

    clauses: list[dict] = []
    current: dict | None = None
    in_toc = False  # skip TOC content

    i = 0
    while i < len(lines):
        page, line = lines[i]

        # Skip headers and footers
        if HEADER_RE.match(line) or FOOTER_RE.match(line):
            i += 1
            continue

        # Detect and skip TOC
        if TOC_RE.match(line):
            in_toc = True
            i += 1
            continue

        # End TOC when we hit PREAMBLE or a section heading
        if in_toc:
            if PREAMBLE_RE.match(line) or SECTION_RE.match(line):
                in_toc = False
                # fall through to handle this line
            else:
                i += 1
                continue

        # PREAMBLE
        if PREAMBLE_RE.match(line):
            _flush(current, clauses)
            current = _new_clause("Preamble", "Preamble", "", page)
            i += 1
            continue

        # Signature block
        if SIGNATURE_RE.match(line):
            _flush(current, clauses)
            current = _new_clause("Signatures", "Signatures", "", page)
            i += 1
            continue

        # Section heading: "4. INTELLECTUAL PROPERTY"
        m = SECTION_RE.match(line)
        if m:
            _flush(current, clauses)
            current = _new_clause(m.group(1), m.group(2).strip().title(),
                                  "", page)
            i += 1
            continue

        # Exhibit heading: "EXHIBIT A: ..."
        m = EXHIBIT_RE.match(line)
        if m:
            _flush(current, clauses)
            title = m.group(2).strip()
            current = _new_clause(f"Exhibit {m.group(1)}",
                                  title.title() if title else "", "", page)
            i += 1
            continue

        # Clause number bare on its own line: "2.1"
        m = CLAUSE_BARE_RE.match(line)
        if m:
            _flush(current, clauses)
            current = _new_clause(m.group(1), "", "", page)
            i += 1
            continue

        # Clause number with inline text: "12.10 Force Majeure. ..."
        m = CLAUSE_INLINE_RE.match(line)
        if m:
            _flush(current, clauses)
            # Try to extract title from "Title. Body text..."
            rest = m.group(2)
            title = ""
            dot_match = re.match(r"^([A-Z][^.]+)\.\s*(.*)", rest)
            if dot_match:
                title = dot_match.group(1)
                rest = dot_match.group(2)
            current = _new_clause(m.group(1), title, rest, page)
            i += 1
            continue

        # Exhibit sub-heading bare: "A.1"
        m = SUB_BARE_RE.match(line)
        if m:
            _flush(current, clauses)
            current = _new_clause(m.group(1), "", "", page)
            i += 1
            continue

        # Exhibit sub-heading with text: "A.1 Overview"
        m = SUB_INLINE_RE.match(line)
        if m:
            _flush(current, clauses)
            current = _new_clause(m.group(1), m.group(2), "", page)
            i += 1
            continue

        # Continuation text — append to current clause body
        if current is not None:
            if current["body"]:
                current["body"] += " " + line
            else:
                current["body"] = line
            current["page_end"] = page

        i += 1

    _flush(current, clauses)

    # Post-process: assign flags
    for clause in clauses:
        combined = f"{clause.get('section_title', '')} {clause['body']}"
        clause["flags"] = assign_flags(combined)

    return clauses


def main():
    parser = argparse.ArgumentParser(description="Parse contract PDF to JSON")
    parser.add_argument("pdf_path", help="Path to contract PDF")
    parser.add_argument("--output", "-o",
                        help="Output JSON file (default: stdout)")
    args = parser.parse_args()

    clauses = extract_clauses(args.pdf_path)
    result = json.dumps(clauses, indent=2, ensure_ascii=False)

    if args.output:
        from path import Path
        Path(args.output).parent.makedirs_p()
        Path(args.output).write_text(result)
        print(f"Wrote {len(clauses)} clauses to {args.output}", file=sys.stderr)
    else:
        print(result)

    # Summary to stderr
    pages = set()
    for c in clauses:
        pages.update(range(c["page_start"], c["page_end"] + 1))
    print(f"\nSummary: {len(clauses)} clauses across {len(pages)} pages",
          file=sys.stderr)


if __name__ == "__main__":
    main()
