---
name: ai-industry-daily-brief
description: Generate a concise, data-driven daily AI industry brief in Chinese with emojis, strict length control, and current news.
category: research
triggers:
  - user asks for "AI industry daily brief" / "AI行业每日简报" / "AI简报"
  - cron job generating a daily AI brief
  - request for a short, structured AI news summary with numbers
tags:
  - ai
  - news
  - brief
  - chinese
  - cron
---

# AI Industry Daily Brief

## Goal
Produce a short, current, factual AI industry brief in Chinese, covering model releases, funding, products, policy, trends, and key numbers, all within a strict character budget.

## Steps
1. **Set the date and day.** Use the current date; title format: `# AI行业每日简报 | 星期X`.
2. **Collect sources** (parallel where possible):
   - Hacker News front page for trending AI/tech stories.
   - The Verge AI section.
   - TechCrunch AI / Startups / Security / Government sections.
   - Company blogs: OpenAI, Anthropic, Google DeepMind, Google AI.
   - Use `r.jina.ai/http://URL` to bypass bot detection on company blogs.
3. **Extract and categorize** items into: 大模型动态, 行业融资, 产品发布, 政策监管, 本周关注, 本周数据.
4. **Verify numbers.** Before using any figure, cross-check it appears in an accessible source. Avoid relying on 404 links or unverified headlines.
5. **Draft in Chinese.** One sentence per item, with specific numbers and dates. Add section emojis.
6. **Enforce length.** Count characters. If the user asks “500字以内”, aim for total rendered text (including spaces/newlines) under 500; otherwise ensure Chinese characters are under the limit.
7. **Trim.** Remove lower-priority items or adjectives, keep the most important numbers.
8. **Final output.** Return only the brief; no extra commentary.

## Pitfalls
- **Do not fabricate data.** If a source is blocked, use an alternative or omit the item.
- **Do not assume “字” means only CJK characters.** For “500字以内” constraints, count the whole rendered text and trim.
- **Company blogs often block browser tools.** Fall back to `r.jina.ai/http://...` or Hacker News discussion.
- **Funding numbers from headlines can be stale or unverified.** Open the article or use a reliable source before citing.
- **Avoid over-explaining.** The brief should be one sentence per item.

## Verification
- Confirm each numbered claim is traceable to a source from the current day or previous 24h.
- Re-run the character count after any edit.

## References
- See `references/sources.md` for reliable starting URLs.
- See `references/template.md` for a reusable brief skeleton.
