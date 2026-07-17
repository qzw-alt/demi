---
name: terminal-web-research
description: "Gather real-time web data (news, trends, stats) via terminal + curl to free APIs, when no web_search/browser toolset is available. Covers HN Algolia, NYT RSS, DuckDuckGo/Bing HTML scraping fallback chain, and source-verification discipline for daily briefings."
version: 1.4.0
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

**Pitfall — `query=A+OR+B+OR+C` returns 0–1 hits (validated 2026-07-16)**: Multi-OR queries in the Algolia `query` parameter are unreliable. `query=GPT+OR+Claude+OR+Gemini+OR+Llama+OR+DeepSeek&tags=story&numericFilters=created_at_i%3E{TS}` returned exactly 1 hit while the same query without `numericFilters` returned 25+. The combination of the OR operator with a date filter seems to defeat relevance scoring. **Fix**: split into separate single-keyword queries per topic/company (`query=Anthropic`, `query=OpenAI`, `query=DeepSeek`, `query=Meta+AI`, `query=Mistral`, `query=China+AI`) and dedupe hits by `objectID` in Python. This is slower but reliable, and per-company queries give much better category coverage for briefings anyway.

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
- **HN Front Page HTML** | `https://news.ycombinator.com/` | HTML | **Cheapest "what's hot" signal** — one curl returns ~30 story titles. **Story-line regex (validated 2026-07-17):** `class="athing submission" id="(\d+)">.*?class="titleline"><a href="([^"]+)">([^<]+)</a>` — must include the `submission` class. The simpler `class="athing"[^>]*id="(\d+)"` regex returns 0 hits because HN wraps every story in `<tr class="athing submission" id="X">`. Points live in a separate span: `id="score_{oid}">(\d+) points`. **Use the front page for "what's hot RIGHT now"** — it surfaces stories the Algolia relevance API misses (e.g. 2026-07-17 Kimi K3 was #1 at 1123pts but invisible to per-keyword `search` re-queries). |
| **HN Comment Pages** | `https://news.ycombinator.com/item?id={ID}` | HTML | Returns full comment threads — useful for extracting community context/discussion of a trending item. Title appears in `<a>` near the top. |
| **HuggingFace Blog RSS** | `https://huggingface.co/blog/feed.xml` | XML/RSS | Returns clean `<title>` + `<pubDate>` for all HF posts. Best signal for "what shipped in open-source AI this week." |
| **Primary-source company blogs** | `https://www.anthropic.com/news/{slug}`, `https://huggingface.co/blog/{slug}`, `https://www.cerebras.net/blog/`, `https://blog.google/technology/ai/`, `https://openai.com/news/`, `https://mistral.ai/news/` | SSR HTML | **Go here FIRST for any "Anthropic / OpenAI / Google / HF / Cerebras" story.** Full article body via `curl -A "Mozilla/5.0"`. Faster AND more accurate than scraping Bing. See `references/primary-source-blogs.md` for the full list and parsing pattern. |
| **TechCrunch article pages** | `https://techcrunch.com/{YYYY}/{MM}/{DD}/{slug}/` | SSR HTML | **Returns full body via curl as of 2026** — article text in `<p>` tags inside `<div class="entry-content">`. Earlier "JS-rendered" advice was outdated. |
| HN Front Page (unofficial API) | `https://hacker-news.firebaseio.com/v0/topstories.json` | JSON array of IDs | Then fetch each item: `https://hacker-news.firebaseio.com/v0/item/{ID}.json` |
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

When HN + NYT + direct-source company blogs alone aren't enough (e.g. Chinese-language news, niche topics, specific company news you can't find on the company's own site), use this ordered chain. Each engine has a different failure mode — know when to switch.

| # | Engine | URL pattern | Watch out for |
|---|--------|-------------|---------------|
| 0 | **Primary-source company blog** | `https://www.anthropic.com/news/{slug}` etc. | **Check this first** before any search engine. For AI labs, model announcements, and product launches, the company blog has the verified numbers, dates, and pricing. See `references/primary-source-blogs.md`. |
| 1 | HN Algolia | `https://hn.algolia.com/api/v1/search_by_date?query=...` | English-only, dev-heavy |
| 2 | HN Front Page HTML | `https://news.ycombinator.com/` | One curl, no query construction, ~30 trending titles |
| 3 | NYT RSS | `https://rss.nytimes.com/services/xml/rss/nyt/Technology.xml` | US-centric, Tech section only |
| 4 | DuckDuckGo HTML | `https://html.duckduckgo.com/html/?q=ENCODED` | **Effectively dead from curl as of 2026** — returns 0 results on most queries even with realistic User-Agent. Don't waste turns retrying; skip straight to Bing. |
| 5 | Bing | `https://www.bing.com/search?q=ENCODED&setlang=zh-CN&mkt=zh-CN` | Returns noisy SEO content farms; strip `<script>`, `<style>`, all tags, search for keyword proximity |
| 6 | Brave Search | `https://search.brave.com/search?q=ENCODED` | JS-heavy SPA; raw curl returns shell without results — needs a real browser |
| 7 | SearX instances | `https://searx.be/search?q=...&format=json` | Most public instances are behind bot-checks (Anubis/Cloudflare); rarely useful from curl |
| 8 | TheVerge / Wired | `https://www.theverge.com/` etc. | **JS-rendered SPAs** — `curl -A "Mozilla/5.0"` returns only nav/footer HTML. Use their RSS feeds (`/rss/index.xml`) where available. TechCrunch is the exception — its article pages DO return full body via curl. |

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
- **TechCrunch article pages DO return full body via curl** (as of 2026) — earlier "JS-rendered" advice was outdated. The article text is in `<p>` tags inside `<div class="entry-content">`. TheVerge and Wired are still JS-only; use their RSS feeds.
- **TheVerge / Wired pages are JS-rendered** — `curl` returns nav/footer HTML only. Don't burn 3 turns trying to parse them; go to their RSS feeds (`/rss/index.xml`).
- **Major news article pages are JS-gated from curl in 2026** (validated 2026-07-17): NYT article URLs (e.g. `nytimes.com/2026/07/16/business/...`), Reuters article URLs, Axios article URLs, FT article URLs, TheVerge article URLs — all return either "Please enable JS and disable any ad blocker" or Cloudflare "Attention Required!" shells via `curl -A "Mozilla/5.0"`. Web Archive (`web.archive.org`) also returned `429 Too Many Requests` for these. **For these sources, the article URL is only usable as a *citation* — you cannot fetch the body.** Fall back to the HN title (already editorial-summary-grade), or use the publication's RSS / news listing page where headlines alone are enough for a briefing.
- **Company blogs that DO return full body via curl** (verified 2026-07-17): `anthropic.com/news/{slug}`, `kimi.com/blog/{slug}` (Moonshot), `fireworks.ai/` homepage, `lmstudio.ai/blog/{slug}`, `blog.google/technology/ai/{slug}` (when slug is right — slugs rot). `fireworks.ai/blog/{slug}` 404s — announcements live on the homepage. **Always curl-test the specific URL before quoting a number from it.**
- **Subagent fabrication risk**: When delegating research to subagents, their summaries are self-reports. If the tool_trace is empty, the results may be LLM-generated fabrications. Always re-fetch source URLs yourself.
- **DDG HTML is effectively dead from curl (2026)**: the endpoint returns 0 snippets even with realistic User-Agents. The "rate-limits after 5 queries" advice is stale. Don't waste turns; skip to Bing.
- **Bing in zh-CN returns gov-blocked rebrand pages**: If you see "国内版 / 国际版" toggle and "增值电信业务经营许可证" footer, you're being served the China-compliant Bing shell with censored results. Switch to `setlang=en-US&mkt=en-US` for tech/AI news.
- **Bing returns the same SEO farms as DDG for hot queries**: "AI funding July 2026" → top 5 results are listicle sites recycling the same dollar amounts. Cross-check via HN before quoting any specific number.
- **SearX public instances are mostly dead**: As of 2026, Anubis bot-checks have killed most public instances for unauthenticated curl. Don't waste time trying more than one.
- **The "$X billion" in snippet ≠ verified fact**: SEO farms recycle the same number with no sourcing. If only SEO sites have the number, the number doesn't exist.
- **Company blogs are SSR but spin positive** — use them for specific numbers/dates/model names, but cross-check the "why it matters" framing against independent sources (HN comments, NYT, Reuters).
- **The "AI行业每日简报" format spec (validated 2026-07-16)**: When the user requests this exact product, deliver with title `# AI行业每日简报 · {weekday}` (compute weekday from `datetime.now().strftime('%A')` translated to Chinese: 周一/二/三/四/五/六/日). Six sections in order: 大模型动态 (2–3 items), 行业融资 (1–2), 产品发布 (1–2), 政策监管 (1), 本周关注 (2–3 trends), 本周数据 (1–2 numbers). Each item is **one sentence** with emoji prefix. Specific numbers must be HN-verified (≥10 pts OR primary-source URL) — never quote SEO-farm numbers. Keep total under 500 Chinese characters of prose. See `references/ai-briefing-format.md` for the worked template.

- **Pricing pages change without notice** — Anthropic's "introductory pricing until 8/31" is exactly the kind of time-bound detail that gets stale fast; re-fetch pricing at briefing time.

- **Cron-running this skill end-to-end**: The worked example's `cd /tmp/briefing && cmd & cmd & cmd & wait` pattern **breaks in the Hermes foreground-only terminal** — `&` backgrounding is rejected. Use either `terminal(background=true)` for the long-running curl batch OR run curls sequentially in one `terminal()` call (5–6 curls take ~10s total, well under the 60s timeout). Also: `mkdir -p /tmp/x && cd /tmp/x` fails silently if `/tmp/x` doesn't exist (separate command, separate session) — run them in the same command line OR `write_file` a marker first. Always check `pwd` before assuming `ls` will find your output.

## Linked References

- `references/hn-nyt-api-snippets.md` — copy-paste Python pipelines for HN Algolia and NYT RSS (no scraping needed)
- `references/search-engine-fallback.md` — extended scraping recipes for DuckDuckGo HTML, Bing, Brave, SearX with rotation/anti-throttle discipline
- `references/daily-ai-briefing-pipeline.md` — turnkey recipe for the "AI行业每日简报" pattern: 5 parallel HN queries by category, date-filter timestamp math, points-threshold ranking, NYT cross-coverage, and a worked example with verified 2026-07-09 output
- `references/primary-source-blogs.md` — **start here for any "Anthropic / OpenAI / Google / HF / Cerebras / Mistral" story**: SSR blog endpoints that return full article body via `curl -A "Mozilla/5.0"`, with a Python parsing pattern and a "fetch the primary source to verify the number" workflow. Promoted to step 0 of the fallback chain.
- `references/ai-briefing-format.md` — the exact "AI行业每日简报" format spec (6 sections, one-sentence-per-item, emoji, ≤500 chars, HN-verified numbers only), with a worked template and the 2026-07-16 example. Load when the user asks for a daily AI briefing.