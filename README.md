# Jeek_Prompt_Engineer

> 吉客AI / Jeek AI —— 提示词工程知识库（公开仓库）

集中存放各模型（文生图 / 图像编辑 / 视频 / 大模型对话等）的**提示词工程支持性文件**与 **Agent 技能（Skill）**，按模型分类管理，便于版本化、复用与跨 Agent 共享。

本仓库的技能为**通用型**：以 WorkBuddy 为主要适配与测试对象，但同时适用于任何其他支持「加载技能 / 指令文件」的 Agent——只需把对应技能的网址发给 Agent，由 Agent 自动安装即可，无需改写内容。

## 分类索引

| 分类目录 | 模型 | 内容 |
|---|---|---|
| `QwenImage2.1/` | 阿里 Qwen-Image 2.1（文生图 / 图像编辑） | Agent 技能：`jeek-qi21-prompt` —— 提示词增强、双模式（t2i / edit）、缺失信息追问、JSON 校验 |
| `MOSSImage/` | 上海人工智能实验室 OpenMOSS MOSS-Image（文生图 / 图文排版） | Agent 技能：`jeek-moss-prompt` —— 提示词增强、双模式（caption / Layout）、缺失信息追问、JSON 校验 + 编译 |
| `H3/` | MiniMax H3（文本 / 图像 / 视频 / 音频多模态视频生成） | Agent 技能：`jeek-h3-prompt` —— 五模式（T2VA / I2VA / FL2VA / L2VA / Ref2VA）提示词编写、缺失信息追问、输出结构校验 |

## 目录结构

```
Jeek_Prompt_Engineer/
├── README.md
├── QwenImage2.1/
│   ├── README.md                # 本分类自述（可单独查看 / 安装）
│   └── jeek-qi21-prompt/        # 可直接复制安装到任意 Agent 的 skills 目录
│       ├── SKILL.md
│       ├── references/
│       │   ├── t2i_guide.md        # 文生图：官方 8 步法动作化重排
│       │   ├── edit_guide.md       # 图像编辑：双语言决策 + 属性解耦 + 尺寸决策全表
│       │   └── missing_info.md     # 缺失信息闸门与追问模板
│       └── scripts/
│           └── prompt_validator.py # 原创 JSON 校验器
├── MOSSImage/
│   ├── README.md                # 本分类自述（可单独查看 / 安装）
│   └── jeek-moss-prompt/         # 可直接复制安装到任意 Agent 的 skills 目录
│       ├── SKILL.md
│       ├── references/
│       │   ├── caption_guide.md    # caption：连贯散文、空间关系用文字、可见文字精确引用
│       │   ├── layout_guide.md     # Layout：bbox 坐标系统 + 字段 schema + 编译转换
│       │   └── missing_info.md     # 缺失信息闸门与追问模板
│       └── scripts/
│           └── prompt_validator.py # 原创 JSON 校验 + 编译（caption / Layout）
├── H3/
│   ├── README.md                # 本分类自述（可单独查看 / 安装）
│   └── jeek-h3-prompt/           # 可直接复制安装到任意 Agent 的 skills 目录
│       ├── SKILL.md
│       ├── references/
│       │   ├── base_guide.md       # 基础四模式 T2VA/I2VA/FL2VA/L2VA 编写指南
│       │   ├── ref_guide.md        # 全参考 Ref2VA 六段式编写指南（参考标签体系）
│       │   └── missing_info.md      # 缺失信息闸门与追问模板
│       └── scripts/
│           └── prompt_validator.py # 原创输出结构校验器（base / ref / auto）
└── docs/                          # 跨模型通用文档（预留）
```

## 分类目录 = 可独立安装 / 可单独分发的单元

每个**分类目录**（如 `QwenImage2.1/`、`MOSSImage/`）都是自包含、可单独分发的。**让 Agent 安装某模型的技能时，不需要用户手动下载文件再复制**——直接把该分类目录（或其中具体技能文件夹）的网址发给 Agent，Agent 会自动拉取并安装。

- 分类目录内必含一份 `README.md`（说明本分类用途与安装方式）和一个或多个技能文件夹。
- 想只装某个模型：把该分类目录的网址发给 Agent；想装单个技能：发该技能文件夹的网址。

## 安装 / 使用

推荐方式：**把技能网址发给 Agent，由 Agent 自动安装**，无需手动下载或复制文件。

