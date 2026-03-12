# Talk Delivery Checklist

## Must cover

- [ ] Context engineering: chunking, prompt framing, checklists,
      acceptance criteria, traceability
- [ ] Agentic workflows: decomposing tasks into sub-jobs with
      routing and validation
- [ ] Live "No-Miss Review" demo (task graphs, specialized agents,
      routing, validation)
- [ ] Map demo patterns to engineering workflows (code review,
      test planning)
- [ ] Actionable playbook: takeaway artifact attendees can use
- [ ] Reliability + auditability: how to reach "trusted" standard
- [ ] Dual-domain relevance: business/legal AND engineering

## Must demonstrate

- [ ] Speaker has solved the problem (not a landscape survey)
- [ ] Approach beats current tooling (not just MCP/chat wrappers)
- [ ] Demo uses realistic artifact (not a toy example)
- [ ] Patterns generalize beyond demo domain (concrete parallels)
- [ ] Orchestration guidance: when to use which style
- [ ] Eventual consistency: show iterative validation converging

## Must deliver

- [ ] Audit trail / governance: provable process, not just prompts
- [ ] Safety + containment: specific techniques for blast radius
- [ ] Playbook artifact: repo, template, or checklist to take home
- [ ] Practical > theoretical: attendees can replicate the approach

## Demo workspace

- [x] `demo/plan.md` is the canonical source of truth for the demo
- [x] `demo/README.md` is optimized for fast use under stress
- [x] `demo/explainers-plan.md` defines the required visual explainers
- [x] Conference demo spec exists in `specs/001-conference-demo/spec.md`
- [x] Conference demo plan exists in `specs/001-conference-demo/plan.md`
- [x] Postgres is the fixed demo database choice
- [x] Fake buildpack artifact is defined as a vulnerable `Dockerfile`
- [x] Predetermined-state cutover is part of each demo segment design

## Tooling and operator setup

- [x] Vendored speckit skills can be installed locally
- [x] Short `sk-*` aliases can be installed for speckit skills
- [x] Repo-local Codex launcher exists with Ralph MCP enabled
- [x] Repo-local Codex demo-mode launcher exists
- [x] Ralph MCP launcher prefers the Cargo-installed `ralph` binary
- [x] Local skill frontmatter repair helper exists for broken Codex skills

## Next implementation items

- [ ] Create `demo/Makefile`
- [ ] Add Postgres scaffolding under `demo/`
- [ ] Add vulnerable `Dockerfile` specimen under `demo/`
- [ ] Build the highest-priority explainers from `demo/explainers-plan.md`
- [ ] Add prepared artifacts for each demo segment fallback
- [ ] Run `speckit-tasks` for the conference demo feature
