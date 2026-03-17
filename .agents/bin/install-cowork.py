#!/usr/bin/env python3
"""Install all Claude Desktop / cowork integration files.

Run: python3 .agents/bin/install-cowork.py
"""
import os
import textwrap

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DEMO = os.path.join(ROOT, "demo")

FILES = {}

# --- 1. MCP server script ---
FILES[os.path.join(ROOT, ".agents/bin/contract-mcp-server.py")] = textwrap.dedent('''\
    #!/usr/bin/env python3
    """MCP server exposing contract review tools over stdio.

    Usage:
        uv run --with 'mcp,pymupdf,chromadb,sentence-transformers' contract-mcp-server.py

    Exposes the contract pipeline (parse, load, search, audit) as MCP tools
    so Claude Desktop, Cowork, or any MCP client can drive the review workflow
    without needing Claude Code CLI.
    """
    from __future__ import annotations

    import json
    import sqlite3
    import subprocess
    import sys
    from pathlib import Path

    from mcp.server.fastmcp import FastMCP

    SCRIPT_DIR = Path(__file__).resolve().parent
    DEMO_DIR = SCRIPT_DIR.parent.parent / "demo"
    DEFAULT_DB = DEMO_DIR / "data" / "contracts.db"
    DEFAULT_CHROMA = DEMO_DIR / "data" / "chroma"
    PARSE_SCRIPT = SCRIPT_DIR / "contract-parse.py"
    LOAD_SCRIPT = SCRIPT_DIR / "contract-load.py"
    SEARCH_SCRIPT = SCRIPT_DIR / "contract-search.py"
    DEFAULT_PDF = DEMO_DIR / "assets" / "contracts" / "bigco-msa.pdf"

    server = FastMCP(
        "contract-review",
        instructions=(
            "Contract review pipeline tools. Use these to parse, load, search, "
            "and audit contract documents. Typical workflow: load a contract PDF, "
            "search for relevant clauses, evaluate against criteria, then review "
            "the audit trail."
        ),
    )


    @server.tool()
    def load_contract(pdf_path: str = "") -> str:
        """Parse a contract PDF and load clauses into SQLite + ChromaDB.

        Args:
            pdf_path: Path to the contract PDF. Defaults to the demo contract.
        """
        if not pdf_path:
            pdf_path = str(DEFAULT_PDF)
        pdf = Path(pdf_path)
        if not pdf.exists():
            return f"Error: PDF not found at {pdf_path}"
        result = subprocess.run(
            [sys.executable, str(LOAD_SCRIPT), str(pdf),
             "--db", str(DEFAULT_DB), "--chroma", str(DEFAULT_CHROMA)],
            capture_output=True, text=True,
        )
        output = result.stderr.strip()
        if result.returncode != 0:
            return f"Error loading contract: {output}"
        return f"Contract loaded successfully.\\n\\n{output}"


    @server.tool()
    def search_contract(
        query: str, section: str = "", flag: str = "",
        full: bool = False, top: int = 10,
    ) -> str:
        """Search loaded contract clauses using semantic + keyword search.

        Args:
            query: Search query (e.g. "intellectual property", "termination").
            section: Filter by section number pattern (e.g. "4.*").
            flag: Filter by topic flag (e.g. "ip", "payment").
            full: Show full clause body instead of snippet.
            top: Number of results to return.
        """
        if not DEFAULT_DB.exists():
            return "Error: No contract loaded. Use load_contract first."
        cmd = [sys.executable, str(SEARCH_SCRIPT), query,
               "--db", str(DEFAULT_DB), "--chroma", str(DEFAULT_CHROMA),
               "--top", str(top), "--json"]
        if section:
            cmd.extend(["--section", section])
        if flag:
            cmd.extend(["--flag", flag])
        if full:
            cmd.append("--full")
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            return f"Search error: {result.stderr.strip()}"
        try:
            hits = json.loads(result.stdout)
        except json.JSONDecodeError:
            return result.stdout
        if not hits:
            return f"No results found for: {query}"
        lines = [f"Found {len(hits)} results for: {query}\\n"]
        for h in hits:
            sec = h["section_number"]
            title = h.get("section_title", "")
            score = h.get("score", 0)
            body = h.get("body", "")
            snippet = body if full else body[:200].replace("\\n", " ")
            label = f"{title}: {snippet}" if title else snippet
            lines.append(f"  [{sec}] (score: {score:.2f}) {label}")
        return "\\n".join(lines)


    @server.tool()
    def audit_contract() -> str:
        """Display the audit trail of all contract analysis actions."""
        if not DEFAULT_DB.exists():
            return "Error: No contract loaded."
        conn = sqlite3.connect(str(DEFAULT_DB))
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            "SELECT id, timestamp, action, actor, detail "
            "FROM audit_log ORDER BY id"
        ).fetchall()
        conn.close()
        if not rows:
            return "Audit log is empty."
        lines = ["# Audit Trail\\n"]
        for row in rows:
            detail = row["detail"] or ""
            try:
                detail = json.dumps(json.loads(detail), indent=2)
            except (json.JSONDecodeError, TypeError):
                pass
            lines.append(
                f"**[{row['id']}]** {row['timestamp']} | "
                f"action={row['action']} | actor={row['actor']}\\n"
                f"```json\\n{detail}\\n```\\n"
            )
        return "\\n".join(lines)


    @server.tool()
    def list_criteria_files() -> str:
        """List available criteria files for contract evaluation."""
        criteria_dir = DEMO_DIR / "assets" / "criteria"
        if not criteria_dir.exists():
            return "Error: Criteria directory not found."
        files = sorted(criteria_dir.glob("*.md"))
        if not files:
            return "No criteria files found."
        lines = ["# Available Criteria Files\\n"]
        for f in files:
            content = f.read_text()
            headings = [l.strip("# ").strip() for l in content.split("\\n") if l.startswith("## ")]
            lines.append(f"**{f.name}** ({len(headings)} criteria)")
            for h in headings:
                lines.append(f"  - {h}")
            lines.append("")
        return "\\n".join(lines)


    @server.tool()
    def get_contract_stats() -> str:
        """Get summary statistics about the loaded contract."""
        if not DEFAULT_DB.exists():
            return "Error: No contract loaded."
        conn = sqlite3.connect(str(DEFAULT_DB))
        conn.row_factory = sqlite3.Row
        total = conn.execute("SELECT COUNT(*) as cnt FROM clauses").fetchone()["cnt"]
        pages = conn.execute(
            "SELECT MIN(page_start) as mn, MAX(page_end) as mx FROM clauses"
        ).fetchone()
        rows = conn.execute("SELECT flags FROM clauses WHERE flags IS NOT NULL").fetchall()
        conn.close()
        flag_counts: dict[str, int] = {}
        for row in rows:
            try:
                for flag in json.loads(row["flags"]):
                    flag_counts[flag] = flag_counts.get(flag, 0) + 1
            except (json.JSONDecodeError, TypeError):
                pass
        lines = [
            "# Contract Statistics\\n",
            f"- **Total clauses:** {total}",
            f"- **Pages:** {pages['mn']} to {pages['mx']}",
            "",
            "## Flag Distribution",
        ]
        for flag, count in sorted(flag_counts.items(), key=lambda x: -x[1]):
            lines.append(f"  - {flag}: {count} clauses")
        return "\\n".join(lines)


    @server.tool()
    def read_criteria_file(filename: str) -> str:
        """Read a criteria file's contents.

        Args:
            filename: e.g. "ip-and-ownership.md"
        """
        criteria_dir = DEMO_DIR / "assets" / "criteria"
        filepath = criteria_dir / filename
        if not filepath.exists():
            available = [f.name for f in criteria_dir.glob("*.md")]
            return f"Error: '{filename}' not found. Available: {', '.join(available)}"
        return filepath.read_text()


    if __name__ == "__main__":
        server.run(transport="stdio")
''')

