---
name: cron-content-pipeline-cap-safe
description: "Reference pattern for cron-driven content publishing (news/blog/articles) when the cron agent hits a tool-call iteration cap mid-pipeline. Covers commit-before-humanize ordering, recovery-via-script separation, and the failure mode where the skill's own recovery recipe loops forever."
version: 1.0.0
author: Hermes Agent
platforms: [linux]
metadata:
  hermes:
    tags: [cron, content-pipeline, cap-hit, recovery, git, publishing]
    category: devops
---

# Cron Content Pipeline: Cap-Safe Patterns

Companion reference for any skill that drives a daily cron job producing articles / blog posts / news posts and pushes them via git to a static-site repo (GitHub Pages, Cloudflare Pages, etc.). The pattern originated from `content-research-writer-cn` after 10 documented mid-pipeline cap-hits in 2 months, but it generalizes to any "write file → humanize → commit → push → verify" pipeline.

## When to load

- A cron job writes content to disk and publishes via git
- The job has hit "mid-pipeline cap-hit" failures (article written but uncommitted, or article not even written)
- The skill's own recovery recipe says "next cron run should pick this up" — and it doesn't, repeatedly
- The cron prompt budget for `humanizer` patches is eating the budget for `git commit + git push`

## The core failure mode

The classic order in human-friendly pipelines:

```
research → write → humanize loop (3-10 patches) → commit → push → verify
```

Every step is reasonable in isolation. The combined pipeline burns 25-40 tool calls. The cron iteration cap fires during humanize. Article is on disk, uncommitted. Cron exits with error. Next day's cron tries to recover the article, but **the cron that just failed has the freshest context about WHY it failed**, and the next cron doesn't have the budget to research + recover + ship a NEW article in the same run.

This is the 10x failure pattern observed in `content-research-writer-cn` 2026-06-14 → 2026-07-05. Every cap-hit entry in the skill's recovery section says "next cron run should do X" — and the next cron run **never has budget to do both recovery and a fresh article** in the same 30-call budget.

## The fix: cap-safe ordering

Reorder the pipeline so the deterministic plumbing (commit + push) happens BEFORE the open-ended refinement loop (humanize):

```
Step 0: recovery check (1 call) — git status + ls news/$(date).html
Step 1: research (3-5 calls)
Step 2: source fetch (1-2 calls)
Step 3: write article to disk (1 call, write_file)
Step 4: COMMIT + PUSH IMMEDIATELY (3 calls) — even if score is 50/100
Step 5: update sitemap + index + commit + push (2 calls)
Step 6: humanize POST-HOC, single pass only (1-2 calls)
Step 7: verify HTTP 200 (1 call)
```

**Total budget: ~15 calls** (vs 30+ in the old order). Worst-case cap-hit now loses only the post-publish polish, never the publish itself.

### Hard rules

- **NEVER** run a multi-round humanize loop before the first commit. One pass max.
- **NEVER** block the pipeline on humanize score ≥X. Ship at ≥60, polish later.
- **ALWAYS** have a Step 0 recovery check at the top of the cron prompt. If yesterday's article is on disk uncommitted, push it before starting new work.
- **ALWAYS** end Step 4 with `git push` returning success, not just `git commit`. An unpushed commit is the same failure mode.

## The recovery-recipe antipattern

If a skill's "recovery recipe" says:

> "The next cron run should detect this state with `git status` and JUST push + verify, NOT start fresh research"

…that recipe is broken by design. The next cron run has 30 calls of budget, and pushing the recovered article takes 5 of them. That leaves 25 for a fresh article — usually not enough. **A recovery recipe that the next run can actually execute must fit in ≤5 calls**, or it must be split into a separate cron job (see below).

## Alternative: split recovery into a separate cron job

If a skill's pipeline is too complex to fit in the cap-safe ordering above, split it:

- **Cron A (writes):** research + write + commit + push. No humanize loop, no recovery logic.
- **Cron B (polishes, runs 60-90 min after A):** detects uncommitted polish work OR low-scoring recent articles, runs a single humanize pass, commits + pushes.
- **Cron C (recovers, runs daily at low-traffic hour):** scans for uncommitted files in the article directory, pushes them. No research, no writing. Idempotent.

