# Em-dash baseline drift — verified 2026-07-28

The `| Site | Em dashes per ~1200 words (verified) |` table in SKILL.md is now outdated for **oriental-destiny.com**. The 10–18 figure was measured in May/June 2026 articles when the voice ran with deliberate em-dash asides. The current voice (July 2026) runs sparser.

## Verified densities (July 2026 cron runs)

| Article | Words | Em-dashes | Per 1200 |
|---|---|---|---|
| fate-2026-07-21.html | 4,313 | 13 | 3.6 |
| fate-2026-07-22.html | 6,551 | 9 | 1.6 |
| fate-2026-07-23.html | 6,474 | 25 | 4.6 |
| fate-2026-07-24.html | 6,349 | 28 | 5.3 |
| fate-2026-07-25.html | 2,711 | 0 | 0.0 |
| fate-2026-07-26.html | 3,051 | 20 | 7.9 |
| fate-2026-07-27.html | 4,244 | 5 | 1.4 |
| fate-2026-07-28.html | 4,290 | 1 | 0.3 |

**July 2026 range: 0–5 per 1200 for the median article, with 07-26 the outlier at 7.9.** The 10–18 figure is from May/June and is no longer current.

## What this means for the next cron run

1. **Do NOT auto-strip em-dashes below 5/1200 to "fix" a low score.** The script's "low=4" line is a diagnostic note, not a score penalty. The 07-28 article shipped at 89/100 with 1 em-dash (0.3/1200) — the score was driven by clean voice + no banned-vocab + good sentence-variance, not by em-dash count.

2. **Do NOT add em-dashes to chase the 10–18 figure.** Em-dashes need to be load-bearing (a clinical aside, a parenthetical definition, a comparison) — padding them with empty dashes will burn the article's voice and re-introduce the AI-em-dash-overuse pattern the humanizer skill warns against.

3. **The script's "em-dashes too few" note is informational.** Voices drift. The 2026-07 site voice is sparser because the thread-arc cluster (outdoor walk) used em-dashes specifically for parenthetical definitions, and the article-to-article cadence over the arc did not need many. A new arc (transition into a different topic) may pull the density back up naturally.

4. **The chinahospitalsguide.com baseline (17–23) is unchanged.** The two sites have different voices. Do not let the oriental-destiny baseline shift alter the chinahospitalsguide reading.

## How to detect drift in future runs

```bash
# Quick baseline check at the start of every cron run
for f in fate-$(date +%Y-%m-)-*.html fate-$(date +%Y-%m-)-*.html; do
  [ -f "$f" ] || continue
  em=$(grep -o '&mdash;' "$f" | wc -l)
  words=$(python3 -c "import re; c=open('$f').read(); t=re.sub(r'<[^>]+>',' ',c); print(len(t.split()))" 2>/dev/null)
  echo "$f: $em em-dashes, $words words, density $(python3 -c "print(round($em*1200/$words, 2))" 2>/dev/null)"
done
```

If 5+ consecutive articles show density outside the table's stated range, the table is stale and needs patching.

## Companion skill note

The `humanizer` skill's "Em Dash Overuse" pattern (#14) says "flag when an article has more than 4 em dashes per ~1000 words in a context that doesn't justify them." For oriental-destiny.com in July 2026, the context justifies them within ~0–5/1200, well under the 4/1000 ceiling. The humanizer rule still applies as a ceiling, not a floor.
