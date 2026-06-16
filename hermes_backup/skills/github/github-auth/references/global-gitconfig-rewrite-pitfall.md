# Global gitconfig `url.*.insteadOf` Rewrite Pitfall

## Problem

A global git rewrite rule in `~/.gitconfig`:

```ini
[url "git@github.com:"]
    insteadOf = https://github.com/
```

...silently rewrites **all** HTTPS GitHub URLs to SSH, even when:
- The local `remote.origin.url` is explicitly set to `https://github.com/owner/repo.git`
- The push command explicitly uses an HTTPS URL

## Symptom

```
git remote -v
# origin  https://github.com/qzw-alt/demi.git (push)
# origin  https://github.com/qzw-alt/demi.git (fetch)

git push origin main
# git@github.com: Permission denied (publickey).
# fatal: Could not read from remote repository.
```

`git remote -v` shows HTTPS, but git internally rewrites to SSH before connecting.

## Diagnosis

```bash
# Check global git config for rewrite rules
git config --global --list | grep insteadOf

# Or directly
cat ~/.gitconfig

# GIT_TRACE shows the actual command git runs
GIT_TRACE=1 git push origin main
# Shows: ssh -i ~/.ssh/id_ed25519 ... git@github.com 'git-receive-pack ...'
# (proves URL was rewritten to SSH)
```

## Fix

Remove the rewrite rule from global config. Edit `~/.gitconfig` directly:

```
# Find the [url "git@github.com:"] section and remove it entirely,
# including its insteadOf line.
```

The rewrite happens because git processes the URL rewrite **after** the local
remote URL is read — so `remote.origin.url=https://...` gets converted to
`git@github.com:` before any network call is made.

## Key Insight

`git remote set-url origin https://...` only changes the local remote URL,
but the **global rewrite rule takes precedence** at connection time. The
remote shows HTTPS in all git commands, but git internally converts it
before any network call.

## Prevention

For machines that need both SSH (for some repos) and HTTPS (for others):
- Remove the global rewrite rule
- Add per-host SSH config: `~/.ssh/config` with key selection per host
- Or scope `insteadOf` to specific paths, not the full domain
