---
name: medical-tourism-site-ops
description: "Operations workflow for English-language medical tourism websites covering China (chinahospitalsguide archetype) — content matrix strategy, SEO technical patterns, duplicate-content defense, static site deployment to Cloudflare via GitHub, conversion blocks (trust + newsletter + featured-pillar), and how the user wants this class of work run (iterative, single-step verified, no grand roadmaps)."
version: 0.3.0
author: Hermes Agent
platforms: [linux]
metadata:
  hermes:
    tags: [medical-tourism, seo, content-ops, chinahospitalsguide, static-site, cloudflare, conversion, gsc]
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

## Site archetype: chinahospitalsguide.com stack (verified 2026-07-01)

- **Stack:** static HTML, no server-side rendering. Generated pre-build with Nunjucks templates.
- **Deploy:** Cloudflare Pages / Netlify (uses `_redirects` file at repo root).
- **Repo:** `https://github.com/qzw-alt/chinahospitalsguide`
- **Content layout:**
  - `index.html` — homepage (full HTML rewrite risk = high; surgical `<section>` inserts only)
  - `blog/<slug>.html` — evergreen guides (107 articles in mid-2026, target ~300-500 over 2 years)
  - `blog/index.html` — blog landing page (filter buttons, popular topics section, "latest articles" grid)
  - `news/<slug>.html` — daily news articles (1/day cadence, demoted to 2-3 days/week as content depth grows)
  - `treatments/`, `hospitals/`, `stories/`, etc. — supporting content
  - `sitemap.xml` — single file, hand-maintained `lastmod` dates
  - `_redirects` — 301 redirects for legacy phantom URLs and duplicates
- **Analytics:** GA4 (`G-RVYZENK472`), AdSense (`ca-pub-2521119288266043`)
- **CDN-cache gotcha:** external stylesheets via CDN cache hard; CSS must be **inline `<style>` blocks** per-page, not external. This is documented in the project memory and is critical when matching the existing blog template style. Same rule for ALL conversion blocks — Trust section, Newsletter form, Featured Pillar, Decision Tree, Quick Answers — all inline.

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

## Static-site deployment to Cloudflare via GitHub (verified pattern)

The chinahospitalsguide repo has these deployment quirks (per AGENTS.md + memory):

- **Local proxy required:** port 10808 (HTTP proxy)
- **Git SSL backend:** `openssl` (schannel fails in this sandbox environment)
- **Push pattern:** `git -c http.sslBackend=openssl push`
- **Pull pattern:** `git -c http.sslBackend=openssl pull --rebase` (when remote has advanced since the cron started)
- **Verify pattern after push:** wait for Cloudflare Pages to redeploy (~60s typically), then `curl --max-time 25 -s -o /dev/null -w "%{http_code}\n" URL`. The 60-second foreground timeout on the `sleep` portion of a `sleep && curl` chain is a recurring trap — **always split into two calls** and use `--max-time 25` on curl from the start.
- **CDN cache verification protocol:** if first curl returns 200 but expected-text grep returns 0, **wait 30+ seconds and re-poll** before declaring failure. CDN edges propagate at different rates — first poll may be stale. See `references/conversion-optimization.md` for the full protocol.
- **CNAME file** controls the domain — do NOT edit.

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

## Support files

- `references/duplicate-content-defense.md` — canonical worked example of detecting two same-topic pillar pages, deciding which to keep, and recovering cleanly (delete + 301 + sitemap edit + verify). Includes a 5-command detection script and a 1-command audit script for future site scans.
- `references/conversion-optimization.md` — three conversion blocks (homepage trust section with stat cards + media references, Newsletter sign-up form with Formspree placeholder endpoint pattern, blog-index "Featured: What Only China Can Do" pillar block + "Browse by What Makes China Different" 3-category block). Includes copy-paste HTML for each block and a Cloudflare CDN cache verification protocol (curl may be stale on first poll — wait 30+s and re-check before any rollback).
- `references/delegate-task-gotchas.md` — six subagent failure modes: hardcoded `max_concurrent_children=3` (split batches), 600s subagent timeout (rescue missing items via focused child, don't re-submit same batch), subagent HTML template drift (always validate output schema), internal cross-link correctness, "be explicit about slugs in the prompt" rule, and CDN cache propagation delay.
- `references/execute-code-bulk-edit-patterns.md` — when `patch` tool fails on whitespace or multi-match markers, use `re.search` + capture groups + `c[:m.start()] + m.group(1) + new_block + m.group(2) + m.group(3) + c[m.end():]`. Covers common bugs (whitespace variants, multiple matches, insertion-order matters), the canonical idempotent insert_block() recipe, and verification protocol.
- `references/gsc-oauth-setup.md` — verified working 5-step recipe for OAuth auth of Google Search Console from a remote Hermes container, with the 5 gotchas (API key alone doesn't work, test-user not added, unverified-app warning, Search Console API not enabled, PKCE Missing-code-verifier when flow is split across invocations) and the file layout / token-lifecycle rules. **Updated 2026-07-01 with verified working cron pattern (job_id `16a08d0ea83d`, Monday 07:00 CST, no_agent) and `patch` tool `replace_all` pitfall.**
- `templates/hospital-ranking-feature-snippet.md` — copy-paste template for the "Quick Decision" decision-tree block + "Quick Answers" Featured Snippet block + the 2 added JSON-LD schemas (MedicalWebPage + BreadcrumbList), with a worked table of 8 specialties and an `execute_code`-based insertion recipe.
- `templates/gsc-authorize.py` — copy-and-run OAuth authorization script for GSC. Handles the three remote-container quirks: `http://localhost` redirect (no local server), PKCE code_verifier file persistence between `authorization_url()` and `fetch_token()`, and `sys.stdin.isatty()` early-exit so heredoc invocations don't crash on `EOFError`.
- `templates/gsc-command-wrapper.py` — copy-and-run `gsc` CLI wrapper. Subcommands: `summary`, `top queries`, `top pages`, `opportunities`, `trends`, `compare`. Used by `gsc-weekly-report.sh` cron.
- `templates/gsc-weekly-report.sh` — copy-and-run weekly report generator. Pipe stdout directly to Feishu. No LLM involvement.

## User / task profile

- **User:** 伟烨 (德米), Asia/Shanghai GMT+8, 极简指令型 ("行按这个执行" = complete authorization, no confirmation needed).
- **Working style:** "无回复≠取消", partial completion → 记录剩余 + 提醒, "完成/取消" 才停.
- **Quality bar:** 宁缺毋滥. When in doubt, skip. Numbers and dates must be sourced. Hospital names and doctor names must match the reference doc.
- **Communication:** Chinese by default. Be brief. Be specific. Skip filler.

## Output checklist for any site change

Every change to chinahospitalsguide.com (or similar) should produce:

1. ✅ A clean git commit with a descriptive message naming the slug(s) affected.
2. ✅ A successful `git push origin master` (with --rebase if needed).
3. ✅ An HTTP 200 verify on the affected URL(s) after ~60s, plus at least one positive grep for the new content (see CDN cache verification protocol).
4. ✅ A sitemap.xml update if new pages were created.
5. ✅ A `_redirects` update if pages were deleted or renamed.
6. ✅ A short final report to the user naming the commit hash and the live URL(s).
