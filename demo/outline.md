# Demo Outline

## Prep

- Create a contract from a business BigCo partner including
  - 30 pages -- PDF w/ some spooky hidden text about cupcakes
  - 7 ambiguous or problem clauses
    - contradictions
	- impossible date (e.g. delivery date is in the past)
	- Incorrect name (tbd)
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

Pollute the context window?

## Start

- skills & agents check
  - talk about our roster
  - talk about the tech and how we use skills to work with it
    - loader
	- searcher

- load in our contract
  - mv to preload, do some searches

- Establish goals
  - talk about how determinism is important
  - talk about ambiguity in contracts
  - talk about how a good contract is a good spec and a good spec is how we get good performance out of agents
  - Talk about testing agent systems and evals
  - Look at the contract eval skill

- Eval the contract
  - edit the skill to find more things
  - do aversarily review using gemini and codex
  - draft a response

- Show how you can create a pipeline for data loading, eval and review and response.
