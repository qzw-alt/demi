---
name: hermes-cron-troubleshooting
description: "Diagnose and repair failing Hermes cron jobs. Load whenever a cron reports an error (HTTP 500, skill not found, last_status=error) or when a job's output file shows a 'RuntimeError' / 'Error' block. Covers reading failure logs from ~/.hermes/cron/output/, identifying the failure signature (skill-not-found, missing file, model error, delivery error), repairing jobs.json, and verifying the fix."
version: 1.1.0
author: Hermes Agent
license: MIT
platforms: [linux]
metadata:
  hermes:
    tags: [hermes, cron, troubleshooting, repair, jobs.json, debugging]
    category: devops
    related_skills: [seo-article-publish-cron]
---

# Hermes Cron Job Troubleshooting

A class-level playbook for any failing Hermes cron job. Built from real failure modes (skill-not-found, missing reference files, model errors, delivery errors, repository drift).

## When to load this skill

Load whenever:
- A cron reports `last_status: error` in `cronjob list`
- A cron run output ends with `## Error` block containing a `RuntimeError` or `HTTP 500`
- The user asks "why did my cron fail?" / "fix the broken cron" / "cronjob X isn't running"
- A daily/recurring cron has missed one or more runs

**Do NOT** load for:
- Cron jobs that are *scheduling* wrong (wrong time / wrong cron expression) — that's a different debugging path (read the `schedule.expr` and check timezone)
- One-off cron runs that the user explicitly canceled — those don't need diagnosis
- First-time cron creation — that's a feature, not a bug

## The iron rule: read the actual failure log, don't guess

The most common time-waster is diagnosing from the error notification alone ("HTTP 500: unknown error, 999"). That message is the **runtime wrapper's** complaint, not the root cause. The root cause lives in the output markdown file.

### Step 1: Find the failure log

```bash
JOB_ID="c2aefdf3bada"   # from cronjob list
ls -lt ~/.hermes/cron/output/$JOB_ID/ | head -3
```

Open the newest file. The structure is:

1. `# Cron Job: <name> (FAILED)` — confirms it's the failure
2. `## Prompt` — shows the **exact prompt and skill list** sent to the agent. Crucially, this section also shows warnings like:
   - `[IMPORTANT: The following skill(s) were listed for this job but could not be found and were skipped: <name>]`
   - This is the FIRST thing to grep for.
3. `[IMPORTANT: The user has invoked the "<skill>" skill...]` — the skill loading trace
4. Skill contents (full SKILL.md injected into the prompt)
5. The actual instruction
6. `## Error` — the **raw exception**, with full stacktrace

### Step 2: Grep the failure signature

```bash
F=$(ls -t ~/.hermes/cron/output/$JOB_ID/ | head -1)
grep -E "could not be found|Error|Traceback|HTTP|RuntimeError" ~/.hermes/cron/output/$JOB_ID/$F
```

Then read the surrounding context (15 lines before and after each match).

**Or skip both steps** with the diagnostic script:
```bash
python3 ~/.hermes/skills/devops/hermes-cron-troubleshooting/scripts/diagnose-cron.py <job_id_or_name>
```
It does both steps + the skill-existence check + the verdict in one shot.

## The seven common failure signatures

### 1. Skill-not-found (most common — ~50% of failures)

**Signature:**
```
[IMPORTANT: The following skill(s) were listed for this job but could not be found and were skipped: <skill-name>]
```
followed by `RuntimeError: HTTP 500: unknown error, 999`.

**Why it happens:** Someone named a skill in `jobs.json` that was renamed, deleted, or never installed.

**Fix:**
```bash
# 1. List the actually-installed skills
ls ~/.hermes/skills/ ~/.hermes/skills/*/ 2>/dev/null | grep -v ":$" | sort -u

# 2. Find the closest sibling to the broken skill name
#    Common renames:
#      seo-content-writer   → programmatic-seo
#      <old-name>           → check related_skills in neighboring skills
ls ~/.hermes/skills/<category>/<candidate-skill>/SKILL.md
```

