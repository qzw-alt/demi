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
  --exclude='kanban.db.init.lock' \
  --exclude='models_dev_cache.json' \
  /home/ubuntu/.hermes/ /tmp/hermes-backup/
```

**After rsync — verify exclusions actually took effect** (rsync can silently leak root-level files; don't trust the exclude to have worked):

```bash
cd /tmp/hermes-backup/
# Verify each user-specified exclude is absent
for p in sessions/ memories/ cache/ logs/ sandboxes/ audio_cache/ image_cache/ \
         auth.json auth.lock .env .hermes_history \
         gsc/client_secret.json gsc/token.json kanban.db.init.lock \
         models_dev_cache.json gateway.lock gateway.pid cron/output/; do
  [ -e "$p" ] && echo "LEAK: $p"
done
# Heavy dirs that may have leaked if user excluded list is smaller than the canonical one
for d in hermes-agent/venv hermes-agent/website hermes-agent/tests hermes-agent/ui-tui; do
  [ -d "$d" ] && du -sh "$d"
done
# If any LEAK appeared, rm -f it (or rm -rf for dirs) and git rm --cached
# If heavy dirs appeared, add them to .gitignore in step 3 BEFORE running git add -A
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
# If .gitignore was wiped by rsync --delete, restore it from the canonical template below.
# Otherwise just ensure every rsync --exclude is also listed (defense in depth).
GITIGNORE_NEEDED=0
[ ! -s .gitignore ] && GITIGNORE_NEEDED=1
if [ "$GITIGNORE_NEEDED" = 1 ]; then
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

# Kanban runtime lock + model registry cache (regenerated on every gateway tick)
kanban.db.init.lock
models_dev_cache.json
EOF
fi
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
python3 <skill_dir>/scripts/redact_secrets.py /tmp/demi-backup "workspace/website/中文目录/文件.md"

# <skill_dir> = /home/ubuntu/.hermes/skills/devops/hermes-backup/  (or wherever the skill is installed)
```

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

echo "=== Real sk- API keys (40+ chars) ==="
HITS=$(grep -rln -E "sk-[a-zA-Z0-9_-]{40,}" \
  --include='*.yaml' --include='*.yml' --include='*.json' \
  --include='*.py' --include='*.sh' --include='*.txt' --include='*.md' \
  --include='*.env' --include='*.toml' --include='*.conf' --include='*.ini' \
  . 2>/dev/null | grep -v "$NOISE" | head -10)
if [ -z "$HITS" ]; then echo "  OK No full sk- API keys found"; else echo "$HITS"; fi

echo "=== providers/ literal keys ==="
for f in providers/*.json; do
  [ -f "$f" ] && grep -q -E '"[a-zA-Z0-9_-]*key": "[a-zA-Z0-9_-]{40,}"' "$f" 2>/dev/null && \
    echo "POTENTIAL KEY: $f — review and strip"
done
echo "Secret scan complete"

# LOOP GUARD: if the HITS variables are non-empty, the walker skipped files.
# Re-run redaction directly on each flagged file (do NOT re-run the full batch walker):
#   python3 -c "import re,sys; p=sys.argv[1]; c=open(p).read(); \
#     print(re.sub(r'sk-[a-zA-Z0-9_-]+', \
#       lambda m: m.group(0) if '...' in m.group(0) or len(m.group(0))<=15 \
#         else f'sk-{m.group(0)[3:9]}...{m.group(0)[-4:]}', c), end='')" "$f" > tmp && mv tmp "$f"
# Re-run the scan above. Repeat until both HITS variables are empty.
```

