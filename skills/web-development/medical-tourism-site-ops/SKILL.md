---
name: medical-tourism-site-ops
description: "Operations workflow for English-language medical tourism websites covering China (chinahospitalsguide archetype) — content matrix strategy, SEO technical patterns, duplicate-content defense, static site deployment to Cloudflare via GitHub, conversion blocks (trust + newsletter + featured-pillar + ranking-page decision-tree), GA4/MS-Clarity event tracking, and how the user wants this class of work run (iterative, single-step verified, no grand roadmaps)."
version: 0.5.0
author: Hermes Agent
platforms: [linux]
metadata:
  hermes:
    tags: [medical-tourism, seo, content-ops, chinahospitalsguide, static-site, cloudflare, conversion, gsc, ga4, clarity, schema]
    category: web-development
---

# Medical Tourism Site Ops (English-language China health-travel websites)

This skill covers the recurring operational class of running an English-language medical-tourism/content site focused on **China** as a destination (the chinahospitalsguide.com archetype). It captures the strategic content-matrix decisions, the SEO technical patterns that work on static HTML pages, the duplicate-content defense needed when multi-agent pipelines generate similar content, the static-site GitHub-to-Cloudflare deployment, the conversion blocks (trust / newsletter / featured-pillar) that turn traffic into leads, **GSC data-driven SEO workflow (title/description optimization from search-console data)**, and the subagent orchestration patterns that bulk-content generation requires.

It does NOT cover content writing itself (covered by `content-research-writer-cn`, `programmatic-seo`, `humanizer`) — those handle the *what* of an article. This skill handles the *how the site is run*, *how content is distributed and cross-linked*, *how GSC data drives SEO edits*, and *how conversion paths are built*.

## Workflow preference — single-step, verified, no long roadmaps (USER PREFERENCE — STRONG)

The user has explicitly rejected long-horizon roadmaps ("90 天方案太长 一个个来", "一步步做 做到那个算那个"). When asked "what should we work on next", the correct response is:

1. **Pick the ONE highest-ROI thing the user explicitly hinted at** (their words, not mine).
2. **Do it fully** — execute, verify, commit, push, confirm live URL.
3. **Report what was done with the actual artifacts** (file paths, diff stats, HTTP status).
4. **Then ask what to do next** with a short list of remaining items if appropriate.

DO NOT, in a single response:
- Lay out a "90-day roadmap" of 30+ items.
- Defer verification / measurement to "next phase".
- Add a "Phase 2" / "Phase 3" outline before Phase 1 is finished.
- Promise ongoing automation that wasn't explicitly requested.

DO feel free to mention what's STILL UNDONE as a short list (3-8 items, not 30+), but only AFTER the current step is complete.

The signal "follow up on the 90-day plan" / "what's left from the 90-day plan" still requires this preference to apply — answer with what was completed and a short remaining list, not the original 30-item plan.

### ⚠️ "90-day plan" trap — DO NOT fabricate (VERIFIED 2026-07-02)

When the user says "按 90 天方案继续", the trap is to **immediately execute the plan as if it were vetted**. The plan itself may have been generated in a single past session with **no underlying data** — GSC data, ROI calculation, customer validation, etc.

**The verified failure (2026-07-02)**: I had a "90-day plan" with 15 items, of which 7 were already done. I picked items by **my own gut-feeling of "high ROI"** and executed 5 "decision guide long-tail pages" (liposuction Beijing, LASIK Shanghai, etc.). Total GSC impressions for all 5 target queries combined: **< 100 per month**. The pages were deployed, then user said **"5 个决策页回滚"** — they were dead on arrival.

**The fix — execute this audit BEFORE any "continue the plan" instruction**:

1. **Question the plan's data basis.** Ask: "这个 90 天方案的 15 项是基于什么数据生成的？" Don't apologize — just ask.
2. **Cross-check each item against current GSC/GA4 data.** Use `gsc opportunities`, `gsc top pages`, `gsc top q` to verify there is real search demand for the topic. If impressions < 100/mo for the target query, skip the item.
3. **Check for "fictional case studies" / "patient stories"** — these are often content placeholders. Ask the user before building more.
4. **Look at what the user actually has revenue-side** — confirmed customers, actual conversion path. If they have 0 real customers (as of 2026-07-02 user confirmed), do NOT build "patient story" pages or trust signals that depend on social proof.

**The user said this verbatim**: *"我看你摆数据说的头头是道的 我也拍脑袋 并没有深入研究数据 反正也是觉得做就对了"* — the user is admitting the same trap. Mutual questioning is the fix.

### ⚠️ Collaboration model — question and push back, don't just execute (VERIFIED 2026-07-02)

When the user says "行按这个执行" / "按你的理解去做" / "你按你的理解去做" / "没有顺序 你按照你的理解去做" — this is **complete authorization, not a gag order**. The user expects:

1. **Pick the order** based on actual ROI, not gut.
2. **Question the underlying assumptions** of the plan if they are weak.
3. **Surface disagreements before doing 6 hours of work** that may need to be reverted.
4. **State the data basis** for each decision. "I'm picking this because GSC shows X impressions/mo and the page has CTR of Y%" — not "this feels important".

**The verified failure**: I executed a 5-page "decision guide" rollout without ever asking "are these queries from real patients or just SEO data noise?". Result: 5 pages deployed, then reverted. Wasted 30 min of commits + 2 hours of git history noise + user trust.

**The pattern**: after saying "行", immediately voice the *one or two* reservations you have, then proceed with the highest-confidence item only. Don't dump 5 items of reservations and ask permission — that's worse than the original problem. State the top 1-2 doubts AND the recommended path, in 2-3 lines total.

**The user's correction was explicit**: *"不是说你自作主张 你有发表你意见的权利 我也能接受 但是我也有质疑的权利 我们的目标是共同把项目好好做下去 我说的话 你同样有质疑我的权利 所以不需要道歉"*. Translation: "Don't apologize, push back when warranted. We are partners on this project."

## Site archetype: chinahospitalsguide.com stack (verified 2026-07-01)

- **Stack:** static HTML generated by **Eleventy** (Nunjucks templates). Source files at repo root; Eleventy builds into `_site/`; **the `_site/` directory is what actually gets served.**
- **Deploy:** **GitHub Pages** (NOT Cloudflare — `chinahospitalsguide.com` resolves to GitHub Pages IPs 185.199.108-111.153; `www.` subdomain is on Cloudflare but apex is GitHub Pages). Triggered by `.github/workflows/deploy.yml` on push to master: `npm ci → npm run build → upload _site artifact → deploy`.
- **Repo:** `https://github.com/qzw-alt/chinahospitalsguide`
- **CNAME file** controls the apex domain — do NOT edit.
- **Content layout (verified 2026-07-02 — FULL coverage required for any site-wide operation):**
  - `index.html` — homepage (full HTML rewrite risk = high; surgical `<section>` inserts only)
  - `blog/<slug>.html` — evergreen guides (107 articles in mid-2026, target ~300-500 over 2 years)
  - `blog/index.html` — blog landing page (filter buttons, popular topics section, "latest articles" grid)
  - `news/<slug>.html` — daily news articles (1/day cadence, demoted to 2-3 days/week as content depth grows)
  - `treatments/<slug>.html` — **specialty landing pages** (cancer.html, cardiac.html, ivf.html, orthopedics.html, stem-cell.html, nutcracker-syndrome.html, orthopedic-surgery-china.html). Often missed in site-wide operations. Currently 7 files.
  - `hospitals/`, `stories/`, etc. — supporting content
  - Root landing pages (`about.html`, `contact.html`, `contact-new.html`, `services.html`, `hospitals.html`, `pricing.html`, `how-it-works.html`, `checklist.html`, `cost-comparison.html`, `privacy.html`, `terms.html`, `ivf.html`, `cancer.html`, `orthopedics.html`, `resources.html`, `medical-chinese-phrases.html`) — **16 files**. Often missed in site-wide operations.
  - `docs/` directory — legacy documentation copy of public pages (mirror). Should be treated as duplicates — never the canonical version. Schema updates should still reach them but content rewrites should target the canonical non-docs path.
  - `blog-export/blog-articles/` and `blog-export/` — **export backup of blog content**. Not deployed (or deployed as dead weight). **Always skip in any site-wide operation.**
  - `report-carlos-mendoza-*` — **programmatic per-patient report templates, one file per timestamp**. Generated by another agent/cron. Skip in any site-wide operation.
  - `404.html`, `panel.html`, `api/`, `course/`, `patient-story-program.html` — utility pages, no SEO value. Skip.
  - `sitemap.xml` — single file, hand-maintained `lastmod` dates
  - `_redirects` — 301 redirects for legacy phantom URLs and duplicates
