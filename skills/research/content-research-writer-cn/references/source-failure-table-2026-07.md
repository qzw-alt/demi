# Source Failure Table: Verified Working vs. Broken Sources (2026-07-30 update)

Companion to the main SKILL.md source failure table. Tracks new failures discovered during the 2026-07-30 cron run and others where the main SKILL.md needs a more detailed entry than fits inline.

## Newly-broken source (verified 2026-07-30)

### NCBI PubMed eutils API — 302 to abuse page

**Failure mode:** `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?...` returns:

```html
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html><head>
<title>302 Found</title>
</head><body>
<h1>Found</h1>
<p>The document has moved <a href="https://misuse.ncbi.nlm.nih.gov/error/abuse.shtml?orig_args=/entrez/eutils/esearch.fcgi">here</a>.</p>
</body></html>
```

The cron sandbox IP is on NCBI's abuse blocklist. The 311-byte response body contains no useful metadata. Any `json.load` against the response fails with `JSONDecodeError`.

**Decision rule:** if a cron job needs recent peer-reviewed TCM / acupuncture / clinical-trial metadata from PubMed, **skip NCBI entirely** and use one of these working paths:

1. **CrossRef API** — `curl -A "Mozilla/5.0 ..." "https://api.crossref.org/works?query.bibliographic=...&rows=10&sort=published&order=desc"`. Works, but **caveat:** relevance ranking is weak for TCM queries and date parsing is fragile for some metadata. The 07-30 query for `acupuncture OR traditional Chinese medicine AND meta-analysis AND 2026` returned 10 items with publication dates 2106-2121 (clearly misparsed). Useful for title/authors when you have a known DOI; not reliable for keyword discovery.

2. **Direct journal HTML fetch** for known-DOI papers (Frontiers, MDPI, PLOS, BMC — see the two-source pattern in main SKILL.md). Best when you already have a DOI from another source.

3. **ChinaDaily.com.cn section scraping** — `curl -A "Mozilla/5.0" https://www.chinadaily.com.cn/business` (and `/china`, `/life/health`). Returns 50-95KB of full article list HTML. The `<a target="_blank" href="//www.chinadaily.com.cn/a/YYYYMM/DD/WS{HASH}.html">Title</a>` pattern gives date + URL + title in one grep. Best for industry / pharma / biotech news and executive interviews. **This was the working source for the 07-30 Merck article.**

4. **Bing News specific-query pivot** — when Bing returns 0 relevant URLs on broad TCM queries (07-30 saw pollution with non-medical results), the third or fourth query should pivot to specific named entities (drug class + regulator + year, named-company + named-asset) rather than broader "Chinese medicine" queries. If 3+ Bing queries all return noise, switch directly to ChinaDaily.com.cn section scraping.

**Tool-call cost of the NCBI 302 detour:** 2 calls wasted discovering the redirect + trying json_parse on the HTML body before pivoting. Future runs should detect the 302 in the first response and switch immediately.

## Working sources (reminder — already documented in main SKILL.md)

These sources were confirmed working on the 07-30 run and remain reliable:

- **ChinaDaily.com.cn** `/business/`, `/life/health/`, `/china/`, `/culture/` — section landing pages return 50-95KB with full article lists
- **ChinaDaily.com.cn** per-article URLs (`/a/YYYYMM/DD/WS{HASH}.html`) — 50-70KB with full body in `<p>` tags + reliable `<meta name="publishdate" content="YYYY-MM-DD">`
- **akesobio.com** `/en/media/akeso-news/` — 32KB full press release body
- **carsgen.com** `/en/news/{YYYYMMDD}/` — 104KB full press release body
- **Mirage News** — 59KB university press release mirror
- **finanznachrichten.de** — 70KB PR Newswire mirror for biotech + university releases
- **prnewswire.com / manilatimes.net** — 350KB PR Newswire body (Miracle News style)
- **pharmaphorum.com** — 94KB FiercePharma substitute
- **genengnews.com** — 250KB regulatory/policy/business angle
- **CrossRef API** — works but relevance ranking weak (see above)
- **Direct Frontiers / MDPI / PLOS HTML fetch** — full body for open-access journals

## Sources confirmed broken on 07-30 (extends main SKILL.md table)

| Source | Failure mode | Status |
|---|---|---|
| `eutils.ncbi.nlm.nih.gov` | 302 → misuse.ncbi.nlm.nih.gov | NEW 2026-07-30 |
| `pubmed.ncbi.nlm.nih.gov` (direct page fetch) | Likely same abuse block; not tested 07-30 | Likely broken; use Europe PMC or OpenAlex instead |
| `api.crossref.org` | Works but returns misparsed dates for some queries | Partially working; verify dates before citing |
| `bing.com/news` (broad TCM queries) | Pollution + format instability | Working for specific queries, broken for broad; pivot after 1-2 failed attempts |