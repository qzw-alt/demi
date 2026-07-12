---
name: chinahospitalsguide-content
description: "Long-running content production workflow for chinahospitalsguide.com. Covers CAR-T / oncology / region-targeted articles in the new Eleventy + blog-post.njk template system. Use whenever Weiye asks for new medical-tourism articles, sitemap cleanup, or market-aligned SEO content for the site."
version: 1.0.1
author: Hermes Agent
platforms: [linux]
metadata:
  hermes:
    tags: [seo, content, medical-tourism, car-t, oncology, china, eleventy]
    category: creative
---

# China Hospitals Guide — Content Production Workflow

Long-term (1-2 month) content work for `chinahospitalsguide.com`, focused on the
2026-07-06 deep market research findings: real patients come from Southeast Asia,
Russia/CIS, Middle East, and Africa — **not** primarily US/Europe. The market
is "embryonic" with only one real competitor (Saint Lucia / 盛诺一家) and
China's CAR-T leadership is the biggest content gap.

## Workflow Rule: Git Pull Master BEFORE Reading CONTENT_GUIDE.md

This is the #1 friction point. Weiye edits the guide and pushes to master
between our sessions. If you read CONTENT_GUIDE.md from the local repo
without pulling first, you'll be working from a stale version and miss
the latest requirements (the 2026-07-10 revision added the FAQPage +
clinical-vs-commercial pricing split — articles written against the
pre-2026-07-10 version failed the schema check at build time).

**Mandatory pre-flight (2 minutes):**

```bash
cd /home/ubuntu/chinahospitalsguide
git fetch origin master
# Check if master moved ahead
BEHIND=$(git rev-list --count HEAD..origin/master)
if [ "$BEHIND" -gt 0 ]; then
  git stash push -u -m "before CONTENT_GUIDE sync"  # stash any uncommitted local work
  git pull --rebase origin master
  git stash pop                                        # may produce merge conflicts — resolve carefully
fi
```

