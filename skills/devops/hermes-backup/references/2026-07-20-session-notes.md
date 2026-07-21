# 2026-07-20 backup session — three refinements

Clean SSH-auth backup, 15 files committed, 0 secrets leaked. Three refinements
captured for the skill:

## 1. Submodule `.gitmodules` missing → still works, but `git submodule status` errors

**Reproduction:**
- `git ls-files --stage | awk '$1=="160000"'` listed `hermes-agent` and `workspace/oriental-destiny`
- `git submodule status` returned `fatal: no submodule mapping found in .gitmodules for path 'hermes-agent'`
- But `git add -A` still recorded gitlink SHAs correctly
- `git push` succeeded; remote received the new commit

**Workflow impact:**
- Do NOT treat `git submodule status` failure as fatal
- `git check-ignore` on a path inside a submodule returns `fatal: Pathspec ... is in submodule 'hermes-agent'` (not "ignored")
- `git show :<path>` for a submodule-internal path returns the same "is in submodule" error
- The staged-blob scan MUST skip submodule paths entirely

**Recipe — submodule-aware noise filter (run BEFORE step 5):**
```bash
cd /tmp/demi-backup
# Get submodules (works even with missing .gitmodules)
SUBMODULES=$(git ls-files --stage | awk '$1=="160000"{print $4}')
echo "Submodules: $SUBMODULES"
# Expand each into a NOISE alternation
EXTRA_NOISE=""
for sm in $SUBMODULES; do
  EXTRA_NOISE="$EXTRA_NOISE\|$(echo "$sm" | sed 's|/|\\/|g')"
done
echo "Extra noise filter: $EXTRA_NOISE"
# Use in NOISE var:
# NOISE="$NOISE$EXTRA_NOISE"
```

## 2. `providers/*.json` regex false-positive — JSON-walk instead

**Reproduction:**
- File: `providers/minimax_coding.json` (real config, no secrets)
- Content includes `"api_mode": "anthropic_messages"` — the field name pattern `[a-zA-Z0-9_-]*` matched `"_mode"`, then `: "`, then the value
- The 40-char gate `[a-zA-Z0-9_-]{40,}` didn't match (the value is short), BUT a different provider file with a longer config could false-positive more often

**Fix:** the step-5 grep is now replaced with a JSON walker that only flags string values of length ≥ 40:

```bash
for f in providers/*.json; do
  [ -f "$f" ] && python3 -c "
import json, sys
p = sys.argv[1]
try:
    d = json.load(open(p))
except Exception as e:
    print(f'  PARSE FAIL {p}: {e}')
    sys.exit(0)
def walk(o, path=''):
    if isinstance(o, dict):
        for k,v in o.items():
            walk(v, f'{path}.{k}' if path else k)
    elif isinstance(o, list):
        for i,v in enumerate(o):
            walk(v, f'{path}[{i}]')
    elif isinstance(o, str) and len(o) >= 40:
        print(f'  POTENTIAL KEY: {p} :: {path} = len={len(o)} preview={o[:6]}...{o[-4:]}')
walk(d)
" "$f"
done
```

Output: zero false positives on `minimax_coding.json` (no actual key values).

## 3. End-of-step-3 `.gitignore` re-verification

**Reproduction:**
- Clone succeeded; prior commit tracked `.gitignore` (52 lines)
- rsync --delete ran; verified `ls .gitignore` → "No such file or directory"
- Even though I had run `git checkout HEAD -- .gitignore .gitattributes` before rsync, rsync's --delete wiped them
- The skill's step-3 cleanup loop's `git checkout HEAD -- .gitignore` re-restored it

**Fix:** add this verification at the END of step 3 (after all the `git rm --cached` cleanup runs):

```bash
# END OF STEP 3: verify .gitignore is present and matches HEAD
test -s .gitignore && git diff --quiet HEAD -- .gitignore || {
  echo "ERROR: .gitignore missing or drifted from HEAD — restoring"
  git checkout HEAD -- .gitignore 2>/dev/null
  # Fallback: write canonical template if HEAD's version was also bad
  if [ ! -s .gitignore ]; then
    cat > .gitignore <<'EOF'
.git/
cache/
audio_cache/
image_cache/
gateway.lock
gateway.pid
state.db*
auth.lock
auth.json
kanban.db.init.lock
kanban.db.dispatch.lock
sessions/
memories/
memory/
memory_backup_*/
migration/
.env
.hermes_history
sandboxes/
logs/
cron/output/
gsc/client_secret.json
gsc/token.json
**/.curator_backups/
**/node_modules/
hermes-agent/venv/
hermes-agent/website/
hermes-agent/tests/
hermes-agent/ui-tui/
**/__pycache__/
**/*.pyc
verification_evidence.db-shm
verification_evidence.db-wal
models_dev_cache.json
bin/uv
bin/tirith
EOF
  fi
}
```

**Why "at the end of step 3" not "at the beginning":**
- Beginning: rsync may run AGAIN later in step 2 (e.g., user adds another `--exclude` mid-backup)
- End: all subsequent steps (4 redaction, 5 scan, 6 commit) assume .gitignore is correct; this is the last chance to fix it before stage

**Complements the 2026-07-16 pitfall:** the three-layer fix there is necessary but
not sufficient if a re-rsync occurs. The end-of-step-3 verification is the
final safety net.

## Today's scan summary (for reference)

| Provider prefix | Threshold | Hits | Action |
|---|---|---|---|
| `github_pat_` | 40+ chars | 0 | OK |
| `gh[pousr]_` | 40+ chars | 0 | OK |
| `sk-` | 40+ chars | 0 (after 4 CJK-path single-file redacts) | OK |
| `tvly-` | 40+ chars | 0 (after 3 prefix-script redacts) | OK |
| `AIza` | 30+ chars | 0 | OK |
| `providers/*.json` literal values | len ≥ 40 | 0 (JSON walk) | OK |

Walker reported 580+ redactions across 163 files in batch pass; 4 CJK-path
files needed single-file redacts (sk-); 3 files needed `tvly-` prefix-script
redacts. Total: 7 manual interventions, all caught by step-5 scan before
staging.

Commit: `a79308491 Backup: 2026-07-20_22:04`, remote verified, no PAT in
commit history (SSH auth used throughout).