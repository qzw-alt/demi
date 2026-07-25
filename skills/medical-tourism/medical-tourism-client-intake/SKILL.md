---
name: medical-tourism-client-intake
description: "处理国际患者来华就医咨询的全流程：接收邮件 → 分析病情 → 确定服务方案 → 与医院初步沟通 → 回复客户。适用于 chinahospitalsguide.com 的客户咨询处理。"
version: 1.5.0
author: agent
tag: [medical-tourism, client-intake, hospital-coordination, email, whatsapp, payment-flow, case-sharing, internet-hospital-probe, diagnostic-pivot, qq-mail-compat]
---

# 医疗旅游客户咨询处理流程

国际患者通过网站或邮件发起咨询时的标准处理流程。

## 触发条件

- 收到新患者咨询邮件（nutcracker syndrome、cancer、cardiac、orthopedic等）
- 用户说「有个客户咨询，你看看」
- 需要起草/发送回复邮件给海外患者

### 0. 快速定位——中国独有医疗卖点

收到客户咨询时，先对照 `references/china-unique-medical-selling-points.md` 判断：
- 客户的疾病是否属于中国有独特优势的领域？
- 如果是，回复中**主动植入**卖点（"该手术由唐都/四医大首创"等）
- 如果不是，重点突出成本优势（50-80% less）和零等待时间

## 核心原则

### 1. 先初步沟通，后谈费用

用户明确的商业规则：
> **"先跟医院方面确定是否接诊后再谈收费"**

即：
- 收集患者病历资料
- 汇总给医院初步评估
- 确认医院可以接诊后，再谈咨询费/协调费
- **不要一开始就要求患者付费**

**例外：案例合作模式（Case-Sharing Partnership）** — 患者愿意分享治疗过程作为公开案例时，免费给 ¥399 套餐（详见 `references/case-sharing-mode.md`）。但 airport pickup 这项**不包**，由患者自费。

### 2. 跟进规则

用户偏好：「没有明确回复 ≠ 任务取消」
- 发出邮件后如果客户未回复，1-2天后跟进
- 如果用户说「明天处理」，记录日期，第二天主动提醒

### 3. 沟通风格

- 对患者：专业、有同理心、清晰列出所需信息
- 对用户（德米）：简洁、直接、给出选项让决策
- 给用户反馈时：先说结论/总结，再说详细内容

## 工作流步骤

### Step 1 — 接收与分析

收到患者邮件后：
1. **提取关键信息**：病种、症状时长、既往治疗、检查情况、所在国家、支付方式
2. **总结成结构化表格**给用户看（病情/影像数据/生活影响/支付/时间要求）
3. **提出下一步选项**（通常给2个选择，让用户定方向）

#### ⚠️ 国籍判定 — 不要从影像语言推国籍（2026-07-07 教训）

Maria Rios 案的翻车点：她的影像报告是"original Spanish + English translation"形式，最早被默认填成 Spain/Spanish，后来又被改成 Netherlands/Dutch —— **两个都错**。她实际是 **🇨🇴 哥伦比亚籍、居住荷兰 (Colombian citizen, Netherlands residence)**。影像有西语版只是因为她在拉美/西班牙做的检查，**报告语言 ≠ 国籍**。

**规则：**
- **永远以伟烨明示的国籍为准**。患者邮件里没有明示 → 在飞书对话里问伟烨确认，不要自己推
- **不要凭"报告里有 X 语言"就推断她是 X 国人**。在跨境医疗里：
  - 哥伦比亚籍患者可能因旅游/工作/历史原因在西班牙做过检查
  - 拉美裔美国人/欧洲华人可能英语+母语双报告
  - 同一份报告可能由翻译机构处理过
- **报告语言≠国籍**。报告语言只能写"original language"或具体语种，不能改写成"国籍语言"

**如果不确定**，在给医院的邮件里这样写最稳：
- `[Country]` → 用 `Country (待伟烨确认)` 占位，等伟烨回话再回填
- 影像报告语言 → 写 `original language (待伟烨确认)` 而不是直接命名

这条偏好已写入 `templates/hospital-inquiry-email-en.md` 的 Maria Rios 槽位表注释里，下次复用模板时直接看。

### Step 2 — 确认方案

用户决策后，按用户方向执行。常见方向：
- **再次沟通，索要病历资料**（当前会话的选择）
- 发摘要给医院获取初步意向
- 直接报价

### Step 2.5 — 客户询问定价/服务范围

当患者问"What do you offer?" "How much?" "What's included?"时：

1. **判断推荐版本** — 如果患者需要我们联系/协调医院 → ¥399。如果患者只想自己研究 → ¥49
2. **起草回复** — 使用 `references/email-templates.md` 模板4（英文版¥399/¥49对比说明）
3. **明确购买时机建议** — 建议患者在需要我们对接医院**之前**购买（"Recommend purchasing before we contact the hospital"）
4. **说明费用流向** — ¥399付给我们（协调服务费），治疗费直接付医院
5. **如适用，提供sample报告预览** — 帮助患者降低决策门槛
6. **提供支付入口** — 引导客户到 `pricing.html` 页面或直接发PayPal链接

### ⚠️ Step 2.7 — 案例合作模式识别（2026-07-07 新增）

当患者表示愿意分享治疗经历时，**主动**考虑 case-sharing partnership：

触发信号：
- 患者原话提到 "share my experience"、"document my case"、"help other patients"、"story"、"video" 等
- 罕见病 / 自媒体影响者 / SEO 关键词稀缺病种

如果识别到 → 用模板5确认 partnership（详见 `references/case-sharing-mode.md`）

如果不确定 → 在回复末尾轻轻带一句："If you would also be open to sharing your experience with us later — even just a few notes — it could really help other patients in the same situation, please feel free to let us know." 给患者开一扇门但不强推。

### ⚠️ 支付流程验证（重要！）

在引导客户去网站支付前，先检查支付流程是否通畅：

1. **检查 pricing.html** — PayPal按钮是否正常渲染（SDK加载、Button ID正确）
2. **检查 contact-new.html → pricing.html 路由** — 填表后的成功页面是否有"去支付"按钮？如果没有，先修网站再发指引
3. **已知问题（2026-06-30）**：contact-new.html 提交成功后没有通往 pricing.html 的链接，需要手动添加

### Step 3 — 起草回复邮件

邮件结构要素：
- 感谢对方的详细回复
- 说明下一步计划（初步评估免费，确认接诊后再谈费用）
- 列出需要对方提供的资料清单（报告、影像、病史摘要）
- 回答对方可能有的附加问题（如：May Thurner是否也能治）
- 提供发送文件的方式（邮件附件/云盘链接）
### ⚠️ 给医院国际部发问询邮件（2026-07-07 新增模板）

每次需要给医院国际部（如唐都涉外医疗科 tangdu_foreign@fmmu.edu.cn）发英文问询邮件时，**不要从零写**。直接复用 `templates/hospital-inquiry-email-en.md` 模板，把患者具体信息填进 `[槽位]` 即可。模板里已经定好了：

- 标准 Subject 格式：`International Inquiry – [Disease 1] + [Disease 2], Remote Review Request`
- CC 患者本人邮箱、Reply-To 设为伟烨 QQ 邮箱
- "What we are requesting" 4 项固定结构（确认接诊 → 远程审阅 → 报价 → 签证邀请函）
- "What we will provide" 4 项固定结构（影像报告 + DICOM + 摘要 + 单一对接人）
- 承诺 2-3 个工作日反馈 —— 内部就要做好周三/周四前同步患者的准备

### 内部医院联系卡（每次新医院对接前先填）

新患者对接新医院时（不是已知数据库里的），先填一份内部联系卡到 `/home/ubuntu/chinahospitalsguide/internal-contact-cards/<hospital-id>.md`，把"首选/备选 + 邮箱 + 电话 + 临床重点 + 数据可信度"都列清楚，再写邮件。模板见 `templates/internal-hospital-contact-card.md`。

数据源（按优先级）：
1. `api/v1/hospitals.json`（51+ 医院主库）
2. `hospital-directory-51.csv`（简版 CSV）
3. `news/<hospital>-<topic>.html`（内部新闻条目，往往含科室细节）
4. `blog/hospitals-in-<city>-for-international-patients.html`（城市医院指南）
5. `treatments/<disease>.html`（治疗页）

### ⚠️ 邮件内容输出格式（用户强偏好 — 2026-06-30 强化于 2026-07-07）

