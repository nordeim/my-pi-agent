#!/bin/bash
#
# anchor-v2.sh - Enhanced Context Anchor with Full QMD Integration
# Version: 2.0.0 - Production Ready
#
# Recover context after compaction by scanning memory files and generating
# a comprehensive "here's where you are" briefing with semantic enhancement.
#

set -euo pipefail

# ─────────────────────────────────────────────────────────────────────────────
# Configuration
# ─────────────────────────────────────────────────────────────────────────────

WORKSPACE="${WORKSPACE:-$(cd "$(dirname "$0")/../../.." && pwd)}"
MEMORY_DIR="$WORKSPACE/memory"
CONTEXT_DIR="$WORKSPACE/context/active"
SNAPSHOT_DIR="$WORKSPACE/context/snapshots"

# Defaults
DAYS_BACK="${DAYS_BACK:-3}"
USE_SEMANTIC=false
QUICK_MODE=false
SAVE_SNAPSHOT=false

# Output modes
SHOW_ALL=true
SHOW_TASK=false
SHOW_ACTIVE=false
SHOW_DECISIONS=false
SHOW_LOOPS=false

# ─────────────────────────────────────────────────────────────────────────────
# Colors
# ─────────────────────────────────────────────────────────────────────────────

if [ -t 1 ]; then
    BOLD='\033[1m'; DIM='\033[2m'; RESET='\033[0m'
    BLUE='\033[34m'; GREEN='\033[32m'; YELLOW='\033[33m'
    CYAN='\033[36m'; MAGENTA='\033[35m'
else
    BOLD=''; DIM=''; RESET=''; BLUE=''; GREEN=''; YELLOW=''; CYAN=''; MAGENTA=''
fi

header() { echo -e "${BOLD}${BLUE}$1${RESET}"; echo -e "${DIM}───────────────────────────────────────────────────────────${RESET}"; }
section() { echo ""; echo -e "${BOLD}${CYAN}$1${RESET}"; echo -e "${DIM}───────────────────────────────────────────────────────────${RESET}"; }

relative_time() {
    local file="$1" now=$(date +%s) mod
    if [[ "$OSTYPE" == "darwin"* ]]; then mod=$(stat -f %m "$file" 2>/dev/null || echo 0)
    else mod=$(stat -c %Y "$file" 2>/dev/null || echo 0); fi
    local diff=$((now - mod))
    if [ $diff -lt 60 ]; then echo "just now"
    elif [ $diff -lt 3600 ]; then echo "$((diff / 60))m ago"
    elif [ $diff -lt 86400 ]; then echo "$((diff / 3600))h ago"
    else echo "$((diff / 86400))d ago"; fi
}

extract_date() {
    local p="$1"
    if [[ "$p" =~ /daily/([0-9]{4})/([0-9]{2})/([0-9]{2})\.md$ ]]; then echo "${BASH_REMATCH[1]}-${BASH_REMATCH[2]}-${BASH_REMATCH[3]}"
    else basename "$p" .md; fi
}

qmd_ok() { command -v qmd >/dev/null 2>&1 && [ "$QUICK_MODE" = false ] && [ "$USE_SEMANTIC" = true ]; }

semantic_expand() {
    local query="$1" depth="${2:-3}"
    if ! qmd_ok; then return 0; fi
    qmd query "$query" -c daily --limit "$depth" 2>/dev/null | grep -v "^Warning:" | grep -v "^Collection:" | head -$depth 2>/dev/null || true
}

get_daily_files() {
    local files=() seen=()
    for i in $(seq 0 $((DAYS_BACK - 1))); do
        local y m d
        if [[ "$OSTYPE" == "darwin"* ]]; then y=$(date -v-${i}d +%Y); m=$(date -v-${i}d +%m); d=$(date -v-${i}d +%d)
        else y=$(date -d "-$i days" +%Y); m=$(date -d "-$i days" +%m); d=$(date -d "-$i days" +%d); fi
        [[ " ${seen[@]:-} " =~ " ${y}-${m}-${d} " ]] && continue
        seen+=("${y}-${m}-${d}")
        if [ -f "$MEMORY_DIR/daily/$y/$m/$d.md" ]; then files+=("$MEMORY_DIR/daily/$y/$m/$d.md")
        elif [ -f "$MEMORY_DIR/${y}-${m}-${d}.md" ]; then files+=("$MEMORY_DIR/${y}-${m}-${d}.md"); fi
    done
    printf '%s\n' "${files[@]:-}"
}

# ─────────────────────────────────────────────────────────────────────────────
# Output Sections
# ─────────────────────────────────────────────────────────────────────────────

