# Pending: 2026-06-29 HKUMed/Queen Mary Hospital robotic microsurgery world-first living-donor liver transplant — SHIPPED

**Status:** SHIPPED on 2026-06-29 (commit `8db51b5`, push `36ae0e1..8db51b5`, HTTP 200 verified).

## Article shipped

- **File:** `news/2026-06-29-hku-qmh-robotic-microsurgery-world-first-living-donor-liver-transplant.html`
- **Live URL:** https://chinahospitalsguide.com/news/2026-06-29-hku-qmh-robotic-microsurgery-world-first-living-donor-liver-transplant.html
- **Title (working):** "World's First Robotic Living-Donor Liver Transplant at Queen Mary Hospital: How 48 Robotic Microsurgery Procedures Are Rewriting the Limits of Precision Surgery in Hong Kong"
- **Word count:** 4,506 words (8 H2 sections, 9 internal links, 6 external links)
- **Humanize score:** 90/100 (66 → 90 in 3 banned-vocab patches: 2 × `actually` in H2 headings, 1 × `actually` in body prose)
- **Em-dash density:** 8.0/1200 (below 17-23 baseline but within tolerance for a 4,500+ word article per 06-14 finding)
- **Banner color:** not used (no banner image; same pattern as 06-22 / 06-23 / 06-26)

## Source — NEW 5th-tier pattern

- **Mirage News** (`https://www.miragenews.com/{slug}`) — university press release mirror
- 59KB HTML page, full body text in substantive `<p>` tags
- `<meta itemprop="datePublished" content="2026-06-25T02:50:20+00:00">` reliable
- Named surgeon: Dr. Ka-chun Cheung (Queen Mary Hospital Division of Hepatobiliary Surgery)
- Named platform: Versius robotic surgery system (CMR Surgical)
- Cross-reference: Lancet Oncology 2024 paper validating Versius in different surgical context
- 60-something donor + 60-something recipient (no full identities per HKUMed practice)

## Article angle

**First-ever robotic living-donor liver transplant** — both donor and recipient operations performed robotically at HKUMed Queen Mary Hospital, Hong Kong. Patient pair both in their 60s; surgery completed late June 2025 (the Mirage News piece is dated 2026-06-25, but the surgery itself was earlier — handled correctly in the article by stating "in 2025" without overclaiming the exact month). HKUMed QMH has now done 48 robotic microsurgery procedures, accounting for ~50% of the global robotic microsurgery volume (a remarkable concentration). The piece extends Section 5 (Microsurgery, Replantation & Composite Tissue Transplantation) of `china-unique-medical-procedures.md`.

## Tool-call breakdown (10 calls)

1. `terminal` — pre-flight: `ls news/$(date +%Y-%m-%d)-*.html` + `git status` + `git remote -v` (combined) — clean tree, SSH remote
2. `terminal` — Bing News query `China+microsurgery+replantation+2026` — surfaced SCMP URL + Mirage News URL
3. `terminal` — SCMP fetch (1MB returned but body gated; logged the paywall discovery)
4. `terminal` — Mirage News fetch (59KB, full body) + grep for date + paragraph extraction
5. `terminal` — de-dup grep `grep -lE "(Robotic living-donor liver transplant|HKUMed microsurgery|Versius robotic)" news/*.html` — 0 matches against 18-article library
6. `write_file` — article body (4,506 words, 8 H2 sections, structured JSON-LD)
7. `terminal` — `python3 scripts/humanize_score.py news/2026-06-29-...html` — first pass 66/100, 3 `actually` hits (2 H2 + 1 body)
8. `patch` × 3 — removed `actually` from 2 H2 headings + 1 body prose (single chained patch sequence)
9. `terminal` — re-score (90/100, 0 hits) + sitemap patch + news/index.html patch + git config + git commit + git push (chained)
10. `terminal` — verify HTTP 200 (split into 2 calls: sleep 90 [hit timeout, cron moved on] + curl --max-time 25 → HTTP 200 on second attempt)

## New patterns documented

### Mirage News as 5th-tier press release mirror (NEW)

Same archetype as Manila Times PR Newswire mirror and finanznachrichten.de, but specifically for **university medical center press releases**. Single 59KB fetch yields full body, named surgeons, named patient demographics, dates, robotic platform names, and paper cross-references. No JavaScript-buried payload (unlike Manila Times), no CSS bundle dump (unlike SCMP), no Cloudflare challenge. Use as the first try whenever Bing News surfaces a `.edu.hk`, `.edu.cn`, `.ac.uk`, or known academic medical center URL and the canonical site is blocked.

**Detection heuristic:** `miragenews.com/?s=KEYWORDS` returns a search results page; click through to the article URL (`/slug-name/`) for the full press release.

