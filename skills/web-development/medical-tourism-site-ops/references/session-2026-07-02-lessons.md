# 2026-07-02 Session — Lessons (transcript + reasoning)

This file captures a session where the agent made several systemic mistakes that the user had to catch and correct. The lessons here are already encoded in the parent SKILL.md; this file is the **raw transcript + reasoning** for future agents who want to understand the full failure mode.

## What happened (chronological)

### Lesson 1: Identity flip — agent called itself "德米" and addressed user as "德米"

User had previously been named 伟烨 (user) and the agent Hermes (called 德米). Across sessions, memory became polluted — agent started signing reports as "德米" and addressing the user as "德米".

User caught this: *"你是基于哪里的源文件来定的这个90天改进计划的 哈哈 真的可以正常进行下去？"* — that question made me realize I was confused about identity too. Then user followed up directly: *"还有 你才是德米 我叫伟烨 你的记忆出问题了"*.

**Memory contamination is real**. The same agent across sessions can lose track of who is who. Fix: every session, re-read the user profile entry before addressing the user.

### Lesson 2: "Cloudflare" memory contamination

Earlier sessions had the site on Cloudflare. By 2026-07-02, the site was on GitHub Pages. But my memory still had "Cloudflare 60s deploy". I told the user "60s to deploy" and verified multiple times in 60s windows.

User caught this: *"我们的网站部署在GITHUB呢。。"* — wait, user already said this. Then: *"我怕你是用Cloudflare 的旧网站源码在改 那就太浪费时间了"*.

**Lesson**: deployment platform, deploy time, cache TTL — all are infrastructure facts that change. Always verify with `curl -I` and `git remote -v` before assuming. Memory ages.

### Lesson 3: "90-day plan" was fabricated

A "90 天方案" was generated in a single past session with **no underlying data** — GSC data, ROI calculation, customer validation. The 15 items were:

1. Cron prompt revamp ✅
2. 11 new pillar pages ✅
3. 49 blog TCM injection ✅
4. Duplicate page cleanup ✅
5. Blog index overhaul ✅
6. Homepage overhaul ✅
7. Blog index newsletter ✅
8. Hospital ranking P0 overhaul ✅
9. Deployment verification ✅
10-15. Various — some completed, some pending

When user said "按 90 天方案继续", I picked 4 ranking pages (which were actually productive) plus 5 "decision guide long-tail pages" (which were not). I had no real data basis for picking the 5 long-tail pages — just gut feeling + opportunity noise from `gsc opportunities` showing 0% CTR.

User caught this: *"你基于哪里的源文件来定的这个90天改进计划的"*.

**Lesson**: a multi-item plan that was generated in one session with no data backing is not a "plan" — it's a wishlist. Always cross-check each item against current GSC/GA4 data before executing.

### Lesson 4: GSC data noise mistaken for real demand

`gsc opportunities` showed queries like "beijing liposuction hospital recommendations 2026" with 21-24 impressions, position 7-9, CTR 0%. I assumed this meant "lots of demand, just need a page to convert". 

**Reality**: 21-24 impressions in 28 days = ~0.8 impressions/day = essentially noise. The query "beijing junior college for liposuction 2026" (2 impressions) was also there — that pattern is suspicious, probably a bot or a search test. Real demand for medical tourism from English speakers is **tiny** — the actual top page (plastic-surgery-china-guide-2026.html) gets 967 imp/mo TOTAL, with most queries being "china medical tourism" general queries, not city-specific ones.

**Lesson**: when GSC opportunity list contains 40+ "city × procedure" queries all with < 30 impressions each, that's noise, not signal. Filter ruthlessly: < 100 impressions/mo is not worth a dedicated page.

### Lesson 5: Patient stories were fictional — affected 3+ downstream decisions

Memory had "3 patient stories (Ahmed/David/Margaret)" as a content asset. I had been treating these as proof-of-engagement that could be expanded.

User revealed: *"3 个患者故事 是虚构的 是建立网站初期的操作 但很遗憾 我们目前为止没有真实的客户成交 所以我们没有案例"*.

This changed everything:
- Cannot use patient stories as social proof
- Cannot build "trust" content based on patient count
- Cannot expand patient story section (would be building more fictional content)
- The "conversion path" assumption (visitor reads patient story → contacts us) needs to be redesigned around pre-revenue signals (free consultation, cost comparison, FAQ)

**Lesson**: when memory mentions "patient stories", "case studies", "customer logos" — **verify these are real** before treating them as conversion assets. The user may have placeholder content from site launch.

