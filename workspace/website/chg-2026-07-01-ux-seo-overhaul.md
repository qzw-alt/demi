# CHG 2026-07-01 — UX/SEO 全面改版

**会话日期**: 2026-07-01 (Wednesday)
**作者**: Hermes (受德米/伟烨指示)
**目标**: chinahospitalsguide.com 的 90 天改版方案（已执行 7/15 项）

---

## 本次会话完成的所有工作

### 1. cron 提示词改版（TCM 优先级）
- **Job**: `daily-chg-medical-news` (id: `fa7a29b3464e`)
- **改动**:
  - 加 TCM 优先级（每月 ≥10 篇，约 33%）
  - 三大模板：A 中西医结合案例 / B 传统疗法现代化 / C 政策与可及性
  - TCM 关键词库（针灸/艾灸/拔罐/中草药/八段锦等）
- **明天 9:00** 自动按新规则发首篇

### 2. 11 个新 Pillar 页面（TCM 集成 + China 独有疗法）
- **聚合页**: `china-unique-medical-procedures-guide.html`（5,221 字）
- **10 个子页**:
  - integrated-chinese-western-medicine-china.html
  - autonomous-robotic-surgery-china.html
  - solid-tumor-car-t-china.html
  - microsurgery-replantation-china.html
  - organ-transplant-china-cost-access.html
  - 3d-printed-implants-china.html
  - hepatobiliary-surgery-china-wu-mengchao.html
  - stem-cell-therapy-china-access.html
  - crispr-gene-therapy-china-clinical-trials.html
  - ophthalmology-china-volume-expertise.html

### 3. 49 篇现有 Blog 注入 TCM 段
- 病种 × TCM 12 个模板（cancer/orthopedic/IVF/eye/dental/cardio/neuro/wellness/cosmetic/kidney/transplant）
- 49 篇病种博客精准注入 TCM 段，每段 +200 字 + 2-3 个内链
- 排除 47 篇非病种文（医院排名/城市/签证等无需 TCM 段）

### 4. 修复 china-unique-medical-procedures.html 重复页（SEO 灾难）
- 发现 `24e927c` 已建 `china-unique-medical-procedures-guide.html`（与我的同名重复）
- 保留 `-guide.html`（已被 blog 索引 + news 引用）
- 删除我建的 `china-unique-medical-procedures.html`
- 加 301 重定向
- 验证：3 个文件引用，全部指向保留版

### 5. Blog 索引页大改版
- **修关键 bug**: `blog-grid` div 缺 `id="blog-grid"`，导致 14 个分类 filter 按钮**全部失效**（用户点 filter 无反应）
- **加 3 个新分区**（在 "Latest Articles" 之前）:
  - Featured Pillar Pages（4 个核心 pillar 入口，深蓝渐变）
  - Browse by What Makes China Different（3 大类 12 个内链：TCM/Frontier/Volume）
- filter bug 修复后所有分类按钮可用
- 详情：`blog/index.html` +7,672 字符

### 6. 首页改版
- **首页加 Featured Articles section**（"What Only China Can Do"）—— 5+1 卡片网格
- **首页加 Trust Section**（"Trusted by Patients Worldwide"）—— 4 个数据卡 + 6 个权威源
- **首页加 Newsletter 订阅**（蓝色渐变 + Formspree 表单）
- 详情：`index.html` +13,000+ 字符

### 7. Blog 索引页 Newsletter
- 在 "Latest Articles" grid 之后加 Newsletter 订阅（同首页表单，紧凑版）
- 详情：`blog/index.html` +1,596 字符

### 8. 医院排名页 P0 改造（最高 ROI）
- **目标页**: `best-hospitals-china-international-patients.html`（"best hospital China" 最高搜索量）
- **改动**:
  - "Quick Decision" 决策树（8 个专科，每专科给具体医院 + 费用 + 内链）
  - "Quick Answers" Featured Snippet 优化（5 条 Q&A 格式 `X is Y`）
  - MedicalWebPage schema + BreadcrumbList JSON-LD
  - 保留原 Article + FAQPage schema 不动
- 详情：+12,393 字符

### 9. 部署（git 推送 7 个 commit）
- `41bf79c` → TCM integration: 11 new pillar pages
- `a5b7026` → 推送到 GitHub
- `56f6a55` → SEO: remove duplicate pillar page
- `40ffd0e` → UX: blog index page overhaul + homepage Featured Articles
- `c5b2a34` → SEO: hospital ranking page overhaul
- `f837893` → Conversion: trust section + newsletter subscription

---

## 部署 + 验证全部通过 ✅

所有改动在 Cloudflare 部署成功（每 commit 后等 60s 验证）：
- 首页 200
- Blog 索引 200
- 11 个 pillar 页 200
- 医院排名页 200
- 所有验证点（关键文案/schema）100% 出现

---

## ⚠️ 伟烨必须做的一步

**Newsletter 表单需要填 Formspree endpoint 才能工作**。

