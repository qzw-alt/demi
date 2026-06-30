---
name: hospital-customer-report
description: "Generate customer-facing medical tourism hospital report packages (Y49 basic / Y399 premium) from the chinahospitalsguide.com directory data. Single unified `scripts/generate-report.js` with 3 modes (quick match, basic, premium). Auto-matches hospitals from keywords, shows CN vs US pricing, generates beautiful HTML page with cover letter, action guide, service flow, and TXT download."
version: 2.0.0
author: agent
tags: [medical-tourism, chinahospitalsguide, customer-report, hospital-directory, premium-report]
---

# Hospital Customer Report Generation

> ⚠️ NOTE: An overlapping skill exists at `web-development/hospital-directory-report` (v1.0.0). This skill (v2.0.0) is the authoritative, more current version. The older skill should be consolidated into this one.

Generate customer-facing hospital report packages from the chinahospitalsguide.com directory data.

## Two-Tier Product Structure

### ¥49 基础版 (Basic Edition)

**定位:** "信息+温度" — 给你精准推荐和出行提示，你自己来
**交付:** 与¥399相同的2-3家医院推荐。区别在于：¥49 = 信息（你自己联系医院、自己安排），¥399 = 服务（我们全程帮你搞定）。
**客户心理:** "知道去哪了，但自己联系医院有点怵" → 升级到¥399让专业的人做专业的事
**模板文件:** `hospital-directory-basic-49.md`（已在 repo root — 用于内容结构参考）

**¥49 基础版报告结构（2026-06-28 重写 — 匹配模板）:**
```
├── 🌿 一封写给你的信（中文版，共情开场）
├── 📖 如何使用这份报告（5步表格）
├── 💰 费用对比（中/美，中文标签）
├── 🏆 推荐医院（2-3家）
│   ├── 🥇 首选推荐 / 🥈 备选推荐 / 🥉 第三选择
│   ├── 💬 一句话性格（引号版）
│   ├── 📊 完整信息表（排名/地址/电话/网站/国际部/机场交通）
│   └── 💰 费用参考（中国 vs 美国）
├── ✈️ 城市交通指南（按城市动态生成，覆盖10个城市）
├── 📋 行前准备清单（必备材料分类清单）
├── ⭐ 升级服务提示（5阶段服务对比表）
│   「以下服务均属于Pre-Arrival Coordination ($399)，基础版不包含」
├── ❓ 常见问题（中文6QA，含升级路径说明）
└── 📥 下载完整报告按钮
    📋 重要提示 / 📧 页脚
```

**关键设计：** 两个版本用同一份医院推荐。¥49客户拿到后自己行动；如果觉得"还是不知道怎么开始"，自然升级到¥399。基础版费用可抵扣升级。

### ¥399 升级版 (Premium Edition)

**定位:** "专属就诊顾问" — 客户买的不是数据，是安心感
**交付:** 完整报告（致客户信 + 医院深度画像 + 服务流程 + FAQ）

**¥399 升级版报告结构（2026-06-28 重写 — 匹配模板）:**
```
├── 🌿 一封写给你的信（中文版，共情开场）
├── 📖 如何使用这份报告（5步表格）
├── 💰 费用对比（中/美，中文标签）
├── 🏆 推荐医院（2-3家，同¥49基础的相同卡片）
├── ✈️ 城市交通指南（按城市动态生成）
├── 📋 行前准备清单（必备材料分类清单）
├── 🚀 我们的服务流程（6步全流程）
│   ├── 💳 费用说明：✅ ¥399已包含 / 💰 需额外付费
│   ├── 第1步：需求确认（1-2天）
│   ├── 第2步：医院对接（3-7天）
│   ├── 第3步：行前准备（1-4周）
│   ├── 第4步：抵达中国（治疗期间）
│   ├── 第5步：出院与回国
│   └── 第6步：回国后跟进
├── ❓ 常见问题（中文6QA）
├── 📥 下载完整报告按钮
    📋 重要提示 / 📧 页脚
```

**差异点：** ¥49有"⭐ 升级服务"提示无"🚀 服务流程"；¥399有"🚀 服务流程"无"⭐ 升级服务提示"。

### 一句话性格（per hospital）