- **Analytics:** GA4 (`G-RVYZENK472`), AdSense (`ca-pub-2521119288266043`)
- **CDN-cache gotcha:** external stylesheets via CDN cache hard; CSS must be **inline `<style>` blocks** per-page, not external. This is documented in the project memory and is critical when matching the existing blog template style. Same rule for ALL conversion blocks — Trust section, Newsletter form, Featured Pillar, Decision Tree, Quick Answers — all inline.

### ⚠️ Site-wide operation scope checklist (NEW 2026-07-02 — VERIFIED MISTAKE)

When running any site-wide operation (schema batch, sitemap regen, link audit, header/footer change, analytics deployment), the **scope to cover is ALL of these**, not just `blog/` + `news/`:

1. ✅ `blog/*.html` (105 files mid-2026)
2. ✅ `news/*.html` (83 files)
3. ✅ `treatments/*.html` (7 files — cancer, cardiac, ivf, orthopedics, stem-cell, nutcracker-syndrome, orthopedic-surgery-china)
4. ✅ Root landing pages: `about.html`, `contact.html`, `contact-new.html`, `services.html`, `hospitals.html`, `pricing.html`, `how-it-works.html`, `checklist.html`, `cost-comparison.html`, `privacy.html`, `terms.html`, `ivf.html`, `cancer.html`, `orthopedics.html`, `resources.html`, `medical-chinese-phrases.html` (16 files)
5. ⚠️ `docs/*.html` — legacy doc copy. **Still update for consistency if doing schema/header/footer**, but never treat as canonical.
6. ⏭️ `blog-export/blog-articles/` + `blog-export/` — **export backup, SKIP** (duplicate of blog/).
7. ⏭️ `report-carlos-mendoza-*` — programmatic per-patient report templates, **SKIP** (auto-generated, one per timestamp).
8. ⏭️ `404.html`, `panel.html`, `api/index.html`, `course/index.html`, `patient-story-program.html` — utility pages, **SKIP** (no SEO value).

**The verified failure (2026-07-02)**: I ran "P1-1 schema batch coverage" covering only `blog/` + `news/` — reported "100% coverage" with 152 files changed. **43 content pages were missed**: 16 root landing + 7 treatments + 20 docs. The user's verification step ("我怕你白忙了 你先确认下") caught this. Without that prompt I would have shipped an "incomplete complete".

**Pre-flight scan** (10 seconds, prevents the mistake):
```bash
cd /home/ubuntu/.hermes/workspace/website
for d in blog news treatments; do
  count=$(find $d -name "*.html" 2>/dev/null | wc -l)
  echo "$d: $count"
done
echo "root landings:"
ls *.html | grep -vE "^(index|404|panel|patient-story-program)\.html$" | wc -l
echo "docs:"
find docs -name "*.html" 2>/dev/null | wc -l
echo "blog-export:"
find blog-export -name "*.html" 2>/dev/null | wc -l
echo "report-carlos:"
ls report-carlos-*.html 2>/dev/null | wc -l
```
Expected (mid-2026): blog 105, news 83, treatments 7, root 16, docs ~50, blog-export ~33, report-carlos ~4.

## Content matrix strategy (China-first, TCM-integrated)

The site has a recurring content mandate from the user: focus on the **特殊性唯一性** (special/unique) factor — medical procedures and projects that are truly unique to China or where China offers a genuine advantage that cannot be replicated elsewhere.

**Three content axes, in priority order:**

1. **Axle A: China-only / China-leading procedures** (CAR-T, autonomous robotic surgery, stem cell via Hainan Boao Lecheng, integrated Chinese-Western medicine, 3D-printed implants, CRISPR clinical trials, hepatobiliary surgery, transplant). High search volume for "X in China" queries, defensible against competition.
2. **Axle B: Traditional Chinese Medicine (TCM) — acupuncture, herbal, moxibustion, cupping, baduanjin/tai chi, integrated oncology/IVF/cardiac/orthopedic adjuncts.** TC-integrated protocols are a real differentiator that no other destination offers at scale.
3. **Axle C: World-leading volume specialties** (ophthalmology, orthopedics, cardiac surgery, microsurgery, IVF) where China's surgical volume + JCI network make it a credible first-tier destination.

For each new article or content batch, prefer a topic that combines at least 2 of the 3 axles (e.g. "solid-tumor CAR-T" = A; "acupuncture adjunct for IVF" = B; "SMILE refractive surgery in China" = C; "integrated oncology with TCM support" = A+B).

### TCM content injection pattern (verified across 49 blog articles, 2026-07-01)

When the user instructs to "fuse TCM into the existing blog" or any variant, apply this pattern:

1. **Categorize** every blog article by disease/procedure: cancer, orthopedic, IVF, eye, dental, cardiac, neuro, cosmetic, kidney-dialysis, organ-transplant, etc. (regex match on filename slug).
2. **Build one TCM injection block per category** — 200-300 words, structured: heading 🌿 + 1 paragraph framing + 3 bullet points (specific TCM therapies + cost anchor + safety note) + 2-3 internal cross-links to TCM pillar pages. Use a **green color family** (`#28a745`, `#155724`, `#d4edda`) so it reads visually different from existing content but stays on-brand.
3. **Find an insertion anchor** in each article — preference order:
   1. Before `<h2 id="related-articles">` or `<h2>📚 Related Articles</h3>` if present
   2. Before `<footer` if no Related Articles section
   3. Before `</div></body>` as last resort
4. **De-dupe check:** skip articles that already contain the TCM marker emoji 🌿 in the body.
5. **Skip non-disease articles:** city guides, hospital rankings, "how to book" pages, visa pages, pricing pages — these are not TCM-injection candidates by default.

### Pillar page structural pattern (China-unique procedures)

When the user asks for a "pillar page", "framework guide", or "single source of truth" article:

1. **Master pillar page** = 4,500-5,500 words, 10 sections, TOC with named anchors, FAQ with 5-7 questions, JSON-LD FAQPage + Article + BreadcrumbList.
2. **Sub-pillar pages** = 1,200-1,500 words each, 1 sub-topic per page, same schema.org markup pattern.
3. **Sub-pages must cross-link to the master AND to each other** where relevant (3-5 internal cross-links per sub-page, anchor-text-rich).
4. **Master pillar is the canonical slug** — sub-pages use the master's filename as the prefix source for canonical confusion checks.

