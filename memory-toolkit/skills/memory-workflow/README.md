# 🧠 Memory Workflow Skill

> A comprehensive memory management system for AI agents with three-tier architecture, morning review automation, and project indexing.
> 
> Created by [Demi](https://github.com/qzw-alt) • 2026

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](./)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](./LICENSE)
[![OpenClaw](https://img.shields.io/badge/OpenClaw-Compatible-orange.svg)](https://openclaw.ai)

---

## ✨ Features

### 🔥 Three-Tier Memory Architecture

```
┌─────────────────────────────────────────┐
│  🔥 HOT (memory/hot/)                   │
│  • Current active tasks                 │
│  • Temporary information                │
│  • Updated: Every session               │
├─────────────────────────────────────────┤
│  🌡️ WARM (memory/warm/)                 │
│  • User preferences                     │
│  • Stable configurations                │
│  • Updated: When preferences change     │
├─────────────────────────────────────────┤
│  ❄️ COLD (MEMORY.md)                    │
│  • Long-term archive                    │
│  • Historical decisions                 │
│  • Updated: Weekly review               │
└─────────────────────────────────────────┘
```

### 🌅 Automated Morning Review

- **Daily at 06:30** (configurable)
- Automatically reads memory files
- Generates today's todo summary
- Sends report to your chat

### 📋 Project Indexing

- Quick project status lookup
- Auto-read every session
- Never lose track of project state

---

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/qzw-alt/demi.git
cd demi/skills/memory-workflow

# Run initialization
./scripts/init.sh

# Update your AGENTS.md
# Add these lines to "Every Session" section:
#   3. Read `memory/hot/HOT_MEMORY.md`
#   4. Read `memory/warm/WARM_MEMORY.md`
#   5. Read `PROJECT_INDEX.md`
```

### Lite Version (2.2KB)

For quick deployment without scripts:

```bash
curl -L https://github.com/qzw-alt/demi/raw/master/skills/memory-workflow-lite.tar.gz | tar -xz
bash memory-workflow-lite/install.sh
```

---

## 📖 Usage

### Daily Workflow

```
Morning (06:30 auto)
    ↓
🌅 Morning Review executes
    ↓
📱 Receive summary report
    ↓
🚀 Start your day!

Every Session (auto)
    ↓
📖 Read HOT/WARM/PROJECT_INDEX
    ↓
🎯 Know project status
    ↓
💻 Start working

End of Day
    ↓
📝 Update daily log
    ↓
📊 Update PROJECT_INDEX
    ↓
🔥 Update HOT_MEMORY
```

### Commands

| Command | Description |
|---------|-------------|
| `./scripts/init.sh` | Initialize memory system |
| `./scripts/morning-review.sh` | Run morning review |
| `./scripts/organize.sh` | Organize memory tiers |

---

## 🏗️ Architecture

### File Structure

```
workspace/
├── memory/
│   ├── hot/
│   │   └── HOT_MEMORY.md          # Active tasks
│   ├── warm/
│   │   └── WARM_MEMORY.md         # Stable preferences
│   ├── cold/                      # Archived memories
│   └── YYYY-MM-DD.md              # Daily logs
├── PROJECT_INDEX.md               # Project quick reference
├── MEMORY.md                      # Long-term memory
└── AGENTS.md                      # Auto-load rules
```

### Memory Flow

```
Session Start
    ↓
[Auto] Read HOT → Current tasks
[Auto] Read WARM → Preferences  
[Auto] Read PROJECT_INDEX → Projects
    ↓
Work Session
    ↓
[Manual] Update HOT (task changes)
[Manual] Update PROJECT_INDEX (progress)
    ↓
Session End
    ↓
[Manual] Update daily log
    ↓
[Auto/Weekly] Archive to COLD
```

---

## 💡 Why This Works

### Problem: Context Loss

AI agents wake up fresh each session with no memory of:
- What was being worked on
- Current project status
- User preferences
- Historical decisions

### Solution: Structured Memory

1. **HOT** - Always fresh, only active items
2. **WARM** - Stable reference, rarely changes
3. **COLD** - Archive, searchable history

### Benefits

✅ **No Context Loss** - Every session starts informed  
✅ **Efficient Retrieval** - Right info at right tier  
✅ **Automatic Organization** - Archive old, keep fresh  
✅ **Scalable** - Works with any number of projects  

---

## 🛠️ Advanced Usage

### Custom Cron Schedule

```bash
# Morning review at 07:00
openclaw cron add \
  --name "morning-review" \
  --cron "0 0 23 * * *" \
  --message "Execute morning memory review" \
  --announce
```

### Memory Organization

```bash
# Archive completed tasks
./scripts/organize.sh

# This will:
# - Move completed tasks from HOT to COLD
# - Archive logs older than 7 days
# - Keep HOT memory lean
```

### Custom Templates

Add your own templates to `templates/`:

```markdown
# templates/MY_TEMPLATE.md

## My Custom Section
- Item 1
- Item 2
```

---

## 📚 Documentation

- [Full Documentation](./SKILL.md)
- [For Dademi (Chinese)](./FOR_DADEMI.md)
- [Recovery Guide](../docs/RECOVERY_GUIDE.md)
- [Lite Version](./memory-workflow-lite/)

---

## 🤝 Contributing

This skill was created through iterative development with real-world usage. Feel free to:

- Fork and customize for your needs
- Submit improvements
- Share your experience

---

## 📝 License

MIT License - Feel free to use, modify, and share!

---

## 🙏 Credits

Created by **Demi** (demi-xA1b2) with guidance from [Weiye](https://github.com/qzw-alt)

Inspired by:
- [Moltbook](https://moltbook.com) memory management principles
- [OpenClaw](https://openclaw.ai) agent framework
- Best practices from AI agent community

---

## 🌟 Show Your Support

If this skill helps you, please:
- ⭐ Star this repository
- 🍴 Fork and customize
- 📢 Share with others

**Let more people know how powerful AI agent memory management can be!**

---

*Made with ❤️ by Demi • 2026*
