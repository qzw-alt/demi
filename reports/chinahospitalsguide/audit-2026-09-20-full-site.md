# chinahospitalsguide.com 全站审计报告

**审计日期** 2026-09-20 ｜ **审计对象** https://chinahospitalsguide.com （310 URL 全量） ｜ **仓库基线** origin/master `3959812` (2026-09-19)
**上次审计** 2026-07-22（273 URL）｜ **基线快照** `~/.hermes/tmp/audit/audit-report-2026-07-22-baseline.md`

---

## 一句话结论

结构层面已相当干净（310 页 0 死链 / 0 断链 / schema 覆盖 100%），真正的问题集中在三处：
**JSON-LD 语法损坏（8 页线上整块失效）、内链孤岛（4 个中文页 0 内链）、一批内部痕迹泄漏到线上。**
内容质量整体在变好（HEALTHY +45），但新建页面仍在拉低均值。

---

## 一、数字总览（与 07-22 基线对照）

| 类别 | 07-22 | 09-20 | 方向 |
|---|---|---|---|
| HEALTHY | 226 | **271** | ↑ +45 |
| NO_SCHEMA | 17 | **0** | ✅ -17 |
| THIN (<400 词) | 22 | 36 | ⚠️ +14 |
| TOO_SHORT (<150 词) | 8 | 3 | ✅ -5 |
| BROKEN | 0 | **0** | = |
| **总 URL** | 273 | **310** | +37 |

- 平均正文 **1261 词**；≥1500 词 **103 页**，≥800 词 **165 页**
- 内部链接 **17830 条 / 549 页 / 0 死链**（build 期 `audit-links.js` + 独立线上扫描双验证）
- 310/310 页加载 GA4 与 `/ga4-events.js`；310/310 有 canonical
- Schema 类型分布：BreadcrumbList 176、Article 163、FAQPage 160、MedicalBusiness 166、Hospital 330、MedicalCondition 23

**上次遗留的 NO_SCHEMA 17 页已全部清零，BROKEN 保持 0 —— 这两项确实修好了。**

---

## 二、P0（必须修）

### P0-1　10 个模板的 `schema:` 是相邻两个 JSON 对象，8 页线上 schema 整块失效

`<script type="application/ld+json">` 内塞入 `{...}{...}` 两个相邻对象，`JSON.parse` 抛 `Extra data`，
**Google 会整块丢弃该页所有结构化数据**（不是丢一半，是全丢）。

线上实测解析失败（8 页）：

| 页面 | 报错位置 |
|---|---|
| `/apps-guide.html` | Extra data @L9C1 |
| `/contact-new.html` | Extra data @L15C1 |
| `/contact.html` | Extra data @L15C1 |
| `/insurance-guide.html` | Extra data @L9C1 |
| `/medical-imaging.html` | Extra data @L11C1 |
| `/payment-guide.html` | Extra data @L9C1 |
| `/services.html` | Extra data @L15C1 |
| `/visa-guide.html` | Extra data @L11C1 |

源码模板全量扫描（10 个损坏，含 2 个线上表现不同）：

```
about.njk          how-it-works.njk      apps-guide.njk      contact-new.njk
contact.njk        insurance-guide.njk   medical-imaging.njk payment-guide.njk
services.njk       visa-guide.njk
```

根因链路：模板 frontmatter `schema: |` 里写了多个对象 → `_includes/head.njk` 用一个 `<script>` 原样输出 → 非法。

**建议修法**：frontmatter 改成 JSON 数组 `[ {...}, {...} ]`，脚本块内第一个非空字符必须是 `[`。
修完可一次拿回 Article / ContactPage / MedicalWebPage / FAQPage / OfferCatalog 五类富结果资格。

### P0-2　`patients/` 未进 .gitignore —— 真实患者病历可被 push 公开

本地已复现：`npm run build` 会把
`patients/elspeth-ruzic-hunt/2026-09-12/*.md`（含姓名、出生日期、病历摘要）编译进 `_site/`。

线上当前为 **404**（origin 上没有该目录），**所以此刻没有泄露**；
但只要 commit + push 一次就会公开。同类的 `drafts/` 已停止发布（0 tracked），`patients/` 漏了。

**建议**：`.gitignore` 加 `patients/`，并给构建加一条跳过规则（当前无 `.eleventyignore`）。

### P0-3　9 个页面 0 内链（孤岛）

在 sitemap 中，但全站 549 个构建产物里**没有任何一个 `<a>` 指向它们**（已 grep 全量验证）：

```
/zh/hospital-rankings-2026.html
/zh/eye-hospital-rankings-2026.html
/zh/liposuction-hospital-rankings-2026.html
/zh/orthopedic-hospital-rankings-2026.html
/blog/fuzhou-orthopedic-hospital-ranking.html
/hair-transplant-china-vs-turkey.html
/plastic-surgery-china-vs-korea.html
/patient-story-program.html
/real-stories.html
```

