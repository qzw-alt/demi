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
# Alternatively check for credential helpers
git config --global --get credential.helper 2>/dev/null
cat ~/.git-credentials 2>/dev/null || echo "No .git-credentials file"
```

If neither works, set up SSH: `ssh-keygen -t ed25519 -C "backup" && cat ~/.ssh/id_ed25519.pub` and add to GitHub.

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
  /home/ubuntu/.hermes/ /tmp/hermes-backup/
```

### 3. Remove old sensitive artifacts from previous backups
```bash
cd /tmp/hermes-backup
# These may exist from previous commits — delete and git rm them
for dir in sessions memories memory memory_backup_* migration cache logs sandboxes; do
  [ -d "$dir" ] && { git rm -r --cached "$dir" 2>/dev/null; rm -rf "$dir"; }
done
rm -f gateway.lock gateway.pid auth.lock kanban.db.init.lock
```

### 4. Strip API keys from tracked files
```bash
cd /tmp/hermes-backup
# Strip all non-empty api_key values from config.yaml
sed -i '/api_key:/ {/'\'''\\''/!s/api_key:.*/api_key: '\'''\\''/}' config.yaml
# Strip access_token in auth.json (handles both top-level and credential_pool entries)
sed -i 's/"access_token": "[^"]*"/"access_token": ""/g' auth.json
# Check providers/ for literal keys (env var refs like env:DEEPSEEK_API_KEY are safe)
for f in providers/*.json; do
  [ -f "$f" ] && grep -q '"api_key": "[a-zA-Z0-9]\{16,\}"' "$f" && \
    echo "WARNING: literal API key in $f — strip manually!"
done
# Remove .env from tracking
git rm --cached .env 2>/dev/null; rm -f .env
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
| `.env` | Environment secrets |

## Pitfalls
- **PAT auth may fail** — GitHub fine-grained PATs expire, get truncated in messages, or are revoked. Always verify with `ssh -T git@github.com` first. SSH keys don't expire.
- **Remote URL switching** — If cloned with HTTPS (PAT) and auth fails, switch to SSH: `git remote set-url origin git@github.com:qzw-alt/demi.git`
- **GitHub push protection** blocks commits containing `sk-*` API keys. Always strip them before committing, then scan with grep.
- **`rsync --delete` may warn** about non-empty directories from old backup artifacts. Just git rm + rm them manually.
- **auth.json credential_pool** — Keys may be stored as env var references (`env:DEEPSEEK_API_KEY`) which are safe, or as literal strings which are not. The sed command strips all `access_token` values regardless.
- **providers/\*.json** — May contain model configs without literal keys, but check anyway.
- **Amending history requires `--force` push** — fine for personal backup repos.
- **Large rsync timeout** — `rsync -a --delete` on a large ~/.hermes/ may take >60s. Use a 300s timeout or run in background.
- **Temp directory name** — Can be any path like `/tmp/demi-backup/`; just be consistent across all steps. The absolute path matters for rsync source and repo destination paths.
