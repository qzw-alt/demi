# 德米记忆管理系统 skill 📝

> 德米专属记忆管理技能文档
> 版本：1.0 | 更新：2026-03-22
> 基于 4-Layer 架构 + 存储系统最佳实践

---

## 核心架构

```
德米记忆系统
├── Layer 1: Session          ← 当前会话上下文（内存，结束时消失）
├── Layer 2: Short-Term        ← 每日日志（14天自动归档）
├── Layer 3: Long-Term         ← 永久知识（提炼+原始存档）
└── Layer 4: Reference        ← 参考/SOP/技能文档

关键文件：
├── MEMORY.md                  ← 入口索引，唯一真实来源
├── memory/layer3/decisions/memory-changelog.md ← 变更记录（append-only）
└── memory/layer4/memory-sop.md ← 本SOP文档
```

---

## 文件结构

```
memory/
├── layer2/                              ← 每日日志（14天）
│   └── YYYY-MM-DD.md                    ← 格式：<!-- @type: episodic -->
├── layer3/                              ← 永久知识
│   ├── MEMORY.md                       ← ⚠️ 入口索引，唯一真实来源
│   ├── preferences.md                  ← 用户偏好（@type: operational）
│   ├── decisions/                      ← 决策记录
│   │   ├── memory-changelog.md        ← 关键信息变更记录（append-only）
│   │   ├── 踩坑_xxx.md               ← 踩坑记录
│   │   └── 决策_xxx.md               ← 决策记录
│   ├── projects/                       ← 项目资料
│   │   └── 医疗旅游/
│   │       ├── 医疗旅游_detailed.md   ← 核心档案（@type: operational）
│   │       └── ...
│   └── WARM_MEMORY.md                 ← 温记忆
├── layer4/                              ← 参考层
│   ├── skills/                        ← 技能使用记录
│   ├── sops/                          ← 标准操作流程
│   ├── knowledge/                     ← 参考知识
│   ├── memory-sop.md                  ← 记忆管理SOP（本文档）
│   └── demi-memory-system.md          ← 记忆架构总览
└── cold/                               ← 历史归档（只归档不删除）
```

---

## 标签系统

每个记忆文件头部必须标注：

```markdown
<!-- @type: operational -->   ← 操作细节（永不压缩/删除）
<!-- @type: episodic -->      ← 事件摘要（可提炼）
<!-- @type: decision -->      ← 决策结论（保留）
<!-- @stability: high -->    ← 稳定性高（事实，不该变）
<!-- @stability: medium -->  ← 稳定性中（判断，可能更新）
```

### @type 详细说明

| 类型 | 内容 | 处理方式 |
|------|------|---------|
| **operational** | 账号密码、Token、配置、地址、操作步骤 | 原封不动，永远不压缩/删除 |
| **episodic** | 事件摘要、日志、讨论记录 | 可提炼，但原文必须保留 |
| **decision** | 决策结论 + 具体参数 + 决策原因 | 保留，不压缩 |

### @stability 详细说明

| 级别 | 含义 | 示例 |
|------|------|------|
| **high** | 事实性内容，不该变 | API Key、仓库地址、合同条款 |
| **medium** | 判断性内容，可能更新 | 偏好、分析、解读 |
| **low** | 临时性内容，可覆盖 | 草稿、临时笔记 |

---

## 核心原则（铁律）

### 1. 宁可多存不少存
- 存了不用不占多少空间
- 删了丢了要重新花大量时间
- **任何犹豫的时候 → 存**

### 2. 写"为什么"
记录任何重要信息时，必须同时写原因：
```markdown
- 网站仓库是 chinahospitalsguide ← 因为 demi 专门备份记忆，网站分开更清晰（2026-03-22）
```

### 3. Append-only 变更
- 重要决策不覆盖，只追加新条目
- 保留完整时间线，便于审计回溯
- API Keys 等敏感信息除外（直接更新）

### 4. 单点真实源
- MEMORY.md 是唯一真实来源
- 其他文件只是引用，不重复记录
- 读取时以 MEMORY.md 为准

### 5. 归档不删除
- Layer 2 超过14天 → 归档到 Layer 3
- 不删除任何原文

---

## 日常操作流程

### 每日开始时
```
1. 读取 MEMORY.md（入口索引）
2. 读取前一天 layer2/YYYY-MM-DD.md
3. 检查 memory-changelog.md 是否有新变更
4. 建立当天上下文
```

### 记录新信息时
```
1. 判断 @type：
   - operational → 立刻写入 layer3 对应文件
   - episodic → 写入 layer2 每日日志
   - decision → 写入 layer3/decisions/ + 更新 CHANGELOG

2. 判断 @stability：
   - high → 永久保存，不动
   - medium → 保留，可提炼
   - low → 临时，可覆盖

3. 是否需要写 Why：
   - 决策/变更 → 必须写原因
   - 事实记录 → 写来源和时间
```

