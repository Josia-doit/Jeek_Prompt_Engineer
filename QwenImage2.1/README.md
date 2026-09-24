# QwenImage2.1 —— Qwen-Image 2.1 提示词工程技能

本目录是 `Jeek_Prompt_Engineer` 仓库的一个**分类目录**，可单独复制其网址、让 Agent 只安装本模型的提示词技能，而不必拉取整个仓库。

## 包含的技能

| 技能文件夹 | 适用模型 | 功能 |
|---|---|---|
| `jeek-qi21-prompt/` | 阿里 Qwen-Image 2.1（文生图 / 图像编辑） | 提示词增强、双模式（t2i / edit）、缺失信息追问、JSON 校验 |

## 安装（通用型，Agent 自动安装）

把本目录（或下方技能文件夹）的网址发给你的 Agent，**由 Agent 自动拉取并安装，无需手动下载或复制文件**：

- 本分类网址：`https://github.com/Josia-doit/Jeek_Prompt_Engineer/tree/main/QwenImage2.1`
- 单技能网址：`https://github.com/Josia-doit/Jeek_Prompt_Engineer/tree/main/QwenImage2.1/jeek-qi21-prompt`

Agent 安装后，直接说「帮我把这个想法写成 Qwen 出图提示词」或「把这张图改成…」即可触发。

## 校验脚本（独立运行，不依赖任何 Agent）

```bash
python jeek-qi21-prompt/scripts/prompt_validator.py --mode t2i
# 或 --mode edit，详见脚本内 --help
```

## 说明

- 技能为**通用型**：以 WorkBuddy 为主要参考实现，同时兼容其他支持技能 / 指令加载的 Agent。
- 技能名 `jeek-qi21-prompt` 为 hyphen-case 全小写（`^[a-z0-9-]+$`）。
- 规则来源：阿里官方 Qwen-Image 2.1 提示词重写 system prompt（文生图 8 步法、图像编辑属性解耦法）。
