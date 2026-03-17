# Concept Note: Conference Demo in Claude Desktop / Cowork

Thinking out loud about what happens if the live demo runs in Claude
Desktop instead of Claude Code CLI.  Not a spec yet -- just working
through the tradeoffs.

---

## 1. What changes

The CLI demo is command-driven.  The presenter types slash commands
(`/load-document`, `/search-document`, `/eval-document`,
`/audit-document`) and references agent templates by path.  It is
deterministic, scriptable, and terminal-native.

In Claude Desktop / Cowork the interaction model is fundamentally
different:

- **Chat UI replaces the terminal.**  The audience sees a familiar
  message-based interface, not a blinking cursor.  This matters for
  audiences that are not developers.

- **MCP tools replace skill triggers.**  Instead of `/load-document
  "assets/..."` the presenter says "load the RFP archive" and Claude
  calls the `load_contract` MCP tool.  The `.mcp.json` already
  configures the `contract-review` server, so the tools are available
  automatically.

- **Natural language replaces exact commands.**  "Search the documents
  for insurance requirements" instead of `/search-document "insurance
  requirements"`.  The presenter does not need to remember syntax.

- **Multiple windows represent multiple agents.**  In Cowork mode you
  can have two or three Claude Desktop instances open, each with a
  different system prompt (evaluator, verifier, drafter).  They share
  the same SQLite DB in `demo/data/contracts.db`, so one instance's
  work is visible to the others.

- **Agent templates become system prompt preambles.**  The
  `.agents/*.md` files can't be loaded with a path reference the way
  Claude Code does it.  You'd paste the relevant persona into each
  Desktop window's project instructions, or reference them via a
  project-level `CLAUDE.md` that includes instructions.

- **The eval step is conversational, not triggered.**  Instead of
  `/eval-document assets/criteria/ip-and-ownership.md`, the presenter
  would say something like "evaluate this document package against the
  IP criteria -- here are the criteria:" and either paste the file or
  rely on the `read_criteria_file` MCP tool.

---

## 2. Advantages

### More accessible to non-technical audiences
The biggest win.  A conference audience that has never seen a terminal
will immediately understand a chat window.  The "this is just a
conversation" framing lands harder when it literally looks like a
conversation.

### Claude Desktop handles MCP automatically
The `.mcp.json` in the demo directory already configures the
`contract-review` MCP server.  Claude Desktop connects to it on
launch -- no `make load`, no `uv run`, no explaining what a CLI
flag is.

### Natural language interaction
"Load the RFP and tell me what's in it" is more compelling on stage
than `/load-document "assets/1-RFP 20-020 - Original Documents.zip"`.
The audience can follow the intent without parsing command syntax.

### Better rendering
Claude Desktop renders markdown, tables, and code blocks nicely.
The eval reports with severity tables and quoted evidence will look
polished without any extra work.

### Cowork mode is the pipeline story
This is the real selling point.  Instead of describing the pipeline on
a slide and saying "imagine these agents running in parallel," you
open two or three Desktop windows side by side:

1. **Window 1: Evaluator** -- loads docs, runs criteria, produces
   findings
2. **Window 2: Verifier** -- reads the findings from the shared DB,
   challenges them
3. **Window 3: Drafter** -- takes verified findings, produces the memo

The audience watches agents coordinate through the shared SQLite DB
in real time.  The audit trail (`audit_contract` tool) shows entries
from all three agents.

### The "OH NO" moment is more natural
Step 0 currently asks the presenter to switch to Claude Desktop
anyway, paste document text into a polluted session, and show the
bad output.  If the whole demo is in Desktop, this becomes seamless
-- it is the same interface, just a dirty session vs a clean one.

---

## 3. Challenges

### No skills system
Claude Desktop does not have `.claude/skills/` discovery.  The four
skills (`contract-loader`, `contract-search`, `contract-eval`,
`contract-audit`) would need to be replaced entirely by:

- MCP tools for the mechanical parts (load, search, audit -- already
  done in `contract-mcp-server.py`)
- CLAUDE.md instructions for the LLM-judgment parts (eval, response
  drafting)

The MCP server already covers load, search, audit, stats, and criteria
listing.  The gap is **eval** -- the eval skill is the most complex
because it orchestrates search + LLM judgment + structured output.
There is no `eval_contract` MCP tool today.

### The eval gap
The eval step is the hardest to port.  In Claude Code, the
`contract-eval` skill gives detailed instructions:

1. Load criteria from a markdown file
2. For each criterion, run `contract-search`
3. Assess severity with evidence
4. Output a structured report

In Desktop, this would rely on CLAUDE.md instructions or the system
prompt to guide the same flow.  The risk is that without skill-level
structure, Claude might:
- Skip criteria
- Not cite evidence properly
- Produce a different output format each time
- Not use the search tool when it should

