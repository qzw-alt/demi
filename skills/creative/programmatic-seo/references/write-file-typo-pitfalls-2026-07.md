# write_file / patch Typo Pitfalls (verified 2026-07-16)

Two typo patterns have shipped (or nearly shipped) on first `write_file` calls. Both are character-level slips that the human eye misses when copying a snippet from a prior article.

## 1. gtag URL typo (verified 2026-07-16, oriental-destiny.com)

**Symptom:** the Google Analytics snippet is written as `https://www.googletagmanaper.com/gtag/js?id=G-XXXX` instead of `https://www.googletagmanager.com/gtag/js?id=G-XXXX`.

**Why it slips through:** the URL contains 18 characters of mixed-case English, and the typo (`manaper` → `manager`) is one character transposed. The patch tool / write_file passes it silently.

**Defense (1 tool call):**
```bash
grep -n 'googletagmanager' FILE.html
```
Confirm the line contains `googletagmanager.com` exactly. Common misspellings to watch for:
- `googletagmanaper` (transposed `a-p-e-r` for `a-g-e-r`)
- `googletagmanger` (missing `e`)
- `googletagmanagr` (missing `e`)
- `tagmanager` (missing `google`)

**Same review for canonical URL:** a typo on `<link rel="canonical" href="https://oriental-destiny.com/...">` is worse than the gtag typo — it breaks SEO. After every write_file, confirm the canonical URL is correct.

**Why this matters:** the broken analytics snippet would silently ship to production and disable page-view tracking. The user would notice weeks later when GA reports flatlined.

## 2. Chinese-character accidents (verified 2026-06-09)

See the main SKILL.md section "Patch tool pitfall: Chinese-character accidents in English articles" for the full pattern. The 2026-06-09 case was `实验室` accidentally inserted mid-sentence.

**Combined defense (2 grep calls, run in parallel):**
```bash
grep -n 'googletagmanager' FILE.html  # gtag URL integrity
grep -P '[^\x00-\x7F]' FILE.html | head -10  # CJK accidents
```

Run both after every `write_file` or `patch` on a long English article. Total cost: 2 tool calls. Catches: broken analytics, broken canonical, silent CJK inserts.

## When these patterns most likely fire

- When the cron is under time pressure (operator wants the article out before a deadline)
- When the writer is copy-pasting a 200-line `<head>` block from a prior article
- When the writer is updating an analytics snippet in a hurry (e.g. switching GA IDs)

The defensive grep is a 1-2 tool call insurance policy against a class of bugs that are otherwise invisible until production.