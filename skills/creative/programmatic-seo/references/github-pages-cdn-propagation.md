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

## Cross-reference

- Sibling pitfall: "`sleep N && curl` 60-second foreground timeout" (covered in main SKILL.md)
- Sibling pitfall: "Cron iteration cap hit BETWEEN local commit and `git push`" — the 07-04 case is the OPPOSITE failure mode (push succeeded, verify lagged). Recovery recipes apply in reverse.
- Sibling pitfall: "Remote `origin/master` can advance between cron runs" — on 2026-07-04 the chinahospitalsguide remote was 8 commits ahead (a 43-page SEO batch). `GIT_EDITOR=true git rebase origin/master` was the clean recipe.
