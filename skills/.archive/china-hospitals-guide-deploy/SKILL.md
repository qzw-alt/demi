---
name: china-hospitals-guide-deploy
description: China Hospitals Guide 网站部署流程 - 新闻写作、发布、备份
category: productivity
---
# China Hospitals Guide 部署流程

## 仓库
- **网站仓库**: `qzw-alt/chinahospitalsguide` (GitHub)
- **备份仓库**: `qzw-alt/demi` (GitHub)

## 工作区路径（已更新 2026-05-02）

**网站仓库工作目录**: `/root/.hermes/workspace/chinahospitalsguide/`
- `git remote -v` → `origin → https://github.com/qzw-alt/chinahospitalsguide.git`
- **不要混淆**：`oriental-destiny` 项目在 `/root/.hermes/workspace/oriental-destiny/`

**GitHub Pages 部署**: push 后约 1-2 分钟自动刷新（无构建系统，纯静态托管）

## Git 终端链式命令问题

**症状**: `git add ... && git commit ... && git push` 报错 `Foreground command uses '&' backgrounding`

**原因**: 终端工具不支持 `&&` 链式命令。

**解决 — 两种方式（任选）**:

**方式A — 分行执行（推荐，最简单）**:
```bash
cd /root/.hermes/workspace/chinahospitalsguide
git add blog/slug.html blog/index.html sitemap.xml
git commit --message "Add blog post: slug"
git push origin master
```

**方式B — git -C 指定路径**:
```bash
git -C /root/.hermes/workspace/chinahospitalsguide add blog/slug.html blog/index.html sitemap.xml
git -C /root/.hermes/workspace/chinahospitalsguide commit --message "Add blog post: slug"
git -C /root/.hermes/workspace/chinahospitalsguide push
```

**注意**: 不要混用 `&&`，每条命令单独执行。

### 远程并发提交导致 Diverged Branches

**场景**: 本地和 origin/master 都有新 commit，push 时被拒绝。

**策略A — Merge（推荐，用于内容更新）**:
```bash
cd ~/.hermes/workspace/chinahospitalsguide
git fetch origin master
git merge origin/master   # 产生冲突时用 ours 策略
git checkout --ours blog/article.html   # 保留我们的版本
git add blog/article.html
git commit -m "Resolve merge: keep our version"
git push origin master
```

**策略B — Rebase + 清理**（如果坚持用 rebase）:
```python
# 批量清理冲突标记（Python 比 sed 更可靠）
import re, glob

for fpath in glob.glob("blog/*.html"):
    content = open(fpath).read()
    if '<<<<<<' in content:
        canonical_m = re.search(r'<link rel="canonical"[^>]+>', content)
        if canonical_m:
            canonical_val = canonical_m.group(0)
            parts = re.split(r'<<<<<<|======|>>>>>>', content)
            cleaned = parts[0].strip()
            for i, part in enumerate(parts[1:-1], 1):
                if i % 2 == 0:
                    cleaned += '\n' + part.strip()
            with open(fpath, 'w') as f:
                f.write(cleaned)
            print(f"Fixed: {fpath}")
```

**清理孤儿 rebase 目录**:
```bash
rm -rf .git/rebase-apply .git/rebase-merge
git status  # 确认干净
```

### Token 问题（同上远程URL）

**检查**:
```bash
git remote -v
cat ~/.git-credentials
```

**修复**:
```bash
git remote set-url origin https://qzw-alt:NEW_TOKEN@github.com/qzw-alt/chinahospitalsguide.git
```

`og-image.jpg` 是所有新闻列表页共用的封面图，每篇新闻都会重复加载。**发布新文章前必须优化**。

### 判断标准
- 新闻列表页有 20+ 篇 → 每篇加载同一张图 → 必须优化
- 列表页单张图超过 80KB → 需要优化

