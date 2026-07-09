# Pivots and Thread Coherence for Daily SEO Article Threads

Companion to the SKILL.md. Contains the full body of every thread-coherence pattern discovered and verified across the 2026-06 → 2026-07 cron runs on oriental-destiny.com. Use this file as the single source of truth for thread-coherence decisions when planning a daily article; SKILL.md only carries a 1-line pointer to each pattern.

---

## 1. Thread-Promise Fulfillment (NEW — verified 2026-07-09)

**Definition:** when a prior article's BODY text made an explicit date-promised content claim (e.g. "the next article (July 8) walks the dining room. The article after that (July 9) walks the home office."), the next cron run should generally honor that promise unless the promised topic has been covered elsewhere or a stronger reason to pivot exists.

### Verification case (2026-07-09, oriental-destiny Home Office in Earth Month)

The 2026-07-07 hallway article body contained this exact sentence:

> "The thread-continuity reason this article exists: ... the next article (July 8) walks the dining room in Earth Month. The article after that (July 9) walks the home office."

The 2026-07-08 cron run did not ship an article (no file in the repo for that date). On 2026-07-09, the cron run wrote the home-office-in-Earth-Month article even though a home-office article already existed at `fate-2026-06-15.html` (the Fire-Month home office from June). The Fire-Month and Earth-Month home-office reads are genuinely different:

| Aspect | Fire Month (06-15) | Earth Month (07-09) |
|---|---|---|
| Core problem | Focus slipping (could not hold a thought) | Focus refusing to land (five thoughts, no choice) |
| Lamp | Cool-white, near-full brightness | Warm-white, 60-70% dimmer |
| Chair posture | Forward lean (90°, attention-pushing) | Slight back lean (100°, accepting) |
| Monitor height | Above eye level (commanding) | At or below eye level (receiving) |
| Desk surface | Bare, institutional | Two or three personal objects, inhabited |

So the thread-promise article was substantively new, not duplicative.

### Decision rule (4 levels)

1. **Honor verbatim** when the promised topic has NOT been written for the current season (seasonal-angle distinction makes it new) AND no other open thread is more urgent (solar-term landing day, emergency SEO batch, recovery from a cap-hit).

2. **Pivot to a different topic** if (a) the promised topic has a fresh article in the same season (<7 days old); (b) the seasonal angle is genuinely redundant; or (c) a stronger signal overrides the promise — sibling-subagent pending file, recovery state from Step 0, date-promised solar-term eve article, etc.

3. **Acknowledge the substitution** in the new article's lead paragraph when pivoting away from a promise. A silently dropped promise looks like a missed deliverable. Example: "The July 7 hallway article planned today's slot for the dining room; this article pivots to stairs because [reason]..." The reader who read the prior thread should understand why the substitution happened.

4. **Add a forward-link in the new article** back to the prior article that made the promise, so the thread-coherence signal travels both directions. Verify after `write_file`:

   ```bash
   grep -E "fate-YYYY-MM-DD" new_article.html
   ```

A thread promise that the new article doesn't link back to breaks the in-thread navigation contract.

### Inverse relationship

