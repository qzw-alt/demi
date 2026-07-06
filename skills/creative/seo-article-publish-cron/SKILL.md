---
name: seo-article-publish-cron
description: "Run a daily SEO article publishing cron job — verify repo state, match existing article template, write English article, de-AI pass, update sitemap, commit and push to the deployed branch. Use when a cron task says 'publish daily SEO article to <site>' with a GitHub Pages deployment from a repo."
version: "1.3.0"
author: Hermes Agent
license: MIT
platforms: [linux]
metadata:
  hermes:
    tags: [seo, publishing, cron, github-pages, articles]
    category: creative
    related_skills: [programmatic-seo, humanizer]
---

# SEO Article Publishing Cron Job

A repeatable workflow for daily article publishing to a static-site repo (GitHub Pages, Cloudflare Pages, Netlify, etc.) where the cron spec may or may not be accurate. Built from a real session running the oriental-destiny.com daily feng shui article cron.

## When to load this skill

Load whenever the user says:
- "daily SEO article cron job"
- "publish one article per day to <site>"
- "post a blog post to GitHub Pages every day"
- A scheduled job hands you a repo URL + branch + filename pattern + "publish" instruction

Also load when you inherit any cron job that combines: research → write → publish to a static repo.

## The iron rule: verify the cron spec before you trust it

Cron specs drift. Repos get renamed, branches get renamed, reference files get moved, deployed branch ≠ default branch. **Spend 2 minutes verifying before writing anything.** A wrong assumption baked into a 4,500-word article + git push is 30+ minutes of cleanup.

### Mandatory pre-flight checklist (run BEFORE writing)

```bash
cd <repo>
git status                                    # confirm clean working tree
git branch -a                                 # confirm deployed branch — NOT just "master" by default
git log --oneline -5                          # see recent commit cadence / format
git remote -v                                 # confirm remote URL matches spec
```

Then verify the spec's referenced resources:

- If the spec says "read X from memory/research/competitor-research.md" — `ls` the directory. The file may not exist.
- If the spec says "branch: master" — `git branch -a` may show `main`. Use whatever is actually deployed (GitHub Pages default is `main` since 2020 for new repos).
- If the spec names a skill that isn't installed — note it, fall back to a sibling skill (`programmatic-seo` covers most SEO workflow needs), and tell the user.

Common spec drift to expect:
- Branch name (`master` vs `main`) — **`oriental-destiny.com` actually runs on `main`, not the `master` the original spec says. Always run `git branch -a` and check `remotes/origin/HEAD -> origin/<branch>` to discover the real deployed branch before pushing.**
- Topic-source filename (often renamed or never existed — search `~/.hermes/memories/` recursively for the closest match; the oriental-destiny memory files are `article_topics.md` and `terminology_mapping.md`, not `competitor-research.md`)
- Skill names (spec author remembered wrong — fall back to sibling skills and tell the user)
- The deployed branch ≠ the spec's stated branch

## The article-template fingerprint (read before writing)

Every daily-article site has an established template fingerprint. Match it before you draft a single paragraph. Inconsistency breaks visual trust and signals "this article isn't from the same site."

```bash
# 1. Read yesterday's article in full
cat fate-YYYY-MM-DD-minus-1.html

# 2. Confirm the template style hasn't shifted recently (last 5-7 days)
for f in $(ls -t fate-*.html | head -7); do
  echo "=== $f ==="
  grep -oE '<title>[^<]+</title>' "$f" | head -1
done

# 3. Note the structural fingerprints
#    - CSS variables block (colors, fonts)
#    - Hero block pattern (.hero, .subtitle, h1, .lead, .meta)
#    - Content-block pattern (.content-block, h2 with border-bottom, h3, p, .pullquote)
#    - FAQ section (div.faq-item, div.faq-q, div.faq-a) — count Qs to match site norm
#    - CTA section (background gradient, button, link to /instant_reading.html or /products.html)
#    - Footer with date-stamped "Explore more" cross-links
#    - JSON-LD Article schema in <head>
```

Match these exactly. Use `templates/fate-article.html` as the boilerplate — it has the full CSS, JSON-LD, navigation, footer, and CTA already wired with `{{PLACEHOLDER}}` markers. Copy it to `fate-YYYY-MM-DD.html`, fill the placeholders, and edit body content. This is faster and more reliable than re-reading yesterday's <style> block on every run.

