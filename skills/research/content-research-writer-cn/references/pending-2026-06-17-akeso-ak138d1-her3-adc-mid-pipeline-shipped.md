# Pending: 2026-06-17 Akeso AK138D1 HER3 ADC + Ivonescimab (Mid-Pipeline Cap-Hit Recovery)

**Status:** Article written, sitemap updated, humanize scored 90/100. Cap hit BEFORE news/index.html insertion, BEFORE git commit, BEFORE git push. Working tree clean (no commit), article on disk as `news/2026-06-17-akeso-ak138d1-her3-adc-ivonescimab-breast-cancer.html` (4,701 words).

**Cron run date:** 2026-06-17
**Press release date:** 2026-06-15 (Akeso press release)
**Article filename:** `news/2026-06-17-akeso-ak138d1-her3-adc-ivonescimab-breast-cancer.html` (uses cron run date — fresh news cycle, no date-preservation wrinkle)
**Article word count:** 4,701
**Em-dash density:** 17.1 per 1200 words (67 raw em-dashes)
**Humanize score:** 90 / 100 (threshold 60)
**De-dup verification:** `grep -lE "(AK138D1|HER3.ADC|IO2\.0|ADC2\.0|Dual-Shield ADC|HKEX.*9926.*HER3)" news/*.html` → 0 matches against 18-article library.

## Failure mode

This is the **FOURTH documented cron iteration cap-hit failure mode** (after 06-14 post-commit, 06-16 during-research, 06-04/06-07/06-10/06-12 during-writing). The cap fired mid-pipeline after `sitemap.xml` was patched but BEFORE `news/index.html` was patched and BEFORE any git commit was made.

**Detection signal for next run:** `ls news/$(date +%Y-%m-%d)-*.html 2>/dev/null` — non-empty result indicates partial completion. The `git status` check alone is NOT sufficient (working tree is clean since no commit was made).

## Recovery recipe for next run (5-7 tool calls)

```bash
cd /home/ubuntu/.hermes/workspace/website

# 1. Verify article + sitemap are in good state
head -20 news/2026-06-17-akeso-ak138d1-her3-adc-ivonescimab-breast-cancer.html
grep -c "2026-06-17" sitemap.xml  # should be >= 1 (the new <lastmod> entry)

# 2. Insert news/index.html card above the 2026-06-14 gumokimab article
#    The card structure is the same <article class="news-item"> block used by prior articles
#    Image: <img src="../images/medical-tourism.jpg" alt="...">
#    Date: "June 17, 2026"
#    Title: "Akeso's HER3 ADC AK138D1 Plus Ivonescimab Enters First Patient in a Phase Ib/II Breast Cancer Study..."
#    Excerpt: ~250 chars summarizing the story

# 3. Commit + push + verify
git add news/2026-06-17-akeso-ak138d1-her3-adc-ivonescimab-breast-cancer.html \
        sitemap.xml news/index.html
git commit -m "article: 2026-06-17"
git push origin master
sleep 180
curl -s -o /dev/null -w "%{http_code}" \
  https://chinahospitalsguide.com/news/2026-06-17-akeso-ak138d1-her3-adc-ivonescimab-breast-cancer.html
# Expect: 200
```

## Story summary (for next-run reference)

**Headline:** Akeso's HER3 ADC AK138D1 Plus Ivonescimab Enters First Patient in a Phase Ib/II Breast Cancer Study — An "IO2.0 + ADC2.0" Strategy Built for Refractory Disease

