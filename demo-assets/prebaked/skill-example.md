# Skill Example: `say`

A Claude Code skill is a markdown file placed in `.claude/skills/` that
teaches the agent a new capability. Skills compound -- each skill the
agent learns makes it more effective, and skills can reference each
other.

Below is an annotated example of a simple skill.

---

## File: `.claude/skills/say.md`

```markdown
# Skill: say

## Description
<!-- What this skill does, in one sentence. The agent uses this to
     decide when to activate the skill. -->
Speak a message aloud using the system text-to-speech engine.

## When to use
<!-- Trigger conditions. Be specific so the skill activates only
     when appropriate. -->
- The user asks you to "say" something out loud
- The user asks for audio output or voice feedback
- Another skill requests spoken confirmation of a result

## Instructions
<!-- Step-by-step procedure. The agent follows these literally. -->
1. Determine the message text to speak.
2. Use the Bash tool to invoke the platform's TTS command:
   - macOS: `say "<message>"`
   - Linux: `espeak "<message>"` (or `spd-say`)
3. Confirm to the user that the message was spoken.

## Examples
<!-- Concrete examples help the agent pattern-match. -->

User: "Say hello world"
Action: `say "hello world"`

User: "Read this error message aloud: connection refused"
Action: `say "connection refused"`

## Constraints
<!-- Guardrails. What the skill must NOT do. -->
- Never speak sensitive information (passwords, tokens, secrets)
- Keep messages under 500 characters to avoid long audio playback
- If TTS is unavailable, fall back to printing the message with a
  note that audio is not supported
```

---

## Key Anatomy

| Section | Purpose |
|---|---|
| **Description** | One-line summary; used for skill discovery |
| **When to use** | Trigger conditions; keeps the skill from firing on unrelated requests |
| **Instructions** | The actual procedure; should be unambiguous |
| **Examples** | Concrete input/output pairs; helps the model generalize |
| **Constraints** | Safety rails; what the skill must never do |

## How Skills Compound

Once `say` exists, other skills can reference it:

```markdown
# Skill: deploy-notify

## Instructions
1. Run the deployment pipeline.
2. If deployment succeeds, use the `say` skill to announce
   "Deployment complete."
3. If deployment fails, use the `say` skill to announce
   "Deployment failed, check logs."
```

This is the compounding effect: each new skill can build on previous
ones without duplicating logic. The agent's capabilities grow
combinatorially rather than linearly.
