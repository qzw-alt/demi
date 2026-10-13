# 香港主体 — 公司名称 与 业务性质（"经营范围"）建议

日期: 2026-09-26 · 关联: `planning/stripe-hk-eligibility-2026-09-21.md` · 级别: 建议稿（公司名查册 + 章程条款由秘书/会计师定）

## 0. 一句话

香港**没有"经营范围"这个概念**——能填的只有三处：①公司注册处（无此栏，默认无限定）②商业登记证上的「業務性質 / Nature of Business」（自由文本，银行和 Stripe 都看这张）③Stripe/银行的开户表。名字推荐 **China Hospitals Guide Limited**（中文名可选「中國醫院指南有限公司」），业务性质推荐 `Cross-border medical coordination and information services`。

---

## 1. 名称候选

| # | 英文名 | 配对中文名（可选） | 优点 | 代价 |
|---|---|---|---|---|
| 1 ⭐ | **China Hospitals Guide Limited** | 中國醫院指南有限公司 | 与 chinahospitalsguide.com 完全对齐 → Stripe 尽调"公司名 = 网站品牌"零解释；"Guide" 天然是信息/指南定位，不是医疗机构 | 含 "Hospitals"，开户经理会多问一句 |
| 2 | China Medical Access Limited | 中國就醫通道有限公司 | "Access" 最贴近我们实际卖的东西（通路 + 安排） | 含 "Medical"，同样多问一句；"Access" 偏营销 |
| 3 | China Medical Coordination Limited | 中國醫療協調有限公司 | 最直白，与 BR 业务性质同款措辞，银行/Stripe 一眼看懂 | 名字长、品牌感弱，像 B2B 服务商 |
| 4 | Chinahospitalsguide Limited | — | 100% 域名同款（Stripe 零摩擦） | 18 个字母连写，念不出、开户填表易打错 → 不建议 |

**零医疗词的备选**（若开户行/Stripe 对医疗字眼明显敏感）：`Chinaguide Services Limited`、`Sino Patient Support Services Limited`。

**决定逻辑**：优先保品牌一致性（选 1）；若银行面谈明确对 "Hospitals" 有顾虑 → 落到 3（"Coordination" 是 Stripe 尽调最想听到的词）。

## 2. 命名硬规则（已核 CR《香港公司名稱註冊指引》）

- 英文名最后必须 `Limited`；中文名最后四字必须 `有限公司`；**一个名字里不能中英混写**；中文必须繁体
- 可只注册英文名（省事），也可英文 + 中文各一
- 名称与《公司名稱索引》既有名称相同 → 不批；"过于相似" 也会被挡
- **需注册处处长事先批准的词**（Cap. 622A）: chamber of commerce / kaifong / levy / savings / **tourist board** / **tourist association** / trust / trustee（中文：商會、街坊、徵費、儲蓄、旅遊協會、旅遊發展局、受託、信託）→ 我们一律避开
- **其他法例禁止使用的词**：Bank(銀行) 需金管局同意；insurance / assurance / 保險 需保监局同意；交易所；"certified public accountant / CPA / 會計師 / 核數師" 等专业头衔；暗示官方关联的 "committee(委員會)" 一般不批
- 避免 `Travel` / `Tour` / `Tourist` 类词：①无旅行代理商牌照不得经营 travel agent business（《旅遊業條例》Cap. 634 s.4 — 代订离港/来港交通、香港或境外住宿、观光餐饮购物行程都在定义内）②Stripe 把 Travel 列为受限类目
- 避免 `Group` / `Holdings` / `International` 这类虚词：无实际业务支撑，"Group" 会让银行追问集团架构
- "Medical / Hospital / Clinic" **不在** CR 受限清单上（已核，清单里没有医疗类词），但放进名字就要准备好回答"你们有执业牌照吗"

## 3. 业务性质（BR「業務性質」）推荐写法

- 首选：`Cross-border medical coordination and information services`
- 更保守：`Business coordination, interpretation and advisory services`
- 中文：`跨境就醫協調及資訊服務`（繁体）
- BR 字段较短 → 以一句为限；写不下的补充内容放银行开户表
- 可后续修改（IRD 改业务性质不需重注册公司）

**银行开户 / Stripe 尽调展开版（标准答案，直接可用）**：

> We provide cross-border medical coordination and information services for international patients seeking treatment in China. Our services are (1) case-file translation and transmission to hospitals, (2) arranging appointments and specialist reviews with hospital teams, (3) medical interpretation and accompaniment, (4) arranging local transfer and accommodation on the patient's behalf, and (5) post-discharge follow-up coordination. We do not provide medical advice, diagnosis or treatment. All treatment is provided and charged by the hospitals directly; we never receive or transmit treatment fees.

这段话同时覆盖 Stripe 两条硬红线：不诊疗（避开 telemedicine）、不代收代付治疗费（避开 third-party agent / money transmission）。

