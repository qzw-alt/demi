# Em-Dash Insertion Technique: Density Below Baseline (verified 2026-07-26)

When a fresh draft comes in with **em-dash density below the site baseline** (oriental-destiny <10/1200, chinahospitalsguide <17/1200), the inverse of the documented "don't strip below baseline" rule applies: **ADD em-dashes by surgical patch insertion**, not by prose restructuring.

The technique is mechanical and repeatable. Each em-dash should add a clinical parenthetical (drug-name expansion, abbreviation definition, study-name parenthetical, comparison parenthetical, or *position/aside clarification*), not break the sentence.

## Why this happens

A clean first draft written in a conversational register (oriental-destiny) tends to come in at 5-9 em-dashes/1200 instead of the 10-18 baseline. The site-aware script flags "low em-dash density" implicitly through the score (or "high word count" when length overwhelms the density formula), not directly. Without active insertion, the article ships below baseline and reads as well-edited prose but loses the deliberate "filler comma → clinical aside" rhythm the rest of the site carries.

A clinical-research article (chinahospitalsguide) has the opposite problem: em-dashes come in at 20-30+ raw even at baseline density, and the script's `em_dash_high=23` raw cap (vs. the 17-23/1200 baseline density) means long articles always exceed the cap. Different pitfall, same fix: surgical insertion is the answer for oriental-destiny, surgical reduction (or accepting the false negative) is the answer for chinahospitalsguide.

## The four repeatable insertion patterns

Each pattern is a 1-line `patch` that converts one prose seam into a clinical aside. Each raises raw em-dash count by 1 and word count by 5-15.

### Pattern 1: Standalone opening sentence → em-dash fronted clarification

**Before:**
```html
<p>Stand outside the closed study door. Does the door open against a wall or into clear floor?</p>
```

**After:**
```html
<p>Stand outside the closed study door — the position the room sees first from the rest of the house. Does the door open against a wall or into clear floor?</p>
```

Why it works: the em-dash front-loads a clarifying aside that the prose would otherwise need a separate sentence for. Reader parses "Stand outside the closed study door" as a complete command, then takes in "the position the room sees first" as a parenthetical. Adds one em-dash, no extra sentence.

**Where to find candidates in any article:**
```bash
grep -nE '^\s*<p>[A-Z][a-z]+( [a-z]+){1,8}\. [A-Z]' fate-YYYY-MM-DD.html
```
Two sentences in a row starting with capital letters in the same paragraph = perfect candidate. The first ends in a noun, the second opens a related thought.

### Pattern 2: "and" join with two separately true facts → em-dash parenthetical

**Before:**
```html
<p>A chair pointed at a "wealth" compass sector but floating with no behind-wall will not read as wealth to the reader after the third evening.</p>
```

**After:**
```html
<p>Do not let an auspicious direction force a poor physical position — a chair pointed at a "wealth" compass sector but floating with no behind-wall will not read as wealth to the reader after the third evening.</p>
```

Why it works: turns a single sentence with a "but" into a sentence with a claim + em-dash aside + contrast. The aside is *evidence for* the claim, not just two facts glued together. Reader still parses it the same way.

### Pattern 3: Two-clause topic sentence → em-dash aside

**Before:**
```html
<p>Avoid placing the chair directly facing the window. A reader who stares out the window is not reading; a reader with the window at an oblique angle can choose to look up and recover.</p>
```

**After:**
```html
<p>Avoid placing the chair directly facing the window — a reader who stares out the window is not reading; a reader with the window at an oblique angle can choose to look up and recover.</p>
```

Why it works: collapses a "statement. Explanation." pairing into a "statement — explanation" structure. The aside naturally elaborates the "avoid" instruction with the "why." Reader absorbs both as one breath.

### Pattern 4: List-item turn marker → em-dash aside

**Before:**
```html
<p>Morning one: close the door fully, install the hook-and-eye if needed.</p>
```

**After:**
```html
<p>Morning one: close the door fully, install the hook-and-eye if needed — the room's first habit.</p>
```

