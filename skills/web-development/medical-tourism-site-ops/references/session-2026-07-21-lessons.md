# 2026-07-21 Session — Content ops cadence + unindexed cleanup + Playwright pipeline

This file captures the 2026-07-21 session that established three new repeatable patterns:

1. **Realistic content cadence math** (1 篇/week is the realistic ceiling with human quality gate)
2. **Site-wide unindexed page audit** (236 URLs → 25-30 to dispose → recovery protocol)
3. **Playwright headless HTML→PNG pipeline** (Playwright venv + Chromium install + render-to-png.py)

The lessons here are also encoded in the parent SKILL.md as concise pitfall sections; this file is the worked transcript + reusable scripts.

## A. Realistic content cadence (the math Weiye asked about)

**The trigger**: Weiye asked *"我不明白为什么每天一篇还需要这么长的时间"* after I estimated 14 weeks to clear 9 topics.

**The mistake I almost made**: would have answered with abstract "depends on quality / depends on review" handwaving. That's wrong. The honest answer is a **time-accounting** problem:

| 步骤 | 耗时 |
|---|---|
| 选题 + 资料收集 (cost / hospital / clinical / regulations) | 30-45 min |
| 写大纲 (H2 结构 + FAQ + 内部链接) | 15-20 min |
| 写正文 (1000-1500 词) | 45-60 min |
| Schema + 费用表 + 元数据 | 15-20 min |
| agent 审 (事实 / 模板 / Schema / 链接) | 15-20 min |
| 拍板 + 发布 + sitemap | 5-10 min |
| **总计** | **2-3 小时/篇** |

**Weekly throughput ceiling**:
- agent "deep review" 上限：1-2 篇/天
- 伟烨 human review 上限：1 篇/天
- 实际一周 5-6 篇（按工作日）

**Why 9 topics + 1 week cleanup = 14 weeks**:
```
Week 1     : Cleanup unindexed 87 pages → 0 内容
Week 2-3   : 3 篇 (Maria case + SG 心脏 + CAR-T 淋巴瘤)
Week 4-5   : 3 篇 (膝关节 / MY 专区 / 拉美着陆页)
Week 6-8   : 3 篇 (印尼 / 巴基斯坦 / 肺癌 专题)
Week 9-14  : 复盘 + 第二轮选题 → 3-6 篇
```

**Lesson**: when the user asks "why so long for daily output?", don't hand-wave. Show the per-article work breakdown table and the week-by-week allocation. They get it in 5 seconds.

**Speed-up options** (only with explicit user buy-in):
- 现有计划 1 篇/week + agent审 + 你点头：默认推荐
- agent 审完直接发布 + 你仅周回顾 + 抽审：3-5 篇/week
- cron 自动发布：7 篇/week（YMYL 不推荐）

## B. Site-wide unindexed cleanup (236 URLs → 25-30 to dispose)

**The trigger**: Weiye said *"87 页没被收录"* — needed cleanup before adding new content.

**The actual scan** (`audit.py` ran 2026-07-21):

| 类别 | 数量 | 处置 |
|---|---|---|
| HEALTHY | 212 | 保留 |
| NO_SCHEMA | 6 | 加 JSON-LD |
| THIN | 4 | 合并 |
| TOO_SHORT | 8 | 强删 |
| BROKEN | 6 | 修或删 |
| 重复组 | 8 组 | 每组保留 1 个 + 301 |

**Total: 25-30 of 236 URLs to dispose (10-13%).**

**The audit.py script** (reusable for future scans):

