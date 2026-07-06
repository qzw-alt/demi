# Search Engine Fallback Recipes

When HN Algolia + NYT RSS aren't enough, use this fallback chain. Each engine has different rate-limit and content characteristics — the order below minimizes total time-to-result.

## Engine Comparison

| Engine | Best for | Limit | Risk |
|--------|----------|-------|------|
| DuckDuckGo HTML | Chinese topics, general news | ~5 queries / IP / session | Silent throttle; switch after that |
| Bing (HTML) | English tech, some Chinese | Generous but noisy SEO results | Top results are content farms |
| Brave Search | Anything | JS-heavy SPA — needs real browser | Raw curl returns shell only |
| SearX instances | Anything | Mostly behind Anubis bot-checks | Rarely useful from curl |

**Default rule**: HN + NYT first, DDG second (for Chinese/long-tail), Bing third (for cross-checking English), Brave/SearX only when the first three fail.

## Recipe 1: DuckDuckGo HTML (zh-CN friendly)

```python
import re, subprocess, urllib.parse, time

def ddg_search(query, max_results=10):
    """Single query. Returns list of clean snippets, or empty list if throttled."""
    url = f"https://html.duckduckgo.com/html/?q={urllib.parse.quote(query)}"
    result = subprocess.run(
        ["curl", "-sL",
         "-A", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
               "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
         url],
        capture_output=True, text=True, timeout=30
    )
    snippets = re.findall(r'class="result__snippet"[^>]*>(.*?)</a>',
                          result.stdout, flags=re.DOTALL)
    return [re.sub(r'<[^>]+>', '', s).strip() for s in snippets[:max_results]]

# Usage
results = ddg_search("AI 大模型 2026年7月")
for i, r in enumerate(results):
    print(f"[{i}] {r[:300]}")

# Critical: sleep between queries, stop after 4 queries total
time.sleep(2)
```

**Throttle signals**: First call returns 10 snippets, second 0-2, fifth returns empty page. Once you see the drop, **switch to Bing — don't retry DDG**.

## Recipe 2: Bing HTML scraping

```python
import re, subprocess, urllib.parse

def bing_search(query, lang="zh-CN", mkt="zh-CN"):
    """Returns list of clean text chunks near keywords."""
    url = (f"https://www.bing.com/search?q={urllib.parse.quote(query)}"
           f"&setlang={lang}&mkt={mkt}")
    result = subprocess.run(
        ["curl", "-sL",
         "-A", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
               "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
         "-H", f"Accept-Language: {lang},{lang.split('-')[0]};q=0.9,en;q=0.8",
         url],
        capture_output=True, text=True, timeout=30
    )
    html = result.stdout
    clean = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL)
    clean = re.sub(r'<style[^>]*>.*?</style>', '', clean, flags=re.DOTALL)
    clean = re.sub(r'</p>|</div>|</li>', ' ', clean)
    clean = re.sub(r'<[^>]+>', ' ', clean)
    clean = re.sub(r'&nbsp;|&amp;|&#0183;|&ensp;|&[a-z]+;', ' ', clean)
    clean = re.sub(r'\s+', ' ', clean)
    return clean

def chunks_near_keywords(text, keywords, max_per_kw=4):
    """Find 80-400 char chunks containing any keyword."""
    seen, out = set(), []
    for kw in keywords:
        idx = 0
        hits = 0
        while hits < max_per_kw:
            idx = text.find(kw, idx)
            if idx < 0:
                break
            chunk = text[max(0, idx-30):idx+280].strip()
            if (80 < len(chunk) < 400
                and chunk not in seen
                and not any(skip in chunk.lower()
                           for skip in ['skip to', 'pagination', 'open links',
                                        'accessibility', 'learn more'])):
                seen.add(chunk)
                out.append(chunk)
                hits += 1
            idx += 1
    return out

# Usage
text = bing_search("AI融资 2026年7月")
chunks = chunks_near_keywords(text, ["2026", "发布", "融资", "亿", "投资"])
for c in chunks[:10]:
    print(f"  • {c}")
```

**Censorship switch**: If you see "国内版 / 国际版" toggle + "增值电信业务经营许可证" footer, you're on the China-compliant shell with censored results. Force English locale:
```python
text = bing_search(query, lang="en-US", mkt="en-US")
```

## Recipe 3: Identifying SEO Content Farms (verification filter)

```python
FARM_DOMAINS = {
    "top10.com", "gemini-cnblog.com", "aimadetools.com",
    "aitoolreport.com", "best-ai-apps", "*.blogspot.com",
    "*.wordpress.com", "deepseek-v4.icu", "deepseek-ai.net",
}

def is_likely_farm(url_or_domain):
    """Returns True if source looks like an SEO/AI-mirror content farm."""
    d = url_or_domain.lower()
    return any(farm in d for farm in FARM_DOMAINS)

# Apply before quoting any specific number/date from snippet
if is_likely_farm(source_domain):
    # Either: drop the number, OR label it as unverified in the output
    pass
```

**Rule of thumb for daily briefings**: If a specific dollar amount appears in 3+ snippets from different domains, but **none of them cite Reuters/Bloomberg/官方公告**, it's a recycled number from an SEO farm — strip it.

## Rotation / Anti-Throttle

```python
import time, random

def search_with_rotation(queries):
    """Try DDG up to 4 queries, then fall back to Bing automatically."""
    engines = [
        ("ddg", ddg_search),
        ("bing", lambda q: chunks_near_keywords(bing_search(q),
                    ["2026", "发布", "亿", "launch", "release", "billion"], 5)),
    ]
    all_results = {}
    ddg_count = 0
    for q in queries:
        for engine_name, fn in engines:
            if engine_name == "ddg" and ddg_count >= 4:
                continue  # Don't push past DDG rate limit
            results = fn(q)
            if results:
                if engine_name == "ddg":
                    ddg_count += 1
                    time.sleep(2 + random.uniform(0, 1))  # Jitter
                all_results[q] = results
                break
    return all_results
```