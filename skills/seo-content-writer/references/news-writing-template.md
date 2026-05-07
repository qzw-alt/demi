---
name: news-writing-template
description: Medical tourism news article writing template for China Hospitals Guide. Structure, headline framework, de-AI checklist, and publishing workflow.
category: seo-content-writer
---

# News Writing Template — China Hospitals Guide

> **10-Section structure is shared with `blog-content-writer`.**
> The canonical structure (Sections 1-10) is identical for blog and news.
> Reference: `blog-content-writer` skill — do not duplicate its content here.

## Fusion Writing Rules (Core Principles)

**News article = news hook + 10-section blog guide structure.**

**Fusion判断流程（每次选题时执行）：**

1. 读取 `/root/.hermes/workspace/chinahospitalsguide/references/keyword-database.md` 的「内容日历」
2. 搜索当日/近3天医疗新闻热点（Google News）
3. **如果热点匹配一个 `Status: todo` 的长尾词** → 写「新闻长尾融合文」
   - 新闻钩子 + 长尾指南主体
   - 两层搜索意图同时满足
4. **如果热点不匹配任何待写长尾词** → 选「内容日历」中 P0-P1 词写纯指南文（不加新闻框架）
5. **如果当天无好热点且无紧急长尾词** → 跳过，不强写

**融合文标题公式：**
> `[长尾关键词] (2026): [具体数据/事件] + [China对比/指南补充]`
> 例: "CAR-T Therapy Cost in China (2026): $150K–$200K, Top Hospitals, and the New NMPA Approval"
> 例: "Stem Cell Therapy in China (2026): What China's Clinical Trial Boom Means for International Patients"

---

## Article Structure

```
[HERO IMAGE — Unsplash/Custom medical photo, 1200x630px, saved as news/YYYY-MM-DD-slug.jpg]

[HEADER — dark gradient]
  H1: [Event] — [Surprising stat or angle] — How Does China Compare?
  Subtitle: [1-sentence hook with specific number]

[META BAR]
  Published: YYYY-MM-DD | By China Hospitals Guide | Category: [Breakthrough/Policy/Treatment/Comparison]

[CONTENT]
  Section 1: The Breaking News
    - Opening paragraph: Who/what/when/where/why (5Ws)
    - Specific numbers and data
    - Real human impact angle (patient story or expert quote)
    - Named sources (NYT, Nature Medicine, NEJM, FDA, etc.)
    - If news is from the past 24 hours, note the timestamp (e.g., "announced today" or "published X hours ago") — this signals recency to readers and search engines

  Section 2: China's Current Landscape
    - What China already does well in this area
    - Recent Chinese developments (past 6 months)
    - Clinical trials, approvals, hospital programs
    - Be honest — acknowledge gaps where they exist

  Section 3: Comparison Table
    [Factor | International | China]
    - Key treatment/drug names and trial phases
    - Cost ranges (USD)
    - Wait times
    - Survival/outcome data if available
    - Access for international patients

  Section 4: The Numbers — Real Cost Breakdown
    - Treatment cost at specific named hospitals
    - What's included / what's not
    - Comparison with named US/UK hospital prices
    - Format: "Hospital A costs ¥X–¥Y including [list]. The same treatment
      at Named US Hospital costs $Z before insurance."

  Section 5: What a Real Patient Journey Looks Like
    - One anonymized patient case (age, country, diagnosis, treatment)
    - Timeline: arrival → assessment → treatment → discharge → follow-up
    - Actual total cost paid
    - One honest quote from the patient (can be fictionalized but plausible)

  Section 6: Expert Perspective
    - Named expert + institution + specific data point
    - Real quote from conference/presentation/paper (cite source)
    - Format: "Dr. [Name] at [Hospital/University] has overseen [N] cases since [year].
      [Specific outcome data], according to [source, year]."

  Section 7: Policy and Regulatory Timeline
    - NMPA (or relevant agency) approval timeline for this treatment
    - Current approved products count
    - Access pathways for international patients
    - Format: "Year: Event — [detail]"

  Section 8: Risks, Limitations, and Who Should NOT Come
    - Honest assessment of who is NOT a candidate
    - Specific contra-indications
    - Known complication rates where available
    - This section BUILDS trust — don't skip it

  Section 9: What This Means for International Patients
    - Concrete next steps
    - Which Chinese hospitals handle this (named, with data)
    - Who is a good candidate
    - Cost comparison in practical terms
    - Honest risk factors

  [CTA BOX — green gradient]
    Title: [Action-oriented question]
    Body: 2 sentences on how coordination service helps
    Button: Get a Free Consultation →

  Section 10: Sources
    - Numbered list of named sources cited in the article
    - Link to each source
    - Article name, outlet, publication date

[FOOTER]
  ← Back to Homepage | ← All News
```

## Headline Formulas

### Formula 1: Breakthrough + Stat + China Compare
> **[Drug/Procedure] [Verb in Past Tense] — [Big Number] — How Does China Compare?**
> e.g. "New KRAS Inhibitor Cuts Pancreatic Cancer Death Risk 40% — How Does China Compare?"

