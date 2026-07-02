# Source patterns added 2026-07-02: ABC News tier + Two-meta-analysis contrast framing + Remote-advance standard practice

## ABC News (abc.net.au) — seventh-tier generic-Western-news source for Cochrane / Lancet / NEJM / JAMA meta-analyses (verified 2026-07-02, acupuncture-IVF add-on story)

When the canonical source for a meta-analysis or systematic review is behind Cloudflare (The Lancet, NEJM, JAMA direct fetches, plus The Economist, Wiley, Springer), **www.abc.net.au/news/health/...** is a reliable working source for the same story.

The 2026-07-02 run needed The Lancet Obstetrics, Gynaecology & Women's Health meta-review of 10 IVF add-ons (Lensen et al., 24 June 2026, DOI 10.1016/s3050-5038(26)00054-3) and `thelancet.com` returned Cloudflare challenge; the same story was covered by ABC News at `https://www.abc.net.au/news/health/2026-06-24/ivf-australia-add-on-treatment/106818036`, which returned **425KB of full article body HTML** including 61 substantive paragraphs, all extractable via standard `<p>` regex.

The body includes the lead author's full name and affiliation, the headline statistic (7 of 10 add-ons with no evidence of benefit), the named-expert quotes (Sarah Lensen, Devini Ameratunga, Kath Whitton, Genia Rozen), the cost figures (A$810M Australian IVF add-on industry, A$1,000-A$3,000 out-of-pocket per cycle, patient story of Deanna Carr spending A$60,000 over 4 years), and the second-paper reference to the codesigned IVF information website published in the same journal.

Date verification: `<meta property="article:published_time" content="2026-06-23T22:00:00+00:00">` is reliable. The article also includes a `<meta itemprop="datePublished">` field. Both align with the URL date in `/YYYY-MM-DD/`.

**Body extraction recipe:**
```bash
curl -A "Mozilla/5.0 ..." "https://www.abc.net.au/news/health/2026-06-24/ivf-australia-add-on-treatment/106818036" -o /tmp/abc.html
python3 -c "
import re
with open('/tmp/abc.html') as f: c = f.read()
c = re.sub(r'<style[^>]*>.*?</style>', ' ', c, flags=re.DOTALL)
c = re.sub(r'<script[^>]*>.*?</script>', ' ', c, flags=re.DOTALL)
m = re.search(r'<article[^>]*>(.*?)</article>', c, re.DOTALL)
body = m.group(1) if m else c
paras = re.findall(r'<p[^>]*>(.*?)</p>', body, re.DOTALL)
for p in paras:
    text = re.sub(r'<[^>]+>', ' ', p).strip()
    text = re.sub(r'\s+', ' ', text)
    if len(text) > 80:
        print(text)
"
```

**Decision rule:** when Bing News returns an `abc.net.au/news/health/...` URL for a Lancet/NEJM/JAMA/Cochrane meta-analysis or systematic review that the canonical journal page blocks from the cron sandbox, ABC News is the working fallback. The article is generic-public-broadcast journalism (not peer-reviewed), but it carries the named-author quotes, the headline numbers, the editorial framing, and the second-paper reference that the article body needs. ABC News works for health, science, and world-news sections. The URL pattern is `abc.net.au/news/{section}/YYYY-MM-DD/{slug}/{numeric-id}`.

**Tier position in the source ladder:** ABC News sits alongside The Star (Malaysia, 06-26) and The Straits Times (06-22) as a 4th-7th tier source for stories where the canonical Western outlet is blocked. The difference: ABC News is a public broadcaster (government-funded, ad-light, strong science desk) which gives it more depth on Cochrane / Lancet / NEJM meta-analyses than commercial Western outlets. Use ABC News as the first try when the meta-analysis is from Australia/New Zealand researchers or Australian clinical practice (Lensen is at University of Melbourne); use The Star for *China Daily* syndication; use Straits Times for institutional China-coverage.

---

## Two-meta-analysis contrast as a Template B framing device (NEW pattern — verified 2026-07-02)

**Context:** Template B (Traditional Therapy Modernization) usually has one meta-analysis or one journal paper as the hook, with Chinese practice as the implementation. A stronger version of Template B uses **two papers that reach opposite conclusions in the same week** as the framing device, then explains why both can be true.

