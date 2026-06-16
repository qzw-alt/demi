// Paginate blog index: split 79 articles across pages of 30
// Runs on _site/ after Eleventy build, or on source in dev mode
const fs = require('fs');
const path = require('path');

const ARTICLES_PER_PAGE = 30;
const BASE = 'https://chinahospitalsguide.com';

function paginateBlog(dir) {
  const blogDir = path.join(dir, 'blog');
  const indexPath = path.join(blogDir, 'index.html');
  if (!fs.existsSync(indexPath)) return;

  let html = fs.readFileSync(indexPath, 'utf8');

  // Extract all blog-card blocks
  const cards = [];
  const cardRegex = /<div class="blog-card">[\s\S]*?<\/div>\s*<\/div>/g;
  let match;
  while ((match = cardRegex.exec(html)) !== null) {
    cards.push(match[0]);
  }

  const totalCards = cards.length;
  if (totalCards === 0) {
    console.log('Paginate: No blog cards found, skipping.');
    return;
  }

  const totalPages = Math.ceil(totalCards / ARTICLES_PER_PAGE);
  if (totalPages <= 1) {
    console.log(`Paginate: Only ${totalCards} articles, no pagination needed.`);
    return;
  }

  console.log(`Paginate: ${totalCards} articles → ${totalPages} pages (${ARTICLES_PER_PAGE}/page)`);

  // Extract page boilerplate: everything before blog-grid and after blog-grid
  const gridStart = html.indexOf('<div class="blog-grid">');
  const gridEnd = html.lastIndexOf('</div>', html.indexOf('<a href="/" class="back-link">'));

  const beforeGrid = html.substring(0, gridStart);
  const afterGrid = html.substring(gridEnd + '</div>'.length);

  // Helper: generate pagination nav HTML
  function paginationNav(page) {
    let nav = '<nav class="blog-pagination" style="display:flex;justify-content:center;align-items:center;gap:12px;margin:40px 0;flex-wrap:wrap;" aria-label="Blog pagination">';
    if (page > 1) {
      const prevUrl = page === 2 ? '/blog/' : `/blog/${page - 1}/`;
      nav += `<a href="${prevUrl}" style="padding:10px 20px;background:#1e3c72;color:white;border-radius:25px;text-decoration:none;font-weight:500;">← Previous</a>`;
    }
    for (let i = 1; i <= totalPages; i++) {
      const pageUrl = i === 1 ? '/blog/' : `/blog/${i}/`;
      if (i === page) {
        nav += `<span style="padding:10px 16px;background:#ff6b6b;color:white;border-radius:25px;font-weight:700;">${i}</span>`;
      } else {
        nav += `<a href="${pageUrl}" style="padding:10px 16px;background:#f0f0f0;color:#1e3c72;border-radius:25px;text-decoration:none;font-weight:500;">${i}</a>`;
      }
    }
    if (page < totalPages) {
      nav += `<a href="/blog/${page + 1}/" style="padding:10px 20px;background:#1e3c72;color:white;border-radius:25px;text-decoration:none;font-weight:500;">Next →</a>`;
    }
    nav += '</nav>';
    return nav;
  }

  // Helper: update filter button total count
  function updateFilterCount(html, count) {
    return html.replace(/All \(\d+\)/, `All (${count})`);
  }

  // Helper: update "Latest Articles" heading for paginated pages
  function getHeading(page) {
    if (page === 1) return 'Latest Articles';
    return `Latest Articles — Page ${page}`;
  }

  // Helper: add page-specific SEO tags to head
  function updateHeadMeta(html, page) {
    const pageUrl = page === 1 ? `${BASE}/blog/` : `${BASE}/blog/${page}/`;
    const canonicalTag = `\n    <link rel="canonical" href="${pageUrl}">`;
    const pageTitle = page === 1
      ? 'Medical Tourism China Blog - Guides, Costs & Patient Stories | China Hospitals Guide'
      : `Medical Tourism Blog — Page ${page} | China Hospitals Guide`;

    // Update title
    html = html.replace(/<title>[^<]*<\/title>/, `<title>${pageTitle}</title>`);

    // Update OG title
    html = html.replace(/<meta property="og:title" content="[^"]*">/, `<meta property="og:title" content="${pageTitle}">`);

    // Update OG URL
    html = html.replace(/<meta property="og:url" content="[^"]*">/, `<meta property="og:url" content="${pageUrl}">`);

    // Update canonical
    if (html.includes('rel="canonical"')) {
      html = html.replace(/<link rel="canonical" href="[^"]*">/, `<link rel="canonical" href="${pageUrl}">`);
    } else {
      html = html.replace('</head>', canonicalTag + '\n</head>');
    }

    // Add prev/next link tags for SEO
    let seoLinks = '';
    if (page > 1) {
      const prevUrl = page === 2 ? `${BASE}/blog/` : `${BASE}/blog/${page - 1}/`;
      seoLinks += `\n    <link rel="prev" href="${prevUrl}">`;
    }
    if (page < totalPages) {
      seoLinks += `\n    <link rel="next" href="${BASE}/blog/${page + 1}/">`;
    }
    if (page > 1) {
      seoLinks += `\n    <meta name="robots" content="noindex,follow">`;
    }
    html = html.replace('</head>', seoLinks + '\n</head>');

    return html;
  }

  // ── Generate pages ──

  for (let p = 1; p <= totalPages; p++) {
    const startIdx = (p - 1) * ARTICLES_PER_PAGE;
    const pageCards = cards.slice(startIdx, startIdx + ARTICLES_PER_PAGE);

    let pageHtml = beforeGrid + '<div class="blog-grid">\n';
    pageHtml += pageCards.join('\n');
    pageHtml += '\n</div>';
    pageHtml += paginationNav(p);
    pageHtml += afterGrid;

    // Update filter button total
    pageHtml = updateFilterCount(pageHtml, totalCards);

    // Update heading
    pageHtml = pageHtml.replace(
      /<h2 id="latest-articles"[^>]*>[^<]*<\/h2>/,
      `<h2 id="latest-articles" style="color: #1e3c72; margin-bottom: 30px; font-size: 2em;">${getHeading(p)}</h2>`
    );

    // Update SEO tags
    pageHtml = updateHeadMeta(pageHtml, p);

    if (p === 1) {
      // Overwrite blog/index.html as page 1
      fs.writeFileSync(indexPath, pageHtml);
      console.log(`Paginate: blog/index.html (page 1, ${pageCards.length} cards)`);
    } else {
      // Create blog/N/index.html for pages 2+
      const pageDir = path.join(blogDir, String(p));
      if (!fs.existsSync(pageDir)) fs.mkdirSync(pageDir, { recursive: true });
      fs.writeFileSync(path.join(pageDir, 'index.html'), pageHtml);
      console.log(`Paginate: blog/${p}/index.html (page ${p}, ${pageCards.length} cards)`);
    }
  }

  // Clean up stale page directories beyond new total
  const blogEntries = fs.readdirSync(blogDir, { withFileTypes: true });
  for (const entry of blogEntries) {
    if (entry.isDirectory() && /^\d+$/.test(entry.name)) {
      const pageNum = parseInt(entry.name, 10);
      if (pageNum > totalPages) {
        fs.rmSync(path.join(blogDir, entry.name), { recursive: true, force: true });
        console.log(`Paginate: Removed stale page dir blog/${entry.name}/`);
      }
    }
  }
}

// ── Entry point ──

let targetDir;
if (fs.existsSync('_site')) {
  targetDir = '_site';
  console.log('Paginate: Processing _site/ (build mode)');
} else {
  targetDir = path.join(__dirname, '..');
  console.log('Paginate: Processing source directory (dev mode)');
}

paginateBlog(targetDir);
console.log('Blog pagination done.');