为每家医院写一句有温度的个人化描述，格式：`💬 *"话——话"*`

| 医院 | 示例 |
|------|------|
| 阜外医院 | 中国心脏手术的"最高法院"——别的医院搞不定的心脏病例，最后都转到这里 |
| 协和医院 | 中国医学的"百年圣殿"——协和出手，全国没有不敢接的病 |
| 华西医院 | 中国西部医疗的"定海神针"——全国综合排名第2，什么病在华西都有解 |
| 唐都医院 | 军队医院出身能打硬仗——胸外科全军第一，胡桃夹综合征3D支架全国独家 |
| 复旦大学附属肿瘤医院 | 中国抗癌的"国家队"——国家级癌症中心，治疗方案最权威 |

## Human-Touch Design Principles

### 核心原则

1. **开场先共情** — 不是"这里是医院名单"，而是"我们知道你现在最担心什么"
2. **给医院一个性格** — 每家医院一句话讲出气质，而不是只有排名和地址
3. **回答真实问题** — 客户真正担心的不是排名，而是"到了机场有人接我吗"
4. **实话实说** — 强在哪、弱在哪都说清楚，不说假话

### 致客户信模板

```markdown
你好，

我们知道，你读到这份资料的时候，心里可能已经装了很多问题。不是"排名第几"的那种问题，而是更真实的：

- "我去了中国，真的有人接我吗？"
- "医生能跟我直接沟通吗？"
- "如果出了问题，谁帮我协调？"
- "在一个陌生的国家住院几周，我应付得来吗？"

这些问题，才是医疗旅游中最真实、也最容易被忽略的部分。

这份资料库不只是51家医院的名单和电话——它是我们想让你感觉到：**有人在路的另一端等着你，知道你的名字，了解你的情况，会把你的事情当一回事。**

如果读完还有任何担心的问题——哪怕是很小的——都欢迎随时联系我们。祝你早日康复。

—— China Hospitals Guide 团队
```

### ⚠️ 用户纠正记录（必须遵守）

这些是用户在审核时明确纠正过的点，做报告时直接遵循，不需要再问：

1. **不要出现"排队"或"等待时间可能更长"等表述** — 国际患者在中国医院通过国际部预约就诊，不走普通门诊排队流程。用"北京的生活成本和住宿费用高于西安"这类表述替代。

2. **不要写"中文现场支持"** — 大型医院国际部本身配备双语协调员，不需要我方提供中文翻译。国际部能直接以外语沟通。我方不提供现场翻译/协调服务。

3. **行前清单必须写具体** — 不能只写"告诉你带什么"，要展开为完整分类：
   - **医疗类（必须带）：** ① 全部原始病历 + 影像资料（CT/MRI光盘或U盘，DICOM格式最佳）② 正在服用的药物（带足治疗期间用量 + 原厂包装 + 英文说明书）③ 过敏史清单（药物/食物过敏，中英文）④ 既往手术记录（如有）⑤ 疫苗接种记录（如有）
   - **证件类（必须带）：** ① 护照（有效期6个月以上）② 医院邀请函（用于入境和签证）③ 旅行保险单（如有）
   - **生活类（建议带）：** ① 个人常用物品（牙刷、拖鞋等，酒店也有提供）② 信用卡（Visa/Mastercard）+ 少量人民币现金 ③ 📱 **抵达中国机场出关后，建议购买一张中国电话卡（约¥100）**——有本地号码后，注册微信、叫车、叫外卖、联系医院都方便很多 ④ 常用App建议提前下载：微信（中国必备）、翻译软件、百度/高德地图 ⑤ 转换插头（中国标准：两脚扁型，220V）
   - **不要带：** ① 大量现金（中国已基本实现全电子支付，**强烈建议出发前下载支付宝App，绑定你的国际信用卡**——到了中国后，从便利店到药店到餐厅都可以扫支付宝，比现金方便百倍。医院和大部分商店也接受刷卡）② 新鲜水果/肉类/种子（中国海关严格限制入境）③ 含有麻醉成分的药物（需提前申报）④ 贵重首饰

### Premium医院深度画像模板

对于报告中重点推荐的医院（通常3家），每家写以下3个板块：

**板块1 — 人的温度**
- 一句话性格
- 国际部是谁接你（双语协调员、预约方式）
- 费用参考（分项目列明）

