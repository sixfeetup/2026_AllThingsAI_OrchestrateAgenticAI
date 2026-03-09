# The Audit & Verification Framework (The "No-Miss" Proof)

*Focus: How to prove the AI didn't hallucinate or skip a step.*

## 1. Human-Readable Evidence
*   **The "Receipt":** Every claim must include a `Source_Snippet` and a
  `Confidence_Score`.
*   **Negative Confirmation:** The agent must explicitly state what it *did not*
  find (e.g., "Termination for Convenience: NOT PRESENT").

## 2. Deterministic Checks
*   **Schema Enforcement:** Final output must pass a Pydantic/Zod validation
  gate before being shown to the user.
*   **Cross-Reference Loop:** Agent D scans the final report against the
  original raw text to ensure no "hallucinated clauses" were introduced during
  synthesis.

## 3. The "Kill Switch" Logic
*   **Abort Conditions:** Define thresholds (e.g., Token usage > 50k, 3+ failed
  retries on a single sub-task).
*   **Transparency:** The UI must show the **Task Graph Progress** (which agents
  succeeded/failed) in real-time.
