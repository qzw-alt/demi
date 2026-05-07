---
name: blog-content-writer
description: >
  Content research and writing pipeline for blog articles on the China Hospitals Guide
  medical tourism site. Covers both NEW article creation and EXISTING article refresh.
  Triggered when: writing a new blog article, refreshing a thin article (under 400 lines),
  or doing a competitor-gap article. This is the companion to news-writing-template
  (which covers news articles); this skill covers long-form blog guides.
category: seo-content-writer
---

# Blog Content Writer — China Hospitals Guide

## When to Use This Skill

- Writing a **new** blog article for China Hospitals Guide
- **Refreshing** an existing thin article (under 400 lines)
- Creating a **competitor-gap** article (competitor has a专题 we don't)
- User or cron asks to "refresh", "upgrade", or "rewrite" a blog article

For **news articles**, use `news-writing-template` instead.

## Reference Implementation

- `blog/knee-replacement-surgery-china-2026.html` (1,088 lines) — full 10-section structure
- `blog/dental-implants-china.html` (662 lines) — excellent long-tail SEO article with Straumann earnings hook, patient story, expert quote, regulatory timeline, FAQ schema, dual JSON-LD blocks; used as benchmark for date-refresh decisions

```
Section 1:  Introduction / Breaking News Hook
             Lead with a specific number or patient angle. No generic opener.

Section 2:  China's Current Landscape
             Stats, NMPA approvals, hospital annual volumes, clinical trials

Section 3:  Comparison Table [Factor | US/Intl | China]
             Named hospitals on both sides. Specific costs (USD). Wait times.

Section 4:  Real Cost Breakdown
             Named Chinese hospital → price range. What's included vs excluded.
             "Fudan Cancer Hospital charges ¥650,000–¥1.1M ($89K–$151K)
              including the drug, 14-day hospitalization, CRS monitoring,
              and 3-month follow-up scans."

Section 5:  Real Patient Journey
             Anonymized case: age, country, diagnosis, day-by-day timeline,
             actual total cost paid, one patient quote.

Section 6:  Expert Perspective
             Named expert + institution + specific data + source citation.
             "Dr. Wang at PUMCH has overseen 800+ CAR-T treatments since 2021,
              58% complete response rate in relapsed LBCL — ASH 2025."

Section 7:  Policy & Regulatory Timeline
             Year-by-year: approval dates, regulatory milestones, access pathways.
             Format: "Year: Event — [detail]"

Section 8:  Risks, Limitations & Contraindications
             Honest. Name specific complication rates. State who is NOT a candidate.
             E-E-A-T trust builder — do not skip or soften this section.

Section 9:  Next Steps for International Patients
             Named hospitals that accept foreign patients. Step-by-step process.
             Visa, documentation, language support.

Section 10: Sources
             Numbered list. Each: outlet name, publication date, URL.
```

## Refresh Workflow (for existing articles — FULL procedure)

Use this when refreshing an existing article (date update, news angle injection, data refresh).
For brand-new articles, use the 10-section structure from scratch instead.

> **Key decision: refresh vs. skip.** If article is already excellent and has recent data (≤30 days old), a date-only refresh is sufficient. If article has stale data (prices, statistics, sources >60 days old) or a weak structure, do a full content refresh injecting new news angles. Use judgment: articles with strong April/May 2026 data can skip fresh web search if search engines are blocked.

```
1. wc -l article.html                        → confirm it exists and is the target
2. read_file existing article (limit=50-100)  → see structure, CSS classes, schema blocks
3. Attempt web search for fresh news angles (3 attempts: Google → DuckDuckGo → Bing)
   If all blocked: fall through to date-only refresh without search
4. read_file article (offset=200-400)         → find: city/hospital list, FAQ section, Sources section
5. identify specific text to patch:
      a. datePublished / dateModified in BOTH JSON-LD schema blocks
      b. header date display (<span>May X, 2026</span>)
      c. opening paragraph → strengthen hook with news angle IF fresh angle found, else leave
      d. section heading if news angle warrants it
      e. FAQ section → add new Q&A if news angle is relevant
      f. Sources section → replace 2-3 stale refs with fresh news items
      g. sitemap.xml → update <lastmod> to today's date
6. Apply patches (patch mode=replace, ONE patch per change)
7. git add → git commit → git push
8. Verify: git log --oneline -3 shows correct commit
```

### Search Engine Failure Fallback

When Google, DuckDuckGo, Bing, and Qwant all return blocks/challenges:
- Proceed with date-only refresh (update dates + sitemap lastmod)
- Document in commit message: "date-only refresh, article already strong"
- Do NOT spend >5 minutes attempting alternative search methods
- The article's existing content quality is the primary signal — recent good content = skip search

### Refresh Changes Checklist (what to update every time)

| Element | Old value example | Action |
|---------|-------------------|--------|
| JSON-LD `datePublished` + `dateModified` | 2026-05-02 | → today's date (both blocks) |
| Header date `<span>May X, 2026</span>` | May 2, 2026 | → May 3, 2026 |
| Lead paragraph | generic opener | strengthen with news angle or patient stat |
| Section 2 heading | "Why X is dropping" | rename if news angle shifts frame |
| FAQ section | old Q&A | add 1 new Q&A relevant to news angle |
| Sources section | old citations | replace 2-3 stale refs with fresh news items |
| sitemap.xml `<lastmod>` | 2026-05-02 | → today's date (SINGLE entry only) |

### sitemap.xml Editing — Avoid Duplicate `<lastmod>` Tags

When updating `<lastmod>` in sitemap.xml, **never use sed replacement that blindly appends**. The sed pattern `<loc>...</loc>\s*<lastmod>` can match multiple times and create duplicate `<lastmod>` entries for the same URL.

**Correct approach:** Use `patch` mode=replace with the full surrounding XML context:
```python
# Wrong — creates duplicates:
sed -i 's|old_date|utc_date|' sitemap.xml  # don't use globally on sitemap.xml

# Right — patch with full context:
patch(old_string='  <url>\n    <loc>https://site.com/page.html</loc>\n    <lastmod>2026-05-02</lastmod>\n    <changefreq>monthly</changefreq>',
      new_string='  <url>\n    <loc>https://site.com/page.html</loc>\n    <lastmod>2026-05-05</lastmod>\n    <changefreq>monthly</changefreq>',
      mode='replace')
```

**Fix a duplicate if it happens:**
1. `grep -n "lastmod.*2026-05-0" sitemap.xml` to find all instances
2. Read the surrounding lines to identify the duplicate
3. Patch with full XML context around the `<url>` block

### News Angle Sourcing Priority

```
1. Today's Google News RSS for topic keywords (first 10 items)
2. Prioritize: company earnings reports, market research, policy changes
3. Avoid: older than 2 weeks unless it's a landmark event
4. Good angles: Straumann/Dentium earnings, new hospital branches,
   VBP policy updates, new JCI certifications, dental tourism destinations
```

**Parallel batching:** Use `delegate_task` with max 3 concurrent tasks.
Batch articles by similar topic. Each task handles 1 article independently.

## Competitor Gap Workflow

```
1. Read references/competitors/mychinamed.md → get gap list
2. Priority: short-term (LASIK, knee) → medium (spine, facelift) → long (CAR-T)
3. Apply 10-section structure + competitor title format:
   "[Procedure] in China: Cost, Top [Specialty] Hospitals &
    What Foreign Patients Need to Know"
4. Always include named US hospital in comparison tables
5. After publish: update keyword-database.md status: todo→done
```

## De-AI Checklist (run before every publish)

- [ ] No "pivotal moment" / "groundbreaking" / "testament" / "showcases"
- [ ] No "serves as" / "boasts" / "features" / "offers" (use "is" / "has" / "includes")
- [ ] No em-dash chains (max 1 per article)
- [ ] No hollow superlatives ("best in class", "leading provider")
- [ ] Section 6: Named expert with specific data + source
- [ ] Section 4: Specifies what's included in the cost
- [ ] Section 5: At least one specific patient detail (age, country)
- [ ] Section 8: At least 2 specific contraindications
- [ ] Section 9: At least 2 named hospitals

## Output Requirements

- Schema.org `Article` markup in `<head>`
- Canonical URL in `<head>`
- Featured image: 1200×630px, saved to article directory
- **sitemap.xml updated after every new article** (add URL entry)
- Push to GitHub → wait 5 min → `curl -sI URL | grep HTTP` verify 200

## Support Files

- `references/competitors/mychinamed.md` — competitor analysis (gap list, structure, title format)
- `references/keyword-database.md` — keyword priority list with status tracking

## Related Skills

- `humanizer` — de-AI pattern removal
- `news-writing-template` — news article format and publishing checklist
- `china-hospitals-guide-deploy` — GitHub push → deployment verification