**板块2 — 决策数据**
- 关键指标速览卡
- 实话实说：推荐的理由 + 不建议直接选的理由

**板块3 — 生活指南**
- 机场交通
- 附近住宿
- 饮食/文化贴士

## Pricing Clarity (CRITICAL — user requirement)

Every service item in the premium report MUST be tagged with a clear pricing label:

| Tag | Meaning |
|-----|---------|
| ✅ **¥399已包含** | Included in the ¥399 premium package — no extra charge |
| 💰 **需额外付费** | Value-added service — charged at actual cost or agreed rate |

Use a legend table at the start of the service flow section in every premium report.

### Included vs Extra: Complete Mapping

| Step | ¥399 Included | Extra Fee |
|------|--------------|-----------|
| **Step 1: Needs assessment** | ✅ 1-on-1 consultation, precise matching (51→3 hospitals), custom adjustments | — |
| **Step 2: Hospital contact** | ✅ Record submission (translated + sent), follow-up (3-7 day response), translation coordination, multi-hospital comparison | — |
| **Step 3: Pre-departure** | ✅ Visa document guidance, appointment lock, accommodation tips, packing checklist, **airport pickup coordination** | — |
| **Step 4: During treatment** | ✅ Hospital liaison communication, emergency coordination, 7x24 hotline | 💰 Family life assistance (per-service fee) |
| **Step 5: Discharge & return** | ✅ Medical records (Chinese + English), medication instructions, follow-up handover, post-discharge checkup booking | 💰 Return travel assistance (actual cost) |
| **Step 6: Post-return** | — | 💰 Remote follow-up + health archive (annual or per-visit subscription) |

### FAQ — Pricing Template

Include this in the premium report FAQ:

```markdown
### Q: ¥399包含什么？额外费用有哪些？

**¥399包含**以下完整就诊协调服务：
| 阶段 | 已包含服务 |
|------|-----------|
| 需求确认 | 一对一顾问对接、精准匹配、定制调整 |
| 医院对接 | 代发病历、翻译协调、跟进回复、多院对比 |
| 行前准备 | 签证材料指导、医院预约锁定、住宿建议、行前清单 |
| 治疗期间 | 医院沟通衔接、突发问题协调、紧急联系电话 |
| 出院回国 | 中英文病历整理、用药说明、复查预约、远程随访衔接 |

**需额外付费的服务：**\n| 服务项目 | 计费方式 |\n|---------|---------|\n| 家属生活协助 | 按实际服务收费 |\n| 回国航旅协助 | 按实际费用结算 |\n| 回国后远程随访（含健康档案） | 按年或按次，详情咨询 |

**费用流向说明：**
- ¥399 —— 付给我们（就诊协调服务费）
- 医院治疗费用 —— 直接付给医院，不经我们手
```

## 服务流程（6步模型 — 含定价标注）

客户购买¥399升级版后，服务的完整流程。每项服务已标注价格归属：

### 第1步：需求确认（1-2天）
- ✅ **一对一顾问对接**——了解你的具体情况（¥399已包含）
- ✅ **精准匹配**——从51家医院中筛选最适合你的2-3家（¥399已包含）
- ✅ **定制化调整**——如果你对推荐不满意，重新匹配（¥399已包含）

### 第2步：医院对接（3-7天）
- ✅ **代发病历**——将你的病历翻译整理后，发送给医院国际部（¥399已包含）
- ✅ **跟进回复**——跟踪医院评估进度（¥399已包含）
- ✅ **翻译协调**——协助中英文病历翻译（¥399已包含）
- ✅ **多院对比**——同时对接多家，拿到评估结果和报价（¥399已包含）

### 第3步：行前准备（1-4周）
- ✅ **医疗签证协助**——协调医院出具正式邀请函，指导准备签证材料（¥399已包含）
- ✅ **医院预约锁定**——确认具体入院日期（¥399已包含）
- ✅ **住宿建议**——根据位置、预算和需求推荐住宿（¥399已包含）
- ✅ **行前清单**——包含医疗类/证件类/生活类分类清单（¥399已包含）
- ✅ **接机安排**——协调医院或我们安排接机（¥399已包含）