用户原话：**「我复制到邮箱那里的话一堆太乱了」**
2026-07-07 用户进一步明示：**「内容直接发给我。我现在直接转发给他。我跟他是邮件联系的」**

**规则：发给用户的邮件内容必须满足：**

1. **一整块纯净文本** — 不要在邮件正文前后夹"以下是..."、"Subject:"、"---"分割线、解释说明、emoji装饰边框
2. **可直接复制粘贴到 Gmail/Outlook** — 全选后能一次性复制，不带我的"下面是"那种引导词
3. **不要 Markdown 标题** — 标题用粗体文字（`**Stage 1**`）而不是 `#` Markdown符号
4. **不要富文本装饰** — 避免 `💡` 装饰性emoji分散注意力（正文用，签名档可以保留）
5. **分块用 `---`** — 多个段落之间用三横线分隔，不是大段空白
6. **结尾必须有"可以直接复制到邮箱里了"** — 提醒用户这是终稿
7. **触发器**：用户说「直接发我 / 我直接转发 / 内容发我 / 复制用」时 — 邮件正文**只能包含邮件本身**，**严禁**在邮件前后添加任何"⚠️ 伟烨号是不是打多了""要不要我调整""这个数字你确认下"之类的客服/审稿附注。这类附注应在**飞书对话里**作为独立消息发出，不混入邮件正文
8. **飞书消息体长度限制 + 长文强制拆段（2026-07-08 伟烨拍板强化，2026-07-11 再次强化）** — 伟烨原话："反正这种长文的话，你就拆分两段就可以了"。**这是默认行为，不是询问选项**。**对策**：起草任何长邮件/长文档时，**默认拆成 part 1 / 2 两段**分别贴出来：
   - 第一段顶部：`--- Part 1 / 2 ---`
   - 第二段顶部：`--- Part 2 / 2 ---`
   - 两段之间用 `---` 分隔符让伟烨一眼区分
   - 拆段点选在邮件自然段落的中间（列表结束、问候语之前），不要从句子中间切
   - **默认动作，不是询问项**：不要在飞书对话里问"拆不拆段？"，直接拆好贴出来。伟烨说"OK 发"或"按你建议"时直接采纳默认
   - 触发场景：任何给伟烨复制转发的纯文本（不只是邮件——抖音文案、给医院咨询稿、患者随访问卷等都算"长文"）
   - **2026-07-11 强化（"按你建议" 信号）**：伟烨多次用"按你建议 / 你写好发我 / 我现在就发"表明偏好 **agent 给默认推荐 + 拆段**，而不是列 1️⃣2️⃣3️⃣4️⃣ 让用户拍。起草邮件前若有不确定项，**先列 1-2 个推荐方案 + 默认值 + "不告诉我即默认采用"**，让伟烨一次性拍 yes/no，而不是列 5 个问题让伟烨挨个答。**违反这个规则就是违反 2026-07-11 偏好**。
9. **患者云盘链接时效** — DICOM 通常通过 Google Drive / WeTransfer / Sinosend / Dropbox 发送，链接普遍 7-30 天失效，但 Sinosend 等部分云盘可能更短。**收到链接当天**就在飞书对话里提醒伟烨"链接有时效，建议 24-48h 内下载"；如果是关键影像（DICOM、CT/MRI），优先当天下载到本地 `/home/ubuntu/chinahospitalsguide/patients/<name>/<date>/`

**❌ 反例（不要这样做）：**
```
好的，下面是邮件内容，你可以复制到 Gmail：

---

**Subject:** Your case

Dear Maria,

...

---

⚠️ 伟烨，这个号是不是打多了一位？你确认下：
- 是 **+86 157 6310 7083**？→ 直接发，没问题

还需要我修改吗？
```

**✅ 正例：**
```
**Subject:** Your case

Dear Maria,

...

Warm regards,
Weiye
```

> 这条偏好是用户明确说"太乱" + "我直接转发给他"后的强信号，必须遵守。下次起草任何给客户的邮件/文档时直接按此格式输出。任何对邮件正文的疑问、待确认事项、风险提示，都放进飞书对话的独立消息里，不进邮件正文。

### Step 4 — 发送邮件

使用 himalaya CLI 或 Python smtplib 发送邮件。
参见 `references/email-setup.md` 获取当前邮箱配置。

**注意：SMTP 没配置时，按用户偏好起草邮件正文给用户，让用户手动复制粘贴转发，不要尝试自动发送。**

### Step 5 — 跟进

- 如果邮件成功发送，记录已发送
- 如果对方未回复，1-2天后提醒用户是否需要跟进
- 如果对方回复了新资料，进入 Step 1 分析新信息

## 数据收集标准

每封患者咨询需要提取的信息：

| 字段 | 说明 |
|------|------|
| 病种 | 主诊断 + 并发症 |
| 症状时长 | 何时开始 |
| 生活影响 | 是否影响工作/学习/日常生活 |
| 关键影像数据 | CT/MRI/超声的具体测量值 |
| 既往治疗 | 做过什么，效果如何 |
| 年龄/体型 | 身高体重（用于评估手术风险） |
| 国籍/居住地 | 签证和旅行安排需要 |
| 支付方式 | 自费/保险 |
| 时间要求 | 是否有期望的治疗时间 |
| 联系方式 | 手机/邮箱（备用） |
| **是否愿意分享案例** | 案例合作模式判断 |

## 医院数据库检查

收到客户咨询后，检查该医院是否已在我们的核心资料库中：
- **API 资料库**：`/home/ubuntu/chinahospitalsguide/api/v1/hospitals.json`（51+ 家医院，覆盖北京、上海、广州、深圳、西安、成都、天津、杭州、南京、济南等城市）
- **前端页面**：`/home/ubuntu/chinahospitalsguide/hospitals.html`（数据驱动的医院目录页，内嵌 JS 数组）
- 如果不在库中，需要手动收集资料后新增（参见 `hospital-directory` 技能）

> ⚠️ 注意：新医院从资料搜索到录入目录是一个完整流程，先检查数据库看目标医院是否已有，没有则走新增流程。

### 新增医院到目录的流程

向数据库中添加新的医院需要同步更新两个文件：
1. `api/v1/hospitals.json` — 完整 API 数据（含信任评分、国际合作部详情）
2. `hospitals.html` — 前端展示（JS 数组 + 可选的新标签映射）

详见 `hospital-directory` 技能。

### 生成客户报告（针对已购买资料包的客户）

如果客户已购买资料包（¥49基础版 / ¥399升级版），生成标准医院报告：
- **¥49基础版** — 51家医院信息卡片格式
- **¥399升级版** — 带有人性化温度的完整报告（致客户信 + 医院深度画像 + 行动指南 + FAQ）

详见 `hospital-customer-report` 技能。生成后 push 到 GitHub 或直接发送给客户。

## 案例合作模式（Case-Sharing Partnership）

详见 `references/case-sharing-mode.md`，核心要点：

- 患者同意公开分享治疗过程 → 我们免费给 ¥399 套餐
- **airport pickup 不包**（患者自费）
- 发布前必须给患者过审
- 内部账本标记 `revenue: 0, value-given: ¥399-equivalent`
- 模板5 在 `references/email-templates.md`

## 相关引用

- `references/patient-questionnaire.md` — 标准咨询问题清单
- `references/email-templates.md` — 常见邮件模板（含模板5 案例合作确认）
- `references/china-unique-medical-selling-points.md` — 中国独有医疗领域卖点（用于回复时主动植入）
- `references/whatsapp-business-profile.md` — WhatsApp Business 资料设置（头像、简介、快捷回复、目录）
- `references/case-sharing-mode.md` — 案例合作模式业务规则（2026-07-07 新增）

## 增量主题索引（2026-07-07 补强，2026-07-08 增补）

为方便未来 agent 快速定位同类场景，正文分散在下方各 ⚠️ 段落里：

- **云盘链接诊断三步法** — `### ⚠️ 云盘链接诊断三步法（2026-07-07 新增 — Sinosend 案）`（HEAD → 跳第一跳 → follow all）
  - 可重跑脚本: `scripts/probe-cloud-share-link.sh "<URL>"` —— 把整套诊断命令打包好，下次有患者链接过来直接跑
