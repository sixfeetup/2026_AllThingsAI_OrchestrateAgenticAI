---
type: content-slide
image: ../images/sorcerors-apprentice-grok.jpg
image_alt: The sorcerer's apprentice — iteration as a feature
image_layout: split
footer: "11"
---

# The Brownian Ratchet

_Eventual consistency as a strategy_

- Testing validity > initial correctness
- Each iteration catches what the last missed
- Agent proposes → tests validate → agent fixes → loop
- Like TDD, but the agent writes both sides
- Converges because the ratchet only moves forward

> "Make it work, make it right, make it fast."
> — Kent Beck

???

The key insight: we don't need the agent to be right the first time.
We need it to be right eventually, with proof.

The brownian ratchet pattern:

1. Agent generates code/content
2. Automated checks run (tests, linting, type checking, security scans)
3. Failures feed back as context for the next attempt
4. Each pass fixes something — the ratchet clicks forward
5. When all checks pass, we have both the result AND the proof it works

This is not wishful thinking — it's the same pattern CI/CD uses.
The difference is the agent closes the loop automatically.

Real example: multiclaude swarm generates 5 PRs, each with TDD.
3 pass immediately. 2 fail tests, get auto-fixed on retry.
All 5 land with green CI. That's eventual consistency in practice.
