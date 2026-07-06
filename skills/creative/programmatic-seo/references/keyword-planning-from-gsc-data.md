# Keyword Planning: From Real GSC Data, Not From Theory

Companion to the SKILL.md workflow. Read this when the user asks for a content/keyword/SEO **strategy** (not for writing today's article).

## The trap

It is tempting to immediately produce a 3-6 month content roadmap: layer 1 daily, layer 2 programmatic pillar, layer 3 conversion content. Do NOT do that. A roadmap built on assumed search volumes is content-mill theater. The user has already been burned by this — they will interrupt you with "先别规划，让我先看现有数据" if you skip the data step.

## Correct order

1. **Pull GSC data first.** Use the per-site CLI (see `references/oriental-destiny-gsc-snapshot-2026-07-06.md` for the snapshot recipe).
   - `gsco summary 60` — totals
   - `gsco top q 30` — actual queries that have any impression
   - `gsco top p 30` — actual pages that have any impression
   - `gsco opportunities` — high-impression low-CTR rewrite candidates
   - `gsco trends 90` — daily trend to see if impressions are even climbing

2. **Read the numbers as a sandbox diagnostic.** If impressions < 500 over 60 days and avg position is in the 60-100 band, the site is in Google Sandbox. Say so directly. Don't pretend the content is "almost working."

3. **Identify which categories of already-written content have shown up in GSC.** For oriental-destiny.com (snapshot 2026-07-06):
   - Bazi fundamentals ("bazi day master", "bazi five elements") → pages: what-is-day-master.html, five-elements-explained.html
   - Element / calculator ("feng shui element calculator", "element calculator") → pages: element-calculator.html, kua_calculator.html
   - Feng shui commercial ("feng shui bracelet meaning", "taoism jewelry") → pages: feng-shui-bracelet-meaning.html, daoist-treasures.html
   - Conversion pages (instant_reading.html at position 69.7, bazi-guide.html at position 13.8) → these are the highest-leverage existing assets

   Notably absent: all 36 daily "Fire Month / Earth Month" seasonal feng shui articles. Zero impressions. They are publishing into a void.

4. **Present 3-4 options with the data as evidence.** Do NOT present an opinionated single plan. Format:
   - A: stop seasonal pipeline, write 4 articles targeting the actual impressions
   - B: reduce cadence, mix keyword-matrix days with seasonal days
   - C: dual-track, cron unchanged + manual keyword-matrix articles weekly
   - D: zero new content, fix indexing / sitemap / mobile first

   Always include a "D" option because the data usually shows the priority is plumbing, not writing.

5. **Wait for the user to pick.** Then act on the pick. Do not pre-commit or start writing on assumption.

## Common "wrong first move" patterns to avoid

- Producing a 3-layer architecture when 0 pages have ranked
- Recommending "write more seasonal articles" when GSC shows seasonal terms get 0 impressions
- Setting monthly article quotas before checking whether any daily article has indexed
- Treating the user's "先看数据" response as a delay tactic — it is them saving you from wasted work
- Optimistically extrapolating one well-performing page to mean the whole site is healthy

## What "the data" looks like for a sandbox-stage English-language SEO site

Reference snapshot from oriental-destiny.com on 2026-07-06 (60-day window):

| Metric | Value | Implication |
|---|---|---|
| Total clicks | 0 | No organic traffic |
| Total impressions | 127 | Google has indexed a tiny fraction |
| Avg position | 62.1 | 4-5 pages deep |
| CTR | 0.00% | No ranking high enough for clicks |
| Daily impressions trend | Flat at 0-11/day | Not climbing |
| Top query | "bazi day master" — 23 impr, pos 82 | Foundation keyword, not yet ranking |
| Top page | what-is-day-master.html — 38 impr, pos 76.3 | Single pillar showing movement |
| Mobile share | 3.1% (4/127) | Mobile likely broken or non-indexed |
| Geo | USA 45.7%, SGP 24.4%, AUS 7.1% | English-speaking, not just US |

Sites that look like this need 3-6 more months of disciplined publishing + on-page SEO before expecting clicks. The honest framing is "we are building toward ranking, not yet earning traffic."