### 工具：ffmpeg（可用）
```bash
# 压缩 JPEG：290KB → 60KB（800px宽，quality 80）
ffmpeg -i og-image.jpg -vf "scale=800:-1" -q:v 5 -y og-image-compressed.jpg

# 生成 WebP 版本（推荐，更小）
ffmpeg -i og-image.jpg -vf "scale=800:-1" -c:v libwebp -quality 80 -y og-image.webp

# 验证大小
ls -lh og-image.jpg og-image.webp
```

### 发布前更新列表页图片引用
所有新闻/博客列表页的 `<img src="...og-image.jpg">` 改为 `.webp`：
```bash
# 替换所有列表页的 og-image.jpg → og-image.webp
sed -i 's|og-image\.jpg|og-image.webp|g' news/index.html
# Blog 列表页同理
```

### 图片尺寸标准
| 用途 | 最大宽度 | 文件大小目标 |
|------|----------|-------------|
| 新闻列表封面 | 800px | < 80KB |
| 博客列表封面 | 800px | < 80KB |
| OG 社交分享图 | 1200px | < 200KB |

---

## 发布流程

### 1. 确认工作目录
```bash
cd /root/.hermes/workspace/chinahospitalsguide
git status   # 确认在 master 分支
```

### 2. 编辑文件
- 新闻文章: `news/YYYY-MM-DD-slug.html`
- 博客文章: `blog/slug.html`
- 站点文件: `sitemap.xml` 等

### 3. Git 提交并推送
```bash
git add <changed-files>
git commit -m "描述"
git push origin master
```

### 4. 验证
等待约 1-2 分钟，检查 https://chinahospitalsguide.com/ 是否更新

### 5. 备份到 demi（可选）
```bash
cd /root/.hermes/workspace/
git add <changed-files> && git commit -m "Backup: 描述" && git push backup master
```

---

## 博客文章发布流程（完整6步）

### Step 1 — 研究
搜索主题关键词、竞品文章、搜索意图。参考同类文章结构（如 `/blog/dental-implants-china.html` 的版式）。

### Step 2 — 写文章
- 路径: `/root/.hermes/workspace/chinahospitalsguide/blog/slug.html`
- 结构: H1 → Quick Cost Snapshot → 章节（H2/H3）→ CTA box → FAQ → Disclaimer
- 元数据: description, og:title, og:description, canonical URL, NewsArticle Schema

### Step 3 — 去AI化（必须，不可跳过）
对照 `humanizer` skill 扫描以下特征并修复：
- AI词汇: delve, tapestry, pivotal, testament, underscore, showcase 等
- 句式问题: 无谓的 "—"，被动语态过度，三段式套路
- 空洞表述: 无具体支撑的 "considered more stable" → 改为具体建议
- 信号词: "In order to", "It is important to note", "The real question is"

### Step 4 — 更新博客索引（关键：先检查是否已存在）

**先搜索确认文章是否已在索引中**:
```bash
grep -i "dental-implants\|slug" ~/.hermes/workspace/chinahospitalsguide/blog/index.html
```

- 文章已在索引中 → 检查日期是否需要更新，是否需要调整位置
- 文章不在索引中 → 按以下格式插入

在 `blog/index.html` 中插入文章卡片（在 Dental Tourism 类别之前）:
```html
<div class="blog-card">
    <div class="blog-image" style="background: linear-gradient(...)">👁️</div>
    <div class="blog-content">
        <div class="blog-category">分类名</div>
        <h3 class="blog-title">标题</h3>
        <p class="blog-excerpt">摘要</p>
        <div class="blog-meta"><span>📅 May 2026</span><span>⏱️ 10 min read</span></div>
        <a href="slug.html" class="read-more">Read Article →</a>
    </div>
</div>
```

### Step 5 — 更新 sitemap.xml
在 `sitemap.xml` 插入新文章条目（参考 dental-implants 的位置）:
```xml
<url>
  <loc>https://chinahospitalsguide.com/blog/slug.html</loc>
  <lastmod>2026-05-02</lastmod>
  <changefreq>monthly</changefreq>
  <priority>0.8</priority>
</url>
```

