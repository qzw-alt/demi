---
name: memory-management
description: Hermes Agent memory management system — multi-file wiki-style storage under /root/.hermes/.memories/ with git versioning and crash-safe update rules.
---

# Memory Management Skill

## Problem This Solves

Context compaction (260+ turns) can corrupt/empty `~/.hermes/MEMORY.md`. This happened on 2026-04-29 — an entire session's memory was lost. The fix: split memory across many files so compaction cannot wipe everything at once.

## Architecture

```
~/.hermes/
├── config.yaml                   # Hermes config (NOT git-tracked, backed up as config_backup.yaml)
├── MEMORY.md                     # 入口索引（不存核心内容）
├── memory/                       # 本地目录，非git仓库
│   └── layer4/                   #   (was initialized as git repo during 2026-05-02 — local only)
└── .memories/                   # 真实记忆（多文件）← GIT BACKED (remote: demi → qzw-alt/demi)
    ├── SCHEMA.md               # 规则定义
    ├── index.md                # 索引目录
    ├── log.md                  # 变更日志（追加型）
    ├── config_backup.yaml      # config.yaml (API keys redacted)
    ├── projects/               # 项目
    │   ├── medical-tourism.md
    │   └── oriental-destiny.md
    ├── preferences/            # 用户偏好
    │   └── weiye.md
    ├── workflows/             # 工作流程
    │   ├── blog-writing.md
    │   └── news-writing.md
    └── tech/                  # 技术配置
        └── config-changes.md
```

## Session Startup (Critical — Do This First)

Every session MUST read the `.memories/` files before doing anything else:

```bash
cat ~/.hermes/.memories/index.md
cat ~/.hermes/.memories/log.md
cat ~/.hermes/.memories/projects/*.md
cat ~/.hermes/.memories/preferences/*.md
```

## Memory Update Rules

### When to Update
- User provides new information (name, preference, project detail)
- User corrects you
- You discover something important about the environment
- A task is completed or status changes
- Config is changed

### Update Procedure
1. Find the correct file in `.memories/`
2. Update the specific file (not MEMORY.md)
3. Append a log entry to `log.md`
4. If urgent/sensitive, also update MEMORY.md entry

### What Goes Where
| Category | File |
|----------|------|
| Project details | `projects/<project-name>.md` |
| User preferences | `preferences/<name>.md` |
| Workflows | `workflows/<workflow-name>.md` |
| Config changes | `tech/config-changes.md` |
| Index/entry | `MEMORY.md` (just pointer) |
| Change history | `log.md` |

### DON'T Put in MEMORY.md
- Project operational details (use `projects/*.md`)
- User preferences (use `preferences/*.md`)
- Workflows (use `workflows/*.md`)
- MEMORY.md is only an INDEX/CATALOG pointing to real files

### What CAN Stay in MEMORY.md
- Brief catalog of what exists where
- Current active session context
- One-liner status of important projects
- The "⚠️ events" section for notable incidents

## Crash Recovery

If MEMORY.md is empty/corrupted:
1. Read `.memories/index.md` to find all memory files
2. Read `.memories/projects/*.md` for project data
3. Rebuild MEMORY.md as an index from those files
4. Log the incident in `log.md`

## Git Backup (demi Repository)

The canonical backup repo is `https://github.com/qzw-alt/demi` (remote named `demi` in `.memories/`).

### Repo Structure
```
~/.hermes/.memories/   ← git repo (remote: demi → qzw-alt/demi)
~/.hermes/memory/      ← local only, NOT git-tracked (initialized during 2026-05-02 cron)
```

### Daily Backup Workflow (CRON — runs 22:00 daily)

> ⚠️ **CRITICAL**: `~/.hermes/memory/` and `~/.hermes/.memories/` both contain embedded `.git/` directories. Do NOT run `git add` on these directories from within `~/.hermes/` — that creates nested git repo errors. Always work in a fresh clone of the demi repo.

**Step 1 — Clone demi fresh (avoids nested git issues):**
```bash
# Always clone fresh to avoid embedded .git conflicts
rm -rf ~/demi
git clone https://github.com/qzw-alt/demi.git ~/demi
```

**Step 2 — Copy .memories/ content (exclude .git):**
```bash
mkdir -p ~/demi/.memories
cp -r ~/.hermes/.memories/* ~/demi/.memories/  # copies all except .git subdirs
```

