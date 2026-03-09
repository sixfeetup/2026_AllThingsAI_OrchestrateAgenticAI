# Parallel Workflow: The "Wizard's" Code Review

*Mapping the "Agentic Quest" patterns to a software engineering context.*

## 1. The Party Roles (Engineering Mapping)
*   **The Cleric (Governance/Style):** Agent focused on linting, docstrings,
  naming conventions, and project structure.
*   **The Wizard (Logic/Optimization):** Agent focused on algorithmic
  complexity, edge cases, and "hallucinated" logic in code.
*   **The Ranger (Security/Ops):** Agent focused on dependency vulnerabilities,
  secret detection, and performance regressions.
*   **The Warforged (The Automator):** The execution engine (Claude Code) that
  runs the tests and applies the "fixes."

## 2. The Task Graph (The Code Quest)
1.  **Decomposition (Cleric):** Scan the PR/Diff. Identify modified functions.
   Extract related types and interfaces to provide context.
2.  **Specialist Analysis (Wizard/Ranger):**
    *   **Sub-Task A:** Check for O(n^2) loops or resource leaks in modified
      functions.
    *   **Sub-Task B:** Scan for hardcoded credentials or insecure API calls.
3.  **Validation Loop (Warforged):**
    *   Generate a `pytest` or `vitest` file targeting the new logic.
    *   Run the tests in an isolated Docker container.
    *   Capture `stderr` and feed back to the Wizard if tests fail (The
      "Brownian Ratchet").
4.  **Reconciliation (The Party):**
    *   If Security (Ranger) flags a critical risk but Logic (Wizard) says it's
      fine $\rightarrow$ Flag for Senior Dev (Human) review.
    *   Aggregate all "Green" checks into a summary.

## 3. The "No-Miss" Code Audit
To prove high-assurance, the system produces:
*   **Traceability:** "Checked `auth_service.py:124` for SQL injection. Result:
  CLEAN. (Reason: Used parameterized queries)."
*   **Negative Confirmation:** "No new external dependencies added in this PR."
*   **Verification Receipt:** "Test Suite `PR_123_Validation` passed with 85%
  coverage on modified lines."

## 4. Cynefin Alignment
*   **Simple:** Formatting and Linting (Level 3 Autonomous).
*   **Complicated:** Refactoring a 500-line class (Level 2 Co-pilot).
*   **Complex/Chaotic:** Debugging a race condition in production (Level 1
  Direct Drive).
