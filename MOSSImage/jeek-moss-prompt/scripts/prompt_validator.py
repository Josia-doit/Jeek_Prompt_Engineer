#!/usr/bin/env python3
"""Validate and compile a MOSS-Image caption or Layout draft.

This is a deterministic sanity check + compiler for the prompt JSON produced by
the jeek-moss-prompt skill. It catches the most common failure modes before the
prompt is fed to MOSS-Image, and (for Layout) converts absolute-pixel bounding
boxes into the center-origin form MOSS-Image expects.

Modes:
  caption  -> {"caption": "..."}                       (plain text out)
  layout   -> {width,height,bbox_coord_space,bbox_format,summary,items}
             compiled to a single-line JSON with abs_centralized / yxyx boxes

Usage:
    python prompt_validator.py --mode caption --json '{"caption":"A cat."}'
    python prompt_validator.py --mode layout  --json '<layout-draft.json>'
    echo '<layout-draft>' | python prompt_validator.py --mode layout
    python prompt_validator.py --mode layout --json '<draft>' --check-only

Exit code 0 = compiled output on stdout (or PASS with --check-only); 1 = FAIL.
WARN / FAIL / RESULT lines go to stderr so stdout stays pipe-clean.
"""

import argparse
import json
import math
import sys


# --- helpers ----------------------------------------------------------------

def require(condition, message):
    if not condition:
        raise ValueError(message)


def fields(value, allowed, required, location):
    require(isinstance(value, dict), "%s must be an object" % location)
    unknown = set(value.keys()) - set(allowed)
    missing = set(required) - set(value.keys())
    require(not unknown, "%s: unknown fields %s" % (location, sorted(unknown)))
    require(not missing, "%s: missing fields %s" % (location, sorted(missing)))


def text(value, location):
    require(isinstance(value, str) and bool(value.strip()),
            "%s must be nonempty text" % location)


def strings(value, location):
    require(isinstance(value, list), "%s must be an array" % location)
    for index, item in enumerate(value):
        text(item, "%s[%d]" % (location, index))


def centered_box(box, width, height, location):
    """Validate an absolute xyxy box and return the compiled yxyx center box."""
    require(isinstance(box, list) and len(box) == 4,
            "%s must be [x1,y1,x2,y2]" % location)
    require(all(type(v) in (int, float) and math.isfinite(v) for v in box),
            "%s must contain four finite numbers" % location)
    x1, y1, x2, y2 = box
    require(x1 < x2 and y1 < y2, "%s must have positive width and height" % location)
    require(0 <= x1 < x2 <= width and 0 <= y1 < y2 <= height,
            "%s exceeds the %dx%d canvas" % (location, width, height))
    # Enclose fractional edges before centering, then reorder to yxyx.
    result = [
        math.floor(round(y1, 9)) - height // 2,
        math.floor(round(x1, 9)) - width // 2,
        math.ceil(round(y2, 9)) - height // 2,
        math.ceil(round(x2, 9)) - width // 2,
    ]
    require(result[0] < result[2] and result[1] < result[3],
            "%s is too small at export precision" % location)
    return result


# --- mode: caption -----------------------------------------------------------

def compile_caption(draft):
    fields(draft, {"caption"}, {"caption"}, "Caption draft")
    text(draft["caption"], "caption")
    return draft["caption"]


# --- mode: layout ------------------------------------------------------------

def compile_layout(draft):
    root_allowed = {"width", "height", "bbox_coord_space", "bbox_format",
                    "summary", "items"}
    fields(draft, root_allowed, root_allowed, "Layout draft")
    width, height = draft["width"], draft["height"]
    for name, value in (("width", width), ("height", height)):
        require(type(value) is int and value > 0 and value % 16 == 0,
                "%s must be a positive integer multiple of 16" % name)
    require(draft["bbox_coord_space"] == "abs",
            "Draft bbox_coord_space must be 'abs'")
    require(draft["bbox_format"] == "xyxy",
            "Draft bbox_format must be 'xyxy'")

    summary = draft["summary"]
    fields(summary, {"caption", "meta", "canvas", "palette"},
           {"caption"}, "summary")
    text(summary["caption"], "summary.caption")
    if "canvas" in summary:
        require(summary["canvas"] in ("single", "multi_panel", "collage"),
                "summary.canvas must be single, multi_panel or collage")
    for key in ("meta", "palette"):
        if key in summary:
            strings(summary[key], "summary.%s" % key)

    items = draft["items"]
    require(isinstance(items, list) and bool(items),
            "items must be a nonempty flat array")
    compiled_items = []
    for index, item in enumerate(items):
        location = "items[%d]" % index
        fields(item, {"label", "caption", "bbox", "text", "tags", "palette"},
               {"label", "caption", "bbox"}, location)
        require(item["label"] in ("object", "character", "text"),
                "%s.label must be object, character or text" % location)
        text(item["caption"], "%s.caption" % location)
        if item["label"] == "text":
            require("text" in item,
                    "%s: text items require a literal 'text' field" % location)
        if "text" in item:
            text(item["text"], "%s.text" % location)
        for key in ("tags", "palette"):
            if key in item:
                strings(item[key], "%s.%s" % (location, key))
        compiled_items.append({
            key: centered_box(value, width, height, "%s.bbox" % location)
            if key == "bbox" else value
            for key, value in item.items()
        })

    return json.dumps(
        {"summary": summary, "items": compiled_items,
         "bbox_coord_space": "abs_centralized", "bbox_format": "yxyx"},
        ensure_ascii=False, separators=(",", ":"), allow_nan=False)


# --- entry ------------------------------------------------------------------

def unique_object(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, "Duplicate JSON key: %s" % key)
        result[key] = value
    return result


def reject_constant(value):
    raise ValueError("Invalid JSON number: %s" % value)


def main():
    ap = argparse.ArgumentParser(
        description="Validate + compile a MOSS-Image caption or Layout draft.")
    ap.add_argument("--mode", required=True, choices=["caption", "layout"],
                    help="prompt mode")
    ap.add_argument("--json", help="JSON string to validate (else read stdin)")
    ap.add_argument("--check-only", action="store_true",
                    help="print RESULT: PASS/FAIL without emitting compiled output")
    args = ap.parse_args()

    raw = args.json if args.json is not None else sys.stdin.read().strip()
    if not raw:
        sys.stderr.write("FAIL: no JSON provided (use --json or pipe via stdin)\n")
        sys.exit(1)

    try:
        draft = json.loads(raw, object_pairs_hook=unique_object,
                           parse_constant=reject_constant)
        if args.mode == "caption":
            output = compile_caption(draft)
        else:
            output = compile_layout(draft)
    except (ValueError, OverflowError) as error:
        sys.stderr.write("FAIL: %s\n" % error)
        sys.stderr.write("\nRESULT: FAIL\n")
        sys.exit(1)

    if args.check_only:
        sys.stderr.write("\nRESULT: PASS\n")
        sys.exit(0)

    sys.stdout.write(output + "\n")
    sys.exit(0)


if __name__ == "__main__":
    main()
