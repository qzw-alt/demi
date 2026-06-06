---
name: github-auth
description: "GitHub auth setup: HTTPS tokens, SSH keys, gh CLI login."
version: 1.1.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [GitHub, Authentication, Git, gh-cli, SSH, Setup]
    related_skills: [github-pr-workflow, github-code-review, github-issues, github-repo-management]
---

# GitHub Authentication Setup

This skill sets up authentication so the agent can work with GitHub repositories, PRs, issues, and CI. It covers two paths:

- **`git` (always available)** — uses HTTPS personal access tokens or SSH keys
- **`gh` CLI (if installed)** — richer GitHub API access with a simpler auth flow

## Detection Flow

When a user asks you to work with GitHub, run this check first:

```bash
# Check what's available
git --version
gh --version 2>/dev/null || echo "gh not installed"

# Check if already authenticated
gh auth status 2>/dev/null || echo "gh not authenticated"
git config --global credential.helper 2>/dev/null || echo "no git credential helper"
```

**Decision tree:**
1. If `gh auth status` shows authenticated → you're good, use `gh` for everything
2. If `gh` is installed but not authenticated → use "gh auth" method below
3. If `gh` is not installed → use "git-only" method below (no sudo needed)

---

## Method 1: Git-Only Authentication (No gh, No sudo)

This works on any machine with `git` installed. No root access needed.

### Option A: HTTPS with Personal Access Token (Recommended)

This is the most portable method — works everywhere, no SSH config needed.

**Step 1: Create a personal access token**

Tell the user to go to: **https://github.com/settings/tokens**

- Click "Generate new token (classic)"
- Give it a name like "hermes-agent"
- Select scopes:
  - `repo` (full repository access — read, write, push, PRs)
  - `workflow` (trigger and manage GitHub Actions)
  - `read:org` (if working with organization repos)
- Set expiration (90 days is a good default)
- Copy the token — it won't be shown again

**Token format checks:**
- Fine-Grained PAT: `github_pat_` prefix + 101 chars after (total ~111 chars) — **validate before use**
- Classic PAT: `ghp_` prefix + 40 chars
- `x-access-token:` URL embedding works for `git clone` but **fails for `git push`** with: `remote: Invalid username or token. Password authentication is not supported for Git operations.`

**Always validate a PAT before backup/restore operations:**
```python
import urllib.request, json
PAT = "<token>"
req = urllib.request.Request(
    "https://api.github.com/user",
    headers={"Authorization": f"Bearer {PAT}", "Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28"}
)
with urllib.request.urlopen(req) as resp:
    print(f"Authenticated as: {json.loads(resp.read())['login']}")
# If 401: token invalid or lacks repo scope. If 200: token is valid.
```

If `git push` fails with embedded PAT (even though clone works), fall back to pushing via the GitHub REST API directly (see `github-repo-management` skill → `references/backup-to-github.md`)."

**Alternative: cache helper (credentials expire from memory)**

```bash
# Cache in memory for 8 hours (28800 seconds) instead of saving to disk
git config --global credential.helper 'cache --timeout=28800'
```

**Alternative: set the token directly in the remote URL (per-repo)**

```bash
# Embed token in the remote URL (avoids credential prompts entirely)
git remote set-url origin https://<username>:<token>@github.com/<owner>/<repo>.git
```

**Step 3: Configure git identity**

```bash
# Required for commits — set name and email
git config --global user.name "Their Name"
git config --global user.email "their-email@example.com"
```

**Step 4: Verify**

```bash
# Test push access (this should work without any prompts now)
git ls-remote https://github.com/<their-username>/<any-repo>.git

# Verify identity
git config --global user.name
git config --global user.email
```

### Option B: SSH Key Authentication

Good for users who prefer SSH or already have keys set up.

**Step 1: Check for existing SSH keys**

```bash
ls -la ~/.ssh/id_*.pub 2>/dev/null || echo "No SSH keys found"
```

**Step 2: Generate a key if needed**

```bash
# Generate an ed25519 key (modern, secure, fast)
ssh-keygen -t ed25519 -C "their-email@example.com" -f ~/.ssh/id_ed25519 -N ""

# Display the public key for them to add to GitHub
cat ~/.ssh/id_ed25519.pub
```

Tell the user to add the public key at: **https://github.com/settings/keys**
- Click "New SSH key"
- Paste the public key content
- Give it a title like "hermes-agent-<machine-name>"

**Step 3: Test the connection**

```bash
ssh -T git@github.com
# Expected: "Hi <username>! You've successfully authenticated..."
```

**Step 4: Configure git to use SSH for GitHub**

