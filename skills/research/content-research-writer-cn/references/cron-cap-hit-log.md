# Cron Cap-Hit Log (chinahospitalsguide)

Running log of mid-pipeline cap-hits and recoveries for the `daily-chg-medical-news` cron (job_id `fa7a29b3464e`). The PURPOSE of this file is to detect when the same failure mode recurs 3+ times in a month — that is the signal to apply a structural fix (see `cron-content-pipeline-cap-safe` skill), not to add another "next cron recovers" recipe.

## Failure-mode taxonomy

The cap-hit can fire at different phases. Each phase has different recovery cost:

| Phase | Tool calls burned | Recovery cost | Worst case |
|---|---|---|---|
| A. During research | 5-15 | High — re-research needed | Whole day lost |
| B. During writing | 10-20 | Medium — article fragment on disk | Partial day lost |
| C. During humanize loop | 20-35 | Low — article complete, just unpolished | Day's article present, score low |
| D. After humanize, before commit | 30-40 | Very low — just `git add && commit && push` | One-day delay |
| E. After commit, before push | 35-45 | Very low — just `git push` | One-day delay |
| F. After push, before HTTP verify | 45-50 | Trivial — just `curl` | One-day delay |

Phase C and D are the most common failures (10 of 12 documented hits). Phase C is the one this skill's recovery recipe "solved" by deferring to the next cron — which has now demonstrably failed 10x.

## Historical hits

| Date | Phase | Score on disk | Recovered by | Notes |
|---|---|---|---|---|
| 2026-06-14 | E | n/a (post-commit) | Next cron, single push | First documented case. Recovery worked because phase was E (trivial). |
| 2026-06-16 | A | n/a (no article) | Pending file handoff | Bing News recipe broken that day. |
| 2026-06-17 | D | 90/100 | Manual intervention | Akeso AK138D1 article, 4701 words, complete on disk. |
| 2026-06-21 | D | n/a | Manual intervention | Pattern started repeating. |
| 2026-06-28 | D | n/a | Manual intervention | Same pattern. |
| 2026-07-02 | D | n/a | Manual intervention | Acupuncture IVF article. |
| **2026-07-04** | **D** | **~85/100** (estimated) | **Manual intervention 2026-07-05** | **Electroacupuncture post-stroke dysphagia. Pushed by Hermes (not cron recovery).** |
| 2026-07-05 | A | n/a (no article) | No recovery — day lost | Bing News ran but never reached writing. |

## Trigger rule

After **3 cap-hits in the same phase within 30 days**, that phase requires structural fix (reorder pipeline, reduce work, or split into a separate cron). The 06-17/06-21/06-28/07-02/07-04 sequence (5 hits in phase D across 18 days) crossed this threshold on 2026-07-02. The fix was applied on 2026-07-05.

## What "structural fix" looks like in this skill

The 2026-07-05 fix:

1. Workflow reordered: Step 4 = `commit + push IMMEDIATELY after write_file`, before any humanize work.
2. Humanize loop budget capped: 1 round, max 2 substitutions.
3. Step 0 added: recovery check (if previous day's article is uncommitted, push it before starting new work — ≤5 calls).
4. Total budget target: ~15 calls (vs 30+ before).

Re-evaluate this log on 2026-07-15. If 2+ more cap-hits fire after the fix, the fix is insufficient — split write+humanize into two separate cron jobs (write cron at 09:00, humanize cron at 10:30, recovery cron at 11:00). See `cron-content-pipeline-cap-safe` for the split pattern.

## See also

- Parent skill: `content-research-writer-cn`
- Pattern reference: `cron-content-pipeline-cap-safe` (full cap-safe ordering + cron split pattern)