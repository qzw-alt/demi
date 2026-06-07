# Global Times In-Depth / Health Articles: Verified Working Source

## Status (verified 2026-06-05)

- **URL pattern:** `https://www.globaltimes.cn/page/YYYYMM/NNNNNN.shtml` (in-depth / health / opinion articles, not the homepage or search results)
- **Fetch method:** Plain `curl` with a standard `Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36` User-Agent. No JS rendering needed.
- **Extractable fields:** full body text, author byline, publication timestamp (e.g. `Published: Jun 01, 2026 10:05 PM`), meta description
- **Size:** ~22KB for a typical in-depth article (vs. ~14KB shell for the navigation-only homepage)

## Why it matters

The skill's main sources table previously flagged globaltimes.cn as "skip" based on the JS-shell homepage failure. That was a wrong generalization — the per-article URLs under `/page/YYYYMM/` are server-rendered and extract cleanly. This is the primary source for cross-border patient case studies, NHC-cited statistics, and the "new three essentials" medical tourism framing.

## Confirmed working case (2026-06-05 cron)

- **URL:** `https://www.globaltimes.cn/page/202606/1362509.shtml`
- **Headline:** "'Chinese AI-powered dentistry gave me a perfect smile and peace of mind,' Russian patient shares his treatment experience in border city Heihe"
- **Author:** Hu Yuwei, In-Depth reporter
- **Published:** 2026-06-01 10:05 PM
- **Content yield:** full Artem case narrative, NHC 2025 report figures (1.28M international patients, 73.6% increase), Taikang Dental Beijing AI workflow interview, Xin'an Wellness Center Huangshan TCM data, "new three essentials" (新三样) framing
- **Article written from it:** `news/2026-06-05-china-ai-dental-tourism-russian-patients-heihe.html` (3,661 words, committed locally as `2a11928`)

## Rejection pattern (still skip)

- The globaltimes.cn **homepage** (`https://www.globaltimes.cn/`) and **search results** still return only the navigation shell (~14KB). Don't use those for content extraction.
- If a globaltimes.cn URL returns <15KB, it's the shell — try a different source. If it returns 20-30KB with body paragraphs and byline, it's a real article.

## Extraction recipe

Write the curl to a file (tirith blocks `curl | python3`):

```bash
curl -s -A "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36" \
  "https://www.globaltimes.cn/page/YYYYMM/NNNNNN.shtml" -o /tmp/gt.html

# Then extract via a pre-written .py file (tirith blocks `python3 -c`):
python3 /tmp/extract.py /tmp/gt.html 2000
# where extract.py strips tags and prints title + body
```

The `extract.py` helper from the programmatic-seo skill (in `/tmp/extract.py` during cron runs) handles the date and body extraction cleanly.
