# Pre-Demo Setup

Run these checks **the night before** your talk, then again **15 minutes before** your slot.

---

## Night Before

### 1. Environment

```bash
cd demo

# Create venv and install all deps
make pre-demo-setup

# Verify offline readiness
make preflight
```

Expected output: all checks pass, model loads offline, data cache exists.

### 2. Model Cache

The `pre-demo-setup` target warms both:
- `demo/.model-cache/` (used by Makefile targets)
- `~/.cache/huggingface/` (used by live skill invocations)

Verify both exist:
```bash
ls .model-cache/
ls ~/.cache/huggingface/hub/
```

### 3. Data Snapshots

Verify cached data exists for instant fallback:
```bash
ls data-cache/loaded/documents.db
ls data-cache/loaded/chroma/
```

### 4. Prebaked Outputs

Verify fallback files exist:
```bash
ls assets/prebaked/naive-review.md
ls assets/prebaked/document-review-checklist.md
ls assets/prebaked/bitrot-research.md
ls assets/criteria/ip-and-ownership.md
ls assets/criteria/general-red-flags.md
```

### 5. Claude Code

```bash
# Verify CLI works
claude -p "respond with just ok" --max-turns 1

# Open a session in demo/, verify skills appear
cd demo && claude
# Type: /help — confirm /load-document, /search-document, /eval-document, /audit-document
# Exit
```

### 6. Claude Desktop (if using hybrid script)

- Open Claude Desktop
- Verify `demo/.mcp.json` is picked up (the `document-review` MCP server should connect)
- Check tools appear: `load_document`, `search_document`, `audit_document`, etc.
- Pre-populate a session with some unrelated conversation (for Step 0 polluted context)

### 7. Slides

```bash
cd presentation && make build-reveal && make open-reveal
```

Verify slides render. Set browser zoom for projector readability (100-125%).

### 8. Full Dry Run

Walk through the entire demo script once. Time each step. Note slow spots.

### 9. Backup

```bash
# After successful dry run, snapshot everything
tar czf ~/demo-backup-$(date +%Y%m%d).tar.gz demo/.model-cache demo/data-cache demo/data
```

---

## 15 Minutes Before

```bash
cd demo

# 1. Clean slate
make clean

# 2. Verify archive
make document

# 3. Quick preflight
make preflight

# 4. Open Claude Code, leave at prompt
claude
```

### macOS Checklist

- [ ] **Do Not Disturb** — System Settings > Focus > Do Not Disturb ON
- [ ] **Display sleep** — System Settings > Displays > Turn off after: Never
- [ ] **Power** — plugged in
- [ ] **Terminal font** — 18-20pt minimum
- [ ] **Terminal width** — ~100 columns (wider = smaller text on projector)
- [ ] **Dark/light theme** — test with the actual projector during sound check

### Browser (for slides)

- [ ] Open `presentation/output/deck-reveal.html` in Chrome
- [ ] Fullscreen on projector display (F key in reveal.js)
- [ ] Presenter laptop shows Claude Code terminal

### Recovery Kit

If something breaks mid-demo:

| Situation | Recovery |
|-----------|----------|
| Load fails/slow | `make load-cached` — instant restore |
| Claude Code crashes | `cd demo && claude` — data persists on disk, resume from current step |
| API is slow | Narrate what would happen, show prebaked outputs |
| API is down | Run the entire demo from prebaked files with narration |
| WiFi drops | Local search/audit still works. Eval/adversarial/draft need API — fall back to prebaked |

### Phone Tether

Know your phone hotspot password. Test it connects. This is your backup if venue WiFi fails.
