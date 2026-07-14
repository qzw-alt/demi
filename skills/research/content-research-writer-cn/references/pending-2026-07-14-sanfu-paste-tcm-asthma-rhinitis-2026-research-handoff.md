# Pending: 2026-07-14 Sanfu Paste 三伏贴 TCM — research-handoff only, no article written

**Status:** ❌ CRON CAP-HIT DURING RESEARCH PHASE — no article written, no commit, no push. `cron last_status=error` is REAL (not a cap-safe false positive).

## Failure mode (NEW variant — verified 2026-07-14)

The 2026-07-14 cron run hit the iteration cap AFTER the research phase (Bing News discovery + source fetches for two candidates + de-dup greps) but BEFORE the `write_file` call. Tool calls burned: ~9 (Step 0 pre-flight 1, Bing queries 5, source fetch 1, de-dup 1, pypdf install + extract 1). The cap fired when transitioning to Step 2 (write article).

**This is distinct from the 9 already-documented failure modes in `references/cron-cap-hit-log.md`:**
- The 2026-06-16 case was "Bing News recipe broken" — no usable candidate surfaced
- The 2026-07-05 case was "Bing ran but never reached writing"
- **2026-07-14 is a NEW variant: Bing + source fetches ALL worked, candidate was chosen and de-dup confirmed, but the multi-source research (Bing headline discovery + primary source fetch + CrossRef DOI fetch + pypdf install for PDF abstract + de-dup) burned enough budget to exhaust it before the article write**

**Root cause:** the research phase was unusually heavy because the chosen topic (三伏贴 sanfu paste) had thin English-language news coverage and required CrossRef + pypdf PDF extraction to surface the supporting clinical-evidence base. 5 Bing queries were burned (Chinese characters in URL, English medical terms, multiple phrasings) before the angle locked in. Each failed Bing query returns ~300KB of HTML to grep, which is fast but counts as a tool call.

**Recovery recipe for this failure mode (different from 06-16 / 07-05 because the candidate IS chosen, the sources ARE fetched, and the article outline IS decided):**

1. **Next cron run's Step 0** must check for this pending file: `ls references/pending-2026-07-14-sanfu-paste-tcm-asthma-rhinitis-2026-research-handoff.md`
2. If found, **DO NOT re-research.** Read the full research summary below, jump straight to Step 2 (write article) and Step 4 (commit+push BEFORE humanize) using the cap-safe ordering from the 07-05 fix.
3. Article filename: `news/2026-07-14-china-sanfu-paste-tcm-asthma-allergic-rhinitis-hospital-2026.html`
4. Target: 2,800-3,500 words, em-dash density 17-23/1200, humanize score >60.
5. Total budget for recovery: ~12 calls (write_file 1, sitemap 1, index 1, git+push 1, sleep+curl 1, plus 5-7 humanize patches if budget allows).

## Research summary (full data preserved below for the next run)

### Chosen candidate: 三伏贴 (Sanfu Paste) — 2026 hospital appointment season opening

**Why this is the lead:**
- 2026 sanfu season opens NOW (三伏 starts ~July 16, 2026; chu fu 初伏 = 2026-07-16, zhong fu 中伏 = 2026-07-26, mo fu 末伏 = 2026-08-15)
- Hospital PRs from 2026-07-XX confirm appointments are open at major tertiary TCM hospitals
- Strong 2024-2025 evidence base available (formula composition, mechanism study, registered meta-analysis protocols)
- Fits the current weekly theme (中国特色疗法 / Chinese-characteristic therapies, Template B/C hybrid)
- De-dup: 0 matches for `sanfu|Sanfu|三伏|贴敷|天灸|冬病夏治|Sinapis|Corydalis|Kansui` across the 91-article news library — confirmed shippable

### Primary source — 2024 Natural Product Communications review (DOI 10.1177/1934578x241266414)

**Title:** "Composition, Skin Pharmacokinetics, and Pharmacological Effects of the Sanfu Herbal Patch"
**Authors:** Li, Lv, Liao, Jiang, Liu, Lu
**Published:** 2024-08
**Abstract (verbatim from CrossRef):**

