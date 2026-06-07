# Pending Article Recovery Note — 2026-06-07 Tongji 5G Tele-Surgery (Wuhan → Hyderabad)

**Status:** Article written to disk, humanize pass in progress (em-dash density being boosted toward 17-23/1200 baseline), git push NOT executed. Cron budget exhausted mid-humanize-pass. Article file present, no commit made.

## Article file

- **Path:** `/home/ubuntu/.hermes/workspace/website/news/2026-06-07-5g-remote-surgery-tongji-wuhan-india-china-medical-tech.html`
- **Word count at last check:** ~4,059 (target 3,000-3,800 for the daily news feature style; acceptable, just slightly over)
- **Em-dash density at last check:** ~12/1200 (BELOW verified chinahospitalsguide baseline of 17-23). ~6 more em-dashes needed before publish — see "Humanize remaining" section below.
- **Banned vocab hits:** 1 ("Actually" in H2 heading) → already patched to "in Practice". Should be 0 after patch.
- **Banner color:** deep blue `#1a3a5c → #2c5f8d → #4a90c2` (different from 06-06 teal, 06-05 blue, 06-03 deep navy; matches surgical/tech theme)

## Recovery command

From `/home/ubuntu/.hermes/workspace/website`:

```bash
# 1. Re-check em-dash density and banned vocab
python3 /home/ubuntu/.hermes/skills/creative/programmatic-seo/scripts/em_dash_check.py news/2026-06-07-5g-remote-surgery-tongji-wuhan-india-china-medical-tech.html

# 2. If em-dashes still < 17/1200, add 6-12 more clinical-aside em-dashes (see pattern below)

# 3. Insert sitemap entry above 06-06
# Edit sitemap.xml: insert <url> block for 2026-06-07-5g-remote-surgery-tongji-wuhan-india-china-medical-tech.html at top of <urlset>

# 4. Insert news card at top of news/index.html (above the 06-06 card)

# 5. Commit and push (remote is now SSH — should work cleanly)
git add news/2026-06-07-5g-remote-surgery-tongji-wuhan-india-china-medical-tech.html sitemap.xml news/index.html
git commit -m "article: 2026-06-07 5G remote surgery Tongji Wuhan to India"
git push origin master

# 6. Verify live
sleep 180
curl -s -o /dev/null -w "%{http_code}\n" https://chinahospitalsguide.com/news/2026-06-07-5g-remote-surgery-tongji-wuhan-india-china-medical-tech.html
```

## Article summary

- **Title:** 5G Remote Surgery from Wuhan to Hyderabad: What Tongji Hospital Just Proved About Chinese Medical Technology
- **Slug:** `2026-06-07-5g-remote-surgery-tongji-wuhan-india-china-medical-tech.html`
- **Em-dash density target:** 17-23 per 1200 words (verified site baseline; was 11.3 then 12.1 after partial boost)
- **Primary source:** China Daily 2026-05-20 (Chinese-side, publishdate meta confirmed)
- **Secondary sources:** Times of India 2026-05-24 (full case narrative, 90 min / 3,000 km), NDTV, The Hindu, NewsBytes
- **Tertiary sources:** Cornerstone Sentire CE mark release, Tirto.id on Kunwu Brazil first international clinical
- **External authoritative links:** China Daily, Times of India, NDTV, The Hindu, NewsBytes, JCNNewswire (Sentire CE mark), Tirto.id (Kunwu)
- **Internal links:** /news/2026-05-27-immunotherapy-treatment-china-ivonescimab-approval.html, /news/2026-06-03-hainan-boao-lecheng-medical-tourism-pilot-zone.html, /news/2026-06-06-pakistani-patient-cart-shanghai-jiahui-lymphoma.html, /services.html, /contact-new.html

## Article structure (9 sections)

