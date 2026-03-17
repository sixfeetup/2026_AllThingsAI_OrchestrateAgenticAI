# Implementation Plan — Demo Agents & Skills

**Source spec:** `demo/spec.md`
**Checklist cross-ref:** `presentation/checklist.md`

---

## Architecture Decision: Skills vs Scripts

Claude Code skills are **markdown instruction files** — they tell the
agent *what to do*, not *how to do it* in code. The actual heavy lifting
(document extraction, parsing, DB loading, vector search) lives in
**Python scripts** in `.agents/bin/`. Skills reference these scripts
via `uv run`.

This separation means:
- Skills are readable, editable, demo-friendly markdown
- Scripts are deterministic Python — no LLM in the data path
- The agent orchestrates; the scripts execute

---

## Implementation Order

Work is ordered by dependency. Items within a phase are independent
and can be built concurrently.

### Phase 1: Data Layer (scripts)

**No dependencies. Pure Python. Can be tested independently.**

#### 1.1 `contract-parse.py` — Document → structured JSON

- **File:** `.agents/bin/contract-parse.py`
- **Input:** path to document (PDF, DOCX, DOC) or ZIP archive
- **Output:** JSON array of clause objects (section_number, title, body,
  source_file, page_start, page_end)
- **Deps:** `pymupdf`, `python-docx`, `openpyxl` (via `uv run --with`)
- **Approach:** Detect file type. For ZIPs, extract and process each
  document. For PDFs, use PyMuPDF. For DOCX, use python-docx. For
  spreadsheets, use openpyxl. Split on section heading patterns. Assign
  flags heuristically (keyword matching).
- **Test:** Run against `assets/1-RFP 20-020 - Original Documents.zip`,
  verify all documents are captured, spot-check clause bodies.

#### 1.2 `contract-load.py` — JSON → SQLite + ChromaDB

- **File:** `.agents/bin/contract-load.py`
- **Input:** JSON from parse step (or path to archive — can call parse
  internally)
- **Output:** populated `data/contracts.db` and `data/chroma/`
- **Deps:** `chromadb`, `sentence-transformers` (via uv)
- **Creates both tables:** `clauses` and `audit_log`
- **Logs:** writes a `load` entry to `audit_log`
- **Test:** Load the archive, query SQLite for clause count, verify
  ChromaDB collection exists.

#### 1.3 `contract-search.py` — Query both stores

- **File:** `.agents/bin/contract-search.py`
- **Input:** query string, optional flags (--section, --flag, --source, --full)
- **Output:** formatted table to stdout
- **Approach:** Semantic search (ChromaDB top-k=10) + SQL LIKE search,
  merge and deduplicate by section_number, sort by score.
- **Logs:** writes a `search` entry to `audit_log`
- **Test:** Load archive, search "submission requirements", verify
  relevant sections appear in results.

### Phase 2: Content (markdown — no code deps)

**Can run in parallel with Phase 1.**

#### 2.1 `assets/criteria/ip-and-ownership.md`

3 criteria (spec 2.5). Each criterion is a `##` heading with:
- What to look for
- Why it matters
- What a problematic clause looks like

#### 2.2 `assets/criteria/general-red-flags.md`

6 criteria (spec 2.5). Same format.

#### 2.3 `assets/prebaked/naive-review.md`