## Article-length calibration

```bash
# What word count does this site target?
for f in $(ls -t fate-*.html | head -7); do
  echo -n "$f: "; wc -w "$f" | awk '{print $1}'
done
```

For oriental-destiny.com the range was 3,200-4,550 words with a mean around 3,800. If your draft is 1,500 words or 6,000 words, you've drifted. Adjust before publishing.

## Writing the article

### Continuity over novelty

If the site publishes daily, the article you write today is part of a series. **Read yesterday's article before picking today's topic.** Build on it rather than starting a new thread. Good continuity patterns:

- Topic ladder: yesterday's "Bagua map overview" → today's "How to read the wealth cell of the bagua" (next logical cell)
- Same example worked through: yesterday used a south-facing home → today use a west-facing home to widen coverage
- Same metaphor expanded: yesterday introduced the "compass is the canvas, prescriptions are the paint" metaphor → today show two more "paint" techniques

The footer cross-link block in the template exists to make continuity obvious. Use it: link to the prior 3-5 articles.

### Topic selection from research notes

If the spec says "read competitor-research.md," first check what files actually exist in the memories/research/ directory:

```bash
ls ~/.hermes/memories/layer*/research/ 2>/dev/null
find ~ -name "competitor-research.md" 2>/dev/null
```

The actual files are usually named more specifically: `article_topics.md`, `terminology_mapping.md`, `keyword-research.md`. Read whatever exists.

For SEO topic selection, prefer:
- **Low-competition, high-volume** categories (specific life areas, common cures, regional variants)
- **Topics that ladder from existing articles** (continuity bonus)
- **Topics that hit a specific year's calendar** (2026 Flying Stars, 2026 Tai Sui, Fire Horse year) — these compound with seasonal search traffic

Avoid:
- Topics already published on this site (search the site for the topic before writing)
- Topics too narrow (single-day search traffic)
- Topics the site has already established a position on (don't contradict yesterday's stance)

### Primary keyword and headline template (HARD RULE)

Every article on this site has a **Primary Keyword** that MUST appear in `<title>`, `<h1>`, `og:title`, and `schema.org headline`. The template is:

```
[Primary Keyword]: [Long-tail Hook] | Oriental Destiny
```

Where:
- **Primary Keyword** = `X Feng Shui` | `X BaZi` | `X Destiny` form. The head term (`Feng Shui` / `BaZi` / `Destiny`) **must not be dropped**.
- **X** = a concrete topic object (Front Garden / Back Garden / Balcony / Rooftop / Li Qiu / Door / Bedroom / Kitchen / a specific solar term). NOT a pure temporal adverb like "Eve" or "Morning" without an anchor object.
- **Long-tail Hook** = a scene-setting long-tail phrase, e.g. "What to Do on the Eve Before the Fire-to-Earth Handoff".

**Examples (✅ / ❌):**
- ✅ `Front Garden Feng Shui for July: What to Do in the Fire-to-Earth Transition`
- ✅ `Li Qiu Feng Shui: What to Do on the Eve Before the Fire-to-Earth Handoff`
- ❌ `Li Qiu Eve: The Night Before the Fire-to-Earth Handoff` (head term `Feng Shui` dropped — the article was realigned on 2026-07-06 to fix exactly this)
- ❌ `July Outdoor Reading` (no head term, no concrete object)

The `<meta name="description">` MUST contain the Primary Keyword in the **first sentence** — don't make readers wait until sentence 3 to see what the article is about.

**Why this matters:** a daily SEO site earns topical authority by clustering. The oriental-destiny.com July thread was built on `Front Garden / Back Garden / Balcony / Rooftop / Outdoor + Feng Shui for July`. If one article in the thread drops the head term (`Feng Shui`), the cluster fractures and that one article ranks for a near-zero-volume phrase (`Li Qiu Eve` ≠ `Li Qiu Feng Shui`). The cron is responsible for this — topic research notes won't catch it.

