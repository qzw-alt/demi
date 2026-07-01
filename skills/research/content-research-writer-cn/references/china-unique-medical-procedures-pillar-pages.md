# China's Unique Medical Procedures — Pillar Page Map (Verified 2026-07-01)

This file lists the **11 pillar / sub-pillar pages** built on top of `china-unique-medical-procedures.md`. All URLs are live as of 2026-07-01, deployed via chinahospitalsguide.com (commit `a5b7026` for the original batch, `56f6a55` for the duplicate-slug cleanup).

## Pillar Hub (the master page)

- **`/blog/china-unique-medical-procedures-guide.html`** — 3,363 words, 10 H2 sections (one per unique procedure). The KEEP-SLUG page, cross-linked from `blog/index.html` "Featured Pillar Pages" section. Refer to this URL by name; do not create a competing `<slug>.html` page.

## 10 Sub-pillar pages (each ~1,200-5,200 words)

| URL | Topic | Internal links |
|---|---|---|
| `/blog/integrated-chinese-western-medicine-china.html` | 中西医结合 — the exclusive model | TCM guide, acupuncture, Hainan wellness, cancer treatment |
| `/blog/autonomous-robotic-surgery-china.html` | AFMU Xi'an 2017 world's first autonomous dental implant | Spine surgery, neurosurgery, JCI hospitals, hospital rankings |
| `/blog/solid-tumor-car-t-china.html` | satri-cel NMPA approval June 2026, world's first solid tumor CAR-T | CAR-T news June 2026, cancer treatment, cost |
| `/blog/microsurgery-replantation-china.html` | 60 years of world-firsts including HKUMed 2025 | Neurosurgery, JCI, why China medical treatment |
| `/blog/organ-transplant-china-cost-access.html` | 10,000+/year, kidney $70K vs $300K+ US | Bone marrow transplant, kidney dialysis, JCI |
| `/blog/3d-printed-implants-china.html` | 7-14 days turnaround, 40-60% less | Dental, knee replacement, hip replacement, spine |
| `/blog/hepatobiliary-surgery-china-wu-mengchao.html` | Wu Mengchao legacy + Eastern Hepatobiliary | Cancer treatment, organ transplant, hospital rankings Shanghai |
| `/blog/stem-cell-therapy-china-access.html` | iPSC Parkinson dual FDA+NMPA + Boao Lecheng | Stem cell news June 2026, Boao Lecheng, why China |
| `/blog/crispr-gene-therapy-china-clinical-trials.html` | World's largest CRISPR pipeline | Cancer, stem cell, hospital rankings, Boao Lecheng |
| `/blog/ophthalmology-china-volume-expertise.html` | World's highest surgical volume | Cataract, LASIK, hospital rankings Beijing/Shanghai/Guangzhou |

## TCM Section Injections (verified 2026-07-01, a5b7026)

49 existing disease/procedure blog articles each received a TCM highlight box pointing to `integrated-chinese-western-medicine-china.html` plus disease-specific cross-links. Files modified: every blog post with disease/specialty keywords (cancer, orthopedic, IVF, eye, dental, cardio, neuro, wellness, cosmetic, kidney, transplant). Use `grep -l "🌿 TCM for" blog/*.html` to enumerate — current count is 49.

## When to write a new pillar page (decision rules)

A new pillar page on `china-unique-medical-procedures` topic should be created only when:
1. **No existing sub-pillar covers the topic** — check the 10 URLs above first
2. **The topic is significant enough for 1,200+ words** — short topics belong in news articles or as a section in an existing sub-pillar
3. **The topic ties to 3+ hospital names or sources** — pillars without name-level hospital backing read as generic

If a candidate pillar fails one of these, route the topic to the daily news cron (`seo-article-publish-cron`) instead. Pillar pages are expensive (2,000-5,000 words) and slow to write; reserve them for topics that justify the depth.

## Slug naming when adding new sub-pillars

Use the pattern `<topic>-china.html` or `<topic>-china-<year>.html`. Examples that already exist:
- `integrated-chinese-western-medicine-china.html` — descriptive slug
- `autonomous-robotic-surgery-china.html` — feature-name slug
- `solid-tumor-car-t-china.html` — abbreviated clinical-term slug

Avoid generic `<topic>.html` (collides with existing pages) and avoid `<topic>-guide.html` (collides with the master pillar). The `-china` suffix disambiguates every sub-pillar cleanly.

## Cross-link matrix (verified 2026-07-01)

Every sub-pillar page has 5-7 internal links back to:
- The master pillar (`china-unique-medical-procedures-guide.html`)
- 2-3 other sub-pillars (creating a cluster)
- 1-2 news articles from `/news/YYYY-MM-DD-*.html`
- 1-2 existing blog articles (cost guides, hospital guides)

When writing a new sub-pillar, follow the cross-link pattern, not the strict 5-7 count. The connection graph matters more than the link count.

## Pitfalls observed during the 2026-07-01 build

- **Existing pillar check** — `china-unique-medical-procedures-guide.html` was created by a sibling session at 16:35 UTC on 2026-07-01 (commit `24e927c`). The orchestrator's plan to create `china-unique-medical-procedures.html` would have produced duplicate content. Always run `ls <dir>/<topic>*` and `grep -l "<topic-phrases>"` BEFORE writing a pillar.
- **Subagent internal-link prompts** — when delegating pillar-sub-page creation to subagents, the prompt must explicitly list the kept-slug master pillar as the cross-link target. If the prompt says "10 China-unique procedures" without specifying the master-slug URL, the subagent may invent a new master-slug and create a duplicate.
- **301 redirect instead of file deletion** — when the duplicate is already pushed to Cloudflare, deleting the file alone leaves the URL serving 404 (worse than serving 301). Add the 301 in `_redirects` BEFORE deleting the file. Final state: both URLs serve the kept page; the deprecated URL signals retirement to Google.
