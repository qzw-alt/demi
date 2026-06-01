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

## chinahospitalsguide.com (legacy)

| Setting | Value |
|---|---|
| GitHub | https://github.com/qzw-alt/chinahospitalsguide |
| Branch | `master` |
| Article dir | `news/` |
| Article naming | `YYYY-MM-DD.html` |
| Sitemap | `news/sitemap.xml` |
| Publish verification | `curl ... https://chinahospitalsguide.com/news/YYYY-MM-DD.html` |
| Verification wait | 2-3 minutes |

---

## Adding a new site

Copy the oriental-destiny block as a template. Keep branch name prominent — this is the most common push failure point across sites.
