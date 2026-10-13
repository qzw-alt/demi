# 香港 Stripe 申请合规评估 — chinahospitalsguide.com

日期: 2026-09-21 · 评估对象: 以香港主体申请 Stripe 收款 · 结论级别: 可申请（有条件通过）

## 一句话结论

医疗旅游 / 医疗协调服务**不在** Stripe 禁止清单上，可以申请。但它落在"受限行业（需额外尽调）"的边缘 —— 医疗 + 跨境 + 高客单 + 退款风险。能不能过审，取决于两件事：

1. 香港主体是否真实落地（注册地址 / 电话 / 香港实体银行账户）
2. 网站怎么描述业务性质（现有 MDT Review 页措辞有被判成 telemedicine 的风险）

---

## 1. Stripe 香港的硬性门槛（每条都是必须有）

| # | 要求 | 来源 |
|---|---|---|
| 1 | **香港注册实体**（有限公司或个体户）—— Stripe 香港服务协议：只有"位于香港的企业（含个体）"可开户 | Stripe HK Services Agreement |
| 2 | 商业登记号 **BRN**（个体户无 HKID 时必须有 BRN） | Stripe Support（HK requirements） |
| 3 | 香港本地**实体地址**（能收信，不能是 PO Box）+ 香港电话 | Stripe Support（another-country requirements） |
| 4 | 董事/实控人**政府签发身份证件**（护照即可，不需要 HKID） | 同上 |
| 5 | **能正常展示业务的网站**（英文站 OK，现有站达标） | 同上 |
| 6 | 香港本地**实体银行账户**收提现 —— Stripe 明确"不能是虚拟银行账户" | 同上 |
| 7 | 申请时填写的业务描述必须和网站实际内容一致 | Stripe 禁止项（虚假/误导信息） |

> 第 6 条最容易踩坑：Airwallex / Payoneer / Wise 这类第三方账户不要指望当提现账户。要汇丰、中银香港、恒生这类实体银行账户。内地董事 2026 年可走汇丰"大湾区企业账户通"在内地分行视频见证开户。

## 2. 我们的业务在不在禁止/受限清单上

**禁止清单（绝对不能做）**：没有"医疗旅游 / 医疗协调"这一项。

**受限清单（要额外尽调，可能不批）**：跟我们最近的三个词条——

| 词条 | Stripe 原文要点 | 对我们的影响 |
|---|---|---|
| Pharmaceuticals, medical devices and telemedicine | 含 "Telemedicine and telehealth services" | ❗最高风险项，$499 MDT Review 视频问诊措辞要改 |
| Travel | "Travel reservation services and clubs" | 别把自己写成旅行社/预订服务 |
| 美国辖区专项禁止 | "Medical benefit packages not offered by a government or health insurance company" | 对香港主体不直接适用，但用词避免 "medical benefit package" |

**禁止项里的两条硬红线（触犯直接封号）**：

- Peer-to-peer money transmission
- Third-party agents: "receiving settlement proceeds for goods or services that you did not provide"

→ 永远不要代收/代付治疗费。网站上"治疗费直接付医院"的表述必须保持。

## 3. 网站需要改的 4 处措辞（这是过审关键）

1. **MDT Review ($499)** — 现在写 "panel reviews your case" + "video consultation with the panel"。改成"我们 **organise/arrange** 医院专家组评审；评估和视频由 **医院的 specialists** 提供"，我们只负责安排、翻译、随访解读。全站避免 "we provide medical advice / we diagnose / online consultation"。
2. **"package" 一词** — $199/$649 描述成 "coordination and information service"，不要用 "treatment package / medical benefit package" 把治疗和套餐绑在一起。
3. **Travel 措辞** — 不提 travel agency / tour booking。Airport pickup 写成 "we arrange a local transfer on your behalf"（代安排，不是提供旅行社服务）。
4. **保持现有的诚实口径** — "no hospital commissions"、"we don't promise outcomes"、"treatment costs paid directly to the hospital" 这些在尽调时是**加分项**，不要为了转化率删掉。

## 4. 申请时怎么填

