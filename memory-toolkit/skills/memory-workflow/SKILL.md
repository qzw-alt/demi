---
name: memory-workflow
description: Complete memory management workflow with HOT/WARM/COLD tiering, morning review, and project indexing. Automatically organizes context and prepares for daily work.
version: 1.0.0
author: demi-xA1b2
---

# Memory Workflow Skill 🧠⚡

A comprehensive memory management system that implements:
- **Three-tier memory architecture** (HOT/WARM/COLD)
- **Automatic morning review** (daily memory recap)
- **Project indexing** (quick project status lookup)
- **Memory tiering** (automated context organization)

## Installation

```bash
# Copy to your skills directory
cp -r memory-workflow ~/.openclaw/workspace/skills/

# Or use clawhub
clawhub install memory-workflow
```

## Quick Start

### 1. Initialize the workflow

```bash
# Run initialization
openclaw skill memory-workflow init
```

This creates:
- `memory/hot/HOT_MEMORY.md` - Active tasks
- `memory/warm/WARM_MEMORY.md` - Stable preferences
- `PROJECT_INDEX.md` - Project quick reference

### 2. Daily morning review

```bash
# Manual trigger
openclaw skill memory-workflow morning-review

# Or wait for automatic cron job (06:30 daily)
```

### 3. Organize memory tiers

```bash
# Organize context across tiers
openclaw skill memory-workflow organize
```

## Architecture

### Three-Tier Memory System

```
┌─────────────────────────────────────────┐
│  🔥 HOT (memory/hot/)                   │
│  • Current session context              │
│  • Active tasks                         │
│  • Temporary information                │
│  • Updated: Every session               │
├─────────────────────────────────────────┤
│  🌡️ WARM (memory/warm/)                 │
│  • User preferences                     │
│  • Stable configurations                │
│  • Common tools & workflows             │
│  • Updated: When preferences change     │
├─────────────────────────────────────────┤
│  ❄️ COLD (MEMORY.md)                    │
│  • Long-term archive                    │
│  • Historical decisions                 │
│  • Project milestones                   │
│  • Updated: Weekly review               │
└─────────────────────────────────────────┘
```

## File Structure

```
workspace/
├── memory/
│   ├── hot/
│   │   └── HOT_MEMORY.md          # Active tasks
│   ├── warm/
│   │   └── WARM_MEMORY.md         # Stable preferences
│   ├── cold/                      # (optional) Archived memories
│   └── YYYY-MM-DD.md              # Daily logs
├── PROJECT_INDEX.md               # Project quick reference
├── MEMORY.md                      # Long-term memory
└── AGENTS.md                      # Auto-load rules (updated by skill)
```

## Commands

### `init` - Initialize workflow

Creates all necessary files and directories.

```bash
openclaw skill memory-workflow init
```

### `morning-review` - Daily memory recap

Performs morning memory review:
1. Reads HOT/WARM/PROJECT_INDEX
2. Checks yesterday's work log
3. Generates today's todo summary
4. Updates active tasks

```bash
openclaw skill memory-workflow morning-review
```

### `organize` - Organize memory tiers

Redistributes context across tiers:
- Move completed tasks from HOT to COLD
- Update WARM with new preferences
- Archive old daily logs

```bash
openclaw skill memory-workflow organize
```

### `update-index` - Update project index

Synchronizes PROJECT_INDEX.md with current project status.

```bash
openclaw skill memory-workflow update-index
```

## Templates

### HOT_MEMORY.md Template

```markdown
# 🔥 HOT MEMORY - Current Session Context

> Last updated: {{date}}
> Update frequency: Every session

## 🎯 Active Tasks

### Project 1
- **Status**: In progress
- **Today**: 
  - [ ] Task 1
  - [ ] Task 2

### Project 2
- **Status**: Pending
- **Today**:
  - [ ] Task 3

## 📝 Current Context

- **Date**: {{date}}
- **Session type**: Main session
- **Current topic**: 

## ⚡ Temporary Information

- None

---
*This file is updated every session, keeping only active information*
```

### WARM_MEMORY.md Template

```markdown
# 🌡️ WARM MEMORY - Stable Preferences

> Last updated: {{date}}
> Update frequency: When preferences change

## 👤 User Profile

| Field | Value |
|-------|-------|
| Name | {{user_name}} |
| Timezone | {{timezone}} |
| Communication style | Direct, efficient |

## 🛠️ System Configuration

### Installed Skills
- memory-workflow
- web-search
- (your other skills)

### API Keys (reference locations)
- Service A: TOOLS.md
- Service B: TOOLS.md

## 📋 Project List

| Project | Status | Key File |
|---------|--------|----------|
| Project 1 | Active | PROJECT_INDEX.md |

## 🔗 Quick Links

- PROJECT_INDEX.md
- MEMORY.md

---
*This file records stable configurations, updated only when changes occur*
```

### PROJECT_INDEX.md Template

```markdown
# PROJECT_INDEX - Quick Reference

> Auto-read every session
> Last updated: {{date}}

## 🏥 Project 1

### Core Info
| Field | Value |
|-------|-------|
| Website | https://... |
| GitHub | https://... |

### Key Pages
| Page | URL | Status |
|------|-----|--------|
| Home | / | ✅ Live |

### This Week's Todos
- [ ] Task 1
- [ ] Task 2

### Completed This Week
- [x] Task 3

---
*This file is auto-read every session to ensure latest project status*
```

## Cron Job Setup

The skill automatically sets up a morning review cron job:

```bash
# Daily at 06:30 (GMT+8)
openclaw cron add \
  --name "morning-memory-review" \
  --cron "0 30 22 * * *" \
  --message "Execute morning memory review" \
  --skill memory-workflow
```

## Integration with AGENTS.md

The skill updates AGENTS.md to include automatic memory loading:

```markdown
## Every Session

Before doing anything else:

1. Read `SOUL.md`
2. Read `USER.md`
3. Read `memory/hot/HOT_MEMORY.md`
4. Read `memory/warm/WARM_MEMORY.md`
5. Read `PROJECT_INDEX.md`
6. Read `memory/YYYY-MM-DD.md` (today + yesterday)
7. **If in MAIN SESSION**: Also read `MEMORY.md`
```

## Best Practices

### Daily Workflow

1. **Morning**: Review automatic morning summary
2. **During work**: Update HOT_MEMORY.md with active tasks
3. **End of day**: Update daily log and PROJECT_INDEX.md
4. **Weekly**: Run `organize` to archive completed tasks

### Memory Updates

**Update HOT when**:
- Starting new task
- Task status changes
- Context switches

**Update WARM when**:
- Preferences change
- New skills installed
- Workflow changes

**Update COLD when**:
- Project completed
- Major milestone reached
- Weekly review

## Troubleshooting

### "Memory files not found"

Run initialization:
```bash
openclaw skill memory-workflow init
```

### "Morning review not running"

Check cron status:
```bash
openclaw cron list
openclaw cron status
```

### "Context too long"

Organize memory tiers:
```bash
openclaw skill memory-workflow organize
```

## Version History

- **v1.0.0** (2026-03-04)
  - Initial release
  - Three-tier memory architecture
  - Morning review automation
  - Project indexing

## License

MIT License - Feel free to modify and share!

## Credits

Created by Demi (demi-xA1b2) based on best practices from Moltbook and OpenClaw community.
