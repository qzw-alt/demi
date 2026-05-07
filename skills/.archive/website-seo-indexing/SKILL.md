---
name: website-seo-indexing
description: Google Search Console issues, sitemap indexing problems, and CTR optimization for China Hospitals Guide
---

# Website SEO & Indexing Workflow

## Google Search Console Issues

### "备用网页" (Alternative page with proper canonical)
- **不是错误** — 这是正常状态，Google正确处理了带www和不带www的页面
- **不需要处理**

### sitemap 49页但只索引8页
- **原因**：sitemap刚提交，Google需要数天到数周抓取所有页面
- **正常现象**，尤其是新站
- **解决方案**：
  1. 手动在 Search Console "网址检查" 请求核心页面索引
  2. 每天提交5-10个
  3. 一周后复查覆盖率报告

### URL检查返回404但页面实际存在
- 可能是Google工具临时故障或缓存问题
- 解决方法：等几分钟重试，或用"测试实时网址"

### 排名好但CTR低
- **原因**：标题/描述不够吸引人
- **优化策略**：
  - 标题添加数字（价格、节省金额）
  - 标题包含明确关键词
  - 描述有行动号召 (CTA)
  - 匹配用户搜索词

## SEO Metadata Audit — All HTML Pages

> **Triggered when:** user asks to audit, fix, or inject SEO meta tags (canonical, og:*, twitter:*, JSON-LD) across any batch of HTML files.

### Scope: Blog AND Top-Level Pages

The same SEO tags apply to ALL `.html` pages — not just `blog/*.html`. Top-level pages (about.html, cancer.html, pricing.html, etc.) need the same treatment. Always audit and fix the **full site** when doing batch SEO work, not just blog articles.

### JSON-LD Page Type by Filename

```python
def get_page_type(fname):
    if fname == 'index.html':     return 'WebSite'
    elif fname == 'about.html':   return 'AboutPage'
    elif 'contact' in fname:      return 'ContactPage'
    elif fname == 'privacy.html': return 'PrivacyPolicy'
    elif fname == 'terms.html':   return 'TermsOfService'
    else:                         return 'WebPage'
```

### Injection Pattern (Python, NOT PowerShell)

```python
import os, re, glob

BASE = "/path/to/site"
OG_IMAGE = "https://example.com/og-image.jpg"  # must exist; fallback if no per-page image
SITE_NAME = "Site Name"

for fpath in glob.glob(f"{BASE}/*.html"):
    fname = os.path.basename(fpath)
    if fname == 'sitemap.xml': continue
    content = open(fpath, encoding='utf-8').read()
    page_url = f"https://example.com/{fname}"

    title_m = re.search(r'<title>([^<]+)</title>', content)
    title = title_m.group(1).strip() if title_m else ""
    desc_m = re.search(r'<meta name="description" content="([^"]*)"', content)
    description = desc_m.group(1).strip() if desc_m else ""

    seo_block = ""
    for tag in [
        ('og:type', '<meta property="og:type" content="website">'),
        ('og:title', f'<meta property="og:title" content="{title}">'),
        ('og:description', f'<meta property="og:description" content="{description}">'),
        ('og:url', f'<meta property="og:url" content="{page_url}">'),
        ('og:image', f'<meta property="og:image" content="{OG_IMAGE}">'),
        ('og:site_name', f'<meta property="og:site_name" content="{SITE_NAME}">'),
    ]:
        field, tag_str = tag
        if not re.search(rf'<meta property="{field.split(":")[0]}:"', content):
            seo_block += f"\n    {tag_str}"

    if not re.search(r'<meta name="twitter:card"', content):
        seo_block += f"""
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{title}">
    <meta name="twitter:description" content="{description}">
    <meta name="twitter:image" content="{OG_IMAGE}">"""

    if not re.search(r'<script type="application/ld\+json"', content):
        ptype = get_page_type(fname)
        seo_block += f'''
    <script type="application/ld+json">
{{
"@context": "https://schema.org",
"@type": "{ptype}",
"headline": "{title}",
"description": "{description}",
"author": {{ "@type": "Organization", "name": "Site Name" }},
"publisher": {{
"@type": "Organization",
"name": "Site Name",
"logo": {{ "@type": "ImageObject", "url": "https://example.com/images/logo.png" }}
}},
"dateModified": "2026-05-02",
"url": "{page_url}"
}}
</script>'''

    if seo_block and '</head>' in content:
        content = content.replace('</head>', seo_block + "\n    " + '</head>')
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated: {fname}")
```

### Pitfall: og:image Must Exist Before Using

Check `og-image.jpg` exists at site root before using as fallback. If it does NOT exist:
- Report to user immediately
- Do NOT generate a placeholder image
- Do NOT hotlink external images
- Wait for user decision (use logo.png? provide real image?)

### Pitfall: PowerShell Regex Encoding Bug

PowerShell 5.x misinterprets Unicode characters in .ps1 source files, writing them as `??`. Workaround:
- Write audit/injection scripts in Python, not PowerShell
- If PowerShell is unavoidable: save as UTF-8 with BOM, use ASCII-only string literals

## SEO Metadata Audit — 批量博客文章

> **Triggered when:** user asks to audit, fix, or inject SEO meta tags (canonical, og:*, twitter:*, JSON-LD) across a batch of blog HTML files.

### Critical Discovery: Audit First, Don't Inject Blindly

