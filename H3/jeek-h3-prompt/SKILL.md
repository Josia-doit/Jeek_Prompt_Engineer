---
name: jeek-h3-prompt
description: "为 MiniMax H3 视频生成编写提示词，覆盖文生视频 T2VA、图生视频 I2VA/FL2VA/L2VA 与全参考 Ref2VA 五种模式；自动识别输入模态、组装多模态描述与音景、校验输出结构。通用型技能，可由任意支持加载本地技能的 Agent 使用，无需外部 API。"
---

# jeek-h3-prompt · MiniMax H3 视频提示词编写

## 适用模型
MiniMax H3 视频生成（文本 / 图像 / 视频 / 音频多模态输入，输出带画面与声音的视频）。

## 五种输入模式

| 模式 | 输入 | 含义 |
| --- | --- | --- |
| `T2VA` | 纯文本 | 从文字构建完整视听时间线 |
| `I2VA` | 首帧图 | 以首帧为起点向后发展 |
| `FL2VA` | 首帧 + 尾帧图 | 描述首帧到尾帧之间的连续变化 |
| `L2VA` | 尾帧图 | 推断合理开头并收敛到尾帧 |
| `Ref2VA` | 参考图 / 视频 / 音频（要求保特征） | 全参考模式，用标签体系精确控制参考内容的保留与迁移 |

## 工作流

1. **判定输入模态**：无参考资产 → `T2VA`；仅首帧图 → `I2VA`；首尾帧图 → `FL2VA`；仅尾帧图 → `L2VA`；带参考图/视频/音频且要求保留特定主体/风格/声音 → `Ref2VA`。
2. **基础模式**（T2VA / I2VA / FL2VA / L2VA）：读 `references/base_guide.md`，按「对齐指令行 + 三段核心字段」输出。
3. **全参考模式**（Ref2VA）：读 `references/ref_guide.md`，按「六段式」输出。
4. **缺必要信息**：按 `references/missing_info.md` 主动追问补全（模态、时长、参考资产及其角色、风格等）。
5. **输出后校验**：用 `scripts/prompt_validator.py` 检查字段完整性、标签一致性与时间轴格式。

## 输出规则（两种模式通用）

- 重写正文用英文；对话、歌词、画面可见文字保留原始语言（不翻译、不改写）。
- 每个镜头描述：构图、主体、环境、动作、镜头运动、声音，以及被参考内容出现的具体时刻。
- 避免：剧情摘要式空泛描述、未闭合的参考标签、与请求时长不符的时间轴。

## 基础模式最终结构（三段字段）

```text
integrated_multimodal_description: [Shot 1] ...

overall_soundscape: ...

non_diegetic_music: ...
```

- `I2VA` 在字段前加一行：`For the target video, at 0.00 seconds into the target video, <Picture 1> (from [Shot 1]) is fully referenced.`
- `FL2VA` / `L2VA` 在字段前加一行对齐说明（见 `references/base_guide.md` 第 2 节）。

## 全参考模式最终结构（六段字段，顺序固定）

```text
subject_definitions:
summary:
retention_analysis:
detailed_description:
overall_soundscape:
non_diegetic_music:
```

参考标签贯穿全篇保持一致：`<Subject N>`（可复用可视内容）、`<Picture N>`（参考图/关键帧锚点）、`<Video N>`（参考视频/结构来源）、`<Audio N>`（参考音频）。详见 `references/ref_guide.md`。

## 兼容性
纯本地文件技能，无外部 API 调用、无专有运行时依赖。可被任意能读取本地技能目录的 Agent 加载（WorkBuddy 直接发本分类网址即可安装，其他 Agent 复制 `jeek-h3-prompt/` 到其 skills 目录即可）。
