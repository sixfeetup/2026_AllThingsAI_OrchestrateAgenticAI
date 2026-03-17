# Cowork Contract Review Pipeline

**Trigger:** `/cowork-review [pdf-path]`

Orchestrate a full multi-agent contract review. This skill coordinates
the complete pipeline: load, evaluate, verify, and draft a response.

## Workflow

### Step 1: Load the Contract
Run the contract-loader skill (or MCP `load_contract` tool) on the PDF.
Default: `assets/contracts/bigco-msa.pdf`

Verify the load succeeded — check clause count (expect 100+) and page coverage.

### Step 2: Focused Evaluation
Run eval against `assets/criteria/ip-and-ownership.md`:
- For each criterion heading, search the contract for relevant clauses
- Rate severity: CRITICAL / HIGH / MEDIUM / LOW / CLEAR
- Cite specific section numbers and quote evidence

### Step 3: Broad Red Flag Scan
Run eval against `assets/criteria/general-red-flags.md`:
- Same process as Step 2 but with broader criteria
- Look for impossible dates, party name errors, one-sided terms,
  buried material terms, undefined obligations, hidden provisions

### Step 4: Adversarial Review
Switch to the verification-agent persona. For each finding from Steps 2-3:
- Construct a counter-argument
- Search for exculpatory context elsewhere in the contract
- Verdict: `upheld`, `downgraded`, or `dismissed`
- Be rigorous but fair — don't dismiss legitimate issues

### Step 5: Draft Response
Switch to response-drafter-agent persona:
- Group verified findings by severity and topic
- Draft a professional memo with:
  - Executive summary
  - Detailed findings with clause references
  - Recommended changes / redlines
  - Prioritization (must-fix vs nice-to-have)
- Tone: professional, constructive, firm on critical issues

### Step 6: Audit Trail
Run `/audit-contract` to display the full provenance trail.

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
