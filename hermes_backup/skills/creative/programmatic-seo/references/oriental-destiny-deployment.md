# oriental-destiny.com — Deployment Notes

Session-specific operational knowledge for the daily SEO cron targeting
oriental-destiny.com. Updated 2026-06-05.

## Branch facts (verified)

- **Deployed branch: `main`** (not `master` as the cron prompt says)
- Verified via `git ls-remote --heads origin` — `refs/heads/main` is the live HEAD
- `master` exists in origin but is not wired to GitHub Pages
- The cron prompt will keep saying `master` for the foreseeable future; do not follow it blindly. Trust `git remote -v` output.

## Repo state quirks

- `local main` and `origin/main` regularly diverge. Local main tends to have
  one extra "article: YYYY-MM-DD" commit that a previous cron run committed
  but never pushed. So `main` is 1 commit ahead of `origin/main` going into
  every new run.
- The cron pattern is: create a per-day branch (`article-0602`, etc.),
  commit, push that branch to origin, then merge into `local main`, then
  push `local main` to `origin/main`. Sometimes the second push is skipped
  (the cron probably doesn't always do it). That's why the divergence
  accumulates.
- **Don't `git reset --hard origin/main`** — this would drop the prior day's
  local commit and the `fate-YYYY-MM-DD.html` file it added. Use the
  merge + conflict-resolve path described in SKILL.md Step 6.

## Sitemap ordering convention

The cron pattern is to push each new `<url>` entry to the TOP of
`sitemap.xml`, not append it. So after several days, the entries look like:

```
fate-2026-06-02.html  ← newest, top
fate-2026-06-01.html
fate-2026-05-31.html
... other static pages ...
policies.html         ← oldest, bottom
```

When resolving sitemap merge conflicts, **keep HEAD's ordering** (local
chronological reordering) and discard the article-XXXX branch's
"appended at bottom near policies.html" placement.

### Sitemap conflict patch — typo pitfall (verified 2026-06-05)

When you resolve the sitemap conflict by hand-editing the conflict
markers, the `old_string` and `new_string` you pass to `patch` both
contain a full `<loc>` line. The conflict always looks like:

```
<<<<<<< HEAD
    <loc>https://oriental-destiny.com/fate-2026-06-04.html</loc>
=======
    <loc>https://oriental-destiny.com/fate-2026-06-05.html</loc>
>>>>>>> article-0605
```

To keep both at the top, your replacement string contains BOTH `<loc>`
lines. The day segment (`-06-04` vs `-06-05`) is one character apart
and the only meaningful difference — a single-character typo
(`2026-04` instead of `2026-06-04`) silently produces a broken URL in
the live sitemap that a future Googlebot crawl will hit.

**Verified 2026-06-05**: a single edit typo (`-2026-04` instead of
`-2026-06-04`) had to be caught and re-patched in a follow-up call.
Cost: 2 extra tool calls. Prevention:

1. After writing the conflict resolution, `git diff sitemap.xml` and
   eyeball every `<loc>` line for the correct `YYYY-MM-DD` format.
2. Verify with the humanize-score harness (it parses sitemap.xml as
   XML and reports the first 3 entries):
   ```bash
   python3 scripts/humanize_score.py fate-YYYY-MM-DD.html \
     --site oriental-destiny --sitemap sitemap.xml
   ```
   Confirm the first 3 entries are the three most recent dates in
   order.

## Article template (copy-paste header)

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="[150-160 char keyword-rich description]">
    <link rel="canonical" href="https://oriental-destiny.com/fate-YYYY-MM-DD.html">
    <meta property="og:title" content="[Article Title] | Oriental Destiny">
    <meta property="og:description" content="[120-150 char OG description]">
    <meta property="og:type" content="article">
    <title>[Article Title] | Oriental Destiny</title>
    <link rel="icon" href="favicon.svg" type="image/svg+xml">
    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "Article",
      "headline": "[Article Title]",
      "description": "[Article deck]",
      "author": { "@type": "Organization", "name": "Oriental Destiny" },
      "publisher": {
        "@type": "Organization",
        "name": "Oriental Destiny",
        "url": "https://oriental-destiny.com/"
      },
      "datePublished": "YYYY-MM-DD"
    }
    </script>
    <style>/* see site-configs.md for CSS variables */</style>
