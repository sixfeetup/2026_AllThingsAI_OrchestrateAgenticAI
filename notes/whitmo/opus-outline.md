# The Agentic Quest: Orchestrating AI You Can Actually Trust

## Talk Concept

**RPG Metaphor:** The audience is a party of adventurers (business leads, product engineers, ops people) embarking on a quest through increasingly dangerous territory — the CAPEX/OPEX wilderness. Each stage of the quest levels up their agentic AI capability, from hand-steering every action to trusting autonomous agents with real stakes.

**Core tension:** "Fast, cheap, quality — pick any two or get none." But Kevin Kelly's "the future is here, just unevenly distributed" means the triangle isn't fixed — it shifts depending on who has the right tools, workflows, and trust frameworks. The quest is about moving your position on that triangle.

**Arc:** Why → What → How. Start with the pain (missed clauses, audit gaps, stalled reviews), show the landscape (agentic patterns, trust levels), then walk through the dungeon (live demo).

---

## Character Classes

### The Party (Audience Roles)

- **The Cleric** — Compliance officer / HR / BizOps / procurement. Overtasked healer keeping everyone alive. Juggles contracts, policies, audits, onboarding — always one crisis away from burnout. Cares about risk, correctness, and not getting sued.
- **The Wizard** — Developer. Powerful but possibly unstable. Can reshape reality with code but occasionally blows up the lab. Cares about shipping, code quality, and not being on-call forever.
- **The Ranger** — Ops / security / infrastructure. Civil engineer background energy — builds bridges, watches the perimeter, makes sure the ground doesn't collapse under the party. Cares about reliability, audit trails, and blast radius.

### The NPC (AI Role)

- **Claude Code — The Warforged Artificer** — Tireless construct that follows orders, crafts tools, and does the repetitive dangerous work. Loyal but literal. Only as good as the instructions and context it's given. The party's most capable hireling — if they learn to direct it properly.

Each section of the talk shows how the quest applies to all three party members, with the Warforged leveling up alongside them.

---

## 45-Minute Version

### Act I — The Tavern: Why Are We Here? (10 min)

**1. The Broken Promise (3 min)**
- Open with the scene: you hand a 20-page contract to the AI oracle. It misses the clause that matters. You correct it. It says "Oh, you're right." That's not a reviewer — that's a yes-man NPC.
- Same failure mode in code review, policy compliance, test planning.
- The party has been burned. Trust is low.

**2. The Iron Triangle and the Decision Frameworks (4 min)**
- Fast, cheap, quality — still real. AI doesn't break the triangle, it reshapes it.
- Kevin Kelly's uneven distribution: some teams are already operating at Level 3 autonomy. Most are stuck at Level 0 (copy-paste into chat).
- The gap isn't intelligence — it's orchestration, context, and trust.
- Introduce two frameworks everyone working with AI needs:
  - **OODA Loop (Observe → Orient → Decide → Act):** This is how you and your Warforged should operate together. Every agentic interaction is an OODA cycle. The question is: who's doing which steps? At Level 1, the human does all four. At Level 3, the agent runs its own OODA loops and the human audits.
  - **Cynefin:** Not all problems are the same. Simple (checklists, automation), Complicated (expert analysis, multi-step review), Complex (probe-sense-respond, adversarial agents), Chaotic (act first, stabilize, then assess). Your autonomy level should match the domain. Don't send a fully autonomous agent into a complex domain unsupervised.

**3. The Quest Board (3 min)**
- Frame the quest: take a real-world CAPEX/OPEX problem set (contract review, vendor evaluation, compliance check, code review) and solve it at progressively higher levels of autonomy.
- Security as *enabler*, not gate. The Ranger isn't here to block the party — they're here to let the party move faster by making the path safe.

---

### Act II — The Levels: What Does Agentic AI Actually Look Like? (15 min)

**4. Level 1 — The Apprentice: Human-Orchestrated (5 min)**
*You swing the sword. The AI sharpens it.*