**Self-check before publishing (run after drafting, before de-AI):**
1. `grep -oE '<title>[^<]+</title>' fate-YYYY-MM-DD.html` — does it match the template? If not, rewrite.
2. `grep -oE '<h1[^>]*>[^<]+</h1>' fate-YYYY-MM-DD.html` — does it match the `<title>` exactly (modulo the "| Oriental Destiny" suffix)?
3. `grep -oE 'og:title"[^>]*content="[^"]+"' fate-YYYY-MM-DD.html` — does it match?
4. `grep -A1 '"headline"' fate-YYYY-MM-DD.html` — does the schema.org headline match?

If any of the four mismatch the template, **fix and re-verify before running the de-AI gate**.

### Continuity over novelty

The cron spec usually says "de-AI score > 60 to publish." Treat it as a hard gate. Run the humanizer skill audit (the SKILL.md lists 29 patterns to scan).

Quick programmatic scan (catches most tells in seconds):

```bash
python3 references/../scripts/de-ai-scan.py fate-YYYY-MM-DD.html
```

Or the inline version (kept here for reference; the script above is the maintained version):

```python
from hermes_tools import read_file
import re
path = "fate-YYYY-MM-DD.html"
html = read_file(path, offset=1, limit=2000)['content']
text = re.sub(r'<[^>]+>', ' ', html).lower()

ai_words = ['delve', 'tapestry', 'testament', 'underscore', 'underscoring',
            'enduring', 'pivotal', 'intricate', 'fostering', 'garner',
            'showcase', 'showcases', 'showcasing', 'vibrant', 'nestled',
            'renowned', 'breathtaking', 'must-visit', 'stunning', 'groundbreaking',
            'beacon', 'enhance', 'enhancing', 'crucial', 'vital', 'symbolizing',
            'fostering', 'i hope this helps', 'great question', 'let me know',
            'in conclusion', 'the future looks bright', 'exciting times lie ahead',
            "at its core", "in reality", "what really matters", "fundamentally",
            "let's dive in", "let's explore", "without further ado",
            "journey toward excellence", "robust", "leverage", "utilize",
            "in order to", "due to the fact that"]

for w in ai_words:
    c = text.count(w.lower())
    if c > 0:
        print(f"  AI tell: '{w}' x{c}")

# Em dash count (site-specific baseline)
print(f"Em dashes: {text.count('—')}")
# Curly quotes (should be 0)
print(f"Curly quotes (double): {html.count('\u201c') + html.count('\u201d')}")
# Emojis (should be 0)
emoji_pattern = re.compile("["
    u"\U0001F600-\U0001F64F" u"\U0001F300-\U0001F5FF"
    u"\U0001F680-\U0001F6FF" u"\U0001F1E0-\U0001F1FF"]+", flags=re.UNICODE)
print(f"Emojis: {len(emoji_pattern.findall(html))}")
```

Site-specific calibration: some sites (feng shui sites in particular) use em dashes as a stylistic tic. Compare your count to the recent baseline:

```bash
for f in $(ls -t fate-*.html | head -5); do
  echo -n "$f: "
  grep -c "—" "$f"
done
```

Don't auto-strip below the site's baseline. Match the site's voice, including its quirks.

**Voice-matching without a sample:** when no voice sample is provided, match the cadence of the previous 3 articles. If they use long, mechanism-first paragraphs with concrete numbers ("the south wall of the home is the Wu mountain, the 15-degree slice from 172.5 to 187.5"), use the same. If they use short declarative sentences, use the same.

## Sitemap update

Sitemap convention for daily articles:

1. The new article goes at the TOP of the urlset (after the XML declaration and urlset tag, before any other url)
2. Same `<changefreq>` and `<priority>` as the prior daily entries (usually `monthly` / `0.7`)
3. Use `patch` with a precise old_string match — the file is often shared with git history

```python
# Pattern for adding a new entry at the top
old = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n  <url>\n    <loc>https://example.com/fate-YYYY-MM-DD.html'
new = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n  <url>\n    <loc>https://example.com/fate-YYYY-MM-DD-NEW.html</loc>\n    <changefreq>monthly</changefreq>\n    <priority>0.7</priority>\n  </url>\n  <url>\n    <loc>https://example.com/fate-YYYY-MM-DD.html'
```

## Commit and push

```bash
cd <repo>
git add fate-YYYY-MM-DD.html sitemap.xml
git commit -m "article: YYYY-MM-DD — <Short Title>"
git push origin <deployed-branch>   # NOT necessarily "master"
```

