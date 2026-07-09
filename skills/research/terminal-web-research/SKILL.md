---
name: terminal-web-research
description: "Gather real-time web data (news, trends, stats) via terminal + curl to free APIs, when no web_search/browser toolset is available. Covers HN Algolia, NYT RSS, DuckDuckGo/Bing HTML scraping fallback chain, and source-verification discipline for daily briefings."
version: 1.1.0
metadata:
  hermes:
    tags: [web, research, news, curl, api, rss, terminal, daily-briefing, source-verification]
---

# Terminal Web Research

When `web_search` or `web` toolset is unavailable, use `terminal` + `curl` to hit free public APIs and RSS feeds. This skill covers reliable, zero-auth endpoints, the search-engine fallback chain when HN+NYT aren't enough, and how to verify what you actually scraped.

## When to Use

- You need real-time news, trends, or data but lack the `web_search` tool
- The `delegate_task` with `toolsets=["web"]` returns fabricated-looking results (empty tool_trace) — always verify subagent claims by fetching the source URL yourself
- You need structured data (JSON/XML) that's faster to parse than browsing
- You're writing a daily/weekly briefing and need news across multiple topics/languages

## Reliable Free Endpoints

### 1. Hacker News Algolia API (JSON)

Search for recent stories by keyword, sorted by date:

```bash
# Recent stories by date (best for news)
curl -sL "https://hn.algolia.com/api/v1/search_by_date?query=KEYWORD&tags=story&hitsPerPage=20"

# Top stories by points (best for finding what's trending)
curl -sL "https://hn.algolia.com/api/v1/search?query=KEYWORD&tags=story&hitsPerPage=20"
```

**Key differences:**
- `search_by_date` — sorted by `created_at` descending. Use for "what happened in the past 24h."
- `search` — sorted by relevance (points-weighted). Use for "what's the most important on this topic."

**Filtering by date with `numericFilters`** — critical for "last 24h / 7 days" briefings:
```bash
# Unix timestamp for "N days ago" — compute in Python first
TS=$(python3 -c "import datetime; print(int((datetime.datetime.utcnow() - datetime.timedelta(days=7)).timestamp()))")
curl -sL "https://hn.algolia.com/api/v1/search?query=AI&tags=story&numericFilters=created_at_i%3E${TS}&hitsPerPage=30"
```

**Pitfall — timestamp URL-encoding**: the `>` MUST be URL-encoded as `%3E` inside `numericFilters`, not `&gt;` or raw `>`. Use `%3E` (works in curl) or the equivalent `&numericFilters=created_at_i>${TS}` (works in browsers). Verify by checking the response has any hits; if 0, your filter is wrong (or your timestamp math is off — always sanity-check `int(datetime.datetime(Y,M,D).timestamp())` for the date you want).

**Pagination**: Use `&page=N` (0-indexed).

**Rate limit**: Generous — no API key needed. Up to ~10 req/s without issues.

**Parsing pattern:**
```python
import json, sys
data = json.load(sys.stdin)
for h in data.get('hits', []):
    d = h.get('created_at','')[:10]
    t = h.get('title','')
    p = h.get('points',0)    # only in search(), NOT search_by_date
    u = h.get('url','') or h.get('story_url','') or ''
    print(f'{d} | {t} [{p}pts]')
```

**Tip for daily briefings**: Run a parallel batch of narrow queries (`AI model`, `AI funding`, `AI regulation`, `Anthropic`, `OpenAI`) with the same date filter — HN Algolia is fast enough that 5 parallel curls take <3s and give you much better category coverage than one broad `query=AI`. Combine with `search` (relevance/points-weighted) + `search_by_date` (chronological) for both "what's hot" and "what just dropped".

### 2. NYT Technology RSS Feed (XML)

The NYT RSS feed is freely accessible and carries the day's top tech/AI stories:

```bash
curl -sL "https://rss.nytimes.com/services/xml/rss/nyt/Technology.xml"
```

**Filtering for AI stories:**
```python
import xml.etree.ElementTree as ET
root = ET.fromstring(data)
for item in root.findall('.//item'):
    title = item.find('title').text
    desc = item.find('description')
    pubDate = item.find('pubDate')
    link = item.find('link')
    if 'AI' in title or 'ai' in title.lower():
        print(f'[{pubDate.text[:16]}] {title}')
        print(f'  {link.text}')
        print(f'  {desc.text[:200]}')
```

**No rate limit on RSS** — it's designed for polling.

### 3. Other Free Endpoints to Try

