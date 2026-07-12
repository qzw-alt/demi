# Heavy-Dir Leak Scenarios

When the user supplies a smaller exclude list than the canonical one, rsync
silently syncs hundreds of MB of heavy hermes-agent / lsp directories into the
working tree. The protection comes from `.gitignore` (step 3), not from rsync
excludes. This file documents real-world numbers from past backups so future
runs can verify the protection is actually working.

## 2026-07-11_22:02 run — clean baseline (no leaks), with walker AND scan fixes

User-supplied exclude list (~12 paths from a cron prompt):
```
.git, cache/, audio_cache/, image_cache/, gateway.lock, gateway.pid,
state.db*, sandboxes/, logs/, sessions/, memories/, plus the cron prompt's
"防止 secret scanning 拦截" framing
```

SSH auth verified (`Hi qzw-alt!`). The cron prompt also embedded a literal
`github_pat_11B67EO2Y0...` token; that PAT was NEVER used for auth (SSH only)
but was rsynced from `~/.hermes/cron/jobs.json` and had to be redacted.

| Protection layer                                  | Fired? | Result |
|---------------------------------------------------|--------|--------|
| `rsync --exclude` for user's 12 paths             | ✅     | All 12 verified absent post-rsync |
| Heavy-dir visibility check (`for d in venv/...`)  | ✅     | 0 HEAVY flags — clean |
| Skill canonical rsync heavy-dir excludes (venv/website/tests/ui-tui/lsp/node_modules) | ✅     | 382M working tree (vs 3.2G source) |
| Canonical `.gitignore` restore (rsync wiped it)   | ✅     | 48 entries written — critical, see pitfall |
| `git rm --cached` of legacy tracked artifacts    | ✅     | 0 needed — previous run had cleaned already |
| Walker redaction (config.yaml + tree walk) — **widened INCLUDE_EXT to .js/.tsx/.html/.css etc.** | ✅ | 137 files modified, **19 PATs + several hundred sk- redactions** (incl. 97 in one compiled JS bundle) |
| CJK-path single-file recovery                     | n/a    | Walker handled CJK paths fine once INCLUDE_EXT was widened; no single-file recovery needed |
| Length-gated grep scan (40+ chars) — **widened `--include` same 22 extensions** | ✅ | 0 hits — clean |
| Commit + push (SSH)                               | ✅     | `d2ab340` on origin/master, +593 / −2335 |
| Push protection                                   | ✅     | 0 blocks — all secrets stripped |

**Outcome:** 3.2G rsync source → 382M working tree of untracked-only-heavy-dirs
+ tracked config/skills/plugins, then a clean diff commit. Zero leaks to GitHub.

**Key takeaway:** the multi-layer defense (rsync excludes + post-rsync
visibility check + .gitignore restore + walker redaction + length-gated
scan with **matched extension coverage**) is robust when ALL steps run. The
critical 2026-07-11 fix was extending both the walker's `INCLUDE_EXT` tuple AND
the step-5 grep `--include` list from 11 → 22 file types — `.js`, `.mjs`,
`.cjs`, `.jsx`, `.ts`, `.tsx`, `.html`, `.htm`, `.css`, `.less`, `.scss`,
`.svg`, `.xml`. The previous narrower list silently missed an entire class of
real sk- tokens embedded in compiled JS/CSS bundles and blog HTML.

**Files with the heaviest leaks captured** (representative):
- `hermes-agent/hermes_cli/web_dist/assets/index-CBTV-n-R.js` — 97 sk- redactions
- `hermes-agent/hermes_cli/web_dist/assets/index-BVrUoMGI.css` — 21 redactions
- `cron/jobs.json` — 1 PAT (the cron prompt's embedded token)
- `bin/uv` (99MB compiled binary) — 7 sk- redactions via `strings(1)`
- `config.yaml` — 2 sk- redactions
- 4 SKILL.md files in `skills/.curator_backups/` snapshots — each with 0-1 PAT

**Operational change for next run:** the skill's bundled
`scripts/redact_secrets.py` was patched in this commit. Future cron agents
loading the skill via `skill_view` will get the widened INCLUDE_EXT
automatically.

## 2026-07-09 run — user-supplied exclude list too short

User-supplied exclude list (11 paths):
```
.git, cache/, audio_cache/, image_cache/, gateway.lock, gateway.pid,
state.db*, sandboxes/, logs/, sessions/, memories/
```

Heavies that leaked through rsync despite the exclude list (caught by post-rsync
visibility check, then blocked by step 3's canonical .gitignore):

| Path                          | Size   | Why it leaked                              |
|-------------------------------|--------|--------------------------------------------|
| `hermes-agent/venv/`          | 456M   | Not in user's short exclude list           |
| `lsp/node_modules/`           | 64M    | Not in user's short exclude list           |
| `hermes-agent/website/`       | 27M    | Not in user's short exclude list           |
| `hermes-agent/tests/`         | 26M    | Not in user's short exclude list           |
| `hermes-agent/ui-tui/`        | 3.5M   | Not in user's short exclude list           |

**Outcome:** Step 2's `du -sh` post-rsync check flagged all five, step 3 wrote
the full canonical `.gitignore` (heavy-dir block included), `git add -A` then
saw them as ignored, and the commit went from a potential ~600M diff to the
actual `14 files changed, 756 insertions(+), 206 deletions(-)`.

## Default canonical heavy-dir block

Always include this in `.gitignore`, regardless of what the rsync `--exclude`
list looks like:

```gitignore
hermes-agent/venv/
hermes-agent/website/
hermes-agent/tests/
hermes-agent/ui-tui/
hermes-agent/node_modules/
hermes-agent/**/node_modules/
hermes-agent/__pycache__/
hermes-agent/**/__pycache__/
lsp/node_modules/
**/node_modules/
**/__pycache__/
**/*.pyc
```

## Why `rsync --exclude` alone is not enough

Two reasons:

1. **User-supplied exclude lists are typically short** (cron prompts copy a
   minimal subset of paths). The canonical list has 25+ entries; users usually
   list 10-15.
2. **Defense in depth**: `.gitignore` is the last line of defense. Even if
   rsync brings a file into the working tree, `.gitignore` keeps `git add -A`
   from staging it. Without `.gitignore`, the file lands in the commit.

## Verification recipe

After step 2's rsync, before step 3's `.gitignore` write, run:

```bash
cd /tmp/demi-backup/
for d in hermes-agent/venv hermes-agent/website hermes-agent/tests \
         hermes-agent/ui-tui lsp/node_modules; do
  [ -d "$d" ] && echo "HEAVY: $d - $(du -sh "$d" | cut -f1)"
done
```

If any of those directories is present, the next step MUST add them to
`.gitignore` (or `rm -rf` them outright if they're known-unneeded). Then before
step 6's commit, run `git status --short | wc -l` — if the count is in the
thousands, .gitignore is still missing entries.

## Related pitfalls in SKILL.md

- "User-supplied exclude lists are often smaller than the canonical one —
  verify heavy dirs aren't in the working tree"
- "rsync `--delete` can wipe the working tree's `.gitignore` if the source
  doesn't have one"
- "Default git clone over SSH may take >60s" (related: heavy repos = slow clones)
- "Cron job prompt becomes the source of the next backup's PAT leak" +
  "PAT-in-cron-prompt delivery advisory must be prominent, not buried"