# --- 2. MCP project config ---
FILES[os.path.join(DEMO, ".mcp.json")] = textwrap.dedent('''\
    {
      "mcpServers": {
        "contract-review": {
          "command": "uv",
          "args": [
            "run", "--with", "mcp,pymupdf,chromadb,sentence-transformers",
            "../.agents/bin/contract-mcp-server.py"
          ]
        }
      }
    }
''')

# --- 3. Demo CLAUDE.md ---
FILES[os.path.join(DEMO, "CLAUDE.md")] = textwrap.dedent('''\
    # Contract Review Demo

    This directory contains a contract review pipeline demo for a conference talk
    on building agentic AI systems with Claude Code.

    ## Quick Start

    ```bash
    # Reset and load the demo contract
    make reset

    # Or step-by-step:
    make contract   # generate the PDF
    make load       # parse + load into SQLite/ChromaDB
    make search Q="intellectual property"   # test a search
    ```

    ## Available Skills

    | Skill | Trigger | What it does |
    |-------|---------|-------------|
    | contract-loader | `/load-contract` | Parse PDF, load into SQLite + ChromaDB |
    | contract-search | `/search-contract <query>` | Semantic + keyword search |
    | contract-eval | `/eval-contract [criteria]` | Evaluate against criteria file |
    | contract-audit | `/audit-contract` | Show audit trail |

    ## Available MCP Tools

    The `contract-review` MCP server exposes the same pipeline as tools:
    - `load_contract` — parse and load a PDF
    - `search_contract` — dual semantic + keyword search
    - `audit_contract` — view audit trail
    - `get_contract_stats` — clause counts and flag distribution
    - `list_criteria_files` / `read_criteria_file` — browse eval criteria

    ## Agent Templates

    Agent templates in `.agents/` define specialized roles:
    - **data-loader-agent** — ingestion and data quality
    - **contract-eval-agent** — systematic clause analysis
    - **data-investigator-agent** — exploratory forensic analysis
    - **verification-agent** — red team / adversarial review
    - **response-drafter-agent** — draft professional response memo

    ## Cowork Workflow

    For multi-agent review using Claude Desktop or cowork:

    1. **Load phase**: Use `load_contract` tool to ingest the PDF
    2. **Eval phase**: Apply criteria files via `search_contract` + LLM judgment
    3. **Verify phase**: Challenge findings with adversarial perspective
    4. **Draft phase**: Produce response memo from verified findings
    5. **Audit phase**: Review the full trail with `audit_contract`

    Each phase can be handled by a different Claude instance or agent role.

    ## Data Stores

    - `data/contracts.db` — SQLite (clauses + audit_log tables)
    - `data/chroma/` — ChromaDB vector store
    - Both are ephemeral — `make clean` removes them

    ## Constraints

    - All deps via `uv run --with` (never pip)
    - Everything runs locally (no external services)
    - The contract is fake (L&LL LLC) — demo-safe
''')

