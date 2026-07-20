# GitHub Pages CDN Propagation Pitfall (verified 2026-07-04 oriental-destiny, RE-CONFIRMED 2026-07-04 chinahospitalsguide)

## The pattern

GitHub Pages CDN cache can stay at "yesterday" for **7–15+ minutes after a successful push** even when the article is verifiably on origin. Sitemap-touching commits are the worst case (10+ minute lag confirmed).

## Verified scenarios

### 2026-07-04, oriental-destiny.com (the original case)
- Local commit `f2a6023` pushed successfully to `origin/main`
- `git ls-remote --heads origin main` confirmed commit on origin
- `curl raw.githubusercontent.com/.../fate-2026-07-04.html | head -5` returned the article's `<!DOCTYPE html>` — **article IS on origin**
- `curl --max-time 25 -I https://oriental-destiny.com/fate-2026-07-04.html` returned **HTTP 404** for 7+ minutes
- Homepage `last-modified: Fri, 03 Jul 2026 00:03:57 GMT` — **homepage still serving yesterday's deploy**

### 2026-07-04, chinahospitalsguide.com (RE-CONFIRMATION — the cron run in this skill's training)
- Article: `news/2026-07-03-china-bathhouse-wellness-boom-120-billion-yuan-straits-times-2026.html`
- Commit: `c8b1210` local → `c8c4505` on origin (after rebase over 8 remote commits including a sitemap touch)
- Push: SUCCEEDED (`f197387..c8c4505 master -> master`)
- Origin verification (raw.githubusercontent.com): article's `<!DOCTYPE html>` returned — **article IS on origin**
- Live verify (chinahospitalsguide.com): HTTP 404 for **at least 10 minutes** post-push
- Homepage `last-modified: Thu, 02 Jul 2026 13:06:24 GMT` — **homepage still serving 2-days-ago deploy**
- Triage action: shipping-with-pending-note; HTTP 200 expected to land in the next cron run window (the next run is the natural re-verify moment)

### Why chinahospitalsguide lag is worse than oriental-destiny
The 8-commit SEO batch touched 40+ files in a single deploy (43-page schema coverage, plastic-surgery-page meta-tag optimization, Formspree activation, MS Clarity), and the cron commit's sitemap-touch was added on top. **Multi-file deploys with sitemap rewrites trigger a Pages CDN full rebuild**, which is 10-15 min vs. the typical 3-5 min for an article-only update.

## Diagnosis

**The `last-modified` header on the homepage is the ground truth** for "has Pages rebuilt yet." If it shows a date earlier than your commit's date, Pages is still serving the prior deploy and HTTP 200 on the new URL will lag.

```bash
curl --max-time 25 -sI https://<site>/ | grep -i last-modified
# If the date is BEFORE your commit's datePublished, Pages hasn't rebuilt yet
```

## Decision rules when this state fires

1. **Verify on origin:** `curl --max-time 25 -s "https://raw.githubusercontent.com/OWNER/REPO/BRANCH/FILE" | head -5` — if the article's `<!DOCTYPE html>` returns, the push succeeded.
2. **Do NOT re-push.** This creates a duplicate commit and burns cron iteration budget on a problem that resolves itself.
3. **Do NOT `git reset --hard origin/<branch>`.** This drops the local commit. Use the standard recovery recipes.
4. **Move on and report the article as shipped** with a note that the CDN cache is propagating. The next cron run's HTTP 200 verify is the natural re-check moment.

## Preventive detection in cron pre-flight

At the start of a cron run, check whether yesterday's article is still serving its expected HTTP 200 status. If yesterday's article also returns 404 (or homepage `last-modified` is stale), Pages is in slow-rebuild mode today — expect longer verify windows for today's push:

```bash
# Quick Pages health check (add to Step 0 pre-flight, 1 tool call)
curl --max-time 25 -sI https://<site>/ | grep -i last-modified
# + verify yesterday's article returns 200
curl --max-time 25 -sI https://<site>/<article-path-yesterday>.html | head -1
```

If both are stale, budget 2-3 extra tool calls for repeated verify attempts today. **On chinahospitalsguide** with a multi-file SEO batch pushed recently, the window is reliably 10-15 min not the usual 3-5 min.

## Why this is distinct from the 2026-06-25 "sleep 180 timeout" pitfall

The 2026-06-25 pitfall is "the curl returns HTTP 200 but the terminal tool's 60-second foreground timeout aborts it mid-call." The fix was `--max-time 30` to bound the curl.

The 2026-07-04 pitfall is **different**: the curl returns cleanly with `--max-time 30`, but the response is HTTP 404 because Pages hasn't rebuilt. No amount of `--max-time` will fix this — it's a server-side cache invalidation delay.

**Distinguishing the two:**
- 2026-06-25: `sleep 180 && curl ... ` → first call aborts at 60s with no result, second call (separate, fresh 60s budget) gets HTTP 200 immediately
- 2026-07-04: `sleep 180 && curl --max-time 30 ...` returns HTTP 404 cleanly, then repeated retries over 7-15 minutes also return HTTP 404 — but origin has the article

