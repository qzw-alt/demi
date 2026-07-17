# Primary-Source Direct Blog Strategy

When HN Algolia + NYT RSS + DDG/Bing surface a story, you need the **primary source** to verify specific numbers, dates, and quotes. This file covers the direct-blog / direct-RSS path: which company and research-lab sites return full article body via `curl -A "Mozilla/5.0"`, and which only return nav/footer shells.

## TL;DR

For AI/ML daily briefings, **go straight to the company news blog first** for any "Anthropic / OpenAI / Google / Meta / Microsoft / Hugging Face / Cerebras / Mistral / Cohere / DeepSeek / xAI" story. These are server-rendered or have SSR HTML; `curl` returns the full article body. This is faster AND more accurate than scraping Bing.

## Verified SSR (server-side rendered) blog/news endpoints

All return full article body via `curl -sL -A "Mozilla/5.0"`. Verified July 2026.

| Source | URL pattern | Notes |
|--------|-------------|-------|
| Anthropic News | `https://www.anthropic.com/news` + `/news/{slug}` | Per-article page has the full announcement, pricing tables, and system card references. Verified 2026-07-17 ✓ |
| OpenAI News | `https://openai.com/news/` | Index lists recent; individual pages return body for some slugs but `openai.com/index/previewing-gpt-5-6-sol/` returned "Enable JS" shell 2026-07-17 — JS-gated for some model-preview pages |
| Google AI Blog | `https://blog.google/technology/ai/` | Index sometimes JS, but individual `/technology/ai/{slug}/` works. **Watch for 404s**: `blog.google/products/google-ai/notebooklm-is-now-gemini-notebook/` was 404 on 2026-07-17 — slugs rot. Try `blog.google/` search or rely on HN title only. |
| Moonshot Kimi | `https://www.kimi.com/blog/{slug}` | Verified 2026-07-17 ✓ — full body for Kimi K3 announcement including architecture, MoE specs, benchmarks, pricing notes |
| Hugging Face Blog | `https://huggingface.co/blog` + `/blog/{slug}` | Plus RSS: `https://huggingface.co/blog/feed.xml` (returns clean `<title>` + `<pubDate>` for July 2026 posts) |
| Cerebras Blog | `https://www.cerebras.net/blog/` | Per-post page has full text |
| LM Studio Blog | `https://lmstudio.ai/blog/{slug}` | Verified 2026-07-17 ✓ — full body for Bionic announcement |
| Meta AI Blog | `https://ai.meta.com/blog/` | Server-rendered |
| Microsoft AI Blog | `https://blogs.microsoft.com/ai/` | |
| Mistral News | `https://mistral.ai/news/` | |
| xAI | `https://x.ai/news` (or blog) | |
| DeepSeek | `https://api-docs.deepseek.com/news` or blog | Smaller site, full body usually returned |
| Cohere Blog | `https://cohere.com/blog` | |
| Stability AI | `https://stability.ai/news` | |
| Fireworks AI | `https://fireworks.ai/` (homepage) | **Note (2026-07-17)**: `fireworks.ai/blog/{slug}` returns 404 — the "Series D + $1B ARR" announcement lives on the homepage hero banner, not a dedicated blog post. Fetch the homepage and grep for the announcement text. |
| TechCrunch (article) | `https://techcrunch.com/{YYYY}/{MM}/{DD}/{slug}/` | **Yes — full body returned via curl.** Counter to the old "JS-rendered" rule. The article text sits in `<p>` tags inside a `<div class="entry-content">` |
| BBC News (article) | `https://www.bbc.com/news/articles/{slug}` | Verified 2026-07-17 ✓ — full body for TSMC story; better curl-citizen than NYT/Reuters/Axios |
| BIS (central bank pubs) | `https://www.bis.org/publ/bisbull{N}.pdf` | PDF; first 500 chars of header give title/date/authors |
| Federal Register | `https://www.federalregister.gov/` | Full text of proposed/final rules |
| SEC EDGAR | `https://www.sec.gov/cgi-bin/browse-edgar` | Filings list, full text via `/Archives/...` |
| Company IR pages | `https://investors.{company}.com/` | Press releases — full text |

