# oriental-destiny.com Keyword Template (HARD RULE)

The oriental-destiny.com cron job prompt enforces a strict keyword template on every published article. This file captures the rule so future agents encode it directly instead of relying on the cron prompt text.

## The template

Every article's **`<title>`**, **`<h1>`**, **`og:title`**, and **schema.org `headline`** must follow exactly:

```
[Primary Keyword]: [Long-tail Hook] | Oriental Destiny
```

## Components

- **Primary Keyword** = `"X Feng Shui"` or `"X BaZi"` or `"X Destiny"` form.
  - The head noun (`Feng Shui` / `BaZi` / `Destiny`) MUST be present.
  - It cannot be reduced to a time adverb ("Li Qiu Eve") or stripped down ("Garden Tips").
- **X** = a concrete object or anchor.
  - Valid: `Front Garden`, `Back Garden`, `Balcony`, `Rooftop`, `Li Qiu`, `Door`, `Bedroom`, `Kitchen`, `Stairway`, `Mailbox`, etc.
  - Invalid as X: pure time adverbs like "Li Qiu Eve", "August", "July". Time-specific phrasing goes in the **Long-tail Hook**, not in the **X** position.
- **Long-tail Hook** = scene-anchored long-tail.
  - Valid: `What to Do on the Eve Before the Fire-to-Earth Handoff`, `Reading the Vertical Line Between Floors`, `What to Do in the Fire-to-Earth Transition`.

The `<meta name="description">` MUST also lead with the Primary Keyword in its **first sentence** (not in the second or third clause).

## Valid / invalid examples

| Title | Verdict | Why |
|---|---|---|
| `Front Garden Feng Shui for July: What to Do in the Fire-to-Earth Transition \| Oriental Destiny` | ✅ | `Front Garden Feng Shui` is Primary Keyword. Hook is scene-anchored. |
| `Stairway Feng Shui: Reading the Vertical Line Between Floors \| Oriental Destiny` | ✅ | `Stairway Feng Shui` is Primary Keyword. Hook is scene-anchored. |
| `Li Qiu Feng Shui: What to Do on the Eve Before the Fire-to-Earth Handoff \| Oriental Destiny` | ✅ | `Li Qiu Feng Shui` is Primary Keyword (Note: `Li Qiu` IS a concrete anchor name). |
| `Li Qiu Eve: The Night Before the Fire-to-Earth Handoff \| Oriental Destiny` | ❌ | Head noun `Feng Shui` missing. |
| `July Outdoor Reading` | ❌ | Head noun missing AND no concrete object X. |

## Four-location grep self-check (run BEFORE Step 3 humanize)

```bash
grep -nE "(Stairway Feng Shui|Front Garden Feng Shui|<title>|<h1>|og:title|headline)" fate-YYYY-MM-DD.html | head -20
```

Verify the Primary Keyword (with `Feng Shui` / `BaZi` / `Destiny`) appears in:
1. `<title>` line
2. `<h1>` line (inside the `<section class="hero">`)
3. `<meta property="og:title" ...>` line
4. `"headline": "..."` inside the JSON-LD `<script type="application/ld+json">` block

A title without the template fails the SEO brief even if the humanize score is 95/100. Always patch the title BEFORE running the humanize score, because patching the title later will not affect the score anyway and the SEO template check is independent of the humanize check.

## Relationship to the cron prompt

The cron job prompt for oriental-destiny.com enforces this rule in the prompt body. If the cron prompt is ever rewritten or replaced, the rule still must apply — it's an SEO constraint, not a prompt artifact. Verifying the rule lives in the skill (not just in the prompt) means future agents encode it from the start of Step 2, not from the start of the cron run.

## Verified case (2026-07-17)

The `Stairway Feng Shui: Reading the Vertical Line Between Floors` article shipped with the template applied in all four locations, scored 95/100 on humanize, and reached HTTP 200 on GitHub Pages within the standard 2-3 minute CDN propagation window. Self-check ran in 1 grep call, no patches needed.

## When this rule does NOT apply

This rule is oriental-destiny.com-specific. chinahospitalsguide.com uses English medical-tourism / clinical-research headlines (asset names, regulatory milestones, etc.) that do not have a template constraint. If a future site is added to this skill, the keyword template for that site must be documented in its own reference file under its own cron-run conventions, NOT inherited from this file.
