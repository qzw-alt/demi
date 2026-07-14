# Cron Failure — Manual Recovery Recipe

Verified 2026-07-14 (chinahospitalsguide.com `daily-chg-medical-news`,
job_id `fa7a29b3464e`). Pattern generalizes to any daily-publish cron
that has a "research → write → ship" pipeline and burns through the
cron iteration cap.

## When this recipe applies

- Cron `last_status=error` for today's daily SEO article
- The cron output file (under `~/.hermes/cron/output/<job_id>/`) does
  **not** contain `[SHIPPED_OK] <URL>` token
- The repo's `news/YYYY-MM-DD-*.html` does not exist
- `git status` is clean (no ahead-of-origin state, no untracked today article)

This is a **true cap-hit failure**, not the false-positive kind (where
commit+push succeeded but the agent loop threw RuntimeError after the
final tool call). The 2026-07-14 case is the former.

## Why the cron failed

The prompt file (in `~/.hermes/cron/jobs.json`) **does** contain the
cap-safe rule:

> Commit + push MUST happen BEFORE the humanize loop.

But the cron agent **still** burned through its iteration cap on
research + first-pass writing before getting to the commit step. The
11th documented cap-hit failure mode for this cron (per the historical
record in the prompt itself: 06-14, 06-16, 06-17, 06-21, 06-28, 07-02,
07-04, 07-05, 07-12 brotli bug, **07-14 cap-hit**).

The structural fix that the prompt recommends — "ship at 60/100 first,
polish later" — works **only** when the agent that runs the prompt
actually executes that order. In practice, the cron agent optimizes
for "make the article good" first and "make the article shipped"
second. Same root cause as 11 prior cap-hits.

## The manual recovery recipe (verified 2026-07-14, ships in ~10 tool calls)

### Step 1 — verify state (1 tool call)

```bash
cd /home/ubuntu/chinahospitalsguide
git status
git log --oneline -5
ls -la news/ | tail -10
```

Confirm: clean working tree, no today article on disk, last successful
ship was yesterday. If a today article already exists on disk
untracked, STOP — that's a mid-pipeline cap-hit with a different
recovery recipe (see "Mid-pipeline cap-hit variants" at the bottom of
this file).

### Step 2 — read the cron output file to extract research (1-2 tool calls)

```bash
grep -nE "^## |SHIPPED_OK|ERROR|Error|Traceback" \
  ~/.hermes/cron/output/fa7a29b3464e/$(date +%Y-%m-%d)_*.md | head -40
tail -80 ~/.hermes/cron/output/fa7a29b3464e/$(date +%Y-%m-%d)_*.md
```

The cron output is the cap-safe handoff. The cron agent **did**
complete the research step before being cap-killed — the candidate
profile, source URLs, de-dup anchors, and article angle are usually
all there. Re-doing research from scratch is wasted tool calls.

In the 2026-07-14 case, the cron output contained:
- Candidate A (MMC recognition of 8 Chinese medical universities) +
  Candidate B (Sanfu Paste 2026 season opening)
- De-dup verification (0 matches for sanfu|Sinapis|Corydalis across
  the 91-article news library)
- Source URLs with verified dates (NPC 2024 review DOI, JEP 2025
  mechanism paper DOI, INPLASY protocols)
- Suggested article structure (Template B/C hybrid)
- Internal link targets (4 cross-references to recent TCM articles)

### Step 3 — write the article to disk (1 tool call)

```bash
# Use the template fingerprint from the most recent shipped article
# (e.g. 2026-07-13 Unitree G1 for chinahospitalsguide). Don't
# re-derive the CSS / JSON-LD structure — copy the working template.
```

The article template for chinahospitalsguide (verified 2026-07-14) is:
- ~2,500-3,500 words
- JSON-LD as **array** with `[Article, FAQPage]` items (per CONTENT_GUIDE.md)
- `mainEntityOfPage.@id` with full pretty URL
- 5-6 FAQPage questions
- Internal links: ≥1 `/news/` (cross-link), ≥1 `/blog/`, `/contact/`
- H2 banned-vocab audit BEFORE commit (remove `actually` from H2s —
  8 points each per 06-22 verified pattern; leave `pivotal`/
  `landscape` in clinical-research prose)

