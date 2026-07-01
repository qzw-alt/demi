# Duplicate-content defense when generating pillar pages (2026-07-01)

A real incident where two agents (cron + same-session subagents) created overlapping `china-unique-medical-procedures*.html` master pillar pages — same topic, different slugs, both deployed. Both referenced as canonical in the sitemap.

## What went wrong

- Agent A (a cron run) created `blog/china-unique-medical-procedures-guide.html` (committed `24e927c`, ~3,300 words).
- Agent B (interactive session, subagent-delegated for pillar creation) created `blog/china-unique-medical-procedures.html` (committed `a5b7026`, ~5,200 words) plus 10 sub-pillar pages.
- Both made it to production via the standard push flow (SSL openssl, master branch).
- Google would see two URLs serving near-identical content — classic "duplicate content" penalty.

## Detection recipe (5 commands, ~3 minutes)

```bash
# Find every file mentioning the topic
grep -lE "china-unique-medical-procedures" /path/to/site --include="*.html" -r

# Inventory the candidates
ls -la /path/to/site/blog/china-unique*.html

# Check which is older (canonical)
cd /path/to/site
git log --oneline --all -- "blog/china-unique*"

# Find every other page that links to either slug
grep -rE "china-unique-medical-procedures" /path/to/site --include="*.html" -l

# Check sitemap
grep "china-unique-medical-procedures" /path/to/site/sitemap.xml
```

## Recovery (5 steps, ~5 minutes)

```bash
# Step 1: Verify no other code paths link to the duplicate
grep -rE "china-unique-medical-procedures\.html" /path/to/site --include="*.html" | grep -v "guide"

# Step 2: Delete the duplicate
rm /path/to/site/blog/china-unique-medical-procedures.html

# Step 3: Remove its entry from sitemap.xml (manual edit)

# Step 4: Add 301 in _redirects
echo "/blog/china-unique-medical-procedures.html /blog/china-unique-medical-procedures-guide.html 301" >> /path/to/site/_redirects

# Step 5: Commit + push + verify
cd /path/to/site
git add -A
git -c http.sslBackend=openssl commit -m "SEO: remove duplicate pillar page ([slug]) to avoid duplicate-content penalty

- Found in audit: [older-commit] had already created [canonical-slug] (with same topic)
- [newer-commit] created [duplicate-slug] (different slug, same topic)
- Action: kept [canonical-slug] (older commit, already linked from blog index)
- Deleted: [duplicate-slug]
- Added: 301 redirect → [canonical-slug]
- Verified: no other pages link to the deleted slug"
git -c http.sslBackend=openssl push
sleep 60 && curl --max-time 25 -s -o /dev/null -w "%{http_code}\n" "https://YOUR-SITE.com/blog/china-unique-medical-procedures-guide.html"
```

## Prevention — check BEFORE creating pillar/duplicate pages

```bash
# Slug collision check
grep -rE "TOPIC_KEYWORDS" /path/to/site --include="*.html" -l | grep -v "TARGET_FILE"

# Git history (last 7 days)
git log --since="7 days ago" --oneline | grep -i "topic-keyword"

# Sitemap check
grep "topic-keyword" /path/to/site/sitemap.xml
```

If any turn up a near-duplicate, **pause and resolve the conflict** BEFORE creating the new page.

## Audit command for the whole site (1-liner)

```bash
# Find every .html whose basename has a -guide variant that also exists
cd /path/to/site/blog
for f in *-guide.html; do
  bare="${f%-guide.html}.html"
  if [ -f "$bare" ]; then
    echo "DUPLICATE PAIR: $f <-> $bare"
  fi
done
```

A clean site prints zero lines.

## Why this matters

- Google "duplicate content" filter applies **across the same site** as well as across sites. Two URLs on the same domain competing for the same query dilute link equity and reduce both pages' rankings.
- The 301 redirect consolidates the link equity onto the canonical URL. Removing the sitemap entry tells Google to drop the duplicate from indexing.
- The audit command catches the pattern programmatically; should be run as part of any "post-deploy" check, especially after multi-agent content batches.

## Related

- Main skill: `web-development/medical-tourism-site-ops/SKILL.md` — see the "Duplicate-content defense" section in the body for the decision rule and policy.
- Template: `web-development/medical-tourism-site-ops/templates/hospital-ranking-feature-snippet.md` — for the kind of pillar content where this risk is highest.