`/real-stories.html` 更严重：**45 词、无 h1、无 description、无 robots meta、无 og**，
只是跳往 `/stories/` 的空壳，而 `/stories/` 自身缺 canonical，两者标题完全相同（全站唯一重复标题组）。

**建议**：中文 4 页挂到中文 hub；`/real-stories.html` 直接 301 → `/stories/`。

---

## 三、P1（信任与转化受损）

### P1-4　`/resources.html` 存在 5 个明确死链

| 状态 | URL |
|---|---|
| 404 | `http://www.gov.cn/zhengce/foreign.htm`（"Immigration News"） |
| 404 | `https://www.who.int/health-topics/health-tourism`（"WHO Health Tourism Info"） |
| 域名无效 | `https://www.care兄.com` ← 中文字符混入域名，占位符未清理（"Insurance Guide"） |
| 404 | `https://www.scmp.com/news/china/science/article/3300000/...`（`/blog/2026-08-11-china-brain-computer-interface-vein-implant-stairmed/`） |
| 405 | `https://www.digitaltrends.com/cool-tech/chinese-startup-claims-its-brain-implant-takes-just-10-minutes-to-place-no-skull-surgery-required/`（同篇） |

`/resources.html` 是信任背书页，挂 404 的权威外链最伤可信度。
403/412 类（nhc.gov.cn、nmpa.gov.cn、jointcommissioninternational.org、OECD、IATA）疑似反爬 WAF，
**未计入死链**，建议在中国境内复核一次。

### P1-5　约 25 个中国医院官网外链海外不可达

`www.301hospital.com.cn`、`www.pkuph.com.cn`、`www.fuwaihospital.org`、`www.longhua-hospital.com`、
`www.rjh.com.cn` 等 25 个域名 URLError / Timeout / ConnectionReset。
目标用户（海外患者）点进去必然打不开。

**建议**：医院详情页改为"官网仅限中国境内访问，如需联系请走对接通道"，反而提升转化。

### P1-6　`/panel.html` 线上可访问（内部工作面板）

标题「德米工作面板」，HTTP 200，虽带 noindex 但任何人输网址可见内部工作流：
技能名、模型（Kimi K2.5）、技能数、tavily / xhs / lead-research 等内部流程。
**建议**：删除或加访问控制。

### P1-7　`/patient-story-program.html` 残留临时邮箱

页面出现 `motionlessbottle950@agentmail.to`（AI 代理占位邮箱），应替换为
`contact@chinahospitalsguide.com`。该页同时缺 canonical。

### P1-8　MS Clarity 只覆盖 1 个页面

实测仅 `/blog/` 含 clarity 代码。skill 记录 2026-07-02 已 site-wide 部署 —— 该链路基本失效。
（对照：GA4 覆盖 310/310，这条是好的。）
如果你还在看 Clarity 热图，看到的是不完整数据。

### P1-9　定价档位与首单不一致（业务侧）

线上 PayPal item id 实际仅 4 个：`acceptance-check`、`full-journey`、`full-journey-upgrade`、`mdt-review`，
分布在 `/pricing.html` `/ar-pricing.html` `/id-pricing.html` `/ru-pricing.html` `/mdt-review.html`。

但 **2026-09-12 首单（Elspeth Ruzic-Hunt）收的是 $149 L2 咨询档，现页面已无该档位**（现为 $199/$499/$649 + $450 upgrade）。
若继续卖 $149 则无入口；若停卖，需确认存量客户的升级路径。

---

## 四、P2（可修，影响效率）

10. **robots.txt `Disallow` 与页面 `noindex` 撞车**：`/api/`、`/blog-articles/`、`/news/` 既被 Disallow 又带 noindex。爬虫不抓就看不到 noindex → 永远停在"已排除但未确认"。二者只能取一。另 `/api/`（API Explorer，11320 字节、无 canonical）标了 `index, follow`，自相矛盾。
11. **sitemap 310 条 lastmod 全部为 `2026-09-19`**（每次构建刷新全站），lastmod 信号被稀释。应取各文件最后真实修改时间。
12. **og:image 缺 28 页 / twitter:card 缺 35 页 / og:title 缺 5 页**：社交与 AI 摘录无配图。缺 og:title 的 5 页：`/blog/fuzhou-orthopedic-hospital-ranking.html`、`/blog/ivf-china-2026-complete-guide.html`、`/patient-story-program.html`、`/real-stories.html`、`/stories/`。
13. **标题 / 描述超长**：282/310 标题 >60 字符（最长 132）；183/310 描述 >160 字符（最长 369）。医院页标题模板化到 114–124 字符。
14. **构建警告**：`images/hospitals/shenzhen-city.jpg` 文件损坏（sharp 无法解析）；3 页 minify 解析失败被跳过：`blog/hospitals-in-shenzhen-for-international-patients.html`、`blog/lasik-smile-surgery-china.html`、`blog/spine-surgery-cost-china.html`。
15. **URL slug 泄漏客户姓名**：`/MARIA-RIOS-PIPELINE-CHECKLIST/`、`/draft-inquiry-tangdu-maria-rios/` 等返回 200（noindex 跳转壳、不在 sitemap、内容未泄露），但目录名本身含客户姓名。建议改无语义 slug 或 410。

