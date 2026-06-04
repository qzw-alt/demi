const fs = require('fs');
const path = require('path');

// Build set of available WebP files
function findWebpFiles(dir) {
  const webp = new Set();
  function walk(d) {
    if (!fs.existsSync(d)) return;
    const entries = fs.readdirSync(d, { withFileTypes: true });
    for (const e of entries) {
      const full = path.join(d, e.name);
      if (e.isDirectory()) { walk(full); }
      else if (e.name.endsWith('.webp')) {
        webp.add(path.relative(dir, full).replace(/\\/g, '/'));
      }
    }
  }
  walk(dir);
  return webp;
}

const webpFiles = findWebpFiles('_site/images');
console.log(`Found ${webpFiles.size} WebP images`);

// Process HTML files
function processDir(dir) {
  const entries = fs.readdirSync(dir, { withFileTypes: true });
  for (const e of entries) {
    const full = path.join(dir, e.name);
    if (e.isDirectory()) {
      if (!e.name.startsWith('_') && !e.name.startsWith('.')) processDir(full);
    } else if (e.name.endsWith('.html')) {
      let html = fs.readFileSync(full, 'utf8');
      let changed = false;

      // Replace img src from jpg/png to webp when webp exists
      html = html.replace(/<img\s+[^>]*src="([^"]+\.)(jpe?g|png)"/gi, (match, prefix, ext) => {
        const fullSrc = prefix + ext;
        const webpSrc = prefix + 'webp';
        const relPath = fullSrc.replace(/^\/?(images\/)/, '');
        if (webpFiles.has(relPath) || webpFiles.has(fullSrc.replace(/^\//, ''))) {
          changed = true;
          return match.replace(fullSrc, webpSrc);
        }
        return match;
      });

      // Also handle srcset if present
      html = html.replace(/srcset="([^"]+\.)(jpe?g|png)"/gi, (match, prefix, ext) => {
        const fullSrc = prefix + ext;
        const webpSrc = prefix + 'webp';
        const relPath = fullSrc.replace(/^\/?(images\/)/, '');
        if (webpFiles.has(relPath) || webpFiles.has(fullSrc.replace(/^\//, ''))) {
          changed = true;
          return match.replace(fullSrc, webpSrc);
        }
        return match;
      });

      if (changed) {
        fs.writeFileSync(full, html);
        console.log('Fixed WebP:', path.relative('_site', full));
      }
    }
  }
}

processDir('_site');
console.log('WebP fix done.');
