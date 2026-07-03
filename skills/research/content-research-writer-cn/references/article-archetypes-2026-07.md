---
name: article-archetypes-2026-07
description: "Supplemental reference for the SIXTH and SEVENTH article archetypes documented in content-research-writer-cn after the 2026-07-03 cron run."
version: 1.0.0
author: Hermes Agent
platforms: [linux]
---

# Article Archetypes Addendum (2026-07-03)

This file supplements the [SKILL.md](../SKILL.md) "article archetypes" section with the
two new archetypes verified by the 2026-07-03 cron run on chinahospitalsguide.com.

## SIXTH archetype: "Leisure-to-clinical bridge"

**When to use:** the lead is a publicly-visible leisure/wellness phenomenon (bathhouse,
spa, hot-spring resort, qigong festival, tea tourism, fitness-trend) where the **same
cultural tradition** sits underneath clinical services international patients can
actually book into. The article angle is the **bridge** between the two — the visible
phenomenon is named, then translated into the clinical access pathway the site covers.

**Verified 9-section structure** (used on the 2026-07-03 Straits Times bathhouse
article, 3,605 words, humanize 90/100, em-dash density 27):

1. **Lead** — what just happened, headline data point, the international-patient
   question ("what does this have to do with the site?")
2. **Why this story is shippable** (data-box callout) — the credential + regulatory
   distinction across the three layers, with a headline number per layer
3. **What the publicly-visible phenomenon is** — restate the source's headline
   findings with the 2-3 pullquote sources verbatim
4. **What changes when the same tradition operates inside a hospital** — credential
   layer (vocational technician vs licensed TCM physician vs hospital attending),
   billing/regulatory layer, patient population
5. **The hospital-clinical layer** — TCM hospital 治未病 departments, post-acute
   recovery programs, oncology-support tracks; cost + access framing
6. **The medical-tourism cross-border layer** — Bo'ao Lecheng or equivalent
   cross-border TCM access framework; 3-6 month prescription follow-up
7. **What an international patient should ask before booking** — regulatory
   setting, practitioner credential, integration with home clinic, cost
8. **What the next 12-18 months are likely to bring** — three concrete items
9. **Take-home** — explicit statement that the leisure and clinical layers are
   connected by the same cultural tradition and disconnected by credential,
   regulatory setting, and cost

**Differentiators that lift the score:**
- The credential-and-regulatory table in section 4 is load-bearing — without it the
  article reads as a cultural explainer with TCM name-drops
- The three-layer access framing in sections 5-6 (hospital vs cross-border access point
  vs TCM resort) is the second differentiator — it gives the reader a concrete decision
  tree
- Source pullquotes are mandatory (verified 2026-07-03 had 3: Kan Li historian framing,
  Liu Simin industrial framing, No. 517 labor-market framing)

**Chinese-bathhouse / wellness cultural context vocabulary** (verified 2026-07-03):
- **治未病** (zhì wèi bìng, "treating the undiseased") — Chinese-medicine term for
  preventive medicine; hospitals run "Preventive Treatment Center" departments with
  this exact name
- **cuozao** (搓澡) — body-scrub term, traditionally northeast-China practice that
  has gone national via trained-labor migration to Beijing/Shanghai chains
- **Han-era / Song Dynasty / Republican / 1949-state-enterprise / 1990s-restructuring
  historical sequence** — the bathhouse origin story traces welfare-bathhouse in
  state-owned enterprises (1949-1990) as cultural ancestor of today's commercial chain

## Source pattern extension: Straits Times 3rd-tier extended to wellness/cultural

The 2026-06-22 SKILL.md pattern documented Straits Times as a 3rd-tier source for
**inbound medical tourism** stories (Raffles Medical, BT/Bloomberg follow-on). The
2026-07-03 run surfaced a different use case: **Straits Times as a 3rd-tier source for
wellness/leisure/cultural stories with TCM adjacency**.

**Verified source**: Michelle Ng's 2026-07-03 article "Bathhouse boom: China's new
24-hour hangout" published at 2026-07-03T05:00:00+08:00. Body extractable via standard
`<article>` regex. Fetched as ~600KB page yielding ~7500 chars of clean prose.

**New tier-position insight:** Straits Times serves the same Michelle Ng correspondent
niche for **non-clinical-but-culturally-significant** Chinese stories — the kinds of
pieces that don't surface in clinical journals or biotech press releases but do appear
in international lifestyle/business coverage. The bridge to the site's clinical mission
runs through the 治未病 (hospital wellness), Bo'ao Lecheng, and Hainan hot-spring
convalescence programs the same tradition supports.

**Decision rule:** when (a) the Bing News query for a TCM-adjacent story returns mostly
Straits Times / SCMP / Yahoo News headlines rather than clinical sources, AND (b) the
lead has named sources + market data + a cultural angle, fetch Straits Times directly
without trying to first-skip to a clinical mirror.

## Image-asset naming pitfall (verified 2026-07-03)

The `images/` directory in the chinahospitalsguide repo follows a consistent kebab-case
`<topic-hyphen-separated>.jpg` convention with both `.jpg` and `.webp` variants
side-by-side. When picking the hero-image src for a new `news/index.html` card,
**always `ls images/ | grep -i KEYWORD` first** instead of guessing a filename.

Common verified image assets for cn-hospitals (June-July 2026 audit):
- `wellness-spa.jpg` — spa/wellness/bathhouse stories (the 2026-07-03 article was the
  first to use this image)
- `hainan-beach.jpg` — Hainan tourism
- `china-hospital-building.jpg` — general hospital
- `acupuncture-treatment.jpg` — acupuncture/TCM
- `china-medical-team.jpg` — international medical cooperation
- `china-drug-discovery.jpg` — pharma/biotech
- `china-rare-disease.jpg` — rare disease

For new topics without a verified image, either use a generic existing asset matching
the broader category, or skip the `<img>` tag for the news/index.html card entirely — a
missing image breaks the page; a generic image degrades it.

## Mid-pipeline cap-hit re-occurrence (verified 2026-07-03, second instance after 06-28)

The 2026-07-03 cron run hit the iteration cap AFTER write + humanize-loop completion
(5 banned-vocab patches) + sitemap + index patching but BEFORE the git commit. This is
the SECOND documented instance of the 06-28 failure mode (mid-pipeline cap-hit after
humanize loop, before publish plumbing).

**Reinforcement of the 06-28 lesson:** when the cron agent notices it's burning tool
calls on the humanize loop and budget is tight, STOP polishing and front-load the
publish plumbing. The recommended sequence when budget is tight:
1. Write article
2. Humanize pass with maximal-3 banned-vocab patches (NOT the 5-7 patch loop)
3. Sitemap patch
4. News/index.html patch
5. Git commit + push + verify
6. THEN resume humanize iteration if any budget remains

A published article at 70/100 ships value to readers; an uncommitted article at 95/100
ships nothing. The 06-28 SKILL.md "Hard rule #2" guidance was correct but not salient
enough in the 2026-07-03 moment — this second-instance reinforcement is now in the
record.
