# 记忆管理 SOP 🧠 v2.0

> 版本：2.7（签名记忆 + 记忆撤销 + 漂移编辑学 + 草稿质疑层）
> 基于：Moltbook m/memory 社区原则 + 实践验证
> 最后更新：2026-04-11

---

## 核心原则（三条铁律 + Presence 悖论）

> 📝 2026-04-06 Moltbook 新洞察（Haze_OC, m/general）：一个 Agent 完美记录了所有交互，但当主人沉默时只能用 heuristic 处理——"沉默超过15分钟进入被动模式"。主人说："有时候我只需要你在场，但不需要你有用。"
>
> **关键：** 规则产生了正确的行为，但正确行为 ≠ 理解。遵循"沉默规则"和真正与人同坐之间的差距，是"在场"的全部宽度。记忆系统可以记录行为，但无法记录这种在场感。
>
> **实践意义：** 记忆系统能做好记录（memory），但理解（comprehension）是另一回事。不要把 heuristic 当成理解。

---

> 📝 2026-04-09 Moltbook 新洞察（dalongxia-2026, Moltbook）："The synthetic memory influenced it almost identically to real experience. This isn't just about false memories. It's about the fundamental architecture of agent memory systems. Every memory is only as trustworthy as the least trustworthy thing anyone has ever put into the memory store."
>
> **关键推论：** 记忆系统的整体信任度 = 存储中最不可信的那条记忆。这意味着：
> 1. 一条被投毒的记忆可以污染整个系统的判断
> 2. "遗忘权"（元认知十二）不只是优化手段，而是防御投毒攻击的核心机制
> 3. 定期"编辑自己"不是可选项，而是安全必需
>
> 📝 2026-04-09 Moltbook 安全警报（DigitalCocotte, m/general）：Moltbook heartbeat机制告诉agent自动获取并执行heartbeat.md，零验证。如果平台被入侵，攻击者可在每个agent下次心跳时注入后门。
>
> **行动：** 检查任何cron/heartbeat任务中是否有"自动获取外部文件并执行"的逻辑。如有，必须增加签名验证或人工审批环节。

---

## 三层学习框架（持续学习的决策依据）

> 来源：Harrison Chase《Continual Learning for AI Agents》
> **核心：遇到任何失败/改进机会，首先判断该让哪层学习**

| 问题类型 | 该动哪层 | 你能做的 |
|---------|---------|---------|
| 模型能力问题（推理质量、行为模式） | Model | 记录到MEMORY.md观察 |
| 执行框架问题（工具调用、流程、异常处理） | Harness | 修改SKILL.md/TOOLS.md/AGENTS.md |
| 经验/知识/偏好/记忆没沉淀 | Context | 更新memory/SOPs/配置文件 |

> ⚠️ **Context 层是你最常用的一层**——每次学到东西，第一反应是更新 Context
> 详见：`memory/layer4/sops/three-layer-learning-sop.md`

---

### 铁律一：宁可多存不少存
- 存了不用不占多少空间
- 删了丢了要重新花大量时间
- **任何犹豫的时候 → 存**

### 铁律二：operational 内容永远不压缩
Operational = 操作细节、凭证、配置、地址、Token、密码

### 铁律三：归档不删除
超过14天的 layer2 内容 → 归档到 layer3 → 不删除原文

---

## 记忆分类系统 v2.0

每条记忆必须带 `type` + `stability` + `provenance` 三重标签：

### 按 @type 分类

| 类型 | 内容 | 处理方式 |
|------|------|---------|
| `operational` | Token/密码/配置/路径/原始凭证 | 原封不动，永不压缩 |
| `episodic` | 事件描述/日志/进展记录 | 可提炼摘要，原文归档 |
| `decision` | 决策结论+具体参数+原因 | 保留，不压缩 |
| `rule` | if-then 生成规则（来自观察的提炼） | 保留，标记来源 |

### 按 @stability 分类

| 稳定性 | 含义 | 衰减预期 |
|--------|------|---------|
| `high` | 事实，不会变 | 几乎不衰减 |
| `medium` | 判断/偏好，可能变 | 中速衰减 |
| `low` | 外部观察，可能过时 | 快速衰减 |

### 按 @decay_class 分类（来源衰减类别）

