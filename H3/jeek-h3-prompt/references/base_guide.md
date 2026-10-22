# 基础模式提示词编写指南（T2VA / I2VA / FL2VA / L2VA）

本指南覆盖不含全参考标签的四种基础模式。全参考模式（Ref2VA）见 `ref_guide.md`。

## 1. 任务概述

- **T2VA**：无参考图，从文本直接构建完整视听时间线。
- **I2VA**：T2VA 主体 + 首帧指令 + 从首帧向前发展的视觉路径。
- **FL2VA**：T2VA 主体 + 首尾帧指令 + 从首帧到尾帧的连续路径。
- **L2VA**：T2VA 主体 + 尾帧指令 + 从合理前置状态收敛到尾帧的路径。

## 2. 最终提示词结构

### 2.1 第一部分是对齐指令行

**T2VA** 无对齐指令，直接以三个核心字段开头。

**I2VA** 始终使用：

```text
For the target video, at 0.00 seconds into the target video, <Picture 1> (from [Shot 1]) is fully referenced.
```

**FL2VA** 始终使用（N 为实际尾帧所在镜头序号，S.SS 为精确到两位小数的有效时长）：

```text
How the reference pictures align with the target video — Picture 1 (from Shot 1) aligns with the 0.00-second mark of the target video; Picture 2 (from Shot N) aligns with the S.SS-second mark of the target video.
```

**L2VA** 始终使用：

```text
How the reference pictures align with the target video — <Picture 1> (from [Shot N]) aligns with the S.SS-second mark of the target video.
```

对齐指令行必须是最终提示词的第一行，其后空一行再接核心字段。

### 2.2 第二部分含三个核心字段

```text
integrated_multimodal_description: [Shot 1] ...

overall_soundscape: ...

non_diegetic_music: ...
```

- **integrated_multimodal_description**：沿时间线描述视觉、动作、镜头、说话人、对话、歌唱与画面内（diegetic）声音。
- **overall_soundscape**：汇总整段视频的环境声、物理动作声、非语言人声。
- **non_diegetic_music**：描述只有观众能听到、角色听不到的背景音乐。

## 3. 如何把关键帧融入多模态描述

### 3.1 I2VA：从图像出发向前发展
`<Picture 1>` 即 0.00 秒的首帧，属于 `[Shot 1]`。先确立图中的风格、主体、构图与场景锚点，再描述下一步动作；角色身份、服装、颜色、关键物体、空间关系保持一致。

推荐结构：**首帧锚点 → 动作起势 → 连续发展 → 结果或反应**。

### 3.2 FL2VA：描述首帧到尾帧之间的路径
Picture 1 是开头，Picture 2 是结尾。聚焦主体如何移动、姿态如何变化、物体如何被操作、构图如何演化、场景或光线如何过渡。通常偏好单镜头以便模型从首帧连续插值到尾帧；仅在用户明确要求时才用多镜头。尾帧必须在视频结尾的 `[Shot N]` 抵达。

推荐结构：**首帧状态 → 可观测的中间变化 → 差异逐渐收窄 → 尾帧状态**。

### 3.3 L2VA：推断开头并落在尾帧
`<Picture 1>` 是视频尾帧，属于最后的 `[Shot N]`，并不天然属于 Shot 1。从用户意图与尾帧推断合理的前置状态，再描述角色、物体、镜头、场景如何逐渐逼近参考图。

推荐结构：**合理前置状态 → 明确的动作与过渡路径 → 末镜头逐渐收敛 → 尾帧落地**。

## 4. 三个共享核心段写法

### 4.1 沿时间线展开多模态描述
`integrated_multimodal_description` 是重写主体，每个细节都应对应可见或可听的内容：视觉风格、初始构图、主体外观与位置、场景与关键道具、动作与反应、镜头切换、口语、以及同步的画面内声音。

在 `[Shot 1]` 开头给出整体风格与初始构图。常见风格：`Cinematic`、`live-action`、`2D-animated`、`3D CG`、`claymation`、`watercolor`、`vintage film`。关键帧任务从参考图推导风格，T2VA 从用户文本选择。

```text
[Shot 1] Live-action, cinematic, a medium-wide shot frames...
```

### 4.2 镜头与剪辑
首镜头不加时间戳；后续镜头用递增的镜头序号，并以落在视频时长内的递增切镜时间开头：

```text
[Shot 2] At 00:03.500, the camera cuts to...
```