### 第4步：抵达治疗期间
- ✅ **医院沟通衔接**——与医院国际部保持沟通（¥399已包含）
- ✅ **突发协调**——治疗中出现任何问题，我们帮你沟通（¥399已包含）
- 💰 **家属协助**——陪同家属生活问题（需额外付费）

### 第5步：出院回国
- ✅ **病历整理**——中英文双语病历摘要（¥399已包含）
- ✅ **用药说明**——协助翻译出院带药使用说明（¥399已包含）
- ✅ **复查安排**——协助预约（¥399已包含）
- ✅ **远程随访衔接**——确认回国后联系渠道（¥399已包含）
- 💰 **回国航旅协助**——安排回国行程（需额外付费）

### 第6步：回国后跟进（长期）
- 💰 **远程随访通道**——通过微信/邮件与主治医生保持联系（需额外付费）
- 💰 **复查资料传递**——将国内复查报告传给主治医生（含在远程随访中）
- 💰 **长期健康档案**——病历和治疗记录归档保存（含在远程随访中）
```

## Implementation (Legacy — Historical Reference)

Previous report generation used these approaches (now superseded by `scripts/generate-report.js`):

### Data source
- Primary: `/home/ubuntu/chinahospitalsguide/api/v1/hospitals.json` (51 hospitals, used for the legacy markdown templates)
- Current: `data/hospital-directory-51.csv` (used by the unified script)

### File output
- Old: `hospital-directory-basic-49.md` / `hospital-directory-premium-399.md` — legacy markdown templates
- Current: `reports/report-{name}-{timestamp}.html` (via scripts/generate-report.js)

### Generation approach (Legacy)
- Old: Python scripts read JSON and output formatted markdown
- Current: Node.js script reads CSV and outputs standalone HTML with auto-matching

## Report Delivery — Unified Report Generator

**Single tool, 3 modes.** Replaces both the old `generate-report-auto.js` (automated matcher, now deleted) and the old separate `generate-report.js` (manual humanizer, now merged into this one).

### Tool

| Detail | Value |
|--------|-------|
| **Script** | `scripts/generate-report.js` (self-contained, no template dependency) |
| **Data** | `data/hospital-directory-51.csv` (51 hospitals, 14 columns) |
| **Output dir** | `reports/` (gitignored) |
| **Output format** | Standalone HTML page with inline CSS, no external deps |

### Three Modes

| Mode | Command | Use Case | Humanized Content |
|------|---------|----------|-------------------|
| **Quick match** | `node scripts/generate-report.js "knee replacement" Beijing` | First-pass inquiry, "just browsing" | Price comp + action guide + FAQ. No cover letter. No service flow. |
| **Basic $49** | `node scripts/generate-report.js --name "Maria" --case "knee replacement" --city Beijing --basic` | Customer paid ¥49 | Adds cover letter with customer name. Shows "Need help? Upgrade to $399" prompt. |
| **Premium $399** | `node scripts/generate-report.js --name "John" --case "nutcracker syndrome" --city Xi'an --premium` | Customer paid ¥399 | Full: cover letter + price comp + hospital cards + action guide + **service flow** (with included/extra fee tags) + FAQ. |

### Quick Reference

```bash
cd /home/ubuntu/chinahospitalsguide

# Mode 1: Quick match (no name needed)
node scripts/generate-report.js "knee replacement"
node scripts/generate-report.js "heart bypass" Beijing
node scripts/generate-report.js "心脏搭桥" 上海
node scripts/generate-report.js "lung cancer"

# Mode 2: Basic ($49)
node scripts/generate-report.js --name "Maria Garcia" --case "knee replacement" --basic

# Mode 3: Premium ($399)
node scripts/generate-report.js --name "John Smith" --case "nutcracker syndrome" --premium

# With city filter
node scripts/generate-report.js --name "Carlos" --case "knee replacement" --city Beijing --premium
```

### How Matching Works

1. Reads `data/hospital-directory-51.csv` → 51 hospitals with Tags, Trust_Score, etc.
2. User keywords are split and checked against `KEYWORD_TAG_MAP` (200+ Chinese + English medical terms in the script)
3. Match scoring: exact tag hit = 3pts, keyword-to-tag map hit = 2pts
4. Sort by (match_score + trust_score * 2)
5. Falls back to national search if city filter returns 0
6. `PRICE_DB` auto-looks up China vs US cost for 25+ procedures