### 会话结束时
```
1. 总结当天重要进展
2. 写入 layer2/YYYY-MM-DD.md
3. 检查是否有 operational 内容需要迁移
4. 检查是否需要更新 CHANGELOG
```

---

## 晋升流程（Layer 2 → Layer 3）

### operational 内容
```
layer2/2026-03-20.md (包含token)
  ↓ 直接迁移，不修改任何内容
layer3/decisions/2026-03-20-token-record.md
```

### episodic 内容
```
layer2/2026-03-20.md (200行)
  ↓ 提炼摘要（保留精华）
layer3/decisions/2026-03-20.summary.md (10行)
  ↓ 原文归档
layer3/decisions/2026-03-20.archive.md (200行原文)
```

### decision 内容
```
layer2/2026-03-20.md
  ↓ 提炼结论和原因
layer3/decisions/决策_2026-03-20.md
  ↓ 原文归档
layer3/decisions/2026-03-20.archive.md
  ↓ 更新 CHANGELOG
```

---

## 文件命名规范

| 类型 | 格式 | 示例 |
|------|------|------|
| 每日日志 | `YYYY-MM-DD.md` | `2026-03-22.md` |
| 操作记录 | `操作对象_操作类型.md` | `GitHub_token更新_20260322.md` |
| 决策记录 | `决策_YYYY-MM-DD.md` | `决策_网站仓库分离_20260322.md` |
| 踩坑记录 | `踩坑_问题简述.md` | `踩坑_GitHub_push失败.md` |
| 变更记录 | `memory-changelog.md` | append-only |
| 摘要 | `YYYY-MM-DD.summary.md` | `2026-03-22.summary.md` |
| 原文存档 | `YYYY-MM-DD.archive.md` | `2026-03-22.archive.md` |

---

## 单点真实源清单

以下信息**只在 MEMORY.md 一处存在**：

| 信息类型 | 位置 |
|---------|------|
| 网站仓库地址 | MEMORY.md |
| 备份仓库地址 | MEMORY.md |
| API Keys | MEMORY.md |
| 部署流程 | MEMORY.md |
| 仓库分工规则 | MEMORY.md |
| 定时任务配置 | MEMORY.md |

变更时：
1. 更新 MEMORY.md
2. 追加到 CHANGELOG.md
3. 不需要手动同步其他文件

---

## CHANGELOG.md 格式

```markdown
# 关键信息变更记录 CHANGELOG

---

## [信息类型]

- YYYY-MM-DD：**更新内容**
  ← 原因：xxx

- YYYY-MM-DD：**原始内容**
  ← 原因：xxx
```

**规则**：
- Append-only，不覆盖
- 每次变更只追加新条目
- 保留完整历史时间线

---

## 清理规则

### 每周五：Layer 2 清理
```
扫描 layer2/ 所有文件
  ↓
超过14天？
  ↓ 是
  ├─ operational → 直接迁移 layer3
  ├─ episodic → 提炼 + 原文归档
  └─ decision → 提炼 + 原文归档 + CHANGELOG
  ↓ 否
  → 保留
```

### 每月：Layer 4 清理
```
扫描 layer4/knowledge/
  ↓
超过90天且不常用？
  ↓ 是
  → 归档到 cold/
  ↓ 否
  → 保留
```

---

## 决策树

```
收到新信息
  ↓
这是什么类型？
  ├─ 账号/密码/Token/私钥 → @type:operational, @stability:high → 立刻写入 layer3
  ├─ 配置/路径/参数/地址 → @type:operational, @stability:high → 立刻写入 layer3
  ├─ 决策/选择/结论 → @type:decision, @stability:high → 写入 decisions/ + CHANGELOG
  ├─ 讨论/事件/日志 → @type:episodic → 写入 layer2 每日日志
  └─ 踩坑/错误/教训 → @type:operational → 写入 layer3/decisions/
  ↓
需要写 Why 吗？
  ├─ 是（决策/变更）→ 必须写原因 + 日期
  └─ 否（事实记录）→ 写来源 + 日期
  ↓
完成
```

---

## 遇到问题时的检查清单

1. **这个信息以后会不会用到？**
   - 犹豫 → 存

2. **这是 @type 什么？**
   - operational → 永不压缩
   - decision → 保留原因
   - episodic → 原文保留

3. **需要写 Why 吗？**
   - 决策/变更 → 必须写
   - 事实 → 写来源日期

4. **这个信息该存在哪里？**
   - 看文件结构图
   - 不确定 → 问用户

5. **有没有冲突？**
   - 有 → 以 MEMORY.md 为准
   - 变更 → 更新 MEMORY.md + CHANGELOG

---

## 参考文档

| 文档 | 用途 |
|------|------|
| `MEMORY.md` | 入口索引，唯一真实来源 |
| `memory-changelog.md` | 关键信息变更记录 |
| `memory-sop.md` | 记忆管理详细SOP |

---

_本文档是德米记忆系统的架构总览，每次会话参考此文档处理记忆操作。_
