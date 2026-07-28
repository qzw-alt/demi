# news/ → blog/ migration (verified 2026-07-28, HARD RULE)

## What changed

As of 2026-07-28, 伟烨 deleted the `news/` section on chinahospitalsguide.com. The reason: **many articles were duplicated across `news/` and `blog/`** (同一篇内容在两处都出现过). Going forward, **all daily cron articles go to `blog/` only**.

The `news/` path is gone from the site. New articles must be written to `blog/`. This is permanent, not temporary.

## Effective immediately

| What | Before (≤ 2026-07-27) | After (2026-07-28+) |
|---|---|---|
| Write path | `news/YYYY-MM-DD-<slug>.html` | `blog/YYYY-MM-DD-<slug>.md` (preferred) or `.html` (legacy ok) |
| De-dup grep | `grep -lE "(...)" news/*.html` | `grep -lE "(...)" blog/*.html blog/*.md` |
| Sitemap entry | `https://chinahospitalsguide.com/news/YYYY-MM-DD-...html` | `https://chinahospitalsguide.com/blog/YYYY-MM-DD-...html` or `.md` (verify the `.html` permalink convention) |
| Verify HTTP | `curl /news/YYYY-MM-DD-...html` | `curl /blog/YYYY-MM-DD-...html` (note: even for `.md` source file, permalink is `.html` per `blog/2026-07-18-iza-bren-*.md` frontmatter) |
| Cron prompt path string | `news/YYYY-MM-DD-<slug>.html` | `blog/YYYY-MM-DD-<slug>.md` |

## Format choice — .md + frontmatter OR .html?

The `blog/` directory has BOTH formats as of 2026-07-28:

- **102 old `.html` files** (legacy convention, pre-2026-07-10)
- **2 new `.md` files** with YAML frontmatter (2026-07-18 iza-bren, 2026-07-27 electroacupuncture — post-CONTENT_GUIDE update)

**Decision:** prefer `.md` + frontmatter for new articles (matches CONTENT_GUIDE 2026-07-10 update), but `.html` is acceptable for now. If user prefers `.md`, the conversion is large (frontmatter restructure + JSON-LD schema in YAML `schema:` block + .html body → markdown body).

## De-dup verification for the 2026-07-28 article

When 伟烨 first raised the "去重" concern in the same session, I ran a targeted dedup against the source-pattern anchor strings:

```bash
grep -lE "(Shufeng Jiedu|Anhui Jiren|Bahnhof-Apotheke|Suxiao Jiuxin|Tianjin Da Ren|Tasly.*Huawei)" news/*.html
# → news/2026-07-28-tcm-going-global-shufeng-jiedu-germany-ai-workflow.html (only the new article)

grep -lE "(Shufeng Jiedu|Anhui Jiren|Bahnhof-Apotheke|Suxiao Jiuxin|Tianjin Da Ren|Tasly.*Huawei)" blog/*.html blog/*.md
# → 0 matches (no blog/ duplicate of this topic)
```

**Verdict: zero duplicates.** The 2026-07-28 TCM globalisation article was NOT duplicated — it only existed in `news/`. Migration to `blog/` is safe.

## Why the duplication was happening (root cause)

Same cron prompt, same article, same content → user observed the SAME article in both `news/` and `blog/`. Most likely scenarios:

1. **Manual cross-posting:** someone (operator or earlier cron version) copied a `news/` article to `blog/` and committed both, then forgot
2. **Prompt version mismatch:** an older cron prompt version wrote to `blog/` while a newer one writes to `news/` (or vice versa) — the two coexisted
3. **Different cron jobs on different sites:** sibling cron for oriental-destiny or another site accidentally wrote to chinahospitalsguide/blog/

Whichever it was, the user fix is: delete `news/`, force everything to `blog/`. Future cron runs use the new path exclusively.

## What to do if cron agent wakes up and finds `news/` reference still in the prompt

The cron job `fa7a29b3464e` (`daily-chg-medical-news`) has the prompt text stored in `~/.hermes/cron/jobs.json` (or similar). As of 2026-07-28 the prompt likely STILL says `news/YYYY-MM-DD-<slug>.html` because the prompt file was not updated in the same session. **Future cron runs may need to:**

1. Self-detect: `ls blog/$(date +%Y-%m-%d)-*.md 2>/dev/null` AND `ls blog/$(date +%Y-%m-%d)-*.html 2>/dev/null` for Step 0 recovery check
2. If only `news/`-path article exists (the 2026-07-28 case): move it: `git mv news/2026-07-28-...html blog/2026-07-28-...md` (or .html), commit + push, then continue
3. Update sitemap entry to point to `/blog/...` instead of `/news/...`
4. Self-update the cron prompt if there's a tool to do so (`cronjob action=update`)

## TODO (open question for next session)

- [ ] Update the actual cron job `fa7a29b3464e` prompt via `cronjob action=update` to replace all `news/YYYY-MM-DD-<slug>.html` references with `blog/YYYY-MM-DD-<slug>.md` references. This is the durable fix.
- [ ] Decide `.md` vs `.html` for new articles and bake the answer into the cron prompt.
- [ ] Run a full-site audit of existing `news/` residual files (only 2 left after 07-28 cleanup: `news/2026-07-16-ai-briefing.md` and `news/2026-07-28-tcm-going-global-shufeng-jiedu-germany-ai-workflow.html`) — these should be either moved to `blog/` or deleted.

## See also

- `references/news-article-html-format-2026-07.md` — superseded by this file; HTML template still works for `blog/*.html` but path is wrong
- `references/cron-cap-hit-log.md` — running cap-hit taxonomy; news→blog change adds 1 new failure mode (path-mismatch if cron prompt not updated)
- `cron-content-pipeline-cap-safe` — cap-safe ordering pattern, unaffected by this migration