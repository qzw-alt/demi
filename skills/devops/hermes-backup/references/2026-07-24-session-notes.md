# Session notes — 2026-07-24 (cron backup)

Authoritative log of the 2026-07-24 22:00 Asia/Shanghai cron run.
New lessons captured in this run are folded into `SKILL.md` pitfalls and
the step-5 inline redaction recipe; this file is the day-by-day context
where the reproduction transcripts live.

## TL;DR — what worked, what broke

| Step | Status | Notes |
|------|--------|-------|
| 0. SSH auth | OK | `Hi qzw-alt! You've successfully authenticated` |
| 1. Clone | OK after retry | First attempt needed `background=true` + `notify_on_complete=true` + `timeout=600` |
| 2. Rsync | OK | All excludes held; no LEAK warnings |
| 3. Cleanup | OK | `.gitignore` survived — restored from HEAD (1007 bytes / 50 lines, unchanged) |
| 4. Redact (walker) | Partial | Walker processed ~50+ files, but missed two CJK-path MEMORY.md files |
| 5. Length-gated scan | Caught both | Real tvly- in 3 files + a sk- in workspace/website/德米知识库/... |
| 6. Commit + push | OK | `1c6992e1a Backup: 2026-07-24_22:04` |
| 7. Cleanup | OK | `/tmp/demi-backup/` removed |

Final commit: **`1c6992e1a74bac8504dd2e2575cd51644d6a6ab2`** (master).
Local HEAD matched remote HEAD after `git fetch` — push verified.

## New finding 1 — bundled `redact_secrets.py` single-file mode ALSO misses `tvly-`

Previously the skill only flagged **batch** mode as walker-gappy on `tvly-`.
Today I verified the same gap exists in single-file mode.

### Reproduction

```bash
cd /tmp/demi-backup
F='workspace/website/德米知识库/01-记忆系统/MEMORY.md'

# Bundled single-file mode
python3 $SKILL_DIR/scripts/redact_secrets.py /tmp/demi-backup "$F"
# → REDACTED: /tmp/demi-backup/workspace/website/.../MEMORY.md (0 PAT, 1 sk-)

# Re-scan: tvly- still present
grep -nE "tvly-[a-zA-Z0-9_-]{40,}" "$F"
# → 88:- **Tavily API**: tvly-dev-sAFTx-2XjSFsXdR5Z...a7Si
```

The single-file mode only handles the prefix list hard-coded in the script
(`sk`, `github_pat_`, `gh[pousr]_`). It prints success and silently
fails on `tvly-`, `glpat-`, `AIza`. **You cannot rely on the bundled script
for any prefix outside its regex list — even in single-file mode.**

### Fix

Use the `/tmp/redact_providers.py` snippet from step 5 of the skill as
a complementary pass. Today the working call was:

```bash
python3 /tmp/redact_providers.py "$F"
# → truncated 1 tvly- token(s) in workspace/website/.../MEMORY.md
# → WRITTEN: workspace/website/.../MEMORY.md
```

## New finding 2 — inline `redact_prefix.py` (v1, 2026-07-19) is silently buggy

The 2026-07-19 version of the inline snippet (documented in the skill's
"Provider-prefix-aware inline redaction" block) was:

```python
prefix, p = sys.argv[1], sys.argv[2]
c = open(p, encoding='utf-8').read()
pat = re.compile(rf'{prefix}-[a-zA-Z0-9_]+')
def _trunc(m):
    s = m.group(0)
    if '...' in s or len(s) < 30: return s
    head = s[: 5 + len(prefix) + 6]
    return f'{head[:-2]}...{s[-4:]}'
open(p, 'w', encoding='utf-8').write(pat.sub(_trunc, c))
```

### Bug

The character class `[a-zA-Z0-9_]+` does NOT include `-`. On
`tvly-dev-sAFTx-2XjSFsXdR5Z...a7Si`:

- Match attempt starts at `tvly-`
- `[a-zA-Z0-9_]+` matches `dev` (3 chars)
- Then `-` stops the match
- `m.group(0)` is `tvly-dev` (8 chars total), body length is 3
- The `len(s) < 30` gate short-circuits → return s unchanged
- Replaced with self → file written with `UNCHANGED:` print

So the script silently reports "no change" but `tvly-` IS in the file.

### Fix (now embedded in SKILL.md step 5)

- Add `-` to the body character class → `[a-zA-Z0-9_-]+`
- Replace `\b` boundary with negative look-behind `(?<![\w-])` so the
  match doesn't anchor at internal hyphens
- Drop the `<prefix>` argv in favor of a multi-prefix loop so one
  invocation handles `tvly`, `sk`, `github_pat`, `ghp`, etc. without
  needing a fresh `/tmp/redact_*` file per provider

```python
prefixes = ['tvly', 'sk', 'github_pat', 'ghp', 'gho', 'ghu', 'ghr', 'ghs',
            'AIza', 'glpat', 'xoxb', 'xoxp']
p = sys.argv[1]
c = open(p, encoding='utf-8').read()
new = c
for pref in prefixes:
    pat = re.compile(rf'(?<![\w-]){re.escape(pref)}-[a-zA-Z0-9_-]+')
    def _trunc(m, _pref=pref):
        s = m.group(0)
        if '...' in s: return s
        body = s[len(_pref)+1:]
        if len(body) < 25: return s
        return f'{_pref}-{body[:6]}...{body[-4:]}'
    new = pat.sub(_trunc, new)
if new != c:
    open(p, 'w', encoding='utf-8').write(new)
    print(f'WRITTEN: {p}')
else:
    print(f'UNCHANGED: {p}')
```