```bash
# Rewrite HTTPS GitHub URLs to SSH automatically
git config --global url."git@github.com:".insteadOf "https://github.com/"
```

> ⚠️ **PITFALL:** This rewrite rule is **global** and takes precedence over
> any per-repo HTTPS URLs you set with `git remote set-url`. If a later task
> needs to push via HTTPS (e.g., using a GitHub PAT), the rewrite silently
> converts the URL to SSH and causes `Permission denied (publickey)`. Always
> check `GIT_TRACE=1` or `git config --global --list | grep insteadOf` when
> pushes fail unexpectedly. See `references/global-gitconfig-rewrite-pitfall.md`
> for a full diagnosis and fix.

**Step 5: Configure git identity**

```bash
git config --global user.name "Their Name"
git config --global user.email "their-email@example.com"
```

---

## Method 2: gh CLI Authentication

If `gh` is installed, it handles both API access and git credentials in one step.

### Interactive Browser Login (Desktop)

```bash
gh auth login
# Select: GitHub.com
# Select: HTTPS
# Authenticate via browser
```

### Token-Based Login (Headless / SSH Servers)

```bash
echo "<THEIR_TOKEN>" | gh auth login --with-token

# Set up git credentials through gh
gh auth setup-git
```

### Verify

```bash
gh auth status
```

---

## Using the GitHub API Without gh

When `gh` is not available, you can still access the full GitHub API using `curl` with a personal access token. This is how the other GitHub skills implement their fallbacks.

### Setting the Token for API Calls

```bash
# Option 1: Export as env var (preferred — keeps it out of commands)
export GITHUB_TOKEN="<token>"

# Then use in curl calls:
curl -s -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/user
```

### Extracting the Token from Git Credentials

If git credentials are already configured (via credential.helper store), the token can be extracted:

```bash
# Read from git credential store
grep "github.com" ~/.git-credentials 2>/dev/null | head -1 | sed 's|https://[^:]*:\([^@]*\)@.*|\1|'
```

### Helper: Detect Auth Method

Use this pattern at the start of any GitHub workflow:

```bash
# Try gh first, fall back to git + curl
if command -v gh &>/dev/null && gh auth status &>/dev/null; then
  echo "AUTH_METHOD=gh"
elif [ -n "$GITHUB_TOKEN" ]; then
  echo "AUTH_METHOD=curl"
elif [ -f ~/.hermes/.env ] && grep -q "^GITHUB_TOKEN=" ~/.hermes/.env; then
  export GITHUB_TOKEN=$(grep "^GITHUB_TOKEN=" ~/.hermes/.env | head -1 | cut -d= -f2 | tr -d '\n\r')
  echo "AUTH_METHOD=curl"
elif grep -q "github.com" ~/.git-credentials 2>/dev/null; then
  export GITHUB_TOKEN=$(grep "github.com" ~/.git-credentials | head -1 | sed 's|https://[^:]*:\([^@]*\)@.*|\1|')
  echo "AUTH_METHOD=curl"
else
  echo "AUTH_METHOD=none"
  echo "Need to set up authentication first"
fi
```

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `git push` asks for password | GitHub disabled password auth. Use a personal access token as the password, or switch to SSH |
| `remote: Permission to X denied` | Token may lack `repo` scope — regenerate with correct scopes |
| `fatal: Authentication failed` | Cached credentials may be stale — run `git credential reject` then re-authenticate |
| `ssh: connect to host github.com port 22: Connection refused` | Try SSH over HTTPS port: add `Host github.com` with `Port 443` and `Hostname ssh.github.com` to `~/.ssh/config` |
| Credentials not persisting | Check `git config --global credential.helper` — must be `store` or `cache` |
| Multiple GitHub accounts | Use SSH with different keys per host alias in `~/.ssh/config`, or per-repo credential URLs |
| `gh: command not found` + no sudo | Use git-only Method 1 above — no installation needed |

### Container/Sandbox Credential Helper Failure

In restricted container or sandbox environments, git's credential helper subsystem may be blocked at the syscall level — credential commands (`git credential-store get`, `git credential fill`, etc.) fail with "could not read Username" or "No such device or address" even when credentials are correctly configured in `~/.netrc` or `~/.git-credentials`. This is **not** a configuration error — it is an environment restriction.

**Symptoms:**
- `~/.netrc` or `~/.git-credentials` is correctly populated with `machine github.com\nlogin ...\npassword ...`
- `git config credential.helper "store --file ~/.netrc"` is correctly set
- `curl -u "user:token" https://api.github.com/user` works (API auth succeeds)
- `git push` fails with: `could not read Username for 'https://github.com': terminal prompts disabled`
- `git credential-store get` or `git credential fill` fails when called by git

