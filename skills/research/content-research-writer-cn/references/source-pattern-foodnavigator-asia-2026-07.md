# FoodNavigator-Asia (foodnavigator.com) — 7th-tier source for TCM-industry / nutrition-industry / consumer-product stories (verified 2026-07-22)

## Summary

FoodNavigator-Asia is the Asia edition of FoodNavigator, the William Reed–published food/beverage industry trade press. It works as a reliable cron-sandbox fetch for **TCM-adjacent industry / functional-food / consumer-nutrition / executive-interview** stories that the pharma trade press (GEN, pharmaphorum, FiercePharma) does not cover.

The 2026-07-22 cron run surfaced the Yili Group × Beijing Tongrentang partnership announcement (TCM recipes in dairy products for elderly nutrition) via Bing News. The canonical source for the Yili quote was FoodNavigator-Asia (`https://www.foodnavigator.com/Article/2026/07/20/healthy-ageing-yili-taps-tcm-flavour-to-boost-elderly-nutrition/`).

## Fetch recipe

```bash
curl -A "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36" \
  "https://www.foodnavigator.com/Article/2026/07/20/healthy-ageing-yili-taps-tcm-flavour-to-boost-elderly-nutrition/" \
  -o /tmp/foodnav.html
```

**Returns:** ~1.18 MB of full article HTML. WordPress-style `<article>` body block with substantive `<p>` paragraphs (200-500 chars each, 18-25 paragraphs in a typical industry piece). Named executives and companies are in plain prose, not buried in JS.

## Body extraction recipe

```python
import re
with open('/tmp/foodnav.html') as f:
    c = f.read()
# Strip styles/scripts first (avoid the 57KB CSS dump trap from SCMP)
c = re.sub(r'<style[^>]*>.*?</style>', ' ', c, flags=re.DOTALL)
c = re.sub(r'<script[^>]*>.*?</script>', ' ', c, flags=re.DOTALL)
# Standard article body extraction
m = re.search(r'<article[^>]*>(.*?)</article>', c, re.DOTALL)
body = m.group(1) if m else c
text = re.sub(r'<[^>]+>', ' ', body)
text = re.sub(r'\s+', ' ', text).strip()
```

The 07-22 Yili piece yielded 4,579 chars of clean prose from this single regex pass. Enough for a 1,800-word article without a second source.

## Date verification

The publication date is encoded in BOTH the URL (`/Article/YYYY/MM/DD/`) AND the `<title>` tag (`Healthy ageing: Yili taps TCM, flavour to boost elderly nutrition`). For additional verification:

```bash
grep -oE '<meta[^>]*property="article:published_time"[^>]*content="[^"]+"' /tmp/foodnav.html | head -1
```

The 07-22 URL had `/Article/2026/07/20/` (article date = July 20) but the article body referenced the Growth Asia Summit held 8-10 July. The publication date in the URL is the source of truth for "fresh 热点" claims; the summit date is a context anchor.

## When to use FoodNavigator-Asia (decision rule)

Use it when the lead is a **TCM-adjacent industry / consumer-product / functional-food / nutrition-industry** angle, specifically:

- TCM-ingredient food or beverage launches (Yili × Tongrentang, nutraceutical launches, herbal-infused SKUs)
- Trade-show coverage of TCM at industry events (Growth Asia Summit, Vitafoods Asia, Fi Asia)
- Executive interviews about TCM ingredient supply chains (Yili VP, Tongrentang CEO, By-Health CEO, etc.)
- Dairy / beverage / supplement brands adopting TCM recipes for elderly, maternal or pediatric nutrition
- Asia food regulatory changes touching TCM or herbal ingredients (China SAMR blue-hat reviews, Singapore SFA, Thailand FDA, Japan MHLW)
- Functional-food clinical trials (probiotic + TCM combinations, postbiotic + herbal extracts)

**Do NOT use** for:

- Pure pharma / biotech / oncology / cell therapy stories (use pharmaphorum, GEN, FiercePharma mirror via Manila Times, etc.)
- Hospital-specific clinical trial news (use Akeso / CarsGen / Oricell IR pages)
- Government policy on NMPA / NHC (use GEN.com for the 06-30 Order 818 archetype)
- University medical center press releases (use Mirage News or finanznachrichten.de)

## What the 07-22 Yili × Tongrentang article pulled from the source

Named anchors extractable from a single FoodNavigator-Asia fetch:

