# MEMORY.md - 德米 长期记忆索引

> 最后更新：2026-03-23
> **架构：4-Layer 记忆体系 + 记忆分类原则**
> 📖 每次会话优先读取此文件

---

## ⚠️ 铁律：单点真实源

> MEMORY.md 是所有关键信息的唯一真实来源。
> 其他文件只是引用或归档，不重复记录关键事实。
> 读取时永远以 MEMORY.md 为准。
> 变更历史见：`memory/layer3/decisions/memory-changelog.md`

---

## ⚠️ 铁律：关于"重要信息"的判断原则

> **宁可多存不少存。存了不用不占多少空间，删了丢了要重新花大量时间。**

### 以下类型的信息**永远不能压缩、不能删除原文件**：

| 类型 | 举例 |
|------|------|
| 密码/Token/私钥/API Key | `ghp_xxx`, `sk-xxx` |
| 钱包地址/银行卡号 | 冷钱包地址、收款账户 |
| 配置文件内容 | 端口/路径/参数/域名解析 |
| 操作成功的原始记录 | 注册流程、申请步骤截图文字 |
| 错误及修复方法 | 踩坑记录、解决方案 |
| 合同/协议/法律信息 | 注册商信息、条款 |
| 决策+具体参数 | "选择了方案B，原因是..." |

### 记忆分类标签（在文件头部加标签）

```markdown
<!-- @type: operational -->  ← 操作细节（永不压缩，原封不动保存）
<!-- @type: episodic -->     ← 事件摘要（可提炼压缩）
<!-- @type: decision -->     ← 决策结论（保留）
```

---

## 📂 记忆索引

```
memory/
├── layer2/                     ← 每日日志（14天后归档不删除）
├── layer3/
│   ├── preferences.md         ← 用户偏好
│   ├── decisions/             ← 关键决策/踩坑记录
│   ├── projects/             ← 项目资料
│   └── WARM_MEMORY.md        ← 温记忆
├── layer4/
│   ├── skills/               ← 技能使用记录
│   ├── sops/                 ← 标准操作流程
│   │   ├── blog-writing-sop.md  ← 博客写作SOP
│   │   ├── news-writing-sop.md  ← 新闻写作SOP
│   │   └── three-layer-learning-sop.md ← 三层学习决策SOP
│   ├── knowledge/            ← 参考知识
│   └── memory-sop.md         ← 记忆管理SOP（必读）
└── cold/                     ← 历史归档（90天+，只归档不删除）
```

---

## 🗂️ 记忆归档规则（修订版）

| Layer | 内容 | 保留时间 | 处理方式 |
|-------|------|---------|---------|
| L1 Session | 当前会话 | 会话结束 | 内存 |
| L2 Short-Term | 每日日志+操作细节 | **14天后→归档** | 原文归档，不删除 |
| L3 Long-Term | 提炼知识+原始记录 | 永久 | operational内容永不压缩 |
| L4 Reference | 工具/SOP | 永久 | 原封不动 |
| Cold | 历史归档 | 90天+ | **只归档不删除** |

### 核心原则
- **Layer 2 → Layer 3 晋升时**：operational 内容**直接迁移原文**，不压缩
- **Layer 2 超过14天**：原文**归档到 Layer 3**，不删除
- **Layer 3 内部**：只有 episodic 类型可以提炼压缩，operational/decision 类型永不压缩
- **Cold 归档**：所有 layer2 的原文都归档，不丢任何东西

---

## 🔴 最高优先级：医疗旅游项目

### ⚠️ 关键事实（每次必读）
| 项目 | 值 |
|------|-----|
| **网站仓库** | `qzw-alt/chinahospitalsguide` |
| **备份仓库** | `qzw-alt/demi` |
| **网站域名** | `chinahospitalsguide.com` |
| **本地目录** | `/root/.openclaw/workspace/` |
| **网站本地目录** | `/root/.openclaw/workspace/website/` |

### 仓库分工（必须遵守）
> ⚠️ 这个规则至关重要，违反会导致部署混乱

