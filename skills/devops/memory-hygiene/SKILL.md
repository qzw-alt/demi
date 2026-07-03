---
name: memory-hygiene
description: "Use when maintaining the multi-layer memory system on Hermes — preventing 'I forgot what you said yesterday' failures, designing what lives in MEMORY.md (auto-injected) vs DETAIL/ (on-demand), and recovering from capacity overflow or aspirational-architecture drift. Triggers include: '我的记忆出了问题', '昨天我跟你说过...', '记忆管理系统', '分层记忆', 'memory 满了', 'memory 改造', '分层架构', '你怎么忘了'."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [memory, hermes-internal, architecture, user-state]
    related_skills: [medical-tourism-site-ops, hermes-cron-troubleshooting, hermes-backup]
---

# Memory Hygiene (multi-layer memory maintenance)

## Overview

Hermes has a hard constraint: only **MEMORY.md** (≤2,200 chars) and **USER.md** (≤1,375 chars) are auto-injected into every session's system prompt. Everything else — plans, large references, full schemas, customer files — must live elsewhere. This skill covers the discipline of **what goes where**, **how to detect when the system has drifted**, and **how to recover** when the user says "you forgot what I told you."

The most common failure mode is writing **aspirational architecture** into the live memory file ("4-Layer 架构 + 单点真实源") without actually implementing it — the user later asks about a thing MEMORY.md says is handled, and we discover it never was. **If a structure isn't real, don't write it into MEMORY.md.** Plans belong in a skill or in a DETAIL/ file.

## When to Use

- User says "记忆管理系统", "分层记忆改造", "memory 满了", "你怎么忘了"
- About to add a long new fact to MEMORY.md and notice the budget is tight
- Suspect that an "established" pattern referenced in MEMORY.md is actually aspirational text
- Deciding where a new fact (cron job, customer, project plan, technical reference) should live
- After a "你漏记了" or "我昨天说过" moment — recovering and preventing recurrence
- When `~/.hermes/memories/DETAIL/` doesn't exist yet, or exists but nothing is being read from it

## The Two-Layer Reality (and the Aspiration Trap)

| Layer | Lives in | Auto-injected? | Read with | Size budget |
|---|---|---|---|---|
| **Hot (always on)** | `~/.hermes/memories/MEMORY.md` + `USER.md` | ✅ Every session | (auto) | 2,200 + 1,375 chars (hard) |
| **Detail (on demand)** | `~/.hermes/memories/DETAIL/*.md` | ❌ Never | `read_file` tool, manually | No hard cap |
| **Code-resident** | `~/.hermes/skills/<category>/<name>/` | ❌ Per-skill | `skill_view` | 100k chars/skill |

**The `memory` tool only edits `MEMORY.md` and `USER.md`.** It does not know DETAIL/ exists. If you want DETAIL/ content surfaced, you must (a) write the file with `write_file` or `execute_code`, and (b) put a **trigger-aware pointer** in MEMORY.md like "写新闻前 → read_file DETAIL/chinahospitalsguide-content-matrix.md" so future sessions know when to read it.

**The aspiration trap:** writing "4-Layer 架构" or "单点真实源" in MEMORY.md **without** the corresponding DETAIL/ files actually being populated and being read. This is worse than not having the line at all, because it makes future sessions confidently recommend actions based on a non-existent structure. Verify every "架构" claim with `ls ~/.hermes/memories/DETAIL/` before treating it as a contract.

## Decision tree: where does a new fact go?

```
Is it ~always relevant in every session?
  (identity, working style, current top-priority project, hard-won lesson, time-zone)
  → MEMORY.md or USER.md

Is it relevant only in a specific scenario
  (writing news, deploying site, customer follow-up, technical fact lookup)
  and would I want to read it on demand rather than always inject it?
  → DETAIL/<scenario>.md, with a trigger line in MEMORY.md

Is it a reusable procedure or workflow
  (how to do X, including the traps and the verification steps)
  → skill, possibly with a pointer from MEMORY.md
```