Why it works: a tagged list-item ("Morning one:", "Morning two:") is a natural anchor for a closing em-dash aside. The aside names the *why* of the item in 2-4 words. Adds density without growing the list. Use on every 3rd-4th list item, not all of them — otherwise the rhythm turns metronomic.

## How to verify the technique worked

After ~10 patches, run:
```bash
python3 /home/ubuntu/.hermes/skills/creative/programmatic-seo/scripts/humanize_score.py fate-YYYY-MM-DD.html --site oriental-destiny --sitemap sitemap.xml
```

Pre vs post (verified 2026-07-26, study feng shui article):

| Metric | Before patches | After 11 patches |
|---|---|---|
| Words | 2,314 | 2,391 |
| Raw em-dashes | 7 | 20 |
| Density / 1200 words | 2.8 | 7.9 |
| Banned vocab hits | 1 (`navigate`) | 0 |
| Humanize score | 72 | 80 |

The density is still slightly below baseline (7.9 vs. 10-18), and the script flags "high word count" not "low density" — that's the correct behavior. The score lifted 8 points from em-dash rhythm alone; further em-dash insertion past 20 raw would not raise the score because the script's word-count penalty and "high word count" note take over at ~2,400 words.

**Target density:** 10-18/1200 for oriental-destiny (or absolute 20-35 raw for 2,300-3,200 word articles), 17-23/1200 for chinahospitalsguide (or absolute 30-50 raw for 2,500-3,800 word articles).

## Anti-patterns to avoid

- **Don't insert em-dashes that break the parse** ("The reader — who came in tired — sat down" — the parenthetical is too long and the sentence fragments unnaturally)
- **Don't insert two em-dashes back-to-back in one sentence** (renders as muddied prose, not clinical)
- **Don't add an em-dash after every "and" or comma** — the rhythm turns didactic and the humanize script flags the article as "rule-of-three overuse"
- **Don't insert em-dashes in FAQ answers** (FAQ reads cleaner as straight prose; em-dashes in answers feel like a glossary bullet)
- **Don't insert em-dashes in headers** (visually renders as `—` running text in the H-tag, breaks the layout)

## Pre-flight vs. mid-flight detection

**Pre-flight (before writing):** run `em_dash_count_check.py` (or inline decode, see SKILL.md) on the prior day's article to confirm where the site is sitting. If 07-25 sat at 7 em-dashes/2,400 words (2.8/1200), it's a low-density day — write with extra em-dashes from the start.

**Mid-flight (after first pass):** the humanize script does not flag density direction directly. Use:

```bash
python3 -c "
import re
with open('fate-YYYY-MM-DD.html') as f: c = f.read()
c = c.replace('&mdash;', '\u2014')
t = re.sub(r'<[^>]+>',' ', c)
words = len(t.split())
em = t.count('\u2014')
print(f'Em-dashes: {em} ({em*1200/words:.1f} per 1200 words)')
"
```

If density < 8/1200 (oriental-destiny) or < 14/1200 (chinahospitalsguide), pre-emptively apply 8-12 insertions from the four patterns above before pushing to `git commit`.

## When this technique doesn't apply

- Article under 1,500 words: density isn't relevant, script doesn't track it, ship as-is
- Article in a different voice (technical-doc, medical-research report): the em-dash density baseline differs; check the site's most recent 2-3 articles, don't apply oriental-destiny baseline to a different register
- Article has 50+ em-dashes already (chinahospitalsguide long-form): you're in the "strip and accept false negative" regime, not the "add" regime

## Related references

- SKILL.md Site-Specific Humanizer Baselines table — for the per-site density targets
- SKILL.md `Em-dash density too LOW` pitfall (06-07 verified) — the inverse rule this technique implements
- `references/step5-site-divergence-2026-07.md` — for site-specific Step 5 behavior this technique doesn't interact with but coexists with
- `references/teed-up-next-article-2026-07.md` — companion technique for picking which article to apply this to