- **患者说"链接是活的"但 curl 看不到** — `### 当患者说"链接是活的"但 curl 返回 404`
- **国家/居住地/影像语言三元组** — `## 患者国家/居住地三元组`
- **双邮件同发模式（Maria + 唐都 同步）** — `## 双邮件同发模式`
- **倒计时承诺追踪（commit log + checklist）** — `## 倒计时承诺的内部追踪`
- **飞书消息体长度限制** — `## 飞书消息体长度限制`
- **数据库驱动的医院候选筛选 + 50KB 读取坑** — `## 数据库驱动的医院候选筛选（2026-07-08 新增）`
- **中国三甲统一规则：必须本人到场** — `## 中国顶级三甲对国际患者的统一接诊规则（2026-07-08 新增 — 北大第一案）`
- **服务流程改造触发器** — `## 服务流程改造触发器（2026-07-08 新增）`
- **医院"互联网问诊"渠道核实 4 步法** — `## 医院"互联网问诊"渠道核实 4 步法（2026-07-08 新增 — 中日友好案）` + 详见 `references/hospital-internet-consultation-probe.md`

## 数据库驱动的医院候选筛选（2026-07-08 新增 — 北大第一案教训）

**为什么要做这一步**：每次新患者进来想"哪家医院能治"时，**不要凭记忆或拍脑袋**。当前 51 家医院库里每一家的 `tags` / `rank` / `trust.notes` 都是结构化的，可以用关键词一次过滤出真实候选。

**读取 51 家医院主库的关键技巧**：

1. **不要用 `terminal(cat ...)`** —— terminal 输出有 **50KB stdout 上限**，文件 58KB 会被截到 50KB，导致 JSON parse 在中段挂掉。本会话踩过 4 次坑，最后一次直接 `open(..., 'rb')` 才读到完整内容
2. **正确方式**（Python `execute_code` 里）：
   ```python
   import json
   with open("/home/ubuntu/chinahospitalsguide/api/v1/hospitals.json", "rb") as f:
       data = json.loads(f.read().decode("utf-8-sig"))  # utf-8-sig 自动剥 BOM
   hosp = data["hospitals"]
   ```
3. **字段名注意**：`name` + `name_zh`（不是 `name_en` / `name_cn`）；`city` 用英文 "Beijing" 不是 "北京"；联系方式在顶层 `phone` 或 `international_dept.{email,phone}`

**按病情关键词筛选标准流程**：

```python
KEYWORDS = {
    "nutcracker": ["nutcracker", "renal vein", "left renal", "胡桃夹"],
    "may-thurner": ["may-thurner", "iliac vein", "iliac compression", "髂静脉"],
    "vascular": ["vascular", "blood vessel", "血管"],
    "interventional": ["interventional", "介入"],
    "urology": ["urology", "泌尿"],
}
scoreboard = []
for h in hosp:
    blob = json.dumps(h, ensure_ascii=False).lower()
    matched = [cat for cat, kws in KEYWORDS.items() if any(k.lower() in blob for k in kws)]
    if matched:
        scoreboard.append((len(set(matched)), h, matched))
scoreboard.sort(reverse=True)  # 命中越多家排越前
```

**当前数据库的硬约束（2026-07-08 验证过）**：

| 病种 | 数据库命中医院数 | 备注 |
|------|------------------|------|
| Nutcracker + May Thurner 同时 | **仅 1 家** — Tangdu | `trust.notes` 里写明 |
| Beijing 内能做血管介入 + 接海外资料 | **0 家** | 主库里无匹配 |
| 只接外籍 + 强血管外科 | 几乎都是军事医院（北京 301、西安唐都），**军事医院体制上不直接接诊外籍患者**，但**专家可以作 MDT 远程协诊方**参与。Maria Rios 案确立：主诊医院必须选非军队背景，唐都可作跨院 MDT 协诊备选 | Maria Rios 案已踩雷 |

**这套筛选得到的结论直接喂给伟烨做决策**。**不要瞎推荐医院**，尤其是"看起来在 Beijing 又在主库"的就推——主库筛选是唯一可信源。

完整可重跑脚本参考：`references/script-filter-hospitals-by-keywords.md`

## 中国顶级三甲对国际患者的统一接诊规则（2026-07-08 新增 — 北大第一案）

**触发**：伟烨说"北大第一医院要求必须本人到场"，这其实**不是个别医院的偏好，是中国顶级三甲的统一规则**——国家卫健委规范下的"非急诊国际患者就诊流程"，三家三甲基本一致。

**标准流程**（各家基本一致）：

> 本人带齐资料到场 → 普通门诊挂号（非国际部） → 一周后排上号 → 看诊当日审核资料 → 不通过则不收治 → 患者回国

**这条规则的实际含义**：

1. **"提前把资料发给大夫私下审核"在中国三甲几乎不可能**——医生不能脱开医院受理外部会诊资料，这是合规红线
2. **国际部 ≠ 远程预审通道** —— 北京 15 家里只有少数（中日友好 / 安贞 / 301）有独立国际部电话，但**国际部也只是"加速挂号 + 翻译陪同"，不提供资料预审**
3. **患者真正进入治疗前的预期是**：到中国 1-2 周才能见到大夫，**不是"我先递资料，你们看完再让我来"**
4. **唯一例外**：少数医院国际部（如唐都涉外医疗科 tangdu_foreign@fmmu.edu.cn）的"远程影像评估 + 报价"服务，但**不是所有医院都做**，且**军事医院对外籍有限制**

**对服务流程的影响（必须告诉患者）**：

- ¥399 / ¥49 套餐里"协调医院先看资料判断能否接诊" **不是标配前置**，得先**逐家确认**哪家愿意做预审
- 患者从一开始就要被告知："先到中国，再看病"是基准事实
- 如果医院不接受预审，¥399 的价值就退化为"现场挂号 + 翻译陪同 + 行程安排"，**这不是失败的协调，是市场基线**

**伟烨问"后续服务流程也要适当改变了"时的具体改造方向**（给伟烨讨论用）：

| 当前 ¥399 内容 | 改造方向（建议） |
|---|---|
| 免费前置资料预审 | 拆出"材料整理费 ¥X"作为可选付费前置 |
| 假定能联系上大夫 | 改成"医院接受预审 → 找替代医院"二选一流程 |
| 现场全包 | 加入"接机不含 / 现场陪同 1 周起 / 一周内不收治即返程"的明确预期管理 |

**避免做的事**：

- ❌ 不要承诺医院一定会接诊
- ❌ 不要暗示"提前审核资料"是中国医院的常规服务
- ❌ 不要用"我可以联系上大夫私下沟通"这种话术——医院合规线过不去

## 服务流程改造触发器（2026-07-08 新增）

**触发场景**：伟烨说类似"看来我们后续的服务流程也要适当改变了"。

**触发时的标准动作**：

1. **不要立刻改造**——先把当下的具体卡点（哪一家医院、什么规则、为什么不行）写成可复用判断框架
2. **优先落 memory**（"业务规则" + 日期 + 触发案例），让这次教训能影响未来同类对话
3. **其次落 skill**（服务流程类改造 → medical-tourism-client-intake SKILL.md 的 `## 服务流程改造触发器` 一节）
4. **最后才是改套餐定价 / pricing.html / 给客户的 marketing 文案**

**判断是否真要改 ¥399 / ¥49 套餐**（不是伟烨一开口就改）：

- 一次单点卡点 ≠ 流程问题（北大第一是个例还是普遍？）
- 多次同种卡点（不同医院都拒预审）= 流程问题，必须改
- 患者/医院任一方反馈"我以为 X"导致满意度差 = 流程问题，必须改

**改造前必须问伟烨**：

- "这次拒预审是 X 家医院独有，还是已经发生了 N 次？"
- "¥399 的价格要不要同步调？（因为服务范围缩了）"
- "在 pricing.html 上写'远程预审'宣传词要不要改？"

## 医院"互联网问诊"渠道核实 4 步法（2026-07-08 新增 — 中日友好案）

**触发场景**：伟烨说"X 医院的电话说他们有 APP 互联网问诊，你查一下官网是不是真的有"——或者更宽泛："查一下 X 医院互联网医院 / 在线问诊的真实情况"。

**核心警告**：**大陆三甲官网普遍挂着"互联网医院"图标，但很多是 4 年前的占位符空壳**。中日友好医院就是一个具体反例——官网入口在，但点开是 2022-09 的"网站建设中"页面，官方患者 APP 只有"预约挂号+取报告单"，没有在线问诊；医护端 APP 倒是有，但只给医生用。

**4 步法**（详见 `references/hospital-internet-consultation-probe.md` 完整脚本）：