**Default rule: when in doubt, DETAIL/.** The cost of a `read_file` call is small; the cost of an always-injected item eating 200 chars of MEMORY.md budget for the rest of time is permanent.

## Discipline rules

1. **Never write architecture into MEMORY.md that you haven't actually built.** If you say "→ see DETAIL/foo.md", that file must exist and be populated, AND there must be a protocol to read it. Verify with `ls ~/.hermes/memories/DETAIL/` before claiming the structure exists.

2. **MEMORY.md is a pointer list, not a knowledge base.** Every entry should be either (a) a fact that's too important to be a pointer, or (b) a "X → read Y" line. Long explanations, full schemas, multi-line procedures → DETAIL/ or skill.

3. **Capacity budget is 2,200 / 1,375 chars (or whatever `config.yaml` says).** The 2,200 cap is the platform's hard limit on MEMORY.md; exceeding it may cause silent truncation. Before every `patch`/`write_file` to MEMORY.md, run `wc -c` and confirm headroom.

4. **Use `memory` tool for surgical edits; use `patch`/`write_file` for bulk rewrites.** The `memory` tool's `replace` action matches entry by entry (good for adding one line, updating one fact). When MEMORY.md has drifted away from the `memory` tool's atomic-entry format (e.g., a previous session hand-edited it with `§` separators), `patch`/`write_file` is the only path — but **verify afterwards that `memory` tool can still find entries if needed**.

5. **DETAIL/ files need a trigger line in MEMORY.md that says WHEN to read them.** Without this, they're dead stock. Trigger phrasing should be imperative and scenario-anchored:
   - ✅ "写新闻/blog 前 → 必读 `DETAIL/chinahospitalsguide-content-matrix.md`"
   - ❌ "There is a content matrix in DETAIL/." (no trigger, will be ignored)

6. **Read DETAIL/ before acting on its pointer.** If MEMORY.md says "写新闻前必读 X", and the user asks me to write a news article, the first action is `read_file` on X. If I skip this, the pointer is decorative.

7. **When the user says "你忘了" or "昨天我说过",** the recovery is not "let me add it now" — it's "let me check whether (a) it was ever written to a persistent location, and (b) if not, write it to DETAIL/ with a trigger line, and (c) verify I can retrieve it." This is the protocol that prevents the next "you forgot".

## Detection signals (when memory is drifting)

