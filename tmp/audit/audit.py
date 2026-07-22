"""
Audit chinahospitalsguide.com for unindexed cleanup candidates.

Steps:
1. Pull sitemap.xml from the live site (it's gitignored _site/ thing -> GitHub Pages serves it)
2. For each URL, fetch the page and measure:
   - title
   - meta description
   - word count (visible text only)
   - canonical URL
   - has schema JSON-LD
   - is index/follow
3. Detect near-duplicates (same title prefix, similar word count)
4. Categorize as DELETE / MERGE / REWRITE / KEEP

Output: Markdown report
"""

import urllib.request
import urllib.error
import re
import json
import os
import sys
from collections import defaultdict
from pathlib import Path

# Step 1: Fetch sitemap
SITEMAP_URL = "https://chinahospitalsguide.com/sitemap.xml"

print(f"[1] Fetching sitemap: {SITEMAP_URL}")
try:
    with urllib.request.urlopen(SITEMAP_URL, timeout=30) as resp:
        sitemap_xml = resp.read().decode('utf-8')
except urllib.error.URLError as e:
    print(f"  ERROR fetching sitemap: {e}")
    sys.exit(1)

# Extract URLs
url_pattern = re.compile(r'<loc>([^<]+)</loc>')
urls = url_pattern.findall(sitemap_xml)
urls = [u for u in urls if 'chinahospitalsguide.com' in u]
# Dedupe but keep order
seen = set()
unique_urls = []
for u in urls:
    if u not in seen:
        seen.add(u)
        unique_urls.append(u)
print(f"  Found {len(unique_urls)} unique URLs")

# Step 2: Fetch each URL and gather HTML metrics
HTML_TAG_RE = re.compile(r'<[^>]+>')
WS_RE = re.compile(r'\s+')

def html_metrics(url):
    """Fetch a URL and return basic content metrics."""
    try:
        with urllib.request.urlopen(url, timeout=20) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
            status = resp.status
    except Exception as e:
        return {'url': url, 'status': 'error', 'error': str(e)[:100]}

    # Title
    title_m = re.search(r'<title>([^<]+)</title>', html, re.IGNORECASE)
    title = title_m.group(1).strip() if title_m else ''

    # Meta description
    desc_m = re.search(r'<meta\s+name=["\']description["\']\s+content=["\']([^"\']*)["\']', html, re.IGNORECASE)
    description = desc_m.group(1).strip() if desc_m else ''

    # Canonical
    canon_m = re.search(r'<link[^>]*rel=["\']canonical["\'][^>]*href=["\']([^"\']*)["\']', html, re.IGNORECASE)
    canonical = canon_m.group(1).strip() if canon_m else ''

    # Meta robots
    robots_m = re.search(r'<meta\s+name=["\']robots["\']\s+content=["\']([^"\']*)["\']', html, re.IGNORECASE)
    robots = robots_m.group(1).strip() if robots_m else 'no-meta'

    # Schema JSON-LD count
    schema_count = html.count('application/ld+json')

    # Body text extraction (very rough, strip tags)
    body_m = re.search(r'<body[^>]*>(.*?)</body>', html, re.IGNORECASE | re.DOTALL)
    body_text = body_m.group(1) if body_m else html
    # Remove script/style
    body_text = re.sub(r'<script[^>]*>.*?</script>', '', body_text, flags=re.DOTALL | re.IGNORECASE)
    body_text = re.sub(r'<style[^>]*>.*?</style>', '', body_text, flags=re.DOTALL | re.IGNORECASE)
    # Strip remaining tags
    body_text = HTML_TAG_RE.sub(' ', body_text)
    body_text = WS_RE.sub(' ', body_text).strip()
    word_count = len(body_text.split())

    return {
        'url': url,
        'status': status,
        'title': title,
        'desc_len': len(description),
        'canonical': canonical,
        'robots': robots,
        'schema_count': schema_count,
        'word_count': word_count,
    }

