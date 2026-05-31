# Site Configurations for Programmatic SEO

## Setup Prerequisites

**Both sites require GitHub write access.** Before cloning or pushing, verify credentials exist:

```bash
# Check for GitHub token
cat ~/.git-credentials | grep github_pat || grep "GITHUB_TOKEN" ~/.hermes/.env | grep -v "^#"
```
If no token found → ask user before attempting any git push operations.

When cloning inside a cron job, always embed the token in the remote URL:
```bash
TOKEN=$(grep "GITHUB_TOKEN" ~/.hermes/.env | cut -d= -f2 | tr -d '"' | tr -d ' ')
git remote set-url origin "https://${TOKEN}@github.com/owner/repo.git"
```
Otherwise the clone/push will silently fail at push time even if clone succeeds.

## oriental-destiny.com (Feng Shui / BaZi / Destiny)

- **Repo**: https://github.com/qzw-alt/oriental-destiny
- **Branch**: `main` (NOT master!)
- **Deploy**: GitHub Pages from `main` branch
- **Article dir**: root directory (not a subdirectory)
- **Article naming**: `fate-YYYY-MM-DD.html`
- **Sitemap**: `sitemap.xml` in root (add entry after publish)
- **No news/index.html** (articles go straight to root, sitemap handles discovery)
- **Topic research**: Use `memories/layer3/research/article_topics.md` + `terminology_mapping.md`
- **Theme**: Feng shui, BaZi, I Ching, Chinese zodiac, Five Elements, Daoist treasures
- **Language**: English output (native English rendering per terminology_mapping.md)
- **Write style**: Use native English feng shui terms — see `terminology_mapping.md` Section 7 spelling rules
  - "Qi" not "Chi" (Qi is dominant)
  - "Feng shui" not "wind water" (never translated)
  - "Taoist" not "Daoist" (Western standard)
  - "I Ching" not "Yijing" (popular usage)
  - "Bagua" not "Pa Kua"
  - Lowercase in running text, capital in titles

## chinahospitalsguide.com (Chinese Medical Tourism)

- **Repo**: https://github.com/qzw-alt/chinahospitalsguide
- **Branch**: `master` (note: master, NOT main!)
- **Deploy**: GitHub Pages from `master` branch
- **Article dir**: `news/` subdirectory
- **Article naming**: `YYYY-MM-DD.html` inside news/
- **Sitemap**: `sitemap.xml` in root + `news/index.html` link list (update BOTH)
- **Topic research**: Use `content-research-writer-cn` skill for 热点
- **Theme**: Chinese hospitals, medical tourism, health travel

## Common Requirements

Both sites require:
- 去AI化 (humanizer) score >60 before publish — if score ≤60, do NOT publish
- Internal links to other site pages where relevant
- Schema.org Article structured data
- Canonical URL in `<head>`
- After git push, wait 2-3 minutes then verify at the target URL