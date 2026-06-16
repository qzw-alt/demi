# Humanize Score Script: When to Trust, When to Override

The `scripts/humanize_score.py` script has hardcoded per-site em-dash caps that lag the verified site baselines documented in the SKILL.md "Site-specific humanizer baselines" table.

## Body extraction bug — fixed 2026-06-06 (verified against `fate-2026-06-06.html`)

**Symptom:** Script reports "Word count: 193" and "Em dashes: 0" for a 2,200+ word article that uses `&mdash;` entities throughout. The 193-word figure is the *first* `<article>` block only; the 0 em-dashes is because the script was counting literal `\u2014` (—) characters, not the HTML entity `&mdash;`.

**Root cause:** Two bugs in `extract_article_body()` (pre-2026-06-06 version):

1. `r"<article[^>]*>(.*?)</article>"` is non-greedy. Articles on this site use **multiple** `<article>` blocks (one per H2 section, typical layout: 5-7 blocks per page). The regex returned only the *first* one, so the script was scoring the intro paragraph.
2. The text was never HTML-entity-decoded. Sites that use `&mdash;`, `&hellip;`, `&rsquo;` in their HTML (this site does) get 0 em-dash counts every time, triggering the false "em-dashes too few" penalty.

**Fix (applied 2026-06-06):** `extract_article_body()` now:
- Uses `re.findall` instead of `re.search` to capture all `<article>` blocks, then joins them.
- Strips `<style>`, `<script>`, and HTML comments before stripping tags.
- Decodes common HTML entities (`&mdash;`, `&ndash;`, `&hellip;`, `&amp;`, `&quot;`, `&apos;`, `&nbsp;`, smart quotes) and numeric entities (`&#8212;`, `&#x2014;`).

**Before/after on `fate-2026-06-06.html`:**
- Old: words=193, em_dashes=0 (false "em-dashes too few" penalty, false "low word count" penalty, false "missing first-person voice" penalty)
- New: words≈2200, em_dashes=16 (correct; matches the 16 `&mdash;` entities in the source)

**If you see "em-dashes too few: 0" or "Word count: <300" on an article that is clearly much longer:** the patch may have been reverted, or the article uses an unusual layout (e.g., a single giant `<section>` with no `<article>` tags — in which case the script falls back to full HTML, which is fine).

## Raw vs per-1200-words em-dash counting (verified 2026-06-08)

The patched script's `em_dash_high=23` is a **raw count** cap, not a per-1200-words cap. For a chinahospitalsguide daily-news-feature article at 4,400 words, baseline density of 17-23/1200 = 62-85 raw em-dashes — every chinahospitalsguide article over ~2,800 words will exceed 23 raw em-dashes even at the recommended baseline density. The script will therefore flag a 14/100 score on every 4,000-word article regardless of how good the humanize pass was.

**How to read the score on a 4,000+ word article:**
- The em-dash note is meaningless — ignore it.
- Check the actual density with `scripts/em_dash_check.py`; if it's in the 15-23 band, the article is shippable.
- The remaining script notes that matter: real banned vocab in headings (not body prose), -ing tails outside legitimate clinical phrases, and "Despite" overuse. Each one of these is independently actionable; the em-dash note is not.

**Why the raw-cap design is broken for chinahospitalsguide:** the 23 raw cap was set when articles were 1,200-1,800 words (the SEO skill's nominal target). After the 2026-05-28 baseline update, chinahospitalsguide's actual article length is 3,000-4,400 words. The cap needs to scale with word count: a per-1200-words cap of 23 × (4000/1200) ≈ 77 raw would be correct. Patch the script to compute the cap from word count, or just hardcode `em_dash_high=80` for chinahospitalsguide as a stopgap (verified 2026-06-08 as the right value for a 4,400-word article at upper-baseline density).

## Banned-vocab checks apply to H2 headings too (verified 2026-06-06)

The script's `extract_article_body()` strips HTML tags but keeps the text content of `<h2>`, `<h3>`, etc. — meaning every banned-vocab hit in a heading fires the same penalty as a body hit. On 2026-06-06 the article "What CAR-T Therapy Actually Is" and "What the International Patient Path Actually Looks Like" each counted "actually" as a banned-vocab hit, even though the phrase "what X actually is/looks like" is a standard non-AI-tell English construction. Lesson: when choosing H2 / H3 wording, mentally scan against the banned list (`actually`, `pivotal`, `leverage`, `navigate`, `crucial`, `delve`, `tapestry`, `underscore`, `vibrant`, `showcase`, `intricate`, `interplay`, `garner`, `enduring`, `enhance`, `fostering`). Cheap rewrites that keep the same meaning: "What X Is" / "How X Works" / "The X Process" / "X in Practice" / "X at a Glance".

## Known mismatch (status update 2026-06-08)

| Site | Script `em_dash_high` (raw) | Verified baseline (SKILL.md) | Status |
|------|-----------------------------|------------------------------|--------|
| chinahospitalsguide | **23** (raw, scaled by word count in scoring) | 17-23 per 1200 words | **Patched 2026-06-08** — script now scales the cap with word count (`em_cap = max(23, int(23 * wc / 1200))`), so a 4,400-word article at baseline density has a cap of ~84, not 23. False negative for daily-news-feature articles is resolved. |
| oriental-destiny | 25 (raw) | 10-18 per 1200 words | Tolerant enough; no false flag. Same scaling applied for consistency. |

## How to interpret the script's "em-dashes too many" warning

1. Run the check: `python3 scripts/em_dash_check.py news/YYYY-MM-DD.html`
2. Look at the reported density line: "Em-dashes: N (X per 1200 words)"
3. If X < 17 for chinahospitalsguide → **false negative**. The script's config is wrong, the article is fine. Do NOT strip em-dashes to "fix" the score.
4. If X >= 17 → real warning, follow the humanizer skill guidance to reduce.

## When to fix the script (preferred over override)

The script is in `/home/ubuntu/.hermes/skills/creative/programmatic-seo/scripts/humanize_score.py`. The chinahospitalsguide config block sets `em_dash_high=23`; the per-1200-words baseline is 17-23. The actual penalty calculation (verified 2026-06-08) is:

```python
# scripts/humanize_score.py, in the score() function (around line 116)
em = text.count("\u2014")
em_cap = max(cfg["em_dash_high"], int(cfg["em_dash_high"] * wc / 1200))
if em > em_cap:
    over = em - em_cap
    score_val -= 2 * over
    notes.append(f"em-dashes too many: {em} (cap={em_cap} for {wc} words)")
```

This is the permanent fix for the raw-vs-density mismatch — the cap now scales with word count, so a 4,400-word article at baseline density has a cap of ~84, not 23. Apply once and the score will align with the documented baseline.

## 2026-06-05 case in point

Article: `news/2026-06-05-china-ai-dental-tourism-russian-patients-heihe.html`
- Script score: 52/100 (flagged "em-dashes too many: 31 (high=12)")
- Actual density: 10.2 em-dashes per 1200 words
- Verdict: false negative. Article is below the 17-23 baseline. Published as-is with a pending-article note flagging the script's outdated cap for the next run to patch.
