# Content Matrix Overhaul (verified 2026-07-01, chinahospitalsguide.com)

A **content matrix overhaul** is the right pattern when the user wants to (a) restructure a content site around a new thematic axis, (b) build a pillar-page cluster (1 master page + N sub-pages), or (c) inject a standardized section (e.g. "China-specific advantage," "TCM/acu Section," "Risk Disclosure") into many existing articles at once.

This is distinct from daily cron article publishing — the goal is **structural rewrite of an existing content corpus**, not just one new article.

The verified pattern (chinahospitalsguide.com, 2026-07-01) had **11 pillar pages built + 49 existing articles augmented + 1 cron prompt rewritten** in a single session:

- 11 new pillar pages (1 master + 10 sub-pages, 1,200-5,200 words each)
- 49 existing blog articles augmented with category-specific TCM/acupuncture/integrated-medicine sections
- 1 daily cron prompt updated to surface the new thematic axis (TCM-priority + 3 article templates)
- sitemap.xml updated (+11 URLs), git commit → pull --rebase → push → verify HTTP 200 × 15 URLs
- Total tool-call budget: ~80 calls across 5 phases

## When this pattern fits

- User says "build out the [topic X] angle" / "make [topic Y] the main content line"
- User says "fill the [topic X] gap" / "add [section Z] to every relevant article"
- Site has 30+ existing articles on related topics and the user wants them all to surface a new angle
- Daily cron is running on a generic theme and the user wants a one-time structural rewrite to bias future crons toward a new axis

## When NOT to use this pattern

- Single new article — just write it
- Removing/rewriting existing content — different workflow (search-and-replace patches, not section-injection)
- Cosmetic site-wide changes (CSS, nav, theme)
- User has not explicitly authorized multi-page rewrite — confirm before starting

## The 5 phases

### Phase 1 — Theme + taxonomy (5 calls)

1. Audit current corpus: count articles in `blog/` + `news/`, sample 5-10 existing articles for template structure, list topical gaps
2. Pick a thematic axis that aligns with the site's differentiation
3. Define 3-5 pillar topics underneath the new axis. Each pillar becomes 1 master page + N sub-pages
4. Build the keyword bank: per-pillar 5-10 long-tail keywords + 5-10 site-internal anchor links

