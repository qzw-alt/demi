# Article Archetypes — Rolling Addendum (verified 2026-07-XX)

This file extends the **four → six verified article archetypes** documented in
`programmatic-seo/SKILL.md` Step 2. Each archetype is added when a cron run
proves that the existing four don't cleanly fit a recurring article type.

## 7th archetype: SEVENTH — Emerging-tech signal-vs-service (verified 2026-07-13)

**Context.** The 2026-07-13 chinahospitalsguide article on the UC San Diego / Unitree G1
humanoid surgical robot story (`news/2026-07-13-china-unitree-g1-humanoid-surgical-robot-world-first.html`,
2,181 words, 79/100, 11.6 em-dashes per 1,200, shipped in ~17 tool calls)
introduced a structural shape that doesn't fit any of the existing six archetypes:

- The news is a **hardware / technology story**, not a clinical trial readout,
  regulatory approval, IND clearance, cell-therapy Phase 1, clinical
  meta-analysis, or structural policy.
- The platform is NOT yet clinically available to international patients —
  it is a research milestone with a 3–5 year clinical-translation horizon.
- The clinical access story still exists: international patients can access
  the **existing capability corridor** (da Vinci, Microport Toumai, 5G remote
  proctoring, robotic microsurgery) that will absorb the new platform.

The archetype that emerged — the "signal-vs-service" framing — solves three
problems at once:

1. **Avoids press-release paraphrase.** Without an explicit
   "what this does not change" section, the article reads as marketing copy
   for Unitree + UC San Diego. With it, the article reads as honest analysis.
2. **Gives international patients a concrete path today.** The "signal vs
   service" framing lets the article name what is available at Chinese
   hospitals in 2026 (da Vinci Xi/SP, Microport Toumai, 5G remote proctoring
   at Tongji, robotic microsurgery at HKUMed QMH) — i.e., the capability
   corridor that the new tech will plug into.
3. **Anchors a realistic timeline.** A research-grade robot that works on
   pigs in 2026 needs NMPA approval, sterilization engineering, malpractice
   framework, and clinical trials before any human case. The article names
   the first clinical translation as 2029–2030 for first human cases — which
   is calibrated, not made-up.

### Verified 7-section structure (2026-07-13 reference)

1. **Lead** + **data-box callout** (3 specific data points: who did what, why
   it matters for Chinese hospitals, what international patients get today)
2. **What the research team actually did** — study details, named surgeons,
   published-paper quote, GitHub overview excerpt
3. **Why the [country/company] angle is the entire story** — supply chain,
   procurement cycle, state policy backing (the 3 structural-consequence pattern)
4. **How this connects to what Chinese hospitals already do** — named tertiary
   centers, existing platforms (da Vinci, Toumai, Edge, 5G remote, microsurgery)
   — the "deployment corridor" framing
5. **What this does not change (yet)** — explicit "honest calibration" section
   with 3 named gaps (clinical translation, sterilization, malpractice/consent)
6. **What international patients should actually do today** — concrete access
   paths with cost numbers, naming the existing platforms
7. **What to watch in the next 12–18 months** — 4 concrete data points
   (regulatory approval, industry partnership, state policy publication,
   first clinical trial)
8. **Bottom line for international patients** — explicit timeline (2029–2030
   vs 2026), honest assessment of what is and is not shippable today

### Critical differentiators from press-release paraphrase

- **Section 5 (the "honest calibration" section)** is load-bearing — without
  it, the article reads as marketing. With it, the article reads as analysis.
  Three named gaps minimum: clinical translation gap, engineering gap
  (sterilization / instrument handling), regulatory + malpractice gap.
- **Section 8 (the "Bottom line" section)** names a specific first-clinical-
  use year (2029–2030 for the 2026-07-13 story). Without a calendar anchor,
  the closing reads as generic optimism.
- **Section 4 (the "deployment corridor")** names 4–6 existing platforms at
  Chinese hospitals. This converts the article from "what's coming" to
  "what's available + how the new tech plugs in." The named platforms lift
  the article's specificity score and produce natural cross-link targets.

