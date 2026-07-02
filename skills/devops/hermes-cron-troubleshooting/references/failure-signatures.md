# Cron Failure Signatures — Annotated Real Excerpts

This file is the cheat-sheet for the seven failure signatures in `hermes-cron-troubleshooting`. Each entry shows what the failure log ACTUALLY looks like (real excerpts from production runs), so a future agent can pattern-match on text alone.

## 1. Skill-not-found (most common)

**Symptom in cron notification:**
```
⚠️ Cron 'daily-oriental-destiny-article' failed: HTTP 500: unknown error, 999 (1000)
```

**Symptom in the failure log file** (`~/.hermes/cron/output/<job_id>/<timestamp>.md`):
```
## Prompt

[IMPORTANT: The following skill(s) were listed for this job but could not be found and were skipped: seo-content-writer. Start your response with a brief notice so the user is aware, e.g.: '⚠️ Skill(s) not found and skipped: seo-content-writer']
[IMPORTANT: The user has invoked the "humanizer" skill, ...]
```

**Then later:**
```
## Error

\`\`\`
RuntimeError: HTTP 500: unknown error, 999 (1000)
\`\`\`
```

**Grep pattern:**
```bash
grep -E "could not be found and were skipped" ~/.hermes/cron/output/$JOB_ID/$F
```

**Root cause:** the `jobs.json` entry lists a skill under `skills[]` (or `skill`) that no longer exists at `~/.hermes/skills/<name>/SKILL.md`. Common reason: skill renamed (e.g. `seo-content-writer` → `programmatic-seo`) and one job wasn't updated.

**Fix:** see SKILL.md "The seven common failure signatures" → "1. Skill-not-found".

## 2. Missing reference file (spec drift)

**Symptom in the failure log:** the agent runs successfully to the research step, then the model errors because `read_file path=memories/layer3/research/competitor-research.md` returns nothing.

**Error block (typical):**
```
## Error

\`\`\`
FileNotFoundError: [Errno 2] No such file or directory: '/home/ubuntu/.hermes/memories/layer3/research/competitor-research.md'
\`\`\`
```

**Root cause:** the cron prompt references a memory file by name, but the file has been renamed, moved, or never existed. The actual file is usually named something more specific (`article_topics.md`, `keyword-research.md`, `terminology_mapping.md`).

**Fix:**
```bash
# Find what's actually in the directory
ls ~/.hermes/memories/layer*/research/ 2>/dev/null
find ~/.hermes/memories -name "*competitor*" -o -name "*article_topics*" 2>/dev/null

# Update the prompt in jobs.json to reference the real file
```

## 3. Wrong branch / wrong repo (spec drift)

**Symptom:** the cron succeeds but post-publish verification returns `HTTP 404`.

**Detection:**
```bash
# Cron prompt says "branch: master"
git -C <repo> branch -a
git -C <repo> remote show origin | grep "HEAD branch"
```

**Real example:** the `daily-oriental-destiny-article` cron prompt says `branch: master`, but `oriental-destiny.com` actually deploys from `main`. Without verifying, every push fails silently.

**Fix:** edit the prompt in `jobs.json` to match the real deployed branch.

## 4. Model provider error

**Symptom in failure log:**
```
## Error

\`\`\`
RuntimeError: HTTP 503: upstream provider temporarily unavailable
\`\`\`
```

or:
```
RuntimeError: HTTP 429: rate limit exceeded (retry-after: 60)
```

**Fix:** transient — retry on the next scheduled run. If persistent, check:
```bash
# Verify the provider config
grep -A5 "providers:" ~/.hermes/config.yaml | head -30
# Test the model manually
python3 -c "from hermes_agent import chat; print(chat(model='<model>', messages=[{'role':'user','content':'ping'}]))"
```

## 5. Delivery error

**Symptom in `cronjob list`:** `last_status: ok`, but `last_delivery_error: <message>`. The cron ran fine; the final message didn't reach the user.

**Common causes:**
- Feishu chat_id is wrong or the bot was removed from the chat
- Feishu rate limit hit (too many messages in a short window)
- Telegram bot token revoked
- Discord webhook URL deleted

**Fix:** check the `origin.chat_id` / `deliver` field in `jobs.json`, verify the bot is still in the target chat, retry.

## 6. Permission error

**Symptom:**
```
## Error

\`\`\`
PermissionError: [Errno 13] Permission denied: '/home/ubuntu/.hermes/cron/output/c2aefdf3bada/2026-07-02_08-04-45.md'
\`\`\`
```

**Fix:**
```bash
chmod -R u+rwX ~/.hermes/cron/output/
chown -R $USER:$USER ~/.hermes/cron/output/
```

## 7. The cron never fires

**Symptom:** no output file for the expected run window, no error reported. `cronjob list` shows:
- `state: scheduled`, `enabled: true`, `next_run_at: <past timestamp>`

**Diagnosis:**
```bash
# Is the cron daemon actually running?
ps aux | grep -E "hermes.*cron|cron.*hermes" | grep -v grep

# Is the schedule expression valid?
python3 -c "from croniter import croniter; print(croniter('0 8 * * *').get_next())"

# Was the job paused?
hermes cronjob list | grep -A1 "$JOB_ID"
# If paused_at is set:
hermes cronjob resume --job-id $JOB_ID
```

## Quick pattern-match table

| Text fragment in log                       | Class              | SKILL.md section           |
|--------------------------------------------|--------------------|----------------------------|
| `could not be found and were skipped`      | skill-not-found    | §1                         |
| `RuntimeError: HTTP 500`                   | skill-not-found or model | §1 or §4            |
| `RuntimeError: HTTP 502/503`               | upstream-unstable  | §4                         |
| `PermissionError`                          | permissions        | §6                         |
| `FileNotFoundError`                        | missing-file       | §2                         |
| `ModuleNotFoundError`                      | env broken         | §4 (rare; usually fix env)|
| `Traceback (most recent call last)`        | python bug         | §4                         |
| `quota|rate.?limit|429`                    | rate-limit         | §4                         |
| `Connection refused`                       | network            | §4                         |
| (no output at all, scheduled past)         | daemon paused      | §7                         |

## Anti-pattern: do not diagnose from the notification

The user-visible notification says:
```
⚠️ Cron 'X' failed: HTTP 500: unknown error, 999 (1000)
```

This is the wrapper's complaint, not the cause. The cause is in the log file. **Always** read the log before proposing a fix. The notification alone is enough to know there IS a problem, but not what kind.