# Cowork Document Review Pipeline

**Trigger:** `/cowork-review [archive-path]`

Orchestrate a full multi-agent document review. This skill coordinates
the complete pipeline: load, evaluate, verify, and draft a response.

## Workflow

### Step 1: Load the Documents
Run the document-loader skill (or MCP `load_document` tool) on the archive.
Default: `assets/1-RFP 20-020 - Original Documents.zip`

Verify the load succeeded — check document count (expect 17 files) and clause coverage.

### Step 2: Focused Evaluation
Run eval against `assets/criteria/ip-and-ownership.md`:
- For each criterion heading, search across all loaded documents
- Rate severity: CRITICAL / HIGH / MEDIUM / LOW / CLEAR
- Cite specific section numbers, source documents, and quote evidence

### Step 3: Broad Red Flag Scan
Run eval against `assets/criteria/general-red-flags.md`:
- Same process as Step 2 but with broader criteria
- Look for missing dates, inconsistencies across documents, one-sided terms,
  buried material terms, undefined obligations, cross-document contradictions

### Step 4: Adversarial Review
Switch to the verification-agent persona. For each finding from Steps 2-3:
- Construct a counter-argument
- Search for exculpatory context in other documents in the package
- Verdict: `upheld`, `downgraded`, or `dismissed`
- Be rigorous but fair — don't dismiss legitimate issues

### Step 5: Draft Response
Switch to response-drafter-agent persona:
- Group verified findings by severity and topic
- Draft a professional memo with:
  - Executive summary
  - Detailed findings with document and clause references
  - Recommended changes / redlines
  - Prioritization (must-fix vs nice-to-have)
- Tone: professional, constructive, firm on critical issues

### Step 6: Audit Trail
Run `/audit-document` to display the full provenance trail.

## Output
Save the final report to `data/review-report.md` with all sections:
findings, verification results, response draft, and audit summary.

## Cowork Notes
When running in cowork mode (multiple Claude instances):
- Each step can be assigned to a different instance
- Use the shared SQLite DB as the coordination point
- The audit_log table tracks which agent did what and when
- Pass findings between steps as markdown — each step reads the
  previous step's output and builds on it
