# Pricing Tier Evolution — chinahospitalsguide.com

> **Maintained by**: chinahospitalsguide-content skill
> **Last updated**: 2026-07-25
> **Trigger**: when Weiye mentions pricing / service tier / L1 L2 L3 / "49 149 399" / "Hospital Match" / "Pre-Arrival Coordination"

This file documents the **canonical pricing-tier definition** and the
**rename-completion status** of the chinahospitalsguide 3-tier restructure.

---

## Canonical Definition (verified 2026-07-25)

| Tier | Name | Price | Includes | Delivery |
|---|---|---|---|---|
| **L1** | Hospital Shortlist | **$49** | 2-3 hospital recommendations + cost comparisons + transport guidance + preparation checklist. Information only — no hospital contact. | within 24h |
| **L2** | Hospital Verification | **$149** | Weiye sends case summary in Chinese to 2-3 hospitals, translates hospital responses into English, connects patient directly with best-fit hospital. | 4-7 business days |
| **L3** | Full Journey Management | **$399** | Everything in L2, plus: medical record translation, visa invitation letter, appointment booking, airport pickup, ongoing coordination throughout treatment (matching → discharge). | 1-4 weeks |

### Upgrade matrix (L1 ↔ L2 ↔ L3)

| Upgrade | Customer pays difference |
|---|---|
| L1 → L2 | +$100 (L1 $49 credited toward L2 $149) |
| L1 → L3 | +$350 (L1 $49 credited toward L3 $399) |
| L2 → L3 | +$250 (L2 $149 fully credited) |

**Valid for 30 days** from initial payment.

---

## Files Containing the Canonical Definition (verified complete)

These files correctly use L1/L2/L3 + new tier names:

- `thank-you.html` (canonical English reference — copy text from here)
- `ar-pricing.html` (Arabic translation)
- `id-pricing.html` (Indonesian translation)
- `ru-pricing.html` (Russian translation)
- `sg.html` (Singapore landing — partial, mentions Hospital Shortlist + Full Journey)

---

## Files Still Containing Old Tier Names (verified 2026-07-25, post Weiye's fix commit `022f1b3`)

| File | "Hospital Match" mentions | "Pre-Arrival" mentions | Priority |
|---|---|---|---|
| `pricing.html` | 4 | 4 | 🔴 **top** |
| `how-it-works.html` | 7 | 12 | 🔴 **top** |
| `about.html` | 3 | 7 | 🟠 |
| `contact-new.html` | 2 | 2 | 🟠 |
| `index.html` | 2 | 2 | 🟠 |
| `services.html` | 1 | 2 | 🟡 |
| `course.html` | 1 | 0 | 🟡 |
| `checklist.html` | 0 | 1 | 🟡 |
| `patient-story-program.html` | 0 | 2 | 🟡 |

**Total**: ~50 stale references across 9 files. **pricing.html + how-it-works.html** are top priority because they are the user-journey definition pages.

### Files where "Hospital Match" is acceptable (natural language, NOT a tier name)

- `cancer.html` — "Hospital Matching" is the action verb, not the $49 product name. Weiye confirmed 2026-07-25 commit `022f1b3`.

---

## Mapping Rules for Future Rename

| Old text | New text |
|---|---|
| "Hospital Match & Plan" | "**L1 Hospital Shortlist**" or "**Hospital Shortlist (L1)**" |
| "Hospital Match and Plan" | same as above |
| "Hospital Matching" (action verb) | "hospital shortlisting" (only if it reads awkwardly; often fine to leave) |
| "Pre-Arrival Coordination" | "**L3 Full Journey Management**" or "**Full Journey Management (L3)**" |
| "Pre-arrival coordination" (lowercase) | same as L3 |

**When replacing**: do not just find-and-replace — re-derive from `thank-you.html`
so the surrounding sentences flow correctly.

---

## Commit-Message Typos to Watch For

Two commits have misleading titles:

- `528e891` — title says "$9 / $49 / $99" — **typo**. Real prices are $49 / $149 / $399. Don't act on the title.
- Other commits may have similar price typos in titles — always verify against `thank-you.html` (the canonical English reference) before reporting pricing changes.

---

## Origin of This Document

This reference file was created during the 2026-07-25 audit session. The audit
report is at `planning/pricing-audit-2026-07-25-conflicts-and-resolution.md`
(published to `qzw-alt/demi` repo for archival).

When future sessions touch pricing/service-tier copy on chinahospitalsguide.com,
update both this file and run the audit script in the parent skill's
**Pitfall 7** to refresh the stale-reference count.