### When to use this archetype

- Hardware / robotics / device news with a research-grade milestone
- Drug / biologic / cell therapy with a research-grade milestone that is
  NOT yet commercially available (and not a registration trial, IND, or
  regulatory approval)
- A platform (rather than a specific drug) that will absorb multiple
  future indications — surgical robots, AI diagnostic platforms, etc.

### What this archetype is NOT

- Not a regulatory approval (use the 2nd archetype, 7-part structure)
- Not a Phase X data readout (use the 1st archetype, 4-part structure)
- Not an IND clearance (use the 3rd archetype, 6-section structure)
- Not a cell-therapy Phase 1 (use the 4th archetype, 7-section structure)
- Not a clinical meta-analysis (use the 5th archetype)
- Not a structural policy (use the 6th archetype)

The decision rule: **if the news is a platform milestone that will eventually
translate to clinical use but is not clinically available today, and if
international patients have an existing access path through other platforms,
use this 7th archetype.**

### Em-dash density target (extending the 06-14 finding)

The 2026-07-13 article shipped at **2,181 words / 11.6 em-dashes per 1,200**
at 79/100. This extends the existing em-dash-density table in `SKILL.md`:

- 2,000–2,500 word articles: **10–14 em-dashes per 1,200 words** is shippable
  (the 2026-07-13 reference confirms 11.6/1,200 at 79/100)
- 3,000–3,800 word articles: **17–23 em-dashes per 1,200 words** is the
  baseline (per the existing 06-02 measurement)
- 4,000+ word articles: 10–12 em-dashes per 1,200 is also fine (per the
  06-14 finding that long articles can ship at lower density)

The script cap `em_dash_high=23` is a per-1,200-words measurement on a
specific word count. For a 2,181-word article at 11.6/1,200, the raw em-dash
count is 21 — below the 23 cap, no false-negative penalty.

### Word count target for this archetype

2,000–2,500 words for the headline story. Articles in this band shipped at
72–82/100 across the 2026-06-25 / 2026-07-04 / 2026-07-13 reference runs.
Going longer dilutes the "signal" punchline without adding analytical depth.

### Reference cases

- **2026-07-13 (this run, shipped):** Unitree G1 humanoid surgical robot —
  Nature study by UC San Diego teleoperating two Chinese-made G1 humanoids
  for live-pig gallbladder surgery. 2,181 words, 79/100, commit `9453bea`,
  HTTP 200 verified. **Primary reference for the 7th archetype.**

---

## 6th archetype: Structural policy (verified 2026-06-30)

Already documented in `SKILL.md` Step 2. Cross-reference: `references/pending-2026-06-30-china-order-818-shipped.md`.

## 5th archetype: Clinical meta-analysis (verified 2026-07-04)

Already documented in `SKILL.md` Step 2. Cross-reference: `references/article-archetype-clinical-meta-analysis-2026-07.md`.

## 4th archetype: Cell-therapy Phase 1 (verified 2026-06-25)

Already documented in `SKILL.md` Step 2. Cross-reference: `references/pending-2026-06-25-unixell-ux-da003-fda-ind-ipsc-parkinson-shipped.md`.

## 3rd archetype: IND clearance (verified 2026-06-24)

Already documented in `SKILL.md` Step 2. Cross-reference: `references/pending-2026-06-24-mabwell-6mw5311-lilrb4-cd3-tce-shipped.md`.

## 2nd archetype: Regulatory approval (verified 2026-06-23)

Already documented in `SKILL.md` Step 2. Cross-reference: `references/pending-2026-06-23-carsgen-satri-cel-worlds-first-solid-tumor-cart-shipped.md`.

## 1st archetype: Phase X data readout (verified 2026-06-09)

Already documented in `SKILL.md` Step 2. Cross-reference: `references/pending-2026-06-09-oricell-gpc3-cart-hcc.md`.