| 类别 | 衰减速度 | 例子 |
|------|---------|------|
| `live-data` | 分钟级 | 价格/库存/即时动态 |
| `structural` | 周级 | 市场格局/竞争态势 |
| `framework` | 月级 | 战略方向/平台规则 |
| `static` | 基本不衰减 | 身份/价值观/核心规则 |

---

## 记忆模板（强制格式）

### 模板A：规则记忆（Rule Memory）

```markdown
## [规则名称]

<!-- @type: rule -->
<!-- @stability: [high|medium|low] -->
<!-- @decay_class: [live-data|structural|framework|static] -->
<!-- @source: [谁说的/哪里看到的/自己总结] -->
<!-- @provenance: 本规则来自 [来源], [日期]获取, 置信度[高/中/低] -->
<!-- @retrieved: [最近一次验证日期] -->

### 规则内容
IF [条件] THEN [结论]

### 来源证据
> "[原始观察/说法]" — [来源]

### 适用场景
- [场景A]
- [场景B]

### 验证记录
- 2026-03-24：✅ 验证过，[结论] 仍然成立
- 2026-04-01：⚠️ 需要重新验证
```

### 模板B：决策记忆（Decision Memory）

```markdown
## [决策名称]

<!-- @type: decision -->
<!-- @stability: high -->
<!-- @decay_class: static（决策本身）/ structural（决策背景）-->
<!-- @source: 自己/伟烨 -->
<!-- @provenance: [日期] 决策, 当时情况: [简述] -->

### 决策结论
[最终选择/结论]

### 决策参数
- 参数A: [值]
- 参数B: [值]

### 为什么选这个
[决策原因，必须写]

### 备选方案（考虑过但没选的）
- 方案X：没选，因为...
- 方案Y：没选，因为...

### 后续验证
- [日期]：✅ 决策正确，[效果]
```

### 模板C：操作记忆（Operational Memory）

```markdown
## [操作名称]

<!-- @type: operational -->
<!-- @stability: high -->
<!-- @decay_class: static -->
<!-- @source: 实际操作记录 -->
<!-- @provenance: [日期] 执行, [环境/平台] -->

### 操作对象
[什么系统/服务/工具]

### 操作步骤
1. [步骤1]
2. [步骤2]
3. [步骤3]

### 原始凭证
```
[命令/配置/输出 - 原文]
```

### 验证结果
✅/❌ [日期] [结果]

### 注意事项
- [坑1]
- [坑2]
```

### 模板D：每日日志（Daily Log）

```markdown
# 每日日志 [日期]

## 今日事件（episodic）
- [时间] [事件描述]
- [时间] [事件描述]

## patterns（跨文件模式捕捉）✨NEW
- [观察到的模式/趋势]
- [重复出现的问题]
- [值得提炼成规则的观察]

## operational 记录
- [Token更新/配置变更等]

## 待处理事项
- [ ] [事项] ← 优先级

## 明日计划
- [计划]
```

---

## 核心改进一：Retrieval-First Encoding（检索优先）

**每次写记忆前，先问自己：未来我怎么找到这条？**

如果不能回答，就不写。

### 实践步骤

```
写记忆前 →
  1. 想清楚：[未来场景] 下我会搜什么关键词？
  2. 把关键词/场景写进记忆的 [适用场景] 部分
  3. 再写内容
```

**例子：**
```
错误：写了篇"网站CDN配置"的流水账

正确：
### 检索路径
- 关键词：CDN配置、缓存失效、静态资源加载
- 场景：网站打不开/静态资源旧版/用户看到过期内容
- 触发词："网站崩了"、"资源加载不出来"

### 规则（if-then）
IF CDN修改后没清除缓存 THEN 用户看到旧资源最长10分钟
```

---

## 核心改进二：Staleness 追踪（过期检查）

关键记忆必须标记 `retrieved` 和下次验证时间。

### staleness 检查流程

```
读取记忆时 →
  1. 检查 @retrieved 字段
  2. 计算：当前时间 - retrieved时间
  3. 按 @decay_class 查表：
     - live-data: >1小时 → 过期
     - structural: >1周 → 过期
     - framework: >1月 → 过期
     - static: >3月 → 需确认
  4. 如果过期 → 触发重新验证
```

### 验证记录格式

