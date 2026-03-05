# Orchestrate Agentic AI: Context, Checklists, and No-Miss Reviews

## Pitch

Have you ever run a 20-page contract through an AI and watched it miss
the clause that actually mattered? You point it out and the model
replies, “Oh, you’re right.” You are not alone, which raises a hard
question: how can AI be trusted in high-stakes environments?
>
AI practitioners are under pressure to deploy AI on contracts,
policies, and code reviews without increasing risk. Yet most teams
still rely on chat-style prompts and generic tools that miss key
clauses, skip steps, and make it hard to prove what was actually
reviewed. New tool frameworks and MCP-style integrations are
multiplying calls and windows, but not reliability. The result is
stalled negotiations, audit anxiety, governance gaps, and persistent
doubts about whether AI is safe to trust.
>
Join Calvin Hendryx-Parker (AWS Hero and CTO of Six Feet Up, the
premier AI and Python agency in the U.S.) for a practical look at
orchestrating agentic AI systems. Learn how to turn generative AI into
a dependable reviewer for contracts, policies, audits, and software
development workflows such as code review and test planning.
>
### What You’ll Learn:
>
- Context Engineering Tactics: How to chunk documents and tasks, frame
  targeted prompts, and apply checklists so each sub-task has clear
  acceptance criteria and traceability.
>
- Agentic Workflow Strategies: How to turn a vague “review this” into
  a structured series of sub-jobs, including clause-level analysis,
  routing, and validation so nothing is silently skipped.
>
- No-Miss Review Demo: A live, clause-level walkthrough of an
  AI-driven contract review that shows task graphs, specialized
  agents, routing, and validation, plus direct parallels for
  engineering workflows.
>
Walk away with an actionable playbook to make AI reliable, auditable,
and ready for high-stakes enterprise use.

## 1st blush

- workable playbook: scaf template and docs?

- what process, what tech?
- tech problem should be something relatable: linux commands, common language problems, etc.
- styles of approach
  - iterative conversation
  - spec and drive
  - spec and orchestrate
- skills usage
- reliability engineering
  - how good is good enough (difference in stance based on downstream factors)
  - test to develop and deploy, monitoring after deploy
  - have the agents lean on CI (brownian ratchet)


Eventual consistency
- agents making writing tons of code easy
- Knowing what to write, how to write it so it can be thrown away when requirements change, and verifying it does what is needed is the struggle
- testing validity and impact initial correctness

Orchestration approaches
- conductor: run multiple agents, bounce from windo to window
  - good: decent control of speed and direct
  - bad: decision fatigue and context overload for the conductor
- relentless loop: ala openclaw or ralph
  - good: requires only initial input
  - bad:
    - what have we built?
	- what has happened along the way?
- swarm: many tentacles pumping on the keys
  - good:
    - concerns farmed out to focussed agents
    - utilize mechanism for isolating and merging streams of work (enforce breaking work up)
  - bad:
    - require higher level orchestration either by a conductor or a loop
- spec driven
  - good:
    - force upfront definition of what has to happen
	- specs == audit trail
  - bad
    - require upfront specification


The dependencies for good outcomes are not so different than human
actors: good parts, clean work area, clear and constrained problem
space, freedom to iterate, a good system for testing and
validation.

The concerns around safety are similar, but due to speed
things can wrong and the distance that a mistake might travel,
practices around containment, isolation, modularity, and transparency
become much more important.  Readability and reasonability become
primary structures of trust.

Every line of code is an operational liability, so so our aim is
getting the LLM to write a goldilocks amount of code that does what
our business needs.  If writing code is cheap, a well factored system
will allow us to iterate quickly over suboptimal code since throwing
away code should be cheap as well.  We just need to make progress and
eventually succeed at delivering our goal.
