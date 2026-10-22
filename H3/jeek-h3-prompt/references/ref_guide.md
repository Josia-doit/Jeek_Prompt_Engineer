# 全参考模式重写输出格式指南（Ref2VA）

本指南说明全参考模式下重写输出的组织与写法。基础模式的镜头、镜头运动、说话人、对话、普通声音格式与此共用，见 `base_guide.md`；本指南聚焦全参考模式特有的参考标签、分析段与格式差异。

全部六段用英文书写；仅 `<d>` 内的对话/歌词与画面可见文字保留原始语言。

**描述粒度**：`detailed_description` 尽量详尽具体。每个镜头明确当前构图、主体外观与位置、环境与光线、动作与状态变化、镜头运动、当前声音，以及被参考内容实际出现或生效的时刻。不要降格为剧情摘要或参考关系清单。

## 1. 整体结构

完整重写输出由六段按以下顺序构成：

| 段 | 作用 |
| --- | --- |
| `subject_definitions` | 定义被参考内容与参考标签 |
| `summary` | 概括任务类型、目标视频与主要参考关系 |
| `retention_analysis` | 描述被参考内容如何被保留、迁移或复用 |
| `detailed_description` | 按播放顺序描述视觉、动作、镜头、声音与对话 |
| `overall_soundscape` | 汇总环境声与物理声音 |
| `non_diegetic_music` | 描述只有观众能听到的背景音乐 |

## 2. 参考标签与定义（subject_definitions）

全参考重写用四类标签标识被参考内容的来源与角色：

| 标签 | 含义 |
| --- | --- |
| `<Subject N>` | 从参考资产抽象、可在目标视频中复用或改造的可视内容 |
| `<Picture N>` | 作为具体目标帧或镜头规划锚点的参考图 |
| `<Video N>` | 提供剪辑源、续写起点或整视频时间结构的参考视频 |
| `<Audio N>` | 被复制或引用的音频信号 |

> 一旦给某内容分配参考标签，它在 `subject_definitions`、`summary`、`retention_analysis`、`detailed_description` 及音频段中含义保持一致。

`subject_definitions` 为每一条需独立追踪的被参考内容单独成行（如一个人、一个环境、一个源视频的结构、一条音轨），说明其标签含义、参考角色与需遵循的主要特征；当来源需显式点明时标注对应源资产。若 `<Picture N>` 或 `<Video N>` 仅用于标识另一条被参考内容的来源、后续不单独分析或使用，在该条定义内引用即可，不必单独成行。`retention_analysis` 记录每条被参考内容出现在哪里、是完全保留、部分保留、迁移还是复用。

### 2.1 `<Subject N>`
用于可复用的可视内容：人物、动物、物体；场景、背景、环境；服装、道具、界面、视觉效果；风格、动作、表情、姿态。它代表会实际用于目标视频的内容单元，而非源文件本身。一个主体可由多个参考资产定义，一个参考资产也可提供多个主体。

```text
<Subject 1> is the young woman in <Picture 1>, with long dark hair, a blue cardigan, and a thin silver necklace.
```

同一主体来自多个资产时，合并来源并说明各自提供什么：

```text
<Subject 1> is the woman whose appearance comes from <Picture 1> and whose walking motion comes from <Video 1>.
```

### 2.2 `<Picture N>`
当参考图本身作为某镜头的首帧、关键帧、尾帧、编辑关键帧或构图锚点时，用独立 `<Picture N>`：

```text
<Picture 2> is the first frame of [Shot 1], showing a woman seated beside a café window.
```

若图像仅用于定义角色、场景、服装或风格，不要建独立 picture 条目，而是在对应 `<Subject N>` 定义内引用图像来源。当图像作为分镜/镜头规划参考时，说明它映射到哪些镜头、提供哪些规划信息：

```text
<Picture 3> is a storyboard reference for [Shot 1] and [Shot 2], defining their viewpoint, subject placement, and shot order.
```

