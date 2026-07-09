# Thread-Promise Fulfillment & Keyword-Template HARD RULE

Two complementary patterns, both verified on oriental-destiny.com 2026-07-09.
Companion to the SKILL.md "Pivots and pivots" section.

---

## Thread-Promise Fulfillment (verified 2026-07-09, oriental-destiny)

**Definition:** when a prior article's BODY text made an explicit date-promised content claim (e.g. "the next article (July 8) walks the dining room. The article after that (July 9) walks the home office."), the next cron run should generally honor that promise unless the promised topic has been covered elsewhere or a stronger reason to pivot exists.

**Verification case (2026-07-09):**

The 2026-07-07 hallway article body contained this exact sentence:

> "The thread-continuity reason this article exists: ... the next article (July 8) walks the dining room in Earth Month. The article after that (July 9) walks the home office."

The 2026-07-08 cron run did not ship an article (no file in the repo for that date). On 2026-07-09, the cron run wrote the home-office-in-Earth-Month article even though a home-office article already existed at `fate-2026-06-15.html` (the Fire-Month home office from June). The Fire-Month home office and the Earth-Month home office are genuinely different reads:

| Aspect | Fire Month (06-15) | Earth Month (07-09) |
|---|---|---|
| Core problem | Focus slipping (could not hold a thought) | Focus refusing to land (five thoughts, no choice) |
| Lamp | Cool-white, near-full brightness | Warm-white, 60-70% dimmer |
| Chair posture | Forward lean (90 deg, attention-pushing) | Slight back lean (100 deg, accepting) |
| Monitor height | Above eye level (commanding) | At or below eye level (receiving) |
| Desk surface | Bare, institutional | Two or three personal objects, inhabited |

So the thread-promise article was substantively new, not duplicative. The seasonal-angle distinction made it shippable.

**Decision rule for honoring vs. pivoting from a thread-promise:**

1. **Honor verbatim** when:
   - The promised topic has NOT been written for the current season (seasonal-angle distinction makes it new), AND
   - No other open thread is more urgent (e.g. a solar-term landing day, an emergency SEO batch, a recovery from a cap-hit).

2. **Pivot to a different topic** if:
   - (a) The promised topic has a fresh, recent article in the same season (<7 days old), OR
   - (b) The seasonal angle is genuinely redundant with what's already on disk, OR
   - (c) A stronger signal overrides the promise — sibling-subagent's pending file, recovery state from Step 0, a date-promised solar-term eve article, etc.

3. **When pivoting away from a promise:** acknowledge the substitution in the new article's lead paragraph. A thread-promise that's silently dropped without acknowledgment looks like a missed deliverable. Example phrasing: "The July 7 hallway article planned today's slot for the dining room; this article pivots to stairs because [reason]..." The reader who read the prior thread should understand why the substitution happened.

4. **Always add a forward-link in the new article** back to the prior article that made the promise, so the thread-coherence signal travels both directions:

   ```bash
   grep -E "fate-YYYY-MM-DD" new_article.html
   ```

   Verify the link exists after `write_file`. A thread promise that the new article doesn't link back to breaks the in-thread navigation contract.

**Inverse of:** the "Referenced-but-never-covered pivot" pattern (which uses prior references to PICK a new topic). The thread-promise pattern uses prior body-text to OBLIGATE a specific topic and date. Both are valid thread-coherence signals.

---

## Keyword-Template HARD RULE Compliance Check (verified 2026-07-09)

**When the cron job prompt imposes a hard title/headline template, verify in 1 grep BEFORE the humanize pass.**

The oriental-destiny cron prompt's HARD RULE: every article's `<title>`, `<h1>`, `og:title`, `schema.org headline` MUST follow `[Primary Keyword]: [Long-tail Hook] | Oriental Destiny`, where Primary Keyword is "X Feng Shui" / "X BaZi" / "X Destiny" form. The `<meta name="description">` first sentence must contain the Primary Keyword verbatim.

**Compliance grep (run immediately after `write_file`, BEFORE humanize_score.py):**

```bash
grep -oE '<title>[^<]+</title>|<h1>[^<]+</h1>|og:title" content="[^"]+|"headline":\s*"[^"]+|<meta name="description" content="[^"]+' file.html
```

Expected: all 5 fields visible. Title and H1 must be IDENTICAL. Headline may omit the trailing `| Oriental Destiny` site suffix but must match the first half.

**Pass/fail check:**

```bash
# All 4 title-class fields must match X Feng Shui / X BaZi / X Destiny pattern
grep -oE '<title>[^<]+</title>' file.html | grep -E '(Feng Shui|BaZi|Destiny|中式)'
```

If 0 matches across the 4 title-class fields, the article violates the HARD RULE — patch the fields to satisfy the template BEFORE running `humanize_score.py`.

**Failure cost when skipped:** the humanize score can come back 90/100 on an article that doesn't satisfy the template. The article ships, the keyword density is wrong, the SEO benefit is lost. There's no point in spending humanize-budget on an article that has to be rewritten for the template. Patch the template first, then run humanize.

**Common template failures:**

1. **Missing Primary Keyword in `<meta name="description">`:** the keyword appears in the title but the description buries it in sentence 3. Fix by leading the description with the keyword phrase (e.g. "Front Garden Feng Shui for July: what to do in the Fire-to-Earth transition. [additional prose]...").

2. **Topic-object-is-pure-time-adverb failure:** the cron prompt's X (object before "Feng Shui") cannot be a pure time expression. "Li Qiu Eve Feng Shui" is FAIL because X = "Li Qiu Eve" is a time phrase, not a thing. The fix is to anchor X to a concrete place or object ("Hallway Feng Shui for July" or "Door Feng Shui for Li Qiu" works; "Li Qiu Eve Feng Shui" fails).

3. **Title/og:title/headline divergence:** typically happens when the cron prompt was edited but the article was not. Run the grep and reconcile.

**Belt-and-suspenders:** after the humanize patch loop, before committing, re-run the grep. A small banned-vocab patch can accidentally introduce a template violation if the patch was sloppy.

---

## Cross-reference

For the broader thread-coherence patterns (room-walk completion, close-out checklist, narrow-window eve piece, outdoor-room walk), see SKILL.md "Pivots and seasonal transitions" section. This file covers only the two patterns verified on 2026-07-09: thread-promise fulfillment and keyword-template enforcement.
