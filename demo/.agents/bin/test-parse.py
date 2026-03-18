#!/usr/bin/env python3
"""Smoke-test document-parse.py against the RFP document archive.

Usage:
    uv run --with 'pymupdf,python-docx,openpyxl,path' test-parse.py
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent
ZIP_PATH = REPO / "demo" / "assets" / "1-RFP 20-020 - Original Documents.zip"
PARSER = Path(__file__).resolve().parent / "document-parse.py"


def main():
    if not ZIP_PATH.exists():
        print(f"SKIP: ZIP archive not found at {ZIP_PATH}")
        print("  Place the RFP archive at demo/assets/")
        sys.exit(0)

    # Run parser against the zip
    result = subprocess.run(
        [sys.executable, str(PARSER), str(ZIP_PATH)],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        print(f"FAIL: parser exited {result.returncode}")
        print(result.stderr)
        sys.exit(1)

    clauses = json.loads(result.stdout)

    passed = 0
    failed = 0

    # --- Check: non-trivial clause count ---
    if len(clauses) < 10:
        print(f"FAIL: expected 10+ clauses, got {len(clauses)}")
        failed += 1
    else:
        print(f"  OK: {len(clauses)} clauses parsed")
        passed += 1

    # --- Check: multiple source documents ---
    source_files = set(c.get("source_file", "") for c in clauses)
    source_files.discard("")
    if len(source_files) < 3:
        print(f"FAIL: expected 3+ source documents, got {len(source_files)}: {source_files}")
        failed += 1
    else:
        print(f"  OK: {len(source_files)} source documents found")
        passed += 1

    # --- Check: source_file is set on every clause ---
    missing_source = [c for c in clauses if not c.get("source_file")]
    if missing_source:
        print(f"FAIL: {len(missing_source)} clauses missing source_file")
        failed += 1
    else:
        print(f"  OK: all clauses have source_file set")
        passed += 1

    # --- Check: PDF format handled ---
    pdf_sources = [sf for sf in source_files if sf.lower().endswith(".pdf")]
    if not pdf_sources:
        print("FAIL: no PDF documents parsed")
        failed += 1
    else:
        print(f"  OK: {len(pdf_sources)} PDF(s) parsed: {', '.join(pdf_sources)}")
        passed += 1

    # --- Check: DOCX format handled ---
    docx_sources = [sf for sf in source_files if sf.lower().endswith(".docx")]
    if not docx_sources:
        print("FAIL: no DOCX documents parsed")
        failed += 1
    else:
        print(f"  OK: {len(docx_sources)} DOCX(s) parsed: {', '.join(docx_sources)}")
        passed += 1

    # --- Check: XLSX format handled ---
    xlsx_sources = [sf for sf in source_files if sf.lower().endswith(".xlsx")]
    if not xlsx_sources:
        print("FAIL: no XLSX documents parsed")
        failed += 1
    else:
        print(f"  OK: {len(xlsx_sources)} XLSX(s) parsed: {', '.join(xlsx_sources)}")
        passed += 1

    # --- Check: DOC files were skipped (not parsed) ---
    doc_sources = [sf for sf in source_files if sf.lower().endswith(".doc")]
    if doc_sources:
        print(f"FAIL: DOC files should be skipped but found: {doc_sources}")
        failed += 1
    else:
        print("  OK: DOC files correctly skipped")
        passed += 1

    # --- Check: XLS files were skipped (not parsed) ---
    xls_sources = [sf for sf in source_files
                   if sf.lower().endswith(".xls") and not sf.lower().endswith(".xlsx")]
    if xls_sources:
        print(f"FAIL: XLS files should be skipped but found: {xls_sources}")
        failed += 1
    else:
        print("  OK: XLS files correctly skipped")
        passed += 1

    # --- Check: flags assigned ---
    flagged = [c for c in clauses if c.get("flags")]
    if len(flagged) < 5:
        print(f"FAIL: expected 5+ flagged clauses, got {len(flagged)}")
        failed += 1
    else:
        # Collect all unique flags
        all_flags = set()
        for c in clauses:
            all_flags.update(c.get("flags", []))
        print(f"  OK: {len(flagged)} clauses flagged, {len(all_flags)} unique flags: "
              f"{', '.join(sorted(all_flags))}")
        passed += 1

    # --- Check: clause body is not empty for most clauses ---
    empty_body = [c for c in clauses if not c.get("body", "").strip()]
    empty_pct = len(empty_body) / len(clauses) * 100 if clauses else 100
    if empty_pct > 50:
        print(f"FAIL: {empty_pct:.0f}% of clauses have empty bodies")
        failed += 1
    else:
        print(f"  OK: {100 - empty_pct:.0f}% of clauses have non-empty bodies")
        passed += 1

    # --- Check: stderr contained skip warnings for DOC/XLS ---
    stderr = result.stderr
    if "skipping legacy DOC" not in stderr.lower() and "warning" not in stderr.lower():
        # Don't fail — just note. The archive might not have DOC files.
        print("  NOTE: no DOC skip warnings in stderr (may be expected)")
    else:
        print("  OK: skip warnings present in stderr")
        passed += 1

    # --- Summary ---
    print(f"\n{'PASS' if failed == 0 else 'FAIL'}: {passed} passed, {failed} failed")
    if source_files:
        print(f"\nSource documents:")
        for sf in sorted(source_files):
            count = sum(1 for c in clauses if c.get("source_file") == sf)
            print(f"  {sf}: {count} clauses")

    sys.exit(0 if failed == 0 else 1)


if __name__ == "__main__":
    main()
