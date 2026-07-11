---
name: hermes-upgrade
description: "Upgrade the Hermes Agent installation itself — diagnose source-tree state, pick the right upgrade path (git-pull / install.sh / pip), and handle the 2.6 GB backup-rebuild case. Triggers: '升级 hermes', 'update hermes', 'hermes update failed', 'latest version of hermes', 'upgrade Hermes Agent to X.Y', 'hermes-agent 不是 git repo', 'Not a git repository' from hermes update / install.sh."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [hermes, upgrade, update, install, migration]
---

# Hermes Agent Upgrade

Upgrade the Hermes Agent installation on this machine. This skill covers the
decision-tree and pitfalls the user (and a future you) will hit when `hermes
update` doesn't just work — which is the **common case**, not the exception.

For general Hermes commands / config / troubleshooting, see the bundled
`hermes-agent` skill. This skill is specifically about **upgrading the
Hermes Agent installation itself**.

## Trigger conditions

Load this skill when ANY of these come up:

- User says "升级 Hermes / update hermes / 升级到 X.Y"
- `hermes --version` shows "Update available: N commit behind — run `hermes update`"
- `hermes update` fails with `✗ Not a git repository`
- `curl ... install.sh | bash` fails with `✗ Directory exists but is not a git repository`
- User wants to know which upgrade path to use, or whether to upgrade at all
- After a fresh Hermes install, to verify the upgrade path that was used

## The 3-step workflow

### Step 1: Diagnose current installation state

Before choosing a path, **always** run the diagnostic script (or the inline
commands) to understand HOW this Hermes was installed. The 3 paths diverge
based on whether `~/.hermes/hermes-agent/` is a git repo, a non-git source
tree, or absent entirely.

```bash
# Quick check (run inline if script not available):
ls -la ~/.hermes/hermes-agent/.git 2>/dev/null && echo "GIT_REPO=yes" || echo "GIT_REPO=no"
du -sh ~/.hermes/hermes-agent/ 2>/dev/null
stat -c '%y %n' ~/.hermes/hermes-agent/ 2>/dev/null | head -1
which hermes
pip show hermes-agent 2>&1 | head -3
```

Or run the bundled diagnostic script:

```bash
bash ~/.hermes/skills/devops/hermes-upgrade/scripts/diagnose-hermes-install.sh
```

It prints one of three states:

| State | Meaning | Upgrade path |
|-------|---------|--------------|
| `GIT_REPO` | Installed via `git clone` + `pip install -e` | `hermes update` works directly |
| `NON_GIT_SOURCE_TREE` | Installed via installer script or manual extract; `.git/` is missing but the directory is intact | Backup → `install.sh` → restore |
| `PIP_ONLY` | Installed via `pip install hermes-agent`; `~/.hermes/hermes-agent/` may not even exist | `pip install --upgrade hermes-agent` |
| `ABSENT` | `~/.hermes/hermes-agent/` doesn't exist at all | `install.sh` works (creates fresh clone) |

### Step 2: Choose upgrade path

**Path A — `hermes update`** (only if State = `GIT_REPO`)

```bash
hermes update
hermes --version
hermes doctor
```

This is the official "happy path". It runs `git pull` inside the source tree.

**Path B — Backup + reinstall via official script** (State = `NON_GIT_SOURCE_TREE`)

This is the most common case for the user — it's what happened in the
2026-07-11 session. The directory exists but lacks `.git/`. Both `hermes
update` AND the official `install.sh` reject it.

```bash
# 1. Backup the source tree (do NOT delete — preserve for forensics)
mv ~/.hermes/hermes-agent ~/.hermes/hermes-agent.bak-$(date +%Y%m%d-%H%M%S)

# 2. Run installer (will git clone a fresh checkout)
curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash -s -- --skip-setup

# 3. Verify
hermes --version
hermes doctor

# 4. Restart gateway (if running) to pick up new version
hermes gateway restart 2>/dev/null || true
```

**Why `--skip-setup`:** the installer otherwise runs `hermes setup`, which
launches an interactive wizard and may overwrite the user's `config.yaml` /
`.env` / `auth.json`. Skip it; user can run `hermes doctor --fix` manually
if they want to migrate config.

**Path C — `pip install --upgrade`** (State = `PIP_ONLY`)

```bash
pip install --upgrade hermes-agent
hermes --version
```

This is rare for end-users — most use the official installer.

**Path D — `git init` + manual fetch** (last resort, when Path B's backup
step is unacceptable for disk reasons)

```bash
cd ~/.hermes/hermes-agent
git init
git remote add origin https://github.com/NousResearch/hermes-agent.git
git fetch origin
git checkout -b main origin/main  # may conflict with local files
```

