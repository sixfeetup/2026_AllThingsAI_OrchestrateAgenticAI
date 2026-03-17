# Demo Agents & Skills — Specification

**Goal:** Create a self-contained set of Claude Code skills and agent
prompt-templates that drive the live demo: load a document archive, evaluate
it against criteria, run adversarial review, and draft a response.

All artifacts live under `demo/` and are designed to be used from a
Claude Code session rooted at the `demo/` directory (or its parent with
`demo/` as working context).

---

## 1. Context & Fixtures

| Artifact | Path | Notes |
|---|---|---|
| Document archive | `assets/1-RFP 20-020 - Original Documents.zip` | Real government RFP package — 17 documents (3 PDFs, 4 DOCX, 3 DOC, 4 XLSX, 1 XLS) |
| Prebaked review | `assets/prebaked/contract-review-checklist.md` | Example output to show if live generation is slow |

### Runtime Data Stores

The demo uses two local stores, created at load time:

- **SQLite** (`demo/data/contracts.db`) — structured clause data
  (section number, title, body text, source file, metadata flags)
- **ChromaDB** (`demo/data/chroma/`) — vector embeddings of clause text
  for semantic search

Both are ephemeral — `make clean` removes them.

---

## 2. Skills

Skills are Claude Code skill files (`demo/.claude/skills/<name>/skill.md`).
Each skill is a self-contained capability the agent can invoke.

### 2.1 `contract-loader` — Extract, Parse, Schema, Load

**Trigger:** `/load-document <path-to-archive-or-pdf>`

**What it does:**
1. If the path is a ZIP archive, extract all documents to a temp directory.
2. Parse each document by type (PDF via PyMuPDF, DOCX via python-docx,
   XLSX/XLS via openpyxl, DOC via textract or fallback).
3. Apply a predefined schema:
   - `section_number` (str) — e.g. "4.1", "12.10"
   - `section_title` (str)
   - `body` (str) — full clause text
   - `source_file` (str) — original filename within the archive
   - `page_start` (int)
   - `page_end` (int)
   - `flags` (list[str]) — tags like `"ip"`, `"termination"`, `"staffing"`
4. Create/replace SQLite table `clauses` in `data/contracts.db`.
5. Create/replace ChromaDB collection `contract_clauses` with embeddings
   of each clause body (use default sentence-transformer model).
6. Print summary: document count, clause count, any parse warnings.

**Dependencies:** `uv run --with pymupdf,chromadb,sentence-transformers,python-docx,openpyxl`

**Schema DDL (SQLite):**
```sql
CREATE TABLE IF NOT EXISTS clauses (
    id            INTEGER PRIMARY KEY,
    section_number TEXT NOT NULL,
    section_title  TEXT,
    body           TEXT NOT NULL,
    source_file    TEXT,
    page_start     INTEGER,
    page_end       INTEGER,
    flags          TEXT  -- JSON array
);
```

### 2.2 `contract-search` — Search & Augment

**Trigger:** `/search-document <query>`

**What it does:**
1. Run semantic search against ChromaDB `contract_clauses` (top-k=10).
2. Run keyword/SQL search against SQLite `clauses` for exact matches.
3. Merge and deduplicate results, rank by combined score.
4. Return results as a formatted table: section number, source file, title,
   relevance score, and a truncated snippet (first 200 chars of body).

Results span all loaded documents in the archive.

**Options:**
- `--section <pattern>` — filter by section number glob (e.g. `4.*`)
- `--flag <tag>` — filter by flag
- `--source <filename>` — filter by source document
- `--full` — show full body text instead of snippet

### 2.3 `contract-eval` — Evaluate Against Criteria

**Trigger:** `/eval-document [criteria-file]`

**What it does:**
1. Load criteria from a markdown file (default:
   `assets/criteria/general-red-flags.md`
   or a custom criteria file). Each `## N. Title` heading is one criterion.
