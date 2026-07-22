---
name: hermes-backup
description: Backup ~/.hermes/ to GitHub backup repository, excluding sensitive files
---

# Hermes Backup to GitHub

Backup `~/.hermes/` to a GitHub backup repository (e.g., `qzw-alt/demi`).

## Workflow

1. **Verify GitHub auth** — check SSH key first, then credential helpers
2. **Clone/update repo** to `/tmp/hermes-backup/`
3. **Sync with rsync**, excluding sensitive files
4. **Strip API keys** from tracked config files before commit
5. **Commit and push**

## Exact Commands

### 0. Verify GitHub auth first
```bash
# Prefer SSH key auth — verify it works.
# Note: `ssh -T git@github.com` ALWAYS exits 1 on success (GitHub deliberately
# rejects the shell session — "successfully authenticated" still appears on stderr).
# Check stderr text, NOT return code. Using `&& echo OK` masks the non-zero exit
# and makes SSH look broken, but technically still works because grep finds the match.
SSH_OUT=$(ssh -T -o StrictHostKeyChecking=no -o ConnectTimeout=10 git@github.com 2>&1)
echo "$SSH_OUT" | grep -q "successfully authenticated" && echo "SSH OK" || echo "SSH NOT available"
# Check credential store (don't cat it — never print the PAT)
grep -q '^https://.*github.com' ~/.config/git/credentials 2>/dev/null && echo "credential store: present"
# Check for custom credential helpers
git config --global --get-all credential.https://github.com.helper 2>/dev/null
git config --global --get credential.helper 2>/dev/null
# Check known helper scripts
ls /tmp/git-cred-helper.py 2>/dev/null && echo "Custom cred helper found: /tmp/git-cred-helper.py"
```

If neither works, set up SSH: `ssh-keygen -t ed25519 -C "backup" && cat ~/.ssh/id_ed25519.pub` and add to GitHub.
If the credential store has an expired PAT, renew it by editing `~/.config/git/credentials` (or the custom helper script) with a new fine-grained token. Generate PAT at https://github.com/settings/tokens?type=beta with repo:Contents:Write scope.

**SSH key auth is preferred over PAT** — `git@github.com:qzw-alt/demi.git` works when PAT fails.

**⚠️ Cron-context SSH-only policy (added 2026-07-21):** If the cron prompt explicitly bans HTTPS / PAT / credential URLs (or says "don't ask the user for a PAT", or specifies "SSH 不可用时直接报告失败，不要改用 PAT"), follow the prompt's rules even when SSH is unavailable. Do NOT silently fall back to a PAT, do NOT generate a new PAT, do NOT use a credential helper. When SSH fails in this context, abort the backup and lead the delivery response with: "SSH auth unavailable — backup aborted per cron policy. Restore SSH key to `~/.ssh/id_ed25519.pub` and re-test with `ssh -T git@github.com`." The existing "renew the PAT" / "switch to HTTPS clone" / "use credential helper" guidance below applies ONLY to interactive user sessions where the user has not imposed this restriction.
Verify with: `ssh -T git@github.com` (should print "Hi <username>! You've successfully authenticated").
If SSH works but PAT doesn't, switch the remote to SSH after clone:
```bash
git remote set-url origin git@github.com:qzw-alt/demi.git
git push origin master
```

**MANDATORY: curl-test the user-supplied PAT (if any) before relying on it.** Cron prompts frequently embed PATs that are dead-on-arrival. Before proceeding with HTTPS, do:
```bash
PAT="<token from cron prompt or credentials>"
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" -H "Authorization: token $PAT" https://api.github.com/user)
[ "$HTTP_CODE" = "200" ] && echo "PAT VALID" || { echo "PAT INVALID (HTTP $HTTP_CODE) — falling back to SSH"; }
```
If 401, the PAT is dead — don't try to use it, don't try to "renew" it, just fall back to SSH and lead the delivery response with the "rewrite the cron prompt" advisory (Case A in the pitfalls). `git ls-remote` is NOT a valid auth test (works on public repos without auth, gives false-positive).

### 1. Clone repo (use SSH — PATs expire, SSH keys don't)
```bash
rm -rf /tmp/hermes-backup/
mkdir -p /tmp/hermes-backup/
cd /tmp/hermes-backup
git clone git@github.com:qzw-alt/demi.git .
```

**Fallback:** If only a PAT is available, clone with `https://USER:PAT@github.com/...` but switch to SSH remote before pushing if PAT fails:
```bash
git remote set-url origin git@github.com:qzw-alt/demi.git
```

### 2. Rsync with exclusions
```bash
rsync -a --delete \
  --exclude='.git/' \
  --exclude='cache/' \
  --exclude='audio_cache/' \
  --exclude='image_cache/' \
  --exclude='gateway.lock' \
  --exclude='gateway.pid' \
  --exclude='state.db*' \
  --exclude='sandboxes/' \
  --exclude='logs/' \
  --exclude='sessions/' \
  --exclude='memories/' \
  --exclude='auth.json' \
  --exclude='auth.lock' \
  --exclude='cron/output/' \
  --exclude='**/.curator_backups/' \
  --exclude='hermes-agent/node_modules/' \
  --exclude='hermes-agent/**/node_modules/' \
  --exclude='lsp/node_modules/' \
  --exclude='**/node_modules/' \
  --exclude='hermes-agent/__pycache__/' \
  --exclude='hermes-agent/**/__pycache__/' \
  --exclude='**/__pycache__/' \
  --exclude='**/*.pyc' \
  --exclude='.env' \
  --exclude='.hermes_history' \
  --exclude='gsc/client_secret.json' \
  --exclude='gsc/token.json' \
  --exclude='kanban.db.init.lock' \
  --exclude='kanban.db.dispatch.lock' \
  --exclude='models_dev_cache.json' \
  --exclude='bin/uv' \
  --exclude='bin/tirith' \
  /home/ubuntu/.hermes/ /tmp/hermes-backup/
```