### Step 4 — commit + push IMMEDIATELY (2 tool calls)

```bash
git config user.email "hermes@chinahospitalsguide.com"
git config user.name "Hermes Agent"
git add news/2026-07-14-<slug>.html
git commit -m "article: 2026-07-14 — <Title>"
git push origin master
```

**Why before sitemap/index patches:** in the cron failure mode, the
cap always fires during humanize or sitemap/index steps. By the time
you've reached manual recovery, the goal is "ship today, polish if
budget allows" — not "make it perfect before publishing." The next
commit will patch sitemap + index; this one ships the article itself.

### Step 5 — patch sitemap.xml (1 tool call)

Insert the new `<url>` entry **between the prior day's entry and the
last shipped entry** (for a daily news site the order is reverse-
chronological; new entry goes at the top of the recent batch). Use
`patch` with a precise `old_string` anchored on the most-recent entry.

**Pitfall: trust the file, not the diff.** Patch tool's unified diff
can show insertions in misleading positions (looking like they're
inside the wrong `<url>` block). After every patch, verify with:

```bash
grep -nE "YYYY-MM-DD-(NEW|YESTERDAY)" sitemap.xml
```

If the new entry is in the wrong position or has malformed XML
(missing `</url>` close, broken `<changefreq>`/`<priority>`), fix it
before committing the sitemap patch.

### Step 6 — patch news/index.html (1 tool call)

Insert the new article card **before the most-recent shipped card**
(again reverse-chronological). Use the **canonical pattern** that
the repo uses for that article type:

For chinahospitalsguide (verified 2026-07-14):

```html
<article class="news-item">
    <img src="../images/wellness-spa.jpg" alt="<Title>">
    <div class="news-content">
        <span class="news-date">July 14, 2026</span>
        <h2 class="news-title"><a href="2026-07-14-<slug>.html"><Title></a></h2>
        <p class="news-excerpt"><2-3 sentence excerpt></p>
        <a href="2026-07-14-<slug>.html" class="read-more">Read More →</a>
    </div>
</article>
```

**Image filename sanity check:** before referencing any image in the
card, run `ls images/ | grep -i <KEYWORD>`. If no match, fall back
to one of the curated defaults: `wellness-spa.jpg`, `china-hospital.jpg`,
`global-medical.jpg`. Don't invent a path.

### Step 7 — commit + push the patches (1 tool call)

```bash
git add sitemap.xml news/index.html
git commit -m "index: YYYY-MM-DD <slug> news card + sitemap entry"
git push origin master
```

### Step 8 — humanize pass (2-3 tool calls, optional if budget allows)

Run banned-vocab audit + em-dash density check. The 2026-07-14 case
caught two `actually` in H2s after first commit and shipped them as a
follow-up commit:

```bash
git add news/2026-07-14-<slug>.html
git commit -m "fix: remove 2 'actually' from H2s (humanize per 06-22 lesson)"
git push origin master
```

Acceptable score band for chinahospitalsguide: 75-85 for 2,500-3,500
word articles, 60-70 for 4,000+ word long-form (per the verified
baseline in `references/article-archetypes-2026-07.md`).

### Step 9 — HTTP 200 verification (2-3 tool calls)

```bash
# Wait for GitHub Pages deploy — DO NOT use `sleep 180` (the terminal
# tool's foreground timeout is 60s and will kill your command before
# the sleep completes). Use sleep 50 + separate curl, or run in
# background with notify_on_complete.
sleep 50
curl -s -o /dev/null -w "HTTP %{http_code} size=%{size_download}\n" \
  --max-time 25 \
  "https://chinahospitalsguide.com/news/YYYY-MM-DD-<slug>.html"
curl -s --max-time 25 \
  "https://chinahospitalsguide.com/news/" | grep -c "YYYY-MM-DD"
```

Expected: `HTTP 200`, byte count ~ matches your file size, the date
string appears 2x in `news/index.html` (link + visible title).

### Step 10 — emit `[SHIPPED_OK]` token

End the response with:

