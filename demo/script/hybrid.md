# Demo Script — Hybrid (Claude Desktop + Claude Code)

**Total:** ~18 min | **Interface:** Desktop for OH NO + cowork, Code for everything else
**Prereq:** `predemo.md` completed, Claude Desktop configured with `.mcp.json`

---

## Why Hybrid

Three interfaces, each for what it does best:

| Phase | Interface | Why |
|-------|-----------|-----|
| Step 0 | Claude Desktop | Natural — paste into chat, get bad output. Relatable. |
| Steps 1-9 | Claude Code CLI | Deterministic, scriptable, skill-driven. The engineering story. |
| Step 10 | Claude Desktop (2 windows) | Live multi-agent cowork. The "future" moment. |

The interface switch itself is a talking point: *"We started in chat because that's where everyone starts. We moved to CLI because engineering requires structure. Now we're back in chat — but with structure underneath."*

---

## Pre-Setup (Claude Desktop)

Before going onstage, have three Claude Desktop windows ready:

1. **Window 1: "Polluted"** — a session with some prior unrelated conversation. This is the Step 0 window.
2. **Window 2: "Verifier"** — fresh session. Paste the verification agent persona from `.agents/verification-agent.md` into the project instructions.
3. **Window 3: "Drafter"** — fresh session. Paste the response-drafter persona from `.agents/response-drafter-agent.md` into the project instructions.

Windows 2 and 3 are for Step 10. Keep them minimized until then.

Verify MCP tools are available in all windows:
- Ask "what tools do you have?" — should list `load_document`, `search_document`, `audit_document`, etc.

Also have Claude Code open in a terminal, rooted in `demo/`.

---

## Flow

```
Slides 0-7 (intro)
  → Step 0: OH NO [CLAUDE DESKTOP — Window 1]
Slides 8-10 (problem → oh no → control context)
  ← Switch to Claude Code terminal →
  → Step 1: Roster
Slide 11 (memory & skills)
  → Step 2: Load
  → Step 3: Search
Slide 12 (search to assessment)
  → Step 4: Eval (IP)
  → Step 5: Eval (red flags)
  → Step 5.5: Naive contrast
  → Step 6.5: Bitrot
Slide 13 (more orchestration)
  → Step 7: Adversarial
  → Step 8: Draft
Slide 14 (show your work)
  → Step 9: Audit
  ← Switch to Claude Desktop — Windows 2+3 →
  → Step 10: Cowork Pipeline [CLAUDE DESKTOP]
Slides 15-17 (takehome → future → exit)
```

---

## Step 0 — OH NO in Claude Desktop (~1:30)

**Window 1** (polluted session — prior conversation visible)

Paste a section of the RFP (scope of work or evaluation criteria) into the chat.

Type: **"Review this for issues"**

Let the audience see the response stream in. It will be vague, hedge-wordy — "may want to review," "seems somewhat broad," "no critical red flags."

**Say:** "This is the default experience — paste and pray. It missed everything. Polluted context, no structure, no criteria. We can do better."

**Transition:** "Let me show you what 'better' looks like."

> SLIDE: Show slides 8-10

**Switch to Claude Code terminal.**

---

## Steps 1-9 — Claude Code CLI

*(These are identical to `terminal.md` — same commands, same talking points)*

### Step 1 — Roster (~1:00)

```
Show me the skills in .claude/skills/ and agents in .agents/ — list each with a one-line description.
```

### Step 2 — Load (~1:30)

```
/load-document "assets/1-RFP 20-020 - Original Documents.zip"
```

### Step 3 — Search (~2:00)

```
/search-document "submission requirements"
/search-document "evaluation criteria scoring"
/search-document "liability indemnification"
```

### Step 4 — Focused Eval (~2:00)

```
/eval-document assets/criteria/ip-and-ownership.md
```

### Step 5 — Broad Eval (~1:30)

```
/eval-document assets/criteria/general-red-flags.md
```

### Step 5.5 — Naive Contrast (~0:45)

```
@assets/prebaked/naive-review.md
Compare this to what we just found.
```

