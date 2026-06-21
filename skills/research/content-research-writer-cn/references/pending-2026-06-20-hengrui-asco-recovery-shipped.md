---
date: 2026-06-20
status: shipped
type: recovery-mid-pipeline
---

# 2026-06-20 Cron Run: Hengrui ASCO 2026 — Recovery (Mid-Pipeline Cap-Hit Recovery, Shipped)

## Run Summary

**Cron iteration cap was hit mid-pipeline in the prior (2026-06-20) run, after Steps 1-5 (research → article → humanize 95 → sitemap patch → news/index.html insert) completed but BEFORE Steps 6 (git commit + push + verify).** The 2026-06-21 cron run (this one) detected the partial state at Step 0 pre-flight and shipped in 5 tool calls.

## Detection at Start of Run

```bash
ls news/$(date +%Y-%m-%d)-*.html
# Returned: 2026-06-20-hengrui-asco-2026-trastuzumab-rezetecan-colorectal-horizon-crc01.html (untracked)

git status
# modified: news/index.html
# modified: sitemap.xml
# Untracked: news/2026-06-20-...html
```

This is the FIFTH documented cap-hit failure mode — same variant as the 06-17/06-18/06-19 mid-pipeline cap-hits documented in the `content-research-writer-cn` skill. The state is: article written, humanize passed, sitemap + index.html updated, no commit, no push. The 5-call recovery recipe applies.

## Article State at Recovery (verified)

- **Title:** "Hengrui Pharma at ASCO 2026: 91 Studies, Four Phase III Readouts, and What It Means for Patients Coming to China"
- **Word count:** 2,880 (per `humanize_score.py`)
- **Em-dash count:** 52 → density ~21.7 per 1200 words (within 17-23 chinahospitalsguide baseline)
- **Humanize score:** 95/100 (only note: "high word count" — same as the 06-11 Antengene article; not actionable)
- **Sitemap:** 198 entries, top entry = 2026-06-20 article
- **news/index.html:** 2 matches for "2026-06-20" (the new card at top of article list)
- **Non-ASCII check:** clean (only legitimate single-byte chars like `—`, em-dashes from `&mdash;` entities; no CJK contamination)

## Recovery Steps Executed (06-21 cron run)

1. Pre-flight `ls news/$(date +%Y-%m-%d)-*.html` — found the 06-20 article as untracked file
2. `git status` — confirmed sitemap.xml and news/index.html modified, article untracked
3. `python3 scripts/humanize_score.py …` — confirmed score 95/100 (already passing threshold)
4. `git add news/...html sitemap.xml news/index.html && git commit -m "article: 2026-06-20 …"` — local commit `f98ae04`
5. **`git push origin master` — REJECTED:** remote had 3 new commits I didn't have (a MEMORY.md, an AGENTS.md/git-push-helper, and an SEO optimization of 23 pages). Required `git pull --rebase origin master` first, then re-push.
6. `git pull --rebase origin master` — clean rebase (no conflicts since none of the 3 new remote commits touched the article or the news/sitemap files)
7. `git push origin master` — succeeded, push SHA `6dfb9d5`
8. `sleep 180 && curl -s -o /dev/null -w "%{http_code}" …` — HTTP 200 verified
9. `curl … sitemap.xml` — confirmed top entry is the 06-20 article
10. `curl … news/ | grep -c "2026-06-20"` — returned 2 (top card in news index list)

Total: 10 tool calls for a full mid-pipeline recovery. Faster than the 06-17/06-18 variants because all the content-state was already correct (no humanize patches needed, no sitemap re-patches).

## Push-Rejection Pattern (NEW pitfall, verified 2026-06-21)

**The remote's master branch can advance between cron runs.** In this case, 3 new commits appeared on `origin/master` between the 06-20 run and the 06-21 run (a MEMORY.md, an AGENTS.md/git-push-helper.ps1, and a SEO batch optimization touching 23 pages' meta tags). The local branch was 1 commit ahead of origin, but origin was also 3 commits ahead of local — the cron run's commit was a fork off the previous origin HEAD, not a fast-forward.

**Recovery recipe:**
1. `git fetch origin master` — surface the new remote commits
2. `git log --oneline HEAD..origin/master` — list the commits you don't have
3. Inspect: are any of the new commits touching the same files you're about to commit (news/, sitemap.xml, news/index.html)? If yes, expect a rebase conflict. If no (the case here), the rebase will be clean.
4. `git pull --rebase origin master` — rebase your local commit on top of the new origin HEAD
5. `git push origin master` — should succeed
6. Verify with the standard `sleep 180 && curl ... 200`

**Why it works:** the cron runs are append-only on the article side (one new article per day, one new sitemap entry, one new index.html card). None of the 3 remote commits touched the article, the sitemap, or the news index — they touched MEMORY.md, AGENTS.md, git-push-helper.ps1, and 23 page meta tags. The rebase is a clean cherry-pick of the article commit onto the new origin HEAD, with no conflict markers in the working tree.