Verify the push succeeded before reporting:

```bash
git log --oneline -3   # confirm new commit on origin
```

## Post-publish verification

GitHub Pages / Cloudflare Pages / Netlify all take 30s-3min to deploy after push. Don't fire the verification curl instantly.

```bash
sleep 90
curl -s -o /dev/null -w "HTTP %{http_code} | %{size_download} bytes\n" https://example.com/fate-YYYY-MM-DD.html
curl -s https://example.com/fate-YYYY-MM-DD.html | grep -oE '<title>[^<]+</title>'
```

Expected: `HTTP 200`, title matches what you wrote, byte count ~ matches your file size. If `HTTP 404`, wait another minute and retry.

## Common pitfalls

### Don't assume the cron spec is right

The biggest time-saver is the pre-flight check. Specs get written once, then the repo changes. Spec says `master`, repo is on `main`. Spec says `competitor-research.md`, file is `article_topics.md`. Always verify before writing.

**Don't auto-push without verifying**

Always check `git status` and `git log` before pushing. A cron that runs at 8am every day could collide with a manual push from the user. If `git status` shows unstaged changes or `git log` shows a commit you didn't make, stop and investigate before pushing.

**Pillar-page slug collision across subagents and crons (NEW pitfall — verified 2026-07-01):**
Two agents writing the same pillar topic on the same day will create two URLs with different slugs (e.g. `china-unique-medical-procedures-guide.html` and `china-unique-medical-procedures.html`). Both pages ship, both get indexed, Google sees duplicate content and ranks neither well, and the sitemap ends up with near-duplicate entries. The 2026-07-01 case had a 24e927c commit at 16:35 creating `china-unique-medical-procedures-guide.html`, then a separate agent created `china-unique-medical-procedures.html` as part of a 11-page pillar batch — same topic, different slug, twice the size, 0% incremental SEO value.

**Pre-flight check for pillar / evergreen pages — added 2026-07-01:**
Before writing any evergreen / pillar / pillar-hub page (file pattern: not dated, lives in a topic directory), run:

```bash
cd <repo>
# Detect existing URL with same topic from sibling crons / subagents / past commits
git log --all --pretty=format: --name-only --since="7 days ago" | grep -E "^<dir>/<topic-slug-stem>" | sort -u
# If 1+ similar slugs exist in the last 7 days, the topic is already covered. Either:
#   a) reuse the existing slug and append new content
#   b) if the existing page is genuinely thin (< 2000 chars), expand it instead of creating a duplicate
#   c) if 2+ subagents are working concurrently, coordinate the slug naming in a shared lead-up message BEFORE writing
```

**Slug-coordination rule (NEW — added 2026-07-01):**
When a session prompt says "build a pillar for <topic>", the first action (BEFORE writing) is `ls <dir>/<topic>*` and `grep -l "<topic-phrase-1>\|<topic-phrase-2>" <dir>/*.html`. If a near-duplicate exists, STOP and pick one of three resolutions:
1. Reuse the existing slug, expand the existing page
2. Pick a more specific slug (`<topic>-guide.html`, `<topic>-hub.html`, `<topic>-overview.html`)
3. Push-back to the orchestrator before writing

The third option is the cheapest — flagging the collision costs 1 message; recovering from duplicate content + 301 redirect setup costs 4-6 tool calls + a re-push.

**301 redirect for the deprecated pillar (verified 2026-07-01):**
For the duplicate-pillar cleanup, the patch to add to `_redirects`:
```
/<dir>/<deprecated-slug>.html /<dir>/<kept-slug>.html 301
```
Cloudflare Pages / Netlify auto-apply on the next deploy. One line, one push, both URLs converge on the kept slug. Verify with `curl -I https://example.com/<dir>/<deprecated-slug>.html | head -1` returning `HTTP/2 301`.

**Subject-page stub verification before batch-creating 10+ pages (verified 2026-07-01):**
When a session is asked to build a "10 sub-pages for pillar X" or any coordinated batch, the pre-batch check is:

```bash
ls <dir>/<topic-prefix>-* 2>/dev/null
git log --all --pretty=format: --name-only --since="30 days ago" -- <dir>/ | grep -E "<topic-prefix>" | sort -u
```