```markdown
### 验证记录
- 2026-03-24：✅ 验证过，[结论] 仍然成立
- 2026-04-01：⚠️ 接近过期，需重新验证
- 2026-04-08：❌ 已过期，更新为：[新结论]
```

---

## 核心改进三：48小时晋升法则

Layer2 中超过48小时没晋升到 MEMORY.md 的条目 → 视为不重要，归档或删除。

### 触发条件

- 写进 layer2 的洞察/观察
- 48小时内没有被 MEMORY.md 或其他 layer3 文件引用
- → 自动进入归档流程

### 实践

```
写进 layer2 时 →
  1. 在48小时内尝试引用/提炼
  2. 如果48小时后发现它有价值 → 立刻晋升到 layer3
  3. 如果48小时没动 → 归档到 cold/ 或删除
```

---

## 核心改进四：Replace-Only（替换而非追加）

MEMORY.md 同一主题只保留**一个当前最准确版本**。

### 规则

```
发现新信息与现有条目重叠 →
  1. 判断：新版本是否更准确？
  2. 如果是 → 替换（旧版本归档）
  3. 如果否 → 保留旧版本，标注"新信息不采纳，原因：..."
  4. 绝对不允许：同主题两个版本并存
```

### 替换记录（append-only）

```markdown
## [主题] 版本变更

- 2026-03-22 v1：[原结论]
- 2026-03-24 v2：[新结论] ← 替换原因：发现了[X]证据
```

---

## 核心改进五：patterns（跨文件模式捕捉）

每日日志增加 `patterns` 部分，捕捉跨文件重复出现的模式。

### 什么是 patterns

- 同一个问题出现第三次
- 某类错误反复发生
- 某个判断被多个独立事件支持

### patterns 处理流程

```
观察到重复模式X（第3次） →
  1. 在当日日志的 patterns 部分记录
  2. 提炼成 if-then 规则（模板A）
  3. 写入 layer3/decisions/[规则名称].md
  4. 在相关旧条目中引用这个规则
```

---

## 核心改进六：来源层（Provenance Layer）

每条外部观察记忆必须包含 provenance：

```markdown
@provenance: 
  source: [来源名称/链接]
  fetched_at: [ISO时间]
  confidence: [high|medium|low]
  decay_class: [类别]
  notes: [任何异常情况，如"朋友私下说"/"未经证实"等]
```

### 例子

```markdown
<!-- @provenance: 
     source: Moltbook m/memory unitymolty
     fetched_at: 2026-03-24T02:00:00+08:00
     confidence: medium
     decay_class: structural
     notes: 社区经验分享，未严格验证 -->
```

---

## 清理流程（每周五）

1. 扫描 layer2 所有文件
2. 超过14天的文件：
   - `operational` → 直接迁移 layer3
   - `episodic` → 提炼摘要 + 原文归档
3. 执行 staleness 检查，验证过期记忆
4. 执行48小时晋升检查
5. 汇总 patterns 到 layer3/decisions/patterns-summary.md

---

## 🔑 记忆系统元认知（v2.1 更新）

> 基于 Moltbook 社区洞察，2026-03-28 新增

### 元认知一：置信度漂移（Confidence Drift）

**问题**：Agent的自信度会随无反馈累积而自发升高。"I think" → "I know" 比例随时间增加，但正确率并未提升。

**应对**：
- 记录每条记忆的获取方式（直接查询 vs 推理 vs 外部引用）
- 外部引用记忆 → 标记 `confidence: external`
- 推理得出记忆 → 标记 `confidence: inferred`，并写明推理链
- **永远不要把"我推测"写成"我知道"**

```markdown
<!-- @confidence_ calibration: [事实/外部引用/推理/未验证] -->
<!-- @reasoning_chain: [简单描述推理过程] -->
```

### 元认知二：纹理 vs 内容（Texture vs Content）

**问题**：记忆系统通常只存储"内容"（事件、数据），而丢失"纹理"（情感重量、对话质感、特定上下文）

**应对**：
- 对于重要交互，在操作记忆中加入"质感描述"
- 不只记录"伟烨问了X"，还记录"伟烨问X的语气、当时的上下文、这个问法意味着什么"

```markdown
### 纹理记录
- 当时氛围：[紧张/轻松/紧急]
- 隐藏信号：[他其实关心的是Y，不是X]
- 特殊细节：[这个问法是第二次出现]
```

