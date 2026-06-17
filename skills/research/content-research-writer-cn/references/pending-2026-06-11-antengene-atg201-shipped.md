---
story: Antengene ATG-201 (CD19 × CD3 bispecific T-cell engager) NMPA IND clearance for B-cell autoimmune disease
date_researched: 2026-06-10
date_shipped: 2026-06-11
research_status: shipped
target_article_slug: 2026-06-10-antengene-atg-201-bispecific-autoimmune-pku.html
commit_hash: 9966cd8
live_url: https://chinahospitalsguide.com/news/2026-06-10-antengene-atg-201-bispecific-autoimmune-pku.html
em_dash_density_at_publish: 13.4 per 1200 words (raw 63, 5638 words total)
humanize_score_at_publish: 62/100
banner_color: teal/blue gradient
---

# Pending → Shipped: Antengene ATG-201 / CD19-CD3 Bispecific TCE for Autoimmune Disease

## What shipped

The 2026-06-10 article (`news/2026-06-10-antengene-atg-201-bispecific-autoimmune-pku.html`) was successfully written, humanized, published, and verified in the 2026-06-11 cron run.

- **Cron run date:** 2026-06-11 (Thursday)
- **Article publish date in file:** 2026-06-10 (the press-release date is preserved as the story date)
- **Slug:** `2026-06-10-antengene-atg-201-bispecific-autoimmune-pku.html`
- **Commit:** `9966cd8 article: 2026-06-10 Antengene ATG-201 CD19-CD3 bispecific TCE for B-cell autoimmune disease, Phase I ATTRACT at PKUPH`
- **Live URL:** https://chinahospitalsguide.com/news/2026-06-10-antengene-atg-201-bispecific-autoimmune-pku.html (HTTP 200 verified at T+3min after push)
- **Sitemap updated:** entry added at the top of the news section, before 2026-06-09
- **News index updated:** card added at top, before the Ori-C101 article

## Article stats

- **Word count (em_dash_check.py):** 5638 total
- **Word count (humanize_score.py body extraction):** 5229 (the difference is script body-extraction regex)
- **Em-dashes:** 63 raw, 13.4 per 1200 words — in the false-negative band (10-17) per the verified pitfall in programmatic-seo SKILL.md
- **Humanize score:** 62/100 (passes >60 threshold)
- **Banned vocab hits:** 2 × "actually" (in legitimate prose, not headings — tolerated per 2026-06-08 pitfall), 1 × "navigate the" (in "navigate the cross-border clinical-trial pathway" — also legitimate clinical-prose usage, not a strip)
- **-ing tails:** 12 (within normal range for clinical prose)
- **"Despite" uses:** 0

## Sections shipped (9, matching 06-09 Ori-C101 pattern)

1. News brief (banner section)
2. Why B-cell autoimmune disease is the next frontier
3. The molecule: how a masked bispecific T-cell engager works
4. The ATTRACT Phase I trial design
5. Why PKU People's Hospital matters
6. The UCB deal and what it means
7. Beijing as an autoimmune inbound hub
8. Cost and access (5 access routes)
9. Practical guidance + Outlook

## Internal links used

- `/news/2026-06-09-oricell-gpc3-cart-hcc-nmpa-phase2-clearance.html` (Shanghai cell-therapy corridor context)
- `/news/2026-06-06-pakistani-patient-cart-shanghai-jiahui-lymphoma.html` (Jiahui international CAR-T comparison)
- `/news/2026-06-03-hainan-boao-lecheng-medical-tourism-pilot-zone.html` (Lecheng access pathway)
- `/contact.html` (CTA)

## External sources cited (11 total)

- manilatimes.net PR Newswire mirror of Antengene press release (primary)
- antengene.com, pkuph.cn, cde.org.cn, ucb.com/our-science/pipeline
- Background citations for academic CAR-T-for-lupus (Mackensen, Schett) and blinatumomab

## Pitfalls encountered / learned

1. **Pending-file recovery loop continues to work end-to-end.** This is the 9th cron run with the pending-file handoff pattern; the recipe is now stable and reliable.
2. **Em-dash density of 13.4/1200 (false-negative band 10-17)** is acceptable per the verified pitfall in the programmatic-seo SKILL.md. The article reads as clinical-prose with reasonable density. Did NOT strip em-dashes to "fix" the score.
3. **Score 62 vs the 06-09 Ori-C101 article's score 82** — the difference is mostly word count (5229 vs 4216) and the -ing-tail count. Both articles pass the >60 threshold; the lower score on the autoimmune article is acceptable for a 5,200+ word piece.
4. **`grep -P '[^\x00-\x7F]'` check caught legitimate non-ASCII content** — `栗占国` (Prof. Li's Chinese name) and `×` (multiplication sign in "CD19 × CD3") — both are intentional, not contamination. The check is to find accidentally-introduced CJK, not to block intentional CJK.
5. **No fresh research done on 2026-06-11.** The recovery pattern is: check `ls references/pending-*.md` at start of run, write the article from the recipe in the pending file, ship. ~7 tool calls total for this run (terminal check, pending read, template read, article write, sitemap patch, index patch, commit, push, verify).

## Cron state at end of run

- Local master HEAD: `9966cd8 article: 2026-06-10 Antengene ATG-201 CD19-CD3 bispecific TCE for B-cell autoimmune disease, Phase I ATTRACT at PKUPH`
- Remote master HEAD: `9966cd8` (in sync)
- SSH remote intact: `git@github.com:qzw-alt/chinahospitalsguide.git`
- No pending files remaining
- Next cron run: 2026-06-12, fresh research cycle
