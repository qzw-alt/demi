# GA4 Event Tracking Template (chinahospitalsguide.com)

**Status**: Deployed site-wide 2026-07-02 across **217 pages** via external `ga4-events.js` (NOT inlined per-page).

**Why external script, not inlined**: Browser-cached across all 217 pages, single source of truth, easier to maintain, `defer` attribute = non-blocking. Original inline approach (added 2026-07-02 commit `1c03aab`) only covered 2 pages; replaced by commit `d481cac` which injected `<script src="ga4-events.js" defer></script>` site-wide.

**Existing tracking**: GA4 base config already in every page's `<head>` (ID `G-RVYZENK472`).

## Events tracked (7)

| Event | Trigger | Category |
|---|---|---|
| `scroll_depth` (25/50/75/100%) | Page scroll milestones | engagement |
| `article_complete` | 100% scroll + 30s dwell | engagement |
| `cta_click` | `.cta-button`, `.nav-cta`, `.btn-primary`, `.btn-cta`, or any `contact*` link | conversion |
| `outbound_click` | External links (not chinahospitalsguide.com) | engagement |
| `internal_click` | Internal navigation (article-to-article, `/blog/` or `.html` targets) | navigation |
| `newsletter_submit` | Formspree form submission (any `action` containing `formspree.io`) | conversion |
| `file_download` | PDF/doc/docx/xls/xlsx/zip/rar links | engagement |

All events fire `gtag('event', '<name>', {event_category, event_label, page_type, page_path, ...})`. `PAGE_TYPE` is auto-detected from URL path: `home`, `blog_index`, `article` (any `/blog/*.html`), `news`, or `other`. This enables funnel analysis by content type without manual tagging.

## Drop-in `ga4-events.js` (full source — deployed version)