2. For each criterion:
   a. Use `contract-search` to find relevant clauses across all documents.
   b. Assess whether the issue described exists in the loaded documents.
   c. Rate severity: `CRITICAL`, `HIGH`, `MEDIUM`, `LOW`, `CLEAR`.
   d. Provide evidence (quote the clause text) and reasoning.
   e. Note which source document(s) the finding comes from.
3. Output a structured report in markdown:
   - Summary table (criterion, severity, source files, section refs)
   - Detailed findings per criterion
   - Overall risk score (count of CRITICAL/HIGH/MEDIUM)

**Options:**
- `--adversarial` — also generate counter-arguments for each finding
  (simulate opposing counsel's defense)
- `--model <model>` — override model for eval (enables using Gemini/Codex
  for adversarial cross-check)

### 2.4 `contract-audit` — Audit Trail & Provenance

**Trigger:** `/audit-document`

**What it does:**
1. Read the SQLite `audit_log` table (populated by other skills when they
   run).
2. Display a chronological log of all actions taken:
   - What was loaded, when, from which archive/file
   - Searches performed and result counts
   - Eval runs: criteria used, findings, severity counts
   - Any manual edits or overrides
3. Generate a provenance summary: which findings are supported by which
   evidence, and flag any findings that lack direct textual support.

**Audit log schema (SQLite):**
```sql
CREATE TABLE IF NOT EXISTS audit_log (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp  TEXT NOT NULL DEFAULT (datetime('now')),
    action     TEXT NOT NULL,  -- 'load', 'search', 'eval', 'draft'
    detail     TEXT,           -- JSON blob with action-specific data
    actor      TEXT            -- 'user', 'contract-eval', 'verifier', etc.
);
```

All other skills append to this table when they perform actions.

---

## 2.5 Criteria Files

Criteria files live in `assets/criteria/` and define what the eval
skill looks for. Each file is a markdown document where every `##`
heading is one criterion to evaluate. The eval skill iterates over
them, searches the documents, and reports findings.

Two criteria files ship with the demo:

### `ip-and-ownership.md` — Focused IP Criteria

A narrow, 3-criterion file used in the first eval pass to show
focused evaluation:

1. **Exclusive vs Non-Exclusive IP Assignment** — Do any clauses
   contradict each other on who owns the work product?
2. **Pre-Existing IP Protection** — Does the contract protect the
   consultant's pre-existing tools, frameworks, and libraries?
3. **License Scope Clarity** — Are license grants (scope, duration,
   exclusivity, transferability) explicitly defined or left to
   "mutual understanding"?

### `general-red-flags.md` — Broad Red Flag Scan

A broader, 6-criterion file used in the second eval pass:

1. **Impossible or Missing Dates** — Are there dates that don't exist
   or timelines that are undefined?
2. **Incorrect Party Names** — Do all references to parties use
   consistent, correct legal names?
3. **One-Sided Indemnification** — Is indemnification symmetric, or
   does one party bear disproportionate risk?
4. **Buried Material Terms** — Are important terms (auto-renewal,
   non-compete, etc.) placed in unexpected sections?
5. **Undefined Obligations** — Are performance obligations defined with
   measurable criteria, or left to "reasonable effort"?
6. **Hidden Unusual Provisions** — Are there any non-standard clauses
   buried in boilerplate sections?

---

## 3. Agent Prompt Templates

Agent templates are markdown files in `demo/.agents/` that define
persona, goals, and tool access for each agent role. During the demo
these are invoked via Claude Code's Agent tool or by setting system
context.

### 3.1 `contract-eval-agent`

**File:** `demo/.agents/contract-eval-agent.md`

**Role:** Primary document analyst. Methodically reviews each section
across all loaded documents for legal, financial, and operational risks.

**Behavior:**
- Uses `contract-search` to navigate the documents
- Uses `contract-eval` to apply criteria
- Produces a structured findings report
- Tags each finding with severity, affected party, and source document
- Does NOT suggest remediation (that's the response drafter's job)

**Persona prompt key points:**
- Act as an experienced contract analyst
- Be thorough but concise — cite section numbers and source files
- Flag anything unusual, even if not in the criteria file
- Maintain a skeptical, detail-oriented posture

### 3.2 `data-investigator-agent`

**File:** `demo/.agents/data-investigator-agent.md`

**Role:** Exploratory analyst. Performs open-ended investigation of
document data, looking for patterns, anomalies, and cross-document
contradictions.

**Behavior:**
- Uses `contract-search` with varied queries to explore the documents
- Cross-references clauses across documents to find contradictions
- Looks for hidden or buried provisions
- Reports findings as "leads" with confidence levels

**Persona prompt key points:**
- Act as a forensic investigator — follow the threads
- Don't stop at the obvious; dig into boilerplate sections and attachments
- Score confidence: `confirmed`, `likely`, `suspicious`, `speculative`

### 3.3 `data-loader-agent`

**File:** `demo/.agents/data-loader-agent.md`

**Role:** Data engineer. Handles ingestion of document archives into
the local data stores.

**Behavior:**
- Uses `contract-loader` skill to extract, parse, and load archives
- Validates loaded data (document count, clause count, coverage, parse quality)
- Reports any parsing issues (garbled text, missing sections, unsupported formats)
- Can reload or patch data if issues are found

**Persona prompt key points:**
- Focus on data quality and completeness
- Verify that all documents in the archive were captured
- Report statistics: total documents, total clauses, format breakdown

### 3.4 `verification-agent` (Adversarial Review)

**File:** `demo/.agents/verification-agent.md`

**Role:** Red team reviewer. Takes the eval agent's findings and
argues against them — looking for false positives, overstatements,
or missing context.

**Behavior:**
- Receives findings from `contract-eval-agent`
- For each finding, constructs a counter-argument:
  - Is this actually a problem, or standard industry practice?
  - Is the severity rating justified?
  - Is there exculpatory context elsewhere in the documents?
- Uses `contract-search` to find supporting/contradicting clauses
- Produces a "challenge report" with each finding either `upheld`,
  `downgraded`, or `dismissed`, with reasoning

**Persona prompt key points:**
- Act as opposing counsel defending the document
- Be rigorous but fair — don't dismiss legitimate issues
- The goal is to stress-test findings, not to rubber-stamp the documents

### 3.5 `response-drafter-agent`

**File:** `demo/.agents/response-drafter-agent.md`

**Role:** Business communicator. Takes verified findings and drafts a
professional response (letter or memo) based on the document review.

**Behavior:**
- Receives verified findings (post adversarial review)
- Groups issues by severity and topic
- Drafts a response document with:
  - Executive summary of concerns
  - Detailed findings with specific clause and document references
  - Recommended changes / redline suggestions
  - Prioritization (must-fix vs. nice-to-have)
- Tone: professional, constructive, firm on critical issues
- Uses `contract-audit` to include provenance references

**Persona prompt key points:**
- Write for a business audience, not a legal one
- Be specific: quote clause numbers, source documents, and text
- Suggest concrete alternatives, not just "this is bad"
- Maintain a collaborative tone — the goal is a better outcome, not
  a confrontation

---

## 4. Demo Flow

The demo has two phases: **interactive walkthrough** (step through each
piece manually, explain it) then **pipeline** (wire them together).

### Phase 1: Interactive Walkthrough

Each step is done manually in the Claude Code session. Pause between
steps to talk about what just happened.

| Step | Action | Talking Point |
|---|---|---|
| **1. Roster** | Show the skills and agents, explain what each does | Skills compound; agents are perspectives |
| **2. Load** | Run `/load-document "assets/1-RFP 20-020 - Original Documents.zip"` manually | Data quality, multi-format parsing, schema design, determinism |
| **3. Search** | Run `/search-document "submission requirements"` and a few other queries | Semantic vs keyword search, cross-document retrieval |
| **4. Eval (focused)** | Run `/eval-document assets/criteria/ip-and-ownership.md` — just the IP criteria | Good specs = good performance |
| **5. Eval (broad)** | Run `/eval-document assets/criteria/general-red-flags.md` — broader scan | Criteria files are the "spec" for the agent |
| **6. Edit & re-eval** | Live-edit a criteria file, re-run eval to show the difference | Iterating on specs, not on prompts |
| **7. Adversarial** | Run verification agent against the findings (optionally with Gemini/Codex) | Testing agent systems, red teaming |
| **8. Report** | Run response drafter on verified findings | Handoff between agents, final output |
| **9. Audit** | Run `/audit-document` to show the full trail | Provenance and trust |

### Phase 2: Pipeline (Improve)

Show how the same steps wire into an automated pipeline with routing
and handoffs:

```
┌─────────────┐     ┌──────────────┐     ┌───────────────┐
│ data-loader  │────▶│ contract-eval│────▶│  verification │
│   agent      │     │    agent     │     │    agent      │
└─────────────┘     └──────────────┘     └───────────────┘
                           │                      │
                    ┌──────▼──────┐         ┌──────▼──────┐
                    │    data     │         │  response   │
                    │investigator │         │   drafter   │
                    └─────────────┘         └─────────────┘
```

This demonstrates orchestration — same skills and agents, but now
the system drives the flow instead of the presenter.

---

## 5. File Layout

```
demo/
├── .claude/
│   └── skills/
│       ├── contract-loader/
│       │   └── skill.md
│       ├── contract-search/
│       │   └── skill.md
│       ├── contract-eval/
│       │   └── skill.md
│       └── contract-audit/
│           └── skill.md
├── .agents/
│   ├── contract-eval-agent.md
│   ├── data-investigator-agent.md
│   ├── data-loader-agent.md
│   ├── verification-agent.md
│   └── response-drafter-agent.md
├── assets/
│   ├── 1-RFP 20-020 - Original Documents.zip   ← real RFP package (17 docs)
│   ├── criteria/
│   │   ├── ip-and-ownership.md        ← focused: IP assignment & licensing
│   │   └── general-red-flags.md       ← broad: common document red flags
│   ├── gen-contract.py                ← legacy: generates fake PDF for testing
│   ├── playbook.md                    ← attendee take-home artifact
│   └── prebaked/
│       ├── contract-review-checklist.md
│       ├── naive-review.md            ← shallow single-prompt review for contrast
│       └── skill-example.md
├── data/                          ← created at runtime
│   ├── contracts.db
│   └── chroma/
├── Makefile
├── outline.md
└── spec.md                        ← this file
```

---

## 6. Key Demo Talking Points

Each artifact maps to a presentation theme:

| Artifact | Theme |
|---|---|
| Skills (composable, reusable) | Skills compound — each one makes the agent smarter |
| Agent templates (role-based) | Agents as specialized perspectives, not just LLM calls |
| Eval criteria in markdown | Good specs = good performance; determinism matters |
| Adversarial review agent | Testing agent systems — you need a red team |
| Audit trail | Provenance and trust — show your work |
| Pipeline handoffs | Routing and orchestration — agents as a team |

---

## 7. Supporting Materials

### `assets/playbook.md` — Attendee Take-Home

A self-contained guide attendees can use to replicate the approach in
their own domain. Sections:

1. **Criteria File Template** — how to structure eval criteria
2. **Agent Role Template** — how to define an agent persona and scope
3. **Orchestration Patterns** — when to use single agent, pipeline,
   or adversarial review
4. **Containment Checklist** — sandboxing, permissions, local data
5. **Engineering Parallels** — mapping document review patterns to
   code review, test planning, incident response

### `assets/prebaked/naive-review.md` — Contrast Example

A deliberately shallow document review (what a single generic LLM
prompt produces) to contrast with the structured agent output. Used
during the demo to show the difference between "ask ChatGPT" and a
structured agentic approach.

---

## 8. Constraints

- **No external services** — everything runs locally (SQLite, ChromaDB
  in-process, local embeddings via sentence-transformers).
- **All deps via uv** — no pip installs. Skills specify their deps in
  `uv run --with` invocations.
- **Real documents** — the demo uses a real government RFP package.
  No synthetic data or planted problems in the demo flow.
- **Presentation pacing** — each skill should produce visible output
  within ~10 seconds. Pre-baked outputs exist as fallbacks in
  `assets/prebaked/`.
