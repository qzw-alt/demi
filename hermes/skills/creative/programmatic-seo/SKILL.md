---
name: programmatic-seo
description: "Programmatic SEO article writing for content sites. Workflow: research → draft → humanize → publish → update sitemap. Currently serving oriental-destiny.com and chinahospitalsguide.com."
version: 1.1.0
author: Hermes Agent
platforms: [linux]
metadata:
  hermes:
    tags: [seo, content, writing, feng-shui, bazi, destiny, medical-tourism, programmatic]
    category: creative
---

# Programmatic SEO: Article Writing for Content Sites

Write and publish daily SEO articles for oriental-destiny.com (feng shui / BaZi / destiny) and chinahospitalsguide.com (Chinese medical tourism).

## Workflow (6 Steps)

### Step 1: Research
Load and use `content-research-writer-cn` skill to find today's热点.

### Step 2: SEO Writing
Based on research findings, write article following these rules:

**Article Structure:**
- Title: clear, keyword-rich, Chinese audience
- Lead paragraph: who/what/when/where/why in 2-3 sentences
- Body: 3-5 sections with H2/H3 headings
- Conclusion: practical next steps or summary

**SEO Requirements:**
- Target keyword in title, first paragraph, one H2 heading
- Internal link to relevant hospital page if applicable
- External link to authoritative source (卫健委, 医院官网, etc.)
- 800-1500 words
- Readability: Chinese Flesch score target (use simple sentences, short paragraphs)

**Tone:** Professional but accessible; factual; no sensationalism

### Step 3: Humanize
Load `humanizer` skill and apply to draft. Score must be >60.

### Step 4: Publish
Save to news/ directory as `YYYY-MM-DD.html`

### Step 5: Update Sitemap
- Add article entry to `sitemap.xml` (insert new `<url>` entry at top of `<urlset>`)
- Add article card to `news/index.html` link list (insert at top, before the oldest article)
- **Verify both** before proceeding to Step 6

### Step 6: Git Push
First check which branch the remote uses (`main` vs `master`):
```bash
git remote -v
git branch -a | head -5
```
If the remote uses `main`, push to `origin main`, not `origin master`.

Always verify the remote URL has credentials embedded — otherwise push silently fails:
```bash
git remote -v
# If no token in URL (shows "github.com" without "token"), fix:
git remote set-url origin "https://$(cat ~/.git-credentials 2>/dev/null | grep -o 'github_pat_[^@]*')@github.com/qzw-alt/REPO.git"
```

**Sitemap conflict prevention:** Before pulling or rebasing, check whether another agent has recently pushed. Concurrent sitemap edits cause rebase conflicts. If the remote is ahead, prefer a merge commit over a rebase, or work on a short-lived branch:
```bash
git checkout -b article-YYYY-MM-DD origin/main
# work, commit, push to article-YYYY-MM-DD:main
```

After push, wait 2-3 minutes then verify the live URL returns HTTP 200.

### Step 7: Report
After publish, report:
- 文章标题
- 字数
- 去AI化评分
- 发布的 URL

## Integration

```
content-research-writer-cn → (hot topic) → programmatic-seo → (draft) → humanizer → (humanized) → publish → sitemap → git push
```

Each skill feeds into the next. Always run in sequence.

- 去AI化评分 >60 required for publish
- 1 article per day during 栏目新建期
- No good 热点 → no publish (宁缺毋滥)
- After push, verify at https://chinahospitalsguide.com/news/ (wait 2-3 min)

## Site Configurations

See `references/site-configs.md` for per-site configuration (branch names, directory layout, naming conventions, sitemap handling).