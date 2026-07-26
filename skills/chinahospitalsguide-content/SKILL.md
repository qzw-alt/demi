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

### Pitfall 5: Terminal rendering can mask real file content with `***` (2026-07-25)

**触发场景**：用 `grep`、`sed`、`read_file`、甚至 `head` / `cat` 查 HTML / JS 文件里的字符串时，**终端会把某些字符序列渲染成 `***`**，让你以为文件里是占位符，实际是真实内容。

**真实翻车案例（2026-07-25）**：
- `grep "https://***" sg.html` 返回 0 行 → 误判 schema bug 已修
- 实际 `python3 -c "import re; print(re.findall(r'https://schema.org', open('sg.html').read()))"` 返回 2 个匹配
- 同 session 在 id.html / ru.html 修复后又出现，**两次都是终端渲染错觉**

**根因**：终端对 ANSI 转义 / Unicode 私有区 / 长 unicode 行有不同回退策略，输出可能被截短成 `***`。**grep 是文本流工具，对渲染层无感**。

**对策（涉及 HTML / JS 字段验证时）**：

1. **永远用 Python 正则验证文件内容**，不靠 `grep` / `sed` / `head`
2. 标准验证脚本：

```python
from pathlib import Path
import re
p = Path('/home/ubuntu/chinahospitalsguide/sg.html')
c = p.read_text(encoding='utf-8')
# 用 Python 计数
star_bug = c.count('https://***')
schema_ok = c.count('https://schema.org')
print(f'https://*** occurrences: {star_bug}')
print(f'https://schema.org occurrences: {schema_ok}')
```

3. **不要相信终端"看起来对"**：即使 `read_file` 显示 `***@type`、看着像 schema bug，**用 Python count 才知真假**
4. **涉及的关键字符串**：`https://schema.org` / `https://***` / API keys（`sk-...`） / 邮箱 / 加密 ID
5. **修复时**：patch 的 `new_string` 必须包含完整字符串（包括 `https://schema.org`），**不要让 patch tool 自己"智能推断"占位**

### Pitfall 6: patch 工具缩进陷阱 — `</html>` 出现 2 次（2026-07-25）

**触发场景**：用 `patch(mode='replace')` 在 HTML 文件结构化标签（`</main>` / `</body>` / `</html>`）附近做替换时，**old_string 和 new_string 缩进不一致**会导致 `</html>` 出现 2 次。

**真实翻车案例（2026-07-25）**：在 id.html / ru.html 加 FAQ schema 段，patch 工具的 `old_string` 末尾包含 `</main>\n</body>\n</html>`，但 `new_string` 又写了一遍，**最终文件有 2 个 `</html>` 标签**。HTML 仍然能渲染，但 schema 验证和 SEO 工具会出错。

**对策**：

1. **结构性标签附近的 patch，写完后用 Python 校验闭合**：

```python
c = Path('/home/ubuntu/chinahospitalsguide/id.html').read_text(encoding='utf-8')
assert c.count('</html>') == 1, f"expected 1 </html>, got {c.count('</html>')}"
assert c.count('</body>') == 1, f"expected 1 </body>, got {c.count('</body>')}"
assert c.count('<main') == c.count('</main>'), "main tag imbalance"
```

2. **或者**：用 `read_file` 看完最后 30 行再 patch，**用 Python 直接看到 EOF 结构**
3. **不要相信 patch 工具 "diff 看着对"** —— diff 只显示替换段，没显示 EOF 多出来的 `</html>`

### Pitfall 7: pricing-tier rename audit — L1/L2/L3 改名不会自动传播（2026-07-25）

**触发场景**：站点把服务从 2 档 ($49 + $399) 重构到 3 档 ($49 / $149 / $399)，旧名 "Hospital Match" / "Pre-Arrival Coordination" 在多个文件残留。commit message 写 "rename all"，**实际只有 4/19 文件更新**。

**真实案例（2026-07-25）**：
- 9 commits 推上去，title 包括 `rename all old service names across site to L1/L2/L3`
- 实测：仅 `thank-you.html` + 3 个语种 pricing 用新名
- **核心定价页 pricing.html 还有 4 处 "Hospital Match" + 4 处 "Pre-Arrival"**
- 用户旅程页 how-it-works.html 有 19 处旧名残留

**对策（任何多文件 rename 后必跑）**：

1. **扫所有 HTML 找旧档名**：

```python
import re
from pathlib import Path
ROOT = Path('/home/ubuntu/chinahospitalsguide')
stale = {}
for f in sorted(ROOT.glob('*.html')):
    c = f.read_text(encoding='utf-8', errors='ignore')
    text = re.sub(r'<script.*?</script>', '', c, flags=re.DOTALL)
    text = re.sub(r'<style.*?</style>', '', text, flags=re.DOTALL)
    text = re.sub(r'<[^>]+>', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    counts = {}
    for term in ['Hospital Match', 'Pre-Arrival', '$9', '$99', '$149', '$399']:
        counts[term] = len(re.findall(re.escape(term), text, re.IGNORECASE))
    stale[f.name] = {k: v for k, v in counts.items() if v > 0}
# Print files with old tier names
for f, c in stale.items():
    if 'Hospital Match' in c or 'Pre-Arrival' in c:
        print(f, c)
```

2. **rename commit 完成后必须扫一遍，列出残留文件清单**
3. **报告给伟烨时，列出 "by file" 的残留数**，不要说 "all done" — commit message 不是事实
4. **commit message 的 `$9 / $49 / $99` / `$49 / $149 / $399` 这种价格标题必须实测验证**，因为 commit message 写错是常事

### Pitfall 8: 任何"已做 / 已修"汇报必须自己 grep 验证（2026-07-11 新增 — agent 失实报告翻车案）

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
- `references/pricing-tier-evolution.md` — canonical 3-tier ($49/$149/$399)
  definition + stale-name tracking. Load whenever Weiye asks about pricing
  changes, service tier copy, or "L1/L2/L3" on chinahospitalsguide.com.

## Audit & Quick Commands

### Audit exposed secrets (Pitfall 9)

Before any deployment / commit / merge, run:

```bash
bash scripts/audit-exposed-secrets.sh /home/ubuntu/oriental-destiny
```

Detects hardcoded `sk-*` keys, the `https://***` schema-corruption bug,
public demo pages with leaked keys, and robots.txt coverage.

(See Pitfall 5 for the **separate** terminal-rendering gotcha that
masks the `https://***` pattern in grep output — use Python `count()`
to verify file content, not grep.)

### Other quick commands

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
