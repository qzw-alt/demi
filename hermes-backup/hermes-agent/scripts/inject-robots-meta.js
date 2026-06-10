// Inject robots meta tag into pages that lack it
const fs = require('fs');
const path = require('path');

function processDir(dir) {
  const entries = fs.readdirSync(dir, { withFileTypes: true });
  for (const e of entries) {
    const full = path.join(dir, e.name);
    if (e.isDirectory()) {
      if (!e.name.startsWith('_') && !e.name.startsWith('.')) processDir(full);
    } else if (e.name.endsWith('.html')) {
      let html = fs.readFileSync(full, 'utf8');

      // Skip pages that already have robots meta
      if (/<meta\s+name=["']robots["']/i.test(html)) continue;

      // Skip 404 and redirect pages
      if (e.name === '404.html' || html.includes('http-equiv="refresh"')) continue;

      // Inject after charset or viewport meta
      const robotsMeta = '\n    <meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large">';
      if (html.includes('<meta charset="UTF-8">')) {
        html = html.replace('<meta charset="UTF-8">', '<meta charset="UTF-8">' + robotsMeta);
      } else if (html.includes('<meta charset="utf-8">')) {
        html = html.replace('<meta charset="utf-8">', '<meta charset="utf-8">' + robotsMeta);
      } else if (html.includes('<meta name="viewport"')) {
        html = html.replace(/<meta name="viewport"[^>]*>/, '$&' + robotsMeta);
      } else if (html.includes('<head>')) {
        html = html.replace('<head>', '<head>' + robotsMeta);
      }

      fs.writeFileSync(full, html);
    }
  }
}

processDir('_site');
console.log('Robots meta injection done.');
