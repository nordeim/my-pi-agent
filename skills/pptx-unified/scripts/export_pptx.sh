#!/usr/bin/env bash
# export_pptx.sh — Wrapper that finds batch_html2pptx.js dynamically + runs export.
#
# Usage:
#   bash export_pptx.sh /path/to/slides_dir /path/to/output.pptx
#
# This wrapper handles:
#   1. Dynamically finding batch_html2pptx.js (the canonical pptx skill doc has a
#      typo — it says skills/ppt/ but the actual path is skills/pptx/).
#   2. Setting NODE_PATH so pptxgenjs / playwright / sharp resolve.
#   3. Running the export.
#   4. Scanning output for 🚨 CRITICAL warnings.
#
# Exit codes:
#   0 = export succeeded, no critical warnings
#   1 = usage error
#   2 = batch_html2pptx.js not found
#   3 = export failed or critical warnings found

set -euo pipefail

# ─── Usage check ───
if [ $# -lt 1 ] || [ $# -gt 2 ]; then
    echo "Usage: bash export_pptx.sh /path/to/slides_dir [/path/to/output.pptx]"
    echo ""
    echo "Arguments:"
    echo "  slides_dir   Directory containing slide_NN.html files + global.css"
    echo "  output.pptx  Output path (optional, defaults to <slides_dir>/../<basename>.pptx)"
    exit 1
fi

SLIDES_DIR="$1"
OUTPUT_PPTX="${2:-}"

# ─── Validate slides_dir ───
if [ ! -d "$SLIDES_DIR" ]; then
    echo "❌ slides_dir does not exist: $SLIDES_DIR"
    exit 1
fi

if [ ! -f "$SLIDES_DIR/global.css" ]; then
    echo "❌ global.css not found in slides_dir: $SLIDES_DIR"
    exit 1
fi

SLIDE_COUNT=$(ls "$SLIDES_DIR"/slide_*.html 2>/dev/null | wc -l)
if [ "$SLIDE_COUNT" -eq 0 ]; then
    echo "❌ No slide_*.html files found in slides_dir: $SLIDES_DIR"
    exit 1
fi

# ─── Default output path ───
if [ -z "$OUTPUT_PPTX" ]; then
    PARENT_DIR=$(dirname "$SLIDES_DIR")
    BASENAME=$(basename "$PARENT_DIR")
    OUTPUT_PPTX="$PARENT_DIR/$BASENAME.pptx"
fi

echo "━━━ pptx-unified export ━━━"
echo "Slides dir:  $SLIDES_DIR"
echo "Slide count: $SLIDE_COUNT"
echo "Output:      $OUTPUT_PPTX"
echo ""

# ─── Find batch_html2pptx.js dynamically ───
# The canonical pptx skill's SKILL.md says the script is at skills/ppt/ — that's
# a typo. The actual path is skills/pptx/. We search both locations to be safe.
SCRIPT=""
for candidate in \
    "/home/z/my-project/skills/pptx/batch_html2pptx.js" \
    "/home/z/my-project/skills/ppt/batch_html2pptx.js" \
    "/home/z/my-project/my-pi-agent/skills/pptx/batch_html2pptx.js"; do
    if [ -f "$candidate" ]; then
        SCRIPT="$candidate"
        break
    fi
done

# Fallback: search the filesystem
if [ -z "$SCRIPT" ]; then
    SCRIPT=$(find /home/z/my-project/skills /home/z/my-project/my-pi-agent/skills \
        -name "batch_html2pptx.js" -type f 2>/dev/null | head -1)
fi

if [ -z "$SCRIPT" ]; then
    echo "❌ batch_html2pptx.js not found."
    echo "   Searched: /home/z/my-project/skills/pptx/, /home/z/my-project/skills/ppt/,"
    echo "             /home/z/my-project/my-pi-agent/skills/pptx/"
    echo "   Install the canonical pptx skill or add the script manually."
    exit 2
fi

echo "Resolved script: $SCRIPT"
echo ""

# ─── Run the export ───
cd /home/z/my-project

# Capture output to scan for 🚨 CRITICAL warnings
OUTPUT_FILE=$(mktemp)
trap 'rm -f "$OUTPUT_FILE"' EXIT

NODE_PATH=/usr/local/lib/node_modules node "$SCRIPT" "$SLIDES_DIR" "$OUTPUT_PPTX" 2>&1 | tee "$OUTPUT_FILE"
EXPORT_EXIT=${PIPESTATUS[0]}

echo ""
echo "━━━ Post-export checks ━━━"

# ─── Check exit code ───
if [ "$EXPORT_EXIT" -ne 0 ]; then
    echo "❌ Export failed with exit code $EXPORT_EXIT"
    exit 3
fi

# ─── Check for 🚨 CRITICAL warnings ───
CRITICAL_COUNT=$(grep -c "🚨 CRITICAL" "$OUTPUT_FILE" || true)
if [ "$CRITICAL_COUNT" -gt 0 ]; then
    echo "❌ Found $CRITICAL_COUNT 🚨 CRITICAL warning(s) in export output:"
    grep "🚨 CRITICAL" "$OUTPUT_FILE"
    echo ""
    echo "Fix the source HTML and re-run. The .pptx was generated but has critical issues."
    exit 3
fi

# ─── Verify output file ───
if [ ! -f "$OUTPUT_PPTX" ]; then
    echo "❌ Output .pptx not created: $OUTPUT_PPTX"
    exit 3
fi

FILE_SIZE=$(ls -lh "$OUTPUT_PPTX" | awk '{print $5}')
echo "✅ Export succeeded."
echo "   File: $OUTPUT_PPTX"
echo "   Size: $FILE_SIZE"
echo "   Critical warnings: 0"

# ─── Soft warnings count (informational) ───
SOFT_WARNING_COUNT=$(grep -c "^⚠" "$OUTPUT_FILE" || true)
if [ "$SOFT_WARNING_COUNT" -gt 0 ]; then
    echo "   Soft warnings: $SOFT_WARNING_COUNT (review recommended but non-blocking)"
fi

exit 0
