# Loot Table: Repository Structure
*File: loot-table-repo-structure.md*

To deliver on the "Actionable Playbook" promise, this repository structure should be shared with the audience as a "Starter Kit."

```text
agentic-quest-starter/
├── .claude/
│   ├── CLAUDE.cleric.md      # Governance & Audit Rules
│   ├── CLAUDE.wizard.md      # Logic & Contradiction Rules
│   └── CLAUDE.ranger.md      # Security & Containment Rules
├── artifacts/
│   ├── sample-contract.md    # The "Dungeon Map" (Synthetic)
│   └── audit-report-template.md
├── scripts/
│   ├── run-level-1.sh        # Single-shot prompt (The "Failure" demo)
│   ├── run-level-2.sh        # Multi-agent orchestration script
│   └── run-level-3.sh        # Autonomous loop with verification
├── tools/
│   ├── mcp-server-contract/  # Custom MCP server for clause extraction
│   └── sandbox-executor/     # Docker-based containment script
├── README.md                 # The Playbook (How to use this kit)
└── LICENSE                   # Open Source (MIT)
```

## Key Playbook Sections:
1.  **The "Trust Graduation" Checklist:** 5 criteria for moving a task from Level 1 to Level 2.
2.  **The "Adversarial" Prompt Template:** How to use one LLM to red-team another.
3.  **The "Human-in-the-Loop" Hand-off:** Defining the JSON schema for when a human must intervene.
