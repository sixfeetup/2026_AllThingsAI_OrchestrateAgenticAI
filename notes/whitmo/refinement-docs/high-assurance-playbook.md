# The High-Assurance Playbook (The "Loot Table")

*Focus: Actionable engineering patterns for 2026 agentic workflows.*

## 1. Graduated Trust Framework
*   **Level 1 (Direct Drive):** Manual trigger, manual audit. Use for novel or chaotic tasks (Cynefin: Chaotic).
*   **Level 2 (Co-Pilot):** Automated task decomposition, manual gate on "Act." Use for expert-level analysis (Cynefin: Complicated).
*   **Level 3 (Autonomous Loop):** Automated execution, audit-by-exception. Use for deterministic or high-volume tasks (Cynefin: Simple).

## 2. The `CLAUDE.md` Standard
*   Define **Roles** (Cleric/Wizard/Ranger) as system-level constraints.
*   Define **Invariants** (e.g., "Never modify `package.json` without running `npm install`").
*   Define **Verification Gates** (e.g., "Every contract flag must cite a line number").

## 3. Containment Strategy
*   **Ephemeral Sandboxes:** Every agentic "Act" occurs in a disposable container.
*   **State Snapshots:** Capture system state before and after agent intervention for 1-click rollback.
