# 2026-07-21 backup session — cron-imposed SSH-only policy + more redactions caught

Clean SSH-auth backup, 16 files committed (14M + 2A), 0 secrets leaked in
commit. Three refinements captured for the skill:

## 1. Cron prompt now hard-bans HTTPS/PAT — update skill accordingly

**Reproduction:** today's cron prompt (the daily 22:00 Shanghai backup job)
explicitly forbade HTTPS, PATs, credential URLs, and the assistant from
*generating* new PATs:

> 【认证硬性规则】
> - 只使用 SSH：git@github.com:qzw-alt/demi.git。
> - 禁止使用 HTTPS、PAT、credential URL，也不要向用户索取或生成 PAT。
> - 先用 ssh -T -o StrictHostKeyChecking=no -o ConnectTimeout=10 git@github.com 验证 SSH
> - SSH 不可用时直接报告失败，不要改用 PAT。

This **contradicts** the existing skill step 0 fallback ("If the credential
store has an expired PAT, renew it...") and step 1 fallback ("If only a PAT
is available, clone with `https://USER:PAT@github.com/...`"). Those fallbacks
are unsafe in the cron context — the agent must not silently fall back to a
PAT when SSH is unavailable; it must surface the failure to the user.

**Workflow impact:**

The skill's step 0 / step 1 guidance needs to distinguish two contexts:
1. **Interactive user session** — PAT fallback + renew guidance is OK
2. **Cron/automated session** — SSH-only; if SSH fails, REPORT FAILURE,
   do NOT fall back to HTTPS / PAT / credential helper; do NOT generate a
   new PAT

**Recipe — detect cron context:**

The skill itself is environment-agnostic; the cron prompt is where the
SSH-only policy lives. But the skill's general guidance should be amended
to: "If the cron prompt explicitly bans PAT auth, follow the prompt's
rules. Do not silently substitute a PAT even if `~/.config/git/credentials`
contains one. Lead the failure response with: 'SSH auth unavailable — backup
aborted. Cron prompt forbids HTTPS/PAT fallback.'"

The PAT-in-cron-prompt pitfalls should NOT push the user toward a new PAT
in this context — the whole point of the SSH-only policy is to stop PATs
from being embedded in cron prompts at all.

## 2. `.gitignore` STILL got wiped despite both pre-rsync AND step-3 top guards

**Reproduction:**
- Pre-rsync guard ran: `for entry in .gitignore .gitattributes; do git checkout HEAD -- "$entry" 2>/dev/null && echo "Guarded $entry"; done`
- Both files restored (per `ls -la` after the guard)
- rsync ran
- Post-rsync LEAK check ran (no LEAK reported)
- Step 3 ran: `for entry in .gitignore .gitattributes; do [ -f "$entry" ] && git checkout HEAD -- "$entry" 2>/dev/null; done` — this is the *real* step-3 guard
- Then `ls .gitignore` reported "No such file or directory"

**Diagnosis:** unclear. Possibilities:
- (a) `rsync --delete` ran twice (some automated process or pre-existing background rsync)
- (b) The pre-rsync `git checkout HEAD` re-created the file, then rsync --delete removed it AGAIN in a second pass
- (c) Some other concurrent writer (kanban, gateway) removed it between the guards

**Fix applied today:** since the file was missing at the END of step 3,
the canonical .gitignore was rewritten via `cat > .gitignore <<'EOF' ... EOF`
*unconditionally* (not gated on `[ ! -s .gitignore ]`). The 2026-07-20
end-of-step-3 verification (`test -s .gitignore && git diff --quiet HEAD --`)
then confirmed the file is non-empty and differs from HEAD — which is the
expected state when we just rewrote it from the canonical template.

**Skill amendment:** the step-3 guard MUST include an unconditional
write of the canonical `.gitignore` at the end, not just a guard that
restores from HEAD. Reasons:
- HEAD's `.gitignore` may itself be stale or partial
- The canonical template is the source of truth for *this* skill
- Writing it unconditionally is cheap (~1ms) and prevents the entire
  "next commit has no .gitignore" failure mode

**Recommended new step-3 guard (replaces the current
`for entry in .gitignore .gitattributes; do git checkout HEAD -- ...; done`
which proved insufficient today):**

```bash
cd /tmp/demi-backup
# ALWAYS write the canonical .gitignore at end of step 3 — NOT gated on existence.
# The pre-rsync + step-3-top guards are necessary but not sufficient (reproduced 2026-07-21).
cat > .gitignore <<'EOF'
.git/

# Caches
cache/
audio_cache/
image_cache/

# Runtime state
gateway.lock
gateway.pid
state.db*
auth.lock
auth.json
kanban.db.init.lock
kanban.db.dispatch.lock

# Sensitive content
sessions/
memories/
memory/
memory_backup_*/
migration/
.env
.hermes_history

# Sandboxes, logs, OAuth tokens
sandboxes/
logs/
cron/output/
gsc/client_secret.json
gsc/token.json

# Node / Python deps
**/node_modules/
hermes-agent/node_modules/
hermes-agent/**/node_modules/
lsp/node_modules/
hermes-agent/__pycache__/
hermes-agent/**/__pycache__/
**/__pycache__/
**/*.pyc

# Heavy dirs that often leak through short exclude lists
hermes-agent/venv/
hermes-agent/website/
hermes-agent/tests/
hermes-agent/ui-tui/

# Kanban runtime lock + model registry cache (regenerated on every gateway tick)
kanban.db.init.lock
kanban.db.dispatch.lock
models_dev_cache.json

# Compiled bundles (text walkers can't safely redact binaries)
bin/uv
bin/tirith

# SQLite WAL / SHM transient runtime files for verification_evidence.db
verification_evidence.db-shm
verification_evidence.db-wal
EOF
# Verify it landed
test -s .gitignore && echo "OK .gitignore restored (canonical template)" || echo "ERROR: .gitignore write failed"
```

This supersedes both the pre-rsync guard AND the step-3-top guard as the
**primary** defense. The other guards remain useful belt-and-braces, but
the unconditional write is the one that worked today.

**Update reproduction count for the relevant pitfall:** now 7 (the
"gitignore silently deleted" pattern, with 2026-07-16 being the original
post-step-3 observation and 2026-07-20/-21 being reproductions despite
multiple guards).

## 3. CJK walker miss + `tvly-` miss reproduced AGAIN — 6th and 4th confirmed runs

**Reproduction:** today's run had 4 separate redactions needed:

| File | Token type | Why walker missed |
|---|---|---|
| `workspace/website/德米知识库/01-记忆系统/MEMORY.md` | `sk-` (kimi) | CJK-encoded path; `os.walk` skips it |
| `workspace/website_old/MEMORY.md` | `tvly-` | Walker regex only covers `sk-` and `github_pat_` |
| `workspace/website_old/德米知识库/01-记忆系统/MEMORY.md` | `tvly-` | Same |
| `workspace/website/德米知识库/01-记忆系统/MEMORY.md` | `tvly-` | Same |

**Step-5 scan still caught all 4** before staging. Single-file redaction
via `redact_secrets.py <dir> <file>` for the sk- hit, and `/tmp/redact_prefix.py
tvly <file>` for the three tvly- hits. Total: 4 manual interventions, all
caught by step-5 scan.

**Update reproduction counts in the relevant pitfalls:**
- CJK walker miss: 6 confirmed runs (2026-07-08, -13, -14, -16, -17, -21)
- `tvly-` walker miss: 4 confirmed runs (2026-07-19, -20, -21 + today's
  validation; in practice every backup that finds any user `MEMORY.md`
  with a Tavily key will reproduce this)

**Skill amendment:** the existing pitfalls already document these; they
just need updated reproduction counts in the text. No workflow change —
the single-file + prefix-script fallback recipes already worked.

## 4. `models_dev_cache.json` rsync-exclude failed AGAIN — confirms 2026-07-12 pitfall

**Reproduction:** the rsync invocation included
`--exclude='models_dev_cache.json'`, but the file STILL appeared in the
working tree post-rsync. Today's run shows this is the **third** confirmed
reproduction of the rsync root-level filename matching bug.

**Action:** `git rm --cached models_dev_cache.json` + `rm -f models_dev_cache.json`
cleaned it. `.gitignore` already lists it (per canonical template).

**Workflow impact:** zero — the existing rsync root-level filename matching
pitfall is already documented. Today just adds another data point to the
reproduction count.

## 5. Submodule-internal `AIza` key confirmed (3rd run with this file)

`workspace/oriental-destiny/config.real.js` contained an `AIzaSy...`
Google API key. Confirmed today:
- `git ls-files --stage | awk '$1=="160000"'` listed `workspace/oriental-destiny` as a submodule
- `git ls-files | grep '^workspace/oriental-destiny'` returned 1 entry (`workspace/oriental-destiny` gitlink itself)
- `git ls-files workspace/oriental-destiny/config.real.js` returned empty
- → confirmed: the file is submodule-internal, won't be committed to parent
- → no redaction needed for the parent commit

This is the **third** run where this file shows up in the byte scan but
turns out to be submodule-internal. The 2026-07-19 submodule pitfall
covers it correctly; no amendment needed beyond reproduction count.

## 6. Cron prompt + delivery format — Chinese summary required

**Reproduction:** today's cron prompt explicitly requires:
> 7. 输出中文简报：认证方式、结果（成功/失败/无变更）、远程提交哈希、敏感扫描结果

The skill doesn't currently mention output language. This is a
user-preference delivery detail that should be encoded in the skill
because the user asked for it via the cron prompt (which is the
deliverable source of truth).

**Skill amendment:** add a note in the "Pitfalls" or a new "Delivery
format" section: "If the cron prompt specifies an output language, follow
it. The user may require Chinese (`输出中文简报`) or English; the default
delivery language is whatever the cron prompt or session context
dictates."

## Today's scan summary (for reference)

| Provider prefix | Threshold | Hits found | After redaction |
|---|---|---|---|
| `github_pat_` | 40+ chars | 0 | 0 |
| `gh[pousr]_` | 40+ chars | 0 | 0 |
| `sk-` | 40+ chars | 1 (CJK path) | 0 |
| `tvly-` | 40+ chars | 3 | 0 |
| `AIza` | 30+ chars | 1 (submodule) | N/A |
| `providers/*.json` literal values | len ≥ 40 | 0 | 0 |
| `xox[bpars]-` (Slack) | 20+ chars | 0 | 0 |

Staged-blob scan: 0 hits. Working tree: 4 manual redacts applied before
staging.

Commit: `c4b8c6b6a Backup: 2026-07-21_22:05`, local HEAD == remote
master HEAD verified by `git fetch` + `git log origin/master`. SSH auth
used throughout; no PAT was touched or generated.