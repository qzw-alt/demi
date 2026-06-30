# Payment Flow Architecture — chinahospitalsguide.com

Confirmed 2026-06-30 (德米). Two parallel entry paths for every user.

## Core Architecture: Two-Path Journey

```
USER arrives on any page (index / services / how-it-works / contact)
                     │
        ┌────────────┴────────────┐
        ▼                         ▼
   PATH A (不确定)            PATH B (已决定)
   "填表咨询"                 "直接支付"
        │                         │
        ▼                         ▼
   contact-new.html          pricing.html
   (填入病例详情)              (选择套餐)
        │                         │
        ▼                         ▼
   成功页面                    PayPal按钮
   「Choose Package          ¥49 → ID: K4HNCDD7GDS5C
    & Pay →」                ¥399 → ID: ZBY36JV2X5A3U
        │                         │
        └────────┬───────────────-┘
                 ▼
         等待我们确认付款
          → 进入服务流程
```

**PATH A** — "不确定/先填表"：用户填写 contact-new.html 的病例咨询表单 → 提交后看到成功页，含金色「Choose Package & Pay →」按钮指向 pricing.html → 我们收到邮件后审阅推荐 → 用户付钱 → 我们开始服务

**PATH B** — "已决定/直接付"：用户直接去 pricing.html → 选择 ¥49 或 ¥399 → PayPal 支付完成 → 通过「Already paid? Open the intake form」链接回到 contact-new.html → 我们收到付款后启动服务

## Page Requirements (payment entry points)

Every page that describes the service MUST offer both paths:

| Page | Path A (form) | Path B (direct pay) | Status |
|------|--------------|---------------------|--------|
| index.html | Hero「Start Free Case Review」✅ |「View Pricing」✅ | OK |
| index.html 套餐区 | — |「View Pricing」✅ | OK |
| services.html |「Start Review」✅ |「See Pricing」✅ | OK |
| how-it-works.html |「Submit Your Case →」✅ |「View Pricing & Pay」✅ | OK (fixed 2026-06-30) |
| contact-new.html | 表单本身 ✅ | 侧边栏「Pay Now →」金色卡片 ✅ (fixed 2026-06-30) | OK |
| contact-new.html success | — |「Choose Package & Pay →」金色按钮 ✅ (fixed 2026-06-30) | OK |
| contact.html | 旧版联系页 ✅ |「Go to Pricing」✅ | OK |

## The contact-new.html Success Message Pattern

After form submission, the success message MUST show:

1. **"Case submitted ✅"** + checklist (check email, 1 biz day reply, WhatsApp urgency)
2. **"Already know which package you need?"** divider
3. **Golden CTA button** → `pricing.html` with text "Choose Package & Pay →"
4. **Secondary actions**: Back to Home (neutral), Message on WhatsApp (green)

CSS for the payment button: `background:linear-gradient(135deg,#b78a42 0%,#d4a84b 100%)` (gold, matching the brand accent)

The success message slides into the form area via JS: `document.getElementById('successMessage').classList.add('visible')`.

## The contact-new.html Sidebar Pattern

The sidebar panel "What happens after you submit" was redesigned on 2026-06-30 to show two clear paths:

1. **Blue card** (f0f6ff bg, #1e3c72 heading) — "✅ Not sure yet — Let us review your case first"
   - Text: "We review your case details, recommend the right package, and guide you on next steps."

2. **Gold card** (fff8ef bg, #e8d5a8 border, #b78a42 heading) — "💰 Already know which package you need — Pay directly"
   - Text: "Go straight to pricing, choose your package, and pay with PayPal. Return here after payment if needed."
   - Has a golden "Pay Now →" button linking to pricing.html

## Audit Checklist (run when adding new pages or modifying existing ones)

- [ ] Page mentions the service? Must have BOTH paths visible
- [ ] Path A target: `contact-new.html` (or contact.html if legacy)
- [ ] Path B target: `pricing.html`
- [ ] Button/link text is action-oriented: "Pay Now", "Choose Package & Pay", "View Pricing & Pay", "Go to Pricing" — never just "See More"
- [ ] Golden color (#b78a42 / #d4a84b gradient) for payment CTAs — signals "this is a money action"
- [ ] No dead-end success pages — every form submission ends with a link to pricing.html

## Payment Methods

| Package | Price | PayPal Button ID | Page |
|---------|-------|-----------------|------|
| Hospital Match & Plan | $49 USD | K4HNCDD7GDS5C | pricing.html (line 298) |
| Pre-Arrival Coordination | $399 USD | ZBY36JV2X5A3U | pricing.html (line 322) |

PayPal SDK loaded in pricing.html with client ID: `BAAuEJ4aj4Glmel3a35W5yg1QY9idTSZt5LkxbWG-z5pvfIMEyG8E6vnCCLJNynRoAVW6XjqCCtnSKBzEY`

Post-payment flow: pricing.html shows "Already paid?" section → links to `contact-new.html?paid=1&package=...&source=pricing` → contact form prefills package and shows payment-detected banner.

## Important: Fee Flow explained to customers

- ¥399 → paid to us (coordination service fee)
- Hospital treatment costs → paid directly to hospital, not through us

Always explain this distinction when writing to customers who ask about payment.
