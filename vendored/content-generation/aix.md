---
name: aix
description: "Cache and manage API keys from 1Password for the session."
argument-hint: env | run <command> | clear | status
---

# aix — 1Password API Key Cache

Wraps `aix` (which calls `op run`) to cache API keys in `/tmp/ai-keys.env`, avoiding repeated biometric prompts.

The user's shell has: `aix () { op run --env-file /Users/whit/.aider/ai-creds.env --no-masking -- $@ }`

## Subcommands

### `env` (default if no args)

Fetch keys and cache them.

```bash
for key in GEMINI_API_KEY OPENAI_API_KEY ANTHROPIC_API_KEY GITHUB_TOKEN; do
  val=$(aix printenv "$key" 2>/dev/null)
  [ -n "$val" ] && echo "export ${key}=${val}"
done > /tmp/ai-keys.env
chmod 600 /tmp/ai-keys.env
```

- If the user specifies additional key names, include those too.
- Report which keys were cached (key names only, no values).
- This is the only subcommand that touches 1Password.

### `run <command>`

Run a command with cached keys injected.

```bash
source /tmp/ai-keys.env && <command>
```

- If `/tmp/ai-keys.env` doesn't exist, run the `env` subcommand first.
- Pass the entire argument after `run` as the command.

### `clear`

```bash
rm -f /tmp/ai-keys.env
```

Confirm removal.

### `status`

Show which keys are cached and a masked preview (first 8 chars + `...`).

```bash
source /tmp/ai-keys.env 2>/dev/null
for key in GEMINI_API_KEY OPENAI_API_KEY ANTHROPIC_API_KEY GITHUB_TOKEN; do
  val="${!key}"
  [ -n "$val" ] && echo "$key=${val:0:8}..."
done
```

If the cache file doesn't exist, say so.

## Rules

- Keep responses terse — this is a utility.
- Never print full key values in output to the user.
- The cache file is `/tmp/ai-keys.env` — ephemeral, cleared on reboot.
- Bare `/aix` with no args is the same as `/aix env`.
