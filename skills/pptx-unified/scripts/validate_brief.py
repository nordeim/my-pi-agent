#!/usr/bin/env python3
"""
Validate slides_brief.json schema + path checks.

Usage:
    python3 validate_brief.py /path/to/slides_brief.json

Checks:
    1. Valid JSON
    2. Required top-level fields (design, global_css_path, slides_dir, language, speaker_notes, slides)
    3. design block has palette (background, primary, accent) + typography (heading, body, numeric)
    4. Every slide has title, layout, output_path, task_brief
    5. global_css_path exists on disk
    6. slides_dir exists on disk
    7. Every slide output_path is absolute (not relative)
    8. Filenames sort alphabetically into list order (warning, not error)
    9. speaker_notes is one of: none, short, full
   10. language is one of: en, zh, bilingual

Exit codes:
    0 = all checks passed
    1 = errors found
"""

import json
import os
import sys
from pathlib import Path


VALID_LANGUAGES = {"en", "zh", "bilingual"}
VALID_NOTE_MODES = {"none", "short", "full"}
VALID_LAYOUTS = {
    "cover", "stat_block", "bento_grid", "stats_grid", "section_divider",
    "split_text_features", "comparison_card", "three_column_spotlight",
    "timeline", "step_guide", "closing", "quote"
}

REQUIRED_TOP_FIELDS = {"design", "global_css_path", "slides_dir", "language", "speaker_notes", "slides"}
REQUIRED_DESIGN_FIELDS = {"title", "style_name", "palette", "typography", "reference"}
REQUIRED_PALETTE_FIELDS = {"background", "primary", "accent"}
REQUIRED_TYPOGRAPHY_FIELDS = {"heading", "body", "numeric"}
REQUIRED_SLIDE_FIELDS = {"title", "layout", "output_path", "task_brief"}


def validate(brief_path: str) -> int:
    errors = []
    warnings = []

    # 1. Valid JSON
    try:
        with open(brief_path, "r", encoding="utf-8") as f:
            brief = json.load(f)
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON: {e}")
        return 1
    except FileNotFoundError:
        print(f"❌ File not found: {brief_path}")
        return 1

    # 2. Required top-level fields
    missing_top = REQUIRED_TOP_FIELDS - set(brief.keys())
    if missing_top:
        errors.append(f"Missing top-level fields: {missing_top}")

    # 3. design block
    if "design" in brief:
        design = brief["design"]
        missing_design = REQUIRED_DESIGN_FIELDS - set(design.keys())
        if missing_design:
            errors.append(f"design block missing fields: {missing_design}")

        if "palette" in design:
            missing_palette = REQUIRED_PALETTE_FIELDS - set(design["palette"].keys())
            if missing_palette:
                errors.append(f"design.palette missing fields: {missing_palette}")

        if "typography" in design:
            missing_typo = REQUIRED_TYPOGRAPHY_FIELDS - set(design["typography"].keys())
            if missing_typo:
                errors.append(f"design.typography missing fields: {missing_typo}")

    # 4. language and speaker_notes
    if "language" in brief and brief["language"] not in VALID_LANGUAGES:
        errors.append(f"language must be one of {VALID_LANGUAGES}, got: {brief['language']}")

    if "speaker_notes" in brief and brief["speaker_notes"] not in VALID_NOTE_MODES:
        errors.append(f"speaker_notes must be one of {VALID_NOTE_MODES}, got: {brief['speaker_notes']}")

    # 5. global_css_path exists
    if "global_css_path" in brief:
        css_path = brief["global_css_path"]
        if not os.path.isabs(css_path):
            errors.append(f"global_css_path must be absolute, got: {css_path}")
        if not os.path.isfile(css_path):
            errors.append(f"global_css_path does not exist on disk: {css_path}")

    # 6. slides_dir exists
    if "slides_dir" in brief:
        slides_dir = brief["slides_dir"]
        if not os.path.isabs(slides_dir):
            errors.append(f"slides_dir must be absolute, got: {slides_dir}")
        if not os.path.isdir(slides_dir):
            errors.append(f"slides_dir does not exist on disk: {slides_dir}")

    # 7. Every slide has required fields
    slides = brief.get("slides", [])
    if not slides:
        errors.append("slides array is empty")
    else:
        for i, slide in enumerate(slides):
            missing_slide = REQUIRED_SLIDE_FIELDS - set(slide.keys())
            if missing_slide:
                errors.append(f"slides[{i}] missing fields: {missing_slide}")

            # Check output_path is absolute
            if "output_path" in slide:
                op = slide["output_path"]
                if not os.path.isabs(op):
                    errors.append(f"slides[{i}].output_path must be absolute, got: {op}")

            # Check layout is valid
            if "layout" in slide and slide["layout"] not in VALID_LAYOUTS:
                warnings.append(f"slides[{i}].layout '{slide['layout']}' not in canonical set {VALID_LAYOUTS}")

            # Check task_brief is non-empty
            if "task_brief" in slide and len(slide["task_brief"].strip()) < 20:
                warnings.append(f"slides[{i}].task_brief is suspiciously short (<20 chars)")

    # 8. Filenames sort alphabetically into list order
    if slides and all("output_path" in s for s in slides):
        filenames = [os.path.basename(s["output_path"]) for s in slides]
        if filenames != sorted(filenames):
            warnings.append(f"Filenames do not sort alphabetically into list order: {filenames}")
            warnings.append("  Stage 5 export will produce slides in filename-sorted order, not list order.")
            warnings.append("  Rename to slide_{NN:02d}.html matching list index AND update output_paths.")

    # Report
    print(f"\nValidating: {brief_path}")
    print(f"Slides: {len(slides)}")

    if errors:
        print(f"\n❌ {len(errors)} error(s):")
        for e in errors:
            print(f"  - {e}")

    if warnings:
        print(f"\n⚠  {len(warnings)} warning(s):")
        for w in warnings:
            print(f"  - {w}")

    if not errors and not warnings:
        print("\n✅ All checks passed.")
    elif not errors:
        print(f"\n✅ All errors passed ({len(warnings)} warnings to review).")

    return 1 if errors else 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 validate_brief.py /path/to/slides_brief.json")
        sys.exit(1)
    sys.exit(validate(sys.argv[1]))
