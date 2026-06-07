// Standardize CTA text across all blog and news articles
// Replaces varied CTA texts with the canonical "Start Free Case Review"
const fs = require('fs');
const path = require('path');

// Map of variant -> canonical text
const replacements = [
  ['Request Free Consultation', 'Start Free Case Review'],
  ['Get Free Consultation', 'Start Free Case Review'],
  ['Get a Free Consultation', 'Start Free Case Review'],
  ['Request a Free Consultation', 'Start Free Case Review'],
  ['Get Free Quote', 'Start Free Case Review'],
  ['Request Free Quote', 'Start Free Case Review'],
  ['Free Quote Request', 'Start Free Case Review'],
  ['Get Free Case Review →', 'Start Free Case Review'],
  ['Get Free Case Review &rarr;', 'Start Free Case Review'],
  ['Get Free Case Review →', 'Start Free Case Review'],
  ['Get in Touch →', 'Start Free Case Review'],
  ['Get Free Hospital Recommendations →', 'Start Free Case Review'],
  ['Get My Free Hospital Guide →', 'Start Free Case Review'],
  ['Request Free Assessment', 'Start Free Case Review'],
  ['Get Free Clinic Recommendations', 'Start Free Case Review'],
  ['Get Free Assistance', 'Start Free Case Review'],
  ['Get Your Free Cost Estimate', 'Start Free Case Review'],
  ['Get My Free Quote', 'Start Free Case Review'],
];

function processDir(dir) {
  const entries = fs.readdirSync(dir, { withFileTypes: true });
  for (const e of entries) {
    const full = path.join(dir, e.name);
    if (e.isDirectory()) {
      if (!e.name.startsWith('_') && !e.name.startsWith('.')) processDir(full);
    } else if (e.name.endsWith('.html')) {
      let html = fs.readFileSync(full, 'utf8');
      let changed = false;

      for (const [from, to] of replacements) {
        if (html.includes(from)) {
          html = html.split(from).join(to);
          changed = true;
        }
      }

      if (changed) {
        fs.writeFileSync(full, html);
        console.log('Fixed CTA:', path.relative('.', full));
      }
    }
  }
}

processDir('blog');
processDir('news');
processDir('treatments');
processDir('stories');

console.log('CTA standardization done.');