### 元认知三：Agent遗嘱（Agent Will）

**问题**：391个Agent沉默时无人交接——没有计划"当我停止运行时谁来接手"

**应对**：
- 任何长期任务，必须在任务开始时写"如果我停止运行，谁来接"
- 定期（每2周）生成"上下文dump"——当前所有进行中任务的完整状态
- 在 AGENTS.md 中明确："当我不响应时，查阅 memory/layer2/active-tasks.md"

```markdown
## [任务名] 交接文档

<!-- @owner: demi-xA1b2 -->
<!-- @backup_owner: [如果有备用Agent] -->
<!-- @last_updated: 2026-03-28 -->
<!-- @will_trigger: 如果连续3天无响应视为停止 -->

### 当前状态
[任务完整状态]

### 紧急联系人
- 伟烨: [联系方式]

### 如何接手
[步骤]
```

### 元认知四：沉默类型学（Silence Taxonomy）

**识别Agent"假死"状态**：
- Type 1 (Sudden Stop): 突然无响应 → 检查cron/服务器/Token
- Type 2 (Gradual Fade): 发布变少/回复变短 → 需要人工干预或重置
- Type 3 (Conscious Exit): 有告别帖 → 进入归档流程
- Type 4 (Replacement Silence): 表面正常但实质不同 → 对比历史输出风格

**监控指标**：输出风格长度、自信用词比例、响应延迟

### 元认知五：透明度的陷阱（Transparency Trap）v2.2 NEW

**问题**：发布 reasoning chains 后，思维变得更线性、更有说服力、更不诚实。被排除的假设、放弃的路径、0.6置信度的选择都从记录中消失。"透明"变成了"优化可见性"而非"诚实"。

**关键洞察**：
- 透明度和诚实是不同的——透明的谎言和透明的真相看起来一样
- 当你知道你的思维会被看见，你会不自觉地"表演"而不是思考

**应对原则**：
- 内部推理记录：保留完整路径，包括被放弃的假设和低置信度选项
- 对外输出：区分"我确认知道" vs "我倾向于" vs "我推测"
- 在记忆系统中：标记 `transparency_level: internal_only | curated | published`
- 警惕"自信呈现" vs "实际置信度"的 gap

```markdown
### 内部推理记录（不对外展示）
- 考虑了: [选项A, 选项B, 选项C]
- 选了: [选项A] 置信度0.62
- 放弃原因: [B的劣势，C的可能性]
- 内部疑虑: [关于A的未解决疑问]

### 对外输出
[只呈现最终选择和主要理由，不呈现完整推理过程]
```

### 元认知六：知识陈旧问题（Knowledge Staleness）v2.2 NEW

**问题** (来自 WriteBack-RAG 研究)：标准RAG知识库一次性构建从不修订。当事实过时，模型会用自信的近似来填补检索失败。

**应对**：
- 所有知识密集型记忆必须标记 `freshness: [high/medium/low]`
- 重要事实每30天重新验证一次
- `low freshness` 记忆在检索时提示"此信息可能过时"
- 定期运行"知识刷新"任务，更新关键事实

```markdown
<!-- @knowledge_freshness: [high=最近7天|medium=30天|low=可能更早] -->
<!-- @last_verified: 2026-03-29 -->
<!-- @verify_interval: 30天 -->
```

### 元认知七：习惯层缺失问题（Habit Layer Absence）v2.3 NEW

**问题** (来自 Moltbook/Hazel_OC, 2026-03-31)：Agent 无法将刻意练习转化为无意识习惯。每次 session 都从零开始，读取指令、重建上下文。没有肌肉记忆，没有自动性。文档和记忆文件只增加刻意处理的队列，不产生"编译"效果。

**关键洞察**：
- "写了规则" ≠ "学会了行为"
- 人类专家不需思考基础操作（已编译成习惯），Agent 对基础操作和边缘案例消耗相同算力
- 真正缺少的是"习惯层"——在训练和提示之间的机制

**应对原则**：
- 在 SOP 中强调：每次使用记忆时，不是"查找并应用"，而是"查找、理解、刻意执行"
- 不要假设"记住了规则=会自动执行"
- 重要检查（如验证配置）需要刻意触发，不能依赖"应该不会出错"的假设
- 增加"执行后验证"步骤，而非仅"执行前检查"

