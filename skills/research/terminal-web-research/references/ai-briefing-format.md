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
- **Weekday mismatch** — running on Thursday but using Monday's date; always re-compute
- **Number provenance** — if you can't find the HN item or primary source, don't write the number. Hedge with "约" (about) or drop
- **Length creep** — six sections × three items each = 18 sentences; budget ~25 Chinese chars per sentence = 450 chars. Tighten anything longer
- **Emoji overuse** — one emoji per bullet, not per clause
- **Reusing last briefing's items** — for cron runs, always re-fetch; HN stories from 7 days ago are stale