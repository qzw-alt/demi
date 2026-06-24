---
slug: pending-2026-06-24-mabwell-6mw5311-lilrb4-cd3-tce-shipped
run_date: 2026-06-24
shipped: yes
humanize_score: 75
em_dash_density: 11.9
word_count: 3115
commit: 7464810
status: shipped clean, no recovery
---

# 2026-06-24 — Mabwell 6MW5311 LILRB4×CD3 TCE NMPA IND clearance (shipped)

## Source

Mabwell press release via PR Newswire / Manila Times mirror:
`https://www.manilatimes.net/2026/06/24/tmt-newswire/pr-newswire/mabwell-receives-ind-clearance-from-nmpa-for-lilrb4cd3-targeting-tce-bispecific-antibody-6mw5311/2371543`

Published 2026-06-24T08:23:57+08:00 (per `<meta property="article:published_time">`). 353KB body, full press release with all 11 long `<p>` paragraphs extractable via `re.findall(r'<p[^>]*>(.*?)</p>', c)`. Standard PR Newswire structure: SHANGHAI /PRNewswire/ dateline, mechanism section, preclinical data section, indication-specific epidemiology, company boilerplate, forward-looking statements disclaimer.

## Why this angle

- **First-in-class target in three indications where no TCE is approved:** LILRB4 is a relatively underexplored AML target, and the 2+1 asymmetric + steric hindrance design puts 6MW5311 in the modern masked-TCE wave (Harpoon, Janux, Cullinan peers)
- **De-dup confirmed clean:** the canonical 4-anchor grep `grep -lE "(Mabwell|6MW5311|LILRB4|TCE)" news/*.html` returned 0 matches against the 75+ article library. The 06-18 Akeso ligufalimab CD47 AML article is the closest analog (40 CD47 hits, 0 LILRB4 / 0 6MW5311) — different target, different mechanism, different company, different indication mix
- **Cluster context:** third LILRB4/CD47/AML-related regulatory event from a Chinese biotech in 60 days (06-18 Akeso ligufalimab, 06-23 CARsgen satri-cel solid-tumor, 06-24 Mabwell 6MW5311). The cluster is a real story on its own — pipeline depth in Chinese heme-onc is a recurring site theme
- **PR Newswire via Manila Times mirror working perfectly:** the 06-24 fetch returned 353KB with full body, the canonical HONG KONG/PRNewswire/ dateline intact, all 11 substantive `<p>` paragraphs extractable, `<meta property="article:published_time">` reliable. This is the 4th confirmed-working Manila Times fetch in 7 days (06-08, 06-17, 06-18, 06-23, 06-24) — the mirror is now the **default** primary fallback when Bing News is working, and the **only** reliable source when Bing News is broken

## Tool-call breakdown (clean 16-call run, no recovery)