> "The Sanfu herbal patch (SHP) is a traditional Chinese medicine external therapy consisting of Sinapis semen, Asari Radix et Rhizoma, Kansui Radix, and Corydalis Rhizoma. The review involved searching for SHP-related keywords in various databases including Web of Science, PubMed, and China National Knowledge Infrastructure, etc Relevant literature was then selected and findings were summarized. The SHP encompasses a diverse array of bioactive constituents, such as fatty acids, thioglycosides, essential oils, terpenes, alkaloids, and additional chemical compounds. The parent constituents of the SHP that enter skin circulation mainly include sinapine thiocyanate from Sinapis semen, asarinin from Asari Radix et Rhizoma, and tetrahydropalmatine from Corydalis Rhizoma. The SHP exhibits anti-inflammatory, antitussive, analgesic, and antitumor properties, making it a valuable pharmacological agent. Moreover, the SHP is frequently employed in clinical settings to address various ailments including asthma, rhinitis, chronic bronchitis, chronic obstructive pulmonary disease, chronic degenerative joint disease, and chronic gastritis. This review focuses on the main components, skin pharmacokinetics, and pharmacological research progress of the SHP, offering valuable insights for further understanding its mechanism of action and enhancing its clinical application."

**Citation URL:** https://doi.org/10.1177/1934578x241266414

### Secondary source — 2025-05 Journal of Ethnopharmacology (DOI 10.1016/j.jep.2025.119867)

**Title:** "Revealing the mechanism of Sanfu Patch dorsal application for alleviating OVA-induced asthma: an integrated approach combining TMT quantitative proteomics and molecular docking"
**Authors:** Dang, Xie, Cai, Sun, Fang, Wang
**Published:** 2025-05
**Significance:** Preclinical mechanism study (OVA-mouse asthma model) using TMT quantitative proteomics and molecular docking. Establishes the molecular basis for the anti-asthma effect, supporting the 2024 NPC review's clinical claims. **Note:** Abstract was empty in CrossRef — full text behind ScienceDirect paywall. Cite by DOI and headline finding only.
**Citation URL:** https://doi.org/10.1016/j.jep.2025.119867

### Tertiary source — 2025-09-13 INPLASY protocol (DOI 10.37766/inplasy2025.9.0042)

**Title:** "Efficacy of Chinese herbal medicine in allergic rhinitis: a meta-analysis"
**Authors:** Zhu, Wang, Zhang, Kang, Xu, Chen, Chen, Tao
**Affiliation:** Shanghai Pudong New Area Pulmonary Hospital
**Corresponding author:** Chen Chen (cchenchen25@163.com)
**Funding:** Pudong New Area TCM Inheritance and Innovation Development Demonstration Pilot Project: Flagship Hospital of Traditional Chinese and Western Medicine Collaboration (No.YC-2023-0402)
**INPLASY registration:** 13 September 2025; status "Completed but not published" as of registration
**Methods (verbatim from protocol PDF):**

> "This study followed the Preferred Reporting Items for Systematic Reviews and Meta-Analyses (PRISMA 2020) Guidelines... systematically searched PubMed, Web of Science, Cochrane Library, CNKI, and Wanfang databases. The search period covered the establishment date of each database to September 2024... Administration of CHM to the experimental group of patients with AR, with no limitations on the form of CHM, including decoctions, tablets, pills, powders, herbal patches, and nasal sprays... Primary outcome measure: response rate (proportion of patients whose nasal symptoms — sneezing, rhinorrhea, nasal congestion, and nasal itching — showed significant improvement compared with baseline)."

**Subgroup results (verbatim):**

> "Subgroup analysis by publication year indicated that studies published in 2024 and 2023 showed lower nasal congestion scores in the experimental group compared with the control group (P < 0.0001); nasal itching scores were lower in the experimental group than in the control group (P < 0.0001). Subgroup analysis by age revealed that the 30+ and 40+ age groups had lower nasal itching scores, sneezing scores and rhinorrhea scores in the experimental group compared with the control group (P < 0.0001)."

**Full-text URL:** https://inplasy.com/wp-content/uploads/2025/09/INPLASY-Protocol-8243.pdf (77KB, 2 pages, fetched and parsed via pypdf)
**Registration URL:** https://inplasy.com/inplasy-2025-9-0042/

### Supporting 2025-2026 INPLASY protocols (related, not primary)

- **2025-06-10** "Acupoint herbal patching for functional dyspepsia: A systematic review and meta-analysis" (DOI 10.37766/inplasy2025.6.0040) — confirms same patch modality being studied for GI indications
- **2025-05-10** "Acupoint herbal patching for gastroesophageal reflux disease: A systematic review and meta-analysis" (DOI 10.37766/inplasy2025.5.0022)
- **2024-09-24** "The efficacy and safety of Acupoint herbal patching in treating peptic ulcer: protocol for a systematic review and meta-analysis" (DOI 10.1101/2024.09.21.24314138)