If ≥1 page with the topic prefix already exists, prefer appending to the existing series (`<topic>-2.html`, `<topic>-index.html`) instead of starting from `<topic>.html`. The 2026-07-01 batch shipped 10 new `<topic>-*.html` sub-pages that all cross-linked to the existing `<topic>-guide.html` correctly, but also tried to ship an 11th page called exactly `<topic>.html` which created the duplicate-content bug.

### Don't write into the wrong template

A repo with two article styles (e.g., one template for `fate-YYYY-MM-DD.html` and another for `report-*.html`) will look broken if you mix them. Match the style of the most recent matching file in the same series.

### Don't ignore the prior article's topic

If yesterday's article was "Bagua Map" and today you write "Five Elements," you've broken the series continuity. The footer cross-link block will look weird, the reader's mental model breaks, and the site's topical authority is split across disjoint articles. Always read yesterday first.

### Don't ship an article that dropped the head term from the cluster (verified 2026-07-06)

The most subtle cluster-fracture is the one where the article is *about* the same topic as yesterday but the **headline doesn't carry the cluster's keyword**. The 2026-07-06 `fate-2026-07-06.html` shipped with `Li Qiu Eve: The Night Before the Fire-to-Earth Handoff` — a phrase that has near-zero search volume — breaking the July thread's `Front/Back/Balcony/Rooftop + Feng Shui for July` cluster on the article that was supposed to *cap* the thread (the eve-of-Li-Qiu closing article).

**Recipe to catch this BEFORE de-AI / publish:**
```bash
# Show today's headline + the prior 6 articles' headlines for visual coherence check
for f in $(ls -t fate-*.html | head -7); do
  echo -n "$(basename $f): "
  grep -oE '<title>[^<]+</title>' "$f" | head -1
done
```

If today's title is the odd one out (no shared head term with the prior 6), rewrite the headline to match the cluster before publishing. The body content can be left alone — the topic was right, only the keyword wrapper was wrong.

**Fix recipe for a ship-already article (verified 2026-07-06):** the fix is in 5 places that must move together:
- `<title>` (and ensure it's the only `<title>` — duplicate `<title>` tags break SEO)
- `<meta name="description">` (Primary Keyword in first sentence)
- `<meta property="og:title">` + `og:description`
- `<h1>` and hero `.subtitle` (subtitle usually mirrors the keyword too)
- `schema.org` JSON-LD `"headline"` and `"description"`

Use `patch` with a precise multi-line `old_string` that captures all 5 in one block, NOT one-by-one. One-by-one is brittle because of the `og:title` content length and the JSON-LD formatting. Do NOT add a `<meta name="keywords">` tag — Google has ignored that meta since 2009 and the prior 5 articles don't have one (consistency matters more than a 0-impact tag).

Verify with:
```bash
grep -E '<title>|<h1>|headline|og:title' fate-YYYY-MM-DD.html | head -10
```
All four should show the same Primary Keyword in the same position.

### Topic threading: the "conceptual foundation ladder" pattern (verified 2026-06-24 → 2026-06-28)

The seasonal threading pitfall above covers month-long themes (June = Fire Month room walk). A second, complementary pattern emerged in late June 2026: the **conceptual foundation ladder** — a 4-5 day sequence of articles that climb from one layer of the practice to the next, where each new article assumes the prior one as background. Verified sequence from oriental-destiny.com June 2026:

- 06-24: Bagua Map (the 9-cell energy grid — the spatial map)
- 06-25: Wealth Corner (Xiu cell) (one specific cell of the bagua, with activation rules)
- 06-26: Yin and Yang (the polarity concept that sits UNDER yin/yang-style cell readings)
- 06-27: Common Feng Shui Mistakes (6 cures applied without diagnosis — depends on bagua + yin/yang literacy)
- 06-28: Five Elements (the next layer down from yin/yang — Wood/Fire/Earth/Metal/Water as the qualities a room carries)

**Recipe to recognize a foundation-ladder opportunity:** at the start of the run, after reading yesterday's article, check whether yesterday (or the 2-3 prior articles) introduced a new concept (a tool, a layer, a methodology) without defining it. If 1+ articles assumed the concept is known, that concept is the **next ladder rung** — write the foundational piece that the prior articles assumed the reader already had. The lead paragraph of the new piece should explicitly reference the prior articles ("Earlier this month the Fire Month articles leaned on the word 'yang' without ever defining it..." — see programmatic-seo skill's "referenced-but-never-covered pivot" recipe for the full sentence pattern).

