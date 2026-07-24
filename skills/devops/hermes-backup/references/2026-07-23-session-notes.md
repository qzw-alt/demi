# 2026-07-23 session notes

Clean run. The major finding today is **procedural**: the cron prompt was
finally rewritten (no embedded `github_pat_...`), and the "idempotent
re-desensitization vs. real new leak" distinction was empirically validated
for the first time. No new redactions were needed — all CJK walker miss /
tvly- miss flags turned out to be safe placeholders that match the HEAD
content.

## 1. Cron prompt is now clean — escalation count resets

**Reproduction:** today's cron prompt (the daily 22:00 Shanghai backup
job) NO LONGER embeds a `github_pat_11B67EO2Y0...Q5` token. The cron
source `~/.hermes/cron/jobs.json` (after rsync) was scanned for any
PAT-shaped string and produced zero hits. This is the first day since
2026-07-21 (when the SSH-only policy was added to the prompt) where
the dead-PAT case A escalation can stop.

**Workflow consequence:**
- Skip the lead-sentence "rewrite cron prompt to remove dead PAT"
  advisory — there's no PAT to remove.
- The 6-consecutive-runs escalation note in the SKILL.md pitfall block
  (the "PAT-in-cron-prompt Case A is now reproduced SIX times..." entry)
  is **resolved** as of today. Update or remove it on the next pass;
  for now leave it as historical record.
- Continue verifying each new cron run — if a future prompt regresses
  and re-embeds a PAT, the lead-sentence advisory comes back.

## 2. CJK + tvly- walker "misses" were idempotent re-redaction, not new leaks

**Reproduction:** step 5 length-gated scan flagged the usual three files:
- `workspace/website/德米知识库/01-记忆系统/MEMORY.md` — `sk-kimi-...NGGW` hit
- `workspace/website_old/MEMORY.md` — `tvly-dev-sAFTx-...a7Si` hit
- `workspace/website_old/德米知识库/01-记忆系统/MEMORY.md` — same tvly- hit

Each was treated with the single-file redaction recipe (`python3
redact_secrets.py <dir> <file>` for sk-, `/tmp/redact_prefix.py tvly
<file>` for tvly-). But on close inspection with:

```bash
diff <(git show HEAD:"workspace/website_old/MEMORY.md") \
     "workspace/website_old/MEMORY.md"
# exit code: 0  (no diff)
```

…all three files were **already in truncated placeholder form in HEAD**.
The walker "miss" is a re-desensitization of an already-safe file:
identical bytes before and after. The grep output showed
`tvly-dev-sAFT...a7Si` — which at first glance looks like a 57-char
real token, but `re.findall(rb'tvly-[a-zA-Z0-9_-]{40,}', data)` via
Python's raw-bytes API returned `len=20` (a truncated placeholder
shape: `tvly-dev-sAFT...a7Si` is exactly `tvly-` + 8 + `...` + 4 = 20
chars), confirming the placeholder form.

**New verification pattern (added to skill):** when step 5 flags a file
that you suspect is already safe (because the walker redacted it last
run, or because the file is on the canonical-MEMORY.md list), check
`diff <(git show HEAD:"<path>") "<path>"` first. If exit 0, the file
is already in safe form — no re-desensitization is needed, and the
"walker miss" was a false alarm. If exit non-zero, the working tree
differs from HEAD, meaning a new leak is in the source itself (or
HEAD was desensitized with a different prefix/length — rare).

**Why this matters:** applying redundant re-desensitization wastes
cycles AND risks the "Truncation regex falsely matches across `...`
markers" pitfall (see SKILL.md pitfalls block) if the redaction
function's regex isn't careful with already-truncated tokens. Always
diff against HEAD before single-file re-running.

## 3. Heavy-dir "leak" inside submodule = informational, not blocker

**Reproduction:** post-rsync LEAK check reported heavy dirs present in
working tree:

| Dir | Size | Verdict |
|---|---|---|
| `hermes-agent/venv` | 607M | submodule-internal — parent doesn't track |
| `hermes-agent/website` | 27M | submodule-internal |
| `hermes-agent/tests` | 32M | submodule-internal |
| `hermes-agent/ui-tui` | 3.7M | submodule-internal |

All four dirs live under the `hermes-agent` submodule. The parent
repo's `git ls-files --stage` shows `hermes-agent` as a `160000` gitlink;
the parent commit records only the submodule's SHA, not its internal
files. So the heavy-dir presence in the working tree is **expected
and harmless** — `git add -A` won't add them, no .gitignore changes
needed.

