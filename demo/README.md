# GTD w/ a coding agent

- [Demo Prep](./scripts/predemo.md)
  - set up all precaching and loading
- [Scripts](./scripts)
  - [Terminal Claude Code](./scripts/terminal.md)

## Terminal Demo

`atai` skill provides a way to navigate the demo steps
  - `atai next` load display and execute the next prompt
  - `atai load` will reload the demo steps in the json cache

Saves you cutting and pasting from another doc.

For search results and other situations, `cntl-o` will expand the
return allowing it to be seen and discussed.

Most actions take about 20s - so hit the prompt and start providing narrative context.


## Cowork

Have not had adequate time to assure it works or try demoing with it.  Might be worth some more investigation, at least to see if we can get the agents orchestrated MCP to work with it. The mcp has accidentally worked a few time in claude code.

- `cowork-review` is the agent pipeline trigger


## Notable caveats

We have no way to address a document in this system, so whatever is
loaded is what the skills operate on. Loading another document cleans
out the old one.