show_current_task() {
    section "📋 CURRENT TASK"
    local tf="$MEMORY_DIR/current-task.md"
    if [ -f "$tf" ]; then
        echo -e "${DIM}($(relative_time "$tf"))${RESET}"; echo ""; cat "$tf"
        if qmd_ok; then
            echo ""; echo -e "${DIM}Related via QMD:${RESET}"
            semantic_expand "$(head -3 "$tf")" 2 | sed 's/^/  └─ /' | sed "s/^/${DIM}/;s/$/${RESET}/" || true
        fi
    else echo -e "${DIM}No current task set${RESET}"; fi
    echo ""
}

show_active_context() {
    section "📂 ACTIVE CONTEXT FILES"
    if [ ! -d "$CONTEXT_DIR" ] || [ -z "$(ls -A "$CONTEXT_DIR" 2>/dev/null)" ]; then
        echo -e "${DIM}No active context files${RESET}"; echo ""; return; fi
    local found=false
    for f in "$CONTEXT_DIR"/*.md; do [ -e "$f" ] || continue; found=true
        local n=$(basename "$f") a=$(relative_time "$f")
        local p=$(head -n 4 "$f" 2>/dev/null | grep -v '^#' | grep . | head -n 1)
        echo -e "${GREEN}• ${n}${RESET} ${DIM}(${a})${RESET}"
        [ -n "$p" ] && echo -e "  ${DIM}└─ ${p:0:60}${RESET}"; done
    [ "$found" = false ] && echo -e "${DIM}No active files${RESET}"
    echo ""
}

show_decisions() {
    section "🎯 RECENT DECISIONS (last $DAYS_BACK days)"
    local files=($(get_daily_files)) found=false
    for f in "${files[@]}"; do [ -f "$f" ] || continue
        local d=$(extract_date "$f")
        grep -iE "(decision:|decided:|✅)" "$f" 2>/dev/null | while read -r line; do
            found=true; echo -e "${CYAN}[$d]${RESET} $line"; done; done
    [ "$found" = false ] && echo -e "${DIM}No decisions found${RESET}"
    echo ""
}

show_loops() {
    section "❓ OPEN LOOPS & TODO"
    local files=($(get_daily_files)) found=false
    for f in "${files[@]}"; do [ -f "$f" ] || continue
        local d=$(extract_date "$f")
        grep -E "(TODO:|FIXME:|Blocker:|Need to|\?$)" "$f" 2>/dev/null | grep -v "✅" | while read -r line; do
            found=true; echo -e "${YELLOW}[$d]${RESET} $line"; done; done
    [ "$found" = false ] && echo -e "${DIM}No open loops found${RESET}"
    echo ""
}

# ─────────────────────────────────────────────────────────────────────────────
# Snapshot & Main
# ─────────────────────────────────────────────────────────────────────────────

save_snapshot() {
    mkdir -p "$SNAPSHOT_DIR"
    local snap="$SNAPSHOT_DIR/$(date +%s)-context-snapshot.md"
    {
        echo "---"
        echo "anchor: v2.0"
        echo "timestamp: $(date -Iseconds)"
        echo "days_scanned: $DAYS_BACK"
        echo "semantic_mode: $USE_SEMANTIC"
        echo "---"
        echo ""
        echo "# Context Snapshot: $(date)"
        echo ""
        show_current_task
        show_active_context
        show_decisions
        show_loops
    } > "$snap" 2>/dev/null
    echo -e "${GREEN}Snapshot saved: ${snap#$WORKSPACE/}${RESET}"
}

show_help() {
    echo "anchor-v2.sh — Enhanced Context Anchor with QMD Integration"
    echo ""
    echo "Usage: anchor-v2.sh [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  --quick          Fast mode (skip QMD semantic search)"
    echo "  --semantic       Enable QMD semantic expansion (default: off)"
    echo "  --task           Show only current task"
    echo "  --active         Show only active context files"
    echo "  --decisions      Show only recent decisions"
    echo "  --loops          Show only open loops"
    echo "  --save           Save snapshot to context/snapshots/"
    echo "  --days N         Scan N days back (default: 3)"
    echo "  --help           Show this help"
}

# ─────────────────────────────────────────────────────────────────────────────
# Parse Arguments
# ─────────────────────────────────────────────────────────────────────────────

while [[ $# -gt 0 ]]; do case $1 in
    --quick) QUICK_MODE=true; shift;;
    --semantic) USE_SEMANTIC=true; shift;;
    --task) SHOW_ALL=false; SHOW_TASK=true; shift;;
    --active) SHOW_ALL=false; SHOW_ACTIVE=true; shift;;
    --decisions) SHOW_ALL=false; SHOW_DECISIONS=true; shift;;
    --loops) SHOW_ALL=false; SHOW_LOOPS=true; shift;;
    --save) SAVE_SNAPSHOT=true; shift;;
    --days) DAYS_BACK="$2"; shift 2;;