未填的 placeholder: `REPLACE_WITH_YOUR_FORMSPREE_ID`

替换位置（2 处）:
1. `index.html`（首页 newsletter 表单 action）
2. `blog/index.html`（blog 索引 newsletter 表单 action）

### 操作步骤（5 分钟）
1. 注册 https://formspree.io（免费档每月 50 提交）
2. 创建新 form，设转发邮箱为伟烨的收件邮箱
3. 拿到 endpoint（格式 `https://formspree.io/f/xyzabcde`）
4. 全局替换 `REPLACE_WITH_YOUR_FORMSPREE_ID` → `xyzabcde`
5. 提交 commit + push

### 备选方案
如果不想用 Formspree，告诉我用：
- **Mailchimp**（强大，需 API key）
- **Buttondown**（极简，付费档好用）
- **Google Forms**（零配置，UI 差但能用）
- **Substack**（写作型平台）

---

## 90 天方案剩余项（按优先级）

### P0（全部完成）✅

### P1 — 数据驱动
- [ ] **GSC 周报 cron**（1h）—— 让我开始看数据
- [ ] **MS Clarity 热力图**（0.5h）—— 立刻装，能看到用户在哪些页跳出
- [ ] **GA4 事件补全**（2h）—— 滚动深度、CTA 点击、文章完成度

### P1 — 转化导向
- [ ] **同样的改造套到其他排名页**（2-3h）
  - `best-cancer-hospitals-china-2026.html`
  - `china-orthopedic-hospital-rankings-2026.html`
  - `best-cardiac-surgery-hospitals-china-2026.html`
  - `china-hospital-rankings-2026.html`（Fudan Top 100）
- [ ] **患者故事扩到 8 篇**（持续，月 2-3 篇）
  - 现有 3 篇：Ahmed/David/Margaret
  - 建议加：HIV/罕见病/儿童肿瘤/年轻女性 IVF/老年慢性病
- [ ] **决策指南矩阵**（持续）—— "X 病去中国"长尾页

### P1 — 技术债
- [ ] **news 索引页改版**（2h）—— 参考 blog 改版思路
- [ ] **全站加 MedicalProcedure/Hospital schema**（4h）—— 50+ 篇文章

### P2 — 长期（流量起来再做）
- [ ] Compare Tool 交互式（vs 泰印新，8h+）
- [ ] A/B 测试框架（4h）
- [ ] YouTube transcript 转录 + 嵌入（2h/篇）
- [ ] 多语言（俄/阿/西，不做直到 5K/月）
- [ ] Affiliate（Booking/Trip/保险，1h）
- [ ] B2B 服务（医院网络年费，1h）
- [ ] 季度内容审计 cron（2h）

---

## 重要文件路径（明天续作时直接打开）

| 文件 | 用途 |
|---|---|
| `/home/ubuntu/.hermes/workspace/website/blog/index.html` | Blog 索引页（含 3 个新分区 + filter 修复） |
| `/home/ubuntu/.hermes/workspace/website/index.html` | 首页（含 Featured Articles + Trust + Newsletter） |
| `/home/ubuntu/.hermes/workspace/website/blog/best-hospitals-china-international-patients.html` | 医院排名 P0 改造页（决策树 + Quick Answers） |
| `/home/ubuntu/.hermes/workspace/website/blog/china-unique-medical-procedures-guide.html` | 10 unique procedures 聚合页 |
| `/home/ubuntu/.hermes/workspace/website/_redirects` | 301 重定向规则 |
| `/home/ubuntu/.hermes/workspace/website/sitemap.xml` | 233 个 URL（已加 11 个新文章） |
| `/home/ubuntu/.hermes/memories/MEMORY.md` | 跨会话记忆 |
| `/home/ubuntu/.hermes/skills/research/content-research-writer-cn/SKILL.md` | news cron 用的技能 |

---

## git 状态

```
master 分支: clean（所有 commit 已 push）
最近 commit: f837893 (Conversion: trust section + newsletter subscription on home + blog index)
```

---

## 明天继续时建议的第一句话

> "按 `chg-2026-07-01-ux-seo-overhaul.md` 继续。"

我会读取本文件，定位剩余待办，按你之前的偏好（"行按这个执行"=完全授权）继续。

---

## 关键决策记录

1. **Newsletter 方案**: Formspree（最快上线、零维护）—— 但需要伟烨注册
2. **信任区设计**: 不用真 logo（避免版权），用 "Coverage & References" 通用标签
3. **Hospital ranking P0 改造**: 决策树 + Quick Answers 双前移，schema 加 MedicalWebPage + BreadcrumbList
4. **重复页处理**: 保留 24e927c 的 -guide.html（先到先得），删 41bf79c 重名版，加 301
5. **TCM 注入策略**: 病种 × TCM 12 个模板，只注入 49 篇病种博客（不污染医院/城市/签证类）

---

*记录人: Hermes*
*最后更新: 2026-07-01*
