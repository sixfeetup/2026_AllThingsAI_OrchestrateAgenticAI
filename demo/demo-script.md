# Demo Script — Agentic Document Review

**Total time:** ~18:15 (adjust pacing based on audience energy)
**Setup:** Claude Code session rooted in `demo/` directory

---

## Pre-Show Setup & Reset

Run these before going onstage. Ideally 15 minutes before your slot.

### Pre-flight checks

```bash
# From repo root
cd demo

# 1. Clean slate — remove all generated artifacts
make clean

# 2. Verify the document archive exists
make document

# 3. Verify the zip is present and non-trivial
ls -lh "assets/1-RFP 20-020 - Original Documents.zip"

# 4. Verify Python deps will resolve (downloads models if needed)
uv run --with 'pymupdf,chromadb,sentence-transformers,python-docx,openpyxl' python -c "import pymupdf; import chromadb; print('deps OK')"

# 5. Pre-warm sentence-transformers model (avoids 30s cold start live)
make load
make clean

# 6. Verify prebaked fallback files exist
ls assets/prebaked/contract-review-checklist.md
ls assets/prebaked/naive-review.md

# 7. Verify criteria files exist
ls assets/criteria/ip-and-ownership.md
ls assets/criteria/general-red-flags.md

# 8. Open Claude Code session, verify skills are discovered
claude
# Type: /help — confirm /load-document, /search-document, /eval-document, /audit-document appear
# Exit the session
```

### Cached Data Load

A pre-populated `demo/data/` directory with SQLite + ChromaDB already loaded
is stored in `assets/prebaked/data-cache/`. If the live load fails or is slow,
the presenter can skip to exploring with:

```bash
# If live load fails, restore cached data:
cp -r assets/prebaked/data-cache/ data/
```

This lets you jump straight to search/eval/adversarial without waiting for load.
The `make load-cached` target does this automatically:

```bash
make load-cached   # copies prebaked data into place
```

### Right before going on

```bash
cd demo
make clean          # fresh state, no leftover data/
make document       # verify archive exists
# Open Claude Code — leave it at the prompt, ready to go
claude
```

### Fallback kit

If anything stalls or breaks live, show the prebaked files:

| Situation | Show instead |
|---|---|
| Loading is slow (>15s) | `make load-cached` to restore prebaked data, or show `assets/prebaked/contract-review-checklist.md` |
| Eval is slow or incomplete | `assets/prebaked/contract-review-checklist.md` |
| Need naive contrast | `assets/prebaked/naive-review.md` |
| Bitrot demo inconclusive | Describe with the tables from `assets/prebaked/bitrot-research.md` section 4 |

---

## Phase 1: Interactive Walkthrough

> SLIDE: Deliver outline slides 1–7 (intro, who am I, what is this about, where we are going, determinism, the tool, orchestration) before starting the demo

### Step 0 — The OH NO (~1.5 min)

**What to do:** Open Claude Desktop (or a fresh Claude session with polluted context). Paste a section of the RFP documents into the session. Ask a naive question. Get terrible results.

**What to do (live):**
1. Switch to Claude Desktop (have it open with some prior conversation visible — a polluted context)
2. Paste a section of one of the RFP documents (e.g., scope of work or evaluation criteria) into the chat
3. Type: "Review this for issues"
4. Let the audience see the response

**Fallback:** If Claude Desktop is not cooperating or time is tight, open the prebaked output:
```
@assets/prebaked/naive-review.md

"This is what we got when we pasted part of the document into a regular chat session and asked it to review."
```

**What the audience sees:** Vague, hedge-wordy output. Things like "may want to review," "seems somewhat broad," "no critical red flags were identified." A wall of non-committal language that misses everything important.

**Talking points:**
- "This is the default experience — paste and pray"
- "Notice the vague language: 'may want to review', 'seems somewhat broad'"
- "It missed contradictions between documents, inconsistent requirements, and buried conditions"
- "This is what happens when you dump a document into a polluted context with no structure"
- "We can do better. We need to control the context"

**Transition:** "So how do we fix this? We need to control the context. Let me show you what we're working with." Then proceed to Step 1 (Roster).

**Timing:** ~1.5 min

---

> SLIDE: Show "The problem" and "OH NO" slides, then "Control the Context" slide before proceeding

### Step 1 — The Roster (~1 min)

**What to do:** Show the skill and agent files. Do NOT run anything yet.

