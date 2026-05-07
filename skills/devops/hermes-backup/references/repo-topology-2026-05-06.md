# Hermes Repo Topology — 2026-05-06

## Actual Directory Structure

```
~/.hermes/                        # NOT a useful git repo (it's NousResearch/hermes-agent checkout)
│                                 # Remote: upstream → NousResearch/hermes-agent
│                                 # Remote: demi-backup → qzw-alt/demi (added during session)
├── memory/                       # IS a git repo (subdirectory, separate from ~/.hermes)
│   # Remote: demi → qzw-alt/demi
│   # Remote: (origin not configured in this repo)
│   └── memory/                   # daily memory files go here
│
├── .memories/                   # IS a git repo
│   # Remote: origin → qzw-alt/memory-system (primary push)
│   # Remote: demi → qzw-alt/demi (secondary push)
│   └── (memory system files)
│
├── config.yaml                  # NOT tracked in any git repo (needs explicit handling)
│
└── (other hermes-agent files: SOUL.md, MEMORY.md, skills/, etc.)
```

## Key Discovery

`~/.hermes/` itself is NOT a git repo for backup purposes. The backup repos are:
- `~/.hermes/memory/` (the `memory/` subdirectory is its own repo)
- `~/.hermes/.memories/` (the `.memories/` subdirectory is its own repo)

This explains the confusing error pattern: checking `~/.hermes/.git` shows it's a git repo
(it's the NousResearch worktree), but `cd ~/.hermes && git push origin` fails because
`origin` doesn't exist there — `origin` is in `.memories/` and `demi` is in `memory/`.

## Remote Configuration Found

### ~/.hermes/memory/.git/config
```
[remote "demi"]
    url = https://github...ku07@github.com/qzw-alt/demi.git
```

### ~/.hermes/.memories/.git/config
```
[remote "origin"]
    url = https://github...ku07@github.com/qzw-alt/memory-system.git
[remote "demi"]
    url = https://github...ku07@github.com/qzw-alt/demi.git
```

### ~/.hermes/.git/config
```
[remote "upstream"]
    url = https://github.com/NousResearch/hermes-agent.git
[remote "demi-backup"]
    url = https://github.com/qzw-alt/demi.git
```
Note: demi-backup was ADDED during this session (2026-05-06) — may not persist.

## Error Log

### Error 1: "fatal: 'origin' does not appear to be a git repository"
Cause: `~/.hermes/` (not `~/.hermes/memory/` or `~/.hermes/.memories/`) was the working directory.
Origin remote only exists in `.memories/` repo, not in `memory/` repo.

### Error 2: "rejected master -> master (non-fast-forward)"
Cause: Remote `qzw-alt/demi` master has commits not in local branch.
Resolution: Push to dated branch instead (`memory-backup-YYYY-MM-DD`).

### Error 3: "refusing to merge unrelated histories"
Cause: Attempted `git merge demi-backup/master` in ~/.hermes which has unrelated history.
Do NOT merge across repos.

## demi repo branch structure (qzw-alt/demi)
```
master                        - 2026-05-05 snapshot (remote divergent)
memory-backup-2026-05-06     - memory/ snapshot (pushed today)
memories-backup-2026-05-06   - .memories/ snapshot (pushed today)
bali-article-2026-04-19      - article branch
```