### Step 6 — Git 提交并推送（处理分支分叉）
```bash
cd /root/.openclaw/workspace/website

# 如果本地和 origin/master 分叉，先合并
git fetch origin master
git merge origin/master
# 如果有冲突 → 使用 ours 策略保留新文章内容
# git checkout --ours blog/slug.html && git add blog/slug.html

git add blog/slug.html blog/index.html sitemap.xml
git commit -m "Add blog post: slug"
git push origin master
```

**验证**: GitHub Pages 通常需要 **2-5 分钟**重新构建。
GitHub Pages 通常需要 **2-5 分钟**重新构建。先推送，再等 3 分钟验证 URL。首次访问新文章 URL 可能返回 404（GitHub Pages 还在构建），稍后再试。

---

## ⚠️ 终端 Git 链式命令问题

**症状**: `git add ... && git commit ... && git push` 报错 `Foreground command uses '&' backgrounding`

**原因**: 终端工具不支持 `&&` 链式命令。

**解决**: 拆分成独立命令，分开执行。
```bash
git -C /path/to/repo add 文件
git -C /path/to/repo commit --message "提交信息"
git -C /path/to/repo push
```

---

## 新闻写作标准流程

**详细流程 → 见 `news-writing-template` skill**

关键点：
- 路径：`news/YYYY-MM-DD-slug.html`
- 新闻索引：`news/index.html` — 新文章卡片**插入最顶部**（最新在前）
- sitemap.xml：插入位置在 `<loc>https://chinahospitalsguide.com/news/</loc>` 之后
- **必须有真实来源脚注**（带超链接的编号列表）
- **必须有配图或 CSS gradient banner**
- **必须用 NewsArticle Schema**（不是 Article）
- URL 格式是 `news/`（目录），**不是 `news.html`**

### 新闻选题来源
```
Google News: https://news.google.com/search?q=medical+tourism+china+2026
优先找：有具体数据/机构名/事件的当天或近1-2天内的真实新闻
标题公式：[事件] — [惊喜数据] — How Does China Compare?
```

### Git 终端链式命令（已验证有效）
```bash
cd /root/.openclaw/workspace/website
git add news/YYYY-MM-DD-slug.html news/index.html sitemap.xml
git commit --message "News: 文章标题"
git push
```

## 网站仓库清洁规则（重要）

**只放网站运行必需的文件**。内部运营文档必须删除或放到备份仓库 `demi`：

| 目录/文件 | 是否保留 | 说明 |
|-----------|----------|------|
| `ops/` | ❌ 删除 | Google Sheets 模板、仪表盘、内部文档 |
| `scripts/` | ❌ 删除 | 表单处理、webhook、内部脚本 |
| `api/hospital-info-collection.md` | ❌ 删除 | 内部文档 |
| `api/v1/` + `api/index.html` | ✅ 保留 | 前端用到 |
| `.nojekyll` / `robots.txt` / `CNAME` | ✅ 保留 | GitHub Pages 必需 |
| `og-image.jpg` | ⚠️ 可选 | 太大可以用图床替代 |

**清理命令**:
```bash
cd ~/.hermes/workspace/chinahospitalsguide
git rm -rf ops/ scripts/
git rm api/hospital-info-collection.md
git commit -m "chore: remove internal ops/docs from website repo"
git push origin master
```

**注意**：远程其他人可能也推送了 ops/ 文件，合并后要重新删除并推送（2026-04-30 遇到此情况）。

---

## sitemap.xml 新增页面规则

新增 treatments/ 或 stories/ 页面时，必须同步添加到 sitemap.xml，否则 Google 不会索引。

sitemap.xml 插入位置参考：
- treatments/: 插入 `treatments/index.html` 条目附近
- stories/: 插入 `stories/index.html` 条目附近
- priority 值：index页=0.8，详情页=0.6-0.7

