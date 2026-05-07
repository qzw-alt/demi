# 新闻写作 SOP 📰

> 状态：已固化
> 最后更新：2026-03-24
> 触发：每天早上7:00 CST 自动执行（cron job: daily-medical-news）

---

## 目的

- 蹭全球医疗热点，Google喜欢新鲜内容
- 对比中国现状，创造独特价值
- 引导到我们的服务/医院页面

---

## ⚠️ 铁律：质量门槛

**如果当天没有足够好的热点 → 不发布**
- 宁缺毋滥
- 低质量新闻比没新闻更损害品牌形象

### 频率说明
- **现阶段**：每日1篇（栏目新建期，填充内容）
- **后续调整**：栏目充实后降为2-3天1篇
- 届时修改 cron 表达式即可

---

## 文章结构模板

### 1. 热点引入（The Breaking News）
```
[国家]最近宣布了[技术/突破]，这是[相关领域]的重大进展。
- 什么技术？
- 有什么特别？
- 为什么现在发生？
```

### 2. 中国现状（China's Current Landscape）
```
与此同时，中国在[相关领域]也有显著发展。
- 哪些医院有类似技术？
- 发展到什么程度？
- 与全球相比处于什么位置？
```

### 3. 对比分析（Comparison Table）
必须包含表格：

| 因素 | [国家] | 中国 |
|------|--------|------|
| 技术水平 | | |
| 费用 | | |
| 服务质量 | | |
| 可及性 | | |
| 等待时间 | | |

### 4. 关键要点（Key Takeaways）
- 3-5个核心洞察
- 用 bullet points

### 5. 内部链接（Related Information）
- 链接到网站相关页面
- 癌症治疗 → /treatments/cancer.html
- 心脏手术 → 相关页面
- 服务页面 → /services.html

### 6. 外部权威链接 ✨
- **学术论文/研究** → 链接到原文（PubMed、Google Scholar等）
- **高权重新闻网站** → 链接到原始报道（Reuters、Nature、NEJM、BBC Health等）
- 外部权威链接 → 提升文章可信度，Google喜欢有出处的内容

### 7. CTA
- 标准 CTA section

---

## Schema 要求

**必须使用 NewsArticle Schema**（不是 Article）

```json
{
  "@type": "NewsArticle",
  "headline": "[标题]",
  "datePublished": "[YYYY-MM-DD]",
  "dateModified": "[YYYY-MM-DD]"
}
```

参考模板：`/root/.openclaw/workspace/website/news/template-news-article.html`

---

## 标题规范

- 包含国家名 + 技术名 + "China Compare"
- 示例：`Thailand's New Cancer Treatment: How Does China Compare?`
- 长度：50-60字符
- 包含搜索关键词

---

## URL & 文件名规范

```
URL: /news/[日期-标题-slug].html
例：/news/2026-03-24-thailand-cancer-treatment-china-compare.html
```

## 图片规范 🖼️

**下载图片到本地（推荐）：**
```bash
# 从 Unsplash 等免费图源下载
curl -L -A "Mozilla/5.0" -o /website/images/[图片名].jpg "[图片URL]"

# 常用免费图源
- Unsplash: https://unsplash.com/s/photos/[关键词]
- Pexels: https://www.pexels.com/search/[关键词]/
```

**图片保存位置：** `/root/.openclaw/workspace/website/images/`

**HTML 引用格式：**
```html
<figure style="margin: 20px 0; text-align: center;">
    <img src="/images/[图片文件名].jpg" alt="[图片描述]" style="max-width: 100%; border-radius: 10px; box-shadow: 0 4px 12px rgba(0,0,0,0.15);">
    <figcaption style="font-size: 0.85rem; color: #666; margin-top: 8px;">[图片来源说明] | Photo: [来源](链接)</figcaption>
</figure>
```

**图片来源标注：**
- 必须注明图片来源
- 推荐使用 CC0 授权图片（Unsplash、Pexels）
- 如果是原始新闻的图片，保留原始来源

---

## Sitemap 更新

```xml
<url>
  <loc>https://chinahospitalsguide.com/news/[slug].html</loc>
  <lastmod>[YYYY-MM-DD]</lastmod>
  <changefreq>weekly</changefreq>
  <priority>0.9</priority>
</url>
```

---

## 搜索关键词

每天搜索时用的关键词：

- `[国家] medical breakthrough 2026`
- `China hospital new technology 2026`
- `medical tourism [country] vs China`
- `healthcare innovation [region]`
- `cancer treatment [country] 2026`

---

## ★ Humanizer 去AI化（必须执行）

文章写完后，必须调用 `ai-humanizer` skill 做去AI化处理：

```bash
# 全文分析+评分
node skills/ai-humanizer/src/cli.js analyze -f news/[文章文件名].html

# 或直接 humanize（保留原文件，输出到新文件）
node skills/ai-humanizer/src/cli.js humanize -f news/[文章文件名].html -o news/[文章文件名]_humanized.html
```

**或通过 skill 调用**：读取 `skills/ai-humanizer/SKILL.md` 获取完整指令。

⚠️ 如果 humanizer 评分 > 60（明显AI味），必须修改后再发布。

---

## ★ Git 推送步骤（必须执行）

文章写作完成后，必须执行以下步骤将内容推送到 GitHub：

```bash
cd /root/.openclaw/workspace/chinahospitalsguide
git add news/[新文章文件名].html news/index.html sitemap.xml
git commit -m "Add news article for YYYY-MM-DD"
git push
git add news/[新文章文件名].html news/index.html sitemap.xml
git commit -m "Add news article for YYYY-MM-DD"
git push
git push

# 同步备份到 demi 仓库
cd /root/.openclaw/workspace/demi
git pull
git add news/[新文章文件名].html news/index.html sitemap.xml
git commit -m "Add news article for YYYY-MM-DD"
git push
```

⚠️ **没有推送 = 任务未完成**

---

## 快速恢复

如果忘记新闻写作流程：
1. 读 `MEMORY.md` → 找"新闻写作标准流程"
2. 读 `memory/layer4/sops/news-writing-sop.md`
3. 参考模板：`website/news/template-news-article.html`
