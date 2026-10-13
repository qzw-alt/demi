# China Hospitals Guide — Pricing & Service Architecture Redesign

**Status**: planning draft v1.0
**Date**: 2026-07-24
**Author**: Weiye (via Hermes session)
**Trigger**: 0-revenue observation across 3 cases (Maria / Pakistan / recent cancer case)

---

## 1. The Core Problem

Three live cases, three different payment friction patterns, **zero revenue earned yet**:

| Case | Pattern | Lesson |
|---|---|---|
| Maria Rios (Netherlands, Colombia) | case-sharing free | Profile-driven cases are valuable but free |
| Pakistan patient | PayPal unavailable in country | Cross-border payment friction creates zero-revenue work |
| Recent cancer case | "Talk to me first, I'll decide" | Without a midpoint service, customers settle for free |

**Unifying cause**: there is no paid step that the customer faces AFTER they have made contact
**but BEFORE** they commit to $399. Result: every prospective customer drifts toward free consultation,
because that's the only thing available until they pay.

---

## 2. The Insight

The midpoint is not just a price. It is a **product**.

Customers don't avoid $399 because it's expensive; they avoid it because they don't yet know
whether we can deliver for their specific case. The existing $49 is a "research report" — useful
but abstract. The existing $399 is the whole thing — scary for a first engagement.

What's missing is: **a tiny, paid exchange that proves our value to THIS customer's case**.

The midpoint = us asking a hospital on the customer's behalf, and the customer seeing what comes back.

---

## 3. Three-Tier Service Architecture

### L1 — Self-Service Report  ·  $49  ·  (existing, no change)

| Element | Detail |
|---|---|
| Delivery | Generic PDF report, template-fill by condition |
| Who delivers | Automated / pre-existing content |
| Customer effort | Pays + downloads |
| Customer support | None — FAQ + email-only |
| Time to deliver | Immediate |
| What is NOT included | No hospital contact. No personalization. No answers to patient's specific case. |
| CTA inside delivery | "If you want the hospital itself to look at your case — see L2 ($149)" |

### L2 — Hospital Consultation  ·  **NEW**  ·  $149

| Element | Detail |
|---|---|
| Delivery | Weiye personally contacts one hospital on customer's behalf, asks the question the customer needs answered, returns a written summary of the hospital's response |
| Who delivers | Weiye (personally, this is the difference) |
| Customer effort | Pays + sends case summary + waits |
| Customer support | Weiye on WeChat + email, 1 business day response |
| Time to deliver | 4–7 business days |
| What is included | One specific hospital query. Customer's prepared case summary in Chinese, sent to the relevant department. Translation of the hospital's response into English. |
| What is NOT included | No further coordination. No MDT. No visa. No arrival logistics. No second hospital. |
| CTA inside delivery | "If you're ready for full coordination, see L3 ($399) — this $149 fee is deducted from $399 if you upgrade within 30 days." |

**Why this works**:
- $149 = low enough to be a "let me just check" decision
- Delivers a **concrete artifact**: written hospital feedback specific to the customer's case
- Once customer sees that artifact, upgrade to $399 is a natural progression
- Weiye's time is bounded: one hospital, one query, one summary
- The upgrade incentive (`$149 抵扣 $399`) makes L2→L3 conversion high

### L3 — Full Coordination  ·  $399  ·  (existing, with clearer boundaries)

| Element | Detail |
|---|---|
| Delivery | End-to-end coordination: case preparation → 2–3 hospital shortlist → MDT setup → video consultation → documents & visa letters → arrival logistics → post-treatment follow-up |
| Who delivers | Weiye + coordination team |
| Customer effort | Pays + engages |
| Customer support | WeChat + email + emergency phone, 4 hour SLA on business days |
| Time to deliver | 1–4 weeks depending on case |
| What is included | All L2 deliverables, plus: matched hospital network (not just one), MDT multi-department coordination, translation (case files), visa invitation letter, ground transport partner intro (separately billed), arrival accompaniment |
| What is NOT included | Hospital treatment fees. Medication. Family accommodation. Continuation support beyond the agreed case scope. |

---

## 4. Funnel Math (Hypothetical)

Reading GSC + Pakistan + recent case data, here is the expected pathway:

```
Landing Page (sg.html, id.html, ru.html, ar.html)
   ↓ "How much does treatment in China cost?"
L1 ($49) — Self-Service
   │ 80% drop here (no commitment)
   ↓
L2 ($149) — Hospital Consultation
   │ 50% convert here (the artifact convinces)
   ↓
L3 ($399) — Full Coordination
   │ 70% go through (case viability confirmed)
   ↓
Active Case
```

Without L2, the L1→L3 transition rate is ~5–10%. With L2 as a midpoint, L1→L2 is ~15–20% and L2→L3 is ~50–60%. Combined L1→L3 is ~7–12% (vs 5–10% baseline) — modest improvement on conversion but **massive improvement on zero-revenue cases**.

---

## 5. Why Customers Will Pay

The $149 works because it answers a question the customer **cannot answer themselves**:

> "If I, a foreigner with no Chinese, send my case to Beijing XX Hospital, what will they actually say back?"

That question, today, has these answers:
- (a) The customer makes 40 cold calls to international departments and gets nowhere.
- (b) They hire a medical tourism agency (often $1500–$3000 upfront).
- (c) They give up and stay with their domestic option that may be inadequate.

