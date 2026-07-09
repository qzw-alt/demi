# 2026-07-09 Bing News Cold-Start Pitfall (REFERENCE ADDENDUM)

This addendum documents a NEW failure mode surfaced by the 2026-07-09 cron run that is **distinct from** the 06-16 "Bing HTML format change" pitfall documented in the main SKILL.md.

## The failure mode

**Bing News is structurally correct but returns 0 relevant results for the topic axis on a given day.**

The 2026-07-09 cron run hit 12 different Bing News queries across the full topic axis (acupuncture RCT 2026, TCM NEJM/Lancet, Hainan Boao Lecheng TCM, moxibustion breech, ASCO integrative oncology, tai chi Parkinson, baduanjin COPD, tuina stroke, IVF PCOS, chemo nausea, allergic rhinitis, etc.). All 12 queries returned HTTP 200 with valid article URLs in the grep output — but 11 of the 12 returned 0 China-medical URLs, and the one that did (chemo nausea) returned an Indian Council of Medical Research olanzapine study, not a Chinese trial. The 12 queries were:

| Query angle | Result |
|---|---|
| `acupuncture+clinical+trial+2026+china` | Straits Times 06-21 (already covered 06-22), The Hindu old piece, knowridge.com, USAtoday |
| `TCM+clinical+trial+NEJM+Lancet+2026+china` | 0 results |
| `traditional+chinese+medicine+acupuncture+2026+study` | Guyana wellness tourism, Manila Times lifestyle, The Star TCM-cultural piece |
| `acupuncture+chemotherapy+nausea+rct+2026+china` | 0 results |
| `acupuncture+migraine+2026+randomized+trial` | 0 results |
| `acupuncture+ivf+infertility+2026+china+trial` | 1 (HK fertility clinic, non-TCM) |
| `Hainan+Boao+Lecheng+traditional+chinese+medicine+2026` | 1 (Yonhap en.yna, Korean wire) |
| `%E5%8D%9A%E9%9D%96%E4%B9%90%E5%9F%8E+%E4%B8%AD%E5%8C%BB+%E5%92%AA%E4%B8%B4%E5%BA%8A+2026` (Chinese 博鳌乐城 + 中医 + 临床 + 2026) | 0 results |
| `acupuncture+low+back+pain+NEJM+2026+china` | 0 results |
| `tuina+massage+stroke+rehabilitation+china+2026` | 0 results |
| `baduanjin+exercise+COPD+lung+function+china+2026` | 0 results |
| `acupuncture+fibromyalgia+china+randomized+2026` | 1 (NDTV old piece) |
| `tai+chi+parkinson+disease+fall+prevention+2026+china` | 0 results |

Total: 2 China-medical URLs (both already-covered stories from 06-21/06-22), 0 fresh RCT/meta-analysis candidates.

## The diagnostic distinction

**The 06-16 "Bing HTML format broken" pitfall** is diagnosed by:
- HTML returns 250-360KB
- Grep returns only Bing-internal navigation links (`/chat`, `/copilot`, `/images`, `/maps`, `/news/search`, `/?FORM=...`)
- `<script>` JS endpoints surface in grep
- MSN/People.com/AOL/unrelated news dominate

**The 07-09 "Bing returns empty for the topic" pitfall** is diagnosed by:
- HTML returns 200 OK, structurally normal
- Grep returns valid external article URLs (manilatimes, straitstimes, channelnewsasia, thehindu, etc.)
- BUT the URLs are off-topic (HK fertility, India olanzapine, USAtoday Florida laws, cultural wellness, lifestyle)
- The 0-1 China-medical URLs that surface are 1-2 weeks old and already covered

These are two different failure modes. The 06-16 fix is "switch to fallback sources (ChinaDaily section scraping, biotech IR pages, Manila Times PR Newswire feed)". The 07-09 fix is "STOP — this is a true cold-start, no source will rescue the day."

## The decision rule

**If after 3 topic-diverse Bing queries (3 different keyword angles, not 3 retries of the same query) the union of returned URLs is <3 China-medical articles total, STOP trying Bing with more keyword permutations and report "无可用热点，跳过今日发布" per the 宁缺毋滥 rule.**

