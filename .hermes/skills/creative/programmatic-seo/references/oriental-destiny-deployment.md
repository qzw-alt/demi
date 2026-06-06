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

## Em-dash baseline for this site

10–18 em dashes per ~1200 words is normal here. The humanizer skill's
default "max 4" is too strict. Focus the audit on banned vocab and
-ing analysis tails, not on em-dash count.

## Recent published articles (for tone reference)

- `fate-2026-05-31.html` — earlier article
- `fate-2026-06-01.html` — 8 Feng Shui Bedroom Rules (1,285 words, 18 em dashes)
- `fate-2026-06-02.html` — Summer Solstice Fire Element (1,240 words, 10 em dashes)
- `fate-2026-06-03.html` — Feng Shui for the Bathroom (~1,200 words)
- `fate-2026-06-04.html` — Summer and the Fire Element in BaZi (~1,275 words, score 100/100)
- `fate-2026-06-05.html` — Kitchen Feng Shui (~1,275 words, 9 em dashes, score 100/100)

## Verification command (after push)

```bash
curl -s -o /dev/null -w "%{http_code}" https://oriental-destiny.com/fate-YYYY-MM-DD.html
# Expect 200 after 2-3 min
```

If 404 persists past 5 minutes, check:
1. `git log origin/main -1` — is the commit actually on origin?
2. `https://github.com/qzw-alt/oriental-destiny/deployments` — is the
   GitHub Pages build running or did it fail?
