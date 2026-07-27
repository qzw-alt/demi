# Eleventy Migration on chinahospitalsguide (verified 2026-07-27)

## Repo-state change

The chinahospitalsguide repo migrated to Eleventy 11ty (v2.0.1) on 2026-07-26. The old `news/` and `treatments/` directories were deleted in commit `21696ec` ("Clean: delete news/course/treatments directories, 120 files, 50K LOC"). Daily articles now live under `blog/` as Markdown files with frontmatter, rendered to `.html` by Eleventy using the `blog-post.njk` layout.

**The old `news/YYYY-MM-DD-slug.html` filename convention is dead.** Writing there now either silently no-ops (when `news/*.md` is the file extension, ignored by `eleventy.config.js` line 21) or gets published at a non-canonical path that 404s. Cron prompts that still instruct `news/YYYY-MM-DD-slug.html` are stale (the 2026-07-27 cron job prompt had this defect).

## Detection recipe when a cron prompt is unclear

1. `git ls-tree -r --name-only HEAD | grep -E '^(news|blog)/' | head -30` — see what file pattern HEAD has
2. `ls news/` — if it has only legacy leftovers (e.g. `2026-07-16-ai-briefing.md`), `news/` is dead
3. `ls blog/ | grep -E '2026-07'` — see what daily articles currently live in `blog/`
4. `curl --max-time 25 -sLI https://chinahospitalsguide.com/news/YYYY-MM-DD.html` — should 404
5. `curl --max-time 25 -sLI https://chinahospitalsguide.com/blog/YYYY-MM-DD.html` — should 200

The 2026-07-27 cron run on chinahospitalsguide detected the migration via steps 1, 2, 4, 5 and shipped the article to `blog/2026-07-27-...md` instead of `news/`.

## Canonical daily-article recipe (verified 2026-07-27, end-to-end shipped)

1. Write `blog/YYYY-MM-DD-slug.md` with frontmatter:
   ```yaml
   ---
   layout: blog-post.njk
   title: "..."
   description: "..."
   kicker: "..."
   subtitle: "..."
   date: YYYY-MM-DD
   permalink: "/blog/YYYY-MM-DD-slug.html"
   canonical: "https://chinahospitalsguide.com/blog/YYYY-MM-DD-slug.html"
   ogType: "article"
   ogTitle: "..."
   ogDescription: "..."
   ogImage: "https://chinahospitalsguide.com/og-image.webp"
   schema: |
     [
       { "@context": "https://schema.org", "@type": "Article", ... },
       { "@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [...] }
     ]
   pageStyle: |
     .rct-box { ... }
   ---
   ```
2. The `schema:` field is a JSON **array** (two schema blocks side-by-side), not two parallel `{}` objects. Eleventy renders this through Nunjucks; the array form survives intact into the output HTML.
3. `pageStyle:` is an optional block for article-specific CSS that gets inlined via the layout.
4. After writing the file, run `npx @11ty/eleventy` (~1 second on this repo size) to render to `_site/`.
5. The **sitemap is build-driven**, not git-tracked from source. After Eleventy renders, run `node scripts/generate-sitemap.js` to regenerate `sitemap.xml` from the `_site/` tree. The script walks `_site/` for `.html` files only (line 21 of the script: `e.name.endsWith('.html')`), so a `.md` source file is only sitemap-eligible after Eleventy has rendered its `.html` to `_site/`.
6. Commit both the new `.md` source AND the regenerated `sitemap.xml` together. Push, then `sleep 75 && curl --max-time 25 -sI https://chinahospitalsguide.com/blog/YYYY-MM-DD-slug.html` for HTTP 200 verify.

## Repo-level Eleventy quirks (verified 2026-07-27)

