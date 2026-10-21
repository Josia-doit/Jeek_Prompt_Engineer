# MOSSImage —— MOSS-Image 提示词工程技能

本目录是 `Jeek_Prompt_Engineer` 仓库的一个**分类目录**，可单独复制其网址、让 Agent 只安装本模型的提示词技能，而不必拉取整个仓库。

## 包含的技能

| 技能文件夹 | 适用模型 | 功能 |
|---|---|---|
| `jeek-moss-prompt/` | 上海人工智能实验室 OpenMOSS MOSS-Image（文生图 / 图文排版） | 提示词增强、双模式（caption / Layout）、缺失信息追问、JSON 校验 + 编译 |

## 安装（通用型，Agent 自动安装）

把本目录（或下方技能文件夹）的网址发给你的 Agent，**由 Agent 自动拉取并安装，无需手动下载或复制文件**：

- 本分类网址：`https://github.com/Josia-doit/Jeek_Prompt_Engineer/tree/main/MOSSImage`
- 单技能网址：`https://github.com/Josia-doit/Jeek_Prompt_Engineer/tree/main/MOSSImage/jeek-moss-prompt`

Agent 安装后，直接说「帮我把这个想法写成 MOSS 出图提示词」或「用 MOSS-Image 做个精准排版的封面」即可触发。

## 校验脚本（独立运行，不依赖任何 Agent）

```bash
python jeek-moss-prompt/scripts/prompt_validator.py --mode caption
# 或 --mode layout，详见脚本内 --help
```

## 说明

- 技能为**通用型**：以 WorkBuddy 为主要参考实现，同时兼容其他支持技能 / 指令加载的 Agent。
- 技能名 `jeek-moss-prompt` 为 hyphen-case 全小写（`^[a-z0-9-]+$`）。
- 规则来源：MOSS-Image 公开 Layout 词汇（caption / Layout 双模式、绝对像素 bbox 编译为中心原点坐标）。
