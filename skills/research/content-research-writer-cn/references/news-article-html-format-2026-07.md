# News article HTML format on chinahospitalsguide.com (verified 2026-07-23)

**Status as of 2026-07-23:** news/ articles are full HTML files, NOT Jekyll/Markdown frontmatter.

The cron prompt's 2026-07-10 patch 4 mentions a possible future switch to `.md` + frontmatter under `_layouts/blog-post.njk` for news/ articles, but that switch has not actually happened. Do not assume a Jekyll/Markdown structure for new news/ articles — the current convention is full HTML files.

## The trap

When writing a fresh news/ article from scratch, the natural starting point is Jekyll-style YAML frontmatter at the top of an HTML file. This produces an HTML file that looks correct in code review but renders wrong:

- (a) The YAML frontmatter leaks into the visible page body as text
- (b) Missing JSON-LD Article/FAQPage schema costs rich-result eligibility
- (c) Missing `<meta property="article:published_time">` and canonical URL loses SEO signals
- (d) Missing inline stylesheet makes the article look unstyled on the site

## Working pattern

1. **BEFORE writing a new article**, read the most recent published article: `head -50 news/YYYY-MM-DD-<prev-slug>.html` to confirm the full HTML pattern
2. **Use that file as the structural template** — copy its `<!DOCTYPE html>` through `<head>` through `<body>` opening tags, fill in your content, save as the new file
3. **Verification:** after write_file, `head -20 news/YYYY-MM-DD-*.html` should show `<!DOCTYPE html>` and `<html lang="en">` on lines 1-2, NOT `---` frontmatter delimiters

## Canonical HTML structure (verified 2026-07-23)

Reference article: `news/2026-07-22-yili-tongrentang-tcm-elderly-nutrition-china-2026.html`

```
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>...</title>
<meta name="description" content="...">
<meta name="keywords" content="...">
<meta name="robots" content="index, follow">
<link rel="canonical" href="https://chinahospitalsguide.com/news/YYYY-MM-DD-...html">
<meta property="og:type" content="article">
<meta property="og:url" content="...">
<meta property="og:title" content="...">
<meta property="og:description" content="...">
<meta property="og:image" content="https://chinahospitalsguide.com/images/china-hospital.jpg">
<meta property="article:published_time" content="YYYY-MM-DD">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="...">
<meta name="twitter:description" content="...">
<script type="application/ld+json">
[
  {
    "@context": "https://schema.org",
    "@type": "Article",
    "headline": "...",
    "description": "...",
    "image": "...",
    "author": {"@type": "Organization", "name": "China Hospitals Guide"},
    "publisher": {"@type": "Organization", "name": "China Hospitals Guide", "logo": {"@type": "ImageObject", "url": "https://chinahospitalsguide.com/logo.webp"}},
    "datePublished": "YYYY-MM-DD",
    "dateModified": "YYYY-MM-DD",
    "mainEntityOfPage": {"@type": "WebPage", "@id": "..."}
  },
  {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": [
      {"@type": "Question", "name": "...", "acceptedAnswer": {"@type": "Answer", "text": "..."}},
      ...3-5 Q&As
    ]
  }
]
</script>
<link rel="stylesheet" href="/styles.css">
<style>
.article-body { ... }
... (inline styles)
</style>
</head>
<body>
<main class="article-body">
<h1>...</h1>
... body content with H2/H3/p/ul/li/pullquote/div data-box etc.
</main>
</body>
</html>
```

## Required elements checklist

- `<!DOCTYPE html>` on line 1
- `<html lang="en">` on line 2
- Canonical URL in `<link rel="canonical">`
- `og:type=article`, `og:url`, `og:title`, `og:description`, `og:image`
- `article:published_time` meta tag with YYYY-MM-DD
- Twitter card meta tags
- JSON-LD wrapped in `[...]` array (NOT separate `<script>` tags)
- JSON-LD Article + FAQPage blocks both required
- `<main class="article-body">` body wrapper
- `<img src="../images/china-hospital.jpg" alt="...">` for news/index.html cards

## Common failures to avoid

- **DO NOT** use YAML frontmatter (`---` delimiter + key/value pairs at top of file)
- **DO NOT** put JSON-LD blocks in two separate `<script>` tags — they MUST be in a single array
- **DO NOT** omit the FAQPage block — it's part of the site's standard rich-result pattern
- **DO NOT** use `@@type` (double @) — typo trap; should be `@type`
- **DO NOT** omit `<meta property="article:published_time">` — date verification breaks
- **DO NOT** skip the `image:` field in JSON-LD Article — Google's article rich-result requires it