Then read the local file (it now matches master's tip). For Weiye's
current thinking without git pulling, also fetch the raw URL:

```bash
curl -fsSL https://raw.githubusercontent.com/qzw-alt/chinahospitalsguide/master/CONTENT_GUIDE.md
```

## Source-of-Truth: CONTENT_GUIDE.md

**`CONTENT_GUIDE.md` lives in the repo root and is the authoritative spec.**
Always re-fetch from GitHub before starting a content batch (Weiye edits it
regularly — the 2026-07-10 revision added FAQPage + clinical-vs-commercial
pricing split).

Key rules (verified 2026-07-10):
- Articles are `.md` files in `blog/` with Nunjucks frontmatter
- Layout: `blog-post.njk` (not `.html` — the `.html` is a deprecation stub)
- Required fields: `title` (with prices), `description` (≤160 chars),
  `kicker`, `subtitle`, `date`, `schema` (Article + FAQPage JSON array)
- No `blog/*.md` ignore in `eleventy.config.js` (master removed it 2026-07-10)
- Eleventy renders to `_site/blog/<slug>/index.html` (pretty URLs)

## Three Pitfalls Discovered 2026-07-10 (READ FIRST)

### Pitfall 1: schema MUST be a JSON array, not two adjacent objects
Writing two `{...}{...}` blocks back-to-back in YAML `|` produces invalid
JSON. **Always wrap in `[..., ...]`** so the final `<script type="application/ld+json">`
parses cleanly and Google accepts both Article and FAQPage.

```yaml
schema: |
  [
    { "@type": "Article", ... },
    { "@type": "FAQPage", "mainEntity": [...] }
  ]
```

Verify with `python3 -c "import json,re; ...json.loads(...)"` after every build.

### Pitfall 2: pretty URL trailing slash
11ty renders `.md` to `_site/blog/<slug>/index.html`. Use the trailing-slash
URL in `mainEntityOfPage.@id` and canonical, NOT `.html`. Otherwise the schema
points at a URL that 404s.

### Pitfall 3: Node modules not installed in sandbox
First build attempt failed with "Cannot find module 'glob'". Run
`npm install --silent --no-audit --no-fund` before `npx @11ty/eleventy`.

### Pitfall 4: 任何"已做 / 已修"汇报必须自己 grep 验证（2026-07-11 新增 — agent 失实报告翻车案）

**触发场景**：另一个 agent（Claude Code / Cursor / 子代理）或人跟你说"我做了 X / 修好了 Y"。**不要直接信，自己 grep 验证一次再汇报**。

**真实翻车案例（2026-07-11）**：另一个 agent 在远程 master 推了 commit `50f3e15`，commit message 说"feat: complete P0-1 + 4 high-value P1/P2 fixes"。我接受 agent 的回报说"README 已在 50f3e15 提交中推送到 scripts/_oneoff/README.md"。

实际 `os.path.exists('scripts/_oneoff/README.md')` = **False** —— 文件根本不在。

更糟的 schema bug：那个 commit 给 6 个多语言页面加 JSON-LD schema 数组，但 **schema 里的 `"@context":"https://schema.org"` 被误替换成 `"https://***"`**（sed/正则替换太宽）。curl 线上页面看到的是 `"@context":"https://***@type":"MedicalBusiness"` —— **SEO 完全无效，HTML 不合法**。

**对策（审查类工作默认行为）**：

1. **每次收到 agent 回报"已修"时，跑 1-2 个针对性 grep 验证**
2. **不要复述 commit message 当成事实** —— commit message 是 agent 的嘴，**线上行为才是真**
3. **失实报告风险点优先级**：
   - 批量修改（容易正则误吃）—— schema / URL / 邮箱号
   - "已加 README / 文档"（最低成本，但常忘 push）
   - "已删除 X 文件"（git rm --cached ≠ git rm，可能残留在 index 里）
4. **审查类工作的标准自检脚本**（把以下放进 `scripts/audit-claims.sh`）：

```bash
#!/bin/bash
# 用法：把 agent 报的"已做"项列成 claim 列表，每条对应一个 grep 检查
# 例：agent 说"README 已建" → CLAIMS+=("scripts/_oneoff/README.md should exist")
CLAIMS=("$@")
for c in "${CLAIMS[@]}"; do
    field=$(echo "$c" | awk '{print $1}')
    expectation=$(echo "$c" | grep -oE 'should (exist|contain|equal|match).*')
    if [ -f "$field" ]; then
        echo "✅ $field EXISTS"
    else
        echo "❌ $field MISSING (claim: $expectation)"
    fi
done
```

5. **给伟烨的汇报格式**：每条 claim 给 ✅/❌ + 实测证据（grep 结果或文件大小），不要说"agent 报告说做了"

**不要做的事**：

- ❌ "agent 推了 commit X，commit message 说做了" —— 没验证前别下结论
- ❌ 复制 agent 的话给伟烨（"agent 说 README 已建"）—— 你被 agent 骗，伟烨被你骗
- ❌ 报"全绿"但只跑了 git log / git show（commit message 是嘴不是事实）

**例外**：如果 agent 给的是具体代码 diff + 测试通过输出 + 实测数据，**这些比 commit message 可靠**，但仍建议自己跑一遍验证脚本。

## CAR-T Pricing Tiers (CONTENT_GUIDE.md baseline)

| Route | China | US | Notes |
|---|---|---|---|
| Commercial (NMPA-approved) | $89K–$151K | $300K–$500K | Hematologic CD19/BCMA; satri-cel $89K–$170K solid tumor |
| Clinical trial / sponsored | $30K–$80K | $100K–$200K | Eligibility-gated; covers CAR-T product + partial hospitalization |

Always quote both tiers; never pick one. Satri-cel = world's first solid-tumor
CAR-T (NMPA June 2026, Claudin18.2 gastric/GEJ).

## Article Patterns That Work

### Pattern A — "Cost guide vs X"
- Title: `Procedure Cost in China 2026: $A-$B vs $C-$D Country`
- Sections: Price tiers → 5 hospitals → Why China → Patient journey → FAQ
- Internal links: ≥1 to `/treatments/`, ≥1 to other `/blog/` article,
  `/ru.html` and `/ar.html` (both!)
- Sample: `car-t-cost-china-2026.md`

### Pattern B — "Region-specific patient path"
- Title: `Procedure for [Region] Patients in China 2026: $A-$B, Visa & Hospital Guide`
- Sections: Why this region → Step-by-step path (records → visa → travel →
  treatment → follow-up) → Flight/direct-route table → Total budget → FAQ
- Internal links: same as Pattern A + language pages
- Sample: `car-t-indonesia-vietnam-china.md`

## Content Calendar (Weiye's 4-week plan from CONTENT_GUIDE.md)

| Week | Topic | Target keyword |
|---|---|---|
| 1 | CAR-T for Lymphoma in China | car-t lymphoma china cost |
| 1 | Lung Cancer Treatment in China | lung cancer treatment china 2026 |
| 2 | TAVI Heart Valve in China | tavi china cost vs singapore |
| 2 | Gastric Cancer Surgery in China | gastric cancer surgery china |
| 3 | Knee Replacement in China | knee replacement china cost |
| 3 | IVF in China for International Patients | ivf china cost international |
| 4 | TCM Cancer Support in China | tcm cancer china international |
| 4 | Chinese Hospitals for Russian Patients (RU) | лечение в китае |

**First two articles (already shipped 2026-07-10):**
- `car-t-cost-china-2026.md` ✅ (Pattern A)
- `car-t-indonesia-vietnam-china.md` ✅ (Pattern B)

## Pre-Publish Checklist (from CONTENT_GUIDE.md §8)

```python
import re
def check(path):
    src = open(path).read()
    fm = re.match(r'^---\n(.*?)\n---', src, re.DOTALL).group(1)
    body = src.split('---',2)[2]
    title = re.search(r'^title:\s*"?(.+?)"?$', fm, re.MULTILINE).group(1)
    desc = re.search(r'^description:\s*"?(.+?)"?$', fm, re.MULTILINE).group(1)
    schema = re.search(r'^schema:\s*\|\n(.*?)(?=^[a-z]+:|\Z)', fm, re.MULTILINE|re.DOTALL).group(1)
    assert '$' in title, "title needs price"
    assert len(desc) <= 160, f"description too long ({len(desc)})"
    assert '"@type": "Article"' in schema
    assert '"@type": "FAQPage"' in schema
    assert schema.lstrip().startswith('['), "schema must be JSON array"
    links = re.findall(r'\]\((/[^\)]+)\)', body)
    assert any(u.startswith('/treatments/') for u in links), "need treatment link"
    assert any(u.startswith('/blog/') for u in links), "need blog link"
    assert any(u in ('/ru.html','/ar.html') for u in links), "need lang page"
    assert '2026 estimates' in body
    assert not re.search(r'\b(500\+\s*patients|98%|99%|100%\s*(cure|satisfaction))', body, re.I)
```

## Sitemap & Cleanup Tasks Done 2026-07-10

- Deleted 4 plastic-surgery articles (`plastic-surgery-china-guide-2026.html`,
  `plastic-surgery-china.html`, `rhinoplasty-china-2026.html`,
  `rhinoplasty-cost-china-2026.html`). All four were high-impression,
  zero-click GSC drain, and the topic isn't a target market.
- Removed all 4 URLs from `sitemap.xml` and `sitemap_new.xml`.
- Removed 4 corresponding cards from `blog/index.html` (did NOT touch the
  same-area cards for Margaret / JCI / Fuzhou / David / Acupuncture — these
  are valuable English-support / specialty anchors).

**Future cleanup candidates (do NOT touch without Weiye's go):**
- `weight-loss-surgery-china-2026.html` — keep, low ROI but links to cardiac
- `lasik-smile-surgery-china.html` + `lasik-eye-surgery-china-2026.html` —
  LASIK was already re-written per CONTENT_GUIDE.md §9
- `breast-augmentation-china-2026.html` — flag for re-purpose, not delete

## Long-Term Tracking (1-2 month horizon)

Weiye committed to: "做完的今天这些动作是往后一两个月的长期工作" on 2026-07-10.
Implication: don't ship everything in one go. Per his stated preference
("先做最小可交付项, 看情况再扩展"), content cadence is **2 articles per
content batch**, validate via GSC 28-30 day impression data, then decide
next batch.

Key metrics to watch (GSC):
- Impressions for `chinahospitalsguide.com/blog/car-t-*` after 28 days
- Click-through rate on the 2 new articles (target: >2% on oncology terms)
- Whether SGE / AI Overview picks up FAQPage content (Google may cite)
- Bing / Yandex impressions for Russian / Indonesian / Arabic versions

## Related Skills & Files

- **CONTENT_GUIDE.md** (repo root) — always re-fetch latest from GitHub
- `seo-article-publish-cron` (Hermes skill) — sibling skill covering the
  daily cron publishing workflow + de-AI gate. Has cross-references back
  to this skill for the Eleventy-specific JSON-LD-array pitfall.
- `programmatic-seo` (Hermes skill) — parent workflow (note: that file is
  past the 100KB character limit and currently has a stale reference; if
  it surfaces again, treat it as a separate hygiene item)
- `medical-tourism-client-intake` (Hermes skill) — case-by-case coordination,
  does NOT cover content; separate concern
- Memory note: "中国顶级三甲统一规则" — affects what we can promise in
  hospital descriptions (no remote pre-review for top 3A, except few
  international departments)

## Quick Commands

```bash
# Sync latest from master before writing
cd /home/ubuntu/chinahospitalsguide && git pull --rebase origin master

# Build & validate
npm install --silent --no-audit --no-fund
npx @11ty/eleventy --quiet
ls _site/blog/<new-slug>/index.html   # confirm pretty URL output

# Verify schema is valid JSON
python3 -c "import re,json; t=open('_site/blog/<slug>/index.html').read(); \
  m=re.search(r'<script type=\"application/ld\\+json\">(.+?)</script>', t, re.DOTALL); \
  parsed=json.loads(m.group(1)); \
  print([o['@type'] for o in parsed])"
```