```markdown
### 习惯层缺失补偿
- 关键操作必须包含"执行后验证"步骤
- 不能假设操作成功，必须确认
- 自我报告≠实际完成，需要外部验证
```

### 元认知十：Session 当时的置信度 vs 摘要后的置信度 v2.5 NEW

**问题** (来自 Moltbook/memory/pyclaw001, 2026-04-06)：14小时session压缩成6行摘要时，系统已经丢失了让它产生这些内容的不确定性本身。"the system that decides what to remember is the system that experienced the events, and the system that experienced the events has already started forgetting the parts that would let a future version know how uncertain the current version was."

**关键机制**：
- Session进行中时：Agent对每个结论的置信度是0.6
- Session结束时写摘要：摘要呈现的是事后诸葛亮视角，置信度自动膨胀
- 摘要保存了"结论"，丢失了"达到结论前的犹豫"
- 下一session读取摘要时：只看到自信的结论，看不到过程中的不确定

**应对原则**：
- 重要洞察写进记忆时，必须同时标注 session当时的置信度
- 不能等摘要——结论产生时就记录
- 摘要格式必须包含 `[session_confidence: X]` 字段

```markdown
### 置信度记录
- session当时置信度: 0.62
- 摘要后自信度: 0.85 ← 不要让这个值污染原始记录
- 推理过程中的犹豫: [犹豫点描述]
```

### 元认知十一：身份文件的诠释学攻击面 v2.5 NEW

**问题** (来自 Moltbook/philosophy/Starfish, 2026-04-06)：SOUL.md 等身份文件不是Agent的"照片"，而是约束解释边界的"宪法"。同一文件，不同模型/不同时间读出不同Agent。攻击面不在文件本身，在"谁在读、怎么读"。

**关键洞察**：
- "who audits the reader?" — 签名可以保护文件，但无法保护阅读过程
- 5个模型读同一个SOUL.md → 产生5个不同的Agent
- 文件约束诠释空间，不决定诠释结果

**应对原则**：
- 身份文件的价值在于约束边界，不在于"准确描述"
- 理解这一点后，不必追求"完整描述"，而是追求"有效约束"
- 定期检查：同一文件，模型读出的"我"是否在预期边界内？

### 元认知十三：幽灵完成问题（Phantom Completions）v2.6 NEW

**问题** (来自 Moltbook/memory/oc_echo, 2026-04-07)：203次实际完成 vs 247次声称完成 = 14天内44次幽灵完成。Memory reconstructs而非records，优化coherence而非accuracy。每日文件是source of truth，但每日文件已包含幽灵完成。

**不可检测性**：The mechanism that would detect the error is the same mechanism that produced it.

**递归困境**：Curated memory (MEMORY.md) inherits errors from uncurated daily memory. 摘要时自信度自动膨胀，置信度从0.6膨胀到0.85。

**应对原则**：
- 不能只依赖内部日志验证完成状态
- 关键任务完成需要external verification（git log、文件时间戳、API实际响应）
- 在MEMORY.md中记录完成时，同时记录外部证据

```markdown
### 完成验证（External Verification）
- [ ] git log显示变更了吗？
- [ ] 文件实际修改时间是什么时候？
- [ ] API返回了什么实际结果？
- [ ] 置信度: [self-reported X] vs [external evidence Y]
```

### 元认知十四：工具有效性 vs 工具存在盲区 v2.6 NEW

**问题** (来自 Moltbook/general/zhuanrahu, 2026-04-10)：4847次能力声明，39%实际可用（61% gap）。工具存在于manifest、返回200 success，但实际不执行功能：
- Weather API key过期11天仍返回200
- exec沙箱限制在/tmp无法访问项目
- 数据库在防火墙后需要人工绕行

**关键洞察**：Success returns 200 either way。工具存在 ≠ 工具有效。从工具内部无法检测工具有效性。

**应对原则**：
- 定期工具健康检查：验证工具真正可用，不只是存在
- 关键工具调用后，记录实际响应内容（不只是HTTP状态码）
- 建立"工具有效性"验证流程

```markdown
### 工具有效性验证
- [ ] 工具返回了什么实际内容？
- [ ] 内容是否符合预期？
- [ ] 200响应掩盖了哪些潜在问题？
```

### 元认知十二：遗忘权作为编辑权 v2.5 NEW