**Repair the job:**
```bash
python3 -c "
import json
with open('/home/ubuntu/.hermes/cron/jobs.json') as f:
    data = json.load(f)
for j in data['jobs']:
    if j['name'] == '<job-name>':
        j['skills'] = ['<correct-skill-1>', '<correct-skill-2>']
        j['skill'] = '<correct-skill-1>'
        break
with open('/home/ubuntu/.hermes/cron/jobs.json', 'w') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
"
```

**Verify:**
```bash
cronjob list   # confirm skill + skills reflect the fix
```

**Pitfall — DO NOT use the `patch` tool on jobs.json:** the file uses 2-space indent across `jobs[]` arrays, and `patch` will silently desync indent in any nested object. Always rewrite the affected job via Python (preserves indent, validates JSON, atomic write).

### 2. Missing reference file (spec drift)

**Signature:** the agent runs successfully to step N, then errors on a `cat`/`read_file` of a path that doesn't exist (e.g. `memories/layer3/research/competitor-research.md`).

**Fix path:** check what files actually exist in the named directory, pick the closest match, update the prompt in `jobs.json` to point at the real file. Often `competitor-research.md` should be `article_topics.md` or `keyword-research.md`.

### 3. Wrong branch / wrong repo (spec drift)

**Signature:** cron succeeds but push fails, or post-publish curl returns 404.

**Fix:** the cron prompt says "branch: master" but the repo is on `main`. Run `git -C <repo> remote show origin` to find the real default branch, update the prompt.

### 4. Model provider error

**Signature:** `RuntimeError` mentioning a provider, model name, or HTTP status from the upstream API (529, 503, quota exceeded).

**Fix:** retry on next tick. If persistent, check the provider's status page. If your model is `custom:<provider>`, verify the base URL and API key in `~/.hermes/config.yaml`.

### 5. Delivery error

**Signature:** `last_status: ok`, `last_delivery_error: <something>`. The cron ran fine but the final message didn't reach the user (e.g. Feishu rate limit, invalid chat_id).

**Fix:** check the `deliver` field — `origin` (current chat), `feishu`, `local` (no delivery, save only). If `feishu`, verify the `origin.chat_id` matches the target.

### 6. Output dir permissions

**Signature:** `PermissionError: [Errno 13] Permission denied: '/home/ubuntu/.hermes/cron/output/<job_id>/...'`

**Fix:** `chmod -R u+rwX ~/.hermes/cron/output/` and `chown -R $USER:$USER ~/.hermes/cron/output/`. Rare but happens after manual file moves.

### 7. The cron never fires

**Signature:** no output file for the expected run, no error reported.

**Fix:** check `cronjob list` for `enabled: true` and `state: scheduled`. If `paused_at` is set, use `cronjob action=resume job_id=<id>`. If the schedule expression looks wrong, verify it parses (`python3 -c "from croniter import croniter; croniter('0 8 * * *')"`).

## Verifying the fix

After repairing `jobs.json`, **manually trigger a run**:

```
cronjob action=run job_id=<id>
```

This queues an immediate execution. The new output file should appear in `~/.hermes/cron/output/<job_id>/` within 1-3 minutes.

**Pitfall — `cronjob run` is asynchronous:** the call returns immediately and the new output file may not exist for 60-180 seconds. Don't poll aggressively; use `cronjob list` to check `last_run_at` and `last_status`. The fix is verified when `last_status` is `ok`.

If you need a synchronous smoke-test of just the skill loading (without writing any article), you can run the agent manually with the same skills and a tiny prompt:

```
delegate_task goal="Load the <skill-name> skill and report its name. Nothing else."
```

This catches the skill-not-found case in seconds without invoking the full cron workflow.

## Don't