```javascript
// ===== GA4 EVENT TRACKING =====
// Centralized event tracking for chinahospitalsguide.com
// Requires gtag.js + dataLayer to be loaded (see <head> in each page).
// Author: Hermes (2026-07-02)
(function() {
    'use strict';
    if (typeof gtag === 'undefined') return;

    var PAGE_TYPE = document.body.getAttribute('data-page-type')
        || (location.pathname.indexOf('/blog/') === 0 ? 'article'
            : (location.pathname.indexOf('/news/') === 0 ? 'news'
                : (location.pathname === '/' || location.pathname === '/index.html' ? 'home'
                    : (location.pathname.indexOf('/blog') === 0 ? 'blog_index' : 'other'))));

    // -------- 1. SCROLL DEPTH --------
    var scrollMarks = { '25': false, '50': false, '75': false, '100': false };
    var articleCompleteFired = false;
    var dwellStart = Date.now();

    function trackScroll() {
        var docHeight = Math.max(document.body.scrollHeight, document.documentElement.scrollHeight);
        var winHeight = window.innerHeight;
        var scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        if (docHeight <= 0) return;
        var scrollPercent = Math.floor(((scrollTop + winHeight) / docHeight) * 100);
        for (var pct in scrollMarks) {
            if (!scrollMarks[pct] && scrollPercent >= parseInt(pct, 10)) {
                scrollMarks[pct] = true;
                gtag('event', 'scroll_depth', {
                    'event_category': 'engagement',
                    'event_label': pct + '%',
                    'page_type': PAGE_TYPE,
                    'page_path': location.pathname,
                    'value': parseInt(pct, 10)
                });
            }
        }
    }
    var scrollTimer = null;
    window.addEventListener('scroll', function() {
        if (scrollTimer) return;
        scrollTimer = setTimeout(function() { trackScroll(); scrollTimer = null; }, 150);
    }, { passive: true });
    window.addEventListener('load', trackScroll);

    // -------- 2. ARTICLE COMPLETE (100% scroll + 30s dwell) --------
    function maybeFireArticleComplete() {
        if (articleCompleteFired) return;
        if (!scrollMarks['100']) return;
        if (Date.now() - dwellStart < 30000) return;
        articleCompleteFired = true;
        gtag('event', 'article_complete', {
            'event_category': 'engagement',
            'event_label': 'read_full_article',
            'page_type': PAGE_TYPE,
            'page_path': location.pathname,
            'value': 1
        });
    }
    setInterval(maybeFireArticleComplete, 5000);
    window.addEventListener('beforeunload', maybeFireArticleComplete);

    // -------- 3. CTA + OUTBOUND + INTERNAL CLICK --------
    document.addEventListener('click', function(e) {
        var target = e.target.closest('a, button');
        if (!target) return;
        var href = target.getAttribute('href') || '';
        var text = (target.textContent || '').trim().substring(0, 80);

        if (target.classList.contains('cta-button') || target.classList.contains('nav-cta')
            || target.classList.contains('btn-primary') || target.classList.contains('btn-cta')) {
            gtag('event', 'cta_click', {
                'event_category': 'conversion', 'event_label': text,
                'cta_text': text, 'cta_href': href,
                'page_type': PAGE_TYPE, 'page_path': location.pathname
            });
            return;
        }
        if (href && (href.indexOf('contact.html') !== -1 || href.indexOf('contact-new') !== -1 || href.indexOf('/contact') !== -1)) {
            gtag('event', 'cta_click', {
                'event_category': 'conversion', 'event_label': 'Contact CTA',
                'cta_text': text, 'cta_href': href,
                'page_type': PAGE_TYPE, 'page_path': location.pathname
            });
            return;
        }
        if (href && (href.indexOf('http://') === 0 || href.indexOf('https://') === 0)
            && href.indexOf('chinahospitalsguide.com') === -1
            && href.indexOf('localhost') === -1) {
            gtag('event', 'outbound_click', {
                'event_category': 'engagement', 'event_label': text,
                'outbound_url': href,
                'page_type': PAGE_TYPE, 'page_path': location.pathname
            });
            return;
        }
        if (href && href.indexOf('#') !== 0 && href.indexOf('javascript') !== 0
            && (href.indexOf('/blog/') !== -1 || href.indexOf('.html') !== -1)) {
            gtag('event', 'internal_click', {
                'event_category': 'navigation', 'event_label': text,
                'link_path': href,
                'page_type': PAGE_TYPE, 'page_path': location.pathname
            });
        }
    }, true);

    // -------- 4. NEWSLETTER FORM SUBMIT (Formspree) --------
    document.addEventListener('submit', function(e) {
        var form = e.target;
        if (!form || form.tagName !== 'FORM') return;
        var action = form.getAttribute('action') || '';
        if (action.indexOf('formspree.io') !== -1) {
            gtag('event', 'newsletter_submit', {
                'event_category': 'conversion', 'event_label': 'Newsletter Signup',
                'form_action': action,
                'page_type': PAGE_TYPE, 'page_path': location.pathname, 'value': 1
            });
        }
    }, true);

    // -------- 5. FILE DOWNLOADS --------
    document.addEventListener('click', function(e) {
        var target = e.target.closest('a');
        if (!target) return;
        var href = target.getAttribute('href') || '';
        if (/\.(pdf|doc|docx|xls|xlsx|zip|rar)(\?|$)/i.test(href)) {
            gtag('event', 'file_download', {
                'event_category': 'engagement', 'event_label': href.split('/').pop(),
                'file_url': href,
                'page_type': PAGE_TYPE, 'page_path': location.pathname
            });
        }
    }, true);

})();
```

## HTML injection (per page)

Add this single line right after the `gtag('config', 'G-RVYZENK472');</script>` block in every page that has the GA4 base config:

```html
    <script src="ga4-events.js" defer></script>
```

That's it. The script auto-detects whether gtag is loaded and gracefully no-ops if not.

## ⚠️ CRITICAL: Eleventy passthrough copy (verified mistake 2026-07-02)

