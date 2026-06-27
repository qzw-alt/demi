# Oriental-Destiny.com — Article Template Fingerprint

Saved from the 2026-06-25 publishing session. Use this as the reference when drafting a new daily article for this site.

## Repository

- GitHub: `qzw-alt/oriental-destiny`
- Deployed branch: `main` (NOT `master` — the cron spec was wrong)
- Hosting: GitHub Pages, custom domain `oriental-destiny.com`
- Google Analytics 4 ID: `G-TBGDZRZZEJ`
- File pattern: `fate-YYYY-MM-DD.html` in repo root

## CSS fingerprint (extract from yesterday's article, never change)

Color palette (CSS variables):
- `--ink: #241915` — body text
- `--paper: #f8f1e7` — page background base
- `--cinnabar: #a63a2c` — primary accent (logo, links, CTA)
- `--gold: #b78a42` — secondary accent (subtitle, borders)
- `--pine: #315247` — h3 color, muted accents
- `--line: rgba(36, 25, 21, 0.1)` — borders

Typography:
- Body: `Georgia, "Times New Roman", serif`
- No sans-serif except where forced (CTA button)
- Line height: 1.72
- Body font size in content blocks: 1.02rem

Layout containers:
- `.container` — `width: min(1120px, calc(100% - 40px))`
- `.content-block` — `max-width: 820px`, `border-radius: 14px`, `box-shadow: 0 18px 48px rgba(70, 41, 24, 0.12)`
- `.content-block` padding: `40px 44px` (desktop), `26px 22px` (mobile)

## Structural blocks (always present, in this order)

1. **Sticky topbar** — `.brand-mark` ("Oriental Destiny"), `.brand-name` ("Feng Shui · BaZi · Destiny"), nav links: Home / Free Reading / Plans / Sample Report / Order
2. **Hero** — `.subtitle` (small caps, gold, e.g. "Compass School · Energy Map · Fire Month"), `<h1>` (clamp 2rem-3.4rem), `.lead` paragraph, `.meta` (date + read time)
3. **Content blocks** — typically 5-8 of them, each its own `<article class="content-block">` with one `<h2>` and several `<p>` / `<h3>` / `<ul>` elements
4. **FAQ section** — typically 5-8 `.faq-item` blocks with `.faq-q` and `.faq-a`
5. **CTA section** — gradient cinnabar, `<h2>` headline, short pitch, white-on-cinnabar button linking to `/instant_reading.html`
6. **Footer** — "Explore more" cross-link block (prior 5 articles) + shipping/refund/privacy/contact links + "For self-reflection and symbolic guidance only" disclaimer

## JSON-LD schema (in every article's `<head>`)

```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "<h1 text>",
  "description": "<meta description text>",
  "author": { "@type": "Organization", "name": "Oriental Destiny" },
  "publisher": {
    "@type": "Organization",
    "name": "Oriental Destiny",
    "url": "https://oriental-destiny.com/"
  },
  "datePublished": "<YYYY-MM-DD>",
  "mainEntityOfPage": "https://oriental-destiny.com/fate-YYYY-MM-DD.html"
}
```

## Meta tags (in `<head>`)

- `<meta name="description">` — 150-160 chars, keyword-dense
- `<link rel="canonical">` — full URL
- `<meta property="og:title">` — article title + " | Oriental Destiny"
- `<meta property="og:description">` — longer summary
- `<meta property="og:type">` — "article"

## Title pattern

Format: `<Headline> | Oriental Destiny`
Headline length: 50-80 chars
Style: practical and concrete ("How to Read X", "Y for Z", "X vs Y"), not poetic or "elevated"

## Footer cross-link block — what to link to

Link to the prior 3-5 articles in the `fate-YYYY-MM-DD.html` series in reverse chronological order. Use a multi-dot middot separator (` &middot; `). Always include `index.html` as the last link.

## Hero subtitle pattern

A small-caps line above the H1, typically 3 short phrases separated by middots. Sets context for what kind of feng shui topic this is. Examples from prior articles:

- "Compass School · Energy Map · Fire Month"
- "Luo Pan · Compass School · Xia Zhi 2026"
- "Bagua Cell · Xun · Fire Horse Year"