- 行业描述：`Professional services — medical travel coordination & information services`（不要选 healthcare / medical clinic）
- URL：`https://chinahospitalsguide.com`（必须能打开且看得到价格与服务说明）
- 产品描述：逐档写清交付物 + 交付时间 + 退款规则（pricing 页 refund terms 已具备）
- Statement descriptor：建议 `CHINAHOSPITALS` 或 `CHGUIDE`（5–22 字符，不能含 `< > ' "`），并在网站写明客户账单上会看到这个名字 → 显著降低拒付率
- 备料：BR 证、公司注册证、董事护照、香港地址证明、银行账户证明、pricing 链接、refund 链接

## 5. 费用与拿钱

- 收单：香港卡 **3.4% + HK$2.35/笔**（官网价）
- 国际卡另有加价（官网 "additional fees" 折叠项；第三方口径约 +1%），非 HKD 结算再 +2% → 国际客户每笔粗算 4.4%–5%（$649 约 $29–32）
- 提现：支持 HKD，也支持 USD settlement 到香港美元账户
- 对比现有 PayPal NCP（站上 4 个按钮）：费率量级接近；Stripe 的增量价值 = 本地收单 + Apple/Google Pay + API/订阅 + 退款对账更顺

## 6. 主体真实性红线（比什么都重要）

- ❌ 不能用别人的香港公司 / 借别人银行账户收款 → Stripe"虚假或误导信息"禁止项，封号 + 进 Mastercard MATCH 黑名单（全行业收单 5 年受影响）
- ⚠️ 香港公司不能纯壳。香港利得税首 200 万港币 8.25%、其后 16.5%；离岸豁免 2026 年税局查得很紧，别按"注册就免税"规划 —— 找香港持牌会计师定，这不是我能下的判断

## 7. 香港主体成本（2026 实际政府价）

| 项 | 金额 |
|---|---|
| 公司注册处电子成立费 | HK$1,545 |
| 商业登记证（2026/27 年度） | HK$2,200 + 徵费 150 = HK$2,350 |
| 法定合计 | ≈ HK$3,895 |
| 秘书 / 注册地址 / 审计代理年费 | 数千至一万港币级（按代理报价） |
| 时间 | 注册 1–3 天（电子）；银行开户 2–6 周；Stripe 审核数天（可能补件） |

## 8. 并行通道建议

- **保留 PayPal**（现有 4 个 NCP 按钮不动）→ 双通道，客户按国家自己选
- Airwallex / Checkout.com：香港主体可申请，风控口径不同
- 高风控备用：2Checkout / Verifone、Oceanpayment
- ❌ 任何"包过"的第三方代开 / 共享 Stripe 账户 —— 就是 MATCH 黑名单的来源

## 9. 顺带一条（Stripe 不管，但是另一条线）

患者病历属敏感个人数据：香港 PDPO，欧盟客户（Maria / Elspeth）还涉及 GDPR。网站隐私政策要写清收集范围，**付款页 / Stripe 结账页绝不传病历**，病历走邮件或云盘。

---

## 行动顺序

1. 定主体：香港有限公司 + 秘书/地址 + 银行账户（开户可并行启动）
2. 先改网站 4 处措辞（文案我出，工程改动你拍）
3. 材料一次齐再递 Stripe 申请
4. PayPal 保留为并行通道

## 来源

- Stripe HK 服务协议（eligibility：仅香港本地企业）
- https://support.stripe.com/questions/requirements-for-hong-kong-based-businesses
- https://support.stripe.com/questions/requirements-to-open-a-stripe-account-in-another-country
- https://stripe.com/en-hk/legal/restricted-businesses （Last updated 2026-05-13）
- https://support.stripe.com/questions/stripe-atlas-restricted-business-categories （"Unregulated health services"）
- https://stripe.com/en-hk/pricing
- https://docs.stripe.com/get-started/account/checklist
- 香港税务局商业登记费表 2026/27：https://www.ird.gov.hk/chi/pdf/brfee_table.pdf
- 公司注册处收费：https://www.cr.gov.hk/tc/services/fees.htm
- InvestHK 税制（两级制 8.25% / 16.5%）
