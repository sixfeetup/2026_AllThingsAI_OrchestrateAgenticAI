# Demo Outline

## Prep

- Create a contract from a business BigCo partner including
  - 30 pages -- PDF w/ some spooky hidden text about cupcakes
  - 7 ambiguous or problem clauses
    - contradictions
	- impossible date
	- Incorrect name (not SixFeetUp)
	- Ambiguous timeframe
	- Ambiguous terms
	- Ambiguous licensing
	- Ambiguous staffing

- schema for loading

- Templates for our agents
  - contract eval agent
  - data investigator
  - data loader
  - verification agent (adversarial review)
  - response drafter

- templates for skill
  - data loader
    - parse pdf
	- create a schema for contract review
	- load into sqllite and chroma
  - data search and augment
  - eval skill
    - look at a criterion in md
	- apply and report
  - auditing skill

Pollute the context window?

## Demo

### Start

- skills & agents check
  - talk about our roster
  - talk about the tech and how we use skills to work with it
    - loader
	- searcher

### Load

- load in our contract
  - mv to preload, do some searches

### Plan

- Establish goals
  - talk about how determinism is important
  - talk about ambiguity in contracts
  - talk about how a good contract is a good spec and a good spec is how we get good performance out of agents
  - Talk about testing agent systems and evals

### Eval

_Look at the contract eval skill_

- Eval the contract
  - edit the skill to find more things
  - do aversarily review using gemini and codex

### Report

Draft a response


### Improve

Show how you can create a pipeline for data loading, eval and review and response. Demonstrates wrouting and handoff.
