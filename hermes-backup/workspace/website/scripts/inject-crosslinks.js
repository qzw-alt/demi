// Inject cross-content links between blog articles, treatments, news, and stories
// Run during build (on _site/) or dev (on source directories)
const fs = require('fs');
const path = require('path');

// ── Link mappings ──

// Blog articles → relevant treatment pages
const blogToTreatments = {
  'best-cancer-hospitals-china-2026.html': ['cancer.html'],
  'cancer-treatment-china-2026.html': ['cancer.html'],
  'cancer-treatment-cost-china.html': ['cancer.html'],
  'car-t-therapy-china-2026.html': ['cancer.html'],
  'car-t-therapy-hospitals-china-2026.html': ['cancer.html'],
  'proton-therapy-china-2026.html': ['cancer.html'],
  'bone-marrow-transplant-china.html': ['cancer.html'],
  'thyroid-cancer-treatment-china-2026.html': ['cancer.html'],
  'heart-surgery-cost-china.html': ['cardiac.html'],
  'best-cardiac-surgery-hospitals-china-2026.html': ['cardiac.html'],
  'cardiac-bypass-surgery-china-2026.html': ['cardiac.html'],
  'china-orthopedic-hospital-rankings-2026.html': ['orthopedics.html'],
  'fuzhou-orthopedic-hospital-rankings-2026.html': ['orthopedics.html'],
  'knee-replacement-cost-china.html': ['orthopedics.html'],
  'knee-replacement-surgery-china-2026.html': ['orthopedics.html'],
  'hip-replacement-cost-china.html': ['orthopedics.html'],
  'spine-surgery-cost-china.html': ['orthopedics.html'],
  'orthopedic-surgery-china-2026.html': ['orthopedics.html'],
  'rotator-cuff-surgery-china-2026.html': ['orthopedics.html'],
  'ivf-cost-china-2026.html': ['ivf.html'],
  'ivf-fertility-treatment-china-2026.html': ['ivf.html'],
  'ivf-fertility-treatment-china.html': ['ivf.html'],
  'ivf-china-2026-complete-guide.html': ['ivf.html'],
  'stem-cell-therapy-china-2026.html': ['stem-cell.html'],
  'stem-cell-therapy-china-cost-2026.html': ['stem-cell.html'],
};

// Treatment pages → relevant blog articles
const treatmentToBlogs = {
  'cancer.html': ['best-cancer-hospitals-china-2026.html', 'cancer-treatment-cost-china.html', 'car-t-therapy-china-2026.html', 'proton-therapy-china-2026.html'],
  'cardiac.html': ['heart-surgery-cost-china.html', 'best-cardiac-surgery-hospitals-china-2026.html', 'cardiac-bypass-surgery-china-2026.html'],
  'orthopedics.html': ['china-orthopedic-hospital-rankings-2026.html', 'knee-replacement-cost-china.html', 'hip-replacement-cost-china.html', 'spine-surgery-cost-china.html'],
  'ivf.html': ['ivf-cost-china-2026.html', 'ivf-fertility-treatment-china-2026.html'],
  'stem-cell.html': ['stem-cell-therapy-china-2026.html', 'stem-cell-therapy-china-cost-2026.html'],
};

// Friendly names for treatment pages
const treatmentNames = {
  'cancer.html': 'Cancer Treatment in China',
  'cardiac.html': 'Heart Surgery in China',
  'orthopedics.html': 'Orthopedic Surgery in China',
  'ivf.html': 'IVF & Fertility in China',
  'stem-cell.html': 'Stem Cell Therapy in China',
};

// Friendly names for blog articles (extracted from <title>)
function getBlogTitle(filePath) {
  try {
    const html = fs.readFileSync(filePath, 'utf8');
    const match = html.match(/<title>([^<]+)<\/title>/);
    return match ? match[1].replace(/\s*\|\s*China Hospitals Guide\s*$/i, '').trim() : path.basename(filePath, '.html');
  } catch {
    return path.basename(filePath, '.html').replace(/-/g, ' ');
  }
}

// ── Injection functions ──

function makeTreatmentLinkHTML(treatmentFile, prefix) {
  const name = treatmentNames[treatmentFile] || treatmentFile;
  const href = `/treatments/${treatmentFile}`;
  return `\n<li><a href="${href}">${prefix} ${name}</a> — save 70-85% at JCI-accredited hospitals</li>`;
}

function makeBlogLinkHTML(blogFile, blogDir) {
  const blogPath = path.join(blogDir, blogFile);
  const title = getBlogTitle(blogPath);
  const href = `/blog/${blogFile}`;
  return `\n<li><a href="${href}">${title}</a></li>`;
}

