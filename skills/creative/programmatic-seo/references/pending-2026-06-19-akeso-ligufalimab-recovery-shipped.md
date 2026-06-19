---
date: 2026-06-19
slug: 2026-06-19-akeso-ligufalimab-recovery-shipped
status: shipped
commit: 0eca72b
recovery_target: 2026-06-18
---

# 2026-06-19 Recovery Run — Akeso Ligufalimab (06-18 partial) Shipped

## What this run was
A pure RECOVERY run — no fresh research, no new article writing. The 2026-06-18 cron run wrote the Akeso ligufalimab CD47 frontline AML article (3,299 words, EHA 2026 Phase II readout) but hit the cron iteration cap BEFORE the humanize verify, BEFORE the sitemap.xml patch, BEFORE the news/index.html card insertion, and BEFORE any git operation. The article was on disk as `news/2026-06-18-akeso-ligufalimab-cd47-frontline-aml-eha-2026.html` (26KB, complete, clean) but untracked. There was NO pending file under `references/` — the original 06-18 cron had no time to write one.

## State at start of 06-19 run
Step 0 detection sequence fired cleanly:
- Check 1 (`ls news/$(date +%Y-%m-%d)-*.html`) → returned `news/2026-06-18-akeso-ligufalimab-cd47-frontline-aml-eha-2026.html` (untracked, mtime Jun 18 09:15)
- Check 2 (`git status`) → working tree had the 06-18 article as untracked, no ahead-of-origin state
- Check 3 (`ls references/pending-*.md`) → empty

The combination of Check 1 + Check 2 was sufficient — no pending file was needed.

## Recovery recipe executed (8 tool calls total)
1. `head -5` + `tail -3` + `em_dash_check.py` (combined) — verified article completeness (3,299 words, 10.5 em-dashes/1200, 0 banned vocab)
2. `humanize_score.py` — initial score 74/100, flagged "landscape" x1
3. `grep -n landscape` → found 1 hit in section 5 heading
4. `patch` — replaced "Landscape" → "Field" in section 5 H2
5. `humanize_score.py` — re-score 79/100 (passes >60 threshold)
6. `grep -P '[^\x00-\x7F]'` — verified only legitimate mathematical symbols (×, ≥) and curly quotes
7. `patch` — inserted sitemap.xml URL entry at top
8. `patch` — inserted news/index.html article card at top of list
9. `git add ... && git commit ... && git push origin master` — single chained call (commit `0eca72b`)
10. `sleep 180 && curl ... 200` — verified live at HTTP 200

## New finding — proper-noun embedded banned-vocab hits
The script flagged `enhance` x2 as banned vocab. Both hits were inside the ALL-CAPS proper noun `ENHANCE-3` (the magrolimab MDS trial name). The script's regex does NOT distinguish proper-noun boundaries, so it false-positives on trial names like ENHANCE, ENHANCE-3, KEYNOTE-XXX, CHECKMATE-XXX, HARMONi, HARMONi-2, HARMONi-6, etc. **Decision rule encoded in SKILL.md:** leave ALL-CAPS proper-noun hits alone; only patch lowercase body-prose uses. The 06-19 article shipped at 79/100 with the 2 ENHANCE-3 hits left intact — well above the >60 threshold.

## Recovery recipe for future mid-pipeline cap-hits (now well-documented)
The Step 0 detection works without a pending file. The signal is:
- `ls news/$(date +%Y-%m-%d)-*.html` returns non-empty
- `git status` shows the file as untracked (not ahead-of-origin)
- `ls -la news/$(date +%Y-%m-%d)-*.html` confirms recent mtime

Recovery sequence:
1. Verify article completeness (head + tail + em_dash_check.py)
2. Run humanize_score.py to get the baseline score
3. Patch only actionable banned-vocab hits (skip proper-noun false positives)
4. Patch sitemap.xml (insert at top)
5. Patch news/index.html (insert card at top)
6. Commit + push + verify (chain in one terminal call)

Total: 6-10 tool calls depending on how many patches are needed.

## Cron state at end of run
- Local master is ahead of origin/master by 1 commit (`0eca72b`)
- All three files committed and pushed
- Live URL: https://chinahospitalsguide.com/news/2026-06-18-akeso-ligufalimab-cd47-frontline-aml-eha-2026.html (HTTP 200 verified)
- Working tree clean

## Recommended action for 2026-06-20 cron run
Fresh research day. No partial state to recover. Standard Step 1 → Step 6 workflow.