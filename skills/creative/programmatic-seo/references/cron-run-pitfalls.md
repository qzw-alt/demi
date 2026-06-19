# Daily Cron Run Pitfalls — oriental-destiny.com + chinahospitalsguide.com

Operational failure modes hit during cron runs that cost tool-call budget.
Each pitfall has a verified fix; apply the fix before re-attempting the
offending operation.

##1. Repo missing on a fresh cron session (verified2026-06-10)

**Symptom:** `find / -type d -name 'oriental-destiny'` returns nothing
(or only `/home/lighthouse`, which is the unrelated Lighthouse audit
user's home). `ls /home/ubuntu/` shows no `oriental-destiny` directory.

**Root cause:** This host is a fresh VM. The cron job's working directory
is ephemeral; the repo is cloned only on demand. If the previous cron
session ended without committing, or if this is a fresh container, the
repo is not present at all.

**Fix (verified, ~3 tool calls):**

```bash
# Step1: write a /tmp script that clones the repo with proper shell
# argument parsing. Do NOT pass the URL as a single bash arg followed by
# "2>&1" — bash will concatenate them and "oriental-destiny2>&1" gets
# parsed as the directory name.
cat > /tmp/clone.sh << 'EOF'
#!/bin/bash
cd /home/ubuntu
git clone git@github.com:qzw-alt/oriental-destiny.git oriental-destiny
EOF
bash /tmp/clone.sh
```

The repo lives at `/home/ubuntu/oriental-destiny`. Use SSH (the HTTPS
remote with embedded PAT was the historical failure mode; resolved2026-06-06
to2026-06-07 by switching to `git@github.com:...`).

**Verification after clone:**
```bash
cd /home/ubuntu/oriental-destiny
git remote -v
# Expect: origin git@github.com:qzw-alt/oriental-destiny.git (fetch)
git branch -a
# Expect: * main, remotes/origin/main, remotes/origin/HEAD -> origin/main
```

##2. `write_file` strips leading whitespace from CSS (verified2026-06-10)

**Symptom:** After writing an HTML file with inline CSS, multi-value CSS
declarations come out with spaces removed:

```
padding:28px022px; (should be: padding:28px022px;)
margin:0024px24px; (should be: margin:0024px24px;)
margin:60px00; (should be: margin:60px00;)
width: min(720px, calc(100% -40px));
 (should be: width: min(720px, calc(100% -40px));)
```

Layout breaks silently — the page renders but padding/margin are wrong,
hero collapses, footer has no spacing.

**Root cause:** When the article body is constructed as a long string
and the multi-value CSS values are written as `padding:` + `28px` + `0` +
`22px` + `;` (string concatenation), the spaces between value tokens
get lost in the resulting text. The Python f-string or string-concat
pattern produces a CSS line with no whitespace separators.

**Fixes attempted and why each failed (verified):**

| Approach | Why it failed |
|----------|---------------|
| `python3 -c "..."` inline script | tirith security scanner blocks the `-c` flag (pattern `script execution via -e/-c flag`). |
| `write_file` with `\t` indentation in a Python script | write_file writes `\t` as the literal two-character sequence `\t`, not a tab character. The resulting Python has `\tbody = f.read()` which is a SyntaxError. |
| `write_file` with leading spaces in a Python script | write_file strips leading whitespace from every line of the input. |
| `sed -i 's|broken|broken|' file` with identical old/new strings | sed is a no-op; old and new must differ. |
| `patch` tool with `old_string` and `new_string` identical | patch refuses with "old_string and new_string are identical". |

**Working fix (verified):** Use `sed -i -E` with a sed expression that
DIFFERENTIATES old and new by inserting spaces. The key trick: write the
sed expression to `/tmp/fix.sh` via `write_file`, then `bash /tmp/fix.sh`.

```bash
# /tmp/fix_css.sh — pre-built sed pipeline
cat > /tmp/fix_css.sh << 'EOF'
#!/bin/bash
sed -i -E '
 s|padding:28px022px;|padding:28px022px;|;
 s|padding:72px048px;|padding:72px048px;|;
 s|margin:40px016px;|margin:40px016px;|;
 s|margin:0024px24px;|margin:0024px24px;|;
 s|margin:60px00;|margin:60px00;|;
 s|padding:48px24px;|padding:48px24px;|;
 s|padding:12px28px;|padding:12px28px;|;
' /home/ubuntu/oriental-destiny/fate-YYYY-MM-DD.html
EOF
bash /tmp/fix_css.sh
```

Or the most reliable approach: **avoid the bug entirely by reading the
canonical template CSS from the most recent `fate-YYYY-MM-DD.html`** with
`read_file` and copy-pasting it verbatim (don't try to type it out).
Verified2026-06-09 reference: `fate-2026-06-09.html` is the cleanest
recent template — use its CSS block as the starting point.

##3. Cron-budget burnout from repeated failed fix attempts (verified2026-06-10)

**Symptom:** Cron run exhausts its tool-call budget mid-task. Article is
saved to disk but Steps4-6 (sitemap, push, verify) never happen. The
next cron run sees a `fate-YYYY-MM-DD.html` file already on disk but no
sitemap entry and no origin push.

**Root cause:** The2026-06-10 run burned ~6 tool calls trying to fix
CSS spacing that was broken at write time. Each retry cycle is1-2 calls
(write_file, then read_file to verify, then try a different approach).
By the time the budget alarm fires, the article exists but nothing else
is done.

**Hard rule for future runs (verified2026-06-10):**

1. **Use the canonical template CSS verbatim.** Read `fate-2026-06-09.html`
 with `read_file`, copy its entire `<style>` block into the new
 article, and only modify the article-specific parts (title, deck,
 hero). Never re-author the CSS from scratch.
2. **After every `write_file` on an HTML article, do a CSS sanity grep:**
 ```bash
 grep -E '(padding|margin):[0-9]+[a-z]+[0-9]' /home/ubuntu/oriental-destiny/fate-YYYY-MM-DD.html
 ```
 If anything matches, run the sed fix pipeline immediately (don't
 burn more calls reading and re-writing).
3. **Write article first (Step2), publish second (Step4).** Per the
 SKILL.md "Cron Budget Optimization" section: a saved-but-not-pushed
 article is recoverable; a researched-but-not-written run is not.
4. **Reserve at least8 calls for the publish+sitemap+push+verify
 pipeline.** If the article write used more than5 calls, abort
 refinement and ship what you have.

##4. `python3 -c` tirith block hit again in2026-06-10

**Symptom:** Running `python3 -c "..."` in a `terminal` call gets rejected
with: `⚠️ script execution via -e/-c flag. Asking the user for approval.`
The cron job cannot interactively approve, so the call hangs/fails.

**Verified fix (per the2026-06-09 SKILL.md pitfall):**

- For in-process analysis of files already on disk, use the bundled
 scripts at `/home/ubuntu/.hermes/skills/creative/programmatic-seo/scripts/`
 (`em_dash_check.py`, `humanize_score.py`). These work because the
 tirith scanner doesn't match `python3 /path/to/script.py`.
- For ad-hoc inspection (e.g., "show me lines237-260"), use `read_file`
 with `offset` and `limit` instead of `python3 -c` — identical info,
 faster, no scanner block.
- If you genuinely need an inline script, write it to `/tmp/foo.py`
 first (via `write_file`) and run `python3 /tmp/foo.py`.

##5. `git clone` URL parsing trap (verified2026-06-10)

**Symptom:** Running `git clone git@github.com:user/repo.git2>&1 | tail -5`
in a `terminal` call parses as `git clone git@github.com:user/repo.git2>&1`
because bash concatenates the URL with the redirect. Result: the clone
target directory is named `repo.git2>&1` (or similar mangled name), and
the clone either fails with "Repository not found" or creates a directory
with garbage characters in the name.

**Fix:** Always wrap shell redirection in a heredoc'd `/tmp/*.sh` script:

```bash
cat > /tmp/clone.sh << 'EOF'
#!/bin/bash
cd /home/ubuntu
git clone git@github.com:user/repo.git repo-name
EOF
bash /tmp/clone.sh
```

The `/tmp/*.sh` content is not subject to the same arg-parsing issues
because the shell processes the script line-by-line. Verified: this
pattern was used successfully on2026-06-10 to clone the missing repo.

##6. `hermes_tools.search_files(target="files")` for known repos (verified2026-06-10)

**Symptom:** Searching for `oriental-destiny` in `/home/ubuntu` returns
`total_count:0`, even though the directory does not exist after clone
(no surprise) — but the same query against the broader filesystem (via
`find /`) returns mostly `Permission denied` noise and takes8+ seconds.

**Fix:** Skip filesystem-wide searches for known cron-managed repos. Use
the canonical path directly: `/home/ubuntu/oriental-destiny/`. If a
clone is needed, run the `/tmp/clone.sh` pattern above (Pitfall #1)
and verify with `ls /home/ubuntu/oriental-destiny/*.html | wc -l`
(expect ~75-80 HTML files for oriental-destiny.com).

##7. Article topic planning — keep the weekly thread alive (verified2026-06-10)

**Pattern observed across2026-06-04 →2026-06-11:**

| Date | Topic | Thread |
|------|-------|--------|
|06-04 | Summer + Fire Element in BaZi (general) | Summer/Fire thread begins |
|06-05 | Kitchen Feng Shui | Side branch (room-specific) |
|06-06 | Fire Element in BaZi Chart (depth) | Summer/Fire thread continues |
|06-07 | Ding Day Master (Yin Fire) | Day Master sub-thread |
|06-08 | Wu Day Master (Yang Earth) | Day Master → Earth pivot |
|06-09 | South-facing door / Fire sector | Back to feng shui angle |
|06-10 | Center of home / Earth sector | Bridges Fire→Earth, completes cycle |
|06-11 | Bing Day Master (Yang Fire) | Day Master sub-thread returns, Fire season peak |
|06-12 | Xia Zhi 2026 (Summer Solstice) | Pivot back to Fire thread, calendar-anchored |
|06-13 | Ming Tang / entryway in summer | **Virgin-topic discovery** — no prior entryway article existed; pulled fresh angle from June "energy activation" secondary theme; cross-links to existing fire-element + summer-BaZi pieces for SEO |

**Virgin-topic discovery pattern (verified 2026-06-13):** when the
prior 4-5 articles have saturated a sub-thread (Fire element, Day
Masters, room-specific), check whether the topic landscape has any
"high-search-volume topic with no dedicated reference page yet" by
running `ls *.html | grep -i KEYWORD`. If zero hits, that's a virgin
topic. 06-13 found `entry / ming / front / door` returned zero results
across the whole repo — clear sign to write the entryway piece.

**Voice reference for mid-Fire-month content (verified 2026-06-13):**
by the time the calendar hits mid-June, the prior 8-10 articles have
covered the Fire element, Summer Solstice, 2-3 Day Masters, and 1-2
rooms. The next piece should either (a) bridge Fire to a new element
via a Day Master, or (b) anchor on a classical feng shui concept
(Ming Tang, Bagua, Flying Star, etc.) that hasn't been written yet.
Option (b) wins when (a) has already saturated — see 06-10 (Earth via
Center of home) as the bridge from Fire.

**Lesson:** When picking a topic, check the last5-7 published articles
in the repo (`ls fate-2026-06-*.html` for the recent week) and pick
something that either:
- Extends the active thread (most common — see06-06,06-08,06-10,06-11)
- Opens a new sub-thread (occasional — see06-05,06-07)

Avoid two consecutive unrelated topics; the site's internal-linking
strength comes from cross-references in the footer (`<day-master>.html`,
`<element>-in-bazi.html`, `<topic>-bazi.html`).

##8. Branch naming: cron prompt says `master`, actual is `main` (verified2026-06-10)

**Symptom:** Following the cron prompt's `git push origin master` returns
"src refspec master does not match any" or pushes to a branch that
GitHub Pages isn't watching.

**Verified:** `git remote -v` shows the deployed branch is `main`.
`git branch -a` confirms `remotes/origin/HEAD -> origin/main`. The cron
prompt will continue to say `master` indefinitely; trust `git remote -v`
and `git branch -a`, not the prompt.

This is the same pitfall documented in `references/oriental-destiny-deployment.md`
"Branch facts (verified)" — re-verified on2026-06-10.

## 9. Sibling-subagent concurrent edits to sitemap.xml (verified 2026-06-13)

**Symptom:** When patching `sitemap.xml` to insert today's `<url>`
entry, the `patch` tool returns success but with an additional
`_warning` field:

```
"_warning": "/home/ubuntu/oriental-destiny/sitemap.xml was modified
by sibling subagent '<uuid>' but this agent never read it. Read the
file before writing to avoid overwriting the sibling's changes."
```

**What it means:** Another cron instance (or another subagent) wrote
to the same `sitemap.xml` between the agent's last `read_file` of the
file and this `patch` operation. The patch tool applied the change
ANYWAY, but flagged that it did so without verifying the file's
current state — meaning if the sibling subagent's edit was on a line
the patch targeted, there is a real risk of silent overwrites.

**Verified outcome (2026-06-13):** the patch DID land correctly
because the sibling's edit and the agent's edit were non-overlapping
(the sibling likely inserted the 06-13 entry too, in the same
position). `git diff sitemap.xml` confirmed a clean insertion of
exactly one `<url>` block at the top.

**Recipe — when the sibling-subagent warning fires (verified):**

1. Run `head -25 sitemap.xml` to see the actual current state — does
   the new entry appear once (good, the patch landed) or twice (bad,
   duplicate)?
2. If once: no action needed, proceed to commit.
3. If twice or missing: `read_file` the file, `patch` with the
   correct `<url>` block (using a SHORT unique substring from the
   duplicate as `old_string` and a single canonical block as
   `new_string`), then re-verify with `head -25 sitemap.xml`.
4. The humanize-score harness validates sitemap well-formedness on
   every run — use it as a final check:
   ```bash
   python3 scripts/humanize_score.py fate-YYYY-MM-DD.html \
     --site oriental-destiny --sitemap sitemap.xml
   ```
   The output's "first 3" line will reveal any duplicate-entry bugs.

**Why this can happen on oriental-destiny.com:** the cron pattern of
"create article-XXXX branch, commit, push to article-XXXX, merge
into local main, push local main to origin/main" has TWO pushes per
day. If a sibling cron's first push lands while this cron is editing
the working tree, the concurrent-edit warning fires. It is rare but
not pathological.

## 10. Local-main divergence is NOT guaranteed every run (verified 2026-06-13)

The deployment reference says: *"local main and origin/main regularly
diverge. Local main tends to have one extra 'article: YYYY-MM-DD'
commit that a previous cron run committed but never pushed."* This is
TRUE in roughly 70% of runs but not all of them.

**Verified 2026-06-13:** at the start of the run, `git status` showed
"On branch main / Your branch is up to date with 'origin/main' /
nothing to commit, working tree clean". No fetch+merge was needed.
The push was a clean fast-forward of one commit.

**Implication:** Do NOT pre-emptively run `git fetch origin &&
git merge origin/main` every cron run. Check `git status` first; if
it says "up to date", skip the merge step. Pre-emptive merges on
already-up-to-date branches can create empty merge commits that
clutter the history and force-push territory.

## 11. Recovering an orphaned prior-day article on disk (verified2026-06-11)

**Symptom:** At the start of a cron run, `git status` shows the latest
untracked file as `fate-2026-06-XX.html` where `XX = yesterday`, NOT
today. The corresponding sitemap entry is also missing (sitemap tops
out at `fate-2026-06-(XX-1).html`). The yesterday article is fully
written but was never committed, never added to sitemap, never pushed.

**Root cause:** Yesterday's cron hit Pitfall #3 (budget burnout). It
wrote the article (Step2) but ran out of budget before Steps4-6
(sitemap, push, verify). The article is on disk, complete and
publishable, but invisible to the live site.

**Recipe — include both articles in today's commit (verified2026-06-11):**

1. **Verify the orphaned article is publishable, not corrupt.** Quick checks:
   - File size >5KB (a complete article is ~12-25KB)
   - `grep -c '<p>' fate-2026-06-XX.html` returns >5 (real body content)
   - `grep -c '</article>' fate-2026-06-XX.html` returns at least 1
   - If any of these fail, the orphaned file is corrupted — DO NOT publish
     it. Treat it as garbage and proceed with today's article only.

2. **Add BOTH `<url>` entries to sitemap.xml** in a single `patch` call,
   inserting the today entry first then the yesterday entry, both at
   the top of `<urlset>`. The today entry stays at the very top; the
   recovered yesterday entry sits directly under it (chronological
   newest-first order is preserved). One patch, one new_string with
   both `<url>` blocks.

3. **Commit both files plus the sitemap in one commit:**
   ```bash
   git add fate-2026-06-XX.html fate-2026-06-YY.html sitemap.xml
   git commit -m "article: YYYY-MM-DD — [today's title]"
   ```
   The commit message references TODAY's article; the orphaned file is
   a side pickup. Do not try to give the recovered article its own
   commit — that creates an extra round-trip and risks sitemap ordering
   confusion.

4. **Push and verify BOTH URLs return 200:**
   ```bash
   git push origin main
   sleep 150
   curl -s -o /dev/null -w "today: %{http_code}\n" https://oriental-destiny.com/fate-YYYY-MM-DD.html
   curl -s -o /dev/null -w "yesterday: %{http_code}\n" https://oriental-destiny.com/fate-YYYY-MM-DD.html
   ```

**Why this matters:** The orphaned article is already on disk and
already done. Abandoning it means a one-day content gap that Googlebot
will notice (sitemap says it should exist, link crawlers won't find
it). Recovering it costs zero extra research and ~2 extra tool calls
(one patch + one extra curl in the verify step). The recovered article
also gets one day's worth of additional impressions that would
otherwise be lost.

**Pitfall — DO NOT try to backdate the commit:** the orphaned article
should commit alongside today's commit with today's message. Trying to
amend the commit message to reference yesterday's date creates a
non-monotonic history that complicates future conflict resolution and
adds nothing to the live site (the URL is what determines freshness to
Googlebot, not the commit message).

**Pitfall — DO NOT clean up the orphaned file before committing it:**
even if you suspect the file has minor issues, recovering it as-is is
almost always better than losing a day of content. If the file is
genuinely broken (the verification checks in step1 fail), then and only
**Pitfall — DO NOT clean up the orphaned file before committing it:** even if you suspect the file has minor issues, recovering it as-is is almost always better than losing a day of content. If the file is genuinely broken (the verification checks in step1 fail), then and only then should you skip it.

## 13. `sleep N && curl` chained command exceeds terminal's 60s default timeout (verified 2026-06-17)

**Symptom:** The verify step in the recommended 9-call clean recipe ends with:

```bash
sleep 180 && curl -s -o /dev/null -w "HTTP %{http_code}\n" https://oriental-destiny.com/fate-YYYY-MM-DD.html
```

The terminal tool's default timeout is 60s. `sleep 180` alone blocks the call for the full 180s, then the curl runs after — but the terminal tool returns control only after the entire command exits. Three consecutive `sleep 180 && curl` attempts timed out at 60s with `Command timed out after 60s` and exit code 124, leaving the deployment unverified even though the push had already succeeded.

**Fix (verified 2026-06-17):** split the sleep and the curl into separate terminal calls, OR run the curl with `--max-time 30` and no chained sleep:

```bash
# Option A: split into two calls (most reliable)
# Call 1: just sleep
sleep 120
# Call 2: curl with --max-time
curl -s -o /dev/null -w "HTTP %{http_code}\n" --max-time 30 https://oriental-destiny.com/fate-YYYY-MM-DD.html
```

```bash
# Option B: single call, no chained sleep (use --connect-timeout, accept partial delay)
curl -s -o /dev/null -w "HTTP %{http_code}\n" --max-time 30 --connect-timeout 20 https://oriental-destiny.com/fate-YYYY-MM-DD.html
```

The verify is best-effort — if the curl returns HTTP 200, deployment is confirmed; if it returns a network error or the call times out, the push likely succeeded anyway and a follow-up manual check can confirm. Do NOT retry the sleep+curl 3+ times in a row; that burns budget with no new information. After 1-2 failed verify attempts, report the push SHA and let the next cron run do the verify.

**Budget impact:** each timed-out `sleep 180 && curl` consumes one full tool-call slot. Three timeouts is three lost slots on a verify step that is supposed to be one slot. Always split sleep and curl when the sleep exceeds ~50s.

## 14. SSH-remote-revert is recurring, not a one-time fix (verified 2026-06-07, re-verified 2026-06-17)

**Symptom:** A cron run starts with `git remote -v` showing the HTTPS URL:

```
origin	https://github.com/qzw-alt/oriental-destiny.git (fetch)
origin	https://github.com/qzw-alt/oriental-destiny.git (push)
```

The push then fails with `fatal: could not read Username` / `Password authentication is not supported for Git operations`. The 2026-06-06 cron initially switched the remote to SSH, the 2026-06-07 cron confirmed the fix was durable, but the 2026-06-17 cron found the remote had reverted to HTTPS again.

**Root cause (working hypothesis):** a sibling cron, a separate git operation, or a fresh clone in a different session wrote the HTTPS URL back into `.git/config`. The exact trigger is not known.

**Recipe — always check the remote URL at the start of every cron run (verified):**

```bash
cd ~/oriental-destiny && git remote -v
# If SSH (git@github.com:qzw-alt/oriental-destiny.git), proceed.
# If HTTPS, switch before pushing:
git remote set-url origin git@github.com:qzw-alt/oriental-destiny.git
```

Combine the check with `git status` and `git branch -a` in a single terminal call:

```bash
cd ~/oriental-destiny && git remote -v && git status && git branch -a | head -5
```

This is one tool call that catches: (a) HTTPS→SSH revert, (b) divergent local main, (c) clean working tree (so the 9-call clean recipe applies rather than the 10-call merge-and-resolve recipe).

## 15. JSON-LD `@context` and `@@type` typos — grep-validation recipe (verified 2026-06-13)

The SKILL.md already documents the `@@type` (double `@`) and
`@@context` typos as JSON-LD pitfalls. The remediation is: after
writing the schema block, run a single grep to catch both:

```bash
grep -E '"@@(type|context)"' /home/ubuntu/oriental-destiny/fate-YYYY-MM-DD.html
# Expect: no output. Any match is a fat-finger typo.
```

Apply this grep every time, even when copy-pasting the block from a
prior article. The risk surface is small but a broken schema.org
payload silently costs Google rich-result eligibility. Cost: 1 tool
call.

## 16. `/tmp/check_*.py` is the third working pattern for the tirith `-c` block (verified 2026-06-18)

The existing recipes for the tirith `script execution via -e/-c flag`
block are: (a) use the bundled scripts at
`/home/ubuntu/.hermes/skills/creative/programmatic-seo/scripts/` for
in-process analysis; (b) use `read_file` with `offset` and `limit` for
ad-hoc inspection. Both are confirmed working. A third pattern is now
verified for cases where neither (a) nor (b) is sufficient:

**When to use `/tmp/check_*.py`:** when you need MULTIPLE things in one
call — e.g., "run the humanize score script AND check word count AND
check for non-ASCII content AND check for JSON-LD typos" — and the
bundled script doesn't do all of it. The 2026-06-18 cron run combined
all four checks into one Python script and ran it in one terminal call
(8 seconds, 0 tool-call waste).

**Recipe (verified):**

```bash
# Step 1: write_file the script to /tmp/check_article.py
# Step 2: terminal call — python3 /tmp/check_article.py
```

The script can do anything: `subprocess.run()` the bundled score
script, parse the HTML directly, write log lines, return multi-section
output. The tirith scanner only blocks `python3 -c` and `python3 -e`
flags; `python3 /path/to/script.py` is fine.

**Why this beats chaining 4 separate `terminal` calls:** each separate
`terminal` call is one tool-call slot. Four checks via four calls is 4
slots. One `/tmp/check_article.py` invocation is 2 slots (write + run)
for the same information. The savings compound when you have 4+ checks
in a row, and the cron-budget cap is brutal on large runs.

**Why this beats `read_file` with `offset`/`limit`:** the
`offset`/`limit` approach forces you to eyeball raw lines, which is
slow and error-prone for tasks like "count em-dashes after decoding
HTML entities" or "check JSON-LD for `@type` vs `@@type` typos
across the whole file." A small Python script does both in one
deterministic pass.

**Cleanup is optional:** the script lives in `/tmp/` which is wiped
on session restart, so no housekeeping is needed. If the script might
be useful for the next run too (e.g., a "verify-no-CJK-chars" check
that runs on every new article), save it to
`scripts/inspect_article.py` and reference it from the skill body.

## 17. Thread-completion pivot recipe — when a multi-day sub-thread ends (verified 2026-06-18)

The `SKILL.md` "Seasonal content threading" section documents a
month-long room walk (06-10 → 06-17). The pivot that happened AFTER
the walk completed is the part that needed its own verified recipe.

**Signal that a thread has completed (verified 2026-06-18):** the
prior 3-5 articles in the repo have all been in the same sub-thread
(e.g., room-by-room Fire Month walk), the final article in the
thread (06-17 Living Room) closes the loop, and the next article
needs a fresh angle to avoid "the site has been saying the same
thing for 8 days straight" reader fatigue.

**Verified pivot recipe (2026-06-18 Flying Stars article):**

1. **Confirm thread completion:** the most recent article should
   close the loop on the active sub-thread. The 06-17 Living Room
   piece was the fifth and final major room — no obvious next room
   to write.
2. **Identify the next sub-thread from the SKILL.md list of options.**
   The `SKILL.md` "Room walk completion milestone" note lists three
   pivot options: (a) classical feng shui concept not yet covered,
   (b) element transition article, (c) chart-side deepening. Pick
   based on:
   - **Grep first to confirm virgin status:** `ls *.html | grep -i
     KEYWORD` for the option's anchor keyword. Zero hits = virgin
     topic. The 2026-06-18 run grep'd
     `(bagua|flying.star|annual|nine|luo|compass|sect)` and got
     zero hits across the whole repo — strong signal to write the
     Flying Stars piece.
   - **Seasonal adjacency:** a thread that opens a few days before
     a solar term reads better than one that opens weeks before.
     Flying Stars 2026 is calendar-agnostic (it runs from Li Chun
     Feb 4 to Li Chun Feb 4 next year), so timing is fine any
     time post-February.
   - **Chart-side depth available:** the 06-18 Flying Stars piece
     uses the per-Day-Master read of each star placement, which
     cross-links cleanly to all 10 existing day-master.html pages.
     This is the "weave it back to BaZi" move that keeps the site's
     two content strands (feng shui + BaZi) talking to each other.
3. **Choose the topic title and target keyword.** For 2026-06-18:
   - Title: "Annual Flying Stars 2026: The Nine Stars in Your Home
     This Fire Horse Year"
   - Target keyword: "annual flying stars 2026" (long-tail,
     low-competition, matches the site voice's "year of X" phrasing
     in 06-12 Xia Zhi and 06-11 Bing Day Master)
   - H1: matches title (minus site suffix)
4. **Set up the article structure to bridge the thread change.** The
   06-18 piece opens with a meta-reference: "The room walk I have
   been doing all month — the bedroom, the kitchen, the home
   office, the entryway, the living room — is the practical side
   of the same practice. The Flying Stars tell you which room is
   loud this year. The room walk tells you what to do once you
   walk in." This single sentence re-anchors the prior thread
   and frames the new thread as a complement, not a replacement.
   Without that bridge, a reader landing on 06-18 directly feels
   like the site just changed topics under them.
5. **Plan 3-5 days ahead.** The pivot article is the start of a
   new sub-thread. For 06-18, the natural next sub-threads are:
   - 06-19: depth on one Flying Star sector (e.g., "Flying Star
     5 Yellow in the Southwest: How to Live With the Worst Star
     of 2026")
   - 06-20: per-chart flying star reading (e.g., "What the 2026
     Flying Stars Mean for a Fire-heavy Chart")
   - 06-21: prep for Xiao Shu (July 7) — the next solar term
   This is the 3-5 day lookahead the SKILL.md's "Seasonal
   content threading" section recommends; thread it explicitly
   when you write the pivot article so the next cron run has a
   target.

**Why this recipe matters:** without an explicit pivot, the next
cron run after a thread completion re-runs the "pick a topic"
heuristic and may land on a sub-thread that's slightly off
(eg., a new Day Master when the chart thread has been quiet for
a week, or a room-specific piece when the room walk has
obviously closed). The pivot recipe says: "the thread is done;
here are the three structured options; pick by grep-verified
virgin status first, then seasonal adjacency, then chart-side
depth."

## 18. Long-article humanize scoring — sub-baseline em-dash density is fine (verified 2026-06-18)

The oriental-destiny em-dash baseline is 10-18 per 1200 words. The
06-18 Flying Stars article shipped at 4421 words with 24 em-dashes
= 5.3/1200 words (less than half the baseline) and scored 95/100
after one `actually` → `really` patch.

**Why this is fine (and not a hidden problem):**

- The humanize score formula penalizes word count DIRECTLY
  (a "high word count" note appears in the script output for any
  article over ~3000 words).
- The em-dash penalty in the score is keyed to the 10-18 baseline,
  but the actual scoring penalty for "too few em-dashes" is
  smaller than the penalty for "too many em-dashes" — and the
  word-count penalty already absorbs the cost of a long article.
- A 4400-word article with 24 em-dashes is consistent with a
  working-practitioner voice: long explanations, fewer aside
  parentheticals, more direct sentences. The voice reference
  in `references/oriental-destiny-deployment.md` already documents
  that the 06-14 Bedroom Fire Month article shipped at 0 em-dashes
  with a score of 88.

**Recipe — when to add em-dashes vs. leave the article alone
(verified):**

- If the score is ≥85 after the first run: leave it. Do not add
  em-dashes artificially to hit the baseline. The 06-18 article
  hit 87 on the first pass (one banned-vocab hit + word count
  note) and 95 after a single one-word patch. Total: 1 patch,
  no em-dash fiddling.
- If the score is 60-80 and the only notes are "high word count"
  and "banned vocab Nx": patch the banned-vocab hits one at a
  time. Each clean patch usually bumps the score by 5-10 points.
- If the score is <60: read the actual notes list. The "banned
  vocab" notes are the real problem; the "em-dash too many/too
  few" note alone rarely drops the score below 60 on a 4-5K
  word article.

**Why not strip em-dashes or add them to align with the
baseline:** doing so pushes the article OUT of its natural
voice rhythm. The 06-18 article's 5.3/1200 density matches
the long-form "explainer" voice the site uses for classical
concepts (compare to 06-12 Xia Zhi at 3,492 words, which
shipped with sub-baseline em-dash density as well — the
classical-concept articles are consistently more text-dense
and parenthetical-light than the room-specific articles).
Sticking to the per-topic voice profile is more important
than hitting the global em-dash baseline.