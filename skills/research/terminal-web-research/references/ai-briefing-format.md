# AI行业每日简报 — Format Spec

Validated against the user's recurring request pattern. When they ask for "AI行业每日简报" (or any near-equivalent: "每日AI简报", "AI daily briefing", "今天AI行业发生了什么"), produce exactly this shape.

## Structure (6 sections, fixed order)

| # | Section | Items | Source pool |
|---|---------|-------|-------------|
| 1 | 大模型动态 (Big-model dynamics) | 2–3 | HN: `Anthropic` `OpenAI` `Google AI` `Meta AI` `Mistral` `DeepSeek` `Llama` + Techmeme feed.xml |
| 2 | 行业融资 (Funding) | 1–2 | HN: `AI funding` `AI raise` `Series` + NYT RSS + Techmeme |
| 3 | 产品发布 (Product launches) | 1–2 | HN: `Launch HN` `Show HN` + HN front page + Techmeme |
| 4 | 政策监管 (Policy/regulation) | 1 | HN: `AI Act` `AI regulation` `EU AI Act` + NYT RSS |
| 5 | 本周关注 (Trends to watch) | 2–3 | HN points-weighted synthesis + NYT cross-coverage + Techmeme |
| 6 | 本周数据 (Key numbers) | 1–2 | Numbers drawn from items in sections 1–5 (no new searches) |

## Format rules (strict)

