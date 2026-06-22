# 2026-06-22 — Straits Times / Raffles Medical Group / China Inbound Medical Tourism (CLEAN RUN, SHIPPED)

## Outcome

- **Article:** `news/2026-06-22-raffles-medical-china-37000-foreign-patients-2025-inbound-medical-tourism.html`
- **Word count:** 4,983
- **Humanize score:** 90/100 (after 6 targeted banned-vocab patches: 3 × `actually`, 2 × `navigate`, 2 × `landscape`)
- **Em-dash density:** ~14.9/1200 (62 raw em-dashes / 4,983 words × 1200)
- **Commit:** `a1526b4` (local master, pushed to `origin/master` as fast-forward from `6dfb9d5`)
- **Verification:** HTTP 200 on `https://chinahospitalsguide.com/news/2026-06-22-raffles-medical-china-37000-foreign-patients-2025-inbound-medical-tourism.html` after `sleep 180`
- **Total tool calls:** ~13 (pre-flight + 2 Bing fetches + 1 ST fetch + de-dup grep + write article + score + 6 patches + re-score + sitemap patch + index.html patch + commit + push + verify)

## Source

- **Primary:** The Straits Times, "Why hospitals in China, including Raffles Medical, are attracting more foreign patients" by Michelle Ng, 2026-06-21, 168KB body
- **URL:** `https://www.straitstimes.com/asia/east-asia/why-hospitals-in-china-including-raffles-medical-are-attracting-more-foreign-patients`
- **Date verification:** `<meta property="article:published_time" content="2026-06-21T19:00:00+08:00">` (1 day before cron run, within 48h freshness window)

## Unique anchor points (all from the Straits Times article)

1. **Raffles Medical Group:** 3 China hospitals (Beijing, Shanghai, Chongqing), **37,000 international patients in 2025**, 130 countries, **+7.9% YoY**. Source: Phua Tien Beng, MD Raffles China Healthcare.
2. **Emma Holden, 36, New Zealand, multiple myeloma:** third-round CAR-T in Shanghai brought disease under control in October 2025. Treatment not commercially available in NZ at the time.
3. **Victor Cao, China Joyful Medical (Shanghai agency):** monthly enquiries went from ~10 (pre-mid-2025) to 30-40 (current); 20-30% conversion to actual travel.
4. **Cui Cui, Jefferies Asia healthcare research:** China's key edge is complex oncology and advanced therapeutics, distinct from Korea (cosmetics) and Thailand (dental).
5. **Cost benchmarks (from the ST article):** CAR-T China $150K-$200K vs US ~$500K; dental implants China $2K-$3K/tooth vs Australia $5K-$8K.
6. **Linjia Zhang, Xi'an Jiaotong-Liverpool University:** "In many ways, China already has the medical capacity; what it is still building is international recognition and trust."
7. **1.28 million international patients in 2025, +73.6% over 3 years** (state-media-cited national data; the 04-10 chinahospitalsguide article used the same figure).
8. **Global medical tourism market:** US$38.2B (2025) → US$46.78B (2026) → US$250.02B (2034) per Fortune Business Insights; China = 1.3% of global.
9. **Top source countries for Raffles China:** Russia, Kazakhstan, Europe, North America, Japan, South Korea. Top services: rehabilitation, paediatrics, dentistry.

## De-dup check (verified shippable)

```bash
cd news && grep -lE "(Raffles Medical Group|37,000 international|Phua Tien Beng|China Joyful Medical|Victor Cao|Emma Holden)" *.html
# Result: 1 match — 2026-06-11 BT article (only "Victor Cao / China Joyful" overlap, in the context of the BT article's Stuart Lye patient story)
# Decision: SHIPPABLE — the new angle is Raffles-as-institutional-player with hard 37,000 patient number, distinct from BT's individual-patient-narrative angle. 9 new anchor points.
```

## What worked

1. **Bing News returned usable URLs on first call (326KB, 14 external article URLs)** — the recipe is still working on 2026-06-22 (transient Bing issue is a run-specific pitfall, not durable).
2. **Straits Times fetch worked on first call** — 168KB body, full article text inside `<div class="layout-content">...</div>`. No Cloudflare, no paywall, no JS challenge.
3. **Score-band recovery:** 40 → 90 in 6 targeted banned-vocab patches. The article was structurally fine from the first draft; only the AI-vocab hits needed fixing. No restructuring required.
4. **Pre-flight clean** — no pending file, no untracked article, no ahead-of-origin state. SSH remote already in place from prior fixes. Git config needed (see below).
5. **Push succeeded cleanly** — no rebase needed, no `git pull --rebase` dance. Fast-forward from `6dfb9d5` to `a1526b4`.

