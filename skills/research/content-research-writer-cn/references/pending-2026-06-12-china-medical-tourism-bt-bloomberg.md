# Pending: 2026-06-12 — China Medical Tourism BT/Bloomberg

**Status:** Research complete; article not written; cron budget exhausted on Bing News discovery + Business Times fetch (200+ tool calls). Pending file written for next cron run to pick up.

## Source (verified working, 2026-06-12)

**Primary:** https://www.businesstimes.com.sg/international/global/chinas-nascent-medical-tourism-lures-foreign-patients-cutting-edge-cheap-medical-care
- Published: 2026-06-11 09:02 SGT (datePublished meta)
- ~220KB, full body, JSON-LD intact
- Body selector: `<p class="whitespace-pre-wrap break-words mb-4 md:mb-6" data-testid="article-paragraph-component">`
- Syndicated to: MSN, AP, Yahoo Finance (all mirrors, not canonical)

**Secondary mirror:** https://www.prnewswire.co.uk/news-releases/lecheng-launches-service-center-for-international-medical-tourism-302797757.html
- 2026-06-11, China Daily / Lecheng service center (May 29) angle; stub article

## Target article (next run)

**Filename:** `2026-06-11-china-medical-tourism-cutting-edge-cheap-bloomberg.html`
- Use press release date (2026-06-11), not cron run date, per the verified 2026-06-11 date-preservation rule
- Canonical URL: `https://chinahospitalsguide.com/news/2026-06-11-china-medical-tourism-cutting-edge-cheap-bloomberg.html`
- Meta `lastmod` in sitemap: 2026-06-11

## Key facts to weave into the article (from BT body)

1. **Stuart Lye, 58, New Zealand high-risk myeloma patient**: 2018 diagnosis, 3-month prognosis, CAR-T via Shanghai clinical trial in 2025; 7 weeks treatment, US$65,000 all-in (vs A$500,000 in Australia). Direct quote: "Looking outside of New Zealand for CAR-T was my only option. China was an easy choice as they are at the forefront in research and development, and the treatment is near a 10th of the cost of other countries."

2. **SinoUnited Health, Shanghai**: ~30 foreign CAR-T patients since late 2024. CEO Shi Haoying: "The patients chose China for something they can't get at home. I think the growing attention to medical tourism to China is the inevitable result of long-term accumulation and development in many areas."

3. **Victor Cao, Joyful Medical agency, Shanghai**: "There are two reasons why a patient travels for medical treatments: availability of advanced treatments and price. Chinese people used to travel overseas for treatments that were not available at home, but now tables have turned."

4. **Cost arbitrage data** (American Cancer Society + China data):
   - US CAR-T: $300,000–$475,000/infusion
   - China CAR-T: $150,000–$180,000
   - One therapy (sub-300,000 yuan, ~S$57,036) approved in China

5. **7 approved commercial CAR-T products in China** = matches US; China leads world in CAR-T clinical-trial count (ClinicalTrials.gov)

6. **Market data:**
   - Global: US$34B → US$126B by 2035 (Grand View Research)
   - China: US$1.3B (2025) → US$3.4B (2035) (Market Research Future)

7. **Lecheng International Medical Tourism Pilot Zone (Hainan)**: designated 2013; "just a few thousand foreign medical tourists last year" vs "hundreds of thousands of domestic patients"; allows access to drugs/devices/therapies approved elsewhere but not in mainland China

8. **McKinsey data (2024):** China at parity with US in experimental medicines entering clinical testing; trials 2-5x faster than US/EU

9. **Clinical milestones mentioned in BT piece:**
   - 2024: China first to use homegrown cell therapy for pediatric lupus
   - 2025: Asia's first cross-species kidney transplant
   - March 2026: world's first commercial brain-implant approval (spinal cord injury)

10. **May 2026 regulation shift** (KEY NEW DATA POINT):
    - Banned hospitals from charging clinical-research fees
    - Allowed qualified hospitals to commercialize cell therapy, BCI, xenotransplantation without traditional drug registration
    - Per Zhao Bing (China Renaissance Securities): "The regulations are intended to shift China's emerging medical technologies from a period of rapid, loosely supervised expansion towards stronger oversight and regulatory compliance."

