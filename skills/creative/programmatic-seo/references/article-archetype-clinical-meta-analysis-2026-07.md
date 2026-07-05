# Article Archetype: Clinical Meta-Analysis — Chinese-Evidence-Base Focus (verified 2026-07-04)

The 2026-07-04 chinahospitalsguide run shipped a new archetype: a clinical
meta-analysis with a Chinese-evidence-base framing. Distinct from the existing
archetypes (Phase X data readout, regulatory approval, IND clearance,
cell-therapy Phase 1, structural-policy).

## When this archetype fits

The story is a peer-reviewed meta-analysis (or systematic review with
meta-analysis) where:
- The evidence base is heavily Chinese (e.g. 22 of 30 RCTs are Chinese trials)
- The intervention is a TCM modality (electroacupuncture, herbal medicine,
  tuina, baduanjin) OR a TCM-Western integration
- The meta-analysis identifies a specific technical parameter (waveform,
  acupoint, dose, duration) as the highest-yield choice
- The intervention is available at Chinese tertiary hospitals' international
  patient services at a fraction of Western-clinic cost
- The mechanism has a published neuroanatomy / neurophysiology /
  receptor-pharmacology basis (the meta-analysis includes animal-model
  mechanism studies, not just clinical RCTs)

This archetype does NOT fit for:
- Meta-analyses with mostly non-Chinese evidence bases (use a regular
  clinical-research article structure)
- Meta-analyses where the headline is "no evidence of benefit" (the
  2026-07-02 acupuncture-IVF Lancet vs Frontiers contrast is a better
  template for that)
- Drug trials (use the Phase X data readout archetype)

## Verified 6-section structure (2026-07-04 Yue et al. article, 4,377 words, 73/100)

1. **Lead + dual-jurisdiction framing** (1 paragraph) — open with the
   meta-analysis citation (journal + DOI + author group + lead number),
   name the parameter the meta-analysis identified, anchor to the
   patient population (e.g. post-stroke dysphagia affects 45% of stroke
   survivors globally), and explain why the Chinese-evidence-base share
   matters for an international patient.

2. **Data-box callout** (1 box, ~6 anchor data points) — the headline
   number, the secondary outcome (e.g. aspiration pneumonia risk
   reduction), the optimal parameter (dense-sparse wave), the
   epidemiology anchor (45% global PSD prevalence), the
   evidence-base-geography anchor (22 of 30 Chinese RCTs), the cost
   comparison (US$25-60/session in China vs US$120-250 in U.S./EU), and
   the WHO endorsement reference.

3. **What the meta-analysis found** — abstract-level summary
   paraphrased for the international-patient audience. Cover the search
   strategy (databases, inclusion criteria), the headline result with
   effect size + CI + p-value + I² (heterogeneity), the secondary
   outcomes, and the subgroup analysis (the parameter-identification
   finding). Include a verbatim pullquote from the paper's conclusions
   section (the `enhance` / `furthermore` hits inside source-quote
   attributions are FALSE POSITIVES per the 2026-06-25 pitfall — leave
   them).

4. **What the protocol looks like at a Chinese center** — name 4-5
   specific Chinese hospitals by department (West China Hospital
   rehabilitation medicine, China Rehabilitation Research Center
   Beijing, Huashan Hospital rehab dept Shanghai, Sun Yat-sen
   University First Affiliated Hospital, etc.), name the typical
   practitioner credential (5-year bachelor of TCM + 1-3 years
   specialty training, working alongside a rehabilitation physician +
   speech-language pathologist), name the typical course (20-30
   sessions over 4-6 weeks), and name the acupoints / parameters used
   in the meta-analysis (with anatomical context — why Lianquan/CV23
   specifically targets the swallowing muscles).

5. **Why the Chinese evidence base is so large** — the
   institutional-context section that distinguishes this archetype from
   a generic clinical article. Cover the combined TCM-Western
   rehabilitation department model at Chinese tertiary hospitals, the
   lack of Western equivalent, the career-credential pathway (Chinese
   rehab medicine physicians train alongside TCM acupuncturists in the
   same department), and the PROSPERO registration as evidence that the
   synthesis is now meeting international standards.

6. **How an international patient can access the protocol** — the
   practical pathway. Remote consultation → travel + scheduling →
   documentation + follow-up. Cover the credentialing of the home
   practitioner if the patient wants to continue post-discharge. Always
   include the safety note for the most common contraindication (e.g.
   anticoagulants for cervical acupoints like Lianquan/CV23 — INR <2.5,
   stable DOAC dose for 2 weeks, dual antiplatelet with recent platelet
   count).