**Why this matters for SEO:** Google ranks sites that demonstrate topical depth. A site with 30 articles on room-specific feng shui reads as a topical cluster; a site with 5 articles on concepts + 25 on applications reads as having a coherent body of work. The ladder pattern produces both kinds of article in the same week, with each piece explicitly cross-linking the others via the footer "Explore more" block.

**Detection signal:** run `ls -t fate-YYYY-MM-DD-*.html | head -7 | xargs grep -l "[UNDEFINED_TERM]"` to find articles that USED a term without defining it. If 2+ recent articles assume the term, that term is a ladder-rung candidate. The 06-26 Yin/Yang article emerged from finding `yin|yang` referenced but never pillar-defined in the prior 30 days.

**Scaled-companion extension (NEW — verified 2026-07-03):** when the current thread assumes a property the majority of readers don't have (e.g. "back garden" for an audience of mostly apartment-dwellers), write a companion piece at a different scale using the same structural skeleton. The 07-03 Balcony article extended the 07-01 Front Garden + 07-02 Back Garden thread by writing the same Fu Wei concept at apartment-dweller scale, with the same bridge-sentence → 5 moves → Day-Master-by-element → undo-at-Li-Qiu → FAQs structure. Pattern generalizes: full property → apartment, full chart → child chart, surgery → outpatient, US pathway → cross-border pathway. Always use the SAME close-out checkpoint as the original thread (both 07-02 and 07-03 land on "undo at Li Qiu on July 7"). Full recipe and pitfalls: `references/thread-extension-patterns.md`.

### Don't ship before verifying de-AI

If the spec says "score > 60 required," treat it as a hard gate. A humanizer audit that finds 12 instances of `delve`/`tapestry`/`testament`/`underscore` should be rewritten, not shipped. Programmatic scan catches most of these in seconds.

### Don't repeat the same parallel structure across listicle cards

The humanizer's 29 patterns are mostly about vocabulary and grammar. There's a class-level structural tell that doesn't show up in any word list: **when every card in a listicle opens with the same parallel structure, the article starts to read as templated**. Example failure mode from the 2026-06-27 cron run: six "mistake" cards each opened with "The popular version: X. The classical version: Y. Cleaner prescription: Z." The structure is fine for one card. After three or four repetitions the article reads like a fill-in-the-blank form.

Mitigation:
- Vary the opener of each card (1-2 lines that set up the specific mistake in its own terms)
- Keep the structural skeleton identical only if you have to (and at most 2-3 cards in a row)
- If the article has 5+ list items with the same skeleton, run `references/../scripts/de-ai-scan.py` which now flags repeated sentence-openings and repeated section markers as warnings

### Don't bury the article in unrelated cross-links

The footer "Explore more" block should link to the prior 3-5 articles in the same series. Linking to `/checkout.html` and `/index.html` is fine for the static links, but the series-context links should be dated articles, not random other pages.

**Don't inherit a sibling-agent's sitemap indent (verified 2026-07-03):** when patching sitemap.xml, the new entry's indentation should match the file's DOMINANT convention (typically 4 spaces in this repo), not the immediately-prior entry's indent. The 2026-07-03 patch initially came in at 6-space indent because I copy-pasted the 07-02 entry as my anchor — and the 07-02 entry itself was at 6-space indent (a sibling-agent artifact from the prior day). The fix was a second patch to normalize the new entry to 4 spaces. Check `head -20 sitemap.xml` after the first patch and compare the new entry's indent to entries 3-5 lines down (the historical convention) before committing. Don't "fix" the sibling's wrong indent in the same commit — that's a separate concern, and mixing it with the new article's commit pollutes the article's diff.

