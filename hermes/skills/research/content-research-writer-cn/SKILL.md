---
name: content-research-writer-cn
description: "Research Chinese medical/health news热点 for daily article publishing on chinahospitalsguide.com. Find timely, relevant stories from Chinese medical sources."
version: 1.0.0
author: Hermes Agent
platforms: [linux]
metadata:
  hermes:
    tags: [research, chinese, medical, health, news, content, seo]
    category: research
---

# Content Research: Chinese Medical News (医疗新闻热点研究)

Research Chinese medical/health news热点 for daily article publishing on chinahospitalsguide.com.

## Context

- Website: https://chinahospitalsguide.com (medical tourism guide for China)
- Article output: `news/` directory, file naming `YYYY-MM-DD.html`
- Publishing cadence: 1 article per day (栏目新建期)
- Quality bar: 去AI化评分 >60; no good热点 = no publish (宁缺毋滥)

## Research Sources

Prioritize these for Chinese medical/health news:

- **丁香园** (dxy.cn) — most authoritative Chinese medical professional portal
- **健康报** (jkj.cnjkw.com) — 人民健康网 (People's Health) — state medical newspaper
- **国家卫健委** (nhc.gov.cn) — official policy announcements
- **医学界** (yiduozhe.com) — medical news
- **澎湃新闻** (thepaper.cn) — general news with health section
- **财新** (caixin.com) — health policy coverage
- **PubMed/知网** — for cutting-edge clinical research
- **微博热搜** — trending health topics (weibo.com)
- **微信搜索** — 搜一搜 health articles

## Additional High-Value International Sources

For clinical advances with Chinese relevance (新疗法, 新药上市, 国际临床试验), also check:
- **ASCO** (asco.org) — oncology congresses, published June 2026 with CROWN trial 7-year data
- **ESMO**, **AHA**, **ACC** — major congresses with Chinese hospital co-authorship
- **NEJM**, **The Lancet**, **JAMA** — high-impact clinical papers with Chinese authors
- Congress press releases often have the best patient-facing summaries

**Pitfall**: High-quality international clinical data (e.g., ASCO abstract releases) can outrank Chinese domestic sources for clinical progress topics. Check congress websites directly when domestic sources are thin.

## Hot Topic Categories (优先级排序)

1. **重大政策** — 医保改革, 分级诊疗, 药品审评审批, 医疗器械政策
2. **公共卫生** — 传染病疫情, 疫苗, 慢性病防控
3. **临床进展** — 新疗法, 新药上市, 手术突破, 基因治疗
4. **国际合作** — 中外医疗合作, 进口药, 国际临床试验
5. **AI/数字医疗** — 医疗AI, 远程医疗, 智慧医院
6. **患者故事** — 真实就医经历 (适合旅游场景)
7. **医疗机构动态** — 知名医院新技术/新科室

## Research Process

1. **Daily scan** — check headlines from above sources (morning recommended)
2. **Evaluate novelty** — is this genuinely new? Or already covered recently on the site?
3. **Assess relevance** — does it connect to medical tourism themes? (international patients, quality hospitals, advanced treatments, medical travel logistics)
4. **Select top story** — pick the strongest candidate; skip if nothing meets bar
5. **Document source** — record URL, publication date, key facts for citation

## Output

Return to the workflow:
- 热点标题 (title)
- 关键信息点 (3-5 bullet facts)
- 原始来源 (source URL + date)
- 是否适合发布 (yes/no — if no, explain why)

## Integration

This skill feeds into `programmatic-seo` for the writing phase. Run research first, then pass findings to the SEO writer skill.

## Quality Gate

- Must have: credible source, recent date (within 48h preferred), medical accuracy
- Must avoid:旧闻 (old news), rumor/unverified claims, politically sensitive topics
- If no story meets bar: report "无可用热点，跳过今日发布" and stop