1. **官网入口识别** —— `curl` 首页 + grep "互联网医院/在线问诊/APP/小程序" 关键词
2. **占位符空壳识别** —— 直接 GET 子页面，看 title/meta/文件大小是否疑似"建设栏目"空壳
3. **iTunes Search API 查官方 APP** —— `https://itunes.apple.com/search?term=<医院名>&country=cn&entity=software` → 用 `sellerName` 字段筛官方 APP（必须是医院官方名），看 bundleId 是 `.patient` 还是 `.doctor`
4. **Lookup API 拿描述** —— `https://itunes.apple.com/lookup?id=<APP_ID>` → 看 `description` 里有没有"在线问诊/复诊/视频问诊"

**给伟烨汇报的措辞**：三段式（先说有/没有入口 → 再说是真是假 → 最后给选择）。

**踩过的坑**（写下来防再踩）：

- ❌ "X 医院官网有'互联网医院'图标，所以能做在线问诊"——**错**，可能是空壳
- ❌ "X 医院有 APP，所以能做在线问诊"——**错**，APP 可能只是挂号+报告
- ❌ "X 医院 APP 描述里写'在线问诊'，所以能做"——**错**，可能是医护端

完整诊断档案落 `internal-research-notes/<医院>-internet-hospital-<日期>.md`。

## 复杂并发病情协调：单家医院 + 跨院专家 MDT 模式（2026-07-11 新增 — Maria Rios 案确立）

**触发场景**：患者有 **2-3 个并发/罕见病种**，单个医院（或任何单一医院）单独覆盖所有病种的能力不足。常见案例：

- 血管 + 泌尿 + 胃肠 多系统并发（如 Maria Rios: Nutcracker + May Thurner + 疑似 SMAS）
- 骨科 + 整形 + 神经外科 多学科交叉（如复杂脊柱侧弯 + 神经损伤）
- 罕见病并发（如神经纤维瘤 + 血管畸形）

**问题**：患者单一医院看不全，跑 3 家医院风险高（国际患者语言、体能、签证、机票都是负担）

**解法（伟烨 2026-07-11 明示）**：**单家窗口医院 + 跨院专家 MDT 远程协诊网络**

```
┌─────────────────────────────────────────────────────────────┐
│  Maria Rios                                                  │
│       │                                                      │
│       ▼                                                      │
│  上海第九人民医院（窗口医院 — 收诊/排号/MDT召集/会诊主持）       │
│       │                                                      │
│       ▼                                                      │
│  MDT 远程协诊（医院有同行资源池）                                │
│  ├─ 泌尿科 (Nutcracker)  ← 也许有其他医院的专家                  │
│  ├─ 血管外科 (May-Thurner)                                  │
│  └─ 胃肠外科 (SMAS 评估)                                      │
└─────────────────────────────────────────────────────────────┘
```

**这套解法对应业务定位**：我们是 **跨院 MDT 协调者**，不是医院。这是 chinahospitalsguide 跟其他中介的差异化卖点。

**邮件叙事结构**（给患者的英文邮件）：

1. **进展好消息** —— 不需要跑 3 家医院
2. **机构能力** —— 我们找到了**有同行资源**的医院，能调外部专家协诊
3. **病情分别处理**（每条 1 句）：
   - 谁负责（科室）
   - 方向（达芬奇/介入/开放手术 —— **不替医生下结论**）
   - 由谁解释（"details to be explained to you directly by the operating surgeon"）
4. **下一步**：医生主动联系患者（不要让她跑）
5. **影像/病历**：说明是否已转过去
6. **案例合作**：简短一段，无 deadline

**关键措辞模板（不替医生下结论）**：

> "The direction currently under consideration is a minimally-invasive [approach] using [technique], with details to be explained to you directly by the operating surgeon during the upcoming video discussion. I am intentionally not specifying step-by-step what the surgical technique will be in writing, because the right technique depends on findings your imaging will show the team, and the surgeon should explain it to you face-to-face rather than through me."

**诚实处理"外院专家邀请是否答应"**（不能打包票）：

> "They will be inviting certain outside specialists into the MDT based on your imaging. Whether each invited specialist accepts is not something any hospital can promise in advance — that is a normal part of how these consultations work in China, and it is one of the reasons we wanted the hospital with the right peer connections rather than the closest one."

**避免做的事**：

- ❌ 不要承诺"具体哪个外院专家一定参加" —— 邀请和答应是两件事
- ❌ 不要承诺"3 个病一定都能治" —— 让医院评估
- ❌ 不要承诺"达芬奇/某种技术的具体步骤" —— 让医生视频说
- ❌ 不要让患者自己跑 3 家医院 —— 单家窗口 + 跨院 MDT 才是解法

完整案例档案见 `references/maria-rios-cross-hospital-mdt-case.md`（模板化写作参考）。

## 军队背景三甲对外籍接诊的限制（2026-07-11 新增 — Maria Rios 案确立）

**触发**：伟烨 2026-07-11 明示 — "唐都是军队医院不对外国人治疗，但有可能让唐都的专家一起会诊"。

**核心规则**：

- **军队背景三甲**（中国人民解放军 / 武警 / 军校附属医院 — 唐都、西京、301、304 等）**体制上不直接接诊外籍患者**
- **军队专家可以**作 MDT **远程协诊方**参与（作为会诊专家，不是主诊）
- **主诊医院必须是非军队背景的三甲**（如上海九院、北大第一、华西、协和等）

**业务判断流程**：

```
新患者病情 → 主诊医院候选筛选
            ↓
       候选包含军队医院？
            ├─ YES → 调整：选非军队背景做主诊，军队医院专家作 MDT 远程协诊
            └─ NO  → 正常对接
```

**对邮件叙事的实际含义**：

- 不告诉患者"军队医院对外籍有政策限制"这种体制内部细节
- 改用 positive 措辞："the hospital has direct working relationships with the specific specialist groups elsewhere in China"
- 如果唐都专家被邀请进 MDT，写 "the specific specialist groups" 模糊措辞，**不点名唐都**（避免揭"为什么没去成"的旧伤）

**对 pricing.html / 套餐宣传的影响**：

- 不能写"我们能让你去唐都" —— 主诊层面进不去
- 可以写"对罕见/复杂病例协调跨院专家 MDT 会诊" —— 这是新卖点

## 诊断转折期的中立邮件 + 邮件节奏控制（2026-07-11 新增 — Maria Rios 第 2 阶段）

**触发场景**：经过 7+ 天协调（病例评估 → 院方初步回应 → 临床资料对接 → 视频会诊），医院**给了诊断结论**，但**结论跟之前预期不同** —— 不是简单确认，而是**转向**：
- 之前的预期是"3 个并发血管病，要分别处理"
- 现在医院的判断是"首要问题不是血管，是另一个系统，先看那个"
- 之前的预期是"建议手术"，现在是"建议保守治疗 / 建议先在本地评估"

Maria Rios 案的第 2 阶段（2026-07-21）：九院 3 位教授共识 —— 之前判断的 Nutcracker + May-Thurner + SMAS 中，**首要诊断变成肠问题**，建议**先解决肠** —— 术后 Nutcracker 等可能**自然改善甚至不需要手术**。苏楷（九院联络人）甚至建议 Maria **在荷兰本地询问这个肠手术是否可行** —— 因为如果能在本地医保下做，Maria 根本不用来中国。

### ⚠️ 诊断转折期邮件的 3 个判断点

#### 1. 邮件基调：**中性务实**（不要 A 庆祝 / 也不要 C 谨慎过头）

| 选项 | 风险 |
|---|---|
| A. 庆祝（"太好了有结果了！"） | 误导患者以为**她之前的方案还在**。如果主诊方向已变，庆祝 = 让她以为 Nutcracker 还要做 |
| B. 中性务实（推荐默认） | 复述医院判断 + 提供"本地询问"路径 + 保留中立 |
| C. 谨慎过头（"等医院更详细的报告再回你"） | 患者已经焦虑 4.5 年了，再压几天她情绪会崩 |

**正例措辞**（Maria 第 2 阶段邮件的关键句）：

> "The consensus among Prof. Yao and the other two professors is an important turning point: rather than starting with the complex vascular and urological work, the priority has been set on resolving the underlying intestinal issue first, with the expectation that this may significantly improve — or even resolve — the Nutcracker findings later. That is exactly the kind of clarity a good MDT should produce."

**避免措辞**：
- ❌ "Excellent news!" / "We're thrilled!" —— 患者看完以为她在做 Nutcracker 手术准备
- ❌ "We need to discuss this further" —— 焦虑型患者会解读为"坏消息"
- ❌ "Whatever you decide, we are not going anywhere" —— 太戏剧化、像告别式