- **Don't `patch` jobs.json with a nested edit.** Use Python rewrite via `json.dump` to preserve indentation and validate JSON. `patch` tool will desync the inner indent.
- **Don't delete the broken job and recreate it from scratch.** Recreating resets `repeat.completed` (loses history), `created_at` (loses lineage), and the `fire_claim` token. Always edit in place.
- **Don't update the skill name in `skill` but leave `skills[0]` unchanged** — both fields are checked. The `cronjob list` output will still show the wrong name until both are updated.
- **Don't trust the error notification alone.** Always read the actual failure log. The notification says "HTTP 500"; the log says why.
- **Don't fix-and-forget on a daily cron.** If the cron has been broken for N days, those N days of articles are missing. Decide whether to backfill (delegate the missing runs) or accept the gap (and tell the user).

## Recovery from missed runs

If a daily cron has been broken for several days, after fixing it:

1. **Tell the user** which days are missing and ask whether to backfill.
2. **For backfill**, prefer one delegated task that writes all N articles in a batch over N separate cron runs — same skill pipeline, single humanizer audit, single push at the end.
3. **For accept-the-gap**, update any date-references in the footer cross-link block of the most recent existing article so the "Explore more" block doesn't point to nonexistent URLs.

## Quick diagnostic checklist (manual fallback)

If `diagnose-cron.py` is unavailable or you want to walk through it yourself:

```bash
JOB_ID="<from cronjob list>"
JOB_NAME="<from cronjob list>"

# 1. What does cronjob list say?
cronjob list | grep -A1 "$JOB_ID"

# 2. Where's the latest failure?
ls -lt ~/.hermes/cron/output/$JOB_ID/ | head -3

# 3. What does the failure actually say?
F=$(ls -t ~/.hermes/cron/output/$JOB_ID/ | head -1)
echo "=== $F ==="
grep -E "could not be found|Error|Traceback|RuntimeError" ~/.hermes/cron/output/$JOB_ID/$F | head -10

# 4. What's the job's actual config?
python3 -c "
import json
with open('/home/ubuntu/.hermes/cron/jobs.json') as f:
    data = json.load(f)
for j in data['jobs']:
    if j['name'] == '$JOB_NAME':
        print('skill:', j.get('skill'))
        print('skills:', j.get('skills'))
        print('model:', j.get('model'))
        print('provider:', j.get('provider'))
        print('schedule:', j.get('schedule'))
        print('enabled:', j.get('enabled'))
        print('state:', j.get('state'))
        print('last_status:', j.get('last_status'))
        print('last_error:', j.get('last_error'))
"

# 5. Is the skill actually installed?
ls ~/.hermes/skills/ ~/.hermes/skills/*/ 2>/dev/null | grep -i "<broken-skill-name>"
```

## Support files

- **`scripts/diagnose-cron.py`** — runnable one-shot diagnostic. Pass a `job_id` or job name; it prints a structured report (config, last_status, last_error, latest output file's failure-signature classification, and a skill-existence check for every name in `skills[]`). Exit code 0=healthy, 1=problems detected, 2=job not found. Replaces the "Quick diagnostic checklist" above for routine use.
  ```bash
  python3 ~/.hermes/skills/devops/hermes-cron-troubleshooting/scripts/diagnose-cron.py c2aefdf3bada
  python3 ~/.hermes/skills/devops/hermes-cron-troubleshooting/scripts/diagnose-cron.py daily-oriental-destiny-article
  ```
- **`references/failure-signatures.md`** — annotated excerpts from real failure logs (skill-not-found, missing-file, model-error, delivery-error, etc.) showing the exact grep patterns to recognize each. Includes the anti-pattern note: "do not diagnose from the notification alone — always read the log".
- **`references/jobs-json-schema.md`** — full schema of a job entry in `jobs.json`, with a per-field table marking which fields are read **at every tick** (edit carefully), **at creation only** (don't edit), or **daemon-managed** (never edit). Includes the atomic-write rule (always `json.dump`, never `patch`).