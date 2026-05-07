# 决策记录

---

## 2026-04-28：记忆系统重建

**问题**：4月份太忙，MEMORY.md 一个月没更新，加上 OpenClaw 共用 workspace 导致4/18-4/27日志丢失，"德米变得健忘"。

**决策**：
- 简化记忆架构，取消四层复杂设计
- 新结构：`memory/daily/` + `memory/projects/` + `memory/decisions/` + `memory/personals/`
- MEMORY.md 作为唯一入口，每次会话优先读取
- 每日会话结束写 daily log，cronjob 22:00 自动备份到 GitHub
- 项目状态用 projects/README.md 追踪，避免靠脑子记

**不再使用的旧结构**：layer2/3/4（已保留但新内容不再写入）

_记录：2026-04-28 08:00_