#### 2. 本地治疗 vs 来华治疗：**完全中立**（不要 B 拉客 / 不要 C 劝退）

- **A. 完全中立**（推荐默认） —— "无论你在荷兰还是中国治疗，我们都支持。决定权在你。"
- **B. 偏中国** —— "来中国有附加好处（家人陪同 / 资深医生面对面）"，微妙拉客
- **C. 偏本地** —— "减少跨国奔波 + 本地医保覆盖"

**为什么 A 是对的**：
- case-sharing 客户是**长期人脉**，不是要立刻转化的高客单价
- 维护关系 > 短期转化 —— 患者朋友 / 家人将来再来找你的概率远大于这一单
- 而且她有 4.5 年病史，case-sharing 内容沉淀下来**比 ¥399 套餐重要得多**

**邮件里如何表达中立**：
- 提供"具体步骤 1/2/3" 给本地医院，让本地医院判断
- 明确说"医院 open to 任何 path" —— 让医院侧也承担选择压力
- 不提"来中国有什么好处" —— 即使是事实

#### 3. "我们的服务一直都在"：**全程陪同**（不是 A "随时在" / 不是 B "帮你拿到的"）

3 种解读伟烨的"我们的服务一直都在"：

| 解读 | 风险 |
|---|---|
| A. "我们随时在" —— "你后续要回中国或再问询医院，我们随时响应" | 太模糊，患者不知道具体承诺 |
| B. "我们帮你拿这个诊断" —— "这是我们协调的成果" | 把九院的诊断说成"我们功劳"，会让人觉得不专业 |
| C. "我们跟进"（推荐默认） —— "我们会陪你做完本地询问的全过程 + 跟九院保持沟通" | 具体到行动，明确不丢下她 |

**正例措辞**：

> "We will remain on standby with the Shanghai team throughout your decision process. If your Dutch doctors raise technical questions about the diagnosis or treatment, we can route them back to Prof. Yao's team for clarification."

### ⚠️ 节奏控制：第 1 封（叙事/进展类）跟第 2 封（动作确认类）至少 12 小时间隔

Maria Rios 案反复踩的坑：用户当晚发完大叙事邮件后，**立刻就想发动作确认邮件**（"是否同意 + 联系方式授权 + 联系信息确认"），间隔 < 12 小时。

**为什么这是节奏压迫**：
- 焦虑型患者（Maria 4.5 年病史）一晚收到 2 封"重要更新"，会从"she is taking care of me"滑到"she is pressuring me"
- 让她**消化 + 行动 + 回信**的时间被压缩，回复质量必然下降
- 患者回信间隔太短可能错过一些关键问题（你问她"是否有其他联系方式"，她没想到要补 WeChat ID）

**对策（2026-07-11 验证）**：
- 第 1 封（叙事/进展类）和第 2 封（动作确认类）之间**至少 12 小时间隔**
- 如果用户说"我现在就发"，**主动提醒一句**："建议明天白天发，给 Maria 一晚消化上一封"
- 用户说"没事，现在发"就发，但**主动提醒了就是 audit pass**（用户后悔了不是 agent 的责任）
- 如果时间隔不到 12 小时（比如凌晨 + 早上），邮件标题用"Re: ..." 而不是新建主题，**视觉上像延续不是新要求**

### ⚠️ QQ Mail 网页版 + 飞书复制粘贴的兼容性坑（2026-07-11 验证 — user "复制到邮件 还是一堆"）

伟烨用 QQ Mail 网页版发邮件，从飞书复制粘贴正文到 QQ Mail 编辑器时：

- **`### 三级标题` Markdown 会被 QQ Mail 当字面文字渲染**（显示 `### Heading`），不变成粗体
- **复制框里夹中文说明**（"⚠️ 这里是说明"）会粘到正文里
- **复制框周围的 `--- Part 1 / 2 ---` 分隔符** 也会被粘进去
- **`**bold**` 飞书渲染好看但 QQ Mail 也会被吃成 `**bold**` 字面文字**

**对策（飞书对话侧 / 起草端）**：
- 任何 QQ Mail / Outlook / 飞书邮件客户端之间复制粘贴的正文，**先假设接收端会按字面渲染**，**不要用任何依赖语法的标记**（不要 `###` 不要 `**bold**` 不要 `[link](url)`）
- 飞书对话里的分隔符 `--- Part 1 / 2 ---` 是给伟烨看的**视觉提示**，**不是邮件正文的一部分** —— 复制框必须**显式标"不要复制分隔符"**
- 复制框设计规则：
  - **框外顶部**：3-5 行排版规则（哪些不复制、为什么）
  - **框内**：**只有邮件正文**
  - **框外底部**：1-2 行怎么用说明
  - 任何"⚠️ 伟烨号是不是打多了 / 要不要我调整" 这种客服附注**不进框内**，留作飞书对话的独立消息

**正例**（Maria 邮件复制框）：

```markdown
## ⚠️ 复制规则

- ✅ 只复制下面两个虚线框之间的英文
- ❌ 不要复制虚线框本身
- ❌ 不要复制上方/下方的中文说明
- ❌ 不要复制分隔符 "--- Part 1 / 2 ---"

---

[从这里开始复制 ↓]

Hi Maria,

...（邮件正文）...

[复制到这里结束 ↑]

---

## 📎 怎么用这份稿
（用 1-2 行告诉用户怎么操作）
```

**反例**（user "复制到邮件 还是一堆"那次的失败）：

```markdown
--- Part 1 / 2 ---          ← 用户粘进去了
⚠️ 伟烨号是不是打多了？   ← 用户粘进去了

Hi Maria,                  ← 这才是邮件开头

...（正文）...

--- Part 1 / 2 ---          ← 用户也粘进去了
```

**General rule for 复制框**：任何"我要提醒自己 / 我想问伟烨"的内容**永远不写进复制框内**，**只写飞书对话消息里**。

### 诊断转折邮件的 narrative arc（4 步）

```text
1. 复述医院共识（中性、具体，不评价好坏）
2. 提供"本地询问"路径（具体到 1/2/3 步骤，让本地医院决定）
3. 全程陪同承诺（具体到"如果本地医院有技术问题，我们转回九院"）
4. 案例合作轻提 + 留个轻 action（"如果你方便，回复里说下你跟本地医院的沟通窗口"）
```

### 案例合作模式在诊断转折期的处理

之前 case-sharing 提的是"治疗过程笔记 / 照片 / 视频" —— 但**诊断转折期没有治疗过程**，**该提什么？**

**正例**（Maria 第 2 阶段邮件里的措辞）：

> "On the case-sharing side: please do not feel any obligation. The conversation so far has been useful in its own right, and what you decide locally — and how that goes — will be valuable for other patients in your situation regardless of where treatment ultimately happens."

**关键词**：
- **"in its own right"** —— 即使没成交，**对话过程本身就是 case-sharing 价值**
- **"regardless of where treatment ultimately happens"** —— 解绑 case-sharing 与是否来中国的关联
- **"valuable for other patients in your situation"** —— 锚定"沉淀故事"的真实价值

**避免**：
- ❌ "If you choose to come to China, we'd love to document..." —— 把 case-sharing 跟中国方案绑定
- ❌ "We hope you'll consider sharing..." —— 任何"希望"语气都带压力

### 诊断转折邮件应避免做的事

- ❌ **不要承诺 "Shanghai team will see you"** —— 即使上海九院说"open to"，措辞也只能是 "open to seeing you if local treatment is not feasible or not preferred"
- ❌ **不要替医生下结论** —— 医院说"first look at intestinal issue"，邮件里就照搬"intestinal issue"而不是我的转述
- ❌ **不要给隐性优惠** —— 诊断转折期患者情绪脆弱，"打个折"会被解读为"在帮她做选择"
- ❌ **不要 push 她现在决策** —— "Take your time" 必须明确写出来
- ❌ **不要揭"为什么没去成唐都"的旧伤** —— 用"the specific specialist groups" 模糊措辞代替具体医院名（即使唐都专家已被邀请进 MDT）

## 邮件动作确认邮件的 3 个易错点（2026-07-11 Maria Rios 案新增）

### ⚠️ "I am passing... right now" 措辞必须先核实再写

写给患者的"动作确认"邮件里很常见"我马上把你的联系方式发给医院" / "I am passing your details to the hospital right now" 这种句式。