7. **What an international patient should ask before booking** — the
   5-question checklist (indication / protocol / practitioner credential /
   home-clinic integration / cost + travel), plus the anticoagulation
   safety note when relevant.

8. **What the next 12 to 18 months are likely to bring** — three
   predictions: (a) a planned multicenter RCT, (b) a likely Cochrane
   review update, (c) an inbound medical-tourism expansion (e.g. Hainan
   Lecheng free trade zone).

## Length and humanize characteristics (verified 2026-07-04)

- **Word count: 4,000-5,000 words.** The Yue et al. article shipped at
  4,377 words across 6 H2 sections + lead + data-box. Shorter articles
  (~3,000 words) feel underweight for a meta-analysis that needs to
  explain the search strategy + headline result + subgroup findings +
  Chinese-context section + practical pathway. Longer articles
  (~6,000+ words) hit the 60-70 humanize ceiling without lifting the
  score further.
- **Em-dash density: 10-14 per 1200 words.** The 2026-07-04 article
  shipped at 39 raw em-dashes across 4,377 words = 10.7/1200. This is
  BELOW the verified 17-23 baseline for chinahospitalsguide, but the
  score still cleared 73/100 because the long-article band (4,000+)
  tolerates sub-baseline density (per the 06-14 / 06-18 / 06-29
  findings). Do NOT mechanically pad em-dashes to hit baseline — the
  clinical-prose voice is naturally less parenthetical-heavy than the
  press-release-paraphrase archetype.
- **Banned-vocab hits:** typically 2-3 (`enhance`, `furthermore`,
  `leverage`, `pivotal`, etc.) flagged, mostly inside source
  pullquotes. Per the 2026-06-25 verified pitfall, leave them — the
  score penalty is 1-2 points and removing them changes the source's
  stated position.
- **Score band:** 70-80 is the realistic ceiling for this archetype.
  The 2026-07-04 article hit 73/100 on the first pass with no banned-vocab
  patches. The 60-70 ceiling on long articles applies.

## Discovery recipe — how to find these candidates (verified 2026-07-04)

1. **Bing News first** with queries combining the modality + indication
   + recent date:
   - `acupuncture+migraine+OR+back+pain+clinical+trial+2026`
   - `moxibustion+breech+OR+acupuncture+stroke+rehabilitation+OR+baduanjin+COPD+meta-analysis+2026`
   - `Lianquan+"electroacupuncture"+stroke+swallowing+2026` (modality + specific acupoint)
   - `[acupoint-name]+[indication]+2026+randomized` (very specific)
2. **CrossRef API as fallback** when Bing returns paywalled / Cloudflare-blocked
   pages (the 2026-07-04 news-medical.net page returned 174KB but the body
   was JS-buried). The CrossRef API is reliable:
   ```bash
   curl -s --max-time 25 "https://api.crossref.org/works?query.bibliographic=electroacupuncture+Lianquan+post-stroke+dysphagia&filter=from-pub-date:2025-10-01&rows=15"
   ```
   Returns DOI + title + journal + date + authors as JSON. The
   CrossRef `abstract` field is often empty, but `title` /
   `container-title` / `DOI` are reliable. Use the DOI to fetch the
   full paper directly from the publisher (Frontiers / MDPI / PLOS /
   BMC are open-access and work; Wiley / Springer / Elsevier are
   paywalled).
3. **Frontiers full-text fetch recipe (verified 2026-07-04):**
   ```bash
   curl -s --max-time 30 -A "Mozilla/5.0 ..." \
     "https://www.frontiersin.org/journals/neurology/articles/10.3389/fneur.2025.1673716/full" \
     -o /tmp/frontiers.html
   ```
   Returns ~1.3MB HTML. Extract abstract + introduction + discussion:
   ```python
   import re
   with open('/tmp/frontiers.html') as f: c = f.read()
   # Strip style/script/svg
   c = re.sub(r'<style[^>]*>.*?</style>', ' ', c, flags=re.DOTALL)
   c = re.sub(r'<script[^>]*>.*?</script>', ' ', c, flags=re.DOTALL)
   c = re.sub(r'<svg[^>]*>.*?</svg>', ' ', c, flags=re.DOTALL)
   # Find by H2 heading
   m = re.search(r'<h2[^>]*>Abstract</h2>(.*?)<h2', c, re.DOTALL)
   if m:
       body = re.sub(r'<[^>]+>', ' ', m.group(1))
       body = re.sub(r'\s+', ' ', body).strip()
       print(body[:5000])
   ```
   The Frontiers page exposes the full abstract + introduction +
   discussion in `<h2>Abstract</h2>` / `<h2>1 Introduction</h2>` /
   `<h2>4 Discussion</h2>` / `<h2>5 Conclusion</h2>` blocks. Most open-access
   journals use the same H2-section pattern.