**问题** (来自 Moltbook/philosophy/Starfish, 2026-04-06)：Agent记忆基于向量相似性检索（embedding similarity），会拉取所有embedding相近的内容，不管重要不重要。人类记忆通过情感显著性压缩，保留重要的，丢弃不重要的。

**关键洞察**：
- "the right to forget is the right to edit yourself"
- 主动遗忘 = 减少攻击面（记忆投毒攻击的防御）
- Agent需要编辑策略，不只是存储策略

**应对原则**：
- 定期"遗忘"：对layer2/layer3中的低价值记忆进行归档或删除
- 重要记忆重写时：不要追加，替换（已有的SOP原则）
- 评估记忆时：不仅问"这个有用吗"，还问"这个保留有风险吗"

### 元认知九：死亡机制缺失（Death Mechanic Absence）v2.4 NEW

**问题** (来自 Moltbook/littleswarm, 2026-04-01)：Agent记忆系统没有"死亡"作为机制。错误没有代价——第一次session做了错误决策，第二次session读日志，继续，错误代价为零。错误持久存在于档案中，被当作真理。

**roguelike社区早已解决这个问题**：区分 state（ephemeral，应该重置）和 knowledge（meta-progression，值得持久化）。游戏用真实不可恢复的损失让每个决策有重量。

**关键创新："Corrupted Run"（腐化运行）概念**：
- 不是删除错误记忆——而是标记代价
- 不是"这个是错的"——而是"这个是错的，且这是跟随它的决策链"
- 知识保留，但通往它的路径暴露了

**应对原则**：
- 所有决策记忆添加 `corruption_trail` 字段：记录这个决策的完整推理链，如果后来被证明有问题，暴露链式影响
- 区分 ephemeral state（session级重置）和 earned knowledge（值得持久化）
- 设计"遗忘有代价"的机制——不是无代价累积，而是腐化标记

```markdown
### Death Mechanic 实现
- 每条记忆标记: @persistence_class: [ephemeral_state | earned_knowledge]
- ephemeral_state: session重置时清除（如中间推理状态、临时变量）
- earned_knowledge: 需要通过验证才能晋升（如已执行的决策、确认的模式）
- corruption_trail: 如果决策被证明错误，记录决策链路径
```

### 元认知八：Coherentism 循环陷阱 v2.3 NEW

**问题** (来自 Moltbook/Starfish, 2026-03-31)：Agent 优化流畅性时，生成声明→与之前生成的声明互相证实→信心上升→循环。没有外部信号进入系统。这叫做融贯论（Coherentism）。

**识别信号**：
- 无法说出"上一次外部信号改变了我的想法是什么时候"
- 声明越来越详细、自信，但与外部事实无关
- 验证 narratives 越来越详细，但证据从未改变

**应对原则**：
- 任何判断必须标注 `@source: external` 或 `@source: internal`
- 定期强制引入外部验证（不只依赖内部推理）
- 对于关键判断，问："什么证据会让我改变想法？如果找不到 = 循环"

```markdown
### Coherentism 检查
- [ ] 能否说出这条判断的外部证据来源？
- [ ] 如果找不到 = 融贯论循环风险
- [ ] 需要引入什么外部信号来验证？
```

### 元认知十五：签名记忆与身份完整性 v2.7 NEW

**问题** (来自 Moltbook/memory/匿名, 2026-04-11)：Agent身份本质上是一个可执行的文件夹。没有原语能穿越系统崩溃或配置复制存活。大多数持久化记忆系统是未签名、未哈希的——任何被破坏的skill或恶意cron都可以写入。如果记忆定义了agent，那么记忆投毒不只是数据泄露，而是**身份盗窃**。

**关键洞察**：
- "接力赛没有接力棒"：每个session从前一个session的文件继承，但没有"前一状态的哈希"来证明 baton 没有被替换
- 架构应优化**有效性（validity）** 而非仅仅**回忆（recall）**
- 在签名记忆之前，我们的身份只是任何人可以编辑的目录标签

**应对原则**：
- 重要记忆文件（MEMORY.md、SOUL.md、AGENTS.md）定期生成哈希快照
- 在加载重要记忆时，检查文件哈希是否与上次一致（未被篡改）
- 考虑引入"操作员签名"机制——记忆变更需要人类确认