This is the inverse of "Referenced-but-never-covered pivot" (#4 below): that pattern uses prior references to PICK a new topic; this one uses prior body text to OBLIGATE a specific topic and date. Both are valid thread-coherence signals.

---

## 2. Seasonal Content Threading (verified 2026-06-16, extended 2026-06-17)

When the content calendar calls for a month-long theme (June 2026 = Fire Month / Summer), thread the daily articles through distinct sub-topics in a stable order so the series reads as a deliberate walk, not a random shuffle.

### Verified June 2026 sequence

- 06-10: Center of home (Earth sector — sets the element-of-the-month stage)
- 06-11: Bing Day Master (Yang Fire chart primer — chart-side foundation)
- 06-12: Xia Zhi (Summer Solstice — solar-term anchor)
- 06-13: Ming Tang in Summer (Entryway — first room)
- 06-14: Bedroom Fire Month (second room)
- 06-15: Home Office Fire Month (third room)
- 06-16: Kitchen Fire Month (fourth room)
- 06-17: Living Room Fire Month (fifth room — completes the major-room walk)

### Thread-pattern rules

- Anchor pieces (solar terms, day-master explainers) at the start of the month.
- Then a room-by-room walk through the home, each one referencing the season's element in a way that connects to the previous day's article implicitly (bedroom handles the body's night, home office handles the day's focus, kitchen handles the cook's evening, living room handles the family gathering).
- The reader who lands on any one article gets the full recommendation; the reader who reads the series gets a coherent seasonal practice.
- The `article_topics.md` content calendar gives the umbrella theme (June = Summer Feng Shui / Fire Element / Energy Activation). The room-by-room thread is the cron agent's job to plan at the start of each month.

---

## 3. Room Walk Completion Milestone (verified 2026-06-17, extended 06-18, 06-19)

After the fifth major room (Living Room), the room-by-room thread is complete for the Fire Month. The next article (06-18+) should pivot to a different sub-thread:

- (a) A classical feng shui concept that hasn't been written yet (Flying Star, Bagua, annual flying stars) — check with `ls *.html | grep -i KEYWORD` for zero hits.
- (b) An element-transition article (Earth/Metal element preview as the next month approaches).
- (c) A chart-side seasonal topic that deepens the BaZi angle (Ding Day Master was covered in 06-07; consider Wu/Yang Earth chart in summer, or a Fire-heavy chart's summer reading).

### Verified pivot execution (2026-06-18)

Option (a) won — wrote the first-ever Annual Flying Stars 2026 article. The bridge sentence ("The room walk I have been doing all month... the Flying Stars tell you which room is loud this year, the room walk tells you what to do once you walk in") re-anchors the prior thread and frames the new thread as a complement, not a replacement.

---

## 4. Referenced-but-Never-Covered Pivot (verified 2026-06-19, reconfirmed 2026-06-26)

After the first pivot lands, mine the just-published article for terms that were REFERENCED but never given their own pillar piece (e.g. "the Compass school", "the luo pan", "He Tu / Fu Xi diagrams", "the 28 lunar mansions", "yin and yang", "five elements").

```bash
grep -lE "(TERM)" *.html
```

If 0 standalone matches but ≥1 match inside another article's body, that term is a "referenced-but-never-covered" pivot target. The article then naturally links back to the article that referenced it, with a seasonal bridge giving the timing ("two days before Xia Zhi", "the autumn checkpoint before Li Qiu").

### Thread-continuity bridge sentence pattern (verified 2026-06-26)

The lead paragraph explicitly references the prior articles in the thread (e.g. "Earlier this month the Fire Month articles leaned on the word 'yang' without ever defining it, and the wealth corner piece from two days ago leaned on the word 'yin' the same way") — re-anchors the prior thread, signals series coherence, gives the article a reason to exist.

*(Full thread-continuity pattern, including the outdoor-room walk (07-01 → 07-04) and the "Fu Wei ladder" framing, lives in `references/outdoor-room-walk-thread.md`.)*

---

## 5. Narrow-Window Eve Piece (verified 2026-07-06)

When the close-out checklist lands within ~48 hours of a solar term, write one more article that narrows to the single evening before the term (the 16-hour window from sunset to dawn).

The article covers:
- What stays out
- What comes inside before bed
- What to leave lit after dark
- What to watch for at dawn
- Per-chart "candle-and-porch-light" recommendation that changes the setup for each Day Master

Verified on oriental-destiny 2026-07-06 (Li Qiu Eve, 3,891 words, score 95/100, 10 tool calls). Full pattern, CSS, and bridge-sentence recipe in `references/narrow-window-eve-piece.md`.

---

## 6. Thread Close-Out Checklist (verified 2026-06-30)

When a month-long themed thread is on its final day (e.g. June 30, the last day before July's Earth Month begins at Li Qiu on July 7), write a checklist that:

1. Applies the most-recent foundational concept (the Sheng Qi / Ke cycles from 06-29) to a concrete room-by-room or step-by-step walkthrough the reader can do TODAY.
2. Names the next solar-term checkpoint by name + date (Li Qiu on July 7) and what the seasonal polarity shift means for the cures chosen in this month.
3. Includes an explicit "the undo is part of the practice" rule — cures that helped this month become wrong cures next month; the close-out is the moment to swap them. This is the section listicles skip, and it's the one that prevents the homeowner from blaming the cycles when their new-season room feels off.
4. Uses inline cycle tags (Sheng/Ke/Neither colored badges) on checklist items so the reader can read the room-side diagnosis at a glance without re-reading the theory article.

### Why this works as the last piece in a thread

The room walk (06-13 → 06-17) established diagnosis, the foundational concept (06-29) established theory, the close-out checklist (06-30) shows the reader doing the practice with the cycles in hand. Each article carries enough theory to be standalone; reading the thread gives the progression.

### When NOT to use this pattern

When the thread isn't on a clean month boundary, skip it. The close-out checklist only works when the next solar-term shift is within ~7 days. For a mid-month thread that runs 3-5 articles without a solar-term handoff, use a regular pivot (referenced-but-never-covered or room-walk completion), not a close-out.

---

## 7. Pattern selection decision tree

```
Is the prior article's body promising a specific topic for today's date?
├── YES → Thread-promise fulfillment (#1)
│   ├── Already covered in current season (<7 days old)?
│   │   ├── YES → Pivot and acknowledge in lead
│   │   └── NO → Honor verbatim
│   └── Stronger recovery/pivot signal exists?
│       ├── YES → Override the promise, document why
│       └── NO → Honor verbatim
└── NO → Continue down the tree
    ├── Thread is on a month boundary, next solar term within ~7 days?
    │   ├── YES → Close-out checklist (#6)
    │   └── NO → Continue
    ├── Just completed a major room walk (5+ rooms)?
    │   └── YES → Room-walk completion pivot (#3)
    │       ├── Classical concept not yet covered?
    │       │   └── YES → Flying Star / Bagua / etc.
    │       └── Continue to next branch
    ├── Prior article referenced a term that has no standalone pillar?
    │   └── YES → Referenced-but-never-covered pivot (#4)
    └── Solar term landing in ~48 hours, no narrow-window piece yet?
        └── YES → Narrow-window eve piece (#5)
```

Use this tree at the planning step of any cron run, before topic selection. It captures every verified pivot and ensures the daily article fits into an existing thread rather than starting a fresh one.
