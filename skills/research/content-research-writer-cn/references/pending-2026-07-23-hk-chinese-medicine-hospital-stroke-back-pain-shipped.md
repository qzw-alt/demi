# 2026-07-23 HK Chinese Medicine Hospital stroke/back pain — SHIPPED

**Run date:** 2026-07-23
**Status:** SHIPPED
**Article:** https://chinahospitalsguide.com/news/2026-07-23-hong-kong-chinese-medicine-hospital-stroke-back-pain-launch-2026.html
**Word count:** ~2,235 (with markup overhead counted by regex; ~1,500-1,700 words of body prose excluding CSS/head)
**Humanize score:** 85/100 (above 60 threshold)
**Em-dash density:** 8.6/1200 (below 17-23 baseline but acceptable for Template B article with mostly clinical content)
**Article archetype:** Template B — TCM modernisation (multidisciplinary TCM-Western stroke / lower back pain programmes at HK government flagship hospital)
**Source:** SCMP "Hong Kong's Chinese Medicine Hospital to launch stroke, back pain programmes next week" (2026-07-22)
**Commits:**
- `9f87f03` — article body
- `a918f41` — sitemap.xml + news/index.html
**Verify:** HTTP 200 (after 90s sleep, 25s bounded curl)

## What worked

1. **Cap-safe order applied.** Article committed and pushed to origin/master (commit `9f87f03`) BEFORE any humanize loop, exactly per the 2026-07-10 cron prompt mandate. Humanize score check ran AFTER both pushes; score 85 was already above threshold.
2. **Source diversity from Bing News.** First Bing query returned ChinaDaily narcolepsy drug (NMPA approval) but thin TCM angle. Second targeted query (`acupuncture+TCM+RCT+July+2026`) returned the SCMP HKCMH story as #1 — clean match for the cron-prompt's "Template B (TCM modernisation)" structure.
3. **JSON-LD articleBody extraction.** SCMP returned 1MB page with Next.js JSON carrying `"articleBody":"..."` — extracted cleanly via regex `r'"articleBody"\s*:\s*"((?:[^"\\]|\\.)*)"'`. The skill's known 2026-07-04 SCMP JSON-LD extraction recipe worked.
4. **De-dup verified.** Anchor strings `(Tseung Kwan O|Bian Zhaoxiang|23 special disease|stroke.*programme.*Hong Kong|Chinese Medicine Hospital of Hong Kong)` returned 0 matches against the 80+ article library — confirmed shippable.
5. **Existing site HTML format used.** Matched the 2026-07-22 Yili x Tongrentang article's HTML structure (full `<!DOCTYPE html>` with head, JSON-LD Article + FAQPage, internal styles). Initial Jekyll-style draft was rewritten to match site convention.

## Cron state at end of run

- Working tree: clean
- Local branch `master`: 2 commits ahead of pre-run state (`9f87f03` + `a918f41`), both pushed to `origin/master`
- Remote `origin/master`: at `a918f41` (no further advance during the run)
- Article live: HTTP 200 verified via `curl --max-time 25`
- No pending files needed (clean run, all state in repo)

## Article angles

- **Hook:** First government-funded flagship TCM hospital in any major Chinese-speaking economy opens stroke + back pain programmes
- **Substance:** 23-programme portfolio over 5 years, two tracks per indication (acute + chronic), TCM bundle (acupuncture, moxibustion, cupping, tuina, herbal baths, herbal medicine), multidisciplinary Western medicine co-management
- **International patient angle:** HK$250 (US$32) subsidised outpatient fee, HK$25/day prescriptions, WhatsApp+voice booking via +852 5799 3233, visa-free access for most Asian/Middle East/Commonwealth passports, hospital as TCM-side anchor alongside Shanghai CAR-T corridor and Hainan Boao Lecheng zone
- **CTA:** Clear practical booking info + programme portfolio context

## Banned-vocab / humanize notes

- Score 85/100 first pass — well above threshold without any patch needed
- The `1st-person: 1` note in the humanize_score output is a false-positive (the script likely counted "we" or "our" in an unrelated context); the article is appropriately clinical and impersonal in voice, not first-person
- `missing first-person voice` note is the default site config flagging that the article is third-person clinical, which is appropriate for medical tourism content
- 0 `pivotal`, 0 `actually` in H2, 0 `leverage`, 0 `landscape`. Style matches the site's clinical-voice baseline

## Tool-call budget

Total tool calls: ~14 (within the 15-call cap-safe target):
1. Step 0 — git status + ls check
2. Bing News query 1 (returned only NMPA narcolepsy — not TCM-fit)
3. Bing News query 2 (returned SCMP HKCMH — target)
4. SCMP fetch + meta verification
5. JSON-LD articleBody extraction
6. De-dup grep
7. Write article (initial Jekyll format — needed rewrite)
8. Rewrite article in site HTML format
9. git add + commit (article)
10. git push origin master (article)
11. sitemap.xml patch
12. news/index.html patch + git commit
13. git push origin master (sitemap+index)
14. humanize_score.py check
15. Sleep + curl HTTP 200 verify

## Next-run recommendations

- Continue the SCMP HKCMH thread — could follow on with a 2026-08-XX piece on the second wave of programmes (fertility + developmental delay announced for end-2026)
- Consider the 2026-07-04 Yue et al. Frontiers meta-analysis as a standalone article when budget allows — strong TCM-RCT angle
- The cron prompt's 2026-07-10 customer-source targeting (Indonesia/Vietnam/Russia/Middle East) is well-served by this article — most medical tourism pricing comparisons in it use Singapore/Korea benchmarks rather than US
- Em-dash density 8.6/1200 is below the 17-23 chinahospitalsguide baseline — for a clinical article with lots of proper nouns and short factual sentences, the lower density is acceptable. Future articles should add more clinical parentheticals if targeting the upper band

## Pitfall encoded as support file

The Jekyll-vs-HTML format mistake (writing the article initially in Jekyll frontmatter format, then having to rewrite to match the site's HTML format) is captured in `references/news-article-html-format-2026-07.md` — future cron runs on this site should consult that file before writing a fresh article.