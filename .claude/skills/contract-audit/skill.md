# contract-audit

Display the audit trail of all contract analysis actions.

## Triggers

- `/audit-contract`
- User asks to see the "audit trail", "history", or "what we've done"

## Instructions

1. Query the audit log from SQLite:
   ```bash
   sqlite3 -header -column demo/data/contracts.db "SELECT id, timestamp, action, actor, detail FROM audit_log ORDER BY id"
   ```

2. Present the results as a chronological log:
   - **load** actions: what file was loaded, how many clauses
   - **search** actions: what was searched, how many results
   - **eval** actions: what criteria were used, findings summary

3. If the user asks for a provenance summary, cross-reference:
   - Which findings are supported by which search results
   - Which searches returned the evidence used in findings
   - Flag any findings that lack direct search evidence

## Prerequisites

- Contract must be loaded (the audit_log table is created during load)

## Constraints

- The audit log is append-only — never delete or modify entries
- Timestamps are UTC
- Present in reverse chronological order if the user asks for "recent" activity