**Skill amendment:** the 2026-07-19 submodule pitfall covers "submodule
hits are informational" but doesn't explicitly mention heavy-dir LEAK
warnings. Add a clarifying line: "When the post-rsync LEAK check
reports heavy dirs (`hermes-agent/venv/`, `website/`, `tests/`,
`ui-tui/`) under a submodule path, treat as informational — these are
inside `hermes-agent` (or `workspace/oriental-destiny`) and the parent
repo doesn't track submodule contents. The 2026-07-09 heavy-dir-leak
pitfall's worst-case numbers (venv 456M → 607M today, etc.) describe
non-submodule scenarios and remain valid; submodule-internal versions
of those same dirs are silent no-ops."

## 4. 8th reproduction of rsync --delete wiping .gitignore

**Reproduction:** today's run also showed the pattern:
1. `git clone` → working tree has `.gitignore` from HEAD
2. `rsync --delete` runs → working tree `.gitignore` is deleted
   (source `~/.hermes/.gitignore` is absent, so `--delete` removes
   the destination file too)
3. Step 3's top guard `git checkout HEAD -- .gitignore` re-creates it
4. Step 3's `for dir in sessions memories ...` cleanup loop runs
5. End of step 3: `.gitignore` is back (the unconditional `cat >
   .gitignore <<EOF` write recovered it)

The unconditional canonical-template write at end of step 3 (added
2026-07-21) continues to be the primary defense and held today.
Reproduction count: **8 confirmed runs** (was 7 in the SKILL.md
pitfall).

## 5. Bash `$(git show :path)` on CJK paths emits null-byte warning — informational

**Reproduction:** the staged-blob scan loop ran
`CONTENT=$(git show ":$f")` for files with CJK-encoded paths. Bash
emitted:
```
warning: command substitution: ignored null byte in input
```
…but the captured CONTENT still produced valid byte data and the
length-gated regex scan returned 0 hits (matching the Python
byte-check via execute_code). The warning is harmless — bash's
command substitution strips NUL bytes from the variable, but the
rest of the output is preserved.

**Workflow impact:** zero — the warning is informational, and the
scan result is correct. If you want zero-noise output, replace bash
command substitution with `git show ":$f" | cat` (no `$()` wrap) or
run the scan via Python subprocess (already documented in
references/secret-redaction-verification.md).

## 6. Today's scan summary

| Pattern | Threshold | Working tree | Staged blobs |
|---|---|---|---|
| `github_pat_` | 40+ chars | 0 | 0 |
| `gh[pousr]_` | 40+ chars | 0 | 0 |
| `sk-` | 40+ chars | 0 (after idempotent re-redact) | 0 |
| `tvly-` | 40+ chars | 0 (after idempotent re-redact) | 0 |
| `AIza` | 30+ chars | 1 (submodule `workspace/oriental-destiny/config.real.js`) | N/A |
| `providers/*.json` literal values | len ≥ 40 | 0 | 0 |
| `cron/jobs.json` PAT/sk- search | any | 0 | 0 |

Working tree changes today: **21 files** (增 1199 / 删 665). New file
additions include 6 new SKILL.md reference files (`indoor-room-walk-thread`,
`2026-07-22-session-notes`, `news-article-html-format-2026-07`,
`pending-2026-07-23-hk-chinese-medicine-hospital-stroke-back-pain-shipped`,
`iterative-audit-and-report-upload`) plus `tmp/audit/action-list.json` and
`tmp/audit/extract-actions.py`. Tracked delete:
`reports/chinahospitalsguide/audit-2026-07-22-unindexed-cleanup.md`.

## Numbers worth noting

- hermes-agent/venv grew from 607M (2026-07-22) → 607M (today, same)
- Working tree changes today: 21 files, +1199 / −665 (modest; daily runtime-state churn)
- No PAT-in-cron-prompt today — escalation count goes from 6 to **0**
- `models_dev_cache.json` not present (rsync --exclude worked today, unlike 2026-07-21)

## Commit

`f9e78c57e011a5c6e83312a73ed99815cbc15f0a` (master, Remote = Local
verified). SSH auth used throughout. Cron prompt finally clean.

## Action items

- **None for the user.** The previous "rewrite cron prompt" advisory is
  resolved.
- For future runs: if the cron prompt re-embeds a PAT, the lead-sentence
  advisory comes back automatically (the user reverted it).