```python
"""
Audit chinahospitalsguide.com for unindexed cleanup candidates.
"""
import urllib.request, re
from collections import defaultdict

SITEMAP_URL = "https://chinahospitalsguide.com/sitemap.xml"
sitemap_xml = urllib.request.urlopen(SITEMAP_URL, timeout=30).read().decode('utf-8')
urls = list(set(re.findall(r'<loc>([^<]+)</loc>', sitemap_xml)))
urls = [u for u in urls if 'chinahospitalsguide.com' in u]

def html_metrics(url):
    try:
        with urllib.request.urlopen(url, timeout=20) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
    except Exception as e:
        return {'url': url, 'status': 'error'}
    title_m = re.search(r'<title>([^<]+)</title>', html, re.IGNORECASE)
    title = title_m.group(1).strip() if title_m else ''
    desc_m = re.search(r'<meta\s+name=["\']description["\']\s+content=["\']([^"\']*)["\']', html, re.IGNORECASE)
    description = desc_m.group(1).strip() if desc_m else ''
    canon_m = re.search(r'<link[^>]*rel=["\']canonical["\'][^>]*href=["\']([^"\']*)["\']', html, re.IGNORECASE)
    canonical = canon_m.group(1).strip() if canon_m else ''
    robots_m = re.search(r'<meta\s+name=["\']robots["\']\s+content=["\']([^"\']*)["\']', html, re.IGNORECASE)
    robots = robots_m.group(1).strip() if robots_m else 'no-meta'
    schema_count = html.count('application/ld+json')
    body_m = re.search(r'<body[^>]*>(.*?)</body>', html, re.IGNORECASE | re.DOTALL)
    body_text = body_m.group(1) if body_m else html
    body_text = re.sub(r'<script[^>]*>.*?</script>', '', body_text, flags=re.DOTALL | re.IGNORECASE)
    body_text = re.sub(r'<style[^>]*>.*?</style>', '', body_text, flags=re.DOTALL | re.IGNORECASE)
    body_text = re.sub(r'<[^>]+>', ' ', body_text)
    body_text = re.sub(r'\s+', ' ', body_text).strip()
    word_count = len(body_text.split())
    return {'url': url, 'status': 200, 'title': title, 'desc_len': len(description),
            'canonical': canonical, 'robots': robots, 'schema_count': schema_count,
            'word_count': word_count}

def categorize(m):
    if m.get('status') != 200: return 'BROKEN'
    if m.get('word_count', 0) < 150: return 'TOO_SHORT'
    if m.get('word_count', 0) < 400: return 'THIN'
    if m.get('schema_count', 0) == 0: return 'NO_SCHEMA'
    return 'HEALTHY'

results = []
for u in urls:
    m = html_metrics(u)
    results.append({**m, 'category': categorize(m)})

# Detect duplicate title groups
title_groups = defaultdict(list)
for m in results:
    if not m.get('title'): continue
    prefix = ' '.join(m['title'].split()[:5]).lower()
    prefix = re.sub(r'\| china hospitals guide.*$', '', prefix).strip()
    title_groups[prefix].append(m['url'])

dup_groups = {k: v for k, v in title_groups.items() if len(v) > 1}

cat_counts = defaultdict(int)
for m in results:
    cat_counts[m['category']] += 1

print(f"HEALTHY: {cat_counts['HEALTHY']}")
print(f"NO_SCHEMA: {cat_counts['NO_SCHEMA']}")
print(f"THIN: {cat_counts['THIN']}")
print(f"TOO_SHORT: {cat_counts['TOO_SHORT']}")
print(f"BROKEN: {cat_counts['BROKEN']}")
print(f"Duplicate title groups: {len(dup_groups)}")
```

**5 cleanup gotchas**:

1. **没有 GSC "Why pages aren't indexed" CLI access** — only web UI; 需伟烨导出 CSV 交叉对比
2. **删 URL 会导致流量下降 4-6 周** — 不是立竿见影
3. **合并必须配 301** — 没 301 流量归零
4. **加 Schema 用 `inject_schemas_safe()`** — 防止破坏现有 Schema
5. **删 25-30 页 ≠ 解决 crawl budget** — 可能根本是 Google 信任分问题

**Pre-flight checklist before deleting any URL**:

```bash
# 1. Verify no other pages link to the deleted slug
grep -rE "deleted-slug" /home/ubuntu/chinahospitalsguide --include="*.html" -l

# 2. Verify no sitemap entry exists
grep -E "deleted-slug" /home/ubuntu/chinahospitalsguide/sitemap.xml

# 3. If both empty → safe to delete + add 301 in _redirects

# 4. Commit message must explain:
#    - What was deleted
#    - What 301 was added
#    - What category (TOO_SHORT/BROKEN/THIN/dup) for audit trail
```

## C. Playwright headless HTML→PNG pipeline (朋友圈自动化)

**The trigger**: Weiye said *"你直接发图给我"* after I asked him to manually screenshot 6 HTML files in Chrome.

**The reality**: I cannot directly produce PNG images. Had to install Playwright + Chromium headless in the venv.

**The install sequence** (one-time, in venv):

```bash
# In Hermes venv (PEP 668 doesn't block venv)
~/.hermes/hermes-agent/venv/bin/python -m pip install playwright

# Download Chromium headless shell (~114MB)
~/.hermes/hermes-agent/venv/bin/python -m playwright install chromium --with-deps
```

**The render script** (saved at `chinahospitalsguide/figma-friends-circle/render-to-png.py`):

```python
import asyncio, os, glob
from pathlib import Path
from playwright.async_api import async_playwright

ROOT = Path("/path/to/figma-friends-circle")
OUT = ROOT / "png"; OUT.mkdir(exist_ok=True)
HTML_FILES = sorted(glob.glob(str(ROOT / "*.html")))

async def render_one(browser, html_path):
    page = await browser.new_page(viewport={"width": 1080, "height": 1350})
    await page.goto(f"file://{html_path}", wait_until="networkidle")
    width, height = await page.evaluate("""() => {
        const card = document.querySelector('.card') || document.body;
        const r = card.getBoundingClientRect();
        return [Math.ceil(r.width), Math.ceil(r.height)];
    }""")
    await page.set_viewport_size({"width": width, "height": height})
    await page.wait_for_timeout(150)
    out_path = OUT / f"{html_path.stem}.png"
    await page.screenshot(path=str(out_path), full_page=False)
    await page.close()
    return out_path, width, height

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        for f in HTML_FILES:
            out, w, h = await render_one(browser, Path(f))
            print(f"  ✓ {Path(f).name}  {w}x{h}  {os.path.getsize(out)/1024:.1f} KB")
        await browser.close()

asyncio.run(main())
```

**Gotchas** (encoded in `patient-cases-public-outreach` skill):

- `networkidle` 在带 Google Fonts 的 HTML 会卡 30 秒 —— HTML 里只用系统字体
- HTML 里**不要写 viewport meta** —— Playwright 按 `set_viewport_size` 来
- 多张图批量：每张独立 `new_page`，**关闭前 `await page.close()`**，不图省事复用 page
- `render-to-png.py` 是 untracked 脚本，跟 HTML 同目录；不进 git

**HTML 路径 vs Playwright 自动化的取舍**:

| 维度 | HTML 路径（伟烨手动截图） | Playwright 自动化 |
|---|---|---|
| 适用 | 伟烨有空 / 想本地控制 | 伟烨直接要图 / 批量出 |
| 风险 | 浏览器兼容性 | 无头渲染稳定 |
| 时间 | 伟烨手动 5 分钟 | agent 自动 30 秒 |
| **默认路径** | 第一次出图（让伟烨看效果） | 后续批量化（风格定了后） |

## D. The "right now" / 节奏 control lesson (cross-cuts multiple skills)

**The trigger**: Maria Rios case, two emails within 12 hours. Weiye was about to send 2 emails in one night to the same patient.

**The pitfall**: Maria anxiety case (chronic anxiety, weight loss, 4.5-year search) would feel pressured. "She is taking care of me" → "she is pressuring me".

**The fix** (encoded in `medical-tourism-client-intake` SKILL.md):