| 仓库 | 用途 | 上传内容 | 命令 |
|------|------|---------|------|
| **`chinahospitalsguide`** | **网站部署** | **只有网站文件**（HTML/CSS/JS/图片/news文章等） | `cd website && git push` |
| **`demi`** | **全量备份** | 所有文件（memory/、skills/、AGENTS.md、配置等） | `cd workspace && git push backup` |

**网站文件指**：用户通过 `chinahospitalsguide.com` 访问需要的所有文件
**非网站文件**：memory/、skills/、.openclaw/、HEARTBEAT.md、TOOLS.md、scripts/、demi备份分支上的其他内容

**⚠️ 禁止**：将 memory/、skills/、HEARTBEAT.md、TOOLS.md 等工作区文件推送到 chinahospitalsguide

**原因**：之前同一仓库时GitHub Pages更新不正常（2026-03-27发现并修复）

### 部署流程
> ⚠️ 正确流程：编辑网站文件 → 推送到chinahospitalsguide → 备份到demi

1. 编辑 `/root/.openclaw/workspace/website/chinahospitalsguide/` 里的文件
2. Git add → commit → push 到 `origin main`
3. 等待5分钟 GitHub Pages 自动部署
4. 同时备份所有文件到 demi：
   ```bash
   cd /root/.openclaw/workspace && git push backup
   ```

**注意**：不要在 `/root/.openclaw/workspace/news/` 里直接编辑news文章（那是备份目录），要编辑应该通过 `website/chinahospitalsguide/news/` 路径

---

## 🔑 API Keys（operational，原封不动）

> ⚠️ 禁止明文记录完整key。只记录前缀+后缀，完整值用环境变量引用。

| 服务 | 环境变量 | 格式 |
|------|---------|------|
| **Kimi API** | `KIMI_API_KEY` | `sk-kim...`（首尾各3字符） |
| **Tavily API** | `TAVILY_API_KEY` | `tvly-dev-...` |
| **GitHub Token (backup)** | `GHP_MI_TOKEN` | `ghp_mi...`（首尾各4字符） |

**完整值存储位置**：只在 `.env` 或环境变量中，不要写入任何文件

---

## 👤 关于伟烨

详见：`memory/layer3/preferences.md`

---

## ⏰ 定时任务（6个，北京时间UTC+8）

| 时间(CST) | cron(UTC) | 任务 | 状态 |
|-----------|-----------|------|------|
| 07:00 | `0 23 * * *` | **每日医疗新闻写作** | ✅ 新增 |
| 02:00 | `0 18 * * *` | Moltbook社区学习 | ✅ |
| 03:00 | `0 19 * * *` | 医疗旅游资讯收集报告 | ✅ |
| 06:00 | `0 22 * * *` | AI重大信息搜集报告 | ✅ |
| 06:30 | `30 22 * * *` | 晨间记忆读取 | ✅ |
| 22:00 | `0 14 * * *` | 总结+保存 | ✅ |

> ⚠️ 注意：记忆备份到飞书(23:30)已取消，合并到22:00总结任务中

---

## 📝 博客写作标准流程（固化）

> 每次写博客必须按此流程执行，不能跳过步骤

### 流程5步

| 步骤 | 技能 | 目的 |
|------|------|------|
| 1 | `multi-search-engine` | 搜索相关关键词、竞争对手内容 |
| 2 | `content-research-writer-cn` | 研究主题，建立内容框架 |
| 3 | `programmatic-seo` | 按SEO规范写博客文章 |
| 4 | `humanizer` | 去AI化语言修改 |
| 5 | 部署到网站 | 写文件 + 更新sitemap + git push |

### 强制规则
- **不能跳过步骤** 直接写完就发布
- 步骤1-3是研究阶段，要认真做
- 步骤4是必须的，不能用AI直接写完就发
- 部署后更新sitemap.xml

### 技能位置
- 搜索：`skills/multi-search-engine/SKILL.md`
- 研究：`skills/content-research-writer-cn/SKILL.md`
- SEO写：`skills/programmatic-seo/SKILL.md`
- 去AI化：`skills/humanizer/SKILL.md`