**Diagnosis:**
```bash
# This will succeed
curl -s -u "username:PAT" https://api.github.com/user

# This will fail in a restricted environment
echo "protocol=https\nhost=github.com" | git credential fill
```

**Critical pitfall — `~/.netrc` takes priority over `credential.helper`:**

Git checks `~/.netrc` (or `~/.git-credentials`) **before** calling `credential.helper`. If `~/.netrc` contains a stale or invalid PAT, `git push` will fail with `Authentication failed` even when `credential.helper` is correctly configured and a valid token is available. The error is identical to a genuinely wrong token — `remote: Invalid username or token. Password authentication is not supported` — so this is easy to misdiagnose.

**Fix — update the netrc token directly:**
```bash
# Check what netrc currently has
cat ~/.netrc

# Option 1: Update netrc with the new token
cat > ~/.netrc << 'EOF'
machine github.com
login x-access-token
password github_pat_NEW_TOKEN_HERE
EOF
chmod 600 ~/.netrc

# Option 2: Remove netrc entirely and rely on credential.helper only
rm ~/.netrc
```

**Verified working pattern — gh auth git-credential as helper (bypasses netrc):**
```bash
# Download and extract gh (no sudo required)
curl -fsSL "https://github.com/cli/cli/releases/download/v2.93.0/gh_2.93.0_linux_amd64.tar.gz" -o /tmp/gh.tar.gz
tar -xzf /tmp/gh.tar.gz -C /tmp

# Authenticate gh with the PAT
export GH_TOKEN="github_pat_NEW_TOKEN"
/tmp/gh_2.93.0_linux_amd64/bin/gh auth status  # verify works

# Use gh as git credential helper — bypasses netrc entirely
git config --global credential.helper "/tmp/gh_2.93.0_linux_amd64/bin/gh auth git-credential"
git push origin master  # now works
```

**Why this works:** `gh auth git-credential` reads from the `GH_TOKEN` environment variable directly, completely bypassing the file-based credential chain (netrc → git-credentials → helper store) that is broken in restricted containers. This is the most reliable pattern for cron jobs running in sandboxed environments.

**Prevention for recurring cron jobs:**
Always use `gh auth git-credential` as the helper for backup/publish cron jobs running in restricted containers — netrc's priority will silently block the helper if netrc contains any token (valid or stale).

### Combined Failure Mode: Stale netrc + Global rewrite rule

**This is the most insidious failure pattern.** Both mechanisms work in isolation, but together they produce a silent deadlock:

1. `~/.gitconfig` has `url.git@github.com:.insteadOf=https://github.com/` (global rewrite)
2. `~/.netrc` contains a stale or invalid PAT
3. `credential.helper` is configured to use `gh auth git-credential` (which would work)

**What happens:** Git sees the HTTPS remote URL → rewrite rule converts it to SSH → SSH auth fails because no key is deployed → fallback to netrc → netrc has stale token → push fails with `Authentication failed`. Error message gives no clue that the rewrite rule was the real cause.

**Diagnosis (the right order):**
```bash
# 1. Check if global rewrite rule exists (this is the hidden culprit)
git config --global --list | grep insteadOf

# 2. Check netrc contents
cat ~/.netrc

# 3. Check what git ACTUALLY runs (shows the rewritten URL)
GIT_TRACE=1 git push origin main 2>&1 | grep -E "(ssh|git@|rewrite)"
```

**Fix — both steps required:**
```bash
# Step 1: Clear stale netrc entirely (remove it, don't update it)
cp /dev/null ~/.netrc && chmod 600 ~/.netrc

# Step 2: Ensure global rewrite rule points to a key that IS registered on GitHub
# If SSH key was just added, verify it works first:
ssh -T git@github.com

# Step 3: Verify rewrite rule is NOT converting HTTPS to SSH for this specific repo
# (if the intent is to use HTTPS with PAT, remove the rewrite rule instead)
git config --global --unset url.git@github.com:.insteadOf
```

**Prevention for cron jobs in restricted containers:**
- **Prefer SSH** (add key to GitHub → works reliably, no file-based credential chain)
- **Never leave stale netrc** — if switching from PAT to SSH, delete netrc completely, don't just leave an old token in it
- **Document which auth method the machine uses** — put a marker comment in netrc if it must coexist with SSH

**Prevention:** For recurring backup jobs in restricted environments, use GitHub Actions (workflow_dispatch) or a CI runner instead of pushing directly from the sandboxed host.