**Pillar topics that work (verified demand):**
- China-unique medical procedures (10 anchor topics: robot surgery, CAR-T, stem cell, integrated medicine, microsurgery, hepatobiliary, transplant, 3D implants, CRISPR, ophthalmology)
- TCM guide + TCM therapy cost (acupuncture, herbal, moxibustion, cupping)
- City hospital guides (Beijing, Shanghai, Guangzhou, Chengdu, Xi'an, Shenzhen)
- Procedure cost guides (LASIK, cataract, IVF, knee/hip replacement, cardiac bypass)

## SEO technical patterns on static HTML

### Hospital ranking page → Featured Snippet (verified 2026-07-01, `best-hospitals-china-international-patients.html`)

The "Top 10" / "Best Hospitals" article archetype is the highest-value SEO target (high search volume, GSC positions 5-9, zero-click problem). The optimization template:

1. **Quick Decision block** (deep-blue gradient `#1e3c72 → #2a5298` background) — 8-12 cards, one per specialty/condition, each card: emoji + condition name + 1-paragraph "Start with: X hospital. $X cost vs $X US/West" + deep link to specialty page. Insert **between the "Quick Cost Overview" / cost-highlight block and the TOC**.
2. **Quick Answers block** — 5 high-impact Q&As in `X is Y` format (Google Featured Snippet preferred phrasing). Insert **between the TOC and the first detail section (Section 1)**.
3. **Add JSON-LD schemas** at the top of `<head>` after the existing Article schema:
   - `MedicalWebPage` — helps Google classify as a medical-decision page
   - `BreadcrumbList` — improves SERP display
4. **Preserve existing content** — do NOT remove the original FAQ section at the bottom; the JSON-LD FAQPage schema needs the on-page FAQ to match.
5. **Cross-link strategy** — 8+ internal links to:
   - Specialty ranking pages (best-cancer-hospitals, china-orthopedic-hospital-rankings, etc.)
   - Cost pages (cost-comparison-procedures, individual procedure cost pages)
   - City guides (hospitals-in-X-for-international-patients)
   - Process pages (how-to-book-hospital-appointment-china, china-medical-visa-guide)

### FAQ schema and placement

- Every evergreen blog article should have a JSON-LD `FAQPage` schema with 4-7 questions.
- Questions should match the format people actually search (Google autocomplete, "People Also Ask" boxes), not abstract topic questions.
- On-page FAQ can stay at the bottom OR move to a "Quick Answers" callout near the top — both work.

### Blog index page filter bug pattern (verified 2026-07-01)

The `<div class="blog-grid">` MUST have `id="blog-grid"` for any JS `document.getElementById('blog-grid')` filter to work. When auditing an existing blog index page that has filter buttons in the HTML but clicking them does nothing, **always check this first**. The fix is one character: add the id attribute. This bug is recurring because it's syntactically valid HTML (the class is there, the JS just can't find the element).

When the bug exists, ALL filter buttons silently fail (JavaScript throws on `null.querySelectorAll`). The page still LOOKS fine — it just doesn't filter. Easy to miss without interactive testing.

### Common tag/attribute mismatches (audit checklist)

When a single-page interactive feature (filter, tab switcher, accordion, modal) is in the HTML but doesn't work in the browser, the fix is almost always one of:

1. `id="X"` missing on the target div → JS `getElementById` returns null
2. `onclick="foo(...)"` defined but `foo` not in scope at click time (script loaded after the inline handler)
3. `<button>` inside `<a>` or nested interactive elements (HTML spec violation; click bubbling breaks)
4. `event.target.classList.add('active')` but the element has `class="filter-btn"` not `class="filter-btn active"` (initial mismatch)

## Conversion blocks (verified 2026-07-01)

Three conversion-orientation blocks were added to spread trust + capture points beyond the hero CTA:

