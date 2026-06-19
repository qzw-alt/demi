---
name: hermes-backup
description: Backup ~/.hermes/ to GitHub backup repository, excluding sensitive files
---

# Hermes Backup to GitHub

Backup `~/.hermes/` to a GitHub backup repository (e.g., `qzw-alt/demi`).

## Workflow

1. **Set up GitHub auth** — use SSH key auth (preferred) or PAT
2. **Clone/update repo** to `/tmp/hermes-backup/`
3. **Sync with rsync**, excluding sensitive files
4. **Strip API keys** from tracked config files before commit
5. **Commit and push**

## Exact Commands

### 1. Clone repo
```bash
rm -rf /tmp/hermes-backup/
mkdir -p /tmp/hermes-backup/
cd /tmp/hermes-backup
git clone git@github.com:qzw-alt/demi.git .
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
# Strip all non-empty api_key values
sed -i '/api_key:/ {/'\'''\''/!s/api_key:.*/api_key: '\'''\''/}' config.yaml
# Strip access_token in auth.json
sed -i 's/"access_token": "sk-[^"]*"/"access_token": ""/' auth.json
# Remove .env from tracking
git rm --cached .env 2>/dev/null; rm -f .env
```

### 5. Check for remaining secrets
```bash
grep -r "sk-[a-zA-Z0-9]\{20,\}" --include='*.{yaml,yml,json,py,sh,txt,md,env}' . 2>/dev/null | grep -v '.git/' | head -5
grep -r "DEEPSEEK\|OPENAI\|ANTHROPIC.*API" --include='*.{yaml,yml,json,py,sh,txt,md,env}' . 2>/dev/null | grep -v '.git/' | head -5
```

### 6. Commit and push
```bash
TIMESTAMP=$(date '+%Y-%m-%d_%H:%M')
git add -A
git commit -m "Backup: $TIMESTAMP"
git push origin master
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
- **PAT auth may fail** — GitHub fine-grained PATs expire. Use SSH key auth instead.
- **GitHub push protection** blocks commits containing `sk-*` API keys. Always strip them before committing.
- **`rsync --delete` may warn** about non-empty directories from old backup artifacts. Just git rm + rm them manually.
- **Amending history requires `--force` push** — fine for personal backup repos.
