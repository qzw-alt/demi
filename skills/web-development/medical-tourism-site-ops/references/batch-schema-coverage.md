# Batch Schema Coverage Audit + Inject — Reference

**Verified**: 2026-07-02. **Result**: 152 files updated, blog 64%→100%, news 16%→100% in ~10 minutes.

## When to use

When the site has hundreds of HTML content pages and you suspect schema coverage is incomplete. **Symptoms**:
- GSC `Enhancements` tab shows far fewer Articles/Breadcrumbs than the sitemap entry count
- Manual inspection of random pages shows some have no JSON-LD at all
- Site was built by multiple agents/cron jobs over time and schema was added ad-hoc

## Pre-flight: inventory script

```python
import os, re
from collections import Counter

base = "/home/ubuntu/.hermes/workspace/website"
SKIP_DIRS = ["blog-export", "blog-articles", "stories", "course", "医疗旅游",
             "templates", "report-carlos", ".git", "node_modules", "docs"]
SKIP_FILES = ["404.html", "panel.html", "patient-story-program.html"]

def inventory():
    no_schema, one_schema, two_plus = [], [], []
    type_counter = Counter()
    for root, dirs, files in os.walk(base):
        if any(s in root for s in SKIP_DIRS):
            continue
        for f in files:
            if not f.endswith(".html"):
                continue
            if f in SKIP_FILES:
                continue
            full = os.path.join(root, f)
            with open(full) as fp:
                text = fp.read()
            schemas = re.findall(
                r'<script type="application/ld\+json">([\s\S]*?)</script>', text)
            n = len(schemas)
            all_types = []
            for s in schemas:
                all_types += re.findall(r'"@type"\s*:\s*"([^"]+)"', s)
            for t in all_types:
                type_counter[t] += 1
            rel = full.replace(base + "/", "")
            if n == 0:
                no_schema.append(rel)
            elif n == 1:
                one_schema.append((rel, all_types))
            else:
                two_plus.append((rel, all_types))
    total = len(no_schema) + len(one_schema) + len(two_plus)
    return {
        "total": total,
        "no_schema": no_schema,
        "one_schema": one_schema,
        "two_plus": two_plus,
        "type_counter": type_counter,
    }

inv = inventory()
print(f"Total: {inv['total']}")
print(f"  No schema: {len(inv['no_schema'])}")
print(f"  1 schema:  {len(inv['one_schema'])}")
print(f"  2+ schema: {len(inv['two_plus'])}")
print(f"\nType coverage:")
for t, c in inv["type_counter"].most_common():
    pct = c / inv["total"] * 100
    print(f"  {t}: {c}/{inv['total']} = {pct:.0f}%")
```

## Inject script (idempotent)

