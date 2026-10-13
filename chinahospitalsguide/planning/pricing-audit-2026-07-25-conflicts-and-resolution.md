# chinahospitalsguide.com 3-Tier Service Audit & Resolution Guide

**Status**: Active work — 4 conflicts pending
**Date**: 2026-07-25
**Trigger**: User confirmed 3-tier restructure (L1 $49 / L2 $149 / L3 $399) is desired, but website has not been fully updated.
**Source audit data**: live scan of `~/chinahospitalsguide` master branch synced with origin/master (commit `1ccc80a`)

---

## 1. Current Confirmed State

### Pricing definition (decided)

| Tier | Name | Price | What is included |
|---|---|---|---|
| **L1** | Hospital Shortlist | **$49** | 2-3 hospital recommendations with cost comparisons, transport guidance, preparation checklist. Delivered within 24 hours. Information only — no hospital contact. |
| **L2** | Hospital Verification | **$149** | Weiye sends patient's case summary in Chinese to 2-3 hospitals, translates the hospital responses into English, connects patient directly with the best-fit hospital. Delivered within 4-7 business days. |
| **L3** | Full Journey Management | **$399** | Everything in L2, plus: medical record translation, visa invitation letter, appointment booking, airport pickup, ongoing coordination throughout treatment (matching → discharge). |

### Where the new definition lives

- `thank-you.html` — the only English page with the complete canonical L1/L2/L3 text + upgrade matrix
- `ar-pricing.html` / `id-pricing.html` / `ru-pricing.html` — translated 3-tier tables (Arabic / Indonesian / Russian)
- The 8 other pages that mention pricing have NOT been refactored to this definition

### Commit message typo (not user-approved pricing)

The commit `528e891` has a misleading message that references `$9 / $49 / $99`. This is **a commit-message typo, NOT an actual pricing decision**. Confirmed by the live website state. Do not act on the typo. The canonical prices are **$49 / $149 / $399**.

---

## 2. The 4 Open Conflicts (from previous audit)

### Conflict A — Stale "Pre-Arrival" / "Hospital Match" terminology

| Term | Files affected | Mentions per file |
|---|---|---|
| **"Hospital Match"** (old L1 name) | 9 files | 1–7 mentions each |
| **"Pre-Arrival"** (old L3 name) | 8 files | 1–12 mentions each |

**Files with stale terminology**:

#### File → mentions breakdown

| File | Hospital Match | Pre-Arrival |
|---|---|---|
| `how-it-works.html` | 7 | 12 |
| `about.html` | 3 | 7 |
| `pricing.html` | 4 | 4 |
| `index.html` | 2 | 2 |
| `services.html` | 1 | 2 |
| `contact-new.html` | 2 | 2 |
| `cancer.html` | 1 | 0 |
| `course.html` | 1 | 0 |
| `stories.html` | 1 | 0 |
| `checklist.html` | 0 | 1 |
| `patient-story-program.html` | 0 | 2 |

**Total fixes needed**: ~50 individual text replacements across 11 unique files.

**Fix mapping rules**:

| Old text | New text | Tier reference |
|---|---|---|
| "Hospital Match & Plan" | "**L1 Hospital Shortlist**" or "**Hospital Shortlist (L1)**" | L1 |
| "Hospital Match and Plan" | same as above | L1 |
| "Hospital Matching" (action verb) | "hospital shortlisting" or rephrase as needed | L1 service detail |
| "Pre-Arrival Coordination" | "**L3 Full Journey Management**" or "**Full Journey Management (L3)**" | L3 |
| "Pre-arrival coordination" (lowercase) | same as above | L3 |

**Priority**: pricing.html (the canonical pricing page) and how-it-works.html (the user journey explanation page) are top priority. Index pages (index.html, sg.html, id.html, ru.html, ar.html) are second priority because they are entry points for SEO traffic. Services.html and about.html are tertiary.

### Conflict B — Pricing definition (RESOLVED)

