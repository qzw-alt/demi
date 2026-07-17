# Vertical-Gate Discovery Pattern (verified 2026-07-17)

Use this recipe when orientaldestiny.com's daily cron needs an uncovered room-level pillar for the July (or other month) thread.

## Why this pattern exists

The July thread walks property-types horizontally (apartment → townhouse → city lot → Day Master overlay → chart branch overlay) and room-by-room vertically (stairway, hallway, entryway, landing, mailbox). Each thread day needs a topic. After 5-10 days of cron, most obvious topics have been covered. The remaining uncovered rooms are exactly the vertical-gate and room-level pillars that a single grep call can surface.

## The discovery recipe (1 terminal call)

```bash
cd /home/ubuntu/oriental-destiny && grep -lE "(Staircase Feng Shui|Stairway Feng Shui|Stairs Feng Shui|Stair Feng Shui|Landing Feng Shui)" *.html 2>/dev/null
echo "---STAIRS---"
grep -lE "(Mailbox Feng Shui|Letters Feng Shui|Postbox Feng Shui)" *.html 2>/dev/null
echo "---MAILBOX---"
grep -lE "(Garage Feng Shui|Carport Feng Shui|Entryway Feng Shui|Foyer Feng Shui|Hallway Feng Shui)" *.html 2>/dev/null
echo "---GARAGE/ENTRY---"
grep -lE "(Window Feng Shui|Windowsill Feng Shui|Doorplate Feng Shui|Doorknob Feng Shui)" *.html 2>/dev/null
```

Zero matches across the targeted regex = uncovered pillar candidate. Specifically:

| Topic slug | Detection regex | Status as of 2026-07-17 |
|---|---|---|
| Stairway Feng Shui | `(Staircase\|Stairway\|Stairs \|Stair )` | **Uncovered** before 2026-07-17, covered after |
| Mailbox Feng Shui | `(Mailbox\|Letters\|Postbox)` | Tangential-only matches (2 hits in unrelated articles) |
| Garage / Carport Feng Shui | `(Garage\|Carport)` | Tangential-only matches |
| Window / Windowsill Feng Shui | `(Window Feng Shui\|Windowsill)` | Tangential-only matches |

## Why "vertical gate" is a viable pillar

A vertical gate (stairway, stairwell, stair landing) bridges the property-type reads (which are ground-floor-only) and the room reads (which are single-room). The stairway is the door between floors, the line the dragon vein takes when the property has more than one story, and the missed-gate in most horizontal property reads. Articles that reference but never dedicate a pillar to a vertical gate (e.g. prior hallway, gates, city lot articles mention stairways as one-line examples) are good next-day targets.

## When this pattern does NOT apply

If the article corpus already has 50+ cron-published articles (high churn rate) and obvious topics are exhausted:
- Pivot to the **referenced-but-never-covered pattern** (find terms referenced inside other articles' body prose that have no dedicated pillar)
- Pivot to a **solar-term anchor** (write one article on the eve / day / week-of an upcoming solar term — 2026 calendar includes Li Qiu on July 7, Bai Lu on September 7, etc.)

The referenced-but-never-covered recipe (already documented in the parent SKILL.md): `grep -lE "(TERM)" *.html` — 0 standalone matches + 1+ in-body matches = clean pivot target.

## Quality bar

The chosen topic must pass:
1. Zero existing dedicated articles (grep returns empty for the Primary Keyword regex)
2. Reference-able from at least 2 prior articles (so the new article can anchor to the thread via the footer cross-link sequence)
3. Match the month's content calendar (July = Outdoor Feng Shui, room-level pillars OK because the property-type base was just established)
4. Allow a real 30-60 minute home walkthrough (avoid purely abstract topics that have no property read)
5. Pass the keyword template HARD RULE (`[X Feng Shui]: [Hook] | Oriental Destiny` — see `references/oriental-destiny-keyword-template.md`)

Verified on 2026-07-17 with `Stairway Feng Shui: Reading the Vertical Line Between Floors` — 4,774 words, 95/100 humanize, shipped in 9 tool calls.