## Verifying before quoting

When a number appears in an HN title or DDG/Bing snippet, fetch the underlying primary-source blog for the actual quote. The pipeline:

```python
import re, subprocess

def fetch_article_body(url, max_chars=4000):
    """Fetch URL, return clean text body. Works for the SSR blogs above."""
    result = subprocess.run(
        ["curl", "-sL", "-A", "Mozilla/5.0",
         "--max-time", "20", url],
        capture_output=True, text=True, timeout=25
    )
    html = result.stdout
    # Strip script/style first (they contain noise, not content)
    html = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL)
    html = re.sub(r'<style[^>]*>.*?</style>', '', html, flags=re.DOTALL)
    # Drop all tags
    text = re.sub(r'<[^>]+>', ' ', html)
    # Decode common entities
    text = (text.replace('&nbsp;', ' ').replace('&amp;', '&')
                .replace('&#x27;', "'").replace('&#39;', "'")
                .replace('&quot;', '"').replace('&lt;', '<').replace('&gt;', '>'))
    text = re.sub(r'\s+', ' ', text).strip()
    # Truncate
    return text[:max_chars]
```

Then search within the body for the specific number/date/claim:

```python
body = fetch_article_body("https://www.anthropic.com/news/claude-sonnet-5")
# Look for: $2 per million input tokens, pricing, dates
for kw in ["$2 per million", "$10 per million", "August 31", "Sonnet 4.6", "Opus 4.8"]:
    idx = body.find(kw)
    if idx >= 0:
        print(f"FOUND '{kw}': ...{body[max(0,idx-50):idx+150]}...")
```

## Why direct-source first is faster than scraping

For a 6-section daily briefing:
- HN front page gives 5-10 candidate topics in one curl
- For each candidate, fetching the primary source takes ~5-10s and gives **verified primary-source numbers** (e.g. actual pricing, actual valuation, actual date)
- Compare to scraping Bing: 30s per query, mostly SEO farms, numbers must be cross-checked

Net: direct-source first → 5 minutes for 6 sections with verified numbers. Bing/DDG scraping → 15+ minutes for the same with lower confidence.

## Pitfalls

- **Don't trust company blogs for "neutral" framing** — they always spin positive. Use them for **specific facts** (numbers, dates, model names) but cross-check the "why it matters" framing against independent sources (HN comments, NYT, Reuters).
- **Some "news" pages are JS SPAs even when the index is SSR** — Anthropic `/news` index renders fine, but a few subpages are partial. If you get <500 chars of body, fall back to the Algolia `story_text` field for HN discussion or the Google cache URL.
- **Pricing pages change without notice** — always re-fetch the pricing section of a model announcement at briefing time; Anthropic's "introductory pricing until 8/31" framing is exactly the kind of time-bound detail that gets stale fast.
- **TechCrunch / TheVerge / Wired** are NOT always JS-rendered. TechCrunch's article pages returned full body in July 2026. TheVerge still returns shell — for TheVerge, use RSS (`/rss/index.xml`) or fall back to HN.
- **BIS Bulletin / Federal Register PDFs** are real PDFs; `head -c 500` gets you the title metadata. For full text, use `pdftotext` (`apt install poppler-utils`).
- **Don't ship a number from a snippet without primary-source confirmation** — the previous version of this skill already covered this in the "SEO farm" section. The direct-blog path is the **positive** corollary: primary source = verified, ship it.

## Workflow (for AI行业每日简报 specifically)

1. `curl -sL https://news.ycombinator.com/` → grab top 30 story titles + URLs (one curl, <1s)
2. `curl -sL https://huggingface.co/blog/feed.xml` → grab recent blog titles + pubDates (RSS, clean)
3. For each candidate story, fetch the primary source (company blog, press release) and extract the verified fact(s)
4. NYT RSS for cross-coverage on funding/regulation that HN under-indexes
5. Skip DDG/Bing unless you need a Chinese-source or long-tail topic