User confirmed the canonical pricing is **$49 / $149 / $399** ("Hospital Shortlist / Hospital Verification / Full Journey Management"). The commit message typo on `528e891` ("$9 / $49 / $99") is NOT to be acted on.

This conflict is now **closed by confirmation**. No code change needed for the definition itself.

### Conflict C — Currency (RMB in patient report pages)

After the more recent commits, **zero files use the ¥ symbol** — this conflict appears to have been already resolved in prior commits (likely during the `cleanup: remove 309 non-website files from repo, fix sitemap and SEO config` commit). Files such as `report-carlos-mendoza-1782620864897.html` are now in USD. **Resolved**.

### Conflict D — Mixed old/new tier names

Two files use the new L1/L2/L3 names (`thank-you.html` + the 3 translated pricing pages) while the majority (17 files) still use the old "Hospital Match" / "Pre-Arrival" terminology. This is the same root issue as Conflict A. Resolving Conflict A (rename everything to L1/L2/L3) will close Conflict D automatically.

---

## 3. Files Where Conflicts Exist (Full List, 18 files)

| File | Has $99? | Has L1/L2/L3? | Has old name? | Action needed |
|---|---|---|---|---|
| `pricing.html` | ❌ | ❌ | ✅ (8 mentions) | **Top priority** — canonical pricing page |
| `index.html` | ❌ | ❌ | ✅ (4 mentions) | Entry page — fix |
| `how-it-works.html` | ❌ | ❌ | ✅ (19 mentions) | Highest concentration — fix |
| `about.html` | ❌ | ❌ | ✅ (10 mentions) | Brand page — fix |
| `services.html` | ❌ | ❌ | ✅ (3 mentions) | Service detail page — fix |
| `contact-new.html` | ❌ | ❌ | ✅ (4 mentions) | Form page — fix |
| `cancer.html` | ❌ | ❌ | ✅ (1 mention) | Service detail — fix |
| `course.html` | ❌ | ❌ | ✅ (1 mention) | Course listing — fix |
| `stories.html` | ❌ | ❌ | ✅ (1 mention) | Stories — fix |
| `checklist.html` | ❌ | ❌ | ✅ (1 mention) | Checklist — fix |
| `patient-story-program.html` | ❌ | ❌ | ✅ (2 mentions) | Patient program — fix |
| `sg.html` | ❌ | ❌ | ❌ | OK |
| `id.html` | ❌ | ❌ | ❌ | OK (only $49/$399 generic mentions) |
| `ru.html` | ❌ | ❌ | ❌ | OK |
| `ar.html` | ❌ | ❌ | ❌ | OK |
| `ar-pricing.html` | ❌ | ✅ | ❌ | OK (already uses new L1/L2/L3 + 3 tiers) |
| `id-pricing.html` | ❌ | ✅ | ❌ | OK |
| `ru-pricing.html` | ❌ | ✅ | ❌ | OK |
| `thank-you.html` | ❌ | ✅ | ❌ | OK (canonical reference for new copy) |

---

## 4. Also Affected: Multi-language index pages

The four landing pages (`sg.html`, `id.html`, `ru.html`, `ar.html`) still say:
> "Biaya layanan: $49 (rekomendasi RS) atau $399 (koordinasi penuh)" (etc.)

This implicitly says there are **two** services ($49 and $399). It does not mention **$149 / Hospital Verification** at all. This is misleading for international visitors who need to know the third tier exists. These should be updated to mention all three tiers or at least hint at the middle option.

---

## 5. Audit of: Other potential conflicts (semantic, not yet numerically)

These are not yet confirmed by exact-match scanning but are plausible from re-reading pricing.html and services.html. To be verified when rename happens:

### Potential conflict E: Does L3 include treatment-period coordination?

- `thank-you.html` describes L3 as: "ongoing coordination throughout your treatment — from matching to discharge."
- `pricing.html` (old version) describes the prior $399 as: "Treatment period — hospital communication and emergency coordination. Discharge support — medical summary, medication instructions, follow-up handover."
- These two are consistent. ✅ No conflict.

### Potential conflict F: Refund policy unification