**Step 3 — Copy memory/ content (exclude .git):**
```bash
mkdir -p ~/demi/memory
cp -r ~/.hermes/memory/* ~/demi/memory/  # copies all except .git subdirs
```

**Step 4 — Backup config.yaml (redacted, via Python):**
```python
import yaml
with open('/root/.hermes/config.yaml') as f:
    config = yaml.safe_load(f)
sensitive = ['api_key', 'api_key_', 'secret', 'password', 'token', 'key']
def redact(d):
    if isinstance(d, dict):
        for k in list(d.keys()):
            if any(s in k.lower() for s in sensitive):
                d[k] = '***REDACTED***'
            elif isinstance(d[k], dict):
                redact(d[k])
    return d
redact(config)
with open('/root/demi/config_backup.yaml', 'w') as f:
    yaml.dump(config, f, default_flow_style=False)
```

**Step 5 — Commit and push:**
```bash
cd ~/demi
git add memory/ .memories/ config_backup.yaml
git commit -m "memory backup $(date +%Y-%m-%d)"
git push origin master
```

### GitHub Authentication Troubleshooting

**Credential file location:** `~/.git-credentials`  
**Format:** `https://github.com/qzw-alt:ghp_TOKEN@github.com`

**If push fails with "Authentication failed":**
1. Check if token is truncated/corrupted: `cat ~/.git-credentials`  
   - Normal: `https://github.com/qzw-alt:ghp_xxxxxxxxxxxx@github.com`  
   - BROKEN (truncated): `https://github.com/qzw-alt:github...ku07@github.com`
2. If broken: generate a new GitHub PAT at https://github.com/settings/tokens (classic, needs `repo` scope)
3. Update credentials: `git config --global credential.helper store` then `git push` and provide new token
4. Or write directly: `echo "https://github.com/qzw-alt:ghp_NEWTOKEN@github.com" > ~/.git-credentials`

**If SSH key is preferred:**
1. Ensure `~/.ssh/id_ed25519` is added to ssh-agent: `ssh-add ~/.ssh/id_ed25519`
2. Add the public key to GitHub: https://github.com/settings/keys
3. Switch remote: `git remote set-url origin git@github.com:qzw-alt/demi.git`

**If using HTTPS with working token but still failing:** GitHub requires personal access tokens, not account passwords. Password authentication was disabled in 2021.

### Handling Divergent Branches on Push

When the remote `master` has commits not in your local branch (common in cron overlaps):
```bash
git fetch origin
git merge origin/master -m "merge origin/master"
# If conflict: git add -A && git commit -m "resolve conflicts"
git push origin master
```

**⚠️ Never use `git push --force` unless explicitly approved** — it rewrites remote history and can destroy others' commits.

### Backup Log
- 2026-05-02 22:00 CST — Full backup: `.memories/` sync OK (up-to-date), `memory/` init+merge+push done, `config_backup.yaml` (redacted) pushed to demi
- 2026-05-03 22:00 CST — FAILED push: `.git-credentials` token corrupted (`github...ku07`), SSH key not registered. Backup staged locally in `~/demi/`. Auth needs repair before next push.

### Skill Version
- Created: 2026-04-29
- Updated: 2026-05-03 22:00 CST — Rewrote daily cron backup workflow: fresh clone approach (avoids nested .git conflicts), Python-based config redaction, auth troubleshooting section with corrupted token detection

## Oriental Destiny SEO (2026-04-30补充)
- 域名: https://oriental-destiny.com/
- 仓库: qzw-alt/oriental-destiny (只放网站文件)
- 完成: canonical标签(7页)、Organization+WebSite结构化数据(index.html)、内链(instant_reading/products/report_demo底部导航)
- 新增5个内容页: feng-shui-bracelet-meaning | what-is-day-master | bazi-reading-vs-zodiac | five-elements-explained | instant-reading-preview
- sitemap.xml已更新并提交Search Console

## 仓库分工规则 (强化版)
- chinahospitalsguide: 只上传网站文件
- oriental-destiny: 只上传网站文件
- demi: 备份所有文件(记忆/配置/临时)
- memory-system: 记忆系统git仓库

## 记忆系统修复
- 问题: context compression会把MEMORY.md写空(bug)
- 修复: 关闭compression.enabled + 多文件git管理
- 备份: 每日22:00推送到demi仓库
- git remote: demi(backup) + origin(memory-system)