| Source | URL Pattern | Format | Notes |
|--------|-------------|--------|-------|
| HN Front Page (unofficial) | `https://hacker-news.firebaseio.com/v0/topstories.json` | JSON array of IDs | Then fetch each item: `https://hacker-news.firebaseio.com/v0/item/{ID}.json` |
| GitHub Trending | `curl -sL https://api.github.com/search/repositories?q=KEYWORD+created:>YYYY-MM-DD&sort=stars` | JSON | Needs `Accept: application/vnd.github.v3+json` header |
| Wikipedia | `https://en.wikipedia.org/api/rest_v1/page/summary/TITLE` | JSON | No auth needed |
| Reddit (JSON) | `https://www.reddit.com/r/KEYWORD/hot.json` | JSON | Append `?limit=25` |
| NewsAPI (needs key) | `https://newsapi.org/v2/everything?q=KEYWORD&apiKey=demo` | JSON | `demo` key may work with limits |

## Workflow for Daily Briefing

A proven sequence for generating a news briefing:

1. **Search HN for topic + date**: `search_by_date?query=AI+KEYWORD&tags=story&hitsPerPage=20` — covers startup/tech news
2. **Fetch NYT Tech RSS**: Covers broader tech industry stories (funding, regulation, product launches)
3. **Cross-reference**: HN tends to be more technical/developer-focused; NYT covers business/regulation/policy angles
4. **Verify**: Always check that the subagent actually made tool calls (tool_trace non-empty). If tool_trace is empty, results may be fabricated — re-verify by fetching the source URL

## Search Engine Fallback Chain

When HN + NYT alone aren't enough (e.g. Chinese-language news, niche topics, specific company news), use this ordered chain. Each engine has a different failure mode — know when to switch.

| # | Engine | URL pattern | Watch out for |
|---|--------|-------------|---------------|
| 1 | HN Algolia | `https://hn.algolia.com/api/v1/search_by_date?query=...` | English-only, dev-heavy |
| 2 | NYT RSS | `https://rss.nytimes.com/services/xml/rss/nyt/Technology.xml` | US-centric, Tech section only |
| 3 | DuckDuckGo HTML | `https://html.duckduckgo.com/html/?q=ENCODED` | **Effectively dead from curl as of 2026** — returns 0 results on most queries even with realistic User-Agent. Don't waste turns retrying; skip straight to Bing. |
| 4 | Bing | `https://www.bing.com/search?q=ENCODED&setlang=zh-CN&mkt=zh-CN` | Returns noisy SEO content farms; strip `<script>`, `<style>`, all tags, search for keyword proximity |
| 5 | Brave Search | `https://search.brave.com/search?q=ENCODED` | JS-heavy SPA; raw curl returns shell without results — needs a real browser |
| 6 | SearX instances | `https://searx.be/search?q=...&format=json` | Most public instances are behind bot-checks (Anubis/Cloudflare); rarely useful from curl |
| 7 | TechCrunch / TheVerge / Wired | `https://techcrunch.com/category/artificial-intelligence/` etc. | **JS-rendered SPAs** — `curl -A "Mozilla/5.0"` returns only nav/footer HTML, no article titles or content. Use their RSS feeds instead (`/feed/`, `/rss`) where available. |

**DuckDuckGo HTML reality check (2026)**: DDG HTML returned **0 snippets on every query** in a recent briefing session, even with `Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 Version/17.0 Safari/605.1.15` User-Agent and a 30s timeout. The earlier "rate-limits hard after ~5 queries" advice is now outdated — the endpoint appears fully JS-gated or IP-blocked from curl. Don't retry, don't sleep-then-retry, just **skip to Bing immediately** for the same query.

**Rotation discipline**: When switching engines, change the query string format too (not just the URL host). DDG and Bing both have separate rate-limit buckets per (host, query). After each successful Bing response, add `time.sleep(2)` before the next query. If Bing returns 0 relevant results on a query that should yield hits, **try a tighter query** (more specific keywords, quoted phrases) before giving up — Bing loves to return generic SEO pages for broad queries.

**DuckDuckGo HTML parsing pattern** — works only if you stay under rate limit:
```python
import re, urllib.parse, subprocess
q = urllib.parse.quote("AI融资 2026年7月")
html = subprocess.run(
    ["curl", "-sL", "-A", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 Version/17.0 Safari/605.1.15",
     f"https://html.duckduckgo.com/html/?q={q}"],
    capture_output=True, text=True, timeout=30).stdout
snippets = re.findall(r'class="result__snippet"[^>]*>(.*?)</a>', html, flags=re.DOTALL)
for s in snippets[:10]:
    print(re.sub(r'<[^>]+>', '', s).strip()[:300])
```

**Bing parsing pattern** — Bing wraps results differently than DDG:
```python
clean = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL)
clean = re.sub(r'<style[^>]*>.*?</style>', '', clean, flags=re.DOTALL)
clean = re.sub(r'</p>|</div>|</li>', ' ', clean)
clean = re.sub(r'<[^>]+>', ' ', clean)
clean = re.sub(r'&nbsp;|&amp;|&#0183;|&ensp;', ' ', clean)
clean = re.sub(r'\s+', ' ', clean)
# Then grep around keywords for 80–400 char chunks
```

