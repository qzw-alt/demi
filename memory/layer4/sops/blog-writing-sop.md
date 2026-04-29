# 博客写作标准流程 SOP 📝

> 状态：已固化
> 最后更新：2026-03-24
> 触发：每次写博客文章时

---

## ⚠️ 铁律：不能跳过步骤

本流程共5步，每步都必须执行：
1. 搜索（multi-search-engine）
2. 研究（content-research-writer-cn）
3. SEO写作（programmatic-seo）
4. 去AI化（humanizer）
5. 部署到网站

---

## 步骤1：搜索 🔍

**技能：** `multi-search-engine`

**目的：** 了解搜索环境、竞争对手、用户需求

**操作：**
1. 读取 `skills/multi-search-engine/SKILL.md`
2. 搜索相关关键词
3. 查看竞争对手的内容
4. 找到搜索意图和内容缺口

**输出：** 关键词列表、竞争对手分析、内容方向

---

## 步骤2：研究 📚

**技能：** `content-research-writer-cn`

**目的：** 深入研究主题，建立内容框架

**操作：**
1. 读取 `skills/content-research-writer-cn/SKILL.md`
2. 按技能要求进行内容研究
3. 建立文章大纲

**输出：** 文章大纲、内容框架、关键数据/引用

---

## 步骤3：SEO写作 ✍️

**技能：** `programmatic-seo`

**目的：** 按SEO规范输出高质量文章

**操作：**
1. 读取 `skills/programmatic-seo/SKILL.md`
2. 参考现有博客模板（如 `website/blog/how-to-prepare-medical-travel-china.html`）
3. 按SEO要求写文章
4. 包含 Schema markup（Article、BreadcrumbList）

**输出：** 完整的HTML博客文章

---

## 步骤4：去AI化 � human

**技能：** `humanizer`

**目的：** 移除AI写作痕迹，让文章读起来更自然

**操作：**
1. 读取 `skills/humanizer/SKILL.md`
2. 对文章进行humanize处理
3. 检查：语气、节奏、个性、观点

**输出：** 去AI化后的文章

---

## 步骤5：部署到网站 🚀

**目的：** 将文章发布到网站

**操作：**
1. 保存HTML文件到 `website/blog/[文章slug].html`
2. 更新 `website/sitemap.xml` 添加新文章条目
3. git add → commit → push

**文件名规范：** 英文slug，用连字符分隔，如 `medical-guide-seeking-treatment-china.html`

**sitemap格式：**
```xml
<url>
  <loc>https://chinahospitalsguide.com/blog/[文章slug].html</loc>
  <lastmod>2026-03-24</lastmod>
  <changefreq>monthly</changefreq>
  <priority>0.8</priority>
</url>
```

---

## 模板参考

写博客前先参考现有模板：
- `/root/.openclaw/workspace/website/blog/how-to-prepare-medical-travel-china.html`

**模板特点：**
- CSS内嵌（响应式设计）
- 包含 Article Schema + BreadcrumbList Schema
- 多个内容区块：highlight-box、warning-box、tip-box、timeline、checklist
- CTA section 在文章末尾
- Footer 包含版权和链接

---

## 快速恢复

如果忘记流程：
1. 读 `MEMORY.md` → 找"博客写作标准流程"章节
2. 读 `memory/layer4/sops/blog-writing-sop.md`