普通切镜用 `the camera cuts to`、`the shot cuts to`、`the shot transitions to`、`the shot changes to`、`the shot switches to`；用户明确要求时也可用 cross-dissolve / fade / wipe。切镜应引入主体、空间、状态、视角或时间上的新信息；若只需改变距离或轻微角度，优先用镜头运动。

### 4.3 镜头运动：运动类型 + 幅度 + 速度
完整镜头运动表达含三维：**运动类型**定义相机如何动，**幅度**定义构图变化范围，**速度**定义变化节奏。仅在有意义时加幅度与速度；中幅度、正常速度通常省略。

| 维度 | 可用表达 | 说明 |
| --- | --- | --- |
| 运动类型 | `Zoom In / Zoom Out` | 机身不动，焦距变化 |
| 运动类型 | `Push In / Pull Out` | 相机前 / 后移动 |
| 运动类型 | `Pan Left / Pan Right` | 机身不动，镜头水平转动 |
| 运动类型 | `Truck Left / Truck Right` | 相机水平平移 |
| 运动类型 | `Tilt Up / Tilt Down` | 机身不动，镜头垂直转动 |
| 运动类型 | `Pedestal Up / Pedestal Down` | 整机升降 |
| 运动类型 | `Arc Shot` | 绕主体弧线运动 |
| 运动类型 | `Tracking Shot` | 跟随运动主体 |
| 运动类型 | `Static Shot` | 机位与镜头静止 |
| 运动类型 | `Shake Slightly / Shake Strongly` | 轻微 / 强烈抖动 |
| 运动类型 | `POV` | 主体主观视角 |
| 运动类型 | `Roll Clockwise / Roll Counterclockwise` | 绕光轴顺时针 / 逆时针滚转 |
| 幅度 | `with small amplitude` | 小范围变化 |
| 幅度 | `with large amplitude` | 大范围变化 |
| 速度 | `at slow speed` | 慢速 |
| 速度 | `at fast speed` | 快速 |

镜头运动写成镜头内的自然英文动作，不要堆在句尾当标签：

```text
The camera pushes in with small amplitude at slow speed toward the folded letter in her hands.
The camera pans right with large amplitude at fast speed, revealing the open doorway.
The camera holds a static shot as the runner exits the frame.
```

### 4.4 说话人、对话与歌唱
会说话、唱歌或发出画外人声的主体用稳定 ID，如 `(S1)`、`(S2)`；多人同说同唱用复合 ID 如 `(S1,S2)`。同一说话人跨镜头保持同一 ID；从不发声的角色不分配 ID。

说话人首次出现时，从视觉与音频语境给出足以稳定其身份的信息（角色类型、年龄、性别、是否在画面内、音高、音色、语速、口音），把身份信息、ID、动作、语气放在 `<d>` 之外；`<d>` 内只放语言标签与用户提供的实际口语内容，逐字保留原词与标点，不翻译不改写：

```text
The young woman with a quiet, breathy voice (S1) says: <d>[English] I get off at the next station.</d>
The two children (S1,S2) shout together, <d>[English] Wait for us!</d>
```

画外音用 `says in an off-screen voiceover`，并在每段画外音 `<d>` 后立即说明对应画面角色嘴唇保持闭合：

```text
The man (S1) says in an off-screen voiceover: <d>[English] I still remember that road.</d> while his lips remain completely closed.
```

同一句对话或歌词跨切镜时，在两端连接点用 `<scenetrans>` 并显式说明声音跨切连续；语音被视频结尾截断时用 `<cutoff>`。连续性可用 `continues seamlessly across the cut`、`continues uninterrupted into the next shot`、`carries over from the previous shot`、`remains audible across the transition`。

### 4.5 画面文字
任何实际可见的横幅、标牌、标签、字幕、霓虹文字，用英文双引号包裹，逐字保留原文与标点，不翻译：

```text
A red neon sign reading "营业中" glows above the doorway.
```

### 4.6 overall_soundscape
用 1–4 句英文、一个连续段落，汇总整段视频的环境声、物理动作声、非语言人声（风、雨、车流、脚步、布料摩擦、撞击、呼吸、笑声、喘息等）。对话、歌唱、画面内音乐已属于多模态描述，不在此重复。仅当用户明确要求整段完全静音时用 `N/A`。

```text
overall_soundscape: Steady rain taps against the café windows while low room ambience continues underneath. The entrance bell rings once, followed by wet footsteps and the soft scrape of a chair.
```

### 4.7 non_diegetic_music
用 1–3 句英文描述只有观众能听到、角色听不到的背景音乐；聚焦配器、速度、节奏、动态变化，不用抽象情绪词，不解释配乐情感功能。角色能听到的歌唱、乐器、广播、电视、手机音乐属于画面内事件，应写进多模态描述。无此类音乐时用 `N/A`。