# --- 4. Cowork review skill ---
FILES[os.path.join(DEMO, ".claude/skills/cowork-review/skill.md")] = textwrap.dedent('''\
    # Cowork Contract Review Pipeline

    **Trigger:** `/cowork-review [pdf-path]`

    Orchestrate a full multi-agent contract review. This skill coordinates
    the complete pipeline: load, evaluate, verify, and draft a response.

    ## Workflow

    ### Step 1: Load the Contract
    Run the contract-loader skill (or MCP `load_contract` tool) on the PDF.
    Default: `assets/contracts/bigco-msa.pdf`

    Verify the load succeeded — check clause count (expect 100+) and page coverage.

    ### Step 2: Focused Evaluation
    Run eval against `assets/criteria/ip-and-ownership.md`:
    - For each criterion heading, search the contract for relevant clauses
    - Rate severity: CRITICAL / HIGH / MEDIUM / LOW / CLEAR
    - Cite specific section numbers and quote evidence

    ### Step 3: Broad Red Flag Scan
    Run eval against `assets/criteria/general-red-flags.md`:
    - Same process as Step 2 but with broader criteria
    - Look for impossible dates, party name errors, one-sided terms,
      buried material terms, undefined obligations, hidden provisions

    ### Step 4: Adversarial Review
    Switch to the verification-agent persona. For each finding from Steps 2-3:
    - Construct a counter-argument
    - Search for exculpatory context elsewhere in the contract
    - Verdict: `upheld`, `downgraded`, or `dismissed`
    - Be rigorous but fair — don't dismiss legitimate issues

    ### Step 5: Draft Response
    Switch to response-drafter-agent persona:
    - Group verified findings by severity and topic
    - Draft a professional memo with:
      - Executive summary
      - Detailed findings with clause references
      - Recommended changes / redlines
      - Prioritization (must-fix vs nice-to-have)
    - Tone: professional, constructive, firm on critical issues

    ### Step 6: Audit Trail
    Run `/audit-contract` to display the full provenance trail.

    ## Output
    Save the final report to `data/review-report.md` with all sections:
    findings, verification results, response draft, and audit summary.

    ## Cowork Notes
    When running in cowork mode (multiple Claude instances):
    - Each step can be assigned to a different instance
    - Use the shared SQLite DB as the coordination point
    - The audit_log table tracks which agent did what and when
    - Pass findings between steps as markdown — each step reads the
      previous step's output and builds on it
''')

# --- Write all files ---
for fp, content in FILES.items():
    os.makedirs(os.path.dirname(fp), exist_ok=True)
    with open(fp, "w") as f:
        f.write(content)
    print(f"  wrote {fp}")

# Make MCP server executable
os.chmod(os.path.join(ROOT, ".agents/bin/contract-mcp-server.py"), 0o755)
print("\nDone. 4 files created.")
