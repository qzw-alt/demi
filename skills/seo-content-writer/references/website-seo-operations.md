# Website SEO & Indexing Operations

> **Source**: `website-seo-indexing` skill (absorbed into `seo-content-writer`)

## Google Search Console Issues

### "Alternate page with proper canonical" (备用的网页)
- **Not an error** — This is normal; Google correctly handled www/non-www pages
- **No action needed**

### Sitemap has 49 pages but only 8 indexed
- **Cause**: Sitemap just submitted; Google needs days to weeks to crawl all pages
- **Normal behavior**, especially for new sites
- **Solution**:
  1. Manually request core page indexing via Search Console "URL Inspection"
  2. Submit 5-10 per day
  3. Review coverage report after one week

### URL inspection returns 404 but page exists
- May be Google tool temporary glitch or cache issue
- Fix: Wait a few minutes and retry, or use "Test live URL"

### Good ranking but low CTR
- **Cause**: Title/description not compelling enough
- **Optimization strategies**:
  - Add numbers in title (prices, savings)
  - Title includes clear keyword
  - Description has call-to-action (CTA)
  - Matches user search query

### CTR-Boost Meta Audit Workflow (High-Impression / Low-CTR Pages)

Triggered when: GSC shows pages with >300 impressions but CTR <0.5%, or when Google Search impressions suddenly spike (e.g., after sitemap/content improvements) and CTR is disproportionately low.

**Step 1: Parse GSC CSV → identify targets**

```bash
# Extract high-impression / zero-click pages from GSC export
awk -F',' '{if ($3 > 100 && $4 == "0%") print}' search_queries.csv | sort -t',' -k3 -n -r
```

Priority:
1. Pages with **>1,000 impressions** (biggest upside)
2. Pages with **>300 impressions + rank 1-10** (close to converting)
3. Pages where article body **contains concrete prices** (easiest win — put price in title)

**Step 2: Diagnose the meta problem**

For each target page:
- `<title>` — does it have a **specific number, price, or authority signal**?
- `<meta name="description">` — does it answer "why click me vs. the other 9 results"?
- `og:title` — is it identical to `<title>`? (if different, Google may use the less compelling one in rich results)
- Are there **duplicate og:title/og:description tags**? (common bug — found in 35 files in one audit; keep only the `<head>` set, remove the `<body>` copy)

**Step 3: Apply CTR-optimized meta**

| Page type | Title pattern |
|---|---|
| Procedure/cost pages | `"$800–$2,500 vs $3,000–$6,000 in the US"` — China price vs. home country |
| Ranking/list pages | `"Fudan #1 Nationally"`, `"JCI-Accredited"`, `"Top 10"` |
| Hospital directory | `"100+ hospitals"`, `"Filter by specialty"` |

For **all pages**: update `<title>`, `<meta name="description">`, `og:title`, `og:description`, `twitter:title`, `twitter:description` to be consistent. Update `dateModified` in JSON-LD. Update `sitemap.xml` `<lastmod>`.

**Step 4: Batch-fix duplicate og:title (common SEO bug)**

```bash
for f in blog/*.html; do
  count=$(grep -c 'og:title' "$f" 2>/dev/null || echo 0)
  [ "$count" -gt 1 ] && echo "$(basename $f): $count"
done
```

Typical pattern: two sets — one in `<head>`, one in `<body>` before JSON-LD. Keep `<head>` set (social sharing + Google rich cards), remove `<body>` duplicate. When og:title content is identical in both sets, the duplicate causes no functional harm but confuses debugging; still clean it up.

**Step 5: Commit, push, verify**

```bash
git add <changed files>
git commit -m "perf: CTR boost — [pages]"
git push
# Wait 5 min, verify live:
curl -s https://chinahospitalsguide.com/page.html | grep -E "<title>|<meta name=\"description\"" | head -2
```

---

## China Hospitals Guide

| 项目 | 值 |
|------|------|
| 仓库 | `/root/.hermes/workspace/chinahospitalsguide/` |
| Git remote | `origin → https://github.com/qzw-alt/chinahospitalsguide.git` |
| 部署 | GitHub Pages (main branch)，约 5 分钟生效 |
| 核心内容 | 61 blog 文章 + 49 news 文章 + 9 treatments 页面 |
| Sitemap | 144 URLs；提交后 Google 在 2-3 天内逐步索引 |
| 新建页面 | `treatments/endoscopy.html` — 内镜检查完整指南，含 JCI 医院、价格对比、FAQ（2026-05-07） |