**Rotation discipline**: After each successful DDG response, add `time.sleep(2)` before the next query. If you get 0 snippets on a query that should return results, **switch to Bing immediately** — don't retry DDG, you'll be throttled for hours.

## Source Verification Discipline (CRITICAL)

**The trap**: When scraping Bing/DDG for "AI融资 2026年7月" or similar hot-topic Chinese queries, the top results are **SEO content farms and AI mirror sites** (e.g. `gemini-cnblog.com`, `top10.com`, `aimadetools.com`). They confidently state specific dollar amounts, dates, and company actions — but cite no primary source.

**Symptoms you've been fooled**:
- Result domain is `*.blogspot.com`, `gemini-cnblog.com`, `*.icu`, or generic listicle sites
- The same dollar amount (e.g. "$965 billion") appears verbatim across 5+ different sites
- No link to Reuters/Bloomberg/官方公告/SEC filing
- Date in snippet uses future-tense framing ("expected to", "预计")

**Required behavior**:
1. **Never quote a specific number, date, or acquisition from search snippets alone.** Strip the number, keep only the directional claim.
2. Add a `> ⚠️ 重要提示` block at the top of any briefing that uses these engines, stating which items are unverified.
3. If the user asks for "本日数据" or "数字要具体" while you're stuck with only SEO-source data, **explicitly downgrade**: use ranges ("十亿美元级"), directions ("继续上行"), or omit the number entirely.
4. Cross-checking via HN/NYT is the minimum bar. If HN/NYT don't carry the story, it's almost certainly not newsworthy enough to quote specific numbers.

## Pitfalls

- **search_by_date does NOT return points** — use `search` endpoint when you need popularity scores
- **HN API returns old stories** mixed with new ones in `search` mode; always prefer `search_by_date` for timeliness, OR combine `search` + `numericFilters=created_at_i>{TS}` to get recent + relevance-ranked
- **`numericFilters=created_at_i>{TS}` gotcha**: TS is **Unix seconds** (not ms), must be **URL-encoded `%3E`** not raw `>`, and must be the **UTC** timestamp. Easy off-by-one mistakes: using `datetime.datetime.now()` instead of `datetime.datetime.utcnow()` adds hours; using `.timestamp()` on a naive local datetime silently uses local TZ. Always sanity-check the result count: 0 hits on a broad query means your filter is wrong, not that there's no news.
- **NYT RSS only covers Tech section** — won't include AI stories filed under Business, Science, or Politics
- **RSS items have no `points`/score** — all articles are equally weighted
- **No JS rendering** — these are static JSON/XML APIs; they won't help with SPAs or client-rendered pages
- **TechCrunch / TheVerge / Wired article pages are JS-rendered** — `curl` returns nav/footer HTML only. Don't burn 3 turns trying to parse them; go straight to their RSS feeds (`/feed`, `/rss`) or fall back to HN Algolia for the same stories.
- **Subagent fabrication risk**: When delegating research to subagents, their summaries are self-reports. If the tool_trace is empty, the results may be LLM-generated fabrications. Always re-fetch source URLs yourself.
- **DDG HTML is effectively dead from curl (2026)**: the endpoint returns 0 snippets even with realistic User-Agents. The "rate-limits after 5 queries" advice is stale. Don't waste turns; skip to Bing.
- **Bing in zh-CN returns gov-blocked rebrand pages**: If you see "国内版 / 国际版" toggle and "增值电信业务经营许可证" footer, you're being served the China-compliant Bing shell with censored results. Switch to `setlang=en-US&mkt=en-US` for tech/AI news.
- **Bing returns the same SEO farms as DDG for hot queries**: "AI funding July 2026" → top 5 results are listicle sites recycling the same dollar amounts. Cross-check via HN before quoting any specific number.
- **SearX public instances are mostly dead**: As of 2026, Anubis bot-checks have killed most public instances for unauthenticated curl. Don't waste time trying more than one.
- **The "$X billion" in snippet ≠ verified fact**: SEO farms recycle the same number with no sourcing. If only SEO sites have the number, the number doesn't exist.

## Linked References

- `references/hn-nyt-api-snippets.md` — copy-paste Python pipelines for HN Algolia and NYT RSS (no scraping needed)
- `references/search-engine-fallback.md` — extended scraping recipes for DuckDuckGo HTML, Bing, Brave, SearX with rotation/anti-throttle discipline
- `references/daily-ai-briefing-pipeline.md` — turnkey recipe for the "AI行业每日简报" pattern: 5 parallel HN queries by category, date-filter timestamp math, points-threshold ranking, NYT cross-coverage, and a worked example with verified 2026-07-09 output