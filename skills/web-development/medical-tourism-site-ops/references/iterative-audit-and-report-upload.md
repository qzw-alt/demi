# Iterative SEO audit + report-upload workflow (NEW 2026-07-22)

This file captures a repeatable pattern that emerged when Weiye asked *"再查看一下 看看情况"* after the first audit. It complements `references/session-2026-07-21-lessons.md` §B (the one-shot `audit.py` recipe) by adding what happens on the **second** and subsequent runs.

## When this pattern triggers

Any time the user says:

- "再查看一下 看看情况"
- "处理过了一下 你现在再查看一下"
- "在审查一遍" / "再审一轮"
- Or after they say "我改了一些" / "我处理了一下"

— the right move is **iterative audit**, not a from-scratch site re-scan. The artifacts in `~/.hermes/tmp/audit/` from the previous run are reusable; do NOT re-fetch + re-classify from scratch unless explicitly asked.

## The 6-step iterative loop (verified 2026-07-22)

### 1. Re-run `audit.py` against the live site

```bash
~/.hermes/hermes-agent/venv/bin/python /home/ubuntu/.hermes/tmp/audit/audit.py
```

Inventory is fresh data (sitemap may have new URLs since last run; e.g. session saw 236 → 273 = +37 new pages). Report writes to the same path as before; **don't overwrite the previous report first** — the comparison step needs both.

### 2. Capture old report before overwriting

```bash
cp /home/ubuntu/.hermes/tmp/audit/audit-report.md \
   /home/ubuntu/.hermes/tmp/audit/audit-report-2026-07-21-baseline.md
```

Or whatever date stamp matches the previous run. Naming convention I've settled on:

- `audit-report.md` ← current run (overwritten each time)
- `audit-report-YYYY-MM-DD-baseline.md` ← frozen snapshots for delta comparison

Keep the baselines in `/home/ubuntu/.hermes/tmp/audit/` (NOT in the project repo — these are operational artifacts, not user-facing).

### 3. Compute the delta — what changed, what regressed

The pattern that surfaced:

| Metric | Last | Now | Direction |
|---|---|---|---|
| HEALTHY | 212 | 226 | ↑ +14 |
| NO_SCHEMA | 6 | 17 | ⚠️ +11 |
| THIN | 4 | 22 | ⚠️ +18 |
| TOO_SHORT | 8 | 8 | = |
| BROKEN | 6 | 0 | ✅ -6 |
| Total URLs | 236 | 273 | ↑ +37 |

The wins BROKE=0 deserve celebrating (Weiye's edit fixed the 6 broken pages). The losses THIN=22 and NO_SCHEMA=17 deserve flagging — these are regressions caused by **adding 37 new pages that are mostly thin**, which is a content-quality problem the cleanup alone can't solve.

**Always run this delta table**, not just one snapshot. The user's "did the cleanup work?" question only makes sense as a delta.

### 4. Pull category-level deltas, then add a "key finding" callout

Three things must be visible up front:

1. **What got better** (e.g. "BROKEN 6 → 0")
2. **What got worse** (e.g. "THIN +18 — new pages are mostly thin")
3. **What stayed** (e.g. "TOO_SHORT 8 → 8")

…plus at least one **root-cause hypothesis** for the regressions. Don't just say "things got worse"; tell the user the *why*.

For the 07-22 audit, the root-cause hypothesis that turned out to be right:
- "Weiye added 37 new pages between audits"
- "Most of the new pages are <400 words (thin)"
- "Several new pages didn't get any schema block"
- → **Treatment: tighten the page-creation quality gate (≥800 words + schema or don't publish)**

### 5. Generate the delta-aware report (Markdown)

Copy the previous report's skeleton + replace the totals with the delta table, keep the per-URL detail unchanged or trimmed.

Critical UX rule: **keep both reports linkable** in the report header so the user can flip between them without re-asking.

```markdown
**Latest audit** (2026-07-22, 跟上次对照):
[URL to latest]

**上次 audit** (2026-07-21, 基线):
[URL to baseline]
```

### 6. Upload to `qzw-alt/demi` `reports/chinahospitalsguide/` and report GitHub links

Pattern that works (verified 2026-07-22):

```bash
REPO=demi; cd /tmp; rm -rf demi-final 2>/dev/null
git clone --depth 1 git@github.com:qzw-alt/$REPO.git demi-final
mkdir -p demi-final/reports/chinahospitalsguide
cp /home/ubuntu/.hermes/tmp/audit/audit-report.md \
   demi-final/reports/chinahospitalsguide/audit-YYYY-MM-DD-topic.md
cd demi-final
git add reports/chinahospitalsguide/audit-YYYY-MM-DD-topic.md
git commit -m "docs(audit): <site> unindexed-pages audit (YYYY-MM-DD, follow-up)

- N URLs scanned (vs M last audit = +K new pages)
- HEALTHY: X → Y (+Z) — old cleanup landed
- BROKEN: A → B — fully resolved
- BUT: THIN C → D (+E), NO_SCHEMA F → G (+H)
- 1 new duplicate-content group emerged
- Net: structural quality up, content quality regressing on new pages"
git push origin master
cd /tmp; rm -rf demi-final
```

Naming convention: `audit-YYYY-MM-DD-<short-topic>.md` (`-baseline` suffix only on the frozen reference snapshot, not for uploaded reports to demi). The `audit-2026-07-21-unindexed-cleanup.md` and `audit-2026-07-22-unindexed-cleanup.md` pair is the canonical example.

## Things to NOT do on the second audit (anti-patterns)

- ❌ Don't re-fetch + re-classify from scratch without preserving the previous baseline first. The delta is the value.
- ❌ Don't promise "fully automated cross-check" against GSC exclusion data — see the parent SKILL.md pitfall (Step 2) added 2026-07-22. `~/.hermes/bin/gsc --help` returns 8 subcommands, none of which can list "why pages aren't indexed".
- ❌ Don't suggest a single "fix the schema bug" for ALL 17 NO_SCHEMA pages — split into cohorts:
  - 3 `report-carlos-*` programmatic report pages → add `<meta name="robots" content="noindex">` instead of schema (these aren't SEO targets)
  - Other 14 → add JSON-LD + audit one by one
- ❌ Don't pre-pick a scope to ask the user about without first doing the inventory. The user expects "what's the situation now" not "what shall we do".

## Edge case — when the data contradicts the previous plan

On 07-22, the conversation had a 6-week cleanup+content plan from 07-21. The 07-22 audit showed **the new pages added since 07-21 are themselves the THIN problem** — i.e. the cleanup plan's Week 1 "make 25-30 changes" was good, but **didn't prevent new thin pages from being published**. The conclusion isn't "abandon the plan" — it's "add a quality gate (wordcount + schema check) before next batch".

Frame the inconsistency this way: plan + new data → refined plan, not "plan was wrong".

## Files

This skill file replaces the one-shot pattern in `references/session-2026-07-21-lessons.md` §B for any task >1 audit iteration. For the very first audit on a project, use the §B recipe. For the 2nd+ iteration, use this file.

## Verification checklist before saying "audit done"

- [ ] `audit.py` ran without error and produced a new `audit-report.md`
- [ ] Previous baseline is preserved (NOT overwritten) so the diff is reproducible
- [ ] Delta table is in the report header (Last vs Now vs Direction)
- [ ] Root-cause hypothesis is attached for every regression
- [ ] Report uploaded to `qzw-alt/demi` `reports/chinahospitalsguide/` and `git push` returned 200
- [ ] Both old + new report URLs surfaced in chat response
- [ ] User knows which pages are still actionable (next session decision)