```text
non_diegetic_music: Sparse piano notes at a slow tempo, joined by sustained low strings that gradually increase in volume before fading out.
```

## 5. 案例

### 案例 1：T2VA
无参考图，直接从文本构建时间线，可补充与用户意图一致的场景、角色、动作、声音细节。

```text
integrated_multimodal_description: [Shot 1] Live-action, cinematic, a medium-wide shot frames a baker opening the shutters of a small street bakery before sunrise. The camera pushes in with small amplitude at slow speed as the middle-aged baker with a calm, slightly raspy voice (S1) places a fresh loaf on the wooden counter and says: <d>[English] First batch of the morning.</d> [Shot 2] At 00:05.000, the camera cuts to a close-up of steam rising from the sliced bread while the baker's final words carry over from the previous shot.

overall_soundscape: Wooden shutters scrape open over a quiet street as trays clink softly inside the bakery. The doorbell rings once, followed by light footsteps and the crisp sound of bread being sliced.

non_diegetic_music: A soft acoustic-guitar pattern at a moderate tempo, joined by sparse upright-bass notes and a gentle fade at the end.
```

### 案例 2：I2VA
先写首帧指令，再以 Picture 1 的主体、构图、场景作为 Shot 1 起点，描述场景如何继续发展。

```text
For the target video, at 0.00 seconds into the target video, <Picture 1> (from [Shot 1]) is fully referenced.

integrated_multimodal_description: [Shot 1] Live-action, cinematic, the young woman shown in <Picture 1> remains beside the rain-covered train window, preserving her appearance, clothing, seat position, and the carriage layout. The camera trucks right with small amplitude at slow speed as she lifts her gaze from the folded letter toward the passing city lights. Her reflection moves across the glass while the quiet, breathy young woman (S1) says: <d>[English] I get off at the next station.</d> She folds the letter along its existing crease.

overall_soundscape: The train wheels produce a steady metallic rhythm beneath a low ventilation hum. Rain ticks against the window while paper rustles softly in her hands.

non_diegetic_music: Sustained cello notes at a slow tempo with widely spaced piano tones, gradually decreasing in volume.
```

### 案例 3：FL2VA
两张图分别锚定开头与结尾，主体不重复两张静态图的描述，而是给出连接它们的运动路径。以下为 8 秒单镜头示例。

```text
How the reference pictures align with the target video — Picture 1 (from Shot 1) aligns with the 0.00-second mark of the target video; Picture 2 (from Shot 1) aligns with the 8.00-second mark of the target video.

integrated_multimodal_description: [Shot 1] Live-action, cinematic, a rain-soaked cyclist begins in the position and framing established by Picture 1, holding a closed black umbrella beside a silver bicycle. The camera pulls out with small amplitude at slow speed as she releases the bicycle handle, raises the umbrella above her shoulder, and presses the runner upward until the canopy opens. Water rolls from the expanding fabric while she steps beneath it, rotates the handle into the final angle, and settles into the pose, spacing, and composition established by Picture 2 at the end of the shot.

overall_soundscape: Rain falls steadily on the pavement, followed by the metallic click of the umbrella runner and the soft snap of the canopy opening. Water drips from the bicycle frame as distant traffic passes.

non_diegetic_music: N/A
```

### 案例 4：L2VA
图像只锚定最后时刻。先建立兼容的前置状态，再让动作、物体状态、构图在末镜头逐渐落到 Picture 1。以下为 6 秒单镜头示例。

```text
How the reference pictures align with the target video — <Picture 1> (from [Shot 1]) aligns with the 6.00-second mark of the target video.

integrated_multimodal_description: [Shot 1] Live-action, cinematic, a close shot begins with an intact drinking glass near the edge of a dark wooden table, while the same hand and sleeve visible in <Picture 1> approach from the right. The camera pushes in with small amplitude at slow speed as the fingertips strike the rim. The glass tips, falls, and hits the floor with a sharp impact; cracks spread through it as fragments slide outward. Toward the end, the moving pieces lose momentum and settle into the exact broken arrangement, hand position, camera angle, lighting, and final composition established by <Picture 1>.

overall_soundscape: Fingertips tap the glass before it scrapes across the tabletop, falls, and breaks with a sharp crash. Small fragments scatter and gradually stop sliding across the floor.

non_diegetic_music: A low electronic pulse at a slow tempo, ending immediately after the glass breaks.
```