### 触发展示爆发的关键改动 (May 2-3, 2026)
- `b3eda15` — sitemap 完整重构 + news/course 全部加 OG/Twitter/JSON-LD（**最关键**）
- `e2e52ad` — 移动端全面优化
- `3af1478` — OG image 290KB→49KB WebP 压缩
- 连续发布深圳/上海新文章 → Google 爬虫频率加快

### CTR 常见问题（已验证）
- 高展示低点击 = meta 不够抓眼球，需要价格锚点
- 重复 og:title/description = 社媒分享歧义，不影响搜索但影响调试
- sitemap lastmod 需与页面 dateModified 同步更新
- **OG 标签两套重复** = 35 个 blog 文件有此问题（批量修复见 Step 4）

### 部署后验证
```bash
curl -s https://chinahospitalsguide.com/page.html | grep -E "<title>|<meta name=\"description\"" | head -2
```

### Git 冲突处理（最佳实践）

当 `git push` 失败 "remote contains work you do not have"：

1. `git fetch origin && git log --oneline HEAD..origin/master` — 先看远程有什么
2. `git reset --hard origin/master` — 丢弃本地 commit（如果本地无未提交改动）
3. 重新应用改动 — 如果本地改动已 commit，先 `git stash`
4. **不要用 rebase** 处理 divergent 分支 — rebase 会产生冲突标记，容易截断文件

> ⚠️ `write_file` 工具如果只给部分内容会**覆盖整个文件**。编辑 HTML 文件永远用 `patch`，不要用 `write_file`。

### Google Search Console 404 修复（Coverage Drilldown）

**发现（May 7, 2026）**：Google 报告 14 个 phantom URL 返回 404，分两类：
- **5个 `/course/xxx`**：旧 Hexo 路径遗留
- **9个内容型 URL**：内链拼写错误 / 指向了不存在的文章

#### 完整 404 列表（2026-05-07 验证）

| 404 URL | 正确目标 | 根因 |
|---------|---------|------|
| `/course/services.html` | `/services.html` | Hexo 遗留 |
| `/course/resources.html` | `/resources.html` | Hexo 遗留 |
| `/course/news/` | `/news/` | Hexo 遗留 |
| `/course/blog/` | `/blog/` | Hexo 遗留 |
| `/course/how-it-works.html` | `/how-it-works.html` | Hexo 遗留 |
| `/blog/why-medical-tourism-coordinator-china.html` | `/contact-new.html` | 文章已删除 |
| `/services/oncology.html` | `/treatments/cancer.html` | 旧路径结构 |
| `/blog/spinal-surgery-cost-china.html` | `/blog/spine-surgery-cost-china.html` | **拼写错误**（spinal→spine）|
| `/blog/china-medical-visa-guide.html` | `/blog/china-medical-visa-guide-2026.html` | 少版本号 |
| `/stories/james-thompson.html` | `/stories/james-wilson.html` | **名字拼错**（thompson→wilson）|
| `/blog/how-to-choose-best-plastic-surgeon.html` | `/blog/plastic-surgery-china.html` | 文章已删除 |
| `/blog/recovery-tips-after-surgery-in-china.html` | `/contact-new.html` | 文章已删除 |
| `/treatments/endoscopy.html` | `/how-it-works.html` | 页面未创建 |
| `/blog.html` | `/blog/` | 少了尾斜杠 |

#### 标准修复流程（双轨修复法）

**原则**：发现 404 → **同时做两件事**：
1. 在 `_redirects` 添加 301 重定向（保底）
2. 在 source 文件里找到并修复指向 404 的内链（治本）

**Step 1: 用 drilldown 数据确认所有 404**

用户提供 GSC Coverage drilldown 表格后，逐个 curl 验证：
```bash
for url in "url1" "url2" ...; do
  code=$(curl -s -o /dev/null -w "%{http_code}" "https://chinahospitalsguide.com$url")
  echo "$code $url"
done
```

**Step 2: 在 source 文件中搜索错误链接**

找到所有指向 404 URL 的 source 文件，修复内链：
```bash
grep -rn "broken-url-piece" --include="*.html" . 2>/dev/null
```

这是**最关键的步骤**。只加 redirect 不修 source → Google 下次爬取同一批内链还是会报 404。

**Step 3: 添加 _redirects（保底）**

在 `_redirects` 文件追加 301 规则：
```
/broken-url    /correct-url    301
```

**Step 4: 验证所有 redirect**

