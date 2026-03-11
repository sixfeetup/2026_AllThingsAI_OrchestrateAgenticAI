---
type: content-slide
image: ../images/kent-v-genie-1_web.jpg
image_alt: Kent Beck wrestling the genie — taming the new power
image_layout: split
footer: "02"
---

# Agents: Do I Need One?

_Everybody says they are great, but..._

- Why: automate non-deterministic, multi-step work
- What: LLM-driven workers that plan, act, and validate
- How: skills, tool use, context engineering, orchestration
- When: start small — one agent, one task, tight feedback loop

> "We're in the 'horseless carriage' stage of coding genies."
> — Kent Beck
<<<<<<< HEAD

???
This is the slide for the skeptics in the room — and you should be skeptical.

Why: because the work we do is full of non-deterministic, multi-step tasks
that don't reduce to a single API call. Review this contract. Plan this
migration. Audit this codebase. These are judgment-heavy workflows.

What: agents are LLM-driven workers that can plan a sequence of actions,
execute them with tools, and validate their own output. Not chatbots —
workers.

How: the magic is in skills (reusable prompt+tool bundles), context
engineering (giving the agent the right information at the right time),
and orchestration (coordinating multiple agents and humans).

When: start with one agent, one repetitive task, one tight feedback loop.
Don't boil the ocean. Kent Beck's quote nails it — we're early. Treat
agents like a junior team member: trust but verify.
=======
>>>>>>> whitmo/tweaks