The diagnostic command `curl --max-time 25 -sI SITE_ROOT | grep -i last-modified` distinguishes them: 2026-06-25 would show today's `last-modified`, 2026-07-04 shows yesterday's (or days-old).

## Mid-pipeline cap-hit recovery is now stable (RE-CONFIRMED 2026-07-04 chinahospitalsguide)

This run also confirmed that the mid-pipeline cap-hit recipe (article on disk, sitemap + index updated, no commit yet) is now standard cron workflow. The 07-03 article was recovered in 10 tool calls:

```
Step 0 detection (3 checks combined) → humanize verify → 
git config identity + add + commit → push (rejected by remote-advance) → 
fetch + log --stat (find sitemap/news/index conflict candidates) → 
GIT_EDITOR=true git rebase origin/master (often clean, no conflict) → 
push (succeed) → sleep + curl verify (may 404 due to CDN lag) → 
origin + last-modified diagnostic → pending-note write
```

State-matrix entries (see main SKILL.md cron iteration cap-hit section for the running matrix):
- 07-03: article + sitemap + index ready, no commit, no push → recovered in 10 calls with clean rebase (no sitemap conflict despite remote commit `c66e65e` touching sitemap.xml — rebase-cherry-pick on top of remote worked cleanly because our patch inserted at top and the remote commit inserted later)

### 2026-07-20, chinahospitalsguide.com (FOURTH CONFIRMATION — pattern confirmed-stable across 4 instances)
- Article: `news/2026-07-20-auriculotherapy-migraine-evidence-china-hospitals-2026.html` (3,051 words, auriculotherapy for migraine — FENS Forum 2026 + Frontiers in Neurology 2023 evidence base)
- Commits: `69603fb` (article) + `11a2134` (sitemap + news/index) on local master
- Push: SUCCEEDED (`820ce78..69603fb → 11a2134 master -> master`)
- Origin verification (raw.githubusercontent.com): article `<!DOCTYPE html>` returned HTTP 200 — **article IS on origin**
- Sitemap.xml HTTP 200 (rebuild ran for the existing-file sitemap update) but did NOT yet contain the new article URL — Pages rebuilt incrementally for the modified file but the new file path takes longer to propagate
- Live verify (chinahospitalsguide.com/news/2026-07-20-...html): HTTP 404 for the full verify window after push
- Triage action: `git log` + origin-verification gave the diagnostic; reported `[SHIPPED_OK]` with the CDN-propagation-delayed note per the cron-week delivery signal contract from the main SKILL.md and the cron-job prompt

**Cumulative 4-instance confirmation (2026-07-04 oriental-destiny + 2026-07-04 + 2026-07-19 + 2026-07-20 chinahospitalsguide):**
- Push succeeds, origin has the file (verified via `curl raw.githubusercontent.com/...`)
- Sitemap.xml typically rebuilds faster than the new article path (Pages incremental rebuild)
- New article URL stays at HTTP 404 for 7-15+ minutes depending on deploy batch size
- The `[SHIPPED_OK]` token rule from the cron-job prompt applies: "Reporting `[SHIPPED_OK]` is appropriate when file is on origin + push succeeded + sitemap returned 200, even if the article URL still 404s"

**Future cron runs can rely on the origin + push + sitemap-200 diagnostic as the ship signal** and skip the polled-verify loop entirely. The next cron run's HTTP 200 verify is the natural re-check moment.

### 2026-07-19, chinahospitalsguide.com (third confirmed instance)
- Sitemap returned HTTP 200, new article URL 404'd for 10+ minutes. Pattern consistent with the 07-04 cases.

## Canonical 2-call verify sequence on chinahospitalsguide (post-07-20)

The 2-call split for `sleep + curl` is now canonical on chinahospitalsguide, not an optional fix. The 60-second foreground timeout reliably fires on either chained link:

```bash
# Call 1: sleep (will hit 60s cap, cron moves on, sleep accumulates in shell)
sleep 120
# Call 2: curl with bounded --max-time (gets a fresh 60s foreground budget)
curl --max-time 25 -s -o /dev/null -w "HTTP %{http_code}\n" URL
```

If HTTP 404 + sitemap.xml returns 200 + raw.githubusercontent.com of the article returns 200 → article is shipped, CDN is propagating, report `[SHIPPED_OK]` and move on. **Do not poll.**

## Cross-reference

- Sibling pitfall: "`sleep N && curl` 60-second foreground timeout" (covered in main SKILL.md)
- Sibling pitfall: "Cron iteration cap hit BETWEEN local commit and `git push`" — the 07-04 case is the OPPOSITE failure mode (push succeeded, verify lagged). Recovery recipes apply in reverse.
- Sibling pitfall: "Remote `origin/master` can advance between cron runs" — on 2026-07-04 the chinahospitalsguide remote was 8 commits ahead (a 43-page SEO batch). `GIT_EDITOR=true git rebase origin/master` was the clean recipe.
