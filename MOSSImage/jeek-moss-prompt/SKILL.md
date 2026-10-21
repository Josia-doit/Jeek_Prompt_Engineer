---
name: jeek-moss-prompt
description: "Expand an image-generation idea into a MOSS-Image-ready caption or pixel-precise Layout, then compile the draft into a paste-ready prompt. Use for MOSS-Image prompt enhancement, image composition and exact text placement; this skill does not generate images. The skill auto-detects caption versus Layout mode, asks for any missing required information (subject for captions; canvas size and the literal text for Layout items) before drafting, and validates plus compiles the final JSON."
version: 1.0.0
agent_created: true
---

# MOSS-Image Prompt Enhancer

## What this skill does

Turn the user's idea into a **MOSS-Image-ready prompt**: either a detailed image **caption** or a pixel-precise spatial **Layout**, packaged in JSON and compiled into the exact compact form MOSS-Image expects. Two deliverables, one skill:

- **Caption** — a single, cohesive description of the finished image (prose, optionally multi-paragraph). Maps directly to MOSS-Image's positive caption input.
- **Layout** — a structured draft with bounding boxes, used when exact text placement, a poster, several panels, or controlled object relationships would benefit from precise coordinates.

On top of the raw MOSS-Image prompt vocabulary, this skill adds three practical layers the bare spec assumes but does not provide:

1. **A unified intent classifier** — one entry point decides caption vs Layout instead of shipping two disconnected prompts.
2. **A missing-information gate** — refuses to guess silently; asks for the subject (caption) or the canvas size and literal text (Layout) before drafting.
3. **A deterministic validator + compiler** — `scripts/prompt_validator.py` checks the draft for the most common failures (bad fields, out-of-bounds boxes, non-multiple-of-16 dimensions, a text item missing its string) and compiles absolute-pixel coordinates into the center-origin form MOSS-Image requires.

The bundled Python tool needs no external service or third-party dependency; it only does coordinate arithmetic and serialization.

## When to use

- The user wants a **MOSS-Image** prompt: "帮我写个 MOSS 出图提示词", "用 MOSS-Image 生成…", or hands over a concept and wants it expanded.
- The image needs **exact text placement / a poster / panels / controlled object layout** → Layout.
- The user wants an ordinary scene, photo, or illustration described richly → caption.
- Do **not** use this skill for model inference, ComfyUI node wiring, or non-MOSS image models. It produces prompt text + JSON only.

## The two modes at a glance

| | Caption | Layout |
|---|---|---|
| Best for | Scenes, photos, illustrations, "just describe it well" | Posters, UI, multi-panel, precise text/copy placement, controlled object relations |
| Trigger signal | Ordinary description request; no bounding-box need | "精准排版 / 海报 / 多面板 / 把文字放这里", or the user supplies exact copy + positions |
| Output (raw draft) | `{"caption": "..."}` | `{width, height, bbox_coord_space, bbox_format, summary, items[]}` |
| Compiled output | plain text caption | one physical line of compact JSON (center-origin boxes) |
| Hard requirement | A subject (what is in the frame) | Canvas `width`/`height` (positive multiples of 16) + literal text for every `text` item |
| Core rule | Cohesive prose; spatial relations in words; visible wording quoted exactly | Boxes in absolute pixels `xyxy` from canvas top-left; compiler converts to center-origin |

## Workflow

### Step 0 — Classify the deliverable

Apply this decision rule, in order:

1. **Layout mode** if **any** of these hold: the user asked for precise placement / a poster / panels / controlled object relationships, supplied exact copy that must sit at specific positions, or named "Layout / 布局 / 排版".
2. **caption mode** otherwise (a plain, rich description).

If the signal is ambiguous, **ask the user which they want** before proceeding — never assume.

### Step 1 — Gather missing information (the gate)

Before drafting, check the required fields for the detected mode. If anything required is missing, **stop and ask** — do not invent it.

- caption required/recommended fields → `references/missing_info.md#caption`
- Layout required/recommended fields → `references/missing_info.md#layout`

How to ask is environment-dependent; see **Asking the user** below.

### Step 2 — Draft

Load the matching reference and follow it as the procedure:

- caption → `references/caption_guide.md` (cohesive prose, spatial relations in words, visible wording quoted exactly)
- Layout → `references/layout_guide.md` (bbox coordinate system, item schema, dimensions, the compile transform)

Follow the field rules exactly. For Layout, write the **draft** with absolute-pixel `xyxy` boxes from the canvas top-left; the compiler (Step 3) converts them — never hand-write center-origin coordinates.