11. **Skeptical voices (counter-narrative):**
    - Jacob Becraft (Strand Therapeutics, Boston): "Personally, I would certainly have reservations about rushing off to get into a clinical trial in China."
    - Jeroen Groenewegen-Lau (Mercator Institute): "Many new treatments... are made in China but too advanced for the state of its healthcare system and the ability of its patients to pay for these things."
    - Zhao on Thailand/Singapore competition: "Why has Thailand been able to develop medical tourism successfully? It had tourism first, and then medical tourism. Even foreigners who have lived in China for years still encounter many inconveniences in daily life, so travelling to China for serious treatments will unlikely become mainstream anytime soon."

## De-dup check (next run must do FIRST)

The chinahospitalsguide library already has:
- `2026-04-18-china-medical-tourism-car-t-global-destination.html` — SinoUnited Health, CAR-T international destination angle
- `2026-06-06-pakistani-patient-cart-shanghai-jiahui-lymphoma.html` — SinoUnited + Jiahui, Pakistani patient
- `2026-06-03-hainan-boao-lecheng-medical-tourism-pilot-zone.html` — Lecheng May 29 service center

The new BT article is shippable BECAUSE it carries these net-new data points absent from prior coverage:
- Stuart Lye NZ patient narrative (first NZ→China CAR-T case documented on the site)
- $65,000 vs A$500,000 cost comparison
- May 2026 clinical-trial-fee ban
- March 2026 brain-implant commercial approval
- US$1.3B→US$3.4B China market projection
- Lecheng "thousands vs hundreds of thousands" patient-volume framing
- Skeptical voices (Becraft, Groenewegen-Lau, Zhao)

**If ≤2 of these are preserved in the next article, the piece is too duplicative and should be skipped (宁缺毋滥).**

## Suggested 9-section structure

1. **News brief** — BT piece + 3-bullet summary of the trend
2. **Why foreigners are coming now** — visa-free policy + cost arbitrage + treatment availability
3. **The Stuart Lye case** — full patient narrative as the human anchor
4. **The clinical landscape** — 7 approved CAR-Ts, China leads in trials, McKinsey data
5. **Cost: how cheap is cheap** — table comparing US vs China CAR-T, A$500K vs $65K NZ
6. **The May 2026 regulation shift** — clinical-trial-fee ban + commercialization rules
7. **Lecheng and the Hainan path** — link to 2026-06-03 article
8. **The skeptical case** — Becraft, Groenewegen-Lau, Zhao on why this isn't Thailand-style medical tourism yet
9. **Outlook** — what to watch over 18 months

## Internal link targets

- `2026-06-03-hainan-boao-lecheng-medical-tourism-pilot-zone.html` (Lecheng — Section 7)
- `2026-06-06-pakistani-patient-cart-shanghai-jiahui-lymphoma.html` (SinoUnited + Jiahui — Section 3 or 4)
- `2026-04-18-china-medical-tourism-car-t-global-destination.html` (SinoUnited history — Section 4)
- `2026-06-10-antengene-atg-201-bispecific-autoimmune-pku.html` (PKU autoimmune bispecific — Section 5 or 8)

## External link targets

- BT primary source
- American Cancer Society CAR-T cost page
- ClinicalTrials.gov CAR-T count page
- Hainan provincial government / Lecheng zone
- Mercator Institute China Studies (Groenewegen-Lau quotes)

## Em-dash target

17-23 per 1200 words (chinahospitalsguide verified baseline). The BT body is naturally heavy on em-dashes (Bloomberg house style) — easy to inherit the baseline, but watch for over-22/1200.

## Cron state at end of 2026-06-12 run

- Working tree: clean on `master`, in sync with `origin/master`
- SSH remote intact: `git@github.com:qzw-alt/chinahospitalsguide.git`
- Last shipped: `2026-06-10-antengene-atg-201-bispecific-autoimmune-pku.html`
- Article NOT written; no local commit; nothing to push
- Cached raw fetches: `/home/ubuntu/.hermes/workspace/website/.hermes/tmp/lecheng-research/bt1.html` and `lecheng.html`
- Pending note written to this file
