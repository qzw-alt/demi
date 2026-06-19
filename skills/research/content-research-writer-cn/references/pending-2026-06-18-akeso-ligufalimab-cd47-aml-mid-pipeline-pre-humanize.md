# Pending: 2026-06-18 Akeso Ligufalimab (CD47) AML Phase II EHA 2026 (Mid-Pipeline Cap-Hit — Pre-Humanize Variant)

**Status:** Article written, NOT humanize-scored, NOT committed, NOT pushed. Working tree clean (article is untracked). This is a **NEW VARIANT of failure mode #4** (mid-pipeline cap-hit) — distinguished from the 06-17 case by the cap firing BEFORE the humanize verify call, not AFTER.

**Cron run date:** 2026-06-18
**Press release date:** 2026-06-17 (Akeso / PR Newswire)
**Article filename:** `news/2026-06-18-akeso-ligufalimab-cd47-frontline-aml-eha-2026.html`
**Article word count:** ~3,400 (file size 26,654 bytes; 9 sections complete with JSON-LD, data table, sources block, CTA box)
**Em-dash density:** Not yet measured (humanize not run)
**Humanize score:** Not yet scored — pending
**De-dup verification:** `grep -lE "(ligufalimab|AK117|CD47|AML|EHA)" news/*.html` → 0 matches against the entire library at the time of write.

## Failure mode (NEW VARIANT — fifth cap-hit mode)

This is the **FIFTH documented cron iteration cap-hit failure mode** and the **first variant of failure mode #4 (mid-pipeline)**. The cap fired AFTER the article was written to disk but BEFORE the humanize_score.py verify call. The 06-17 mid-pipeline case had completed humanize (90/100) before the cap; the 06-18 case never reached humanize.

**Key distinction from 06-17 mid-pipeline variant:**
- 06-17: article on disk + humanize scored + sitemap patched → cap before index.html / commit / push
- 06-18 (this): article on disk only → cap before humanize / sitemap / index.html / commit / push
- Recovery cost is the same (5 tool calls) but the FIRST step is humanize verify, not index.html insertion

**Detection signal:** `ls news/$(date +%Y-%m-%d)-*.html 2>/dev/null` — non-empty result indicates partial completion. The `git status` check alone is NOT sufficient (working tree is clean since no commit was made). This detection check is the same as 06-17 mid-pipeline, so future runs that pick up either variant follow the same 5-call recipe — the humanize verify call simply runs first when the article is unverified.

## Recovery recipe for next run (5-7 tool calls)

```bash
cd /home/ubuntu/.hermes/workspace/website

# 1. Verify article is in good state and run humanize
head -20 news/2026-06-18-akeso-ligufalimab-cd47-frontline-aml-eha-2026.html
python3 /home/ubuntu/.hermes/skills/creative/programmatic-seo/scripts/humanize_score.py \
  news/2026-06-18-akeso-ligufalimab-cd47-frontline-aml-eha-2026.html \
  --site chinahospitalsguide --sitemap sitemap.xml
# Expect: score ≥ 60. If <60, patch the banned-vocab hits and re-score.

# 2. Patch sitemap.xml — insert new <url> entry at top of <urlset>
#    (the entry must match the article's <link rel="canonical"> URL)

# 3. Patch news/index.html — insert 06-18 card before the 06-17 card
#    Card structure matches prior articles in news/index.html
#    Image: <img src="../images/medical-tourism.jpg" alt="...">
#    Date: "June 18, 2026"
#    Title: "Akeso Ligufalimab (CD47) Plus AZA + VEN Hits HR 0.46 in Frontline AML at EHA 2026: A New Path for Older Patients Ineligible for Chemo"
#    Excerpt: ~250 chars

# 4. Commit + push + verify
git add news/2026-06-18-akeso-ligufalimab-cd47-frontline-aml-eha-2026.html \
        sitemap.xml news/index.html
git commit -m "article: 2026-06-18 Akeso ligufalimab CD47 + AZA + VEN Phase II AML EHA 2026"
git push origin master
sleep 180
curl -s -o /dev/null -w "%{http_code}" \
  https://chinahospitalsguide.com/news/2026-06-18-akeso-ligufalimab-cd47-frontline-aml-eha-2026.html
# Expect: 200
```

## Story summary (for next-run reference)

**Headline:** Akeso Ligufalimab (CD47) Plus AZA + VEN Cuts EFS Hazard by More Than Half in Frontline AML — EHA 2026 Phase II Readout

**Key facts:**
- Akeso (9926.HK) presented oral Phase II data from AK117-206 at EHA 2026 in Milan on June 13, 2026 (press release issued June 17, 2026)
- Ligufalimab (AK117) is Akeso's next-generation humanized IgG4 anti-CD47 monoclonal antibody — Fc-engineered to spare erythrocyte CD47 (addressing the magrolimab red-cell toxicity issue)
- Trial design: randomized, double-blind, placebo-controlled Phase II; ligufalimab + azacitidine + venetoclax vs placebo + azacitidine + venetoclax in treatment-naïve AML patients ineligible for intensive chemotherapy
- Primary endpoint met: EFS hazard ratio 0.46 (54% reduction in event risk)
- Median EFS: 9.1 months (ligufalimab) vs 6.9 months (placebo)
- 6-month EFS: 67.8% vs 55.5%; 9-month EFS: 53.2% vs 14.1% (39.1 percentage-point gap)
- 6-month OS: 83.3% vs 73.2%; 9-month OS: 78.7% vs 43.1% (35.6 percentage-point gap)
- Composite complete response (CRc): 56.7% vs 53.3%
- CRc with MRD negativity: 46.7% vs 36.7%
- Median duration of CRc: 10.4 months vs 5.6 months (nearly doubled)
- Safety: TEAE/SAE rate comparable between arms; no hemolysis or RBC agglutination signal
- Class context: magrolimab (Gilead) was substantially de-prioritized after the ENHANCE-3 MDS failure in 2024; ligufalimab now has the strongest randomized AML data in the CD47 class