- `pricing.html` says: "Hospital Match & Plan: Non-refundable once delivery work begins. Pre-Arrival Coordination: $369 refund if cancelled 72+ hours before service start."
- After rename, this should be updated for L1 / L2 / L3:
  - **L1 $49**: refundable / non-refundable? The old rule was "non-refundable after delivery" — should L1 keep this?
  - **L2 $149**: new tier — refund policy needs definition
  - **L3 $399**: keep old rule ($369 refund 72h+ before)

This is a **product policy question** that should not be auto-decided by code-only renaming. See Section 7.

### Potential conflict G: Airport pickup inclusion

- `thank-you.html` for L3 says: "Includes everything in L2, plus... airport pickup, and ongoing coordination throughout your treatment"
- Old `pricing.html` for $399 said: "airport pickup arrangement"
- These are consistent: L3 includes airport pickup. **No conflict**, but the rename should preserve this explicitly.

---

## 6. Recommended Implementation Order

To keep the cleanup safe and reviewable, do the rename in 3 phased commits, each independently publishable.

### Commit 1: Canonical pricing page (`pricing.html`)

- ~8 text replacements
- Risk: low (single page, well-known content)
- Verification: open the page in a browser, confirm the table reads "L1 Hospital Shortlist ($49) / L2 Hospital Verification ($149) / L3 Full Journey Management ($399)"

### Commit 2: Service detail and journey pages

- Files: `how-it-works.html`, `services.html`, `about.html`
- ~32 text replacements across 3 files
- Risk: medium (these are content-heavy pages where text replacement could break sentence flow if done blindly)
- Recommendation: regenerate the relevant sections from `thank-you.html` text, not just find-and-replace

### Commit 3: Entry / SEO / index pages

- Files: `index.html`, `contact-new.html`, `cancer.html`, `course.html`, `stories.html`, `checklist.html`, `patient-story-program.html`
- ~14 text replacements across 7 files
- Risk: low (most are short references)
- After this commit, the only place "Hospital Match" / "Pre-Arrival" should remain is in the canonical reference: `thank-you.html`

### Optional Commit 4: Multi-language index pages

- Files: `sg.html`, `id.html`, `ru.html`, `ar.html`
- Update the pricing line to mention 3 tiers, not 2
- Translation per file; should mirror the structure in `thank-you.html`

---

## 7. Open Decisions Still Required from Weiye

1. **Refund policy for L2 ($149)**: ?? (the L2 tier did not exist before; the refund policy is a new product decision)
2. **Refund policy for L1 ($49)**: keep "non-refundable after delivery" or change?
3. **Update the multi-language index pages in this same PR, or separate PR?**
4. **Update the `internal-research-notes/` directory pricing reference if any**: should be cleaned in same PR as it contains the old definitions

---

## 8. Provenance of This Audit

This audit was generated by:
1. Pulling master to origin/master (commit `1ccc80a`)
2. Scanning all 18 *named* HTML files in the repository for: regex matches of `$9 / $49 / $99 / $149 / $399 / ¥49 / ¥399 / L1 / L2 / L3 / Hospital Match / Hospital Shortlist / Hospital Verification / Full Journey / Pre-Arrival`
3. Listing untracked files (20 found; mostly research notes and unrelated content)
4. Cross-referencing with a previous audit to identify which conflicts were resolved between audits (currency conflict → resolved; rename conflict → ~30% complete)

---

## 9. Files Now Documented

| Document | Location | Status |
|---|---|---|
| Original 3-tier planning doc | `planning/pricing-redesign-2026-07-24.md` | Superseded by this audit (still useful as background) |
| This audit report | `planning/pricing-audit-2026-07-25-conflicts-and-resolution.md` | Current source of truth for conflicts |

---

**Next step**: Weiye reviews this report and either:
- (a) Approves the 3-commit implementation plan and assigns it
- (b) Requests changes to the plan (e.g., different commit boundaries, different tier names, different prices)
- (c) Defers all rename work to a future batch

The audit itself does not modify any website file — it only documents what needs to change.
