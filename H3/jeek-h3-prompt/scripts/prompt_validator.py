#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
jeek-h3-prompt 提示词结构校验器。

校验 MiniMax H3 视频提示词的最终输出是否符合本技能约定的结构：
  - 基础模式（base，含 T2VA/I2VA/FL2VA/L2VA）：对齐指令行(可选) + 三段核心字段
  - 全参考模式（ref，Ref2VA）：六段字段 + 参考标签一致性

用法：
  python prompt_validator.py --mode base  --text "..."            # 直接传文本
  python prompt_validator.py --mode ref   --file out.txt          # 读文件
  python prompt_validator.py --mode auto  --text "..."            # 自动判定模式

输出：EXIT 0 = 通过；EXIT 1 = 存在错误。错误信息以中文列出。
"""
import argparse
import re
import sys

CORE_FIELDS = ["integrated_multimodal_description", "overall_soundscape", "non_diegetic_music"]
REF_SECTIONS = ["subject_definitions", "summary", "retention_analysis",
                "detailed_description", "overall_soundscape", "non_diegetic_music"]
VIS_MARKERS = {"fully_preserved", "partially_preserved", "attribute_transfer", "weak_reference"}
AUD_MARKERS = {"fully_copy", "partially_copy", "reference", "weak_reference"}
LABEL_RE = re.compile(r"<(Subject|Picture|Video|Audio)\s+(\d+)>")


def _field_lines(text):
    """返回 (字段名, 行号) 列表，字段名为行首 `name:` 形式。"""
    out = []
    for i, line in enumerate(text.splitlines(), 1):
        m = re.match(r"^([a-z_]+):\s*", line)
        if m:
            out.append((m.group(1), i))
    return out


def _check_order(found, required, errors, warnings):
    missing = [f for f in required if f not in found]
    if missing:
        errors.append("缺少必需字段：" + "、".join(missing))
        return
    # 顺序检查
    idxs = [found.index(f) for f in required]
    if idxs != sorted(idxs):
        errors.append("字段顺序错误，应为：" + " → ".join(required))


def _desc_span(text, name):
    """返回字段 name 的值区间 (start, end)，到下一个字段行为止。"""
    m = re.search(r"^" + name + r":", text, re.M)
    if not m:
        return None
    rest = text[m.start():]
    nxt = re.search(r"\n[a-z_]+:", rest)
    start = m.end()
    end = (m.start() + nxt.start()) if nxt else len(text)
    return (start, end)


def _check_shots(text, errors, warnings, span=None):
    """检查 [Shot N] 时间戳格式：首镜头不带 At；后续带 At MM:SS.mmm。

    按镜头段（相邻 [Shot N] 标记之间）判断，而非整行——因为
    integrated_multimodal_description / detailed_description 整段常写在同一字段行内。
    span 限定只在描述字段体内检查，避免 retention_analysis 里的镜头引用被误判。
    """
    matches = list(re.finditer(r"\[Shot\s+(\d+)\]", text))
    if span:
        matches = [m for m in matches if span[0] <= m.start() < span[1]]
    for idx, m in enumerate(matches):
        n = int(m.group(1))
        ln = text[:m.start()].count("\n") + 1
        start = m.end()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else (span[1] if span else len(text))
        seg = text[start:end]
        has_at = bool(re.search(r"\bAt\s+\d{2}:\d{2}\.\d{3}", seg))
        if n == 1 and has_at:
            errors.append(f"第 {ln} 行附近：首镜头 [Shot 1] 不应带切镜时间戳（At ...）。")
        elif n > 1 and not has_at:
            warnings.append(f"第 {ln} 行附近：[Shot {n}] 建议带切镜时间戳 At MM:SS.mmm。")


def _check_dialogue(text, errors, warnings):
    """检查 <d>[Lang]...</d> 成对、[Language] 标签存在。"""
    opens = len(re.findall(r"<d>\s*\[", text))
    closes = len(re.findall(r"</d>", text))
    if opens != closes:
        errors.append(f"对话标签不平衡：<d> 开 {opens} 次，</d> 闭 {closes} 次。")
    if re.search(r"<d>\s*\[", text) and not re.search(r"<d>\s*\[[A-Za-z\-]+\]", text):
        warnings.append("存在 <d> 但缺少语言标签，如 <d>[English] ...</d>。")


def validate_base(text):
    errors, warnings = [], []
    fields = _field_lines(text)
    found = [f for f, _ in fields]
    # 对齐指令行（关键帧模式）
    has_align = bool(re.search(r"aligns with the (?:0\.00|\d+\.\d{2})-second mark", text)) or \
                bool(re.search(r"is fully referenced", text))
    if has_align:
        # 对齐行应是第一个核心字段之前
        first_core = next((ln for f, ln in fields if f in CORE_FIELDS), None)
        align_ln = None
        for i, line in enumerate(text.splitlines(), 1):
            if "aligns with the" in line or "is fully referenced" in line:
                align_ln = i
                break
        if align_ln and first_core and align_ln > first_core:
            errors.append("对齐指令行应位于核心字段之前（提示词首行）。")
    _check_order(found, CORE_FIELDS, errors, warnings)
    _check_shots(text, errors, warnings, _desc_span(text, "integrated_multimodal_description"))
    _check_dialogue(text, errors, warnings)
    return errors, warnings


def validate_ref(text):
    errors, warnings = [], []
    fields = _field_lines(text)
    found = [f for f, _ in fields]
    _check_order(found, REF_SECTIONS, errors, warnings)

    # summary 任务类型前缀
    m = re.search(r"^summary:\s*\[([^\]]+)\]", text, re.M)
    if not m:
        warnings.append("summary 建议以方括号任务类型前缀开头，如 [reference generation]。")

    # 参考标签一致性
    defined = set()
    in_defs = False
    for line in text.splitlines():
        if line.startswith("subject_definitions:"):
            in_defs = True
            continue
        if in_defs and re.match(r"^[a-z_]+:", line):
            in_defs = False
        if in_defs:
            for t, n in LABEL_RE.findall(line):
                defined.add((t, int(n)))
    used = set((t, int(n)) for t, n in LABEL_RE.findall(text))
    undefined = used - defined
    if undefined:
        s = "、".join(f"<{t} {n}>" for t, n in sorted(undefined))
        warnings.append(f"以下参考标签未在 subject_definitions 中定义即被使用：{s}（建议补充定义）。")

    # retention_analysis 关系标记合法
    in_ret = False
    for line in text.splitlines():
        if line.startswith("retention_analysis:"):
            in_ret = True
            continue
        if in_ret and re.match(r"^[a-z_]+:", line):
            in_ret = False
        if in_ret:
            if "<Audio" in line:
                if not any(mk in line for mk in AUD_MARKERS):
                    warnings.append(f"音频保留标记未识别（应属 {sorted(AUD_MARKERS)}）：{line.strip()[:60]}")
            elif any(k in line for k in ("<Subject", "<Picture", "<Video")):
                if not any(mk in line for mk in VIS_MARKERS):
                    warnings.append(f"可视保留标记未识别（应属 {sorted(VIS_MARKERS)}）：{line.strip()[:60]}")
            if "(S" in line:
                errors.append("retention_analysis 中不应出现说话人 ID (Sx)。")

    _check_shots(text, errors, warnings, _desc_span(text, "detailed_description"))
    _check_dialogue(text, errors, warnings)
    return errors, warnings


def detect_mode(text):
    if "subject_definitions:" in text:
        return "ref"
    return "base"


def main():
    ap = argparse.ArgumentParser(description="jeek-h3-prompt H3 提示词结构校验器")
    ap.add_argument("--mode", choices=["base", "ref", "auto"], default="auto")
    ap.add_argument("--text", help="直接传入提示词文本")
    ap.add_argument("--file", help="从文件读取提示词文本")
    args = ap.parse_args()

    if args.text:
        text = args.text
    elif args.file:
        with open(args.file, encoding="utf-8") as f:
            text = f.read()
    else:
        ap.error("必须提供 --text 或 --file")

    mode = args.mode
    if mode == "auto":
        mode = detect_mode(text)

    errors, warnings = (validate_ref if mode == "ref" else validate_base)(text)

    print(f"模式判定：{mode}")
    if warnings:
        print("\n警告（不阻断）：")
        for w in warnings:
            print("  - " + w)
    if errors:
        print("\n错误：")
        for e in errors:
            print("  - " + e)
        print(f"\n校验失败：{len(errors)} 个错误。")
        sys.exit(1)
    print("\n校验通过：结构符合 jeek-h3-prompt 约定。")
    sys.exit(0)


if __name__ == "__main__":
    main()
