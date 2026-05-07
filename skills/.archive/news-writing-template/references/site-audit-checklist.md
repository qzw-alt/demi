# Site Audit Checklist — China Hospitals Guide

> Last updated: 2026-05-03
> Run these checks before publishing or starting a new writing cycle.

## Known Issues

### 1. `treatments/` URLs return 404
**Symptom:** Links to `/treatments/` pages break when accessed from news article entry points.
**Cause:** Relative path links in article templates.
**Fix:** Always use absolute paths: `https://chinahospitalsguide.com/treatments/...`

### 2. `news/index.html` — articles missing from list
**Symptom:** New articles not appearing on the news listing page.
**Cause:** Article card not inserted into `<div class="news-list">` in `news/index.html`.
**Fix:** Insert at the very top of `<div class="news-list">` (before all existing `<article>` elements).

### 3. Two news articles missing NewsArticle Schema
**Symptom:** Missing or incorrect `NewsArticle` structured data.
**Files affected:** `news/2026-03-24-japan-china-proton-therapy.html` and `news/2026-03-24-japan-stem-cell-diabetes-therapy-approval.html` (suspected — verify).
**Fix:** Add NewsArticle schema per skill template. Schema type MUST be `NewsArticle` (NOT `Article`).

### 4. GitHub push via HTTPS (not SSH)
**Symptom:** `git push` fails with "Permission denied (publickey)".
**Cause:** This repo uses token auth over HTTPS, not SSH keys.
**Fix:** Ensure remote URL is `https://github.com/qzw-alt/chinahospitalsguide.git` — token is stored in credential helper.

## Pre-Publish Checklist

- [ ] All internal links use absolute paths (no `../` relative links)
- [ ] New article card inserted at top of `news/index.html`
- [ ] Sitemap updated with new article URL
- [ ] NewsArticle schema present with correct `datePublished` format (YYYY-MM-DD)
- [ ] `curl -sI https://chinahospitalsguide.com/news/YYYY-MM-DD-slug.html | grep HTTP` returns 200
- [ ] Git push successful

## File Paths Reference

```
~/.hermes/workspace/chinahospitalsguide/
  news/index.html          — news article listing (insert new cards here)
  sitemap.xml              — all URLs (append new article at end of news section)
  blog/                   — long-form guide articles
  news/                   — news/feature articles
  references/
    keyword-database.md    — topic priority queue and written article log
    competitors/
      mychinamed.md       — competitor title/content analysis
```