Deliberately shallow document review — what you'd get from a single
generic LLM prompt like "review this document for issues." Should:
- Miss cross-document contradictions
- Use vague language ("seems fine", "may want to review")
- Lack section references and evidence
- Be ~1 page (vs the structured review's ~5 pages)

Purpose: contrast artifact for the demo. Shows why structured
agent approach matters.

#### 2.4 `assets/playbook.md`

Attendee take-home. Sections (from spec 7):
1. **Criteria File Template** — blank template + worked example
2. **Agent Role Template** — blank template + worked example
3. **Orchestration Patterns** — decision framework: when single agent
   vs pipeline vs adversarial review
4. **Containment Checklist** — sandboxing (uv), scoped permissions,
   local-only data stores, audit trail
5. **Engineering Parallels** — explicit mapping table:
   - Criteria files :: test specs / acceptance criteria
   - Adversarial agent :: code review / QA
   - Audit trail :: CI logs / compliance records
   - Pipeline handoffs :: CI/CD stages
   - Data loader :: ETL / data pipeline

### Phase 3: Skills (markdown)

**Depends on Phase 1 scripts existing.**

Each skill is a `skill.md` file instructing the agent when/how to
invoke the underlying script and present results.

#### 3.1 `contract-loader` skill

- **File:** `demo/.claude/skills/contract-loader/skill.md`
- **References:** `.agents/bin/contract-parse.py`,
  `.agents/bin/contract-load.py`
- **Trigger:** `/load-document`
- **Key instruction:** extract archive, parse each document by format,
  load all into stores, then report summary stats.

#### 3.2 `contract-search` skill

- **File:** `demo/.claude/skills/contract-search/skill.md`
- **References:** `.agents/bin/contract-search.py`
- **Trigger:** `/search-document`

#### 3.3 `contract-eval` skill

- **File:** `demo/.claude/skills/contract-eval/skill.md`
- **This is LLM-heavy** — the agent reads criteria, uses search for
  evidence, then applies judgment.
- **References:** search script, criteria files
- **Trigger:** `/eval-document`
- **Key instruction:** iterate criteria headings, search across all
  loaded documents for each, rate severity, produce report.

#### 3.4 `contract-audit` skill

- **File:** `demo/.claude/skills/contract-audit/skill.md`
- **References:** SQLite `audit_log` table (simple SQL query)
- **Trigger:** `/audit-document`

### Phase 4: Agent Templates (markdown)

**Depends on Phase 3 (agents reference skills by name).**

All five agents in `demo/.agents/`. Each ~30-50 lines: persona,
goals, available skills, output format, constraints.

#### 4.1 `data-loader-agent.md`
#### 4.2 `contract-eval-agent.md`
#### 4.3 `data-investigator-agent.md`
#### 4.4 `verification-agent.md`
#### 4.5 `response-drafter-agent.md`

### Phase 5: Makefile & Wiring

**Depends on everything above.**

#### 5.1 Update `demo/Makefile`

Targets:
- `document` — verify the document archive exists
- `load` — run contract-load against the archive
- `search` — convenience wrapper for contract-search
- `clean` — remove `data/` directory
- `reset` — clean + load

#### 5.2 Add `data/` to `.gitignore`

Runtime artifacts should not be committed.

---

## Dependency Graph & Parallelism

```
Phase 1 (scripts)              Phase 2 (content)
┌──────────────────┐           ┌──────────────────────┐
│ 1.1 parse script │           │ 2.1 ip-criteria      │
└────────┬─────────┘           │ 2.2 red-flags        │
         │                     │ 2.3 naive-review     │
    ┌────▼────┐                │ 2.4 playbook         │
    │ 1.2 load│                └──────────────────────┘
    └────┬────┘                         │
         │                              │
    ┌────▼──────┐                       │
    │ 1.3 search│                       │
    └────┬──────┘                       │
         │                              │
         ▼                              ▼
Phase 3 (skills) ◄──────────────────────┘
┌──────────────────────────────────────┐
│ 3.1 loader  3.2 search              │
│ 3.3 eval    3.4 audit    (parallel) │
└────────────────┬─────────────────────┘
                 │
                 ▼
Phase 4 (agents)
┌──────────────────────────────────────┐
│ 4.1-4.5 all five agents  (parallel) │
└────────────────┬─────────────────────┘
                 │
                 ▼
Phase 5 (wiring)
┌──────────────────────────────────────┐
│ 5.1 Makefile   5.2 gitignore        │
└──────────────────────────────────────┘
```

**Concurrent groups:**
- Phase 1 + Phase 2 run in parallel
- Within Phase 1: 1.1 first, then 1.2+1.3 in parallel
- Within Phase 2: all four items in parallel
- Phase 3: all four skills in parallel (after Phase 1 + 2)
- Phase 4: all five agents in parallel
- Phase 5: both items in parallel

---

## Risk / Complexity Notes

1. **ChromaDB + sentence-transformers cold start** — first `uv run`
   downloads ~400MB of model weights. Pre-download in Makefile or note
   in demo prep. Pre-baked `data/` directory as fallback.

2. **Multi-format parsing** — the archive contains PDFs, DOCX, legacy
   DOC, XLSX, and XLS files. The parse script must handle each format
   gracefully and fall back (e.g., skip DOC files if textract is
   unavailable, with a warning).

3. **Eval skill is the most complex** — only skill where LLM does
   substantive reasoning. Keep criteria files tight and specific.

4. **Skill discovery path** — Claude Code finds skills in `.claude/skills/`
   relative to working directory. Demo session must be rooted in `demo/`,
   or symlink skills into repo-root `.claude/skills/`.

5. **Naive review must be believably bad** — it needs to look like a
   plausible LLM output, not a strawman. Miss things through lack of
   structure, not through being obviously dumb.

6. **Filename with spaces** — the archive path contains spaces
   (`1-RFP 20-020 - Original Documents.zip`). All Makefile targets
   and skill commands must quote this path properly.