For chinahospitalsguide.com 2026-07-01: the new axis was **"中国特色医疗"** (China's unique medical procedures + integrated TCM-Western medicine), with 4 pillars (10 unique procedures, integrated TCM-Western, acupuncture, Hainan Boao Lecheng). The 10 unique-procedures pillar became 1 master + 10 sub-pages.

### Phase 2 — Batch pillar content via parallel subagents (30-40 calls)

1. Write the master page first (1 aggregation article, ~2,000 words). This anchors the cross-linking graph
2. Dispatch N subagent tasks (`delegate_task` with `tasks=[]`, **max 3 concurrent**) to write the N sub-pages in parallel
3. Each subagent gets:
   - The article spec (title, meta, structure, content outline, internal-link target list)
   - The reference doc (if any)
   - The site template (path to read — e.g. `blog/cataract-surgery-china.html`)
   - The canonical link list (real existing files only, no fabrication)
4. Subagent returns: file path + word count + internal-link count. Verify the output (read 5 lines of each file) before moving on.

### Phase 3 — Section-injection mode (10 calls)

The verified technique for batch-augmenting 50+ existing articles with a single standardized section. Worked example: TCM section into 49 disease/procedure blogs.

```python
# 1. Classify articles into categories via filename keyword match
# 2. Write 1 HTML template per category
# 3. Inject at the right insertion point per article (multi-marker fallback)
```

Key technical patterns:

- **Multi-marker insertion fallback**: every article has different "Related Articles" markup. Use a list of markers (regexes) and pick the first that matches, in this order:
  1. `<h3[^>]*>\s*📚\s*Related Articles` (chinahospitalsguide convention)
  2. `<h3[^>]*>\s*📚\s*Related Reading`
  3. `<h2[^>]*>[^<]*Related Articles`
  4. `<h2[^>]*>[^<]*Related Reading`
  5. `<h2[^>]*>[^<]*You Might Also Like`
  6. `<h2[^>]*>[^<]*You may also like`
  7. Last-resort: `</div>\s*\n?\s*</body>` or `</div>\s*\n?\s*<footer` — places section right before article close, still validates
- **Idempotency check** — before each injection, grep for the section's marker text to avoid double-injection. UTF-8 emoji check: `b'\xf0\x9f\x8c\xbf' in content_bytes` (🌿 = U+1F33F). Pre-checking avoids a class of subtle bugs where re-running the script silently re-injects.
- **Category classification** — use simple keyword lists per category. ML-classification is overkill for 50-200 file corpora.
- **Skip non-target articles** — maintain a clear "skip list" with filename keywords (`hospitals-in-`, `china-vs-usa`, `medical-visa`, `how-to-see-a-doctor`).
- **Counted verification** — at the end of injection, count the section's marker byte-string across all `.html` files and confirm = expected injection count.

### Phase 4 — Cron prompt update (3 calls)

After a structural overhaul, **also update the daily cron job prompt** so future daily articles stay on-theme:

1. Read current cron prompt via `cronjob action=list`
2. Add a new "本周主题方向" section that references the matrix's axis
3. Update the template section to surface 3 specific archetypes the matrix defined
4. Run `cronjob action=update job_id=<id> prompt=<new_prompt>` — this is the highest-leverage single edit

### Phase 5 — Sitemap update + deployment (5-10 calls)

Same as the standard cron workflow: insert N new `<url>` entries into `sitemap.xml`, preserving the site's existing priority convention. Git commit → pull --rebase (often needed) → push → verify HTTP 200 on all new pages + 5 sample modified pages.

## Pitfalls (verified 2026-07-01)

**Don't fabricate content.** Subagents writing pillar pages: canonical-link list and cost numbers must come from real sources (the reference doc, the existing site, named published reports). Explicit instruction to subagents: "DO NOT fabricate hospital/department/doctor names not in the reference." Prevents plausible-looking fabricated doctor names.

**Subagents can be slow — one task may time out at 600s.** Workarounds: keep each subagent's task to ≤4 articles per dispatch; for ≥10 articles, split into ≤3-article dispatches and iterate. Always verify per-subagent output (read 5 lines + word count + internal-link count) before declaring success.

**Marker diversity in existing articles is bigger than you think.** The 2026-07-01 run hit 4 different "Related Articles" markup variants across the 49 articles. The 7-marker fallback chain handled every case, but inspect 5-10 random existing articles first to enumerate the marker space.

**Idempotency check is critical for re-runnability.** After the first run, re-running without idempotency check will double-inject the section. Use a unique marker phrase that doesn't appear elsewhere in normal prose.

**Emoji string matching in Python: pick a mode and stick with it.** Either text-mode (`'🌿 TCM' in content`) or byte-mode (`b'\xf0\x9f\x8c\xbf' in content_bytes`). Mixing the two fails on `==`. The 2026-07-01 byte-mode check inside `with open(..., 'rb')` works because the file is opened in bytes mode AND the check literal is bytes.

**Verify injection count matches expectation.** Count `(marker_byte_string in open(f, 'rb').read())` across all `.html` files at end. The 2026-07-01 run expected 49 + 3 (already-injected files) = 52 matches; got 52/52. If you get <49, some articles in the injection target list were skipped — re-check the skip-category list.

**Don't forget to update the daily cron prompt.** Highest-leverage single edit in a matrix overhaul. Without it, tomorrow's daily article doesn't reference the new axis.

**Sitemap priority matches site convention.** Different sites / different section types have different priorities. chinahospitalsguide news = 0.6-0.7, blog/evergreen = 0.8, pillar pages = 1.0. Always check `head -20 sitemap.xml` first. Inserting all new URLs at priority 1.0 is over-aggressive.

**`delegate_task` concurrency ceiling is 3.** Default `delegation.max_concurrent_children` in config.yaml caps parallel subagents at 3. Dispatching 4+ tasks in one call returns "Too many tasks" error. Workaround: split into 2 calls, each with ≤3 tasks. Each call returns within ~600s timeout for the slowest task — so budget ~10 minutes per batch of 3.

**BEFORE writing 10+ pillar pages on a topic, check git history for slug collisions (NEW pitfall — verified 2026-07-01):** when the matrix overhaul targets a topic that might already have a dedicated page, run `git log --oneline -- "blog/*<keyword>*.html"` first. The 2026-07-01 matrix created `china-unique-medical-procedures.html` as the master page — only to discover that the user (or a prior cron run) had already committed `china-unique-medical-procedures-guide.html` minutes earlier (commit `24e927c`). The two pages had the same H1, same `/china-unique-medical-procedures/` URL prefix, same topic, ~80% overlapping content → instant SEO duplicate-content penalty (Google treats both as competing for the same query and splits rank, or de-ranks both for thin/duplicate content).

**Pre-flight check sequence before dispatching subagents:**
```bash
cd blog/  # or wherever the new pages go
ls *<topic-keyword>* 2>&1
git log --oneline -- "*<topic-keyword>*" | head -5
grep -lE "<topic H1 string>" *.html 2>/dev/null
```

If ANY existing file with a near-identical slug exists, **stop and decide the canonical slug BEFORE writing**. Three options:
- **(a) Keep the existing page, delete your duplicate** (safest — preserves git history)
- **(b) Overwrite the existing page with your new content** (only when user explicitly says "I'm replacing X")
- **(c) Rewrite your new file's slug to `-v2.html` style** and update all sub-page internal links

Default to (a) — preserve older commits unless explicitly told to overwrite. The 2026-07-01 fix was option (a): delete the new page, add `_redirects` 301 entry, commit + push. ~8 calls to fix; the disaster was 1 commit history away from being permanent.

**Duplicate-content + 301 redirect recovery recipe (NEW — verified 2026-07-01):** when a pillar page is wrong and the correct page already exists, this 8-call recovery:

1. `rm blog/<wrong-slug>.html` — delete the wrong page from the local working tree
2. `cat _redirects` to see existing redirect format, then `patch` to append: `/blog/<wrong-slug>.html  /blog/<correct-slug>.html  301`. Cloudflare Pages / Netlify use **space-delimited** format (the file already had ~27 entries; match the format exactly)
3. **`git log -- "blog/<correct-slug>.html"` first** to confirm the correct page exists in git history AND has been pushed (not orphaned). If it hasn't been pushed yet, the redirect alone catches it; if it has been pushed, the 301 from Cloudflare will hit the deployed version
4. Verify all internal links in **other pages** still point to the correct URL: `grep -rE "<wrong-slug>" blog/ --include="*.html" -l`. If any non-deleted page still links to the wrong slug, fix each link to point to the correct slug. The `_redirects` 301 will catch them, but explicit fixes are cleaner and avoid the redirect indirection cost
5. `git add -A && git commit -m "SEO: remove duplicate pillar page, redirect to <correct-slug>" && git -c http.sslBackend=openssl push` (chinahospitalsguide.com requires the SSL backend flag — see Site Configurations in `references/site-configs.md`)
6. Verify the redirect works: `curl --max-time 30 -s -o /dev/null -w "%{http_code}" https://<site>/blog/<wrong-slug>.html` should return `301`. Follow the redirect chain with `curl --max-time 30 -sL -o /dev/null -w "%{http_code} %{url_effective}\n" <wrong-url>` to verify the destination returns `200`

Pin this recipe — duplicate-content emergencies will recur as more agents/cron jobs write pillar content on the same site. The 8-call cost is much cheaper than the search-rank damage from two competing pages.

## Tool-call budget table

| Phase | Target | Activity |
|-------|--------|----------|
| 1 | 5 calls | Audit + theme + taxonomy + keyword bank |
| 2 | 30-40 calls | Parallel subagents writing N pillar pages |
| 3 | 10 calls | Section-injection script (single Python run, verify) |
| 4 | 3 calls | Cron prompt rewrite (`cronjob action=update`) |
| 5 | 5-10 calls | Sitemap + commit + push + verify HTTP 200 |
| **Total** | **~80 calls** | chinahospitalsguide.com 2026-07-01 reference |

## When the user wants even bigger scope

If the user wants 30+ pillar pages or 200+ section injections in one session, split into multiple dispatch rounds with `git commit` between rounds so each round is independently pushable. Don't try to fit 80 tool calls of pillar content + 10 calls of section injection + 5 calls of cron + 10 calls of git into a single uninterrupted batch — the iteration cap will fire.

## Output template (when reporting a matrix overhaul)

When the matrix is done, report:

1. **Pages built**: list of N new pages with word counts and internal-link counts
2. **Articles augmented**: count of injected sections, by category breakdown
3. **Cron prompt updated**: confirmation of `cronjob action=update` success
4. **Deployment**: commit hash, push status, verify HTTP 200 for sample URLs
5. **Open follow-ups**: any skipped articles (with reason), recommended next pillar expansions

Keep the report 5-7 numbered sections, max ~300 words. The user wants the facts + what was shipped, not a transcript.
