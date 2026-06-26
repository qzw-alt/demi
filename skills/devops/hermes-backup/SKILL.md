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
# Prefer SSH key auth — verify it works
ssh -T git@github.com 2>&1 | grep -q "successfully authenticated" && echo "SSH OK"
# Check credential store
cat ~/.config/git/credentials 2>/dev/null | head -1 || echo "No credential store"
# Check for custom credential helpers
git config --global --get-all credential.https://github.com.helper 2>/dev/null
git config --global --get credential.helper 2>/dev/null
# Check known helper scripts
ls /tmp/git-cred-helper.py 2>/dev/null && echo "Custom cred helper found: /tmp/git-cred-helper.py"
```

If neither works, set up SSH: `ssh-keygen -t ed25519 -C "backup" && cat ~/.ssh/id_ed25519.pub` and add to GitHub.
If the credential store has an expired PAT, renew it by editing `~/.config/git/credentials` (or the custom helper script) with a new fine-grained token. Generate PAT at https://github.com/settings/tokens?type=beta with repo:Contents:Write scope.

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
  --exclude='cron/output/' \
  --exclude='hermes-agent/node_modules/' \
  --exclude='hermes-agent/__pycache__/' \
  --exclude='hermes-agent/**/__pycache__/' \
  --exclude='.env' \
  /home/ubuntu/.hermes/ /tmp/hermes-backup/
```

### 3. Remove old sensitive artifacts from previous backups
```bash
cd /tmp/hermes-backup
# These may exist from previous commits — delete and git rm them
for dir in sessions memories memory memory_backup_* migration cache logs sandboxes cron/output; do
  [ -d "$dir" ] && { git rm -r --cached "$dir" 2>/dev/null; rm -rf "$dir"; }
done
rm -f gateway.lock gateway.pid auth.lock kanban.db.init.lock
# Remove auth.json from tracking if it was committed in older backups
git rm --cached auth.json 2>/dev/null && echo "auth.json removed from tracking" || true
# Add auth.json to .gitignore so rsync doesn't re-expose it as untracked
if ! grep -q '^auth.json$' .gitignore 2>/dev/null; then
  echo "auth.json" >> .gitignore
  sort -u .gitignore -o .gitignore
  echo "auth.json added to .gitignore"
fi
```

### 4. Strip API keys from tracked files
```bash
cd /tmp/hermes-backup
# config.yaml keys are usually truncated (sk-8bc...87d2 format) and safe for GitHub.
# DO NOT attempt sed-based stripping — complex quoting breaks in bash and destroys truncated keys.
# Instead, scan for non-truncated keys and warn if any are found:
python3 << 'PYEOF'
import re, glob
full_keys = []
for f in ['config.yaml'] + glob.glob('providers/*.json'):
    try:
        with open(f) as fh:
            for i, line in enumerate(fh, 1):
                m = re.search(r"api_key:\s*['\"]?(sk-[a-zA-Z0-9]{20,})['\"]?", line)
                if m and '...' not in m.group(1):
                    full_keys.append(f'{f}:{i}')
    except FileNotFoundError:
        pass
if full_keys:
    print('WARNING: full API keys found — strip manually:')
    for k in full_keys: print(f'  {k}')
else:
    print('config.yaml keys are truncated or empty — safe for GitHub')
PYEOF
# auth.json is excluded from rsync entirely (--exclude='auth.json' in step 2),
# so no stripping needed. If it was previously committed, remove it in step 3.

# Remove .env from tracking
git rm --cached .env 2>/dev/null; rm -f .env

# Check providers/ for literal keys (env var refs like env:DEEPSEEK_API_KEY are safe)
for f in providers/*.json; do
  [ -f "$f" ] && grep -q '"api_key": "[a-zA-Z0-9]\{16,\}"' "$f" && \
    echo "WARNING: literal API key in $f — strip manually!"
done

# Redact PAT tokens from cron job definitions (prompt fields may contain embedded tokens)
for f in cron/jobs.json skills/.curator_backups/*/cron-jobs.json; do
  [ -f "$f" ] && grep -q 'github_pat_' "$f" && \
    sed -i 's/github_pat_[a-zA-Z0-9_-]*/[PAT_REMOVED]/g' "$f" && \
    echo "Redacted PAT in $f"
done
```