// Inject treatment links into a blog HTML file
function injectBlogLinks(filePath, treatmentFiles) {
  let html = fs.readFileSync(filePath, 'utf8');
  if (html.includes('rel-treatment-link')) return false; // Already injected

  const linksHTML = treatmentFiles.map(t => makeTreatmentLinkHTML(t, '🎯')).join('');

  // Find the "Related Articles" section and inject before it closes
  const relatedPatterns = [
    /(<h[23][^>]*>📚 Related Articles<\/h[23]>\s*<ul[^>]*>)/,
    /(<h[23][^>]*>Related Articles<\/h[23]>\s*<ul[^>]*>)/,
    /(<div[^>]*class="[^"]*related[^"]*"[^>]*>\s*<ul[^>]*>)/,
  ];

  for (const pattern of relatedPatterns) {
    if (pattern.test(html)) {
      html = html.replace(pattern, (match) => match + linksHTML);
      fs.writeFileSync(filePath, html);
      return true;
    }
  }

  // Fallback: inject before </article> or </main> or last </section>
  if (html.includes('</article>')) {
    const block = `\n<section class="related-treatments" rel-treatment-link style="max-width:900px;margin:40px auto;padding:20px 30px;background:#f0f7ff;border-radius:12px;border-left:4px solid #1e3c72;"><h3 style="color:#1e3c72;">🎯 Related Treatment Pages</h3><ul style="list-style:none;padding:0;margin:10px 0 0;">${linksHTML}</ul></section>\n</article>`;
    html = html.replace('</article>', block);
    fs.writeFileSync(filePath, html);
    return true;
  }
  return false;
}

// Inject blog links into a treatment HTML file
function injectTreatmentLinks(filePath, blogFiles, blogDir) {
  let html = fs.readFileSync(filePath, 'utf8');
  if (html.includes('rel-treatment-blog-link')) return false;

  const linksHTML = blogFiles.map(b => makeBlogLinkHTML(b, blogDir)).join('');

  // Find footer or end-of-content area
  const block = `\n<section class="related-blog-articles" rel-treatment-blog-link style="max-width:1180px;margin:0 auto 40px;padding:20px 30px;background:#f0f7ff;border-radius:12px;border-left:4px solid #2a5298;"><h3 style="color:#1e3c72;">📚 Related Guides & Cost Comparisons</h3><ul style="list-style:none;padding:0;margin:10px 0 0;display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:8px;">${linksHTML}</ul></section>`;

  // Insert before <footer> or before </body>
  if (html.includes('<footer')) {
    html = html.replace('<footer', block + '\n<footer');
  } else if (html.includes('</body>')) {
    html = html.replace('</body>', block + '\n</body>');
  } else {
    return false;
  }
  fs.writeFileSync(filePath, html);
  return true;
}

// ── Process ──

function processDir(dir, baseDir) {
  if (!baseDir) baseDir = dir;
  const entries = fs.readdirSync(dir, { withFileTypes: true });
  for (const e of entries) {
    const full = path.join(dir, e.name);
    if (e.isDirectory()) {
      if (!e.name.startsWith('_') && !e.name.startsWith('.')) processDir(full, baseDir);
    } else if (e.name.endsWith('.html')) {
      const relPath = path.relative(baseDir, full).replace(/\\/g, '/');

      // Check if blog article
      if (relPath.startsWith('blog/') && e.name !== 'index.html') {
        const blogFile = path.basename(relPath);
        const treatments = blogToTreatments[blogFile];
        if (treatments && treatments.length > 0) {
          const result = injectBlogLinks(full, treatments);
          if (result) console.log(`Crosslinks: ${relPath} → treatments`);
        }
      }

      // Check if treatment page
      if (relPath.startsWith('treatments/') && e.name !== 'index.html') {
        const treatmentFile = e.name;
        const blogs = treatmentToBlogs[treatmentFile];
        if (blogs && blogs.length > 0) {
          const blogDir = path.join(baseDir, 'blog');
          const result = injectTreatmentLinks(full, blogs, blogDir);
          if (result) console.log(`Crosslinks: ${relPath} → blog`);
        }
      }
    }
  }
}

// ── Entry point ──

let targetDir;
if (fs.existsSync('_site')) {
  targetDir = '_site';
  console.log('Processing _site/ (build mode)');
} else {
  targetDir = path.join(__dirname, '..');
  console.log('Processing source directory (dev mode)');
}

processDir(targetDir);
console.log('Cross-link injection done.');
