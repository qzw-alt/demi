---
name: terminal-web-research
description: "Gather real-time web data (news, trends, stats) via terminal + curl to free APIs, when no web_search/browser toolset is available. Covers HN Algolia, NYT RSS, and other zero-auth endpoints."
version: 1.0.0
metadata:
  hermes:
    tags: [web, research, news, curl, api, rss, terminal]
---

# Terminal Web Research

When `web_search` or `web` toolset is unavailable, use `terminal` + `curl` to hit free public APIs and RSS feeds. This skill covers reliable, zero-auth endpoints and how to parse their output.

## When to Use

- You need real-time news, trends, or data but lack the `web_search` tool
- The `delegate_task` with `toolsets=["web"]` returns fabricated-looking results (empty tool_trace) — always verify subagent claims by fetching the source URL yourself
- You need structured data (JSON/XML) that's faster to parse than browsing

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

## Pitfalls

- **search_by_date does NOT return points** — use `search` endpoint when you need popularity scores
- **HN API returns old stories** mixed with new ones in `search` mode; always prefer `search_by_date` for timeliness
- **NYT RSS only covers Tech section** — won't include AI stories filed under Business, Science, or Politics
- **RSS items have no `points`/score** — all articles are equally weighted
- **No JS rendering** — these are static JSON/XML APIs; they won't help with SPAs or client-rendered pages
- **Subagent fabrication risk**: When delegating research to subagents, their summaries are self-reports. If the tool_trace is empty, the results may be LLM-generated fabrications. Always re-fetch source URLs yourself.
