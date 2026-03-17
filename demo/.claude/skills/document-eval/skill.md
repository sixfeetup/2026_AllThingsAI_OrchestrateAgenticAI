# document-eval

Evaluate loaded documents against a criteria file, producing a structured findings report.

## Triggers

- `/eval-document [criteria-file]`
- User asks to "evaluate", "review", or "check" the documents against criteria

## Instructions

1. **Load criteria.** Read the criteria markdown file. Default: `demo/assets/criteria/general-red-flags.md`. Each `##` heading is one criterion to evaluate.

2. **For each criterion:**
   a. Extract the criterion name and description from the heading and body.
   b. Use the search script to find relevant clauses across all loaded documents:
      ```bash
      uv run --with 'chromadb,sentence-transformers' .agents/bin/document-search.py "<criterion keywords>" --full --json
      ```
   c. Read the returned clause text and assess whether the issue described
      in the criterion exists in the documents.
   d. Rate severity: `CRITICAL`, `HIGH`, `MEDIUM`, `LOW`, or `CLEAR`.
   e. Quote the specific clause text as evidence.
   f. Note which source document(s) the finding comes from.
   g. Explain your reasoning.

3. **Produce the report** in this format:

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

## Options

- `--adversarial` — for each finding, also generate a counter-argument

## Available criteria files

- `demo/assets/criteria/ip-and-ownership.md` — focused IP review (3 criteria)
- `demo/assets/criteria/general-red-flags.md` — broad scan (6 criteria)
- Custom: any markdown file with `##` headings as criteria

## Constraints

- Documents must be loaded first
- Always cite section numbers, source documents, and quote clause text as evidence
- Rate conservatively — only use CRITICAL for genuine contradictions or impossibilities
- If a criterion finds no issues, rate it CLEAR and say so explicitly
- Look for cross-document contradictions (e.g., main RFP vs addenda)
