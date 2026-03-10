# Presentation: The Agentic Quest

Slide deck for AllThings AI 2026. Content lives in markdown,
built into a single HTML file.

## Structure

```
presentation/
  content/          # one markdown file per slide, ordered NN-slug.md
  output/           # rendered deck (gitignored)
  build.py          # markdown -> HTML renderer
  template.html     # CSS/JS shell (Six Feet Up brand)
  deck.html         # legacy hand-built deck
  Makefile          # build tasks
```

## Slide markdown format

Each file has YAML frontmatter + body:

```markdown
---
type: content-slide          # title-slide | content-slide | dark-slide | divider-slide
image: ../images/photo.jpg   # optional
image_alt: description       # optional
image_layout: split           # split | inline | divider (optional)
section_number: II            # divider slides only
footer: "05"                  # slide number shown bottom-right
---

# Slide Title

> "Blockquote text"

- Bullet one
- Bullet two

:::grid
:::card Card Title
Card body text.
:::
:::grid
```

## Commands

```sh
make build    # render content/ -> output/deck.html
make open     # build + open in browser
make list     # show slide order
make clean    # remove output
make watch    # auto-rebuild on changes (needs fswatch)
```

## Adding / reordering slides

- Files sort lexicographically: `01-title.md`, `02-topic.md`, ...
- To insert a slide between 03 and 04, name it `03b-new.md`
  or renumber from 04 onward
- To remove a slide, delete the file and rebuild
