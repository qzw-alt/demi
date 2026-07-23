# Indoor Room-Walk Thread Pattern (verified 2026-07-22 through 2026-07-23)

The companion pattern to `references/outdoor-room-walk-thread.md`. The outdoor thread walks the dragon across the property's perimeter (sidewalk → gate → dragon vein → three gates → property-type variants → room-by-room outdoor spaces). The indoor thread picks up after the dragon crosses inside and walks room-by-room through the dwelling, in a deliberate sequence.

## Established indoor sequence (verified as of 2026-07-23)

| Article | Room | Position count | Archetype |
|---|---|---|---|
| 07-17 | Stairway | vertical read | outdoor pivot |
| 07-18 | Balcony | in-between gate | outdoor pivot |
| 07-19 | Courtyard | private compound | outdoor pivot |
| 07-21 | Side Yard | narrow gate | outdoor pivot |
| **07-22** | **Living Room** | **7-position walk** | **first indoor article — settling volume** |
| **07-23** | **Dining Room** | **5-position walk** | **second indoor — three-meal room** |
| TBD | Kitchen | TBD | hands-rhythm room (the room that feeds the dining room) |
| TBD | Bedroom | TBD | night-settling room |
| TBD | Study / Home Office | TBD | focus room |
| TBD | Bathroom | TBD | water-room |

Position count varies by room: smaller rooms (Dining, Kitchen, Bath) use the **5-position walk**; larger rooms (Living Room, Stairway, Bedroom) use the **7-position walk**. The 07-22 Living Room article laid down the 7-position template explicitly; the 07-23 Dining Room article scaled it down to 5 positions for the smaller room. Future indoor articles should match the template to their room's size.

## Universal scaffolding (every indoor article uses this shape)

1. **Why this room is the room the indoor thread walked toward** — re-anchors the prior thread explicitly; e.g. 07-23 lead: *"Yesterday's piece walked the living room. Today's piece walks the room the dragon settles into when the household gathers around food."*
2. **A "X-position walk" foundation section** (5 or 7 positions) with one `<h3>` per position
3. **A "Y-and-Z rule"** — the single most useful rule in this room, named for the two objects it concerns (07-22 = "seating-and-sofa rule", 07-23 = "table-and-chair rule")
4. **A read the foundation articles skip** — a single named technique that fixes most of the other problems (07-22 = "electronics-shelf treatment", 07-23 = "shared-plate line", plus 07-23's "lighting treatment" as a second)
5. **The defects grid** — `posture-grid` div with `<div class="posture-row">` rows: defect name | position number | one-line read
6. **Six deliberate acts** — bulleted, each tied to a specific position or rule
7. **A pullquote** — wraps the lean-into forward-momentum
8. **"What the X read does not cover"** — names the next room in the thread explicitly; this is the **most important paragraph for thread continuity**
9. **Six FAQs** — room-specific (small room, dual-use, missing seat, season rotation, before-vs-after buying, age/multi-member variants)
10. **"What to do this week"** — closes with a one-week + four-week rhythm
11. **A teed-up next article** — the closing paragraph names the next room with a one-clause framing

## Thread-continuity mechanics across indoor articles

The 07-22 article teed up 07-23. The 07-23 article should tee up 07-24. The teed-up sentence in every indoor article's closing paragraph names the next room and what the room's read adds to the thread. Example pattern (verified 07-22 → 07-23):

> *"Tomorrow's article will walk the room that feeds the dining room — the kitchen, the room where the meals are made, the room the household's qi moves through fastest, the room with a different read because the kitchen's rhythm is the rhythm of hands instead of voices."*

The recipe has four parts: (a) the room name, (b) the household activity that defines the room, (c) the qualitative read difference from the prior article, (d) the rhythm signature (hands / voices / minds / bodies — choose a verb noun pair that signals what kind of energy moves through the room).

## Prior-article promised-handoff pattern

Detection signal at the start of every cron run on oriental-destiny:

```bash
tail -10 fate-$(date -d "yesterday" +%Y-%m-%d).html | grep -E "(tomorrow's article|next piece|next read|tomorrow's piece|tomorrow's read)"
```

If matched, the article to write is named in the prior article's closing sentence. Do not re-derive the topic from the seasonal calendar. Writing a different topic after the prior article promised a specific topic breaks the implicit reader contract — the reader who clicked through from yesterday's article expects the named follow-up.

Verified 2026-07-23: the 07-22 Living Room article ended with "Tomorrow's article will walk the room the dragon settles into when the household gathers around food — the dining room." The 07-23 cron run honored this by writing Dining Room Feng Shui with the lead paragraph explicitly closing back on 07-22 ("Yesterday's piece walked the living room..."). Score 95/100, single humanize patch (`highest-leverage` → `highest-impact`), 5,457 words.

## Position-count scaling rule

The 07-22 article's 7-position walk was the foundation. The 07-23 article's 5-position walk was the smaller-room adaptation. Future articles:

- **5 positions**: Dining Room (set), Kitchen, Bathroom, Pantry, Laundry (rooms defined by single activity, ≤30 sq m)
- **7 positions**: Living Room (set), Bedroom, Home Office, Master Suite, Basement (rooms with multiple distinct functional zones, >30 sq m)
- **9 positions** (potential future): combined rooms like open-plan living/dining, family room, loft (rooms that blend two functions)

The position count is not arbitrary — it tracks the number of distinct functional zones in the room. A new indoor article should pick its count before drafting the H2.

## Cross-link pattern in the footer

Every indoor article's footer must list all prior threads, not just the indoor ones. The 07-23 footer chains: Dragon Vein (07-10), Three Gates (07-11), Apartment (07-12), Townhouse (07-13), City Lot (07-14), Day Master (07-15), Chart Branch (07-16), Stairway (07-17), Balcony (07-18), Courtyard (07-19), Side Yard (07-21), Living Room (07-22) = 12 links. Future indoor articles should add themselves to this chain WITHOUT removing the prior links, even as it grows past 14-15 entries.

## Why the indoor-thread template holds

Each indoor article is self-contained (a reader landing on any single article gets a complete picture, with the theory inline). But the thread signals a larger reading experience: each article's last paragraph points to the next, and the reader who follows the thread gets a room-by-room walk through their home with the same vocabulary (the position walk, the defects, the deliberate acts) applied to each room. The repetition of vocabulary across rooms is the thread's signal — the indoor thread teaches the reader to read their own home room-by-room, then the reader gets to apply the same read in the next room on their own.

## Pitfalls specific to indoor articles

1. **Don't repeat the theory from the foundation articles** — the indoor article should reference (not re-derive) the dragon vein, three gates, and the outdoor reads. One sentence per reference is enough.
2. **The "what this room does not cover" section is mandatory** — without it, the article reads as if it's the indoor thread's only article, breaking the serial pattern.
3. **The position count must match the room's complexity** — forcing 7 positions into a small room reads padded; forcing 5 into a large room reads thin.
4. **The FAQ count should be 6, not 8** — oriental-destiny's indoor articles run 6 FAQs (verified 07-22 and 07-23). Foundation articles can run 6-8 FAQs; indoor articles have a tighter profile.
5. **The closing CTA should always link to the chart-side read** — every indoor article closes with a CTA that frames BaZi as the chart-side upgrade to the room-side read. This is the indoor thread's commercial loop.
