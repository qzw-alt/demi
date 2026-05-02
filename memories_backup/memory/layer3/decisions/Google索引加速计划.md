# Google 索引加速行动计划

> 目标：让 Google 尽快抓取和索引网站所有页面
> 创建时间：2026-03-19
> 当前状态：29个页面已发现但未索引

---

## 📊 当前状况

| 指标 | 数值 | 状态 |
|:---|:---|:---|
| 已发现页面 | 29个 | ✅ |
| 已索引页面 | 0个 | ❌ |
| 上次抓取 | 1970-01-01（从未抓取）| ❌ |
| 问题类型 | Discovered - currently not indexed | ⚠️ |

---

## 🎯 行动计划（分阶段）

### 阶段1：立即执行（今天-明天）

#### 1.1 重新提交 Sitemap
**操作步骤：**
1. 访问 [Google Search Console](https://search.google.com/search-console)
2. 选择你的网站属性
3. 左侧菜单 → Sitemaps
4. 删除旧的 sitemap.xml
5. 重新提交 `https://chinahospitalsguide.com/sitemap.xml`

**预期效果：** 触发 Google 重新抓取

#### 1.2 手动提交关键页面
**操作步骤：**
1. 在 Search Console 中，使用 URL Inspection 工具
2. 逐个提交以下关键页面：
   - `https://chinahospitalsguide.com/`（首页）
   - `https://chinahospitalsguide.com/blog/`（博客首页）
   - `https://chinahospitalsguide.com/hospitals.html`
   - 最新发布的3篇博客文章

**预期效果：** 优先抓取重要页面

#### 1.3 检查 robots.txt
**验证：**
- 访问 `https://chinahospitalsguide.com/robots.txt`
- 确保没有 `Disallow: /` 或阻止 Google 的规则

---

### 阶段2：本周执行（3-7天）

#### 2.1 创建外部链接（最重要）

**Reddit 策略：**
| 子版块 | 帖子类型 | 链接方式 |
|:---|:---|:---|
| r/medicaltourism | 分享经验帖 | 软植入网站链接 |
| r/healthcare | 问答帖 | 回答问题时引用博客文章 |
| r/frugal | 省钱医疗帖 | 分享费用对比 |

**Quora 策略：**
- 搜索问题："affordable surgery abroad", "medical tourism"
- 撰写详细回答，引用相关博客文章
- 示例回答结构：
  ```
  简短回答 + 个人经验/数据
  
  详细解释...
  
  更多信息：[博客文章标题](链接)
  ```

**社交媒体：**
- LinkedIn：发布专业内容，链接到博客
- Twitter/X：分享博客文章片段+链接

#### 2.2 内部链接优化
**操作：**
- 确保每篇博客文章都有3-5个内部链接
- 从首页链接到重要博客文章
- 创建"相关文章"推荐区块

#### 2.3 持续内容发布
**计划：**
- 每天发布1篇新博客文章
- 新内容会触发 Google 重新抓取网站

---

### 阶段3：持续优化（2-4周）

#### 3.1 监控索引状态
**每周检查：**
- Search Console Coverage 报告
- 查看新页面是否被索引
- 记录索引率变化

#### 3.2 技术优化
**检查清单：**
- [ ] 页面加载速度 < 3秒
- [ ] 移动端适配良好
- [ ] 所有图片有 alt 标签
- [ ] 无404错误页面
- [ ] Schema 标记正确

#### 3.3 内容质量提升
**Google 偏好：**
- 长内容（2000+ 词）
- 原创、有价值的信息
- 定期更新
- 用户停留时间长

---

## 📈 预期时间线

| 时间 | 预期结果 |
|:---|:---|
| 1-3天 | Sitemap重新提交，Google开始抓取 |
| 1周 | 首页和主要页面被索引 |
| 2-3周 | 博客文章开始被索引 |
| 1个月 | 大部分页面被索引 |
| 2-3个月 | 开始获得自然搜索流量 |

---

## 🛠️ 工具清单

| 工具 | 用途 | 链接 |
|:---|:---|:---|
| Google Search Console | 监控索引状态 | search.google.com/search-console |
| Google Analytics | 流量分析 | analytics.google.com |
| PageSpeed Insights | 速度测试 | pagespeed.web.dev |
| Mobile-Friendly Test | 移动适配测试 | search.google.com/test/mobile-friendly |

---

## ✅ 每日检查清单

- [ ] 发布新博客文章
- [ ] 在 Reddit/Quora 分享1个链接
- [ ] 检查 Search Console 是否有新错误
- [ ] 监控网站流量（Analytics）

---

## 📊 成功指标

| 指标 | 当前 | 1个月目标 | 3个月目标 |
|:---|:---|:---|:---|
| 索引页面数 | 0 | 20+ | 40+ |
| 自然搜索流量 | 0 | 50/月 | 500/月 |
| 关键词排名 | - | 5个前50 | 10个前20 |

---

*计划制定：德米*
*最后更新：2026-03-19*
