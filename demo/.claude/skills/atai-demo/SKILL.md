# atai-demo

Demo prompt navigator. Reads `script/prompts.json` for the prompt list.

## Triggers

- `/atai` — show the prompt list, let presenter pick
- `/atai <N>` — jump to and execute prompt #N
- `/atai next` — execute the next prompt in sequence
- `/atai reload` — regenerate prompts.json from terminal.md

## Instructions

1. Read `script/prompts.json`. Each entry has: `num`, `step`, `title`,
   `prompt`, `type`, `run`, and optionally `optional: true`.

2. **No arguments:** show a compact numbered list (one line per prompt,
   truncated to ~65 chars). Use AskUserQuestion to let the presenter pick.

3. **With a number or `next`:**
   a. Print just the command as a markdown heading:
      ```
      ## <prompt truncated to 80 chars>
      ```
      Show only the command text — no `#N`, no `Step S`, no `▶`.
   b. Execute based on `type`:
      - `script` → run the `run` command via Bash
      - `script+assess` → run `run` via Bash, then apply LLM judgment
        (severity ratings, evidence quotes, findings)
      - `file` → Read and display the file referenced in `run`
      - `file+compare` → Read the file, compare to prior eval findings
      - `agent` → Read the agent template in `run`, execute the `prompt`
      - `freeform` → execute `prompt` directly as a Claude instruction
      - `talk` → nothing to execute, show key info and move on
   c. Print footer with step context and next pointer:
      ```
      Step S · #N/16 — NEXT → <next title>
      ```

4. **`next` skips `optional` prompts** unless explicitly requested by number.

5. **`--notes`**: read `script/terminal.md` and append Say: lines for the
   current step only.

## Reload

When invoked with `reload`: run `python3 script/gen-prompts.py` to
regenerate `script/prompts.json` from `script/terminal.md`. Report
the prompt count and list.

## Constraints

- Screen is audience-visible — no meta-commentary unless `--notes`.
- Track position across invocations so `next` works.
