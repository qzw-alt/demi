# Eleventy `.md` Source Files Render to Trailing-Slash Directory URLs

Verified 2026-07-29, chinahospitalsguide.com China 2026-30 TCM five-year plan article. The 2026-07-10 cron prompt standard requires new articles to use `.md` + frontmatter + `_layouts/blog-post.njk` layout. When Eleventy renders a `.md` source file, the live URL is the trailing-slash directory form, NOT the `.html` extension form.

## The state matrix

For a `.md` source file at `blog/YYYY-MM-DD-slug.md`:

| URL form | HTTP response | Notes |
|---|---|---|
| `/blog/YYYY-MM-DD-slug/` | HTTP 200 (canonical) | Live URL after Eleventy render |
| `/blog/YYYY-MM-DD-slug.html` | HTTP 404 or CDN-delayed 404 | The `.html` extension is wrong for `.md` sources |
| `/blog/YYYY-MM-DD-slug/index.html` | HTTP 200 | Internal Eleventy file, not directly accessible |

For an `.html` source file at `news/YYYY-MM-DD-slug.html` (legacy convention):
| URL form | HTTP response |
|---|---|
| `/news/YYYY-MM-DD-slug.html` | HTTP 200 |
| `/news/YYYY-MM-DD-slug/` | HTTP 404 (no directory index) |

## What happened on 2026-07-29

The article was written as `blog/2026-07-29-china-tcm-five-year-plan-2026-2030-international-patients.md`. Three files reference the URL:

1. **Canonical `<link>` in the rendered HTML:** `https://chinahospitalsguide.com/blog/2026-07-29-china-tcm-five-year-plan-2026-2030-international-patients/` (trailing slash, correct)
2. **JSON-LD `mainEntityOfPage` URL:** same trailing-slash form (correct)
3. **Sitemap `<loc>` entry I patched:** `https://chinahospitalsguide.com/blog/2026-07-29-china-tcm-five-year-plan-2026-2030-international-patients.html` (`.html` extension, WRONG)

**Verify result:**
- `curl --max-time 25 -I https://chinahospitalsguide.com/blog/2026-07-29-china-tcm-five-year-plan-2026-2030-international-patients/` → HTTP 200 ✓
- `curl --max-time 25 -I https://chinahospitalsguide.com/blog/2026-07-29-china-tcm-five-year-plan-2026-2030-international-patients.html` → HTTP 404 ✗

The sitemap entry is a soft 404 — Google will still discover the article via the canonical link in the rendered HTML and via the JSON-LD `mainEntityOfPage`, but the sitemap is supposed to be the authoritative source of truth for crawler discovery. Future cron runs should fix the sitemap entry.

## The sitemap fix recipe

For a `.md` source file at `blog/YYYY-MM-DD-slug.md`, the sitemap entry should be:

```xml
<url>
  <loc>https://chinahospitalsguide.com/blog/YYYY-MM-DD-slug/</loc>
  <lastmod>YYYY-MM-DD</lastmod>
  <changefreq>weekly</changefreq>
  <priority>0.7</priority>
</url>
```

Note the **trailing slash** on the `<loc>` URL. Drop the `.html` extension.

## Detection recipe (after every new article)

```bash
curl --max-time 25 -s -o /dev/null -w "HTTP %{http_code}\n" "https://chinahospitalsguide.com/blog/YYYY-MM-DD-slug/"
curl --max-time 25 -s -o /dev/null -w "HTTP %{http_code}\n" "https://chinahospitalsguide.com/blog/YYYY-MM-DD-slug.html"
```

Expected:
- First call: HTTP 200
- Second call: HTTP 404 (or CDN-delayed 404)

If the first call returns 404 and the second returns 200, the source file is `.html` (legacy convention) and the `.html` URL is correct.

## Why the SKILL.md body keeps saying `.html`

The SKILL.md `Step 4: Publish` section says: "Save to `news/YYYY-MM-DD.html`". This is correct for the legacy `.html` convention. The 2026-07-10 cron prompt updated the standard to `.md` + frontmatter + blog-post.njk layout (publishing to `blog/`). The SKILL.md has not been fully updated to reflect this — the cron prompt carries the latest instruction set, and the SKILL.md provides the long-form rationale + pitfalls. Future SKILL.md revisions should consolidate the `.md` vs `.html` decision rule into a single canonical section.

## Cron budget impact

The 07-29 cron run hit this pitfall once during the verify step (call 28 returned HTTP 404 on the `.html` URL, call 30 on the trailing-slash URL returned HTTP 200). Total tool calls consumed by the pitfall: 2. Without the pitfall, the run would have hit ~18 tool calls; with it, ~20. The cost is small but recurring — every `.md`-source article will hit this unless the sitemap URL convention is fixed at write-time.

## Related

- The `chinahospitalsguide-content-guide.md` reference has the full `.md` + frontmatter publishing standard
- The 2026-07-10 cron prompt update has the latest instruction set for `.md`-source files
- The `cap-safe order` pitfall in the parent SKILL.md ensures the article is pushed to origin before any verify step — even if the verify step returns 404, the article is on disk + origin and recoverable in the next cron cycle