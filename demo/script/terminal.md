# Demo Script — Terminal (Claude Code CLI)

**Total:** ~18 min | **Interface:** Claude Code only | **Prereq:** `predemo.md` completed

---

## Flow

```
Slides 0-7 (intro)
  → Step 0: OH NO (prebaked naive review)
  → Step 0.5: Context pollution (bitrot generator)
Slides 8-10 (problem → oh no → control context)
  → Step 1: Roster
Slide 11 (memory & skills)
  → Step 2: Load
  → Step 3: Search
Slide 12 (search to assessment)
  → Step 4: Eval (IP)
  → Step 5: Eval (red flags)
  → Step 5.5: Naive contrast
  → Step 6.5: Bitrot (talk)
Slide 13 (more orchestration)
  → Step 7: Adversarial
  → Step 8: Draft
Slide 14 (show your work)
  → Step 9: Audit
  → Step 10: Pipeline
  → Step 11: Full Pipeline (composed)
Slides 15-17 (takehome → future → exit)
```

---

## Step 0 — OH NO (~1:30)

> SLIDE: After slide 7 (Orchestration), transition to demo

Show the prebaked naive review:

```
@assets/prebaked/naive-review.md

"This is what we got from paste-and-pray — a single prompt with no structure."
```

**Say:** "Notice: 'no critical red flags identified.' It missed everything. Vague, hedge-wordy, no section references. This is a context failure, not a model failure."

**Transition:** "We can do better. We need to control the context."

---

## Step 0.5 — Context Pollution (~0:30)

Inject noise to show what unmanaged context looks like:

```
!bitrot all --intensity 5 --seed 42
```

**Say:** "And this is what happens in a long session — tool outputs, tangents, contradictory instructions pile up. The context fills with noise. Watch what that does to quality."

> SLIDE: Show slides 8 (The Problem), 9 (OH NO), 10 (Control the Context)

---

## Step 1 — Roster (~1:00)

> SLIDE: Show slide 11 (Memory & Skills Demo)

```
Show me the skills in .claude/skills/ and agents in .agents/ — list each with a one-line description.
```

**Say:** "6 skills, 6 agents. Skills are capabilities — they DO things. Agents are perspectives — they bring a point of view. All markdown files. Readable, editable, version-controlled."

---

## Step 2 — Load (~1:30)

```
/load-document "assets/1-RFP 20-020 - Original Documents.zip"
```

**While loading, narrate:** "17 documents — PDFs, Word docs, spreadsheets. Watch it extract the zip, parse each by type, normalize into a common schema, and load into SQLite + ChromaDB. This is ETL, not prompt engineering."

**After load:** "97 clauses from 10 documents. Everything local — no document text leaves this machine."

**If slow:** `make load-cached`

---

## Step 3 — Search (~2:00)

```
/search-document "submission requirements"
```

**Say:** "Keyword match — results from five different source files."

```
/search-document "evaluation criteria scoring"
```

**Say:** "Semantic match — finds the evaluation procedure, scoring methodology, even the fractional rounding rules. Things you wouldn't find with grep."

```
/search-document "liability indemnification"
```

**Say:** "Cross-document — the contract template has indemnification terms AND the main RFP has compliance requirements. These need to be checked against each other."

---

## Step 4 — Focused Eval (~2:00)

> SLIDE: Show slide 12 (From search to assessment)

```
/eval-document assets/criteria/ip-and-ownership.md
```

**Say:** "Three criteria, each with what-to-look-for and red-flag indicators. This is the agent's test spec. Not 'review this document' — that's paste-and-pray. We're giving it acceptance criteria."

**Call out:** IP/ownership inconsistencies across the RFP requirements and contract template.

**Say:** "Criteria files are acceptance criteria. If you wouldn't ship code without test specs, don't review documents without eval criteria."

---

## Step 5 — Broad Eval (~1:30)

```
/eval-document assets/criteria/general-red-flags.md
```

**Say:** "Same tool, different spec. Six criteria scanning for dates, names, indemnification, buried terms, undefined obligations, hidden provisions."

