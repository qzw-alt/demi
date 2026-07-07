---
name: medical-tourism-client-intake
description: "处理国际患者来华就医咨询的全流程：接收邮件 → 分析病情 → 确定服务方案 → 与医院初步沟通 → 回复客户。适用于 chinahospitalsguide.com 的客户咨询处理。"
version: 1.2.0
author: agent
tag: [medical-tourism, client-intake, hospital-coordination, email, whatsapp, payment-flow, case-sharing]
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

Maria Rios 案的翻车点：她的影像报告是"original Spanish + English translation"形式，结果被默认填成了 Spain/Spanish，发了 3 封邮件后才被伟烨纠正——她实际是 **荷兰人（Dutch / Netherlands）**。

**规则：**
- **永远以伟烨明示的国籍为准**。患者邮件里没有明示 → 在飞书对话里问伟烨确认，不要自己推
- **不要凭"报告里有 X 语言"就推断她是 X 国人**。在跨境医疗里：
  - 荷兰人可能因旅游/工作/历史原因在西班牙做过检查
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
8. **飞书消息体长度限制** — 邮件正文超过 ~3000 字时，飞书渲染会截断显示。伟烨会说"邮件后面断层了"。对策：起草时主动把超长邮件拆成两段分别发，第一段"This is part 1 / 2"，第二段"This is part 2 / 2"；或者直接告知"邮件较长，已拆开发送，复制时请按顺序拼接"
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

## 增量主题索引（2026-07-07 补强）

为方便未来 agent 快速定位同类场景，正文分散在下方各 ⚠️ 段落里：

- **云盘链接诊断三步法** — `### ⚠️ 云盘链接诊断三步法（2026-07-07 新增 — Sinosend 案）`（HEAD → 跳第一跳 → follow all）
  - 可重跑脚本: `scripts/probe-cloud-share-link.sh "<URL>"` —— 把整套诊断命令打包好，下次有患者链接过来直接跑
- **患者说"链接是活的"但 curl 看不到** — `### 当患者说"链接是活的"但 curl 返回 404`
- **国家/居住地/影像语言三元组** — `## 患者国家/居住地三元组`
- **双邮件同发模式（Maria + 唐都 同步）** — `## 双邮件同发模式`
- **倒计时承诺追踪（commit log + checklist）** — `## 倒计时承诺的内部追踪`
- **飞书消息体长度限制** — `## 飞书消息体长度限制`

## 注意事项

- 患者的DICOM文件通常很大，建议提供云盘链接接收；**云盘链接 24-48h 内下载**
- 回复邮件时保持邮件线程（Re: 主题），不要新建线程
- 涉及May Thurner等并存疾病时，一并询问医院的治疗方案
- 不要承诺医院一定能治疗——先让医院评估
- 不要在没有用户确认的情况下直接发送邮件
- 如果服务器没有配置SMTP，把邮件正文写出来让用户手动发送
- 案例合作模式下，不要告诉医院"这是免费患者"，按标准 ¥399 case 跟医院对接

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