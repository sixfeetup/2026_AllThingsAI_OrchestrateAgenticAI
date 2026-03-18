# Named Document Sets

## Problem

The document review pipeline supports only one document set per session. Every `/load-document` call replaces the previous data (DELETE FROM clauses, drop ChromaDB collection). There's no way to load multiple documents and switch between them.

## User Stories

1. As a reviewer, I want to load multiple document packages by name so I can compare findings across contracts without re-parsing.
2. As a reviewer, I want to set a "current document" so searches, evals, and audits scope to the right package automatically.
3. As a presenter, I want to pre-load several documents before the demo and switch between them live.

## Functional Requirements

### FR-1: Named loading

`/load-document assets/contract-a.zip --name contract-a`

- `--name` argument on `document-load.py` (and the MCP `load_document` tool)
- Defaults to slugified archive filename if omitted
- Loading a name that already exists replaces only that set's data

### FR-2: Document sets table

New SQLite table:

```sql
CREATE TABLE document_sets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    source_path TEXT,
    created_at TEXT DEFAULT (datetime('now')),
    clause_count INTEGER DEFAULT 0
);
```

`clauses` table gains `document_set_id INTEGER REFERENCES document_sets(id)`.

### FR-3: ChromaDB namespacing

One collection per set: `document_clauses_{name}` instead of the single `document_clauses`.

### FR-4: Current-document pointer

- Stored in `data/.current-set` (plain text, just the name)
- Written on load, switchable via `/current-document <name>`
- All search/eval/audit tools read this file and auto-filter

### FR-5: Listing sets

`/current-document` with no argument lists all loaded sets and marks the active one.

### FR-6: MCP tool changes

| Tool | Change |
|------|--------|
| `load_document` | Add optional `name` param |
| `search_document` | Add optional `document_set` param; default to current |
| `get_document_stats` | Scope to current set; add `set_name` to output |
| `audit_document` | Filter by current set |

## Files to modify

| File | What |
|------|------|
| `.agents/bin/document-load.py` | Schema migration, `--name` arg, scoped insert/delete |
| `.agents/bin/document-search.py` | Read `.current-set`, add `--set` filter |
| `.agents/bin/document-mcp-server.py` | Expose `name`/`document_set` params on tools |
| `.claude/skills/load-document/skill.md` | Document `--name` option |
| `.claude/skills/search-document/skill.md` | Document set scoping |

## New files

| File | What |
|------|------|
| `.claude/skills/current-document/skill.md` | `/current-document [name]` skill |

## Constraints

- Backward compatible: omitting `--name` works as before (uses default name)
- No new dependencies beyond what's already used
- `make clean` still wipes everything
- `make load-cached` restores a single default set

## Non-goals

- Cross-set search (search across all loaded sets at once)
- Set versioning or diffing
- Remote/shared document stores
