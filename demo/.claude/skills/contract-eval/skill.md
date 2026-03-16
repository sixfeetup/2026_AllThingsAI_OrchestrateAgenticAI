# contract-eval

Evaluate a loaded contract against a criteria file, producing a structured findings report.

## Triggers

- `/eval-contract [criteria-file]`
- User asks to "evaluate", "review", or "check" the contract against criteria

## Instructions

1. **Load criteria.** Read the criteria markdown file. Default: `demo/assets/criteria/general-red-flags.md`. Each `##` heading is one criterion to evaluate.

2. **For each criterion:**
   a. Extract the criterion name and description from the heading and body.
   b. Use the search script to find relevant clauses:
      ```bash
      uv run --with 'chromadb,sentence-transformers' .agents/bin/contract-search.py "<criterion keywords>" --full --json
      ```
   c. Read the returned clause text and assess whether the issue described
      in the criterion exists in the contract.
   d. Rate severity: `CRITICAL`, `HIGH`, `MEDIUM`, `LOW`, or `CLEAR`.
   e. Quote the specific clause text as evidence.
   f. Explain your reasoning.

3. **Produce the report** in this format:

   ```markdown
   # Contract Evaluation Report

   **Criteria file:** <path>
   **Date:** <date>
   **Clauses searched:** <count>

   ## Summary

   | # | Criterion | Severity | Sections |
   |---|-----------|----------|----------|
   | 1 | ...       | CRITICAL | 4.1, 12.12 |

   ## Detailed Findings

   ### 1. <Criterion Name>

   **Severity:** CRITICAL
   **Sections:** 4.1, 12.12
   **Evidence:** > "quoted clause text..."
   **Finding:** <explanation>
   ```

4. **Log the eval** — after producing the report, record results:
   ```bash
   # The search script logs automatically, but also note the eval in summary
   ```

## Options

- `--adversarial` — for each finding, also generate a counter-argument
  (what opposing counsel might say in defense of the clause)

## Available criteria files

- `demo/assets/criteria/ip-and-ownership.md` — focused IP review (3 criteria)
- `demo/assets/criteria/general-red-flags.md` — broad scan (6 criteria)
- Custom: any markdown file with `##` headings as criteria

## Constraints

- Contract must be loaded first
- Always cite section numbers and quote clause text as evidence
- Rate conservatively — only use CRITICAL for genuine contradictions or impossibilities
- If a criterion finds no issues, rate it CLEAR and say so explicitly
