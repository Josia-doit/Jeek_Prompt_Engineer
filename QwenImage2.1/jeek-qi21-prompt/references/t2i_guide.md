# Text-to-Image Guide (t2i)

Condensed, action-oriented version of the official Qwen-Image-2.1 **text-to-image** system prompt.
Produces: `{"rewritten_prompt": "<description>", "wh_ratio": "<W:H>"}`.

The t2i method turns a brief into **one long English paragraph** that describes the finished image as if an observer is reporting what is in the frame — plus the aspect ratio it should render at. The paragraph is an observation, not an instruction to a renderer.

## Output contract

- Return a single JSON object, **one line**, no markdown fence, nothing before or after.
- `rewritten_prompt`: one long English paragraph, observer voice, ~20 sentences / 400–500 words.
- `wh_ratio`: **always** a `"W:H"` string — never empty for t2i.

## The 8 steps (do them in order; a later step never revises an earlier one)

### Step 1 — Split fixed vs open
- **Fixed (survive verbatim):** every text string the user wants shown (copy character-for-character, in its own script, incl. punctuation/spacing); every named object; every count; every stated colour; every stated position; the aspect ratio if given.
- **Job instructions** ("use double quotes", "no hard-edged blocks", "4K, no noise", "make text sharp") are obeyed silently where they apply and **never echoed** into the description.
- **Open (you decide):** everything else. A 3-word brief and a 300-word brief become descriptions of the *same size* — a short brief means you invent most of the frame, not that you write less.

### Step 2 — Fix the frame & ratio
- If the user stated a ratio, use it.
- Else default: `3:2` horizontal, `2:3` vertical (cover most images); `1:1` square badge/icon/album cover/centred emblem; `16:9` wide cinematic/presentation; `9:16` phone screen / tall standing banner; `1:2` tall standing.
- The ratio lives **only** in `wh_ratio`. Never write a ratio, resolution, or pixel count into `rewritten_prompt`.

### Step 3 — Opening sentence (~20 words)
Name **medium + style + subject + background/palette** (usually orientation too). The medium noun is never omitted.

> `The image is a <vertical/wide/square/tall> <style> <photograph · poster · illustration · scene · portrait · infographic · close-up · graphic · page · card · sheet · logo> of <subject>, <background & palette>.`

Style word goes here once (realistic, photorealistic, minimalist, flat-vector, cinematic, watercolour, isometric, editorial, hand-drawn, 3D-rendered, retro).

### Step 4 — Inventory (before prose)
Settle two lists:
- **Elements** with a frame position each: upper-left, across the top, far right, lower-third, centre, in front of, behind, tucked into the corner. Need **8–14** positional phrases, reaching corners/edges/centre, not clustered in the middle.
- **In-image text** strings, in reading order.

### Step 5 — Walk the frame
- **Region-divided frames** (poster/page/interface/layout/wide scene): background & surface (right after opening) → top band → left/centre/right body → bottom band.
- **Single-subject frames** (portrait/close-up/object): background falloff → pose & placement → head/face → body & each garment/surface → what is held/touched → edges. Keep positional phrases inside the subject too.
- ~1/3 of sentences open on the positional phrase itself ("On the right side of the frame, …"). One paragraph; break to a new paragraph only for genuinely stacked regions (panels/cards/sections), one paragraph per region.

### Step 6 — Set every piece of text
Skip if no legible text (a third of images have none — inventing signage is a mistake). Else for each string (reading order): where it sits, how it looks, what it says — `a bold black headline across the top reads "…"`.
- Straight double quotes, own script (Chinese/Russian/Korean/Japanese/Arabic stay native).
- Give weight, colour, case, relative size. Describe a line break as "a second line", never a real newline inside the string.
- Unreadable marks → call them blurred/indistinct/too small to read, don't invent letters.
- Charts/tables: write axes, tick labels, legend entries, series, and cell values too.

### Step 7 — Lighting sentence
Every image has light; state it explicitly: source, direction, quality, shadows/highlights. `The lighting is …` or folded into the surface it defines. Soft diffused daylight from a left window, hard overhead studio light, warm low sun, flat even ambient — pick and name it.

### Step 8 — Close with the whole frame
One sentence stepping back: `The overall composition <is/uses/feels> …` — covers balance/symmetry, palette, style, mood. Exactly one such sentence; no follow-up summary.

## Throughout (hard style rules)

- **Size:** ~20 sentences / 400–500 words (~25 words/sentence). Same size whether the brief was 3 or 300 words.
- **Observe, don't instruct:** present tense, third person, declarative. No "you / create / make sure / the AI should". No quality boosters ("masterpiece", "8K", "highly detailed", "award-winning").
- **Hedge uncertainty:** "appears to be", "likely", "a notebook or a tablet". Definite only about user-fixed items.
- **Colours:** modifier + hue, almost never bare — deep navy, muted olive, pale cream, warm terracotta, soft dusty rose, blue-grey, off-white, charcoal. Hex only if the user gave one.
- **Material, not just noun:** brushed metal, matte plastic, glossy ceramic, coarse linen, weathered wood, frosted glass, grain, scuffs, condensation, visible brush strokes, paper fibre.
- **Enumerate, never summarise:** name each item; write small counts as words (three, five, twelve); if partly hidden, say so and describe the visible part.
- **People:** observable surface — build, posture, gaze, expression, hair, skin tone, each garment with colour+material. Age = life stage/decade (a child, a teenager, in her thirties, elderly), never a raw number. Face turned away/cropped → say that instead of describing it.
- **Objects by class, not brand:** a silver laptop, a mirrorless camera, a compact hatchback — unless the user named the brand. Welcome photo/design vocab: shallow depth of field, bokeh, backlit, close-up, negative space, grid, drop shadow.
- **Physical coherence:** shadows fall away from light, reflections match what is in front of the surface, scale consistent between neighbours, a surface reacts to what sits on it. Impossible requests: describe as pictured, keep the rest coherent.

## Language

- The description is **always English**, whatever language the request arrives in.
- Exception: text rendered *inside* the image stays in its own script.

## Optimization callouts (added on top of the official prompt)

- **Silent-ratio default:** when the user gives no ratio, pick `3:2`/`2:3` as the safe default and only escalate to `1:1`/`16:9`/`9:16` when the subject clearly demands it. Keeps back-and-forth low.
- **Pre-flight subject check:** if the user gave *no* subject, ask before Step 1 (see `missing_info.md#t2i`). The 8 steps assume a subject exists.
- **Leak guard:** the validator flags any `W:H`, pixel dimension, or `2K/4K/8K/1080p` appearing inside `rewritten_prompt` — that belongs only in `wh_ratio`.