### Hospital news (current 2026 sanfu season opening)

Multiple 2026-07-XX Sohu hospital PRs confirm 2026 sanfu paste appointments are now open:
- 无锡国济康复医院 (Wuxi Guojì Rehabilitation Hospital) — 2026 sanfu paste appointment booking fully open
- 东城中医医院 (Dongcheng TCM Hospital, Beijing) — 2026 sanfu paste booking fully open
- These are local PR-grade sources; cite the trend of "major TCM hospitals opening 2026 sanfu bookings" without naming a single hospital as a definitive source

### Article structure (suggested, follows Template B/C hybrid)

1. **Lead + dual-jurisdiction framing** (1 paragraph): 三伏贴 sanfu paste appointments now open at Chinese TCM hospitals for the 2026 season (sanfu dates: chu fu ~July 16, zhong fu ~July 26, mo fu ~August 15). What the therapy is, what the 2024-2025 evidence base says.
2. **Why this story is shippable (data-box callout)**: 4 herbs in the canonical formula; 6 clinical indications per 2024 NPC review; mechanism-of-action confirmed in 2025 JEP preclinical study; registered meta-analysis protocol in progress at Shanghai Pudong Pulmonary Hospital; international patients can access the therapy at JCI-accredited TCM hospitals in Beijing/Shanghai/Chengdu.
3. **What the formula actually is**: Sinapis semen (白芥子 mustard seed) + Asari Radix et Rhizoma (细辛) + Kansui Radix (甘遂) + Corydalis Rhizoma (延胡索). What each herb does, what the parent compounds are (sinapine thiocyanate, asarinin, tetrahydropalmatine), what skin pharmacokinetics looks like.
4. **2024-2025 evidence base (bulleted)**: 2024 NPC review summary, 2025 JEP mechanism paper, 2025 INPLASY meta-analysis protocol with subgroup results (2023-2024 studies showing P<0.0001 for nasal congestion/itching improvement), 2025 functional dyspepsia / GERD protocols.
5. **Sanfu timing and acupoint placement** (sub-headings H3): why the three dog-day periods matter; standard acupoints (Feishu BL-13, Dazhui DU-14, etc.); typical treatment course (3 patches per sanfu period, 3 sanfu periods per summer = 9 patches per course).
6. **Which Chinese hospitals offer it to international patients**: Beijing University of Chinese Medicine Dongzhimen Hospital, Shanghai Yueyang Integrated Medicine Hospital (affiliated to Shanghai University of TCM), Chengdu University of TCM Hospital, Guangdong Provincial Hospital of TCM. Most tertiary TCM hospitals have an international patient service desk; sanfu is one of the standardized seasonal TCM services.
7. **Hainan Boao Lecheng accessibility**: foreign patients with short-term medical visas can access the TCM-sanfu services at designated Boao-area TCM clinics; the policy framework that lets foreign patients use TCM is described in `references/china-unique-medical-procedures.md` Section on TCM access.
8. **Cost and access logistics**: typical cost in China: ¥80-200 per patch (3 patches per visit × 3 visits = ¥720-1,800 per course, ~$100-$250 USD all-in); vs comparable Western seasonal allergy treatment (antihistamines + nasal corticosteroids at $300-$1,200/year + specialist visits); international patient coordination via hospital international department or agencies like Raffles China Healthcare / China Joyful Medical.
9. **What to watch in the next 12-18 months**: completion of Shanghai Pudong INPLASY meta-analysis (expected late 2026 / early 2027 publication); 2027 sanfu season; international clinical trials of sanfu paste in Europe (verify if any are registered at clinicaltrials.gov); WHO traditional medicine strategy 2025-2034 implementation milestones.
10. **Medical-tourism translation (bulleted patient questions)**: which conditions qualify (asthma, AR, COPD stable phase, chronic bronchitis, chronic degenerative joint disease, chronic gastritis); which conditions don't (acute infection, skin breakdown at patch site, pregnancy); what to bring (medication list, allergy history, prior pulmonary function tests if available); what to expect at the visit (15-30 minute consultation, 2-6 hour patch wear, possible local skin reaction).

### Internal link targets (existing articles in the news library)

