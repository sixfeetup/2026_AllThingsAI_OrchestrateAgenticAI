# The Orchestration Task Graph (The Architecture)

*Focus: Moving from "Prompts" to "State Machines" to ensure reliability.*

## 1. Decomposition (The Cleric’s Lens)
*   **Input:** `Contract.pdf` or `FeatureBranch`.
*   **Action:** Sub-agent splits input into atomic units (Clauses or Functions).

## 2. Parallel Analysis (The Wizard’s Lens)
*   **Agent A (The Specialist):** Performs primary review (e.g., "Find Liability").
*   **Agent B (The Adversary):** Challenges Agent A (e.g., "Why is this NOT a risk?").
*   **Agent C (The Validator):** Checks for structural completeness (e.g., "Did we skip Section 4?").

## 3. Reconciliation & Routing (The Ranger’s Lens)
*   **Decision Logic:** If Agent A and B disagree $\rightarrow$ Escalate to Human.
*   **Feedback Loop:** If Validator flags a skip $\rightarrow$ Re-run Decomposition.
*   **Output:** Unified JSON Schema $\rightarrow$ Markdown Report.
