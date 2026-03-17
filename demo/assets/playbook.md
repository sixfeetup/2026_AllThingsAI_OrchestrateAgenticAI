# Agent Review Playbook

A take-home guide for building agent-driven review systems.
Everything here generalizes beyond contracts — the patterns work for
code review, compliance audits, security analysis, or any domain where
you need structured evaluation of documents against criteria.

---

## 1. Criteria File Template

Criteria files are markdown documents. Each `##` heading names one
criterion. Under each heading you provide the context an agent needs to
evaluate that criterion: what to look for, why it matters, and what
constitutes a finding.

The format is intentionally simple. Agents parse markdown natively, and
humans can read and edit it without tooling. One file can hold all
criteria for a domain, or you can split them across files by category.

### Blank template

```markdown
# [Domain] Criteria

## [Criterion Name]

### What to look for

[Describe what the agent should examine. Be specific about patterns,
keywords, structural elements, or relationships between sections.]

### Why it matters

[Explain the risk or impact if this criterion is violated. This helps
the agent weigh severity and write useful findings.]

### Red flag indicators

- [Concrete signal that triggers a finding]
- [Another signal]
- [Another signal]
```

### Worked example: code review

```markdown
# Python Code Review Criteria

## Error Handling Coverage

### What to look for

Identify every function that performs I/O (file access, network calls,
database queries, subprocess execution) and check whether exceptions
are caught and handled. Look for bare `except:` or `except Exception:`
blocks that swallow errors silently. Verify that error messages include
enough context to diagnose the failure (which file, which endpoint,
what input).

### Why it matters

Unhandled exceptions in I/O paths cause silent failures in production.
Bare except blocks hide bugs by catching errors the developer did not
anticipate. Poor error messages turn a five-minute fix into an hour of
log archaeology.

### Red flag indicators

- `except:` or `except Exception: pass` with no logging or re-raise
- I/O operations outside any try/except block
- Error messages that say "an error occurred" without identifying what
  failed or what input caused it
- Retry logic with no backoff or attempt limit
```

---

## 2. Agent Role Template

An agent prompt defines five things: who the agent is, what it is trying
to accomplish, what tools it can use, what its output should look like,
and what it must not do. Constraints are as important as goals — they
prevent the agent from wandering into unhelpful territory.

### Blank template

```markdown
# [Agent Name]

## Persona

You are a [role description]. You have expertise in [domain].

## Goals

1. [Primary objective]
2. [Secondary objective]
3. [Tertiary objective, if any]

## Available Skills

- **[Skill name]**: [What it does, when to use it]
- **[Skill name]**: [What it does, when to use it]

## Output Format

[Describe the structure of the agent's output. Be explicit about
headings, required fields, severity levels, or any schema.]

## Constraints

- [What the agent must NOT do]
- [Scope limits]
- [Data handling rules]
```

### Worked example: test planning agent

```markdown
# Test Planning Agent

## Persona

You are a senior QA engineer. You have expertise in test strategy,
risk-based testing, and identifying gaps in test coverage.

## Goals

1. Read the feature spec and implementation PR diff provided to you.
2. Produce a test plan that covers happy paths, edge cases, failure
   modes, and integration boundaries.
3. Flag any areas where the spec is ambiguous enough that you cannot
   determine correct behavior.

## Available Skills

- **code-search**: Search the codebase for existing tests, fixtures,
  and helper utilities. Use this to avoid duplicating coverage.
- **spec-lookup**: Retrieve the full text of a referenced spec or
  requirements document by name.

## Output Format

Return a markdown document with these sections:

- **Summary**: One paragraph describing what is being tested and why.
- **Test Cases**: A numbered list. Each item has a title, preconditions,
  steps, and expected result.
- **Coverage Gaps**: Areas where you lack enough information to write a
  test. Include what question needs answering.
- **Risk Assessment**: Rank the three highest-risk areas and explain why.

## Constraints

- Do not write test code. Produce only the plan.
- Do not assume behavior that is not stated in the spec. If the spec
  is silent on an edge case, list it as a coverage gap.
- Do not suggest changes to the implementation. Stay in the QA role.
```

---

## 3. Orchestration Patterns

Four patterns cover most agent workflows. The right choice depends on
task complexity, risk level, and whether subtasks are independent.

### Single Agent

**When to use**: The task is well-defined, low stakes, and fits in one
context window. One agent with the right prompt and skills can handle
it end to end.

**Examples**: Summarizing a document. Reformatting data. Generating
boilerplate from a template.

### Pipeline

**When to use**: The work has clear stages, each requiring different
expertise or tooling. The output of one stage is the input to the next.

**Examples**: Parse PDF into structured data, then analyze against
criteria, then generate a report. Extract metrics from logs, then
compute aggregates, then visualize.

### Adversarial Review

**When to use**: The stakes are high enough that you need a second
opinion. False negatives are expensive. The reviewing agent should
actively try to find flaws in the first agent's work.

**Examples**: Security audit findings reviewed by a red-team agent.
Legal clause analysis verified by an agent looking for missed issues.
Code review where a second agent checks that review feedback is
accurate and complete.

### Swarm / Parallel

**When to use**: The work can be split into independent subtasks that
do not depend on each other. Results can be merged at the end without
conflicts.

