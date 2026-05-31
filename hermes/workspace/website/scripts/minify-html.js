// Post-build HTML minification
const fs = require('fs');
const path = require('path');
const { minify } = require('html-minifier');

const options = {
  collapseWhitespace: true,
  removeComments: true,
  removeRedundantAttributes: true,
  removeEmptyAttributes: true,
  minifyCSS: true,
  minifyJS: true,
  processConditionalComments: true,
};

function processDir(dir) {
  const entries = fs.readdirSync(dir, { withFileTypes: true });
  let errors = 0;
  let minified = 0;
  for (const e of entries) {
    const full = path.join(dir, e.name);
    if (e.isDirectory()) {
      if (!e.name.startsWith('_') && !e.name.startsWith('.')) processDir(full);
    } else if (e.name.endsWith('.html')) {
      const original = fs.readFileSync(full, 'utf8');
      try {
        const result = minify(original, options);
        if (result.length < original.length) {
          fs.writeFileSync(full, result);
          const saved = ((1 - result.length / original.length) * 100).toFixed(1);
          console.log(`Minified: ${path.relative('_site', full)} (${saved}% smaller)`);
          minified++;
        }
      } catch (err) {
        console.error(`Skip (parse error): ${path.relative('_site', full)}`);
        errors++;
      }
    }
  }
  return { minified, errors };
}

processDir('_site');
console.log('HTML minification done.');
