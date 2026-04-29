# 记忆变更日志

> 追加型日志，每次记忆变更都记录在这里

## 2026-04-29

### 初始化多文件记忆系统
- 从 MEMORY.md 拆出 6 个独立文件
- 原因：context compaction 把 MEMORY.md 清空，丢失了大量记忆
- 解决：多文件分散存储，context 压缩不会同时影响多个文件

**创建的文件：**
- `.memories/SCHEMA.md`
- `.memories/index.md`
- `.memories/log.md`
- `.memories/projects/medical-tourism.md`
- `.memories/projects/oriental-destiny.md`
- `.memories/preferences/weiye.md`
- `.memories/workflows/blog-writing.md`
- `.memories/workflows/news-writing.md`

### MEMORY.md 被清空事件
- 原因：260条对话被压缩，压缩系统的摘要输出覆盖了 MEMORY.md
- 教训：单文件存储是单点故障
- 修复：从 `memories/MEMORY.md` 恢复旧备份（4,531字符）

### 配置变更
- `compression.enabled: false` — 关闭上下文压缩（压缩服务401报错）
