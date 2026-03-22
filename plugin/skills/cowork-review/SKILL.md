---
name: cowork-review
description: Orchestrate a full multi-agent document review pipeline in one pass — load, evaluate, verify, draft, and audit.
argument-hint: "[archive-path]"
disable-model-invocation: true
---

# Document Review Pipeline

Orchestrate a full multi-agent document review: load, evaluate, verify,
draft, and audit — in one pass.

## Instructions

### 1. Gather all evidence (one command)

Run the pipeline script to load documents, evaluate against all criteria
files, and collect the audit trail:

```bash
uv run --with 'pymupdf,python-docx,openpyxl,chromadb,sentence-transformers' \
    "${CLAUDE_PLUGIN_ROOT}/skills/cowork-review/document-pipeline.py" "$ARGUMENTS"
```

Default archive: `assets/1-RFP 20-020 - Original Documents.zip`
Default criteria: `ip-and-ownership.md` + `general-red-flags.md`

If data is already loaded, add `--skip-load` to skip the load stage.

### 2. Assess findings

Read the evidence output. For each criterion, apply judgment:
- Rate severity: `CRITICAL`, `HIGH`, `MEDIUM`, `LOW`, or `CLEAR`
- Quote specific clause text as evidence
- Note source document(s) and section numbers

### 3. Adversarial review

For each finding rated MEDIUM or above, switch to verification-agent
perspective:
- Construct the best counter-argument
- Search for exculpatory context
- Verdict: `upheld`, `downgraded`, or `dismissed`

### 4. Draft response

Switch to response-drafter-agent perspective:
- Group verified findings by severity and topic
- Draft a professional memo: executive summary, critical issues,
  high-priority concerns, moderate items, positive notes, next steps
- Tone: collaborative, specific, constructive

### 5. Save and display

Save the full report to `data/review-report.md`. Display the audit
trail summary at the end.

## Options

- `--skip-load` — skip load stage if data already exists
- `--criteria FILE ...` — use custom criteria files instead of defaults

## Constraints

- The pipeline script handles load + eval + audit in one permission grant
- The LLM handles assessment + adversarial + drafting (judgment work)
- Always cite section numbers, source documents, and quote evidence
- Save final report to `data/review-report.md`
