# demi Backup — Auth & Git Troubleshooting Reference

## Corrupted `.git-credentials` (2026-05-03)

**Symptom:** `git push` fails with `Authentication failed` despite token existing in `~/.git-credentials`.

**Root cause:** The token in `~/.git-credentials` was truncated/corrupted. Observed value:
```
https://github.com/qzw-alt:github...ku07@github.com
```
The token should be a full `ghp_` Personal Access Token (~40 chars), but was cut to `github...ku07` (~13 visible chars).

**Detection command:**
```bash
cat ~/.git-credentials
```
Normal: `https://github.com/qzw-alt:ghp_xxxxxxxxxxxxxxxxxxxx@github.com`
Broken: `https://github.com/qzw-alt:github...ku07@github.com`

**Fix:** Generate new PAT at https://github.com/settings/tokens (classic, `repo` scope), then:
```bash
echo "https://github.com/qzw-alt:ghp_NEWTOKEN@github.com" > ~/.git-credentials
chmod 600 ~/.git-credentials
```

---

## Embedded `.git/` Directories (2026-05-03)

**Symptom:** Running `git add memory/` inside `~/.hermes/` produces:
```
warning: adding embedded git repository: memory
fatal: 'origin' does not appear to be a git repository
```

**Root cause:** Both `~/.hermes/memory/` and `~/.hermes/.memories/` contain their own `.git/` directories (embedded repos). When `~/.hermes/` itself is also a git repo, `git add` recursively adds them as submodules, causing confusion.

**Fix:** Never run `git add` on `memory/` or `.memories/` from inside `~/.hermes/`. Instead:
1. Clone the backup repo fresh to a separate working dir (e.g., `~/demi`)
2. Copy content from `~/.hermes/` to the clone using `cp -r` (which skips `.git` dirs)
3. Commit and push from the clone

**Commands:**
```bash
rm -rf ~/demi
git clone https://github.com/qzw-alt/demi.git ~/demi
cp -r ~/.hermes/.memories/* ~/demi/.memories/
cp -r ~/.hermes/memory/* ~/demi/memory/
```

---

## SSH Key Not Registered (2026-05-03)

**Symptom:** `git remote set-url origin git@github.com:... && git push` fails with `Permission denied (publickey)`.

**Root cause:** The Ed25519 key at `~/.ssh/id_ed25519` was not loaded into ssh-agent AND was not registered with GitHub.

**Detection:**
```bash
ssh-add ~/.ssh/id_ed25519  # "agent refused operation" = key not loadable
ssh -T git@github.com      # "Permission denied" = not registered
```

**Fix (option A — SSH):**
1. Register `~/.ssh/id_ed25519.pub` in GitHub Settings → SSH Keys
2. Load key: `ssh-add ~/.ssh/id_ed25519`
3. Switch remote: `git remote set-url origin git@github.com:qzw-alt/demi.git`

**Fix (option B — HTTPS/PAT):** Use the credential file method above.

---

## GitHub API Validation (No-Credential Probe)

When git auth fails but you need to verify the repo is reachable:
```python
import urllib.request, json
req = urllib.request.Request(
    'https://api.github.com/repos/qzw-alt/demi',
    headers={'User-Agent': 'Hermes-Cron/1.0'}
)
with urllib.request.urlopen(req) as resp:
    data = json.loads(resp.read())
    print(data['full_name'], data['default_branch'])
```
This works unauthenticated for public repos — useful for debugging without triggering auth prompts.
