# Missing-Information Gate

The official Qwen-Image-2.1 prompts assume a complete brief is already in hand. Real users omit things — most often the **subject** (t2i) or the **input image** (edit). This skill refuses to guess silently: classify the mode (see `SKILL.md` Step 0), then check the lists below. Anything marked **required** and missing must be asked for before rewriting. Recommended fields should be asked when missing *and* when they would materially improve the result; skip them only when the user clearly wants a quick pass.

Keep questions minimal and high-signal. Never ask the user to re-specify what they already gave.

---

## t2i — required & recommended

### Required
- **Subject / core content** — what should appear in the frame. If the user gave nothing concrete ("帮我写个图" with no topic), this is a hard stop: ask what the image should depict.

### Recommended (ask when missing)
- **Style / medium** — realistic · photorealistic · illustration · 3D-render · watercolour · flat-vector · isometric · cinematic · minimalist · editorial. Picking one changes the whole description; ask if silent.
- **Orientation / ratio** — horizontal · vertical · square · (let the model decide). If silent, the skill defaults to `3:2`/`2:3`; ask only if the user has a preference.
- **In-image text** — any words/headlines/labels to render, and their language. Critical for posters/infographics/UI; safe to assume "none" for pure scenes.
- **Mood / setting** — atmosphere, time of day, environment. Improves coherence but the 8-step method can infer a reasonable default.

> Tip: for a one-line brief like "一只猫", ask only **subject detail + style + ratio** — three tight questions, not a questionnaire.

---

## edit — required & recommended

### Required (hard gates)
- **Input image(s)** — **editing is impossible without them.** If no image is attached, STOP and ask for it immediately; do nothing else. This is the single most important gate.
- **Edit intent** — what exactly should change (object/attribute/background/text/style/viewpoint/canvas). If the user only said "优化一下" with no target, ask which attribute to change; never assume.

### Recommended (ask when missing)
- **Preservation scope** — what must stay fixed (person identity, background, product design, rendering medium). Especially important when the request is vague, to prevent leakage.
- **Output size / ratio** — only if the user cares; otherwise the skill follows the input image (`ratio_follow`).
- **Multi-image roles** (N ≥ 2) — which image is the canvas (composition survives) and which supplies material; what is taken from each.
- **In-image text language** — which language rendered text should be in (decision B). Usually inferable, but ask if ambiguous (e.g. mixed-language source).

---

## How to ask the user

### 用结构化问询工具（以 WorkBuddy 的 `AskUserQuestion` 为例）
Present one question per missing field. Use discrete options; set `multiSelect: false` unless the field genuinely accepts several values. Example shape for a t2i request missing style + ratio:

```
Q1 header="风格"  question="这张图想要哪种视觉风格？"
    options: 写实照片 / 插画 / 3D渲染 / 水彩
Q2 header="比例"  question="画面比例偏好？"
    options: 横版 3:2 / 竖版 2:3 / 方形 1:1 / 你来决定
```

For edit with no image attached, a single blocking question suffices:

```
Q1 header="原图" question="编辑需要原图。请上传要修改的图片（多张请一并上传并说明各自作用）。"
    options: 我现在上传 / 稍后提供 / 其实是想文生图
```

(The third option doubles as a safety re-classification back to t2i.)

### In other agents — plain numbered text
Ask the same questions as a short numbered list and wait for the reply. Example:

```
在重写之前，我需要确认几点：
1. 画面主体是什么？（必填）
2. 偏好哪种风格：写实 / 插画 / 3D / 水彩？
3. 比例：横版 / 竖版 / 方形 / 你来定？
```

### Rules for asking
- Ask **only what is missing**. Do not re-ask fixed items the user already stated.
- Prefer **multiple-choice** over open text where a small option set covers it; fall back to open text for the subject/intent.
- For edit, the **input-image question is non-negotiable and comes first**.
- After the user replies, re-run the gate; only proceed to rewrite once every **required** field is satisfied.