- **Speaker:** Ignatius Szeto, Vice President, Yili Group
- **Event:** Growth Asia Summit 2026, Marina Bay Sands, Singapore, 8-10 July 2026
- **TCM partner:** Beijing Tongrentang (同仁堂), 355-year-old pharmacy chain with its own hospitals and pharmaceutical manufacturing
- **Three product lines:** bone and joint health (TCM-recipe dairy), immunity (lactoferrin + goji berries 枸杞), wider Xinhuo (欣活) functional range
- **Bioavailability claim:** Yili states that TCM ingredients are not image additives — "Sometimes we change the physical and chemical characteristics of the TCM ingredients so that they're more bioavailable or can exert the actual function they're supposed to"
- **Synergy claim:** "Ingredient combinations are designed to produce synergistic benefits, with efficacy exceeding that of the individual components"
- **Policy backdrop:** Healthy China 2030 + broader preventive healthcare initiatives
- **R&D infrastructure:** Yili's National Technology Innovation Center for Dairy, working with Chinese Academy of Sciences + Chinese Academy of Engineering experts

This is enough content for a full 1,500-1,800 word article on TCM nutrition industry + hospital nutrition clinic + split regulatory framework (food vs. clinical TCM), without needing a second source.

## Tier position in the cron source ladder

FoodNavigator-Asia sits at **7th tier** for this site — between GEN.com (6th tier, pharma/biotech policy) and the ChinaDaily.com.cn section scraping fallback (8th tier). It is NOT a substitute for the pharma-tier sources when the lead is clinical data; it IS a substitute when the lead is industry-side TCM-nutrition framing.

The tier ladder for chinahospitalsguide.com cron runs (as of 2026-07-22):

| Tier | Source | Angle |
|---|---|---|
| 1st | Bing News (when working) | headline discovery across all sources |
| 2nd | Akeso / CarsGen / Oricell IR pages | Chinese biotech press releases |
| 3rd | Manila Times PR Newswire mirror | English pharma/biotech press releases |
| 4th | finanznachrichten.de | German PR Newswire mirror, academic medical centers |
| 5th | Mirage News | University medical center press releases (HKUMed, Tsinghua, etc.) |
| 6th | GEN.com / pharmaphorum | Biotech policy/regulatory/clinical-data |
| **7th** | **FoodNavigator-Asia** | **TCM-industry / nutrition-industry / consumer-product** |
| 8th | ChinaDaily.com.cn + chinadaily.com.cn section scraping | Government / state media / official wire |

## Pair-with sources

For a FoodNavigator-Asia lead on TCM industry, pair with:

- **Beijing Tongrentang official site** (`tongrentang.com`) — for the partner's pharmacy history, hospital list, and product catalog
- **Yili Group corporate site / IR page** (`yili.com`) — for product range, R&D center details, and quarterly disclosures
- **China SAMR (国家市场监督管理总局) blue-hat registry** — for verifying health-food claims on specific SKUs
- **Local Chinese trade press** — `21jingji.com` (21世纪经济报道), `cls.cn` (财联社) for follow-up coverage in Chinese
- **English-language pharma coverage** — only if the TCM industry story has a clinical-trial angle (most don't)

## Pitfalls

**Pitfall 1 — globaltimes.cn SPA shell vs. FoodNavigator working body:** the 06-02 PITFALL table flags `globaltimes.cn` as returning only the navigation shell (14KB). FoodNavigator-Asia is the inverse — large payload (1.18MB), full body in `<article>`, no JS-buried payload. Don't generalize "Asia news sites are blocked" from the globaltimes case to FoodNavigator; they are different platforms with different cron-sandbox behavior.

**Pitfall 2 — article date vs. event date:** the URL date (`/Article/YYYY/MM/DD/`) is the publication date. For industry-event coverage, the event may be days or weeks earlier (the 07-22 article used the 07-20 URL for an 8-10 July summit). For "fresh 热点" claims, anchor on the publication date. For "context anchor" framing, the event date is what readers actually want.

**Pitfall 3 — named-executive quote attribution:** FoodNavigator-Asia is industry trade press and typically attributes quotes to the speaker's title and company (e.g. "Ignatius Szeto, Vice President, Yili Group"). Always grep the article body for the exact title spelling before writing — Chinese corporate titles (副总裁, 首席科学家, 董事长) translate inconsistently across English-language press.

## Pending-article handoff format (if used as a recovery file)

If a cron run hits the cap mid-FoodNavigator-Asia pipeline, the pending file should document:

1. The exact URL (`https://www.foodnavigator.com/Article/YYYY/MM/DD/slug/`)
2. The publication date (URL-encoded) and event date (body text)
3. Named speakers with title + company
4. The TCM partner (if any) with 1-line description
5. The specific formulation / clinical / policy claims
6. The suggested article archetype (Template B "Traditional therapy modernization" is the default for FoodNavigator-Asia leads)
7. The internal-link targets (existing TCM nutrition articles + hospital nutrition clinics)
8. The em-dash target (17-23/1200 for chinahospitalsguide, lower for long articles)
9. The score-band target (75-90 for a 1,500-1,800 word article; the 07-22 article shipped at 80/100)