### Page Output Features

| Element | Description |
|---------|-------------|
| **Hero** | Deep navy gradient overlay (`rgba(12,24,48,0.95)` → `rgba(30,60,114,0.92)`), Playfair Display heading, kicker badge (`PERSONALIZED MEDICAL REPORT`), semi-transparent stat cards for PATIENT/CONDITION/CITY/MATCHED/DATE. Design MUST match chinahospitalsguide.com homepage. |
| **Cover letter (一封写给你的信)** | Only in --name modes. Starts "你好，[Name]..." in Chinese with 4 real questions patients ask. MATCHES template exactly. |
| **How to Use (如何使用这份报告)** | 5-step table (第1步-第5步). Replaces old "Action Plan" section. |
| **Price comparison (费用对比)** | 🇨🇳 中国预计成本 vs 🇺🇸 美国/英国典型成本 side-by-side with savings circle. Labels MUST be in Chinese. Uses inline styles (NOT CSS classes — see pitfall below). |
| **Hospital cards (推荐医院)** | 3 hospitals max. Each with: 🥇首选推荐/🥈备选推荐/🥉第三选择 badge, one-liner personality quote (💬 style), complete info table (排名/评级, 地址, 电话, 网站, 国际部, 机场交通), and 💰 费用参考 block (中国约 $X · 美国约 $Y · 节省 Z%). |
| **Transport guide (城市交通指南)** | Per-city airport/transport detail for all 10 cities (Beijing, Shanghai, Guangzhou, Shenzhen, Chengdu, Xi'an, Hangzhou, Tianjin, Nanjing, Jinan). Covers: airport description, taxi cost, metro route, local tips. |
| **Pre-departure checklist (行前准备清单)** | Categorized list: 必带的材料 (medical records, meds, passport, invitation letter, credit card, SIM card, power adapter) + 💡 支付宝 tip. |
| **Upgrade section (⭐ 升级服务) — basic only** | 5-stage service comparison table. Only shown in ¥49 basic version. Hidden in premium. |
| **Service flow (🚀 我们的服务流程) — premium only** | 6-step breakdown with ✅/💰 tags. Legend: ✅ ¥399已包含 / 💰 需额外付费. Covers: 需求确认 → 医院对接 → 行前准备 → 抵达治疗 → 出院回国 → 回国后跟进. |
| **FAQ (常见问题)** | Chinese. 6 Q&A items. Premium version adds service-specific Q&A. |
| **TXT download** | Button extracts clean plain text from page content via `downloadTxt()` JS function. Must use `appendChild/removeChild` (see pitfall). |
| **Print/PDF** | Browser print button + print-friendly CSS |

**⚠️ CRITICAL: All content is now in Chinese (2026-06-28).** Cover letter, FAQ, labels, tables, service flow, checklist, and instructions must all be in Chinese — both on the HTML page AND in the downloaded TXT. The only English remaining is the hero stat labels (PATIENT/CONDITION/CITY/MATCHED/DATE) and the hero kicker (PERSONALIZED MEDICAL REPORT).

**Design constraint (user preference):** The page shows concise info (hospital name/rank/phone only). Full details (address, website, airport info for each hospital) go in the `.txt` download. See `references/delivery-guide.md` → "Report Page Design" for the complete design system spec (fonts, colors, spacing, gradient).

**Placeholder Handling**

The script inserts the customer name into the cover letter automatically. There's no separate placeholder replacement step needed — just pass `--name` and `--case`.

### ⚠️ Known Pitfall: TXT Download Mechanism (fixed 2026-06-28)

**Bug:** The original download button had TWO conflicting mechanisms:
1. `href="data:text/plain;charset=utf-8,..."` — hardcoded cold text from `generateTextReport()` (just hospital name + phone + address)
2. `onclick="downloadTxt()"` — JS function that extracts ALL page content (cover letter, FAQ, action guide, etc.)

The `href` data URL intercepted the click, so users ALWAYS got the cold text version. The warm content on the page was never reflected in the download.

**Fix applied (2026-06-28):**
- Toolbar button: change from `document.getElementById('dloadBtn').click()` to `downloadTxt()` (direct call)
- Download `<a>` tag: remove `download="..."` and `href="data:..."` entirely. Replace with `href="#" onclick="downloadTxt();return false;"`

**Why this matters:** The user (德米) explicitly flagged that the downloaded TXT "doesn't match what we agreed on" — the HTML page was warm but the download was cold. Never embed a data URL for the full download while also having a JS extraction; always use ONE mechanism.

**Download filename quality:** The `downloadTxt()` JS function uses `document.title.replace(/[^a-z0-9]/gi,'-')+'.txt'` which produces ugly filenames like `your-hospital-report---carlos-mendoza---china-hospitals-guide.txt`. For clean filenames, consider setting a data attribute on the download link with the desired filename, or pre-computing `safeTitle` in the generator and embedding it so the download function can reference it.

Verification after any code change to download mechanism:
- grep -c data:text/plain report-*.html should return 0
- The downloadTxt() function MUST include document.body.appendChild(a) before a.click() and document.body.removeChild(a) after — detached a elements don't trigger download in Chrome
- `grep 'dloadBtn' report-*.html` should show `href="#"` not `href="data:..."`
- The toolbar button should call `downloadTxt()` directly, not click another element

### ⚠️ Known Pitfall: TXT Content Duplication (fixed 2026-06-28)

**Bug:** The `downloadTxt()` JS function used `querySelectorAll('h1,h2,h3,h4,p,li,blockquote,div')` which selected BOTH container divs AND leaf elements. Since `textContent` on a div already includes all child text, every paragraph appeared 2-3 times in the output.

**Fix applied (2026-06-28):**
- Remove `div` from the selector: `querySelectorAll('h1,h2,h3,h4,p,li,blockquote')`
- Increase threshold from `length>3` to `length>4` to filter very short fragments
- Also exclude `.footer` from extraction

**Why it matters:** The user (德米) downloaded a TXT that had every block repeated — the letter appeared 3 times, FAQ items 3 times, etc. This makes the report look unprofessional.

**Clean `downloadTxt()` function (reference):**
```javascript
function downloadTxt(){
  var c = document.querySelector('.content');
  if (!c) return;
  var t = '';
  c.querySelectorAll('h1,h2,h3,h4,p,li,blockquote').forEach(function(e){
    if (e.closest('.toolbar') || e.closest('.footer')) return;
    var txt = e.textContent.trim();
    if (txt.length > 4) t += txt + '\n\n';
  });
  var b = new Blob([t.trim()], {type: 'text/plain;charset=utf-8'});
  var u = URL.createObjectURL(b);
  var a = document.createElement('a');
  a.href = u;
  a.download = 'report-' + document.title.replace(/[^a-z0-9]/gi,'-').replace(/--+/g,'-').replace(/^-|-$/g,'') + '.txt';
  a.click();
  URL.revokeObjectURL(u);
}
```

**Verification:** Run the report page in a browser, click Download, and check the TXT for repeated blocks. Each section (letter, prices, hospitals, FAQ) should appear exactly once.

### ⚠️ Hero Design MUST Match Homepage (2026-06-28 user correction)

The user explicitly said the old hero was "太丑了" and directed: "参考我们网站的首页设计".

**Old hero (DO NOT USE):**
- Light gradient: `linear-gradient(135deg, #1a3a6b 0%, #2a5298 60%, #3a6bc0 100%)`
- Emoji badges: `👤 Carlos`, `🔍 knee`, `📍 Beijing`
- Small title: `clamp(1.6rem, 4vw, 2.8rem)`

**New hero (homepage-compatible):**
- Deep navy overlay: `linear-gradient(135deg, rgba(12,24,48,0.95), rgba(30,60,114,0.92))`
- Subtle dot pattern texture via `::before`
- Kicker badge with translucent border (like homepage)
- Large Playfair Display title: `clamp(2rem, 5vw, 3.6rem)`
- Semi-transparent stat cards: PATIENT/CONDITION/CITY/MATCHED/DATE

**Verification:** Open the generated report in a browser. The hero should visually feel like it belongs on chinahospitalsguide.com — same depth of color, same typography hierarchy, same card treatment. If it feels different from the homepage, it needs fixing.

### Price Section CSS Class Name Mismatch (fixed 2026-06-28)

The price comparison HTML used class names that had no corresponding CSS rules. HTML used `price-section`, `price-card`, `price-note` but CSS only defined `price-box`, `price-row`. Fix: use inline styles for the price layout instead of relying on CSS classes.

### Content Now in Chinese (2026-06-28)

All report content (cover letter, FAQ, labels, tables, service flow, checklist) is now in Chinese, matching the markdown templates. The only English remaining: hero stat labels (PATIENT/CONDITION/CITY/MATCHED/DATE) and the hero kicker badge.

### New Sections Added (2026-06-28)

| Section | Replaces | Appears In |
|---------|----------|-----------|
| How to Use (如何使用) | Old Action Guide | Both ¥49 and ¥399 |
| Transport Guide (城市交通指南) | — (new) | Both, per city |
| Pre-departure Checklist (行前准备清单) | — (new) | Both |
| Upgrade section (升级服务) | — (new) | ¥49 basic only |
| 6-step Service Flow (服务流程) | Old 5-step | ¥399 premium only |

- Run `mkdir -p reports` before first use
- `reports/` is gitignored — do not commit customer-specific files
- Send the file URL to the customer; no further action needed

### Legacy Files (SUPERSEDED — do not use for new reports)

The following files are legacy artifacts from before the unified script was built. New customer reports should use `scripts/generate-report.js` only.

| Legacy File | Superseded By | Notes |
|-------------|---------------|-------|
| `hospital-directory-basic-49.md` | `scripts/generate-report.js --basic` | Old markdown template, no auto-matching |
| `hospital-directory-premium-399.md` | `scripts/generate-report.js --premium` | Old markdown template, no auto-matching |
| `templates/report-page.html` | Inline HTML in `scripts/generate-report.js` | Template now built into the script |
| `scripts/generate-report-auto.js` | `scripts/generate-report.js` | Was on `main` branch — now deleted, functionality merged |
| `scripts/generate-basic49-report.py` | `scripts/generate-report.js --basic` | Old Python script, superseded by unified Node tool |

## Customer Payment Flow (confirmed 2026-06-30)

The site uses a **two-path journey**: users can either submit a case review first (path A) or go directly to payment (path B). Every page that describes the service MUST offer both paths.

See `references/payment-flow.md` for the complete architecture: path diagrams, page-by-page requirements, success message patterns, sidebar card designs, PayPal IDs, audit checklist, and fee flow explanation.

### Key principles

- **No dead-end success pages** — every form submission ends with a golden "Choose Package & Pay →" button linking to pricing.html
- **Golden CTA for payment actions** — `background:linear-gradient(135deg,#b78a42 0%,#d4a84b 100%)` signals money action
- **Sidebar shows two clear paths** — blue card for "not sure → review first", gold card for "already know → pay directly"
- **Every service page needs both paths** — a "Submit Your Case" button AND a "View Pricing & Pay" button

## Website Consistency Check (verified 2026-06-30)

After defining the pricing/service scope, ALWAYS check these website pages for consistency:

### Pages to check

1. **`pricing.html`** — Compare $49 and $399 descriptions against the defined scope. Verify PayPal buttons render (Hosted Buttons API with correct IDs).
2. **`index.html`** — Check the package cards on the homepage. Must have both "Start Free Case Review" and "View Pricing".
3. **`contact-new.html`** — Check the radio-button package options, the success message (must link to pricing.html), and the sidebar (must show 2-path pattern).
4. **`services.html`** — Must have both "See Pricing" and "Start Review" in the CTA section.
5. **`how-it-works.html`** — Must have both "Submit Your Case" and "View Pricing & Pay" in the CTA section.
6. **`contact.html`** — Legacy contact page should still have pricing link.

### Common inconsistencies found

| Website says | Our report says | Fix |
|-------------|----------------|-----|
| "Support until you reach the hospital door" | Includes treatment coordination + discharge document collation → **service doesn't stop at the door** | Update website to reflect full post-arrival scope |
| 3 bullet items for $399 | 18 service items across 6 steps → **far more comprehensive** | Expand website descriptions |
| No pricing FAQ on website | Report has detailed ¥399 vs extra fee table | Add FAQ link or sync content |

### Checklist

- [ ] $49 description: "51 hospital directory" vs "3-5 hospital match" — which is correct?
- [ ] $399 description: does it mention post-arrival services?
- [ ] $399 description: does it mention airport pickup? (should be included)
- [ ] pricing FAQ: is the included vs extra fee distinction clear?
- [ ] contact form: do the package options match the defined names?
- [ ] **Payment flow audit** — every page that mentions a service has BOTH path A (form) and path B (direct pay) links
- [ ] **Success message audit** — contact-new.html success message has golden "Choose Package & Pay →" button pointing to pricing.html
- [ ] **Sidebar audit** — contact-new.html sidebar shows two-path pattern (blue card + gold card)

## Verification Pattern (after every generator change)

After modifying `scripts/generate-report.js`, ALWAYS run this verification:

```bash
node scripts/generate-report.js --name "Test Patient" --case "knee replacement" --city Beijing --basic
node scripts/generate-report.js --name "Test Patient" --case "knee replacement" --city Beijing --premium
```

Checklist:
```bash
# 1. All sections present in basic (should have upgrade section, no service flow)
grep -c '升级服务' reports/report-test-patient-*.html
grep -c '服务流程' reports/report-test-patient-*.html    # basic: should be 0

# 2. All sections present in premium (should have service flow, no upgrade section)
grep -c '升级服务' reports/report-test-patient-*.html
grep -c '服务流程' reports/report-test-patient-*.html    # premium: should be > 0

# 3. No data:text/plain in output (old bug)
grep -c 'data:text/plain' reports/report-test-patient-*.html    # must be 0

# 4. appendChild in download function
grep -c 'appendChild' reports/report-test-patient-*.html    # must be 1+

# 5. removeChild in download function
grep -c 'removeChild' reports/report-test-patient-*.html    # must be 1+

# 6. Cover letter in Chinese
grep -c '一封写给你的信' reports/report-test-patient-*.html    # must be 1
```

## Known Limitations & Future Work

### Chinese name → ugly filename
When --name contains Chinese characters (e.g. `--name "张伟"`), the `safeTitle` sanitization regex `[^a-z0-9]+` strips them entirely, producing `report--<timestamp>.html` (double dash). Functionally fine, but ugly. Fix: use a separate Pinyin/slug field or transliteration.

### Missing data in CSV
The CSV has no `Email`, `Intl_Phone`, `Intl_LeadTime`, `Intl_Services`, or `Price_Range` columns. The premium template expects these at the per-hospital level. Currently populated with static/empty content.

### Codex handoff spec
A detailed implementation specification (`REPORT-GENERATOR-SPEC.md`) exists in the repo root for Codex CLI to complete outstanding work:
- Patient profile table (premium)
- Per-hospital price breakdown tables
- Neighborhood lifestyle guides
- "Why choose us" comparison table
- "About" section for premium
- City/hospital description data enrichment

See `REPORT-GENERATOR-SPEC.md` for full task breakdown with priority levels (P1-P4).

### Payment → auto-generation deferred
The user deferred the "pay then auto-generate report" feature for when customer volume increases. No implementation planned yet.

## Related Skills

- `hospital-directory` — maintains the underlying JSON data and frontend HTML that feeds into report generation
- `medical-tourism-client-intake` — uses the hospital directory + report packages during patient consultation
- `content-research-writer-cn` — produces daily news articles for chinahospitalsguide.com

## Skill Files

| File | Description |
|------|-------------|
| `references/delivery-guide.md` | Quick reference for unified generate-report.js: 3 modes, commands, user preference reminders |\n| `references/pricing-model.md` | Confirmed pricing structure, included vs extra fee, PayPal IDs |\n| `references/payment-flow.md` | Two-path customer journey (form→pay vs direct pay), page-by-page audit, PayPal IDs |\n| `references/transport-guide.md` | Per-city airport/transport detail for all 10 cities |\n| `references/premium-report-one-liners.md` | One-line personality descriptions per hospital |

**Note:** The old `scripts/generate-basic49-report.py` and the old markdown templates (`hospital-directory-basic-49.md`, `hospital-directory-premium-399.md`) are legacy artifacts. New reports use `scripts/generate-report.js` only.
