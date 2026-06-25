---
name: seo-article-publish-cron
description: "Run a daily SEO article publishing cron job — verify repo state, match existing article template, write English article, de-AI pass, update sitemap, commit and push to the deployed branch. Use when a cron task says 'publish daily SEO article to <site>' with a GitHub Pages deployment from a repo."
version: 1.0.0
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
- Branch name (`master` vs `main`)
- Topic-source filename (often renamed or never existed)
- Skill names (spec author remembered wrong)
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

Match these exactly. Copy yesterday's <style> block, replace the title/date/headline/body, keep the rest identical. Future agents can edit content without breaking the visual contract.

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

## De-AI pass (hard gate)

The cron spec usually says "de-AI score > 60 to publish." Treat it as a hard gate. Run the humanizer skill audit (the SKILL.md lists 29 patterns to scan).

Quick programmatic scan (catches most tells in seconds):

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

### Don't auto-push without verifying

Always check `git status` and `git log` before pushing. A cron that runs at 8am every day could collide with a manual push from the user. If `git status` shows unstaged changes or `git log` shows a commit you didn't make, stop and investigate before pushing.

### Don't write into the wrong template

A repo with two article styles (e.g., one template for `fate-YYYY-MM-DD.html` and another for `report-*.html`) will look broken if you mix them. Match the style of the most recent matching file in the same series.

### Don't ignore the prior article's topic

If yesterday's article was "Bagua Map" and today you write "Five Elements," you've broken the series continuity. The footer cross-link block will look weird, the reader's mental model breaks, and the site's topical authority is split across disjoint articles. Always read yesterday first.

### Don't ship before verifying de-AI

If the spec says "score > 60 required," treat it as a hard gate. A humanizer audit that finds 12 instances of `delve`/`tapestry`/`testament`/`underscore` should be rewritten, not shipped. Programmatic scan catches most of these in seconds.

### Don't bury the article in unrelated cross-links

The footer "Explore more" block should link to the prior 3-5 articles in the same series. Linking to `/checkout.html` and `/index.html` is fine for the static links, but the series-context links should be dated articles, not random other pages.

### Don't use wrong date format

The filename pattern is `fate-YYYY-MM-DD.html` (ISO 8601). The `datePublished` JSON-LD field uses the same format. The visible "Published" line uses a long-form format ("Published June 25, 2026 · 9 min read"). The reading time is a rough estimate based on word count (~200 words/min).

## Workflow summary

1. **Pre-flight** (2 min): verify branch, repo state, file existence, git remote
2. **Template fingerprint** (3 min): read yesterday's article, extract CSS/structure
3. **Topic selection** (2 min): read research notes, pick topic that ladders from yesterday
4. **Draft** (15-20 min): write 3,500-4,500 word article in matching template
5. **De-AI audit** (3 min): programmatic scan + manual humanizer pass
6. **Sitemap update** (1 min): add new entry at top
7. **Commit and push** (1 min): `git add . && git commit && git push origin <branch>`
8. **Verify** (90s): sleep, then curl to confirm 200 + correct title

Total: ~30 minutes. Buffer: 5-10 minutes for fixes if any step goes wrong.

## Reference files

- `references/site-fingerprint-template.md` — what the oriental-destiny.com template fingerprint looks like, for new agents who haven't seen the site
- `references/de-ai-scan-script.py` — copy-paste de-AI scanner from the audit step above