This pattern is used by some production sites where the main writer cron only does what fits in 15 calls. Cron B and C can be `no_agent=true` shell scripts (3-5 lines each).

## Concrete cron prompt template

Add this block to the cron prompt's "## Workflow" section, replacing any "research → write → humanize → publish" sequence:

```
## Workflow (CRITICAL — cap-safe order)

Commit + push must happen BEFORE the humanize loop. Do not wait for "polished to 90"
before publishing. Ship the 60-point version first, polish later. The 10 documented
mid-pipeline cap-hits in this skill all followed the same pattern: write to disk →
humanize multi-round patch → cap fires before commit → next day tries to recover.

Fixed order, per-step call budget:

1. Step 0 — Recovery check (1 call): `git status` + `ls news/$(date +%Y-%m-%d)-*.html` + `ls references/pending-*.md`
   - Uncommitted article + modified sitemap + modified index → commit + push + done
   - Pending file but no article → use the pending recipe, jump to Step 4
   - Otherwise → normal flow

2. Step 1 — Research (3-5 calls): Bing News → 2-3 candidates → de-dup grep → pick 1

3. Step 2 — Source fetch (1-2 calls): fetch + extract body

4. Step 3 — Write article (1 call): write_file to `news/YYYY-MM-DD-<slug>.html`

5. ⭐ Step 4 — Commit + push IMMEDIATELY (3 calls), do NOT wait for humanize:
   - `git add news/YYYY-MM-DD-<slug>.html` + commit + push
   - On push rejection: `git fetch && git pull --rebase && git push`
   - This step must complete before any humanize work. Ship the unpolished version.

6. Step 5 — Sitemap + index update (2 calls): patch both, commit, push

7. Step 6 — Humanize POST-HOC (1-2 calls, optional): quick banned-words scan
   (furthermore/leverage/robust/seamless/navigate) + em-dash count. If ≥60 already, skip.

8. Step 7 — Verify (1 call): `sleep 75 && curl --max-time 25 ... HTTP 200`

Total budget ~15 calls. Worst-case cap-hit loses only the post-publish polish.

DO NOT:
- Run more than 1 round of humanize patches (max 2 substitutions)
- Wait for humanize score ≥X before pushing
- "Polish to perfection then publish"
```

## What to capture when a cap-hit happens anyway

After a cron run fails with cap-hit and the article needs manual recovery, log it under `references/cron-cap-hit-log.md` in the parent skill. Required fields:

- Date, cron job_id, run_id
- Failure phase (research / writing / humanize / commit / push / verify)
- Pipeline position: what was on disk, what was modified, what was untracked
- Tool-call count at cap (if visible in cron output)
- Article score if humanize completed
- Recovery recipe that actually worked (manual intervention or next-cron)
- Total elapsed time from cron start to error

This log is what makes the pattern **detectable**: after 3 cap-hits in the same phase within a month, that phase needs reordering.

## See also

- Parent skill: `content-research-writer-cn` (the original site of this pattern, v1.1.9+)
- Parent skill's cap-hit log: `content-research-writer-cn/references/cron-cap-hit-log.md` (running table of cap-hits + phase taxonomy + 3-in-30-days trigger rule)
- Sibling reference: `~/.hermes/memories/DETAIL/facts-tech-basics.md` for general git + cron recovery facts

## Why this is a separate umbrella

`content-research-writer-cn` is a site-specific skill (medical tourism news for chinahospitalsguide.com). The cap-safe ordering pattern generalizes to ANY cron-driven content publishing pipeline — blog posts, podcasts, social media drafts, README updates, anything where the cron agent writes a file and pushes via git. Keeping it separate means:

- Future site-specific skills (e.g. `blog-writer-english`, `newsletter-daily`) can reference this pattern without copy-pasting it
- The recovery-recipe antipattern warning is preserved in one place even if the source skills get consolidated
- A new cron job that hits the same failure mode can be diagnosed against this skill before reading 700KB of site-specific skill history