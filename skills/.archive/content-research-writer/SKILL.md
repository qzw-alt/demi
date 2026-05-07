---
name: content-research-writer
description: >
  Content research and writing pipeline for blog posts and news articles for the
  China Hospitals Guide medical tourism project. Covers both NEW article creation
  and EXISTING article refresh. This is the ACTIVE skill — the `.archive/` copy
  is deprecated. All blog/news writing goes through this skill.
  Last updated: 2026-05-06 — 10-section structure is now canonical.
tags: ["blog", "news", "seo", "content", "medical-tourism"]
---

# Content Research & Writer Pipeline — ACTIVE SKILL

## Trigger Conditions

Use this skill when:
- Writing a **new** blog article for China Hospitals Guide
- **Refreshing** an existing thin article (under 400 lines)
- Creating a **competitor-gap** article (keyword exists in competitor but not on our site)
- A cron or user asks to "refresh", "upgrade", or "rewrite" an article

## Standard Workflow

```
1. scan thin articles → identify targets
2. research (multi-search) → gather current data
3. write/refresh → 10-section structure
4. humanizer → strip AI patterns
5. verify → push to GitHub
```

## Article Structure: 10-Section Standard

> **Canonical structure for ALL blog and news articles.**
> Reference implementation: `blog/knee-replacement-surgery-china-2026.html` (1,088 lines, approved format)

```
Section 1:  Introduction / Breaking News Hook
             Lead with a specific number or patient angle. No "pivotal moment" language.

Section 2:  China's Current Landscape
             Stats, NMPA approvals, hospital annual volumes, clinical trials

Section 3:  Comparison Table [Factor | US/Intl | China]
             Named hospitals on both sides. Specific costs (USD). Wait times.

Section 4:  Real Cost Breakdown
             Named Chinese hospital → price range. What's included vs excluded.
             "Fudan Cancer Hospital charges ¥650,000–¥1.1M ($89K–$151K)
              including the drug, 14-day hospitalization, CRS monitoring,
              and 3-month follow-up scans."

Section 5:  Real Patient Journey
             Anonymized case: age, country, diagnosis, timeline day-by-day,
             actual total cost paid, one patient quote.

Section 6:  Expert Perspective
             Named expert + institution + specific data + source citation.
             "Dr. Wang at PUMCH has overseen 800+ CAR-T treatments since 2021,
              58% complete response rate in relapsed LBCL — ASH 2025."

Section 7:  Policy & Regulatory Timeline
             Year-by-year: approval dates, regulatory milestones, access pathways.
             Format: "Year: Event — [detail]"

Section 8:  Risks, Limitations & Contraindications
             Honest. Name specific complication rates. State who is NOT a candidate.
             E-E-A-T trust builder — do not skip or soften this section.

Section 9:  Next Steps for International Patients
             Named hospitals that accept foreign patients. Step-by-step process.
             Visa, documentation, language support.

Section 10: Sources
             Numbered list. Each: outlet name, publication date, URL.
```

## Refresh Workflow (for existing thin articles)

**Trigger:** Article under 400 lines, or flagged as "薄/thin" in keyword database.

```
1. read_file existing article (preserve ALL CSS/head/schema/metadata)
2. research current data (multi-search with specific queries)
3. write new content using 10-section structure
4. preserve: ALL existing CSS, schema markup, meta tags, nav/footer
5. overwrite the file (same path)
6. git add → commit → push
7. curl -sI URL | grep HTTP (verify 200)
```

**Parallel refresh batching:** Use `delegate_task` with max 3 concurrent tasks. Batch by similar topic/directory. Each task handles 1 article.

## City-Foreigner Guide Format (Exception to 10-Section Rule)

> **This format pre-dates the 10-section standard and coexists with it. Do NOT apply the 10-section structure to city-foreigner guides.**

**Trigger:** Writing a new "How to See a Doctor in [CITY] as a Foreigner" article. Cities covered so far: Shanghai, Beijing, Guangzhou.

**Format: 8 sections** (see `references/city-foreigner-guide-format.md` for full template)
```
Section 1:  What Makes [CITY] Easier for Foreigners
Section 2:  Public vs Private in [CITY] (table)
Section 3:  Good Starting Points by Need (named hospitals)
Section 4:  How Registration Usually Works
Section 5:  Insurance and Payment in [CITY]
Section 6:  Emergency Care in [CITY]
Section 7:  What To Bring to an Appointment
Section 8:  Best Strategy for Most Foreigners
```

**Schema required:** Article + BreadcrumbList + FAQPage (2–3 Q&As)
**Image:** `images/hospitals/[city]-city.jpg`
**Path:** `blog/how-to-see-a-doctor-in-[city]-as-a-foreigner.html`
**Date:** Use current date (YYYY-MM-DD)

**Hospital research:** Query `api/v1/hospitals.json` for real hospitals in the target city. Filter by `city`, `international`, `tags`.

## Competitor Gap Workflow

**Trigger:** Competitor analysis shows a专题 we don't have.

```
1. Read references/competitors/mychinamed.md for gap list
2. Priority: short-term (LASIK, knee) → medium (spine, facelift) → long (CAR-T)
3. Apply 10-section structure + competitor title format:
   "[Procedure] in China: Cost, Top [Specialty] Hospitals &
    What Foreign Patients Need to Know"
4. Always include named US hospital in comparison tables
5. After publish: update keyword-database.md status: todo→done
```

## De-AI Checklist (run before every publish)

- [ ] No "pivotal moment" / "groundbreaking" / "testament" / "showcases"
- [ ] No "serves as" / "boasts" / "features" / "offers"
- [ ] No em-dash chains (max 1 per article)
- [ ] No hollow superlatives ("best in class", "leading provider")
- [ ] Section 6: Named expert with specific data + source
- [ ] Section 4: Specifies what's included in the cost
- [ ] Section 5: At least one specific patient detail (age, country)
- [ ] Section 8: At least 2 specific contraindications
- [ ] Section 9: At least 2 named hospitals

## Output Requirements

- Schema.org `Article` markup (blog) or `NewsArticle` (news)
- Canonical URL in `<head>`
- Featured image: 1200×630px, saved to article directory
- **sitemap.xml updated after every new article** (add URL entry)
- Push to GitHub → wait 5 min → `curl -sI URL | grep HTTP` verify 200

## Support Files

- `references/competitors/mychinamed.md` — competitor analysis (gap list, structure, title format)
- `references/keyword-database.md` — keyword priority list with status tracking

## Related Skills

- `humanizer` — de-AI pattern removal (step 4 of workflow)
- `news-writing-template` — news-specific format and publishing checklist
- `china-hospitals-guide-deploy` — GitHub push → deployment verification flow