`ga4-events.js` MUST be added to `eleventy.config.js`'s `addPassthroughCopy` list, OR it returns 404 in production even though git has it. See the "Eleventy passthrough-copy pitfall" section in `SKILL.md` for the full symptom + fix.

```js
// eleventy.config.js
eleventyConfig.addPassthroughCopy("ga4-events.js");
```

Existing passthrough list (2026-07-02): `styles.css`, `ga4-events.js`, `images/`, `CNAME`, `.nojekyll`, `robots.txt`, `sitemap.xml` + globs `news/`, `blog/`, `stories/`, `treatments/`, `*.html`.

## Bulk-deploy recipe (Python `execute_code`)

Use this script when deploying event tracking to a fresh site or adding a new event type. Deployed version lives at `scripts/inject-ga4-events.py`.

```python
import re
from pathlib import Path

ROOT = Path('/home/ubuntu/.hermes/workspace/website')
SCRIPT_TAG = '\n    <script src="ga4-events.js" defer></script>'
skip_prefixes = ('docs/', 'blog-export/', 'blog-articles/', 'templates/',
                 'api/', '医疗旅游/', '_site/', 'node_modules/')

# CORRECT regex — \s* alone covers newlines + whitespace
INJECT_PATTERN = re.compile(r"(gtag\('config', 'G-[A-Z0-9]+'\);\s*</script>)")
# Use this for files where </script> was accidentally removed
RESTORE_PATTERN = re.compile(r"(gtag\('config', 'G-[A-Z0-9]+'\);)")

stats = {'restored-and-injected': [], 'injected': [], 'already-has': [], 'no-gtag': [], 'skipped': []}
for path in ROOT.rglob('*.html'):
    rel = str(path.relative_to(ROOT))
    if rel.startswith(skip_prefixes) or rel.startswith('report-'):
        stats['skipped'].append(rel); continue
    try: content = path.read_text(encoding='utf-8')
    except Exception: continue
    if 'googletagmanager.com/gtag' not in content: continue
    if 'ga4-events.js' in content: stats['already-has'].append(rel); continue

    m = re.search(r"gtag\('config', 'G-[A-Z0-9]+'\);", content)
    if not m: stats['no-gtag'].append(rel); continue
    after = content[m.end():m.end()+80]

    if '</script>' in after:
        new_content = INJECT_PATTERN.sub(r"\1" + SCRIPT_TAG, content, count=1)
        stats['injected'].append(rel)
    else:
        # Damaged: restore </script> + inject
        new_content = RESTORE_PATTERN.sub(r"\1\n    </script>" + SCRIPT_TAG, content, count=1)
        stats['restored-and-injected'].append(rel)

    if new_content != content:
        path.write_text(new_content, encoding='utf-8')

print(f"Restored+injected: {len(stats['restored-and-injected'])}")
print(f"Injected:          {len(stats['injected'])}")
print(f"Already has:       {len(stats['already-has'])}")
print(f"No gtag:           {len(stats['no-gtag'])}")
print(f"Skipped:           {len(stats['skipped'])}")
```

## ⚠️ Two regex pitfalls verified this session

**Pitfall #1 — `\s*\n\s*` whitespace trap**: Python's `\s` character class **already includes `\n`**. So `\s*\n\s*</script>` will NEVER match — the first `\s*` greedily eats the newline, then the literal `\n` can't be found. Use `\s*</script>` (one `\s*` covers everything including newlines). Verified wrong → fixed.

**Pitfall #2 — Greedy inline-block removal**: When trying to remove the old inline tracking code (added 2026-07-02 morning commit `1c03aab`), a pattern like `\n\s*//\s*={3,}\s*GA4 EVENT TRACKING.*?</script>` (DOTALL) will swallow the OUTER `</script>` of the gtag config block too, leaving the page with an unclosed script tag. **Fix: don't try to remove inline blocks at all — just leave them and add the external script reference after the gtag config's `</script>`.**

