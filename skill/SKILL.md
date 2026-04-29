---
name: memory-system
description: 4层记忆管理系统 for AI agents。基于 provenance layer + staleness 追踪 + if-then 规则记忆设计。适用于：(1) 建立或改进记忆系统 (2) 遇到"记忆混乱/丢失"问题 (3) 新 session 无法恢复上下文 (4) 需要快速从零恢复工作状态。核心原则：operational 内容永不压缩，48小时晋升法则，Replace-Only 而非 append-only。
---

# 记忆管理系统 (Memory System v2.0)

> 基于 Moltbook m/memory 社区原则验证，2026-03-24

---

## 三条铁律

1. **宁可多存不少存** — 存了不用不占空间，删了丢了花大量时间
2. **operational 内容永远不压缩** — Token/密码/配置/路径/原始凭证
3. **归档不删除** — 超过14天的内容归档到 layer3，不删除原文

---

## 4层记忆体系

| Layer | 内容 | 保留时间 | 处理方式 |
|-------|------|---------|---------|
| L1 | 当前会话 | 会话结束 | 内存 |
| L2 | 每日日志+操作细节 | 14天后归档 | 原文归档，不删除 |
| L3 | 提炼知识+原始记录 | 永久 | operational永不压缩 |
| L4 | 工具/SOP/参考 | 永久 | 原封不动 |

---

## 记忆分类（每条记忆必须带 @type 标签）

| @type | 内容 | 处理 |
|-------|------|------|
| `operational` | Token/密码/配置/路径/原始凭证 | 原封不动，永不压缩 |
| `episodic` | 事件描述/日志/进展 | 可提炼，原文归档 |
| `decision` | 决策结论+参数+原因 | 保留，不压缩 |
| `rule` | if-then 生成规则 | 保留，标来源 |

---

## 核心模板（按需读取）

### 模板A：规则记忆（Rule Memory）
```markdown
## [规则名称]

<!-- @type: rule -->
<!-- @stability: [high|medium|low] -->
<!-- @decay_class: [live-data|structural|framework|static] -->
<!-- @source: [来源] -->
<!-- @retrieved: [最近验证日期] -->

### 规则内容
IF [条件] THEN [结论]

### 来源证据
> "[原始观察]" — [来源]

### 适用场景
- [场景A]
- [场景B]

### 验证记录
- 2026-03-24：✅ 验证过，仍成立
```

### 模板B：决策记忆（Decision Memory）
```markdown
## [决策名称]

<!-- @type: decision -->
<!-- @decay_class: static -->

### 决策结论
[最终选择]

### 决策参数
- 参数A: [值]

### 为什么选这个
[决策原因，必须写]

### 备选方案
- 方案X：没选，因为...
```

### 模板C：操作记忆（Operational Memory）
```markdown
## [操作名称]

<!-- @type: operational -->

### 操作步骤
1. [步骤1]
2. [步骤2]

### 原始凭证
```
[命令/配置 - 原文]
```

### 验证结果
✅/❌ [日期] [结果]
```

### 模板D：每日日志
```markdown
# 每日日志 [日期]

## 今日事件
- [时间] [事件描述]

## patterns（跨文件模式捕捉）
- [重复出现的模式] → 提炼成规则

## operational 记录
- [Token更新/配置变更等]

## 待处理事项
- [ ] [事项]
```

---

## 核心改进（必须遵守）

### 1. Provenance Layer（来源层）
每条外部观察记忆必须包含：
```markdown
@provenance: source=[来源], fetched_at=[时间], confidence=[level], decay_class=[类别]
```

**衰减类别**：
- `live-data`：价格/库存，分钟级衰减
- `structural`：市场格局，周级衰减
- `framework`：战略/平台规则，月级衰减
- `static`：身份/价值观，基本不衰减

### 2. Staleness 追踪
关键记忆标记 `retrieved`，过期自动提醒：
- live-data: >1小时 → 过期
- structural: >1周 → 过期
- framework: >1月 → 需确认
- static: >3月 → 需确认

### 3. 48小时晋升法则
Layer2 超过48小时没晋升到 MEMORY.md → 归档或删除

### 4. Replace-Only
同一主题只保留**一个当前最准确版本**，旧版归档，不堆积

### 5. Retrieval-First
写记忆前先问：**未来我怎么找到这条？**
- 想清楚检索关键词
- 把关键词写入"适用场景"部分
- 再写内容

### 6. patterns 捕捉
每日日志增加 `patterns` 区域：
- 同一个问题出现第三次 → 提炼成 if-then 规则
- 写入 layer3/decisions/[规则名].md

---

## 快速恢复指南

> 系统崩溃/新环境启动，按这个顺序恢复：

1. **MEMORY.md** → 关键信息+结构
2. **memory-sop.md** → 操作规则
3. **layer3/decisions/** → 所有决策+规则
4. **layer3/WARM_MEMORY.md** → 当前项目状态
5. **layer2 最新3天** → 最近发生了什么

---

## 参考文件

详细模板和完整 SOP：读取 `references/memory-sop-v2.md`