**Commands:**
```
# In Claude Code, type:
Show me the skills in .claude/skills/ and agents in .agents/ — just list them with a one-line description of each.
```

**Talking points:**
- "Before we touch the documents, let me show you what we're working with"
- We have 4 skills (loader, search, eval, audit) and 5 agents (data-loader, eval, investigator, verification, response-drafter)
- Skills are capabilities — they do things. Agents are perspectives — they bring a point of view
- Skills compound: each one we add makes the whole system smarter
- These are all markdown files. Not code libraries, not API wrappers — readable instructions that tell the agent how to use Python scripts underneath
- **Engineering parallel:** This is like having a test suite (skills) and specialized reviewers (agents) — same tools, different expertise

**What audience sees:** List of skill and agent files with descriptions.

**Timing:** ~1 min

---

> SLIDE: Show "Memory & Skills Demo" slide before proceeding

### Step 2 — Load the Document Archive (~1.5 min)

**What to do:** Load the RFP document archive. Narrate the extraction and parsing as it happens.

**Command:**
```
/load-document "assets/1-RFP 20-020 - Original Documents.zip"
```

**Talking points:**
- This is a real government RFP package — 17 documents: PDFs, Word docs, and spreadsheets
- Watch what happens: it extracts the zip, parses each document by type (PDF, DOCX, DOC, XLSX, XLS), and loads them all into SQLite for exact search and ChromaDB for semantic search
- **Narrate the extraction:** "Notice it's handling multiple file formats — PDFs, Word documents, spreadsheets — and normalizing everything into a common schema. Each document's sections are extracted at clause-level granularity"
- Schema matters: section number, title, body text, source file, page range, flags — this is data engineering, not prompt engineering
- **Containment callout #1:** "Everything is local — SQLite file and ChromaDB on disk. No document text leaves this machine. We're using `uv run` for dependency isolation — no global pip installs"
- **Engineering parallel:** "This is an ETL pipeline — extract from multiple document formats, transform into structured records, load into queryable stores"

**What audience sees:** Parse/load output with document count, clause count, confirmation of both stores populated.

**Fallback:** If loading takes >15 seconds, narrate what it's doing and show `assets/prebaked/contract-review-checklist.md` for the expected output shape. Or use `make load-cached` to restore prebaked data instantly.

**Timing:** ~1:30 (including narration during load)

---

### Step 3 — Search the Documents (~2 min)

**What to do:** Run a few searches to show both semantic and keyword retrieval across the full document package.

**Commands:**
```
/search-document "submission requirements"
```

Wait for results, then:

```
/search-document "evaluation criteria"
```

Then one more:

```
/search-document "insurance requirements"
```

**Talking points:**
- First search: keyword match — finds sections with "submission requirements" in the text
- Second search: semantic match — "evaluation criteria" finds not just sections titled that way, but also scoring rubrics and weighting factors buried in other documents. This is why we have both stores
- Third search: cross-document — insurance requirements might appear in a requirements doc, a spreadsheet of minimums, and a contract template. The system finds them all
- **Cross-document insight:** "Notice the results come from different files in the package — the search spans all 17 documents, not just one"
- **Engineering parallel:** "This is the same pattern as code search — sometimes you grep for the exact string, sometimes you need semantic understanding of what the code does"

**What audience sees:** Search results with section numbers, source files, titles, relevance scores, and clause snippets.

**Timing:** ~2 min

---

> SLIDE: Show "From search to assessment" slide before proceeding

### Step 4 — Focused Eval: IP Criteria (~2 min)

**What to do:** Run the eval with just the IP criteria file (3 criteria). This is the "good spec = good performance" moment.

**Command:**
```
/eval-document assets/criteria/ip-and-ownership.md
```

**Talking points:**
- "Now we evaluate the documents against specific criteria. Not 'review these documents' — that's the naive approach. We're giving it a spec"
- Show the criteria file first if time permits: "Three criteria, each with what-to-look-for, why-it-matters, and red-flag indicators. This is the agent's test spec"
- **Key finding to call out:** Look for inconsistencies in IP/ownership terms across documents — the RFP requirements, the contract template, and supplementary docs may contradict each other
- "A good spec is how you get good performance out of agents. Vague instructions produce vague results. Specific criteria produce specific findings"
- **Engineering parallel:** "Criteria files are acceptance criteria. If you wouldn't ship code without test specs, don't review documents without eval criteria"

**What audience sees:** Eval report with summary table showing severity ratings for 3 criteria, detailed findings with quoted evidence.