**风险**：如果患者实际还没点头，或者伟烨实际还没把联系方式发给医院，写了"right now"就是不实表述。患者当天收到邮件，**等到第二天还没看到医院医生加她微信**，会问"你不是说 right now 吗" → 信任裂缝。

**对策**：
- 起草前**必须问伟烨**："你已发 / 你准备发 / 你没发，要我帮你起给医院的邮件？" 任一答复，措辞对应调整：
  - **已发**："I have passed your details to..." (完成时)
  - **准备发**："I will pass your details to the hospital today" (将来时)
  - **没发，要我起医院邮件**："I will draft an inquiry to the hospital today and pass your details once you confirm"
- **不告诉伟烨默认用 "right now"**——这个措辞不能默认

### ⚠️ 同一晚连续发两封邮件给同一患者 = 节奏过紧

Maria Rios 案的具体踩坑：

- 第 1 封（"上海九院 + MDT 叙事"大邮件）：伟烨发
- 第 2 封（"确认意向 + 授权 + 联系信息"短邮件）：**伟烨当晚就想发**

问题：两封邮件间隔 < 12 小时，Maria 一晚收到 2 封"重要更新"，**节奏压迫感强**。Maria 这种焦虑型患者会从"she is taking care of me" 滑到 "she is pressuring me"。

**对策**：
- 第 1 封（叙事/进展类）跟第 2 封（动作确认类）之间**至少 12 小时间隔**
- 如果伟烨说"我现在就发"，**主动提一句**："建议明天白天发，给 Maria 一晚消化上一封"
- 伟烨可能说"没事，我现在就发"，那就发，但**主动提醒了就是 audit pass**

### ⚠️ QQ Mail 网页版 + 飞书复制粘贴的兼容性

伟烨用 QQ Mail 网页版发邮件，飞书复制粘贴正文到 QQ Mail 编辑器时：

- **`### 三级标题` Markdown 会被 QQ Mail 当字面文字渲染**（显示 `### Heading`），不变成粗体
- **复制框里夹中文说明**（"⚠️ 这里是说明"）会粘到正文里
- **复制框周围的 `--- Part 1 / 2 ---` 分隔符** 也会被粘进去

**对策**（伟烨端）：
- 在飞书对话里给邮件正文时，**用最简形式**：纯文本 + 空行分段，**不写 ### 标题符**
- 如果需要"标题层级"，用粗体文字 `**Title**` 而不是 `#`
- 分隔符用 `---`，但分隔符**单独成行**且**两侧各一个空行**，方便伟烨一眼看出"这是分隔符别粘"

**对策**（起草端）：
- 任何 QQ Mail / Outlook / 飞书邮件客户端之间复制粘贴的正文，**先假设接收端会按字面渲染**，不用任何依赖语法的标记
- 飞书对话里的分隔符 `--- Part 1 / 2 ---` 是给伟烨看的**视觉提示**，**不是邮件正文的一部分**

## 注意事项

- 患者的DICOM文件通常很大，建议提供云盘链接接收；**云盘链接 24-48h 内下载**
- 回复邮件时保持邮件线程（Re: 主题），不要新建线程
- 涉及May Thurner等并存疾病时，一并询问医院的治疗方案
- 不要承诺医院一定能治疗——先让医院评估
- 不要在没有用户确认的情况下直接发送邮件
- 如果服务器没有配置SMTP，把邮件正文写出来让用户手动发送
- 案例合作模式下，不要告诉医院"这是免费患者"，按标准 ¥399 case 跟医院对接

### ⚠️ 微信 / WhatsApp 短消息客户边界话术（2026-07-24 新增）

**触发场景**：客户不走官网表单，直接加伟烨私人微信 / WhatsApp，发来资料、问具体病情、问定价。

**跟邮件的根本差异**：
- 微信/IM 节奏快、客户耐心低、屏幕小
- 一封"长邮件"在微信里 = 复制粘贴怪 / 机器人感
- **必须分多条短消息**（1-2 句 / 条）
- **不写 Markdown**（`###` `**bold**` 会被微信当字面文字渲染）
- **正文不加 emoji**（除非客户先加了或伟烨偏好）

### ⚠️ 飞书→伟烨端：只发内容，不要附注（2026-07-24 强化 — 用户原话："只发内容就行了，其他不用说了"）

**触发信号**：伟烨说"直接发我"/"内容发我"/"我直接转发"/"一段发给我"/"只发内容就行了"。

**这是用户的强偏好**，不是"问一下再确认"——任何给伟烨复制转发的产出物（邮件 / 微信消息 / 抖音文案 / 文案），**飞书对话里只贴内容本身**，**不附加任何**：

- "以下是..." / "上面是..." 引导词
- "⚠️ 伟烨，这个 X 你确认下" / "要不要我调整" 客服附注
- 复制框外面的解释、表格、CTA
- 多余的 "用这个"/"你审一下" 提醒

**反例**（违反偏好）：
```
好，下面是 5 条微信消息：

---

消息 1：
[内容]

---

需要我调整某条吗？
```

**正例**（遵守偏好）：
```
消息 1：
[内容]

消息 2：
[内容]
```

**完整的"复制框 + 附注"设计**（仅在伟烨明确要求"你帮我看一下""起草后给我解释"时才用）：见 `references/wechat-unpaid-customer-boundary-templates.md` 的"复制框设计规则"段。

**触发场景**：
- 伟烨说"内容发我就行" / "直接发我" / "一段发给我" → 飞书对话里**只有内容**
- 伟烨说"你审一下" / "改某条" / "起草后我看看" → 飞书对话里**内容 + 简短附注**

**例外**：邮件/微信内容**之前**已经有"我下一步要做什么"或"还差什么资料"这种**待办**信息，可以在飞书对话的**独立消息**里发（不进复制框）。

**核心 3 条边界**：

1. **微信不收款** —— 跨境支付管制 + 个人账号限制。**只用 PayPal**
2. **说"成本结构"不说"流程规定"** —— 医生时间成本 + 人力协调成本 + 医院接洽成本
3. **不评价客户本地医生方案** —— "你已经在本地启动治疗？先按当地走，我们随时能配合"

**当前默认模板**（v1.1 · 2026-07-24）：

```
消息 1：感谢 + 接住情绪
消息 2：讲成本结构（核心 · 3 类成本）
消息 3：把"收费"框成"启动"（¥49 = 服务启动，不付 = 医生不介入）
消息 4：行动引导（pricing.html 链接 + 让客户描述阶段）
消息 5（可选）：紧急情况例外（仅在客户说"急"时发）
```

**完整模板 + 3 段反驳预案 + 微信→英文转换规则 + 客户状态 → 触发动作 + 演进历史**：
见 `references/wechat-unpaid-customer-boundary-templates.md`

**配套文件**：`~/chinahospitalsguide/templates/wechat-unpaid-customer-2026-07-24.md`（可直接复制粘贴到微信）

**避免**：

- ❌ 一长段微信消息（即使是 IM 也别超过 4-5 句）
- ❌ Markdown 标题/粗体（IM 客户端按字面渲染）
- ❌ "流程规定要先付钱"（听起来官僚）
- ❌ "看了您资料觉得可能是 X 癌"（免费医疗建议 = 责任归你）
- ❌ 客户发资料后**立即下载**（没付钱 = 没授权）

**客户已付 ¥49 后的微信处理**：

| 客户动作 | 伟烨/agent 动作 |
|---|---|
| 客户付 ¥49 并发资料 | 立刻下资料（24-48h 内 cloud link 失效）→ 启动病例整理 |
| 客户付 ¥49 但只说"我想了解" | 发标准病例清单 5 项（按邮件模板） |
| 客户没付，发资料 | 资料**不下** + 用 v1.1 模板引导付款 |
| 客户说"急" | 立刻同步给伟烨："X 客户说情况急" |

### ⚠️ 对外发件邮箱选择：QQ 邮箱 vs 企业邮箱（2026-07-07 确立）

伟烨定下来：**所有给患者、给医院国际部的邮件都从 QQ 邮箱 `434338480@qq.com` 发**，不用网站企业邮箱 `contact@chinahospitalsguide.com`。

**理由**：
- 伟烨个人 QQ 邮箱是他日常用的，能在手机/电脑上直接收到回复
- 企业邮箱 `contact@chinahospitalsguide.com` 目前没有 SMTP 配置，发不出去，要走 himalaya CLI

