# GitHub Fine-Grained PAT Format & git-credential Priority Pitfalls

## Problem 1: Fine-Grained PAT Format

GitHub Fine-Grained PATs start with `github_pat_` prefix and are ~111 chars total.
Classic PATs start with `ghp_` and are 40 chars.

**Critical difference:** When embedded in HTTPS URLs:
- Classic PAT `ghp_xxx` → works with `https://user:ghp_xxx@github.com/repo`
- Fine-Grained PAT `github_pat_xxx` → **fails** with `remote: Invalid username or token`

The Fine-Grained PAT format causes GitHub to reject the credentials even when the token
is valid, because the server-side auth flow handles the two formats differently.

## Symptom

```bash
# PAT validates against API fine
curl -u "user:github_pat_xxx" https://api.github.com/user  # → 200

# But git push fails
git push https://user:github_pat_xxx@github.com/repo master
# → remote: Invalid username or token. Password authentication is not supported
```

## Diagnosis

```python
import urllib.request
pat = "github_pat_xxx"
req = urllib.request.Request(
    "https://api.github.com/user",
    headers={"Authorization": f"Bearer {pat}", "Accept": "application/vnd.github+json"}
)
with urllib.request.urlopen(req) as r:
    print(r.status)  # 200 = token valid but format still fails git
```

## Solution: Use git-credential helper (not URL embedding)

Do NOT embed Fine-Grained PATs directly in git remote URLs. Instead, use a
git-credential helper that reads the PAT from a file:

```python
#!/usr/bin/env python3
# /tmp/gh-pat-helper.py — safe credential helper for Fine-Grained PATs
import sys
with open('/tmp/backup-pat.txt') as f:
    pat = f.read().strip()
print(f"username={username}")
print(f"password={pat}")
```

```bash
git config --global credential.helper '/tmp/gh-pat-helper.py'
# Then push normally — git calls the helper to get credentials
git push https://github.com/owner/repo.git master
```

## Problem 2: git-credential Helper Priority Over netrc

Git checks credentials in this order:
1. `~/.netrc` — **highest priority**, takes precedence over everything
2. `credential.helper` — only consulted if netrc is absent or empty
3. `~/.git-credentials` — file-based store

If `~/.netrc` exists with ANY token content (even an invalid/stale one),
the credential helper is never called.

## Symptom

```bash
cat ~/.netrc
# machine github.com\nlogin x-access-token\npassword github_pat_xxx\n

git config --global credential.helper '/path/to/gh-auth-git-credential'
git push origin master
# → Authentication failed (helper was never called)
```

## Diagnosis

```bash
# 1. Check if netrc exists
cat ~/.netrc

# 2. Check credential helper config
git config --global --list | grep credential

# 3. GIT_TRACE proves helper IS called but netrc takes priority
GIT_TRACE=1 git push origin master
# Shows helper running, but netrc content wins
```

## Fix: Remove netrc entirely

```bash
rm ~/.netrc          # deletes stale netrc, lets helper run
# OR update netrc with the new valid token
```

**Prevention:** For cron jobs in restricted environments, always use `gh auth git-credential`
(which reads `GH_TOKEN` env var directly) as the helper — it bypasses the entire
netrc → git-credentials → helper chain.

## Combined Failure Mode

Both pitfalls can stack:
1. Fine-Grained PAT embedded in URL → fails
2. netrc contains stale token → credential helper never called
3. Push fails with no actionable error message

Fix both: remove stale netrc AND use credential helper reading from file.

## Prevention for Recurring Cron Backup Jobs

For backup cron jobs running Fine-Grained PATs:
- Store PAT in `/tmp/backup-pat.txt` (or similar)
- Write a credential helper that reads from that file
- Remove or empty `~/.netrc`
- Verify with `GIT_TRACE=1 git push` before scheduling