# Unorder talk thoughts

## Second blush


### On wizarding

![Fantasia: sorcerors apprentice](https://www.youtube.com/watch?v=B4M-54cEduo)

- first mistake was putting on the wizard hat: plan, then execute, rinse, repeat
- upstream: spec it! define boundaries. problem definition clarity is
  important (in the chair and in the agent context), as is expressing
  to the agents effectively how important or well understodd the
  requirements are to attenuate effort.
- downstream: leverage trap -- if an an individual is given great power, they need equal power to correct a system operating out of alignment
- so many agents

Create hegelian dialectics between agents
- multiple agents mean more context windows
- worktree allow for concurrent development
- files work for coordination (spec-kit example)
- jevvons paradox -- https://en.wikipedia.org/wiki/Jevons_paradox

### On hats

Sorting hat analogy?

### On djinis

Kent beck quote (Glenn or Jim?) needed

### Characters
- fighters are OPEX
- magic users are CAPEX
- warlocks are devops/devex
- rogues are red team
- paladins are blue team
- business people can be any class or NPC
- mix of dnd and real races and genders

### Orchestrators

Maybe a rogue gallery w/ some quick descriptions

- claude driving claude: dipper copying self (gravity fall double dipper)
- multiclaude: too many dippers (same episode)
- ralph: picture of ralph wiggun
- ralph-orchestrator: ralph wiggum in crab armor w/ rust logos
- gastown/wasteland: what if we took this to it's logical conclusions => mad max, thunderdome, fury road imagery.

"What could possibly go wrong"

Provide an vision of corporate gastown, imagery truman show / westworld

### Demo Repo
 - scaf full stack?
- Skills
  - security skills
  - visual-explainer
  - orchestrator skills
  - spec-kit
  - audit logger
  - &
  - multiclaude (w/ /work and /swarm)


## First blush
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
