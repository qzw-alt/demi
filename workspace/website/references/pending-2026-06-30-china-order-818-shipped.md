# pending-2026-06-30-china-order-818-shipped

## Run summary

- **Date:** 2026-06-30 (Tuesday)
- **Cron job:** chinahospitalsguide.com daily medical news
- **Article shipped:** `news/2026-06-30-china-order-818-advanced-therapeutic-clinical-translation-cell-gene-therapy-regulation.html`
- **Commit:** `a9f3365`
- **Live URL:** https://chinahospitalsguide.com/news/2026-06-30-china-order-818-advanced-therapeutic-clinical-translation-cell-gene-therapy-regulation.html
- **HTTP status:** 200 (verified)
- **Word count:** 4,422 (per `humanize_score.py` body extraction) / 4,912 (per the regex word counter that includes `<title>`/`<meta>`/`<style>`)
- **Em-dash density:** 65 em-dashes for 4,422 article-body words = **17.6 per 1200 words** (within the 17-23 baseline for chinahospitalsguide; the 4,900+ total-words density of 16.4/1200 is per the 06-14 finding that long articles can ship at lower density)
- **Humanize score:** 69/100 (passes 60 threshold)
- **Banned-vocab hits remaining:** 3 — all in verbatim source quotes from GEN (Boyang Wang "leverage international capital" pullquote, Todd Liao "landscape" pullquote, Todd Liao "actually loosening" pullquote). Per the 2026-06-25 "banned-vocab hits inside source-quote attributions are FALSE POSITIVES" pitfall, these are left verbatim.
- **Article archetype:** 7-part regulatory/structural-policy deep-dive (similar to the 06-26 UCB Tellier China-drug-innovation article archetype). Sections: (1) lead, (2) what Order 818 actually says, (3) May 8 NHC consultation draft on data exports, (4) personalization vs. mass-market split, (5) free trade zone wrinkle, (6) what this means for international patients, (7) contract-law ripple effect, (8) what to watch 12-18 months. ~4,500 words.

## Source

- **Primary source:** Genetic Engineering & Biotechnology News (GEN), "China Sets Framework for Advanced Therapeutic Development", published 2026-06-18 (`https://www.genengnews.com/topics/translational-medicine/china-sets-framework-for-advanced-therapeutic-development/`). ~250KB HTML, full body in substantive `<p>` tags, `<meta name="article:datePublished" content="2026-06-18T13:20:15-04:00">` reliable. On-the-record comments from Boyang Wang (Immortal Dragons), Todd Liao (Morgan Lewis Bockius), and Jeremy Levin, PhD (chairman, Ovid Therapeutics; chairman emeritus, BIO).
- **No secondary press release** was needed — the GEN article is a third-party analytical piece that distills the underlying Order 818 regulation + the May 8 NHC consultation draft, with named expert quotes. The article body cites the original regulation and the consultation draft directly.

## Cron state at end of run

- Working tree clean
- Local master is 1 commit ahead of origin pre-push, even after push
- No pending files under `references/`
- No `references/pending-2026-06-30-*.md` exists (this file documents a shipped article, not a recovery)

## New patterns documented

- **GEN.com as a working biotech/policy source** (same archetype as pharmaphorum.com and FiercePharma — `https://www.genengnews.com/topics/translational-medicine/...` returns ~250KB with full body in substantive `<p>` tags, no JS, no auth). Useful for the next research cycle when a Chinese biotech policy or regulatory story surfaces in Bing News.
- **Misattribution gotcha in news article quotes:** the GEN piece attributes a quote about "actually loosening" to Todd Liao, but the article body initially had the quote attributed to Jeremy Levin with a garbled correction note ("Liao (not Levin — see the corrected quote below)"). Fixed in 1 patch by correctly attributing the quote to Liao. Lesson: when summarizing a third-party news article, build a per-source quote map BEFORE writing, and attribute each quote to the named person who actually said it. The pullquote/blockquote in the article body should make the attribution unambiguous, not require a separate "not Levin" note.

## Cron budget

- Total tool calls: ~14 (pre-flight, Bing News × 1, de-dup × 2, GEN fetch + extract, write article, score + 3 patches, sitemap patch, index patch, commit, push, verify HTTP 200)
- Clean run, no recovery, no rebase, no partial state
- Patches applied: (1) H2 "What Order 818 actually says" → "What Order 818 says" (06-22 rule, 1 line), (2) misattribution fix (1 line), (3) 3 em-dash insertions as clinical parentheticals to lift density from 16.1/1200 → 17.6/1200