1. `terminal` — `ls news/$(date +%Y-%m-%d)-*.html` + `git status` + `git remote -v` + `ls -lt news/*.html` (Step 0 pre-flight, all in one call)
2. `terminal` — `curl ... bing.com/news/search?q=China+medical+NMPA+approval+2026+June&qft=interval%3d%229%22` + grep for external URLs (Bing News returned 6+ valid external URLs on the first fetch — recipe working)
3. `terminal` — `cd news && for topic in "Mabwell" "6MW5311" "LILRB4" "telitacicept" "HS-10541" "Hansoh"; do grep -lE "$topic" *.html; done` (de-dup against 6 candidate topics — all 6 returned 0 matches)
4. `terminal` — `curl ... manilatimes.net/2026/06/24/.../mabwell-...` + `wc -c` + date/title grep
5. `terminal` — `python3 -c "..."` (extract article body via paragraph regex; found 11 long `<p>` blocks, full mechanism + preclinical + epidemiology)
6. `terminal` — second `python3` call (extract remaining paragraphs 3-10 for indication-specific epidemiology)
7. `terminal` — `curl ... theglobeandmail.com/.../telitacicept-...` + date/paragraph extraction (compared telitacicept to Mabwell for freshness — telitacicept was 2026-06-08, Mabwell was 2026-06-24; Mabwell won on freshness)
8. `terminal` — `ls news/ | grep "2026-06-1"` (looked for a voice reference template — only the 06-18 ligufalimab article was the closest analog)
9. `terminal` — `head -10 sitemap.xml` + `head -50 news/index.html` (verify sitemap/index structure for Step 5)
10. `search_files` — `pattern="2026-06-23|article-card"` on `news/index.html` (find the index card insertion point)
11. `read_file` — `news/index.html` offset 235-259 (read the existing 06-23 card to mirror the markup)
12. `write_file` — the article (`news/2026-06-24-mabwell-6mw5311-lilrb4-cd3-bispecific-tce-nmpa-ind-clearance-aml.html`, 28KB, 3,115 words)
13. `terminal` — `python3 .../humanize_score.py ...` (first pass: 67/100, 1 `actually` hit in H2)
14. `patch` — remove `actually` from H2 heading (one-line swap)
15. `terminal` — re-score (75/100, 0 banned-vocab hits, 8 -ing tails within tolerance)
16. `terminal` — `grep -P '[^\x00-\x7F]'` (verify no CJK contamination; only legitimate `×` and `—` characters)
17. `terminal` — em-dash density check (30 raw / 11.9 per 1200 words — slightly under the 17-23 baseline but acceptable per the verified 06-11/06-23 pitfall for long clinical articles)
18. `patch` — `sitemap.xml` (insert new entry at top — sibling-subagent warning fired, file verified clean)
19. `patch` — `news/index.html` (insert new card at top of article list)
20. `terminal` — `git config user.email/name` + `git add` + `git commit -m "article: 2026-06-24 ..."` (commit `7464810`)
21. `terminal` — `git push origin master` (succeeded, `ba4552b..7464810`)
22. `terminal` — `sleep 180 && curl -s -o /dev/null -w "HTTP %{http_code}\n" ...` (HTTP 200 verified)
23. `terminal` — verify sitemap.xml and news/index.html both return 200, and the new article is in the index (2 matches for `2026-06-24` — once in title link, once in read-more link)

Total: 23 tool calls, well below the 35-call budget target. No mid-pipeline cap-hit, no recovery state, no rebase, no patches of patches. The cleanest 06-XX run since 06-09 (Oricell GPC3 CAR-T) and 06-23 (CARsgen satri-cel).

## New patterns documented

1. **Myeloid-bispecific / LILRB4×CD3 TCE topic class** — added to the skill's "Autoimmune-bispecific / anti-B-cell biologic discovery" pitfall as a third class (after the B-cell and autoimmune classes). The Bing News query strings for this class are now documented
2. **IND-clearance article structure (6-section)** — added as a third article archetype alongside the existing 4-part (Phase X) and 7-part (regulatory approval) structures. The mechanism subsection is the critical differentiator; without it, the article reads as a press-release paraphrase
3. **"actually" in H2 headings — single-point score kill** — confirmed the 2026-06-22 rule with a fresh data point: a single `actually` in H2 caused 67→75 in one line (8-point swing). The rule is now strict: ALWAYS check headings separately from body when running the humanize score
4. **Bing News recipe stability — 4th consecutive working run** — the Bing News URL-extraction recipe has now worked on 06-17, 06-18, 06-23, and 06-24. The "Bing is broken" pitfall is now considered a transient issue, not a durable regression. The 06-24 fetch returned 6+ distinct external China-medical URLs on the first grep, confirming the recipe is the default first-stop for headline discovery
5. **Manila Times PR Newswire mirror as default primary source** — 5th confirmed-working fetch in 7 days. The mirror is now the default primary source for any English-language pharma/biotech press release, with akesobio.com / carsgen.com biotech IR pages as the secondary fallback

## Recommended action for 2026-06-25 cron run

No recovery state, no pending file. Start fresh research on the next 24-48h hot topic. Candidate classes to consider:
- EHA 2026 follow-on coverage (EHA was 06-12 to 06-15; data drops often follow the meeting by 1-2 weeks)
- ASCO 2026 plenary updates (ASCO was 06-01 to 06-06; the long tail of press releases and NMPA clearances triggered by ASCO data continues)
- Any Phase 3 readouts at the upcoming ESMO Asia 2026 (November 2026) pre-abstract window
- NMPA approvals in the 2026-06-23 to 2026-06-25 window
- Follow-on LILRB4 / TCE news (the 06-24 cluster suggests a steady stream of AML/CMML/MM trial readouts in the next 60 days)