**After rsync — verify exclusions actually took effect** (rsync can silently leak root-level files; don't trust the exclude to have worked). This step is **mandatory** — a smaller user-supplied exclude list (typical in cron prompts) will not block heavy dirs like `hermes-agent/venv/` (~456M), `lsp/node_modules/` (~64M), `hermes-agent/website/` (~27M), or `hermes-agent/tests/` (~26M). They will land in the working tree and inflate the next commit by hundreds of MB unless .gitignore catches them in step 3.

```bash
cd /tmp/hermes-backup/
# Verify each user-specified exclude is absent
for p in sessions/ memories/ cache/ logs/ sandboxes/ audio_cache/ image_cache/ \
         auth.json auth.lock .env .hermes_history \
         gsc/client_secret.json gsc/token.json kanban.db.init.lock kanban.db.dispatch.lock \
         models_dev_cache.json gateway.lock gateway.pid cron/output/ \
         verification_evidence.db-shm verification_evidence.db-wal; do
  [ -e "$p" ] && echo "LEAK: $p"
done
# Heavy dirs that will almost always leak when the user supplies a short exclude list
# (real-world numbers from 2026-07-09 backup: venv 456M, lsp 64M, website 27M, tests 26M, ui-tui 3.5M)
for d in hermes-agent/venv hermes-agent/website hermes-agent/tests hermes-agent/ui-tui lsp/node_modules; do
  if [ -d "$d" ]; then
    echo "HEAVY: $d - $(du -sh "$d" 2>/dev/null | cut -f1)"
  fi
done
# If any LEAK appeared, rm -f it (or rm -rf for dirs) and git rm --cached
# If heavy dirs appeared, they MUST be added to .gitignore in step 3 BEFORE running git add -A
# (step 3's canonical .gitignore template already covers them; this is just the visibility check)
```

### 3. Remove old sensitive artifacts from previous backups
```bash
cd /tmp/hermes-backup
# Guard tracked housekeeping files BEFORE the cleanup loop runs.
# Reproduced 2026-07-16: the cleanup loop + rsync --delete chain
# silently deleted a tracked .gitignore and the commit went through
# with `delete mode 100644 .gitignore`. Restore from the previous
# commit so git tracks it as unchanged, not deleted.
#
# ⚠️ As of 2026-07-21 this guard is necessary but NOT sufficient —
# rsync --delete STILL wipes .gitignore on some setups (cron,
# parallel rsync, etc.) even when this guard runs. The unconditional
# `cat > .gitignore <<EOF` at the END of this step is the primary fix.
for entry in .gitignore .gitattributes; do
  git checkout HEAD -- "$entry" 2>/dev/null
done
# These may exist from previous commits — delete and git rm them
for dir in sessions memories memory memory_backup_* migration cache logs sandboxes cron/output; do
  [ -d "$dir" ] && { git rm -r --cached "$dir" 2>/dev/null; rm -rf "$dir"; }
done
rm -f gateway.lock gateway.pid auth.lock kanban.db.init.lock kanban.db.dispatch.lock
# Remove auth.json from tracking if it was committed in older backups
git rm --cached auth.json 2>/dev/null && echo "auth.json removed from tracking" || true
# === UNCONDITIONAL .gitignore WRITE (replaces the conditional block below) ===
# Why unconditional: the prior `[ ! -s .gitignore ] && cat > .gitignore` gated
# the write on the file being missing AND empty. rsync --delete on
# 2026-07-21 wiped .gitignore despite the pre-rsync guard + step-3-top guard
# (both restored it from HEAD), so the file was missing at the END of step 3
# anyway. Writing it from the canonical template unconditionally is the
# only reliable way to guarantee .gitignore is present and complete before
# `git add -A` in step 6. ~1ms cost; eliminates a class of backup failures.
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
# Verify the write actually landed (defensive: catches a permission or heredoc error)
test -s .gitignore && echo "OK .gitignore restored (canonical template)" || { echo "ERROR: .gitignore write failed — aborting"; exit 1; }
# Defense in depth: also restore from HEAD in case the rsync wipe happened mid-step
git checkout HEAD -- .gitignore 2>/dev/null
# End-of-step-3 verification: ensure file is non-empty (the unconditional write above guarantees this)
test -s .gitignore || { echo "ERROR: .gitignore lost during step 3 — aborting before step 4"; exit 1; }
for entry in auth.json .env .hermes_history gsc/client_secret.json gsc/token.json kanban.db.dispatch.lock; do
  if ! grep -qxF "$entry" .gitignore 2>/dev/null; then
    echo "$entry" >> .gitignore
  fi
done
sort -u .gitignore -o .gitignore
# Remove .env, .hermes_history from tracking if previously committed
git rm --cached .env 2>/dev/null && rm -f .env
git rm --cached .hermes_history 2>/dev/null && rm -f .hermes_history
git rm --cached gsc/client_secret.json 2>/dev/null && rm -f gsc/client_secret.json
git rm --cached gsc/token.json 2>/dev/null && rm -f gsc/token.json
git rm --cached kanban.db.dispatch.lock 2>/dev/null && rm -f kanban.db.dispatch.lock
```

### 4. Strip API keys from tracked files

**⚠️ Terminal display trap:** The terminal truncates long strings in the middle with `...` when printing.
`read_file` and `print(repr(line))` can SHOW `sk-8bc...87d2` while the ACTUAL FILE contains the full
key `sk-8bc...87d2`. Always verify with `xxd` / Python hex if in doubt.

**Use the bundled script** `scripts/redact_secrets.py` — it handles the walker + single-file fallback
in one place. **Don't use inline `python3 -c "..."` for redaction** — f-strings with nested braces
break in `terminal()` shell quoting. See `references/secret-redaction-verification.md` for
byte-level recipes for double-checking the script's output.

```bash
cd /tmp/demi-backup  # or /tmp/hermes-backup/ — any backup dir

# 4a. Truncate config.yaml + walk the entire tree for PAT/sk- tokens
python3 <skill_dir>/scripts/redact_secrets.py /tmp/demi-backup

# 4b. If the length-gated scan in step 5 finds a hit the walker missed
#     (typical case: CJK / non-ASCII directory paths), redact that one file directly:
#     IMPORTANT: pass the backup DIR as argv[1] and the file path as argv[2].
#     If you pass only the file path, the script interprets it as BATCH mode and
#     crashes with `os.chdir: NotADirectoryError`.
python3 <skill_dir>/scripts/redact_secrets.py /tmp/demi-backup "workspace/website/中文目录/文件.md"

# <skill_dir> = /home/ubuntu/.hermes/skills/devops/hermes-backup/  (or wherever the skill is installed)
```

**Alternative:** `scripts/redact_inprocess.py` runs from Python directly (no shell quoting,
broader extension coverage, doesn't require the skill to be installed yet). Useful for
`execute_code()` sessions where you want to redact before loading the skill.

The script handles:
- `config.yaml` — regex-truncates every `api_key: sk-...` to `api_key: sk-PREFIX...SUFFIX`
- Batch walker — recursively redacts PATs and sk- keys in all `.json/.yaml/.md/.txt/.py/.sh/.toml/.conf/.ini/.env` files,
  skipping `venv/`, `node_modules/`, `__pycache__/`, `website/`, `tests/`, `ui-tui/`, `.curator_backups/`, `.git/`
- Single-file mode — redaction on a specific path (the CJK recovery path)

**The script's print output ("Redacted N total") is NOT proof of completion.**
The step 5 length-gated grep scan is the only reliable verification. If it finds a hit,
re-run the script in single-file mode on that exact path, then re-scan. Loop until clean.

### 5. Check for remaining secrets — and LOOP if step 4 missed anything

**The simple `grep "sk-..."` scan in old revisions of this skill returns huge noise from `hermes-agent/venv/`, `hermes-agent/website/`, `hermes-agent/node_modules/`, and `hermes-agent/tests/`** (which all contain documentation/test fixtures and library code with `sk-` prefixes that aren't real keys). The reliable check is **length-gated regex with explicit denylist directories** — a `sk-...` placeholder has 5-10 chars total, a real fine-grained PAT has 100+ chars. Use the 40+ char threshold to filter out placeholders.

**This step is the ONLY reliable verification — step 4's print output can lie.** If step 5 flags any file, re-run step 4's redaction DIRECTLY on that path (do not re-run the full batch walker). Loop until step 5 reports zero hits.

For the PAT-specific 40+ char scan, prefer the dedicated `scripts/check_pats.py` helper over inline grep — it groups hits by `(prefix, last4, length)` so you can verify they're truncated placeholder form at a glance instead of drowning in `.curator_backups/*/cron-jobs.json` and skill-docs noise:

```bash
python3 <skill_dir>/scripts/check_pats.py /tmp/demi-backup
# → "OK No full PAT tokens found" if clean
# → "<prefix>...<last4> len=<N>  (M files)" with file list if not
```

```bash
cd /tmp/demi-backup
# Real-token scan: github_pat_ followed by 40+ chars (real fine-grained PATs are ~111 chars)
# Filters out: hermes-agent/venv, website, node_modules, ui-tui, tests, plus .curator_backups noise
NOISE='hermes-agent/venv\|hermes-agent/website\|hermes-agent/node_modules\|hermes-agent/tests\|hermes-agent/ui-tui\|\.curator_backups\|\.git/'
echo "=== Real github_pat_ tokens (40+ chars) ==="
HITS=$(grep -rln -E "github_pat_[a-zA-Z0-9_-]{40,}" \
  --include='*.json' --include='*.yaml' --include='*.yml' \
  --include='*.md' --include='*.txt' --include='*.py' \
  --include='*.sh' --include='*.toml' --include='*.conf' --include='*.ini' \
  . 2>/dev/null | grep -v "$NOISE" | head -10)
if [ -z "$HITS" ]; then echo "  OK No full PAT tokens found"; else echo "$HITS"; fi

echo "=== Real gh[pousr]_ tokens (40+ chars) ==="
HITS=$(grep -rln -E "gh[pousr]_[a-zA-Z0-9]{40,}" \
  --include='*.json' --include='*.yaml' --include='*.yml' \
  --include='*.md' --include='*.txt' --include='*.py' \
  --include='*.sh' --include='*.toml' --include='*.conf' --include='*.ini' \
  --include='*.js' --include='*.ts' --include='*.html' --include='*.css' \
  . 2>/dev/null | grep -v "$NOISE" | head -10)
if [ -z "$HITS" ]; then echo "  OK No full gh*_ tokens found"; else echo "$HITS"; fi

echo "=== Real sk- API keys (40+ chars) ==="
HITS=$(grep -rln -E "sk-[a-zA-Z0-9_-]{40,}" \
  --include='*.yaml' --include='*.yml' --include='*.json' \
  --include='*.py' --include='*.sh' --include='*.txt' --include='*.md' \
  --include='*.env' --include='*.toml' --include='*.conf' --include='*.ini' \
  --include='*.js' --include='*.mjs' --include='*.cjs' --include='*.jsx' \
  --include='*.ts' --include='*.tsx' \
  --include='*.html' --include='*.htm' --include='*.css' \
  --include='*.svg' --include='*.xml' \
  . 2>/dev/null | grep -v "$NOISE" | head -10)
if [ -z "$HITS" ]; then echo "  OK No full sk- API keys found"; else echo "$HITS"; fi

echo "=== Real Tavily tokens (tvly- followed by 40+ chars) ==="
# Added 2026-07-19: redact_secrets.py walker does NOT cover tvly-, and a
# real Tavily key (tvly-dev-sAFTx-...a7Si, 58 chars) was found in three
# MEMORY.md files. The walker redacted sk- and github_pat_ but left tvly-
# untouched, even though tvly- keys are 50+ chars and easily length-gated.
# Any time the walker reports a clean pass but the byte scan finds a
# non-sk-/non-PAT key, the fix is the same: add a provider-specific
# length-gated grep here. Future-proofing: include Cozy/SerpAPI/etc. prefixes
# the moment you see them once — they're already in the wild.
HITS=$(grep -rln -E "tvly-[a-zA-Z0-9_-]{40,}" \
  . 2>/dev/null | grep -v "$NOISE" | head -10)
if [ -z "$HITS" ]; then echo "  OK No full Tavily tokens found"; else echo "$HITS"; fi

echo "=== providers/ literal keys ==="
# JSON-walk for actual string values of length >= 40 (safer than regex on raw text,
# which can false-positive on field NAMES like "api_mode" or empty string values).
# 2026-07-20: the prior regex `'"[a-zA-Z0-9_-]*key": "[a-zA-Z0-9_-]{40,}"'` matched
# `providers/minimax_coding.json` because the file structure created a partial match;
# actual JSON-parse + value-length check produces zero false positives.
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
echo "Secret scan complete"

# LOOP GUARD: if the HITS variables are non-empty, the walker skipped files.
# Re-run redaction directly on each flagged file (do NOT re-run the full batch walker):
#   python3 -c "import re,sys; p=sys.argv[1]; c=open(p).read(); \
#     print(re.sub(r'sk-[a-zA-Z0-9_-]+', \
#       lambda m: m.group(0) if '...' in m.group(0) or len(m.group(0))<=15 \
#         else f'sk-{m.group(0)[3:9]}...{m.group(0)[-4:]}', c), end='')" "$f" > tmp && mv tmp "$f"
# Re-run the scan above. Repeat until both HITS variables are empty.

# Provider-prefix-aware inline redaction (NEW — added 2026-07-19):
# When the byte scan flags a token whose prefix the walker doesn't cover
# (e.g. tvly-, glpat-, AIza, xoxb-, AIzaSy), use this snippet INSTEAD of the
# sk-/-only one above. Pass `<prefix>` as `tvly`, `glpat`, etc. It truncates
# any `<prefix>-<base64-ish>` of length >= 30 to `<prefix>-AAAAAA...XXXX`.
# Write the recipe to /tmp first to dodge f-string + terminal quoting issues:
#   cat > /tmp/redact_prefix.py <<'PY'
#   import re, sys
#   prefix, p = sys.argv[1], sys.argv[2]
#   c = open(p, encoding='utf-8').read()
#   pat = re.compile(rf'{prefix}-[a-zA-Z0-9_-]+')
#   def _trunc(m):
#       s = m.group(0)
#       if '...' in s or len(s) < 30: return s
#       head = s[: 5 + len(prefix) + 6]   # "<prefix>-AAAAAA"
#       return f'{head[:-2]}...{s[-4:]}'
#   open(p, 'w', encoding='utf-8').write(pat.sub(_trunc, c))
#   print(f'redacted {prefix} in {p}')
#   PY
#   python3 /tmp/redact_prefix.py tvly workspace/website/MEMORY.md
# Re-run the relevant scan block. Loop until clean.
```

> **Verification tip:** A scan hit doesn't tell you whether the matched string is a real key or an already-truncated placeholder — both look identical on the terminal. Always confirm with `xxd` or a Python byte-length check before declaring clean. See `references/secret-redaction-verification.md` for the recipe.

### 6. Commit and push
```bash
TIMESTAMP=$(date '+%Y-%m-%d_%H:%M')
git add -A
git status --short | wc -l
echo "files staged — commiting"
# Reproduced 2026-07-16: tracked housekeeping files like .gitignore can
# silently land as `D` (deletion) instead of unchanged/M. Refuse to commit
# until they're restored — otherwise the next backup loses .gitignore
# entirely and the rsync --delete + short-exclude-list path blows up.
for entry in .gitignore .gitattributes; do
  STATUS=$(git status --short -- "$entry" | awk '{print $1}')
  if [ "$STATUS" = "D" ] || [ "$STATUS" = "??" ]; then
    echo "WARNING: $entry staged as $STATUS — restoring tracked version"
    git checkout HEAD -- "$entry" 2>/dev/null && git add "$entry"
  fi
done
git commit -m "Backup: $TIMESTAMP"
git push origin master
```

**Verify push succeeded:**
```bash
# Confirm the remote has the new commit
git fetch origin master
git log --oneline origin/master -1
echo "Pushed commit:"
git log --oneline -1
```

### 7. Cleanup
```bash
rm -rf /tmp/hermes-backup/
```

## References
- `references/cjk-walker-miss-recipes.md` — CJK-path walker miss: reproduction, three root-cause candidates, inline fallback scripts, byte-level verification
- `references/secret-redaction-verification.md` — xxd byte-level disambiguation recipes for the terminal-display-truncation trap
- `references/heavy-dir-leak-scenarios.md` — 2026-07-09 heavy-dir leak numbers (venv 456M, lsp 64M, website 27M, tests 26M, ui-tui 3.5M)
- `references/2026-07-20-session-notes.md` — today's three refinements: submodule `.gitmodules` missing, providers JSON false-positive fix, end-of-step-3 .gitignore re-verification
- `references/2026-07-21-session-notes.md` — cron SSH-only policy, `.gitignore` STILL wiped despite both pre-rsync and step-3-top guards (forced unconditional rewrite), 6th CJK walker miss + 4th tvly- miss, Chinese-summary delivery format requirement

## Scripts
- `scripts/redact_secrets.py` — unified batch walker + single-file mode (handles sk-, github_pat_, ghp_, gho_, etc.)
- `scripts/redact_inprocess.py` — same redaction logic, runnable from `execute_code()` without shell quoting
- `scripts/check_pats.py` — PAT placeholder vs full-token disambiguation helper (groups hits by `(prefix, last4, length)`)

## Exclusions (sensitive files/dirs)

| Path | Reason |
|------|--------|
| `.git/` | VCS metadata |
| `cache/` | Cached data, large |
| `audio_cache/` | Audio files |
| `image_cache/` | Image files |
| `sessions/` | Contains API keys in chat history |
| `memories/` | May contain sensitive config |
| `logs/` | Log files |
| `sandboxes/` | Sandbox environments |
| `gateway.lock` / `gateway.pid` | Runtime state |
| `state.db*` | State database |
| `auth.json` | Full API keys in credential store |
| `auth.lock` | Lockfile companion to `auth.json` |
| `.env` | Environment secrets |
| `.hermes_history` | Shell command log; has pasted credentials |
| `cron/output/` | Cron output logs may contain API key traces |
| `gsc/client_secret.json` | Google OAuth client secret |
| `gsc/token.json` | Google OAuth refresh token |
| `kanban.db.init.lock` | Kanban SQLite init lock (runtime state, like auth.lock) |
| `kanban.db.dispatch.lock` | Kanban dispatcher runtime lock (pairs with `kanban.db.init.lock` — both excluded together) |
| `models_dev_cache.json` | ~3MB model registry cache regenerated on every gateway tick |
| `hermes-agent/node_modules/` | Node dependencies, huge (100k+ files) |
| `lsp/node_modules/` | LSP server deps (typescript-language-server, pyright) |
| `**/node_modules/` | Catch-all for any other node_modules |
| `**/__pycache__/` | Python bytecode cache (covers hermes-agent + plugins) |
| `bin/uv` / `bin/tirith` | Generated compiled bundles; large and may embed token/private-key fixtures that text redaction cannot safely rewrite |

> **Note on runtime JSON files that are NOT excluded:** Several non-sensitive state files leak into every backup commit: `feishu_seen_message_ids.json`, `gateway_state.json`, `channel_directory.json`, `interrupt_debug.log`, `.install_method`, `.skills_prompt_snapshot.json`, `cron/ticker_heartbeat`, `cron/ticker_last_success`, `skills/.curator_state`, `skills/.usage.json`, `verification_evidence.db`. None contain secrets, but they churn every commit (~40 modified files per run). Adding them to the exclude list is optional — leave them tracked if you want a historical record of gateway/changelog activity, exclude them if you want minimal diffs. Other `bin/` tools may remain only after the raw-byte and staged-blob scans pass; `bin/uv` and `bin/tirith` are explicitly excluded.

## Pitfalls
- **Terminal display truncation trap** — The terminal (read_file / print / repr) truncates long strings in the 
  middle with `...`. A key displayed as `sk-8bc...87d2` is NOT necessarily truncated in the file — it may be the full
  35-char key `sk-8bc...87d2` with only the middle hidden. Always verify with Python hex (`val.hex()`) or `xxd`
  when checking whether keys are safe for GitHub. For byte-level disambiguation recipes (xxd worked example,
  Python byte-loop check, truncation script that handles both cases), see
  `references/secret-redaction-verification.md`.
- **API keys may contain `-` and `_` characters** — DeepSeek keys are hex-only (`a-zA-Z0-9`), but MinMax,
  Anthropic, and other providers use `-` and `_` in their keys (e.g. `sk-cp-lL-JHWT...`). The regex for scanning
  and truncation must use `[a-zA-Z0-9_-]` not just `[a-zA-Z0-9]` to catch all keys.
- **Active truncation required in cron context** — The old approach of "scan and warn" works when a user is
  present to respond, but cron backups run autonomously. Always use the automated truncation script in step 4,
  which replaces full keys with `sk-PREFIX...SUFFIX` format before commit.
- **PAT auth may fail** — GitHub fine-grained PATs expire, get truncated in messages, or are revoked. Always verify with `ssh -T git@github.com` first. SSH keys don't expire. If using a custom cred helper (e.g. `/tmp/git-cred-helper.py`), check it's still valid by running it: `echo "" | /tmp/git-cred-helper.py get | grep password`
- **Remote URL switching** — If cloned with HTTPS (PAT) and auth fails, switch to SSH: `git remote set-url origin git@github.com:qzw-alt/demi.git`
- **Credentials storage** — PATs are stored in two places: `~/.config/git/credentials` (credential store) and potentially `/tmp/git-cred-helper.py` (custom helper). Both must be updated when the PAT rotates. The custom helper is registered via `git config --global credential.https://github.com.helper /tmp/git-cred-helper.py`.
- **GitHub push protection** blocks commits containing `sk-*` API keys. Always strip them before committing, then scan with grep. Note: config.yaml keys are usually truncated (e.g. `sk-8bc...87d2`) which doesn't trigger push protection.
- **`rsync --delete` may warn** about non-empty directories from old backup artifacts. Just git rm + rm them manually.
- **`rsync --delete` can wipe the working tree's `.gitignore` if the source doesn't have one** — During rsync, if `~/.hermes/.gitignore` is absent (e.g., because the user never created one, or the file is `.gitignore` in root but not in `~/.hermes/`), the step's already-existing `.gitignore` from the previous commit gets deleted from `/tmp/<backup>/`, and step 3's append loop then creates a near-empty `.gitignore` containing only the 5 entries it adds. **Fix:** after rsync and before step 3, verify `.gitignore` exists in the working tree. If it's missing, immediately write the FULL exclusion list (caches, node_modules, **pycache**, secrets) rather than just augmenting it. A near-empty `.gitignore` allows sensitive files to be tracked by `git add -A` in step 6 even though they were excluded from rsync in step 2 — because git tracks them on subsequent commits when `.gitignore` doesn't list them.
- **auth.json is excluded entirely** from rsync (unlike the old approach of syncing then stripping). `auth.lock` (its companion lock file) should also be cleaned up.
- **hermes-agent/node_modules/ is huge** (~100k+ files). Exclude it from rsync to avoid timeouts (can take >60s otherwise). Same for `__pycache__/` directories.
- **config.yaml keys are usually truncated** (e.g. `sk-8bc...87d2`) — GitHub's secret scanning won't flag them. Only auth.json has full credential payloads.
- **providers/\\*.json** — May contain model configs without literal keys, but check anyway.
- **Amending history requires `--force` push** — fine for personal backup repos.
- **Large rsync timeout** — `rsync -a --delete` on a large ~/.hermes/ may take >60s. Use a 300s timeout or run in background.
- **Self-referential PAT leak in cron prompts** — When the user provides a PAT in the
  cron job's `prompt` field (e.g. "use this PAT to push: github_pat_..."), it gets stored
  verbatim in `cron/jobs.json`. The next backup will sync that file into the working tree.
  If step 4 doesn't redact it, the push will be blocked by GitHub's secret scanner AND the
  PAT will be exposed in the commit history (one commit before the block). The fix is the
  broad `grep -rl 'github_pat_' --include=...` sweep in step 4, which catches it regardless
  of which file holds the prompt. **Tell the user the PAT is compromised** if it was ever
  embedded in a committed prompt — assume it's leaked, even if the redaction succeeded.
  The PAT was visible in plaintext in the rsync source BEFORE redaction (which only writes
  to the working tree copy); the rsync source itself (`~/.hermes/cron/jobs.json`) is never
  modified, so the PAT there is still functional and must be rotated at
  https://github.com/settings/tokens?type=beta. **Action: tell the user to revoke + regenerate.**
- **__pycache__ lives outside hermes-agent/ too** — Plugins under `plugins/*/src/` and
  `plugins/*/socket/` generate `__pycache__/*.pyc` files. The skill's original exclusion
  only covered `hermes-agent/__pycache__/`, so plugin bytecode got committed in past
  backups. The `--exclude='**/__pycache__/'` and `--exclude='**/*.pyc'` rsync patterns
  fix this for new backups; for existing tracked files use `git rm -rf --cached <path>`.
- **auth.lock is auth.json's companion** — When `auth.json` is excluded from rsync, the
  `auth.lock` lockfile that pairs with it can still appear in the working tree on
  every backup (gateway runtime state). Exclude it alongside `auth.json`.
- **Temp directory name** — Can be any path like `/tmp/demi-backup/`; just be consistent across all steps. The absolute path matters for rsync source and repo destination paths.
- **`.hermes_history` is a plaintext credential trap** — This file (lives at `~/.hermes/.hermes_history`) contains a running log of shell commands and pasted content. Past entries include plaintext Feishu app secrets (`cli_a912890ce721dcee...`), pasted API keys in conversation snippets, and other credentials. It MUST be excluded from rsync AND removed from git history if previously committed. Add `--exclude='.hermes_history'` to the rsync invocation, and `git rm --cached .hermes_history` if it was tracked.
- **`gsc/client_secret.json` and `gsc/token.json` are Google OAuth secrets** — These files contain Google Search Console OAuth client secrets and refresh tokens. GitHub push protection blocks any commit containing them. Exclude from rsync (`--exclude='gsc/client_secret.json' --exclude='gsc/token.json'`), remove from tracking, and add to .gitignore. If a previous commit included them, the push will be rejected; use `git reset --soft HEAD~1 && git commit --amend --no-edit && git push --force-with-lease` to rewrite history. (`gsc/authorize.py` is safe to keep — it's just code.)
- **Force-push is required to rewrite history** — When push protection blocks a push because secrets leaked into a commit, you must rewrite local history (soft reset + amend, or filter-branch) then `git push --force-with-lease origin master`. Use `--force-with-lease` instead of `--force` to avoid clobbering concurrent pushes.
- **PAT auth may show false success on `git ls-remote`** — `git ls-remote` works on public repos without valid auth (it ignores bad credentials silently). The only real auth test is `git push` or `curl -H "Authorization: token <PAT>" https://api.github.com/user` (returns 200 = valid, 401 = invalid).
- **`lsp/node_modules/` is a separate `node_modules`, not under `hermes-agent/`** — The `~/.hermes/lsp/` directory (LSP language servers: typescript-language-server, pyright) has its own `node_modules/` with several hundred MB of dependencies. The original `hermes-agent/node_modules/` exclude missed it, so past backups may have grown large and slow. Always use `--exclude='**/node_modules/'` as the catch-all (added in step 2).
- **`x-access-token:` URL-embedded PAT silently fails for push** — Embedding `github_pat_xxx` as `https://x-access-token:PAT@github.com/owner/repo.git` works for `git clone` (download doesn't require auth on a public repo, or reads the URL credentials), but **`git push` returns `remote: Invalid username or token. Password authentication is not supported for Git operations.`** — GitHub removed password-style auth for fine-grained PATs in HTTPS push. The clone "succeeds" without prompting because git reads the embedded credentials, so the failure only surfaces at push time. **Always switch to SSH before pushing** when this error appears: `git remote set-url origin git@github.com:owner/repo.git`. Verify SSH works first with `ssh -T git@github.com`.
- **Truncation regex `[a-zA-Z0-9_-]{40,}` falsely matches across `...` markers** — A first-pass scan of `sk-[a-zA-Z0-9_-]{40,}` matches both `sk-kimi-iGU...NGGW` (the literal string with `...` in the middle) AND the full unredacted key (when checked against the source). When a second pass applies `re.sub(r'sk-[a-zA-Z0-9_-]{30,}', truncate, content)`, the regex matches the full token up to the first non-alphanumeric/underscore/dash char — which for a Chinese-context line may be a CJK character, mangling the output to `sk-kimi-i...配置中` instead of the intended `sk-kimi-i...NGGW`. Fix: in the replace function, check `'...' in m.group(0)` and skip those (they're already truncated), AND match against the unredacted source so the boundary is correct. Always verify with `xxd` on the first matched line before declaring clean.
- **Re-restore from source after a bad regex pass** — If a first-pass truncation script mangled some keys, don't try to fix them in place by guessing what the original was. Read the unredacted source from `~/.hermes/` (the rsync source, which still has the originals), apply the truncation there, and overwrite the bad file. Faster and less error-prone than trying to invert a corrupted regex.
- **Step 4 success message ("Redacted N") is not proof of completion — always re-scan** — In one session, the batch walker in step 4 reported processing files and printed "Redacted N total" for both PAT and sk- passes, but the post-step-5 scan still flagged a real 72-char `sk-kimi-i...NGGW` key in `workspace/website/德米知识库/01-记忆系统/MEMORY.md`. The walker silently missed that file even though a direct Python call against the same path succeeded. **Possible causes** (none fully isolated): (a) the `os.walk` iteration missed a CJK-path file due to a stale `dirs[:]` filter evaluation, (b) the file was re-overwritten by a subsequent operation between read and write, (c) a UnicodeDecodeError in the file content was swallowed by the `except (OSError, UnicodeError)` clause. **Fix:** never trust step 4's print output. Step 5's length-gated grep scan is the ONLY reliable verification — if it finds a hit, re-run the redaction DIRECTLY on that specific file path (not the batch walker), then re-scan. The pattern: `python3 -c "import re; p='./path/to/file'; c=open(p).read(); print(re.sub(r'sk-[a-zA-Z0-9_-]+', lambda m: m.group(0) if '...' in m.group(0) or len(m.group(0))<=15 else f'sk-{m.group(0)[3:9]}...{m.group(0)[-4:]}', c))" > tmp && mv tmp "$p"`, then re-grep. Loop until step 5 reports zero hits.
- **Combine PAT + sk- redaction into a single walker** — The original step 4 ran two separate Python scripts (one for `github_pat_*`, one for `sk-*`), each iterating the whole tree. If the first walker silently skips a file, the second walker might process it — but you can't tell which walker was responsible for any given redaction from the print output. Collapse them into one script that handles both token types per file, so the print output tells you exactly what each file got redacted. The unified walker is in step 4 below.
- **PATs leak into SKILL.md "known-failed token" notes** — When documenting a failed/expired PAT in a skill file, users often paste the *full* token inline (e.g. "PAT `github...Q5` returned 401") thinking the note is purely diagnostic. The full token is still plaintext in the file, and gets rsynced + committed. Mitigation: (a) when writing a SKILL.md, use placeholders like `github...PLACEHOLDER` not the real token; (b) when the backup finds a full PAT in any `.md`/`.yaml`/`.json`/`.txt` file, redact it the same way as `cron/jobs.json` — and flag the user that the token is exposed in skill docs.
- **Length-gated regex is required for secret scanning** — The pattern `sk-[a-zA-Z0-9_-]{16,}` matches `sk-xxx...xxxx` documentation placeholders (15 chars + the `sk-` prefix = matches). Use a 40+ char gate (real fine-grained PATs are ~111 chars; real Anthropic/OpenAI keys are 40+ chars) to filter out placeholders. Otherwise you'll either flood output with false positives from `hermes-agent/venv/`, `hermes-agent/website/`, and SKILL.md docs, or — worse — redact doc placeholders that aren't real secrets (mangling documentation).
- **grep output floods with `hermes-agent/venv/`, `hermes-agent/website/`, `hermes-agent/node_modules/` noise** — These directories contain library code, test fixtures, and Docusaurus docs that all have `sk-`, `github_pat_`, `gho_`, `ghp_` patterns as documentation/format descriptors. Always pipe secret-scan grep output through a `grep -v 'hermes-agent/venv\\|hermes-agent/website\\|hermes-agent/node_modules\\|hermes-agent/tests\\|hermes-agent/ui-tui'` filter (the step 5 scan does this). Note: filtering with `grep -v` only works if you use the right escape syntax — the `\|` alternation is GNU grep specific; on BSD/macOS use `grep -vE 'hermes-agent/(venv|website|node_modules|tests|ui-tui)'`.
- **Cron job prompt becomes the source of the next backup's PAT leak** — The recurring failure mode: user creates cron job with prompt like "use PAT github_pat_xxx to push". That prompt is stored verbatim in `~/.hermes/cron/jobs.json`. On every backup, `cron/jobs.json` is rsynced (not in the exclude list) and the full PAT lands in the working tree. Mitigation in the skill: step 4's Python PAT_RE.subn with a 40+ char gate catches and redacts this. Mitigation at the source: when writing a cron job prompt, never embed a PAT — use `ssh -T git@github.com` style auth, or read the PAT from a credential helper.
- **PAT-in-cron-prompt delivery advisory must be prominent, not buried** — When the redaction scan catches a `github_pat_*` in `cron/jobs.json` (or any other file path that originates from a cron prompt), the user-facing delivery response MUST lead with a security warning, not just say "backup complete". Specifically: (a) the PAT is still live in `~/.hermes/cron/jobs.json` — only the working-tree copy was redacted; (b) the rsync source has been visible in plaintext to every backup run that used this prompt — assume any prior backup attempt that failed redaction leaked it into git history; (c) recommend revoke + regenerate at https://github.com/settings/tokens?type=beta; (d) recommend rewriting the cron prompt to use SSH or a credential helper. Reproduced in 2026-07-11 run: 1 PAT caught in `cron/jobs.json` from this exact prompt.
- **Step 5's `--include` list was too narrow — silently missed the same files the walker missed** — Fixed 2026-07-11: the original list had only 10 extensions (`.yaml`, `.yml`, `.json`, `.py`, `.sh`, `.txt`, `.md`, `.env`, `.toml`, `.conf`, `.ini`). When the walker missed `bin/uv` (compiled binary), `hermes-agent/hermes_cli/web_dist/assets/index-CBTV-n-R.js` (97 redactions in one .js bundle), `workspace/website/blog/*.html` (3-10 sk- literals per file), and `.tsx`/`.css` under `hermes-agent/apps/`, the length-gated grep scan ALSO missed them because the `--include` filter excluded those extensions. **Both filters must cover the same set of extensions**, or the verification has a blind spot matched to the walker's blind spot. The new list adds `.js`, `.mjs`, `.cjs`, `.jsx`, `.ts`, `.tsx`, `.html`, `.htm`, `.css`, `.svg`, `.xml`. Re-verify whenever you add file types to the walker's `INCLUDE_EXT` — add them to step 5's `--include` list in the same commit.
- **`~/.hermes/.gitignore` does not exist by default — rsync --delete WILL wipe the working-tree .gitignore** — Reproduction 2026-07-11: the source `~/.hermes/` had no root `.gitignore`, so `rsync -a --delete` deleted the working-tree `.gitignore` (which step 3 had written on a previous backup). Without the `.gitignore`, `git add -A` would have staged `hermes-agent/venv/`, `lsp/node_modules/`, etc. — hundreds of MB — and the next commit would have been blocked by GitHub's 100MB file-size limit (would have failed entirely). The skill mentions this in passing but treats it as rare. **It is the rule, not the exception** — `~/.hermes/` almost never has a root `.gitignore` because the canonical one is written by this skill. **Always write the full canonical `.gitignore` IMMEDIATELY after `git clone` finishes, before any `git add`.** Don't rely on the step 3 logic that only triggers when `.gitignore` is missing-and-empty — use `cat > .gitignore <<EOF` UNCONDITIONALLY on first commit, or at minimum on every backup. Pre-populating from the previous commit is fine (the rsync --delete won't kill it if the source has it; if the source doesn't, write from the script).
- **`bin/uv` and `bin/tirith` compiled bundles must be excluded, not text-redacted** — A full-tree byte scan found long `sk-` strings in `bin/uv`, plus classic GitHub-token patterns and PEM private-key material in `bin/tirith`. Text walkers either skip binaries or risk corrupting executables, and these files are large/generated. Add `--exclude='bin/uv' --exclude='bin/tirith'` to rsync and both paths to `.gitignore`; remove already-tracked copies with `git rm --cached bin/uv bin/tirith`. Restore them through normal Hermes installation rather than Git backup. If binary restore completeness is required, use a dedicated artifact store with binary-aware secret scanning.
- **Text-only secret scans are insufficient — scan every file as bytes, then scan staged blobs** — Extension-gated walkers and grep both miss compiled binaries and unexpected file types. After normal redaction, recursively scan every non-`.git` file as raw bytes for at least: `github_pat_`, long `sk-`, classic `gh[pousr]_` tokens, Google `AIza` keys, AWS access IDs, Hugging Face tokens, Slack tokens, Stripe live keys, Telegram bot tokens, and JWTs. Report only paths/counts, never matched values. After `git add -A`, run the same patterns against staged blobs (`git show :<path>`): the index is what will actually be committed, so a clean working tree alone is not proof. Remove or redact every hit and repeat until both scans report zero.
- **Generic Google API keys need explicit handling** — The PAT/`sk-` redactor does not cover `AIza...` credentials. Include `AIza[0-9A-Za-z_-]{30,}` in the final byte scan and replace full values in the backup copy with a clearly truncated placeholder before staging. Never modify the rsync source during backup-copy redaction.
- **`.curator_backups/` directories accumulate with embedded PATs** — When the skills curator runs, it snapshots `cron/jobs.json` to `skills/.curator_backups/<timestamp>/cron-jobs.json`. If the cron prompt ever contained a PAT, every backup snapshot also contains it. These directories are *not* in the default rsync exclude list. Step 4's Python redaction script scans them (the `NOISE_DIRS` filter only excludes `hermes-agent/venv/`, `hermes-agent/website/`, `hermes-agent/node_modules/`, `hermes-agent/tests/`, `hermes-agent/ui-tui/`, and `.git/` — *not* `.curator_backups/`). The new commits will have redacted working-tree versions, even though the old commits in git history still contain the unredacted PATs (untouchable without force-push history rewrite).
- **`models_dev_cache.json` is a 3MB gateway cache, not user data** — Lives at `~/.hermes/models_dev_cache.json` and is regenerated on every gateway tick (model registry refresh). Rsyncing it commits a giant diff with no semantic value. Exclude it from rsync (`--exclude='models_dev_cache.json'`) and from .gitignore. Old backups may have committed it — `git rm --cached models_dev_cache.json` once to drop tracking.
- **`kanban.db.init.lock` is a runtime lock, not the kanban DB itself** — Pairs with `kanban.db` the way `auth.lock` pairs with `auth.json`. It's a 0-byte file written when the kanban SQLite is initialized, and shows up on every backup regardless of whether the kanban is in use. The kanban DB itself (`kanban.db`, ~114KB SQLite) IS tracked content — do NOT exclude it. But the `.init.lock` lockfile should be excluded via rsync and .gitignore.
- **`kanban.db.dispatch.lock` is a SIBLING runtime lock (added 2026-07-12)** — Pairs with `kanban.db.init.lock`. It surfaces alongside `.init.lock` in the gateway runtime state. Discovered when rsync's `--exclude='kanban.db.init.lock'` was set but `kanban.db.dispatch.lock` still leaked into the working tree — `rsync` root-level filename matching is brittle, and a sibling lock with a similar name is easy to miss when adding excludes. **Fix:** always exclude BOTH, add BOTH to .gitignore, and add BOTH to the post-rsync LEAK checklist. When you find one missing lockfile via `LEAK:` output, audit related filenames (`*.lock`, `*.pid`) for siblings — the same gateway subsystem typically emits them in pairs.
- **Walker hits `hermes-agent/venv/` and `hermes-agent/tests/`** — The skill's NOISE_DIRS list excludes these from the *walker* (so redaction isn't attempted on third-party code), but **rsync does NOT exclude them** by default. They live in the working tree, get added with `git add -A` if .gitignore misses them, and inflate commits by hundreds of MB of test fixtures / venv site-packages. The canonical .gitignore template above includes `**/node_modules/`, `**/__pycache__/`, and `**/*.pyc` which covers the worst of it, but a strict repository should also exclude `hermes-agent/venv/`, `hermes-agent/tests/`, `hermes-agent/website/`, `hermes-agent/ui-tui/` outright if they're not needed for backup. Verify with `git status --short | wc -l` before commit — if it's in the thousands, .gitignore isn't catching something.
- **Default git clone over SSH may take >60s — `timeout 240` does NOT save you** — The first clone of a populated `qzw-alt/demi` repo (1.2GB working tree, hundreds of commits) routinely exceeds the 60s foreground timeout in `terminal()`. **Reproduction 2026-07-13:** `terminal("timeout 240 git clone git@github.com:qzw-alt/demi.git .")` STILL timed out at 60s (exit_code 124) — the shell-level `timeout` does NOT bypass the foreground `terminal()` wrapper's hard cap; the wrapper kills the process at 60s regardless of what the inner shell says. **You MUST use `background=true` + `notify_on_complete=true` + a generous `timeout` parameter (e.g. 600)** for any first-time SSH clone. After the first clone, `git pull` updates are fast (a few seconds) and the foreground form is safe again. Recipe:
  ```bash
  # WRONG — will still hit 60s cap:
  terminal("timeout 240 git clone git@github.com:qzw-alt/demi.git .")

  # RIGHT — background process with notify:
  terminal(background=true, notify_on_complete=true, timeout=600,
           command="rm -rf /tmp/demi-backup/ && mkdir -p /tmp/demi-backup/ && cd /tmp/demi-backup && git clone git@github.com:qzw-alt/demi.git .")
  # then process(action="poll"|"wait", session_id=..., timeout=300) — wait is clamped to 60s; use repeated poll
  ```
  After the first clone, subsequent updates via `git pull` are fast. **Always default to background mode for the first clone — don't bother trying the foreground form first.**
- **Heavy dirs will leak through short user exclude lists — see `references/heavy-dir-leak-scenarios.md`** for the 2026-07-09 numbers (venv 456M, lsp 64M, website 27M, tests 26M, ui-tui 3.5M that all leaked through a typical 11-path user exclude list and were saved only by step 3's canonical .gitignore).
- **rsync `--exclude='models_dev_cache.json'` does NOT always exclude a root-level file** — In one session the file was rsynced into the working tree despite the exclude pattern being set. Rsync's exclude rules can be confused by file-vs-component matching at the source root. **Always verify the file is absent after rsync** (`test -e path && echo PRESENT`); if it leaked through, manually `rm -f` it AND `git rm --cached` it. Don't trust the exclude to have caught it. Same risk applies to any other root-level dotfile/lockfile the user lists as a bare filename (e.g. `auth.json` in some rsync versions). **This bites `kanban.db.dispatch.lock` too** — when adding excludes for sibling lockfiles, always verify with `[ -e "$file" ] && echo LEAK: $file` in the post-rsync check, even if you trust rsync's pattern matching.
- **User-supplied exclude lists are often smaller than the canonical one — verify heavy dirs aren't in the working tree** — When a user gives a short exclude list (e.g. only the ~10 paths from a cron prompt), the skill's canonical heavy-directory excludes (`hermes-agent/venv/`, `hermes-agent/website/`, `hermes-agent/tests/`, `hermes-agent/ui-tui/`) may NOT be in the user's list. After rsync, ALWAYS check: `for d in hermes-agent/venv hermes-agent/website hermes-agent/tests hermes-agent/ui-tui; do test -e "$d" && echo "HEAVY: $d"; done`. If any are present, add them to .gitignore (the skill's template includes them) and confirm `git ls-files` shows 0 tracked files in those dirs before commit. If gitignore is missing or incomplete, `git add -A` will commit hundreds of MB of venv/test fixtures.
- **CJK-path files (Chinese / Japanese / Korean directory names) silently bypass the os.walk walker — EXPECTED, not rare (reproduced 2026-07-08, 2026-07-13, 2026-07-14, 2026-07-16, 2026-07-17, 2026-07-21 — 6 confirmed runs in a row)** — This is now a known recurring failure mode of the walker, not a one-off. In 2026-07-14 the walker reported 580 redactions across 163 files but step 5 length-gated scan still found 1 real 72-char `sk-kimi-i...NGGW` key in `./workspace/website/德米知识库/01-记忆系统/MEMORY.md`; the same exact path was the only walker-missed file in the 2026-07-17 run even though that day's commit was only 15 files modified (a "clean" run with little source activity still reproduces it). In 2026-07-21 the same path was missed again, alongside the `tvly-` walker miss (also on that exact file). The CJK-encoded path is consistently skipped by `os.walk` for an unknown reason (possibly a stale `dirs[:]` filter, possibly a UnicodeDecodeError swallowed by `except (OSError, UnicodeError)`, possibly a broken path encoding in the scandir backend). **The miss is independent of total commit size** — even a quiet week with minimal source churn reproduces it. **Workflow consequence:** the post-rsync step 5 length-gated grep scan is NOT optional — it is the only reliable verification, and it MUST run every backup regardless of how small the working tree change looks. Plan for at least one CJK-path miss per backup and budget the single-file redaction round-trip accordingly. **Fix:** when step 5 finds a hit, re-run redaction DIRECTLY on the specific file path with `python3 <skill_dir>/scripts/redact_secrets.py <backup_dir> <file>`, NOT the batch walker. Loop until step 5 reports zero hits. The arg order is `<backup_dir> <file>` (NOT just `<file>` — passing only the file triggers BATCH mode and crashes with a misleading `NotADirectoryError`; see the single-file-mode arg-order pitfall below). See `references/cjk-walker-miss-recipes.md` for the full reproduction, three root-cause candidates, the inline fallback script, and the byte-level verification recipe.
- **`redact_secrets.py` single-file mode arg order trap** — The script requires `<backup_dir> <file>` for single-file mode (NOT just `<file>`). If you accidentally invoke `python3 redact_secrets.py "/path/to/cjk/file.md"` (one positional arg), it interprets that as BATCH mode, then crashes at `os.chdir(BACKUP_DIR)` with `NotADirectoryError: [Errno 20] Not a directory: '/path/to/cjk/file.md'`. The error is misleading because it points at the FILE path, not the script's argument parsing. **Fix:** always pass the backup directory as `argv[1]` and the file as `argv[2]`. The script now validates `os.path.isdir(BACKUP_DIR)` up front and exits with a clear usage message instead of a cryptic chdir error. Reproduction in 2026-07-10 session: first single-file redact attempt failed with the misleading traceback; recovery was to write `/tmp/redact_one.py` and run that instead. Now patched, but the lesson generalizes: when an error message points at a path, check whether the script is using the wrong argument as a directory.
- **Inline Python via `terminal()` breaks on f-strings with `{` `}` in shell quoting** — `terminal("python3 -c \"...f-string...\"")` consistently mangles nested f-strings because the shell and Python both interpret braces. The first redaction attempt in 2026-07-08 session failed with `NameError: name 'm' is not defined` from a broken f-string. **Fix:** always write the redaction script to a file (e.g. `/tmp/redact_one.py` or `/tmp/redact_keys.py`) using `write_file`, then `terminal("python3 /tmp/redact_one.py <path>")`. The script file is also reusable across re-runs without re-typing.
- **PAT leak in cron prompt is the most common secret exposure path — treat it as expected, not surprising** — In the 2026-07-08 session the user's own cron prompt embedded a `github_pat_...` token, which the walker caught (1 PAT redaction in `cron/jobs.json`). The skill already documents this in pitfalls, but the user-facing **delivery response** should make the revocation warning prominent, not buried: "The PAT in this cron prompt has been redacted in this commit, but the source file `~/.hermes/cron/jobs.json` still contains the live token. Revoke + regenerate at https://github.com/settings/tokens?type=beta." The PAT was visible to the rsync source on every prior backup attempt; the only thing that changes is whether it's now visible in the working tree, which is fixable. The source itself is the leak.
- **PAT placeholder vs full-token disambiguation takes a dedicated helper (added 2026-07-12)** — When step 5's `grep -rln` lists many `.md` files containing `github_pat_` (typically all `skills/*/SKILL.md` plus `.curator_backups/*/cron-jobs.json` snapshots), the assistant can't tell from grep alone whether each match is a real 100-char token or an already-truncated `github...XXXX` placeholder — both render identically in terminal output. **Fix:** use `scripts/check_pats.py` (bundled) which extracts `(prefix, last4, length)` from each hit and reports per-signature counts. If every hit has `length < 40`, the placeholder form is already safe; if any hit has `length >= 40`, treat it as a live PAT and run single-file redaction on the exact path. The script also filters out the standard noise dirs and skips binary blobs (files with `\\x00` in the first 8KB), so it produces a clean yes/no answer that doesn't require manually eyeballing dozens of `.curator_backups` snapshots.
- **PAT supplied in cron prompt is INVALID (401), not just leaked — fall back to SSH (reproduced 2026-07-13, 2026-07-14, 2026-07-16, 2026-07-17)** — A distinct case from the existing "PAT leak" pitfalls: the cron prompt embeds a PAT that is **dead on arrival** — `curl -H "Authorization: token <PAT>" https://api.github.com/user` returns HTTP 401 before any backup operation starts. This means: (a) the user thinks they're providing a working token but it has been rotated/revoked since they last used it; (b) the existing "PAT-in-cron-prompt delivery advisory" guidance about revoking a leaked PAT doesn't apply because there's no working PAT to revoke — the user just needs to know it's invalid and that the backup succeeded via SSH key instead. **Workflow adjustment:** at step 0 (auth verification), explicitly curl-test the user-supplied PAT (or any PAT found in `~/.config/git/credentials`) before relying on it. If 401, IMMEDIATELY fall back to SSH (`ssh -T git@github.com` check) and proceed with SSH for clone + push. The user-facing delivery response should clearly distinguish three PAT cases: **(A) PAT invalid/dead (401)** → tell user the embedded PAT is no longer valid, recommend rewriting the cron prompt to use SSH (which was working) and stop embedding PATs; **(B) PAT valid but leaked in commit history** → existing revoke+regenerate advisory; **(C) PAT redacted cleanly, no prior leak** → no advisory needed. Don't conflate (A) with (B) — case A means the rsync source `cron/jobs.json` contains an INVALID token, not a live one, so there's nothing to revoke. Just clean it up and migrate the cron to SSH. **Reproduction count: 4 confirmed runs (2026-07-13, 2026-07-14, 2026-07-16, 2026-07-17)** — this is now the expected case, not the rare one. If you see a PAT in a cron prompt, default-assume it's dead until curl-test proves otherwise, and lead the delivery response with the "rewrite the cron prompt to use SSH" advisory.
- **Runtime state files leak by design but cause commit churn** — Discovered 2026-07-12: even with a fully populated .gitignore, ~40 files show up as `M` (modified) in every backup because they're runtime state that changes every cron tick. The ones observed: `feishu_seen_message_ids.json`, `gateway_state.json`, `channel_directory.json`, `interrupt_debug.log`, `.install_method` (small, harmless), `.skills_prompt_snapshot.json`, `cron/ticker_heartbeat`, `cron/ticker_last_success`, `skills/.curator_state`, `skills/.usage.json`, `verification_evidence.db`. They contain no secrets but pollute the commit history. **Decision:** leave them tracked (they serve as a coarse uptime/activity log); only exclude them if the user asks for "minimal diffs" backups. Don't try to whitelist — the list grows whenever a new gateway subsystem is added, and a missed one is harmless because none are sensitive.
- **"Redacted-at-source" files preserve secrets in committed `***` form (2026-07-14)** — Some files in `~/.hermes/` are committed with secrets already stripped at the source, e.g. `workspace/oriental-destiny/config.real.js` contains `apiKey: ***` (not the real value), `workspace/oriental-destiny/config.real.example.js` contains `apiKey: "AIzaSy-your-real-api-key-here"` (29 chars, documentation placeholder). These files will appear "clean" in the length-gated scan but the **rsync source is the source of truth** — if the user ever un-redacts them on disk before a backup, the leak will land in the next commit. The walker doesn't need to touch these files (the literals are already short), but be aware: a redaction scanner that reports "all clean" can give false confidence when the *source* is what's broken. The redaction is one-directional (working-tree copy); the rsync source itself is never modified. This pairs with the "source itself is the leak" PAT-in-cron-prompt pattern.
- **Git submodules are invisible to the parent repo's commit (2026-07-19)** — `workspace/oriental-destiny/` and `hermes-agent/` show up in `git ls-tree HEAD` as mode `160000` (submodule gitlinks). The parent's `git add -A` records ONLY the submodule commit SHA, not the submodule's internal files. Reproduced: rsync brought over `workspace/oriental-destiny/config.real.js` containing an `AIzaSy...` Google key, the step-5 byte scan flagged it, and only after a wasted round-trip did I realize `git ls-files` returned empty for that path and `git check-ignore` returned `fatal: Pathspec 'config.real.js' is in submodule 'workspace/oriental-destiny'`. **Implication for the byte scan:** any hit inside a submodule directory is NOT going to land in the parent's commit — `git show :<path>` will fail with the same `is in submodule` error. So they don't need redaction FOR THIS BACKUP. **However:** (a) don't waste cycles investigating them; treat submodule-internal hits as informational, not blockers; (b) the SUBMODULE'S OWN integrity is tracked by its own commit SHA in the parent, so corruption or secret re-injection inside the submodule is captured by the parent's gitlink (`git submodule status` would show a dirty SHA) — let `git status` flag submodule status changes rather than the byte scanner. **Workflow:** identify submodules FIRST via `git ls-files --stage | awk '$1=="160000"{print $4}'`, then add them to the noise filter: `for sm in $SUBMODULES; do NOISE="$NOISE|$(echo $sm | sed 's|/|\\/|g')"; done`. Use this expanded NOISE in the step-5 grep pipe so submodule paths produce zero false positives.
- **Tavily keys (`tvly-`) bypass the walker entirely (2026-07-19)** — `redact_secrets.py` covers only `sk-` and `github_pat_`. A real Tavily key `tvly-dev-sAFTx-...` (58 chars) was found in three `MEMORY.md` files after a "clean" walker pass — the walker scanned 161 files and redacted 584 sk- keys but left tvly- untouched. Real Tavily keys are 50+ chars and trivially length-gate-able; the walker simply lacks the regex. **The walker is NOT a complete provider list** — it covers what Hermes itself uses; user notes (`MEMORY.md`, skill docs, scratch files) document any provider the user has ever touched. **Fix:** step 5's grep scan block now includes a dedicated `tvly-` (40+ chars) line. When a future non-handled provider prefix surfaces, add a new length-gated grep block for it AND use the `redact_prefix.py` snippet (added to the LOOP GUARD section above) to truncate without re-running the batch walker.
- **`.gitignore` can be silently deleted by the step-3 cleanup loop and get COMMITTED as a deletion (reproduced 2026-07-16)** — A distinct failure mode from the existing "`~/.hermes/` has no `.gitignore` so rsync --delete wipes the working-tree one" pitfall: even when the working tree starts with a fully populated, tracked `.gitignore` (written by step 3 of the *previous* backup), the *current* backup's step-3 loop can lose it. Reproduction 2026-07-16: rsync ran (source had no `.gitignore`, so `--delete` did not affect the working-tree one — it survived). Then step 3's `for dir in sessions memories memory memory_backup_* migration cache logs sandboxes cron/output; do [ -d "$dir" ] && { git rm -r --cached "$dir" 2>/dev/null; rm -rf "$dir"; }; done` did NOT match `.gitignore` (good). But the loop's `git rm -r --cached` on tracked directories + the subsequent `git add -A` in step 6 staged `.gitignore` for *deletion* because by then the working tree's `.gitignore` had been overwritten by something (most likely: rsync's earlier pass brought in the source's missing `.gitignore` as an empty/non-existent file, or a prior step's redact script wrote 0-byte output that clobbered it). The commit succeeded with `delete mode 100644 .gitignore`. After the push I had to manually restore it: `git checkout HEAD~1 -- .gitignore`. **Fix (defense in depth, do all three):** (1) Immediately after `git clone` and BEFORE rsync, write the canonical `.gitignore` UNCONDITIONALLY (the existing pitfall already says this; now add a verification step at the END of step 3): `test -s .gitignore || { echo "ERROR: .gitignore lost during backup — restoring from prior commit"; git checkout HEAD~1 -- .gitignore 2>/dev/null; test -s .gitignore || cat > .gitignore <<'EOF' ... full canonical template ... EOF; }`. (2) In step 6 (after `git add -A` but before `git commit`), verify `.gitignore` is staged as an update or unchanged — NOT as a deletion: `git status --short .gitignore` should never show `D .gitignore`. If it does, `git checkout HEAD -- .gitignore && git add .gitignore` to restore the tracked version before committing. (3) Add `.gitignore` to the step-3 cleanup loop's explicit DO-NOT-DELETE list at the top: `for entry in .gitignore .gitattributes; do git checkout HEAD -- "$entry" 2>/dev/null; done` before the `git rm -r --cached` loop runs. This is the cheapest fix — it runs in <1s and prevents the silent deletion regardless of which earlier step wiped the file.
- **PAT-in-cron-prompt Case A is now reproduced FIVE times (2026-07-13, 2026-07-14, 2026-07-16, 2026-07-17, 2026-07-21) — the user has not yet rewritten the cron job** — Across five consecutive daily backup runs the cron prompt has embedded the same dead `github_pat_11B67EO2Y0...Q5` token, returning HTTP 401 on every auth check, and the cron prompt is still being delivered unchanged. This is no longer an edge case worth re-explaining — it is the expected state. **Workflow consequence:** when a cron prompt contains a `github_pat_` token, skip the advisory about "use SSH instead" in the body of the delivery and put it as the **lead sentence** of the response. The user's action item (rewrite the cron job) has not been acted on across 5 runs; a buried advisory won't get seen. Suggested lead template: "**ACTION NEEDED: Your cron job still embeds a dead PAT (`github...Q5`, HTTP 401 on five consecutive runs). Rewrite the cron prompt to use SSH auth — `git clone git@github.com:qzw-alt/demi.git` works without a token.** Backup pushed via SSH: ..." Then continue with the rest of the report. The PAT itself is dead so there's nothing to revoke (Case A); the only fix is rewriting the cron job source. **2026-07-21 update:** today's cron prompt in fact DID add a SSH-only policy (禁止使用 HTTPS、PAT、credential URL) — that's a partial fix in the right direction (the prompt now bans new PAT use), but the embedded dead `github_pat_` token itself is still in the prompt body, which is what triggers the 401. The user added the SSH ban without first removing the dead PAT from the prompt. Lead the response with both: (a) the dead-PAT rewrite needed, and (b) the SSH-only policy is correctly applied (good).
- **Submodule `.gitmodules` may be missing in cloned backup repo — `git submodule status` errors, do NOT treat as fatal (2026-07-20)** — Confirmed reproduction today: `git ls-files --stage | awk '$1=="160000"'` listed `hermes-agent` and `workspace/oriental-destiny` as gitlinks, but `git submodule status` returned `fatal: no submodule mapping found in .gitmodules for path 'hermes-agent'`. This is NOT a backup-breaking error — the parent repo's `git add -A` will still record the gitlink (SHA) update for any submodule whose working tree changed, even with no `.gitmodules` present. **Implications:** (a) `git check-ignore` on a path inside a submodule will return `fatal: Pathspec ... is in submodule 'hermes-agent'` (not "ignored"), so use `git ls-files` to confirm a path is untracked instead of `git check-ignore`; (b) `git show :<path>` for a submodule-internal path also returns "is in submodule" — the staged-blob scan must skip submodule paths entirely; (c) when adding submodules to the step-5 NOISE filter, get the list via `git ls-files --stage | awk '$1=="160000"{print $4}'` BEFORE running grep, so a missing `.gitmodules` doesn't break the filter expansion. The 2026-07-19 submodule pitfall covers (a) and (b) but doesn't mention (c); without the pre-step-5 submodule discovery, today's run would have flagged submodule paths as noise-source positives when they aren't actually staged.
- **End-of-step-3 `.gitignore` re-verification is mandatory, not optional (2026-07-20 reproduction)** — Today's run: rsync ran, `for entry in .gitignore .gitattributes; do git checkout HEAD -- "$entry"; done` was NOT in the cloned repo's working tree at step-3 entry (it had run earlier, in a custom `git checkout HEAD -- .gitignore .gitattributes` I added between steps 1 and 2 — but the skill's documented step-3 guard ran the same command, so it should have been safe). Then `ls .gitignore` reported "No such file or directory" — meaning the rsync --delete had wiped it despite the early guard. The skill's 2026-07-16 pitfall fix-3 (run `git checkout HEAD -- .gitignore` before the cleanup loop) is necessary AND sufficient, but **only if step-2's rsync didn't wipe the file BEFORE step-3 ran**. Confirmed today: the issue was that the skill's step-2 verification script ran AFTER rsync, then `git checkout HEAD -- .gitignore` was called at the top of step-3, then `ls .gitignore` STILL failed — meaning rsync --delete ran AGAIN somewhere, OR a parallel rsync was running. The robust fix: after step-3's cleanup loop, verify `.gitignore` is non-empty AND matches the prior commit's blob: `test -s .gitignore && git diff --quiet HEAD -- .gitignore || { echo "ERROR: .gitignore mismatch — restoring"; git checkout HEAD -- .gitignore; }`. Run this verification AFTER the `for dir in sessions memories ...` cleanup loop AND BEFORE step-4 redaction (which doesn't touch .gitignore but doesn't fail if it's missing). **Add this line at the END of step 3, not the beginning** — at the beginning, rsync may still wipe the file; at the end, all subsequent steps assume .gitignore is present and correct.
- **`providers/*.json` literal-key regex false-positives on JSON structure, not just values (2026-07-20)** — The canonical step-5 line `grep -q -E '"[a-zA-Z0-9_-]*key": "[a-zA-Z0-9_-]{40,}"' providers/*.json` matched `providers/minimax_coding.json` despite the file containing zero actual key values — the field-name pattern matched part of `"api_mode"` because `_mode` matched `[a-zA-Z0-9_-]*` and `:` matched `:`. JSON-walking for string values of length ≥ 40 produces zero false positives and is more reliable. The fix above (replace the grep with the python walker) is now in step 5. **Generalization:** any regex-based "is this a secret" check on JSON files should JSON-parse first, then walk for string values; don't trust surface regex on serialized JSON.
- **`.gitignore` STILL got wiped despite the pre-rsync guard AND the step-3 top guard (reproduced 2026-07-21, 7th confirmed run of the gitignore-loss pattern)** — Today's run added belt-and-braces: pre-rsync `git checkout HEAD -- .gitignore .gitattributes`, then step-3-top same command, then the [existing pitfall's] "verify at end of step 3" check. None of them prevented the file from being missing at the end of step 3. Root cause unclear — most likely a second rsync --delete pass ran during the step-2 verification, or a parallel cron-launched rsync was in flight, or some gateway process rewrote it. **Fix:** the unconditional `cat > .gitignore <<EOF` write that now lives at the END of step 3 (added 2026-07-21) is the primary defense. It does not try to restore from HEAD — it WRITES the canonical template fresh every backup. This guarantees the file is present and complete before `git add -A` regardless of which earlier step wiped it. Cost: ~1ms. The other guards (pre-rsync, step-3-top) remain as belt-and-braces, but no longer need to be considered load-bearing.
- **Cron-context SSH-only policy overrides the skill's PAT fallbacks (added 2026-07-21)** — If the cron prompt explicitly bans HTTPS / PAT / credential-URL auth (e.g. "禁止使用 HTTPS、PAT、credential URL" or "SSH 不可用时直接报告失败，不要改用 PAT"), the skill's existing PAT-fallback guidance in steps 0 and 1 ("If only a PAT is available, clone with `https://USER:PAT@github.com/...`"; "renew the PAT by editing `~/.config/git/credentials`"; "use a custom credential helper") does NOT apply. Do NOT silently substitute a PAT, do NOT generate a new PAT, do NOT use a credential helper even if `~/.config/git/credentials` has one. When SSH fails in this context, abort and lead the delivery response with: "SSH auth unavailable — backup aborted per cron policy. Restore SSH key to `~/.ssh/id_ed25519.pub` and re-test with `ssh -T git@github.com`." The user imposed the restriction for a reason (preventing future PAT leaks in cron prompts); honoring it is more important than completing the backup. Reproduced today: cron prompt has the SSH-only policy + still embeds a dead PAT — the SSH path worked perfectly; no PAT fallback was needed.
- **Cron-prompt delivery format is part of the contract (added 2026-07-21)** — Cron prompts often specify a required delivery format (e.g. "输出中文简报：认证方式、结果、远程提交哈希、敏感扫描结果"). Follow the prompt's format requirement exactly, including output language. Don't default to English when the prompt is in Chinese; don't include extra sections the prompt didn't ask for; lead with the action items (e.g. "rewrite cron prompt to remove dead PAT") rather than burying them in prose. The skill's existing pitfall about "PAT-in-cron-prompt advisory must be prominent, not buried" reinforces this — the lead sentence is the action item, the body is the backup report.
