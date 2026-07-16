# Step 5 Site Divergence (verified 2026-07-16)

The Step 5 instruction in `SKILL.md` — "Add article entry to `sitemap.xml` AND `news/index.html` link list" — is **not universal**. It's chinahospitalsguide-specific.

## Per-site Step 5 surface

| Site | sitemap.xml | news/index.html | Detection |
|------|-------------|-----------------|-----------|
| chinahospitalsguide.com | YES (insert at top of `<urlset>`) | YES (insert article card at top of list) | `ls news/` returns ≥1 file |
| oriental-destiny.com | YES (insert at top of `<urlset>`) | **NO** (file does not exist) | `ls news/` returns empty |

## oriental-destiny.com verified state (2026-07-16)

- `ls news/` → empty directory (does not exist as a discoverable surface)
- `grep -l 'fate-2026-07-15' index.html` → 0 matches (no central article list in `index.html`)
- The only file referencing the prior fate-article URL is the prior fate-article itself, via cross-link `<a href="fate-2026-07-15.html">` in the footer

**Conclusion:** for oriental-destiny cron runs, sitemap.xml is the SOLE Step 5 surface. Future agents should NOT waste tool calls grepping for a non-existent article list.

## Detection command (run at Step 5 start)

```bash
ls news/ 2>/dev/null
```

- Non-empty = chinahospitalsguide → update sitemap.xml + news/index.html
- Empty / not found = oriental-destiny → update sitemap.xml only

## Why this matters

Future agents reading SKILL.md will hit Step 5 and try to find a `news/index.html` for oriental-destiny. They will run 2-3 grep calls (looking for `fate-2026-07-15` in `index.html`, `articles.html`, `blog.html`) before realizing the list does not exist. Each wasted call is one less call for the humanize loop, the git push, or the recovery sequence. With the 35-call cron budget, 2-3 wasted calls is meaningful.

## When to re-verify this assumption

The site could add an article list at any time (a future SEO batch, a manual operator edit). The detection command should be run at the START of every cron run on oriental-destiny, not assumed from prior runs. If `ls news/` ever returns non-empty on oriental-destiny, the Step 5 surface has expanded to match chinahospitalsguide's pattern.