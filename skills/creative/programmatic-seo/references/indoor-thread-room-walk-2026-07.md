# Indoor-Thread Room Walk (verified 2026-07-22 → 2026-07-24, oriental-destiny)

The indoor-thread room walk is the room-by-room read that follows the outdoor-thread property walk (07-01 → 07-21). The outdoor thread walked the dragon from the sidewalk to the back gate; the indoor thread walks the dragon from the back door to the room the household settles into for the night.

## Verified sequence (July 2026 indoor thread)

| Day | Article | Room type | Qi velocity | Position count |
|-----|---------|-----------|-------------|----------------|
| 07-22 | Living Room | Settling volume | Slow, side-to-side, hours-long | 7 positions |
| 07-23 | Dining Room | Three-meal rhythm | Medium, gathering, three fixed times | 5 positions |
| 07-24 | Kitchen | Hands-rhythm | Fast, up-and-down, five-minute intervals | 5 positions |
| 07-25 | Bedroom | Night-settling | Very slow, downward, hours-long | 7 positions (predicted) |
| 07-26 | Study | Concentration | Very fast, focused, bursts | 7 positions (predicted) |

## Reference run: 2026-07-24 Kitchen

- **Article**: `fate-2026-07-24.html`
- **Word count**: 5,346
- **Score**: 95/100 (first pass, no humanize loop needed — only note was "high word count" which is the natural ceiling per the 06-11 rule)
- **Tool calls**: 9 (clean indoor-thread reference)
- **Tool breakdown**:
  1. `terminal` — `ls *.html | head` + `git status` + `git remote -v` (combined)
  2. `read_file` — `article_topics.md` + `terminology_mapping.md` (combined)
  3. `terminal` — `ls *.html | grep -iE "(kitchen|cook|stove)"` + `grep -oE '<h[1-3]>' fate-2026-07-23.html` — confirmed no kitchen article + voice reference structure
  4. `read_file` — `fate-2026-07-23.html` (offset 1-200 + 200-270) — full voice + scaffolding + FAQs + footer
  5. `read_file` — `references/outdoor-to-indoor-thread-pivot-2026-07.md` — confirmed 07-24 = Kitchen slot in the indoor-thread sequence
  6. `write_file` — `fate-2026-07-24.html` — 5,346-word article (1 typo in gtag URL caught in next call)
  7. `patch` — fixed gtag URL typo (`gtagmanater` → `googletagmanager`)
  8. `terminal` — `python3 scripts/humanize_score.py …` (95/100 first pass) + `grep` checks (no `actually` in H1/H2/H3, no CJK accidents, keyword template verified)
  9. `patch` sitemap + `terminal` git config + commit + push + sleep + curl --max-time 30 (chained) — HTTP 200 verified

Total: 9 tool calls, 5,346 words, 95/100, zero recovery, zero cap-hit. **Cleanest indoor-thread article to date.**

## Hands-rhythm vs voices-rhythm framing (verified 2026-07-24)

Each indoor room has a distinct qi-velocity that drives the read:

| Room | Qi velocity | Active sense | Time on task |
|------|-------------|--------------|--------------|
| Living Room | Slow, side-to-side, hours-long | Sight + sound (TV, conversation) | Hours |
| Dining Room | Medium, gathering, three fixed times | Sound + taste (conversation, food) | 30-45 min × 3 |
| Kitchen | Fast, up-and-down, five-minute intervals | Touch + smell (hands on ingredients) | 20-45 min × 3 |
| Bedroom | Very slow, downward, hours-long | Touch (mattress, linens) | 7-9 hours |
| Study | Very fast, focused, bursts | Sight (screen, paper) | 1-4 hour bursts |

The article opens by naming the room's qi velocity and contrasting it with the prior day's:

> "Yesterday's piece walked the dining room — the room the dragon settles into at the same times every day for the same activity, the room where the household's qi learns a rhythm. The dining room is a voices room. The household talks at the table, the household lingers after the meal, the household's qi in the dining room moves at the speed of conversation — slow, settling, side to side. The kitchen is a hands room. The household chops, stirs, washes, plates, the household's qi in the kitchen moves at the speed of hands — fast, focused, up and down."

**Bridge pattern for the next indoor-thread article (bedroom, 07-25):**
> "Yesterday's piece walked the hands-rhythm — the room the household's qi moves through fastest. Today's piece walks the night-settling — the room the household's qi settles into for hours when the household sleeps."