## 内容选题框架
- `references/pain-point-mining-framework.md` — 挖矿式选题5步法（从真实痛苦中找商业点子）
- `references/seo-metadata-audit-2026-05-02.md` — SEO元数据审计结果（覆盖率基线 + 注入策略）

## 内容风格指南

发布内容前对照：**`content-style-guide.md`**（位于网站根目录）

包含：
- AI写作模式规避清单（28类）
- 可信度建设规范（局限性声明、数据来源标注）
- CSS样式规范（配色、通用类名）
- Schema + SEO 规范
- 发布前检查清单

写作流程中每篇文章必须通过 humanizer 自审。

## 待处理问题（来自2026-04-28巡检，已更新2026-05-02）
- [ ] Privacy/Terms 内容空白 — 需要补全
- [x] Course 9节课全部上线 — **2026-05-02 完成**（剩余8节全部补全，ch2-ch9）
- [ ] Reddit 养号（账号已注册）
- [ ] Quora 推广（刚启动）

## 课程章节写作流程（已验证 2026-05-02）

### 背景
课程 ch2-ch9 原本只有骨架（166-184行/章），ch1是唯一完整章节（796行）。2026-05-02 一次性补全全部8章。

### 流程：子代理并行写作 + 主代理审核合并
```
主代理（你）
  ├── 读取 ch1 完整章节 → 理解模板结构
  ├── 规划9章内容大纲 → todo list
  ├── 并行提交子代理任务（每代理1-2章）
  │   └── 每个子代理：
  │       ├── 读取 ch1/ch2 理解风格
  │       ├── 写完整 HTML（full content, no truncation）
  │       └── 写完返回摘要
  └── 主代理审核行数/质量 → git add + commit + push
```

### 验证信号
- 每章行数应 ≥ 400行（内容丰富的完整章节）
- 每章必须包含：SEO meta、ToC、info-box、comparison/cost table、checklist、chapter nav、CTA
- Git push 成功 = 任务完成

### 子代理 prompt 模板（可直接复用）
```
Write a complete, full-length chapter HTML file at {path}

This is a medical tourism course chapter about {topic}. Write the complete file with FULL substantive content (at least 2,000 words of actual readable chapter content). Do NOT write a skeleton or partial file.

Design specs:
- Color scheme: primary=#1e3c72, accent=#c84b31, success=#22c55e, background=#f8f9fa, white=#ffffff
- HTML entities for emojis: 🏥 = &#x1F3E5;, ✓ = &#x2713;, → = &#x2192;, ...
- BASE_URL = https://chinahospitalsguide.com
- OG_IMAGE = https://chinahospitalsguide.com/og-image.jpg
- Google Analytics ID: G-RVYZENK472
- CSS classes: info-box, info-box.warning, info-box.success, comparison-table, cost-table, checklist-box, ...
- Navigation links: index.html, hospitals.html, services.html, how-it-works.html, blog/, news/, resources.html, ./index.html (active), contact.html, contact-new.html

Full required structure:
1. SEO meta block (canonical, og:type=article, og:title, og:description, og:url, og:image, og:site_name, twitter:card/title/desc/image, JSON-LD Article schema)
2. Complete CSS matching the course template style
3. Google Analytics script in head
4. Navbar with all links
5. Page header (chapter-badge, title, subtitle, meta info)
6. content-card with:
   a. TOC with N sections
   b. Sections 1-N (full content for each)
   c. Chapter Summary with success info-box
   d. Chapter navigation (prev/next)
7. CTA section linking to ../contact-new.html
8. Scroll progress JS and mobile nav toggle

Write the COMPLETE file. Do not truncate. Write it now.
```

### Treatments & Stories Pages 扩展工作流（2026-05-02 新增）

当发现 treatments/ 或 stories/ 下有页面行数异常少（如 <200行），需要整体重建：

