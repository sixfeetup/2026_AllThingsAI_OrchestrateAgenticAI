# Agent Orchestration Document Review Demo — Claude Desktop / Cowork Setup

This directory contains a document review pipeline demo for a conference talk
on building agentic AI systems. These instructions cover setup for
**Claude Desktop** (Cowork mode), not the Claude Code CLI.

## Document Source

The demo uses a real government RFP package:
`assets/1-RFP 20-020 - Original Documents.zip`
containing 17 documents (3 PDFs, 4 DOCX, 3 DOC, 4 XLSX, 1 XLS).

---

## Setup — Step by Step

### 1. Install prerequisites

You need `uv` (Python package runner) installed.

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
uv --version
```

### 2. Load document data

The MCP server reads from `demo/data/`. Load it before anything else:

```bash
cd demo

# Option A: Full parse from the archive
make load

# Option B: Restore from cache (instant, if pre-demo-setup was run)
make load-cached
```

Verify:

```bash
sqlite3 data/documents.db "SELECT COUNT(*) FROM clauses"
# Should return 97
```

### 3. Run the setup script (does everything else)

From the `demo/` directory:

```bash
make setup-desktop
```

This single command auto-detects all paths based on where you downloaded
the project, then:

1. **Verifies prerequisites** — checks for `uv`, `claude` CLI, Claude Desktop
2. **Writes MCP config** — adds the `document-review` server to Claude Desktop's
   global config at `~/Library/Application Support/Claude/claude_desktop_config.json`
   using the resolved absolute path to the MCP server script
3. **Copies skills** — installs all 6 skill directories into Claude Desktop's
   global skills folder at `~/Library/Application Support/Claude/skills/`
4. **Generates agent paste files** — creates ready-to-paste agent templates in
   `demo/generated/` for the Verifier and Drafter windows
5. **Loads data** — restores from cache if available

The script prints every resolved path so you can verify it got them right.

**After running, restart Claude Desktop.**

#### Verify MCP tools

Open a new Claude Desktop conversation and ask:

> "What MCP tools do you have available?"

You should see: `load_document`, `search_document`, `audit_document`,
`get_document_stats`, `list_criteria_files`, `read_criteria_file`.

If tools don't appear, check:

- Is `uv` on the PATH Claude Desktop inherits? (It may not source your
  `.zshrc`. Try adding uv's path to `/etc/paths.d/` or use an absolute
  path to `uv` in the Desktop config.)
- Does the MCP server script path printed by the setup script actually exist?
- Did you restart Claude Desktop?

### 4. Set up agent windows (Verifier + Drafter)

The setup script generated paste-ready agent templates. You need two
separate Claude Desktop conversations, each with different system instructions.

**Window A — Verifier:**

1. Open a new Claude Desktop conversation
2. Go to Project settings → Custom instructions
3. Paste the contents of `demo/generated/paste-verifier.md`
4. Quick copy to clipboard:
   ```bash
   cat demo/generated/paste-verifier.md | pbcopy
   ```
5. Verify MCP tools are available (ask "what tools do you have?")

**Window B — Drafter:**

1. Open another new Claude Desktop conversation
2. Go to Project settings → Custom instructions
3. Paste the contents of `demo/generated/paste-drafter.md`
4. Quick copy to clipboard:
   ```bash
   cat demo/generated/paste-drafter.md | pbcopy
   ```
5. Verify MCP tools are available

The paste files are copies of the agent templates at:
- `demo/.agents/verification-agent.md` → `demo/generated/paste-verifier.md`
- `demo/.agents/response-drafter-agent.md` → `demo/generated/paste-drafter.md`

---

## Available Skills (installed by setup script)

| Skill | Trigger | What it does |
|-------|---------|-------------|
| document-loader | `/load-document` | Extract zip, parse multi-format docs, load into SQLite + ChromaDB |
| document-search | `/search-document <query>` | Semantic + keyword search across all loaded documents |
| document-eval | `/eval-document [criteria]` | Evaluate against criteria file across full document package |
| document-audit | `/audit-document` | Show audit trail |
| cowork-review | `/cowork-review [archive-path]` | Orchestrate full multi-agent review pipeline |
| audlog | `/audlog` | View or add entries to the audit trail |

## Available MCP Tools (configured by setup script)

- `load_document` — extract and load a document archive
- `search_document` — dual semantic + keyword search across all documents
- `audit_document` — view audit trail
- `get_document_stats` — clause counts and flag distribution
- `list_criteria_files` / `read_criteria_file` — browse eval criteria

---

## Cowork Workflow

Multi-agent review using Claude Desktop:

1. **Load phase**: Use `load_document` tool (or `/load-document` skill) to ingest the archive
2. **Eval phase**: Apply criteria files via `search_document` + LLM judgment
3. **Verify phase**: In the Verifier window, challenge findings with adversarial review
4. **Draft phase**: In the Drafter window, produce response memo from verified findings
5. **Audit phase**: In any window, review the full trail with `audit_document`

All windows share the same SQLite + ChromaDB data stores, so audit entries
from one window are visible to others.

---

## Data Stores

- `demo/data/documents.db` — SQLite (clauses + audit_log tables)
- `demo/data/chroma/` — ChromaDB vector store
- Both are ephemeral — `make clean` removes them

## Constraints

- All deps via `uv run --with` (never pip install)
- Everything runs locally (no external services)
- The document archive is a real government RFP — handle with appropriate care

## Quick Reference — File Paths

All paths are auto-resolved by the setup script. These are relative to the
project root for reference:

| What | Relative Path |
|------|---------------|
| Demo root | `demo/` |
| Document archive | `demo/assets/1-RFP 20-020 - Original Documents.zip` |
| MCP server script | `demo/.agents/bin/document-mcp-server.py` |
| Skills source | `demo/.claude/skills/` |
| Agent templates | `demo/.agents/*.md` |
| Generated paste files | `demo/generated/paste-verifier.md`, `demo/generated/paste-drafter.md` |
| SQLite database | `demo/data/documents.db` |
| ChromaDB store | `demo/data/chroma/` |
| Setup script | `demo/script/setup-desktop.sh` |

Resolved destinations on the presenter's machine:

| What | Absolute Path |
|------|---------------|
| Desktop MCP config | `~/Library/Application Support/Claude/claude_desktop_config.json` |
| Desktop skills | `~/Library/Application Support/Claude/skills/` |

## Re-running setup

If you need to re-run the setup (e.g., after moving the project):

```bash
make setup-clean
make setup-desktop
```

This clears the stamp files and re-runs everything, re-resolving all paths.
