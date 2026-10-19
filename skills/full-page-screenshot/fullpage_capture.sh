#!/usr/bin/env bash
# =============================================================================
# fullpage_capture.sh — quality-gated full-page website screenshot (PNG)
#
# Implements the full-page-screenshot skill methodology (Phases 0–8):
#   viewport-first navigation → network-idle load gate → page metrics probe →
#   lazy-content scroll pass → return-to-top settle → full capture →
#   Pillow integrity verification → browser cleanup.
#
# Usage:
#   bash fullpage_capture.sh <URL> <output.png> [width] [height]
#   bash fullpage_capture.sh "https://example.com/" ./example-fullpage.png
#   bash fullpage_capture.sh "https://example.com/" ./out.png 1920 1080
#
# Dependencies:
#   agent-browser (npm i -g agent-browser && agent-browser install)
#   python3 with Pillow (pip install pillow)
#
# Exit codes: 0 = all quality gates passed; non-zero = a gate failed.
# =============================================================================
set -euo pipefail

if [[ $# -lt 2 ]]; then
  echo "Usage: $0 <URL> <output.png> [width] [height]" >&2
  exit 2
fi

URL="$1"
OUT="$2"
W="${3:-1920}"
H="${4:-1080}"

mkdir -p "$(dirname "$OUT")"

cleanup() { agent-browser close >/dev/null 2>&1 || true; }
trap cleanup EXIT

echo "[1/7] Setting viewport ${W}x${H} (before navigation → correct responsive layout)"
agent-browser set viewport "$W" "$H"

echo "[2/7] Navigating to $URL"
agent-browser open "$URL" --timeout 60000
agent-browser wait --load networkidle --timeout 30000
TITLE="$(agent-browser get title)"
agent-browser get url
echo "      page title: ${TITLE}"
PAGE_ERRORS="$(agent-browser errors || true)"
if [[ -n "${PAGE_ERRORS}" ]]; then
  echo "      WARN: page reported JS errors:" >&2
  echo "${PAGE_ERRORS}" >&2
fi

echo "[3/7] Probing page metrics"
METRICS="$(agent-browser eval "JSON.stringify({pageHeight: document.documentElement.scrollHeight, viewportH: window.innerHeight, images: document.images.length, lazyImages: Array.from(document.images).filter(i => i.loading === 'lazy').length})")"
echo "      metrics: ${METRICS}"
PAGE_H="$(python3 - "$METRICS" <<'PY'
import json, sys
raw = sys.argv[1]
try:
    data = json.loads(raw)
    if isinstance(data, str):          # some CLI builds double-encode the payload
        data = json.loads(data)
    print(int(data.get("pageHeight", 0)))
except Exception:
    print(0)
PY
)"

echo "[4/7] Scroll pass to trigger lazy content (page height: ${PAGE_H}px)"
if [[ "${PAGE_H}" -gt "${H}" ]]; then
  PASSES=$(( (PAGE_H + 1199) / 1200 ))
  if [[ "${PASSES}" -gt 30 ]]; then PASSES=30; fi   # guard against infinite-scroll pages
  for ((i = 0; i < PASSES; i++)); do
    agent-browser scroll down 1200 >/dev/null
    sleep 0.4
  done
  sleep 1
  agent-browser wait --load networkidle --timeout 15000 || true
fi

echo "[5/7] Returning to top and letting animations settle"
agent-browser eval "window.scrollTo(0,0); 'top'" >/dev/null
sleep 1.5

echo "[6/7] Capturing full-page screenshot → ${OUT}"
agent-browser screenshot --full "$OUT"

echo "[7/7] Verifying PNG integrity (gate G5)"
python3 - "$OUT" "$W" "$PAGE_H" <<'PY'
import sys
from PIL import Image

path, expect_w, expect_h = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
img = Image.open(path)
fmt = img.format
img.load()
w, h = img.size
print(f"      format={fmt} size={w}x{h} mode={img.mode}")
assert fmt == "PNG", f"GATE FAIL: not a PNG (got {fmt})"
assert w == expect_w, f"GATE FAIL: width {w} != viewport width {expect_w}"
if expect_h:
    assert h == expect_h, (
        f"GATE FAIL: height {h} != probed page height {expect_h} "
        "(page changed mid-capture, or capture truncated — rerun)"
    )
print("      PASS: PNG valid, width matches viewport, height matches probed page height")
PY

echo "DONE: ${OUT} (visual sanity check G6 still recommended: open/read the PNG top-to-bottom)"
