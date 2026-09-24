---
name: jeek-qi21-prompt
description: "Rewrite rough image ideas or vague edit requests into Qwen-Image-2.1-ready prompts. Use this skill when a user wants to generate an image from text (text-to-image) or to modify or edit an existing image with Qwen-Image-2.1 and needs the prompt expanded into the model's required long-form description plus strict JSON output. The skill auto-detects text-to-image versus image-editing, asks for any missing required information such as the input image for edits or the subject, style, and ratio for generation, and validates the final JSON fields rewritten_prompt, wh_ratio, and ratio_follow."
version: 1.0.0
agent_created: true
---

# Qwen-Image-2.1 Prompt Engineer

## What this skill does

Turn a user's short or vague image request into a **Qwen-Image-2.1-ready prompt**: a single, long, observer-style English description packaged in strict JSON, with the correct aspect-ratio fields. It covers both ways Qwen-Image-2.1 is driven:

- **Text-to-Image (t2i)** — generate a brand-new image from a written idea.
- **Image Editing (edit)** — change an existing image (object/attribute/background swap, text/UI edit, scene generation, outpainting, panorama, multi-image composite).

This skill is built directly on the **official Qwen-Image-2.1 prompt-rewriting system prompts** (the t2i 8-step method and the edit attribute-disentanglement method). On top of those, it adds three practical layers that the raw prompts assume but do not provide:

1. **A unified intent classifier** — one entry point decides t2i vs edit instead of shipping two disconnected prompts.
2. **A missing-information gate** — refuses to guess silently; asks the user to supply what is required (most importantly the input image for edits, and the subject/style/ratio for generation).
3. **A deterministic JSON validator** — `scripts/prompt_validator.py` catches the most common failure modes (wrong fields, `wh_ratio`/`ratio_follow` both/neither set, ratio/resolution text leaking into the description, mixed-language quoted strings).

## When to use

- The user says anything like "画一张…", "生成一张…", "帮我写个提示词", "Qwen 出图", or hands over a concept and wants a usable prompt.
- The user wants to **edit** an image: "把背景换成…", "给这张图改成…", "把 A 合成到 B", "扩图", "换脸", "三视图", etc.
- The user explicitly names **Qwen-Image-2.1** as the target model.
- The user supplies a weak prompt and wants it expanded to the model's expected long-form style.

Do **not** use this skill for model inference, ComfyUI node wiring, or non-Qwen image models. It produces prompt text + JSON only.

## The two modes at a glance

| | Text-to-Image (t2i) | Image Editing (edit) |
|---|---|---|
| Trigger signal | No input image; "生成/画/设计一张…" | An input image exists; "改/换/加/扩/合成…" + image |
| Hard requirement | A subject (what is in the frame) | **The input image(s)** — editing is impossible without them |
| Description language | Always English (in-image text keeps its own script) | Prose follows instruction language; in-image text follows language decision (B) — see `edit_guide.md` |
| Output JSON | `{"rewritten_prompt", "wh_ratio"}` | `{"rewritten_prompt", "wh_ratio", "ratio_follow"}` |
| Ratio logic | Always pick a `wh_ratio` (default `3:2` / `2:3` if silent) | One of `wh_ratio` / `ratio_follow` is set, never both, never neither |
| Core rule | Observe, don't instruct; ~20 sentences / 400–500 words | Edit exactly the named attribute; hold everything else at input fidelity |

## Workflow

### Step 0 — Classify the task

Apply this decision rule, in order:

1. **Edit mode** if **any** of these hold: the user attached ≥1 image, or used edit verbs ("改/换/修/加/删除/扩/合成/替换/重绘/把…变成/P 到/风格迁移/换脸"), or referenced "这张图/原图/input".
2. **t2i mode** otherwise (pure generation from text).

If the signal is ambiguous (e.g. "优化一下这个提示词" with no image and no verb), **ask the user which they mean** before proceeding — never assume.

### Step 1 — Gather missing information (the gate)

Before rewriting, check the required fields for the detected mode. If anything required is missing, **stop and ask** — do not invent it.

- t2i required/recommended fields → `references/missing_info.md#t2i`
- edit required/recommended fields → `references/missing_info.md#edit`