**风险与对策**：
- QQ 邮箱对 `edu.cn` / `gov.cn` 类机构邮件，部分医院国际部 / 医生邮箱会标记"个人邮箱"进垃圾箱
- **对策**（仅在第一次发邮件 + 48 小时没回时使用）：在邮件正文加一句 *"Note: This is sent from Weiye's personal coordination mailbox for direct, fast contact. Our institutional correspondence can be reached via the same WhatsApp/WeChat number above."* —— 不主动引发对方猜疑，等真出问题才加
- **写入所有 draft 文件时**：把 `contact@chinahospitalsguide.com` 全替换为 `434338480@qq.com`
- **对外署名统一**（2026-07-07 改）：`Weiye` + QQ 邮箱 + 手号，不再用 `Team at China Hospitals Guide`

### ⚠️ 云盘链接诊断三步法（2026-07-07 新增 — Sinosend 案）

当伟烨贴一个云盘链接过来让"探测一下"时，**不要下载**，按以下三步诊断是不是真失效：

1. **HEAD 请求看响应头**（`curl -sS -I -L -A "Mozilla/5.0" URL`）
2. **不带 follow 跳转看第一跳 Location**（`curl -sS -i URL`）—— 区分是追踪器死了还是底层云盘死了
3. **带 follow 看最终 URL + HTTP code + 返回页 HTML 签名**（`curl -L -o /dev/null -w 'final_url=%{url_effective}\nhttp_code=%{http_code}' URL`）—— 如果返回 200 但页面是云盘"启动壳"（Vue 模板、有 progress 元素），说明要 JS 渲染、curl 看到的就是失效假象，要写明"链接可能没死，但 curl 看不出"

**两种常见死法**：
- **追踪器先死**（`pstmrk.it`、`mailchi.mp` 等邮件追踪服务）—— 第一跳就 404，底下云盘根本没被访问到。**对策**：解 URL 编码直接访问底层云盘 URL
- **云盘文件过期被回收** —— 302 后 200/404，但页面里没真实文件数据

**告知伟烨的措辞模板**（避免技术细节）：

> "Hi, 这个链接我探测了一下，最后返回 [HTTP code]。可能是 [过期/复制丢字符]。建议还是找客户要新链接/密码。"

不在邮件正文里说"我用 curl 解了 base64 看到了 contact@... 邮箱"这类技术细节，给伟烨一句话结论即可。

## 患者国家/居住地三元组 (2026-07-07 Maria Rios 案补强)

跨境患者常见模式：**国籍 ≠ 居住地 ≠ 影像语言**。Maria Rios 是 Colombian 公民 / Netherlands 居民 / 用 Sinosend 上传语言含 Spanish。在跨境医疗里：

- **荷兰人**可能因历史/工作原因在西班牙做过检查
- **拉美裔欧洲居民**常报告双语言
- **单一邮箱用户**可能国籍 A、签证 B、影像语言 C

模板 `templates/hospital-inquiry-email-en.md` 的 `[Country]` 槽位 **不够用**——必须拆为：

| 字段 | 填法 | 用于 |
|------|------|------|
| `[Nationality]` | 护照公民身份 | 签证申请主项 |
| `[Residence]` | 当前居住国家 | 联系方式时区、应急联络 |
| `[Phone with country code]` | 含国际区号 | 24h 联系 |
| `[Imaging language]` | 实际报告语种（不是国籍语言） | 报告附件命名 |

Maria Rios 案的正确填法：

```
- Name: Maria Rios
- Nationality: Colombian citizen
- Residence: the Netherlands
- Contact (in NL): +31 615580429
- Imaging: radiology reports in Spanish + English
```

### 当患者说"链接是活的"但 curl 返回 404（2026-07-07 Maria Rios / Sinosend 案）

伟烨偶尔会贴一个链接让我们探测，然后说"链接是活的 / 可以正常下载"。这种情况通常：

- **云盘有地理/账号限制**——新加坡节点 vs 国内节点看到不一样
- **伟烨从他自己的网络能访问**——但 ssh 出口 IP 在国外被风控
- **链接有 token，curl 没带 cookie**——患者浏览器有登录态，curl 没

**对策（不是质疑伟烨，而是给医院写邮件留余地）**：

1. **承认伟烨的判断**——链接可下就按可下处理
2. **在唐都邮件里这样写最稳**：

   > "DICOM images ready to upload via your secure portal upon indication. A temporary sharing link is available for your convenience: [URL]. If this link is restricted on your network, please advise your standard encrypted upload portal and we will re-upload immediately."

3. **如果唐都回信说"链接打不开"**——立即用 SendGB（5GB 免费）/ 微信文件助手（单次 2GB 上限，分卷）/ 重新问伟烨要 Sinosend 密码再触发

不要在邮件正文里写"链接挂的概率挺大"——那是 agent 内部诊断，不告诉医院。也不要说"这是患者给的，我没验证过"——显得不专业。

## 双邮件同发模式（Maria 确认 + 唐都询单同时发）

当 patient 已经回信确认（接受 ¥399 case-sharing），下一动作常常是**两封邮件同时发出**：

- **邮件 A** → 给 Maria，确认她的临床答复 + 重申接机不含 + 给出 2-3 天承诺 + 案例分享恳请
- **邮件 B** → 给唐都，带上她最新临床数据 + CC Maria

**这两封邮件的关系**：

- A 引用 B："We have already prepared a formal inquiry to ... and we will send it today"
- B 引用 A 的 CC："You will see this email in copy because we just acknowledged it to the patient"
- 两封邮件的承诺时间窗口必须一致（2-3 天，从发邮件那一刻起算）
- **顺序**：先发 B（唐都）还是先发 A（Maria）？**先发 B（唐都）**——倒计时从唐都回信起算，越早发医院越早回。先告诉 Maria"已发"再发医院，会让 Maria 焦虑等待 + 唐都那边我们晚了 1 小时。

**commit 时把这两封邮件作为一组**存到一个 md 文件（如 `draft-final-round-maria-and-tangdu.md`），commit message 里说明两封的承诺时间起点。

## 倒计时承诺的内部追踪（commit log + 文件清单）

每次对外承诺"X 个工作日内反馈"时，**内部动作**：

1. **commit message 写明**承诺起点 + 截止日期 + 节点动作（"T+1 提醒 / T+3 主动同步"）
2. **写一个 `*PIPELINE-CHECKLIST.md`** 文件到仓库根目录，覆盖整个倒计时周期（链接修复、下载、询单、状态同步、升级动作）
3. **Day 1 触发**给伟烨发"X 已发 / 等 Y 回"提示（不是催，是同步）
4. **Day 3 末触发**主动起草一封"进度同步"邮件给 Maria，**不管医院是否回**——主动沟通比沉默好

Maria Rios 案已经这样执行过（commit `e994e67` + `MARIA-RIOS-PIPELINE-CHECKLIST.md`），下次同类案件直接复用这个流程。

## 飞书消息体长度限制（2026-07-07 Maria Rios 邮件断层案）

Feishu 渲染长 Markdown 邮件时会截断显示。伟烨的口头禅是"邮件后面断层了"。**对策**：

- 起草时主动监控邮件正文长度。**超过 ~2800 字**就拆成 2 段以上分别贴出来
- **拆分标记**：第一段尾 `--- This is part 1 / 2 ---`，第二段 `--- This is part 2 / 2 ---`
- 如果是同一封邮件的两段，**用同一标题但不重复正文开头**——直接接续
- 另一种处理：把整封邮件存为文件路径告诉伟烨，让他在终端 cat 完整版——但伟烨偏好飞书内一次性看到，所以**优先拆段发送**

Maria Rios v3 邮件就是这个原因拆过一次（"A mix of written notes..." 后被截断）。

## 跨境支付受限客户：特殊 case（2026-07-24 新增 — 巴基斯坦案）

### 触发场景

客户来自 **PayPal / 国际信用卡收款受限** 的国家：
- 巴基斯坦（PayPal 全境不可发款）
- 部分中亚 / 非洲国家（外汇管制 + 国际制裁规避）
- 部分中东国家（部分银行不接国际信用卡）

**客户典型反应**："我们这里没法用 PayPal，怎么办？"

### 不能做的事

- ❌ **不要硬推 PayPal** —— 客户试了不行会更焦虑
- ❌ **不要承诺"我们想办法收到你的钱"** —— 跨境支付管制在 agent 层面无解
- ❌ **不要给"灰色路径"**（西联 / 地下钱庄 / 加密货币）—— 不合规

### 应该做的事

**思路转变**：客户到中国后，跨境支付管制**自动失效**（他在中国境内用中国支付工具）。

