#!/bin/bash
# Memory Workflow Skill - Organize Memory Tiers
# Usage: ./organize.sh [workspace_path]

set -e

WORKSPACE="${1:-$(pwd)}"
MEMORY_DIR="$WORKSPACE/memory"
HOT_FILE="$MEMORY_DIR/hot/HOT_MEMORY.md"
WARM_FILE="$MEMORY_DIR/warm/WARM_MEMORY.md"
COLD_FILE="$WORKSPACE/MEMORY.md"

echo "🧹 Organizing Memory Tiers"
echo "=========================="
echo ""

DATE=$(date +%Y-%m-%d)

# 1. Check HOT for completed tasks
echo "🔥 Checking HOT_MEMORY.md for completed tasks..."

if [ -f "$HOT_FILE" ]; then
    COMPLETED_TASKS=$(grep -E "^- \[x\]" "$HOT_FILE" || true)
    
    if [ -n "$COMPLETED_TASKS" ]; then
        echo "Found completed tasks:"
        echo "$COMPLETED_TASKS"
        echo ""
        echo "📝 Archiving to COLD memory..."
        
        # Append to MEMORY.md
        if [ -f "$COLD_FILE" ]; then
            echo "" >> "$COLD_FILE"
            echo "## Archived from HOT - $DATE" >> "$COLD_FILE"
            echo "" >> "$COLD_FILE"
            echo "Completed tasks:" >> "$COLD_FILE"
            echo "$COMPLETED_TASKS" >> "$COLD_FILE"
            echo "✅ Archived to MEMORY.md"
        fi
        
        # Remove completed tasks from HOT
        sed -i '/^- \[x\]/d' "$HOT_FILE"
        echo "✅ Removed completed tasks from HOT"
    else
        echo "No completed tasks to archive"
    fi
else
    echo "⚠️  HOT_MEMORY.md not found"
fi

echo ""

# 2. Archive old daily logs (older than 7 days)
echo "📁 Archiving old daily logs..."

ARCHIVE_COUNT=0
for log in "$MEMORY_DIR"/2026-*.md; do
    if [ -f "$log" ]; then
        LOG_DATE=$(basename "$log" .md)
        LOG_TIMESTAMP=$(date -d "$LOG_DATE" +%s 2>/dev/null || date -j -f "%Y-%m-%d" "$LOG_DATE" +%s)
        CURRENT_TIMESTAMP=$(date +%s)
        DAYS_OLD=$(( (CURRENT_TIMESTAMP - LOG_TIMESTAMP) / 86400 ))
        
        if [ $DAYS_OLD -gt 7 ]; then
            echo "   Archiving: $LOG_DATE ($DAYS_OLD days old)"
            mkdir -p "$MEMORY_DIR/cold"
            mv "$log" "$MEMORY_DIR/cold/"
            ARCHIVE_COUNT=$((ARCHIVE_COUNT + 1))
        fi
    fi
done

if [ $ARCHIVE_COUNT -gt 0 ]; then
    echo "✅ Archived $ARCHIVE_COUNT old logs to memory/cold/"
else
    echo "No old logs to archive"
fi

echo ""

# 3. Summary
echo "=========================="
echo "✅ Memory organization complete!"
echo ""
echo "Current state:"
echo "  🔥 HOT: Active tasks"
echo "  🌡️  WARM: Stable preferences"
echo "  ❄️  COLD: Archived memories"
echo ""
