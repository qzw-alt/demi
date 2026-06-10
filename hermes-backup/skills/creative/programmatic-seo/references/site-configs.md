# Site Configurations for Programmatic SEO

## oriental-destiny.com

| Setting | Value |
|---|---|
| GitHub | https://github.com/qzw-alt/oriental-destiny |
| Branch | `main` (not `master`) |
| Article dir | root (`.html` files directly in repo root) |
| Article naming | `fate-YYYY-MM-DD.html` |
| Sitemap | `sitemap.xml` in repo root |
| Publish verification | `curl -s -o /dev/null -w "%{http_code}" https://oriental-destiny.com/fate-YYYY-MM-DD.html` → expect 200 |
| Verification wait | 2 minutes after push |

**Sitemap entry format:**
```xml
<url>
  <loc>https://oriental-destiny.com/fate-YYYY-MM-DD.html</loc>
  <changefreq>monthly</changefreq>
  <priority>0.7</priority>
</url>
```

**CSS variables for article templates:**
```css
:root {
    --ink: #241915;
    --paper: #f8f1e7;
    --cinnabar: #a63a2c;
    --gold: #b78a42;
    --pine: #315247;
    --line: rgba(36, 25, 21, 0.1);
}
```

---

## chinahospitalsguide.com (verified 2026-06-02)

| Setting | Value |
|---|---|
| GitHub | https://github.com/qzw-alt/chinahospitalsguide |
| Branch | `master` |
| Article dir | `news/` |
| Article naming | `YYYY-MM-DD.html` |
| Sitemap | `sitemap.xml` at **repo root** (NOT `news/sitemap.xml` — that was wrong in the prior version of this file) |
| News index | `news/index.html` |
| Publish verification | `curl -s -o /dev/null -w "%{http_code}" https://chinahospitalsguide.com/news/YYYY-MM-DD.html` → expect 200 |
| Verification wait | 2-3 minutes after push |

**Sitemap entry format (root sitemap.xml, top-level URL):**
```xml
<url>
  <loc>https://chinahospitalsguide.com/news/YYYY-MM-DD-slug.html</loc>
  <lastmod>YYYY-MM-DD</lastmod>
  <changefreq>weekly</changefreq>
  <priority>0.6</priority>
</url>
```
Insert at the top of the `<urlset>` block, after the homepage/about/blog entries.

**news/index.html card format** (insert at the top of `<div class="news-list">`):
```html
<article class="news-item">
  <img src="../images/medical-tourism.jpg" alt="Article title here">
  <div class="news-content">
    <span class="news-date">Month DD, 2026</span>
    <h2 class="news-title"><a href="YYYY-MM-DD-slug.html">Article title</a></h2>
    <p class="news-excerpt">One-sentence excerpt with the headline finding and a number.</p>
    <a href="YYYY-MM-DD-slug.html" class="read-more">Read More →</a>
  </div>
</article>
```

**Banner color rotation** (avoid two consecutive articles with the same banner palette):
- Default: blue (`#1a1a2e` → `#0f3460`)
- Oncology/immunotherapy: blue (`#1e3c72` → `#1a365d`)
- Brain/neural/BCI: dark blue (`#1a1a2e` → `#0f3460`)
- ASCO/clinical trial: crimson (`#5b1a1a` → `#b73e3e`) — used for the HARMONi-6 article on 2026-06-02
- Spine/orthopedic: teal
- Cancer screening / infectious disease: amber/orange

**Typical article file size:** 20-32 KB, 2000-2900 words of body text, 14-19 em-dashes per 1000 words.

---

## Adding a new site

Copy the oriental-destiny block as a template. Keep branch name prominent — this is the most common push failure point across sites. **Before publishing to a new site, scrape its 3 most recent articles and measure em-dash density and word count — do not trust defaults.**
