# China Hospitals Guide 内容写作风格指南

> **目标：** 让读者感觉内容是由在该领域有真实经验的人写的，而不是 AI 批量生成。
> 本指南基于对现有文章风格的分析和 AI 写作模式研究。

---

## 一、语气与风格

### 核心原则
- **像一个人写的**：有观点、有温度、有棱角。不只是汇报事实，要对事实有反应。
- **像在说一件真实的事**：不是"本文将探讨"，而是直接开讲。
- **自信但不夸大**：中国医疗的优势说够，局限也说清。

### 禁止腔调
| 类型 | 问题 | 例子 |
|------|------|------|
|  chatbot腔 | "great question!"、"I hope this helps!"、结尾问"Would you like..." | — |
|  官宣腔 | "is proud to announce"、"is committed to"、无意义的排比 | — |
|  旅游软文腔 | "breathtaking"、"nestled in"、"must-visit"、"stunning" | — |
|  中立到空洞 | 只有罗列没有观点，读者看完不知道作者怎么看 | — |

---

## 二、结构规范

### Blog/Article 标准结构

```
1. H1 标题 — 具体、诚实、有信息量，含年份便于SEO
2. 副标题 / 引言 — 钩子：事实/反常识/真实故事，30字内切入
3. 内容主体 — H2划章节，H3子主题，自然段落
4. CTA — 提供真实价值，不过度承诺
```

### NewsArticle 标准结构

```
1. 标题（含新闻点）
2. 副标题（新闻钩子）
3. meta：日期、作者、分类
4. 引言：新闻由头 + 核心结论
5. 主体：新闻展开
6. 背景/延伸
7. CTA
```

---

## 三、AI写作模式（必须规避）

### 语言类

1. **虚假重要性** — 触发：stands as, serves as, testament, underscores, highlights, pivotal, crucial
2. **过度修饰** — 触发：profound, vibrant, groundbreaking, renowned, exceptional
3. **无实质的 -ing** — 触发：highlighting, underscoring, fostering, showcasing, encompassing
4. **模糊归因** — 触发：experts say, industry observers note, sources indicate
5. **"不只是X，是Y"** — 错误：It's not just about cost—it's about access
6. **Rule of Three** — 错误：Innovation, inspiration, and transformation define...
7. **同义替换循环** — 同一事物用不同词反复称呼
8. **虚假范围** — 错误：from heart surgery to wellness checkups
9. **被动语态过度** — 错误：It should be noted that significant progress has been made

### 格式类

10. **Em Dash 滥用** — 最多1个，多余改为逗号或句号
11. **加粗列表标题** — 错误：`- **Speed:** Significantly faster`
12. **标题 Title Case** — 错误：`## Strategic Partnerships And Global Expansion`
13. **Emoji 装饰标题** — 错误：`## 🚀 Key Advantages`
14. **弯引号** — 错误：`"the treatment worked"` → 改为`"the treatment worked"`

---

## 四、数据规范

- 具体数字：`47 Class A hospitals`（不是 `many hospitals`）
- 标注来源：`[机构名称] reported...`
- 无数据时：可以说"医院表示"，不瞎编
- 医院名首次：中文全称 + 英文，后续统一

---

## 五、Schema 和 SEO 规范

### 所有文章必须包含
```html
<!-- Article/NewsArticle Schema -->
<script type="application/ld+json">
{
    "@context": "https://schema.org",
    "@type": "Article",  <!-- 或 NewsArticle -->
    "headline": "...",
    "datePublished": "YYYY-MM-DD",
    "dateModified": "YYYY-MM-DD",
    "author": { "@type": "Organization", "name": "China Hospitals Guide" }
}
</script>

<!-- BreadcrumbList Schema -->
<script type="application/ld+json">
{ "@context": "https://schema.org", "@type": "BreadcrumbList",
  "itemListElement": [
    { "position": 1, "name": "Home", "item": "https://chinahospitalsguide.com/" },
    { "position": 2, "name": "Blog", "item": "https://chinahospitalsguide.com/blog/" },
    { "position": 3, "name": "Article Title", "item": "https://chinahospitalsguide.com/blog/slug.html" }
  ]
}
</script>
```

### Meta 标签
```html
<title>具体标题 | China Hospitals Guide</title>
<meta name="description">150-160字符，包含关键词</meta>
<link rel="canonical" href="...">
<meta property="og:type/title/description/url/image">
<meta name="twitter:card"> （summary_large_image）
```

---

## 六、可信度建设

必须包含：
- **局限性说明**（医疗内容必须）：
  > ⚠️ **重要提示**：此类治疗尚处于临床试验阶段。患者应充分了解风险，选择有资质的医疗机构。
- **方法论说明**（排名类）：`我们根据[公开数据/实地访问]对医院进行了评估...`
- **时效性说明**（数字类）：`*所有数据截至[年份]，如有更新欢迎指出。*`

避免：绝对化疗效（cures cancer）、未验证排名（#1、best in world）

---

## 七、CSS 样式规范

| 类名 | 用途 | 颜色 |
|------|------|------|
| `.highlight-box` | 重要信息 | 蓝色背景，左蓝边 |
| `.tip-box` | 实用建议 | 绿色背景，左绿边 |
| `.warning-box` | 风险/注意 | 黄色背景，左黄边 |
| `.stat-grid` | 数据卡片 | 三列 |
| `.cta-section` | 底部行动 | 渐变蓝底 |

---

## 八、发布前检查清单

**内容**
- [ ] 标题具体，不夸大
- [ ] 引言有真实钩子
- [ ] 无 AI 模式残留（对照 humanizer 自审）
- [ ] 有局限性说明
- [ ] 数据有来源

**SEO**
- [ ] Schema JSON 完整，类型正确（Article/NewsArticle）
- [ ] BreadcrumbList 路径正确
- [ ] meta description 150-160字符
- [ ] canonical URL 正确
- [ ] og:*/twitter:* 完整
- [ ] 日期格式 YYYY-MM-DD

**技术**
- [ ] 图片已优化（< 80KB）
- [ ] HTML 语法正确
- [ ] 发布后更新 sitemap.xml

---

## 参考样本

已有正面示范：
- **结构感好**：`blog/best-cancer-hospitals-china-2026.html` — 章节编号，数据卡片，局限性说明
- **语气自然**：`blog/why-medical-tourists-choose-china-over-thailand.html` — 开篇叙事，数据卡片，承认竞品优势
- **引言钩子好**：`news/2026-04-18-china-medical-tourism-car-t-global-destination.html` — 真实故事开头，直给数字

---

*基于 Wikipedia "Signs of AI writing" 指南和实际内容审查，2026-05-02 制定。*