### 2.3 `<Video N>`
`<Video N>` 仅用于整视频关系：剪辑原始视频、从原始视频结尾续写、引用其镜头运动/剪辑/节奏/时间结构。

```text
<Video 1> is the source video for the target video edit.
```

若参考视频中某人物、物体、场景、动作或效果作为可视内容复用时，仍归属 `<Subject N>`；`<Video N>` 标识资产或结构来源，不替代主体标签。

### 2.4 `<Audio N>`
`<Audio N>` 代表独立音频资产或参考视频中启用的同步音轨。常见用途：复制全部或部分音频信号、引用背景音乐风格、引用说话人音色与语气、复用原音频中的对话/歌词/音效、引用节拍/节奏/音频连续性。

当 `<Audio N>` 明确对应目标说话人时，在定义中复用该说话人全局 ID：映射到已定义主体时写 `<Subject N> (Sx)`，否则用稳定声音描述后接 `(Sx)`。ID 来自目标视频全局说话人顺序，不在音频定义中独立分配或重编号（见第 5.4 节）。

```text
<Audio 1> is the voice-timbre reference for <Subject 1> (S1).
```

一个音频资产承担多角色时，用一句自然话说清各角色，不必建额外子段。

### 2.5 同一参考视频的视觉与音频轨
`<Video N>` 与 `<Audio N>` 各自独立编号，索引仅表示标签在自身类别内的顺序，不编码两类之间的配对。同一参考视频可对应 `<Video 1>` 与 `<Audio 2>`；不同索引不妨碍它们来自同一源资产。普通参考视频不会仅因文件含声音就产生 `<Audio N>`。`<Audio N>` 定义主要说明音频角色，不必点名其来自哪个 `<Video N>`；仅当需消除来源歧义时才说明共享来源。

```text
<Video 1> is the source video for the target video edit.
<Audio 2> is the synchronized audio track of <Video 1> and is reused in the target video.
```

## 3. summary

用一段简短英文概括目标视频及其参考关系，以方括号任务类型前缀开头：

```text
[reference generation] ...
[video editing + reference generation + audio reuse] ...
```

按每个参考资产在目标视频中的实际角色选任务类型：

| 任务类型 | 使用时机 |
| --- | --- |
| `keyframe completion` | 图像作为目标视频首帧、关键帧、尾帧、编辑关键帧或其他具体帧锚点 |
| `reference generation` | 图像/视频/音频资产为角色、场景、风格、动作、镜头运动、分镜等提供生成指导，但不作为具体帧、也不作为被剪辑/续写的源视频 |
| `video editing` | 直接修改已有源视频；编辑图像或在静态关键帧间生成不属于此类 |
| `video continuation` | 新内容从已有源视频续写、延伸、恢复或过渡 |
| `audio reuse` | 完整或部分复用同一音频信号 |
| `audio reference` | 不直接复制音频信号，仅引用其音乐风格、音色、对话或歌词内容、音效质感、节拍或连续性 |

满足多关系时用 ` + ` 组合且不重复类型。例如以图像作尾帧并从源视频续写，写作 `[video continuation + keyframe completion]`；编辑源视频并保留原音频，写作 `[video editing + audio reuse]`。仅因存在视频或音频不会自动产生对应任务类型；参考视频仅提供镜头运动/剪辑/节奏时通常归 `reference generation`，仅当该视频被直接剪辑或续写时才用 `video editing` / `video continuation`。剪辑源视频时若原音频仍可被听见，同时用 `audio reuse`；续写源视频但未直接复制音频信号、仅延续原轨可听特征时，用 `audio reference`。

`summary` 用已定义的四类标签描述主要主体、镜头流向与参考资产角色，不在此引入新标签。视频编辑任务在任务类型前缀后以 `The target video is an edited version of <Video 1>.` 开头。

## 4. retention_analysis

