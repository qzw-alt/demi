# The Star (Malaysia) as 4th-tier source for TCM globalisation wire (verified 2026-07-28)

## Source pattern

**URL pattern:** `https://www.thestar.com.my/aseanplus/aseanplus-news/{YYYY}/{MM}/{DD}/{slug}`
**Section:** `aseanplus-news` is the Asia News Network (ANN) feed — syndicates *China Daily*, Xinhua, and other Asia-Pacific wire content.
**Date in URL:** `/YYYY/MM/DD/` prefix — reliable for the article's publication date.
**Body size:** 400-420 KB HTML, 30+ substantive `<p>` paragraphs (200+ chars each), standard `<p>` regex extraction works.
**Date verification:** `<meta property="article:published_time" content="{YYYY-MM-DD}T00:00:00.000Z">` matches the URL prefix.
**End attribution:** typically `— China Daily`, `— China Daily/ANN`, or `— Xinhua` (varies by source wire).

## Verification: 2026-07-28 TCM globalisation article

**URL:** `https://www.thestar.com.my/aseanplus/aseanplus-news/2026/07/28/no-longer-just-an-exotic-alternative`
**Title:** "No longer just an exotic alternative"
**Published:** 2026-07-28
**Body:** 407KB HTML, ~30 substantive `<p>` paragraphs covering:

1. **Named-product retail evidence (Germany):** Anhui Jiren Pharmaceutical Shufeng Jiedu granules, ~200,000 bottles sold since launch at €39.90/bottle through Bahnhof-Apotheke pharmacy chain.
2. **Named-company regulatory history (Russia/EU):** Tianjin Da Ren Tang Group Suxiao Jiuxin Pills — registered prescription in Russia since 1997, recognised in Australia and Japan. 193 Anhui Jiren granule varieties passed German quality inspections.
3. **Named-executive quotes:**
   - Zhu Qiang, deputy general manager of Anhui Jiren Pharmaceutical — TCM-as-daily-wellness positioning
   - Li Hongjiang, production deputy general manager at Da Ren Tang plant — QR-code batch traceability
   - Guo Yi, vice-president of Tianjin University of TCM — AI synthesis of classical TCM texts
4. **Named-hospital foreign-patient pathway (Hainan):** Sanya Hospital of Traditional Chinese Medicine — customised plans for foreign clients (acupuncture, tuina, herbal baths, medicinal cuisine, weight management). Named patient: Konstantin, Russian engineer, brought parents for acupuncture.
5. **Named-investment figures:** 300M yuan (≈ US$42M) Da Ren Tang intelligent workshop with near-infrared spectroscopy + visual inspection.
6. **Macro framing:** TCM practised in 196 countries; 40+ foreign government cooperation agreements; 100+ ISO standards issued through committee China helped establish.
7. **AI as new layer:** Tasly-Huawei Cloud TCM LLM (2024 launch); separate large model by National SuperComputer Center in Tianjin + Tianjin University of TCM covering 20+ clinical disciplines.

**End attribution:** `— Xinhua` (not China Daily) for this particular wire.

## When to use The Star for TCM/China Daily syndication

Use when:
- The lead is "TCM industry expanding into EU/Russia/Africa with named products and named hospitals" and *China Daily* or *Xinhua* is the canonical source wire.
- The canonical ChinaDaily.com.cn direct fetch is blocked by the cron sandbox (common pattern).
- The piece needs named-product retail evidence (e.g., "200,000 bottles sold in Germany") that's absent from more general press coverage.
- The article needs both pharma/regulatory structure (ISO standards, registrations, certifications) AND a human face (foreign-patient case at named hospital).

Don't use when:
- The lead is a clinical-trial data readout (use pharmaphorum.com or Akeso/CARsgen IR pages).
- The lead is a regulatory approval with detailed mechanism (use GEN.com or NMPA mirrors).
- The lead is a university press release with named-surgeon cases (use Mirage News).

## Source-tier positioning (verified 2026-07-28)

| Tier | Source | Best for |
|---|---|---|
| 1 (primary) | ChinaDaily.com.cn, biotech IR pages, Mirage News | canonical Chinese-domestic sources |
| 2 (PR mirror) | manilatimes.net, finanznachrichten.de | biotech press releases |
| 3 (substitute) | pharmaphorum.com | global pharma news (FiercePharma blocked) |
| 4 (China Daily wire) | **The Star (Malaysia)** aseanplus section | TCM globalisation / Western CEO on China / institutional-pharma commentary |
| 5 (regional) | Straits Times, Business Times Singapore | inbound medical tourism with named institutions |
| 6 (policy) | GEN.com | biotech policy/regulatory/business |
| 7 (academic) | Deccan Herald JSON-LD articleBody | Indian English coverage of clinical evidence |

## Article shipped from this source (2026-07-28)

- **File (originally):** `news/2026-07-28-tcm-going-global-shufeng-jiedu-germany-ai-workflow.html`
- **File (after 2026-07-28 migration):** should be moved to `blog/2026-07-28-tcm-going-global-shufeng-jiedu-germany-ai-workflow.html` (or `.md`) — see `references/news-to-blog-migration-2026-07-28.md` for the migration recipe
- **Word count:** 1,729
- **Humanize score:** 92/100 (after 2 patches: removed `actually` from H2 + `pivotal → necessary`)
- **Archetype:** Template C (Policy & Accessibility)
- **Commits:** `2f327e4` (article), `6827923` (sitemap), `850469b` (humanize), `5c938f4` (pending note)
- **Migration status:** article still on origin as `news/` path; needs `git mv` + sitemap fix + push on next cron run

## Pitfalls

- The articleBody extraction pattern works the same as standard western media sites — `<p>` regex with 200-char filter.
- The 400KB HTML response includes 1 article + sidebar/footer; expect ~30 substantive paragraphs in the body region.
- The Star Malaysia site occasionally rate-limits anonymous curl; if `curl` returns <50KB, retry once after 5s.
- The end-attribution varies (`— China Daily`, `— China Daily/ANN`, `— Xinhua`); verify which wire is the canonical source before citation. For 2026-07-28, attribution was `— Xinhua` even though the lead (TCM globalisation, named-pharmacy evidence, Hainan pathway) was the China Daily beat — Xinhua was the syndication partner for this specific piece.