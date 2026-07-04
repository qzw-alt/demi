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

**SSH key auth is preferred over PAT** — `git@github.com:qzw-alt/demi.git` works when PAT fails.
Verify with: `ssh -T git@github.com` (should print "Hi <username>! You've successfully authenticated").
If SSH works but PAT doesn't, switch the remote to SSH after clone:
```bash
git remote set-url origin git@github.com:qzw-alt/demi.git
git push origin master
```

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
# Add ALL sensitive exclusions to .gitignore so rsync doesn't re-expose them as untracked.
# The skill's original step only added auth.json; broaden to cover every --exclude above.
for entry in auth.json .env .hermes_history gsc/client_secret.json gsc/token.json; do
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
# IMPORTANT: skip tokens containing '...' (already truncated) — otherwise the regex
# matches across the truncation marker and mangles the output. Verify with xxd on the first match.
python3 << 'PYEOF'
import re

with open('config.yaml', 'r', encoding='utf-8') as f:
    content = f.read()

def truncate_key(match):
    full_key = match.group(1)
    if '...' in full_key:
        return match.group(0)  # already truncated, don't re-touch
    if len(full_key) <= 15:
        return match.group(0)  # already short / already truncated
    prefix = full_key[3:9]   # first 6 after sk-
    suffix = full_key[-4:]   # last 4
    return f"api_key: sk-{prefix}...{suffix}"