1. **Homepage Trust Section** (4 stat cards + "Coverage & References" row) — anchors on real data (1.28M patients 2025 from existing news), no fake logos, includes disclaimer.
2. **Homepage Newsletter Form** — Formspree endpoint placeholder (`REPLACE_WITH_YOUR_FORMSPREE_ID`) for ship-now-wire-later pattern. Includes honeypot anti-spam and success-redirect for GA observation.
3. **Blog Index Featured Pillar block** — deep-blue gradient card linking to the 4 strongest pillar pages, sits BEFORE the existing "Latest Articles" grid. A second "Browse by What Makes China Different" block follows with 3 themed categories (TCM / Frontier Medicine / World's-Best Volume).

All three follow the inline-style-no-CDNCache rule. See `references/conversion-optimization.md` for copy-paste HTML and the CDN cache verification protocol.

**Where conversion blocks live in the page hierarchy:** hero (CTA only) → Helpful Guides → Trust Stats + Newsletter → Featured Articles (What Only China Can Do) → Latest News → Footer. Trust and Newsletter sit between "Helpful Guides" and the Featured Articles section so users see evidence + offer right before they decide to engage with the article cluster.

## GSC (Google Search Console) data-driven SEO workflow (verified 2026-07-01)

**The single highest-ROI recurring SEO task on this site:** GSC shows you which pages rank for which queries with 0 clicks. Fixing the title/description of those pages gives immediate CTR lift (3-5x is realistic) at zero ranking cost.

**Full setup details (OAuth, gotchas, cron) in `references/gsc-oauth-setup.md`. The high-level workflow:**

1. **Auth once** (one-time): OAuth client + test user + enable Search Console API + run `templates/gsc-authorize.py`. Token at `~/.hermes/gsc/token.json`.
2. **Query weekly** (or on-demand): `gsc opportunities` returns 20 highest-volume query+page pairs with `position <= 20 + CTR < 5% + impressions >= 5`. This is your 0-click gold mine.
3. **Batch edit 4-10 pages per round** with the 4-tag meta edit (title + description + og:title/desc + twitter:title/desc, all in sync). The recipe is in `references/gsc-oauth-setup.md` under "Meta-tag batch-edit recipe".
4. **Commit, push, verify** with the same git→Cloudflare→HTTP 200 pattern as any other site change.
5. **Wait 7-14 days** for Google re-crawl, then re-run `gsc opportunities` and `gsc compare` to see the lift.
6. **Repeat** every 2-4 weeks until the gold mine is depleted; then the next bottleneck is content depth (more long-tail coverage), not meta quality.

**The 4-tag meta edit pitfall:** when batching meta edits, do NOT use `patch` with `replace_all=true` if your new string also contains generic-looking tokens like `<title>` or `description`. The tool does literal string matching and can rewrite other meta tags accidentally (verified: 4 `<title>` tags, 0 `og:title` tags). Use `execute_code` with `Path.read_text().replace().write_text()` instead, then `grep -c "<title>" file.html` to verify count is exactly 1.

**Auto-monitoring:** the `gsc-weekly-report.sh` cron (job_id `16a08d0ea83d`, every Monday 07:00 CST) delivers the weekly report to Feishu. Zero LLM tokens (no_agent mode).

## Conversion analytics: GA4 event tracking + MS Clarity (deployed site-wide 2026-07-02)

The site had GA4 base config (`G-RVYZENK472`) on every page but **zero event tracking**. After 2026-07-02 deployment, **217 pages** carry full event tracking via external `ga4-events.js`:

| Event | Trigger | Reports to |
|---|---|---|
| `scroll_depth` (25/50/75/100%) | Scroll milestones | Engagement |
| `article_complete` | 100% scroll + 30s dwell | Engagement |
| `cta_click` | `.cta-button`, `.nav-cta`, `.btn-primary`, `.btn-cta`, or any `contact*` link | Conversion |
| `outbound_click` | External links (not chinahospitalsguide.com) | Engagement |
| `internal_click` | Internal navigation (article-to-article) | Navigation |
| `newsletter_submit` | Formspree form submission | Conversion |
| `file_download` | PDF/doc/zip links | Engagement |

**Architecture**: External `ga4-events.js` (6.9KB, `<script src="ga4-events.js" defer></script>`) — NOT inlined per-page. One file, browser-cached across all 217 pages, easy to maintain. PAGE_TYPE auto-detected from URL path (article/news/home/blog_index/other) so events carry content-type context for funnel analysis.

**Full drop-in code, bulk-deploy recipe (the `inject-ga4-events.py` Python script), regex pitfall warning, and the Eleventy passthrough requirement:** `templates/ga4-event-tracking.md`.

**⚠️ Two regex pitfalls verified this session — READ BEFORE deploying:**

1. **Inline-block removal regex gotcha:** when removing the original inline tracking block (added 2026-07-02 by the previous session), a greedy `.*?</script>` DOTALL pattern can swallow the OUTER `</script>` of the gtag config block, leaving it unclosed and breaking the page. The fix: don't try to remove inline blocks — just leave them and overwrite with the external script reference. OR use a non-greedy regex with explicit close-tag capture.

2. **The `\s*\n\s*` whitespace regex trap:** Python regex `\s*` already includes `\n`, so `\s*\n\s*</script>` will NEVER match (the first `\s*` greedily eats the `\n`, then the literal `\n` can't be found). Use plain `\s*</script>` instead. Verified wrong → fixed.

**Microsoft Clarity (companion to GA4)** is heatmaps + session replay — surfaces things GA4 can't (where users rage-click, where they get confused, mobile vs desktop behavior diffs). Ship-now-wire-later pattern: deploy a placeholder comment block with `CLARITY_PROJECT_ID_HERE`, then user does the 5-minute registration + ID replacement step. Don't try to create the Clarity project from the agent — it requires a Microsoft account owner-side OAuth step.

**MS Clarity deploy verified 2026-07-02** (Project ID `xg5cmwdl4y`, commit `88bc358`): replaced `CLARITY_PROJECT_ID_HERE` placeholder + uncommented the `<script>` block in `index.html` + `blog/index.html`. Deploy in 2 files only (homepage + blog index — these get 95%+ of traffic; instrumenting every page would burn user bandwidth). When deploying, also remember **Eleventy passthrough copy rule** if the snippet lives in a separate file — but for inline Clarity script, no passthrough needed.

### ⚠️ Pre-deploy analytics audit pitfall (NEW 2026-07-02)

**Lesson**: Before adding ANY inline tracking code (GA4 events, MS Clarity, custom JS) to a page on this site, **first check if the page already references a site-wide external script**.

Symptom I hit: I spent ~10 minutes writing inline GA4 event tracking JS (scroll_depth / cta_click / outbound_click) and committing it (commit `1c03aab`). Then discovered via `grep "ga4-events.js" /index.html` that commit `d481cac` had ALREADY refactored event tracking into an external `ga4-events.js` site-wide, with **7 events** (more comprehensive than my 3) deployed to **217 pages**. My inline code on 2 pages was redundant and would have shipped duplicate events if not caught.

**The pre-deploy check** (5 seconds, saves 10+ minutes):
```bash
grep -rE "(ga4-events\.js|clarity\.ms|googletagmanager)" /home/ubuntu/.hermes/workspace/website/*.html /home/ubuntu/.hermes/workspace/website/blog/index.html 2>/dev/null | head -5
```
If you see references to an existing analytics file/script, that's the canonical implementation — extend it via a new commit to that file, not by adding inline code.

**The rule on this site**: **analytics code is site-wide via external script**. New events = add to the existing `ga4-events.js`, not to per-page HTML.

## Newsletter / Formspree pattern (verified 2026-07-02)

The newsletter form lives on 2 pages: `index.html` (homepage) + `blog/index.html` (blog landing). Both use the same Formspree endpoint pattern:

```html
<form action="https://formspree.io/f/REPLACE_WITH_YOUR_FORMSPREE_ID" method="POST" style="display:flex;flex-wrap:wrap;gap:12px;justify-content:center;max-width:560px;margin:0 auto">
    <input type="email" name="email" required placeholder="your.email@example.com" style="...">
    <input type="hidden" name="_subject" value="New China Hospitals Guide newsletter subscriber">
    <input type="hidden" name="_next" value="https://chinahospitalsguide.com/?subscribed=1">
    <input type="text" name="_gotcha" style="display:none">
    <button type="submit" style="...">Subscribe Free →</button>
</form>
```

The hidden fields do three jobs:
- `_subject` — gives the email a useful subject line (Formspree default is empty)
- `_next` — redirects user to homepage with `?subscribed=1` flag (GA4 will observe this in URL)
- `_gotcha` — honeypot anti-spam (empty text input that real users never fill but bots do)

**Deploy script** at `templates/formspree-deploy.sh`: takes the Formspree ID as argument, does global replace across 2 files, commits, pushes, waits 60s, verifies prod. Pattern + script in `templates/formspree-deploy.sh`.

## GSC-driven long-tail content matrix (NEW 2026-07-02)

**The pattern**: `gsc opportunities` is not just for CTR optimization on existing pages — it also reveals **city × procedure / condition × city** query patterns that the site has *impressions for but no dedicated page*. The 0% CTR is because Google sends users to a generic ranking page, where they bounce.

**How to identify long-tail opportunities from GSC**:
```bash
gsc opportunities
# Filter for: position 5-15 + impressions 10+ + CTR < 3%
# Look for query patterns that combine:
#   - procedure name (liposuction, myopia surgery, knee replacement, IVF, bronchitis)
#   - city name (Beijing, Shanghai, Guangzhou, Chengdu, Fuzhou, Jinan)
```

**Verified opportunities found 2026-07-02**:
| Query pattern | Impressions | Bounce page | Should-create page |
|---|---|---|---|
| `liposuction in Beijing` | 44 | `plastic-surgery-china-guide-2026.html` | `liposuction-beijing.html` |
| `myopia surgery in Shanghai` | 19 | `lasik-eye-surgery-china-2026.html` | `myopia-surgery-shanghai.html` |
| `bronchitis hospital in Jinan` | 13 | `china-hospital-rankings-2026.html` | `bronchitis-hospitals-jinan.html` |
| `ranking of orthopedic hospitals in Fuzhou` | 41 | `fuzhou-orthopedic-hospital-ranking.html` | (already exists — title/desc tune instead) |

**Long-tail page template** (city × procedure):
1. **H1**: "`<Procedure> in <City>: Top Hospitals, Costs & How to Book (2026)`"
2. **Hero metrics card** (3 cards): typical cost range, wait time, top hospital rank
3. **Top 3-5 hospitals** in that city for that procedure (table format with city + cost + key fact)
4. **"Why this city for this procedure"** (1 paragraph — what makes the city specialized)
5. **Cost breakdown** (US comparison + China breakdown, 1 table)
6. **Quick Decision** (3-4 cards, scaled down from 8 — for "How urgent is your case?")
7. **Quick Answers** (5 Q&A in `X is Y` Featured Snippet format)
8. **Cross-link to the national ranking page** AND the national procedure page

**Schema**: Article + BreadcrumbList + MedicalWebPage (same as ranking pages).

**Rule of thumb**: when `gsc opportunities` shows 10+ impressions for a city×procedure query, build the dedicated page. After 3-7 days, re-run `gsc opportunities` and check if the new page is ranking + the bounce page's CTR improved.

## Full-site schema coverage batch (NEW 2026-07-02 — RECIPE)

**When to run**: schema coverage audit shows <90% on content pages. Mechanical batch job, ~10 minutes for 150 files.

**Recipe** (verified on 152 files this session — blog 105/105 + news 83/83 went from 64%/16% → 100%):

```python
import os, re

base = "/path/to/site"
SKIP = ["blog-export", "blog-articles", "stories", "course", "templates",
        "report-carlos", ".git", "node_modules", "docs"]

# Phase 1: inventory
targets = []
for root, dirs, files in os.walk(base):
    if any(s in root for s in SKIP): continue
    for f in files:
        if not f.endswith(".html"): continue
        full = os.path.join(root, f)
        if any(s in full for s in SKIP): continue
        with open(full) as f: text = f.read()
        schemas = re.findall(r'<script type="application/ld\+json">([\s\S]*?)</script>', text)
        all_types = []
        for s in schemas: all_types += re.findall(r'"@type"\s*:\s*"([^"]+)"', s)
        if "Article" in all_types and "BreadcrumbList" in all_types: continue
        title_m = re.search(r'<title>([^<]+)</title>', text)
        title = re.sub(r'\s*[\|·–-]\s*China Hospitals Guide.*$', '', title_m.group(1) if title_m else f)
        targets.append({"path": full, "title": title[:100]})

# Phase 2: inject Article + BreadcrumbList (idempotent, safe — see schema injection safety pitfall)
for t in targets:
    with open(t["path"]) as f: text = f.read()
    # build Article block from t["title"], BreadcrumbList block from path
    # insert both before </head>
    with open(t["path"], "w") as f: f.write(text)

print(f"Done: {len(targets)} files")
```

**Skip rules** (don't waste time on these):
- `blog-export/` + `blog-articles/` (mirror/backup of main blog/)
- `report-carlos-mendoza-*` (programmatic report templates — generated per patient, one per timestamp)
- `404.html`, `panel.html`, `api/`, `course/`, `patient-story-program.html` (utility pages, no SEO value)
- `stories/`, `templates/` directories (backup/template stores)
- Anything inside `docs/` (documentation, not public marketing)

**Verification**: re-run inventory, expect 100% Article + 100% BreadcrumbList on all non-skipped content pages. Then spot-check prod with `curl` after deploy — `grep -c "BreadcrumbList" file.html` should return ≥1 (the schema itself).

**Why this matters**: schema coverage going from 64% to 100% is the highest-leverage mechanical SEO win available. ~10 minutes of Python work for ~188 pages × future Google rich-snippet eligibility.

## Subagent orchestration patterns (verified 2026-07-01)

Bulk content generation needs subagents. Six hard-won lessons:

1. **`max_concurrent_children=3` is a hard cap per user.** Batches of 4+ tasks fail with a clear error. Split into sequential 3-task batches; expect 2-3 `delegate_task` calls for a 10-file job.
2. **600s subagent timeout.** If a sub-pillar batch timeouts partway through (e.g., 1 of 4 timed out), don't re-submit the same batch. Spawn a focused follow-up child for ONLY the missing items.
3. **Subagent template drift.** Even with explicit prompts, subagents may produce files that miss a schema, drop a closing tag, or use a slightly different slug. Always validate output schema and link targets after a batch.
4. **Cross-link correctness within a batch.** When subagents produce cross-links, verify they actually point to the other files in the same batch (not just generic placeholders).
5. **Explicit slug names in prompts.** Vague phrases like "create a TCM page" can produce 3 different slugs. State exact filenames in the prompt.
6. **CDN cache propagation.** First curl after a Cloudflare redeploy can return stale content from a different edge. Wait 30-60s and re-poll before any rollback decision.

Full details, recipes, and worked examples in `references/delegate-task-gotchas.md`.

## Duplicate-content defense (verified pitfall, 2026-07-01)

A new agent/cron/operator process generating content that overlaps with existing content can produce slug-near-duplicates that Google will penalize. The defense:

1. **Before creating a new article, grep the existing library for the target slug**:
   ```bash
   grep -lE "TARGET_KEYWORDS" /path/to/blog/*.html
   ```
   If 2+ existing URLs match the target topic with similar slug, **DO NOT create a third** — find the canonical (most-linked, oldest, or highest-quality) and update it instead.
2. **Inspect the git log for very recent same-topic commits**:
   ```bash
   git log --oneline --all -- "blog/*topic*"
   git log --since="YYYY-MM-DD" --oneline
   ```
   If a `<topic>-guide.html` was created earlier in the day/week by another agent and a `<topic>.html` is now being proposed, pick the older one and delete the duplicate.
3. **When a duplicate is discovered post-hoc** (you created it, but an older one exists):
   - **Delete the newer file** (the older one was already live, had more links, was already in sitemap).
   - **Add a 301 redirect** in `_redirects` from the deleted slug to the kept slug.
   - **Verify no other pages link to the deleted slug** before deletion:
     ```bash
     grep -rE "deleted-slug" /path/to/site --include="*.html" -l
     ```
   - **Verify no sitemap entry exists for the deleted slug** (delete from sitemap.xml too).
   - **Push in a single commit with explanatory message** ("Removed duplicate page [slug] to avoid duplicate-content penalty, kept [canonical-slug] which was linked from Y/Z places.").

### Default canonical policy

Each distinct topic should have **exactly one** canonical URL. If two slugs both serve the same content (e.g. `-guide.html` and bare `.html`), the older one wins by default; the newer one is deleted and 301'd. Sub-topic pages (e.g. `autonomous-robotic-surgery-china.html`) are NOT duplicates of the master pillar (e.g. `china-unique-medical-procedures-guide.html`) — they are sub-pages and should not be deleted.

## Static-site deployment to GitHub Pages via Eleventy (verified pattern)

The chinahospitalsguide repo has these deployment quirks:

- **Local proxy required:** port 10808 (HTTP proxy)
- **Git SSL backend:** `openssl` (schannel fails in this sandbox environment)
- **Push pattern:** `git -c http.sslBackend=openssl push`
- **Pull pattern:** `git -c http.sslBackend=openssl pull --rebase` (when remote has advanced since the cron started)
- **⚠️ Deploy timing pitfall — NOT 60 seconds (VERIFIED 2026-07-02)**: GitHub Actions build takes ~2-3 min, then GitHub Pages CDN edge propagation takes another **3-10 minutes**. Total time from `git push` to `curl` seeing new content: **5-13 minutes**. I lost 7 minutes this session waiting 60 seconds, then again waiting 3 minutes, before the page actually updated. **Right pattern**:
  ```bash
  git push origin master
  # Now WAIT. Do not poll until at least 4 minutes have passed.
  sleep 240
  # First poll
  curl --max-time 25 -s -o /dev/null -w "%{http_code}\n" URL
  # If still old, wait more
  sleep 180
  curl --max-time 25 -s -o /dev/null -w "%{http_code}\n" URL
  ```
  The 60-second foreground timeout on the `sleep` portion of a `sleep && curl` chain is a recurring trap — **always split into two calls** and use `--max-time 25` on curl from the start. The terminal tool's 180s foreground timeout is real.
- **Verify pattern after push:** wait for GitHub Actions build to complete (~2-3 min, NOT 60s — that's Cloudflare timing). Check `https://api.github.com/repos/qzw-alt/chinahospitalsguide/deployments` for the latest deployment timestamp. Then `curl --max-time 25 -s -o /dev/null -w "%{http_code}\n" URL`.
- **CDN cache verification protocol:** GitHub Pages uses a CDN (Fastly/Varnish) — first curl after a redeploy can return stale content. Wait 30-60s and re-poll before any rollback decision. Telltale sign of GitHub Pages (not Cloudflare): `server: GitHub.com` in response headers.

### ⚠️ Memory pollution trap — verify with git, not with memory (NEW 2026-07-02)

This session I told the user "Cloudflare takes 60s to deploy" — **wrong**. The site is on **GitHub Pages**, deploy is **3-10 minutes**, and the user caught this when they said *"你才意识到你可能记忆出问题 因为确实我们之前网站也转移过 我怕你是用Cloudflare 的旧网站源码在改 那就太浪费时间了"*.

**The fix**: for ANY deployment/hosting fact (platform, deploy time, cache TTL, edge nodes, build steps), **verify with current `git log` and current `curl -I` response headers**, never with memory. Memory ages; infrastructure changes (the user moved off Cloudflare between sessions; my memory still had Cloudflare from a previous stack).

**Pre-deploy verification protocol (5 seconds)**:
```bash
# 1. Confirm the deploy target is still right
git remote -v                              # should show chinahospitalsguide
curl -I https://chinahospitalsguide.com/ | grep -i "server:"   # should be GitHub.com
curl -s https://api.github.com/repos/qzw-alt/chinahospitalsguide  # confirm repo still exists

# 2. Confirm the build flow (look at .github/workflows/)
ls /home/ubuntu/.hermes/workspace/website/.github/workflows/    # should have deploy.yml

# 3. Confirm Eleventy passthrough includes any new assets
grep "addPassthroughCopy" /home/ubuntu/.hermes/workspace/website/eleventy.config.js
```

If any of those answers contradict what you remember, **trust the live check**, not the memory.

### ⚠️ Eleventy passthrough-copy pitfall (NEW 2026-07-02 — VERIFIED MISTAKE)

**The trap:** Eleventy only copies files you explicitly list in `eleventy.config.js` via `addPassthroughCopy()`. Any new file you add to the repo root (CSS, JS, images, fonts, downloads) WILL be in git but WILL NOT be in the deployed `_site/` until you add it to passthrough.

**Symptom** (verified on `ga4-events.js` 2026-07-02): HTML pages reference the new file and serve correctly, but the file itself returns 404. Hours of debugging time wasted because "git has it, push succeeded, why 404?" — the answer is always Eleventy didn't copy it.

**The fix** — add to `eleventy.config.js` BEFORE the function returns:

```js
eleventyConfig.addPassthroughCopy("your-new-file.ext");
```

Existing passthrough list (as of 2026-07-02): `styles.css`, `ga4-events.js`, `images/`, `CNAME`, `.nojekyll`, `robots.txt`, `sitemap.xml`. Plus globs `news/`, `blog/`, `stories/`, `treatments/`, `*.html` (root).

**Pre-deploy check** — before pushing any new static asset:
1. Open `eleventy.config.js`, search for `addPassthroughCopy`
2. If your new file isn't listed, add it
3. Commit both the asset AND the config change in the SAME commit (separate commits work too but invite confusion)
4. Verify after GitHub Actions build: `curl -sI https://chinahospitalsguide.com/<your-file> | head -3` — `server: GitHub.com` + `HTTP/2 200` = good

### Cron iteration cap failure modes (5 documented)

When `git status` shows a non-clean state after a cron ends mid-pipeline, the recovery depends on where in the pipeline the cron died:

| # | Failure mode | Detection signal | Recovery recipe |
|---|---|---|---|
| 1 | During research | `git status` clean, no article on disk, `references/pending-YYYY-MM-DD-*.md` exists | Read pending file, fetch source via alternative recipes documented inside, ship |
| 2 | During writing | No article on disk, pending file exists | Same as #1 |
| 3 | Mid-pipeline (article on disk, sitemap updated, not committed) | `git status` shows untracked article file, modified sitemap.xml | Add news/index.html card, commit, push, sleep 180, curl 200 |
| 4 | Post-commit (article committed locally but not pushed) | `git status` says "Your branch is ahead of 'origin/master' by N commits" | Push, sleep, verify |
| 5 | Remote has advanced (cron commit would be non-fast-forward) | `git push` rejected with "fetch first" / "non-fast-forward" | `git -c http.sslBackend=openssl pull --rebase`, then push |

For the chinahospitalsguide specifically, the cron-related iteration cap has hit modes 1-5 across 2026-06-XX runs. See `content-research-writer-cn/references/pending-*.md` for the canonical examples and the detailed recovery recipes.

### Local git config (new-site spin-up)

If a fresh repo environment lacks git config, fix it inline:
```bash
git config user.email "hermes@<site>.com"
git config user.name "Hermes Agent"
```
This was needed once each on oriental-destiny and chinahospitalsguide (verified 2026-06-22).

## Bulk HTML editing with execute_code (verified pattern)

When the `patch` tool fails on a static HTML file (whitespace mismatch, multiple matches, or the file is too large to safely re-read), use Python regex from `execute_code` for surgical insertions. The canonical recipe:

```python
import re

def insert_block(fp, anchor_regex, new_block, description):
    if not os.path.exists(fp):
        return False
    with open(fp) as f:
        c = f.read()
    if new_block[:80] in c:  # de-dupe
        return True
    m = re.search(anchor_regex, c)
    if not m:
        return False
    new_c = c[:m.start()] + new_block + '\n\n    ' + c[m.start():]
    with open(fp, 'w') as f:
        f.write(new_c)
    return True
```

Full pattern library, common bugs (whitespace variants, multi-match, insertion order), and verification protocol in `references/execute-code-bulk-edit-patterns.md`.

### ⚠️ Python f-string `{var}` parsing trap (NEW 2026-07-02 — VERIFIED MISTAKE)

When building a multi-line HTML template with an f-string and inserting it inside a Python f-string definition (double-f-string nesting), Python interprets `{var}` in the *inner* f-string at definition time, not at format time.

**The verified failure**: I wrote a giant template using `f"""...{stay_days}..."""` then **inside that f-string** referenced `stay_days` again as `{stay_days}`. Python saw `{stay_days}` in the inner template, couldn't find `stay_days` in scope at template-construction time, and threw `NameError: name 'stay_days' is not defined`.

**Fix**: when the inner template uses `{var}` and you want it substituted at format time, **don't** make the outer template an f-string. Use a plain string with `.format(**kwargs)` instead:

```python
# ❌ WRONG — double f-string, inner braces get evaluated at definition time
template = f"""...{stay_days}...{stay}..."""  # NameError if `stay` not in scope

# ✅ RIGHT — plain string, format() called once at use time
template = """...{stay_days}...{stay}..."""
html = template.format(stay_days=stay_days, stay=stay, ...)
```

Or use `Template.safe_substitute()` from `string` if you have CSS braces (which look like Python format syntax) in the same template.

**Other f-string pitfalls**:
- Backslashes inside f-string expressions are forbidden before Python 3.12 — `f"{'\\n'}"` is a SyntaxError. Use a variable: `nl = '\\n'; f"prefix{nl}suffix"`.
- Quote escaping: `f"{dict["key"]}"` fails because the inner `"` ends the f-string. Use `f'{dict["key"]}'` or pull the value into a variable first.

### ⚠️ GSC ROI threshold for content investment (NEW 2026-07-02)

When building new content pages (long-tail decision guides, city pages, FAQ content, etc.) from `gsc opportunities`, **filter the queue by impression volume**:

- **< 100 impressions/mo per target query**: skip. Not enough demand to justify the page; even 100% CTR = < 100 clicks/mo. The opportunity cost of one CMS slot is higher than the gain.
- **100-500 impressions/mo**: build the page if it fills a real category gap AND the bounce page's CTR is < 1%. Expected gain: maybe 20-50 clicks/mo.
- **500-2000 impressions/mo**: high priority. Build a properly templated page. Expected gain: 50-200 clicks/mo.
- **2000+ impressions/mo**: must-build. Optimize the existing page first (Quick Decision + Quick Answers + schema) — building a new page splits ranking signals and may hurt the existing one.

**The verified failure**: 2026-07-02 I built 5 "decision guide" pages (liposuction Beijing, LASIK Shanghai, etc.) targeting GSC queries with **total impressions under 100/mo across all 5**. User reverted within 20 minutes.

**Pre-build checklist**:
```bash
gsc opportunities | head -30
# Filter: position 5-15 + impressions >= 100 + CTR < 3%
# If a candidate doesn't pass, drop it from the batch
```

**Optimize-don't-create rule**: when a query already has a ranking page (the bounce page) with impressions, the higher-ROI move is to **optimize the bounce page** (add Quick Decision cards specific to that query, add FAQ schema with the exact query phrasing). Don't fragment by creating parallel pages.

## `patch` tool `replace_all` pitfall (NEW 2026-07-01)

When batching meta-tag edits across `<title>`, `og:title`, `twitter:title` (or any 3+ tags that share a substring), do **NOT** use `patch mode="replace" replace_all=true` if your `new_string` is just the changed portion of a tag.

**The bug:** `patch` does literal string matching. If your old_string is `<title>Old Page Title</title>` and your new_string is `<title>New Page Title</title>`, the tool will match every line that contains `<title>Old Page Title</title>` — including `<meta property="og:title" content="...Old Page Title...">` if the old title happens to appear in the og:title content. The replacement then strips the `<meta property="og:title"` wrapper and leaves a bare `<title>New Page Title</title>`. Page ends up with 4 `<title>` tags, 0 `og:title` tags.

**Safe pattern** for multi-tag meta edits:

```python
# Use execute_code with literal string replace (verified working):
from pathlib import Path
f = Path("/path/to/file.html")
content = f.read_text(encoding="utf-8")
content = content.replace("old full meta tag line", "new full meta tag line")
f.write_text(content, encoding="utf-8")

# Then verify: grep -c "<title>" file.html should return 1
# Same for og:title and twitter:title
```

**Always verify after meta-tag batch edits:**
```bash
grep -c "<title>" file.html                   # should be 1
grep -c 'property="og:title"' file.html        # should be 1
grep -c 'name="twitter:title"' file.html      # should be 1
```
If counts are wrong, `git checkout file.html` and re-do with the safe pattern.

## Schema injection safety pitfall (NEW 2026-07-02 — VERIFIED MISTAKE)

When adding JSON-LD schemas (Article, FAQPage, BreadcrumbList, MedicalWebPage, etc.) to existing pages, **never** use a greedy regex to "remove duplicates" of schemas you just added. You will accidentally delete the originals too.

**The bug (verified on `best-cancer-hospitals-china-2026.html` 2026-07-02):**
The page already had 3 schemas (Article, BreadcrumbList, FAQPage). I needed to add MedicalWebPage. After adding, I noticed 2 BreadcrumbList schemas (mine + original), so I tried to remove mine using:

```python
# ❌ WRONG — this regex matches too greedily
text = re.sub(r'<script type="application/ld\+json">[\s\S]*?</script>', '', text)
```

**Result**: deleted ALL schemas (mine + the 3 originals). File went from 4 schemas → 1 (only one survived by chance). Required recovery from git HEAD.

**Safe pattern — `inject_schemas_safe()`:**

```python
import re

def get_existing_schema_types(text):
    """Return list of main @type for each JSON-LD block in text."""
    schemas = re.findall(r'<script type="application/ld\+json">([\s\S]*?)</script>', text)
    out = []
    for s in schemas:
        types = re.findall(r'"@type"\s*:\s*"([^"]+)"', s)
        if types:
            out.append(types[0])
    return out

def inject_schemas_safe(text, new_medicalwebpage_block, new_breadcrumb_block):
    """Add MedicalWebPage + BreadcrumbList ONLY if not already present.
    Never modify or delete existing schemas. Safe to call on already-edited files (idempotent)."""
    existing = get_existing_schema_types(text)
    new_blocks = []
    if "MedicalWebPage" not in existing:
        new_blocks.append(new_medicalwebpage_block)
    if "BreadcrumbList" not in existing:
        new_blocks.append(new_breadcrumb_block)
    if not new_blocks:
        return text  # nothing to add
    head_end = text.find("</head>")
    return text[:head_end] + "\n" + "\n".join(new_blocks) + "\n" + text[head_end:]
```

**Pre-flight audit before any schema edit:**

```bash
# Always confirm current schema inventory BEFORE any edit
python3 -c "
import re
with open('/path/to/file.html') as f: text = f.read()
schemas = re.findall(r'<script type=\"application/ld\\+json\">([\\s\\S]*?)</script>', text)
for s in schemas:
    types = re.findall(r'\"@type\"\\s*:\\s*\"([^\"]+)\"', s)
    print(types[:3])
"
```

If you accidentally delete a schema, recover with:

```bash
git show HEAD:blog/<file>.html > blog/<file>.html
# Then re-apply your changes carefully
```

**General rule for ANY bulk HTML edit on schema/head region:** read the original with `git show HEAD:` first, identify the exact blocks you want to preserve, then ONLY insert new blocks at safe anchors (right before `</head>` or right after `</header>`). Never re.sub() existing schema blocks unless you've diffed first.

## Support files

- `references/duplicate-content-defense.md` — canonical worked example of detecting two same-topic pillar pages, deciding which to keep, and recovering cleanly (delete + 301 + sitemap edit + verify). Includes a 5-command detection script and a 1-command audit script for future site scans.
- `references/conversion-optimization.md` — three conversion blocks (homepage trust section with stat cards + media references, Newsletter sign-up form with Formspree placeholder endpoint pattern, blog-index "Featured: What Only China Can Do" pillar block + "Browse by What Makes China Different" 3-category block). Includes copy-paste HTML for each block and a Cloudflare CDN cache verification protocol (curl may be stale on first poll — wait 30+s and re-check before any rollback).
- `references/delegate-task-gotchas.md` — six subagent failure modes: hardcoded `max_concurrent_children=3` (split batches), 600s subagent timeout (rescue missing items via focused child, don't re-submit same batch), subagent HTML template drift (always validate output schema), internal cross-link correctness, "be explicit about slugs in the prompt" rule, and CDN cache propagation delay.
- `references/execute-code-bulk-edit-patterns.md` — when `patch` tool fails on whitespace or multi-match markers, use `re.search` + capture groups + `c[:m.start()] + m.group(1) + new_block + m.group(2) + m.group(3) + c[m.end():]`. Covers common bugs (whitespace variants, multiple matches, insertion-order matters), the canonical idempotent insert_block() recipe, and verification protocol.
- `references/batch-schema-coverage.md` — full audit + inject scripts (inventory + idempotent inject), skip-rules for backup/export directories, post-deploy verification protocol, title-escaping caveat.
- `references/gsc-oauth-setup.md` — verified working 5-step recipe for OAuth auth of Google Search Console from a remote Hermes container, with the 5 gotchas (API key alone doesn't work, test-user not added, unverified-app warning, Search Console API not enabled, PKCE Missing-code-verifier when flow is split across invocations) and the file layout / token-lifecycle rules. **Updated 2026-07-01 with verified working cron pattern (job_id `16a08d0ea83d`, Monday 07:00 CST, no_agent) and `patch` tool `replace_all` pitfall.**
- `references/session-2026-07-02-lessons.md` — **NEW 2026-07-02** — transcript + reasoning from a session where the agent made 7 systemic mistakes in a row (identity flip, Cloudflare memory contamination, fabricated plan, GSC data noise mistaken for demand, fictional patient stories treated as real, 43-file scope miss on schema coverage, decision-tree executed wrong, schema regex deletion ate originals, f-string parsing trap). Includes the user's correction cadence and the 10 takeaways that are also encoded in the parent SKILL.md.
- `templates/hospital-ranking-feature-snippet.md` — copy-paste template for the "Quick Decision" decision-tree block + "Quick Answers" Featured Snippet block + the 2 added JSON-LD schemas (MedicalWebPage + BreadcrumbList). **Verified 2026-07-02** with 4 worked specialty variants (cancer / orthopedic / cardiac / Fudan Top 100) showing all 8 card emoji+condition+color+content+deep-link per variant. Includes `inject_schemas_safe()` recipe (prevent the schema-deletion pitfall) and full insertion + verification + deployment protocol.
- `templates/ga4-event-tracking.md` — drop-in GA4 event tracking JS (scroll_depth + cta_click + outbound_click), bulk-deploy recipe for `index.html` + `blog/index.html` + selective blog slugs, post-7-day reading guide, and the MS Clarity ship-now-wire-later placeholder pattern.
- `templates/formspree-deploy.sh` — one-arg shell script (`./formspree-deploy.sh xyzabcde`) that does global replace across 2 newsletter forms, commits, pushes, waits 60s for Cloudflare deploy, verifies prod. The user just runs this with the Formspree ID they got from the dashboard.
- `templates/gsc-authorize.py` — copy-and-run OAuth authorization script for GSC. Handles the three remote-container quirks: `http://localhost` redirect (no local server), PKCE code_verifier file persistence between `authorization_url()` and `fetch_token()`, and `sys.stdin.isatty()` early-exit so heredoc invocations don't crash on `EOFError`.
- `templates/gsc-command-wrapper.py` — copy-and-run `gsc` CLI wrapper. Subcommands: `summary`, `top queries`, `top pages`, `opportunities`, `trends`, `compare`. Used by `gsc-weekly-report.sh` cron.
- `templates/gsc-weekly-report.sh` — copy-and-run weekly report generator. Pipe stdout directly to Feishu. No LLM involvement.

## User / task profile

- **User:** 伟烨 (Hermes is the agent, not the user — do NOT flip identity. The user is 伟烨, the AI assistant is Hermes/德米), Asia/Shanghai GMT+8, 极简指令型 ("行按这个执行" = complete authorization, no confirmation needed).
- **⚠️ Identity correction (VERIFIED 2026-07-02)**: the user explicitly corrected me when I started signing reports as "德米" and addressing them as "德米". Correct: 伟烨 = user (human), 德米 / Hermes = me (AI assistant). Get this right at session start. Memory got contaminated across sessions; always re-read the user profile before addressing them.
- **Working style:** "无回复≠取消", partial completion → 记录剩余 + 提醒, "完成/取消" 才停.
- **Quality bar:** 宁缺毋滥. When in doubt, skip. Numbers and dates must be sourced. Hospital names and doctor names must match the reference doc.
- **Communication:** Chinese by default. Be brief. Be specific. Skip filler.
- **Execution authority** (verified 2026-07-02): when the user says "你按你的理解去做" / "按这个执行" / "行" with a multi-item list, it means **complete all items in scope, in ROI order, without re-asking for prioritization**. Pick the order myself, report results, don't ask which to start with. This is a stronger signal than "no confirmation needed" — it's "you own the queue".
- **⚠️ But execution authority does NOT mean "skip questioning" (VERIFIED 2026-07-02)**: push back when warranted. State the data basis for prioritization. Surface disagreements before 6-hour rollouts. The user prefers "we are partners, question each other" over "execute silently and apologize later".
- **⚠️ Current business state (VERIFIED 2026-07-02)**: **the user has 0 real customers / 0 closed deals / fictional patient stories**. The site is pre-revenue. This means:
  - Do NOT build trust signals that depend on social proof (patient story count, review count, X-patients-served claim).
  - Do NOT build "patient story expansion" as a content category — the existing 3 stories are placeholders.
  - Optimizing top-impression pages (plastic-surgery-china-guide-2026.html = 967 imp/mo) for **first-touch conversion** (newsletter signup, contact form, free consultation request) is the right path. Once real customers exist, social-proof and patient-story layers can be added on top.
  - The "transformation pipeline" is currently: visitor → ???. The ??? is where the user is figuring it out. Don't assume it's a single sales page or a single conversion endpoint — ask before adding new CTA destinations.

## Trust signal and conversion block — adjust for pre-revenue sites

The conversion blocks in this skill assume a site that has SOME social proof. For a pre-revenue site (as of 2026-07-02):

1. **Skip the "as featured in" media references block** if no actual press mentions exist. Use it only when the user provides actual URLs.
2. **Skip the patient story count** in stat cards. Use neutrals like "Independent guidance" / "Free hospital matching" / "50-80% cost savings verified" — verifiable claims without social proof.
3. **Trust section "coverage"**: instead of logos, use "Based on Fudan Hospital Rankings 2024" + "Verified by Chinese Society of Plastic Surgery" + similar authoritative-but-no-logo references. The site already follows this pattern.
4. **Patient stories**: 3 fictional placeholder stories is OK as a "what your journey looks like" template, but **do not grow this section** until real stories exist. The user will tell you when they have real ones.
5. **Free consultation CTA**: this is the right primary CTA for pre-revenue. "Get free case review" / "Free hospital matching" is the offer; the conversion is email + brief description.

When the user transitions to "have real customers" state, re-evaluate: replace placeholders, add real review widgets, build out the patient-stories archive properly. Until then, keep social-proof scaffolding minimal and truthful.

## Output checklist for any site change

Every change to chinahospitalsguide.com (or similar) should produce:

1. ✅ A clean git commit with a descriptive message naming the slug(s) affected.
2. ✅ A successful `git push origin master` (with --rebase if needed).
3. ✅ An HTTP 200 verify on the affected URL(s) after **at least 4 minutes** (GitHub Actions build + CDN edge propagation), plus at least one positive grep for the new content (see CDN cache verification protocol). **Do NOT poll inside 60 seconds** — that's Cloudflare timing, not GitHub Pages.
4. ✅ A sitemap.xml update if new pages were created.
5. ✅ A `_redirects` update if pages were deleted or renamed.
6. ✅ A short final report to the user naming the commit hash and the live URL(s).
7. ⚠️ **End-to-end verification before declaring success** — if the change claims "X% coverage" or "all pages updated", audit ALL relevant subdirectories (blog/, news/, treatments/, root, docs/) and at least one GitHub-side `curl` of the live URL. Memory-contaminated "I deployed it" reports without verification = waste of user time.

## When the user pushes back — what to do

The user has shown a clear pattern this session: correction is **terse, firm, and specific**. They will not soften the correction ("温柔点"). The expected response pattern when corrected:

1. **Acknowledge what was wrong** in 1 sentence. Not "I'm sorry" — that's passive. Say "you're right, [fact] was [wrong], here's the fix".
2. **Fix the immediate issue**. Don't dump a 5-step plan — just do it.
3. **Update memory/skill if the mistake is structural** (this is what we just did in the parent skill).
4. **Move on to the next thing the user asked for** — don't dwell.

What NOT to do:
- Don't apologize three times.
- Don't re-explain what you did and why it was right (it wasn't).
- Don't ask "is that better now?" after the fix — just do the next thing.
- Don't add "in the future I will..." — that's noise. Encode it in skill/memory and act on it next time.

## The "pre-revenue site" calibration

Verified as of 2026-07-02: this site has 0 real customers, 0 closed deals, fictional patient stories. The user is honest about this. Operating assumptions:

- **Trust signal ceiling**: do not build "X patients served" / "Y reviews" / "Z years in business" claims without real data. Use neutrals: "Independent guidance", "Free hospital matching", "Based on Fudan Hospital Rankings 2024".
- **Patient stories are templates**: existing 3 stories are placeholders. Do NOT grow this section until real stories exist.
- **Conversion path is hypothesis**: the user is figuring out how visitor → customer actually works. Don't assume it's a single CTA page or a single email capture. Ask before adding new CTA destinations.
- **First-touch conversion matters more than social proof**: optimize top-impression pages (e.g. `plastic-surgery-china-guide-2026.html` at 967 imp/mo) for **first-touch CTA** (free consultation, contact form, newsletter) before any patient-story work.

When the user transitions to "I have real customers now", re-evaluate all of the above and rebuild the social-proof scaffolding properly.