print(f"[2] Fetching and measuring {len(unique_urls)} pages...")
results = []
for i, u in enumerate(unique_urls):
    m = html_metrics(u)
    results.append(m)
    if (i+1) % 10 == 0:
        print(f"  {i+1}/{len(unique_urls)} done")

print(f"\n[3] Categorizing...")

# Categorization logic
def categorize(m):
    if m.get('status') != 200:
        return 'BROKEN'
    if m.get('word_count', 0) < 150:
        return 'TOO_SHORT'
    if m.get('word_count', 0) < 400:
        return 'THIN'
    if m.get('schema_count', 0) == 0:
        return 'NO_SCHEMA'
    return 'HEALTHY'

categorized = []
for m in results:
    cat = categorize(m)
    categorized.append({**m, 'category': cat})

# Detecting duplicates
# Group by title-prefix (first 5 words, lowered)
title_groups = defaultdict(list)
for m in categorized:
    if not m.get('title'):
        continue
    prefix = ' '.join(m['title'].split()[:5]).lower()
    # Strip domain name from titles
    prefix = re.sub(r'\| china hospitals guide.*$', '', prefix).strip()
    title_groups[prefix].append(m['url'])

dup_groups = {k: v for k, v in title_groups.items() if len(v) > 1}

# Output
output_path = Path('/home/ubuntu/.hermes/tmp/audit/audit-report.md')
output_path.parent.mkdir(parents=True, exist_ok=True)

with open(output_path, 'w', encoding='utf-8') as f:
    f.write(f"# chinahospitalsguide.com 内容体检报告\n")
    f.write(f"**生成时间**: 2026-07-21\n")
    f.write(f"**扫描 URL**: {len(unique_urls)}\n\n")

    # Summary
    cat_counts = defaultdict(int)
    for m in categorized:
        cat_counts[m['category']] += 1
    f.write("## 分类汇总\n\n")
    f.write("| 类别 | 数量 | 处置建议 |\n|---|---|---|\n")
    actions = {
        'BROKEN': '修复（如可能）或删除',
        'TOO_SHORT': '⚠️ 强删（< 150 字几乎无 SEO 价值）',
        'THIN': '合并到其他相关页面',
        'NO_SCHEMA': '保留 + 加 Schema',
        'HEALTHY': '保留',
    }
    for cat in ['BROKEN', 'TOO_SHORT', 'THIN', 'NO_SCHEMA', 'HEALTHY']:
        f.write(f"| {cat} | {cat_counts[cat]} | {actions.get(cat, '?')} |\n")

    f.write("\n## 重复页面组（同标题前缀）\n\n")
    if dup_groups:
        for prefix, urls in sorted(dup_groups.items()):
            f.write(f"### \"{prefix}...\"\n")
            for u in urls:
                f.write(f"- {u}\n")
            f.write(f"  → **合并**：留 1 个最强的，其他 301 重定向\n\n")
    else:
        f.write("无明显重复组\n\n")

    f.write("\n## 详细清单\n\n")
    f.write("| URL | 类别 | 字数 | Schema | Robots | 标题 |\n|---|---|---|---|---|---|\n")
    for m in sorted(categorized, key=lambda x: (x['category'], -x.get('word_count', 0))):
        title_short = (m.get('title') or '')[:60]
        f.write(f"| [{m['url'].replace('https://chinahospitalsguide.com', '')}]({m['url']}) | **{m['category']}** | {m.get('word_count', '?')} | {m.get('schema_count', 0)} | {m.get('robots', '?')} | {title_short} |\n")

print(f"\n[4] Report written: {output_path}")

# Console summary
print(f"\n=== Summary ===")
for cat in ['HEALTHY', 'NO_SCHEMA', 'THIN', 'TOO_SHORT', 'BROKEN']:
    cnt = cat_counts[cat]
    bar = '█' * cnt
    print(f"  {cat:12} {cnt:4} {bar}")
print(f"  Duplicate title groups: {len(dup_groups)}")