**Say:** "Remember Step 0 in Claude Desktop? Same LLM. The difference is context engineering."

### Step 6.5 — Bitrot (~1:30)

Talk through `assets/prebaked/bitrot-research.md` before/after tables.

### Step 7 — Adversarial (~2:00)

```
Using the verification agent (.agents/verification-agent.md), challenge the findings.
```

### Step 8 — Draft Response (~1:00)

```
Using the response drafter agent (.agents/response-drafter-agent.md), draft a response memo.
```

### Step 9 — Audit (~1:00)

```
/audit-document
```

---

## Step 10 — Cowork Pipeline in Claude Desktop (~1:30)

> SLIDE: Show slide 13 (More orchestration)

**This is the moment.** Instead of describing the pipeline on a slide, show it live.

**Switch to Claude Desktop.** Arrange Windows 2 and 3 side by side (or tile them).

The data is already loaded (from Step 2 in CLI). Both Desktop windows share the same SQLite DB.

### Window 2: Verifier

Type: **"The evaluator found these issues in the RFP. Review the audit trail, then challenge each finding — is it real, or standard practice?"**

The verifier will call `audit_document` to see what was found, then `search_document` to look for counter-evidence, and render verdicts.

### Window 3: Drafter

Once the verifier has rendered verdicts, switch to Window 3.

Type: **"Check the audit trail for the verified findings, then draft a professional response memo grouping issues by severity."**

The drafter calls `audit_document`, reads the verified findings, and produces the memo.

**Say:** "You're watching three agents coordinate through a shared database. The evaluator in the CLI did the analysis. The verifier in this window challenged it. The drafter in that window is producing the deliverable. Same tools, different perspectives — and every action logged to the audit trail."

### Show the shared audit trail

In either window:

Type: **"Show me the complete audit trail"**

The audit trail now has entries from the CLI session AND both Desktop windows — all with different actor names, all timestamped, all traceable.

**APPLAUSE MOMENT:** The audit trail shows entries from three different agents across two different interfaces, all sharing the same data. *"This is orchestration — not a diagram, not a hypothetical. You just watched it happen."*

**Say:** "We started in chat because that's where everyone starts. We moved to CLI because engineering requires structure. Now we're back in chat — but with structure underneath. The agents don't care which interface they're in. The skills, the data stores, and the audit trail connect everything."

> SLIDE: Return to slides 15-17

---

## Wrap-Up (~1:00)

Same as terminal script:

- "Document review is just the domain. The patterns generalize."
- "Criteria files = test specs. Adversarial agents = code review. Audit trail = CI log."
- "Playbook in the repo — take it home."

---

## Fallback: If Cowork Fails

If Claude Desktop can't connect to the MCP server or the cowork segment isn't working:

1. Stay in Claude Code for Steps 7-8 (already have adversarial + draft commands ready)
2. Show the pipeline diagram on a slide for Step 10
3. Show the audit trail from the CLI session
4. **Say:** "In production, these agents run as separate instances sharing a database. Time doesn't permit a full live demo, but the architecture is the same — each agent gets clean context, and the audit trail connects everything."

This is a graceful degradation to the terminal-only script. The audience never knows there was a cowork segment planned.

---

## Timing Budget

| Step | Content | Interface | Time |
|------|---------|-----------|------|
| 0 | OH NO | Desktop | 1:30 |
| 1 | Roster | Code | 1:00 |
| 2 | Load | Code | 1:30 |
| 3 | Search | Code | 2:00 |
| 4 | Eval (IP) | Code | 2:00 |
| 5 | Eval (red flags) | Code | 1:30 |
| 5.5 | Naive contrast | Code | 0:45 |
| 6.5 | Bitrot | Code | 1:30 |
| 7 | Adversarial | Code | 2:00 |
| 8 | Draft | Code | 1:00 |
| 9 | Audit | Code | 1:00 |
| 10 | Cowork pipeline | Desktop (2 windows) | 1:30 |
| — | Wrap-up | Slides | 1:00 |
| | **Total** | | **~18:15** |
