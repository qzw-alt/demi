# Hospital Ranking Page — Featured Snippet Template

**Verified**: 2026-07-02 (4 ranking pages shipped: cancer, orthopedic, cardiac, Fudan Top 100).
**Origin**: Applied across `best-hospitals-china-international-patients.html` (2026-07-01 P0) + 4 specialty ranking pages (2026-07-02 batch).

## When to use this template

Use on any page with:
- High search volume for "best X in China" / "top X hospitals China"
- A list of 5-20 hospitals
- A table of contents structure with sections per specialty/procedure/city

Skip on: pillar pages (different pattern), city guides, single-hospital deep-dive articles.

## Three blocks to add (in order)

### Block 1: Quick Decision (decision-tree card grid)

**Position:** Between the existing quick-answer / highlight block and the TOC.
**Container:** Deep-blue gradient `#1e3c72 → #2a5298`, white text, 32px padding, 14px border-radius, 24px margin.
**Content:** 8 cards in a responsive grid (`grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 14px`).

**Card structure:**
- White-translucent background `rgba(255,255,255,0.1)`, 3px left border in a per-card color
- `<h3>` with emoji + condition/specialty name (1em, semantic accent color)
- 1 paragraph (~2 lines): **Start with:** Hospital X — 1 distinguishing fact + cost anchor ($X vs $X US)
- Deep-link with anchor text matching the condition (e.g. `See lung cancer section →`)

**Per-specialty card variants (verified working):**

#### Variant A: Oncology ranking page (`best-cancer-hospitals-china-2026.html`)