## Four-element productive-cycle path-trace test (verified 2026-07-24)

The kitchen is the only room in the house where four of the five elements share one space:

- **Fire** at the stove
- **Water** at the sink
- **Wood** on the cutting board and in the cabinets
- **Metal** in the knives, pots, utensils, refrigerator
- **Earth** at the cook's center (the cook standing position)

The path-trace test: watch the cook make a meal. Trace the cook's path through the elements. Does the cook's path move through the **productive cycle** (Metal pot → Water from sink → Wooden spoon → Fire stove) or does the cook's path **fight the cycle** (Wood on Metal hook, Metal on Wooden board, Fire next to Water with no buffer)?

**Most kitchens fail on the last step** (fire-water fight with no Wood buffer between them). The fix is to add the missing element:
- A **wooden cutting board** between the sink and the stove = Wood buffers Fire-Water
- A **metal pot rack** near the stove = Metal completes the cycle before Fire
- A **ceramic tile or wooden trivet** at the cook's center = Earth grounds the cook

**The wooden-buffer fix is the highest-value content in the kitchen article** and is reusable for any room where 3+ elements share a space (study, bathroom, outdoor kitchen). When the same fix recurs across multiple articles, lift it into a class-level concept.

## 5-position vs 7-position rule (verified 2026-07-24)

The number of positions in a room walk scales with the room's function-density, NOT its square footage:

| Function density | Position count | Examples |
|------------------|----------------|----------|
| Single dominant activity, smaller room | 5 positions | Dining room, Kitchen |
| Multiple simultaneous activities, larger room | 7 positions | Living Room, Master Bedroom, Study |
| Outdoor gate (transit, one direction) | 3 positions | Front gate, Back gate, Doorway |
| Outdoor small room (limited control) | 3-5 positions | Balcony (3), Side yard (3), Stairway (5) |

**Decision rule:** count positions = 5 for "one room, one job" reads; 7 for "one room, multiple jobs" reads. Outdoor gates and small outdoor rooms use 3-5 positions depending on homeowner control (per `outdoor-room-walk-thread.md`).

## gtag URL typo pitfall (verified 2026-07-24)

When writing the Google Analytics snippet by hand instead of copying from a prior article's head block, the URL `https://www.googletagmanager.com/gtag/js?id=G-TBGDZRZZEJ` is easily fat-fingered as:

- `googletagmanater` (missing second `g`, `r` transposed) — the actual typo in the 07-24 first draft
- `googletagmanager` (missing `.com` slug)
- `gtag.js` without the full domain

**Fix:** ALWAYS copy the GA snippet from the most recent published article's head block rather than typing it from memory. The same applies to the OG / canonical / JSON-LD schema lines — copy the head block wholesale from the most recent prior article, then change only the title / description / date / URL / headline fields.

The skill's existing `@@type` pitfall in SKILL.md covers the JSON-LD typo; this one covers the GA URL specifically. Add to the verification routine: after `write_file`, `head -10 FILE.html` and visually confirm the GA URL is intact before any other patches. The 07-24 typo was caught in 1 tool call (a single-line `patch`); a typo that ships costs the same patch effort AND a re-push.

## Sibling-subagent sitemap warning (re-confirmed 2026-07-24)

The `patch` tool's "sibling subagent modified this file" warning fired again on the 07-24 sitemap edit. The working recipe held:

1. Trust the warning as a yellow flag, not a fatal
2. After the patch, `head -20 sitemap.xml` to verify the entry landed at the top
3. `grep -c "fate-2026-07-24" sitemap.xml` to confirm only 1 entry (no duplicate from sibling)
4. If duplicate: read the file, manually compose the merged version, patch again

The 07-24 sitemap confirmed clean in 1 tool call (the head + grep combined).

## Cross-references

- `outdoor-to-indoor-thread-pivot-2026-07.md` — the bridge pattern that began this thread; predicts the 07-22 → 07-26 indoor sequence verbatim
- `outdoor-room-walk-thread.md` — the Fu Wei ladder and move-set that preceded this thread
- `references/humanize-score-script-pitfall.md` — em-dash density per site (oriental-destiny 10-18; 07-24 had 24 em-dashes = 5.4 per 1200 words, well within band)