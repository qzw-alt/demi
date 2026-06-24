# 2026-06-23 cron run — CarsGen satri-cel NMPA approval (shipped)

## Outcome

- **Article:** `news/2026-06-23-carsgen-satri-cel-worlds-first-solid-tumor-car-t-gastric-cancer-nmpa-approval.html`
- **Word count:** 5,308 (article body, em-dash check); 4,746 (humanize_score.py script count)
- **Em-dash density:** 17.2 per 1200 words (within 17-23 verified site baseline)
- **Humanize score:** 90/100 (threshold 60 — passed cleanly)
- **Commit:** `ba4552b` — "article: 2026-06-23 carsgen satri-cel first solid tumor car-t nmpa approval gastric cancer"
- **Live URL:** https://chinahospitalsguide.com/news/2026-06-23-carsgen-satri-cel-worlds-first-solid-tumor-car-t-gastric-cancer-nmpa-approval.html
- **Verified HTTP:** 200 (within 3 minutes of push)

## Story

NMPA approved satricabtagene autoleucel (satri-cel) on 2026-06-22 — **the world's first CAR-T therapy ever approved anywhere for a solid tumor**. Indication: Claudin18.2-positive, HER2-negative advanced gastric/gastroesophageal junction adenocarcinoma after ≥2 prior lines of systemic therapy.