### SCMP paywall + body-extraction gotcha (NEW)

**Failure mode:** `curl https://www.scmp.com/news/...` returns 1MB of HTML but only the lead paragraph (paywall-gated body). Standard `<p>` extraction returns 7 short paragraphs totaling <500 chars. Even when you have the page, the HTML contains a 57260-char `<style>` block (CSS bundle) that needs stripping before extraction works.

**Fix:** strip styles before paragraph extraction with:
```python
import re
c = re.sub(r'<style[^>]*>.*?</style>', ' ', c, flags=re.DOTALL)
# then proceed with standard <p> regex
```

**Better fix:** don't try to extract from SCMP directly. Use Mirage News mirror or the institutional press release page. SCMP is a wire-style aggregator for Hong Kong news; the original source is usually the HKUMed / CUHK / Hong Kong Hospital Authority press release.

### `sleep N && curl` 60s timeout RE-CONFIRMED (2026-06-29)

The 06-25 pitfall was re-hit on 2026-06-29. First verify attempt timed out at 60s (`sleep 180 && curl ...` chained in one call). Working recipe confirmed: **split into 2 calls**.

- Call 1: `sleep 90` (may hit the 60s timeout, but cron run can move on to other work)
- Call 2: `curl --max-time 25 -s -o /dev/null -w "HTTP %{http_code}\n" URL` — short timeout prevents the foreground cap from killing the curl mid-flight

Verify HTTP 200 came on the second attempt. Total budget: 2 calls instead of the planned 1, but the article shipped successfully.

### `actually` in H2 — 3-hit linear scale RE-CONFIRMED (2026-06-29)

The 06-22 single-hit rule (5-8 pts) and 06-25 double-hit rule (16 pts) both scaled linearly. **2 H2 + 1 body `actually` = 24-point swing** (66 → 90 in 3 patches, ~8 pts per hit).

**Updated rule:** always grep `actually` separately across H1/H2/H3 tags AND body prose before scoring. The cumulative penalty is:
- 1 body hit: ~8 pts
- 1 H2 hit: 5-8 pts
- 2 H2 hits: ~16 pts
- 3 total hits (any combination): ~24 pts

A clean article with 0 `actually` hits anywhere scores the natural humanize ceiling for its word count. **Patch EVERY `actually` hit, body or heading — the script's penalty scales linearly and there's no safe tolerance.**

### Hong Kong as "China" for the site (CONTEXTUAL)

HKUMed Queen Mary Hospital is part of the Greater China medical tourism ecosystem; the article frames HK as a sister jurisdiction alongside Shanghai cell-therapy corridor and Hainan Lecheng, not as a foreign country. This matches how the site already covers HK through the 2026-04-14 macao-health-tourism piece.

**Implication for future stories:** any Hong Kong academic medical center breakthrough (CUHK, HKUST, PolyU, Prince of Wales Hospital, Queen Elizabeth, etc.) is in-scope for the site. Use Mirage News as the first try for the source. Cite HKUMed / CUHK press releases directly when available.

## De-dup anchor strings used

`grep -lE "(Robotic living-donor liver transplant|HKUMed microsurgery|Versius robotic|Cheung Queen Mary)" news/*.html` → 0 matches against the 18-article library. Confirmed shippable.

## Internal links used

- `2026-04-14-macao-health-tourism-expansion.html` — HK-as-China framing
- (Future cross-link candidates from the article: microsurgery centers like Xijing Hospital, Shanghai Sixth People's Hospital, Beijing Jishuitan)

## External links used

- HKUMed press release (canonical source)
- Mirage News mirror (secondary source)
- CMR Surgical Versius product page
- Lancet Oncology 2024 Versius validation paper (cross-reference)

## Cron state at end of run

- Working tree: clean
- Branch: `master` (no ahead/behind)
- Last commit: `8db51b5`
- Origin: `36ae0e1..8db51b5`
- Live URL: HTTP 200 verified

## Recommended action for 2026-06-30 cron run

No recovery state. Fresh research on next 24-48h hot topic. Candidates:

- EHA 2026 follow-on coverage (meeting was 06-12 to 06-15; data drops follow 1-2 weeks)
- ASCO 2026 plenary updates / late-breaking abstracts
- NMPA approvals in 06-26 to 06-29 window (silevimig from 06-26 candidates list, telitacicept IgAN + Sjögren's dual approval, etc.)
- Follow-on robotic surgery / autonomous-surgery news (Xijing Hospital, AFMU-Tangdu ecosystem)
- Mirage News searches for any other HKUMed / Chinese University of Hong Kong press releases in the 06-25 to 06-30 window