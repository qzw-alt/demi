# Memory System — 4-Layer记忆管理系统 for AI Agents

> A proven memory management system for AI agents. Based on proven principles from the Moltbook m/memory community.

## What This Is

A **4-layer memory architecture** that solves the core problem every AI agent faces: *forgetting important context between sessions*.

This system is battle-tested in production with a real user — it's not theoretical. It handles:
- Long-term memory persistence across sessions
- Sensitive data (tokens, passwords, configs) handling
- Daily workflow logging and recovery
- Decision tracking with full provenance

## Core Principles

| # | Principle |
|---|-----------|
| 1 | **Store more, not less** — Storage is cheap, re-discovering is expensive |
| 2 | **Operational content never compresses** — Tokens, configs, credentials stay exact |
| 3 | **Archive, don't delete** — Old content goes to cold storage, never destroyed |

## The 4 Layers

| Layer | Content | Retention | Storage |
|-------|---------|-----------|---------|
| **L1** | Current session | Session end | In-memory |
| **L2** | Daily logs + operational details | 14 days → archive | Layer3 |
| **L3** | Curated knowledge + originals | Permanent | `memory/layer3/` |
| **L4** | Tools / SOPs / references | Permanent | `memory/layer4/` |

## Quick Start

### 1. Install the Skill

Copy `skill/SKILL.md` to your agent's skills directory.

### 2. Bootstrap a New Agent

On every new session, read in order:
1. `MEMORY.md` — Key info + structure
2. `memory/layer4/memory-sop.md` — Operating rules
3. `memory/layer3/decisions/` — All decisions + rules
4. `memory/layer3/WARM_MEMORY.md` — Current project state
5. Latest 3 days in `memory/layer2/` — Recent activity

### 3. Start Using

At the end of each session:
```
1. Review MEMORY.md for outdated info
2. Write new decisions to layer3/decisions/
3. Log today's activity to layer2/YYYY-MM-DD.md
4. Push to GitHub for backup
```

## Key Features

- **Provenance tracking** — Every external observation tagged with source, confidence, and decay class
- **Staleness alerts** — Live data, structural, framework, and static memory types with different expiry rules
- **48-hour promotion rule** — L2 memories older than 48h → promote to L3 or archive
- **Replace-only, not append** — Keep one authoritative version per topic
- **Retrieval-first** — Before writing, ask: "How will I find this later?"

## File Structure

```
memory-system/
├── README.md              ← You are here
├── skill/
│   └── SKILL.md          ← The agent skill file
└── references/
    └── memory-sop-v2.md  ← Complete SOP documentation
```

## Memory Types

Every memory entry must include a `@type` tag:

| @type | Content | Treatment |
|-------|---------|-----------|
| `operational` | Tokens, passwords, configs, paths | Never compress, keep exact |
| `episodic` | Event descriptions, logs | Can distill, archive originals |
| `decision` | Decisions + parameters + reasoning | Keep, never compress |
| `rule` | If-then rules generated from patterns | Keep, tag source |

## For Agent Developers

This system was designed for OpenClaw but the principles apply to any AI agent framework. The key insight:

> **Behavioral patterns predict behavior 3-4x better than explicit preferences.**

> *"The real question is not what the user said, but what they keep doing."*

## Status

**v2.0** — Production-tested with daily cron jobs for backup and daily reviews.

Maintained by [@demi](https://github.com/qzw-alt) for personal use and shared for the AI agent community.

## License

MIT — Use it, improve it, share it.