⚠️ **Don't recommend this by default.** The local source tree may have
local edits (it shouldn't, but verify) and will conflict with upstream
main. Only use if disk space is a concern AND you have verified there are
no local modifications (`git diff` after init should be empty if HEAD == the
upstream commit that the directory was extracted from — it usually won't be).

### Step 3: Verify

Always run after any upgrade:

```bash
hermes --version        # confirm version string changed
hermes doctor           # check dependencies, config, secrets
hermes config check     # config migration needed?
hermes migrate          # if config check flags anything
```

Then **open a NEW session** to continue working. The
[per-conversation prompt caching invariant](https://hermes-agent.nousresearch.com/docs/)
means upgrading mid-session invalidates the cache; finishing the upgrade
and then continuing in the same session loses the benefit.

## Pitfalls

### `hermes update` and `install.sh` both fail on non-git source trees

This is the most common pitfall. The user's setup (2026-07-11) had
`~/.hermes/hermes-agent/` as a 2.6 GB extracted source tree with no `.git/`.
Both upgrade commands refuse to operate:

- `hermes update` → `✗ Not a git repository. Please reinstall:`
- `curl ... | bash` → `✗ Directory exists but is not a git repository:`

The installer deliberately refuses (to avoid clobbering uncommitted local
edits), and `hermes update` can't `git pull` a non-repo. Always diagnose
first; never assume `hermes update` will work.

### Don't delete the old source tree before verifying the new install works

The backup-rename pattern (`mv ~/.hermes/hermes-agent ~/.hermes/hermes-agent.bak-...`)
is the right move — even at 2.6 GB. If the new install fails for any
reason, you can `rm -rf ~/.hermes/hermes-agent && mv ~/.hermes/hermes-agent.bak-... ~/.hermes/hermes-agent` to restore the working state. **Do not** `rm -rf` the old tree before confirming the new version works.

### `--skip-setup` is load-bearing

Without `--skip-setup`, the installer runs the interactive setup wizard,
which (in non-interactive pipe context) will either:
- Hang waiting for input
- Silently overwrite `config.yaml` / `.env` / `auth.json` from stdin defaults

Both are bad. **Always** add `--skip-setup` unless the user explicitly asks
to re-run setup. Setup can be done manually with `hermes setup` or
`hermes doctor --fix` after the upgrade.

### Gateway restart is required, but `hermes update` doesn't always do it

If the user has the gateway running (Feishu / Telegram / etc.), the running
Python process still has the OLD code loaded. After upgrading:

```bash
hermes gateway restart
```

Or if running in foreground (no systemd): kill and restart manually. Tell
the user to expect 1-3 minutes of message interruption.

### Prompt cache invalidates — open a new session

The Hermes prompt-cache invariant: changing the system prompt / toolset /
Hermes version mid-conversation invalidates the cache. After upgrading,
**the user should `/new` (or `/reset`) before continuing**. Don't keep
working in the same session — every subsequent turn will pay full token
cost for the system prompt.

### "1 commit behind" doesn't mean a version bump

`hermes --version` output like "Update available: 1 commit behind" usually
means **a single patch commit ahead**, not a new minor version. The user
might say "upgrade to 0.18" when the upstream is actually 0.17.1. Don't
promise version numbers — verify with `hermes --version` AFTER the
upgrade and report the actual new version.

### Memory and skills live OUTSIDE the source tree

The user's persistent data is in `~/.hermes/memories/`, `~/.hermes/skills/`,
`~/.hermes/cron/`, `~/.hermes/config.yaml`, `~/.hermes/.env`, etc. — none
of which are inside `~/.hermes/hermes-agent/`. Upgrading the source tree
**does not touch any of this**. Verify with `ls ~/.hermes/memories/` before
and after — the file list should be identical.

### Don't suggest "weekly auto-upgrade cron" by default

The user may have considered it, may have it, or may have explicitly
rejected it. Ask first. Auto-upgrading the core agent means the user can't
control when `prompt caching invalidates`, when their session becomes
incompatible with the new version, or when an upstream change breaks a
skill. Most users prefer manual upgrades.

### When in doubt, ask the user before destructive operations

If the diagnostic shows state = `NON_GIT_SOURCE_TREE` and the directory is
2+ GB, ASK before `mv`-ing. The user might:
- Want to keep the old tree for a few days as a safety net
- Have a reason for the non-git layout (e.g., extracted from a tarball)
- Want to take a backup to external storage first

A `mv` is reversible (rename within the same filesystem is fast and
free), but disk space on `/` might be tight. Check `df -h ~/.hermes/`
before backing up, and warn the user if free space is < 5 GB.

## Verification

After any upgrade, verify these are consistent:

| Check | Expected |
|-------|----------|
| `hermes --version` | New version string |
| `~/.hermes/memories/` | Same files as before (memories preserved) |
| `~/.hermes/skills/` | Same skills (skills preserved) |
| `~/.hermes/config.yaml` | User's settings preserved |
| `~/.hermes/.env` | API keys preserved |
| `~/.hermes/hermes-agent/` | Either empty (absent) or a fresh git repo (has `.git/`) |
| `~/.hermes/hermes-agent.bak-*/` | Old source tree, if backed up |
| Gateway | Reachable on the same platform(s) |

## Related

- Bundled `hermes-agent` skill — for general config, CLI, troubleshooting
- `hermes-backup` skill — for backing up user data to GitHub before/after
- `hermes-cron-troubleshooting` skill — for cron-related issues, not upgrade
- `memory-hygiene` skill — if upgrading triggers config migration questions
