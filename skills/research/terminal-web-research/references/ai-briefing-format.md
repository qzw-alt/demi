# AI行业每日简报 — Format Spec

Validated against the user's recurring request pattern. When they ask for "AI行业每日简报" (or any near-equivalent: "每日AI简报", "AI daily briefing", "今天AI行业发生了什么"), produce exactly this shape.

## Structure (6 sections, fixed order)

| # | Section | Items | Source pool |
|---|---------|-------|-------------|
| 1 | 大模型动态 (Big-model dynamics) | 2–3 | HN: `Anthropic` `OpenAI` `Google AI` `Meta AI` `Mistral` `DeepSeek` `Llama` |
| 2 | 行业融资 (Funding) | 1–2 | HN: `AI funding` `AI raise` `Series` + NYT RSS |
| 3 | 产品发布 (Product launches) | 1–2 | HN: `Launch HN` `Show HN` + HN front page |
| 4 | 政策监管 (Policy/regulation) | 1 | HN: `AI Act` `AI regulation` `EU AI Act` + NYT RSS |
| 5 | 本周关注 (Trends to watch) | 2–3 | HN points-weighted synthesis + NYT cross-coverage |
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

## Worked example (validated 2026-07-16)

Real briefing produced under this spec: `/home/ubuntu/chinahospitalsguide/news/2026-07-16-ai-briefing.md` (1,248 total chars including markers, ~480 Chinese prose chars).

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

## Verification tier rubric (refined 2026-07-24)

When picking which HN items to include, score each against this tier table — only Tier 1–2 go into the 6 main sections; Tier 3–4 go in the trailing 备选 section or get cut entirely.

| Tier | Signal | Action |
|------|--------|--------|
| **1 — citable** | HN ≥100pts **OR** primary-source URL on company blog / 一级媒体 with body text verified via curl | Main section, full specifics OK |
| **2 — citable with hedge** | HN 10–99pts **OR** primary-source URL fetched but body JS-gated; multiple secondary outlets corroborate | Main section, hedge numbers ("数十亿美元级") |
| **3 — direction only** | HN 1–9pts, single source, no primary URL | 备选 section only; no specific numbers |
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

**Budget per section** (refined 2026-07-24 — total ≤500字 when 备选 / 本周数据 treated as reference metadata):
- 大模型动态: 60–80字 (2–3 items × ~25字)
- 行业融资: 50–70字
- 产品发布: 40–60字
- 政策监管: 70–90字
- 本周关注: 80–100字
- 本周数据: 60–80字
- 备选/核实说明: 0–150字 (metadata, not prose)

If 大模型动态 runs long, compress by dropping the third item, not by shortening sentences — readers skim, they don't parse hedges.

## Source-fetch failure modes — extended list (refined 2026-07-24)

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

**Rule of thumb**: if the HN `url` field points to any of the above, don't waste curl turns — accept the HN title and look for an Al Jazeera / Reuters / France24 / TechCrunch **non-paywalled** URL of the same story before quoting specifics. TechCrunch article bodies DO return via curl (verified 2026-07-24, `https://techcrunch.com/{YYYY}/{MM}/{DD}/{slug}/`).

## 备选条目 section pattern (added 2026-07-24)

When a story is interesting but fails the verification tier (Tier 3 / 4), include it in a trailing `**备选条目（验证不足）**` line so future analysts can revisit when more signal arrives. Example format:

```markdown
**备选条目（验证不足）**：Anthropic 13× 补贴 Claude Code（Modelplane 19pts）、澳洲要求 AI 数据中心产电大于耗电（The Register 19pts）、Kimi K3 利用最新 Redis 漏洞（HN 31pts）。
```

This keeps weak items visible without diluting the main 6 sections, and gives the next run a known starting list to re-verify.