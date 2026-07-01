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
  --exclude='auth.lock' \
  --exclude='cron/output/' \
  --exclude='hermes-agent/node_modules/' \
  --exclude='hermes-agent/__pycache__/' \
  --exclude='hermes-agent/**/__pycache__/' \
  --exclude='**/__pycache__/' \
  --exclude='**/*.pyc' \
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

**⚠️ Terminal display trap:** The terminal truncates long strings in the middle with `...` when printing.
`read_file` and `print(repr(line))` can SHOW `sk-8bc...87d2` while the ACTUAL FILE contains the full
key `sk-8bc...87d2`. Always verify with `xxd` / Python hex if in doubt.

**Use ACTIVE key truncation** (not just scan-and-warn) — in cron context there is no user to respond to warnings:

```bash
cd /tmp/hermes-backup

# Truncate all full API keys in config.yaml automatically.
# Regex handles keys with -, _, and alphanumeric chars (covers DeepSeek, MinMax, Anthropic, etc.)
python3 << 'PYEOF'
import re

with open('config.yaml', 'r', encoding='utf-8') as f:
    content = f.read()

def truncate_key(match):
    full_key = match.group(1)
    if len(full_key) <= 15:
        return match.group(0)  # already short / already truncated
    prefix = full_key[3:9]   # first 6 after sk-
    suffix = full_key[-4:]   # last 4
    return f"api_key: sk-{prefix}...{suffix}"

content_new = re.sub(
    r'api_key:\s*(sk-[a-zA-Z0-9_-]{10,})',
    truncate_key,
    content
)

with open('config.yaml', 'w', encoding='utf-8') as f:
    f.write(content_new)

# Verify: hex-dump any remaining sk- lines to be sure they're truncated
with open('config.yaml', 'rb') as f:
    for i, line in enumerate(f, 1):
        if b'api_key:' in line and b'sk-' in line:
            val = line.split(b':', 1)[1].strip()
            truncated = b'...' in val
            print(f"  Line {i}: {val[:20]} (len={len(val)}, truncated={truncated})")
            if not truncated and len(val) > 14:
                print(f"    WARNING: FULL KEY — hex: {val.hex()}")
PYEOF

# auth.json is excluded from rsync entirely (--exclude='auth.json' in step 2),
# so no stripping needed. If it was previously committed, remove it in step 3.

# Remove .env from tracking
git rm --cached .env 2>/dev/null; rm -f .env

# Check providers/ for literal keys (env var refs like env:DEEPSEEK_API_KEY are safe)
for f in providers/*.json; do
  [ -f "$f" ] && grep -q '"api_key": "[a-zA-Z0-9_-]\{16,\}"' "$f" && \
    echo "WARNING: literal API key in $f — strip manually!"
done

# Redact PAT tokens from cron job definitions (prompt fields may contain embedded tokens)
# CRITICAL: also self-redact the *running* job — when a user-provided prompt embeds
# the PAT (as the cron job's `prompt` field), `cron/jobs.json` itself contains the
# full token. The known-glob scan below catches it, but a broader sweep is more
# future-proof: scan ALL JSON/YAML/MD files for the github_pat_ prefix.
for f in $(grep -rl "github_pat_" --include='*.json' --include='*.yaml' --include='*.yml' --include='*.md' --include='*.txt' . 2>/dev/null | grep -v '\.git/'); do
  sed -i 's/github_pat_[a-zA-Z0-9_-]\{20,\}/[PAT_REMOVED]/g' "$f" && \
    echo "Redacted PAT in $f"
done
```

### 5. Check for remaining secrets
```bash
cd /tmp/hermes-backup
# Check for sk-* API keys in tracked source files (broader pattern: allows -, _ chars)
grep -rn "sk-[a-zA-Z0-9_-]\{16,\}" --include='*.{yaml,yml,json,py,sh,txt,md,env,toml,conf,ini}' . 2>/dev/null | grep -v '.git/' | grep -v '\.\.\.' | grep -v 'xxx' | grep -v 'Xxx' | head -10
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
| `auth.lock` | Lockfile companion to `auth.json` |
| `.env` | Environment secrets |
| `cron/output/` | Cron output logs may contain API key traces |
| `hermes-agent/node_modules/` | Node dependencies, huge (100k+ files) |
| `hermes-agent/__pycache__/` | Python bytecode cache |

## Pitfalls
- **Terminal display truncation trap** — The terminal (read_file / print / repr) truncates long strings in the 
  middle with `...`. A key displayed as `sk-8bc...87d2` is NOT necessarily truncated in the file — it may be the full
  35-char key `sk-8bc...87d2` with only the middle hidden. Always verify with Python hex (`val.hex()`) or `xxd`
  when checking whether keys are safe for GitHub.
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
  embedded in a committed prompt — assume it's leaked.
- **__pycache__ lives outside hermes-agent/ too** — Plugins under `plugins/*/src/` and
  `plugins/*/socket/` generate `__pycache__/*.pyc` files. The skill's original exclusion
  only covered `hermes-agent/__pycache__/`, so plugin bytecode got committed in past
  backups. The `--exclude='**/__pycache__/'` and `--exclude='**/*.pyc'` rsync patterns
  fix this for new backups; for existing tracked files use `git rm -rf --cached <path>`.
- **auth.lock is auth.json's companion** — When `auth.json` is excluded from rsync, the
  `auth.lock` lockfile that pairs with it can still appear in the working tree on
  every backup (gateway runtime state). Exclude it alongside `auth.json`.
- **Temp directory name** — Can be any path like `/tmp/demi-backup/`; just be consistent across all steps. The absolute path matters for rsync source and repo destination paths.