## Verification protocol (post-deploy)

After `git push` and GitHub Actions build completes (~2-3 min):

```bash
# 1. File itself serves correctly
curl -sI https://chinahospitalsguide.com/ga4-events.js | head -3
# Expect: HTTP/2 200, server: GitHub.com, content-type: application/javascript

# 2. HTML pages reference the script
curl -s https://chinahospitalsguide.com/ | grep -c "ga4-events.js"
# Expect: 1 (one reference per page)

# 3. Sample 3 different page types
for url in https://chinahospitalsguide.com/ \
           https://chinahospitalsguide.com/blog/best-cancer-hospitals-china-2026.html \
           https://chinahospitalsguide.com/news/2026-03-27-china-bci-neuralink-compare.html; do
    count=$(curl -s "$url" | grep -c "ga4-events.js")
    echo "$url: $count references"
done

# 4. <script> tag count balanced (no orphan opens/closes)
for f in index.html blog/index.html blog/best-cancer-hospitals-china-2026.html; do
    op=$(grep -c "<script\b" "$f"); cl=$(grep -c "</script>" "$f")
    echo "$f: open=$op close=$cl"
done
# All should show open == close
```

## After 7 days — read the data

GA4 → Reports → Engagement → Events. Filter by event name.

**What to look for**:
- **Average scroll depth** per page: if homepage < 50%, the Trust/Newsletter/Featured Articles sections aren't holding attention.
- **`article_complete` rate**: this is your "real reader" metric — users who scrolled to the bottom AND stayed 30s. Combine with CTA click rate for true engagement quality.
- **`cta_click` by page_type**: comparison between `article`, `home`, `blog_index` shows where CTAs land best.
- **`outbound_click` rate**: high outbound = users leaving for hospital official sites = high intent. Consider a softer "Free case review" CTA before outbound links.
- **`internal_click` paths**: which articles cross-link to which other articles. Useful for content gap analysis (orphan pages with 0 internal clicks = invisible).

**Next-level actions** based on data:
- Pages with high scroll depth but low CTA clicks → CTA too far down or visually weak.
- Pages with low scroll depth → first 800 words need a hook / TOC / Quick Answers to retain attention.
- High outbound-click rate + low `cta_click` → users want info but don't trust the funnel yet. Add social proof or testimonials.
- `article_complete` rate < 20% site-wide → content density problem; consider TL;DR or FAQ blocks at the top.

## MS Clarity (heatmaps + session replay) — companion to GA4

Clarity is **complementary**, not a replacement. It captures session recordings and heatmaps that GA4 cannot.

**Status (2026-07-02)**: NOT YET DEPLOYED. Pending Project ID from owner (B2 todo: register at https://clarity.microsoft.com tonight).

**Deploy pattern** (when Project ID is available — same flow as GA4 injection):

```html
<!-- Microsoft Clarity — add after GA4 config, inside <head> -->
<script type="text/javascript">
    (function(c,l,a,r,i,t,y){
        c[a]=c[a]||function(){(c[a].q=c[a].q||[]).push(arguments)};
        t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;
        y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);
    })(window, document, "clarity", "script", "CLARITY_PROJECT_ID_HERE");
</script>
```

**Ship-now-wire-later pattern**: If Project ID isn't ready yet, add a placeholder HTML comment in the `<head>` so the deployment step doesn't have to be done twice:

```html
<!-- Microsoft Clarity — ready, awaiting 10-char Project ID from owner -->
<!-- 
STEPS:
1. Register https://clarity.microsoft.com (free, unlimited traffic)
2. Add chinahospitalsguide.com project
3. Get Project ID (10-char alphanumeric)
4. Global replace CLARITY_PROJECT_ID_HERE -> Project ID
5. Uncomment the <script> block below
6. git commit + push
-->
<!-- <script type="text/javascript">...clarity snippet...</script> -->
```