#!/bin/bash
# Memory Workflow Skill - Morning Review Script
# Usage: ./morning-review.sh [workspace_path]

set -e

WORKSPACE="${1:-$(pwd)}"
MEMORY_DIR="$WORKSPACE/memory"
HOT_FILE="$MEMORY_DIR/hot/HOT_MEMORY.md"
WARM_FILE="$MEMORY_DIR/warm/WARM_MEMORY.md"
PROJECT_INDEX="$WORKSPACE/PROJECT_INDEX.md"

echo "🌅 Morning Memory Review"
echo "========================"
echo ""

DATE=$(date +%Y-%m-%d)
YESTERDAY=$(date -d "yesterday" +%Y-%m-%d 2>/dev/null || date -v-1d +%Y-%m-%d)

# 1. Read core memory files
echo "📖 Reading core memory files..."
echo ""

if [ -f "$HOT_FILE" ]; then
    echo "✅ HOT_MEMORY.md loaded"
else
    echo "⚠️  HOT_MEMORY.md not found, run init first"
fi

if [ -f "$WARM_FILE" ]; then
    echo "✅ WARM_MEMORY.md loaded"
else
    echo "⚠️  WARM_MEMORY.md not found, run init first"
fi

if [ -f "$PROJECT_INDEX" ]; then
    echo "✅ PROJECT_INDEX.md loaded"
else
    echo "⚠️  PROJECT_INDEX.md not found, run init first"
fi

echo ""

# 2. Check yesterday's work
echo "📅 Checking yesterday's work ($YESTERDAY)..."
YESTERDAY_LOG="$MEMORY_DIR/$YESTERDAY.md"

if [ -f "$YESTERDAY_LOG" ]; then
    echo "✅ Yesterday's log found"
    echo ""
    echo "📊 Yesterday's completed tasks:"
    grep -E "^- \[x\]" "$YESTERDAY_LOG" | head -5 || echo "   No completed tasks recorded"
    echo ""
else
    echo "⚠️  Yesterday's log not found"
    echo ""
fi

# 3. Check today's todos
echo "🎯 Today's todos ($DATE):"
TODAY_LOG="$MEMORY_DIR/$DATE.md"

if [ -f "$TODAY_LOG" ]; then
    grep -E "^- \[ \]" "$TODAY_LOG" | head -5 || echo "   No todos for today"
else
    echo "   Creating today's log..."
    cat > "$TODAY_LOG" << EOF
# $DATE Work Log

## 🎯 Goals
- 

## 📥 Input
- 

## 🔄 Process
- 

## 📤 Output
- 

## 🔜 Next Steps
- 
EOF
    echo "   ✅ Today's log created"
fi

echo ""

# 4. Extract active projects from PROJECT_INDEX
echo "🏥 Active Projects:"
if [ -f "$PROJECT_INDEX" ]; then
    grep -E "^## " "$PROJECT_INDEX" | head -5 || echo "   No projects found"
else
    echo "   PROJECT_INDEX.md not available"
fi

echo ""

# 5. Generate summary
echo "========================"
echo "📝 Morning Review Summary"
echo "========================"
echo ""
echo "Date: $DATE"
echo ""
echo "📊 Yesterday ($YESTERDAY):"
if [ -f "$YESTERDAY_LOG" ]; then
    COMPLETED=$(grep -c "^- \[x\]" "$YESTERDAY_LOG" 2>/dev/null || echo "0")
    echo "   Completed tasks: $COMPLETED"
else
    echo "   No data"
fi

echo ""
echo "🎯 Today ($DATE):"
if [ -f "$TODAY_LOG" ]; then
    TODOS=$(grep -c "^- \[ \]" "$TODAY_LOG" 2>/dev/null || echo "0")
    echo "   Pending tasks: $TODOS"
else
    echo "   Log created"
fi

echo ""
echo "✅ Morning review complete!"
echo "🚀 Ready to start today's work"
echo ""

# Update HOT_MEMORY.md with today's focus
echo "📝 Updating HOT_MEMORY.md..."
if [ -f "$HOT_FILE" ]; then
    # Update the date
    sed -i "s/> Last updated: .*/> Last updated: $DATE/" "$HOT_FILE"
    echo "✅ HOT_MEMORY.md updated"
fi

echo ""