**Key facts:**
- Akeso (9926.HK) announced first-patient-in for AK138D1-202 Phase Ib/II on June 15, 2026
- AK138D1 is a next-generation HER3 ADC: patritumab (anti-HER3 IgG1) + MC-AAA cleavable linker + DXd topo-I payload
- Trial enrolls HR+/HER2- (65% of breast cancer) and TNBC (10-20%) patients, monotherapy and combination with ivonescimab
- Early data: meaningful single-agent activity in breast cancer, low hematologic toxicity, no ILD observed
- The "IO2.0 + ADC2.0" positioning: ivonescimab is PD-1/VEGF bispecific (Akeso's flagship); AK138D1 is the lead Dual-Shield ADC
- Akeso has 50+ innovative assets, 27 in clinical trials, 15 bispecific/multispecific antibodies or bispecific ADCs, 8 approved drugs
- TROP2/Nectin4 bispecific ADC AK146D1 is the other lead ADC; AK138D1 + AK146D1 give Akeso a portfolio play

**Article structure (9 sections — already written):**
0. News Brief (June 15, 2026 headline + international patient framing)
1. Why Breast Cancer (HR+/HER2- 65%, TNBC 10-20%, 2.3M new cases/year)
2. The Molecule (antibody + linker + payload + binding site barrier)
3. The Trial Design (AK138D1-202 Phase Ib/II, monotherapy + combination)
4. The Breast Cancer ADC Field (T-DXd / sacituzumab govitecan / datopotamab deruxtecan / AK138D1 comparison)
5. The IO2.0 + ADC2.0 Wave (combinations across the industry)
6. Akeso in 2026 (portfolio + 5 platforms)
7. What This Means for International Patients (clinical-trial enrollment pathway)
8. Practical Guidance (workflow + questions for trial site)
9. Outlook (next 18 months watch list)

**Internal links used:**
- /news/2026-06-14-akeso-gumokimab-psoriasis-nmpa-approval-2026.html (Akeso autoimmune pivot context)
- /news/2026-06-02-harmoni-6-ivonescimab-squamous-lung-cancer-asco-plenary.html (ivonescimab HARMONi-6 data)
- /news/2026-06-11-china-medical-tourism-cutting-edge-cheap-bloomberg.html (broader China medical tourism context)

**External source URLs:**
- Akeso press release: https://www.akesobio.com/en/media/akeso-news/260615/
- Akeso corporate: https://www.akesobio.com

**Banner color:** Purple gradient (`#581c87 0%, #7e22ce 50%, #a21caf 100%`) — distinct from the 06-14 gumokimab teal banner.

**Banned-vocab patches applied in this run (8 patches):**
- 2× enhance → amplify / increase
- 5× landscape → field / state / market (the 5 body instances; the section heading also patched)
- 1× removed "actually" from h3 heading

**Score progression:** 36/100 (first pass) → 90/100 (after 8 patches). The -ing tails (9) and high word count (4,701) are persistent notes but don't penalize below the 60 threshold.

## Why this is the FOURTH cap-hit mode (not a repeat of 06-14)

| Failure mode | Article on disk? | Local commit? | Pushed? | `git status` signal | Recovery |
|---|---|---|---|---|---|
| 06-14 post-commit | Yes | Yes | No | "ahead of origin by 1" | `git push && sleep && curl` (2 calls) |
| 06-16 during-research | No | No | No | Clean tree, pending file | `ls references/pending-*.md` then ship from pending |
| 06-17 mid-pipeline (this run) | Yes | No | No | Clean tree, untracked file in `news/` | `ls news/$(date +%Y-%m-%d)-*.html` then index.html + commit + push (5-7 calls) |
| 06-04/06-07/06-10/06-12 during-writing | Sometimes partial | No | No | Clean tree, pending file | Ship from pending file (full write cycle) |

The 06-17 mode is the easiest to recover from, but ONLY if the next run recognizes the partial state via the `ls news/$(date +%Y-%m-%d)-*.html` check.

## New patterns documented (added to SKILL.md)

1. **Akeso IR as primary source** — `https://www.akesobio.com/en/media/akeso-news/{YYMMDD}/` returns ~32KB of full press release body in a single curl. Confirmed working for AK138D1 (06-15) and gumokimab (06-11). Should be the FIRST source checked for any Akeso-related story.
2. **ChinaDaily.com.cn section scraping** — `/china/`, `/business/`, `/life/health/` section pages return full article lists with `/a/YYYYMM/DD/WS{hash}.html` URLs. Date is in the URL path. Use this when Bing News is broken AND you need headline discovery, not just article body.
3. **Pre-flight detection sequence** — codified as Step 0 in `programmatic-seo` workflow. Three checks run BEFORE any research: (a) `ls news/$(date +%Y-%m-%d)-*.html`, (b) `git status`, (c) `ls references/pending-*.md`.
4. **Fourth cap-hit mode** — the mid-pipeline failure mode is now documented alongside the three prior modes, with detection signal and recovery recipe.