$149 is cheaper than (a)'s phone bill and dramatically cheaper than (b). It is also **exactly the labor cost of one hospital query** — so it isn't subsidized; it is priced honestly.

---

## 6. Service Boundaries (Hard)

The L2 service MUST NOT become free work creep. Boundaries:

| Boundary | Why |
|---|---|
| Exactly one hospital contacted | Bounded labor |
| One written response delivered | Bound the artifact |
| No follow-up questions to the hospital | Prevent "one more thing" scope creep |
| No re-query if customer misread the response | One shot |
| No advice on "what should I do with this answer" | Stay descriptive, not prescriptive |

These boundaries are explicit on the website copy and reinforced in the L2 delivery email.

---

## 7. Website Copy Outline

### Pricing Page (pricing.html)

#### Above the table: "Why This Exists"

```
You have tried calling hospitals in China. They didn't pick up.
You have asked in your own country. Nobody has done this before.
You have googled "best hospital in China for X" and got 50 ads.

We are not an ad network. We are a Chinese speaker with a phone
and 5 years of knowing which department picks up and which one
doesn't. We are the person you wish you had.

¥49 — you get a research report
¥149 — we contact one hospital on your behalf, you see what they say
¥399 — we run the whole process for you

You choose what fits the moment.
```

#### The comparison table — directly on the page

| | L1 Self-Service | L2 Hospital Consultation | L3 Full Coordination |
|---|---|---|---|
| Price | $49 | $149 | $399 |
| Hospital contact | None | 1 hospital, 1 query | 2–3 hospitals, MDT |
| Personalized to your case | No (generic report) | Yes (your summary sent) | Yes (full preparation) |
| Response SLA | None | 4–7 business days | 4 hours on business days |
| Translation | No | Hospital reply to English | All materials |
| Visa support | No | No | Yes (invitation letter) |
| Arrival support | No | No | Yes |
| Upgrade credit | — | — | $149 deducted if upgrade within 30 days |

#### Below the table: "If You Don't Know Which One To Pick"

```
Start with $49 if you are still researching.
Start with $149 if you have a specific case and want the hospital's actual answer.
Start with $399 if you are ready to fly and need everything handled.

If you are unsure — message us. We will tell you honestly which one fits.
We will not push you to the higher tier.
```

### Landing Pages (sg.html / id.html / ru.html / ar.html)

Each landing page already includes a "Top Procedures" section. Add a single sentence at the end:

> "For pricing and how we work, see [/pricing.html]."

Plus a small anchor link in the FAQ section:

> "How much does your service cost?
> $49, $149, or $399 — depending on what you need. See [the pricing page] for the full comparison."

---

## 8. Operational Add-Ons (Future)

These are not part of v1 but worth noting for Q4 2026+:

| Add-on | Description | Revenue model |
|---|---|---|
| Continued-care retainer | Post-treatment follow-up coordination monthly | $99/month |
| Family-accompaniment package | Arranging visa + lodging + hospital visits for accompanying family | $199 flat |
| Document translation kit | Translate full medical records, ongoing | $99 per case |
| Ground-transport coordination | Direct partnership with vetted drivers | commission basis |

These can be developed after L1/L2/L3 is stable.

---

## 9. Implementation Checklist

- [ ] Update pricing.html with three-tier comparison table
- [ ] Add "Why this exists" section to pricing.html
- [ ] Add FAQ anchor line to sg.html / id.html / ru.html / ar.html (4 landing pages)
- [ ] Update $49 deliverable copy in /pricing.html to make "no service" boundary explicit
- [ ] Add $149 L2 service description + CTA in CTA buttons after $49 report delivery
- [ ] Update PayPal buttons (in _data/site.json per existing schema) to support $149 endpoint
- [ ] Create email-template for L2→L3 upgrade incentive (deduct $149 from $399)
- [ ] Update wechat template bank to reference $149 as legitimate option for "talk to me first" customers
- [ ] Test funnel from each landing page → pricing → L1/L2/L3 selection

---

## 10. Open Questions (for Weiye)

1. **Hospital side load**: with L2, we are contacting hospitals **on behalf of customers who haven't paid us yet**. Is there a hospital-side cost? Should we pre-arrange letters of intent (LOI) with key JCI hospitals so we can approach without cold calls?
2. **Refund policy**: if L2 customer says "the hospital response wasn't useful," do we refund $149? My recommendation: **no refund for the labor**, but offer 50% discount on a second L2 query with a different hospital.
3. **Translation cost**: who pays for translating customer's case summary into Chinese? Embedded in $149 (since one summary) or itemized? Recommend: embedded, but if summary > 5 pages, $30 surcharge.
4. **Pakistan / cross-border unusual cases**: do we keep the bespoke "arrive-then-pay" model for customers from countries where PayPal doesn't work, or steer them to L3 with a clear "you'll pay $399 when you arrive"? Recommend: keep the bespoke model for L3 only, **never** let it apply to L1 or L2.

---

**Next step**: Weiye reviews this and either (a) approves and assigns implementation, or (b) requests specific changes.

The L2 service is the **most important addition** — without it, the same pattern of zero-revenue cases will continue.

Without L2, the business cannot sustain itself.
