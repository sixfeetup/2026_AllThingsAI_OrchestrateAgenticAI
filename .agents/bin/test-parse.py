#!/usr/bin/env python3
"""Smoke-test contract-parse.py against bigco-msa.pdf.

Usage:
    uv run --with pymupdf test-parse.py
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent
PDF = REPO / "demo" / "assets" / "contracts" / "bigco-msa.pdf"
PARSER = Path(__file__).resolve().parent / "contract-parse.py"

# The 7 planted problems + cupcake — section numbers and substring probes
EXPECTED_CLAUSES = {
    "2.3": "commence promptly",           # Problem 4: ambiguous timeframe
    "2.5": "February 30",                  # Problem 2: impossible date
    "2.7": "reasonable effort",            # Problem 5: ambiguous terms
    "4.1": "exclusive and irrevocable",    # Problem 1a: exclusive IP
    "4.3": "mutually understood",          # Problem 6: ambiguous licensing
    "12.10": "cupcakes",                   # Easter egg: cupcake clause
    "12.12": "non-exclusive",              # Problem 1b: contradicts 4.1
    "12.13": "Six Feet Down",             # Problem 3: wrong name
    "13.1": "adequate staffing",           # Problem 7: ambiguous staffing
}


def main():
    if not PDF.exists():
        print(f"SKIP: PDF not found at {PDF}")
        print("  Run `cd demo && make contract` to generate it.")
        sys.exit(0)

    # Run parser
    result = subprocess.run(
        [sys.executable, str(PARSER), str(PDF)],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        print(f"FAIL: parser exited {result.returncode}")
        print(result.stderr)
        sys.exit(1)

    clauses = json.loads(result.stdout)
    by_section = {c["section_number"]: c for c in clauses}

    passed = 0
    failed = 0

    # Check total clause count
    if len(clauses) < 100:
        print(f"FAIL: expected 100+ clauses, got {len(clauses)}")
        failed += 1
    else:
        print(f"  OK: {len(clauses)} clauses parsed")
        passed += 1

    # Check each planted problem is findable
    for section, probe in EXPECTED_CLAUSES.items():
        clause = by_section.get(section)
        if clause is None:
            print(f"FAIL: section {section} not found")
            failed += 1
            continue
        if probe.lower() not in clause["body"].lower():
            print(f"FAIL: section {section} missing '{probe}'")
            print(f"  body: {clause['body'][:120]}...")
            failed += 1
            continue
        print(f"  OK: {section} contains '{probe}'")
        passed += 1

    # Check flags assigned
    ip_clauses = [c for c in clauses if "ip" in c["flags"]]
    if len(ip_clauses) < 3:
        print(f"FAIL: expected 3+ clauses flagged 'ip', got {len(ip_clauses)}")
        failed += 1
    else:
        print(f"  OK: {len(ip_clauses)} clauses flagged 'ip'")
        passed += 1

    # Check no TOC noise (empty exhibit entries on page 2)
    toc_noise = [c for c in clauses
                 if c["section_number"].startswith("Exhibit")
                 and c["page_start"] <= 3 and not c["body"]]
    if toc_noise:
        print(f"FAIL: {len(toc_noise)} empty TOC exhibit entries still present")
        failed += 1
    else:
        print("  OK: no TOC noise")
        passed += 1

    print(f"\n{'PASS' if failed == 0 else 'FAIL'}: {passed} passed, {failed} failed")
    sys.exit(0 if failed == 0 else 1)


if __name__ == "__main__":
    main()
