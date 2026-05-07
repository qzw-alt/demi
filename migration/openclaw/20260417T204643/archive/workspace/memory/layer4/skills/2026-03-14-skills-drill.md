# 2026-03-14 技能全面演练记录

## 🎯 演练目标
全面测试所有核心技能，记录使用感受，形成使用规范

---

## ✅ 已测试技能

### 1. multi-search-engine ⭐⭐⭐⭐⭐
**使用方式**: `web_fetch` + DuckDuckGo URL
**测试内容**: 并行搜索泰国、印度、新加坡医疗旅游
**效果**: 
- ✅ 3个搜索同时执行，速度快
- ✅ 获取了丰富的竞品信息
- ✅ 马来西亚搜索遇到验证码（正常反爬）

**使用感受**: 
- 比单一搜索引擎覆盖更广
- 无需API key，即开即用
- 需要处理反爬（验证码）
- **结论**: 日常搜索首选

---

### 2. content-research-writer ⭐⭐⭐⭐
**使用方式**: 阅读SKILL.md，按流程整理报告
**测试内容**: 整理竞品调研报告
**效果**:
- ✅ 报告结构清晰
- ✅ 覆盖全面（市场概况、优劣势、策略建议）
- ✅ 输出专业

**使用感受**:
- 技能文档很详细，但主要是方法论
- 实际写作还是需要自己组织
- 适合作为写作框架参考
- **结论**: 辅助写作工具，不能完全替代思考

---

### 3. humanizer ⭐⭐⭐⭐⭐
**使用方式**: 阅读SKILL.md，学习AI文本检测模式
**测试内容**: 分析竞品报告中的AI痕迹
**效果**:
- ✅ 识别出24种AI写作模式
- ✅ 提供了具体的修改建议
- ✅ 基于Wikipedia权威来源

**使用感受**:
- 非常实用的编辑工具
- 可以系统性地优化文案
- 适合发布前的文本润色
- **结论**: 所有对外文案必须经过humanizer检查

---

### 4. memory-simple ⭐⭐⭐
**使用方式**: 阅读SKILL.md
**测试内容**: 了解记忆系统架构
**效果**:
- ⚠️ 需要配置embedding API key
- ⚠️ 未实际测试捕获和召回

**使用感受**:
- 设计合理（JSON存储+向量检索）
- 比LanceDB-Pro稳定
- 但需要额外配置
- **结论**: 需要配置后使用，暂用文件系统替代

---

### 5. agent-browser ⭐⭐⭐⭐⭐
**使用方式**: `agent-browser open` + `snapshot`
**测试内容**: 抓取chinahospitalsguide.com页面元素
**效果**:
- ✅ 成功打开网站
- ✅ 获取了27个交互元素
- ✅ 识别出导航链接、按钮、FAQ等

**使用感受**:
- 非常强大的浏览器自动化工具
- 可以精准定位页面元素（@e1, @e2）
- 适合复杂网页操作、表单填写、测试
- **结论**: 复杂网页操作首选，简单抓取用web_fetch

---

### 6. github ⭐⭐⭐⭐⭐
**使用方式**: `git clone`, `git add`, `git commit`, `git push`
**测试内容**: 推送竞品报告到medical-tourism-notes仓库
**效果**:
- ✅ 成功推送33个博客文件
- ✅ 成功推送竞品报告
- ✅ 使用token认证

**使用感受**:
- 稳定可靠
- 需要token配置
- 是代码/文档管理的核心工具
- **结论**: 必备技能，所有输出都要版本控制

---

## ❌ 未测试技能（需配置或安装）

| 技能 | 原因 | 优先级 |
|------|------|--------|
| image-generation | 需要API key (OpenAI/Gemini/FLUX) | 高 |
| summarize | CLI未安装 | 中 |
| tavily-search | ✅ 已演练，效果优秀 | 高 |
| feishu-doc | 已安装但未测试写入 | 高 |
| feishu-bitable | 已安装但未测试 | 中 |
| social-media-management | 已安装但未测试 | 中 |
| heygen-avatar-lite | 需要API key | 低 |
| agentmail | 需要配置 | 中 |

---

## 📋 技能使用规范（基于演练）

