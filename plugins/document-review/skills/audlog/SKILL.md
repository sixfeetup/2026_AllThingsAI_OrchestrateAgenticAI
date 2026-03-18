# audlog

Session timeline — view or add entries to the audit trail.

## Triggers

- `/audlog` — view the timeline (default, last 20)
- `/audlog view` — same
- `/audlog view all` — show everything
- `/audlog view N` — show last N entries
- `/audlog add <message>` — add a manual entry

## View (default)

Query the audit log:

```bash
sqlite3 -json demo/data/documents.db "SELECT id, timestamp, action, actor, detail FROM audit_log ORDER BY id"
```

Parse JSON detail blobs and render as a table:

```
## Audit Timeline (showing last 20 of N total)

| # | Time       | Action   | Actor            | Detail                              |
|---|------------|----------|------------------|-------------------------------------|
| 1 | 20:29:57   | LOAD     | document-load    | bigco-msa.pdf -> 142 clauses        |
| 2 | 20:30:50   | SEARCH   | document-search  | "intellectual property" -> 10 hits   |
| 3 | 20:30:56   | SEARCH   | document-search  | "cupcakes" -> 3 hits                |

_3 entries in audit trail._
```

Formatting rules:
- **Time**: show `HH:MM:SS` only (drop the date unless entries span multiple days)
- **Action**: UPPERCASE, pad to 8 chars
- **Detail**: parse the JSON blob into a human-readable summary:
  - `load`: `{source} -> {clause_count} clauses`
  - `search`: `"{query}" -> {results} hits`
  - `eval`: `{criteria} — {findings} findings`
  - Other: show raw detail, truncated to 50 chars
- **Pagination**: default to last 20 entries. If `view all`, show everything.
  If `view N`, show last N. Always show total count.
- If > 20 entries and showing paginated: add footer
  `Showing last 20 of N. Use '/audlog view all' for full trail.`

## Add

Insert a manual entry into the audit log. The user provides a freeform
message; you determine the appropriate `action` category.

Action categories: `load`, `search`, `eval`, `verify`, `draft`, `edit`,
`handoff`, `decision`, `note`, `error`.

```bash
sqlite3 demo/data/documents.db "INSERT INTO audit_log (action, detail, actor) VALUES ('<action>', '<user message>', 'user')"
```

Confirm: "Logged: [action] — <message>"

## Examples

- `/audlog` — show last 20 entries as table
- `/audlog view all` — show full trail
- `/audlog view 5` — show last 5 entries
- `/audlog add switching to broad red-flag criteria` — inserts a `decision` entry
- `/audlog add loaded fresh PDF after regeneration` — inserts a `load` entry
- `/audlog add something looks off in section 12` — inserts a `note` entry

## Prerequisites

- `demo/data/documents.db` must exist (created by `/load-document`)