**优先规则**：
- `treatments/cardiac.html` 仅85行 → 重建到600+行（对标 `treatments/ivf.html` 674行作为样式模板）
- `treatments/stem-cell.html` 不存在 → 新建（对标 `treatments/ivf.html` 样式）
- stories 页面行数 <400行 → 扩展（对标 `stories/james-wilson.html` 398行作为样式）
- `stories/index.html` 仅75行 → 整体重建

**Style 模板引用规则**：
```
treatments/ 系列页面  → 参考 treatments/ivf.html（674行）
stories/ 系列页面    → 参考 stories/james-wilson.html（398行）
course/ 系列章节     → 参考 course/chapter-1-healthcare-system.html（796行）
```

**并行任务数限制**：`delegate_task` 单次最多3个子任务（max_concurrent_children=3），超出报错。超过3个任务时，分批提交。

**子代理 Prompt 模板（treatments/stories 页面）**：
```
The existing {template_file} ({template_lines} lines) is your style template.
Read it with read_file to get the exact CSS class patterns, section structure,
and component styles before writing.

File requirements:
- Title: "..."
- Meta description: ...
- Canonical: {BASE_URL}/...
- Full Open Graph + Twitter Card meta tags
- Google Analytics 4 script in head
- Complete CSS matching the template style EXACTLY

Content sections to include:
1. [section name] - ...
2. ...

Write the COMPLETE file matching the template EXACTLY.
Do not truncate. Do not invent new class names.
```

### 注意事项
- 单次 `terminal` 不支持 `&&` 链式命令，必须拆成独立调用
- `git commit && git push` 会报错，需分开执行
- 写作时用 HTML 实体替代 emoji（&#x1F3E5; 等）
- 每章 progress bar width 应递增（ch1=11%, ch2=22%, ch3=33%...）
- Treatments/stories 页面不使用 course 的 progress bar，样式完全不同

### 刷新已有文章（Refresh Workflow）

**场景**: 今日轮到某长尾词，但该文章昨天已发布。需要判断是"跳过"还是"刷新并嵌入今日新闻"。

**判断流程**:

1. 检查文章是否已在 blog/index.html（首页展示）
   - 不在 → 需要添加到首页
   - 在 → 检查日期是否需要更新

2. 搜索当日新闻（Google News RSS）看是否有相关热点
   - 有相关热点 → 执行刷新（见下）
   - 无热点且文章质量尚可 → 跳过，不强写

**刷新操作步骤**:

1. 读取原文章全文（确认最新日期、内容）
2. 检查是否有重复内容（如 Straumann 被提了两次 April + February）
   - 有 → 合并为一句精准的 news hook
3. 找当日/近1-2天相关新闻作为 fresh hook
4. 更新 `datePublished` 和 `dateModified` 为今天日期
5. 更新文章内日期显示（HTML meta 中）
6. 更新来源列表（添加新引用）
7. 检查 blog/index.html — 确认文章卡片存在
8. 检查 sitemap.xml — 确认 URL 已存在（无需重复添加）
9. git add + commit + push

**常见修复项**:
- `replace_all=true` 替换所有 `datePublished: "2026-XX-XX"` 和 `dateModified` 出现
- 文章正文显示日期（如 `May 3, 2026`）需单独 patch 替换
- 来源列表重复 → 合并去重
- 正文内容重复（同一事实被提及两次）→ 合并段落

**Git 操作（刷新已有文章）**:
```bash
cd ~/.hermes/workspace/chinahospitalsguide
git add blog/article-slug.html blog/index.html sitemap.xml
git commit --message "Refresh article-slug: May 4 update with [news hook]"
git push origin master
```

**sitemap.xml 检查**: 刷新已有文章时，sitemap.xml 中的 `<loc>` 已存在，**不要重复添加**，只需确保 `lastmod` 日期已更新（git push 时自动更新）。