- 第 1 封（叙事/进展类）跟第 2 封（动作确认类）之间**至少 12 小时间隔**
- 如果伟烨说"我现在就发"，**主动提一句**："建议明天白天发，给 Maria 一晚消化上一封"
- 伟烨说"没事，我现在就发"——就发，但**主动提醒了就是 audit pass**

**Also**: "I am passing... right now" 措辞必须先核实伟烨的实际状态再写。如果患者实际还没点头，或者伟烨实际还没把联系方式发给医院，写了"right now"就是不实表述 → 患者等不到医生联系 → 信任裂缝。

**Drafting question** before any "right now" email:

```
Q: 伟烨已发 / 准备发 / 没发，要我帮你起给医院的邮件？
   A1 已发    → "I have passed..." (完成时)
   A2 准备发  → "I will pass... today" (将来时)
   A3 没发    → "I will draft an inquiry... and pass once you confirm"
```

## E. QQ Mail / 飞书复制粘贴 兼容性

**The trigger**: Weiye uses QQ Mail web version; my draft had `### Heading` Markdown which QQ Mail renders as literal text.

**The fix**:

- 给邮件正文用**最简形式**：纯文本 + 空行分段，**不写 ### 标题符**
- 需要"标题层级" → 用粗体 `**Title**` 而不是 `#`
- 飞书对话里分隔符用 `---`，但**两侧各一个空行 + 单独成行**，让伟烨一眼看出"这是分隔符别粘"
- 起草时**先假设接收端按字面渲染**，不用任何依赖语法的标记

## F. The verification mindset (reaffirmation)

- **Verify EVERY claim from another agent**: agent's "did X" must be independently verified (`os.path.exists`, `grep -c`, `curl -I`).
- **"改好了" can mean 3 states**: A (pushed), B (local edit), C (elsewhere). Pre-flight check (fetch + status + log) before doing anything.
- **Schema audits must verify URL values, not just structure**: `schema.org` could be corrupted by over-eager regex.
- **Cosmetic vs functional**: text format / RTL hack / build artifact residue — don't waste cycles. Focus on conversion path + schema validity + functional bugs.

## G. The "三伏贴 / 中国特色轻医疗产品" 跨境电商 vs 增值品 议题

Weiye asked about adding a 跨境保健品/三伏贴 e-commerce section. My honest push-back (4 options):

- A. 停在文案层（不做事） — default 最低成本
- B. 加 1 个英文资讯页（不卖货） — 试水
- C. 跨境保健品独立电商站 — **不推荐**（合规 + 履约 + 客服成本极高；跨境保健品是红海）
- D. "轻医疗包"作为协调服务增值品（¥199/¥399/¥699） — **最推荐**

**Why D is the right path**:
- 不需要新网站 / 新域名
- 不需要多国合规（卖给已在中国/已回国的患者）
- 客单价高 ¥199-699
- 转化路径短（已在 pipeline 里）
- 提升 case 客单价

**Weiye said "暂时不需要处理"** — 归档到 pending，不动。

## H. 修复周期 vs pending 议题清单

**这会话推进 / 完成了**：
- chinahospitalsguide.com 1 commit 拉本地（`50f3e15`）
- Hermes 升级到 v0.18.2
- Maria Rios 案 4 封邮件（最终确认 + 联系方式转交）
- 朋友圈 HTML 6 张 + Playwright 自动出 PNG
- 内容规划 Week 0-6 序列 + unindexed 清理 audit

**这会话没动但已识别**：
- Week 0 cleanup 实际执行（25-30 页处置 + 301）
- Week 1-6 内容生产（Maria case / CAR-T 淋巴瘤 / SG 心脏等）
- 三伏贴 / 轻医疗包 业务方向（pending）

**修复流程状态**：chinahospitalsguide 9.5/10 健康度；Maria Rios 案在等九院医生主动联系 Maria；Hermes 0.18.2 已升级。