- Pattern: human driving Claude Code (or similar) step by step.
- Context engineering basics: chunking documents, targeted prompts, checklists as acceptance criteria.
- Example: reviewing a contract clause-by-clause with explicit instructions per section.
- The Cleric sees faster first-pass review. The Wizard sees structured code review. The Ranger sees traceability (what was checked, what wasn't).
- OODA at this level: human Observes (reads doc), Orients (identifies what matters), Decides (writes the prompt), Acts (runs the Warforged). All four steps are manual.
- Limitation: it scales with your attention. You're still the bottleneck.

**5. Level 2 — The Party: Semi-Autonomous Orchestration (5 min)**
*You plan the raid. The agents execute roles.*

- Pattern: multi-agent workflows — multiclaude, ralph, spec-kit.
- Agentic workflow strategies: decomposing "review this" into a task graph of sub-jobs with routing, validation, and rollup.
- Sandboxing: each agent works in a contained environment. Mistakes don't cascade.
- Skills: agents with specialized capabilities (clause extraction, risk scoring, test generation).
- Adversarial agents: deliberately pit one agent against another to find gaps. Red team your own review.
- Human role shifts from doing to supervising — reviewing agent output, approving escalations.
- OODA shift: agents now run their own Observe → Orient → Decide loops. Human retains Act (approval) and audits the Orient step (are they looking at the right things?).
- Cynefin: this is where you tackle Complicated problems. Multiple expert agents, clear decomposition, but the interactions need orchestration.

**6. Level 3 — The Autonomous Guild: Fully Autonomous (5 min)**
*You set the objective. The system runs the campaign.*

- Pattern: self-orchestrating agent networks. (Reference gastown/wasteland — "we're not quite at Fury Road, but the scouts are out there")
- Trust earned through demonstrated reliability at Level 2 + audit trails + validation loops.
- Where this works today (low-risk, well-bounded tasks) vs. where it doesn't (novel, high-ambiguity).
- Cynefin check: fully autonomous works in Simple and some Complicated domains. For Complex domains, you need probe-sense-respond — which means human-in-the-loop even at Level 3. Chaotic? That's incident response, and the human takes the wheel.
- The Kevin Kelly point again: some orgs are already here for specific workflows. The future is unevenly distributed.

---

### Act III — The Dungeon: How to Actually Do This (15 min)

**7. Equipping Your Party: Tools for Involvement and Vigilance (5 min)**
- Writing tools that support human oversight, not replace it.
- Structured outputs: task graphs, checklists, diff-style reports ("here's what changed, here's what I flagged, here's what I skipped").
- Sandboxing strategies: isolated execution, rollback, dry runs.
- Adversarial patterns: using a second agent to challenge the first. "If this contract review missed something, what would it be?"
- Trust levels as a graduated system: observe → verify → approve → delegate → autonomize. Each level earned, not assumed.

**8. Live Demo: The No-Miss Contract Review (8 min)**
- Walk through a contract review using the progression:
  - Level 1: human-prompted clause analysis in Claude Code.
  - Level 2: multi-agent decomposition — one agent extracts clauses, one scores risk, one validates completeness, one generates the report.
  - Show the task graph, routing, validation checkpoints.
- Draw direct parallels: same pattern applies to code review (extract → analyze → test plan → validate coverage) and compliance audits.

**9. The Loot Table: What You Walk Away With (2 min)**
- Actionable playbook recap:
  - Start at Level 1. Get context engineering right first.
  - Build trust incrementally. Level 2 before Level 3.
  - Use adversarial agents. Don't trust a single pass.
  - Write tools for vigilance, not just automation.
  - Security enables speed when it's baked into the workflow, not bolted on.

---

### Epilogue — The Campfire (5 min)
- Q&A or audience discussion.

---

## 30-Minute Version

Compressed structure — same arc, tighter execution.

### Act I — The Tavern (5 min)
- Combine sections 1-3. Open with the broken promise, quickly frame the iron triangle + uneven distribution, introduce OODA and Cynefin as the two lenses for the rest of the talk, post the quest.

### Act II — The Levels (12 min)
- **Level 1 (4 min):** Human-orchestrated basics. Context engineering, checklists, traceability.
- **Level 2 (5 min):** Semi-autonomous. Multi-agent, sandboxing, adversarial agents, skills. This is the meat — spend time here.
- **Level 3 (3 min):** Fully autonomous. Brief — show the horizon, reference gastown/wasteland for the laugh, anchor on trust progression.

### Act III — The Dungeon (10 min)
- **Tools & Trust (4 min):** Combine sections 7's key points — graduated trust, adversarial patterns, structured outputs.
- **Demo (6 min):** Abbreviated version of the clause-level walkthrough. Show Level 1 → Level 2 transition. Skip Level 3 demo, reference it verbally.

### Epilogue (3 min)
- Loot table recap (30 seconds) + Q&A.

---

## Key References & Tools to Name-Drop

| Tool / Concept | Role in Talk |
|---|---|
| Claude Code (Warforged Artificer) | The party's AI companion — levels up with them |
| multiclaude | Level 2 — party coordination |
| ralph | Level 2 — agent orchestration |
| spec-kit | Level 2 — specification-driven workflows |
| gastown / wasteland | Level 3 — the frontier (comedic) |
| OODA Loop | Decision framework — who does Observe/Orient/Decide/Act at each level |
| Cynefin | Domain-matching framework — match autonomy level to problem complexity |
| Sandboxing | Safety mechanic across all levels |
| Skills (Claude) | Agent specialization |
| Adversarial agents | Quality assurance pattern |
| Kevin Kelly quote | Framing device for uneven adoption |
| Iron Triangle | Persistent constraint, reshaped by tooling |

---

## Demo Requirements

### Artifacts to Build Before the Talk

**1. The Contract (The Dungeon Map)**
- A synthetic but realistic CAPEX contract — 8-12 pages, not 20. Long enough to be non-trivial, short enough to demo in minutes.
- Must contain at least: a clean section (obvious, passes review), a tricky clause (ambiguous liability, auto-renewal buried in boilerplate), a missing element (no termination-for-convenience, or missing data handling clause), and a contradiction (two sections that conflict on payment terms or SLA).
- Annotated "answer key" version for the presenter so you can call out what the agents should and shouldn't catch.

**2. Claude Code Skills / CLAUDE.md Files**
- Level 1 skill: a contract review prompt with explicit checklist (clause categories, risk flags, completeness checks). Should be simple enough to show on screen and explain in 60 seconds.
- Level 2 skills (one per agent role): clause extractor, risk scorer, completeness validator, report generator. Each with its own CLAUDE.md or system prompt.
- Adversarial reviewer skill: prompt specifically designed to challenge the primary review output ("what did the first pass miss?").

**3. Orchestration Config**
- multiclaude or ralph config file that wires the Level 2 agents together with routing and validation gates.
- Should produce a visible task graph or execution log — the audience needs to see the structure, not just the output.
- If using spec-kit, a spec file that defines the review workflow with acceptance criteria per sub-task.

**4. Parallel Examples (Slide-Only, Not Live)**
- A code review example showing the same pattern: extract functions → analyze complexity/security → generate test plan → validate coverage. Doesn't need to run live — just show the structural parallel on a slide.
- A compliance audit example: extract policy requirements → map to controls → gap analysis → report. Same deal — slide showing the pattern maps 1:1.

### Environment & Tooling

**Machine Setup**
- Claude Code installed and working with API key. Test the day before. Test again the morning of.
- Terminal with readable font size (18pt+). Dark background, light text. Audience in the back row needs to read it.
- multiclaude / ralph / spec-kit installed and confirmed working against the contract artifact.
- Git repo with all skills, configs, and the contract checked in. Tag a known-good state. Demo from the tag, not from HEAD.

**Fallback Plan**
- Pre-recorded terminal session (asciinema or screen recording) of the full demo running successfully. If the network dies, the API rate-limits you, or anything else goes wrong, switch to the recording without apology.
- The recording should be made from the exact same repo tag you'd demo live from.
- Have the final output artifacts (task graph visualization, review report) as static files you can open directly if both live and recording fail.

**Network**
- Confirm venue WiFi or bring a hotspot. API calls to Anthropic need to work.
- If the venue has a captive portal or aggressive firewall, test Claude Code through it before the talk.
- Consider pre-warming: run the demo once from the venue network during setup to make sure nothing is cached/blocked.

### Demo Flow (8 min / 6 min versions)

**8-Minute Version (45-min talk)**

| Time | Action | What Audience Sees |
|---|---|---|
| 0:00-1:30 | Open contract in terminal. Show it's real, messy, long. | Raw contract text scrolling — "this is what the Cleric deals with every week." |
| 1:30-3:30 | Level 1: Run Claude Code with the single-skill checklist prompt against the contract. | Warforged working clause-by-clause. Output is a checklist with flags. Point out: it caught the contradiction, flagged the tricky clause, but missed the missing element. |
| 3:30-4:00 | Pause. "The Warforged did its job. But it only knows what we told it to look for. OODA: we did all four steps. Let's level up." | Transition beat. |
| 4:00-6:30 | Level 2: Run the multi-agent workflow. Show the task graph spinning up. Agents run in parallel/sequence. | Terminal output showing agents claiming tasks, producing intermediate artifacts, passing to next agent. Completeness validator catches the missing clause. Adversarial agent challenges the risk scores. |
| 6:30-7:30 | Show the final report side-by-side with the Level 1 output. | Clear improvement: the missing element is caught, risk scores are validated, the report has traceability (which agent did what, what was checked). |
| 7:30-8:00 | "Same pattern works for code review, compliance, vendor evaluation. The Cynefin domain determines how much autonomy. The OODA loop determines who does what." | Slide showing the parallel examples. |

**6-Minute Version (30-min talk)**

| Time | Action | What Audience Sees |
|---|---|---|
| 0:00-1:00 | Open contract. Brief framing. | Raw contract. |
| 1:00-2:30 | Level 1: Run single-skill review. Show output. Note the gap. | Checklist output, one miss highlighted. |
| 2:30-3:00 | Transition: "Let's add the rest of the party." | Beat. |
| 3:00-5:00 | Level 2: Run multi-agent workflow. Show task graph and agents running. | Agents in action, completeness validator catches the miss. |
| 5:00-5:30 | Side-by-side comparison. | Level 1 vs Level 2 output. |
| 5:30-6:00 | Parallel examples slide. OODA/Cynefin callback. | Wrap. |

### Open Questions

- [ ] Which contract should we use? Real redacted client contract (more credible) vs. fully synthetic (safer, no NDA risk)? Leaning synthetic with realistic messiness.
- [ ] Should the adversarial agent find something the primary review missed, or confirm it was thorough? Finding something is more dramatic but risks looking like the tools are unreliable. Confirming is less exciting but shows the pattern working. Probably: have it find a borderline issue that's arguable — shows the value without undermining trust.
- [ ] Do we want a visible task graph visualization (mermaid diagram, DAG) or is terminal output enough? A graph is more compelling for the Cleric and Ranger audience. Terminal output is more credible for the Wizard audience. Could do both: terminal runs, then show the graph as a "here's what just happened" summary.
- [ ] gastown/wasteland: do we actually show anything for Level 3, or just reference it verbally with a slide? Verbal + slide is safer for time. A 30-second screencast of an autonomous run with "here be dragons" framing could work in the 45-min version.

---

## Notes

- The RPG metaphor should be light and fun, not belabored. Use it to frame transitions ("we leveled up"), name sections, and keep energy up. Don't force every concept into game terminology.
- The Cleric/Wizard/Ranger party keeps the talk relevant to a mixed audience without splitting into separate tracks. The Warforged Artificer (Claude Code) is always present as the tool they're learning to wield.
- OODA and Cynefin are the real intellectual backbone. The RPG is the wrapper. Don't let the metaphor obscure the frameworks — they're what people will actually use on Monday.
- The demo is the proof. Everything before it is setup. If time is tight, protect the demo.
- The gastown/wasteland reference works as an "and here be dragons" moment — acknowledging the fully autonomous frontier without overselling it.