Pick 3 phrases that locate the article in the feng shui taxonomy.

## Vocabulary conventions (from terminology_mapping.md)

- `feng shui` (lowercase in running text, "Feng Shui" in titles)
- `qi` (not "chi" as primary)
- `Taoist` (not "Daoist")
- `yin and yang` (two words, lowercase)
- `bagua` (not "Pa Kua")
- `I Ching` (capitalized)
- Use Chinese characters with pinyin on first use: `Xun (巽)`, `Wu (午, Horse)`, `Bing Wu (丙午, Fire Horse)`
- Italics for pinyin terms

## Article length and pacing

- Word count: 3,500-4,500 words (visible body)
- Section count: 5-7 main sections + FAQ
- FAQ questions: 5-7 typical
- Read time: ~9 minutes at the "~200 words/min" estimate

## Voice notes

- Mechanism-first: explain what something IS, then where it sits, then how to use it
- Use specific numbers ("the south wall of the home is the Wu mountain, the 15-degree slice from 172.5 to 187.5")
- Use worked examples: walk through 2-3 home orientations, not just one
- Acknowledge the symbolic-system nature honestly (the FAQ "does it actually work" answer admits feng shui is symbolic, not a proven mechanism)
- Em dashes used as stylistic tic — measured baseline for this site (2026-06-25 through 2026-06-27): **6.8 per 1,200 words** (≈5.7 per 1,000). Encode as `&mdash;` in source. Match this density — going below 3 per 1,200 reads as LLM-terse; going above 12 per 1,200 reads as AI-saleswriting.
- No emojis, no curly quotes, no bold-as-emphasis patterns, no "rule of three" padding

## Series continuity (so far, June 2026)

| Date | Title | Focus |
|------|-------|-------|
| 06-19 | Luo Pan: How to Read the Feng Shui Compass | Tool, foundation |
| 06-20 | Tai Sui 2026: The Grand Duke and the Fire Horse Year | Annual, year-specific |
| 06-21 | The 24 Mountains | Compass mechanism |
| 06-22 | Sitting and Facing | Compass-school concept |
| 06-23 | Dining Room Feng Shui for the Fire Month | Room-specific application |
| 06-24 | The Bagua Map: How to Lay the 9-Section Energy Grid | Form-school foundation |
| 06-25 | The Wealth Corner (Xiu) | First cell-specific article |
| 06-26 | Yin and Yang in Feng Shui: What the Two Sides Mean for a Home | Polarity foundation (the "missing pillar" from earlier pieces) |
| 06-27 | Common Feng Shui Mistakes: Six Cures and Decor Trends That Quietly Disrupt Qi | Mythbusting / six-mistake listicle applied to the 06-26 framework |

Topic ladder pattern observed: each article explicitly references the previous 1-3 pieces by date and topic in its hero `.lead` paragraph. The 06-26 piece opens with "Earlier this month the Fire Month articles leaned on the word 'yang' without ever defining it... Today's piece is the missing pillar." The 06-27 piece opens with "Most of what shows up under 'feng shui' on a Pinterest board is a fragment of a real classical idea, with the part that made it work cut off." This continuity is the site's signature voice pattern — never write a "cold open" article.

Next logical topics to ladder from 06-27:
- One-cure-per-room deep dives (taking each of the six mistakes and doing the room-specific version)
- The Luo Pan reading of the same six cures (compass-school perspective vs. form-school perspective)
- A worked example: read one home from front door to back using the five-question diagnostic from 06-27
- Common BaZi chart mistakes (mirror of the 06-27 feng shui mistakes pattern applied to BaZi)
- Late-summer (Li Qiu) Earth-Month transition piece (continues the seasonal arc)

## Sitemap entry format

Add at the top of `<urlset>`, immediately after the XML declaration:

```xml
<url>
  <loc>https://oriental-destiny.com/fate-YYYY-MM-DD.html</loc>
  <changefreq>monthly</changefreq>
  <priority>0.7</priority>
</url>
```

## Commit message format

```
article: YYYY-MM-DD — <Short Title>
```

Example from this session:
```
article: 2026-06-25 — The Wealth Corner (Xiu): How to Read and Activate the Bagua Wealth Cell in 2026
```