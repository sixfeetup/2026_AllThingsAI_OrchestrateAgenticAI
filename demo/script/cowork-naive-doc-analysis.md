# Cowork Context Buffer Exposition

## Prep

- Create a project called ATAI
- unzip the asset bundle into the project directory

Create a new task w/ the RFP file (1-RFP 20-020 - Original Documents.zip) and the following prompt

```
Task 1: RFP Naive Analysis
* Help me understand issues with this RFP
* give me a visualization of token usage afterward
* Note any points where you hit token limits.
* Do not use any skills for this analysis.
* Help me understand the risks of doing this work in the context buffer
```

While that chugs along, create a copy of this task

w/ the RFP file (1-RFP 20-020 - Original Documents.zip) and the following prompt

```
Task 2: RFP Naive Analysis
* Help me understand issues with this RFP
* give me a visualization of token usage afterward
* Note any points where you hit token limits.
* Do not use any skills for this analysis.
* Help me understand the risks of doing this work in the context buffer
```

When the second task completes, at the prompt: load via `@` "Shakespeare-Complete-Works.pdf" and say

```
load in documents until context buffer limit is hit forcing compaction.

Do
- another analysis of issues in the RFP
- an analysis of how your capabilities to assess the RFP have degraded
```

## Demo

Walk through the setup:
- show this as a basic lets ask chat scenario. Dump in the doc, hope for the best
- talk about how we can get claude to report on itself
- show how it does ok loading the docs and cruising through, and how if we had not told claude to tell us, we might think we had ok results.
- show how full the context is via the visualization
- talk about context as a tragedy of the common situation .. workspace not warehouse, desk not database.

Switch to second task
- say "what would happen if our context was say 95% full?"
- talk about loading in shakespeare until we hit compaction
- look at claudes analysis of degradation
- say things like "wow, this seems risky and easy to create poor result that seem ok" and "here we see the problem agents can help us solve"

Switch to cowork document-review demo
- talk about isolation as a strategy for context management, both in isolating data and access, and by creating agents/tools with their own context buffer.