Do not keep iterating — each Bing query costs ~1 tool call and the failure is not query-dependent. 12+ Bing queries burned 12 tool calls and produced the same result as 3 queries. The 07-09 run spent the entire 35-call research budget on Bing queries because the skill's recipes (3 verified sources per topic class) implied "more queries = more chances of finding something" — that's only true when the source pool actually has something to surface. When the topic axis is genuinely cold, no number of queries will help.

## The library-saturation secondary signal

**Before starting Bing research, check the last 5 articles' topic distribution.** The 07-09 run also demonstrated that when the last 5 days have all been TCM archetype A/B (07-02 IVF, 07-04 stroke dysphagia, 07-06 TCM AI, 07-07 TCM AI device, 07-08 stroke motor), the next-day Bing search for "acupuncture X 2026" is biased toward variants of already-covered topics (stroke, IVF, oncology) because those ARE the high-search-volume TCM trial categories. The check is:

```bash
ls news/ | tail -5
# Look at topic distribution
for f in $(ls news/ | tail -5); do echo "=== $f ==="; grep -oE "<title>[^<]+</title>" "news/$f" | head -1; done
```

If 4+ of the last 5 are on a single topic axis (e.g. all TCM acupuncture, all CAR-T, all robotic surgery), the day's Bing results will likely be in the same axis. This is a second signal that the topic axis is saturated. The 宁缺毋滥 rule should fire when either (a) Bing is returning <3 China-medical URLs in 3 queries OR (b) the surfaced URLs are variants of stories already covered in the last 5 days.

## What the next cron run should try FIRST (2026-07-10+)

1. **OpenAlex API** — `curl "https://api.openalex.org/works?filter=concepts.id:C2779444912,from_publication_date:2026-07-09&sort=publication_date:desc&per_page=10"` (concept C2779444912 = "Traditional Chinese Medicine"). OpenAlex indexes PMC, Frontiers, MDPI, Wiley, Springer — the OA-friendly subset of the same pool NCBI PubMed rejects via Cloudflare. This is a 1-call research tool that returned 0 hits on 07-09 (NCBI was rate-limited) but might return results on 07-10 once the 24-hour rate limit window resets.

2. **PubMed via EBI alternative endpoint** — `curl "https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=acupuncture+china+2026&format=json&sort=date"` — Europe PMC mirrors PubMed and was not rate-limited on 07-09.

3. **CNKI / Wanfang via CrossRef `type:journal-article,has-abstract:true`** — `curl "https://api.crossref.org/works?query.bibliographic=acupuncture+china&filter=from-pub-date:2026-07,type:journal-article,has-abstract:true&rows=10"` — CrossRef indexed some CNKI English-language articles in 2025-2026, and the `has-abstract:true` filter is the most direct way to find ones that have enough metadata to write a 1,200-word article from.

4. **Template C fallback** — 海南博鳌乐城 publishes new imported-drug lists in mid-July each year. The 2025-07 list was released around 07-15; the 2026-07 list should appear 2026-07-15 ± 5 days. If 07-10 to 07-14 are still cold, the 07-15 cron run is a strong Template C candidate. Pre-position: keep `https://www.google.com/search?q=%E5%8D%9A%E9%9D%96%E4%B9%90%E5%9F%8E+%E5%8F%AF%E8%BF%9B%E5%8F%A3%E8%8D%AF%E5%93%81+2026` in the saved-query list for 07-15.

## Why this is not a tool failure

PubMed (NCBI E-utilities) returned a 302 to `misuse.ncbi.nlm.nih.gov/error/abuse.shtml` — the cron sandbox IP had been rate-limited earlier in the day (possibly by an unrelated NCBI user on the same egress IP). CrossRef returned 5 results but none on TCM (the 5 were meta-SWOT analysis, GC-MS analysis, hospital efficiency in Cameroon — clearly not filtered correctly). ABC News `https://www.abc.net.au/news/health/` returned a 34-byte redirect-to-https stub, the 425KB body the 2026-07-02 run had relied on is no longer reachable from this egress. These are not skill bugs — they're the realistic state of the cron sandbox's access surface. The skill should document the cold-start case as a routine outcome, not a failure to engineer around.
