---
name: hermes-backup
description: Nightly memory backup to GitHub. Covers the multi-repo structure of ~/.hermes, remote configuration patterns, non-fast-forward handling, and API key redaction for config.yaml.
version: 1.0.0
metadata:
  hermes:
    tags: [backup, git, memory, cron, demi]
    schedule: "0 22 * * *"  # 每天22:00执行
    related_skills: [kanban-orchestrator, kanban-worker]
---

# Hermes Backup — Nightly Memory Sync to GitHub

## Repo Structure (CRITICAL — know before you push)

`~/.hermes` is NOT a single git repo. It contains multiple nested git repositories:

```
~/.hermes/                    # git repo → NousResearch/hermes-agent (upstream)
├── memory/                   # git repo → qzw-alt/demi (remote: demi)
│   └── memory/               # today's daily memory files
├── .memories/                # git repo → qzw-alt/memory-system (origin) + qzw-alt/demi (demi)
│   └── (memory system files)
├── config.yaml               # NOT tracked in ~/.hermes git repo
└── (other hermes files)
```

**Before pushing, always check `git remote -v`** in the target directory. The same logical name (e.g. `demi`) may point to different actual URLs in different sub-repos.

## Remote Map

| Directory | Remote | URL | Notes |
|-----------|--------|-----|-------|
| `~/.hermes/memory/` | `demi` | `qzw-alt/demi` | memory backup target |
| `~/.hermes/.memories/` | `origin` | `qzw-alt/memory-system` | primary push target |
| `~/.hermes/.memories/` | `demi` | `qzw-alt/demi` | secondary push target |
| `~/.hermes/` | `demi-backup` | `qzw-alt/demi` | config backup target |

## Workflow

### 1. memory/ backup (to demi)

```bash
cd ~/.hermes/memory
git add memory/
git commit -m "memory backup $(date +%Y-%m-%d)"
git push demi master
```

### 2. .memories/ sync

```bash
cd ~/.hermes/.memories
git add -A
git commit -m "memories sync $(date +%Y-%m-%d)"
git push origin master   # primary: memory-system repo
git push demi master     # secondary: demi repo
```

### 3. config.yaml backup (to demi, dated branch)

API keys must be redacted before pushing:

```bash
cp ~/.hermes/config.yaml /tmp/config_backup.yaml
sed -i 's/api_key:.*/api_key: ***REDACTED***/g; s/secret:.*/secret: ***REDACTED***/g; s/token:.*/token: ***REDACTED***/g' /tmp/config_backup.yaml

cd ~/.hermes
git checkout -b config-backup-$(date +%Y-%m-%d)
cp /tmp/config_backup.yaml ~/.hermes/demi_config.yaml
git add demi_config.yaml
git commit -m "config backup $(date +%Y-%m-%d)"
git push demi-backup config-backup-$(date +%Y-%m-%d):config-backup-$(date +%Y-%m-%d)
```

## Non-Fast-Forward Error Handling

If `git push demi master` fails with `! [rejected] master -> master (non-fast-forward)`:

**Do NOT force push.** Instead push to a dated backup branch:

```bash
git push demi master:memory-backup-$(date +%Y-%m-%d)
```

Remote already has a `master` with divergent history — use timestamped branches to preserve both histories.

## API Key Redaction Patterns

Redact these fields in config.yaml before any GitHub push:
- `api_key`
- `secret`  
- `token`
- `password`
- `private_key`

Use `***REDACTED***` as the replacement value.

## Verification

After push, confirm branches exist on remote:
```bash
git ls-remote demi --heads  # list remote branches
```

## References

- `references/repo-topology-2026-05-06.md` — Full topology of all ~/.hermes git repos, remote URLs, and the error patterns encountered during the 2026-05-06 session.