content_new = re.sub(
    r'api_key:\s*(sk-[a-zA-Z0-9_-]+)',
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
# (.env, .hermes_history, gsc/* are also removed in step 3.)

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
# Use Python regex (40+ char gate) so we only redact real tokens, not doc placeholders
# like `github_pat_xxx`. The sed regex `\{20,\}` matches short placeholders too and
# will mangle documentation that uses `github_pat_*` as a format descriptor.
python3 << 'PYEOF'
import re, os

REDACTED = "github...REMOVED_LEAKED_TOKEN"
PAT_RE = re.compile(r'github_pat_[a-zA-Z0-9_-]{40,}')

# Same noise denylist as the secret scan
NOISE_DIRS = ('venv/', 'website/', 'node_modules/', 'ui-tui/', 'tests/',
              '.curator_backups/', '.git/')
INCLUDE = ('.json', '.yaml', '.yml', '.md', '.txt', '.py', '.sh',
           '.toml', '.conf', '.ini', '.env')

n_redacted = 0
for root, dirs, files in os.walk('.'):
    # Skip noise directories
    dirs[:] = [d for d in dirs if not any(n in f"{root}/{d}" for n in NOISE_DIRS)]
    for f in files:
        if not f.endswith(INCLUDE):
            continue
        path = os.path.join(root, f)
        try:
            with open(path, 'r', encoding='utf-8', errors='ignore') as fh:
                content = fh.read()
            new_content, n = PAT_RE.subn(REDACTED, content)
            if n:
                with open(path, 'w', encoding='utf-8') as fh:
                    fh.write(new_content)
                print(f"  Redacted {n} PAT in {path}")
                n_redacted += n
        except (OSError, UnicodeError):
            pass

print(f"Total PAT redactions: {n_redacted}")
PYEOF
```

### 5. Check for remaining secrets

**The simple `grep "sk-..."` scan in old revisions of this skill returns huge noise from `hermes-agent/venv/`, `hermes-agent/website/`, `hermes-agent/node_modules/`, and `hermes-agent/tests/`** (which all contain documentation/test fixtures and library code with `sk-` prefixes that aren't real keys). The reliable check is **length-gated regex with explicit denylist directories** — a `sk-...` placeholder has 5-10 chars total, a real fine-grained PAT has 100+ chars. Use the 40+ char threshold to filter out placeholders.

```bash
cd /tmp/demi-backup
# Real-token scan: github_pat_ followed by 40+ chars (real fine-grained PATs are ~111 chars)
# Filters out: hermes-agent/venv, website, node_modules, ui-tui, tests, plus .curator_backups noise
NOISE='hermes-agent/venv\|hermes-agent/website\|hermes-agent/node_modules\|hermes-agent/tests\|hermes-agent/ui-tui\|\.curator_backups\|\.git/'
echo "=== Real github_pat_ tokens (40+ chars) ==="
grep -rln -E "github_pat_[a-zA-Z0-9_-]{40,}" \
  --include='*.json' --include='*.yaml' --include='*.yml' \
  --include='*.md' --include='*.txt' --include='*.py' \
  --include='*.sh' --include='*.toml' --include='*.conf' --include='*.ini' \
  . 2>/dev/null | grep -v "$NOISE" | head -10
if [ -z "$(grep -rln -E 'github_pat_[a-zA-Z0-9_-]{40,}' --include='*.json' --include='*.yaml' --include='*.md' --include='*.txt' --include='*.py' . 2>/dev/null | grep -v "$NOISE")" ]; then
  echo "  ✓ No full PAT tokens found"
fi

echo "=== Real sk- API keys (40+ chars) ==="
grep -rln -E "sk-[a-zA-Z0-9_-]{40,}" \
  --include='*.yaml' --include='*.yml' --include='*.json' \
  --include='*.py' --include='*.sh' --include='*.txt' --include='*.md' \
  --include='*.env' --include='*.toml' --include='*.conf' --include='*.ini' \
  . 2>/dev/null | grep -v "$NOISE" | head -10
if [ -z "$(grep -rln -E 'sk-[a-zA-Z0-9_-]{40,}' --include='*.yaml' --include='*.json' --include='*.md' --include='*.txt' . 2>/dev/null | grep -v "$NOISE")" ]; then
  echo "  ✓ No full sk- API keys found"
fi

echo "=== providers/ literal keys ==="
for f in providers/*.json; do
  [ -f "$f" ] && grep -q -E '"[a-zA-Z0-9_-]*key": "[a-zA-Z0-9_-]{40,}"' "$f" 2>/dev/null && \
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
| `auth.json` | Full API keys in credential store |
| `auth.lock` | Lockfile companion to `auth.json` |
| `.env` | Environment secrets |
| `.hermes_history` | Shell command log; has pasted credentials |
| `cron/output/` | Cron output logs may contain API key traces |
| `gsc/client_secret.json` | Google OAuth client secret |
| `gsc/token.json` | Google OAuth refresh token |
| `hermes-agent/node_modules/` | Node dependencies, huge (100k+ files) |
| `lsp/node_modules/` | LSP server deps (typescript-language-server, pyright) |
| `**/node_modules/` | Catch-all for any other node_modules |
| `**/__pycache__/` | Python bytecode cache (covers hermes-agent + plugins) |

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
- **`.hermes_history` is a plaintext credential trap** — This file (lives at `~/.hermes/.hermes_history`) contains a running log of shell commands and pasted content. Past entries include plaintext Feishu app secrets (`cli_a912890ce721dcee...`), pasted API keys in conversation snippets, and other credentials. It MUST be excluded from rsync AND removed from git history if previously committed. Add `--exclude='.hermes_history'` to the rsync invocation, and `git rm --cached .hermes_history` if it was tracked.
- **`gsc/client_secret.json` and `gsc/token.json` are Google OAuth secrets** — These files contain Google Search Console OAuth client secrets and refresh tokens. GitHub push protection blocks any commit containing them. Exclude from rsync (`--exclude='gsc/client_secret.json' --exclude='gsc/token.json'`), remove from tracking, and add to .gitignore. If a previous commit included them, the push will be rejected; use `git reset --soft HEAD~1 && git commit --amend --no-edit && git push --force-with-lease` to rewrite history. (`gsc/authorize.py` is safe to keep — it's just code.)
- **Force-push is required to rewrite history** — When push protection blocks a push because secrets leaked into a commit, you must rewrite local history (soft reset + amend, or filter-branch) then `git push --force-with-lease origin master`. Use `--force-with-lease` instead of `--force` to avoid clobbering concurrent pushes.
- **PAT auth may show false success on `git ls-remote`** — `git ls-remote` works on public repos without valid auth (it ignores bad credentials silently). The only real auth test is `git push` or `curl -H "Authorization: token <PAT>" https://api.github.com/user` (returns 200 = valid, 401 = invalid).
- **`lsp/node_modules/` is a separate `node_modules`, not under `hermes-agent/`** — The `~/.hermes/lsp/` directory (LSP language servers: typescript-language-server, pyright) has its own `node_modules/` with several hundred MB of dependencies. The original `hermes-agent/node_modules/` exclude missed it, so past backups may have grown large and slow. Always use `--exclude='**/node_modules/'` as the catch-all (added in step 2).
- **`x-access-token:` URL-embedded PAT silently fails for push** — Embedding `github_pat_xxx` as `https://x-access-token:PAT@github.com/owner/repo.git` works for `git clone` (download doesn't require auth on a public repo, or reads the URL credentials), but **`git push` returns `remote: Invalid username or token. Password authentication is not supported for Git operations.`** — GitHub removed password-style auth for fine-grained PATs in HTTPS push. The clone "succeeds" without prompting because git reads the embedded credentials, so the failure only surfaces at push time. **Always switch to SSH before pushing** when this error appears: `git remote set-url origin git@github.com:owner/repo.git`. Verify SSH works first with `ssh -T git@github.com`.
- **Truncation regex `[a-zA-Z0-9_-]{40,}` falsely matches across `...` markers** — A first-pass scan of `sk-[a-zA-Z0-9_-]{40,}` matches both `sk-kimi-iGU...NGGW` (the literal string with `...` in the middle) AND the full unredacted key (when checked against the source). When a second pass applies `re.sub(r'sk-[a-zA-Z0-9_-]{30,}', truncate, content)`, the regex matches the full token up to the first non-alphanumeric/underscore/dash char — which for a Chinese-context line may be a CJK character, mangling the output to `sk-kimi-i...配置中` instead of the intended `sk-kimi-i...NGGW`. Fix: in the replace function, check `'...' in m.group(0)` and skip those (they're already truncated), AND match against the unredacted source so the boundary is correct. Always verify with `xxd` on the first matched line before declaring clean.
- **Re-restore from source after a bad regex pass** — If a first-pass truncation script mangled some keys, don't try to fix them in place by guessing what the original was. Read the unredacted source from `~/.hermes/` (the rsync source, which still has the originals), apply the truncation there, and overwrite the bad file. Faster and less error-prone than trying to invert a corrupted regex.
- **PATs leak into SKILL.md "known-failed token" notes** — When documenting a failed/expired PAT in a skill file, users often paste the *full* token inline (e.g. "PAT `github...Q5` returned 401") thinking the note is purely diagnostic. The full token is still plaintext in the file, and gets rsynced + committed. Mitigation: (a) when writing a SKILL.md, use placeholders like `github...PLACEHOLDER` not the real token; (b) when the backup finds a full PAT in any `.md`/`.yaml`/`.json`/`.txt` file, redact it the same way as `cron/jobs.json` — and flag the user that the token is exposed in skill docs.
- **Length-gated regex is required for secret scanning** — The pattern `sk-[a-zA-Z0-9_-]{16,}` matches `sk-xxx...xxxx` documentation placeholders (15 chars + the `sk-` prefix = matches). Use a 40+ char gate (real fine-grained PATs are ~111 chars; real Anthropic/OpenAI keys are 40+ chars) to filter out placeholders. Otherwise you'll either flood output with false positives from `hermes-agent/venv/`, `hermes-agent/website/`, and SKILL.md docs, or — worse — redact doc placeholders that aren't real secrets (mangling documentation).
- **grep output floods with `hermes-agent/venv/`, `hermes-agent/website/`, `hermes-agent/node_modules/` noise** — These directories contain library code, test fixtures, and Docusaurus docs that all have `sk-`, `github_pat_`, `gho_`, `ghp_` patterns as documentation/format descriptors. Always pipe secret-scan grep output through a `grep -v 'hermes-agent/venv\\|hermes-agent/website\\|hermes-agent/node_modules\\|hermes-agent/tests\\|hermes-agent/ui-tui'` filter (the step 5 scan does this). Note: filtering with `grep -v` only works if you use the right escape syntax — the `\|` alternation is GNU grep specific; on BSD/macOS use `grep -vE 'hermes-agent/(venv|website|node_modules|tests|ui-tui)'`.
- **Cron job prompt becomes the source of the next backup's PAT leak** — The recurring failure mode: user creates cron job with prompt like "use PAT github_pat_xxx to push". That prompt is stored verbatim in `~/.hermes/cron/jobs.json`. On every backup, `cron/jobs.json` is rsynced (not in the exclude list) and the full PAT lands in the working tree. Mitigation in the skill: step 4's Python PAT_RE.subn with a 40+ char gate catches and redacts this. Mitigation at the source: when writing a cron job prompt, never embed a PAT — use `ssh -T git@github.com` style auth, or read the PAT from a credential helper.
- **`.curator_backups/` directories accumulate with embedded PATs** — When the skills curator runs, it snapshots `cron/jobs.json` to `skills/.curator_backups/<timestamp>/cron-jobs.json`. If the cron prompt ever contained a PAT, every backup snapshot also contains it. These directories are *not* in the default rsync exclude list. Step 4's Python redaction script scans them (the `NOISE_DIRS` filter only excludes `hermes-agent/venv/`, `hermes-agent/website/`, `hermes-agent/node_modules/`, `hermes-agent/tests/`, `hermes-agent/ui-tui/`, and `.git/` — *not* `.curator_backups/`). The new commits will have redacted working-tree versions, even though the old commits in git history still contain the unredacted PATs (untouchable without force-push history rewrite).
