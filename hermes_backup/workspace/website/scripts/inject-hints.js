const fs = require('fs');
const path = require('path');

const hints = `
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link rel="dns-prefetch" href="//www.googletagmanager.com">
    <link rel="dns-prefetch" href="//pagead2.googlesyndication.com">
    <link rel="preload" href="/styles.css" as="style">
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Playfair+Display:wght@600;700&display=swap">`;

function injectHints(dir) {
  const entries = fs.readdirSync(dir, { withFileTypes: true });
  for (const entry of entries) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      if (!entry.name.startsWith('_')) injectHints(full);
    } else if (entry.name.endsWith('.html')) {
      let html = fs.readFileSync(full, 'utf8');
      if (html.includes('fonts.googleapis.com')) continue; // already has font link
      html = html.replace('</title>', '</title>' + hints);
      fs.writeFileSync(full, html);
      console.log('Injected:', full);
    }
  }
}

// Preload hero image only on homepage
const indexPath = path.join('_site', 'index.html');
if (fs.existsSync(indexPath)) {
  let html = fs.readFileSync(indexPath, 'utf8');
  if (!html.includes('china-hospital.webp') && !html.includes('china-hospital.jpg')) {
    // Check which hero image is used
  }
  if (!html.includes('<link rel="preload" as="image"')) {
    // Add hero image preload for images referenced in hero CSS
    const heroPreload = '\n    <link rel="preload" as="image" href="/images/china-hospital.webp" fetchpriority="high">';
    html = html.replace('</title>', '</title>' + heroPreload);
    fs.writeFileSync(indexPath, html);
    console.log('Injected hero preload:', indexPath);
  }
}

injectHints('_site');
console.log('Done.');