Approval rests on the **CT041-ST-01 Phase 2 trial** published in The Lancet 2025 (PMID 40460847; Qi C, Liu C, Peng Z, ..., Shen L), led by **Prof Lin Shen at Peking University Cancer Hospital**. Median PFS 3.25 months (satri-cel) vs 1.77 months (treatment of physician's choice). PI Lin Shen quote in CARsgen press release: previous treatment options for these patients "were extremely limited and the prognosis was very poor" and satri-cel "provides us with a novel and effective therapeutic weapon."

## Sources

1. **Primary:** CARsgen IR press release at `https://www.carsgen.com/en/news/20260622/` — 104KB full body, no JS, no auth. Same archetype as Akeso's `/en/media/akeso-news/` pattern. Title: "CARsgen Announces Approval of Satri-cel, the World's First CAR T-Cell Therapy Product for Solid Tumors." Includes named investigator (Prof Lin Shen), The Lancet citation, preconditioning regimen (cyclophosphamide + fludarabine + low-dose nab-paclitaxel), and trial pipeline (NCT05911217 pancreatic adjuvant, NCT06857786 gastric consolidation, NCT07179484 gastric 1L sequential).
2. **Cross-verification:** pharmaphorum 2026-06-22 article at `https://pharmaphorum.com/news/carsgen-bags-world-first-approval-solid-tumour-car-t` — 94KB full body, `<time datetime="2026-06-22T15:54:53+00:00">` for date, named sources, Astellas Vyloy (zolbetuximab) comparator.
3. **Cross-verification:** The Lancet Phase 2 citation at `https://pubmed.ncbi.nlm.nih.gov/40460847/` (PMID 40460847, Lancet 2025 Jun 7;405(10494):2049-2060).
4. **Trial registry:** ClinicalTrials.gov NCT05911217, NCT06857786, NCT07179484.
5. **Background:** WHO/IARC Globocan 2022 — gastric cancer 970K new cases globally/year, 660K deaths, 70%+ in Asia, 47% in China.
6. **Bing News search** `China+NMPA+drug+approval+June+2026` — returned 6+ distinct external URLs (FiercePharma, Yahoo Finance, pharmaphorum, ContractPharma, asiae.co.kr, genengnews.com, manilatimes PR Newswire) on first grep, recipe working.

## De-dup check

`grep -lE "(satri-cel|CT041|CarsGen.*gastric|world.first.*solid.tumor.CAR.T|Claudin18\.2)" news/*.html` → returned 1 match: `2026-05-09-car-t-therapy-cost-china-solid-tumor-breakthrough.html`. **Confirmed non-duplicate:** the 05-09 article was about NDA acceptance ("if approved — expected late 2026"), and the 06-23 article is about the actual approval + Lancet data + access path + cost comparison. Same drug, different news event (NDA acceptance vs. approval).

## Article structure

9 sections, ~5,300 words:

1. Why This Approval Is a Hard Milestone (the three structural reasons solid-tumor CAR-T is hard: target selection, microenvironment, trafficking)
2. The CT041-ST-01 Trial and The Lancet Data (PFS 3.25 vs 1.77 mo, safety profile, caveats)
3. Who Is Eligible — And Who Is Not (biomarker + HER2 + line-of-therapy, list format)
4. The Access Path for International Patients (9-12 week Shanghai timeline with case-box)
5. Cost, Insurance, and the Comparison With US CAR-T (data table with 8 product/setting rows)
6. Earlier-Line and Other-Indication Trials Already Underway (4-trial table)
7. Satri-cel in the Broader Late-Line Gastric Cancer Picture (sequencing question)
8. What an International Patient Should Do Next (6-step practical guide)
9. The Bigger Picture — Cell Therapy as an Export Industry

## Tool-call breakdown (~17 calls, well under 35-call budget)

1. `terminal` — `ls news/$(date +%Y-%m-%d)-*.html` + `git status` + `git remote -v` + `ls references/pending-*.md` + `git log --oneline -5` (combined Step 0 pre-flight)
2. `terminal` — `curl bing.com/news/search?q=China+NMPA+drug+approval+June+2026&qft=interval%3d%229%22 | grep -oE ...` (1 grep returned 6+ valid URLs)
3. `terminal` — `cd news && grep -lE "(satri-cel|CT041|...)" *.html` (de-dup, 1 match on 05-09)
4. `terminal` — `curl https://pharmaphorum.com/news/carsgen-bags-world-first-approval-solid-tumour-car-t -o pharma_satri.html` + `python3` date verification + body extraction (combined)
5. `terminal` — `curl https://www.carsgen.com/en/news/20260622/ -o carsgen_pr.html` + body extraction (104KB confirmed)
6. `read_file` — `news/2026-06-22-raffles-medical-china-37000-foreign-patients-2025-inbound-medical-tourism.html` lines 1-120 (voice reference from most recent article)
7. `write_file` — `news/2026-06-23-carsgen-satri-cel-worlds-first-solid-tumor-car-t-gastric-cancer-nmpa-approval.html` (42KB, single write)
8. `terminal` — `python3 humanize_score.py news/2026-06-23-...html --site chinahospitalsguide --sitemap sitemap.xml` (first pass: 35/100 — banned pivotal x5, landscape x3, -ing x9, high word count)
9. `patch` — body: "The pivotal investigator team" → "The investigator team"
10. `patch` — table cell: "(pivotal)" → "(the registration trial)"
11. `patch` — body: "the pivotal data were generated" → "the registration data were generated"
12. `patch` — body: "competitive landscape for solid-tumor CAR-T" → "competitive field for solid-tumor CAR-T"
13. `patch` — sources list: "(the pivotal Phase 2 trial behind the approval" → "(the registration Phase 2 trial behind the approval"
14. `patch` — sources list: "broader CAR-T cost landscape" → "broader CAR-T cost scene" (initial fix; later retained as "scene" — verify whether script flagged "scene" as banned; final state score 90/100 suggests OK)
15. `patch` — H3: "The Pivotal Phase 2 Trial Behind the Approval" → "The Registration Phase 2 Trial Behind the Approval"
16. `patch` — H2: "Satri-cel in the Broader Late-Line Gastric Cancer Landscape" → "Satri-cel in the Broader Late-Line Gastric Cancer Picture"
17. `terminal` — `python3 humanize_score.py ...` (second pass: 90/100, only -ing tails + high word count notes remaining)
18. `terminal` — `python3 em_dash_check.py news/2026-06-23-...html` (17.2/1200, banned vocab 0, clean)
19. `terminal` — `grep -P '[^\x00-\x7F]' news/2026-06-23-...html` (only em-dash characters, no Chinese contamination)
20. `read_file` — `sitemap.xml` lines 1-15 (verify current top entry, sibling warning re-read safety)
21. `patch` — `sitemap.xml` insert new URL at top
22. `read_file` — `news/index.html` lines 230-260 (find insertion point after opening news-list div)
23. `patch` — `news/index.html` insert new article card at top of list
24. `terminal` — `git config user.email && git config user.name && git add news/...html sitemap.xml news/index.html && git status --short` (chain git config fix + stage)
25. `terminal` — `git commit -m "..." && git push origin master` (single chained call)
26. `terminal` — `sleep 180 && curl -s -o /dev/null -w "HTTP %{http_code}\n" https://chinahospitalsguide.com/news/2026-06-23-...html` (HTTP 200 verified)

(Actual count was 26 calls; my initial "17" estimate above undercounted the humanize loop iterations. Still well under 35-call budget target.)

## New patterns / pitfalls documented

### Pattern 1: carsgen.com as a verified working biotech IR source

The IR archive index at `https://www.carsgen.com/en/news/` lists recent press releases with date-coded URLs (`/en/news/YYYYMMDD/`). Each per-date page returns ~104KB of full body text including title in `<div class="title">`, full `<p>` paragraphs, named investigator quotes, and detailed methodology — same archetype as Akeso's `/en/media/akeso-news/` pattern. Use alongside Akeso for any Chinese biotech press release. Add to SKILL.md direct-fetch feasibility table.

### Pattern 2: pharmaphorum.com as a working primary source for global pharma news

The site returns ~94KB of full article body HTML including byline, named sources, and the publication date in `<time datetime="2026-06-22T15:54:53+00:00">`. Unlike FiercePharma (which returned a Cloudflare challenge page in the 06-23 run), pharmaphorum serves the full article body via a single curl. Use as the primary FiercePharma substitute whenever Bing News returns a FiercePharma URL.

### Pattern 3: "pivotal → registration" / "landscape → field/picture" banned-vocab fix for clinical research prose

When writing articles about clinical trial results (registration trials, Phase 3 readouts, NMPA approvals), the humanize_score.py script flags "pivotal" and "landscape". Two clean swaps work in clinical-research prose:

- `pivotal` → `registration` — `registration trial` is the actual FDA/NMPA term for the trial that supports marketing approval
- `landscape` → `field` or `picture` — 1-word substitutions that preserve meaning

The 06-23 article went from 35/100 → 90/100 in 7 small swaps. **General lesson:** when the score is in the 30-50/100 band on a clinical-research article and the only flagged banned-vocab words are `pivotal` and `landscape`, the fix is the 7-8 small swaps above. Do NOT restructure the prose.

### Pattern 4: Bing News recipe is working again on 2026-06-23

A single Bing News fetch returned 6+ distinct external China-medical URLs (FiercePharma, Yahoo Finance, pharmaphorum, ContractPharma, asiae.co.kr, genengnews.com, manilatimes PR Newswire) on the very first grep — confirming the "transient regression, not durable" pattern from the 06-16 pitfall. The recipe has now been verified working on 06-17, 06-18, and 06-23.

### Pattern 5: "Approved" is a richer news event than "NDA accepted"

The 06-23 satri-cel approval is a follow-up to the 05-09 satri-cel NDA acceptance. The two articles share anchor strings (satri-cel, Claudin18.2, CARsgen) but tell different stories:
- 05-09: "NDA accepted, approval expected late 2026" (a process story)
- 06-23: "approval received, Lancet data confirmed, access path open" (an outcome story)

The de-dup grep returned 1 match on the 05-09 article, but the framing and news event are distinct enough to ship a fresh article. **General rule for follow-up approval articles:** if the prior article was about a regulatory milestone (NDA acceptance, Phase 3 readout, IND clearance) and the current article is about the actual approval or labeling, the match is non-blocking — ship the new article with a clear "what changed" framing.

## Recommended action for 2026-06-24 cron run

No recovery state. Fresh research on next 24-48h hot topic. Candidates to consider:
- Phase 3 readouts at upcoming ASCO 2026 / ESMO Asia 2026 / ASH 2026 pre-abstract windows
- NMPA approvals in the late-June 2026 window (the Bing News 06-23 search surfaced Zai Lab NMPA approval, Harbour BioMed NMPA acceptance, and Vcare PharmTech eratrectinib TRK inhibitor NMPA marketing approval as not-yet-covered candidates)
- Follow-on Claudin18.2 / GPC3 / mesothelin solid-tumor CAR-T news from CarsGen or competitors (the 06-23 article named Pharchoice, Gracell as CarsGen's competitors — these are real candidates for follow-on coverage)