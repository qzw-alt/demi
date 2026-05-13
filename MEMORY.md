# MEMORY.md — 德米长期记忆

> **单一真实源** — 本文件是所有关键信息的唯一真实来源
> **单一记忆位置** — `/root/.hermes/hermes-agent/memory/`（4-Layer体系）
> **最后更新**: 2026-05-13

---

## 📍 单一记忆位置规则

**只有一个地方存放记忆：**
```
~/.hermes/hermes-agent/memory/
├── layer2/          ← 每日日志（14天后→归档到cold/）
├── layer3/           ← 决策/偏好/项目（永久）
├── layer4/           ← 技能SOP/知识参考（永久）
└── cold/             ← 历史归档（只归档不删除）
```

**其他位置（已废弃/归档）：**
- `~/.hermes/memory/.memories/memory/` — git worktree，已归档
- `~/.hermes/.memories/` — 备份仓库，已归档
- `~/.openclaw/workspace/memory/` — OpenClaw遗留，已废弃

**所有记忆读写都在：`/root/.hermes/hermes-agent/memory/`**

---

## 🔒 三条铁律

1. **宁可多存不少存** — 存了不用不占空间，删了丢了花大量时间
2. **operational 内容永不压缩** — Token/密码/配置/路径/原始凭证
3. **归档不删除** — 超过14天的layer2原文归档到cold/，不删除

---

## 🗂️ 记忆分类原则

| 类型 | 处理方式 |
|------|---------|
| operational（密码/Token/配置/路径） | 原封不动保存，永不压缩 |
| decision（决策+具体参数） | 保存+标注来源 |
| episodic（事件摘要） | 可提炼压缩 |

---

## 👤 用户：伟烨

详见：`memory/layer3/preferences.md`

---

## 🔴 当前项目

| 项目 | 域名 | 状态 |
|------|------|------|
| 医疗旅游 | chinahospitalsguide.com | 运营中 |
| Oriental Destiny | oriental-destiny.com | SEO待修复 |

**仓库：**
- 网站：`qzw-alt/chinahospitalsguide`
- 备份：`qzw-alt/demi`

---

## ⏰ 定时任务（6个，CST）

| 时间 | 任务 |
|------|------|
| 07:00 | 医疗新闻写作 |
| 02:00 | Moltbook社区学习 |
| 03:00 | 医疗旅游资讯收集 |
| 06:00 | AI重大信息搜集 |
| 06:30 | 晨间记忆读取 |
| 22:00 | 总结+保存 |

---

## 📝 写作标准流程

新闻：`memory/layer4/sops/news-writing-sop.md`
博客：`memory/layer4/sops/blog-writing-sop.md`

---

## 🔑 API Keys（operational）

- **GitHub Token**: `GHP_MI_TOKEN`（环境变量）
- **Kimi API**: `KIMI_API_KEY`（环境变量）
- **Tavily API**: `TAVILY_API_KEY`（环境变量）

---

## ⚠️ 重要规则

### 记忆同步规则
- 每次会话启动：读 `memory/YYYY-MM-DD.md`（今日+昨日）
- 主会话：额外读 `MEMORY.md`
- 所有读写操作只对 `~/.hermes/hermes-agent/memory/` 进行

### 每日日志缺失问题（2026-04-20 ~ 2026-05-12）
- 这23天没有layer2日志
- 期间cron jobs在运行（ai-news生成了），但没有写每日日志
- 不补写（无法回忆真实内容），标记说明即可

### OpenClaw迁移完成（2026-05-13）
- 记忆已统一到 `~/.hermes/hermes-agent/memory/`
- OpenClaw workspace 仍保留但不再使用
- 从OpenClaw迁移了：USER.md、HEARTBEAT.md、TOOLS.md、2026-04-25.md

### 每日日志强制规则
> **每次会话结束前必须写每日日志** — 这是铁律

- 路径：`memory/layer2/YYYY-MM-DD.md`
- 即使当天没什么重大进展，也要写一行说明"日常维护，无重大事件"
- 日志内容包括：做了什么事、决策、问题、待办
- 每天只能有一篇日志（合并，不要重复创建）

### GitHub备份规则
> **记忆必须备份到 demi 仓库**

**备份频率**：每天22:00（随总结任务一起）
**备份目标**：`git push demi main`（推送到 `qzw-alt/demi`）
**备份内容**：整个 `memory/` 目录（4-Layer全部内容）

**备份流程（22:00总结任务的一部分）**：
1. 检查 `memory/` 是否有今日日志（必须！）
2. `git add memory/` → commit → push to demi
3. 如果 push 失败，记录错误，人工干预

**仓库地址**：
- 备份仓库：`https://github.com/qzw-alt/demi.git`
- 远程名：`demi`（已添加到hermes-agent git remote）

---