The 2026-07-02 article on acupuncture for IVF used this framing. The two papers were:
- **The Lancet Obstetrics, Gynaecology & Women's Health** meta-review (Lensen et al., University of Melbourne, 24 June 2026, DOI 10.1016/s3050-5038(26)00054-3): 85 trials, 10 add-ons, acupuncture named as one of 7 add-ons with no evidence of benefit for the general IVF population
- **Frontiers in Endocrinology** meta-analysis (Guo et al., Longhua Hospital Shanghai University of TCM + Peking University Third Hospital, 29 May 2026, DOI 10.3389/fendo.2026.1845255): 22 RCTs, 2,299 women with PCOS undergoing IVF/ICSI, acupuncture associated with +13% clinical pregnancy rate (p<0.00001), +15% live birth rate (p<0.00001), 633 IU reduction in gonadotropin dose

**Verified 8-section article structure (used on the 2026-07-02 article, 4,881 words, 75/100):**
1. **Lead** — name both papers, both journals, both lead authors, both dates, both sample sizes (2-3 sentences, includes dateline like "MELBOURNE / SHANGHAI")
2. **Explain why the contradiction is not a contradiction** — different population scope (all-comers vs PCOS subgroup), different inclusion criteria, different subgroup granularity, methodological difference between pooled-all and stratified
3. **What the Lancet meta-analysis found** — full unpacking: 10 add-ons reviewed, 7 with no evidence, the named-author quotes, the practical reading for an Australian/American patient
4. **What the Shanghai meta-analysis found** — the 22 RCTs / 2,299 women details, the +13% / +15% / -633 IU numbers, the named acupoints used in the pooled trials, the protocol interaction signals (manual 25% vs electroacupuncture 10%, antagonist 21% vs agonist 11%)
5. **Why the two papers do not contradict each other** — the methodology section that bridges the two findings (homogeneous subgroup vs heterogeneous all-comers, Chinese trials dominated, etc.)
6. **What acupuncture for IVF looks like at a Chinese hospital** — session count (3-4), timing (around trigger, retrieval, transfer, luteal phase), named acupoints (SP6, CV4, CV6, EX-CA1, ST36, LR3, PC6), credential of the practitioner (5-year bachelor + 1-3 years gynecology specialty)
7. **Cost comparison** — Chinese hospital international patient service US$40-$80/session (total US$160-$320 for 4 sessions) vs Australian A$1,000-A$3,000 vs US$1,500-$4,000
8. **How an international patient can access the Chinese protocol** — remote consultation pathway, fresh-cycle-in-China vs home-clinic-stimulation + China-transfer option, what to ask before booking
9. **What the next 12-18 months are likely to bring** — planned Chinese multicenter RCT, Cochrane update, Hainan Lecheng integrated TCM-IVF possibility

**Why the contrast framing works:**
- (a) It gives the reader two reference points to anchor on rather than one
- (b) It lets the article address the Western skepticism (Lancet) without dismissing it, which is the journalistic move that makes the China-practice case land with skeptical readers
- (c) It makes the Chinese practice section read as the resolution to a real clinical question rather than as promotional TCM content
- (d) It naturally splits into two "what each paper found" sections that are easy to write and easy to read

**When to use this framing:** when Bing News surfaces a Cochrane / Lancet / NEJM / JAMA meta-analysis that names a TCM modality (acupuncture, herbal medicine, moxibustion, cupping, tuina, qigong, baduanjin, tai chi) as having "no evidence" or "inconclusive evidence" AND a same-window Chinese-led journal meta-analysis shows positive results in a specific subgroup. Look for:
- Cochrane review update naming a TCM modality
- Lancet, NEJM, or JAMA meta-analysis on a TCM topic with negative/null result
- A Chinese-led journal (Frontiers in Endocrinology, Frontiers in Medicine, Journal of Integrative Medicine, Chinese Journal of Integrative Medicine, etc.) publishing a meta-analysis on the same modality with positive subgroup result
- Both papers published within 30-60 days of each other

**Expected future pairings (candidates for the same Template B contrast framing):**
- Cochrane + Chinese meta on Baduanjin for COPD / pulmonary rehab
- Cochrane + Chinese meta on moxibustion for breech presentation
- Cochrane + Chinese meta on acupuncture for chemotherapy-induced nausea
- Cochrane + Chinese meta on tai chi for fall prevention in elderly
- Cochrane + Chinese meta on Chinese herbal medicine for atopic dermatitis
- Cochrane + Chinese meta on cupping for chronic neck pain

---

## Remote `origin/master` advance is now standard, not edge case (verified 2026-06-21 first occurrence, 2026-07-02 second occurrence)