**Fallback:** Show `assets/prebaked/contract-review-checklist.md` — the CRITICAL findings section covers IP issues.

**Timing:** ~2 min (eval may take 15-30 seconds to run)

---

### Step 5 — Broad Eval: Red Flags (~1.5 min)

**What to do:** Run the eval with the broader criteria file (6 criteria).

**Command:**
```
/eval-document assets/criteria/general-red-flags.md
```

**Talking points:**
- "Same tool, different spec — now we're scanning for general red flags"
- Call out findings as they appear — with a real RFP package, genuine issues emerge:
  - Inconsistent dates or timelines across documents
  - Requirements in one document that contradict terms in another
  - One-sided indemnification or liability terms
  - Buried conditions in attachments that modify main document terms
  - Undefined obligations or ambiguous performance standards
- **APPLAUSE MOMENT: Cross-document contradictions** — "This is where it gets interesting. Watch the system find requirements in one document that directly conflict with terms in another. These are the issues that slip through when humans review documents one at a time"
- "Six criteria, applied across 17 documents. The system cross-references everything — a single-prompt review cannot do this"

**What audience sees:** Eval report with 6 criteria evaluated, findings spanning multiple documents.

**Fallback:** Show `assets/prebaked/contract-review-checklist.md`.

**Timing:** ~1:30

---

### Step 5.5 — Naive Review Contrast (~0:45)

**What to do:** Show the prebaked naive review alongside the structured eval output. Call back to Step 0.

**Command:**
```
# Show the naive review file
@assets/prebaked/naive-review.md

Compare this naive review with the structured eval we just ran. What did it miss?
```

**Talking points:**
- "Remember that first attempt? Here's what it produced next to what we just got"
- Pull up or reference the Step 0 output — "May want to review" / "seems somewhat broad" / "no critical red flags were identified"
- "The paste-and-pray approach missed cross-document contradictions, inconsistent requirements, and buried conditions. Our structured eval found them all with evidence and section citations"
- "The naive approach found vibes. The structured approach found actionable issues with provenance"
- **This is the core thesis:** The difference is not the model — it is the context engineering. Same LLM, wildly different results. The OH NO at the start was not a model failure; it was a context failure

**What audience sees:** Side-by-side contrast — vague naive review vs specific structured findings. The audience connects this back to the failed attempt they saw at the start.

**Timing:** ~0:45

---

### Step 6.5 — Context Bitrot Demo (~1.5 min)

**What to do:** Demonstrate context degradation using prebaked comparison. Do NOT do live pollution — use the prebaked data to keep this tight.

**Command:**
```
# Reference the bitrot research
"We've been working for a while in this session. Let me show you what happens
to eval quality as context fills up."
```

Then talk through the before/after tables from `assets/prebaked/bitrot-research.md` section 4.

**Talking points:**
- "Context is a scarce resource, not infinite memory. Even with 1M tokens, performance degrades"
- Every search result, every tangent, every tool call adds tokens. The middle of the context window gets neglected — this is "lost in the middle," confirmed by Stanford and Chroma research
- Show the numbers: 15-47% performance drop as context grows. At 32K tokens, most models are below 50% of short-context performance
- "This is why containment matters — scoped agents with clean context outperform one long session"
- "Session boundaries are a feature, not a bug. Compaction, sub-agent handoff, and structured checkpoints are how you manage context"
- **Key message:** "Context is managed, not magic. Good specs resist bitrot better than broad ones — fewer criteria means less context needed per evaluation"

**What audience sees:** Before/after tables showing degraded eval output (missed findings, downgraded severities) vs fresh eval.

**Fallback:** Talk through the visual tables in `assets/prebaked/bitrot-research.md` section 4 — the audience sees the summary table shrink. That IS the demo.

**Timing:** ~1:30

---

> SLIDE: Show "More orchestration" slide before proceeding

### Step 7 — Adversarial Review (~2 min)

**What to do:** Run the verification agent against the eval findings.

**Command:**
```
Using the verification agent (.agents/verification-agent.md), challenge the findings from the
evaluation. For each finding, construct the best counter-argument, then render a verdict:
upheld, downgraded, or dismissed.
```