**QwenImage2.1 示例：**
1. 复制下列网址之一，直接发给你的 Agent（任何支持「加载技能 / 指令」的 Agent 均可）：
   - 安装整个 Qwen Image 2.1 分类：`https://github.com/Josia-doit/Jeek_Prompt_Engineer/tree/main/QwenImage2.1`
   - 只安装该技能：`https://github.com/Josia-doit/Jeek_Prompt_Engineer/tree/main/QwenImage2.1/jeek-qi21-prompt`
2. Agent 会自动拉取并安装技能（以 WorkBuddy 为例，会装入用户级 `~/.workbuddy/skills/`；其他 Agent 按各自机制处理，无需你手动操作）。
3. 直接说「帮我把这个想法写成 Qwen 出图提示词」或「把这张图改成…」即可触发；技能自动判别文生图 / 图像编辑，缺信息时主动追问。
4. 校验脚本也可独立运行（不依赖任何 Agent）：`python QwenImage2.1/jeek-qi21-prompt/scripts/prompt_validator.py --mode t2i`（或 `--mode edit`）。

**MOSSImage 示例：**
1. 复制下列网址之一，直接发给你的 Agent：
   - 安装整个 MOSS-Image 分类：`https://github.com/Josia-doit/Jeek_Prompt_Engineer/tree/main/MOSSImage`
   - 只安装该技能：`https://github.com/Josia-doit/Jeek_Prompt_Engineer/tree/main/MOSSImage/jeek-moss-prompt`
2. Agent 安装后，直接说「帮我把这个想法写成 MOSS 出图提示词」或「用 MOSS-Image 做个精准排版的封面」即可触发；技能自动判别 caption / Layout，缺信息时主动追问。
3. 校验 + 编译脚本可独立运行：`python MOSSImage/jeek-moss-prompt/scripts/prompt_validator.py --mode caption`（或 `--mode layout`）。

**H3 示例：**
1. 复制下列网址之一，直接发给你的 Agent：
   - 安装整个 H3 分类：`https://github.com/Josia-doit/Jeek_Prompt_Engineer/tree/main/H3`
   - 只安装该技能：`https://github.com/Josia-doit/Jeek_Prompt_Engineer/tree/main/H3/jeek-h3-prompt`
2. Agent 安装后，直接说「帮我把这个想法写成 H3 视频提示词」或「用 H3 做图生视频，首帧是这张图」即可触发；技能自动判定输入模态（T2VA / I2VA / FL2VA / L2VA / Ref2VA），缺信息时主动追问。
3. 输出结构校验脚本可独立运行：`python H3/jeek-h3-prompt/scripts/prompt_validator.py --mode base`（或 `--mode ref` / `--mode auto`）。

> 仓库所有者：`Josia-doit`（公开仓库，欢迎复用与共建）。

## 如何新增一个模型分类

1. 在仓库根新建一个以模型命名的**分类目录**（如 `HunyuanVideo/`、`LTXVideo/`）。
2. 在该目录下写一份 `README.md`（本分类自述），并放入该模型的技能文件夹，命名遵循 hyphen-case **全小写**（如 `jeek-hv-prompt/`），保持 `SKILL.md` + `references/` + `scripts/` 结构。
3. 在上方「分类索引」表格追加一行。
4. 提交，并在获得授权后将改动推送到本公开仓库。

## 规范

- **分类目录命名**：紧凑格式，**无空格、无下划线**（如 `QwenImage2.1`、`HunyuanVideo`、`LTXVideo`、`MOSSImage`）。**不要缩写**——尤其同一厂商下有多款模型时（如 Qwen 旗下种类很多），缩写会造成误解，请使用能明确区分模型的完整可识别名。
- **Skill 名**：hyphen-case，强制全小写（`^[a-z0-9-]+$`），例如 `jeek-qi21-prompt`、`jeek-moss-prompt`。
- 每个分类目录下：一份自述 `README.md` + 一个或多个**可直接安装**的技能文件夹，结构统一。
- 技能内容为**通用型**：以 WorkBuddy 为主要参考实现，同时兼容其他 Agent（追问提供「结构化问询工具」与「编号文本」两种路径，见技能内说明）。
- 文档与说明使用中文，技术术语（如 `wh_ratio`、`ratio_follow`、t2i / edit / caption / Layout）保留英文原样。
- 当前分类：`QwenImage2.1`（Qwen-Image 2.1 文生图 / 图像编辑提示词增强）、`MOSSImage`（MOSS-Image 文生图 / 图文排版提示词增强，caption / Layout 双模式）、`H3`（MiniMax H3 多模态视频生成提示词编写，T2VA / I2VA / FL2VA / L2VA / Ref2VA 五模式）。