**Context:** the cron push pattern `git push origin master` can fail with `! [rejected] (fetch first)` because the SEO/UX/marketing team on the chinahospitalsguide project pushes commits between cron runs.

**Two documented occurrences:**
- **2026-06-21** (first occurrence, recovery run picking up 06-20 partial state): 3-commit advance (MEMORY.md, AGENTS.md/git-push-helper.ps1, SEO batch optimization of 23 page meta tags)
- **2026-07-02** (clean fresh research → shipped, no recovery state): 9-commit advance (217-page GA4 event tracking deployment, 4 SEO-optimized pages, 49 TCM-section injections, 2 site-config commits, plus the 07-01 CUHK article from the prior cron)

**Working recovery recipe (verified both times):**
```bash
# Step 1: detect the rejection
git push origin master  # returns: "! [rejected] master -> master (fetch first)"

# Step 2: fetch the new remote commits
git fetch origin master

# Step 3: inspect the new commits — check whether they touch sitemap.xml or news/index.html
git log --oneline HEAD..origin/master
git log --stat HEAD..origin/master -- sitemap.xml  # if non-empty, expect rebase conflict

# Step 4: rebase (clean rebase when remote commits don't touch cron files)
git pull --rebase origin master

# Step 5: push (now fast-forward)
git push origin master
```

**Total cost: 3 extra tool calls** (1 fetch + 1 log + 1 rebase + 1 push = 4 actually, but the `log` can be combined with the `fetch` inspection).

**Budget the rebase as standard practice:** any cron run that pushes commits to `master` should expect 2-3 extra tool calls in the push step on any given day, not treat it as a recovery. The detection signal is the failed push itself.

**Conflict-detection rule:** before the rebase, run `git log --stat HEAD..origin/master -- sitemap.xml news/index.html news/`. If non-empty output, the SEO batch touched the cron files and the clean rebase will produce a conflict. In that case:
1. `git checkout -- sitemap.xml` — discard the cron run's sitemap edit, accept origin's version (SEO commits are authoritative for static pages)
2. `git pull --ff-only origin master` — fast-forward to origin HEAD
3. Re-patch sitemap.xml — insert the new article entry as the FIRST news entry, using origin's priority value (priority 0.6 for `/news/*` URLs since 2026-06-27 SEO batch)
4. `git add news/YYYY-MM-DD.html sitemap.xml news/index.html && git commit -m "article: YYYY-MM-DD" && git push origin master`

**Why this wasn't a problem before 2026-06-21:** earlier cron runs either pushed on the same day as the commit (no gap for the remote to advance) or hit the cap mid-pipeline (no commit to push). The 06-21 → 06-22 day-gap was the first recovery where the remote had time to receive new commits from another source (a human operator doing project-meta work, or a parallel cron). Since then, the SEO/UX overhaul team has been pushing 3-9 commits per cron cycle (roughly every 1-2 days), making the remote-advance case a regular occurrence.

**Mitigation (optional):** add `git fetch origin master` to Step 0 pre-flight and `git log --oneline HEAD..origin/master` to detect this state early — if non-empty, the cron run knows to expect a rebase or a fast-forward before the push. The 07-02 cron run did not pre-fetch and discovered the conflict on the first push attempt, costing 2 extra tool calls (fetch + rebase + retry push = 3 calls); a pre-flight fetch would have detected it before the commit was made and saved the 2 calls.

---

## Summary of new patterns from the 2026-07-02 run

1. **ABC News as 7th-tier source** — works for Cochrane/Lancet/NEJM/JAMA meta-analyses where canonical journals are Cloudflare-blocked. Generic-public-broadcast journalism carries the named-author quotes, headline numbers, editorial framing, and second-paper references.
2. **Two-meta-analysis contrast as Template B framing device** — when Lancet/Cochrane says "no evidence" and a same-window Chinese meta says "positive in subgroup X," the article is the resolution of the apparent contradiction. 8-section structure verified at 4,881 words / 75/100.
3. **Remote-advance rebase is now standard cron workflow** — 2nd occurrence in 9 days. The SEO/UX team pushes 3-9 commits per cycle. Budget 3 extra tool calls for the rebase sequence; detect via failed `git push origin master`.

Reference for these patterns: `references/pending-2026-07-02-acupuncture-ivf-lancet-vs-longhua-shipped.md` (the full shipped-article notes from the 2026-07-02 cron run).