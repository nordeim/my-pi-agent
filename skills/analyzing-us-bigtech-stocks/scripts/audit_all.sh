#!/usr/bin/env bash
# audit_all.sh — run both Phase 10 delivery gates with one command.
#
# Why: the numeric audit (python3) and the render audit (node + Playwright)
# are separate commands with different runtimes and prerequisites; an agent
# under instruction-following pressure can "forget" the second one. This
# wrapper makes the gate one command with a single combined exit code
# (report-5 finding L-2). Fix failures in the brief/generator, never by
# nudging the rendered HTML, then re-run until clean.
#
# Usage:
#   bash scripts/audit_all.sh <slides_dir> <fact_base.json> [<checks.json>]
#     <slides_dir>     directory containing slide_NN.html
#     <fact_base.json> the fact base (fact-base mode; required)
#     <checks.json>    optional per-slide needle checks, run in addition
#
# Strict compliance modes (institutional builds) are passed through via the
# STRICT environment variable:
#   STRICT=1 bash scripts/audit_all.sh ...   # adds --strict-verified
#                                           #     --fail-on-unverified
#
# Exit codes: 0 all gates clean, 1 at least one gate failed,
#             2 usage error (missing/extra arguments).
set -uo pipefail

if [ $# -lt 2 ] || [ $# -gt 3 ]; then
  echo "usage: audit_all.sh <slides_dir> <fact_base.json> [<checks.json>]" >&2
  exit 2
fi
SLIDES="$1"
FB="$2"
CHECKS="${3:-}"
HERE="$(cd "$(dirname "$0")" && pwd)"

STRICT_FLAGS=()
if [ "${STRICT:-0}" = "1" ]; then
  STRICT_FLAGS=(--strict-verified --fail-on-unverified)
fi

rc=0

if [ -n "$FB" ]; then
  echo "=== numeric + placeholder audit (fact-base mode) ==="
  python3 "$HERE/fact_base_audit.py" --slides "$SLIDES" --fact-base "$FB" \
    "${STRICT_FLAGS[@]}" || rc=1
fi

if [ -n "$CHECKS" ]; then
  echo "=== per-slide needle checks ==="
  python3 "$HERE/fact_base_audit.py" --slides "$SLIDES" --checks "$CHECKS" \
    "${STRICT_FLAGS[@]}" || rc=1
fi

echo "=== render/overflow audit (1280x720, headless Chromium) ==="
node "$HERE/overflow_audit.mjs" --dir "$SLIDES" || rc=1

echo "=== audit_all: $( [ $rc -eq 0 ] && echo 'ALL GATES CLEAN' || echo 'GATE FAILURE — fix the brief/generator and re-run' ) ==="
exit $rc
