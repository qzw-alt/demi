# Competitor Benchmarking for SEO Content Sites

When the user asks to plan a content direction, **benchmark competitors first** — before keyword planning, before topic generation, before writing anything. The user explicitly stated this preference on 2026-07-06: *"其实目前最好就是对标一下竞品公司 分析一下数据 来指导我们的方向"*.

This document covers the methodology, the data sources, and the pitfall-avoidance patterns. The SKILL.md has the high-level trigger; this file has the recipe.

## Why this is non-negotiable

The failure mode that the user's correction prevents:

1. A request like "规划一下未来 6 个月的关键词方向" triggers an LLM-generated plan based on SEO best-practice patterns (节气 → 五行 → 月度 cadence).
2. The plan looks coherent internally but allocates effort to keywords that have near-zero search volume. Example from 2026-07-06: oriental-destiny.com shipped 30 "Fire Month Feng Shui" articles that showed **zero** impressions in GSC's top-50 query list. The cadence was internally consistent but externally invisible.
3. Cost: wasted cron output, cron cap-hits, human review time, and a missed opportunity to capture the niche's actual search demand.

## The mandatory 3-step sequence

When asked to plan a content direction, run these in order:

### Step 1: Pull GSC data (30 seconds)

```bash
gsc summary 90       # overall traffic trend
gsc top q 30         # top 30 search queries by impressions
gsc top p 30         # top 30 pages by impressions
gsc opportunities    # impressions >= 5 + position <= 20 + CTR < 5% = snippet gold
```

What you're looking for: which clusters are ALREADY getting impressions. Those clusters are where the plan should focus — not on new clusters the LLM invented.

For the multi-site pattern (oriental-destiny.com + chinahospitalsguide.com + future sites): copy `~/.hermes/bin/gsc` to `~/.hermes/bin/gsco`, change the SITE constant + URL-rewrite strings. Same token works across all verified sites on the account (verified 2026-07-06).

### Step 2: Benchmark competitors (10-20 minutes)

Delegate to a subagent with this spec (do not do inline — competing with a fresh context window):

```
Goal: Produce a competitor benchmark table for <site> in the <niche> vertical.

Data sources (in priority order):
1. Sitemap enumeration: fetch /sitemap.xml or /sitemap_index.xml at each candidate domain
   - count total URLs in post-sitemap.xml + page-sitemap.xml + sub-sitemaps
   - identify the cluster distribution (e.g. cafeastrology.com: 13436 URLs, 16 chinese-related = 0.12%)
2. Public key-page grabs: robots.txt + 5-10 representative cluster pages
   - extract: title, meta description, h1/h2 count, internal links count, schema.org presence, word count
3. Tranco list check: https://tranco-list.eu/api/ranks/domain/<domain> — free, no API key
   - tells you whether the domain is in the global top-1M (proxy for traffic tier)

Candidate domains (start with these, expand based on the niche):
- Direct competitors: sites targeting the same audience with the same content type
- Adjacent competitors: sites covering 20%+ of the same topic with a different framing
- Paid-platform competitors: services monetizing the same audience differently (commercial-model benchmark)

Deliverable: a markdown table with columns:
| 域名 | 规模 (URLs) | 内容垂直度 | 域名权重 | 商业模式 | 主要短板 |

Plus a "空白市场" section listing niches that NONE of the competitors are covering.
```

### Step 3: Plan keywords (only against steps 1 and 2)

A keyword plan that isn't grounded in either GSC data or competitor coverage will get sent back. The plan should answer:

1. **Which clusters already get impressions** (extend these — don't abandon them)
2. **Which competitor clusters have low depth** (overtake with deeper content)
3. **Which competitor niches are empty** (build the cluster from scratch)
4. **What content depth beats the median competitor** (word count, schema, internal links, FAQ)

## Worked example: oriental-destiny.com (2026-07-06)

Trigger: *"规划以后的关键词以及内容方向"*

**Step 1 — GSC data (60 days):**
- 0 clicks, 127 impressions, average position 62.1 (sandbox)
- Top queries: `bazi day master` (23), `bazi five elements` (7), `feng shui bracelet meaning` (6), `bazi vs western astrology` (5), `5 elements` (4), `day master` (4)
- Top pages: `what-is-day-master.html` (38), `five-elements-explained.html` (25), `feng-shui-bracelet-meaning.html` (14)
- **No impressions from the 36 daily "Fire Month Feng Shui" articles** — the existing cadence is invisible to Google

**Step 2 — Competitor benchmark (11 domains):**

| 梯队 | 域名 | URLs | Chinese 类垂直度 | 商业模式 |
|---|---|---|---|---|
| 我们 | oriental-destiny.com | 104 | 100% | 免费 BaZi + instant_reading |
| 命理大站 | cafeastrology.com | 13,436 | **0.12% (16篇)** | 免费 + Premium Reports |
| 命理大站 | astrology.com | 大型 | 有频道但旧 | content + premium |
| 直接竞品 | fengshuibeginner.com | ~90 | 100% | 广告 + Amazon affiliate |
| 直接竞品 | bazi-calculator.com | 软件站 | 100% | 卖软件 |
| 直接竞品 | learnbazi.com | **1KB（空白站）** | 100% | — |
| 付费平台 | kasamba.com | 中 | 0% (178字) | $5-10/分钟聊天 |
| 付费平台 | mysticsense.com | 中 | 0% | 类似 Kasamba |

**空白市场 finding:** cafeastrology.com has 13,436 URLs but only 16 Chinese-related articles (0.12%), and ZERO of those are BaZi deep-dive or Feng Shui deep-dive. fengshuibeginner.com covers Feng Shui objects but not BaZi systems. **The english BaZi-systems-depth niche is genuinely empty.**

**Step 3 — Resulting plan:**
- Stop the Fire-Month cadence (zero impressions for 30 articles shipped)
- Add 10 Feng Shui object articles in the fengshuibeginner style (the cluster with proven search demand)
- Reinforce existing pillars with stronger internal linking (target: position improvement from 80+ to 50+)
- Defer: cadence changes (Phase 2), conversion funnel redesign (Phase 2)

Outcome: 10 object articles shipped in parallel via subagent delegation, sitemap updated to 108 URLs, ready for GSC submission (manual because token is readonly).

## Pitfalls

**Don't benchmark via Similarweb/Ahrefs anonymously** — both 403 anonymous requests. Use sitemap enumeration + key-page grabs + Tranco instead. They're free, no API key, and answer 80% of "what's the competitor doing" questions.

**Don't benchmark the wrong competitor tier.** A direct competitor is someone targeting the same audience with the same content type. A paid-platform competitor is a commercial-model benchmark, not a content competitor. A generalist site (thespruce.com) covering 0.1% of feng shui is not a competitor; it's a publisher that happens to have an article.

**Don't treat LLM knowledge of competitors as data.** "I know cafeastrology has a chinese astrology section" is not a benchmark — it's a memory check. The benchmark requires actual page grabs showing word counts, schema presence, and last-modified dates.

**Don't skip the empty-niche finding.** The most valuable row of the benchmark is the row that says "all 8 competitors have <100 words on this topic." That's where the 6-month moat gets built.

## Reusable: what to grab per competitor (snippet)

```python
# Per competitor, in parallel (10-15 concurrent)
def fetch_metadata(domain):
    # 1. robots.txt → sitemap URL discovery
    # 2. sitemap.xml + sitemap_index.xml → URL count + cluster distribution
    # 3. homepage + 3-5 cluster pages → title/desc/h1/h2/internal_links/schema/word_count
    # 4. Tranco rank check
    return {domain: {size, vertical_pct, word_count_baseline, schema_presence, last_updated, ...}}
```

Typical benchmark surface area:
- 30-60 minutes for 10 competitors with parallel fetching
- 10-20 MB of body text for cluster analysis
- 1-2 KB markdown deliverable per competitor row

## Step 4: Bulk-pillar sprint (verified 2026-07-06)

After the benchmark + GSC top-queries picture is complete, **the highest-ROI action is usually to bulk-rewrite existing pillar pages into the depth/structure that the empty-niche finding demands**. The 2026-07-06 oriental-destiny.com session shipped four commits in one session because this pattern was discovered:

| Phase | Commit | Output |
|---|---|---|
| Phase 1 | `77b0936` | 10 Feng Shui object articles (filling fengshuibeginner-style cluster) |
| Phase 2 | `2eb7e73` | 12 zodiac + 2 mega-pillars + footer cross-link fix + robots.txt relaxation |
| Phase 3 | `d86f1d2` | 10 day-master pillar deep rewrites |
| Phase 4 | `a230368` | 3 GSC-validated query-fillers (mantra bracelet / does-it-work / free-bazi-reading) |

Total: 35 new or rewritten pillar pages, ~125,000 words, all pushed to `main` in one session.

### The bulk-pillar recipe (4 layers)

**Layer 1 — Tier-classify the existing pillars.** Don't write blindly. Before delegating, derive the page-by-page target list from GSC top queries + the empty-niche finding:

| GSC-validated query (28d) | Existing page | Action |
|---|---|---|
| `bazi day master` (20i) | what-is-day-master (31i, pos 76.9) | Tier 1 — leave alone (ranking) |
| `bazi five elements` (7i) | five-elements-explained (21i, pos 85.7) | Tier 1 — leave alone |
| `bazi vs western astrology` (5i) | bazi-reading-vs-zodiac (6i, pos 49.5) | Tier 1 — near break-through |
| `feng shui mantra bracelet meaning` (1i, pos 96) | **NONE** | Tier 3 — write new |
| `do feng shui bracelets really work` (1i, pos 87) | **NONE** | Tier 3 — write new |
| `free bazi reading` (1i, pos 82) | **NONE** | Tier 3 — write new |

Three categories:
- **Tier 1 (don't touch):** ranking decently — touching risks regression
- **Tier 2 (rewrite):** exist but too thin (e.g. 2,500 words when 4,500 is the depth bar) — preserve URL, rewrite
- **Tier 3 (write new):** GSC-validated queries with no existing page — write, new URL

**Layer 2 — Every subagent spec must include 6 things:**

1. **Exact target file path** (deterministic) — `rat-zodiac-sign.html`, not `chinese-zodiac-rat.html`
2. **Word count range** with bracket tolerance: `4000-4500 words (allow up to 5500 if extra depth is needed)`
3. **Internal link graph** — URLs that MUST appear in the body (every other pillar in the cluster + conversion target `instant_reading.html`)
4. **Schema requirement** — `Article + BreadcrumbList + FAQPage` as three separate JSON-LD blocks
5. **Design system match** — read one existing pillar in the same cluster, copy CSS class vocabulary (`element-banner`, `trait-grid`, `strength-weakness`, `years-table`, `career-table`, `lucky-grid`, `compat-card`, `fortune-section`, `fortune-grid`, `key-point`, `cta-box`, `faq-section`, `related-grid`)
6. **Element-specific design hook** — per-element color gradient (Rat = cinnabar Fire, Ox = pine Wood, Tiger = green Wood, etc.) so visually distinct

**Layer 3 — Run batches of 3-4 subagents in parallel.** Beyond 4 concurrent subagents the parent loses track, and spec-drift risk rises. The 2026-07-06 session ran four 3-task batches. After each batch, verify with `wc -l` + `grep 'application/ld+json'`, then launch the next. If a subagent times out, retry the single slug — not the whole batch.

**Layer 4 — Fix structural problems that the bulk content reveals.** The bulk-pillar sprint exposes three problems only visible after 30+ pillar pages:

1. **Footer orphans.** If `index.html` footer only links to 4-5 of them, the rest are orphan pages — Google gives them almost no internal-link authority. Fix with a footer link group: `Day Master Series` (10) / `Chinese Zodiac` (12) / `Feng Shui Objects` (11). The 2026-07-06 patch added 32 internal links in one block.

2. **robots.txt over-Disallow.** Common to over-Disallow calculator pages (`kua_calculator.html`, `element-calculator.html`) thinking it "hides" them from competitors. But calculator pages with natural-language explanations around the form are exactly the high-intent SEO bait. The 2026-07-06 fix unblocked both — Google indexes the prose without showing the form.

3. **sitemap.js drift.** `seo-generator/lib/sitemap.js` only knows about pages it has written. Bulk-pillar pages added outside the generator don't get into sitemap.xml automatically. After every batch:
   ```bash
   node -e "
   const { updateSitemap } = require('./seo-generator/lib/sitemap.js');
   const pages = [{loc: 'new-page-1.html', changefreq: 'monthly', priority: '0.8'}, ...];
   updateSitemap(pages);
   "
   ```

### The token-economics pattern

The user said *"不用担心token消耗"* (2026-07-06). When token is unconstrained, **maximize parallelism**:
- 3-4 subagents in flight
- Each writes 1 page (not 5)
- 4 batches × 3 tasks = 12 pages in ~25 minutes
- Commit at every 10-15 pages so mid-sprint crash doesn't lose work

When token IS constrained, **fall back to writing inline**. 1 page = 1,500-3,500 tool calls. 22 pages inline ≈ 660 calls — too many for a tight budget.

### When NOT to do the bulk-pillar sprint

- **When the daily-cadence cron is still useful.** Bulk sprint is complementary, not a replacement. Stop the cron only when measured (not assumed) that the cadence has zero search demand — and even then, reduce frequency rather than stopping.
- **When pillar pages already pass the depth bar.** If `what-is-day-master.html` is 4,500+ words with `Article + BreadcrumbList + FAQPage` schema and 6+ internal links, **leave it alone**. Tier 1 rule is hard.
- **When you've never done Step 1 + Step 2.** Bulk sprint with no benchmark data is just LLM-generated filler. Data-first ordering makes the difference between real SEO value and word count.

### Bulk-pillar sprint checklist

```
[ ] Step 1: GSC top queries for last 28 days
[ ] Step 2: Competitor benchmark → empty-niche finding
[ ] Step 3: Tier 1/2/3 classification of all current pillars
[ ] Step 4: URL list for Tier 2 rewrites and Tier 3 new pages
[ ] Step 5: For each batch of 3-4 subagents, write spec with all 6 delegation requirements
[ ] Step 6: After each batch, wc -l + grep schema check
[ ] Step 7: Commit at every 10-15 pages with descriptive phase-N message
[ ] Step 8: Update sitemap.js after each batch
[ ] Step 9: After all batches, footer cross-link audit + robots.txt audit
[ ] Step 10: Final push + report
```

The 2026-07-06 sprint completed all 10 in roughly 90 minutes wall clock + 4 commits.

## Path note (corrected 2026-07-06)

The original Step 1/2 text referenced `~/.hermes/memories/layer3/research/competitor-research.md`. That path is **wrong** as of the memory-architecture refactor. The real locations:
- GSC token: `~/.hermes/gsc/token.json` (read-only by default; see `seo-article-publish-cron/scripts/gsc-token-upgrade.sh` for upgrade flow)
- GSC scripts: `~/.hermes/bin/gsc` (one site) + `~/.hermes/bin/gsco` (oriental-destiny copy)
- Research notes: no longer in memory — competitor data goes into the site repo under `/home/ubuntu/<site>/competitor-benchmarks-YYYY-MM-DD.md`

Benchmark files live next to the site, not in memory, because:
1. Memory has 2,200-char cap; benchmark files are 5-30 KB
2. Memory is per-session; benchmark files need cross-session + cron visibility
3. The benchmark file IS the SEO rollout plan — when Phase 2/3/4 land, it becomes the deliverable record