#!/bin/bash
#
# context-anchor: Recover context after compaction
# Scans memory files and generates a "here's where you are" briefing
# Supports QMD hierarchical (daily/YYYY/MM/DD.md) and flat (YYYY-MM-DD.md)
# NEW: QMD semantic integration for enhanced context recovery
#
set -e

WORKSPACE="${WORKSPACE:-$(cd "$(dirname "$0")/../../.." && pwd)}"
MEMORY_DIR="$WORKSPACE/memory"
CONTEXT_DIR="$WORKSPACE/context/active"
DAYS_BACK="${DAYS_BACK:-2}"
USE_SEMANTIC=false
SEMANTIC_DEPTH=3
QUICK_MODE=false

if [ -t 1 ]; then
    BOLD='\033[1m'; DIM='\033[2m'; RESET='\033[0m'
    BLUE='\033[34m'; GREEN='\033[32m'; YELLOW='\033[33m'
    CYAN='\033[36m'; MAGENTA='\033[35m'
else
    BOLD=''; DIM=''; RESET=''; BLUE=''; GREEN=''; YELLOW=''; CYAN=''; MAGENTA=''
fi

SHOW_ALL=true; SHOW_TASK=false; SHOW_ACTIVE=false; SHOW_DECISIONS=false; SHOW_LOOPS=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --quick) QUICK_MODE=true; shift ;;
        --semantic) USE_SEMANTIC=true; [[ "$2" =~ ^[0-9]+$ ]] && { SEMANTIC_DEPTH="$2"; shift; }; shift ;;
        --task) SHOW_ALL=false; SHOW_TASK=true; shift ;;
        --active) SHOW_ALL=false; SHOW_ACTIVE=true; shift ;;
        --decisions) SHOW_ALL=false; SHOW_DECISIONS=true; shift ;;
        --loops) SHOW_ALL=false; SHOW_LOOPS=true; shift ;;
        --days) DAYS_BACK="$2"; shift 2 ;;
        --help|-h)
            echo "Usage: anchor.sh [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  --quick              Skip QMD semantic expansion (fast mode)"
            echo "  --semantic [N]       Include QMD expansion (depth N, default: 3)"
            echo "  --task               Show only current task"
            echo "  --active             Show only active context files"
            echo "  --decisions          Show only recent decisions"
            echo "  --loops              Show only open loops"
            echo "  --days N             Scan N days back (default: 2)"
            echo ""
            echo "QMD Integration: Both systems work together for faster, deeper context"
            exit 0
            ;;
        *) echo "Unknown option: $1"; exit 1 ;;
    esac
done

header() { echo -e "${BOLD}${BLUE}$1${RESET}"; echo -e "${DIM}───────────────────────────────────────────────────────────${RESET}"; }

relative_time() {
    local file="$1"
    local now=$(date +%s)
    local mod
    if [[ "$OSTYPE" == "darwin"* ]]; then mod=$(stat -f %m "$file" 2>/dev/null || echo 0)
    else mod=$(stat -c %Y "$file" 2>/dev/null || echo 0); fi
    local diff=$((now - mod))
    if [ $diff -lt 60 ]; then echo "just now"
    elif [ $diff -lt 3600 ]; then echo "$((diff / 60))m ago"
    elif [ $diff -lt 86400 ]; then echo "$((diff / 3600))h ago"
    else echo "$((diff / 86400))d ago"; fi
}

extract_date_from_path() {
    local filepath="$1"
    if [[ "$filepath" =~ /daily/([0-9]{4})/([0-9]{2})/([0-9]{2})\.md$ ]]; then
        echo "${BASH_REMATCH[1]}-${BASH_REMATCH[2]}-${BASH_REMATCH[3]}"
    elif [[ "$(basename "$filepath" .md)" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}$ ]]; then
        basename "$filepath" .md
    else basename "$filepath" .md; fi
}

qmd_available() { command -v qmd >/dev/null 2>&1; }

semantic_expand() {
    local topic="$1" depth="${2:-3}" collection="${3:-daily}"
    if ! qmd_available || [ "$QUICK_MODE" = true ]; then return 0; fi
    qmd query "$topic" -c "$collection" --limit "$depth" 2>/dev/null | \
        grep -v "^Warning:" | head -$((depth * 3)) | grep -E "[a-zA-Z]" | head -$depth || true
}

