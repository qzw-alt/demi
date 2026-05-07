# SEO Metadata Audit — 2026-05-02

## Scope
- 59 blog articles (`blog/*.html`, excluding `blog/index.html`)
- Repository: `/root/.hermes/workspace/chinahospitalsguide/`

## Coverage Before Injection

| Tag | Coverage | Gap |
|-----|----------|-----|
| `canonical` | 53/59 (90%) | 6 missing |
| `og:title` | 33/59 (56%) | 26 missing |
| `og:description` | 33/59 (56%) | 26 missing |
| `og:type=article` | 31/59 (53%) | 28 missing |
| `og:url` | 28/59 (47%) | 31 missing |
| `og:image` | 18/59 (31%) | 41 missing |
| `og:site_name` | **0/59 (0%)** | all missing |
| `twitter:card` | **5/59 (8%)** | 54 missing |
| `twitter:title/desc/image` | ~7% | most missing |
| `JSON-LD Article` | 31/59 (53%) | 28 missing |

## Key Findings

- `og-image.jpg` exists at repo root — use as universal fallback for og:image and twitter:image
- No `images/og/` directory — all images must use existing fallback
- 4 articles fully tagged (dental-implants, ivf-fertility-treatment, and 2 others)
- 6 articles missing canonical: best-cancer-hospitals, best-cardiac-surgery, cancer-treatment, china-medical-visa-guide, china-vs-usa-medical-costs, dental-tourism-china-2026

## Injection Strategy

- **og:image / twitter:image**: always use `https://chinahospitalsguide.com/og-image.jpg`
- **og:site_name**: always add `China Hospitals Guide`
- **twitter:image**: always use same fallback
- **canonical**: skip if already present
- **JSON-LD**: skip if Article schema already present

## Audit Script

```python
# Quick re-audit after injection
import csv, glob, re, os

blog_dir = "/root/.hermes/workspace/chinahospitalsguide/blog"
files = sorted(glob.glob(f"{blog_dir}/*.html"))
files = [f for f in files if "index.html" not in f]

results = []
for fpath in files:
    fname = os.path.basename(fpath).replace(".html", "")
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
    results.append({
        "file": f"blog/{fname}.html",
        "has_canonical": "yes" if re.search(r'<link rel="canonical"', content) else "no",
        "has_og_title": "yes" if re.search(r'<meta property="og:title"', content) else "no",
        "has_twitter_card": "yes" if re.search(r'<meta name="twitter:card"', content) else "no",
        "has_jsonld_article": "yes" if re.search(r'"@type"\s*:\s*"Article"', content) else "no",
        "has_og_site_name": "yes" if re.search(r'og:site_name', content) else "no",
    })

csv_path = "/root/.hermes/workspace/chinahospitalsguide/seo-audit.csv"
with open(csv_path, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=results[0].keys())
    writer.writeheader()
    writer.writerows(results)

for r in results:
    print(r)
```