### Step 3 — Validate & compile

Run the bundled validator/compiler against the produced draft:

```bash
# From inside the skill directory
python scripts/prompt_validator.py --mode caption --json '{"caption":"..."}'
python scripts/prompt_validator.py --mode layout  --json '<layout-draft.json>'
# or pipe JSON via stdin:
echo '<json>' | python scripts/prompt_validator.py --mode layout
```

- caption mode → stdout prints the plain caption text.
- Layout mode → stdout prints the compiled single-line JSON (`bbox_coord_space: "abs_centralized"`, `bbox_format: "yxyx"`, integer center-origin boxes).
- `WARN` lines (stderr) are advisory; resolve them unless the user explicitly overrode the rule.
- Any `FAIL` line (stderr) is a hard stop — fix the draft and re-run; do not hand-write centered JSON to bypass the check.

Use `--check-only` to print `RESULT: PASS/FAIL` without emitting the compiled output.

### Step 4 — Output

Return the compiled prompt so it can be pasted straight into MOSS-Image:

- caption: the plain caption text (one block, no markdown fence needed).
- Layout: the single-line compiled JSON (no reformatting). Also state the required `width×height` **outside** the prompt — the compiled JSON itself does not carry canvas dimensions.

Keep explanations in the conversation, but the deliverable block must be the bare, paste-ready caption or JSON.

## Output schema reference

### Caption (raw draft & final are identical)

| Field | Meaning |
|---|---|
| `caption` | Cohesive description. Spatial relations in words; visible wording in `"double quotes"` exactly as intended. May contain paragraphs; no coordinates. |

### Layout (raw draft → compiled)

| Field | Draft | Compiled | Meaning |
|---|---|---|---|
| `width` / `height` | required | omitted | Canvas size; positive integers, **multiples of 16**. Describes the draft canvas only. |
| `bbox_coord_space` | `"abs"` | `"abs_centralized"` | Draft = absolute pixels; compiled = center-origin. |
| `bbox_format` | `"xyxy"` | `"yxyx"` | Draft = `[x_min,y_min,x_max,y_max]`; compiled = `[y_min_c,x_min_c,y_max_c,x_max_c]`. |
| `summary` | required (`caption` + optional `meta`/`canvas`/`palette`) | kept | Global image description and optional tags. |
| `items` | required, nonempty flat array | kept, boxes converted | Each: `label` (object/character/text), `caption`, `bbox`, optional `text`/`tags`/`palette`. |
| `text` (on a text item) | required | kept | The exact visible characters; `\n` = intended line break. |

Box transform (absolute `xyxy` → compiled `yxyx`, all integers):
`[ floor(x1)-W/2, floor(y1)-H/2, ceil(x2)-W/2, ceil(y2)-H/2 ]` reordered to `[y1c, x1c, y2c, x2c]`.

## Asking the user (portability)

This skill is **agent-agnostic**: primarily adapted for and tested on WorkBuddy, but works with any agent that can load skill or instruction files. WorkBuddy is used below only as the concrete reference implementation for structured questions.

- **Primary reference (WorkBuddy):** present the missing fields as structured choices with the `AskUserQuestion` tool — one question per missing field, options as discrete picks (e.g. mode = caption / Layout; canvas = 1024×1024 / 1536×1024 / 1024×1536 / let-me-decide). Use `multiSelect: false` unless the field genuinely accepts several values.
- **Other agents:** ask the same questions in plain numbered text and wait for the reply before drafting.

Keep questions minimal and high-signal — only ask for what is truly required or strongly improves the result; never ask the user to re-specify what they already gave.

## Bundled resources

| Path | Use |
|---|---|
| `references/caption_guide.md` | caption writing: cohesive prose, spatial relations in words, visible wording quoted exactly |
| `references/layout_guide.md` | Layout bbox coordinate system, item schema, dimensions, the compile transform, full example |
| `references/missing_info.md` | per-mode required/recommended field checklists and example questions |
| `scripts/prompt_validator.py` | deterministic draft validator + compiler (mode-aware; caption/layout) |

## Notes on fidelity and optimization

- The field rules and the bbox coordinate transform follow the public MOSS-Image Layout vocabulary; deviations are flagged as **Optimization** callouts so the intent is auditable.
- The biggest practical win over the bare spec is the **missing-information gate** (Step 1): the spec assumes a complete brief is already in hand, whereas real users often omit the subject (caption) or the canvas size and literal copy (Layout). This skill makes that gap explicit and recoverable instead of silently guessed.
