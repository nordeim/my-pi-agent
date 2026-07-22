#!/bin/bash
# Memory Architecture Health Check
# Validates all three layers: Workspace files, LCM, QMD

echo "=== OpenClaw Memory Architecture Health Check ==="
echo "Date: $(date '+%Y-%m-%d %H:%M:%S %Z')"
echo ""

ERRORS=0
WARNINGS=0

echo "--- Layer 1: Workspace Files ---"

if [ -f ~/.openclaw/workspace/MEMORY.md ]; then
    SIZE=$(du -h ~/.openclaw/workspace/MEMORY.md | cut -f1)
    echo "  ✅ MEMORY.md exists ($SIZE)"
else
    echo "  ❌ MEMORY.md MISSING"
    ((ERRORS++))
fi

TODAY=$(date +%Y/%m/%d)
TODAY_FILE=~/.openclaw/workspace/memory/daily/$TODAY.md
if [ -f "$TODAY_FILE" ]; then
    echo "  ✅ Today's daily note exists"
else
    echo "  ⚠️  Today's daily note missing: memory/daily/$TODAY.md"
    ((WARNINGS++))
fi

# Check for old flat files that should be migrated
OLD_FLAT=$(find ~/.openclaw/workspace/memory/ -maxdepth 1 -name "20[0-9][0-9]-*.md" 2>/dev/null | wc -l)
if [ "$OLD_FLAT" -gt 0 ]; then
    echo "  ⚠️  $OLD_FLAT old flat memory files found (should migrate to daily/)"
    ((WARNINGS++))
else
    echo "  ✅ No old flat files (migration complete)"
fi

# Count daily notes
DAILY_COUNT=$(find ~/.openclaw/workspace/memory/daily/ -name "*.md" -not -name "_context.yml" 2>/dev/null | wc -l)
echo "  ℹ️  Daily notes: $DAILY_COUNT files"

echo ""
echo "--- Layer 2: LCM (Lossless Context Management) ---"

# Check plugin
LCM_PLUGIN=$(openclaw plugins list 2>/dev/null | grep -i "lossless" | head -1)
if [ -n "$LCM_PLUGIN" ]; then
    echo "  ✅ LCM plugin installed"
else
    echo "  ❌ LCM plugin NOT FOUND"
    ((ERRORS++))
fi

# Check context engine slot
if grep -q '"contextEngine".*"lossless-claw"' ~/.openclaw/openclaw.json 2>/dev/null; then
    echo "  ✅ Context engine slot: lossless-claw"
else
    echo "  ❌ Context engine slot NOT SET to lossless-claw"
    ((ERRORS++))
fi

# Check database
if [ -f ~/.openclaw/lcm.db ]; then
    SIZE=$(du -h ~/.openclaw/lcm.db | cut -f1)
    MSG_COUNT=$(sqlite3 ~/.openclaw/lcm.db "SELECT COUNT(*) FROM messages;" 2>/dev/null || echo "?")
    SUM_COUNT=$(sqlite3 ~/.openclaw/lcm.db "SELECT COUNT(*) FROM summaries;" 2>/dev/null || echo "?")
    echo "  ✅ LCM database exists ($SIZE, $MSG_COUNT messages, $SUM_COUNT summaries)"
else
    echo "  ❌ LCM database MISSING (~/.openclaw/lcm.db)"
    ((ERRORS++))
fi

# Check session idle
IDLE=$(grep -o '"idleMinutes":[[:space:]]*[0-9]*' ~/.openclaw/openclaw.json 2>/dev/null | grep -o '[0-9]*')
if [ -n "$IDLE" ]; then
    DAYS=$((IDLE / 1440))
    if [ "$IDLE" -ge 10080 ]; then
        echo "  ✅ Session idle: $IDLE min ($DAYS days)"
    else
        echo "  ⚠️  Session idle: $IDLE min ($DAYS days) — consider 10080 (7 days)"
        ((WARNINGS++))
    fi
else
    echo "  ⚠️  Session idleMinutes not set"
    ((WARNINGS++))
fi

echo ""
echo "--- Layer 3: QMD (Semantic Search) ---"

if command -v qmd &>/dev/null; then
    echo "  ✅ QMD binary: $(which qmd)"

    QMD_STATUS=$(qmd status 2>/dev/null)
    if [ -n "$QMD_STATUS" ]; then
        FILES=$(echo "$QMD_STATUS" | grep "Total:" | grep -o '[0-9]* files' || echo "")
        VECTORS=$(echo "$QMD_STATUS" | grep "Vectors:" | grep -o '[0-9]* embedded' || echo "")
        UPDATED=$(echo "$QMD_STATUS" | grep "Updated:" | grep -o '[0-9]*d ago\|never' || echo "unknown")
        echo "  ✅ QMD index: $FILES, $VECTORS (updated $UPDATED)"

        # Check if index is stale (> 2 days)
        STALE_DAYS=$(echo "$UPDATED" | grep -o '[0-9]*' | head -1)
        if [ -n "$STALE_DAYS" ] && [ "$STALE_DAYS" -gt 2 ]; then
            echo "  ⚠️  QMD index is $STALE_DAYS days old — run: qmd update && qmd embed"
            ((WARNINGS++))
        fi
    else
        echo "  ❌ QMD status failed"
        ((ERRORS++))
    fi
else
    echo "  ⚠️  QMD not installed (memory_search may still work via built-in provider)"
    ((WARNINGS++))
fi

# Check built-in memory index
BUILTIN_DB=~/.openclaw/memory/main.sqlite
if [ -f "$BUILTIN_DB" ]; then
    CHUNKS=$(sqlite3 "$BUILTIN_DB" "SELECT COUNT(*) FROM chunks;" 2>/dev/null || echo "?")
    if [ "$CHUNKS" = "0" ]; then
        echo "  ℹ️  Built-in memory index: 0 chunks (QMD may be primary backend)"
    else
        echo "  ✅ Built-in memory index: $CHUNKS chunks"
    fi
fi

echo ""
echo "--- Summary ---"
echo "  Errors: $ERRORS"
echo "  Warnings: $WARNINGS"

if [ $ERRORS -eq 0 ] && [ $WARNINGS -eq 0 ]; then
    echo "  Status: ✅ All systems healthy"
elif [ $ERRORS -eq 0 ]; then
    echo "  Status: ⚠️  Functional with warnings"
else
    echo "  Status: ❌ Issues need attention"
fi

echo ""
echo "=== Done ==="
