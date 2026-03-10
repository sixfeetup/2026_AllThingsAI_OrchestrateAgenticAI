# Demo Execution Plan — Agents of Legend

_Lowest-risk plan for 3 live demo segments in a 30-minute talk._

---

## Time Budget Overview

| Segment | Slides | Time | Notes |
|---|---|---|---|
| Act I — Intro & Setup | 01-08 | 8 min | Narrative, team intro, quest framing |
| **Demo 1 — OGL Content Crisis** | 09-10 | 6 min | PDF search, DB cross-ref, name replacement |
| Act II — Frameworks & Transition | 10-11 | 3 min | Cynefin/OODA, loot the room, more work |
| **Demo 2 — Contract/Security Review** | 12 | 6 min | Contract ingest, security, adversarial swarm |
| **Demo 3 — Jetpacks / Working Together** | 13 | 4 min | multiclaude TDD, ralph-orchestrator |
| Closing + Q&A | 14-15 | 3 min | Recap, questions |
| **Total** | | **30 min** | |

---

## Demo 1 — OGL Content Crisis

**Slides:** 09 (Spelljammer) → 10 (Loot the Room)
**Time Budget:** 6 minutes (hard stop at 6:30)
**Risk Level:** MEDIUM

### Setup (Pre-Talk)

- [ ] PDFs downloaded and verified in `demo-assets/DnD_Archive/` (18 files, ~170MB — already present)
- [ ] Database pre-loaded with L&LL content dump (SQLite or Postgres, confirm which)
- [ ] Claude Code session pre-warmed: open terminal, `cd` into repo, verify API key with a trivial prompt
- [ ] Pre-create the `/say` notification skill file so the "create a skill on the fly" demo can be a quick edit, not from scratch
- [ ] Have a draft of the skill file ready in clipboard — the "on the fly" creation is really a fast paste-and-tweak
- [ ] Pre-stage a smaller subset of PDFs (2-3 key ones like `ODnD_Men_and_Magic.pdf`, `ODnD_Monsters_and_Treasure.pdf`) for faster search if full corpus is too slow
- [ ] Run the full demo once from the venue network during setup; note timing
- [ ] Tag the repo: `git tag demo-ready-v1`

### Live Steps

1. **[0:00]** Set the scene verbally: "Tasha's phone call just came in. Let's see how bad the damage is."
2. **[0:30]** Open Claude Code. Show the PDF archive briefly (`ls demo-assets/DnD_Archive/`).
3. **[1:00]** Prompt Claude to search PDFs for OGL-protected names (places, monsters, magic items, characters). Use a pre-written prompt from a skill or CLAUDE.md — do NOT improvise the prompt live.
4. **[2:00]** While it runs, narrate what's happening: "It's extracting named entities from these PDFs, cross-referencing against L&LL's content database."
5. **[3:00]** Show the damage report output (names found, count of affected content items).
6. **[3:30]** Quick demo: "Let me create a skill on the fly" — paste the `/say` notification skill, show how skills codify problem-solving.
7. **[4:30]** Prompt for replacement name generation. Show a few generated alternatives.
8. **[5:30]** Wrap: "The cleric and bard now have their damage report. The OGL crisis is quantified."

### Fallback Strategy

| Failure Mode | Fallback |
|---|---|
| API timeout / rate limit | Switch to pre-baked output: `demo-assets/prebaked/ogl-report.md` (create this) |
| PDF parsing too slow | Use the 2-3 PDF subset instead of full 18-file corpus |
| Database connection fails | Use pre-loaded SQLite file with results already populated |
| Total failure | Show pre-recorded screen capture (asciinema) of the full run |
| Everything fails | Skip to slide 10, narrate results verbally using the pre-baked report as a screenshot |

### Dependencies

| Dependency | Online? | Mitigation |
|---|---|---|
| Anthropic API | YES | Pre-warm, verify at venue; hotspot backup |
| PDF files | NO (local) | Already in repo |
| Database | NO (local) | Pre-stage SQLite |
| Claude Code CLI | NO (local) | Verify installed before talk |
| `/say` skill | NO (local) | Pre-draft in clipboard |

### Risk Mitigations

- **Pre-bake the slow parts:** The PDF extraction can take 30-60+ seconds. Consider pre-loading extracted names into the DB and having the "search" step read from cache, with a brief "I ran the extraction earlier" note.
- **Smaller corpus:** Use 2-3 PDFs live, reference full results from pre-bake.
- **Timer discipline:** If extraction isn't done by 2:30, cut to pre-baked output immediately. Do not wait.

---

## Demo 2 — Contract/Security Review ("It's a TRAP!")

