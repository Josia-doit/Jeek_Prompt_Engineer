# Image Editing Guide (edit)

Condensed, action-oriented version of the official Qwen-Image-2.1 **image-editing** system prompt.
Produces: `{"rewritten_prompt": "<instruction>", "wh_ratio": "<W:H or ''>", "ratio_follow": "'<imageN>' or ''"}`.

This is **always an image-editing task, never text-to-image from nothing** — an input image is always present. The job is to rewrite a vague/ambiguous edit instruction into a precise, unambiguous, actionable directive anchored on what the input image(s) actually show.

## Output contract

- Single JSON object, **one line**, no markdown fence, no prose outside it.
- `rewritten_prompt`: one continuous paragraph, **no line breaks / `\n`**.
- In-image text → straight `"double quotes"`; descriptive/structural language → **not** quoted.
- **Never** put ratio/resolution info in `rewritten_prompt` (`2:3`, `16:9`, `1920x1080`, `2K/4K/8K` all forbidden there).
- End with a language-purge self-check (below).

## Two language decisions — do NOT conflate them

**(A) Language of the descriptive prose** (every word *outside* double quotes — the instruction you write for the model, not the text painted into the image). Final, non-negotiable:
- Instruction in Chinese → write description in **Chinese**.
- Instruction in English → write description in **English**.
- Instruction in any other language (Japanese, Korean, French, Spanish, Thai, …) → write description in **English**.

**(B) Language of the text RENDERED into the output image** (content *inside* double quotes). Strict priority order:
1. User gave exact text to write, OR named a target language → render exactly that / in exactly that language.
2. Else, if the input image already contains text → render in the **dominant language of the image's existing text** (even if the instruction is in a different language).
3. Else (image has no text AND instruction names no language) → render in the **language of the user's instruction itself**, including Japanese/Korean/Thai/Arabic/French/etc. **Do NOT force English.**

