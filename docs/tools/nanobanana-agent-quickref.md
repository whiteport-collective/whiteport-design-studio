# NanoBanana — Agent Quick Reference

How to generate images via Anthropic's hosted NanoBanana connector.

**Prerequisite:** Your session must have the `mcp__nanobanana__*` tools available. If `mcp__nanobanana__show_output_stats` errors with "tool not found", the connector is not loaded in this session — open a new Claude Code session in a project that has it (this session type = Claude Code desktop app or VS Code extension with Anthropic connectors enabled).

---

## The one tool you need

`mcp__nanobanana__generate_image` — generates images from a prompt, optionally conditioned on input images.

### Minimal call (new image)

```
mcp__nanobanana__generate_image(
  prompt = "A hand-drawn chalkboard illustration of a designer and an AI agent collaborating. Deep blue chalkboard background, white and light blue chalk strokes, editorial style, no frame.",
  output_path = "c:/tmp/hero.png",
  aspect_ratio = "3:4",
  resolution = "4k",
  model_tier = "pro"
)
```

### Edit / conditioning on existing image

```
mcp__nanobanana__generate_image(
  prompt = "Keep the subject but change the background to a deep blue chalkboard with chalk lines.",
  input_image_path_1 = "c:/tmp/source.jpg",
  output_path = "c:/tmp/edited.png",
  mode = "edit"
)
```

### Multi-image composition (up to 3 inputs)

```
mcp__nanobanana__generate_image(
  prompt = "Combine these references into one cohesive chalkboard illustration.",
  input_image_path_1 = "c:/tmp/ref1.jpg",
  input_image_path_2 = "c:/tmp/ref2.jpg",
  input_image_path_3 = "c:/tmp/logo.png",
  output_path = "c:/tmp/composed.png"
)
```

---

## Parameters that matter

| Param | Values | When to use |
|---|---|---|
| `prompt` | text (max 8192 chars) | Always. Detailed: subject, composition, style, palette, any text to render |
| `output_path` | absolute path to `.png` | Always. File path with extension saves directly there |
| `aspect_ratio` | `1:1`, `3:4`, `4:3`, `16:9`, `9:16`, `21:9`, `4:5`, `5:4`, `2:3`, `3:2` | Pick by deliverable — see table below |
| `resolution` | `1k`, `2k`, `4k`, `high` | `4k` for hero/print, `2k` for web, `1k` for drafts |
| `model_tier` | `flash` (legacy 1024px), `nb2` (default, 4K fast), `pro` (max quality, slow), `auto` | `pro` for client-facing heroes, `nb2` for most, `flash` for rapid drafts |
| `n` | 1–4 | Generate multiple variations in one call |
| `negative_prompt` | text | Exclude specific elements ("no people", "no text") |
| `enable_grounding` | bool (default true) | Leave on — improves factual accuracy for real-world subjects |
| `thinking_level` | `low`, `high` | `high` for complex compositions (slower) |

---

## Format → aspect ratio cheat sheet

| Use case | Aspect ratio | Model tier |
|---|---|---|
| Article hero (Whiteport blog) | `3:4` | `pro` |
| LinkedIn wide / Facebook | `16:9` or `1.91:1` → use `16:9` | `nb2` |
| Instagram portrait | `4:5` | `nb2` |
| Instagram square | `1:1` | `nb2` |
| Instagram story / Reels / TikTok | `9:16` | `nb2` |
| Section illustration (blog body) | `16:9` | `nb2` |
| Thumbnail / icon | `1:1` | `flash` |

---

## Whiteport chalkboard base prompt

Always lead with this when generating Whiteport-brand imagery:

> A deep blue frosted glass chalkboard with chalk-style typography and editorial illustrations showing [TOPIC]. Modern, no frame. White and light blue chalk lines on dark blue background.

Logo (when needed): `whiteportLogo_2-7A-Dot-Transparent.png` from `G:/Shared drives/Whiteport Team/WP Communication/2026-03-20 Chalkboard Infographic Style/` — pass via `input_image_path_1`.

---

## Common pitfalls

- **"Tool not found"** → connector not loaded. Start a new session in Claude Code desktop/VS Code (not every environment has it).
- **Output too small** → set `resolution: "4k"` AND `model_tier: "nb2"` or `"pro"`. Legacy `flash` caps at 1024px.
- **Text in image comes out wrong** → spell it explicitly in the prompt with quotes: `render the text "Vi levererar värde" in chalk lettering`.
- **Colors drift** → add explicit palette: `deep blue #0A1F3D background, white (#FFFFFF) and light blue (#9EC4E8) chalk strokes only`.
- **Composition wrong** → use `input_image_path_1` with a reference image from the Whiteport chalkboard library.

---

## After generation

1. Inspect the file at `output_path`
2. If approved, move to the correct Google Drive folder:
   - Event-related → event folder
   - Non-event → `Whiteport Team > WP Communication > [YYYY-MM-DD] [slug]/`
3. Embed in article / post with relative path

---

## Related tools

- `mcp__nanobanana__upload_file` — upload large images (>20MB) to Files API for reuse
- `mcp__nanobanana__show_output_stats` — check recent generations and output dir
- `mcp__nanobanana__maintenance` — cleanup old files

---

**Full style system:** see [nanobanana.md](nanobanana.md) and [../../../whiteport-agent-space/tools/design/nanobanana/tool.md](../../../whiteport-agent-space/tools/design/nanobanana/tool.md).