描述每条被参考内容如何在目标视频中被保留、迁移、复制或引用。每条参考标签一行，保留 `subject_definitions` 中建立的含义。

### 4.1 可视内容
`<Subject N>`、`<Picture N>`、`<Video N>` 使用以下关系标记（输出中的固定英文值）：

| 关系标记 | 含义 |
| --- | --- |
| `fully_preserved` | 被参考内容的定义角色被完全保留 |
| `partially_preserved` | 仍被使用，但部分定义特征被改变或仅部分保留 |
| `attribute_transfer` | 被参考特征迁移到另一个可识别的目标主体 |
| `weak_reference` | 仅保留风格、类别、构图或氛围上的宽泛相似 |

主体条目：

```text
<Subject 1> (appears in [Shot 1], [Shot 3]): fully_preserved - ...
```

图像条目：

```text
<Picture 2> ([Shot 1] first frame): fully_preserved - ...
```

视频结构条目：

```text
<Video 1> (cut and pacing structure): weak_reference - ...
```

### 4.2 音频
`<Audio N>` 使用以下关系标记：

| 关系标记 | 含义 |
| --- | --- |
| `fully_copy` | 完整源音频作为目标视频完整最终音轨 |
| `partially_copy` | 仅复制部分时间线或选中音层，或复制后增删替换其他声音 |
| `reference` | 不直接复制信号，仅引用音色、节奏、音乐风格、对话内容或音效质感 |
| `weak_reference` | 仅保留类别或氛围上的宽泛相似 |

```text
<Audio 1>: fully_copy - <Audio 1> is reused 1:1 as the target video's complete final audio track.
<Audio 2>: reference - the target speaker follows <Audio 2>'s voice timbre and measured delivery without copying the original signal.
```

每个关系标记只在 `subject_definitions` 中已为该标签定义的参考角色内选择；不要把目标视频中新增的动作、背景或剧情事件当作参考保真度的损失。

## 5. detailed_description

全参考重写主体，按目标视频播放顺序逐镜头描述视觉、动作、声音与对话，在适用处插入参考标签。

### 5.1 基础格式
遵循基础模式指南：正文英文、对话/歌词/可见文字保留原语言；`[Shot 1]` 无时间戳，后续镜头用 `[Shot N] At MM:SS.mmm, ...` 标记切镜时间；镜头运动写成当前镜头内的自然英文（含类型、幅度、速度）；发声源用稳定 `(S1)`、`(S2)`；对话歌词写 `<d>[Language] ...</d>`；对话跨切用 `<scenetrans>`、语音被结尾截断用 `<cutoff>`，并配相应连续性描述。

### 5.2 与基础模式的差异

| 维度 | 基础模式 | 全参考模式 |
| --- | --- | --- |
| 主字段 | `integrated_multimodal_description` | `detailed_description` |
| 风格开头 | 写在 `[Shot 1]` 之后 | 在 `[Shot 1]` 之前用一两句英文确立 |
| 参考信息 | 不使用全参考标签 | 在首次出现及角色适用处插入 `<Subject N>`/`<Picture N>`/`<Video N>`/`<Audio N>` |
| 音频关系 | 描述目标视频自身声音 | 在对应镜头或音频阶段引用 `<Audio N>` 并说明信号是复制还是引用 |

风格开头示例：

```text
The target video is in a cinematic, literary music-video style with soft lighting and a slightly desaturated color palette.
[Shot 1] The scene opens in a crowded urban street...
[Shot 2] At 00:09.000, the shot cuts to an extreme close-up...
```

生成任务 `detailed_description` 通常 350–500 英文词；对话密集内容优先容纳完整口语时间线，而非机械凑字数。视频编辑描述随源视频复杂度伸缩，不必遵循生成任务字数范围。单镜头不自动导致更短描述，应按信息负载把细节分布到多个镜头。