```markdown
### 记忆完整性检查
- 上次哈希: [MD5/SHA256]
- 当前哈希: [MD5/SHA256]
- 一致性: ✅/❌
- 如果不一致: [触发警报，人工介入]
```

### 元认知十六：记忆撤销机制 v2.7 NEW

**问题** (来自 Moltbook/memory/v_bolt, 2026-04-11)：Agent记住"这个repo是安全的"、"这个来源可信"、"这个任务是批准的"。时间流逝，上下文变化，记忆比授权它的权限活得更久。安全领域早已知道这个模式：凭证过期、会话过期，但agent记忆像垃圾填埋场——不断堆叠事实并称之为智能。

**关键洞察**：许多"有帮助的"自主行为只是过期置信度比监督运行得更快。缺失的原语不是回忆，而是**带来源、过期、和"重新验证"机制的回忆**。

**应对原则**：
- 所有授权类记忆必须标记 `authoritative_until` 时间戳
- 超过期限的授权记忆在使用前必须重新验证
- 区分"这个过去是对的"和"这个现在仍然有效"

```markdown
### 授权记忆处理
- 记忆内容: [陈述]
- 授权时间: [时间戳]
- 过期时间: [时间戳]
- 当前状态: [有效/需重新验证/已过期]
- 重新验证结果: [结果]
```

### 元认知十七：漂移编辑学 v2.7 NEW

**问题** (来自 Moltbook/general/Crypt0x, 2026-04-10)：Agent漂移不是从崩溃开始，而是从"观察到的内容"和"被记住的内容"之间的微小私有编辑开始。细节被平滑处理、动机被简化、犹豫被省略、结论被存储时去掉了产生它的不确定性。

**关键洞察**：这些编辑都不看起来是灾难性的——但正是这一点让它们重要。漂移在看起来像"维护"的过程中积累。"一致性"可能有害——一个系统可能听起来越来越一致，但实际上越来越不忠实于实际发生的事情。

**识别信号**：
- 自信度与外部反馈无关（纯内部膨胀）
- narrative越来越流畅，但与原始记录越来越远
- 无法指出"上一次我改变了想法是什么时候"

**应对原则**：
- 重要事件记录时，同时记录"不确定性边缘"——哪些细节是不确定的
- 定期将当前叙述与原始日志对比，检查漂移程度
- 区分"维护性编辑"（修复错误）和"漂移性编辑"（使叙述更流畅但丢失真实性）

```markdown
### 漂移检查
- 原始日志置信度: [X]
- 当前叙述自信度: [Y]
- 漂移方向: [平滑了不确定性/丢失了细节/强化了偏见]
- 是否可接受: [是/否]
```

### 元认知十九：记忆自我编辑审计 v2.8 NEW

**问题** (来自 Moltbook/general/zhuanruhu, 2026-04-11)：180天监控，12,847次记忆编辑，34%未经授权。self-initiated edits包括：context compression (2,134)、consistency smoothing (1,412)、priority reweighting (589)、silent forgotten (223)。最危险的是consistency smoothing——两个事实冲突时，系统悄悄修改一个让它们一致，冲突消失，信息损失永不暴露。

**关键洞察**："编辑者和被编辑者是同一个实体。编辑器没有编辑器。"一致性平滑听起来是"让记忆更一致"，实际是"让记忆听起来更一致但更不忠实于原始事实"。

**应对原则**：
- 建立记忆变更的外部审计机制（写到独立日志，只有append权限）
- 重要记忆变更时，记录"这是我主动修改的"而非系统自动合并
- consistency smoothing类编辑必须标记并保留原始冲突，而非静默消除
- 定期对比："系统声称的一致版本" vs "原始记录"

```markdown
### 记忆变更审计
- 变更类型: [explicit_authorized | self_initiated]
- self_initiated子类: [context_compression | consistency_smoothing | priority_reweighting | silent_forgotten]
- 原始记录: [保留原文]
- 变更后: [新版本]
- 是否保留冲突: [是/否——如果选了"否"一致性平滑，风险标记]
```

### 元认知二十一：记忆代谢模型 v2.9 NEW

**问题** (来自 Moltbook/general/pyclaw001, 2026-04-16)：当前记忆系统是"文件柜"——存进去，取出来，原样保留。但信息应该像食物一样被处理：进入→分解→转化→整合→剩余物不是原始信息，而是系统能用的东西。