This is solvable (put the eval instructions in CLAUDE.md or in the
system prompt preamble for the evaluator window) but it is less
deterministic than a skill trigger.

### Less deterministic, harder to script
The presenter cannot guarantee exact outputs.  In CLI mode, the
demo script says "type this, expect that."  In Desktop mode, the
presenter types natural language and gets whatever Claude produces.
For a conference demo this is higher risk:

- The model might take a different path
- It might produce verbose or terse output unpredictably
- It might not call the MCP tools when expected
- The presenter cannot "re-run" a step cleanly

Mitigation: pre-populate the system prompt with very specific
instructions about tool usage patterns, and rehearse extensively.

### Agent templates don't auto-load
In Claude Code, the presenter says "using the verification agent
(.agents/verification-agent.md), challenge these findings" and
Claude loads the template.  In Desktop, you'd need to:

- Paste the agent persona into the system prompt / project
  instructions for each window, OR
- Include all agent personas in CLAUDE.md and tell Claude which
  role to assume, OR
- Use separate Claude Desktop projects, each with its own
  project instructions

The first option is most practical for a demo -- pre-configure
each window before going onstage.

### No slash commands for the audience to see
Slash commands in the CLI demo serve a secondary purpose: they
are visible, memorable, copy-pastable.  The audience can write
down `/eval-document assets/criteria/ip-and-ownership.md` and
try it later.  In Desktop mode, the equivalent is "I told it to
evaluate against the IP criteria" -- less tangible.

### Timing is less predictable
Chat-based interaction includes typing time, reading time, and
Claude's response streaming.  In CLI mode, the presenter pastes
a command and waits.  In Desktop mode, the presenter types (or
pastes) a message, Claude may ask a clarifying question, and the
output streams in a chat bubble.  Harder to hit the 18-minute
budget.

---

## 4. Hybrid approach

The strongest version might combine both interfaces:

| Phase | Interface | Why |
|-------|-----------|-----|
| Step 0: OH NO | Claude Desktop | Natural -- paste into a chat, get bad output. Relatable. |
| Steps 1-9: Interactive walkthrough | Claude Code CLI | Deterministic, scriptable, skill-driven. The meat of the demo. |
| Step 10: Pipeline / Cowork | Claude Desktop (2-3 windows) | Show multi-instance coordination. The "future" moment. |
| Wrap-up | Slides | |

This gives the audience both interfaces:
- Desktop for the "this is what most people do" framing (Step 0)
- CLI for the "this is how you engineer it" core (Steps 1-9)
- Desktop/Cowork for the "this is where it's going" vision (Step 10)

The interface switch itself becomes a talking point: "We started in
chat because that is where everyone starts.  We moved to CLI because
engineering requires structure.  Now we're back in chat -- but with
structure underneath."

---

## 5. What would need to exist

### Already done
- [x] MCP server with `load_contract`, `search_contract`,
  `audit_contract`, `get_contract_stats`, `list_criteria_files`,
  `read_criteria_file` tools
- [x] `.mcp.json` configuration pointing to the server
- [x] CLAUDE.md with overview of tools and workflow
- [x] Shared SQLite DB with `audit_log` table for cross-instance
  coordination
- [x] Criteria files in `assets/criteria/`

### Needs to be built
- [ ] **`eval_contract` MCP tool** -- the big gap.  Would take a
  criteria filename, run the search+assess loop, and return a
  structured findings report.  This is the most complex tool because
  it combines search with LLM judgment.  Two approaches:
  - **Tool-side eval:** The MCP server calls search internally and
    returns raw clause matches; Claude does the judgment.  Simpler
    but less structured.
  - **Full eval tool:** The MCP server orchestrates the entire eval
    (search + template-based assessment) and returns a finished
    report.  More deterministic but requires the server to call an
    LLM, which adds complexity and API key management.
  - **Recommendation:** Go with tool-side search + Claude judgment.
    Add an `eval_contract` tool that takes a criteria filename,
    runs `search_contract` for each criterion, and returns the raw
    matches grouped by criterion.  Claude Desktop then does the
    severity assessment and report formatting based on CLAUDE.md
    instructions.

- [ ] **Per-agent project instructions** -- one file per agent role
  that can be pasted into a Desktop window's project settings.
  Derive from the existing `.agents/*.md` templates but rewritten
  for Desktop's project instructions format (no file path
  references, self-contained).

