#!/usr/bin/env bash
# Verify all demo artifacts exist and the pipeline works end-to-end.
set -euo pipefail

REPO="$(cd "$(dirname "$0")/../.." && pwd)"
DEMO="$REPO/demo"
PASS=0; FAIL=0

ok()   { echo "  OK: $1"; PASS=$((PASS + 1)); }
fail() { echo "FAIL: $1"; FAIL=$((FAIL + 1)); }
check_file() { [[ -f "$1" ]] && ok "$2" || fail "$2 ($1)"; }

echo "=== Demo Artifact Verification ==="
echo

# --- Skills ---
echo "Skills:"
check_file "$DEMO/.claude/skills/document-loader/skill.md"  "document-loader skill"
check_file "$DEMO/.claude/skills/document-search/skill.md"  "document-search skill"
check_file "$DEMO/.claude/skills/document-eval/skill.md"    "document-eval skill"
check_file "$DEMO/.claude/skills/document-audit/skill.md"   "document-audit skill"

# --- Agents ---
echo "Agents:"
check_file "$DEMO/.agents/data-loader-agent.md"        "data-loader agent"
check_file "$DEMO/.agents/document-eval-agent.md"       "document-eval agent"
check_file "$DEMO/.agents/data-investigator-agent.md"   "data-investigator agent"
check_file "$DEMO/.agents/verification-agent.md"        "verification agent"
check_file "$DEMO/.agents/response-drafter-agent.md"    "response-drafter agent"

# --- Scripts ---
echo "Scripts:"
check_file "$REPO/.agents/bin/document-parse.py"   "contract-parse script"
check_file "$REPO/.agents/bin/document-load.py"    "document-load script"
check_file "$REPO/.agents/bin/document-search.py"  "document-search script"
check_file "$REPO/.agents/bin/test-parse.py"       "test-parse script"

# --- Criteria ---
echo "Criteria files:"
check_file "$DEMO/assets/criteria/ip-and-ownership.md"   "ip-and-ownership criteria"
check_file "$DEMO/assets/criteria/general-red-flags.md"   "general-red-flags criteria"

# --- Supporting materials ---
echo "Supporting materials:"
check_file "$DEMO/assets/playbook.md"                          "playbook"
check_file "$DEMO/assets/prebaked/naive-review.md"             "naive-review contrast"
check_file "$DEMO/assets/prebaked/document-review-checklist.md" "prebaked review checklist"
check_file "$DEMO/assets/prebaked/skill-example.md"            "skill example"
check_file "$DEMO/assets/problem-clauses.md"                   "problem clauses answer key"

# --- Spec & Plan ---
echo "Spec & Plan:"
check_file "$DEMO/spec.md"     "spec"
check_file "$DEMO/plan.md"     "plan"
check_file "$DEMO/Makefile"    "Makefile"

# --- Contract PDF ---
echo "Contract PDF:"
check_file "$DEMO/assets/documents/bigco-msa.pdf" "bigco-msa.pdf"

# --- Pipeline smoke test (only if PDF exists) ---
echo
echo "Pipeline smoke test:"
if [[ -f "$DEMO/assets/documents/bigco-msa.pdf" ]]; then
    # Parser test
    if uv run --with pymupdf "$REPO/.agents/bin/test-parse.py" > /dev/null 2>&1; then
        ok "parser smoke test"
    else
        fail "parser smoke test"
    fi

    # Load test (into temp dir)
    TMPDB="$(mktemp -d)/documents.db"
    TMPCHROMA="$(mktemp -d)/chroma"
    if uv run --with 'pymupdf,chromadb,sentence-transformers' \
        "$REPO/.agents/bin/document-load.py" \
        "$DEMO/assets/documents/bigco-msa.pdf" \
        --db "$TMPDB" --chroma "$TMPCHROMA" > /dev/null 2>&1; then
        ok "load pipeline"
    else
        fail "load pipeline"
    fi

    # Search test
    if [[ -f "$TMPDB" ]]; then
        if uv run --with 'chromadb,sentence-transformers' \
            "$REPO/.agents/bin/document-search.py" \
            "intellectual property" \
            --db "$TMPDB" --chroma "$TMPCHROMA" \
            --top 3 > /dev/null 2>&1; then
            ok "search pipeline"
        else
            fail "search pipeline"
        fi
    else
        fail "search pipeline (no db)"
    fi

    # Cleanup
    rm -rf "$(dirname "$TMPDB")" "$TMPCHROMA"
else
    echo "  SKIP: PDF not found — run 'cd demo && make contract' first"
fi

# --- Summary ---
echo
TOTAL=$((PASS + FAIL))
if [[ $FAIL -eq 0 ]]; then
    echo "PASS: $PASS/$TOTAL checks passed"
else
    echo "FAIL: $PASS passed, $FAIL failed out of $TOTAL"
    exit 1
fi
