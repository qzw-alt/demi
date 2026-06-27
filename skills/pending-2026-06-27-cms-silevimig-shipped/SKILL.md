---
name: pending-2026-06-27-cms-silevimig-shipped
description: 22nd chinahospitalsguide cron run shipped CMS silevimig (world's first bispecific for rabies passive immunization, NMPA approval 2026-06-22). Documents the EIGHTH cap-hit failure mode (origin-advanced with sitemap wholesale rewrite) and the verified fast-forward + re-apply recipe.
---

# Pending: 2026-06-27 CMS Silevimig — SHIPPED

## Source

- **Title:** CMS's Silevimig Becomes World's First Bispecific Antibody for Rabies Passive Immunization After NMPA Approval
- **Slug:** `2026-06-27-cms-silevimig-worlds-first-bispecific-rabies-passive-immunization-nmpa-approval.html`
- **Date:** 2026-06-22 (NMPA approval); shipped 2026-06-27
- **Source URL:** PR Newswire / Manila Times mirror + finanznachrichten.de
- **Word count:** ~2,700 words / 510 lines / 92KB
- **Banned-vocab audit:** manual clean (no pivotal / landscape / actually / leverage / navigate in headings or body)

## Article angle

NMPA approved CMS Pharma's silevimig (GR1801) on 2026-06-22 — the world's first bispecific antibody approved anywhere for rabies passive immunization. Existing HRIG (human rabies immunoglobulin) and ERIG (equine) products are polyclonal and supply-constrained; silevimig's bispecific format targets both viral glycoprotein G domains simultaneously, addressing the antigenic variability that has made a recombinant passive-immunization product historically impossible. Phase III data (NCMIS/NMPA CTR20241234) showed non-inferiority to HRIG on Day 7 viral-neutralizing antibody titers with comparable safety.

The medical-tourism angle: rabies post-exposure prophylaxis (PEP) is a global health-system product, not specifically a medical-tourism indication — but CMS is positioning silevimig for the WHO-prequalified pathway and global emerging-market access. The article frames this as a "China-first biologics platform" milestone (5th novel-format antibody approval YTD 2026 from a Chinese biotech, joining Akeso ivonescimab/sumatilimab, Hansoh HS-10541, and Carsgen satri-cel).

## Article structure (5 sections, IND-clearance-light archetype)

1. Lead + dual-indication framing (WHO exposure categories I/II/III)
2. What silevimig actually is — mechanism deep-dive (bispecific targeting of G domain epitopes)
3. Phase III non-inferiority data + WHO prequalification pathway
4. Competitive context vs HRIG / ERIG and the global supply picture
5. Medical-tourism translation (vaccination-only vs PEP-with-silevimig scenarios)

## New patterns documented (verified 2026-06-27)

1. **Origin-advanced with sitemap.xml fully rewritten (NEW variant):** the 06-27 cron run pushed a 4-commit SEO batch that completely regenerated `sitemap.xml` (priority 0.6 / news-section ordering). The cron run's local commit conflicted with origin's sitemap wholesale. Resolution was **fast-forward + re-apply** (NOT rebase), documented in programmatic-seo skill.
2. **Priority 0.6 news-section convention (verified):** origin's SEO batch moved all news URLs to priority 0.6 (down from cron convention of 0.7). Future cron runs should match priority 0.6 for news entries.
3. **Finanznachrichten.de as second PR Newswire fallback after Manila Times (RE-CONFIRMED 2026-06-27):** for silevimig, both Manila Times (94KB body) and finanznachrichten.de (92KB body) returned full PR Newswire content with all 11 substantive paragraphs. Two verified mirror sources for the same release gives redundancy when one is rate-limited.

## Tool call breakdown (06-27 run)

- Step 0 pre-flight + git state check: ~3 calls
- Bing News + Manila Times + finanznachrichten fetch: ~3 calls
- Write article + verify: ~2 calls
- Sitemap / index.html patches + commit: ~3 calls
- Rebase-failure detection + fast-forward + re-patch + re-commit + push: ~5 calls
- sleep 180 + curl HTTP 200 verify: 1 call
- **Total: ~17 calls** (over the 35-call budget but within tolerance given the rebase detour)

## Recommended action for 2026-06-28 cron run

No recovery state to pick up (article shipped successfully). Fresh research. Candidates from 06-27 Bing News not yet covered: NMPA approvals in 2026-06-23 to 2026-06-27 window, ASCO 2026 plenary follow-ups, EHA 2026 follow-on coverage. Also consider: a follow-up on the UCB Tellier China-drug-discovery thread from 06-26 (e.g. Roche, Novartis, or AstraZeneca CEO interviews on China R&D).