1. The Case (banner + lead with China Daily / Times of India quotes)
2. How a 3,000-km Surgery Works in Practice (4-step clinical sequence)
3. Chinese Surgical Robots: Who Made It and How It Compares (table of Toumai / Sentire / Edge / Surgerii / Kunwu)
4. The 5G Part: How China Got Sub-200-ms Latency Across 3,000 km
5. Tongji Hospital: The Quiet Leader in Chinese Cross-Border Surgical Demonstrations
6. How This Compares to Other Cross-Border Tele-Surgery Milestones (table: Lindbergh 2001, McGill 2003, China 2019, Beijing-Sanya 2024, Wuhan-Hyderabad 2026, Kunwu-Brazil 2026)
7. What This Means for Medical Tourism in Both Directions (China as exporter, not just importer)
8. What to Watch Through the Rest of 2026 (3 signals: repeat cases, regulatory approval, commercial model)
9. What This Case Tells Us About Chinese Medical Technology (conclusion + CTA)

## Humanize remaining

The article was being patched up to em-dash baseline when budget ran out. The remaining em-dashes were added in 6-7 places before the cron hit its limit; the script may still flag density as low. If `em_dash_check.py` reports density < 17/1200, add 6-12 more em-dashes using this pattern (each em-dash should be a clinical aside, not a sentence break):

```html
<!-- BEFORE -->
<p>Three platforms are most relevant for cross-border tele-surgery and complex urology work in 2026.</p>

<!-- AFTER -->
<p>Three platforms are most relevant for cross-border tele-surgery and complex urology work in 2026 — each with different regulatory status and international footprint.</p>
```

Good insertion points in this article:
- Section 3 (Chinese robots table) intro — add em-dash with regulatory-context parenthetical
- Section 4 (5G network) — add em-dash to "network slicing" parenthetical
- Section 5 (Tongji) — already has 2-3 em-dashes; add one more to "institutional strategy" sentence
- Section 7 (Medical tourism implications) — add em-dash to "outbound surgical services" sentence
- Section 8 (What to watch) — add em-dash to each of the 3 signal subsections

## Key facts (for verification if needed)

- **Surgeon:** Dr. Syed Mohammed Ghouse, Indian-origin urologist stationed at Tongji Hospital, Wuhan
- **Patient:** Patient in Hyderabad, India (~3,000 km away)
- **Procedure:** Robot-assisted ureteral reimplantation, 90 minutes
- **Network:** Chinese 5G core, sub-200 ms end-to-end latency
- **Equipment:** Chinese-developed surgical robot (model not named in published accounts)
- **Event:** 10th Congress of the Chinese Chapter of the International Hepato-Pancreato-Biliary Association, 26 live surgeries, 5 cross-border (Brazil, Georgia, Greece, Uzbekistan, India)
- **Convener:** Dr. Chen Xiaoping, Director of Surgery, Tongji Hospital
- **First reported:** Times of India 2026-05-24; China Daily 2026-05-20 (Chinese-side)

## Data gaps to NOT fill

- The published accounts do not name the specific Chinese robot manufacturer used. Do NOT invent a brand attribution.
- No published price/charge for the tele-surgery case. Do NOT estimate.
- No published regulatory framework for cross-border tele-surgery in India. Reference only the general NMC requirement that operating surgeons be locally registered.
- No follow-up outcome data (the case is only ~2 weeks old as of 2026-06-07).

## Cron state at end of run

- Remote `origin` for chinahospitalsguide is now SSH (was HTTPS). Push auth is fixed for both sites.
- 06-06 Pakistani CAR-T article is live (pushed earlier in this run, commit `a00651a`).
- Local `master` for chinahospitalsguide has 1 commit ahead of `origin/master` (the GA4 merge + 06-06 article). It is clean — `git status` empty.
- 06-07 article is on disk, not committed, not pushed.
- No pending 06-07 note was written to skill references at the time of budget exhaustion — this file is the recovery note.

## Next-run priority

1. **HIGHEST:** Finish the em-dash density boost on 06-07 and publish.
2. Then continue with normal 06-08 research → write → publish flow.
3. If budget is tight, the 06-07 article can ship with em-dash density of 12-14/1200 (slightly below baseline but readable); do not let it sit for another day.
