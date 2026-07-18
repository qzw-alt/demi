# Eleventy Markdown publishing validation — chinahospitalsguide

Verified 2026-07-18 after the site's 2026-07-10 migration to Markdown + Nunjucks.

## Explicit permalink is required for filename-style URLs

When the intended public URL ends in `.html`, include all three fields:

```yaml
permalink: "/blog/YYYY-MM-DD-slug.html"
canonical: "https://chinahospitalsguide.com/blog/YYYY-MM-DD-slug.html"
ogType: "article"
```

Without `permalink`, Eleventy emits `/blog/YYYY-MM-DD-slug/index.html`. A canonical ending in `.html` then points to an artifact the build did not produce.

Set `ogType: "article"` because `_includes/head.njk` defaults Open Graph type to `website` even when Article JSON-LD is present.

## Validate the built artifact

```bash
npx eleventy
test -f _site/blog/YYYY-MM-DD-slug.html
grep -q '<meta property="og:type" content="article">' _site/blog/YYYY-MM-DD-slug.html
```

Also inspect the rendered JSON-LD to confirm that Article and FAQPage are inside one JSON array.

## Clean-worktree validation when unrelated drafts break the build

An unrelated untracked Markdown draft can be discovered by Eleventy and fail YAML parsing. Do not modify, delete, or commit someone else's draft merely to make the content build pass.

Instead:

1. Commit and push the intended article first, per the cap-safe workflow.
2. Create a clean detached git worktree at the committed HEAD.
3. Run Eleventy with the clean worktree as the current directory.
4. Inspect that worktree's `_site/` output.

This validates the exact committed source CI will deploy while isolating the test from unrelated local files.

## Canonical live verification only

Do not append an arbitrary `?rev=<sha>` query string to a GitHub Pages article URL. In the verified case, the canonical `.html` page returned HTTP 200 while the query-string variant reached the site's custom 404 route.

Verify the canonical URL exactly. To distinguish stale CDN content from deployment failure:

1. Confirm the source exists on origin.
2. Fetch the canonical live URL.
3. Check the live `<title>` or another unique article marker.
4. Retry after the normal Pages propagation delay if the old version is still served.
