# Demo Implementation — Contract Review Agents & Skills

## Summary

- Built the complete demo toolchain: 4 Claude Code skills (load, search, eval, audit), 5 agent templates (data-loader, contract-eval, data-investigator, verification, response-drafter), and 3 Python scripts (parse, load, search) for agentic contract review of a fake MSA with 7 planted problems.
- Created PDF parser (`contract-parse.py`) that extracts 142 clauses from a generated 30-page MSA, with section/exhibit detection and heuristic flag assignment.
- Implemented dual-store search pipeline: SQLite for structured clause storage + ChromaDB for semantic search, with merged/deduplicated results and audit logging.
- Built 2 criteria files (`ip-and-ownership.md`, `general-red-flags.md`), a naive-review contrast piece, a playbook take-home, and bitrot research document for the context degradation demo segment.
- Created `bitrot-simulator.py` with 5 modes (verbose, tangent, contradict, history, all) for generating context pollution, plus `verify-demo.sh` confirming all 27/27 checks pass.

## Session Log

### Phase 1: Specification & Planning

- Ran `/sk specify` to create `demo/spec.md` defining 4 skills, 5 agents, criteria files, and demo flow
- Ran `/sk clarify` twice — added criteria files section, interactive-first demo flow, cross-referenced `presentation/checklist.md`
- Ran `/sk plan` to create `demo/plan.md` with 5 implementation phases and dependency graph
- Ran `/sk tasks` to break into 18 actionable tasks

### Phase 2: Core Implementation

- Built `contract-parse.py` — PDF text extraction via PyMuPDF with regex-based clause detection
- Built `contract-load.py` — loads parsed clauses into SQLite + ChromaDB
- Built `contract-search.py` — dual semantic + keyword search with score merging
- Built `test-parse.py` — smoke test validating all 7 planted problems + cupcake findable
- Created all 4 skill markdown files and 5 agent templates
- Created `demo/Makefile` with targets: contract, load, search, test, clean, reset

### Phase 3: Supporting Materials (parallel agents)

- `demo/assets/criteria/ip-and-ownership.md` — 3 criteria for IP-focused eval
- `demo/assets/criteria/general-red-flags.md` — 6 criteria covering all planted problems
- `demo/assets/prebaked/naive-review.md` — deliberately shallow "ask ChatGPT" contrast
- `demo/assets/playbook.md` — attendee take-home document
- `demo/assets/prebaked/contract-review-checklist.md` — prebaked review checklist
- `demo/assets/prebaked/skill-example.md` — skill example for slides

### Phase 4: Verification & Bitrot Research

- Built `verify-demo.sh` — 27 checks all passing (file existence + pipeline smoke test)
- Created `bitrot-simulator.py` — context pollution generator (5 modes, intensity 1-10)
- Created `demo/assets/prebaked/bitrot-research.md` — research on context degradation with demo plan

### Key Debugging

- Fixed bare clause number regex (PDF puts `2.1` alone on lines)
- Fixed TOC noise detection in parser
- Fixed ChromaDB `delete_collection` API change
- Fixed bash arithmetic exit code issue in verify script

---
*Session completed: 2026-03-16 (continued from compacted session)*
