# Full-Site SEO Audit Results — 2026-05-02

Repository: `qzw-alt/chinahospitalsguide`, branch `master`
Workspace: `/root/.hermes/workspace/chinahospitalsguide/`

## Site Architecture

```
chinahospitalsguide/
├── blog/          62 files (59 real articles + index + template)
├── news/          51 files (49 real articles + index + template)
├── course/        10 files (9 chapters + index)
├── stories/        5 files (4 stories + index)
├── *.html         20 root-level pages
├── sitemap.xml
└── og-image.jpg   ← site-wide OG fallback (confirmed exists)
```

## Duplicate Physical Files Problem

`blog/` and `news/` share the same filenames for news articles:
- `blog/2026-03-24-japan-china-proton-therapy.html`
- `news/2026-03-24-japan-china-proton-therapy.html`

Both URLs work and both have proper self-referencing canonicals. Google sees them as separate pages. This splits PageRank. Recommendation: consolidate to one canonical location (news/ as canonical, remove from blog/).

## Pre-Existing SEO Coverage (before any work)

| Tag | blog/ (59) | news/ (49) | course/ (9) | root/ (20) |
|-----|-----------|------------|-------------|-----------|
| canonical | 53 ❌ | 49 ❌ | 0 | mixed |
| og:title | 33 | 0 | 0 | mixed |
| og:site_name | 59 ✅ | 0 | 0 | 0 |
| twitter:card | 5 | 0 | 0 | 0 |
| JSON-LD | 31 | 0 | 0 | 0 |

## Problems Found

### blog/ (59 articles)
1. **Duplicate canonical/og:url** — 59 files had 2x canonical, 2x og:url (injection script re-added instead of checking)
2. **Wrong canonical URL** — `hair-transplant-china-2026.html` pointed to root instead of /blog/
3. **Duplicate twitter:card** — 4 files had 2x twitter:card

### news/ (49 articles)
1. **All 49 missing canonical, og:title, og:description, og:image, og:url, og:site_name, twitter:card, twitter:title, twitter:description, twitter:image, JSON-LD**
2. news articles appeared in both blog/ and news/ with same filenames

### course/ (9 chapters)
1. **All 9 missing canonical, og:title, og:description, og:image, og:url, og:site_name, twitter:card, twitter:title, twitter:description, twitter:image, JSON-LD**

### sitemap.xml
1. **86 phantom URLs** — sitemap entries pointing to files that don't exist in expected locations (because news articles were in blog/ not news/)
2. **news/ 50 articles completely absent**
3. **template-news-article.html included** (should be excluded)
4. **index.html entries** for subdirectories (should not be in sitemap)

## Fixes Applied

| Commit | Scope | Fix |
|--------|-------|-----|
| `4de9847` | blog/ 59 | Deduplicate canonical/og:url, fix hair-transplant URL |
| `e63b5ce` | blog/ 4 | Remove duplicate twitter:card |
| `02f860c` | root/ 20 | Add OG/Twitter/JSON-LD to top-level pages |
| `b3eda15` | sitemap + news/ + course/ | Rebuild sitemap from filesystem, add SEO to 49 news + 9 course |

## Final State

| Section | Count | SEO Tags | sitemap.xml |
|---------|-------|----------|-------------|
| blog/ | 59 | ✅ full | ✅ |
| news/ | 49 | ✅ full | ✅ |
| course/ | 9 | ✅ full | ✅ |
| root/ | 20 | ✅ full | ✅ |
| **Total** | **137** | **100%** | **141 URLs (incl subdir index pages)** |

## Lessons Learned

1. **Audit before inject** — batch scripts often re-add existing tags; always check for duplicates first
2. **Python > PowerShell** for regex-heavy file manipulation (encoding, case sensitivity, multiline flags)
3. **Sitemap = filesystem output, not input** — build it programmatically from actual files, never maintain manually
4. **og:image fallback** — `og-image.jpg` at root confirmed to exist; use as site-wide fallback
5. **Audit script regex bugs** — false positives on `has_canonical` (matched content attributes), `has_og_site_name` (case mismatch); always verify against sample of actual files
6. **Git during batch updates** — if remote has concurrent edits, prefer `git merge` over `git rebase` to avoid conflict marker cleanup; if rebase used, clean `rebase-apply/` dir afterward
