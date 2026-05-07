# China Hospitals Guide Deployment Workflow

> **Source**: `china-hospitals-guide-deploy` skill (absorbed into `seo-content-writer`)

## Repository
- **Website repo**: `chinahospitalsguide` (GitHub)
- **Backup repo**: `demi` (GitHub)

## Clone
```bash
cd /root/.hermes/workspace/
git clone git@github.com:qzw-alt/chinahospitalsguide.git
```

## Topic Discovery: Competitor Keyword Gap Analysis (Free Method)

When choosing **commercial long-tail blog topics**, use competitor reverse-engineering instead of guessing. No SEMrush/Ubersuggest login needed.

### Step 1: Get competitor sitemap
```bash
curl -s https://competitor.com/sitemap.xml | grep -oP 'https://[^<]+'
```

### Step 2: Browse competitor content pages
Navigate to competitor blog indexes (e.g. `/blog`, `/resources`) and capture article titles, topic categories, and reading times.

### Step 3: Compare against our sitemap
Extract our sitemap URLs via browser console on our sitemap.xml:
```javascript
Array.from(document.querySelectorAll('loc')).map(el => el.textContent)
```

### Step 4: Identify the gap — category absence + format pattern
Flag topic categories competitors have that we don't. Also note their **title format** — the winning pattern for medical tourism China content is:

```
[Procedure] in China: Cost, [Specialty] Hospitals & What Foreign Patients Need to Know (2026)
```
Components: **Cost number first** + **country-vs-US price comparison** + **top hospitals** + **foreign patients** + **year tag**

### Priority Topic Gaps (as of 2026-05-01)
From MyChinaMed.com live analysis:
- 👁️ LASIK / Eye Surgery ❌ **GAP** — highest priority
- ✨ Rhinoplasty / Cosmetic Surgery ❌ **GAP** — highest priority
- 🎗️ CAR-T Cell Therapy ❌ **GAP** — high value, harder
- 🦴 Spine Surgery ❌ **GAP** — we have orthopedics page but thin
- 🏥 Executive Health Checkup ❌ **GAP** — medium priority
- 🩺 Traditional Chinese Medicine abroad ❌ **GAP** — medium priority

Top 3 immediate candidates:
1. `LASIK surgery China cost` — low difficulty, commercial intent
2. `Rhinoplasty China guide` — low difficulty, commercial intent
3. `Knee replacement China cost` — low difficulty, commercial intent

### Priority Rule
**Commercial intent** keywords (people ready to book) > informational. **Cost-comparison** format has proven ranking power in this niche. **Long-tail** > short-tail (avoid competing with Wikipedia/clinical sites).

---

## Topic Selection for News vs Commercial Blog

- **News**: Daily医疗热点，蹭全球新闻流量，对比中国现状，引导服务（现有cron 07:00）
- **Commercial blog**: 竞品关键词差距分析筛出的长尾选题，成本对比格式，高商业意向（现有cron 09:00）

两者都要做，News引流量，Commercial Blog生成询盘。

---

## Deployment Process (must follow order)

### Critical: Dual-Repository Workspace Structure

The workspace at `/root/.hermes/workspace/` uses two separate Git repositories:

| Directory | Git remote | Purpose |
|-----------|-----------|---------|
| `website/` | `origin` → `chinahospitalsguide` | **DEPLOY** — GitHub Pages reads from this |
| workspace root `/` | `backup` → `demi` | **BACKUP** — full project archive |

**Golden rule**: Edit in the site directory, deploy from `website/` directory only.
**NEVER** push non-site files (memory/, skills/, etc.) to `chinahospitalsguide`. This broke GitHub Pages in March 2026.

### 1. Pull latest first (site may be updated via CMS/Netlify后台)
```bash
cd /root/.hermes/workspace/chinahospitalsguide
git fetch origin
# Check if main or master is newer — site deploys from main
git log --oneline origin/main -3
git log --oneline origin/master -3
# If origin/main is ahead, pull main: git pull origin main
# If origin/master is ahead, pull master: git pull origin master
```

### 2. Edit files
- News article: `news/YYYY-MM-DD-slug.html`
- Commercial blog: `blog/slug.html`
- Sitemap: `sitemap.xml`

### 3. Commit and push
```bash
git add .
git commit -m "description"
git push origin master
```

### 4. Verify
Wait ~5 minutes, check https://chinahospitalsguide.com/ for updates

### 5. Backup to demi repo
After successful deploy:
```bash
cd /root/.openclaw/workspace
git add <changed files>
git commit -m "Backup: description"
git push backup master
```
If remote has diverged since your last pull, use `--no-rebase` to preserve your local changes:
```bash
git pull --no-rebase backup master
git push backup master
```

### Git Conflict Resolution Pattern (Remote Diverged)

When `git push` fails with "remote contains work you do not have":

1. `git fetch origin` — fetch remote state
2. `git log --oneline origin/master -5` — check what's on remote
3. `git pull --no-rebase origin master` — merge remote INTO local (NOT rebase!)
4. If auto-merge conflict: use `--ours` to keep your new content
   ```bash
   git checkout --ours blog/dental-implants-china.html
   git add blog/dental-implants-china.html
   git commit
   ```
5. `git push origin master`

This pattern (merge not rebase, --ours for content) preserves new content while integrating remote changes. Used successfully May 7, 2026.

---

## News Writing Standard Process (6 steps)
1. Search 24-hour medical news hotspots (Yahoo/Bing — avoid Google/DuckDuckGo which block bots)
2. Evaluate hotspot value, choose most viral potential
3. Write article in news format (includes NewsArticle Schema)
4. **De-AI processing (mandatory)** — score must be >60 before publishing
5. Update `news/index.html`
6. Update `sitemap.xml`

## Commercial Blog Writing Process (6 steps)
1. Run competitor keyword gap analysis (see Topic Discovery above)
2. multi-search → research: cost data, hospital names, US comparison prices
3. Write article using winning format: `[Procedure] China Cost + Hospital Guide`
4. **De-AI processing (mandatory)** — score must be >60 before publishing
5. Add to `blog/` directory
6. Update `sitemap.xml` and `blog/index.html` if it exists

---

## Known Site Issues (2026-05-01)
- `/treatments/` returns 404 — needs redirect or reconstruction
- Privacy/Terms pages have placeholder content
- Course: 11 lessons planned, only chapter 1 live

---

## Backup Process
```bash
cd /root/.Hermes/workspace/
git clone git@github.com:qzw-alt/demi.git
# Backup all site files to demi
```
