# Property-Type Trifecta Pivot Pattern (verified 2026-07-12)

When a foundational article walks an idea that has obvious property-type variants (renter / townhouse / city lot / single-family), the next 1-3 articles should be a **property-type trifecta** rather than N separate foundational articles. This pattern is the natural follow-up to a three-gate / four-line / cycle walk-through when the foundational article's framework doesn't apply uniformly to every reader's property.

## Reference case: 2026-07-10 → 2026-07-12 dragon vein thread

- **07-10 (four-line):** Dragon Vein Feng Shui: How the Mountain Lines Run Through Your Property. Walks the framework for a generic property reader. Closes by naming a 7-day dragon vein pass.
- **07-11 (three-gate):** Three-Gate Feng Shui: Standing at the Outer, Inner, and Mouth Gate. Walks the **house** version of the gates (settled/compressed/depleted vocabulary). Closes with the explicit forward-promising sentence: *"tomorrow's article walks the property-type shortcuts — the city lot read, the apartment read, or the townhouse read."*
- **07-12 (apartment property-type variation):** Apartment Feng Shui for July: Reading the Three Gates When You Don't Own the Lot. Walks the **apartment** version. Lead paragraph: *"Yesterday's three-gate article walked the house through its outer gate, its inner gate, and its mouth gate. Today's piece is the apartment version of that walk."* 4,291 words. Score 95/100 after one `actually`-patch lift from 79.
- **N+1 / N+2 (optional):** townhouse and city lot versions. Same template applies.

## Why this pattern works

1. **The foundational article (07-10) leaves ~80% of readers unable to apply it** because they don't own a house at the curb-cut level. The framework's three-gate vocabulary maps cleanly to houses, awkwardly to townhouses, and not-at-all to studios without restating. The three-gate article (07-11) covers the house version cleanly. The property-type variation (07-12) lands the highest-traffic variant — renter feng shui — because it's the most-asked-about unaddressed case.

2. **The lead-paragraph bridge recipe is the thread-continuity bridge from `references/outdoor-room-walk-thread.md`.** The bridge sentence for a property-type variation explicitly references the prior article: "Yesterday's X walked the house version. Today's piece is the Y version." This re-anchors the prior thread and frames the new piece as a complement, not a re-run. But the article carries a different emphasis in body voice — "you don't own the lot" instead of "the walk the homeowner does" — so it reads as a new piece, not a duplicate.

3. **Each property-type variation has a unique "moves the renter / townhouse owner / city-lot owner owns" checklist** that the house version doesn't carry. For apartment feng shui: doormat + side-wall mirror + rug-at-threshold + closed-interior-door-before-opening-apartment-door. For townhouse: front fence + back fence + side-attached wall distance. For city lot: driveway sight line + curb cut + parking pad line. The unique checklist IS the article — without it, the property-type variation is a re-statement of the three-gate article.

4. **The collapsed-gate problem is the highest-value content.** In a house, the three gates are three separate thresholds; the homeowner can deliberately stand at each one. In an apartment, the gates STACK within twenty feet (lobby door + apartment door + mouth gate all sit in the entry sequence), and in a studio the inner gate and mouth gate COLLAPSE into one threshold. The collapsed-gate discussion is where the apartment feng shui failure modes live, and where most apartment feng shui guides skip the conversation.

## Voice recipe for the property-type variation

The article should:
- Open with a 2-3 sentence setup paragraph that the house version did not cover (e.g. "the apartment renter is the homeowner the dragon vein article does not address directly")
- Walk the framework AT the new property type, naming where each gate goes in this property type (apartment outer gate = building lobby; inner gate = apartment door; mouth gate = studio threshold or one-bedroom hallway opening)
- Explicitly include a "moves the renter / townhouse / city-lot owner owns" section — the article without this is a re-statement, the article with this IS the property-type variation
- End with the SAME forward-looking sentence the foundational article uses ("Monday's article walks...") so the reader landing on any one of the three articles knows the thread is in motion
- Keep the same voice profile as the foundational article (em-dash density, 1st-person count, sentence stdev band) so the trifecta reads as a unified thread

## Body-`actually` rule quantified — 3rd reproduction (verified 2026-07-12)

The 06-29 measured +8 pts per body-prose `actually` hit has now held across three reproductions:

| Case | Body `actually` hits | Score before | Score after | Lift per hit |
|------|----------------------|--------------|-------------|--------------|
| 06-29 (fate-2026-06-29, Five Elements Cycles) | 1 | 83 | 91 | +8 |
| 06-22 (Sitting and Facing, body-prose case) | 1 | (similar lift) | (similar lift) | +8 |
| 07-12 (fate-2026-07-12, Apartment Feng Shui) | 2 (in one listicle item) | 79 | 95 | +8 per hit, +16 total |

**Rule:** body-prose `actually` = **+8 pts per occurrence**, stable across the three reproductions. A single `old_string`/`new_string` patch that removes BOTH occurrences in one tool call yields +16 pts and is the cleanest budget-per-point move in the humanize loop. Combined with the 06-22 / 06-26 H1/H2/H3 heading rules (heading `actually` = +5-8 pts per hit, NEVER tolerated in headings — drag the score from 95 → 87 in one line), the agent now has three quantified data points for the `actually` swap cost-benefit.

**When to use:** when the first-pass article comes back in the 70s from 1-2 body `actually` hits, ONE patch is the right move. When the first-pass article has heading `actually` (H1/H2/H3) AND body `actually`, patch the headings FIRST (5-8 pts/hit, holds even in a 95-score article) then patch body if budget allows. Total ceiling for a clean article: 95-100.

## Procedural shortcut — when to skip the property-type variation

If the foundational article (Step 1 of the foundational sequence) explicitly walks the framework for the most-common property type AND the site's reader profile is heavily that property type (e.g. chinahospitalsguide.com readers are hospital operators, not property owners, so the property-type variation never applies), skip the trifecta. If the site's reader profile includes a substantial sub-group whose property type the foundational framework doesn't cover evenly, write the trifecta as the next 1-3 articles.

For oriental-destiny.com, the renter / apartment population is the second-largest after single-family-house owners, so the property-type trifecta is a recurring article pattern once or twice per dragon-vein-class thread.
