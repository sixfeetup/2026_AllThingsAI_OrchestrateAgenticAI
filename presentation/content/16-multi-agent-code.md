---
type: dark-slide
footer: "15"
---

# Multi-Agent Decomposition

```python
# Level 2: task graph decomposition
async def review_contract(doc: Document) -> Report:
    clauses = await clause_extractor(doc)
    risks   = await asyncio.gather(
        *[risk_scorer(c) for c in clauses]
    )
    gaps    = await completeness_validator(clauses, risks)
    review  = await adversarial_check(clauses, risks, gaps)
    return  await report_generator(risks, gaps, review)
```

- Each agent has a focused concern and a contained scope
- Adversarial check challenges the primary review output
