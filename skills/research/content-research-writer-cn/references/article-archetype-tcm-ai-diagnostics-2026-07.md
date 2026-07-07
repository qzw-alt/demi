# Article Archetype: TCM AI Diagnostics & Imaging (verified 2026-07-07)

The 2026-07-07 article on Guanwei Intelligent Technology's AI TCM constitution scanner established two patterns specific to TCM AI / imaging stories:

## 1. Template B is the default structure for TCM-modernization stories

When the news is "a Chinese device/system using AI or digital tools to modernize a TCM practice," the structure should be:

1. **Lead** — what the device does, who built it, the headline data point (language count, pilot locations, etc.)
2. **What the device does, in plain language** — explain the TCM theory being automated (e.g. four diagnoses 望闻问切 → facial-ocular scan) so non-TCM readers can follow
3. **Where it showed up** — the conference, the policy document, the event that gave it the platform
4. **The international angle** — language rollouts, overseas pilots, what makes the cross-border piece distinctive
5. **What the device does NOT do** — three honest limits (e.g. NOT a clinical diagnosis, NOT replacing in-person, NOT substituting for medication review). This section is the credibility differentiator.
6. **Broader context** — China's TCM AI export strategy, 15th Five-Year Plan links, where this fits competitively
7. **How an international patient uses it today** — specific cost, location, access path. This is the medical-tourism translation.
8. **What to watch 12-18 months** — 3 concrete signals (NMPA Class III filing, English validation cohort, HIS integration)
9. **A grounded take** — opinions about who this is for, the questions worth asking, what to watch out for
10. **Data-box callout + Related reading**

The 07-07 Guanwei article ran 2,704 words at clean humanize-pass (single `showcase` swap). Em-dash density 11.5/1200 (within tolerance for a 2,700-word piece).

## 2. Image-asset naming pitfall — verification recipe

**Pitfall (re-hit 2026-07-07):** when adding a `news/index.html` card for a new article, always `ls images/ | grep -iE "<category-keyword>"` before naming the image. TCM/acupuncture-themed articles do NOT have a `tcm-acupuncture.jpg` in this repo's `images/` directory. The verified working fallbacks are:

- `wellness-spa.jpg` — for any TCM-wellness, acupuncture, herbal medicine card
- `china-hospital.jpg` — for any patient-consultation card without a specialized image
- `medical-tourism.jpg` — for any medical-tourism framing
- `hainan-beach.jpg` — for any Lecheng / Hainan card

**Recipe (must run before patch):**
```bash
ls images/ | grep -iE "tcm|acupuncture|chinese|wellness|spa"
# Output is empty for tcm/acupuncture; wellness-spa.jpg exists
# Patch uses ../images/wellness-spa.jpg
```

If the article would benefit from a more specific image but none exists, reuse `wellness-spa.jpg` rather than guessing a non-existent filename (which results in a broken image on the live page).

The script `references/best-image-fallback.sh` could be wired in for future cron runs but the inline grep is sufficient.

## 3. Xinhua-vs-CE.cn same-day cluster problem (new lesson, verified 2026-07-07)

When a same-day cluster produces 3-5 Xinhua wire pieces (Global Digital Economy Conference 2026 produced one Beijing piece, one Guangzhou piece, one Zhongguancun piece on the same index page), `english.news.cn` may serve a different article than the URL your Bing News query surfaced. **Symptom:** fetch the Xinhua URL you have, get an article on a different topic with a different date. **Fix:** pivot to `en.ce.cn` and re-search by the slug or by date — CE.cn mirrors the same Xinhua wire with its own publish-date meta tag.

**Detection signal:** the page's `<meta property="og:title">` does NOT match the headline from your Bing News URL. Or: the page's `<meta name="publishedtime">` returns a date that's >48 hours before/after your target event date.

**Recipe when hit:**
```bash
curl -A "Mozilla/5.0" -sL "http://en.ce.cn/main/latest/202607/" -o /tmp/ce_index.html
grep -oE 't20260706_[0-9]+.shtml' /tmp/ce_index.html | head -10
# Find the slug matching your target (same numeric suffix as en.ce.cn URL from Bing)
curl -A "Mozilla/5.0" -sL "http://en.ce.cn/main/latest/202607/t20260706_NNNNNNN.shtml" -o /tmp/ce.html
grep -oE '<meta name="publishdate" content="[^"]+"' /tmp/ce.html
```
