# Narrow-Window Eve Piece (NEW pattern, verified 2026-07-06, oriental-destiny.com)

A sibling pattern to the "Thread close-out checklist" (06-30): when a month's themed thread reaches the final day before a solar term handoff (Li Qiu in summer, Li Qiu / Autumn Begins in August, etc.), write a piece that **narrows further than the close-out did**, covering only the single evening or single sunrise-window the close-out couldn't fit.

## When this pattern applies

Use a narrow-window eve piece when:
1. A multi-day close-out article has just been written (e.g. 07-05's "Outdoor Feng Shui Close-Out: The Whole-Property Walk Before Li Qiu").
2. The solar term lands within ~48 hours of the close-out (Li Qiu on 07-07 means the 07-05 close-out has only 1 more day).
3. The close-out referenced a "tomorrow morning walk" or "eve piece" in its FAQ section but didn't deliver it (07-05 FAQ: "tomorrow's homeowner will read what the season did overnight").
4. There's still room in the thread for one more piece without breaking the seasonal arc.

If the solar term is more than 1 week away, skip this pattern — use a regular pivot (referenced-but-never-covered) instead.

## Structure that works (verified 2026-07-06, 3,891 words, score 95/100)

Six H2 sections, ~3,500-4,000 words:
1. **Why the eve gets its own article** — 1 paragraph framing the narrow window, plus the thread-continuity sentence pointing back to the close-out
2. **What stays out on the property** — bulleted checklist with cycle-tag pills (Sheng/Ke/Hold), the items the close-out identified as anchors
3. **What comes inside before bed** — numbered list, 6-8 items in priority order, framed as "the leftover, the half-done" not a re-decision
4. **What to leave on the property's edge after dark** — 3 actionable items (a single candle, one warm-white porch light, one back window cracked), each with the cycle-theory reason
5. **What to watch for at dawn tomorrow** — sensory observations (color, sound, light clarity, air temperature), each explained as "what the cycles are doing" not "what you'll visually see"
6. **Day-master-by-element eve reading** — the per-chart candle/porch-light/candlelight pattern (Wood/Fire/Earth/Metal/Water each get a recommendation that changes the setup)

Plus:
- A **timeline grid** (6pm → 7am) using a new CSS class `.timeline` with two columns: `t-time` (left, cinnabar) and `t-when` (right, ink). This is the key visual differentiator vs. the close-out checklist (06-30) which uses a flat `.checklist` list.
- 5-7 FAQs, one of which is the predictable "I am going to bed early tonight. Do I need to stay up for the handoff?" (always YES/no, the cycles accept morning observation)

## Key technique: the timeline grid (NEW CSS, verified 2026-07-06)

```css
.timeline { display: grid; grid-template-columns: 90px 1fr; gap: 10px 18px; margin: 22px 0 26px; padding: 18px 22px; background: rgba(255, 252, 246, 0.6); border-radius: 10px; border: 1px solid var(--line); }
.timeline .t-time { font-weight: 700; color: var(--cinnabar); font-size: 0.95rem; }
.timeline .t-when { color: var(--ink); font-size: 0.98rem; }
```

Markup form (each row is two adjacent divs, NOT a `<ul>`):

```html
<div class="timeline">
    <div class="t-time">6:00 pm</div>
    <div class="t-when"><strong>Sunset.</strong> Lit candle placed by front door. Porch light on warm-white if available. Back window cracked open.</div>
    <div class="t-time">6:30 pm</div>
    <div class="t-when"><strong>Evening bag pass.</strong> Six to ten items collected from the four rooms, placed in the hold-pile basket.</div>
    ...
</div>
```

The timeline grid is the closest thing to a scheduled-by-clock visual the site's CSS carries. It's appropriate when the article's content is implicitly time-bounded (an evening with discrete phases from 6pm to 7am).

## Bridge sentence pattern (verified 2026-07-06)

The lead paragraph carries the same job as the 06-30 close-out lead, but narrower:

> "Sunset on July 6 to sunrise on July 7. About sixteen hours, one transition, four outdoor rooms still reading Fire. A single-evening walkthrough for the homeowner who already did the July 5 property read and the July 6 undo, and who is now standing in the kitchen at dusk wondering whether to leave the patio lantern lit overnight."

The phrase "standing in the kitchen at dusk wondering whether to leave the patio lantern lit overnight" is the humanizer-friendly way to anchor the article's purpose without saying "a guide to Li Qiu eve." It also signals the article's voice: a homeowner-facing piece, not a chart-side piece.

## Voice note: the "as is / stays" pattern

Narrow-window articles have a different verb profile than multiday articles. Multiday articles use "walk," "undo," "observe." Narrow-window articles use **"stays"**, **"stays out"**, **"comes inside"**, **"stays lit"**, **"stays cracked"**. This subtle pattern — the present-tense stative verb instead of the imperative action verb — matches the eve's actual ask of the homeowner (hold steady, don't change anything). Articles full of imperatives read as "do this" articles; articles full of stative "stays" read as "this is fine, leave it alone" articles, which is what an eve piece should read as.

## Banned-vocab watch (verified 2026-07-06)

The article's voice has fewer "actually" / "leverage" / "navigate" hits than a multiday close-out because the prose style is observational rather than instructional. The 07-06 first pass had 1 body-prose `actually` ("actually doing good Fire work"), which patched to "doing real Fire work over the last six weeks" for 95/100. The 06-29 1-body-actually-+8-point pattern held.

Two notes specific to the eve piece:
- The phrase "is meant to" (as in "the item is meant to return in late August") is a soft AI-tell. The patch swapped to "the cure the homeowner wants back in late August" — a concrete noun ("the cure") instead of the passive "is meant to."
- The phrase "is over-correcting" worked cleanly because the chart-side read justified it. Don't strip every "is [gerund]" — only strip when the gerund is a soft hedge rather than a technical description.

## Cross-link targets (verified 2026-07-06)

The footer cross-link list for an eve piece should:
1. Link back to the close-out (the article 1 day before this one)
2. Link to the most recent room-by-room article (the article 2 days before this one, or the day-master series if the series completed earlier)
3. Link to the foundational concept article (Five Elements Explained) for first-time readers
4. Use the wording "Continue the July thread:" not "Related articles:" — the thread language signals series coherence

## When NOT to use this pattern

- If the solar term is more than 7 days out, a multiday pivot serves better (the article can cover more rooms / properties / chart variations).
- If the close-out was already a single-day article (not multiday), there's no further narrowing to do — the close-out IS the eve piece.
- If today's article slot is taken by a different thread (e.g. a planted car or hospital article from another cron schedule), wait one day and use the next slot.

## Budget note

The 07-06 run fit in 10 tool calls (pre-flight combined check → research read combined → voice reference read → de-dup grep → write_file → non-ASCII + word-count + score combined → single banned-vocab patch → re-score → sitemap patch → git commit+push+verify chain). When the close-out was cleanly written the day before and the theme is well-defined (Li Qiu eve = 16-hour window with specific items), the article is mostly template-fill on top of a fresh structural outline. The 3,891-word output landed naturally on first write.