- [ ] **CLAUDE.md enhancements** -- the current CLAUDE.md is written
  for Claude Code.  For Desktop, it would need:
  - Explicit eval workflow instructions (replacing the skill)
  - Output format specifications (the structured report template)
  - Tool usage guidance ("always use search_contract before making
    claims about document content")

- [ ] **Pre-loaded data option** -- Claude Desktop can't run
  `make load-cached`.  The MCP server would need a way to detect
  and use pre-loaded data, or the presenter runs the load in a
  terminal before opening Desktop.

- [ ] **Rehearsal script** -- a Desktop-native version of the demo
  script with suggested natural-language prompts for each step,
  expected tool calls, and fallback talking points.

---

## 6. Demo flow comparison

| Step | CLI Demo | Cowork Demo | Notes |
|------|----------|-------------|-------|
| **0. OH NO** | Switch to Claude Desktop, paste doc text, get vague output | Same -- already in Desktop. Paste into a session with prior conversation. | Identical in both versions |
| **1. Roster** | "Show me the skills and agents" -- lists files | "What tools do you have?" -- Claude lists MCP tools | Desktop can't browse `.claude/skills/` but can describe its MCP tools |
| **2. Load** | `/load-document "assets/..."` | "Load the RFP archive" -- Claude calls `load_contract` | Nearly identical; Desktop streams the tool result in chat |
| **3. Search** | `/search-document "submission requirements"` | "Search for submission requirements" -- Claude calls `search_contract` | Natural language is actually nicer here |
| **4. Eval (IP)** | `/eval-document assets/criteria/ip-and-ownership.md` | "Read the IP criteria file and evaluate each criterion against the documents" | This is the risky step -- needs good CLAUDE.md instructions |
| **5. Eval (flags)** | `/eval-document assets/criteria/general-red-flags.md` | "Now evaluate against the general red flags criteria" | Same risk as Step 4 |
| **5.5. Contrast** | Show prebaked naive review | "Remember that first attempt? Compare it to what we just found" | Works fine conversationally |
| **6.5. Bitrot** | Talk through prebaked tables | Same -- this is verbal either way | No difference |
| **7. Adversarial** | "Using verification-agent.md, challenge findings" | Open Window 2 with verifier persona. "Here are the findings -- challenge them." | **Cowork win** -- visually shows a separate agent |
| **8. Response** | "Using response-drafter-agent.md, draft memo" | Open Window 3 with drafter persona. "Draft a response based on verified findings." | **Cowork win** -- another visible agent |
| **9. Audit** | `/audit-document` | "Show me the audit trail" -- Claude calls `audit_contract` | Desktop renders the trail nicely |
| **10. Pipeline** | Slide + verbal walkthrough | Point at the three windows: "You just watched the pipeline run" | **Cowork win** -- the pipeline is not a diagram, it is live |

---

## 7. Verdict

### Is it worth pursuing?

**For the full demo: no, not yet.** The eval step is too important
and too fragile to run in Desktop without more infrastructure.  The
missing `eval_contract` tool and the lack of skill-level instructions
make Steps 4-5 high-risk for a conference setting.

**For the hybrid approach: yes, absolutely.** Using Desktop for
Step 0 (already in the script) and for Step 10 (cowork pipeline
visualization) adds real value with low risk.  The cowork segment
turns a slide diagram into a live demo.

### What's the effort?

| Work item | Effort | Priority |
|-----------|--------|----------|
| Build `eval_contract` MCP tool (search-side) | 2-3 hours | P1 if doing full Desktop demo |
| Write per-agent project instructions | 1-2 hours | P1 for cowork segment |
| Enhance CLAUDE.md for Desktop | 1 hour | P2 |
| Write Desktop rehearsal script | 1-2 hours | P2 |
| Pre-load data workflow for Desktop | 30 min | P1 |
| Rehearsal (Desktop path) | 2-3 hours | P1 |
| **Total** | **~8-12 hours** | |

For the hybrid approach only (Desktop for Step 0 + cowork for
Step 10), the work is smaller:

| Work item | Effort |
|-----------|--------|
| Per-agent project instructions (verifier + drafter only) | 1 hour |
| Pre-load data before Desktop opens | Already works -- just run `make load` in terminal first |
| Rehearse the cowork segment | 1-2 hours |
| **Total** | **~2-3 hours** |

### What's the risk?

**Full Desktop demo risk: medium-high.**  The eval step can produce
inconsistent results, and the lack of deterministic triggers means
the presenter must improvise more.  A bad eval output on stage is
hard to recover from.

**Hybrid approach risk: low.**  Step 0 is already Desktop-based.
The cowork segment (Step 10) is currently just a slide -- making it
live with two Desktop windows is strictly additive.  If it fails,
fall back to the slide.  The prebaked data + `audit_contract` tool
means the audit trail will always have something to show.

### Recommendation

Do the hybrid.  Keep the CLI for the structured walkthrough where
determinism matters.  Add a live cowork segment at the end using
two Desktop windows (verifier + drafter) to replace the pipeline
slide.  Budget 2-3 hours to set it up and rehearse.

If the cowork segment works well in rehearsal, consider expanding
Desktop usage for the next iteration of the talk.