## New patterns / pitfalls documented

### NEW: Straits Times as a 3rd-tier inbound medical tourism source

The skill body already has BT/Bloomberg documented (verified 2026-06-12) and China Daily / akesobio.com. **Straits Times is now a documented 3rd tier** for inbound medical tourism, with these distinguishing properties:
- **Named institutional sources** (Raffles MD Phua Tien Beng, agency head Victor Cao) that BT/Bloomberg syndication typically does not have
- **168KB body** is extractable via `<div class="layout-content">...</div>` pattern
- **Canonical URL pattern:** `https://www.straitstimes.com/{section}/{sub}/{slug}` — date NOT in URL
- **De-dup decision rule:** shippable if ≥3 new institutional/agency data points absent from prior chinahospitalsguide coverage
- **Date extraction:** `<meta property="article:published_time">` is the source of truth

### NEW: First-time git config on a fresh chinahospitalsguide cron run

The 2026-06-22 cron run hit `fatal: unable to auto-detect email address` on the first `git commit` (the repo had no `user.email` / `user.name` configured). Fix: chain `git config user.email "hermes@chinahospitalsguide.com" && git config user.name "Hermes Agent"` into the same terminal call as the commit. **Heads up:** this is a NEW failure mode for chinahospitalsguide — the 06-22 fix is the first documented instance. The `programmatic-seo` skill already documents the same fix for oriental-destiny (verified 2026-06-22 there). The pattern is now confirmed for BOTH sites.

### Score-band finding: 4,983-word article → 90/100

Prior score-band data points: 06-09 4,216w → 82, 06-11 5,229w → 62, 06-13 3,167w → 95, 06-14 4,930w → 95, 06-17 4,701w → 90, 06-20 2,880w → 95. The 06-22 4,983w → 90 (after 6 patches) fits the pattern: **articles in the 4,500-5,200 word range score 60-95 depending on banned-vocab count, not word count alone.** The 06-22 article had 8 banned-vocab hits before patches (3 actually + 2 navigate + 2 landscape + 1 from 06-21 patches already applied), which is high but patchable. The 06-11 5,229w → 62 had more structural `-ing` tail density that the script penalizes harder.

### `navigate` and `landscape` are now top-3 banned-vocab offenders on chinahospitalsguide

The 06-22 run's 2 × `navigate` + 2 × `landscape` matches the 06-13 (Bloomberg) run's 1 × `navigate` and the 06-22 oriental-destiny (Sitting and Facing) run's 1 × `landscape`. Combined with `actually` (3 hits in 06-22, 3 in 06-22 oriental-destiny), these three words are the highest-frequency AI-vocab offenders in clinical / feng-shui prose. **The "Before → After" swap patterns that worked cleanly:**
- `navigate X` → `use X` (when X is a noun phrase like "the referral process" or "Chinese hospital websites")
- `the X landscape` → `the X system` / `the X map` / `the X scene` (concrete physical words work better than softer abstract ones)
- `actually VERB` → `VERB` (just delete the word)

## State at end of run

- Working tree: clean (after `git add` + commit)
- Local master: `a1526b4` (new HEAD)
- `origin/master`: `a1526b4` (fast-forward, matches local)
- SSH remote: in place (no auth issue)
- No pending files
- Cron iteration cap: not hit (clean ship in ~13 tool calls)

## Recommended action for 2026-06-23 cron run

No recovery state to pick up. Start fresh research on 2026-06-23 hot topic. Suggested candidates based on the 2026-06-22 Bing News results not yet covered:
- **Zai Lab NMPA approval** (from 06-22 Bing) — new drug clearance angle
- **Harbour BioMed NMPA acceptance** (from 06-22 Bing) — new drug clearance angle
- **Vcare PharmTech eratrectinib (TRK inhibitor) NMPA marketing approval** (from 06-22 Bing, surfaced via tirto.id — but tirto.id is Cloudflare-blocked, would need finanznachrichten.de or manilatimes.net mirror)
- **NMPA approvals in the 2026-06-15 to 2026-06-22 window** — general biotech clearance news
- **ESMO 2026 GI abstract follow-on coverage** (ESMO GI usually January, not June — skip unless specific session)
- **Akeso ivonescimab additional indications** (Akeso has been the highest-frequency press-release source in 2026-06)

Bing News query strings worth trying: `China+NMPA+approval+drug+June+2026`, `Akeso+OR+Innovent+OR+BeiGene+OR+Hutchmed+press+release+June+2026`, `China+biotech+IPO+OR+licensing+deal+June+2026`.
