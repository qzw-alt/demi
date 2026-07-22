# Outdoor-to-Indoor Thread Pivot (verified 2026-07-22, oriental-destiny.com)

## The pattern

After the outdoor 5-gate property scan completes (Stairway → Balcony → Courtyard → Side Yard, plus the foundational Dragon Vein + Three Gates + property-type trifecta), the natural pivot is to start an **indoor-room walk thread**. The outdoor thread walked the dragon from the sidewalk to the back gate; the indoor thread walks the dragon from the back door to the room the household settles into.

The two threads are not parallel — the indoor thread is the **continuation** of the outdoor thread. The outdoor thread ended at the back gate; the indoor thread starts at the door the household uses to enter from that back gate. The bridge sentence in the first indoor-thread article should reference the outdoor thread explicitly and frame the indoor thread as the settling-volume read the outdoor thread walked toward without naming.

## Reference run: 2026-07-22 Living Room (oriental-destiny.com)

**Article**: "Living Room Feng Shui: Reading the Center of the Home After the Outdoor Walk"
**Word count**: 5,528
**Score**: 95/100 (after 2 `actually` body-prose patches, first pass was 79 — a 16-point swing, exactly matching the 06-22 + 06-25 rule)
**Tool calls**: 10
**Reference**: `fate-2026-07-22.html`

### Tool-call breakdown (the reference recipe)

1. `terminal` — `ls fate-2026-07-22-*.html 2>/dev/null; git status; git remote -v; git config user.email/name` (combined) — clean tree, SSH remote, identity set in same call
2. `read_file` — `article_topics.md` (July = Outdoor Feng Shui, August = Back to School / Study Areas)
3. `terminal` — for-loop grep of room-name anchors (`Living Room`, `Dining Room`, `Entryway`, `Hallway`, `Door`, `Window`, `Garage`, `Basement`, `Attic`, `Closet`) across `fate-2026-07-*.html` — surfaces the indoor-room coverage gap in one call
4. `read_file` — `terminology_mapping.md` (confirms Living Room as highest-searched feng shui room)
5. `read_file` — `fate-2026-07-21.html` (offset 1-120) — voice + scaffolding reference (NOT the bare template, per the 06-16 pitfall)
6. `terminal` — verify Living Room is 0 dedicated articles + check sitemap top entry
7. `write_file` — `fate-2026-07-22.html` — the article (5,528 words, 7 positions walk + seating-and-sofa rule + electronics-shelf treatment + 7-defect posture grid + 6 deliberate acts + 7 FAQs)
8. `terminal` — `python3 scripts/humanize_score.py …` (first pass 79/100, 2 `actually` body hits)
9. `patch` × 2 — removed `actually` from 2 body-prose sentences (lifted score 79 → 95)
10. `terminal` — sitemap patch (3-line context anchor per 06-29 pattern) + `git add && commit && git push origin main && sleep 150 && curl --max-time 30 ...` (chained) — HTTP 200 verified

### Article structure (verified at 5,528 words)

The indoor-room article structure differs from the outdoor-gate article structure in three ways:

1. **Seven-position walk** (not five-position) — indoor rooms have 7 jobs (doorway side, settle wall, seating cluster, TV wall, shelving wall, path, windows), outdoor gates have 3-5 jobs (entry, climb, pause, settle, daily-cross). The number rises because indoor rooms are settling volumes with more simultaneous functions than gates are transit lines with one function.

2. **Posture-grid callout** (not corner-callout) — the seven defects are best displayed as a table with three columns (defect name, position number, what it looks like). The corner-callout format that worked for the outdoor gates is too compressed for seven defects.

3. **Deliberate acts in numbered weekly cadence** (one act per week for 6 weeks) — indoor reads are slower-paced than outdoor reads because indoor rooms are larger and have more to edit. The 1-act-per-week cadence gives the homeowner permission to do the read over a season rather than a weekend.

### Bridge sentence pattern (verified)

The first indoor-thread article's lead paragraph should reference the outdoor thread explicitly with a "the outdoor thread walked toward X without naming" construction. The 07-22 version:

