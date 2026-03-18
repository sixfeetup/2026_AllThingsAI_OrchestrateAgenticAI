# Demo Script: The Agentic Quest (15-20 Min)
*File: demo-script.md*

## Setup
*   **Terminal:** 18pt font, dark mode.
*   **Hot-swap Fallback:** `asciinema play backups/demo_run.cast`
*   **File Open:** `refinement-docs/synthetic-contract-dungeon-map.md`

---

## Phase 1: The Level 1 Failure (3 min)
**Action:** Run a standard single-shot prompt using Claude Code.
```bash
claude "Review synthetic-contract-dungeon-map.md and flag any risks."
```
**Talking Point:** "Look at the output. It caught the Auto-Renewal (Trap #2),
but it missed the unlimited liability for Data Integrity (Trap #1) because it
didn't have the context of our specific Risk Policy. This is the Yes-Man NPC."

---

## Phase 2: The Level 2 Orchestration (10 min)
**Possible beat:** Live-edit a skill mid-demo (e.g. broaden the eval
criteria in document-eval to find more issues) — shows skills are
iterative, not fixed. Good for illustrating the edit→re-run loop.

**Action:** Run the multi-agent script using the roles.
```bash
./scripts/run-level-2.sh --file artifacts/sample-contract.md
```
**The Visuals:**
1.  **Cleric (Extraction):** Terminal shows: "Extracting 12 clauses... [DONE]"
2.  **Wizard (Analysis):** Terminal shows: "Checking for contradictions... TRAP
   #4 FOUND: Section 7 vs 10."
3.  **Adversary:** Terminal shows: "Red-teaming Clause 3.1... UNLIMITED
   LIABILITY FLAG RAISED."
4.  **Ranger (Verification):** Terminal shows: "Verifying citations... [100%
   GROUNDED]"

**Talking Point:** "Now we're playing as a Party. The Cleric ensures we didn't
skip anything, the Wizard finds the logic traps, and the Ranger ensures we
didn't hallucinate. OODA: The agents are doing the Observe and Orient; the Human
just does the Decide."

---

## Phase 3: The "No-Miss" Report (2 min)
**Action:** Open the final report `artifacts/audit-report.md`.
```bash
cat artifacts/audit-report.md
```
**Talking Point:** "This isn't a chat log. It's an auditable receipt. Every flag
has a quote, a line number, and a risk score. This is what the Cleric can hand
to the CFO with confidence."

---

## Phase 4: The Engineering Parallel (Slide)
**Action:** Switch to slide showing the **Code Review Task Graph**. **Talking
Point:** "Before we go, look at this. It's the exact same pattern. Replace
'Clause' with 'Function,' replace 'Liability' with 'O(n^2) Loop,' and replace
'Audit' with 'Test Suite.' The Quest is the same."