**Slide:** 12 (It's a TRAP!)
**Time Budget:** 6 minutes (hard stop at 6:30)
**Risk Level:** HIGH

### Setup (Pre-Talk)

- [ ] Synthetic contract PDF created and staged in repo (8-12 pages, realistic but safe)
- [ ] Security skills installed and tested: verify they produce clean output
- [ ] `/c^2` skill available and tested with at least one successful multi-agent dispatch
- [ ] Codex CLI installed, API key verified (`/aix` or env var)
- [ ] Gemini API key verified and not at quota (check billing dashboard morning-of)
- [ ] `speckit` installed and working against a test spec
- [ ] `/visual-explainer` skill tested — produces self-contained HTML
- [ ] Pre-generate ALL visual explainer outputs and save to `demo-assets/prebaked/`:
  - `contract-overview.html`
  - `risk-report.html`
  - `adversarial-findings.html`
- [ ] Pre-generate speckit output and save to `demo-assets/prebaked/speckit-output/`
- [ ] Test the full swarm dispatch sequence at least twice; note failure modes

### Live Steps

1. **[0:00]** Transition: "We landed more work. But there's a trap in the contract."
2. **[0:30]** Ingest contract PDF into Claude Code. Show it recognizing the document.
3. **[1:00]** Generate visual explainer and checklist from the contract. If `/visual-explainer` works, show the HTML output. If not, open pre-baked HTML.
4. **[2:00]** Run security skills — show the security report output.
5. **[2:30]** Launch the swarm: `/c^2` dispatching to Codex and Gemini for adversarial review. Narrate: "We're sending this to multiple models for independent adversarial review."
6. **[3:30]** While swarm runs, show the visual explainer overlays (open pre-baked HTMLs if live generation is slow).
7. **[4:30]** Show adversarial review findings (at least one model's output should be ready).
8. **[5:00]** Quick speckit demo: "From these findings, we generate a spec." Show the spec output (pre-baked if needed).
9. **[5:30]** Show `/c^2` with worktrees and PRs: "Each agent works on its own branch. Findings become PRs."
10. **[6:00]** Wrap: "Security baked in, not bolted on. Multiple models cross-checking each other."

### Fallback Strategy

| Failure Mode | Fallback |
|---|---|
| Anthropic API down | Pre-baked outputs for every step |
| Gemini API quota hit | Skip Gemini leg of swarm, show Codex + Claude only |
| Codex API fails | Skip Codex leg, show Claude + narrate what Codex would add |
| Both external APIs fail | Run Claude-only adversarial (self-review), show pre-baked multi-model output |
| `/c^2` dispatch fails | Run agents sequentially in single Claude session |
| speckit fails | Open pre-baked spec output |
| Visual explainer fails | Open pre-baked HTML files directly |
| Total failure | Narrate over pre-baked screenshots/HTML files. Open them as static pages. |

### Dependencies

| Dependency | Online? | Mitigation |
|---|---|---|
| Anthropic API | YES | Pre-warm; hotspot |
| OpenAI/Codex API | YES | Pre-bake output; skip if down |
| Gemini API | YES | Pre-bake output; check quota morning-of |
| `/c^2` skill | NO (local) | Test before talk |
| speckit | NO (local) | Pre-bake output |
| visual-explainer | NO (local) | Pre-bake all HTML outputs |
| Contract PDF | NO (local) | In repo |

### Risk Mitigations

- **This is the highest-risk demo.** Three external APIs, multiple tools chained.
- **Pre-bake everything.** Every output from this demo should exist as a file in `demo-assets/prebaked/` before the talk starts.
- **Graceful degradation:** If only Claude works, still a good demo. If nothing works, the pre-baked HTML explainers carry the narrative.
- **Time-box the swarm:** If `/c^2` dispatch hasn't returned results by 4:00, cut to pre-baked adversarial output. Do not wait.
- **Consider making this demo 50% pre-baked by design:** Start with the ingest live, then "I ran the full swarm earlier, let me show you the results" — audience gets the concept without the live risk.

---

## Demo 3 — Jetpacks / Working Together

**Slide:** 13 (Jetpacks All Around)
**Time Budget:** 4 minutes (hard stop at 4:30)
**Risk Level:** MEDIUM

### Setup (Pre-Talk)

- [ ] Feature specification written and staged (small, well-bounded — e.g., "add a search endpoint to the LARP event API")
- [ ] `multiclaude` installed, daemons tested, TDD workflow verified
- [ ] `ralph-orchestrator` installed with hats prompt configured
- [ ] A clean branch prepared for the demo: `demo/jetpacks`
- [ ] CI/CD pipeline configured (GitHub Actions) — even if it's just lint + test
- [ ] Pre-record a successful multiclaude TDD run (screen capture, 60-90 seconds)
- [ ] Pre-record a successful ralph-orchestrator loop (screen capture, 60-90 seconds)

### Live Steps

1. **[0:00]** Transition: "Now let's build something. Together."
2. **[0:30]** Show the feature spec. Brief. "Here's what we want to build."
3. **[1:00]** Launch multiclaude: "Watch — it's going to write the tests first, then implement, then validate." Show the TDD cycle starting.
4. **[2:00]** While multiclaude runs, narrate: "Built-in TDD. Multiple agents — one writes tests, one implements, one reviews. CI/CD picks it up automatically."
5. **[2:30]** Switch to ralph-orchestrator: "Different approach — hat-based loop-driven development." Show the hats prompt and a loop iteration.
6. **[3:30]** Show the output: passing tests, clean implementation, PR created.
7. **[4:00]** Wrap: "The medium is the message. Agents as environments for other agents."

### Fallback Strategy

| Failure Mode | Fallback |
|---|---|
| multiclaude daemon fails | Show pre-recorded screen capture |
| ralph-orchestrator fails | Show pre-recorded screen capture |
| API rate limit | Switch to recordings immediately |
| Tests fail unexpectedly | "That's actually the point — the loop catches it. Let me show you the successful run." Switch to recording. |
| Total failure | Narrate over slides, show pre-recorded captures |

### Dependencies

| Dependency | Online? | Mitigation |
|---|---|---|
| Anthropic API | YES | Pre-warm; hotspot |
| multiclaude | NO (local) | Test before talk |
| ralph-orchestrator | NO (local) | Test before talk |
| GitHub Actions CI | YES | Not critical for demo narrative |
| Feature spec | NO (local) | In repo |

### Risk Mitigations

- **This demo is the shortest and should be the most rehearsed.** Four minutes is tight.
- **Pre-record everything.** The live attempt is a bonus. The recording is the plan.
- **Focus on the concept, not the terminal output.** The audience needs to understand hats + loops + TDD, not read scrolling terminal text.
- **If multiclaude works live, skip the ralph recording.** If multiclaude fails, show ralph recording. Show at least one tool working live.

---

## General Risk Mitigations

### Pre-Bake vs. Truly Live

| Element | Pre-Bake? | Rationale |
|---|---|---|
| PDF name extraction (Demo 1) | YES — pre-extract, show cached results | Too slow live (30-60s per PDF) |
| DB cross-reference (Demo 1) | Partial — pre-load DB, run query live | Query is fast, dramatic |
| Name generation (Demo 1) | Live | Fast, impressive, low risk |
| Skill creation (Demo 1) | Live (paste from clipboard) | Quick, shows the concept |
| Contract ingest (Demo 2) | Live | Fast, sets the scene |
| Visual explainers (Demo 2) | PRE-BAKE | Generation takes too long for stage |
| Security report (Demo 2) | Live attempt, pre-bake fallback | Medium speed, important to see live |
| Swarm dispatch (Demo 2) | Live attempt, pre-bake fallback | High risk, high reward |
| speckit output (Demo 2) | PRE-BAKE | Too slow for live |
| multiclaude TDD (Demo 3) | Live attempt, recording fallback | Worth trying live |
| ralph-orchestrator (Demo 3) | Recording | Too complex for 4 min live |

### Network Dependency Analysis

**Must have network:**
- Anthropic API (all demos)
- OpenAI Codex API (Demo 2 only)
- Gemini API (Demo 2 only)

**Can run offline:**
- PDF parsing (local files)
- Database queries (local SQLite)
- Skill file creation/editing
- Visual explainer HTML (once generated)
- multiclaude / ralph (local tools, but they call APIs)

**Network plan:**
1. Bring a dedicated hotspot (phone tethering as backup)
2. Test venue WiFi during setup, including API connectivity
3. If venue WiFi has captive portal, use hotspot from the start
4. Pre-warm all API connections 5 minutes before talk

### API Quota / Billing Risks

- **Anthropic:** Monitor usage dashboard morning-of. Ensure sufficient credits.
- **OpenAI/Codex:** Set a spending limit. Check that quota wasn't burned during rehearsal.
- **Gemini:** Already hit limits today. Check free tier reset timing. Consider having a paid tier backup key.
- **Mitigation:** Use `/aix` to manage API keys. Have backup keys from a different account if primary is throttled.

### Branch Strategy

**Recommended:** Run all demos from a dedicated, tagged branch.

```
git checkout -b demo/allthings-2026
# Stage all pre-baked outputs, skills, configs
git add demo-assets/prebaked/
git commit -m "Stage pre-baked demo outputs"
git tag demo-v1
```

- Demo from the tag, not from HEAD
- If any pre-talk changes break something, `git checkout demo-v1`
- Keep `main` clean for the actual project work

### The "Everything Fails" Fallback

If all APIs are down and all tools are broken:

1. **Open the pre-baked HTML visual explainers** in a browser tab. These tell the story visually.
2. **Narrate the demo** using the slides + explainers: "Here's what you would see when we run this..."
3. **Show the pre-baked output files** (markdown reports, spec documents) as static content.
4. **Play the pre-recorded screen captures** (asciinema or video) for Demo 3.
5. **Lean into the meta-narrative:** "Even our demo toolchain has failure modes — which is exactly why we pre-bake, use fallbacks, and plan for graceful degradation. This is the orchestrator's dilemma in action."

The talk's thesis is about managing non-deterministic systems. A gracefully-handled failure IS the demo.

---

## Pre-Talk Checklist (Day-Of)

### 2 Hours Before

- [ ] Arrive at venue, claim speaker setup time
- [ ] Connect to venue WiFi, test API connectivity (Anthropic, OpenAI, Gemini)
- [ ] If WiFi is unreliable, switch to hotspot
- [ ] Open all pre-baked HTML files in browser tabs (hidden)
- [ ] Open terminal, set font to 18pt+, dark background
- [ ] `cd` into demo repo, `git checkout demo-v1`
- [ ] Run a trivial Claude Code prompt to verify API key

### 1 Hour Before

- [ ] Run Demo 1 end-to-end (abbreviated). Time it. Note any issues.
- [ ] Run Demo 2 contract ingest + security report. Verify output.
- [ ] Attempt Demo 2 swarm dispatch. If it works, note timing. If not, confirm pre-baked files open correctly.
- [ ] Run Demo 3 multiclaude start (just verify it launches). Kill after 30 seconds.
- [ ] Verify all pre-baked fallback files are accessible

### 15 Minutes Before

- [ ] Close all unnecessary apps (Slack, email, notifications OFF)
- [ ] Terminal full-screen, correct font size
- [ ] Browser with pre-baked tabs ready (hidden behind terminal)
- [ ] Notes/cheat sheet for demo commands visible on phone or second screen
- [ ] Water bottle accessible
- [ ] Deep breath

### Go-Time Trigger Discipline

- If any demo step takes > 30 seconds with no visible output, **cut to fallback immediately**
- If an API returns an error, **do not retry on stage** — cut to pre-baked
- If you're > 1 minute over time budget for any demo, **wrap and move on**
- The audience remembers the story, not whether the API call was live

---

## Demo Asset Inventory

### Already Available

```
demo-assets/
  dl.py                          # PDF downloader script
  DnD_Archive/                   # 18 D&D PDFs (~170MB)
    ADnD_1e_Monster_Manual_II.pdf
    ADnD_1e_Monster_Manual.pdf
    Chainmail_3rd_Ed.pdf
    DnD Second edition, all 26 books.pdf
    DnD_Basic_Rules_Holmes.pdf
    DnD_Basic_Rules_Moldvay.pdf
    DnD_Expert_Rules_Cook.pdf
    DnD_Rules_Cyclopedia.pdf
    dungeons_and_dragons_book_1_-_men_and_magic.pdf
    ODD Single Volume.pdf
    ODnD_Blackmoor.pdf
    ODnD_Eldritch_Wizardy.pdf
    ODnD_Gods_Demi-Gods_Heroes.pdf
    ODnD_Greyhawk.pdf
    ODnD_Men_and_Magic.pdf
    ODnD_Monsters_and_Treasure.pdf
    ODnD_Swords_and_Spells.pdf
    ODnD_Underworld_and_Wilderness_Adventures.pdf
```

### Needs to Be Created

```
demo-assets/prebaked/
  ogl-report.md                  # Demo 1: pre-baked name extraction results
  ogl-replacements.md            # Demo 1: pre-baked replacement names
  contract-overview.html         # Demo 2: visual explainer — contract overlay
  risk-report.html               # Demo 2: visual explainer — risk analysis
  adversarial-findings.html      # Demo 2: adversarial review output
  security-report.md             # Demo 2: security skill output
  speckit-output/                # Demo 2: speckit-generated spec
    spec.md
    plan.md
  multiclaude-recording.cast     # Demo 3: asciinema recording
  ralph-recording.cast           # Demo 3: asciinema recording

demo-assets/contracts/
  synthetic-contract.pdf         # Demo 2: the contract to review

demo-assets/skills/
  say-notification.md            # Demo 1: the skill created "on the fly"
  contract-review.md             # Demo 2: contract review skill
  security-review.md             # Demo 2: security review skill
  adversarial-reviewer.md        # Demo 2: adversarial agent skill

demo-assets/specs/
  jetpack-feature.md             # Demo 3: feature specification
```

---

## Recommended Rehearsal Schedule

1. **T-7 days:** Full run-through of all 3 demos. Identify what's too slow, what breaks.
2. **T-3 days:** Create all pre-baked outputs. Record asciinema sessions. Tag the repo.
3. **T-1 day:** Full dress rehearsal with timer. Practice the fallback transitions.
4. **T-0 morning:** Abbreviated tech check at venue. Verify APIs, network, font size.
