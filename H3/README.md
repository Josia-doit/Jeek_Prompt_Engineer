# H3 —— MiniMax H3 视频提示词工程技能

本目录是 `Jeek_Prompt_Engineer` 仓库的一个**分类目录**，可单独复制其网址、让 Agent 只安装本模型的视频提示词技能，而不必拉取整个仓库。

## 包含的技能

| 技能文件夹 | 适用模型 | 功能 |
| --- | --- | --- |
| `jeek-h3-prompt/` | MiniMax H3（文本 / 图像 / 视频 / 音频多模态视频生成） | 提示词编写、五模式（T2VA / I2VA / FL2VA / L2VA / Ref2VA）、缺失信息追问、输出结构校验 |

## 安装（通用型，Agent 自动安装）

把本目录（或下方技能文件夹）的网址发给你的 Agent，**由 Agent 自动拉取并安装，无需手动下载或复制文件**：

- 本分类网址：`https://github.com/Josia-doit/Jeek_Prompt_Engineer/tree/main/H3`
- 单技能网址：`https://github.com/Josia-doit/Jeek_Prompt_Engineer/tree/main/H3/jeek-h3-prompt`

Agent 安装后，直接说「帮我把这个想法写成 H3 视频提示词」或「用 H3 做个图生视频，首帧是这张图」即可触发；技能自动判定输入模态（T2VA / I2VA / FL2VA / L2VA / Ref2VA），缺信息时主动追问。

## 技能结构

```
jeek-h3-prompt/
├── SKILL.md                     # 入口：五模式判定、输出字段、工作流
├── references/
│   ├── base_guide.md            # 基础四模式 T2VA/I2VA/FL2VA/L2VA 编写指南
│   ├── ref_guide.md             # 全参考 Ref2VA 六段式编写指南（参考标签体系）
│   └── missing_info.md          # 缺失信息追问闸门与追问模板
└── scripts/
    └── prompt_validator.py      # 原创输出结构校验器（base / ref / auto）
```

## 校验脚本（独立运行，不依赖任何 Agent）

```bash
# 基础模式（T2VA/I2VA/FL2VA/L2VA）
python jeek-h3-prompt/scripts/prompt_validator.py --mode base --file 你的提示词.txt
# 全参考模式（Ref2VA）
python jeek-h3-prompt/scripts/prompt_validator.py --mode ref --text "subject_definitions: ..."
# 自动判定模式
python jeek-h3-prompt/scripts/prompt_validator.py --mode auto --file 你的提示词.txt
```

## 说明

- 技能为**通用型**：以 WorkBuddy 为主要参考实现，同时兼容其他支持技能 / 指令加载的 Agent。
- 技能名 `jeek-h3-prompt` 为 hyphen-case 全小写（`^[a-z0-9-]+$`）。
- 规则来源：MiniMax H3 视频生成的提示词格式规范（五输入模式、三段 / 六段字段、参考标签 `<Subject N>`/`<Picture N>`/`<Video N>`/`<Audio N>`、说话人 `(Sx)`、对话 `<d>[Language] ...</d>`、保留关系标记）。
- 内容语言与详略可按需调整（如正文用中文、主体描述从简），只要字段名、段顺序、标签一致性与时间轴格式不变，模型仍可正确解析。