**Detection at Step 0:** the original pre-flight `git status` only checks "ahead of origin" (post-commit cap-hit detection). To also catch the new pattern (where remote has advanced past your local commit), add a `git fetch origin master` at the start of the recovery recipe before the `git log --oneline HEAD..origin/master` check. The `git push` failure on the first attempt is the natural signal that this pattern has fired, so it's a 1-call cost (the failed push) plus a 1-call cost (the rebase).

## Article Content Overview (Hengrui ASCO 2026)

**Topic:** Jiangsu Hengrui Pharma (one of China's largest innovative-drug companies) presented 91 oncology studies at ASCO 2026 (Chicago, May 29-June 2), including 11 oral talks and four late-stage Phase III readouts. The article unpacks all four Phase III readouts in clinical detail and frames them for international patients considering China for oncology care.

**The four Phase III readouts covered:**

1. **Trastuzumab rezetecan (HORIZON-CRC01)** — next-generation anti-HER2 ADC for HER2-positive, RAS/RAF wild-type metastatic colorectal cancer. Median PFS 5.5 months vs 2.8 months on standard chemo.
2. **Camrelizumab + rivoceranib + TACE (CARES-336)** — for unresectable hepatocellular carcinoma. Median PFS 11.1 months vs 8.3 months (systemic + locoregional combo).
3. **Fluzoparib + abiraterone (FUZUPRO)** — first-line metastatic castration-resistant prostate cancer. Median rPFS 24.8 months vs 19.9 months.
4. **SHR-A2102 (anti-Nectin-4 ADC) + adebrelimab (PD-L1)** — perioperative muscle-invasive bladder cancer. pCR 48.1%, pathological downstaging 59.3% (including renal-dysfunction patients).

**Why this topic is shippable for chinahospitalsguide.com:** Hengrui Pharma is one of the most active Chinese innovators in oncology, and the 2026 ASCO meeting was their most extensive single-company dataset ever. The four late-stage readouts span four of the most common cancer types globally (colorectal, liver, prostate, bladder), so the article has relevance to a wide international patient base. The trastuzumab rezetecan story is particularly relevant — it's a next-gen ADC targeting the same HER2 antigen that trastuzumab deruxtecan (Enhertu) targets, and the China-domestic version will be significantly cheaper for international patients who can access it via Hainan Boao Lecheng or commercial Shanghai/Beijing channels.

**Source verification:** ASCO 2026 official press materials + Hengrui Pharma's published abstracts (the 06-20 article cites the 91-study count, the 11 oral talks, and the specific PFS/pCR data points for each of the four Phase III readouts).

## New Patterns Discovered This Run

1. **Mid-pipeline cap-hit is now a 5-variants class** (06-17 sitemap-not-index, 06-18 article-only-no-humanize, 06-19 recovery-of-18, 06-20 article-sitemap-index-no-commit [this run], 06-14 post-commit-cap-hit [different class]). The unified detection is `ls news/$(date +%Y-%m-%d)-*.html 2>/dev/null` plus `git status`. The recovery cost is 5-10 tool calls depending on which sub-step was missed.
2. **Remote `origin/master` can advance between cron runs** (3 new remote commits in this case: MEMORY.md, AGENTS.md, SEO batch). The cron workflow needs to handle non-fast-forward pushes via `git pull --rebase` and re-push. The 1-2 call cost is acceptable as long as Step 0's `git status` doesn't pre-empt the conflict.
3. **The 06-20 article's humanize score of 95/100 on a 2,880-word article** confirms the long-article em-dash cap is non-actionable for chinahospitalsguide: 52 raw em-dashes = 21.7/1200 = inside the 17-23 baseline. The script's em-dash penalty is a false negative for any article over 2,400 words, as documented in the 06-08 pitfall.

## Recommended Action for 2026-06-22 Cron Run

**No recovery state to pick up — this run is a clean ship.** The 06-20 article is live at https://chinahospitalsguide.com/news/2026-06-20-hengrui-asco-2026-trastuzumab-rezetecan-colorectal-horizon-crc01.html and the working tree is clean (commit `6dfb9d5` on `origin/master`). The next run should start fresh research on 2026-06-22's hot topic.

**Suggested research direction for 2026-06-22:**
- ESMO 2026 Gastrointestinal Cancer Congress (typically late June/early July) — abstracts published around this time
- EHA 2026 follow-on coverage — second/third wave of Chinese biotech allogeneic CAR-T data
- Akeso / Hengrui / BeiGene pipeline updates following ASCO 2026
- NMPA approvals issued in the 2026-06-15 to 2026-06-22 window

## Final State

- ✅ Article: `news/2026-06-20-hengrui-asco-2026-trastuzumab-rezetecan-colorectal-horizon-crc01.html` (2,880 words, humanize 95/100)
- ✅ Sitemap: 198 entries, top entry is the 06-20 article
- ✅ News index: 06-20 article at top of list
- ✅ Commit: `f98ae04` local, `6dfb9d5` on `origin/master` (after rebase onto new remote HEAD `9c0dfae`)
- ✅ Live URL: https://chinahospitalsguide.com/news/2026-06-20-hengrui-asco-2026-trastuzumab-rezetecan-colorectal-horizon-crc01.html — HTTP 200
- ✅ Sitemap live: 06-20 article confirmed as top entry
- ✅ News index live: 06-20 article confirmed as top card