get_daily_files() {
    local files=() seen_dates=()
    for i in $(seq 0 $((DAYS_BACK - 1))); do
        if [[ "$OSTYPE" == "darwin"* ]]; then
            local year=$(date -v-${i}d +%Y) month=$(date -v-${i}d +%m) day=$(date -v-${i}d +%d)
        else
            local year=$(date -d "-$i days" +%Y) month=$(date -d "-$i days" +%m) day=$(date -d "-$i days" +%d)
        fi
        [[ " ${seen_dates[@]} " =~ " ${year}-${month}-${day}" ]] && continue
        seen_dates+=("${year}-${month}-${day}")
        local qmd_file="$MEMORY_DIR/daily/$year/$month/$day.md"
        if [ -f "$qmd_file" ]; then files+=("$qmd_file"); continue; fi
        local flat_file="$MEMORY_DIR/${year}-${month}-${day}.md"
        [ -f "$flat_file" ] && files+=("$flat_file")
    done
    echo "${files[@]}"
}

show_current_task() {
    header "📋 CURRENT TASK"
    local task_file="$MEMORY_DIR/current-task.md"
    if [ -f "$task_file" ]; then
        echo -e "${DIM}($(relative_time "$task_file"))${RESET}"
        echo ""; cat "$task_file"
        if [ "$USE_SEMANTIC" = true ]; then
            echo ""; echo -e "${DIM}Related via QMD:${RESET}"
            semantic_expand "$(head -3 "$task_file")" 2 | sed 's/^/ └─ /' | sed "s/^/${DIM}/;s/$/${RESET}/" || true
        fi
    else echo -e "${DIM}No current task set${RESET}"; fi
    echo ""
}

show_active_context() {
    header "📂 ACTIVE CONTEXT FILES"
    [ -d "$CONTEXT_DIR" ] || { echo -e "${DIM}No context/active/ directory${RESET}"; echo ""; return; }
    local found=false
    for file in "$CONTEXT_DIR"/*.md; do
        [ -e "$file" ] || continue; found=true
        local name=$(basename "$file") age=$(relative_time "$file")
        local preview=$(head -n 5 "$file" | grep -v '^#' | grep -v '^$' | head -n 1)
        echo -e "${GREEN}• ${name}${RESET} ${DIM}(${age})${RESET}"
        [ -n "$preview" ] && echo -e " ${DIM}└─ ${preview:0:70}...${RESET}"
    done
    [ "$found" = false ] && echo -e "${DIM}No active context files${RESET}"
    echo ""
}

show_decisions() {
    header "🎯 RECENT DECISIONS (last $DAYS_BACK days)"
    local files=($(get_daily_files)) found=false
    for file in "${files[@]}"; do
        local date=$(extract_date_from_path "$file")
        grep -n -i -E "(^|\s)(decision:|decided:|chose:|picked:|went with|✅.*completed|✅.*done)" "$file" 2>/dev/null | \
        while IFS= read -r line; do
            found=true
            local content=$(echo "$line" | sed 's/^[0-9]*://; s/^[ -]*//')
            echo -e "${CYAN}[$date]${RESET} $content"
            if [ "$USE_SEMANTIC" = true ]; then
                local related=$(semantic_expand "$content" 2)
                [ -n "$related" ] && echo -e "${DIM} └─ Related: $(echo "$related" | head -1)${RESET}"
            fi
        done
    done
    [ "$found" = false ] && echo -e "${DIM}No explicit decisions found${RESET}"
    echo ""
}

show_loops() {
    header "❓ OPEN LOOPS & TODO"
    local files=($(get_daily_files)) found=false
    for file in "${files[@]}"; do
        local date=$(extract_date_from_path "$file")
        grep -n -E "(^|\s)(\?$|TODO:|FIXME:|Blocker:|Need to|needs to|should|waiting for|- \[ \])" "$file" 2>/dev/null | \
        grep -v -E "(✅|\[x\]|\[X\])" | while IFS= read -r line; do
            found=true
            local content=$(echo "$line" | sed 's/^[0-9]*://; s/^[ -]*//')
            echo -e "${YELLOW}[$date]${RESET} $content"
        done
    done
    [ "$found" = false ] && echo -e "${DIM}No obvious open loops found${RESET}"
    echo ""
}

write_snapshot() {
    local snapshot_file="$CONTEXT_DIR/$(date +%s)-anchor-snapshot.md"
    local decisions=$(grep -c -i -E "(decision:|decided:|✅)" "$MEMORY_DIR/daily/"/*/*/*/ 2>/dev/null || echo 0)
    local loops=$(grep -c -E "(TODO:|FIXME:|Blocker:)" "$MEMORY_DIR/daily/"/*/*/*/ 2>/dev/null || echo 0)
    
    cat > "$snapshot_file" << EOF
---
anchor: true
timestamp: $(date -Iseconds)
days_scanned: $DAYS_BACK
decisions_found: $decisions
open_loops: $loops
semantic_mode: $USE_SEMANTIC
---
# Context Snapshot: $(date "+%Y-%m-%d %H:%M")

##