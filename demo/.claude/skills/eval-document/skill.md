# eval-document

Evaluate loaded documents against a criteria file, producing a structured findings report.

## Triggers

- `/eval-document [criteria-file]`
- User asks to "evaluate", "review", or "check" the documents against criteria

## Instructions

1. **Gather evidence.** Run the eval script to search for relevant clauses per criterion:
   ```bash
   uv run --with 'chromadb,sentence-transformers' .agents/bin/document-eval.py "<criteria-file>"
   ```
   Default criteria: `assets/criteria/general-red-flags.md`

2. **Assess each criterion.** The script outputs evidence grouped by criterion.
   For each criterion, read the evidence and apply judgment:
   - Rate severity: `CRITICAL`, `HIGH`, `MEDIUM`, `LOW`, or `CLEAR`
   - Quote the specific clause text
   - Note which source document(s) the finding comes from
   - Explain your reasoning

3. **Produce the report:**

   ```markdown
   # Document Evaluation Report

   **Criteria file:** <path>
   **Date:** <date>
   **Documents searched:** <count>
   **Clauses searched:** <count>

   ## Summary

   | # | Criterion | Severity | Source Files | Sections |
   |---|-----------|----------|-------------|----------|
   | 1 | ...       | CRITICAL | RFP 20-020.pdf | 4.1, 12.12 |

   ## Detailed Findings

   ### 1. <Criterion Name>

   **Severity:** CRITICAL
   **Source:** RFP 20-020 Document.pdf
   **Sections:** 4.1, 12.12
   **Evidence:** > "quoted clause text..."
   **Finding:** <explanation>
   ```

## Available criteria files

- `assets/criteria/ip-and-ownership.md` — focused IP review (3 criteria)
- `assets/criteria/general-red-flags.md` — broad scan (6 criteria)
- Custom: any markdown file with `##` headings as criteria

## Constraints

- Documents must be loaded first
- Always cite section numbers, source documents, and quote clause text as evidence
- Rate conservatively — only use CRITICAL for genuine contradictions or impossibilities
- If a criterion finds no issues, rate it CLEAR and say so explicitly
- Look for cross-document contradictions (e.g., main RFP vs addenda)