**Article structure (9 sections — already written):**
0. News Brief (June 13, 2026 headline + HR 0.46 framing)
1. What Is AML and Why Is It Hard in Older Adults? (median age 68, 60% chemo-ineligible, AZA+VEN is current SoC with 9-15 month median OS)
2. Why CD47 Is Hard and What Akeso Did Differently (magrolimab history, RBC binding problem, IgG4 Fc engineering)
3. AK117-206 Data Endpoint by Endpoint (full data table)
4. Why EHA 2026 Chose This for an Oral Presentation (program committee signal, oral session context)
5. Where Ligufalimab Sits in the Global CD47 Landscape (magrolimab / Trillium / other CD47 agents)
6. What AK117-206 Means for International Patients (3 access routes: clinical-trial enrollment, Hainan Lecheng, compassionate use)
7. What Comes Next — Phase III, Companion Diagnostics, Combination Strategies (menin inhibitors, FLT3 inhibitors)
8. How This Compares to Other Recent AML Advances (revumenib, ziftomenib, gilteritinib context)
9. Bottom Line (Phase III readiness, immediate access pathways)

**Internal links used (in the article):**
- https://chinahospitalsguide.com/ (home / CTA)
- https://chinahospitalsguide.com/news/ (news index)
- https://chinahospitalsguide.com/hospitals/ (hospitals index)

**External source URLs:**
- Akeso press release (full text via finanznachrichten.de PR Newswire mirror): https://www.finanznachrichten.de/nachrichten-2026-06/68789109-akeso-inc-ligufalimab-cd47-based-combination-achieves-deep-responses-and-survival-benefit-in-frontline-aml-phase-ii-results-presented-in-oral-se-008.htm
- Akeso corporate site / pipeline: https://www.akesobio.com/en/pipeline/
- EHA 2026 Congress: https://ehaweb.org/congress/eha2026-congress/
- Akeso Hong Kong Stock Exchange listing: https://www.hkex.com.hk/-/media/HKEX-Market/Listing/News-and-Market-Reports/News/2026/260615/9926
- DiNardo CD, et al. NEJM 2020;383:617-629 (AZA+VEN standard-of-care backbone reference)
- Sallman DA, et al. (magrolimab MDS background; note: ENHANCE-3 readout was negative)

**Banner color:** Pink/rose gradient (`#831843 0%, #be185d 100%`) — distinct from the 06-17 purple gradient and the 06-14 teal gradient.

## Why this is the FIFTH cap-hit mode (not a repeat of 06-17 mid-pipeline)

| Failure mode | Article on disk? | Humanize done? | Sitemap patched? | Local commit? | Pushed? | `git status` signal | Recovery |
|---|---|---|---|---|---|---|---|
| 06-14 post-commit | Yes | Yes | Yes | Yes | No | "ahead of origin by 1" | `git push && sleep && curl` (2 calls) |
| 06-16 during-research | No | No | No | No | No | Clean tree, pending file | `ls references/pending-*.md` then ship from pending |
| 06-17 mid-pipeline (v1) | Yes | Yes (90) | Yes | No | No | Clean tree, untracked `news/2026-06-17-*.html` | index.html + commit + push (5 calls) |
| **06-18 mid-pipeline (v2, this run)** | Yes | No | No | No | No | Clean tree, untracked `news/2026-06-18-*.html` | humanize + sitemap + index.html + commit + push (5-7 calls) |
| 06-04/06-07/06-10/06-12 during-writing | Sometimes partial | No | No | No | No | Clean tree, pending file | Ship from pending file (full write cycle) |

The detection signal is identical between 06-17 v1 and 06-18 v2 (`ls news/$(date +%Y-%m-%d)-*.html` non-empty), but the FIRST recovery step differs: 06-17 v1 could skip humanize and go straight to index.html; 06-18 v2 must run humanize first to verify the article passes the >60 threshold before shipping.

## New patterns documented (added to SKILL.md)

1. **Bing News format-change regression is transient, not durable** — the 06-16 "Bing is broken" finding was a temporary HTML-format regression. On 06-17 and 06-18 Bing returned valid external article URLs in the grep. Future runs should try Bing first (1-2 fetches) before assuming it is broken; only switch to fallback paths if the first 1-2 Bing calls return only Bing-internal navigation links. The "DEPRECATED" framing in the original pitfall has been softened to "transient — verify before skipping."
2. **finanznachrichten.de as working PR Newswire fallback** — when tirto.id is Cloudflare-blocked (or any other mirror fails), try `https://www.finanznachrichten.de/nachrichten-YYYY-MM/{6-7-digit-numeric}-{slug}.htm`. The German-language site indexes PR Newswire verbatim with full body text intact (verified: 70KB body for the Akeso ligufalimab release, dateline and methodology paragraph preserved). This is a third fallback alongside the existing Manila Times (`manilatimes.net`) and Akeso IR (`akesobio.com/en/media/akeso-news/`) routes.
3. **Fifth cap-hit mode (06-18 mid-pipeline pre-humanize variant)** — failure mode #4 now has two sub-variants distinguished by whether humanize was completed before the cap. Detection is identical (`ls news/$(date)-*.html`); recovery cost differs by 1 tool call.