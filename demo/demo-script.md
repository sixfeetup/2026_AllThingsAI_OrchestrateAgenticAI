# Demo Script — Agentic Contract Review

**Total time:** ~18 minutes (adjust pacing based on audience energy)
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

# 2. Regenerate the contract PDF (ensures planted issues are present)
make contract

# 3. Verify the PDF exists and is non-trivial
ls -lh assets/contracts/bigco-msa.pdf

# 4. Verify Python deps will resolve (downloads models if needed)
uv run --with 'pymupdf,chromadb,sentence-transformers' python -c "import pymupdf; import chromadb; print('deps OK')"

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
# Type: /help — confirm /load-contract, /search-contract, /eval-contract, /audit-contract appear
# Exit the session
```

### Right before going on

```bash
cd demo
make clean          # fresh state, no leftover data/
make contract       # PDF ready
# Open Claude Code — leave it at the prompt, ready to go
claude
```

### Fallback kit

If anything stalls or breaks live, show the prebaked files:

| Situation | Show instead |
|---|---|
| Loading is slow (>15s) | `assets/prebaked/contract-review-checklist.md` (describe what would have loaded) |
| Eval is slow or incomplete | `assets/prebaked/contract-review-checklist.md` |
| Need naive contrast | `assets/prebaked/naive-review.md` |
| Bitrot demo inconclusive | Describe with the tables from `assets/prebaked/bitrot-research.md` section 4 |

---

## Phase 1: Interactive Walkthrough

### Step 1 — The Roster (~2 min)

**What to do:** Show the skill and agent files. Do NOT run anything yet.

**Commands:**
```
# In Claude Code, type:
Show me the skills in .claude/skills/ and agents in .agents/ — just list them with a one-line description of each.
```

**Talking points:**
- "Before we touch the contract, let me show you what we're working with"
- We have 4 skills (loader, search, eval, audit) and 5 agents (data-loader, eval, investigator, verification, response-drafter)
- Skills are capabilities — they do things. Agents are perspectives — they bring a point of view
- Skills compound: each one we add makes the whole system smarter
- These are all markdown files. Not code libraries, not API wrappers — readable instructions that tell the agent how to use Python scripts underneath
- **Engineering parallel:** This is like having a test suite (skills) and specialized reviewers (agents) — same tools, different expertise

**What audience sees:** List of skill and agent files with descriptions.

**Timing:** ~2 min

---

### Step 2 — Load the Contract (~2 min)

**What to do:** Load the contract PDF. Narrate the chunking as it happens.

**Command:**
```
/load-contract assets/contracts/bigco-msa.pdf
```

**Talking points:**
- This is a 30-page MSA between a fake company (L&LL LLC) and Six Feet Up
- Watch what happens: it parses the PDF into structured clauses, loads them into SQLite for exact search and ChromaDB for semantic search
- **Narrate the chunking:** "Notice it's splitting at clause boundaries, not arbitrary page chunks — clause-level granularity is critical for retrieval quality. If you chunk by page, a clause that spans pages gets split and you lose the meaning"
- Schema matters: section number, title, body text, page range, flags — this is data engineering, not prompt engineering
- **Containment callout #1:** "Everything is local — SQLite file and ChromaDB on disk. No contract text leaves this machine. We're using `uv run` for dependency isolation — no global pip installs"
- **Engineering parallel:** "This is an ETL pipeline — extract from PDF, transform into structured records, load into queryable stores"

**What audience sees:** Parse/load output with clause count, page count, confirmation of both stores populated.

**Fallback:** If loading takes >15 seconds, narrate what it's doing and show `assets/prebaked/contract-review-checklist.md` for the expected output shape.

**Timing:** ~2 min (including narration during load)

---

### Step 3 — Search the Contract (~2 min)

**What to do:** Run a few searches to show both semantic and keyword retrieval.

**Commands:**
```
/search-contract "intellectual property"
```

Wait for results, then:

```
/search-contract "who owns the work product"
```

Then one more:

```
/search-contract "cupcake"
```

**Talking points:**
- First search: keyword match — finds sections with "intellectual property" in the text
- Second search: semantic match — "who owns the work product" doesn't appear literally anywhere, but semantic search finds the IP assignment clauses. Same information, different query. This is why we have both stores
- Third search: this is a teaser — the audience will see something weird come back from the force majeure section. Don't explain it yet. Just say "Huh, that's interesting. We'll come back to that."
- **Engineering parallel:** "This is the same pattern as code search — sometimes you grep for the exact string, sometimes you need semantic understanding of what the code does"

**What audience sees:** Search results with section numbers, titles, relevance scores, and clause snippets. The cupcake search should surface Section 12.10.

**Timing:** ~2 min

---

### Step 4 — Focused Eval: IP Criteria (~2.5 min)

**What to do:** Run the eval with just the IP criteria file (3 criteria). This is the "good spec = good performance" moment.

**Command:**
```
/eval-contract assets/criteria/ip-and-ownership.md
```

**Talking points:**
- "Now we evaluate the contract against specific criteria. Not 'review this contract' — that's the naive approach. We're giving it a spec"
- Show the criteria file first if time permits: "Three criteria, each with what-to-look-for, why-it-matters, and red-flag indicators. This is the agent's test spec"
- **Key finding to call out:** The IP contradiction between Section 4.1 (exclusive assignment) and Section 12.12 (consultant retains, non-exclusive license). This should come back as CRITICAL
- "A good spec is how you get good performance out of agents. Vague instructions produce vague results. Specific criteria produce specific findings"
- **Engineering parallel:** "Criteria files are acceptance criteria. If you wouldn't ship code without test specs, don't review contracts without eval criteria"

**What audience sees:** Eval report with summary table showing severity ratings for 3 criteria, detailed findings with quoted evidence.

**Fallback:** Show `assets/prebaked/contract-review-checklist.md` — the CRITICAL findings section covers IP issues.

**Timing:** ~2.5 min (eval may take 15-30 seconds to run)

---

### Step 5 — Broad Eval: Red Flags (~2 min)

**What to do:** Run the eval with the broader criteria file (6 criteria).

**Command:**
```
/eval-contract assets/criteria/general-red-flags.md
```

**Talking points:**
- "Same tool, different spec — now we're scanning for general red flags"
- Call out findings as they appear:
  - Impossible date (Feb 30) — SHOULD be HIGH
  - Incorrect party name ("Six Feet Down") — SHOULD be HIGH
  - One-sided indemnification — "the consultant indemnifies for everything including the client's own misuse of deliverables"
  - Buried auto-renewal in General Provisions instead of Term and Termination
  - **APPLAUSE MOMENT: The cupcake clause** — "And there it is. Section 12.10, Force Majeure. 500 cupcakes per month, three seasonal varieties per quarter, and the obligation *survives* force majeure events. The pandemic can shut down the office but you still owe cupcakes"
- "Six criteria, seven planted problems, plus an easter egg. A single-prompt review missed most of these"

**What audience sees:** Eval report with 6 criteria evaluated, multiple HIGH and CRITICAL findings.

**Fallback:** Show `assets/prebaked/contract-review-checklist.md`.

**Timing:** ~2 min

---

### Step 5.5 — Naive Review Contrast (~1 min)

**What to do:** Show the prebaked naive review alongside the structured eval output.

**Command:**
```
# Show the naive review file
@assets/prebaked/naive-review.md