### Formula 2: Country Comparison (Medical Tourism Angle)
> **[Country] [Verb] as Medical Tourism Destination — How Does China Compare?**
> e.g. "Malaysia Launches Medical Tourism Year — Can China Keep Up?"

### Formula 3: China Milestone + Context
> **China [Achieves/Launches/Approves] [X] — What It Means for International Patients**
> e.g. "China Approves First Homegrown CAR-T Therapy — What International Patients Need to Know"

### Formula 4: Trend + Data + China Angle
> **[Number] International Patients [Verb] in China — [Key Driver]**
> e.g. "410,000 Medical Tourists Visited China in 2025 — CAR-T and Oncology Lead the Way"

## De-AI Checklist (Must Run Before Publishing)

Per `humanizer` skill patterns — scan and fix:

- [ ] No "pivotal moment" / "groundbreaking" / "testament" / "underscores" / "showcases"
- [ ] No "serves as" / "boasts" / "features" / "offers" (use simple "is" / "has" / "includes")
- [ ] No "In order to" / "Due to the fact that" / "At this point in time"
- [ ] No "The real question is" / "At its core" / "What really matters"
- [ ] No em-dash chains (max 3 em-dashes per article; if more, run the cleanup script below)

**Em-dash cleanup script** (run if article exceeds 3 em-dashes):
```python
# Replace em-dashes with commas or periods in the article body
# Keep em-dashes only in: title subtitle, year ranges, or section dividers
lines = content.split('\n')
result = []
em_count = 0
max_em = 3
for line in lines:
    if '—' in line:
        line_em = line.count('—')
        if em_count + line_em <= max_em:
            em_count += line_em
            result.append(line)
        else:
            remaining = max(0, max_em - em_count)
            parts = line.split('—')
            kept = parts[:remaining]
            replaced = ['—'.join([kept[-1]] + parts[remaining:])] if remaining > 0 and remaining < len(parts) else []
            for p in parts[remaining:]:
                replaced.append(',' + p)
            em_count = max_em
            result.append('—'.join(kept + replaced))
    else:
        result.append(line)
```
- [ ] No "of course" / "certainly" / "I hope this helps"
- [ ] No passive voice dominating sentences
- [ ] No "it goes without saying" / "it is important to note"
- [ ] Sentence starters — vary them, no "This/Such/These" always first
- [ ] Numbers: always use specific figures, never vague ("many" → "12 hospitals")
- [ ] Named sources for every claim (not "studies show")
- [ ] No hollow superlatives ("best in class", "leading provider")
- [ ] Section 4 (Cost): Every cost claim must specify what is included
- [ ] Section 5 (Patient Journey): At least one specific detail (age, country, diagnosis)
- [ ] Section 6 (Expert): Must have expert name + institution + specific data point + source
- [ ] Section 7 (Policy): Must include year-specific regulatory milestones
- [ ] Section 8 (Risks): Must include at least 2 specific contra-indications or limitations
- [ ] Section 9 (For Patients): At least 2 named hospitals with specific info

## Image Requirements

Every news article MUST have a featured image:
- Size: 1200×630px (Open Graph minimum)
- Save to: `~/.hermes/workspace/chinahospitalsguide/news/YYYY-MM-DD-slug.jpg`
- Alt text: descriptive, includes location/country where relevant
- Source: Unsplash (free) or AI-generated
- Image URL in HTML: `https://chinahospitalsguide.com/news/YYYY-MM-DD-slug.jpg`
- If no image: use a gradient banner instead (CSS only, no external dependency)

## Schema Requirements

Use `NewsArticle` (NOT `Article`) from Schema.org:
```json
{
  "@type": "NewsArticle",
  "headline": "...",
  "description": "...",  // 150-160 chars max
  "image": "https://chinahospitalsguide.com/news/YYYY-MM-DD-slug.jpg",
  "datePublished": "YYYY-MM-DD",
  "dateModified": "YYYY-MM-DD",
  "author": { "@type": "Organization", "name": "China Hospitals Guide" }
}
```

## Publishing Checklist

1. [ ] Draft article — Sections 1–8 complete before starting
2. [ ] Run De-AI checklist (all boxes checked)
3. [ ] Add featured image (or CSS gradient banner — see CSS patterns below)
4. [ ] Add NewsArticle Schema (verify datePublished format: YYYY-MM-DD)
5. [ ] Update `news/index.html` — add article card at **TOP** of list
6. [ ] Update `sitemap.xml` — add URL entry at end of news section (before `</urlset>`)
7. [ ] **Update keyword database** — three separate patches needed:
   - `keyword-database.md` → classification table: `Status: todo` → `done` + article path in remarks
   - `keyword-database.md` → content calendar: update "预计写作日期" to actual date
   - `keyword-database.md` → written articles log: **append** new row (do NOT overwrite existing rows)
8. Git add → commit → push
9. Wait 30 seconds → verify: `curl -sI https://chinahospitalsguide.com/news/YYYY-MM-DD-slug.html | grep HTTP` — confirm 200