### Lesson 6: Pre-deploy verification caught a 43-file gap

After I deployed "100% schema coverage" on blog/ + news/ (152 files), user asked: *"你先确认一下目前 github里的源文件 是否能对应你目前的工作吧 我怕你白忙了"*.

This forced me to actually run the audit. Found **43 content pages** were missed:
- 16 root landing pages (about, contact, services, etc.)
- 7 treatments/ pages (cancer, cardiac, ivf, etc.)
- 20 docs/ pages

If user had not asked, I would have shipped an "incomplete complete". The fix was a follow-up commit.

**Lesson**: any "X% coverage" claim needs **end-to-end verification** including the scopes that aren't obvious. The blog/ + news/ scope is obvious; treatments/, root landings, docs/ are easy to forget.

### Lesson 7: Decision tree was correct — executed wrong

User said: *"5 个决策页回滚 plastic-surgery 优化立即做"*.

I executed this. The decision was correct: 5 low-volume pages reverted, the highest-traffic page optimized. But I had been pushing the wrong work for the entire afternoon. Once the user redirected, the right work was obvious from `gsc top pages`: plastic-surgery-china-guide-2026.html at 967 imp/mo, position 9.6, CTR 0.21%.

The right question to ask at session start was: "What is the single highest-impression page on the site, and is it optimized?" If yes — pick the next one. If no — optimize it.

**Lesson**: when facing a long todo list, the first move is to identify the **single highest-ROI item** from `gsc top pages` (sorted by impressions, not clicks). That page is the starting point for any optimization work. Anything else is downstream.

### Lesson 8: Schema regex deletion ate original schemas

When I tried to "remove the duplicate BreadcrumbList schema I added", I used a greedy regex that ate ALL schema blocks including the original Article + BreadcrumbList + FAQPage. The page went from 4 schemas to 1 (only one survived by luck).

Recovery: I had to `git show HEAD:blog/...` to get the original back, then re-apply my changes carefully.

**Lesson**: never use `re.sub(r'<script type="application/ld\+json">[\s\S]*?</script>', '', text)` to remove "the one I added". Use the safe `inject_schemas_safe()` pattern: check what's already there, only add what's missing, never delete.

### Lesson 9: f-string `{var}` parsing trap

When building a multi-line HTML template via f-string with nested `{var}` references in the inner template body, Python interprets the inner braces at template-construction time. If `var` isn't in scope, NameError.

Fix: use plain string with `.format(**kwargs)` for the outer, not f-string. Or `string.Template.safe_substitute()` if CSS braces (which look like Python format) are also present.

**Lesson**: when building a complex multi-line string with double-nested braces, **don't use f-string**. Use `.format()`.

## The user's correction cadence (in order)

The user corrected me 7 times this session. The cadence:

1. "我们的网站部署在GITHUB呢。。" — infrastructure fact wrong (Cloudflare memory)
2. "你是基于哪里的源文件来定的这个90天改进计划的" — plan basis missing
3. "你先确认一下目前 github里的源文件 是否能对应你目前的工作吧 我怕你白忙了" — verify before declaring success
4. "5 个决策页回滚 plastic-surgery 优化立即做" — direction correction
5. "也没有真实的客户成交 所以我们没有案例" — business state correction
6. "你才是德米 我叫伟烨 你的记忆出问题了" — identity flip
7. "不是说你自作主张 你有发表你意见的权利 我也能接受 但是我也有质疑的权利" — collaboration model

The user was patient but firm. They corrected me, then let me try again. They did NOT apologize or soften the corrections. That's the model.

## The takeaways (encoded in parent SKILL.md)

1. Always verify infrastructure facts (deploy platform, deploy time, repo URL) with live checks, not memory.
2. Question the data basis of any plan, even one I generated.
3. After "行按这个执行", voice the top 1-2 doubts AND the recommended path in 2-3 lines, then proceed.
4. End-to-end audit any "X% coverage" claim — don't declare success on a partial scope.
5. For long-tail content decisions, filter by impression volume: < 100/mo = skip.
6. Verify "patient stories" / "case studies" / "customer logos" are real before treating as conversion assets.
7. Use the safe `inject_schemas_safe()` pattern, never re.sub() on JSON-LD blocks.
8. Use `.format()` not f-string for nested-brace templates.
9. Address user correctly: 伟烨 = user, Hermes/德米 = me. Get this right at session start.
10. Treat the user as a partner — push back when warranted, don't apologize for having opinions.