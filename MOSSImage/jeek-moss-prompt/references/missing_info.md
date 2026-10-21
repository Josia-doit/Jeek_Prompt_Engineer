# Missing-Information Gate

The base MOSS-Image spec assumes a complete brief is already in hand. Real users omit things — most often the **subject** (caption) or the **canvas size and literal copy** (Layout). This skill refuses to guess silently: classify the mode (see `SKILL.md` Step 0), then check the lists below. Anything marked **required** and missing must be asked for before drafting. Recommended fields should be asked when missing *and* when they would materially improve the result; skip them only when the user clearly wants a quick pass.

Keep questions minimal and high-signal. Never ask the user to re-specify what they already gave.

---

## caption — required & recommended

### Required
- **Subject / core content** — what should appear in the frame. If the user gave nothing concrete ("帮我写个图" with no topic), this is a hard stop: ask what the image should depict.

### Recommended (ask when missing)
- **Style / medium** — realistic · illustration · 3D-render · watercolour · flat-vector · isometric · cinematic · minimalist · editorial. Picking one changes the whole description; ask if silent.
- **Visible wording** — any words/headlines/labels to render, and their language. Critical for posters/infographics/UI; safe to assume "none" for pure scenes.
- **Mood / setting** — atmosphere, time of day, environment. Improves coherence but a reasonable default can be inferred.
- **Output language** — default English prose unless the user asked otherwise; confirm only if ambiguous.

> Tip: for a one-line brief like "一只猫", ask only **subject detail + style** — two tight questions, not a questionnaire.

---

## Layout — required & recommended

### Required (hard gates)
- **Canvas dimensions** — `width` and `height`, positive integers that are multiples of 16. If the user gave none, **default to 1024×1024** (or a shape implied by the medium) and state it; ask only if they have a specific size or ratio.
- **Literal text for every `text` item** — a Layout with a `text` label but no `text` field is invalid. If the user described a poster/copy but did not give the exact wording, ask for it verbatim (including line breaks and language).

### Recommended (ask when missing)
- **Element relationships** — which objects/characters/text go where, and any overlap/occlusion the user wants. Important for posters and multi-panel compositions.
- **Canvas type** — `single` / `multi_panel` / `collage` (the `summary.canvas` field). Usually inferable; ask if the user mentioned panels or a collage.
- **Medium / genre tags** — optional `summary.meta` (e.g. "studio photography"); ask only if it would help the generation.
- **Exact box positions** — if the user named positions ("title top-right"), honor them; otherwise you may propose boxes and let the user adjust.

---

## How to ask the user

### 用结构化问询工具（以 WorkBuddy 的 `AskUserQuestion` 为例）
Present one question per missing field. Use discrete options; set `multiSelect: false` unless the field genuinely accepts several values. Example shape for a Layout request missing canvas size + copy:

```
Q1 header="画布"  question="Layout 画布尺寸用多少？（需为 16 的整数倍）"
    options: 1024×1024 / 1536×1024 / 1024×1536 / 你来定（默认1024×1024）
Q2 header="文案"  question="需要精确放置的可见文字是什么？（请逐字给出，含换行）"
    options: 我来提供 / 暂时不需要文字
```

For caption with no subject, a single blocking question suffices:

```
Q1 header="主体" question="这张图的主体是什么？（必填）"
    options: 我现在说 / 其实想要 Layout 排版
```

(The second option doubles as a safety re-classification back to Layout.)

### In other agents — plain numbered text
Ask the same questions as a short numbered list and wait for the reply. Example:

```
在起草之前，我需要确认几点：
1. 画面主体是什么？（必填）
2. 偏好哪种风格：写实 / 插画 / 3D / 水彩？
3. 是否需要画面上的可见文字？若有，请逐字给出。
```

### Rules for asking
- Ask **only what is missing**. Do not re-ask fixed items the user already stated.
- Prefer **multiple-choice** over open text where a small option set covers it; fall back to open text for the subject/intent/copy.
- For Layout, the **canvas size and literal text questions come first** (hard gates).
- After the user replies, re-run the gate; only proceed to draft once every **required** field is satisfied.
