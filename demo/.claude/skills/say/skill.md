# Say Skill

Use the macOS `say` command to audibly notify the user when you need their input, hit a blocker, or complete a long-running task.

## Trigger

Use automatically when:
- You need user input to continue (e.g., a question via AskUserQuestion)
- A long-running task completes (builds, test suites, deployments)
- You hit an error or blocker that requires user attention
- A background task finishes and the user may have walked away

## Usage

```bash
# Notify the user you need input
say "Hey, I have a question for you"

# Task completed
say "Done. All tests passing."

# Error or blocker
say "Heads up, I hit an error and need your help"
```

## Rules
- Keep messages short and conversational (under 15 words)
- Don't use `say` for routine status updates — only when the user needs to act or a milestone is reached
- Always pair with the actual text output so the message is also visible in the terminal
- Use a neutral tone — no alarm or urgency unless something actually failed