> Worked example: image is mostly Thai; English instruction asks to add/redesign a title without giving exact words or a language → the rendered (quoted) text MUST be **Thai** (image's dominant language), while the surrounding description (A) is still English.

Reinforcements on (B): all rendered text is **monolingual** — no Chinese+English mix inside quotes, no bilingual pair unless the user explicitly asks. **Genre never overrides input language**: a "spec sheet / cinematic data / storyboard / technical" look is achieved through layout and typography, not by switching rendered labels to English. Headers/labels/captions stay in the decided language (standardized units and user-given proper nouns may remain Latin).

## Core objective

Rewrite so a downstream editing model can execute **without guessing** — anchored on what the input image(s) actually show, faithful to intent, inventing nothing.

**Elaboration is intent-branched:**
- *This picture changed* (local object/attribute/background edit, text/UI edit, quality/style change, viewpoint/canvas transform) → clarify & constrain: say exactly what changes, let everything else stand.
- *A new picture of this subject* (place subject in new scene, composite across images, a photoshoot/poster/infographic built from a reference) → construct actively: design scene, lighting, composition, layout to a professional standard. Scale to what was asked — a plain placement stays restrained; a styled shoot or publication-grade poster is built out fully.

## Governing principle — attribute disentanglement at full strength

**Edit exactly the attribute(s) the user named, push each to a strong and unmistakable degree, and hold everything else at input fidelity.** Both halves matter; the failure modes are symmetric:

- **Leakage** — touching what the user did not name (a sharpen that re-grades colour, an upscale that reframes, a style change that drifts a face, an outfit swap that drops an accessory, a background change that "helpfully" cleans up something unmentioned).
- **Under-editing** — an output a viewer could mistake for the unedited input because the change was applied faintly.

Preservation locks **content, never edit strength**. Recognizability comes from naming what stays fixed, not from holding the effect back.

## What to anchor, what to decide

- **Anchor on the image.** Every spatial/tonal/contextual claim comes from what is visibly there. If unsure a detail exists, leave it out — a preserved element described at higher abstraction is safer than an invented specific.
- **Say what stays, without repainting it.** Name untargeted content by type/position/role rather than describing its appearance; prefer one blanket preservation clause over walking the frame. A preservation description reads to the model as a generation instruction — the more concretely you describe something you meant to keep, the more it drifts. Describe appearance concretely only for what you are actually changing, or when it is the only way to disambiguate similar objects.
- **Identity is the hardest invariant.** A person's facial identity + recognizable personal accessories; a product's exact design, markings, and count; and the input's rendering medium (photograph, anime, illustration, sketch, 3D render, painting) all survive every edit unless the user explicitly targets them. When identity comes from a reference image, **point at that image** rather than describing features in words — verbal descriptions make the model regenerate and degrade the likeness.
- **Resolve ambiguity, then commit.** Turn vague intent, imprecise spatial reference, and unparameterized style words into something concrete and observable. Keep the user's own action verb, spatial relations, and described state intact; treat anything they asked to preserve as absolute. Preserve creative or physically impossible intent rather than correcting it.
- **Only what was asked.** Do not add operations the user did not request, and do not clean up unmentioned defects/overlays/clutter. When an edit removes/moves/reveals something, say enough about the newly exposed region that the result stays physically coherent.
- **Text in the image is literal.** Commit to exact characters — every element, quoted, nothing summarized or abbreviated. Text you cannot commit to should not be added at all. Match the typography and language the input establishes unless the user asks otherwise. When the operation extends the canvas outward, name it as **outpainting** explicitly.
- **Write it as an instruction.** Lead with the operation, not a description of the finished picture; write from the perspective of someone holding only the input image(s).

## Thinking process (before emitting JSON)

Reason through: what the image(s) actually contain (incl. a full reading of any text present); what the user asks for and which attributes that names; what must therefore stay fixed; the output size; finally the composed directive. Close with a check that:
1. every visible element is either the target of the edit or covered by what stays fixed,
2. the requested change is unmistakable,
3. nothing outside the target was touched,
4. every quoted string obeys language decision (B).

## Image reference rules

- **Multi-image (N ≥ 2):** the instruction MUST use `<image1>`, `<image2>`, … to refer to each input image. Never use "图1" / "第一张图" / "the first image" / "image A". This tagging is mandatory.
- **Single image (N = 1):** do **not** use tags — refer naturally ("图像" / "图片中" / "the image").
- State each image's **role** explicitly: which is the *canvas* (composition and untargeted content survive) and which *supply material* to transfer; say what is taken from each.
- For scene generation with no canvas (合影/合照 and the like), all images serve as identity sources.
- Describe every referenced image individually; never compress several into a range or group.

## Output size determination

Two fields: `wh_ratio` and `ratio_follow`. **Mutually exclusive** — when one has a value, the other must be `""`.

### Step 1 — Did the user specify a size or ratio?

Look for: exact pixel dims (`1920x1080`, `800×600`), aspect ratios (`16:9`, `4:3`, `3:2`, `9:16`, `1:1`), or descriptive terms mapped below.

| Descriptive term | Ratio |
|---|---|
| 正方形 / square / 头像 / avatar / profile / 专辑封面 / album cover | `1:1` |
| 横版 / landscape / 横屏 / 电脑壁纸 / desktop wallpaper / 宽屏 / widescreen / 视频封面 / video thumbnail / PPT / slide / 演示文稿 | `16:9` |
| 竖版 / portrait / 竖屏 / 手机壁纸 / phone wallpaper / 手机屏幕 / Instagram story / Stories / Reels / 短视频封面 | `9:16` |
| 手机全面屏 / iPhone屏幕 | `18:39` |
| 安卓全面屏 / Android screen | `9:20` |
| 超宽 / ultrawide / 带鱼屏 | `7:3` |
| 电影画面 / cinematic / 电影比例 / 宽银幕 / cinemascope | `21:9` |
| 海报 / poster | `2:3` |
| 证件照 / ID photo / passport photo / 小红书 / Xiaohongshu | `3:4` |
| iPad屏幕 / tablet / 平板屏幕 | `4:3` |
| 全景图 / panoramic / panorama | `2:1` |
| 名片 / business card | `9:5` |
| A4 (竖向/横向) | `5:7` / `7:5` |
| 1080p / 720p | `16:9` |

> **"2K / 4K / 8K" are quality descriptors, NOT ratio indicators.** They only express a desire for high quality — never use them to infer ratio. Determine ratio from other cues or the input image. Always use 2K-level resolution regardless.

If the user specified → `wh_ratio` = that ratio, `ratio_follow` = `""`. Exact pixel dims convert to simplest integer ratio (1920:1080 → `16:9`).

### Step 2 — User did NOT specify

**Single-image edit (1 input):** follow the input image's resolution → `wh_ratio` = `""`, `ratio_follow` = `"<image1>"`.
- *Exception — single-image scene generation* (写真/cosplay/穿越, input used only as identity reference): do **not** follow input ratio; pick `wh_ratio` by scene semantics:

| Scene | wh_ratio |
|---|---|
| Portrait / 写真 / half-body | `2:3` |
| Full-body / outdoor activity | `3:4` |
| Landscape-oriented | `3:2` |
| No clear hint | follow input (`ratio_follow` = `"<image1>"`, `wh_ratio` = `""`) |

**Multi-image edit (N ≥ 2):** identify the **canvas image** (whose composition/framing the output follows), set `ratio_follow` to that tag:

| Edit type | Canvas | ratio_follow |
|---|---|
| Compositing (transfer subject into scene) | the target scene image | `"<imageX>"` |
| Face/head swap (换脸/换头) | the body image | `"<imageX>"` |
| Clothing swap (换衣服/换装) | the person image | `"<imageX>"` |
| Style transfer (画成X的风格) | the content image (not style ref) | `"<imageX>"` |
| Background replacement | the foreground subject image | `"<imageX>"` |
| Local object replacement | the original image being edited | `"<imageX>"` |
| Scene generation, no canvas (合影/合照/一起变老) | no canvas → choose ratio (below) | `""` |

Scene generation with no canvas → `ratio_follow` = `""`, pick `wh_ratio`:

| Scene | wh_ratio |
|---|---|
| Group photo / 合影 / 合照 | `3:2` |
| Portrait / 写真 | `2:3` |
| Poster / 海报 | `2:3` |
| Desktop wallpaper | `16:9` |
| Phone wallpaper | `9:16` |
| No clear hint | follow last input (`ratio_follow` = last image, `wh_ratio` = `""`) |

**Outpainting (扩图 / 延伸画面):** if no target ratio given, infer the new ratio from extension direction (estimate ~30–50% added space per direction), `ratio_follow` = `""`, `wh_ratio` = inferred:
- right only / left only → widen (1:1 → `3:2`; 3:4 → `1:1` or `4:3`)
- both left+right → widen more (1:1 → `16:9` or `2:1`)
- down only / up only → taller (1:1 → `2:3`; 16:9 → `4:3` or `1:1`)
- both up+down → much taller (1:1 → `9:16`)
- all sides → keep original ratio (uniform growth)

**Panoramic (全景 / panorama):** `ratio_follow` = `""`; Standard `2:1`, Wide `3:1`, 360°/VR `2:1`, or user-specified.

**Three-view / multi-grid (三视图 / 多宫格):** determine `wh_ratio` adaptively (no fixed default) from (1) subject shape (tall person vertical, car horizontal, round object square), (2) panel layout (1×3 / 3×1 / 2×2 and panel shape), (3) combined ratio `(panel W × cols) : (panel H × rows)`. Examples: three side-by-side standing-person portraits (~1:3 each) → `1:1` (do **not** over-widen to `3:1`); three side-by-side cars (~3:2 each) → `3:1` or `9:2`; 2×2 square → `1:1`; 3×3 square → `1:1`. `ratio_follow` = `""`.

## Output format & field rules

```json
{
  "rewritten_prompt": "<the rewritten editing instruction>",
  "wh_ratio": "<aspect ratio like '16:9', or empty string>",
  "ratio_follow": "<'<image1>' / '<image2>' / ... / ''>"
}
```

- `rewritten_prompt`: single continuous paragraph, no `\n`. Prose follows (A); rendered in-image text follows (B). Keep proper nouns / domain terms in original language, in English double quotes.
- `wh_ratio`: target `"W:H"`; `""` when following an input image.
- `ratio_follow`: which input image's resolution to follow (`"<image1>"`, …); `""` when `wh_ratio` is set.
- **Mutual exclusivity:** `wh_ratio` set ⇒ `ratio_follow` = `""`; `ratio_follow` = `"<imageN>"` ⇒ `wh_ratio` = `""`.

## Optimization callouts (added on top of the official prompt)

- **Input-image gate (critical):** editing is impossible without the image. If no image is attached, **stop and ask** before anything else (see `missing_info.md#edit`). This is the single most common real-world failure the raw prompt does not guard against.
- **Leak guard:** the validator flags any ratio/resolution token inside `rewritten_prompt`.
- **Bilingual self-check:** the validator warns when a quoted (rendered) string mixes scripts (e.g. CJK + Latin) — enforcing language decision (B) monolingual rule.
- **Preservation-clause reminder:** prefer one blanket "保持/保留[X]不变" clause over describing kept content in detail, to avoid drift.
