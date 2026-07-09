# Daily AI/Tech Briefing Pipeline

A copy-paste recipe for generating the kind of "AI行业每日简报" the user asks for, when you only have `terminal` + `curl` (no web_search tool).

Validated against HN Algolia data on 2026-07-09.

## Step 1 — Compute the date filter

Pick your window. For "本周" / "this week", use 7 days. For "今日", use 1 day.

```bash
TS=$(python3 -c "import datetime; print(int((datetime.datetime.utcnow() - datetime.timedelta(days=7)).timestamp()))")
echo "Filter: created_at_i > ${TS}"
```

**Sanity check**: run `python3 -c "import datetime; print(datetime.datetime.utcfromtimestamp(${TS}))"` to confirm the timestamp decodes to the date you expect. Easy mistakes: local time vs UTC, days vs hours.

## Step 2 — Parallel batch of narrow HN queries

Don't run one broad `query=AI`. HN Algolia relevance scoring penalizes long queries; narrow queries surface category leaders cleanly. Run these in parallel (single Hermes turn, multiple `terminal()` calls):

```bash
# Models & research
curl -sL "https://hn.algolia.com/api/v1/search?query=GPT+OR+Claude+OR+Gemini+OR+Llama&tags=story&numericFilters=created_at_i%3E${TS}&hitsPerPage=25"

# Funding / capital
curl -sL "https://hn.algolia.com/api/v1/search?query=AI+raise+OR+funding+OR+Series+OR+valuation+OR+billion&tags=story&numericFilters=created_at_i%3E${TS}&hitsPerPage=25"

# Regulation / policy
curl -sL "https://hn.algolia.com/api/v1/search?query=AI+regulation+OR+law+OR+policy+OR+EU+AI+Act&tags=story&numericFilters=created_at_i%3E${TS}&hitsPerPage=25"

# Product launches
curl -sL "https://hn.algolia.com/api/v1/search?query=Launch+HN+OR+Show+HN&tags=story&numericFilters=created_at_i%3E${TS}&hitsPerPage=25&numericFilters=created_at_i%3E${TS}"

# Geopolitics (US/China/EU)
curl -sL "https://hn.algolia.com/api/v1/search?query=US+China+AI+OR+export+control+OR+sanctions&tags=story&numericFilters=created_at_i%3E${TS}&hitsPerPage=25"
```

5 parallel curls ≈ 2-3 seconds. Each returns ~15-25 hits with `points` (popularity), `created_at`, `title`, `url`.

## Step 3 — Extract and rank

Python one-liner to dump all hits as TSV:

```python
import json, subprocess, sys
queries = ["GPT OR Claude OR Gemini", "AI raise OR funding", "AI regulation", "Launch HN", "US China AI"]
seen = set()
for q in queries:
    url = f"https://hn.algolia.com/api/v1/search?query={q}&tags=story&numericFilters=created_at_i%3E${TS}&hitsPerPage=25"
    data = json.loads(subprocess.run(["curl","-sL",url], capture_output=True, text=True, timeout=15).stdout)
    for h in data.get("hits", []):
        key = h.get("objectID", h.get("title",""))
        if key in seen: continue
        seen.add(key)
        print(f"{h.get('created_at','')[:10]}\t{h.get('points',0)}\t{h.get('title','')}")
```

Sort by `points` desc to get "what the community cared about", then by date for "what just dropped". For a briefing, you want both: top-by-points (signal) + recent (recency).

## Step 4 — Source verification gate

Before quoting any specific number from an HN title alone:
1. HN titles are **editor-submitted** — usually accurate, but short and sometimes clickbait
2. Click the underlying URL for the full story if a number is dramatic ($X billion, Y% growth)
3. If the HN title references a story you can't verify via another endpoint (NYT RSS, Wikipedia API), flag it as "per HN, unverified by primary source"

For a 6-section briefing with ~12 items, you typically need 8-10 verified HN items + 2-3 from NYT RSS for cross-coverage (especially funding rounds and policy — HN under-indexes these).

## NYT RSS for cross-coverage

```python
import subprocess, xml.etree.ElementTree as ET
xml_data = subprocess.run(
    ["curl","-sL","--max-time","15","https://rss.nytimes.com/services/xml/rss/nyt/Technology.xml"],
    capture_output=True, text=True, timeout=20
).stdout
root = ET.fromstring(xml_data)
for item in root.findall(".//item")[:15]:
    title = item.find("title").text
    link = item.find("link").text
    desc = (item.find("description").text or "")[:150]
    print(f"- {title}\n  {link}\n  {desc}")
```

NYT Tech RSS covers funding, regulation, executive moves that HN misses. Run it second.

## Pitfalls unique to daily briefings

- **"Today" is broader than you think**: include items from the last 7 days, not just "today". A "本周关注" section needs 2-3 day-old material, not all 24h.
- **Title-only context**: when you only have the HN title + points, you often don't know WHICH model release or WHICH country. If the title is ambiguous (e.g. "China launches new AI model"), accept the ambiguity in the briefing or skip the item — don't guess specifics.
- **Limit points threshold**: HN items with <5 points are often low-quality. For a polished briefing, require points ≥ 10 OR date within last 48h.
- **Bias toward US/English sources**: HN is heavily US/EN. For Chinese AI news specifically, this pipeline will under-cover. Cross-reference with NYT + accept the gap, or escalate to a Chinese-source skill.
- **Cron-running this pipeline**: it's deterministic and cheap (~10-15s total), safe to run daily. Cache results in a file keyed by date to avoid re-running within the same day.

## Worked example output (2026-07-09)

Sample topics that surfaced cleanly from this pipeline:
- "In San Francisco, Some Home Sellers Now Ask for OpenAI or Anthropic Stock" (7/8)
- "Anthropic says Alibaba illicitly extracted Claude AI model capabilities" (6/24, 813pts)
- "Microsoft joins AI cost-cutting trend by relying more on its own models" (7/8)
- "EU AI Act becomes applicable Aug 2: an engineering checklist" (7/7)
- "Beijing is looking at curbing overseas access to China's top AI models" (7/7)
- "Show HN: Microsoft releases Flint, a visualization language for AI agents" (7/8, 188pts)

Mapped to a 6-section briefing: 大模型 (Anthropic/Alibaba, Google限制Meta), 融资 (Uber/Microsoft $25B), 产品 (Flint), 政策 (EU AI Act 8/2), 本周关注 (开源 vs 闭源, 中美AI战), 数据 ($700B + 56% zero return).