The edit mode has one **non-negotiable gate**: if no input image is present, ask for it immediately and do nothing else. Without the image there is nothing to anchor on, and the official edit method forbids fabricating image content.

How to ask is environment-dependent; see **Asking the user** below.

### Step 2 — Rewrite

Load the matching reference and follow it as the procedure:

- t2i → `references/t2i_guide.md` (8-step method, condensed into an actionable checklist)
- edit → `references/edit_guide.md` (language decisions A/B, attribute disentanglement, image-reference tags, full output-size logic)

Follow the field rules exactly. The rewritten description is the value of `rewritten_prompt`; never embed ratio/resolution tokens inside it.

### Step 3 — Validate

Run the bundled validator against the produced JSON:

```bash
# From inside the skill directory
python scripts/prompt_validator.py --mode t2i  --json '{"rewritten_prompt":"...","wh_ratio":"3:2"}'
python scripts/prompt_validator.py --mode edit  --json '{"rewritten_prompt":"...","wh_ratio":"","ratio_follow":"<image1>"}'
# or pipe JSON via stdin:
echo '<json>' | python scripts/prompt_validator.py --mode edit
```

Treat any `FAIL` line as a hard stop — fix the prompt and re-validate. `WARN` lines are advisory (e.g. t2i description contains non-English prose); resolve them unless the user explicitly overrode the rule.

### Step 4 — Output

Return **only** the JSON object, nothing before or after (matching the official format so it can be fed straight to the model):

- t2i: `{"rewritten_prompt": "<description>", "wh_ratio": "<W:H>"}` — single line, no markdown fence.
- edit: `{"rewritten_prompt": "<instruction>", "wh_ratio": "<W:H or ''>", "ratio_follow": "<'<imageN>' or ''>"}` — single line, no markdown fence.

If the surrounding conversation needs explanation, put it *outside* the JSON (above/below), but the deliverable block must be a bare, parseable JSON object.

## Output schema reference

| Field | t2i | edit | Meaning |
|---|---|---|---|
| `rewritten_prompt` | required | required | The long-form description / editing instruction. Single paragraph, no line breaks. In-image text in `"double quotes"`. |
| `wh_ratio` | required (never empty) | set XOR `ratio_follow` | Target aspect ratio `"W:H"` (e.g. `3:2`, `16:9`, `2:3`). Empty `""` when following an input image. |
| `ratio_follow` | — (absent) | set XOR `wh_ratio` | Which input image's resolution to follow: `"<image1>"`, `"<image2>"`, … Empty `""` when a `wh_ratio` is given. |

Mutual-exclusivity (edit only): exactly one of `wh_ratio` / `ratio_follow` must be non-empty. The validator enforces this.

## Asking the user (portability)

This skill is **agent-agnostic**: primarily adapted for and tested on WorkBuddy, but works with any agent that can load skill or instruction files. WorkBuddy is used below only as the concrete reference implementation for structured questions.

- **Primary reference (WorkBuddy):** present the missing fields as structured choices with the `AskUserQuestion` tool — one question per missing field, options as discrete picks (e.g. style = realistic / illustration / 3D-render / watercolour; ratio = horizontal / vertical / square / let-me-decide). Use `multiSelect: false` unless the field genuinely accepts several values.
- **Other agents:** ask the same questions in plain numbered text and wait for the reply before rewriting.

Keep questions minimal and high-signal — only ask for what is truly required or strongly improves the result; never ask the user to re-specify what they already gave.

## Bundled resources

| Path | Use |
|---|---|
| `references/t2i_guide.md` | t2i 8-step method, condensed + default-ratio and English-only notes |
| `references/edit_guide.md` | edit language decisions, attribute disentanglement, image-reference tags, full size logic |
| `references/missing_info.md` | per-mode required/recommended field checklists and example questions |
| `scripts/prompt_validator.py` | deterministic JSON validator (mode-aware) |

## Notes on fidelity and optimization

- The procedural rules in the reference files are faithful to the official Qwen-Image-2.1 system prompts; deviations are flagged as **Optimization** callouts so the intent is auditable.
- The biggest practical win over the raw prompts is the **missing-information gate** (Step 1): the official prompts assume a complete brief is already in hand, whereas real users often omit the subject, the style, or — critically for edits — the input image. This skill makes that gap explicit and recoverable instead of silently guessed.
