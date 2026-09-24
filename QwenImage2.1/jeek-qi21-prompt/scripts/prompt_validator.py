#!/usr/bin/env python3
"""Validate a Qwen-Image-2.1 rewritten-prompt JSON object.

This is a deterministic sanity check for the prompt JSON produced by the
jeek-qi21-prompt skill. It catches the most common failure
modes before the prompt is fed to the model:

  * invalid JSON
  * missing / wrong fields for the chosen mode
  * edit mode: wh_ratio and ratio_follow both set or both empty
  * ratio / resolution tokens leaking into rewritten_prompt
  * edit mode: a rendered (quoted) string mixing two writing systems
  * t2i mode: descriptive prose written in a non-Latin script
    (official rule: t2i description is always English; in-image text excepted)

Usage:
    python prompt_validator.py --mode t2i  --json '{"rewritten_prompt":"...","wh_ratio":"3:2"}'
    python prompt_validator.py --mode edit  --json '{"rewritten_prompt":"...","wh_ratio":"","ratio_follow":"<image1>"}'
    echo '<json>' | python prompt_validator.py --mode edit

Exit code 0 = PASS (warnings allowed), 1 = FAIL.
"""

import argparse
import json
import re
import sys

# --- regex helpers -----------------------------------------------------------

# Ratio / resolution tokens that must NEVER appear inside rewritten_prompt.
LEAK_PATTERN = re.compile(
    r"\b\d{1,3}:\d{1,3}\b"          # 16:9, 3:2, 2:3 ...
    r"|\b\d{3,4}[x×]\d{3,4}\b"      # 1920x1080, 800x600
    r"|\b(?:1080p|720p|2[Kk]|4[Kk]|8[Kk])\b",  # quality/resolution keywords
    re.IGNORECASE,
)

# Script-family detection for quoted (rendered) strings.
SCRIPT_RANGES = {
    "Latin": r"[A-Za-z\u00C0-\u024F]",
    "CJK": r"[\u3400-\u4DBF\u4E00-\u9FFF\uF900-\uFAFF]",
    "Kana": r"[\u3040-\u30FF]",
    "Hangul": r"[\u1100-\u11FF\uAC00-\uD7AF]",
    "Cyrillic": r"[\u0400-\u04FF]",
    "Arabic": r"[\u0600-\u06FF]",
    "Thai": r"[\u0E00-\u0E7F]",
}
SCRIPT_PATTERNS = {name: re.compile(p) for name, p in SCRIPT_RANGES.items()}

QUOTE_PATTERN = re.compile(r'"[^"]*"')


def detect_scripts(text):
    """Return the set of script families present in `text`."""
    return {name for name, pat in SCRIPT_PATTERNS.items() if pat.search(text)}


def extract_quoted(text):
    """Return list of double-quoted substrings (the rendered in-image text)."""
    return QUOTE_PATTERN.findall(text)


# --- validation --------------------------------------------------------------

def validate(mode, data):
    """Return (errors, warnings). errors non-empty => FAIL."""
    errors = []
    warnings = []

    if not isinstance(data, dict):
        return ["Top-level JSON is not an object"], warnings

    rp = data.get("rewritten_prompt")
    if not isinstance(rp, str) or not rp.strip():
        errors.append("`rewritten_prompt` is missing or empty")
        rp = ""  # keep going for other checks

    if mode == "t2i":
        if "ratio_follow" in data:
            warnings.append("t2i mode should not carry `ratio_follow`; ignoring it")
        wh = data.get("wh_ratio")
        if not isinstance(wh, str) or not wh.strip():
            errors.append("t2i mode requires a non-empty `wh_ratio` (e.g. '3:2')")
        # English-only descriptive prose (outside quotes)
        quoted = extract_quoted(rp)
        body = rp
        for q in quoted:
            body = body.replace(q, " ")
        foreign = detect_scripts(body) - {"Latin"}
        if foreign:
            warnings.append(
                "t2i description contains non-English prose (%s). "
                "Official rule: t2i description is always English; "
                "only in-image text keeps its own script." % ", ".join(sorted(foreign))
            )

    elif mode == "edit":
        wh = data.get("wh_ratio", "")
        rf = data.get("ratio_follow", "")
        wh_set = isinstance(wh, str) and wh.strip() != ""
        rf_set = isinstance(rf, str) and rf.strip() != ""
        if wh_set and rf_set:
            errors.append("`wh_ratio` and `ratio_follow` are both set; exactly one must be non-empty")
        elif not wh_set and not rf_set:
            errors.append("`wh_ratio` and `ratio_follow` are both empty; exactly one must be non-empty")
        if rf_set and not re.fullmatch(r"<image\d+>", rf.strip()):
            errors.append("`ratio_follow` must look like '<image1>', '<image2>', ... (got %r)" % rf)
        # quoted-string monolingual check (language decision B)
        for q in extract_quoted(rp):
            inner = q[1:-1]
            fams = detect_scripts(inner)
            # Latin + a non-Latin is the classic violation (e.g. "夏日特惠 Summer")
            if len(fams) > 1:
                warnings.append(
                    "rendered text %s mixes writing systems (%s); "
                    "language decision (B) requires a single language unless the user asked for a pair"
                    % (q, ", ".join(sorted(fams)))
                )
    else:
        errors.append("unknown mode %r (expected 't2i' or 'edit')" % mode)

    # Ratio / resolution leak into the description (both modes)
    if rp:
        leaks = LEAK_PATTERN.findall(rp)
        if leaks:
            errors.append(
                "ratio/resolution token(s) %s leaked into `rewritten_prompt`; "
                "keep ratios only in `wh_ratio`/`ratio_follow`" % leaks
            )

    return errors, warnings


def main():
    ap = argparse.ArgumentParser(description="Validate Qwen-Image-2.1 prompt JSON.")
    ap.add_argument("--mode", required=True, choices=["t2i", "edit"], help="prompt mode")
    ap.add_argument("--json", help="JSON string to validate (else read from stdin)")
    args = ap.parse_args()

    raw = args.json if args.json is not None else sys.stdin.read().strip()
    if not raw:
        print("FAIL: no JSON provided (use --json or pipe via stdin)")
        sys.exit(1)

    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        print("FAIL: invalid JSON -> %s" % e)
        sys.exit(1)

    errors, warnings = validate(args.mode, data)

    for w in warnings:
        print("WARN: %s" % w)
    for e in errors:
        print("FAIL: %s" % e)

    if errors:
        print("\nRESULT: FAIL (%d error(s), %d warning(s))" % (len(errors), len(warnings)))
        sys.exit(1)
    print("\nRESULT: PASS (%d warning(s))" % len(warnings))
    sys.exit(0)


if __name__ == "__main__":
    main()