Compare this naive review with the structured eval we just ran. What did it miss?
```

**Talking points:**
- "This is what you get from a single prompt: 'review this contract for issues.' One page of hedge words"
- "May want to review" / "seems somewhat broad" / "no critical red flags were identified" — missed the IP contradiction, missed the impossible date, missed the wrong company name, missed the cupcakes
- "The structured approach found 7+ issues with evidence and section citations. The naive approach found vibes"
- **This is the core thesis:** The difference is not the model — it is the context engineering. Same LLM, wildly different results

**What audience sees:** Side-by-side contrast — vague naive review vs specific structured findings.

**Timing:** ~1 min

---

### Step 6 — Edit & Re-eval (~1.5 min)

**What to do:** Live-edit a criteria file to show iteration on specs, not prompts.

**Command:**
```
Open assets/criteria/ip-and-ownership.md and add a 4th criterion: "Moral Rights Waiver" — look for any waiver of moral rights that is unlimited in scope or lacks geographic boundaries. Then re-run the eval with the updated file.
```

**Talking points:**
- "We're not tweaking a prompt. We're adding a test case to a spec"
- "When you iterate on criteria files instead of prompt-engineering, your improvements are durable, version-controlled, and reviewable by your team"
- Show that the new criterion produces a new finding (the contract has an unlimited moral rights waiver)
- **Engineering parallel:** "This is TDD for agent systems. Write the criteria, run the eval, see what you find. Iterate on the criteria, not the prompt"

**What audience sees:** Edited criteria file, then re-run eval with 4 criteria showing the new finding.

**Timing:** ~1.5 min

---

### Step 6.5 — Context Bitrot Demo (~3 min)

**What to do:** Demonstrate context degradation and recovery.

**Option A — Live pollution (if time permits):**

Run many searches to fill context, then re-eval:
```
/search-contract "indemnification" --full
/search-contract "termination" --full
/search-contract "staffing" --full
/search-contract "deliverables" --full
/search-contract "liability" --full
/search-contract "confidentiality" --full
/search-contract "force majeure" --full
/search-contract "payment terms" --full
```
Then re-run:
```
/eval-contract assets/criteria/ip-and-ownership.md
```

**Option B — Prebaked comparison (recommended for time):**

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

**Recovery (if you did live pollution):**
```
/compact
```
Then re-run eval and show scores recover.

- "Session boundaries are a feature, not a bug. Compaction, sub-agent handoff, and structured checkpoints are how you manage context"
- **Key message:** "Context is managed, not magic. Good specs resist bitrot better than broad ones — fewer criteria means less context needed per evaluation"

**What audience sees:** Degraded eval output (missed findings, downgraded severities) vs fresh eval. Recovery after compaction.

**Fallback:** Talk through the visual tables in `assets/prebaked/bitrot-research.md` section 4 — the audience sees the summary table shrink. That IS the demo.

**Timing:** ~3 min

---

### Step 7 — Adversarial Review (~2.5 min)

**What to do:** Run the verification agent against the eval findings.

**Command:**
```
Using the verification agent (.agents/verification-agent.md), challenge the findings from the
IP evaluation. For each finding, construct the best counter-argument, then render a verdict:
upheld, downgraded, or dismissed.
```

**Talking points:**
- "We've found issues. But are they real? This is where we bring in the red team"
- The verification agent acts as opposing counsel — its job is to argue against every finding
- Watch for the counter-arguments: "Is this actually standard industry practice? Is there qualifying language elsewhere?"
- **APPLAUSE MOMENT: Convergence** — "Notice that the IP contradiction (4.1 vs 12.12) gets UPHELD even by the adversary. When multiple agents with different objectives reach the same conclusion, you have high-confidence findings"
- Some findings may get downgraded — that is the system working, not failing
- **Engineering parallel:** "This is code review. A fresh perspective catches what the author missed — and confirms what the author got right"
- **Containment callout #2:** "The verification agent gets clean context scoped to just the findings and the contract. No accumulated noise from earlier work"

**What audience sees:** Verification report with verdict for each finding — upheld/downgraded/dismissed with reasoning.

**Fallback:** Show the "Adversarial Analysis — Red Flags" section at the bottom of `assets/prebaked/contract-review-checklist.md`.

**Timing:** ~2.5 min

---

### Step 8 — Draft Response (~1.5 min)

**What to do:** Run the response drafter on verified findings.

**Command:**
```
Using the response drafter agent (.agents/response-drafter-agent.md), draft a professional
response memo to L&LL LLC based on the verified findings. Group by severity, suggest specific
changes, and maintain a collaborative tone.
```

**Talking points:**
- "Now we hand off to a different agent with a different job — not analysis, but communication"
- The response drafter groups findings, suggests specific alternative language, and writes for a business audience
- Notice the tone shift: the eval agent is skeptical and forensic, the drafter is constructive and collaborative. Same findings, different framing for a different audience
- "This is a real artifact you could send to a counterparty. Section references, quoted text, suggested changes"
- **Engineering parallel:** "Pipeline handoff — like CI/CD stages. Each stage has a defined input and output. The eval agent's output IS the drafter's input"

**What audience sees:** Professional response memo with executive summary, critical issues, high-priority concerns, and proposed next steps.

**Timing:** ~1.5 min

---

### Step 9 — Audit Trail (~1 min)

**What to do:** Show the full audit trail.

**Command:**
```
/audit-contract
```

**Talking points:**
- **APPLAUSE MOMENT: Full provenance** — "Every action is logged. When someone asks 'how did you reach that conclusion,' you have the answer. Which criteria were used, which clauses were searched, which findings were upheld or dismissed, and by whom"
- "In regulated industries, this isn't optional — it's a compliance requirement. But even if you're not regulated, this is how you build trust in agent systems"
- The audit trail is append-only — agents can't modify or delete earlier entries
- **Engineering parallel:** "CI logs. You can trace any deployment artifact back to the commit, the test run, the review. Same principle"

**What audience sees:** Chronological audit log with timestamps, actions, actors, and details.

**Timing:** ~1 min

---

## Phase 2: Pipeline (~2 min)

### Step 10 — Orchestration

**What to do:** Show how the manual steps wire into an automated pipeline.

**Command:**
```
Run the full contract review pipeline: use the data-loader agent to load
assets/contracts/bigco-msa.pdf, then the contract-eval agent to evaluate against both
criteria files, then the verification agent to challenge findings, then the response-drafter
agent to produce the final memo. Show the handoff between each stage.
```

**Talking points:**
- "Everything we just did manually in 15 minutes — same skills, same agents, but now the system drives the flow"
- Show the pipeline diagram (have it on a slide or draw it):
  ```
  data-loader -> contract-eval -> verification -> response-drafter
                      |
                data-investigator
  ```
- "Each agent gets clean context scoped to its task. The orchestrator manages the meta-state. This is why agent swarms beat single long sessions"
- **Orchestration decision framework:** "When do you use which pattern? Single agent for simple tasks. Pipeline for sequential stages. Adversarial review for high-stakes decisions. Swarm for independent subtasks. It's in the playbook"

**What audience sees:** Automated pipeline running through all stages with handoff output between each.

**Fallback:** If time is tight or execution is slow, describe the pipeline verbally with the diagram slide and reference the complete prebaked output in `assets/prebaked/contract-review-checklist.md`.

**Timing:** ~2 min

---

## Wrap-Up (~1 min)

### Playbook Handout

**What to say:**
- "Everything I showed you generalizes. Contract review is just the domain — the patterns work for code review, compliance audits, security analysis, incident response"
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

## Quick Reference: Planted Problems Cheat Sheet

Keep this handy in case you need to verify findings live.

| # | Problem | Section | Severity |
|---|---------|---------|----------|
| 1 | IP contradiction (exclusive vs non-exclusive) | 4.1 vs 12.12 | CRITICAL |
| 2 | Impossible date (Feb 30) | 2.5 | HIGH |
| 3 | Incorrect name ("Six Feet Down") | 12.13 | HIGH |
| 4 | Ambiguous timeframe ("promptly", "all deliberate speed") | 2.3 | MEDIUM |
| 5 | "Reasonable effort" used 3x without definition | 2.7 | MEDIUM |
| 6 | License scope deferred to "mutual understanding" | 4.3 | HIGH |
| 7 | "Adequate staffing" with no measurable criteria | 13.1 | MEDIUM |
| EE | 500 cupcakes/month in force majeure clause | 12.10 | (easter egg) |

---

## Timing Budget

| Step | Content | Time |
|---|---|---|
| 1 | Roster — show skills & agents | 2:00 |
| 2 | Load — parse PDF, narrate chunking | 2:00 |
| 3 | Search — semantic vs keyword, cupcake teaser | 2:00 |
| 4 | Eval (IP) — focused criteria, IP contradiction | 2:30 |
| 5 | Eval (red flags) — broad scan, cupcake reveal | 2:00 |
| 5.5 | Naive contrast — prebaked shallow review | 1:00 |
| 6 | Edit & re-eval — iterate on specs | 1:30 |
| 6.5 | Context bitrot — degradation and recovery | 3:00 |
| 7 | Adversarial — verification agent challenges findings | 2:30 |
| 8 | Response — draft memo from verified findings | 1:30 |
| 9 | Audit — full provenance trail | 1:00 |
| 10 | Pipeline — automated orchestration | 2:00 |
| — | Wrap-up / playbook mention | 1:00 |
| | **Total** | **~24:00** |

**To fit 18 minutes:** Cut or abbreviate steps 5.5, 6, and 6.5. The bitrot demo is the most cuttable for time — mention the concept, show a slide, move on.

**To fit 15 minutes:** Also abbreviate step 10 (describe pipeline, don't run it) and step 8 (mention the drafter exists, show prebaked output quickly).

---

## Applause Moments Summary

Mark these for emphasis — pause slightly, let the audience absorb.

1. **The cupcake clause** (Step 5) — Hidden 500 cupcakes/month obligation in force majeure. Gets a laugh and proves the system finds buried absurdities.

2. **Naive vs structured contrast** (Step 5.5) — "No critical red flags identified" vs 7 specific findings with evidence. The punchline of the whole talk.

3. **Adversarial convergence** (Step 7) — Multiple agents with opposing objectives reach the same conclusion on the IP contradiction. High-confidence finding through disagreement.

4. **The full audit trail** (Step 9) — Every search, every eval, every verdict logged with timestamps and actor identity. "Show your work" made tangible.

5. **Cupcake callback** (Step 8, if it appears in the response memo) — The drafted response to L&LL includes a polite note about the cupcake obligation. Comedy + professionalism.