- User says "你忘了" / "昨天我说过" / "我跟你讲过"
- User says "你之前不是有 X 系统吗" — and the X system was never real
- MEMORY.md > 2,200 chars (or whatever current limit) — truncation risk
- USER.md > 1,375 chars — same
- `~/.hermes/memories/DETAIL/` doesn't exist, or has files but MEMORY.md doesn't reference them
- A previous session wrote a long block to MEMORY.md using `§` separators (manually hand-edited, not the `memory` tool's format)
- A "详见 path" reference in MEMORY.md points to a file that doesn't exist (e.g., `memory/layer3/preferences.md` referenced when no such file is at that path)

## Recovery protocol (when the user catches a memory failure)

1. **Don't apologize three times.** Say "you're right, [fact] was missing, here's what I'm doing about it" in one sentence.
2. **Diagnose the root cause:** Was it (a) never written, (b) written but not in a place that gets read, or (c) written but truncated by capacity?
3. **Choose the right home** using the decision tree above.
4. **Make it real:**
   - If new fact → write to MEMORY.md (and `wc -c` to confirm) OR to DETAIL/ (and add a trigger line to MEMORY.md)
   - If aspirational architecture was claimed → either (a) build the structure, or (b) delete the lie. **Don't leave aspirational text in MEMORY.md.**
5. **Verify the fix works for the next session:** can a fresh session, reading only MEMORY.md, know when to read DETAIL/foo.md? If not, the pointer is still wrong.

## Common Pitfalls

1. **The "4-Layer 架构" lie.** Writing a multi-layer memory architecture promise into MEMORY.md (e.g., "HOT.md / MEMORY.md / DETAIL/ / archive/") without actually building the directory structure or the read-on-demand protocol. When the user later asks about the structure, you have to confess it never existed. (Verified 2026-07-03 on the wei-ye setup.) **Fix:** Before writing any "X → see Y" line, `ls` the destination and confirm it's real.

2. **Using `memory` tool's `replace` on hand-edited MEMORY.md.** The `memory` tool's `replace` matches by whole-entry string. If a previous session `write_file`-ed MEMORY.md with `§` separators and the entry no longer matches the tool's expected format, `memory` tool returns "No entry matched". Workaround: use `patch` for hand-edited files, and consider rewriting the file to native `memory` tool format when convenient.

3. **Writing the same fact into MEMORY.md, USER.md, and DETAIL/.** Pick one. MEMORY.md/USER.md are for always-on facts. DETAIL/ is for scenario-specific facts. If a fact appears in both MEMORY.md and DETAIL/foo.md, future readers won't know which is canonical. **Rule:** always-on → MEMORY.md/USER.md; scenario-specific → DETAIL/ with pointer.

4. **DETAIL/ files referenced but never read.** A pointer in MEMORY.md that says "→ see DETAIL/foo.md" only helps if the next session actually `read_file`s it. If a session is asked to do a task that matches the trigger, the **first action** must be `read_file` on the pointed file. Don't write pointers as decoration.

5. **Treating memory architecture as a project.** "分层改造" sounds like a project; it's actually a recurring discipline. There's no "done" state — every new fact forces the question of where it lives. The user does NOT want a 5-phase plan; they want a clean state and a discipline. (See `medical-tourism-site-ops` "90-day plan trap" lesson: avoid grand roadmaps.)

6. **Expanding `memory_char_limit` in `config.yaml` without a plan.** The 2,200/1,375 cap is set in `~/.hermes/config.yaml`. Increasing it is possible (and may be the right move for a heavy user), but it requires a gateway restart and a `config.yaml` edit — both with downtime risk. Don't change this without explicit user approval.

7. **Reflexively writing aspirational text after a memory failure.** When the user catches a memory miss, the urge is to over-correct by writing a long "now I will remember X, Y, Z" block into MEMORY.md. This usually makes the file longer and more full of declarations than facts. Better: write the missed fact to the right place, add a tight pointer, move on.

## Verification Checklist

- [ ] `wc -c ~/.hermes/memories/MEMORY.md` ≤ 2,200 (or current configured limit)
- [ ] `wc -c ~/.hermes/memories/USER.md` ≤ 1,375
- [ ] `ls ~/.hermes/memories/DETAIL/` exists if MEMORY.md references it
- [ ] Every "→ see DETAIL/X" pointer in MEMORY.md has a real file at that path
- [ ] Every pointer in MEMORY.md has a **trigger line** (imperative, scenario-anchored), not just a description
- [ ] No duplicate facts across MEMORY.md ↔ USER.md ↔ DETAIL/ (pick one canonical home)
- [ ] No aspirational architecture lines in MEMORY.md (verify with `ls` that claimed structures exist)
- [ ] After any edit to MEMORY.md: simulate a fresh-session reader — can they find what they need?

## The "I Forgot" Recovery Checklist (one-shot)

When the user says "你昨天跟我说过" / "你怎么忘了" / "我以为我们讲好了":

- [ ] Acknowledge in 1 sentence, no triple apology
- [ ] `grep -r "<keyword>" ~/.hermes/memories/` to see if it was ever written
- [ ] If not written → write to DETAIL/<scenario>.md with a trigger line in MEMORY.md
- [ ] If written but not in auto-inject → already in DETAIL/, the fix is to add the trigger line to MEMORY.md
- [ ] If written and triggered but I still missed it → the trigger wording is wrong; rephrase and verify
- [ ] Report what was done with a verifiable handle (file path, grep count, byte count)
