# Safe Edit: `~/.hermes/cron/jobs.json`

> **When to load**: any time a session needs to programmatically mutate the `prompt` field of a cron job in `~/.hermes/cron/jobs.json`. The file is **not** in git (only `hermes-backup` cron at 22:00 pushes it to `qzw-alt/demi`), so a corruption has **no easy undo**.

## The trap (verified 2026-07-28)

The naively-correct-looking Python reconstruction that corrupts the file:

```python
# raw = full file string
# job_block = raw[job_start:job_end]
# ps, pe = positions within job_block of the prompt value

# BUG: ps is in job_block coordinates, but the slice below subtracts job_start,
# which assumes raw coordinates — slices wrap around the entire raw buffer
new_job_block = job_block[:ps - job_start] + new_prompt_escaped + job_block[pe - job_start:]
new_file = raw[:job_start] + new_job_block + raw[job_end:]
```

When `ps < job_start`, `job_block[:ps - job_start]` is a **negative-slice** that picks the *end* of `job_block` instead of the *beginning*. The new prompt gets sandwiched into the middle, and `new_file` ends up with the original prompt embedded 2-3 times.

**Symptom**: file size grows ~60% (35909 → 57454 bytes in the verified case), JSON still parses (so `json.load` doesn't catch it), but the prompt field has duplicated/triplicated content with broken mid-string boundaries.

## The recipe (use this, not free-form `str.replace`)

### Step 1: BACKUP before anything

```bash
cp ~/.hermes/cron/jobs.json ~/.hermes/cron/jobs.json.bak-$(date +%Y%m%d-%H%M%S)
ls -la ~/.hermes/cron/jobs.json.bak-*
```

This is **non-negotiable**. The file isn't in any git repo Hermes can reach, and `hermes-backup` runs at 22:00 — 13 hours after the daily `daily-chg-medical-news` cron at 09:00. If you corrupt it at 09:05, the next clean version is at 22:00.

### Step 2: Parse → mutate the parsed object → re-serialize. Don't try to slice-and-splice the raw string.

```python
import json, shutil
from pathlib import Path

JOBS = Path.home() / ".hermes" / "cron" / "jobs.json"

# Load
with open(JOBS) as f:
    data = json.load(f)

# Find the target job
target = next(j for j in data["jobs"] if j["id"] == "fa7a29b3464e")

# Mutate the prompt field as a normal Python string
# (json.load decoded \uXXXX escapes back to actual CJK chars)
old_prompt = target["prompt"]
new_prompt = old_prompt.replace("OLD_NEWS_TOKEN", "NEW_BLOG_TOKEN")  # do all replacements here

target["prompt"] = new_prompt

# Write back — json.dump re-escapes CJK and handles all the \uXXXX work
with open(JOBS, "w") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
```

**Why this is safe**: `json.load` decodes all `\uXXXX` escapes into real Unicode chars. `json.dump(..., ensure_ascii=False)` re-encodes them. You never touch a raw escaped string, so the coordinate-system pitfall can't bite you. The `\uXXXX` ↔ real-char round-trip happens once, inside the JSON library.

### Step 3: Round-trip verify

```python
import json
with open(JOBS) as f:
    data2 = json.load(f)

target2 = next(j for j in data2["jobs"] if j["id"] == "fa7a29b3464e")

# Checks that catch the 2026-07-28 corruption class:
assert len(target2["prompt"]) < 12000, f"prompt too long ({len(target2['prompt'])} chars) — possible duplication"
assert target2["prompt"].count("每天") <= 2, "prompt has >2 '每天' starts — duplication"
assert "NEW_BLOG_TOKEN" in target2["prompt"], "replacement didn't land"
assert "OLD_NEWS_TOKEN" not in target2["prompt"], "old token not replaced"
assert target2["prompt"].endswith("真失败。"), "prompt truncated — last sentence missing"
```

Plus a manual eyeball: `cat ~/.hermes/cron/jobs.json | python3 -m json.tool | head -40` and confirm the prompt starts with "每天为 chinahospitalsguide.com..." only once.

### Step 4: Diff against backup

```bash
diff ~/.hermes/cron/jobs.json.bak-YYYYMMDD-HHMMSS ~/.hermes/cron/jobs.json | head -100
```

The diff should show only the prompt field changed, with the rest of the file byte-identical.

## If you MUST do free-form string replace (avoid this)

Only acceptable when:
- The replacement is **1 occurrence** in the entire file (verify with `grep -c`)
- The old/new strings are **short ASCII** (no CJK, no quotes, no backslashes)
- You're OK with using `patch` tool with a **uniquely-identifying** old_string anchor

Even then: backup first, round-trip verify after.

## The 5-min quick path: just rebuild from backup cron

If corruption is bad enough that reconstruction is risky:

1. Restore the most recent known-good version. Options:
   - `gh repo view qzw-alt/demi --json files` → look for the last `jobs.json` snapshot in yesterday's backup commit
   - Ask Weiye to paste his local copy (he often has it open)
   - Reconstruct from the other 4 jobs (which weren't touched) + a hand-written prompt (last resort)

2. After restoring: re-test with `crontab -l` and check that all 5 jobs are listed (`hermes cron list`).

## Cron edit cadence rule

Wei's preference is to **plan cron prompt edits carefully, then batch them** — don't do them piecemeal across multiple sessions. Each edit risks corruption, and he wants stable cron behavior between edits. If you find 3 things that need changing in the prompt, propose all 3 in one message; don't drip-feed one per session.