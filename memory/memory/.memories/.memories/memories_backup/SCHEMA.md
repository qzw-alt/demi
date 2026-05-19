# 记忆系统 Schema

> 最后更新：2026-04-29

## 架构

记忆存在 `/root/.hermes/.memories/` 目录，分散成多个独立文件。

**MEMORY.md 只做索引**，真实记忆在各个子文件中。

## 目录结构

```
.memories/
├── SCHEMA.md           # 本文件 — 规则
├── index.md            # 索引目录
├── log.md              # 变更日志
├── projects/           # 项目记忆
│   ├── medical-tourism.md
│   └── oriental-destiny.md
├── preferences/        # 用户偏好
│   └── weiye.md
├── workflows/          # 工作流程
│   ├── blog-writing.md
│   └── news-writing.md
└── tech/               # 技术配置
    └── config-changes.md
```

## 规则

- 每个文件独立，context 压缩不会影响多个文件
- 每次 `memory` 工具调用后，同步更新对应文件
- 日志追加到 `log.md`
- 重要信息（项目、用户偏好、工作流程）在 `.memories/` 中持久化
- MEMORY.md 只是入口索引，不存储核心内容

## 标签说明

- `operational` — 操作流程、标准
- `decision` — 决策记录
- `episodic` — 事件记录
- `preference` — 用户偏好
