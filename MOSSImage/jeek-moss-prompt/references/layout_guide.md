# Layout Guide (Layout mode)

Condensed, action-oriented guidance for writing a MOSS-Image **Layout** draft, then compiling it. Produces a structured JSON with absolute-pixel bounding boxes; the compiler (`scripts/prompt_validator.py --mode layout`) converts them into the compact center-origin form MOSS-Image consumes.

## Output contract

Write a **draft** JSON with absolute-pixel boxes. The compiler handles the model-facing compact form. Do **not** hand-write center-origin coordinates.

- Draft: `{width, height, bbox_coord_space, bbox_format, summary, items[]}`
- Compiled (output of the validator): one physical line of JSON with `bbox_coord_space: "abs_centralized"`, `bbox_format: "yxyx"`, and integer center-origin boxes.

## Default canvas

- If the user gives explicit dimensions, honor them (must be positive multiples of 16).
- If only an aspect ratio is given, choose compatible pixel dimensions.
- If neither is given, default to **1024×1024**, unless the requested medium suggests another shape (e.g. a banner → wider).
- Never silently change explicit but incompatible dimensions — surface the conflict and ask.

## Coordinate system

- `bbox_coord_space`: exactly `"abs"`.
- `bbox_format`: exactly `"xyxy"`.
- A box is `[x_min, y_min, x_max, y_max]` in **actual pixels**, measured from the **canvas top-left**.
- Keep `x` within `0..width`, `y` within `0..height`. `x_min < x_max`, `y_min < y_max`.
- No normalized coordinates; do not manually center, reorder, or quantize the boxes.

## Fields

- `width`, `height`: positive integer multiples of 16, equal to the eventual image dimensions. They describe the draft canvas and are **omitted** from the compiled prompt. Do not rescale boxes merely by changing these fields.
- `summary`:
  - `caption` (required, non-empty): global image description.
  - `meta` (optional array): medium/genre tags, e.g. `["product campaign","studio photography"]`.
  - `canvas` (optional): `"single"`, `"multi_panel"`, or `"collage"`.
  - `palette` (optional): summary-level color tags.
- `items`: a **nonempty flat array**. Each item:
  - `label`: `"object"`, `"character"`, or `"text"`.
  - `caption` (required, non-empty): visible appearance; for text, typography and surface treatment.
  - `bbox` (required): four numbers `[x_min, y_min, x_max, y_max]`.
  - `text` (required **only** for a `text` item): the exact visible characters, with literal intended line breaks written as JSON `\n`. Use separate text items when placement must be independent. Mixed font styles alone do not require splitting.
  - `tags` / `palette` (optional string arrays) on items; `palette` on summary also supported.

Do **not** add `children`, `parent`, `id`, scene-schema `elements`, or presentation notes. The compiler rejects unrecognized fields rather than silently discarding creative intent. Positions are global canvas coordinates, including text on an object. Several items may share or overlap a box when the intended image does.

## Example

A 1536×1024 landscape campaign image, with a ceramic cup and exact Chinese copy:

```json
{
  "width": 1536,
  "height": 1024,
  "bbox_coord_space": "abs",
  "bbox_format": "xyxy",
  "summary": {
    "meta": ["product campaign", "studio photography"],
    "canvas": "single",
    "caption": "A warm studio campaign for a handmade ceramic cup, with an ivory backdrop, soft side lighting and restrained dark-green typography. Keep the ceramic texture tactile and the composition calm."
  },
  "items": [
    {
      "label": "object",
      "caption": "An ivory ceramic cup with a rounded handle, fine speckled glaze and a soft contact shadow, photographed at a three-quarter angle.",
      "bbox": [176, 224, 800, 864]
    },
    {
      "label": "text",
      "caption": "Large dark-green Chinese title in crisp, moderately heavy lettering, with generous spacing and no backing panel.",
      "text": "把日常，过成诗。",
      "bbox": [928, 272, 1408, 448]
    },
    {
      "label": "text",
      "caption": "Smaller dark-green Chinese supporting copy, comfortably legible on two lines.",
      "text": "一杯温暖\n一刻从容",
      "bbox": [928, 512, 1376, 656]
    }
  ]
}
```

## The compile transform (absolute → center-origin)

For each item's `bbox = [x1, y1, x2, y2]` on a `width×height` canvas, the compiler produces:

```
yc1 = floor(round(x1, 9)) - H / 2   # not used directly; see order below
```

The actual compiled box is **`[y1c, x1c, y2c, x2c]`** (format `yxyx`), where:

- `y1c = floor(round(y1, 9)) - H // 2`
- `x1c = floor(round(x1, 9)) - W // 2`
- `y2c = ceil (round(y2, 9)) - H // 2`
- `x2c = ceil (round(x2, 9)) - W // 2`

Fractional draft edges are enclosed (floor the left/top, ceil the right/bottom) **before** subtracting the center, so the model never has to compute these values. The result keeps `x_min_c < x_max_c` and `y_min_c < y_max_c`; a box too small at export precision is rejected.

Compiled output for the cup above: `[-288, -592, 352, 32]` (its original top/bottom minus `H/2`, then left/right minus `W/2`, in `yxyx` order).

## Composition checks

- Read every visible string against the requested wording. Check that line breaks, text length and glyph scale can fit the box at the declared resolution. A short Chinese title needs a different footprint from a paragraph of Latin text. Enlarge or recompose an unreadable layout rather than silently deleting copy or stretching glyphs.
- For a knowledge graphic, develop actual explanations and explanatory imagery; do not substitute empty modules. For a poster, keep its intended visual identity and information hierarchy rather than forcing infographic organization.
- When revising an existing draft, reread it, preserve unrequested content, and change only the specific affected captions or boxes. Keep a single coordinate convention throughout. Recompile after every geometry or canvas edit.