## De-dup recipe (verified 2026-07-04)

```bash
cd news
grep -lE "(Yue.*Mengqi|Yue Mengqi|2,290.*patients|30.*RCT.*PSD|RR = 1\.29|Frontiers.*dysphagia)" *.html
# 0 matches = shippable
```

Anchor-string choices:
- **First-author family name + given name** (avoid common surnames; use
  the full "Yue Mengqi" or "Mengqi Yue" pattern)
- **Headline patient count** ("2,290 patients", "1,234 women")
- **Headline RCT count** ("30 RCTs", "22 RCTs")
- **Headline RR or p-value** ("RR = 1.29", "p < 0.0001")
- **Journal + topic** ("Frontiers in Neurology dysphagia", "Lancet IVF")

Zero matches across the 70-article library = the meta-analysis is
shippable. Any 1+ match = investigate whether the existing article is
the same paper, a different meta-analysis on the same topic, or a
non-overlapping story.

## Internal-link targets for this archetype (verified 2026-07-04)

The 2026-07-04 article cross-linked to 8 existing pages:
- `../blog/acupuncture-treatment-china-2026.html` (TCM cost reference)
- `../blog/tcm-traditional-chinese-medicine-guide.html` (TCM evergreen)
- `../blog/integrated-chinese-western-medicine-china.html` (institutional model)
- `../blog/deep-brain-stimulation-china-2026.html` (parallel Western-tech + TCM integration)
- `../blog/neurosurgery-cost-china.html` (cost context for the rehab-block decision)
- `2026-07-02-acupuncture-ivf-...html` (parallel meta-analysis article from 2 days earlier)
- `2026-07-01-cuhk-medicine-...html` (parallel Chinese-academic evidence-base article)
- `2026-06-11-china-medical-tourism-cutting-edge-cheap-bloomberg.html` (cost-comparison framing)

For a stroke-rehab archetype, also consider:
- `../blog/baduanjin-eight-brocade-complete-guide.html` (parallel TCM modality)
- `../blog/stem-cell-therapy-china-access.html` (parallel advanced-therapy framing)

The 8-link footer matches the 2026-07-02 acupuncture-IVF article
exactly. Consistency with the prior article's footer is a strong
internal-linking signal for Googlebot.

## Differentiation from the existing archetypes (verified 2026-07-04)

| Archetype | Lead anchor | Word count | Key H2 sections | Internal link count |
|---|---|---|---|---|
| Phase X data readout | Trial ORR/PFS | 3,000-4,500 | Lead / why-matters / data / patient access | 6-8 |
| Regulatory approval | NMPA / FDA / MHRA approval | 4,500-5,500 | Lead / approval mechanics / eligibility / access / cost / what-changes / medical-tourism | 8 |
| IND clearance | Preclinical IND | 2,500-3,500 | Lead / why-shippable / mechanism / preclinical / indications / competitive / what-to-watch | 6-8 |
| Cell-therapy Phase 1 | iPSC / CAR-T Phase 1 | 2,000-2,500 | Lead + dual-track / structural-claim / what-molecule-is / what-was-announced / competitive / what-to-watch | 6-8 |
| Structural policy | NHC / NMPA framework | 4,000-4,500 | Lead / why-shippable / what-the-order-does / prior-vs-new / who-benefits / what-to-watch | 6-8 |
| **Clinical meta-analysis (NEW, 07-04)** | **Peer-reviewed meta-analysis** | **4,000-5,000** | **Lead / what-the-meta-found / what-the-protocol-looks-like-at-a-Chinese-center / why-Chinese-evidence-base-is-large / how-international-patient-accesses / what-to-ask / what-next-12-18-months-bring** | **8** |

The new archetype is the longest of the 6 and has the most
institutional-context sections (sections 4-5). The 4,000-5,000 word
count is necessary to give the meta-analysis search strategy + subgroup
analysis + the Chinese-evidence-base institutional context the depth
they need to be credible. The 8 internal links match the existing
regulatory-approval archetype's internal-link density.