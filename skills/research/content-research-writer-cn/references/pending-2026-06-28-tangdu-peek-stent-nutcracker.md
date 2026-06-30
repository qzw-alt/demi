# Pending recovery: 2026-06-28 Tangdu Hospital 3D-Printed PEEK Stent

**Status:** Article written (3,821 words), 3 `actually` H2 patches done, 8 em-dash-insertion patches done, density at ~9/1200 (still under the 17-23/1200 baseline). NOT committed, NOT pushed, NO sitemap/index patches. Cron iteration cap fired during the humanize loop.

**Cron run date:** 2026-06-28
**Article filename:** `news/2026-06-28-tangdu-hospital-3d-printed-peek-extravascular-stent-nutcracker-syndrome.html`
**Article word count:** 3,821
**Em-dash density at cap-hit:** ~9/1200 (target: 17-23/1200)
**Banned-vocab hits at cap-hit:** 0 `actually` in H2 (3 patched), 0 in body prose that need fixing
**Untracked:** YES (`git status` shows the file as untracked, no ahead-of-origin state)

## Source verification (all complete before cap-hit)

- **He Dali et al. 2020 (canonical 28-patient cohort)** — verified via CrossRef + Frontiers HTML fetch. DOI `10.3389/fbioe.2020.00732`. Full abstract extracted from `<meta name="description">`. Frontiers paper is open access.
  - 28 patients (25 men + 3 women), age 18-37 (mean 23.6)
  - December 2017 to May 2019 enrollment
  - Laparoscopic 3D-printed PEEK extravascular stenting
  - Follow-up 6-24 months (median 16.3)
  - 100% technical success
  - All symptoms resolved or improved
  - 2 patients had mild perioperative complications (lymphatic leakage)
  - No stent migration, no thrombosis across entire follow-up
  - Authors at Department of Urology, Tangdu Hospital, FMMU (Fourth Military Medical University)

- **Wang Qi et al. February 2026 (reoperative robotic-assisted case)** — verified via CrossRef. DOI `10.1016/j.jvscit.2025.101985`. Journal: *Journal of Vascular Surgery Cases, Innovations and Techniques*. Authors: Wang Qi, Xin Jiayan, Zhang Minghao, Wang Yong.

- **Tangdu Hospital site** — confirmed via `hospitals.json` listing (specialty: Vascular Surgery, Interventional Radiology; known for NCS diagnosis and treatment).

## Suggested recovery recipe (~7 tool calls)

1. `terminal` — `head -50 news/2026-06-28-tangdu-hospital-3d-printed-peek-extravascular-stent-nutcracker-syndrome.html` and `tail -30 news/...html` — verify the file is complete, not truncated
2. `write_file /tmp/check_dash.py` with the entity-decoding variant — confirm actual em-dash density (the bundled `em_dash_check.py` returns 0 on `&mdash;`-encoded articles)
3. `terminal` — `python3 /tmp/check_dash.py` — get real density. If <17/1200, do 1-2 more clinical-parenthetical `patch` calls to lift it. If budget is tight, accept the score as-is and ship.
4. `terminal` — `python3 /home/ubuntu/.hermes/skills/creative/programmatic-seo/scripts/humanize_score.py news/2026-06-28-tangdu-hospital-3d-printed-peek-extravascular-stent-nutcracker-syndrome.html --site chinahospitalsguide` — get final score for the record
5. `patch` `sitemap.xml` — insert new entry at top of news section (use priority 0.6 per the 06-27 SEO-batch convention)
6. `patch` `news/index.html` — insert new article card at top of news list
7. `terminal` — `git config user.email "hermes@chinahospitalsguide.com" && git config user.name "Hermes Agent" && git add news/2026-06-28-tangdu-hospital-3d-printed-peek-extravascular-stent-nutcracker-syndrome.html sitemap.xml news/index.html && git commit -m "article: 2026-06-28" && git push origin master` — chained (may need `git fetch origin master && git pull --rebase origin master` first if remote has advanced)
8. `terminal` — `sleep 180 && curl --max-time 30 -s -o /dev/null -w "HTTP %{http_code}\n" https://chinahospitalsguide.com/news/2026-06-28-tangdu-hospital-3d-printed-peek-extravascular-stent-nutcracker-syndrome.html` — verify

## Internal/external links to verify after commit

**Internal links used in article (all confirmed exist in the repo):**
- `treatments/nutcracker-syndrome.html` — full hospital comparison
- `hospitals-in-xian-for-international-patients.html` — Xi'an hospital comparison
- `news/2026-06-05-china-ai-dental-tourism-russian-patients-heihe.html`
- `news/2026-06-07-5G-remote-surgery-tongji-wuhan-hyderabad.html`
- `news/2026-06-22-raffles-medical-china-37000-foreign-patients-2025-inbound-medical-tourism.html`
- `blog/china-unique-medical-procedures-guide.html`

**External links in article (all peer-reviewed papers):**
- DOI `10.3389/fbioe.2020.00732` (He et al. 2020)
- DOI `10.1016/j.jvscit.2025.101985` (Wang Qi et al. 2026)
- DOI `10.1186/s12893-026-03848-6` (Hamouda et al. 2026)
- DOI `10.1089/end.2023.0250` (Farhi et al. 2024)
- DOI `10.4081/pmc.2025.353` (Chiarenza et al. 2025)
- DOI `10.4103/0366-6999.246075` (Guo et al. 2018)

## Banned-vocab decisions already made

- 3 `actually` H2 hits patched: "What nutcracker syndrome actually is" → "What nutcracker syndrome is"; "How a 3D-printed extravascular stent actually works" → "How a 3D-printed extravascular stent works"; "The 28-patient cohort, and what it actually showed" → "The 28-patient cohort, and what it showed"
- No `landscape` / `pivotal` / `leverage` / `navigate` hits in current draft (verified pre-cap)

## Lesson for future fresh drafts (the 06-28 takeaway)

**Front-load publish plumbing BEFORE deep humanize iteration when the cron iteration cap is approaching.** The 06-28 run burned 7-8 tool calls on em-dash-insertion patches while density was still at 9/1200, with no commit/push. If the run had instead done:
- 1 call: write article
- 1 call: patch sitemap
- 1 call: patch news/index.html
- 1 call: commit + push (chained)
- 1 call: sleep + curl verify (chained)
- THEN add em-dashes if budget allowed

The article would have shipped at the natural ~70-80/100 score, not uncommitted at 9/1200 density. **A published article at 55/100 is strictly better than an uncommitted article at 90/100.** The cap counts tool calls, not score progress.