```
┌─────────────────────────────────────────────────────────────┐
│  海外客户 → 跨境支付管制 → 限制付款                           │
│        ↓                                                    │
│  客户抵达中国境内 → 切换为中国支付工具（WeChat Pay / Alipay）│
│        ↓                                                    │
│  ¥399 / $399 协调费可正常收款                                  │
└─────────────────────────────────────────────────────────────┘
```

### 业务模型（巴基斯坦案确立）

| 项 | 决策 | 风险归属 |
|---|---|---|
| 服务档 | $399 全包协调 | 客户付费意愿 = 服务价值 |
| 接机 | 不包（单独算） | 客户自费 |
| 医院对接 | 我们承担（提前启动） | **伟烨承担** |
| 付款时点 | 客户到中国开始治疗后付 | **伟烨承担不来的风险** |
| 收款方式 | 客户在中国用 WeChat Pay / Alipay 转账 | 跨境管制失效，正常收款 |
| 案例分享 | 做好可半价（$399 → $199.5） | 激励分享 |

### 微信模板（核心 1 段版 · 伟烨偏好长文浓缩）

**完整 5 段版**：`~/chinahospitalsguide/templates/wechat-pakistan-2026-07-24.txt`

```text
Hi — we understand PayPal isn't available in Pakistan; that's not 
something you can work around. So here is what we offer you:

1. We start coordination now, at our cost. No upfront payment. 
   We review your file, identify 2-3 hospitals, set up video 
   consultations, prepare documents and visa letters.

2. The $399 coordination fee is paid by you after you arrive in 
   China and start treatment — via WeChat Pay or Alipay on the 
   ground, which works normally inside China.

3. Airport pickup and local transport are not included; we can 
   introduce a local partner for that, billed separately to you.

If you also agree to let us record your journey (anonymized — no 
real name, hospital, or city without your explicit consent), we 
cut the $399 to $199.5. Sharing is optional.

If yes, please reply with: (1) your diagnosis and stage, (2) 
where you're currently being treated, (3) rough timeline for 
flying to China. We'll send you a written specialist evaluation 
within 4 business days, with no payment up front.

Weiye
China Hospitals Guide
```

### 风险评估（伟烨心里要清楚）

| 风险 | 可能性 | 影响 |
|---|---|---|
| 客户付了款后不来中国 | 低（签证邀请函已签） | 损失医生沟通时间 |
| 客户来了但拒绝付款 | 中（无强制机制） | 损失 ¥0 + 前期成本 |
| 客户提前付款（亲属代付） | 低 | 解决 |
| 客户本国法规变化允许 PayPal | 极低 | 解决 |

**伟烨已接受"客户不来 = 白干"风险**（2026-07-24 明确）。这一模式**不是默认**，**仅用于跨境支付不可行的国家客户**。

---

## 英文微信 IM 节奏规则（2026-07-24 确立）

### 触发场景

客户是海外（英文 / 俄语 / 印尼 / 阿语），需要用对应语言微信沟通。

### 与"中英微信翻译"的差异

| 维度 | 中文微信模板 | 英文微信 IM |
|---|---|---|
| 节奏 | 中速（客户可读长段） | **快速**（英文 IM 比中文更直接） |
| 客气 | "您好，看到您..." | ❌ 不写 "Hi, hope you're doing well..." |
| 句式 | 完整句子 | **短句 + 缩略**（有时态压缩） |
| emoji | 🙏 单个 | ⚠️ 看客户习惯再定（不要默认） |
| 段落 | 2-3 句 | 1-2 句（IM 节奏不允许长段） |

### 翻译起点（不要走邮件→压缩）

❌ **错路径**：先写"完整英文邮件" → 压缩到 IM 节奏 → 失去自然感
✅ **对路径**：直接用 "WhatsApp/WeChat 英文 IM" 节奏写，**不参考邮件模板**

### 关键英文 IM 措辞（vs 中文微信）

| 中文 | 英文 IM 版 |
|---|---|
| "您好，看到您发的资料了" | "Hi — got your update" / "Saw your message" |
| "您愿意主动找我们" | "Thanks for reaching out" |
| "我得先跟您把话说清楚" | "Quick context" / "Want to be upfront" |
| "我们这边的标准流程是这样的" | "Here's how we work:" |
| "您可以看下我们的套餐说明" | "Quick link: https://..." |
| "辛苦您再等等" | "Thanks for your patience" |

---

## 复制框设计规则（2026-07-24 强化 — 巴基斯坦案）

### 触发场景

伟烨需要把微信消息 / 邮件正文从飞书**复制到翻墙机微信 / 邮箱客户端**发送。

### 用户强偏好（2026-07-24 原话）

> **"只发内容就行了，其他不用说了"**

### 复制框标准结构

```
[飞书对话顶部：1-3 行"复制规则"提示]
   ⚠️ 复制规则：
   - ✅ 只复制下面虚线框之间的内容
   - ❌ 不要复制虚线框本身
   - ❌ 不要复制上方/下方的中文说明
   - ❌ 不要复制分隔符 "---"

[虚线框开始 ↓]
   Message 1: [内容]
   Message 2: [内容]
   Message 3: [内容]
[虚线框结束 ↑]

[飞书对话底部：1-2 行"怎么用"提示（可选）]
```

### 触发场景对应的格式

| 伟烨说 | 飞书对话产出 |
|---|---|
| "直接发我" / "内容发我" / "只发内容" / "一段发给我" | **直接贴内容**，标"Message N: ..."，**不带虚线框** |
| "起草一下" / "你审一下" / "你帮我看下" | **完整复制框**（带"复制规则"提示 + 虚线框 + 怎么用） |
| "帮我改某条" | **改后直接贴修改版**，标"Message N (改)：..." |

### 不要做的事（违反偏好）

- ❌ 复制框外面写"以下是..."、"上面是..." 引导词
- ❌ 复制框里夹"⚠️ 伟烨这个号是不是打多了" 客服附注
- ❌ 在框内加 emoji 装饰边框
- ❌ 任何"待办 / 待你确认"信息进框内 —— 写飞书对话独立消息

---

## 多语种微信版本管理（2026-07-24 确立）

### 触发场景

同一个客户沟通场景，需要英文 / 印尼语 / 俄语 / 阿语 / 中文 5 个版本。

### 翻译起点策略

| 目标语言 | 翻译起点 |
|---|---|
| 英文 | 中文微信 v1.1 → 直接英译（IM 节奏，不是邮件） |
| 印尼语 | 中文 v1.1 → 英译版 → 印尼语（保持 IM 节奏） |
| 俄语 | 中文 v1.1 → 俄语（不参考英文，因俄语客户画像不同） |
| 阿语 | 中文 v1.1 → 阿语（**注意 RTL 排版**） |

### 各语种客户画像（影响措辞）

| 语言 | 客户特征 | 措辞微调 |
|---|---|---|
| 中文（台湾/港澳） | 价格敏感，正式称呼 | "先生 / 女士" |
| 印尼语 | 宗教敏感（穆斯林多） | 避开猪肉/酒精相关内容 |
| 俄语 | 西方医疗对比意识强 | 多提"vs Germany / Israel" |
| 阿语 | 沙特 / 阿联酋，宗教敏感 | 清真食品、宗教服务需提及 |
| 英语（通用） | 国际患者通用 | 不指定国家 |

### 模板文件命名约定

`~/chinahospitalsguide/templates/wechat-<场景>-<语种>-<日期>.<ext>`

**不在文件名里加版本号 v1.1**（避免文档迭代时名字混乱）—— **迭代历史写进 reference**。

---

## 三档服务定价架构（L1/L2/L3 · 2026-07-24 确立）

**完整规划**：`~/chinahospitalsguide/planning/pricing-redesign-2026-07-24.md`

**关键决策**：**新增 $149 咨询档**（L2）作为"价值试金石档"——客户付出够轻的钱拿到具体交付物（医院问询 + 问询摘要），自然升级到 $399。

| 档位 | 价格 | 交付物 |
|---|---|---|
| L1 自助 | $49 | 通用 PDF 报告 |
| L2 咨询 | **$149 新增** | 1 次医院问询 + 问询摘要 |
| L3 协调 | $399 | 全程协调 + 落地陪同 |

**触发服务流程改造的判断标准**：见 SKILL.md "服务流程改造触发器"段。

---

**文档维护**：medical-tourism-client-intake skill · v1.5.0 · 2026-07-24
**作者**：Hermes Agent