```python
import os, re

base = "/home/ubuntu/.hermes/workspace/website"

# Per-directory breadcrumb label
def breadcrumb_section(path):
    if "/blog/" in path: return "Blog"
    if "/news/" in path: return "News"
    if "/stories/" in path: return "Patient Stories"
    return "Home"

# Phase 1: find files missing Article or BreadcrumbList
targets = []
for root, dirs, files in os.walk(base):
    if any(s in root for s in SKIP_DIRS):
        continue
    for f in files:
        if not f.endswith(".html"): continue
        if f in SKIP_FILES: continue
        full = os.path.join(root, f)
        with open(full) as fp: text = fp.read()
        schemas = re.findall(r'<script type="application/ld\+json">([\s\S]*?)</script>', text)
        all_types = []
        for s in schemas: all_types += re.findall(r'"@type"\s*:\s*"([^"]+)"', s)
        if "Article" in all_types and "BreadcrumbList" in all_types:
            continue  # fully covered, skip
        title_m = re.search(r'<title>([^<]+)</title>', text)
        title = (title_m.group(1) if title_m else f).strip()
        title = re.sub(r'\s*[\|·–-]\s*China Hospitals Guide.*$', '', title)
        title = re.sub(r'\s*\(2026\)\s*$', '', title)
        targets.append({
            "path": full, "title": title[:100],
            "need_article": "Article" not in all_types,
            "need_breadcrumb": "BreadcrumbList" not in all_types,
            "section": breadcrumb_section(full),
        })

# Phase 2: inject
success = errors = 0
for t in targets:
    try:
        with open(t["path"]) as fp: text = fp.read()
        blocks = []
        if t["need_article"]:
            article_url = "https://chinahospitalsguide.com" + t["path"].replace(
                "/home/ubuntu/.hermes/workspace/website", "")
            blocks.append(f'''
    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": "{t["title"]}",
        "description": "{t["title"]} - China Hospitals Guide",
        "image": "https://chinahospitalsguide.com/og-image.webp",
        "author": {{ "@type": "Organization", "name": "China Hospitals Guide" }},
        "publisher": {{
            "@type": "Organization",
            "name": "China Hospitals Guide",
            "logo": {{ "@type": "ImageObject", "url": "https://chinahospitalsguide.com/og-image.webp" }}
        }},
        "mainEntityOfPage": {{ "@type": "WebPage", "@id": "{article_url}" }}
    }}
    </script>
''')
        if t["need_breadcrumb"]:
            section = t["section"]
            section_url = f"https://chinahospitalsguide.com/{section.lower()}/"
            blocks.append(f'''
    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {{ "@type": "ListItem", "position": 1, "name": "Home", "item": "https://chinahospitalsguide.com/" }},
            {{ "@type": "ListItem", "position": 2, "name": "{section}", "item": "{section_url}" }},
            {{ "@type": "ListItem", "position": 3, "name": "{t["title"][:80]}" }}
        ]
    }}
    </script>
''')
        head_end = text.find("</head>")
        text = text[:head_end] + "\n" + "\n".join(blocks) + text[head_end:]
        with open(t["path"], "w") as fp: fp.write(text)
        success += 1
    except Exception as e:
        errors += 1
        print(f"  ERR {t['path']}: {e}")

print(f"\nDone: {success} files updated, {errors} errors")
```

## Pitfalls & gotchas

1. **Title field escaping**: if a page title contains a quote `"` or backslash `\`, the JSON-LD will break. The script above does NOT escape. For sites where titles can contain special characters (most static HTML titles), use `json.dumps()` instead of f-string interpolation:
   ```python
   import json
   article_data = {"@context": "https://schema.org", "@type": "Article", "headline": t["title"], ...}
   blocks.append(f'<script type="application/ld+json">{json.dumps(article_data, indent=4)}</script>')
   ```

2. **Idempotency**: re-running the script on already-covered files should be a no-op (the `if "Article" in all_types and "BreadcrumbList" in all_types: continue` check handles this). Verify by re-running inventory after.

3. **`<title>` extraction regex is naive**: it stops at the first `<` character, which is fine for well-formed HTML but breaks on pages with embedded `<` inside `<title>`. For robust extraction, use a proper HTML parser:
   ```python
   from html.parser import HTMLParser
   ```

4. **Don't forget to update `sitemap.xml`** if you create any new pages in the same batch — though this recipe doesn't create pages, only modifies existing ones, so sitemap is untouched.

5. **Backup-counting BEFORE the run**: always print "before" counts, do the run, print "after" counts, expect delta = number of files modified. If delta doesn't match, stop and audit.

## Verification after deploy

```bash
# On prod, sample-check a few formerly-0-schema files
for url in \
  "https://chinahospitalsguide.com/blog/jinan-respiratory-hospital-rankings-2026.html" \
  "https://chinahospitalsguide.com/news/2026-03-24-japan-china-proton-therapy.html" \
  "https://chinahospitalsguide.com/blog/ivf-china-2026-complete-guide.html"; do
  count=$(curl -s "$url" | grep -c '"BreadcrumbList"')
  echo "$url: BreadcrumbList occurrences = $count (expect ≥1)"
done
```

## When NOT to use this

- Site has <20 HTML pages — just edit each one by hand
- Site uses a static site generator (Hugo/Jekyll/Eleventy) where schema should be in the template, not in the rendered HTML — fix the template instead
- Schema is intentionally varied per page (e.g. some pages have FAQPage, others don't because they have no FAQ) — manually crafted schemas may be better