- `eleventy.config.js` line 21: `eleventyConfig.ignores.add("news/*.md")` — do not write to `news/`. Old `news/*.html` files (2026-07-23 and earlier) appear in `git log --all` but were deleted from the working tree.
- `eleventy.config.js` line 35: comment notes "2026-07-26: news/ and treatments/ deleted (CTR destruction, duplicate content). blog/ and stories/ remain as passthrough."
- Old `blog/*.html` files are still passthrough-copied by Eleventy (line 39: `eleventyConfig.addPassthroughCopy("blog/")`), but new articles should be `.md` with frontmatter and will be rendered by the `blog-post.njk` layout. The 2026-07-18 iza-bren article is the reference format.
- `_data/latestNews.js` still reads from `news/` and returns only one entry (`news/2026-07-16-ai-briefing.md` — a leftover Chinese-language AI briefing, not built into the site). This data source is currently decoupled from the daily-article pipeline and is not where new daily articles need to be registered. New daily articles appear on the homepage via the standard blog post flow; the `_data/latestNews.js` consumer is a known-broken legacy hook.
- `eleventy.config.js` lines 35–37 list the canonical convention: "New blog posts should use blog-post.njk layout via frontmatter." Trust this comment over any cron prompt or older skill text.

## Sitemap priority convention (verified 2026-07-27)

The regenerated `sitemap.xml` uses `priority 0.7` for `/blog/*` URLs (per `scripts/generate-sitemap.js` line 31: `if (url.startsWith('/blog/') && url !== '/blog/') return '0.7';`). The earlier 0.6 convention noted in some 2026-06-XX skill references is no longer current. The auto-generated entry is:
```xml
<url>
  <loc>https://chinahospitalsguide.com/blog/YYYY-MM-DD-slug.html</loc>
  <lastmod>YYYY-MM-DD</lastmod>
  <changefreq>weekly</changefreq>
  <priority>0.7</priority>
</url>
```

## Deccan Herald articleBody extraction (7th-tier source, verified 2026-07-27)

Deccan Herald article pages (e.g. `https://www.deccanherald.com/health/healthcare/explained-...-4083259`) return ~1.4 MB of HTML but the body content is NOT in `<p>` tags — every regex-based extraction (`re.findall(r'<p[^>]*>(.*?)</p>', body)`) returns 0 matches. The article text lives inside a single JSON-LD `articleBody` field that is HTML-encoded (`&lt;p&gt;`, `&lt;a href=&quot;...&quot;&gt;`). The working recipe is a 3-line Python pass:

```python
import re, html
c = open('/tmp/dh.html').read()
m = re.search(r'"articleBody":"(.*?)"(?=,"author"|,"datePublished"|,"url")', c, re.DOTALL)
body = html.unescape(m.group(1))
body = re.sub(r'<[^>]+>', ' ', body)  # strip the encoded tags
body = re.sub(r'\s+', ' ', body).strip()
```

`datePublished` for the source is at the top of the same JSON-LD block (`"datePublished":"2026-07-22T18:47:07+05:30"`) and is reliable. `og:description` and `twitter:description` in the `<head>` give a clean 1-sentence summary. Use this as a fallback when the news/medical/science sites Cloudflare-block direct `<p>` extraction. The same articleBody-in-JSON-LD pattern is used by other Indian English-language outlets; treat it as a 7th-tier source after the existing 6 tiers (manilatimes.net, finanznachrichten.de, Mirage News, pharmaphorum, GEN.com, mira­ge news) in the content-research-writer-cn skill.

## CrossRef and PubMed as fallbacks for Chinese TCM journals (verified 2026-07-27)

The DOI `10.13702/j.1000-0607.20240877` (a 2026 *Acupuncture Research* / Zhen Ci Yan Jiu paper on gentle electroacupuncture for facial paralysis) is **not yet indexed in CrossRef** as of 2026-07-27 — `https://api.crossref.org/works/{doi}` returns `{"status":"resource not found"}`. The doi.org resolver redirects to `chndoi.org` (China DOI registration agency), which is not directly fetchable from the cron sandbox. So when a paper's only identifier is a recent Chinese-journal DOI, CrossRef is not a working fallback — direct fetch of the journal's HTML, a secondary press release on Deccan Herald / News-Medical / EIN Presswire, or the journal's own English abstract page is the working path. Mark this as a known-blind-spot for `content-research-writer-cn` when the article is from a Chinese TCM journal (Acupuncture Research, Chinese Journal of Integrative Medicine, Journal of Traditional Chinese Medicine, etc.).

