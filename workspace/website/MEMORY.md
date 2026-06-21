# Project Memory — chinahospitalsguide.com

> 中国医院指南 · China Hospitals Guide · Medical Tourism Directory
> Last updated: 2026-06-20

---

## 1. Project Identity

**Site**: [chinahospitalsguide.com](https://chinahospitalsguide.com)
**Repo**: [github.com/qzw-alt/chinahospitalsguide](https://github.com/qzw-alt/chinahospitalsguide)
**GitHub Access**: local proxy `127.0.0.1:10808` + PAT + `git -c http.sslBackend=openssl`

**Mission**: Help international patients find, compare, and book medical treatment at China's top hospitals. Bridge the information gap between China's world-class medical capabilities and foreign patients who don't know where to start.

**Target Audience**: English-speaking international patients considering medical travel to China — primarily from US, Singapore, Malaysia, UK, Australia. Secondary: Chinese diaspora, medical tourism agencies.

**Value Proposition**: Save 50-80% on medical procedures vs Western countries while accessing Fudan-ranked hospitals with JCI accreditation and English-speaking departments.

---

## 2. Site Architecture

### Page Inventory (~190 HTML pages)
```
/
├── index.html                    Homepage
├── hospitals.html                100+ hospital directory (filterable by city/specialty)
├── about.html                    About page
├── contact.html / contact-new.html   Contact/lead capture
├── pricing.html                  Pricing page
├── services.html                 Services overview
├── resources.html                Resource hub
├── checklist.html                Medical travel checklist
├── cost-comparison.html          Procedure cost comparison tool
├── how-it-works.html             Step-by-step patient journey
├── course.html + chapter-1~9/    9-chapter medical tourism course
├── stories.html / real-stories.html   Patient success stories
├── privacy.html / terms.html     Legal pages
├── panel.html                    Expert panel / doctor directory
├── patient-story-program.html    Patient story submission
├── 404.html                      Custom 404 with JS redirects
│
├── blog/                         93 articles
│   ├── Hospital rankings (by city × specialty)
│   ├── Procedure guides (LASIK, IVF, CAR-T, dental, plastic surgery...)
│   ├── City guides (Beijing, Shanghai, Guangzhou, Chengdu, Xi'an...)
│   ├── Cost breakdowns (cancer, heart surgery, knee replacement...)
│   ├── How-to guides (see a doctor as foreigner, book appointment...)
│   └── Comparison articles (China vs Thailand/India/Korea...)
│
├── news/                         71 news articles
│   └── Daily "China-Compare" format:
│       Global medical tourism news → How does China compare?
│
├── treatments/                   5 specialty landing pages
│   ├── cancer.html, cardiac.html, ivf.html
│   ├── orthopedics.html, stem-cell.html
│
├── 医疗旅游/                      Chinese-language content
├── 德米知识库/                    Internal AI knowledge base (Chinese)
├── 视频内容/                       Video content scripts (Chinese)
│
├── _layouts/base.njk              Nunjucks base template
├── _includes/                     head, nav, footer, scripts (Nunjucks partials)
├── _data/                         Jekyll-style data
├── _redirects                     Cloudflare/Netlify redirect rules
├── config/mcporter.json           Build tool config
├── images/                        Image assets
├── scripts/                       Helper scripts
├── references/                    Reference data
└── reports/                       Analytics reports
```

### Tech Stack
- **Build**: mcporter (custom SSG?) → outputs flat HTML
- **Templates**: Nunjucks (`.njk`), but pages ship as pre-generated `.html`
- **Deploy**: Cloudflare Pages or Netlify (uses `_redirects` file)
- **Analytics**: Google Analytics (G-RVYZENK472)
- **Ads**: Google AdSense (`pagead2.googlesyndication.com`)
- **CSS**: Single `styles.css` + inline per-page styles
- **Fonts**: Google Fonts (Inter + Playfair Display)
- **Schema**: JSON-LD on ~90% of pages (Article, BreadcrumbList, FAQ, MedicalWebPage)

---

## 3. Content Strategy

### Core Content Pillars
1. **Hospital Rankings** — Fudan-ranked hospitals by city × specialty (orthopedics, oncology, cardiology, ophthalmology, respiratory...)
2. **Procedure Cost Guides** — $X in China vs $Y in US/West, with hospital recommendations
3. **City Medical Guides** — How to get treatment in Beijing/Shanghai/Guangzhou/etc as a foreigner
4. **Medical Tourism Comparison** — China vs Thailand, India, Korea, Singapore, Turkey...
5. **Breaking Medical News** — Daily "China-Compare" format on global medical developments

### Title Formula (proven pattern)
```
[Procedure] in China [Year]: $X–$Y — [Number] [Adjective] [Noun]
Example: "LASIK in China 2026: $800–$1,500 per Eye at Top 10 Eye Hospitals"
```

### Content Quality Standards
- Every page must have: unique `<title>`, `<meta description>`, JSON-LD Schema, `canonical` URL, OG tags
- Descriptions should include: numbers, comparisons, action verbs
- Avoid publishing bulk low-quality pages (caused the May 2026 index collapse: 42→499 unindexed)

### High-Performing Content Types
- City-specific hospital rankings (Fuzhou orthopedic, Jinan respiratory — rank positions 1-5)
- Procedure cost comparisons with specific dollar figures
- "How to see a doctor in [City] as a foreigner" guides (4.22% CTR on Guangzhou version)

---

## 4. SEO Performance (GSC data, last 3 months)

### Traffic Snapshot
| Metric | Value |
|--------|-------|
| Total clicks | 105 |
| Total impressions | ~45,000 |
| Avg CTR (desktop) | 0.08% ❌ |
| Avg CTR (mobile) | 3.2% |
| Avg position | 7.0 |
| Indexed pages | ~124-135 |

### Critical Issues
1. **CTR crisis**: Desktop CTR 0.08% — titles/descriptions not compelling despite decent rankings
2. **Zero-click problem**: Hospital ranking pages at position 1-5 getting 0 clicks (snippet cannibalization)
3. **404 errors**: 126 pages returning 404 (wasting crawl budget)
4. **Index bloat**: 499 unindexed pages after May 19 bulk publish (quality flag)
5. **Singapore anomaly**: 19,262 impressions, 0.04% CTR — content doesn't match Singapore user intent

### Top Traffic Sources
- **Countries**: China (25 clicks), US (19), Malaysia (8), Singapore (7), UK (7)
- **Pages**: LASIK (12,753 imp), China hospital rankings (9,121 imp), Cataract (2,420 imp)
- **Queries**: Hospital ranking queries dominate, followed by procedure cost queries

### Opportunities (high-impression, zero-click queries)
- "singaporean certification of medical devices" — 68 imp, rank 45 (created dedicated page)
- "china hematopoietic stem cell transplantation market" — 49 imp
- "fuzhou orthopedic hospital rankings 2026" — 38 imp, rank 1.05!
- "trending wellness cities china 2026" — 20 imp (created dedicated page)

---

## 5. Key Decisions & Patterns

### Content Publishing Rules
- ✅ One well-researched article > ten thin pages (learned from May 2026 index collapse)
- ✅ Every page must target a specific search query visible in GSC data
- ✅ Price ranges in titles (e.g., "$300–$1,200") significantly improve CTR
- ✅ City × Specialty ranking pages perform best for organic discovery
- ❌ Bulk publishing without quality control destroys index coverage

### Technical Patterns
- Redirects use both `_redirects` file (Cloudflare/Netlify) AND 404.html JS fallback
- Schema added manually per-page (not templated) — check `application/ld+json`
- Meta updates MUST use single-quoted PowerShell strings (double-quotes eat `$` signs!)
- Git operations through sandbox require: `GIT_SSL_NO_VERIFY` + `proxy 127.0.0.1:10808` + `openssl` backend

### Edit Safety
- Always restore from git (`git checkout -- file`) before re-editing if a regex replace goes wrong
- Verify with hex inspection (`[Text.Encoding]::UTF8.GetBytes()`) when `$` signs disappear
- The `-replace` operator in PowerShell interprets `$1`, `$2` as regex backreferences
- Use `[regex]::Replace()` with escaped patterns, or string IndexOf/Substring for dollar-safe edits

---

## 6. Current Improvement Status (June 2026)

### Completed
- ✅ Meta titles & descriptions optimized on 23 high-impact pages
- ✅ 404.html improved (noindex, better UX, expanded redirects)
- ✅ _redirects updated with 8 new 301 rules
- ✅ New content: medical-device-certification-singapore-vs-china-2026.html
- ✅ New content: wellness-cities-china-2026.html
- ✅ AGENTS.md created for future Codex sessions

### Pending / Next Steps
- [ ] Submit 404 fixes to Google Search Console for validation
- [ ] Audit and clean up 499 unindexed pages (merge/delete/improve)
- [ ] Monitor CTR changes over 2-4 weeks (target: desktop ≥0.5%)
- [ ] Expand city-specific ranking series to more cities (based on query data)
- [ ] Create "china hematopoietic stem cell transplantation market" content
- [ ] Improve Singapore-focused content to boost 0.04% CTR
- [ ] Add FAQ schema to hospital ranking pages to reduce snippet cannibalization
- [ ] Build internal linking between related articles (blog → news, city guides → hospital directory)

---

## 7. Working with This Project

### Quick Start (Codex Session)
```powershell
# Clone (if not already local)
$env:http_proxy="http://127.0.0.1:10808"; $env:https_proxy="http://127.0.0.1:10808"
git -c http.sslBackend=openssl clone https://github.com/qzw-alt/chinahospitalsguide.git C:\Users\csdm2\Documents\chinahospitalsguide.com\src

# Push changes
. .\scripts\git-push-helper.ps1
Push-GitHub -RepoPath "C:\Users\csdm2\Documents\chinahospitalsguide.com\src"
```

### Common Tasks
- **Edit a page**: Directly modify the `.html` file (pre-generated, no build step for content)
- **Add new blog post**: Copy an existing similar post, update title/desc/schema/content
- **Fix meta tags**: Use string IndexOf/Substring, never `-replace` with `$` in replacement
- **Add redirect**: Append to `_redirects` file + optionally add to `404.html` JS map
- **Check schema**: Search for `application/ld+json` — empty blocks need filling