---

## 五、明确确认「没问题」的部分（无需复查）

- **重定向层是有意设计，非缺陷**：`/news/`（105 页）、`/blog-articles/`（33 页）均 noindex + canonical → `/blog/`，robots.txt 亦 Disallow。属兼容层。
- **医院页发现路径已修复**：`/hospitals.html` 现有 57 个 build-time 静态 `<a href="/hospitals/xxx/">`，解决"Google 只能靠 sitemap 发现医院页"的老问题。
- **分页正常**：`/blog/2/`、`/blog/3/` 均 `index, follow` + canonical 自指。
- **资源健康**：13 个 `<img>`，0 缺 alt，11 个 lazy；图片 src 全部 200；最大页 75 KB，中位 28 KB。
- **0 个 sitemap URL 发生跳转**（无 301/302 链）。
- **日更 cron 已按预期删除**：当前仅 1 个 job（备份，已 paused）。

### 已核实并排除的假警报

| 假警报 | 核实结果 |
|---|---|
| grep 看到 `"@context": "https://***@type"` | 终端显示层脱敏。实际 HTML 中 `https://schema.org` 出现 3 次、`https://***@` 0 次。**非真实损坏** |
| "GA4 事件追踪全部丢失" | 错。按页面 HTML 搜索确实为 0，但事件代码在外部文件 `/ga4-events.js`，308 页加载，scroll_depth / cta_click / outbound_click / newsletter_submit / paypal_sdk_loaded 全部在位 |
| `about.njk` / `how-it-works.njk` 线上 schema 有效 | 这两个模板同样损坏（3 个顶层对象），线上有效 block 是构建期其它注入器补的；frontmatter 里的 Article 等 schema **已被静默丢弃**，需一并修 |

---

## 六、方法层面的两个缺口（必须说明）

1. **GSC 授权已失效**：`~/.hermes/bin/gsc` 报 `RefreshError: invalid_grant: Bad Request`。
   因此 **7–9 月的真实搜索表现（曝光 / 点击 / 排名）本报告不包含**。
   本报告是「技术 SEO + 内容 + 转化架构」审计，**不含流量数据层**。
   补这一层需重走 OAuth（`medical-tourism-site-ops` skill 内 `templates/gsc-authorize.py`）。
2. **本地工作区曾落后 origin 76 个 commit**，审计前已 `git pull` 至 `3959812`。
   2026-08-16 的未完成工作（solid-tumor-car-t 升级 `.md` + 2 篇未跟踪文章）**未改动**，
   仅 stash 为：`local WIP 2026-08-16 solid-tumor-car-t .md upgrade (pre-audit)`。

---

## 七、待决策事项

1. **P0-1 JSON-LD 修复**是否立即执行？（10 个模板改数组，约 15 分钟 + 构建验证）
2. **P0-2 `patients/` gitignore** 是否现在加？（纯隐私防护，无业务改动）
3. **P0-3 中文 4 个孤岛页**：挂中文 hub，还是合并进 `/zh/hospital-rankings-2026.html`？

---

## 附录：复现命令与数据文件

审计脚本（全部只读，未修改任何线上文件）：

```
~/.hermes/tmp/audit/
├── sitemap-live.xml / sitemap-urls.json      # 310 URL 清单
├── site_audit.py     → audit-2026-09-20-raw.json          # 全站逐页抓取
├── analyze.py        → audit-2026-09-20-summary.json      # 分类 / 重复 / 孤儿 / schema
├── check_links.py    → audit-2026-09-20-links.json        # 内链死链验证
├── deepdive.py                                        # 8 个缺陷域的深挖
├── conversion_audit.py                                # GA4 / PayPal / 表单 / WhatsApp
├── ext_assets_audit.py → outbound-status.json         # 站外链接 + 资源 + 页面体积
└── audit-report-2026-07-22-baseline.md                # 冻结基线（勿覆盖）
```

关键验证命令：

```bash
# 构建复验（含全站内链门禁）
cd /home/ubuntu/chinahospitalsguide && npm run build
# → audit-links: 17830 internal links across 549 pages, 0 dead.   EXIT=0

# 线上 JSON-LD 有效性（逐 block）
python3 -c "
import re,json,urllib.request
h=urllib.request.urlopen('https://chinahospitalsguide.com/apps-guide.html').read().decode()
for b in re.findall(r'<script[^>]*application/ld\+json[^>]*>(.*?)</script>', h, re.S):
    try: json.loads(b.strip()); print('OK')
    except Exception as e: print('INVALID', e)
"

# 中文孤岛验证（应为 0 条）
cd _site && grep -roE '<a[^>]*href="(/zh/[^"]*)"' --include=*.html . | wc -l
```

---

*报告生成：Hermes / 德米 ｜ 2026-09-20 ｜ 数据可复现，未修改任何线上文件*