> **Verification tip:** A scan hit doesn't tell you whether the matched string is a real key or an already-truncated placeholder — both look identical on the terminal. Always confirm with `xxd` or a Python byte-length check before declaring clean. See `references/secret-redaction-verification.md` for the recipe.

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
| `kanban.db.init.lock` | Kanban SQLite init lock (runtime state, like auth.lock) |
| `models_dev_cache.json` | ~3MB model registry cache regenerated on every gateway tick |
| `hermes-agent/node_modules/` | Node dependencies, huge (100k+ files) |
| `lsp/node_modules/` | LSP server deps (typescript-language-server, pyright) |
| `**/node_modules/` | Catch-all for any other node_modules |
| `**/__pycache__/` | Python bytecode cache (covers hermes-agent + plugins) |

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
- **`.curator_backups/` directories accumulate with embedded PATs** — When the skills curator runs, it snapshots `cron/jobs.json` to `skills/.curator_backups/<timestamp>/cron-jobs.json`. If the cron prompt ever contained a PAT, every backup snapshot also contains it. These directories are *not* in the default rsync exclude list. Step 4's Python redaction script scans them (the `NOISE_DIRS` filter only excludes `hermes-agent/venv/`, `hermes-agent/website/`, `hermes-agent/node_modules/`, `hermes-agent/tests/`, `hermes-agent/ui-tui/`, and `.git/` — *not* `.curator_backups/`). The new commits will have redacted working-tree versions, even though the old commits in git history still contain the unredacted PATs (untouchable without force-push history rewrite).
- **`models_dev_cache.json` is a 3MB gateway cache, not user data** — Lives at `~/.hermes/models_dev_cache.json` and is regenerated on every gateway tick (model registry refresh). Rsyncing it commits a giant diff with no semantic value. Exclude it from rsync (`--exclude='models_dev_cache.json'`) and from .gitignore. Old backups may have committed it — `git rm --cached models_dev_cache.json` once to drop tracking.
- **`kanban.db.init.lock` is a runtime lock, not the kanban DB itself** — Pairs with `kanban.db` the way `auth.lock` pairs with `auth.json`. It's a 0-byte file written when the kanban SQLite is initialized, and shows up on every backup regardless of whether the kanban is in use. The kanban DB itself (`kanban.db`, ~114KB SQLite) IS tracked content — do NOT exclude it. But the `.init.lock` lockfile should be excluded via rsync and .gitignore.
- **Walker hits `hermes-agent/venv/` and `hermes-agent/tests/`** — The skill's NOISE_DIRS list excludes these from the *walker* (so redaction isn't attempted on third-party code), but **rsync does NOT exclude them** by default. They live in the working tree, get added with `git add -A` if .gitignore misses them, and inflate commits by hundreds of MB of test fixtures / venv site-packages. The canonical .gitignore template above includes `**/node_modules/`, `**/__pycache__/`, and `**/*.pyc` which covers the worst of it, but a strict repository should also exclude `hermes-agent/venv/`, `hermes-agent/tests/`, `hermes-agent/website/`, `hermes-agent/ui-tui/` outright if they're not needed for backup. Verify with `git status --short | wc -l` before commit — if it's in the thousands, .gitignore isn't catching something.
- **Default git clone over SSH may take >60s** — The first clone of a populated `qzw-alt/demi` repo (1.2GB working tree, hundreds of commits) routinely exceeds the 60s foreground timeout in `terminal()`. Use `timeout 240 git clone ...` or run in background. After the first clone, subsequent updates via `git pull` are fast.
- **rsync `--exclude='models_dev_cache.json'` does NOT always exclude a root-level file** — In one session the file was rsynced into the working tree despite the exclude pattern being set. Rsync's exclude rules can be confused by file-vs-component matching at the source root. **Always verify the file is absent after rsync** (`test -e path && echo PRESENT`); if it leaked through, manually `rm -f` it AND `git rm --cached` it. Don't trust the exclude to have caught it. Same risk applies to any other root-level dotfile/lockfile the user lists as a bare filename (e.g. `auth.json` in some rsync versions).
- **User-supplied exclude lists are often smaller than the canonical one — verify heavy dirs aren't in the working tree** — When a user gives a short exclude list (e.g. only the ~10 paths from a cron prompt), the skill's canonical heavy-directory excludes (`hermes-agent/venv/`, `hermes-agent/website/`, `hermes-agent/tests/`, `hermes-agent/ui-tui/`) may NOT be in the user's list. After rsync, ALWAYS check: `for d in hermes-agent/venv hermes-agent/website hermes-agent/tests hermes-agent/ui-tui; do test -e "$d" && echo "HEAVY: $d"; done`. If any are present, add them to .gitignore (the skill's template includes them) and confirm `git ls-files` shows 0 tracked files in those dirs before commit. If gitignore is missing or incomplete, `git add -A` will commit hundreds of MB of venv/test fixtures.
- **CJK-path files (Chinese / Japanese / Korean directory names) silently bypass the os.walk walker** — Reproduced in 2026-07-08 session: walker reported "13 files modified, 30 sk- redactions", but step 5 length-gated scan still found 1 real key in `./workspace/website/德米知识库/01-记忆系统/MEMORY.md`. The CJK-encoded path was skipped by `os.walk` for an unknown reason (possibly a stale `dirs[:]` filter, possibly a UnicodeDecodeError swallowed by `except (OSError, UnicodeError)`). **The fix is the step 5 length-gated grep scan — it is the only reliable verification.** When it finds a hit, re-run redaction DIRECTLY on the specific file path with a one-shot script (`python3 redact_one.py 'CJK/路径/文件.md'`), NOT the batch walker. Loop until step 5 reports zero hits.
- **Inline Python via `terminal()` breaks on f-strings with `{` `}` in shell quoting** — `terminal("python3 -c \"...f-string...\"")` consistently mangles nested f-strings because the shell and Python both interpret braces. The first redaction attempt in 2026-07-08 session failed with `NameError: name 'm' is not defined` from a broken f-string. **Fix:** always write the redaction script to a file (e.g. `/tmp/redact_one.py` or `/tmp/redact_keys.py`) using `write_file`, then `terminal("python3 /tmp/redact_one.py <path>")`. The script file is also reusable across re-runs without re-typing.
- **PAT leak in cron prompt is the most common secret exposure path — treat it as expected, not surprising** — In the 2026-07-08 session the user's own cron prompt embedded a `github_pat_...` token, which the walker caught (1 PAT redaction in `cron/jobs.json`). The skill already documents this in pitfalls, but the user-facing **delivery response** should make the revocation warning prominent, not buried: "The PAT in this cron prompt has been redacted in this commit, but the source file `~/.hermes/cron/jobs.json` still contains the live token. Revoke + regenerate at https://github.com/settings/tokens?type=beta." The PAT was visible to the rsync source on every prior backup attempt; the only thing that changes is whether it's now visible in the working tree, which is fixable. The source itself is the leak.