**Talking points:**
- "We've found issues. But are they real? This is where we bring in the red team"
- The verification agent acts as opposing counsel — its job is to argue against every finding
- Watch for the counter-arguments: "Is this actually a problem, or standard RFP practice? Is the severity rating justified?"
- **APPLAUSE MOMENT: Convergence** — "Notice when the adversarial agent UPHOLDS a cross-document contradiction. When multiple agents with different objectives reach the same conclusion, you have high-confidence findings"
- Some findings may get downgraded — that is the system working, not failing
- **Engineering parallel:** "This is code review. A fresh perspective catches what the author missed — and confirms what the author got right"
- **Containment callout #2:** "The verification agent gets clean context scoped to just the findings and the documents. No accumulated noise from earlier work"

**What audience sees:** Verification report with verdict for each finding — upheld/downgraded/dismissed with reasoning.

**Fallback:** Show the "Adversarial Analysis — Red Flags" section at the bottom of `assets/prebaked/contract-review-checklist.md`.

**Timing:** ~2 min

---

### Step 8 — Draft Response (~1 min)

**What to do:** Run the response drafter on verified findings.

**Command:**
```
Using the response drafter agent (.agents/response-drafter-agent.md), draft a professional
response memo based on the verified findings. Group by severity, suggest specific
changes, and maintain a collaborative tone.
```

**Talking points:**
- "Now we hand off to a different agent with a different job — not analysis, but communication"
- The response drafter groups findings, suggests specific alternative language, and writes for a business audience
- Notice the tone shift: the eval agent is skeptical and forensic, the drafter is constructive and collaborative. Same findings, different framing for a different audience
- "This is a real artifact you could send as a response to the RFP issuer or include in your bid. Section references, quoted text, suggested clarifications"
- **Engineering parallel:** "Pipeline handoff — like CI/CD stages. Each stage has a defined input and output. The eval agent's output IS the drafter's input"

**What audience sees:** Professional response memo with executive summary, critical issues, high-priority concerns, and proposed next steps.

**Timing:** ~1 min

---

> SLIDE: Show "Show Your Work" slide before proceeding

### Step 9 — Audit Trail (~1 min)

**What to do:** Show the full audit trail.

**Command:**
```
/audit-document
```

**Talking points:**
- **APPLAUSE MOMENT: Full provenance** — "Every action is logged. When someone asks 'how did you reach that conclusion,' you have the answer. Which criteria were used, which clauses were searched, which findings were upheld or dismissed, and by whom"
- "In regulated industries, this isn't optional — it's a compliance requirement. But even if you're not regulated, this is how you build trust in agent systems"
- The audit trail is append-only — agents can't modify or delete earlier entries
- **Engineering parallel:** "CI logs. You can trace any deployment artifact back to the commit, the test run, the review. Same principle"

**What audience sees:** Chronological audit log with timestamps, actions, actors, and details.

**Timing:** ~1 min

---

## Phase 2: Pipeline (~1.5 min)

### Step 10 — Orchestration (~1.5 min)

**What to do:** Describe how the manual steps wire into an automated pipeline. Show the diagram on a slide and talk through the flow — do NOT run the full pipeline live (too slow for the time budget).

**Talking points:**
- "Everything we just did manually — same skills, same agents, but now the system drives the flow"
- Show the pipeline diagram (have it on a slide):
  ```
  data-loader -> document-eval -> verification -> response-drafter
                      |
                data-investigator
  ```
- "Each agent gets clean context scoped to its task. The orchestrator manages the meta-state. This is why agent swarms beat single long sessions"
- **Orchestration decision framework:** "When do you use which pattern? Single agent for simple tasks. Pipeline for sequential stages. Adversarial review for high-stakes decisions. Swarm for independent subtasks. It's in the playbook"
- Reference the complete prebaked output in `assets/prebaked/contract-review-checklist.md` for what the full pipeline produces

**What audience sees:** Pipeline diagram slide with agent flow. Verbal walkthrough of how each stage hands off to the next.

**Timing:** ~1:30

---

> SLIDE: Return to slides for "Takehome", "Your Future is Agentic", and "/exit" slides

## Wrap-Up (~1 min)

### Playbook Handout

**What to say:**
- "Everything I showed you generalizes. Document review is just the domain — the patterns work for code review, compliance audits, security analysis, incident response"
- "There's a playbook artifact in the repo — `assets/playbook.md` — with templates for criteria files, agent roles, orchestration patterns, and a containment checklist"
- "The engineering parallels are explicit: criteria files are test specs, adversarial agents are code review, the audit trail is your CI log, pipeline handoffs are CD stages"
- "You can take this home and build your own version for your domain"

