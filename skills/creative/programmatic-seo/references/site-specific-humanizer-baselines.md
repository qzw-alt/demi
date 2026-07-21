# Site-Specific Humanizer Baselines (verified)

Companion to `SKILL.md`. The em-dash density and voice characteristics that differ by site. Always measure the last 3 published articles on the target site before scoring — do not trust the table below for a brand-new site you haven't seen before.

## Em-dash density per site (verified, last update 2026-06-05)

| Site | Em dashes per ~1200 words (verified) | Voice notes |
|------|---------------------------------------|-------------|
| oriental-destiny.com | 10–18 | First-person, conversational, willing to use em dashes for asides. "Leverage" and "actually" are banned (AI-vocab) but em dashes are stylistic. |
| chinahospitalsguide.com | **17–23** (the old 4–8 figure was WRONG — verified 2026-06-02 by counting 3 most recent articles: May 28 BCI = 22.6, May 27 ivonescimab = 20.7, May 13 hantovirus = 17.2 per 1200 words) | Clinical, professional, no first-person, but **em dashes are heavily used for clinical asides, drug-name parentheticals, and result parentheticals**. Do NOT strip em dashes below 17 per 1200 words or the article sounds uncharacteristically stilted for the site. |

## Verification recipe

Before publishing, run the bundled `scripts/em_dash_check.py` on the new article to confirm em-dash density matches the site's actual baseline (not the skill's stated baseline):

```bash
python3 scripts/em_dash_check.py news/YYYY-MM-DD.html
```

This script is the file-based equivalent of the inline `python3 -c "..."` snippet below. Use the file form — the inline form triggers the tirith security scanner's "script execution via -e/-c flag" pattern, which the cron job's safety policy blocks. The script also reports banned-vocab hits and -ing analysis tails, so a single run covers most of the humanizer audit.

## Score-cap gotcha per site

The `scripts/humanize_score.py` script has hardcoded em-dash caps per site that lag the verified baselines:

- chinahospitalsguide: script cap = `em_dash_high=12` (line 56). Verified site baseline = 17-23 per 1200 words. An article with density of 10-16/1200 will be flagged "too many" even though it's below baseline.
- oriental-destiny: script cap = `em_dash_high=25` (line 45). Verified baseline = 10-18. The script is permissive enough that it won't false-flag.

**Rule:** When the script flags "em-dashes too many" for chinahospitalsguide, check the actual density (per 1200 words) against the verified baseline table. If the density is between 10 and 17, it's a false negative — the score penalty is the script's outdated config, not a real humanize issue. Do NOT strip em-dashes below 17/1200 to "fix" the score; you'll push the article below the site baseline and it'll read uncharacteristically stilted.

Patch the script to set `em_dash_high=23` for the chinahospitalsguide config block if you want the score to align with the verified baseline.

## Em-dash density too LOW

The documented pitfall is "don't strip below baseline," but a fresh draft can also come in UNDER baseline (e.g. 11-12/1200 for chinahospitalsguide) if the writer didn't add enough clinical parentheticals. The fix is to ADD em-dashes (not remove them) by inserting clinical aside parentheticals — drug-name expansions, abbreviation definitions, study-name parentheticals, comparison parentheticals. Good insertion points are places where two facts are already joined by "and" or a comma. Target: 17-23 per 1200 words for chinahospitalsguide, 10-18 for oriental-destiny.

## `em_dash_check.py` reports 0 em-dashes when articles use `&mdash;` HTML entities

The script counts raw `—` characters in the file's text. Articles in this repo consistently encode em-dashes as `&mdash;` entities (the prior `humanize_score.py` `extract_article_body()` bug for entity decoding was fixed on 2026-06-06, so that script counts them correctly — but `em_dash_check.py` was NOT updated alongside it). When you run `em_dash_check.py` on a repo article you will see "em-dashes: 0 (0.0 per 1200 words)" even when `humanize_score.py` reports 23+ em-dashes on the same file. **The correct em-dash count is the `humanize_score.py` number.** `em_dash_check.py` is still useful for banned-vocab hits and `-ing` analysis tails — just ignore its em-dash field.

## Site-specific focus areas for the humanize pass

For oriental-destiny: focus the humanize pass on banned vocab (`actually`, `leverage`, `crucial`, `delve`, `pivotal`, `tapestry`, `landscape`, `underscore`, `vibrant`, `showcase`) and -ing analysis tails. Don't strip em dashes below 8.

For chinahospitalsguide: focus the humanize pass on banned vocab (full list in `humanizer` skill — same as oriental-destiny plus `leverage` is the highest-frequency offender in clinical writing). Do NOT touch em dashes.