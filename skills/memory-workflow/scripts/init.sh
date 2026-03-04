#!/bin/bash
# Memory Workflow Skill - Initialization Script
# Usage: ./init.sh [workspace_path]

set -e

WORKSPACE="${1:-$(pwd)}"
MEMORY_DIR="$WORKSPACE/memory"
HOT_DIR="$MEMORY_DIR/hot"
WARM_DIR="$MEMORY_DIR/warm"
COLD_DIR="$MEMORY_DIR/cold"

echo "🧠 Memory Workflow Skill - Initialization"
echo "=========================================="
echo ""

# Create directories
echo "📁 Creating directory structure..."
mkdir -p "$HOT_DIR" "$WARM_DIR" "$COLD_DIR"
echo "✅ Directories created"
echo ""

# Get current date
DATE=$(date +%Y-%m-%d)

# Create HOT_MEMORY.md if not exists
if [ ! -f "$HOT_DIR/HOT_MEMORY.md" ]; then
    echo "📝 Creating HOT_MEMORY.md..."
    cat > "$HOT_DIR/HOT_MEMORY.md" << EOF
# 🔥 HOT MEMORY - Current Session Context

> Last updated: $DATE
> Update frequency: Every session
> Management: Aggressively prune completed tasks

---

## 🎯 Active Tasks

### Project 1
- **Status**: 
- **Today**:
  - [ ] 

---

## 📝 Current Context

- **Date**: $DATE
- **Session type**: 
- **Current topic**: 

## ⚡ Temporary Information

- None

---

*This file is updated every session, keeping only active information*
EOF
    echo "✅ HOT_MEMORY.md created"
else
    echo "⚠️  HOT_MEMORY.md already exists"
fi

echo ""

# Create WARM_MEMORY.md if not exists
if [ ! -f "$WARM_DIR/WARM_MEMORY.md" ]; then
    echo "📝 Creating WARM_MEMORY.md..."
    cat > "$WARM_DIR/WARM_MEMORY.md" << EOF
# 🌡️ WARM MEMORY - Stable Preferences

> Last updated: $DATE
> Update frequency: When preferences change
> Management: Long-term retention

---

## 👤 User Profile

| Field | Value |
|-------|-------|
| Name | |
| Timezone | |
| Communication style | |

---

## 🛠️ System Configuration

### Installed Skills
- memory-workflow

### API Keys (reference locations)
- See TOOLS.md

---

## 📋 Project List

| Project | Status | Key File |
|---------|--------|----------|
| | | PROJECT_INDEX.md |

---

## 🔗 Quick Links

- PROJECT_INDEX.md
- MEMORY.md

---

*This file records stable configurations, updated only when changes occur*
EOF
    echo "✅ WARM_MEMORY.md created"
else
    echo "⚠️  WARM_MEMORY.md already exists"
fi

echo ""

# Create PROJECT_INDEX.md if not exists
if [ ! -f "$WORKSPACE/PROJECT_INDEX.md" ]; then
    echo "📝 Creating PROJECT_INDEX.md..."
    cat > "$WORKSPACE/PROJECT_INDEX.md" << EOF
# PROJECT_INDEX - Quick Reference

> Auto-read every session
> Last updated: $DATE

---

## 🏥 Project 1

### Core Info
| Field | Value |
|-------|-------|
| Name | |
| Website | |
| GitHub | |

### Key Pages
| Page | URL | Status |
|------|-----|--------|
| | | |

### This Week's Todos
- [ ] 

### Completed This Week
- [x] 

---

*This file is auto-read every session to ensure latest project status*
EOF
    echo "✅ PROJECT_INDEX.md created"
else
    echo "⚠️  PROJECT_INDEX.md already exists"
fi

echo ""

# Update AGENTS.md
AGENTS_FILE="$WORKSPACE/AGENTS.md"
if [ -f "$AGENTS_FILE" ]; then
    echo "📝 Checking AGENTS.md..."
    if ! grep -q "HOT_MEMORY.md" "$AGENTS_FILE"; then
        echo "⚠️  AGENTS.md doesn't have memory-workflow rules"
        echo "   Please manually add the Every Session rules from SKILL.md"
    else
        echo "✅ AGENTS.md already has memory-workflow rules"
    fi
else
    echo "⚠️  AGENTS.md not found"
fi

echo ""

# Create today's daily log
TODAY_LOG="$MEMORY_DIR/$DATE.md"
if [ ! -f "$TODAY_LOG" ]; then
    echo "📝 Creating today's log: $DATE.md..."
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
    echo "✅ Daily log created"
else
    echo "⚠️  Daily log already exists"
fi

echo ""
echo "=========================================="
echo "✅ Initialization complete!"
echo ""
echo "Next steps:"
echo "1. Update WARM_MEMORY.md with your preferences"
echo "2. Update PROJECT_INDEX.md with your projects"
echo "3. Run 'morning-review' to start daily workflow"
echo ""
