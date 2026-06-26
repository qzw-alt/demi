# humanize_audit.py false-positive catalog

The `scripts/humanize_audit.py` script (the broad-pattern catalogue that
complements the site-aware `scripts/humanize_score.py`) has a small set of
known false-positive patterns. When the audit returns a low score
(45-65/100) on an article that `humanize_score.py` rates as clean
(80+/100), the divergence is almost always caused by one of the patterns
below, NOT a real humanize issue. Verify the flagged hits against this
list before patching the article.

## Verified false-positive patterns

### 1. `\bfeatures\b` flagged as copula avoidance (verified 2026-06-26)

**Symptom:** 5-15 `features` hits in the "Copula avoidance hits" block of
the audit output, dragging the audit score from 80 → 45 on a 3000-word
article.

**Root cause:** the `COPULA_AVOID` regex list in `humanize_audit.py`
includes `r"\bfeatures\b"`. The actual AI-ism is the **verb** sense
"boasts/features/has" (e.g. "the gallery features four separate
spaces") — not the **noun** sense "the room's measurable features."
Technical/educational articles use the noun 5-15 times per piece
("the room's features", "the chart's features", "the five elements are
the features of the producing cycle"), and all of those are legitimate
prose, not AI-tells.

**Decision rule (verified 2026-06-26 yin/yang article):**
- If the hit is the verb "X features Y" (subject-features-object) where
  the canonical version is "X has Y" → real copula avoidance, patch.
- If the hit is the noun "the features of X" or "a feature of Y" →
  false positive, leave it.

**Quick override test:**
```bash
python3 /home/ubuntu/.hermes/skills/creative/programmatic-seo/scripts/humanize_audit.py /path/to/article.html | grep -A 20 "Copula avoidance"
# If every flagged hit is the noun "features" (referring to a thing's
# measurable characteristics), ignore the copula-avoidance penalty. Use
# the humanize_score.py number as the source of truth.
```

**Future fix:** the `COPULA_AVOID` list should drop `r"\bfeatures\b"`.
Cannot patch the script from the cron run (only memory/skill tools are
allowed during skill-update phase). Apply the patch manually in
`scripts/humanize_audit.py` if a future session has file-write access.

## How to use the two scores together

The SKILL.md `Step 3 — Humanize` section already says "use both scripts
before publishing." Here's the reconciliation rule:

1. `humanize_score.py` is the **publish-or-not** check. Threshold is 60.
   If it returns >= 60, the article is shippable. Period.
2. `humanize_audit.py` is the **pattern-by-pattern audit**. The 0-100
   score is informational; the per-pattern hit list is the actionable
   output. Read the hit list, classify each hit as real or false-positive
   (use the catalog above and the SKILL.md's per-pattern guidance), and
   patch only the real hits.
3. When the two scores disagree by 20+ points, the audit is the one
   being noisy. Find the noisiest pattern (usually `features`), apply
   the override test, and trust the site-aware score.

## Other false-positive patterns to watch for

These have not been verified by a specific failed run yet, but the
underlying logic in `humanize_audit.py` suggests the same risk:

- `\boffers\b` — "the site offers a free reading" is a normal verb use,
  not copula avoidance. Real copula-avoidance is "boasts/offers a
  vibrant..." in promotional contexts.
- `\brepresents\b` — "the chart represents the household's elemental
  balance" is a normal verb use. Real copula-avoidance is "represents a
  shift / represents a testament."
- `\bmarks\b` — "the 2026 wealth point marks the south sector" is
  positional language, not copula avoidance. Real copula-avoidance is
  "marks a pivotal moment" / "marks a shift."

If any of these fire in the audit on a clean article, apply the same
noun-vs-verb / literal-vs-ceremony test before patching.

## Action items for future skill maintainers

- Patch `scripts/humanize_audit.py` COPULA_AVOID list to drop
  `r"\bfeatures\b"`. The fix is one line, but it requires file-write
  access (the cron run's skill-update phase only allows memory + skill
  management tools).
- Consider weighting the audit score by pattern (a real "boasts" hit is
  worth more than a "features" hit). The current flat
  `100 - 5 * hits` formula amplifies false positives.
- Add a `--strict` flag to the audit script that excludes the
  `features` / `offers` / `represents` / `marks` noun-sense matches
  from the score, but still reports them in the hit list. Future agents
  can opt in to the strict mode for new articles.
