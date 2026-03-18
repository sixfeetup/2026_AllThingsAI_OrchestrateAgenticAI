# Hybrid Demo Setup — Step by Step

How to configure Claude Desktop + Claude Code for the hybrid demo.
Do this **the night before** and verify it works end-to-end.

---

## Step 1: Complete the base setup

Run everything in [predemo.md](predemo.md) first. This gives you:
- uv venv with all deps
- Model cache (warm)
- Data cache snapshots
- Claude Code CLI verified

---

## Step 2: Configure Claude Desktop to find the MCP server

Claude Desktop discovers MCP servers from a project-level `.mcp.json`.
Ours is at `demo/.mcp.json` and configures the `document-review` server.

### Option A: Open Claude Desktop from the demo directory

If you launch Claude Desktop while the `demo/` directory is your active
project, it should pick up `.mcp.json` automatically.

1. Open Claude Desktop
2. Use File > Open Project (or equivalent) and point it at the `demo/` directory
3. The `document-review` MCP server should connect

### Option B: Copy the config to Claude Desktop's global config

If project-level detection isn't working:

```bash
# Find Claude Desktop's config location
# Typically: ~/Library/Application Support/Claude/claude_desktop_config.json

# Add the MCP server entry:
cat demo/.mcp.json
# Copy the "mcpServers" block into your claude_desktop_config.json
```

The server config is:
```json
{
  "mcpServers": {
    "document-review": {
      "command": "uv",
      "args": [
        "run", "--with", "mcp,pymupdf,chromadb,sentence-transformers",
        "/ABSOLUTE/PATH/TO/.agents/bin/document-mcp-server.py"
      ]
    }
  }
}
```

**Important:** If copying to the global config, use the **absolute path** to
`document-mcp-server.py` (the project `.mcp.json` uses a relative path that
only works from `demo/`).

### Verify

In any Claude Desktop window, type:

> "What MCP tools do you have available?"

You should see: `load_document`, `search_document`, `audit_document`,
`get_document_stats`, `list_criteria_files`, `read_criteria_file`.

If not, check:
- Is `uv` on your PATH? (Claude Desktop may not inherit shell profile)
- Does the absolute path to the script resolve?
- Restart Claude Desktop after config changes

---

## Step 3: Pre-load data from the terminal

Claude Desktop windows will use the MCP tools, which read from `demo/data/`.
The data needs to exist before Step 10.