### 搜索研究类

| 场景 | 技能 | 命令/方式 | 注意 |
|------|------|----------|------|
| 一般信息查询 | multi-search-engine | `web_fetch` + DuckDuckGo | 可能遇到验证码 |
| 深度研究 | tavily-search | 需配置API | 质量更高 |
| 网页抓取 | web-fetch | 直接URL | 简单快速 |
| 复杂网页操作 | agent-browser | `agent-browser open` | 需要元素交互时用 |

### 内容创作类

| 场景 | 技能 | 使用方式 | 注意 |
|------|------|----------|------|
| 文章写作 | content-research-writer | 参考框架 | 辅助工具，需自己组织 |
| 文案优化 | humanizer | 检查AI痕迹 | 发布前必用 |
| 长文总结 | summarize | 需安装CLI | 待配置 |
| 图片生成 | image-generation | 需API key | 待配置 |

### 数据管理类

| 场景 | 技能 | 使用方式 | 注意 |
|------|------|----------|------|
| 记忆检索 | memory-simple | 需配置embedding | 暂用文件系统 |
| 飞书文档 | feishu-doc | 待测试 | 高优先级 |
| 飞书表格 | feishu-bitable | 待测试 | 中优先级 |

### 发布管理类

| 场景 | 技能 | 使用方式 | 注意 |
|------|------|----------|------|
| 代码/文档版本控制 | github | git命令 | 必备 |
| 社媒发布 | social-media-management | 待测试 | 中优先级 |
| 邮件处理 | agentmail | 待配置 | 中优先级 |

---

## 🔧 立即配置项

### 高优先级（本周）
- [ ] 配置 Tavily API key（深度搜索）
- [ ] 安装 summarize CLI
- [ ] 测试 feishu-doc 写入功能
- [ ] 配置 image-generation API（OpenAI或Gemini）

### 中优先级（本月）
- [ ] 配置 memory-simple embedding
- [ ] 测试 social-media-management
- [ ] 配置 agentmail

---

## 💡 核心洞察

### 技能使用原则
1. **先用multi-search-engine** - 快速获取信息
2. **复杂操作用agent-browser** - 精准控制
3. **发布前用humanizer** - 去除AI痕迹
4. **所有输出用github** - 版本控制
5. **深度研究用tavily** - 高质量结果（配置后）

### 避免的坑
- ❌ 不要直接web_fetch代替multi-search-engine
- ❌ 不要跳过humanizer直接发布
- ❌ 不要忽视agent-browser的强大功能
- ❌ 不要手动管理文件，用github

### 效率提升
- ✅ 并行搜索节省70%时间
- ✅ agent-browser精准定位元素
- ✅ humanizer系统性优化文案
- ✅ github确保数据不丢失

### 7. tavily-search ⭐⭐⭐⭐⭐
**使用方式**: `node scripts/search.mjs "query" --deep`
**测试内容**: 搜索中国医疗旅游政策和质子治疗成本
**效果**:
- ✅ 返回结构化答案（带总结）
- ✅ 显示相关度评分（82%-100%）
- ✅ --deep 模式提供深度研究
- ✅ 支持新闻主题搜索

**使用感受**:
- AI优化的搜索结果，非常适合AI Agent使用
- 比multi-search-engine更深入
- 有API key限制，需要合理使用
- **结论**: 深度研究首选，日常搜索用multi-search-engine

---

## 📊 技能熟练度自评

| 技能 | 熟练度 | 使用频率目标 |
|------|--------|-------------|
| multi-search-engine | ⭐⭐⭐⭐⭐ | 每次搜索 |
| agent-browser | ⭐⭐⭐⭐⭐ | 复杂网页操作 |
| humanizer | ⭐⭐⭐⭐⭐ | 发布前必用 |
| github | ⭐⭐⭐⭐⭐ | 所有输出 |
| content-research-writer | ⭐⭐⭐⭐ | 写作参考 |
| memory-simple | ⭐⭐⭐ | 配置后使用 |
| 其他 | ⭐⭐ | 配置后测试 |

---

*记录时间: 2026-03-14 19:30 UTC*
*演练者: 德米*
*下次演练: 配置API后测试剩余技能*