---

## News Index Card Format

In `news/index.html`, insert this **at the very top** of the `<div class="news-list">` block, before all existing `<article>` elements:

```html
<article class="news-item">
    <img src="https://chinahospitalsguide.com/og-image.jpg" alt="[Article Title]">
    <div class="news-content">
        <span class="news-date">May 1, 2026</span>
        <h2 class="news-title">
            <a href="YYYY-MM-DD-slug.html">
                Article Headline
            </a>
        </h2>
        <p class="news-summary">First 100 characters of summary...</p>
        <a href="YYYY-MM-DD-slug.html" class="read-more">Read More →</a>
    </div>
</article>
```

## Sitemap.xml Insertion Point

News article URLs live in the sitemap's `<urlset>` along with blog URLs, but they are NOT at the top. The sitemap groups by priority/date, so news articles are typically toward the end. Always search backward from the end of the file.

To find the insertion point:
1. Search for the last known news article's slug (e.g., `2026-05-05-thailand-health-insurance`) to find the most recently published news entry
2. The new URL goes after that block, before the next `<url>` (which is usually a blog article)
3. If the last news article slug is unknown, search for `news/` in the file to map where news entries end

> **sitemap.xml editing — avoid duplicate `<lastmod>` tags.** Never use sed globally on sitemap.xml to replace dates — the pattern can match multiple `<lastmod>` entries and create duplicates. Always use `patch` with full XML context around the surrounding `<url>` block.

```xml
  <!-- INSERT NEW URL after the most recent news article -->
  <url>
    <loc>https://chinahospitalsguide.com/news/2026-05-05-thailand-health-insurance-china-tourism-impact.html</loc>
    <lastmod>2026-05-05</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.7</priority>
  </url>
  <url>
    <loc>https://chinahospitalsguide.com/news/2026-05-06-YOUR-SLUG.html</loc>
    <lastmod>2026-05-06</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.7</priority>
  </url>
</urlset>
```

## CSS Patterns Used in Articles

**Highlight box (blue)**: For key insights or positive China advantages
```css
.highlight-box { background: #e8f4f8; border-left: 4px solid #2980b9; padding: 15px 20px; margin: 20px 0; border-radius: 4px; }
```

**Warning box (amber)**: For context or competitive caveats
```css
.warning-box { background: #fef9e7; border-left: 4px solid #f39c12; padding: 15px 20px; margin: 20px 0; border-radius: 4px; }
```

**Table highlight row (green)**: For rows where China has clear advantage
```css
.highlight-row td { background: #e8f8f0 !important; font-weight: 600; }
```

## Competitor Reference

For medical tourism content structure and gaps, also reference:
- `~/.hermes/workspace/chinahospitalsguide/references/competitors/mychinamed.md`
- MyChinaMed article title format: `[Procedure] in China: Cost, Top [Specialty] Hospitals & What Foreign Patients Need to Know`
- MyChinaMed fixed elements: cost numbers + country comparison (vs US) + hospital recommendations + foreign patients + complete guide

## Topic Discovery Search Queries

```
# Medical tourism hot topics
https://news.google.com/search?q=medical+tourism+china+2026
https://news.google.com/search?q=medical+tourism+asia+2026
https://news.google.com/search?q=healthcare+breakthrough+china

# Cancer/oncology (high-value topics)
https://news.google.com/search?q=oncology+treatment+breakthrough+2026
https://news.google.com/search?q=car-t+therapy+china+fda

# Competition countries
https://news.google.com/search?q=Thailand+medical+tourism+2026
https://news.google.com/search?q=Korea+medical+tourism+breakthrough
```

## Site Audit Reference

Before publishing or starting a new writing cycle, run the checks in:
`references/site-audit-checklist.md`

Known issues to watch for:
- **treatments/ 404** — relative path links break when accessed from different entry points
- **news/index.html empty list** — articles not linked in the index page
- **2 news articles missing NewsArticle schema** — see audit file for exact file names
- **GitHub push blocked? Check HTTPS first** — repos use token auth, not SSH

## Quality Gate

If no suitable news topic found on a given day — **skip silently, do not publish**. The reputation cost of a weak article exceeds the benefit of daily frequency. A strong bi-weekly article outperforms a daily commodity piece.

**News freshness threshold:**
- Breaking news window: ~72 hours (ideal)
- Trend/analysis window: ~5 days (acceptable for slower-moving stories)
- Beyond 5 days: treat as stale unless it directly matches a P0 keyword with no existing article

**Example of a skip:** A Korean cell therapy (CartiLife) received Hainan approval on April 27. By May 6 this was 8-9 days old — too stale for a standalone fusion piece, even though it matched a relevant keyword. The Guangzhou medical tourism service center story from ~5 days prior was likewise borderline. When two potential stories are both stale, skip.

**Exception to the 5-day rule:** If a P0 keyword has NO existing article AND no recent news match, write a pure guide article (no news hook) rather than forcing a stale news connection.
