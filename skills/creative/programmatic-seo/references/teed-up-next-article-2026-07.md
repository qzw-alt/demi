# Teed-Up Next-Article Signature (verified 2026-07-26)

When the previous day's `fate-YYYY-MM-DD.html` ends with a paragraph that **explicitly names the next article's topic** (e.g. "the next room is the study"), the current cron run should detect that target via `tail` and pick it up as the day's article instead of starting fresh research.

The signature is the **last paragraph of the article body** (before `</article>`), not the footer. It uses phrasing like:
- "the next room is the X, where qi does Y"
- "the week to come will fold what these rooms say into Z"
- "tomorrow's article will close the thread on A"
- "the next piece is the B"

## Why it matters

When a monthly thread (June Fire Month, July indoor/outdoor walk, 5-gate outdoor property walk, etc.) reaches its final articles, the writer seeds the *next* article's topic in the closing paragraph so the next day's cron run has an obvious target. Without detecting it, the next run burns 1-2 research calls re-deriving a target the prior article already named.

Verified case (2026-07-26 cron run):
- Prior article: `fate-2026-07-25.html` (bedroom)
- Closing paragraph: "The indoor thread has moved from the living room's long settling, through the dining room's meal rhythm and the kitchen's quick hands, to the bedroom's night-settling. **The next room is the study, where qi narrows into concentrated bursts.** It will need another seven-position walk, but the pace will be completely different."
- Target picked up: `study` (specifically NOT `home office`, even though 06-15 and 07-09 had already done home office pieces — the article named study, not office)
- Article shipped: `fate-2026-07-26.html` — Study Feng Shui

## Detection recipe (~1 tool call at start of run)

```bash
tail -25 fate-2026-07-25.html | grep -oE 'next (room|article|piece|gate|step|section|pillar|concept)|tomorrow|next week|coming up|then turn to|will fold|next part'
```

If the grep returns a hit, read the matching sentence (`grep -B1 -A2 'next' fate-...html | tail -10`) to extract the named target. The named target is a single word or short phrase — match it against existing `grep -lE` de-dup checks before writing.

## De-dup grep is still mandatory

The signature names the topic but does not verify it hasn't been covered. Always follow up with the standard canonical de-dup:

```bash
grep -lE "(KEY TERM 1|KEY TERM 2)" fate-2026-*.html
```

If 1-2 matches in earlier months, ship anyway (revisit with new seasonal angle). If 3+ matches, the named target was already covered heavily — pick a referenced-but-never-covered pivot instead (see `referenced-but-never-covered` pitfall in SKILL.md).

## When the signature is ambiguous

Sometimes the closing paragraph names a *category* not a specific topic ("the next room is the study" — clear; vs. "tomorrow's piece will look at the gates" — five possibilities). In that case:

1. Cross-reference against the existing thread (which sub-thread is currently active?)
2. Check `ls *.html | grep -c KEYWORD` for each candidate
3. Pick the one with the lowest existing coverage that still threads naturally from yesterday

If still ambiguous, fall back to a normal pivot (referenced-but-never-covered, room-walk completion, or property-type trifecta) rather than guessing.

## When NOT to use this

- **Single-article threads** (one standalone piece on a topic): no signature is seeded, normal research applies
- **Pivot articles** (referenced-but-never-covered, room-walk completion): these explicitly do NOT seed next-article names because they're termini, not waypoints
- **First article of a month**: the prior month's closing article may have seeded it; check the very last article of the *prior month*, not yesterday's

## Pro-tip: seed the signature from your own write

When you write a thread-internal article that is NOT the last in the thread, end the article's closing paragraph with a forward-looking sentence that names the next article's topic. This converts tomorrow's cron run into a 1-call recovery (read the signature, write the article) instead of a 9-call fresh research run. The seasonal content threading pattern (June Fire Month, July outdoor walk, etc.) is built on this exact mechanism.

Example signature phrasings that have shipped cleanly:

- "The next room is the X, where qi narrows into Y. It will need another seven-position walk, but the pace will be completely different."
- "The thread has now walked all N major pieces. The week to come will fold what these rooms say into a smaller, single-room read for the household that does not have one: the corner of the bedroom or the apartment end-of-hall."
- "Tomorrow's article will close the thread on A before moving into B."

Use one of these phrasings, or a sentence with the same shape: *The next X is the Y, [where / because / which] [verb of differentiation].* Differentiation verb is the key — without it, the signature reads as a generic "more to come" closer.

## Related references

- `references/step5-site-divergence-2026-07.md` — for the Step 5 site-divergence matrix this signature interacts with
- `references/indoor-thread-room-walk-2026-07.md` — the indoor walk thread this signature was first verified against (07-22 living room → 07-23 dining room → 07-24 kitchen → 07-25 bedroom → 07-26 study)
