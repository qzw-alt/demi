# HN Algolia API Quick Reference

## Endpoints

### Date-sorted search (for "what happened today")
```
GET https://hn.algolia.com/api/v1/search_by_date?query={keywords}&tags=story&hitsPerPage={N}
```
- Results sorted by `created_at` descending
- Does NOT return `points` field
- Best for: recent news, today's updates

### Relevance-sorted search (for "most important")
```
GET https://hn.algolia.com/api/v1/search?query={keywords}&tags=story&hitsPerPage={N}
```
- Results sorted by relevance (points-weighted)
- Returns `points` field
- Best for: top stories on a topic

### Advanced numeric filtering
```
&numericFilters=created_at_i>{UNIX_TIMESTAMP}
```
Get UNIX timestamp: `date +%s` or use Python's `datetime`.

## Complete Python Pipeline

```python
import json, subprocess, sys

def hn_search(query, sort_by_date=True, hits=20):
    """Search HN and return list of {date, title, points, url}."""
    endpoint = "search_by_date" if sort_by_date else "search"
    url = f"https://hn.algolia.com/api/v1/{endpoint}?query={query}&tags=story&hitsPerPage={hits}"
    result = subprocess.run(["curl", "-sL", url], capture_output=True, text=True, timeout=15)
    data = json.loads(result.stdout)
    items = []
    for h in data.get("hits", []):
        items.append({
            "date": h.get("created_at", "")[:10],
            "title": h.get("title", ""),
            "points": h.get("points", 0),
            "url": h.get("url", "") or h.get("story_url", ""),
        })
    return items
```

## NYT RSS Feed

```
GET https://rss.nytimes.com/services/xml/rss/nyt/Technology.xml
```

### Complete Python Pipeline

```python
import xml.etree.ElementTree as ET
import subprocess

def nyt_tech_rss(keywords=None, limit=20):
    """Fetch NYT Tech RSS, filter by keywords."""
    result = subprocess.run(
        ["curl", "-sL", "--max-time", "15",
         "https://rss.nytimes.com/services/xml/rss/nyt/Technology.xml"],
        capture_output=True, text=True, timeout=20
    )
    root = ET.fromstring(result.stdout)
    items = []
    for item in root.findall(".//item"):
        title = item.find("title")
        desc = item.find("description")
        pubDate = item.find("pubDate")
        link = item.find("link")
        t = title.text if title is not None else ""
        if keywords:
            match = any(kw.lower() in t.lower() or
                       (desc and desc.text and kw.lower() in desc.text.lower())
                       for kw in keywords)
            if not match:
                continue
        items.append({
            "title": t,
            "date": pubDate.text[:16] if pubDate is not None else "",
            "url": link.text if link is not None else "",
            "description": desc.text[:200] if desc is not None and desc.text else "",
        })
        if len(items) >= limit:
            break
    return items
```
