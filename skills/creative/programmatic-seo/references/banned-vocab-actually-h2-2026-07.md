# "Actually" in headings — score-kill quantification (verified across 4 runs, 2026-06-22 → 2026-07-19)

## The rule

When running the humanize score, ALWAYS grep for `actually` in heading tags (H1/H2/H3) separately from body prose. A single `actually` in a heading is worth **8 score points (±1)**, confirmed across 4 independent runs.

## Pre-humanize grep (mandatory)

```bash
grep -nE '<h[1-3][^>]*>[^<]*actually[^<]*</h[1-3]>' news/FILE.html
```

Zero matches = safe to score. 1+ matches = patch the headings before scoring.

## Verified reproductions

| Date | Site | H2 hits | Score swing | Notes |
|---|---|---|---|---|
| 2026-06-22 | oriental-destiny | 1 ("What 'sitting and facing' actually means") | 95 → 87 → 95 (8 pts) | First quantification, "Sitting and Facing" article |
| 2026-06-24 | chinahospitalsguide | 1 ("What 6MW5311 actually does") | 80+ → 67 → 75 (8 pts) | Mabwell 6MW5311 IND clearance article |
| 2026-06-25 | chinahospitalsguide | 2 ("What UX-DA003 actually is" + "What UniXell actually announced") | 80+ → 56 → 72 (16 pts) | Unixell UX-DA003 article; 2 H2 hits compound to 16 pts |
| 2026-07-19 | chinahospitalsguide | 1 ("What the clinical evidence actually shows") | 95 → 79 → 87 (8 pts) | Goldman→TCM Template A article; confirms 8 pts single H2 |

## Replacement options for `actually` in headings

- `What the clinical evidence actually shows` → `What the clinical evidence shows`
- `What 6MW5311 actually does` → `What 6MW5311 does` or `How 6MW5311 works`
- `What UX-DA003 actually is` → `What UX-DA003 is` or `The UX-DA003 profile`
- `What UniXell actually announced` → `What UniXell announced` or `The UniXell announcement`
- `What 'sitting and facing' actually means` → `What "sitting and facing" means, in plain language`

## Body-prose tolerance (unchanged from 2026-06-08)

1-2 `actually` hits per 4,000 words in body prose is tolerated (they appear in normal constructions like "would actually execute" or "had not actually been done" where they're just emphasis). Score impact in body is ~1 point per hit, not 8. The 8-point H2 penalty is the headline.

## Why the asymmetry

Human readers land on headings first. A single "actually" in an H2 reads as "LLM wrote this" because it's exactly the kind of emphasis word a language model would inject. The script's regex doesn't weight headings more heavily even though human readers do — so the rule update is "patch every H2 `actually` before scoring, regardless of script flags."

## Cost of getting it wrong

A 8-point score swing on a clean article drops it from the 87-95 band (publishable) to the 67-79 band (still above 60 threshold but visibly weaker). Patching 1 line fixes it. Cost of a missed patch: 1 score band lower than necessary, which matters for the score-band recovery pattern when the first-pass article is already in the 60-80 range.