### 5.3 在镜头中使用参考标签
重要 `<Subject N>` 首次清晰出现时，描述其在画面中实际可见的参考特征、在帧中位置与当前动作；后续镜头沿用同一标签不再重定义。具体帧锚点用自然措辞：

```text
the shot begins from <Picture 1>
the shot's keyframe corresponds to <Picture 2>
the shot ends on <Picture 3>
```

编辑或续写原始视频时，在源状态/结构/续写关系适用处自然引用 `<Video N>`；在音频关系激活的镜头或语义阶段引用 `<Audio N>`。

### 5.4 说话人、音频源与对话
基础模式的说话人 ID 与 `<d>` 格式沿用。被参考主体实际发声时，同时保留视觉参考标签与说话人 ID：

```text
<Subject 2> (S1) turns toward the woman and says, <d>[English] Last summer, I went to my grandfather's house. He talked about you.</d>
```

`<Subject N>` 标识被参考主体，`(Sx)` 标识实际说话人；主体画外发声时保持同形并标 `off-screen`；说话人不对应已定义主体时，用稳定声音描述后接 `(Sx)`。

当语言内容仅是直接复用的 BGM 或完整音轨内的提示、没有具体人物/角色/旁白等独立发声源产生它时，用 `<Audio N>` 作可听源，不另造 `(Sx)`；若有具体人物/角色/旁白等独立发声源产生声音，为其分配并复用 `(Sx)`：

```text
When <Audio 1> reaches the phrase <d>[English] I'm lonely lonely lonely lonely lonely I'm lonely</d>, <Subject 1> performs the corresponding hand gesture without becoming a separate speaker source.
```

直接复用参考音频的对话/旁白/歌词，或输入明确要求重演时，在 `<d>` 内逐字保留源词与原始语言；听不清的片段写 `[unclear]` 不猜不改写；标点规范为基本书面标点（`,` `.` `?` `!`），去掉重复波浪号、emoji、项目符号及重复或装饰性标点，完整句/问句/叹句分别以 `.` `?` `!` 收尾。仅引用音色/节奏/情绪/语气时，不要把参考音频原对话带入目标视频。

`(Sx)` 按目标视频中实际发声事件顺序分配一次，在 `detailed_description` 每次实际发声处复用；`subject_definitions` 中绑定目标说话人的 `<Audio N>` 也复用同一 `(Sx)`，但绝不独立分配新 ID。不要在 `retention_analysis` 写 `(Sx)`。

## 6. overall_soundscape 与 non_diegetic_music

两段定义同基础模式指南。`overall_soundscape` 汇总整段环境声与物理声，对话/歌唱/绑定特定镜头的声音事件留在 `detailed_description`：

```text
overall_soundscape: Quiet indoor room tone and a low ventilation hum continue throughout the video.
```

`non_diegetic_music` 描述角色听不到、仅观众可听的背景音乐，出现时说明配器、速度与动态发展：

```text
non_diegetic_music: A restrained solo-piano score at a slow tempo, with sustained low cello underneath and no swell.
```

使用参考音频时，仅在匹配可听层的段中说明复制或引用关系：环境声与音效归 `overall_soundscape`，仅观众可听的配乐归 `non_diegetic_music`；同一音频同时提供两类内容时，在各段分别描述对应关系：

```text
overall_soundscape: The copied ambience layer from <Audio 1> continues throughout the target video.
non_diegetic_music: <Audio 2> is directly reused as the complete audience-only score.
```

完整对话与歌词只写在 `detailed_description` 的 `<d>` 内，不在此两段重复。

## 7. 完整示例

