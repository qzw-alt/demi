# Deccan Herald JSON-LD articleBody extraction (7th-tier source, verified 2026-07-27)

## Pattern

Deccan Herald article pages (e.g. `https://www.deccanherald.com/health/healthcare/explained-...-4083259`) return ~1.4 MB of HTML but the body content is NOT in `<p>` tags. Every standard `<p>` regex extraction returns 0 matches. The article text lives inside a single JSON-LD `articleBody` field that is HTML-encoded (`&lt;p&gt;`, `&lt;a href=&quot;...&quot;&gt;`).

**Working recipe (3 lines Python):**

```python
import re, html
c = open('/tmp/dh.html').read()
m = re.search(r'"articleBody":"(.*?)"(?=,"author"|,"datePublished"|,"url")', c, re.DOTALL)
body = html.unescape(m.group(1))
body = re.sub(r'<[^>]+>', ' ', body)
body = re.sub(r'\s+', ' ', body).strip()
```

`datePublished` is at the top of the same JSON-LD block (e.g. `"datePublished":"2026-07-22T18:47:07+05:30"`) and is reliable. `og:description` and `twitter:description` in the `<head>` give a clean 1-sentence summary.

## When to use

Use Deccan Herald as a 7th-tier source when the canonical news/medical/science sites (Xinhua, ChinaDaily, dxy, thepaper, EurekAlert, News-Medical, EIN Presswire, ScienceDaily) are all blocked by the cron sandbox (Cloudflare / JS challenge / abuse-page), AND the topic is academic-clinical (TCM, RCT, peer-reviewed paper) where a press release mirror is needed.

**Source-tier ordering on this site (verified 2026-07-27):**
1. Primary canonical (ChinaDaily.com.cn, akesobio.com, carsgen.com, biotech IR pages, mira­ge news for university press releases)
2. PR Newswire mirrors (manilatimes.net, finanznachrichten.de, lelezard.com)
3. pharmaphorum.com (FiercePharma substitute)
4. GEN.com (policy/regulatory/business)
5. Mirage News (university press releases)
6. The Star (Malaysia) for *China Daily* syndication, Straits Times for inbound medical-tourism
7. **Deccan Herald (this recipe)** for Indian English-language coverage of international clinical evidence

## Pitfalls

- The HTML page is ~1.4 MB. Don't try to grep `<p>` tags — there are none in the body region. The entire article text is inside one JSON-LD object.
- The `articleBody` regex needs the lookahead `(?=,"author"|,"datePublished"|,"url")` to terminate correctly, because the encoded HTML inside the body can contain escaped quote characters that would otherwise match the `"` terminator early.
- `html.unescape()` decodes `&lt;` to `<`, `&gt;` to `>`, `&quot;` to `"`, `&amp;` to `&`. After unescape, standard `<[^>]+>` strip works.
- The body text is typically 2,500–4,000 chars after unescape+strip. Don't expect a 10,000-char payload from one Deccan article.

## Reference run: 2026-07-27

- Source URL: https://www.deccanherald.com/health/healthcare/explained-facial-paralysis-how-gentle-electroacupuncture-may-boost-nerve-repair-4083259
- Date published (per JSON-LD): 2026-07-22T18:47:07+05:30
- Article extracted: ~3,800 chars covering a 66-patient RCT from Second Affiliated Hospital of Guangzhou University of Chinese Medicine, published in *Acupuncture Research*
- Article shipped: `blog/2026-07-27-electroacupuncture-facial-paralysis-gentle-current-china-rct-2026.html` (2,467 words, 0 banned-vocab hits, em-dash 7.8/1200)

# CrossRef and PubMed E-utilities blind spots (verified 2026-07-27)

## CrossRef

- `https://api.crossref.org/works/{doi}` returns `{"status":"resource not found"}` for the DOI `10.13702/j.1000-0607.20240877` (a 2026 *Acupuncture Research* / Zhen Ci Yan Jiu paper). The doi.org resolver redirects to `chndoi.org` (China DOI registration agency), which is not directly fetchable from the cron sandbox.
- **Decision rule:** when a paper's only identifier is a recent Chinese-journal DOI (Acupuncture Research, Chinese Journal of Integrative Medicine, Journal of Traditional Chinese Medicine, Chinese Acupuncture & Moxibustion / 中国针灸), CrossRef is not a working fallback. Use the journal's own English abstract page, a secondary press release, or the chinahospitalsguide content-research-writer-cn tier-2/3 sources (PR Newswire mirrors, pharma-specific news sites).
- **Working DOIs in CrossRef** (verified 2026-07-27 not-blank): most Western journal DOIs, NEJM, Lancet, JAMA, Frontiers, MDPI, PLOS, BioMed Central, some Hindawi titles. Check with `curl --max-time 30 -A 'Mozilla/5.0' -sL https://api.crossref.org/works/{doi}` first; if 200 + abstract present, use CrossRef as canonical.

## PubMed E-utilities

- `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi` is **blocked at the cron-sandbox IP (43.134.68.35) as of 2026-07-27** with the NCBI "blocked for possible abuse" diagnostic page.
- **Decision rule:** do NOT use PubMed E-utilities from this cron sandbox. Default to CrossRef + secondary press releases for clinical-evidence articles. If a paper has a DOI but no CrossRef entry, search for the title in Bing News / Deccan Herald / News-Medical / EIN Presswire / EurekAlert. The journal's own DOI-resolved page is a last resort.
- **Workaround if PubMed is the only source:** the de facto IP block is at the abuse-detection layer; the block typically resets after 24-48 hours of inactivity. The agent should NOT spend more than 1-2 tool calls probing PubMed before pivoting to the secondary-press-release fallback.

## Combined fallback chain for clinical-evidence articles (verified 2026-07-27)

When a paper is the news and the canonical source is unreachable:

1. CrossRef API (`api.crossref.org/works/{doi}`) — best case, gives abstract + metadata
2. Tier-2 PR Newswire mirror (manilatimes.net, finanznachrichten.de) — most biotech press releases land here
3. Tier-7 Deccan Herald JSON-LD articleBody (this file) — for academic-clinical coverage of Chinese TCM journal papers
4. News-Medical / EIN Presswire / EurekAlert / ScienceDaily / phys.org Bing News search — for popular-press coverage
5. The journal's own HTML page (for open-access titles: Frontiers, MDPI, PLOS, BMC, some Hindawi)
6. PubMed E-utilities — **DO NOT USE**, blocked at the cron-sandbox IP

If steps 1-5 all fail, write the article from the DOI's title + journal name + author list only, and acknowledge in the body prose that the full abstract is not yet publicly available.
