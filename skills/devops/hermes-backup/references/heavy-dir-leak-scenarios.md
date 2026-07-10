# Heavy-Dir Leak Scenarios

When the user supplies a smaller exclude list than the canonical one, rsync
silently syncs hundreds of MB of heavy hermes-agent / lsp directories into the
working tree. The protection comes from `.gitignore` (step 3), not from rsync
excludes. This file documents real-world numbers from past backups so future
runs can verify the protection is actually working.

## 2026-07-09 run

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