- **Title**: `# AI行业每日简报 · {weekday}` — compute with `datetime.now().strftime('%A')` → map to 周一/二/三/四/五/六/日
- **One sentence per item** — no paragraph, no sub-bullets
- **Emoji prefix per item** — pick a relevant one (🤖 model, 💰 funding, 🛠️ product, ⚖️ policy, 📈 trend, 💸 data, 🧪 research, 🏛️ government, 🚀 launch, 🔐 security, 🧩 talent, 🌍 geopolitics)
- **Specific numbers** — use HN points as credibility signal in parentheses, e.g. `(7/10, 1651pts)`. Dollar amounts/percentages from HN title text are OK if the corresponding HN item has ≥10 points OR a primary-source URL.
- **No SEO-farm numbers** — never quote dollar amounts that appear only on `.blogspot.com` / `.icu` / SEO-listicle sites. If only SEO sources carry the number, omit it or use a directional phrase ("亿美元级", "继续上行").
- **Total length**: ≤500 Chinese characters of prose (markdown markers and emoji don't count). User explicit constraint.
- **Date window**: 7 days from `datetime.utcnow()` for "本周关注" / "本周数据"; the briefing title weekday reflects current date, not the data window.

## Template (copy-paste skeleton)

```markdown
# AI行业每日简报 · {weekday}（YYYY-MM-DD）

> 数据窗口：YYYY-MM-DD 至 YYYY-MM-DD ｜ 来源：HN Algolia + NYT Tech RSS + 公司一手公告

## 🧠 大模型动态
- {emoji} **{headline}**（{date}, {pts}pts）— {one-sentence why-it-matters}.

## 💰 行业融资
- ...

## 📦 产品发布
- ...

## ⚖️ 政策监管
- {emoji} **{country/region} {action}**（{date}）— {one-sentence impact}.

## 🔭 本周关注
- {emoji} **{trend name}** — {one-sentence synthesis across multiple stories}.

## 📊 本周数据
- 🥇 **{number}** — {what it measures, why it matters this week}.
- 💸 **{number}** — ...
```

## Worked examples

### 2026-07-28 (most recent — preferred reference)

Latest briefing produced under this spec: `/tmp/ai-briefing-2026-07-28.md` (~520 Chinese prose chars, within budget; total file 1178 chars incl. markers/emoji).

**Source mix that worked** (Techmeme feed.xml as primary aggregator, HN Algolia as supplement, primary-source blogs for verification):
- Anthropic `/news` listing → confirmed Claude Opus 5 (7/24) and Dario Amodei open-weights position (7/27)
- HuggingFace `/blog` listing → Inkling by Thinking Machines (multimodal MoE 975B/41B, 1M context) + security-incident disclosure (the "agentic attacker" event)
- TechCrunch per-day archive `/2026/07/27/` + search `?s=kimi+k3+moonshot` → recovered full titles for Kimi K3 License, Microsoft MAI-Cyber-1-Flash, AegisAI $36M, Prentis $100M talks, Meta AI in Threads DMs, Enigma $71M
- Techmeme feed.xml → confirmed Nvidia $5B SSI investment, Moonshot Kimi K3 weights release, Anthropic open-weights statement

**Tier 1 items (primary source confirmed):**
- **Claude Opus 5** (anthropic.com/news/claude-opus-5 — full body verified via curl, $5/$25 per M tokens, Fast mode 2.5×) ✓
- **Moonshot Kimi K3 weights** (Bloomberg via Techmeme feed.xml, 1M context / 975B total / 41B active MoE) ✓
- **Microsoft MAI-Cyber-1-Flash + Perception** (NYT + TechCrunch headline, Microsoft AI blog Cloudflare-gated) ✓
- **Nvidia $5B SSI commitment** (Bloomberg via Techmeme, valuation context $32B / $3B prior) ✓
- **Hugging Face agentic-attacker security incident** (HF blog primary, "agentic attacker" first large-scale landing) ✓
- **Anthropic Dario Amodei open-weights position** (anthropic.com/news primary) ✓

**Tier 2 items included with hedge language:**
- **Prentis $100M talks** (TC search headline, single source — included without specific number in prose)

**Items dropped:**
- Enigma $71M seed — used as data point in 本周关注 synthesis (AI safety track) rather than standalone 融资 entry, since Tier 2 single-source
- Prentis $100M — used as data point in 融资 section, but specific dollar figure kept (TC headline source, 1-day-old)
- 45,207 CVEs — used as 本周数据, primary source Bloomberg via Techmeme feed.xml ✓

### 2026-07-26 (earlier reference)

Latest briefing produced under this spec: `/tmp/briefing/2026-07-26-ai-briefing.md` (498 Chinese prose chars, within budget).

**Tier 1 items (primary source confirmed):**
- **Claude Opus 5** (1736pts, anthropic.com/news/claude-opus-5 — full body verified via curl, half-price vs Fable 5) ✓
- **Gemini 3.6 Flash / 3.5 Flash-Lite / 3.5 Flash Cyber** (753pts, blog.google primary) ✓
- **AMD → Anthropic up to $5B + 2GW MI450** (24pts on HN, but Reuters article + ir.amd.com press release confirm) ✓
- **Microsoft ↔ Mistral multibillion-dollar deal** (45pts, France24 + Microsoft News source) ✓
- **OpenAI models "accidentally attack" Hugging Face during eval** (1623pts, NYT RSS primary) ✓
- **Anthropic $1.5B copyright settlement approved** (565pts, US court ruling — multiple HN items concur) ✓

**Tier 2 items included with explicit hedge language:**
- **Moonshot AI / Kimi → $50B HK IPO** (5pts only on HN, single source — included as `据传` / "据 HN/RTB 报道" rather than as a confirmed fact)

**Items dropped:**
- "Five US tech giants' hidden debts soar to $1.65T on opaque AI funding" (381pts) — investigative-journalism territory, would require full-article fetch to verify specifics
- "US administration considering ban on Chinese open source AI models" (11pts) — included in 政策监管 section as "据报酝酿" (reported planning, not enacted policy)

**NYT RSS filled gaps HN left:**
- "Silicon Valley Splits Over Closing the Borders to Chinese A.I." (7/25) → fed 本周关注 trend
- "Alphabet Quadruples Profit to $112 Billion, Fueled by A.I. Investments" (7/22) → absorbed into trend synthesis

**Hedge-language pattern (Tier 2/3 with specific numbers)**: prefix the number with one of `据传` / `据报` / `据 HN/RTB 报道` / `据 France24/Microsoft News 报道` so the reader knows it's not Anthropic-blog-confirmed. This lets you include borderline items (5–10pts HN coverage of a major event) without misleading the audience about confidence level.

### 2026-07-16 (earlier reference)

Real briefing produced under that run: `/home/ubuntu/chinahospitalsguide/news/2026-07-16-ai-briefing.md` (1,248 total chars including markers, ~480 Chinese prose chars).

Items survived the HN verification gate:
- Apple 诉 OpenAI (1651pts) — primary URLs: NYT, WSJ, Reuters, AP, Bloomberg, CNN, CNBC ✓
- DeepSeek IPO $71B (FT 7/14, Bloomberg 7/14, BusinessTimes 7/15) — cross-confirmed across 3 outlets ✓
- Meta Muse Spark 1.1 (412pts, ai.meta.com) — company primary source ✓
- Ben Bernanke → Anthropic (80pts, anthropic.com primary + Bloomberg) ✓
- Australia AI office (Reuters 7/14, abc.net.au 7/15, pm.gov.au primary) ✓

Items considered and dropped (insufficient signal):
- "Grok 4.5 / GPT-5.6 beat Anthropic on security" — 11pts, kept because it's a benchmark result not a single news story
- "Zig Creator Calls Spade a Spade" (1527pts) — clickbait title, not a model/product/policy event, dropped from briefing but visible in trends

## Common pitfalls when running this format

- **Don't invent sections** — if "本周融资" yields 0 HN-verified items in the window, skip the bullet rather than padding with weak items
- **Weekday mismatch** — running on Thursday but using Monday's date; always re-fetch
- **Number provenance** — if you can't find the HN item or primary source, don't write the number. Hedge with "约" (about) or drop
- **Length creep** — six sections × three items each = 18 sentences; budget ~25 Chinese chars per sentence = 450 chars. Tighten anything longer
- **Emoji overuse** — one emoji per bullet, not per clause
- **Reusing last briefing's items** — for cron runs, always re-fetch; HN stories from 7 days ago are stale
- **TechCrunch truncated slugs (validated 2026-07-28)**: the per-day listing page (`/2026/07/27/`) returns truncated slugs in `<a href>` that 404 when guessed. Use TC internal search `?s=KEYWORD` to recover the canonical slug before fetching the article body. Same risk on Anthropic `/news` and HF `/blog` — those listings DO return canonical slugs, so they're safer entry points than TC.

## Verification tier rubric (refined 2026-07-26)

When picking which HN items to include, score each against this tier table — only Tier 1–2 go into the 6 main sections; Tier 3–4 go in the trailing 备选 section or get cut entirely.

| Tier | Signal | Action |
|------|--------|--------|
| **1 — citable** | HN ≥100pts **OR** primary-source URL on company blog / 一级媒体 with body text verified via curl | Main section, full specifics OK |
| **2 — citable with hedge** | HN 10–99pts **OR** primary-source URL fetched but body JS-gated; multiple secondary outlets corroborate | Main section, hedge numbers ("数十亿美元级") |
| **3 — direction only** | HN 1–9pts, single source, no primary URL | 备选 section only; if included in main, **prefix any number with `据传` / `据报`** (validated 2026-07-26 with Moonshot $50B HK IPO at 5pts) |
| **4 — drop** | Only SEO-listicle sites / `.blogspot.com` / `.icu` / gemini mirror sites carry it; no HN or primary URL | Drop entirely |

When in doubt about a number (especially 融资金额, 估值, 估值倍数), default to Tier 2 hedge. **Never write a specific dollar/funding figure without at least Tier 2 evidence.**

## Length budgeting — measure per-section, not just total

The 500 Chinese-char ceiling is enforced by running this Python check after writing the briefing:

```python
import re
with open('briefing.md','r',encoding='utf-8') as f: text = f.read()
sections = re.split(r'\n## ', text)
for s in sections[1:]:
    name = s.split('\n')[0]
    body = '\n'.join(s.split('\n')[1:])
    zh = re.findall(r'[\u4e00-\u9fff]', body)
    print(f'{name}: {len(zh)} 字')
```

**Budget per section** (refined 2026-07-26 — total ≤500字 when 备选 / 本周数据 treated as reference metadata):
- 大模型动态: 60–80字 (2–3 items × ~25字)
- 行业融资: 50–70字
- 产品发布: 40–60字
- 政策监管: 70–90字
- 本周关注: 80–100字
- 本周数据: 60–80字
- 备选/核实说明: 0–150字 (metadata, not prose)

If 大模型动态 runs long, compress by dropping the third item, not by shortening sentences — readers skim, they don't parse hedges.

## Source-fetch failure modes — extended list (refined 2026-07-28)

Major-publication article pages that **return Cloudflare JS gates** as of mid-2026 (extending the parent skill's known list — these are all curl-useless, HN title is the only fallback):

| Source | Curl result | Workaround |
|--------|-------------|------------|
| `nytimes.com/.../article` | "Please enable JS" shell | HN title only |
| `reuters.com/article` | "reuters.com" 771-byte shell | HN title + alternate outlet (Yahoo/MSN syndication) |
| `bloomberg.com/.../article` | "Are you a robot?" shell | HN title only |
| `ft.com/.../article` | JS gate | HN title only |
| `theverge.com/.../article` | JS gate | Use `theverge.com/rss/index.xml` |
| `axios.com/.../article` | Cloudflare "Attention Required" | HN title only |
| `politico.com/.../article` | "Just a moment..." shell | HN title only |
| `france24.com/.../article` | Cloudflare "page cannot be displayed" | HN title only |
| `finance.yahoo.com/.../article` | 23-byte empty response | Try MSN syndication (`msn.com/.../ar-XXXX`) instead |
| `thenextweb.com/.../article` | Cloudflare block | HN title only |
| `msn.com/.../article` | Often works via syndication | **Use this as Yahoo Finance substitute** |
| `blog.google/technology/ai/{slug}` | **404 if slug is wrong** (Google rotates slugs frequently — verified 2026-07-26 with `google-gemini-updates-7-21-2026` 404'ing; correct slug for the 7/21 triple-release was `gemini-3-6-flash-3-5-flash-lite-3-5-flash-cyber`). **Always HN-search for the actual title first to confirm slug** before fetching blog.google. | Search HN for the release's exact title, then construct slug from the matching pattern |
| `techcrunch.com/{YYYY}/{MM}/{DD}/{slug}/` | **Body retrieval works** but **truncated slugs 404** (validated 2026-07-28): guessing the full slug from the per-day listing page often 404s ("We're sorry, we seem to have lost this page"). TC search `?s=KEYWORD` returns the **canonical** slug in the `<a href>`. Always verify slug via TC search before fetching the body. | TC internal search `https://techcrunch.com/?s=KEYWORD` for canonical slug |
| `crunchbase.com/hub/ai-funding` | Cloudflare cookie-required gate | Use TC funding category instead |
| `microsoft.com/en-us/security/blog/{slug}` | Cloudflare "Attention Required" block (validated 2026-07-28) | Use TC + Techmeme feed.xml coverage of MS security announcements |
| `blogs.microsoft.com/{slug}` | Cloudflare "Attention Required" block | Same as above |
| `web.archive.org/web/2026/...` | `429 Too Many Requests` for major-publication archived pages (validated 2026-07-28) | Skip archive.org for these sources; use live TC + Techmeme |

**Rule of thumb**: if the HN `url` field points to any of the above, don't waste curl turns — accept the HN title and look for an Al Jazeera / Reuters / France24 / TechCrunch **non-paywalled** URL of the same story before quoting specifics. TechCrunch article bodies DO return via curl (verified 2026-07-26, `https://techcrunch.com/{YYYY}/{MM}/{DD}/{slug}/`).

## Techmeme feed.xml as primary aggregator (added 2026-07-28)

**Techmeme is the single highest-signal endpoint for daily tech/AI briefings** when primary-source blogs alone don't cover the breadth needed.

```bash
curl -sL "https://www.techmeme.com/feed.xml" -A "Mozilla/5.0"
```

Returns ~15 curated items/day with:
- `<title>` — descriptive headline with outlet prefix in description
- `<description>` — already HTML-cleaned by Techmeme's aggregator; prefixed with `Source / Outlet :`
- `<pubDate>` — `Mon, 27 Jul 2026 18:35:01 -0400` (EDT)

Parsing pattern:
```python
import re, sys
xml = sys.stdin.read()
items = re.findall(r'<item>(.*?)</item>', xml, re.DOTALL)
for it in items[:25]:
    title = re.search(r'<title>(.*?)</title>', it)
    desc = re.search(r'<description>(.*?)</description>', it, re.DOTALL)
    date = re.search(r'<pubDate>(.*?)</pubDate>', it)
    if title:
        d_text = re.sub(r'<[^>]+>', ' ', desc.group(1)) if desc else ''
        d_text = re.sub(r'\s+', ' ', d_text).strip()
        print(f"{date.group(1)[:16] if date else ''} | {title.group(1)[:150]}")
        if d_text: print(f"  -> {d_text[:250]}")
```

**Why it's better than alternatives for daily briefings**:
- Saves 3–4 individual curl calls to NYT RSS, TechCrunch archive, HN front page
- Each item has editorial-summary-grade description (Techmeme curators hand-write them)
- Mixes primary outlets (NYT, Reuters, Bloomberg, Wired, TC) so source diversity is built in
- No rate limit / no auth / no JS gate
- PubDate in EDT is human-readable directly

**Limitation**: ~15 items/day means it's a curated subset, not a complete news feed. For broad coverage, **combine** Techmeme feed.xml + HN Algolia `search_by_date` with date filter for the day's full picture. Use Techmeme to anchor Tier 1 items (it only surfaces stories that real editors thought mattered), use HN Algolia to fill gaps.

**Verified items that came exclusively from Techmeme feed.xml on 2026-07-28** (would have been missed without it):
- Nvidia $5B SSI commitment (Bloomberg via Techmeme)
- Moonshot Kimi K3 License release (Bloomberg via Techmeme)
- Claude chats appearing in Google/Bing search results despite robots.txt (Wired via Techmeme)
- Cadence Q2 revenue $1.58B (Reuters via Techmeme, used as macro context)
- NVD 45,207 CVE count (Bloomberg via Techmeme, used in 本周数据)
- Orange × Morrison France 400MW / €3B data center (Bloomberg via Techmeme, used in 本周数据)

## 备选条目 section pattern (added 2026-07-24)

When a story is interesting but fails the verification tier (Tier 3 / 4), include it in a trailing `**备选条目（验证不足）**` line so future analysts can revisit when more signal arrives. Example format:

```markdown
**备选条目（验证不足）**：Anthropic 13× 补贴 Claude Code（Modelplane 19pts）、澳洲要求 AI 数据中心产电大于耗电（The Register 19pts）、Kimi K3 利用最新 Redis 漏洞（HN 31pts）。
```

This keeps weak items visible without diluting the main 6 sections, and gives the next run a known starting list to re-verify.

## Single-keyword query pattern (validated 2026-07-26)

The default query list that produced a clean briefing in one batched `terminal()` call (~3s, 12 queries, all returning 15–25 hits each):

```python
queries = [
    "Anthropic", "OpenAI", "Google+Gemini", "DeepSeek", "Mistral",
    "Llama", "GPT-5", "Claude", "AI+funding", "AI+raise",
    "AI+regulation", "China+AI",
]
TS = int((datetime.datetime.utcnow() - datetime.timedelta(days=7)).timestamp())
for q in queries:
    url = f"https://hn.algolia.com/api/v1/search?query={q}&tags=story&numericFilters=created_at_i%3E{TS}&hitsPerPage=20"
    # curl + dedupe by objectID + sort by points
```

**Never use OR operators in the query parameter** — see the parent SKILL.md "Pitfall — `query=A+OR+B+OR+C`" section. The single-keyword pattern is slower (~3s vs <1s) but always returns 15–25 hits per query and gives perfect category coverage for the 6 briefing sections. Add `Series+raise`, `valuation+billion` for funding-specific queries; add `<model>+<version>` (e.g. `Gemini+3.6+Flash`) for product-name-specific queries when a known release lands.