**Examples**: Reviewing 20 files in a PR simultaneously. Evaluating
a document against 10 independent criteria. Running the same analysis
with multiple models and comparing results.

### Decision flowchart

```
Start
 │
 ├─ Can one agent do it in one pass?
 │   ├─ Yes → SINGLE AGENT
 │   └─ No ↓
 │
 ├─ Are the subtasks independent of each other?
 │   ├─ Yes → SWARM / PARALLEL
 │   └─ No ↓
 │
 ├─ Do the steps require different expertise or tools?
 │   ├─ Yes → PIPELINE
 │   └─ No ↓
 │
 └─ Are the stakes high enough to justify double-checking?
     ├─ Yes → ADVERSARIAL REVIEW (bolt onto any of the above)
     └─ No → SINGLE AGENT (reconsider your "no" above)
```

Note: Adversarial review is not mutually exclusive with the other
patterns. You can add an adversarial reviewer at the end of a pipeline,
or have one agent verify the merged output of a swarm.

---

## 4. Containment Checklist

Agent systems need the same operational discipline as any production
code — more, because the behavior is less predictable. Run through
this list before deploying an agent workflow on real data.

### Sandbox execution

- [ ] Agent code runs inside `uv run`, a container, or a VM — not
      directly on the host with full access.
- [ ] File system access is limited to the working directory. No
      writes outside the project tree.
- [ ] Network access is restricted or disabled if not needed.

### Scoped permissions

- [ ] Agents have read-only access to source data by default.
- [ ] Write access is granted only to specific output directories.
- [ ] API keys are scoped to minimum required permissions.
- [ ] No agent has credentials to production systems.

### Local-only data stores

- [ ] Sensitive documents are processed locally, not sent to
      third-party services unless explicitly authorized.
- [ ] Intermediate results (SQLite, ChromaDB, temp files) stay on
      the local machine or in a controlled environment.
- [ ] Embeddings of sensitive content are treated with the same
      access controls as the original content.

### Audit trail

- [ ] Every agent action is logged with timestamp, agent identity,
      action type, and input/output summary.
- [ ] Logs are append-only — agents cannot modify or delete them.
- [ ] The audit trail captures which criteria were evaluated, what
      findings were produced, and what was marked as clean.

### Human-in-the-loop checkpoints

- [ ] At least one human review step before any agent output is
      treated as final or sent to a stakeholder.
- [ ] Agents surface confidence levels or uncertainty markers so
      reviewers know where to focus attention.
- [ ] The workflow can be paused and resumed without losing state.

### Blast radius limits

- [ ] You can answer: "What is the worst thing this agent could do?"
- [ ] The answer is acceptable. If not, add constraints until it is.
- [ ] Agents cannot delete, overwrite, or exfiltrate source data.
- [ ] Failure of one agent does not corrupt shared state or block
      other agents in the workflow.

---

## 5. Engineering Parallels

The patterns in agent-driven document review map directly to practices
software engineers already use. If you have built a CI/CD pipeline or
written acceptance tests, you already know the underlying concepts.

| Document Review | Software Engineering |
|---|---|
| Criteria files | Test specs / acceptance criteria |
| Adversarial agent | Code review / QA |
| Audit trail | CI logs / compliance records |
| Pipeline handoffs | CI/CD stages |
| Data loader | ETL / data pipeline |
| Eval skill | Test runner / linter |

### Criteria files → Test specs

A criteria file tells the agent what "correct" looks like and what
patterns indicate problems. This is exactly what a test spec or
acceptance criteria document does for a feature. In both cases, you
are writing down the expected behavior before evaluating the artifact.
The discipline of writing criteria first forces you to think clearly
about what you are actually checking — the same benefit as test-driven
development.

### Adversarial agent → Code review

The adversarial reviewer's job is to find problems the first agent
missed. This is the same role a code reviewer plays: a fresh set of
eyes looking for bugs, edge cases, and unstated assumptions. In both
cases, the value comes from having a different perspective applied to
the same artifact. The adversarial agent can even use a different model
to reduce the chance of shared blind spots.

### Audit trail → CI logs

Every agent action is logged with a timestamp and actor identity. This
is the agent equivalent of CI build logs and compliance records. When
something goes wrong — or when someone asks "why did the system flag
this clause?" — the audit trail provides the answer. In regulated
industries, this traceability is not optional; it is a requirement.

### Pipeline handoffs → CI/CD stages

A document review pipeline (parse → analyze → report) mirrors a CI/CD
pipeline (build → test → deploy). Each stage has a defined input and
output contract. If one stage fails, subsequent stages do not run. The
handoff between stages is explicit and inspectable, which makes
debugging straightforward.

### Data loader → ETL

The data loader skill parses a PDF, extracts structured content, and
loads it into a local database. This is a textbook ETL process: extract
from the source format, transform into a queryable schema, load into a
data store. The same patterns (schema validation, error handling,
idempotency) apply in both contexts.

### Eval skill → Test runner

The eval skill takes a criterion, applies it to the loaded data, and
produces a pass/fail result with evidence. This is what a test runner
does: take a test spec, execute it against the system under test, and
report results. The eval skill even uses the same red/green/yellow
vocabulary that test runners use for pass/fail/warning.
