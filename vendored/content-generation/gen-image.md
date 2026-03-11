---
name: gen-image
description: "Generate images via Gemini or Codex (DALL-E). Provide a text prompt and optional flags for style, size, backend, and output path."
argument-hint: "<prompt>" [--backend gemini|codex] [--style <style>] [--size <WxH>] [--output <path>]
---

# Image Generation Skill

Generate images from text prompts using either Gemini (default) or Codex/DALL-E.

## Triggers

- `/gen-image`
- `/img`

## Usage

```
/gen-image "a warforged bard with a flying V guitar" --style cartoon --output images/warforged.png
/img "sunset over a cyberpunk city" --backend codex --size 1792x1024
```

## Flags

| Flag | Default | Description |
|------|---------|-------------|
| `--backend` | `gemini` | `gemini` or `codex` |
| `--style` | _(none)_ | Style hint appended to prompt: `cartoon`, `realistic`, `pixel-art`, `watercolor`, `oil-painting`, etc. |
| `--size` | `1024x1024` | Output dimensions (WxH) |
| `--output` | `images/gen-{timestamp}.png` | Output file path. Creates parent dirs if needed. |

## Workflow

1. **Parse** the user's prompt string and flags. If `--style` is provided, append it to the prompt (e.g., `"a cat" --style cartoon` becomes `"a cat, cartoon style"`).

2. **Ensure output directory exists** — run `mkdir -p` on the parent of the output path.

3. **Generate a default filename** if `--output` is not given: `images/gen-$(date +%s).png`.

4. **Dispatch to the chosen backend:**

### Gemini backend (default)

Use the Gemini API with `curl`. Requires `GEMINI_API_KEY` in environment.

```bash
curl -s "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp-image-generation:generateContent?key=${GEMINI_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "contents": [{"parts": [{"text": "PROMPT_WITH_STYLE"}]}],
    "generationConfig": {"responseModalities": ["TEXT","IMAGE"], "imageSizes": ["SIZE"]}
  }' \
  -o /tmp/gemini-response.json
```

Then extract the base64 image data from the response:

```bash
python3 -c "
import json, base64, sys
resp = json.load(open('/tmp/gemini-response.json'))
for part in resp['candidates'][0]['content']['parts']:
    if 'inlineData' in part:
        data = base64.b64decode(part['inlineData']['data'])
        open(sys.argv[1], 'wb').write(data)
        print(f'Saved to {sys.argv[1]}')
        break
else:
    print('No image in response', file=sys.stderr)
    print(json.dumps(resp, indent=2)[:500], file=sys.stderr)
    sys.exit(1)
" OUTPUT_PATH
```

If the API returns an error, print it and suggest the user check `GEMINI_API_KEY`.

### Codex backend

Dispatch to the Codex skill. Give Codex a self-contained prompt:

```bash
codex exec --full-auto "Generate an image using DALL-E with this prompt: 'PROMPT_WITH_STYLE'. Save the result as a PNG to OUTPUT_PATH. Size: SIZE. Use the OpenAI API (the OPENAI_API_KEY is in the environment). Download the image URL to the output path with curl."
```

Run this with `run_in_background: true` since it may take a while. Report back when complete.

5. **Verify** the output file exists and report its path to the user. If the file is in the working tree, mention the relative path for convenience.

## Error Handling

- If `GEMINI_API_KEY` is unset and backend is gemini, tell the user to `export GEMINI_API_KEY=...` or switch to `--backend codex`.
- If the API call fails, show the error body and suggest retrying or switching backends.
- If the output file wasn't created, report the failure clearly.

## Notes

- Keep responses terse. Confirm what was generated and where it was saved.
- For Gemini, the `gemini-2.0-flash-exp-image-generation` model supports image generation. If it stops working, try `imagen-3.0-generate-002` via the Imagen endpoint instead.
- The `--size` flag maps directly to API parameters. Gemini accepts size hints; DALL-E accepts `1024x1024`, `1792x1024`, or `1024x1792`.
