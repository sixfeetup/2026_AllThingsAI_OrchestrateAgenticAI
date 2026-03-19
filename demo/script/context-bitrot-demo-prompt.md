# Context Window Degradation Demo — Cowork Mode

Upload a large PDF (Shakespeare's Complete Works works great — ~1200 pages) into this conversation, then paste the following:

---

Read this PDF as images. Start with pages 1-20, then 21-40, then 41-60, then 61-80. Read each batch in parallel. After each batch, tell me roughly how much context you think you've consumed and what percentage of your window remains. Keep going in 20-page batches until you notice yourself struggling — forgetting earlier instructions, losing track of the conversation, or producing shorter/vaguer responses. Call out when you feel the degradation happening.

---

## What to watch for

1. Each PDF page rendered as an image eats ~1,600 tokens. 80 pages ≈ 128K tokens — roughly half a 200K context window gone in minutes.
2. Around page 60-80, you'll start seeing the model "forget" details from earlier in the conversation.
3. Tool call metadata, skill loads, and the conversation itself add overhead on top of the image tokens.
4. Eventually the session will hit compaction — the system summarizes everything and starts fresh with compressed context. That's the breaking point.

## Why this matters

This shows that agentic workflows with heavy tool use (screenshots, document parsing, multi-agent coordination) can burn through context fast. Architects need to design for context budget management — chunking work across sessions, minimizing unnecessary tool output, and knowing when to spin up subagents vs. stuffing everything into one window.