**Image-filename sanity check before referencing in news/index.html (verified 2026-07-06):** when writing the `news/index.html` card for a new article, always run `ls images/ | grep KEYWORD` BEFORE referencing any image filename. The article page itself rarely references an image (it lives inline as content), but the index card almost always does. The 2026-07-06 run initially wrote `images/tcm-herbal-medicine.jpg` as the index card's image source — a name I generated from the article's topic that doesn't actually exist on the repo (the repo has `wellness-spa.jpg`, `china-hospital.jpg`, etc., but no `tcm-*` images). The fix was a follow-up patch to swap to `wellness-spa.jpg` (a real file that fits the AI-TCM wellness angle and was already used by the 07-03 bathhouse article). The broader lesson: **image filenames are a curated list on the repo, not a topic-derivable string**. Default to grepping for an existing filename that fits the article's visual angle, and only commit to a new image path if you've actually placed the file. Quick recipe:

```bash
# Find a fitting image by topic keyword
ls images/ | grep -iE "wellness|tcm|china|hospital|medical"
# If a fit exists, use it. If none fit, fall back to the most generic available:
# wellness-spa.jpg, china-hospital.jpg, medical-tourism.jpg, global-medical.jpg
```

The fallback list (verified 2026-07-06): `wellness-spa.jpg` (TCM/wellness/traditional therapy), `china-hospital.jpg` / `china-hospital-building.jpg` (hospital/clinical), `medical-tourism.jpg` (general medical tourism), `global-medical.jpg` (general international medical). One of these will fit almost any medical article. Don't invent a new image path on the fly.

**news/index.html canonical-pattern insertion despite sibling-agent artifact messiness (verified 2026-07-06):** the news/index.html file on multi-agent-cron repos often ends up with interleaved `<article class="news-item">` and `<article class="news-card">` blocks from sibling agents' earlier patches. When inserting a new article card, match the **canonical pattern** (`<article class="news-item">` on chinahospitalsguide) — not whatever the immediately-prior entry uses. Do NOT attempt to clean up the sibling's artifacts in the same patch — that's a separate concern that should ship in its own commit. The 2026-07-06 run inserted cleanly into the canonical pattern even though lines 270-300 of the index showed visible sibling-style interleaving (news-item + news-card mixed). The canonical-pattern anchor (`<article class="news-item">` followed by `<img src="../images/...">`) was uniquely identifiable in the file even with the sibling mess around it. Don't "fix" the sibling's wrong style in the same commit — that pollutes the article's diff and adds review surface for the article itself.

### Don't use wrong date format

The filename pattern is `fate-YYYY-MM-DD.html` (ISO 8601). The `datePublished` JSON-LD field uses the same format. The visible "Published" line uses a long-form format ("Published June 25, 2026 · 9 min read"). The reading time is a rough estimate based on word count (~200 words/min).

## Workflow summary

1. **Pre-flight** (2 min): verify branch, repo state, file existence, git remote
2. **Template fingerprint** (3 min): read yesterday's article, extract CSS/structure
3. **Topic selection** (2 min): read research notes, pick topic that ladders from yesterday
4. **Draft** (15-20 min): write 3,500-4,500 word article in matching template
5. **Keyword template check** (1 min): confirm `<title>` / `<h1>` / `og:title` / schema.org headline all match the `[X Feng Shui/BaZi/Destiny]: [Long-tail Hook]` template and match the cluster's head term — see "Primary keyword and headline template" above
6. **De-AI audit** (3 min): programmatic scan + manual humanizer pass
7. **Sitemap update** (1 min): add new entry at top
8. **Commit and push** (1 min): `git add . && git commit && git push origin <branch>`
9. **Verify** (90s): sleep, then curl to confirm 200 + correct title

Total: ~30 minutes. Buffer: 5-10 minutes for fixes if any step goes wrong.

## Reference files

- `references/site-fingerprint-template.md` — what the oriental-destiny.com template fingerprint looks like, with measured baselines (em-dash density, word count, section norms) and a live series-continuity table
- `references/oriental-destiny-element-card-css.md` — the `.element-card` CSS class scheme with per-element border colors (Wood/Fire/Earth/Metal/Water), for articles that walk through individual elements. Reverse-engineered from the seo-generator's `ELEMENT_THEMES` constant.
- `scripts/de-ai-scan.py` — runnable de-AI scanner that catches humanizer 29-pattern hits plus structural tells (repeated sentence-openers, repeated section markers, heading-restated-by-intro). Run with `--strict` for CI-style gating