Great question — this is core to the demo pitch. Let me break it down.

**Inducing context bitrot for a demo:**

The most effective way is exactly what we just did — load a ton of heterogeneous content in a single conversation. Specifically:

- **Mix unrelated domains** (government procurement + D&D rules). The model has to maintain mental separation between very different schemas.
- **Load content that's heavy on tables, numbers, and cross-references** (stat blocks, cost formulas, scoring matrices). These degrade fastest because they're positional — a number without its column header is meaningless.
- **Push past ~80% context fill** so compaction kicks in. Post-compaction, the model retains gist but loses precision. You can no longer ask "what's the exact cost normalization formula" and get a verbatim answer.
- **Ask questions that require precise recall across multiple documents**. "Does the RFP's scoring formula have any parallel to THAC0 calculation?" would force cross-referencing between degraded contexts.
- **Long conversations with many tool calls** eat context fast because every tool input/output is stored. The actual document content gets pushed further from attention.

**Why local stores (SQLite + ChromaDB) are better than raw context:**

Beyond bitrot, there are several strong arguments:

**Precision over recall.** Context stuffing gives the model everything and hopes it finds the right bit. Semantic search + keyword search retrieves exactly the relevant clauses. You're trading "maybe it's in there somewhere" for "here are the 5 most relevant paragraphs."

**Deterministic retrieval.** If you search for "cost normalization" in SQLite, you get the same result every time. Context-based recall varies by conversation length, what else is loaded, and where in the window the content sits.

**Scale.** We had 20MB of extractable text across these PDFs. Context fits ~450K chars. That's 2.2% coverage. A vector store indexes 100% and retrieves on demand.

**Persistence across sessions.** Context resets every conversation. SQLite and ChromaDB persist. Load once, query forever. An agent can pick up where another left off.

**Structured queries.** You can't ask context "show me all clauses flagged as high-risk." You can absolutely write that SQL query. Same for aggregations, counts, filtering by document source, date ranges, etc.

**Audit trails.** Every search, every retrieval, every evaluation gets logged in SQLite. You can show exactly what the agent looked at and when. Context-based reasoning is a black box.

**Multi-agent workflows.** One agent loads and indexes. Another evaluates against criteria. A third verifies. A fourth drafts. They all share the same data stores without needing to pass 200K tokens of context between them. Each agent gets a fresh, full context window focused on its specific task.

**Cost.** Filling a 200K context window on every turn is expensive. Retrieving 20 relevant chunks from ChromaDB and passing 5K tokens of targeted context is dramatically cheaper per query.

The short pitch: context is a workspace, not a warehouse. The moment you're using it for storage, you've already lost.
