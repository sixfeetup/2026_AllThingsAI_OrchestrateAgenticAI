# atai-demo

Navigate the demo script during the live presentation.

## Triggers

- `/atai-demo` — show the step menu
- `/atai-demo <number>` — jump to a specific step
- `/atai-demo next` — advance to the next step

## Instructions

Read `demo/script/terminal.md` and parse the steps.

When invoked with **no argument** or `menu`, present this chooser:

```
## Demo Navigator

 0. OH NO — prebaked naive review          (~1:30)  [slides 8-10]
 1. Roster — show skills & agents          (~1:00)  [slide 11]
 2. Load — ingest the RFP archive          (~1:30)
 3. Search — keyword + semantic queries    (~2:00)
 4. Eval (IP) — focused criteria eval      (~2:00)  [slide 12]
 5. Eval (red flags) — broad scan          (~1:30)
 5.5 Naive Contrast — before/after         (~0:45)
 6  Edit & Re-eval — TDD for agents        (~1:30)  [if time]
 6.5 Bitrot — context degradation          (~1:30)
 7. Adversarial — red team the findings    (~2:00)  [slide 13]
 8. Draft — response memo                  (~1:00)
 9. Audit — full provenance trail          (~1:00)  [slide 14]
10. Pipeline — show the full flow          (~1:30)

Which step? (enter number)
```

Use the AskUserQuestion tool to let the presenter pick a step from the list. Include all steps as options.

When a step is selected (by number argument or from the menu), display that step's **cue card**:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STEP <N> — <TITLE>                  ~<time>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SLIDE: <slide transition note if any>

RUN:
  <the exact prompt or command to execute>

NOTES:
  <talking points, quoted from terminal.md>

APPLAUSE MOMENT:
  <if any, highlighted>

NEXT → Step <N+1>: <title>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

When invoked with `next`, determine which step was last shown in this session and advance to the next one.

## Cue card content

Pull all content directly from `demo/script/terminal.md`. Do not paraphrase — use the exact prompts and talking points from that file. The "RUN" section should contain the exact code block from the step. The "NOTES" section should contain the **Say:** lines verbatim.

## Constraints

- Do NOT execute the prompts — just display them for the presenter to copy/run
- Keep the cue card compact — it needs to be readable at a glance during a live talk
- Always show which step comes next so the presenter knows the flow
- If step 6 (Edit & Re-eval) is selected, note it's the optional "if time permits" step
