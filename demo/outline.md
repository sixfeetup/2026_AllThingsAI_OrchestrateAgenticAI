# Demo Outline

## Prep

- Load in our RFP document

- Templates for our agents
  - document eval agent
  - data investigator
  - data loader
  - verification agent (adversarial review)
  - response drafter

- templates for skill
  - data loader
    - parse pdf
	- create a schema for document review
	- load into sqllite and chroma
  - data search and augment
  - eval skill
    - look at a criterion in md
	- apply and report
  - auditing skill

Run/follow script to pollute the context window?

## Demo

### Start

- skills & agents check
  - talk about our roster
  - talk about the tech and how we use skills to work with it
    - loader
	- searcher

### Load

- load in our document
  - mv to preload, do some searches

### Plan

- Establish goals
  - talk about how determinism is important
  - talk about ambiguity in documents
  - talk about how a good document is a good spec and a good spec is how we get good performance out of agents
  - Talk about testing agent systems and evals

### Eval

_Look at the document eval skill_

- Eval the document
  - edit the skill to find more things
  - do aversarily review using gemini and codex

### Report

Draft a response


### Improve

Show how you can create a pipeline for data loading, eval and review and response. Demonstrates wrouting and handoff.