> The July outdoor thread walked the dragon from the sidewalk to the back gate, gate by gate, room by room, five different reads over five articles. Today's piece walks the room the dragon settles into when it comes inside — the living room, the Ming Tang's larger cousin, the room that holds the household for the most hours per day.

This is the same bridge pattern the 06-18 + 06-19 + 06-26 articles used for within-thread pivots (Flying Stars, Five Elements cycles, yin/yang), but applied to a thread-boundary pivot (outdoor → indoor). The bridge does two jobs: re-anchors the prior thread (so a reader landing on the indoor article from search knows the outdoor thread exists) AND signals series coherence (so a reader walking the thread gets the progression).

### Indoor-room sequencing (the next 5 articles after 07-22)

Following the same room-by-room walk pattern the outdoor thread used:

| Day | Article | Reason |
|-----|---------|--------|
| 07-22 | Living Room | The settling volume, highest-searched indoor room, gateway into indoor thread |
| 07-23 | Dining Room | Where the household gathers 3× per day around food |
| 07-24 | Kitchen | The cook's room, ties back to June Fire-Month kitchen article |
| 07-25 | Bedroom | The night-settling volume, pairs with August Study Areas transition |
| 07-26 | Study / Home Office | August theme anchor (Back to School / Study Areas) |

The kitchen article should reference the June 06-15 Fire-Month kitchen article to maintain thread continuity across the summer. The bedroom article should be the longest of the five (3,500-4,500 words) because the bedroom has more feng shui positions than the other rooms (sleeping direction, mattress position, mirror rules, electronics, bedside tables, closet door).

## When to use this pattern vs alternatives

Use the **outdoor-to-indoor pivot** when:
- The outdoor 5-gate scan is complete (Dragon Vein + Three Gates + property-type trifecta + Stairway + Balcony + Courtyard + Side Yard all shipped)
- The current month's content calendar is Outdoor Feng Shui (July) or close to a month-boundary
- The next month's theme (August = Back to School / Study Areas) can be naturally threaded into indoor rooms

Use a **referenced-but-never-covered pivot** instead when:
- The outdoor thread is still in progress (don't pivot mid-thread)
- A specific indoor concept was referenced multiple times across the outdoor thread (e.g. "Ming Tang" was referenced in 5+ outdoor articles — its own pillar piece would be a within-indoor-thread pivot candidate)

Use a **solar-term close-out checklist** instead when:
- The thread is on a clean month boundary AND the next solar-term shift is within ~7 days (not the case for 07-22; Li Qiu is July 7, already passed, and Chushu is not until late August)

## Pitfalls specific to indoor-thread starts

**1. Don't pick the lowest-hanging indoor room first (Entryway) — pick the highest-searched (Living Room).** The Entryway was already covered as the Ming Tang article in June (06-13). The Living Room is the highest-searched indoor feng shui room per `terminology_mapping.md` and the most underrepresented pillar. Picking the highest-searched unfilled room first maximizes SEO value of the pivot.

**2. The indoor-room article should NOT include a new solar-term or BaZi chart bridge.** The outdoor thread used chart-side reads (07-15 Day Master, 07-16 Chart Branch) as in-thread additions to the foundational outdoor reads. The indoor thread should stay room-side for the first 2-3 articles, then weave the chart-side back in around article 3-4 of the indoor thread (after the homeowner has the room-side framework in hand and can absorb the chart overlay).

**3. The first indoor-thread article's word count should be at the 5,000+ ceiling, not the 2,500-3,000 typical for the site.** The Living Room read needed 5,500 words because the seven-position walk, the seating-and-sofa rule, the electronics-shelf treatment, the seven-defect posture grid, and the six weekly deliberate acts are all load-bearing for the indoor thread to start on. Subsequent indoor-thread articles can return to the 3,000-3,500 word range once the framework is established.

**4. The indoor-room article should reference the outdoor thread ONCE in the lead and ONCE in the closing, not throughout.** The bridge is the article's reason to exist; repeated outdoor-thread references throughout the body dilute the indoor read. The 07-22 article references the outdoor thread in the lead paragraph and in the closing "What to do this week" paragraph; the body stays indoor-focused.