### 5. Check for remaining secrets
```bash
cd /tmp/hermes-backup
# Check for sk-* API keys in tracked source files
grep -rn "sk-[a-zA-Z0-9]\{20,\}" --include='*.{yaml,yml,json,py,sh,txt,md,env,toml,conf,ini}' . 2>/dev/null | grep -v '.git/' | head -10
# Check for env-var-style API keys with actual values (not just env:VAR references)
grep -rn "DEEPSEEK\|OPENAI\|ANTHROPIC.*API\|HF_TOKEN\|HUGGINGFACE" --include='*.{yaml,yml,json,py,sh,txt,md,env}' . 2>/dev/null | grep -v '.git/' | grep -v ':\s*$' | head -10
# Check providers/ for any literal keys
for f in providers/*.json; do
  [ -f "$f" ] && grep -q '"[a-zA-Z0-9_]*key": "[a-zA-Z0-9]\{16,\}"' "$f" 2>/dev/null && \
    echo "POTENTIAL KEY: $f — review and strip"
done
# Check for github_pat_ tokens in tracked JSON/YAML files
echo "=== Scan for GitHub PAT tokens ==="
grep -rn "github_pat_" --include='*.{yaml,yml,json,py,sh,txt,md,toml,conf,ini}' . 2>/dev/null | grep -v '.git/' | head -10
if [ $? -eq 0 ]; then echo "WARNING: PAT tokens found — redact them"; fi
echo "Secret scan complete"
```

### 6. Commit and push
```bash
TIMESTAMP=$(date '+%Y-%m-%d_%H:%M')
git add -A
git status --short | wc -l
echo "files staged — commiting"
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
| `.env` | Environment secrets |
| `cron/output/` | Cron output logs may contain API key traces |
| `hermes-agent/node_modules/` | Node dependencies, huge (100k+ files) |
| `hermes-agent/__pycache__/` | Python bytecode cache |

## Pitfalls
- **PAT auth may fail** — GitHub fine-grained PATs expire, get truncated in messages, or are revoked. Always verify with `ssh -T git@github.com` first. SSH keys don't expire. If using a custom cred helper (e.g. `/tmp/git-cred-helper.py`), check it's still valid by running it: `echo "" | /tmp/git-cred-helper.py get | grep password`
- **Remote URL switching** — If cloned with HTTPS (PAT) and auth fails, switch to SSH: `git remote set-url origin git@github.com:qzw-alt/demi.git`
- **Credentials storage** — PATs are stored in two places: `~/.config/git/credentials` (credential store) and potentially `/tmp/git-cred-helper.py` (custom helper). Both must be updated when the PAT rotates. The custom helper is registered via `git config --global credential.https://github.com.helper /tmp/git-cred-helper.py`.
- **GitHub push protection** blocks commits containing `sk-*` API keys. Always strip them before committing, then scan with grep. Note: config.yaml keys are usually truncated (e.g. `sk-8bc...87d2`) which doesn't trigger push protection.
- **`rsync --delete` may warn** about non-empty directories from old backup artifacts. Just git rm + rm them manually.
- **auth.json is excluded entirely** from rsync (unlike the old approach of syncing then stripping). `auth.lock` (its companion lock file) should also be cleaned up.
- **hermes-agent/node_modules/ is huge** (~100k+ files). Exclude it from rsync to avoid timeouts (can take >60s otherwise). Same for `__pycache__/` directories.
- **config.yaml keys are usually truncated** (e.g. `sk-8bc...87d2`) — GitHub's secret scanning won't flag them. Only auth.json has full credential payloads.
- **providers/\\*.json** — May contain model configs without literal keys, but check anyway.
- **Amending history requires `--force` push** — fine for personal backup repos.
- **Large rsync timeout** — `rsync -a --delete` on a large ~/.hermes/ may take >60s. Use a 300s timeout or run in background.
- **Temp directory name** — Can be any path like `/tmp/demi-backup/`; just be consistent across all steps. The absolute path matters for rsync source and repo destination paths.