**APPLAUSE MOMENT:** Cross-document contradictions — requirements in one document that conflict with terms in another.

**Say:** "Six criteria, 17 documents. The system cross-references everything. A single-prompt review cannot do this."

---

## Step 5.5 — Naive Contrast (~0:45)

```
@assets/prebaked/naive-review.md

Compare this to what we just found.
```

**Say:** "Remember Step 0? 'No critical red flags identified.' Now look — specific findings with evidence and section citations spanning multiple documents. Same LLM. The difference is context engineering."

---

## Step 6.5 — Bitrot (~1:30)

**Talk through** `assets/prebaked/bitrot-research.md` section 4 (before/after tables).

**Say:** "Context is a finite resource. 15-47% performance drop as context fills. This is why scoped agents with clean context outperform one long session. Session boundaries are a feature, not a bug."

Show: `/context` perhaps comparing to start or a new session

---

## Step 7 — Adversarial Review (~2:00)

> SLIDE: Show slide 13 (More orchestration)

```
Using the verification agent (.agents/verification-agent.md), challenge the findings from the evaluation. For each finding, construct the best counter-argument, then render a verdict: upheld, downgraded, or dismissed.

/eval-document {insert criterion} --adversarial
```

**Say:** "We've found issues. But are they real? The red team's job is to argue against every finding."

**APPLAUSE MOMENT:** When the adversary UPHOLDS a cross-document contradiction. Convergence = high confidence.

**Say:** "This is code review. A fresh perspective catches what the author missed — and confirms what the author got right."

---

## Step 8 — Draft Response (~1:00)

```
Using the response drafter agent (.agents/response-drafter-agent.md), draft a professional response memo based on the verified findings. Group by severity, suggest specific changes.
```

**Say:** "Different agent, different job — not analysis, but communication. Notice the tone shift: forensic → constructive. Same findings, different framing."

---

## Step 9 — Audit (~1:00)

> SLIDE: Show slide 14 (Show Your Work)

```
/audit-document
```

**APPLAUSE MOMENT:** Full provenance trail.

**Say:** "Every action logged. When someone asks 'how did you reach that conclusion,' this is the answer. This is your CI log for document review."

---

## Step 10 — Pipeline (~1:30)

Show pipeline diagram on slide:

```
data-loader → document-eval → verification → response-drafter
                   |
             data-investigator
```

**Say:** "Same skills, same agents — but the system drives the flow. Each agent gets clean context. This is why agent swarms beat single long sessions."

**Say:** "We ran each step manually. What if we compose the whole thing?"

---

## Step 11 — Full Pipeline (~3:00)

> SLIDE: Keep pipeline diagram visible

```
/cowork-review
```

**While running, narrate:** "One command. It loads the archive, runs both criteria files, challenges every finding, drafts the response, and logs everything. Same skills, same agents — but now the system drives the flow. No human in the loop until the report lands."

**After completion:** "Look at the audit trail. Every search, every eval, every verdict — all traceable. This is what production telemetry looks like for an agent system."

**If slow:** Let it run — the audience is watching the pipeline execute in real time. That IS the demo. If it takes more than 3 minutes, narrate what's happening at each stage.

> SLIDE: Return to slides 15 (Takehome), 16 (Future), 17 (/exit)

---

## Wrap-Up (~1:00)

**Say:**
- "Document review is just the domain. The patterns generalize."
- "Criteria files = test specs. Adversarial agents = code review. Audit trail = CI log."
- "There's a playbook in the repo — take it home, build your own."

---

## If Time Permits — Step 6: Edit & Re-eval (~1:30)

Insert between Step 5.5 and Step 6.5 if pacing is ahead.

```
Open assets/criteria/ip-and-ownership.md and add a 4th criterion: "Moral Rights Waiver" — look for any waiver of moral rights that is unlimited in scope or lacks geographic boundaries. Then re-run the eval.
```

**Say:** "We're not tweaking a prompt. We're adding a test case to a spec. This is TDD for agent systems."