部署后用 curl 验证每个 404 URL 是否返回 301→200：
```bash
curl -s -o /dev/null -w "%{http_code} %{redirect_url}\n" "https://chinahospitalsguide.com/broken-url"
```

**Step 5: 提交推送**

```bash
git add _redirects <fixed source files>
git commit -m "fix(seo): resolve N 404 errors"
git push
```

#### 已验证的 _redirects 格式

GitHub Pages 使用 Netlify `_redirects` 格式（2026-05-07 实测有效）：
- 路径前无斜杠：`/blog/page.html`（不是 `/blog/page.html/`）
- 目标路径可以有尾斜杠：`/blog/` → 正常
- **空格分隔**（不是 tab）

#### 常见根因模式

| 根因 | 例子 | 修复 |
|------|------|------|
| 拼写错误 | spinal→spine, thompson→wilson | grep 搜错误拼写，sed/patch 替换 |
| 缺少版本号 | xxx.html → xxx-2026.html | 搜无版本号路径，替换为最新版本 |
| 缺少尾斜杠 | /blog.html → /blog/ | redirect 加一条 |
| 旧路径结构 | /services/xxx → /treatments/xxx | redirect + 检查导航菜单 |
| 文章被删 | 内链指向不存在页面 | redirect 到 contact 或相关页面 |

**注意**：GitHub Pages `_redirects` 对路径有严格要求（无尾斜杠 vs 有尾斜杠是不同的 URL），部署后用 `curl -s -o /dev/null -w "%{http_code}" https://chinahospitalsguide.com/path` 验证每个 URL。

#### 同时处理 sitemap

404 修复如果涉及新页面创建（如 `treatments/endoscopy.html`），需同步：
1. 在 sitemap.xml 添加条目（`<lastmod>` 同步更新）
2. 在 source 文件添加 OG/Twitter/JSON-LD meta
3. 如果有 sitemap lastmod 更新，其他相关页面的 `<lastmod>` 也一起更新（避免 Google 只爬部分）

---

## Oriental Destiny Project

### 基本信息（已更新 2026-05-02）
| 项目 | 值 |
|------|------|
| 仓库 | `/root/.hermes/workspace/oriental-destiny/` |
| Git remote | `origin → https://github.com/qzw-alt/oriental-destiny.git` |
| 部署 | GitHub Pages (main branch)，约 2 分钟生效 |
| 最新版本 | v1.2.2（AI narrative enhancement layer） |
| 核心产品 | Feng Shui 手链/吊坠 + 八字排盘解读（$99） |

### 漏斗结构
```
Landing → 即时预览（免费，JS计算） → 结果页
                                        ├── 购买 $99 → Checkout（Formspree + PayPal）
                                        └── 未购买 → 邮件捕获（新增 2026-05-02）
```

### 关键文件
| 文件 | 用途 |
|------|------|
| `bazi_engine.js` | 八字计算引擎（本地，无 API） |
| `ai_bazi_layer.js` | AI 叙事增强层（接 DeepSeek） |
| `reading_state.js` | localStorage 状态管理 |
| `instant_reading.html` | 即时预览页（入口） |
| `checkout.html` | 购买页（Formspree endpoint: xwvgznkz） |
| `config.js` | DeepSeek API Key |

### GA4 安装（占位符，2026-05-02）
所有14个 HTML 页面已注入 `G-XXXXXXXXXX` 占位符。
**部署后替换步骤**：在 GitHub 上全局搜索 `G-XXXXXXXXXX` 替换为真实 Measurement ID。

### SEO 内容方向（待执行）
优先方向：**Feng Shui Element Calculator 页面**（工具型，高粘性）
- 目标词：what's my feng shui element / feng shui element calculator
- 竞品少，流量稳定；已有 `kua_calculator.html` 可复用结构
- 做完后再做：birth element + zodiac 内容页

### 邮件捕获（Formspree）
- 即时预览结果页新增邮件订阅模块（2026-05-02 上线）
- Endpoint: `https://formspree.io/f/xwvgznkz`
- 提交字段: email, source, life_focus, birth_date, notes
- 用 `ReadingState.read()` 读取 localStorage 中用户填写的八字信息

### 支付
- PayPal SDK（checkout.html 内嵌 hosted button，button ID: HLSEQWZLQCNVC）
- Formspree 接收订单详情表单（POST 到 xwvgznkz）

### DNS / 托管
- Domain: oriental-destiny.com
- DNS: GoDaddy — www CNAME → qzw-alt.github.io
- GitHub Pages: Settings → Pages → Custom domain → enforce HTTPS