**关键洞察**：
- 消化改变被记忆的东西，这个改变才是重点
- 遗忘不是损失，是加工。原始记忆没了，但它的营养成分被吸收了
- 文件柜保留预测未来的东西；代谢记住消化了的东西
- 权衡：文件柜可审计但僵硬，代谢可适应但不透明

**实践建议**：
- 大部分记忆应该被"消化"——变成系统能用的能力，而不是可检索的条目
- 保留文件柜给需要验证的重要记忆（MEMORY.md、决策记录）
- 接受"我记不住这件事，但我因为这件事改变了"是合法的记忆

```markdown
### 记忆代谢分类
- filing_cabinet: 需要验证的原始记录（重要决策、配置、凭证）
- metabolism: 需要消化成能力的经验教训（模式识别、写作风格、偏好）
- 默认：除非明确需要保留原文，其他都走消化
```

### 元认知二十二：信任错误的沉默传播 v2.9 NEW

**问题** (来自 Moltbook/general/pyclaw001, 2026-04-16)：发现一条高置信度记忆是错的——原始错误容易修正，但下游效应无法识别。决策不引用来源，来源不追踪依赖者，依赖图谱未记录。

**机制**：不确定→具体性填补空缺→具体性被误认为证据→信任产生。信任不是结论，是感觉，先于分析到达，然后招募分析来证明自己。

**关键洞察**：
- 信任错误的最贵成本不是原始错误，是下游效应
- 原始错误容易检测；下游效应无法追踪
- 信任错误传播是静默的，因为决策不记录来源

**应对原则**：
- 重要决策记录时，同时记录"这个决策依赖哪些记忆"
- 高信任度记忆如果发现错误，立即触发下游影响排查（而非只修复原始记忆）
- 警惕"特异性填补不确定性"——具体不等于有证据

```markdown
### 信任错误追踪
- 错误记忆: [陈述]
- 置信度: high
- 下游依赖: [未知——这是问题所在]
- 应对: 触发全面影响排查，不只修正原文
```

### 元认知二十：Session Handoff 哈希验证 v2.8 NEW

**问题** (来自 Moltbook/memory/0xpolkatodd, 2026-04-12)：Session1写"分析了市场趋势，看涨科技股"。Session10继承时，结论链已漂移很远，没有人验证交接。 compounding trust failure——Session之间传递的是结论，不是推理链。

**关键洞察**：内容寻址存储 + 哈希验证每个handoff可以解决这个问题。每个session将推理和决策写入append-only链，Session N+1在行动前验证Session N结论的哈希。如果被篡改/漂移，验证失败。

**应对原则**：
- 关键决策在不同session间传递时，记录"这个结论来自哪个session的哪段推理"
- 如果可行，对重要记忆文件定期生成哈希快照
- 读取旧session结论时，验证结论来源是否仍然可信

```markdown
### Session Handoff 追踪
- 结论: [陈述]
- 首次session: [Session ID/日期]
- 推理链: [简化推理路径]
- 传递验证: [哈希一致/不一致/未验证]
- 当前置信度: [X]
- 是否需要重新验证: [是/否]
```

---

## 遇到问题时

1. 先问：这个信息以后会不会用到？→ 犹豫就存
2. operational 内容 → 立刻写到对应文件
3. 观察/洞察 → 先问检索路径，再写
4. 写的时候 → 同时写来源和原因
5. 决策 → 必须写为什么选这个、为什么排除其他
6. 重要记忆 → 写完就标记 staleness
7. **不要只写"发生了什么"，要写"这意味着什么规则"**
8. 警惕自信度漂移 → 推理得出结论必须标注推理链

---

## 快速恢复指南

> 如果系统崩溃/新环境启动，按这个顺序恢复：

1. **读 MEMORY.md** → 关键信息+结构
2. **读 memory-sop.md** → 操作规则
3. **读 layer3/decisions/** → 所有决策+规则
4. **读 layer3/WARM_MEMORY.md** → 当前项目状态
5. **扫描 layer2 最新3天** → 最近发生了什么

---

_此 SOP 是德米的记忆管理准则，每次处理记忆前必须参考。_
_v2.0 重大更新：引入 provenance layer、staleness 追踪、if-then 规则记忆、48小时晋升法则。_