### Key Takeaways (if you have 30 seconds)

- Context engineering > prompt engineering
- Skills compound, agents are perspectives
- Good specs = good performance (criteria files, not prompt tweaking)
- Test your agent systems (adversarial review, convergence)
- Context is managed, not magic (bitrot is real, containment matters)
- Show your work (audit trail, provenance)

---

## Quick Reference: Real Document Discovery

This is a real government RFP package, not a synthetic document with planted
problems. The demo discovers genuine issues and contradictions across the 17
documents in the archive. Key areas where real findings tend to emerge:

| Area | What to watch for |
|---|---|
| Cross-document contradictions | Requirements in one doc that conflict with terms in another |
| Inconsistent terminology | Different names or definitions used across documents |
| Buried conditions | Material terms in attachments that modify the main RFP |
| Ambiguous requirements | Obligations without measurable criteria |
| Missing cross-references | Documents that reference sections that don't exist or are numbered differently |
| Timeline issues | Dates or deadlines that are inconsistent across documents |

The "wow" moment is finding genuine contradictions that span multiple
documents — issues that are nearly impossible to catch reviewing documents
one at a time.

---

## Timing Budget

| Step | Content | Time |
|---|---|---|
| 0 | OH NO — paste-and-pray failure in Claude Desktop | 1:30 |
| 1 | Roster — show skills & agents | 1:00 |
| 2 | Load — extract zip, parse multi-format documents, narrate pipeline | 1:30 |
| 3 | Search — semantic vs keyword across 17 documents | 2:00 |
| 4 | Eval (IP) — focused criteria, cross-document IP findings | 2:00 |
| 5 | Eval (red flags) — broad scan, cross-document contradictions | 1:30 |
| 5.5 | Naive contrast — callback to Step 0 | 0:45 |
| 6.5 | Context bitrot — prebaked comparison only | 1:30 |
| 7 | Adversarial — verification agent challenges findings | 2:00 |
| 8 | Response — draft memo from verified findings | 1:00 |
| 9 | Audit — full provenance trail | 1:00 |
| 10 | Pipeline — describe + diagram, don't run live | 1:30 |
| — | Wrap-up / playbook mention | 1:00 |
| | **Total** | **~18:15** |

**To fit 15 minutes:** Abbreviate step 10 (mention pipeline exists, skip diagram walkthrough), shorten step 8 (show prebaked output only), and trim step 6.5 to a single slide mention. Step 0 can be shortened to ~45s by going straight to the prebaked fallback.

---

## If Time Permits

### Step 6 — Edit & Re-eval (bonus ~1.5 min)

**When to use:** If pacing is ahead of schedule after Step 5.5, insert this before Step 6.5.

**What to do:** Live-edit a criteria file to show iteration on specs, not prompts.

**Command:**
```
Open assets/criteria/ip-and-ownership.md and add a 4th criterion: "Moral Rights Waiver" — look for any waiver of moral rights that is unlimited in scope or lacks geographic boundaries. Then re-run the eval with the updated file.
```

**Talking points:**
- "We're not tweaking a prompt. We're adding a test case to a spec"
- "When you iterate on criteria files instead of prompt-engineering, your improvements are durable, version-controlled, and reviewable by your team"
- Show that the new criterion produces a new finding
- **Engineering parallel:** "This is TDD for agent systems. Write the criteria, run the eval, see what you find. Iterate on the criteria, not the prompt"

**What audience sees:** Edited criteria file, then re-run eval with 4 criteria showing the new finding.

---

## Applause Moments Summary

Mark these for emphasis — pause slightly, let the audience absorb.

1. **Cross-document contradictions** (Step 5) — The system finds requirements in one document that directly conflict with terms in another. This is the "impossible to catch by hand" moment that proves the value of multi-document analysis.

2. **Naive vs structured contrast** (Step 0 + Step 5.5) — The audience saw the failure at the start; now they see the payoff. "No critical red flags identified" vs specific findings with evidence spanning multiple documents. The punchline of the whole talk.

3. **Adversarial convergence** (Step 7) — Multiple agents with opposing objectives reach the same conclusion on critical findings. High-confidence finding through disagreement.

4. **The full audit trail** (Step 9) — Every search, every eval, every verdict logged with timestamps and actor identity. "Show your work" made tangible.

5. **Real document, real findings** (throughout) — This is not a synthetic demo. These are genuine issues discovered in a real government RFP package. The system finds things humans miss.
