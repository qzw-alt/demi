# Hermes Source-Tree States: Diagnosis Reference

Companion to `hermes-upgrade` SKILL.md. This file has the detailed
diagnosis recipes for the 3 source-tree states; the SKILL.md has the
upgrade-path decision tree.

## State 1: GIT_REPO

**Signature:** `~/.hermes/hermes-agent/.git/` exists.

**Implication:** Installed via `git clone https://github.com/NousResearch/hermes-agent.git ~/.hermes/hermes-agent` followed by `pip install -e .` (or similar). The `hermes` command is a wrapper around the editable install.

**Upgrade path:** `hermes update` works directly. It runs `git pull` inside the source tree, then re-installs the editable package.

**Confirm:**
```bash
ls -la ~/.hermes/hermes-agent/.git/ | head -5
# Should see: HEAD, config, description, hooks/, info/, objects/, refs/
```

**Common sub-case:** `.git/` exists but is broken (e.g., the directory was
partially rsynced or backed-up without `.git/`). `git status` will fail.
If that happens, treat as State 2 (`NON_GIT_SOURCE_TREE`).

## State 2: NON_GIT_SOURCE_TREE

**Signature:** `~/.hermes/hermes-agent/` exists but has no `.git/`.

**Implication:** Installed via the official `install.sh`, or by extracting a
tarball, or by some other mechanism that copied the source files but not the
git metadata. This is the most common state for users who installed
Hermes via the recommended one-liner and then updated via `hermes update`
a few times — the installer does `git clone` initially but subsequent
updates via the installer (not via `hermes update`) leave a non-git
tree.

**Reproduced in:** 2026-07-11 session — 2.6 GB source tree, mtime
2026-06-20, no `.git/`, `hermes update` and `install.sh` both refused.

**Upgrade path:** Backup → `install.sh` re-run.

```bash
# Diagnose
test -d ~/.hermes/hermes-agent/.git && echo "git repo" || echo "no .git"
du -sh ~/.hermes/hermes-agent/

# Upgrade (assumes user has approved)
df -h ~/.hermes  # check disk space first
mv ~/.hermes/hermes-agent ~/.hermes/hermes-agent.bak-$(date +%Y%m%d-%H%M%S)
curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash -s -- --skip-setup
hermes --version
hermes doctor
```

**Why backup before delete:** Even though `install.sh` will git-clone a
fresh tree, having the old one as `.bak-*` lets you recover instantly if
something goes wrong with the new install (e.g., a config file got
moved, a skill is incompatible, etc.). 2.6 GB is a lot of disk, but
it's worth the safety margin.

## State 3: PIP_ONLY

**Signature:** `pip show hermes-agent` returns a version; `~/.hermes/hermes-agent/` either doesn't exist or is a git repo (if user mixed pip and source installs).

**Implication:** Installed via `pip install hermes-agent`. The Python package is installed system-wide (or in a venv), but the source tree may not be on disk at all.

**Upgrade path:** `pip install --upgrade hermes-agent`.

**Confirm:**
```bash
pip show hermes-agent
# Should output: Name, Version, Location, Requires, etc.
# Look at Location — that's the install prefix.
```

**Less common sub-case:** User has `~/.hermes/hermes-agent/` as a git
repo AND pip-installed the package separately. In that case,
**`hermes update` will update the source tree**, but `pip install
--upgrade` won't (it'll just re-install the same version into the
Python prefix). Choose one source of truth.

## State 4: ABSENT

**Signature:** `~/.hermes/hermes-agent/` doesn't exist at all.

**Implication:** User installed Hermes via `pip install` and never had a
source tree, OR deleted it manually. Common in Docker / minimal-install
scenarios.

**Upgrade path:** Same as State 3 — `pip install --upgrade hermes-agent`.
Or, if the user wants the source tree (for development or skill
authoring), run `install.sh` fresh — it'll create the tree.

## Decision flowchart

```
Is ~/.hermes/hermes-agent/ present?
├── NO → ABSENT → pip install --upgrade hermes-agent
└── YES
    ├── Is .git/ present?
    │   ├── YES → GIT_REPO → hermes update
    │   └── NO → NON_GIT_SOURCE_TREE → mv backup → install.sh
    └── (pip status doesn't matter — pip is a secondary indicator)
```

## Common confusion: which path am I on?

Quick check — `which hermes` should return one of these patterns:

| Path | Likely state |
|------|-------------|
| `/home/<user>/.local/bin/hermes` | NON_GIT_SOURCE_TREE (editable pip install from source tree, source tree has no .git) |
| `/usr/local/bin/hermes` | Either GIT_REPO or PIP_ONLY (depending on `pip show`) |
| `<venv>/bin/hermes` | PIP_ONLY inside that venv |
| Not found | HERMES NOT INSTALLED |

If you're in doubt, just run `bash ~/.hermes/skills/devops/hermes-upgrade/scripts/diagnose-hermes-install.sh` — it'll print the recommendation.