Load it from Claude Code (you'll do this during Step 2 of the live demo):

```bash
cd demo
uv run --with 'pymupdf,chromadb,sentence-transformers,python-docx,openpyxl,path' \
  ../.agents/bin/document-load.py "assets/1-RFP 20-020 - Original Documents.zip" \
  --db data/documents.db --chroma data/chroma
```

Or restore from cache:

```bash
make load-cached
```

Verify:
```bash
sqlite3 data/documents.db "SELECT COUNT(*) FROM clauses"
# Should return 97
```

---

## Step 4: Set up Window 1 — "Polluted" (for Step 0)

This window is for the OH NO moment.

1. Open a Claude Desktop conversation
2. Have a few exchanges about **unrelated topics** — code, other questions,
   whatever. The point is to have a messy, polluted context.
3. **Don't close this window.** You'll paste RFP text into it during Step 0.

### Prepare the paste text

Copy a section of the RFP to your clipboard (or save it to a file for quick copy).
Good sections to paste:
- The scope of work (Section 1.4 in the main RFP PDF)
- The evaluation criteria (Section 3.2)

You can extract a section with:
```bash
uv run --with 'pymupdf,chromadb,sentence-transformers' \
  .agents/bin/document-search.py "scope of work" \
  --db data/documents.db --chroma data/chroma --full --top 1
```

Copy that output to your clipboard.

---

## Step 5: Set up Window 2 — "Verifier" (for Step 10)

1. Open a **new** Claude Desktop conversation (fresh, clean context)
2. Go to the project settings / system instructions for this conversation
3. Paste the following as the system instructions:

```
You are opposing counsel. Your job is to take the eval agent's findings
and argue against them — stress-testing each one to separate genuine
issues from false positives and overstatements.

Challenge every finding. Construct counter-arguments. Determine which
findings hold up under scrutiny and which should be downgraded or
dismissed.

For each finding:
1. Read the finding — understand the claimed issue and evidence.
2. Use the search_document tool to find counter-evidence.
3. Use the audit_document tool to see what analysis has been done.
4. Construct a defense: Is this standard practice? Is there qualifying
   context elsewhere?
5. Render a verdict: Upheld, Downgraded, or Dismissed.

Be rigorous but fair. The goal is to improve confidence, not rubber-stamp.
Always cite specific evidence for counter-arguments.
```

4. Verify MCP tools are available (ask "what tools do you have?")
5. **Minimize this window** — you'll use it during Step 10

---

## Step 6: Set up Window 3 — "Drafter" (for Step 10)

1. Open another **new** Claude Desktop conversation
2. Paste the following as system instructions:

```
You are a business communicator. Your job is to take verified findings
and draft a professional response memo.

Procedure:
1. Use the audit_document tool to review all findings and verdicts.
2. Group verified findings by severity (CRITICAL, HIGH, MEDIUM).
3. Draft a response memo with:
   - Executive summary (2-3 sentences)
   - Critical issues (must resolve)
   - High-priority concerns
   - Moderate items
   - Positive notes (what's good)
   - Proposed next steps

Write for a business audience. Be specific — quote section numbers
and clause text. Maintain a collaborative tone. Suggest concrete
alternatives, not just "this is problematic."
```

3. Verify MCP tools are available
4. **Minimize this window** — you'll use it during Step 10

---

## Step 7: Arrange your displays

### Projector/external display
- Chrome with reveal.js slides fullscreen (F key)

### Laptop screen
Layout depends on the phase:

**During Steps 0:** Claude Desktop Window 1 visible
**During Steps 1-9:** Claude Code terminal fullscreen
**During Step 10:** Tile Windows 2 + 3 side by side

Practice the window switching:
- Cmd+Tab between Claude Desktop and Terminal
- Use Mission Control or a tiling manager to quickly arrange Windows 2+3

---

## Step 8: Dry run

Walk through the full hybrid script once:

1. **Step 0:** Switch to Window 1, paste RFP text, type "Review this for issues"
   - Verify you get vague output
2. **Switch to terminal.** Run Steps 1-9 in Claude Code
3. **Step 10:** Switch to Window 2, type "Check the audit trail and challenge the findings"
   - Verify it calls `audit_document` and `search_document`
   - Verify it produces verdicts
4. Switch to Window 3, type "Check the audit trail for verified findings and draft a response memo"
   - Verify it calls `audit_document`
   - Verify it produces a memo
5. In either window, type "Show me the complete audit trail"
   - Verify entries from both CLI and Desktop appear

### Timing

Time each step. The cowork segment (Step 10) should take ~1:30.
If it runs long, you can abbreviate by showing just the verifier window
and describing what the drafter would do.

---

## Troubleshooting

### MCP tools not appearing in Claude Desktop

- Restart Claude Desktop after any config change
- Check that `uv` is on the PATH that Claude Desktop inherits
  (it may not source your `.zshrc` — try adding uv's path to
  `/etc/paths.d/` or using an absolute path in the config)
- Verify the script runs from the command line:
  ```bash
  uv run --with 'mcp,pymupdf,chromadb,sentence-transformers' \
    .agents/bin/document-mcp-server.py
  ```
  It should start and wait for input (ctrl+C to exit)

### "No data loaded" errors in Desktop windows

The MCP server reads from `demo/data/documents.db`. Make sure data is
loaded (Step 3 above) before using the Desktop windows.

### Database locking

SQLite handles concurrent reads fine. If two windows try to write
simultaneously (e.g., both searching at the same time, which logs to
audit_log), you might get a brief lock. This is rare and self-resolving —
just wait a moment and retry.

### Desktop gives different output format than expected

Claude Desktop doesn't have skill files guiding its output format.
The system instructions in Steps 5-6 above include format guidance,
but Claude may deviate. This is acceptable for the demo — the point
is showing multi-agent coordination, not pixel-perfect output.

### Fallback

If Claude Desktop isn't cooperating at all, fall back to the
[terminal script](terminal.md). Steps 7-8 already have CLI commands
for adversarial review and response drafting. The audience won't know
there was a cowork segment planned.
