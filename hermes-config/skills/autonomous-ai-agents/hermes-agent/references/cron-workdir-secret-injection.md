# Cron `workdir` Secret-Injection: Reproduction & Resolution

## Symptom

Cron job fails immediately with:
```
Blocked: prompt matches threat pattern 'read_secrets'.
Cron prompts must not contain injection or exfiltration payloads.
```

The job's own prompt template is benign — no credentials appear in it.

## Root Cause

When a cron job has `workdir` set to a directory containing
`AGENTS.md`, `CLAUDE.md`, or `MEMORY.md`, the scheduler injects those
files into the system prompt at execution time. If any of those files
contain secrets (GitHub PATs, API keys, tokens, etc.), the combined
prompt is scanned by the `read_secrets` threat-pattern detector before
the LLM sees it, and the job is blocked.

This is a *runtime injection*, not visible in the stored prompt
template in `cron/jobs.json`.

## Reproduction Path

1. Create a cron job with `workdir: "/home/ubuntu/.hermes/hermes-agent"`
2. That directory contains `MEMORY.md` with a GitHub PAT and `AGENTS.md`
3. At tick time, scheduler builds the full prompt by concatenating the
   job prompt + skills content + `workdir` context files
4. The combined prompt now contains the raw GitHub PAT
5. Security scanner flags `read_secrets` pattern
6. Job blocked before any agent code runs

## Affected Jobs (2026-06-02)

| job_id | name | workdir |
|--------|------|---------|
| `fa7a29b3464e` | daily-chg-medical-news | `/home/ubuntu/.hermes/hermes-agent` |
| `c2aefdf3bada` | daily-oriental-destiny-article | `/home/ubuntu/.hermes/hermes-agent` |

Both had `MEMORY.md` (17804 bytes) injected — contained GitHub PAT.

## Resolution

**Clear the `workdir` field** on affected cron jobs:

```python
cronjob(action='update', job_id='<job_id>', workdir='')
```

The job prompt already contains all necessary GitHub repo URLs and
workflow steps. The skills (`content-research-writer-cn`,
`programmatic-seo`, `humanizer`, etc.) load from the global skills
directory and do not need a per-job `workdir`.

If the job genuinely needs file-context from a specific directory
(e.g. reading a local research file), either:
- Strip secrets from the context file before the job runs, or
- Pass the needed content as prompt variables instead of relying on
  `workdir` injection, or
- Use a dedicated clean workdir that contains no secrets

## Verification

After patching, the job's next run will not inject `MEMORY.md` / `AGENTS.md`
into the prompt. Confirm via:
```bash
hermes cron list --all
# Check the job has workdir: "" or no workdir field
```

Then let the scheduled tick run or trigger manually:
```bash
hermes cron run <job_id>
```

## Prevention

- Cron jobs that don't need per-directory context files should leave
  `workdir` empty
- If `workdir` is set, audit its contents for secrets before creating
  the job
- MEMORY.md and AGENTS.md in shared skill directories are common
  sources of this issue — they often accumulate credentials over time