```
[SHIPPED_OK] https://chinahospitalsguide.com/news/YYYY-MM-DD-<slug>.html <word_count> <humanize_score>
```

This is the contract the cron prompt enforces. Future cron false-
positive diagnostics (the "agent says error but actually shipped"
case) depend on this token being present in the manual-recovery output
just as much as in the cron-run output.

## Total tool-call budget

| Step | Tool calls | Cumulative |
|---|---|---|
| 1 verify state | 1 | 1 |
| 2 read cron output | 1-2 | 2-3 |
| 3 write article | 1 | 3-4 |
| 4 commit + push | 2 | 5-6 |
| 5 patch sitemap | 1 | 6-7 |
| 6 patch news/index | 1 | 7-8 |
| 7 commit + push | 1 | 8-9 |
| 8 humanize (optional) | 2-3 | 10-12 |
| 9 verify HTTP 200 | 2-3 | 12-15 |
| 10 emit token | 0 | 12-15 |

Comfortably under the cron's iteration cap (default 10, can be
extended). The full recipe fits in 10-15 tool calls.

## Mid-pipeline cap-hit variants (different recovery recipe)

If `ls news/$(date +%Y-%m-%d)-*.html` returns a file (today's article
exists on disk but is untracked), that's a different failure mode with
a shorter recovery:

1. Verify article completeness with `head` + `tail`
2. Check `grep "$(date +%Y-%m-%d)" sitemap.xml` — if 0 matches,
   sitemap unpatched
3. Check `grep "$(date +%Y-%m-%d)" news/index.html` — if 0 matches,
   news/index unpatched
4. Patch whichever is missing
5. `git add news/...html sitemap.xml news/index.html`
6. `git commit -m "article: YYYY-MM-DD"` + `git push origin master`
7. Verify HTTP 200

Total: 5-7 tool calls. Faster than the research-still-needed recipe
above because the article is already on disk.

The detection signal that distinguishes the variants:

| State | Failure mode | Recovery cost |
|---|---|---|
| No today file, clean tree | **Research completed, article never written** (07-14 case) | 10-15 calls (full recipe above) |
| Today file on disk, untracked, no commit | Mid-pipeline cap-hit (06-17, 06-28 variants) | 5-7 calls |
| Today file on disk, committed locally, no push | Post-commit cap-hit (06-14 variant) | 1-2 calls (`git push origin master` + verify) |
| Today file on disk, committed, pushed, no `[SHIPPED_OK]` | False-positive cap-hit (07-11 Betta case) | 0 calls — just report success |

The cron prompt encodes all four but the practical signal at the top
of the next run is: `git status` + `ls news/$(date +%Y-%m-%d)-*.html`.

## Long-term fix (not yet applied as of 2026-07-14)

The cron prompt contains the cap-safe rule but the cron agent doesn't
follow it under iteration pressure. Two structural options, both
untested as of 2026-07-14:

1. **Raise the cron's max_iterations** in `~/.hermes/cron/jobs.json`
   (or via `hermes cron edit <id> --max-iterations 25`). Pro: simple.
   Con: extends failure time, doesn't fix the underlying agent
   behavior.

2. **Hard-code the publish-plumbing-first order into the prompt**
   as numbered steps with explicit gates ("Step 4: write article.
   Step 5: commit + push + HTTP 200 verify. Step 6: patch sitemap.
   Step 7: patch news/index. Step 8: humanize pass IF budget remains.").
   Pro: forces the order. Con: prompt becomes more rigid, may not
   survive `git pull` when Weiye edits the prompt in master.

Neither has been applied to `daily-chg-medical-news` as of 2026-07-14.
The structural fix is **deferred until** the third consecutive
cap-hit in a 30-day window, per Weiye's "3-in-30-days trigger rule"
in `references/cron-cap-hit-log.md` (which the cron prompt references).

## Related

- The cap-hit log itself lives in the cron prompt body
  (`references/cron-cap-hit-log.md` is referenced from inside the prompt).
- The chinahospitalsguide content template + JSON-LD-array pitfall is
  in the `chinahospitalsguide-content` skill.
- The `[SHIPPED_OK]` token rule was added 2026-07-11 — see the cron
  prompt itself for the contract.