# Site Audit Signals — cheap health checks before major content work

(verified 2026-07-01, chinahospitalsguide.com)

A **site audit** is the right next step when:
- User says "网站运营这么久，就目前而言" (site has been running for a while, where do we stand)
- User asks for improvement directions without specifying what to fix
- A matrix overhaul is being planned and you need to know what's already on disk
- Periodic (quarterly?) health check on production sites

The audit should run BEFORE recommending improvements, so recommendations are grounded in actual numbers — not generic advice. Cheap audit takes 5-10 tool calls and surfaces 80% of the issues.

## The 5-call audit recipe

```bash
# 1. Article inventory + freshness (1 call)
ls blog/ | wc -l
ls news/ | wc -l
find . -maxdepth 2 -name "*.html" -not -path "./api/*" | wc -l

# 2. Sitemap health (1 call)
wc -l sitemap.xml
grep -c "<url>" sitemap.xml
grep -E "^\s*<priority>" sitemap.xml | sort | uniq -c | sort -rn

# 3. Internal link distribution (1 call) — where does the homepage point?
curl -s https://<site>/ | grep -oE 'href="[^"]+\.html"' | sort -u
curl -s https://<site>/blog/ | grep -oE 'href="[^"]+\.html"' | sort -u

# 4. Git log: who's been writing recently (1 call)
git log --since="30 days ago" --oneline | head -20

# 5. Existing pillar / slug overlaps (1 call)
ls blog/ | grep -E "<your-topic-keyword>"
git log --oneline -- "blog/*<your-topic-keyword>*"
```

**Total: 5 calls, ~30 seconds.** Output tells you:

- Article count and section distribution (content audit)
- sitemap URL count and priority distribution (technical SEO)
- Internal link targets from homepage and blog index (orphan-page detection)
- Recent commit activity (who/what is being edited now — important for slug-collision pre-flight before new pillar content)
- Pillar-page collisions on the topic you want to write about (avoid duplicate content)

## What each signal typically reveals (verified 2026-07-01 chinahospitalsguide.com)

| Signal reading | What it means | Action |
|---|---|---|
| `curl https://<site>/ \| grep -oE 'href="[^"]+\.html"' \| sort -u \| wc -l` returns <10 | Homepage is over-concentrated on a few pages | Add "popular content" cards, "recent articles" module, "by category" nav |
| `curl https://<site>/blog/ \| grep blog/.*html` returns <10 internal links | Blog index is a thin shell — readers can't navigate the corpus | Rebuild blog index with category filter + recent + popular modules |
| `git log --since="30 days ago" --oneline \| wc -l` >30 | High commit velocity (multiple agents/cron writing) | **Always do slug pre-flight** before adding new pillar content; collisions are likely |
| `grep -lE "<topic H1>" blog/*.html \| wc -l` >1 | Multiple files claim the same topic | Read all matches, pick canonical, delete or redirect the duplicates |
| `sitemap.xml` priority distribution heavily skewed to 1.0 | New content over-promised to Google | Re-balance to site convention (news=0.6, blog=0.8, pillar=1.0) |
| News articles >50 and trending toward "X country X news — How Does China Compare?" template | Site is becoming a translation bureau instead of an authority | Reframe cron prompt toward own-voice topics (verify `content-research-writer-cn`'s 内容主题方向 section) |
| TCM/中医-related content covers <10% of total articles on a medical-tourism-China site | The site's biggest differentiation is under-represented | Add TCM matrix (the 2026-07-01 fix) |

The 2026-07-01 chinahospitalsguide audit surfaced (in 7 calls):

1. **News section has 78 articles** — heavy.
2. **Blog has 95 articles** — well-stocked.
3. **sitemap.xml has 233 URLs** — healthy.
4. **Homepage links to only 1 blog article** — orphan-page problem at the index.
5. **`blog/index.html` lists only 2 internal links** — the index page is essentially empty.
6. **Two competing pillar pages existed for the "China unique medical procedures" topic** — duplicate-content emergency (see content-matrix-overhaul.md pitfall).
7. **TCM appeared in only 3 of 95 blog articles** — the site's biggest differentiation was under-represented.

Items 4, 5, 6, 7 directly informed the 2026-07-01 matrix overhaul (which added 11 pillar pages, augmented 49 existing articles with TCM sections, and refactored the cron prompt). The audit took 7 calls; the alternative (working blind from generic advice) would have shipped the matrix with the duplicate-content bug intact.

## Quarterly audit cadence (recommended)

For a site with daily cron publishing:
- **Monthly**: 3-call health check (article count + sitemap count + homepage link audit)
- **Quarterly**: full 7-call audit + comparison vs. last quarter
- **Ad-hoc**: before any major content investment (matrix overhaul, redesign, category launch)

The cheap 3-call health check is the value-extracting habit — it catches the slope changes early (e.g., duplicate content showing up, sitemap growth rate declining, orphan pages accumulating) without the cost of a full audit.

## When NOT to use the audit

- Already did the audit within the last 30 days — trust the previous numbers, re-audit only if commit velocity changed
- User explicitly asks for a single specific improvement (e.g. "rewrite homepage hero") — don't burn 5 calls auditing, just do the work
- Site is brand new (<10 articles) — there's nothing to audit, just write
