# Finished

Wrap up the current session by finalizing the AI work transcript.

**Trigger:** When the user types `/finished` or asks to wrap up/finish the session.

## Workflow

1. **Locate the transcript.** Find the current session's transcript file in `notes/ai-notes/`. It follows the naming convention `{YYYYMMDD}-{model}-topic.md`. If multiple exist for today, use the most recently modified one. If none exists, create one following the convention.

2. **Write a summary.** Add a `## Summary` section at the very top of the transcript (after the `#` title line) with a concise 3-5 bullet point summary of what was accomplished in the session. Each bullet should be a single sentence capturing a key outcome, decision, or deliverable.

3. **Mark as complete.** Add a horizontal rule and a closing line at the bottom of the transcript:
   ```
   ---
   *Session completed: {YYYY-MM-DD HH:MM}*
   ```

4. **Confirm and exit.** Tell the user the transcript has been finalized and where it lives, then exit the conversation.
