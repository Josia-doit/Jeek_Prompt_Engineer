# Caption Guide (caption mode)

Condensed, action-oriented guidance for writing a MOSS-Image **caption**: one cohesive image description in JSON `{"caption": "..."}`.

A caption is prose. It describes the finished image as if reporting what is visible. It does **not** carry coordinates or layout fields — those belong to Layout mode.

## Output contract

- Return a single JSON object `{"caption": "<description>"}`. The `caption` value is cohesive prose; it may contain paragraphs.
- No `xywh`, no `bbox`, no layout fields. Do not add coordinates just to look structured.
- Visible wording that must appear in the image is quoted exactly inside the prose: `"把日常，过成诗。"`.

## Language

- Default to **English** for the descriptive prose, unless the user explicitly asked for another output language.
- Visible wording rendered **inside** the image keeps its own script (Chinese, Japanese, Cyrillic, Arabic, …) with its punctuation, capitalization and requested line breaks preserved verbatim. Do not translate on-screen text.
- A quoted sentence in the user's instruction is **not automatically** text to render: distinguish *visible wording* from *reference material* and *constraints*. Only quote what should actually appear in the picture.

## Develop the image

Describe the visible choices in enough detail to make the requested image concrete:

- **Subject & action** — who/what is in the frame and what they are doing.
- **Appearance** — relevant color, material, surface treatment, clothing, build.
- **Setting** — environment, background, context.
- **Camera / framing** — shot type, angle, distance, depth of field.
- **Medium** — photograph, illustration, 3D render, watercolour, flat vector, isometric, editorial, etc.
- **Lighting** — source, direction, quality, shadows and highlights.
- **Materials & palette** — tactile surfaces; modifier + hue, almost never bare color (`deep navy`, `muted olive`, `warm terracotta`).
- **Mood** — atmosphere and emotional register.

Add detail where it makes the requested image more specific. Avoid redundant quality tags, unrequested style changes, arbitrary word budgets, and invisible process notes ("make it seamless", "no watermark") — those are obeyed silently, never echoed into the prose.

## Keep the brief honest

- Preserve the user's subjects, counts, relationships, medium, style, exclusions and intended visible wording.
- Resolve ordinary creative gaps yourself; **ask only** when a missing decision would materially change the requested image (see `missing_info.md#caption`).
- Do **not** invent factual event logistics or specifications as if the user supplied them.
- Keep an explicit minimalist brief minimalist; develop a rich brief without turning it into a generic title/hero/footer template.
- For designed images, compose the information and imagery together — establish reading order, relative prominence, coherent groups, and readable text at the chosen pixels. Write the intended copy, not placeholders such as "headline here".

## Spatial relations in words

When the layout matters but you do **not** need precise boxes, express position in prose: "a ceramic cup sits front-right on an ivory pedestal, with a tall plant behind it to the left". Reserve true bounding boxes for Layout mode.

## Throughout (hard style rules)

- One cohesive voice; present tense, declarative.
- Enumerate, never summarize: name each item; small counts as words (three, five).
- Physical coherence: shadows fall away from light, reflections match what is in front of the surface, scale consistent between neighbours.
- Do not import unrelated names, watermarks, or copy from a reference.

## Optimization callouts (added on top of the base spec)

- **Pre-flight subject check:** if the user gave *no* subject, ask before drafting (see `missing_info.md#caption`). The caption assumes a subject exists.
- **Visible-text disambiguation:** when the instruction mixes quoted reference text and true on-screen copy, only quote the latter in the caption.