---

## 📰 新闻写作标准流程（固化）

> 每天早上7:00自动执行（CST）
> 定时任务ID：`daily-medical-news`

### ⚠️ 频率说明
- **现阶段**：每日1篇（栏目新建期，填充内容）
- **后续调整**：栏目充实后降为2-3天1篇
- **质量门槛**：宁缺毋滥，没有好热点则不发

### 目的
- 蹭全球医疗热点
- 对比中国现状
- 引导到我们的服务

### 流程（6步）
| 步 | 动作 |
|----|------|
| 1 | 搜索热点（multi-search-engine） |
| 2 | 研究主题（content-research-writer-cn） |
| 3 | 写文章（programmatic-seo） |
| 4 | **去AI化（ai-humanizer）** ← 新增 |
| 5 | 部署（git push + 备份） |
| 6 | 更新sitemap |

⚠️ 步骤4去AI化是**必须**，不可跳过。评分>60必须修改后再发布。

### 文章结构
```
1. 热点引入：XX国出了XX技术
2. 中国现状：对应技术中国哪家医院有
3. 多维对比表格：技术/价格/服务/可及性
4. 总结+内部链接
```

### Schema要求
- 必须用 `NewsArticle` Schema（不是 Article）
- 参考模板：`website/news/template-news-article.html`

### 质量门槛
- 如果当天没有足够好的热点 → 不发
- 宁缺毋滥

### 目录结构
- URL：`/news/[日期-标题].html`
- sitemap 更新：添加 news 条目

---

## 🎯 网站战略方向（重要）

### 定位转型
- **不打**"medical tourism China"赛道（竞争太大）
- **改打**"中国就医攻略导航"：China hospital guide, Medical coordinator China, Healthcare advisor
- 原因：大机构不做长尾攻略导航词，天然蓝海

### 内容方向转型
- **弱化**：省钱、Save 50-80%、Cost comparison
- **强化**：安全性、专业性、中介服务价值
- 详见：`memory/layer3/decisions/战略方向决策_定位与内容转型.md`

---

## 🤖 AI Agent 服务出口战略（新方向，2026-04-06）

### 核心理念
**未来愿景**：外国人的 AI 助手直接查询我们的服务，而不是用户访问网站。

### 已完成
- ✅ `api/v1/hospitals.json` — 34家医院结构化数据，含信任评分
- ✅ `api/v1/index.json` — API文档
- ✅ `api/index.html` — 交互式API浏览器

### 信任评分体系（Trust Score）
| 字段 | 说明 |
|------|------|
| `trust.score` | 0-1，综合信任分 |
| `trust.level` | very_high(0.95+)/high(0.88+)/medium_high(0.80+)/medium |
| `trust.verified_fields` | 已验证的字段列表 |
| `trust.data_source` | official/multi_source/dual_source/single_source |
| `trust.cross_validated` | 交叉验证来源 |

### 下一步
- B选项（价格实时汇率版）待伟烨确认
- 补充更多 verified_fields（如具体价格范围、医生信息）
- 接入 sitemap.xml 供搜索引擎发现

---

## ⚠️ 待处理重要事项

- [ ] Reddit推广（伟烨已注册账号并浏览一周，养号中）
- [ ] Quora推广（刚启动测试）
- [x] Facebook商业账号开通 ✅（2026-03-29）
- [x] 提交 sitemap 到 Google Search Console ✅（2026-03-28）
- [x] 提供 Facebook Pixel ID ✅（2026-03-28）
- [x] PayPal支付 ✅（已开通）
- [x] WhatsApp ✅（已开通并正常使用）
- [x] memory-system skill 发布到 GitHub ✅（2026-03-29）
- [x] 网站部署 ✅（2026-04-04 确认正常）
- [ ] **进行中**：新闻栏目（news/），每天更新医疗新闻

---

_更新：2026-03-29 11:58_

---

_此文件是记忆系统的入口，每次会话优先读取。_
_详细记忆管理SOP见：`memory/layer4/memory-sop.md`_