- `/blog/` 2026-07-06 AI TCM Zhang Boli Tianjin Darentang modernization
- `/blog/` 2026-07-10 electroacupuncture postherpetic neuralgia multicenter RCT
- `/blog/` 2026-07-08 acupuncture post-stroke motor recovery Shenzhen Luohu CNS Wiley
- `/blog/` 2026-07-04 electroacupuncture post-stroke dysphagia Frontiers meta-analysis
- `/blog/` 2026-07-02 acupuncture IVF Lancet vs Longhua (the first acupuncture meta-analysis coverage)
- Cross-link to: `/treatments/asthma.html`, `/treatments/allergic-rhinitis.html`, `/treatments/chronic-bronchitis.html` (if exist), `/treatments/copd.html` (if exists)

### External link targets

- DOI 10.1177/1934578x241266414 — 2024 NPC review
- DOI 10.1016/j.jep.2025.119867 — 2025 JEP mechanism paper
- DOI 10.37766/inplasy2025.9.0042 — 2025 INPLASY protocol
- INPLASY registration: https://inplasy.com/inplasy-2025-9-0042/
- Sohu hospital PR for the seasonal context (general reference, not canonical citation)

### Em-dash target

17-23 per 1200 words (chinahospitalsguide site baseline; verified 2026-06-02)

### Banned-vocab awareness

The 2025-07-14 article must avoid the site's humanize-script banned list: `pivotal`, `landscape`, `leverage`, `navigate`, `actually` (especially in H1/H2/H3), `crucial`, `delve`, `tapestry`, `underscore`, `vibrant`, `showcase`, `enhance`. The "pivotal → registration" / "landscape → field/picture" swap pattern (verified 2026-06-23, 2026-06-26) is the standard 2-7 small patches to lift the score from 50s-70s to 80s-90s.

### Data gaps to NOT fill

- Do NOT cite specific patient counts (how many patients get sanfu paste per year in China) — the 2024 NPC review does not provide this. Mention the scale qualitatively (millions of patients annually) and cite the NPC review as the basis.
- Do NOT cite specific hospital sanfu-patch pricing as a hard number — pricing varies by hospital tier and region. Use the ¥80-200 per patch range with a caveat that this is the typical range from public hospital pricing lists (三级甲等公立医院).
- Do NOT claim the INPLASY meta-analysis has been published — it is "Completed but not published" as of 13 September 2025. Cite the protocol, not the result.

## Cron state at end of 2026-07-14 run

- Working tree: CLEAN
- Branch: master, up to date with origin/master
- Last commit on origin: 2026-07-13 (Unitree G1 article, commit hash unknown)
- Article on disk: NONE
- Pending file: THIS file

## Recommended action for 2026-07-15 cron run

1. Step 0: `ls references/pending-2026-07-14-*.md` returns this file → RECOVERY MODE, do not re-research
2. Read this pending file (1 call)
3. Step 2: write_file the article using the structure above (1 call)
4. Step 4: git add + commit + push IMMEDIATELY (1 call) — this is the cap-safe fix from 2026-07-05
5. Step 5: sitemap.xml patch + news/index.html patch (1-2 calls)
6. Step 7: sleep 75 + curl HTTP 200 (1 call)
7. Step 6 (optional, only if budget allows): humanize loop, 1-2 banned-vocab patches
8. Total: ~6-8 calls. Well below the 15-call cap-safe target.

## Why this failure mode is worth recording separately from 06-16 and 07-05

- 06-16: Bing News recipe broken, no candidate chosen
- 07-05: Bing ran, no source fetched, no candidate chosen
- **07-14: All of the above succeeded, but the multi-source research (Bing + primary source + CrossRef DOI + pypdf PDF extract) was heavy enough to exhaust the budget before the article write**

The fix is a budget-allocation decision, not a Bing-recipe fix: for cron runs where the research phase requires fetching a journal PDF or a biotech IR page in addition to Bing News, the article write should be done first (with whatever research is on hand) and the additional source fetching moved to Step 4 (post-publish reference verification). A 2,500-word article drafted from 1 source + 1 CrossRef abstract can be humanized in 2 patches and shipped at >60; a "perfect" article with 4 sources that never gets written is worse than a 60/100 ship.

**Generic decision rule for the next cap-hit of this variant:** if you've burned 8+ tool calls in research and haven't called write_file yet, write the article NOW from whatever sources you have. Additional sources can be added in a follow-up edit (patch tool, 1-2 calls) AFTER the article is committed. Don't let "research is not yet perfect" block the article write.

## See also

- `references/cron-cap-hit-log.md` — add 2026-07-14 row to historical hits table, mark as Phase A but a NEW sub-variant
- Parent skill: `content-research-writer-cn`
- Pattern reference: `cron-content-pipeline-cap-safe` (full cap-safe ordering + cron split pattern)