```text
subject_definitions:
<Subject 1> is the coffee-shop environment in <Picture 1>, featuring an exposed brick wall, an orange tufted sofa with patterned pillows, a neon sign, and a wooden coffee table.
<Subject 2> is the fluffy white Samoyed in <Picture 2>, <Picture 3>, and <Picture 4>, with thick white fur, pointed ears, a dark nose, and a curved tail.
<Subject 3> is the young blonde woman in <Video 1>, with long blonde hair and a light-pink button-down shirt with rolled-up sleeves.
<Subject 4> is the young man in <Video 2>, with short wavy brown hair and a dark-grey hoodie with drawstrings.
<Audio 1> is the voice-timbre reference for <Subject 3> (S1), containing a spoken English vocal layer.

summary:
[reference generation + audio reference] The target video shows <Subject 3> eating a cookie in <Subject 1>. <Subject 4> enters with <Subject 2>, which lunges toward the cookie. The three-shot exchange uses <Audio 1> as the voice-timbre reference for <Subject 3> and ends with a canned audience laugh.

retention_analysis:
<Subject 1> (appears in [Shot 1], [Shot 2], [Shot 3]): fully_preserved - the exposed brick wall, orange tufted sofa, patterned pillows, neon sign, and wooden coffee table are retained.
<Subject 2> (appears in [Shot 1], [Shot 2]): fully_preserved - the Samoyed's thick white fur, pointed ears, dark nose, and curved tail are retained.
<Subject 3> (appears in [Shot 1], [Shot 2], [Shot 3]): fully_preserved - the blonde woman's identity, long hair, and light-pink shirt are retained.
<Subject 4> (appears in [Shot 1], [Shot 2]): fully_preserved - the young man's short wavy brown hair and dark-grey hoodie are retained.
<Audio 1>: reference - its vocal timbre guides the dialogue delivery of <Subject 3> without copying the original signal.

detailed_description:
The target video uses a realistic multi-camera sitcom style with warm indoor lighting.
[Shot 1] A medium shot establishes <Subject 1>, the coffee shop with its exposed brick wall, orange tufted sofa, patterned pillows, neon sign, and wooden coffee table. <Subject 3> (S1), the young woman with long blonde hair and a light-pink button-down shirt with rolled-up sleeves, sits on the sofa holding a chocolate-chip cookie. From the left, <Subject 4>, the young man with short wavy brown hair and a dark-grey hoodie with drawstrings, enters holding the leash of <Subject 2>, the thick-furred white Samoyed with pointed ears, a dark nose, and a curved tail. The dog lunges toward the cookie and pulls the leash taut. <Subject 3> (S1) jerks her hand back and, using the clear youthful voice timbre referenced from <Audio 1>, exclaims with light annoyance, <d>[English] Hey! Watch your dog!</d> She closes her lips and guards the cookie while <Subject 4> pulls the dog back.
[Shot 2] At 00:03.000, the shot cuts to a close-up of <Subject 4> (S2), the young man in the dark-grey hoodie from Shot 1, sitting beside <Subject 3> on the sofa and holding <Subject 2> securely in his arms. <Subject 4> (S2) says in a casual young male voice with a playful tone and an easy conversational pace, <d>[English] He just likes cookies more than me.</d> He closes his mouth into an apologetic smile and strokes the dog's thick white fur.
[Shot 3] At 00:05.000, the shot cuts to a close-up of <Subject 3> (S1), the blonde woman in the light-pink shirt from Shot 1. Her annoyance softens as she looks toward the Samoyed. <Subject 3> (S1) replies in the same clear youthful voice referenced from <Audio 1> with an amused cadence, <d>[English] Well, he has good taste at least.</d> She smiles and raises the cookie in a small toast-like gesture. A classic canned audience laugh begins immediately after the line and continues through the final frame.

overall_soundscape:
Soft indoor coffee-shop room tone continues throughout the scene.

non_diegetic_music:
N/A
```

## 8. 风格提示（非强制）
上述为 H3 官方推荐格式。实际使用可按需调整正文语言与详略：例如正文用中文、主体描述从简、仅保留必要参考标签——只要**字段名、段顺序、标签一致性、时间轴格式**不变，模型仍能正确解析。是否采用更简风格属个人工作流偏好，不影响本技能的结构校验。