Separately, `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi` is **blocked at the cron-sandbox IP (43.134.68.35) as of 2026-07-27** with the NCBI "blocked for possible abuse" diagnostic page. PubMed E-utilities is unavailable from this sandbox until the IP is whitelisted or a proxy is configured. CrossRef is NOT blocked; only NCBI E-utilities are. The cron agent should default to CrossRef + secondary press releases for any clinical-evidence article rather than reaching for PubMed E-utilities.

## Daily-article verification: HTTP 200 on the canonical URL (verified 2026-07-27)

The cap-safe order (commit + push before humanize loop, then sitemap + index + verify) still applies on the new Eleventy build, but with one extra step: the `npx @11ty/eleventy` + `node scripts/generate-sitemap.js` run must happen BEFORE the sitemap commit, because `_site/` is the source-of-truth for sitemap generation and is NOT in git. The full verified sequence for a clean daily article on chinahospitalsguide is now:

1. Write `blog/YYYY-MM-DD-slug.md` (1 call)
2. `git add blog/...md && git commit && git push` (3 calls; rebase if remote advanced, per the standard pattern)
3. `npx @11ty/eleventy` (1 call, ~1 second) — renders `.md` to `_site/blog/...html`
4. `node scripts/generate-sitemap.js` (1 call, ~0.5 second) — regenerates `sitemap.xml` from `_site/`
5. `git add sitemap.xml && git commit && git push` (3 calls; rebase if needed)
6. `sleep 75 && curl --max-time 25 -sI https://chinahospitalsguide.com/blog/YYYY-MM-DD-slug.html` (1 call) — expect HTTP 200, `last-modified` should reflect the push time

Total: ~10 tool calls. Compare to the old `news/*.html` static-passthrough pipeline which was ~5 calls (no build step). The build is fast and idempotent; running it on every daily article keeps `_site/` in sync with the source `.md` and prevents the `_data/latestNews.js`-style drift.

## Cron prompt dead references on chinahospitalsguide (verified 2026-07-27)

The 2026-07-27 cron job prompt instructed the agent to write to `news/YYYY-MM-DD-slug.html` (e.g. "write_file 直接落盘 `news/YYYY-MM-DD-<slug>.html`"). This instruction is now WRONG. The repo's `eleventy.config.js` line 21 (`eleventyConfig.ignores.add("news/*.md")`) ignores `news/*.md` files entirely, and the 2026-07-26 cleanup commit deleted the `news/` directory's `.html` content. The agent on the 2026-07-27 run detected this by:

1. Reading `git ls-tree -r --name-only HEAD` and seeing the new `blog/2026-07-XX-*.md` files in HEAD
2. `ls news/` returning only the legacy `2026-07-16-ai-briefing.md` AI briefing
3. `curl -sLI https://chinahospitalsguide.com/news/2026-07-23-...html` returning HTTP 404
4. `curl -sLI https://chinahospitalsguide.com/blog/2026-07-18-iza-bren-esophageal-cancer-china.html` returning HTTP 200

**Decision rule for future runs:** trust the actual filesystem state (`ls news/` + `ls blog/` + live HTTP probes) over the cron prompt's text. The prompt's `news/` instruction is a dead reference parallel to the `seo-content-writer` skill and `competitor-research.md` paths that the programmatic-seo skill already documents as dead for oriental-destiny.

## Reference run: 2026-07-27 chinahospitalsguide

Article: `blog/2026-07-27-electroacupuncture-facial-paralysis-gentle-current-china-rct-2026.md`
- Word count: 2,467
- Banned-vocab hits: 0
- `actually` body-prose: 2 (within 1-2 per 4,000-word tolerance)
- Em-dash density: 7.8/1200 (within long-article band)
- Commits: `49925b9` (article), `062ec3b` (sitemap)
- Live URL: https://chinahospitalsguide.com/blog/2026-07-27-electroacupuncture-facial-paralysis-gentle-current-china-rct-2026.html
- HTTP 200 verified 75s after push

Source: Deccan Herald 2026-07-22 (articleBody extracted via the JSON-LD pattern above), 66-patient three-arm RCT from the Second Affiliated Hospital of Guangzhou University of Chinese Medicine. Archetype: Template B (TCM modernisation). Cross-cuts content-research-writer-cn archetype #1 (peer-reviewed Chinese-led RCT) and the 2026-07-04 / 2026-07-10 / 2026-07-23 thread of electroacupuncture coverage.