| # | Emoji | Condition | Color | "Start with" content | Deep link |
|---|---|---|---|---|---|
| 1 | 🫁 | Lung Cancer / Thoracic | `#dc143c` | CAMS Cancer Hospital (Beijing) — 18,000+ lung surgeries/yr; Shanghai Chest | `#lung-cancer` |
| 2 | 🧬 | Liver Cancer / Hepatobiliary | `#8B4513` | Sun Yat-sen Cancer Center (Guangzhou) — world's largest by volume; Eastern Hepatobiliary (Shanghai) | `#liver-cancer` |
| 3 | 🎀 | Breast Cancer / Gynecologic | `#c2185b` | Fudan Shanghai Cancer Center — BRCA testing, fertility preservation; PUCH | `#breast-cancer` |
| 4 | 🧬 | CAR-T / Blood Cancer | `#1565C0` | Ruijin Hospital Shanghai (world's first CAR-T 2017); PU Cancer Hospital | `car-t-therapy-hospitals-china-2026.html` |
| 5 | 🧠 | Brain Tumor / Glioma | `#00b4db` | Beijing Tiantan Hospital — world's #1 neurosurgery volume; West China | `neurosurgery-cost-china.html` |
| 6 | 👶 | Pediatric Cancer | `#28a745` | Beijing Children's Hospital; Shanghai Children's Medical Center — pediatric oncology MDT | `#pediatric` |
| 7 | ☢️ | Proton / Heavy-Ion Therapy | `#d4691e` | Shanghai Proton & Heavy Ion Center — only operating facility (2015+) | `china-unique-medical-procedures-guide.html` |
| 8 | ❓ | Don't Know My Cancer Type | `#1e3c72` | PUMCH — strongest general cancer diagnostics, MDT review, second opinions | `/contact-new.html` |

#### Variant B: Orthopedic ranking page (`china-orthopedic-hospital-rankings-2026.html`)

| # | Emoji | Condition | Color | "Start with" content |
|---|---|---|---|---|
| 1 | 🦵 | Hip / Knee Replacement | `#d4691e` | Beijing Jishuitan — 10,000+ joint replacements/yr; $8K-15K vs $40K-60K US |
| 2 | 🦴 | Spine Surgery (Disc / Scoliosis) | `#00b4db` | Peking University Third Hospital (北医三院); West China for MIS |
| 3 | 🦶 | Sports Medicine / ACL / Meniscus | `#28a745` | Jishuitan; Shanghai Sixth — arthroscopic centers with Olympic-grade specialists |
| 4 | 👶 | Pediatric Orthopedics | `#dc143c` | Beijing Children's Hospital; Shanghai Children's Medical Center (DDH, clubfoot, scoliosis) |
| 5 | 🦴 | Bone Tumor / Oncology Orthopedics | `#8B4513` | PU People's Hospital (musculoskeletal tumor center); limb-salvage surgery |
| 6 | 🦴 | Robotic Surgery (MAKO / DA Vinci) | `#1565C0` | West China Hospital; Shanghai Sixth — MAKO robotic joint replacement |
| 7 | 💪 | Trauma / Fracture (Acute) | `#c2185b` | Nearest top 3A (PUMCH/West China/Ruijin — 24/7 orthopedic trauma); air ambulance medevac |
| 8 | ❓ | Don't Know / Need Guidance | `#1e3c72` | PUMCH — strongest orthopedic + general medicine back-up; best English support |

#### Variant C: Cardiac ranking page (`best-cardiac-surgery-hospitals-china-2026.html`)

| # | Emoji | Condition | Color | "Start with" content |
|---|---|---|---|---|
| 1 | 🫀 | Coronary Bypass (CABG) | `#28a745` | Fuwai Hospital (Beijing) — #1 in Asia, 18,000+ surgeries/yr; $18K-30K vs $100K-200K US |
| 2 | 💓 | Heart Valve Repair/Replacement (TAVI) | `#dc143c` | Fuwai; West China — high-volume TAVI; $25K-45K vs $80K-150K US |
| 3 | 👶 | Congenital Heart (Pediatric) | `#00b4db` | Beijing Fuwai (national pediatric heart center); Shanghai Children's Medical Center |
| 4 | 🏃 | Arrhythmia / AFib / Pacemaker | `#d4691e` | Fuwai; Ruijin (electrophysiology); catheter ablation, leadless pacemakers; $5K-15K vs $30K-80K US |
| 5 | 🫁 | Heart Failure / LVAD / Transplant | `#1565C0` | Fuwai (#1 heart transplant); Tongji Hospital (Wuhan); heart transplant $50K-80K vs $1.4M US |
| 6 | 🩸 | Aortic Aneurysm / Dissection | `#c2185b` | Fuwai; Anzhen Hospital (Beijing Aortic Center); EVAR available; time-critical |
| 7 | 🫀 | Minimally Invasive / Robotic Cardiac | `#1e3c72` | West China; Anzhen — robotic mitral valve repair, MIDCAB, thoracoscopic ASD closure |
| 8 | ❓ | Don't Know / Need Guidance | `#8B4513` | PUMCH — comprehensive cardiac workup, second opinions, weak heart cases |

#### Variant D: Fudan Top 100 generic ranking page (`china-hospital-rankings-2026.html`)

This page is multi-specialty — the cards navigate BY USER SITUATION, not by condition:

| # | Emoji | Situation | Color | "Start here" content |
|---|---|---|---|---|
| 1 | 🎗️ | I Have Cancer — Need Oncology | `#dc143c` | Sun Yat-sen Cancer Center (Guangzhou) + CAMS Cancer Hospital (Beijing) |
| 2 | 🫀 | I Have Heart Disease | `#28a745` | Fuwai Hospital (Beijing) — #1 in Asia by cardiac volume |
| 3 | 🦴 | I Need Orthopedics / Joint Replacement | `#00b4db` | Beijing Jishuitan Hospital; Shanghai Sixth |
| 4 | 🧠 | Brain / Spine Surgery | `#d4691e` | Beijing Tiantan Hospital — world's #1 neurosurgery volume |
| 5 | 🏙️ | I'm Choosing by City | `#c2185b` | Beijing (PUMCH), Shanghai (Ruijin/Huashan), Guangzhou (Sun Yat-sen), Chengdu (West China) |
| 6 | 👶 | I Need Pediatric Specialty | `#8B4513` | Beijing Children's Hospital; Shanghai Children's Medical Center |
| 7 | 🧬 | Frontier Therapy (CAR-T / Gene / Stem Cell) | `#1565C0` | Ruijin (CAR-T pioneer), West China (gene therapy trials), Hainan Boao Lecheng |
| 8 | ❓ | Complex / Multiple Conditions | `#1e3c72` | PUMCH — best general hospital for complex cases, MDT review |

### Block 2: Quick Answers (Featured Snippet Q&A)

**Position:** After the TOC, before the first detail section. OR if no TOC exists: at end of content, just before `</main>` or `</article>`.
**Container:** Light grey `#f8f9fa`, 28px padding, 12px border-radius, 4px left border `#1e3c72`.

**Format:** 5 Q&A pairs in `X is Y` phrasing (Google Featured Snippet optimization).
Each Q: `<h3>` in `#1e3c72`, 1.05em font.
Each A: `<p>` with `<strong>` on key terms (hospital name, cost).

**Per-page topic for the 5 questions** (verify these are the highest-volume queries for that page):
- Cancer: "#1 cancer hospital", "cost", "CAR-T availability", "pre-screening", "success rate"
- Orthopedic: "#1 orthopedic hospital", "knee replacement cost", "international patients", "quality vs US", "wait time"
- Cardiac: "#1 heart hospital", "cost", "safety", "wait time", "TAVI availability"
- Fudan Top 100: "#1 hospital", "vs US News", "how many top hospitals", "best city", "3A vs JCI"

### Block 3: JSON-LD schemas (added to `<head>`)

**Position:** After existing Article schema, before `</head>`.

**Add MedicalWebPage schema** (helps Google classify as medical-decision page):
```json
{
  "@context": "https://schema.org",
  "@type": "MedicalWebPage",
  "name": "<Page Topic> — Quick Decision Guide",
  "description": "Decision guide to help international patients choose the right <specialty> hospital in China by <key dimensions>, cost comparisons, and access information.",
  "specialty": "<Cardiology|Orthopedic Surgery|Oncology|Multi-specialty>",
  "lastReviewed": "2026-07-02",
  "primaryImageOfPage": "https://chinahospitalsguide.com/og-image.webp",
  "about": [
    {"@type": "Thing", "name": "<Sub-topic 1>"},
    {"@type": "Thing", "name": "<Sub-topic 2>"}
  ],
  "citation": [
    {"@type": "Organization", "name": "Fudan Hospital Rankings 2026"},
    {"@type": "Organization", "name": "Joint Commission International (JCI)"}
  ]
}
```

**Add BreadcrumbList schema** (improves SERP display):
```json
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://chinahospitalsguide.com/"},
    {"@type": "ListItem", "position": 2, "name": "Blog", "item": "https://chinahospitalsguide.com/blog/"},
    {"@type": "ListItem", "position": 3, "name": "<Page Title>"}
  ]
}
```

**CRITICAL PITFALL — schema injection safety (learned 2026-07-02):**

Use `inject_schemas_safe()` — **never** delete existing schemas with greedy regex. The cancer page incident (deleted Article + BreadcrumbList + FAQPage in one bad replace) was a hard lesson.

```python
import re

def get_existing_schema_types(text):
    schemas = re.findall(r'<script type="application/ld\+json">([\s\S]*?)</script>', text)
    return [re.findall(r'"@type"\s*:\s*"([^"]+)"', s)[0] for s in schemas]

def inject_schemas_safe(text, new_medicalwebpage_block, new_breadcrumb_block):
    """Add MedicalWebPage + BreadcrumbList ONLY if not already present.
    Never modify or delete existing schemas."""
    existing = get_existing_schema_types(text)
    new_blocks = []
    if "MedicalWebPage" not in existing:
        new_blocks.append(new_medicalwebpage_block)
    if "BreadcrumbList" not in existing:
        new_blocks.append(new_breadcrumb_block)
    if not new_blocks:
        return text
    head_end = text.find("</head>")
    return text[:head_end] + "\n" + "\n".join(new_blocks) + "\n" + text[head_end:]
```

**Pre-flight audit checklist before adding schemas:**
```bash
# Confirm current schema inventory before any edit
python3 -c "
import re
with open('/path/to/file.html') as f: text = f.read()
schemas = re.findall(r'<script type=\"application/ld\\+json\">([\\s\\S]*?)</script>', text)
for s in schemas:
    types = re.findall(r'\"@type\"\\s*:\\s*\"([^\"]+)\"', s)
    print(types[:3])
"
```

## Insertion recipe (execute_code-based)

```python
import re

def insert_quick_decision(file_path, card_html_block):
    """Insert Quick Decision block at first <h2> after <main>."""
    with open(file_path) as f:
        text = f.read()
    if "Quick Decision" in text:  # de-dupe
        return False
    main_start = text.find("<main")
    if main_start == -1:
        main_start = text.find("<article")
    first_h2 = text.find("<h2", main_start)
    text = text[:first_h2] + card_html_block + "\n\n            " + text[first_h2:]
    with open(file_path, "w") as f:
        f.write(text)
    return True

def insert_quick_answers(file_path, qa_html_block):
    """Insert Quick Answers block at </main> or </article>."""
    with open(file_path) as f:
        text = f.read()
    if "Quick Answers (Most Asked Questions)" in text:  # de-dupe
        return False
    main_close = text.find("</main>")
    if main_close == -1:
        main_close = text.find("</article>")
    text = text[:main_close] + qa_html_block + "\n        " + text[main_close:]
    with open(file_path, "w") as f:
        f.write(text)
    return True
```

## Verification protocol (after each page)

```python
import re

def verify_ranking_page(path):
    with open(path) as f:
        text = f.read()
    schemas = re.findall(r'<script type="application/ld\+json">([\s\S]*?)</script>', text)
    schema_types = [re.findall(r'"@type"\s*:\s*"([^"]+)"', s)[0] for s in schemas]
    has_qd = "Quick Decision" in text
    has_qa = "Quick Answers" in text
    h1 = bool(re.search(r"<h1[\s\S]*?</h1>", text))
    qd_cards = len(re.findall(r'<h3 style="margin: 0 0 8px; color: #[a-fA-F0-9]+; font-size: 1em;">', text))
    qa_count = len(re.findall(r'<h3 style="margin: 0 0 6px; color: #1e3c72; font-size: 1\.05em;">', text))
    return {
        "schemas": schema_types,
        "qd": has_qd,
        "qa": has_qa,
        "h1": h1,
        "qd_cards": qd_cards,  # expect 8
        "qa_questions": qa_count,  # expect 5
    }
```

**Expected after edit:**
- `schemas` contains Article + FAQPage (if existed) + MedicalWebPage + BreadcrumbList
- `qd` True, `qa` True, `h1` True
- `qd_cards` == 8, `qa_questions` == 5

## Tag-balance check (don't break the HTML)

```python
import re
def check_balance(path):
    with open(path) as f: text = f.read()
    return {
        "script": (len(re.findall(r'<script(?:\s[^>]*)?>', text)), text.count('</script>')),
        "div": (len(re.findall(r'<div(?:\s[^>]*)?>', text)), text.count('</div>')),
        "h*": (len(re.findall(r'<h[1-6](?:\s[^>]*)?>', text)), len(re.findall(r'</h[1-6]>', text))),
    }
```

All must match. If they don't, **stop and compare to git HEAD** — do not commit.

## Deployment

Same as any chinahospitalsguide change:
1. git add + commit with descriptive message (name the slug(s))
2. `git push origin master` (with `--rebase` if needed)
3. Wait ~60s for Cloudflare Pages deploy
4. Curl HTTP 200 + grep for the new content (`Quick Decision`, `Quick Answers`)
5. **If first curl returns 200 but expected text grep returns 0 → wait 30-60s and re-poll** (CDN propagation)

See parent SKILL.md for the full deployment protocol and `_redirects`/`sitemap.xml` rules.