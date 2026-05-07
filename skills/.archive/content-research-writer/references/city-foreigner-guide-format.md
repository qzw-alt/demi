# City-Foreigner Guide: Full Article Template

Reference implementation: `blog/how-to-see-a-doctor-in-shanghai-as-a-foreigner.html`

## Article Path Pattern
```
blog/how-to-see-a-doctor-in-{city-lowercase}-as-a-foreigner.html
```
Examples: `shanghai`, `beijing`, `guangzhou`

## Featured Image
```
images/hospitals/{city-lowercase}-city.jpg
```
Fallback: use existing image if the city-specific one is not present.

---

## HTML Shell (copy and adjust)

### Head — Adjust per article
- title: `How to See a Doctor in {CITY} as a Foreigner 2026 | China Hospitals Guide`
- canonical: `https://chinahospitalsguide.com/blog/how-to-see-a-doctor-in-{city}-as-a-foreigner.html`
- og:image: `https://chinahospitalsguide.com/images/hospitals/{city}-city.jpg`
- datePublished / dateModified: current date (YYYY-MM-DD)

### Schema Block — Article
```json
{
  "@type": "Article",
  "headline": "How to See a Doctor in {CITY} as a Foreigner",
  "datePublished": "{YYYY-MM-DD}",
  "dateModified": "{YYYY-MM-DD}"
}
```

### Schema Block — BreadcrumbList
```json
{
  "@type": "BreadcrumbList",
  "itemListElement": [
    {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://chinahospitalsguide.com/"},
    {"@type": "ListItem", "position": 2, "name": "Blog", "item": "https://chinahospitalsguide.com/blog/"},
    {"@type": "ListItem", "position": 3, "name": "How to See a Doctor in {CITY} as a Foreigner", "item": "https://chinahospitalsguide.com/blog/how-to-see-a-doctor-in-{city}-as-a-foreigner.html"}
  ]
}
```

### Schema Block — FAQPage (include 2–3 questions)
```json
{
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "Can foreigners use public hospitals in {CITY}?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Yes. Foreigners can use any public hospital in {CITY}..."
      }
    },
    {
      "@type": "Question",
      "name": "Do doctors in {CITY} speak English?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "It varies widely. Private international clinics..."
      }
    },
    {
      "@type": "Question",
      "name": "How can I register at a {CITY} hospital without speaking Chinese?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Several options exist..."
      }
    }
  ]
}
```

---

## Section Content Guide

### Kicker's template
```
{CITY} healthcare guide for expats, students, travelers, and international patients
```

### Hero H1 template
```
How to See a Doctor in {CITY} as a Foreigner
```

### Quick Answer (lead paragraph after hero)
```
<strong>Quick answer:</strong> for routine care or easier English support, many foreigners in {CITY} start with a private international clinic or hospital. For complex specialist care, advanced surgery, or high-volume clinical departments, {CITY}'s public tertiary hospitals are often the stronger option. In emergencies, go to the emergency department or call 120.
```

### Section 1 — What Makes {CITY} Easier for Foreigners
- International airport + transfer infrastructure
- Expat community size, international student population
- Hospital English-language support maturity
- WeChat-based hospital services availability
- 3–4 bullet points

### Section 2 — Public vs Private Table
| Option | Best for | Tradeoff |
|---|---|---|
| Private international hospitals/clinics | Primary care, pediatrics, routine specialist, clear English, direct billing | Higher cost |
| Public tertiary hospitals | Complex surgery, difficult diagnoses, high-volume departments | Busier, variable English, longer waits |
| Public hospital VIP/international departments | Middle ground — clinical depth + smoother experience | Depends on hospital |

### Section 3 — Good Starting Points by Need
Pull real hospitals from `api/v1/hospitals.json` filtered by `city: "{CITY}"`.
Format: `**Specialty**: Hospital Name (one-line rationale)`.
Include 3–6 hospitals covering different specialties.
End with an info-box tip about not choosing by reputation alone.

### Section 4 — How Registration Works
Step-by-step numbered list (5–6 steps):
1. Identify correct department
2. Register with passport
3. Pay consultation fee
4. Receive queue number, wait
5. See doctor, receive orders
6. Pay for ordered services, return with results

Add a paragraph about WeChat mini-programs if common in that city, or international desks.

### Section 5 — Insurance and Payment
- Direct billing (private hospitals more experienced)
- Public hospitals: pay first, claim later
- Pre-authorization requirements
- Keep all receipts and itemized invoices
- 4 bullet points

### Section 6 — Emergency Care
- Call 120 / go to nearest ED
- Hotel/residence staff can help communicate
- Carry: passport, allergy list, medication list, emergency contact
- Call insurance assistance hotline ASAP
- Do NOT delay for hospital comparison
- Note which private hospitals have 24h emergency (or don't)

### Section 7 — What To Bring
- Passport + Chinese phone number
- Insurance card + policy info
- Previous reports, imaging, lab results, medication list
- Translation app / phrase sheet
- Written questions in advance
- 5 bullet points

### Section 8 — Best Strategy
Numbered list (3–4 steps):
1. Private international clinic for first eval if communication is priority
2. Move to public tertiary hospital if condition is complex/surgical
3. Ask for English records at every step
4. (Optional) Offer help with hospital shortlisting

### CTA Box (after Section 8)
```html
<div class="cta-box">
    <strong>Need help shortlisting {CITY} hospitals?</strong>
    <p>We can help compare suitable hospitals, departments, and next steps based on your condition, timeline, language needs, and budget.</p>
    <p><a class="cta-button" href="../contact-new.html">Start a free case review</a></p>
</div>
```

### Useful Next Steps links
```html
<a href="../hospitals.html">Browse hospitals in China</a>
<a href="foreigners-guide-healthcare-china.html">Read the national healthcare guide</a>
<a href="../medical-chinese-phrases.html">Open the phrase sheet</a>
<a href="../checklist.html">View the preparation checklist</a>
```

---

## Blog Index Card Template
```html
<div class="blog-card">
    <div class="blog-image" style="background: linear-gradient(135deg, #{hex} 0%, #{hex} 100%);">XX</div>
    <div class="blog-content">
        <div class="blog-category">City Guide</div>
        <h3 class="blog-title">How to See a Doctor in {CITY} as a Foreigner</h3>
        <p class="blog-excerpt">A practical {CITY} guide to public vs private hospitals, emergency care, registration, insurance, payment, and where foreigners usually start.</p>
        <div class="blog-meta">
            <span>{Month} 2026</span>
            <span>10 min read</span>
        </div>
        <a href="how-to-see-a-doctor-in-{city}-as-a-foreigner.html" class="read-more">Read Article</a>
    </div>
</div>
```
Insert in blog/index.html grid after Shanghai, before Beijing.

Color gradients by city:
- Shanghai: `#113c7a` → `#4f7dd8` (blue)
- Beijing: `#8B0000` → `#dc143c` (red)
- Guangzhou: `#0d5c2e` → `#28a745` (green)

---

## Sitemap Entry Template
```xml
<url>
  <loc>https://chinahospitalsguide.com/blog/how-to-see-a-doctor-in-{city}-as-a-foreigner.html</loc>
  <lastmod>{YYYY-MM-DD}</lastmod>
  <changefreq>monthly</changefreq>
  <priority>0.9</priority>
</url>
```
Insert after Shanghai entry, before Beijing entry.
