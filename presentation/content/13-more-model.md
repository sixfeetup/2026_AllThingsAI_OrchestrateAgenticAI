---
type: dark-slide
footer: "12"
---

# More Me (Or Rather More Model)

> "One agent found the clauses. But who scores the risk? Who checks for gaps?"

- Batch processing: run multiple passes over the same artifact
- Shell out to other agents — or more of yourself
- Task graph decomposition: clause extractor, risk scorer, completeness validator
- Each agent has a focused concern and a contained scope

```python
# Level 2: task graph decomposition
async def review_contract(doc: Document) -> Report:
    clauses = await clause_extractor(doc)
    risks   = await asyncio.gather(
        *[risk_scorer(c) for c in clauses]
    )
    gaps    = await completeness_validator(clauses, risks)
    return  await report_generator(risks, gaps)
```