## 4. 公司注册处：不写"经营范围"

- 香港公司**无经营范围栏**；默认可从事任何合法业务
- **不要**为了"写经营范围"在章程细则里加收窄的 objects clause —— 将来加业务线就要改章程
- → 保留标准章程（unrestricted objects），**由秘书确认**（属公司秘书/律师意见范围）

## 5. 不要写进任何表/网站的词

`treatment package` · `medical benefit package` · `telemedicine / telehealth` · `online consultation` · `travel agency` · `tour booking` · `代收治疗费 / 代付医院款`

Stripe 行业类目：`Professional services — medical travel coordination & information services`（**不要**选 healthcare / hospital / clinic / telehealth）

## 6. 定名后要同步的 5 处

1. 网站页脚 legal 名（现在站上没有主体名，正好一次写对）
2. Stripe account name + statement descriptor（建议 `CHINAHOSPITALS`，与公司名一致可降拒付）
3. 银行账户名
4. 发票 / 收据 / 退款条款页面署名
5. 隐私政策里"数据控制者"主体名（PDPO；欧盟客户还涉 GDPR）

## 7. 待办

- [ ] 名称查册：CR 电子服务网站「以全名查冊」**免费**，英文名 + 中文名分别查（中文用繁体）；一次查 3–5 个备选并排序（被占就往下走，别等）
- [ ] 秘书确认：章程 objects clause 是否保持无限定
- [ ] 会计师确认：利得税 / 离岸豁免（不由 agent 下结论）
- [ ] 商标：公司名注册 ≠ 品牌保护；建议同时向香港 IPD 申请商标（费用提交前核实现价）

## 来源

- CR《香港公司名稱註冊指引》(Guide_RegCompName-e.pdf, updated May 2025)：https://www.cr.gov.hk/en/companies_ordinance/docs/Guide_RegCompName-e.pdf
- CR 常见问题 — 公司名称（免费全名查册）：https://www.cr.gov.hk/tc/faq/local-company/company-name.htm
- Companies (Words and Expressions in Company Names) Order (Cap. 622A)
- TIA — 旅行代理商牌照 / Cap. 634 s.4 定义：https://tia.org.hk/en/licensing/travel-agents.html
- 商业登记「業務性質」：HSBC Business Go — Nature of Business in Hong Kong
- Stripe 受限行业清单与香港门槛：见 `planning/stripe-hk-eligibility-2026-09-21.md`

---

# 8. ⚠️ 2026-10-10 更新 — 第 1 顺位作废，改为「注册名中性 + 品牌/商标保留」

**触发**：伟烨已向秘书公司缴费、公司准备开起来，要求替掉 "Hospital" 字眼。

**§1 表格里的第 1 顺位 `China Hospitals Guide Limited`（含中文「中國醫院指南有限公司」）不再推荐。** 见 skill 参考文件 `medical-tourism-client-intake/references/hk-entity-setup-naming-and-business-nature.md` 的 §1.5（含完整替代名表 + Cap. 633 依据 + NNC2 改名程序）。

**新推荐**：
- **公司注册名（中性）**：`China Health Guide Limited`（中國健康指南有限公司）；开户行若仍敏感 → 退到 `China Medical Coordination Limited`（中國醫療協調有限公司）
- **对外品牌 / 商标**：保留 **China Hospitals Guide**，另行向香港 IPD 申请商标

**关键区分**：公司注册名会出现在合同、发票、银行账户、Stripe 主体上 → 必须中性；网站域名/品牌里的 "hospitals" 是描述性内容 → 可以保留。

**法规依据（已核）**：《私營醫療機構條例》(Cap. 633) 明文规定日間醫療中心**不得**、診所**未經衛生署署長書面批准不得**，在名稱或描述中使用「醫院」或 "hospital"（或相類詞語）。我们不属该条例持牌主体、CR 层面注册得下来，**卡点是银行 KYC 与支付通道**。

**改名程序（若已注册完成）**：股东特别决议（≥75%）→ **15 天内** 递交表格 **NNC2** + **HK$295** → 公司更名证明书（电子约 1 小时 / 纸本约 4 个工作日）→ **更名自证明书发出当日起生效**；**BRN 不变**，BR 名称自动更新，无额外 BR 费；**曾用名会留在 CR 记录**（部分银行会看到）。若尚未拿到公司注册证书 → 直接改，几乎零成本。

**§7 待办更新**：
- [ ] **先问秘书：公司名称是否已提交/已注册？** —— 决定"免费改"还是"走 NNC2"
- [ ] 名称查册：`China Health Guide Limited` / `China Medical Coordination Limited` + 繁体中文名，CR 电子服务网站免费查
- [ ] 确认"名称预留"是否存在（资料冲突：一说 HK$140 预留 60 天，一说香港无保留制度 → 以秘书答复为准）
- [ ] 商标查册（IPD）单独做，"China Hospitals Guide" 可注册性需另核