</head>
```

The site uses an ink/cinnabar/gold/pine color palette (warm East-Asian
serif aesthetic) and a single-column ~720px max-width layout. See
`references/site-configs.md` for the full CSS variable block.

## Banned vocab (humanizer) — oriental-destiny specifically

Even though the humanizer skill flags these generally, they're particularly
likely to slip into oriental-destiny articles because the topic (feng shui,
BaZi, destiny) invites them:

- `leverage` / `leveraging` / `leverages`
- `actually`
- `crucial` / `pivotal`
- `delve` / `delving`
- `tapestry` (figurative)
- `landscape` (abstract noun — "the feng shui landscape")
- `underscore` (verb)
- `vibrant` (figurative — "vibrant energy")
- `showcase` (verb)
- `intricate` / `intricacies`
- `interplay`
- `navigate` (the "navigate the complexities of..." trope)

Voice is first-person, conversational, willing to use "I think" and
"here is what I usually suggest." Articles should sound like a working
practitioner talking to a friend, not a press release.

**Em-dash baseline for this site**

10–18 em dashes per ~1200 words is the typical range here. The humanizer skill's
default "max 4" is too strict. Focus the audit on banned vocab and
-ing analysis tails, not on em-dash count.

**Zero-em-dash is also viable (verified 2026-06-14):** the `fate-2026-06-14.html`
Bedroom Fire Month article shipped at 2,672 words with **0 em dashes** and a
humanize score of ~88/100 (6 first-person uses, sentence variance 1–58 words,
11 contractions, no banned vocab). The 10–18 baseline is a *typical* range, not
a floor — articles can score above the >60 threshold with zero em dashes if the
voice is otherwise strong. Don't add em dashes artificially to hit the baseline;
only add them when they serve a real aside (one example: a Day Master
abbreviation parenthetical, an English clarification of a Chinese term).

## Recent published articles (for tone reference)

- `fate-2026-05-31.html` — earlier article
- `fate-2026-06-01.html` — 8 Feng Shui Bedroom Rules (1,285 words, 18 em dashes)
- `fate-2026-06-02.html` — Summer Solstice Fire Element (1,240 words, 10 em dashes)
- `fate-2026-06-03.html` — Feng Shui for the Bathroom (~1,200 words)
- `fate-2026-06-04.html` — Summer and the Fire Element in BaZi (~1,275 words, score 100/100)
- `fate-2026-06-05.html` — Kitchen Feng Shui (~1,275 words, 9 em dashes, score 100/100)
- `fate-2026-06-06.html` — Summer and the Fire Element in Your BaZi Chart (~1,300 words, score 100/100) — best voice reference for Day Master articles
- `fate-2026-06-07.html` — Ding Day Master: The Yin Fire Candle (1,700 words, 21 em dashes = 14.8/1200, score 100/100) — cross-links `ding-day-master.html` and `bing-day-master.html`
- `fate-2026-06-08.html` — Wu Day Master: The Yang Earth Mountain (1,973 words, 18 em dashes = 10.9/1200, score 87/100) — best voice reference for **bridging a Day Master piece with prior week's summer/fire content**; cross-links `wu-day-master.html` and `earth-element-in-bazi.html` in footer; written after a sibling-cron had already pushed 06-06 and 06-07 to origin/main (required fetch+merge+sitemap-conflict-resolve)
- `fate-2026-06-09.html` — best CSS template (verbatim — see Pitfall #2 in `cron-run-pitfalls.md`)
- `fate-2026-06-12.html` — Xia Zhi 2026: Summer Solstice Feng Shui (3,492 words, score 100/100) — best voice reference for **calendar-anchored solar-term pieces**; 6 FAQ items, 5 content blocks, explicit "what to avoid" section, all BaZi sub-types covered
- `fate-2026-06-13.html` — Ming Tang in Summer: Setting Up the Entryway (2,681 words, score 95/100, em-dashes ~11.6/1200) — best voice reference for **virgin-topic discovery** (no prior entryway reference page); opens with classical concept definition (明堂), bridges to seasonal context (Fire month), 5 practical moves + 4 things to avoid + per-Day-Master read of the entryway; cross-links to `fire-element-in-bazi.html` and `summer-and-the-fire-element-in-bazi.html`
- `fate-2026-06-14.html` — Bedroom Feng Shui for the Fire Month (2,672 words, score ~88/100, **0 em dashes**) — best voice reference for **the highest-traffic competitor keyword ("bedroom feng shui")** paired with the Fire-month framing; 5 moves + 5 things to avoid + per-Day-Master read of the bedroom; cross-links `fire-element-in-bazi.html` + `summer-and-the-fire-element-in-bazi.html` + `five-elements-explained.html`; proves zero-em-dash is viable if voice is otherwise strong
- `fate-2026-06-15.html` — Home Office Feng Shui for the Fire Month (3,140 words, score 95/100, 29 em dashes = 11.1/1200) — best voice reference for **the room-specific + Fire-month + 5-moves + 5-things-to-avoid + per-Day-Master structure** applied to a room with no prior reference page; topic fit was 6 days pre-Xia Zhi (June 21) in the "mid-summer ramp" window between Xia Zhi prep and actual solstice; filled the room-specific gap left by 06-05 Kitchen and 06-14 Bedroom; cross-links to `fire-element-in-bazi.html` + `summer-and-the-fire-element-in-bazi.html` + `five-elements-explained.html` + `li-chun-bazi-beginning-of-spring.html`; 6 FAQ items; one banned-vocab patch ("actually" → "keep refilling through the day") brought the score from 87 → 95 in 1 tool call; full run completed in 9 tool calls with no sibling-cron divergence (see SKILL.md "EVEN cleaner run" reference); **the patch tool emitted a sibling-subagent warning on the sitemap.xml edit** — the warning was a false positive (sibling made an equivalent no-op change in the same region) and the patch was verified clean by re-reading the file before the commit. See SKILL.md "Patch tool pitfall: sibling-subagent write warning" pitfall for the recovery recipe.

**Voice reference recipe (verified 2026-06-07):** before writing, `read_file` the two most recent `fate-YYYY-MM-DD.html` articles in full (body section, not just head/CSS). The site voice is first-person, uses `&mdash;` HTML entities (rendered as em dashes), pulls cross-links to existing reference pages (`<day-master>.html`, `<element>-in-bazi.html`, `<topic>-bazi.html`), and ends with a 5-question FAQ + a cinnabar CTA to `instant_reading.html`. Match the structure exactly: hero → 5–6 content blocks → CTA → FAQ → footer with policy links.

## Verification command (after push)

```bash
curl -s -o /dev/null -w "%{http_code}" https://oriental-destiny.com/fate-YYYY-MM-DD.html
# Expect 200 after 2-3 min
```

If 404 persists past 5 minutes, check:
1. `git log origin/main -1` — is the commit actually on origin?
2. `https://github.com/qzw-alt/oriental-destiny/deployments` — is the
   GitHub Pages build running or did it fail?