## New finding 3 — first-time clone is a slow path

Today was the first run after the repo was emptied on the host side
(`/tmp/demi-backup/` did not exist). Populated `qzw-alt/demi` (1.2GB
working tree, hundreds of commits) routinely exceeds 60s on `git clone`.

The skill's existing pitfall ("Default git clone over SSH may take
>60s — `timeout 240` does NOT save you") had the right recipe — I used:

```python
terminal(background=true, notify_on_complete=true, timeout=600,
         command="rm -rf /tmp/demi-backup/ && mkdir -p /tmp/demi-backup/ && "
                 "cd /tmp/demi-backup && git clone git@github.com:qzw-alt/demi.git .")
# then process(action='wait', timeout=60) → repeated poll, took ~2 min total
```

Then rsync (foreground, 8s) and the rest were fast. **No new patch
needed — the existing pitfall recipe worked.** Marked it as confirmed
in this run; no skill change beyond the reference-file pointer.

## New finding 4 — CJK walker miss, confirmed REAL (not idempotent)

Yesterday's session notes (2026-07-23) tentatively classified CJK misses
as idempotent re-redactions. Today's diff confirmed the opposite — this
time it was a real leak.

```bash
cd /tmp/demi-backup
F='workspace/website/德米知识库/01-记忆系统/MEMORY.md'
diff <(git show HEAD:"$F") "$F"
# → 87,88c87,88
# < - **Kimi API (2.5)**: sk-kimi-i...NGGW（新配置中）
# < - **Tavily API**: tvly-dev-sAFT...a7Si
# ---
# > - **Kimi API (2.5)**: sk-kim...NGGW（新配置中）
# > - **Tavily API**: tvly-dev-sAFTx-2XjSFsXdR5Z...a7Si
# exit 1
```

The headline `sk-kim...NGGW` is shorter than the prior commit's
`sk-kimi-i...NGGW` (the walker truncated slightly more aggressively
on a fresh scan) AND the `tvly-` was brought back full by the rsync
source (rsync always restores the original 62-char key).

**Cumulative CJK walker miss count: 9 confirmed runs in a row** (2026-07-08,
-13, -14, -16, -17, -21, -22, -23, -24). Not getting better over time — plan
for at least one miss per backup indefinitely.

## Today's redactions

Three `MEMORY.md` files truncated (one sk- + three tvly- in total):

1. `workspace/website/德米知识库/01-记忆系统/MEMORY.md`
   - `tvly-dev-sAFTx-2XjSFsXdR5Z...a7Si` (62 chars)
     → `tvly-dev-sA...a7Si` (14 chars) via `redact_providers.py`
   - `sk-kimi-i...NGGW` got further truncated to `sk-kim...NGGW` by the
     bundled single-file mode pass (same line, more aggressive).
2. `workspace/website_old/MEMORY.md`
   - `tvly-dev-sAFTx-2XjSFsXdR5Z...a7Si`
     → `tvly-dev-sA...a7Si` via `redact_providers.py`
3. `workspace/website_old/德米知识库/01-记忆系统/MEMORY.md`
   - same tvly- truncation

After: length-gated scan + staged-blob scan both returned zero hits
across `github_pat_`, `gh[pousr]_`, `sk-`, `tvly-`, `AIza`, and
`providers/*.json` JSON-walked values.

## 19-file commit summary

```
M .skills_prompt_snapshot.json
 M channel_directory.json
 M cron/jobs.json
 M cron/ticker_heartbeat
 M cron/ticker_last_success
 M feishu_seen_message_ids.json
 M gateway_state.json
 M processes.json
 M skills/.usage.json
 M skills/creative/programmatic-seo/SKILL.md
 M skills/devops/hermes-backup/SKILL.md
 M skills/medical-tourism/medical-tourism-client-intake/SKILL.md
 M skills/research/terminal-web-research/references/ai-briefing-format.md
 M verification_evidence.db
 M workspace/website/德米知识库/01-记忆系统/MEMORY.md        ← redaction
 M workspace/website_old/MEMORY.md                          ← redaction
 M workspace/website_old/德米知识库/01-记忆系统/MEMORY.md     ← redaction
?? skills/creative/programmatic-seo/references/indoor-thread-room-walk-2026-07.md
?? skills/devops/hermes-backup/references/2026-07-23-session-notes.md
```

Plus my own SKILL.md for hermes-backup was modified — the in-flight
patched version was rsynced, and the working-tree diff was recorded
in this very commit. The SKILL.md will have the 2026-07-24 updates
when pushed from the next run.

## Submodule-heavy-dir informational warnings (no action)

```
HEAVY: hermes-agent/venv - 607M
HEAVY: hermes-agent/website - 27M
HEAVY: hermes-agent/tests - 32M
HEAVY: hermes-agent/ui-tui - 3.7M
```

All four are inside the `hermes-agent` submodule (mode `160000` gitlink).
The parent repo doesn't track them. Per the 2026-07-23 submodule
clarification, these are silent no-ops — leaving them alone.

## Cron job delivery

The cron prompt explicitly demanded Chinese-language简报. The delivery
followed exactly: **认证方式 / 结果 / 远程提交哈希 / 敏感扫描结果**,
with the CJK + tvly- redactions surfaced as "今天踩中的已知坑（已处理）"
section, not buried under a generic success message.

No advisories needed — the cron job is SSH-only and the prompt contains
zero PAT-shaped strings (the 2026-07-23 escalation resolved for good).
