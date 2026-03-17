# Demo Assets

Supporting materials for the three live demos in
**Agents of Legend: The Orchestrator Dilemma**.

These are prebaked safety-net outputs so the talk can proceed smoothly
even if live generation stalls.

## Directory Layout

```
demo-assets/
  contracts/
    sample-consulting-agreement.md   -- fictional MSA for Demo 3
  ogl-content/
    sample-content-db.json           -- L&LL's content database (Demo 1)
    ogl-reference-terms.json         -- SRD terms that trigger OGL flags
  prebaked/
    ogl-crisis-report.md             -- safety-net output for Demo 1
    document-review-checklist.md     -- safety-net output for Demo 3
    skill-example.md                 -- annotated skill file for Demo 2
  DnD_Archive/                       -- source PDFs (downloaded separately)
  dl.py                              -- PDF download script
```

## How to Use During the Talk

### Demo 1 -- OGL Content Crisis (slide 09)

1. Run the live agent against `DnD_Archive/` PDFs and
   `ogl-content/sample-content-db.json`.
2. If the agent stalls, open `prebaked/ogl-crisis-report.md` and
   walk through it as if it were generated live.

### Demo 2 -- Skills in Action (slide 10)

1. Create a skill live in the terminal.
2. If creation fails or takes too long, show
   `prebaked/skill-example.md` as the finished artifact.

### Demo 3 -- Contract Analysis (slide 12)

1. Feed `contracts/sample-consulting-agreement.md` to the agent.
2. If the agent stalls, open `prebaked/document-review-checklist.md`
   and walk through the findings.

## Notes

- The consulting agreement is entirely fictional. "L&LL LLC" and
  "Six Feet Up, Inc." are used for narrative consistency with the talk.
- The OGL content database is synthetic. Term lists are based on the
  SRD 5.1 but simplified for demo purposes.