**Most blog files already have SEO meta in place.** The real problems are:
1. **Duplicate tags** (same tag appearing 2x in one file) — causes Google/FB/Twitter to pick wrong value
2. **Wrong canonical URL** (pointing to root instead of /blog/ subfolder)
3. **Missing og:image** (use site-wide fallback `og-image.jpg`)

**Always run audit BEFORE writing any injection script.** Script approach:
```python
# Audit script pattern (use Python, NOT PowerShell — avoids regex/encoding bugs)
import re, glob

BLOG = "/path/to/blog"
BASE_URL = "https://example.com/blog"

for fpath in sorted(glob.glob(f"{BLOG}/*.html")):
    content = open(fpath, encoding='utf-8').read()
    fname = os.path.basename(fpath)
    canonicals = re.findall(r'<link rel="canonical" href="[^"]*"', content)
    og_urls = re.findall(r'<meta property="og:url" content="[^"]*"', content)
    tw_cards = re.findall(r'<meta name="twitter:card"', content)
    has_article = bool(re.search(r'"@type"\s*:\s*"Article"', content))

    issues = []
    if len(canonicals) > 1: issues.append(f"canonical_dup:{len(canonicals)}")
    if len(og_urls) > 1: issues.append(f"og_url_dup:{len(og_urls)}")
    if len(tw_cards) > 1: issues.append(f"twitter_dup:{len(tw_cards)}")
    if issues:
        print(f"ISSUE {fname}: {', '.join(issues)}")
```

**Common audit findings:**
- `og:site_name` often already present — don't re-add
- Most files already have full OG + Twitter + JSON-LD Article schema
- Deduplication (not injection) is usually the needed fix

### Deduplication Fix Pattern

```python
# For each conflicted file:
canonicals = re.findall(r'<link rel="canonical" href="[^"]*"', content)
if len(canonicals) > 1:
    # Keep first occurrence, remove rest
    first_idx = content.find(canonicals[0])
    rest = content[first_idx + len(canonicals[0]):]
    rest = re.sub(r'<link rel="canonical"[^>]*>', '', rest)
    content = content[:first_idx + len(canonicals[0])] + rest
```

### Git Conflict Resolution During Batch Updates

When remote has concurrent edits during `git rebase`:
- Conflict markers (<<<<<<, =======, >>>>>>) break HTML parsing
- Resolve by: read conflict blocks → keep deduplicated version → `git add` → continue
- After resolution: verify all files clean (`<<<<<<` absent) before push
- If rebase leaves orphaned `rebase-apply/` dir: `rm -rf .git/rebase-apply`

## Oriental Destiny 项目

### 收款方案
- Gumroad：个人可注册，支持PayPal
- 域名验证需要自定义域名 + DNS配置

### DNS配置 (GoDaddy)
- www CNAME → qzw-alt.github.io
- @ URL转发 → https://www.oriental-destiny.com

### GitHub Pages
- Settings → Pages → Custom domain → oriental-destiny.com
- 勾选 Enforce HTTPS

### Critical Discovery: blog/ and news/ Are the Same Physical Files

**This is a site architecture problem.** News articles appear in both `blog/` AND `news/` directories under the SAME filename:
```
blog/2026-03-24-japan-china-proton-therapy.html  ← blog article URL
news/2026-03-24-japan-china-proton-therapy.html  ← same file, different URL
```
Both URLs resolve and both have distinct canonicals pointing to themselves. Google sees them as two different pages with different content (even though they're identical). This creates:
- **Duplicate content penalty risk**
- **Split ranking signals** — links/authority are divided between two URLs
- **Sitemap confusion** — which URL is the "real" one?

**Recommended action**: Choose one as canonical:
- If blog articles should be the canonical version → remove news/ duplicates and have news/ directory redirect or not exist
- If news/ should be the canonical version → remove from blog/ and update sitemap

**Quick check**:
```python
blog_files = set(os.listdir(f"{BASE}/blog"))
news_files = set(os.listdir(f"{BASE}/news"))
overlap = blog_files & news_files
# overlap will include 'index.html' + any news articles duplicated in blog/
```

### Sitemap Source of Truth: Filesystem, Not Manual Maintenance

**Critical workflow change discovered 2026-05-02:**

The sitemap was being manually maintained, which caused massive drift:
- news/ 50 articles completely absent from sitemap
- phantom URLs (template files, index pages) present
- blog/ had 59 articles but sitemap had 86 phantom entries

**Correct approach**: Rebuild sitemap from filesystem every time:
```python
import os, re
from datetime import datetime

BASE = "/path/to/site"
BASE_URL = "https://example.com"
TODAY = "2026-05-02"

def lm(filepath):
    try:
        return datetime.fromtimestamp(os.path.getmtime(filepath)).strftime("%Y-%m-%d")
    except:
        return TODAY

# For each directory, enumerate real .html files (exclude index.html, template-*.html)
# Build sitemap programmatically, always from filesystem
```

**Exclusions for sitemap** (never include):
- `index.html` in any subdirectory (directory index pages are not useful to Google)
- `template-*.html` (draft/article template files)
- Any file whose content indicates it's not a real page

**News sitemap priority**: Use `weekly` changefreq + `0.7` priority (news articles decay faster than blog)

## Support Files

- `references/full-site-seo-2026-05-02.md` — comprehensive audit: blog (59) + news (49) + course (9) + top-level (20) = 137 pages, all findings, all fixes applied