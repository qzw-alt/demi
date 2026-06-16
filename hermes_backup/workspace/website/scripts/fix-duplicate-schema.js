// Fix corrupted/duplicate JSON-LD schema blocks in blog and news pages
// Removes: 1) blocks with HTML injected into JSON 2) duplicate @type schemas (keep first)
const fs = require('fs');
const path = require('path');

function fixFile(filePath) {
  let html = fs.readFileSync(filePath, 'utf8');
  let changed = false;

  // Find all JSON-LD script blocks
  const scriptRegex = /<script type="application\/ld\+json">([\s\S]*?)<\/script>/g;
  const blocks = [];
  let match;
  while ((match = scriptRegex.exec(html)) !== null) {
    blocks.push({
      fullMatch: match[0],
      content: match[1],
      start: match.index,
      end: match.index + match[0].length,
    });
  }

  if (blocks.length <= 1) return false;

  const cleanBlocks = [];
  const seenTypes = new Set();

  for (const block of blocks) {
    // Check for corruption: HTML tags inside JSON content
    if (/<(nav|div|header|footer|a|span|ul|li|h[1-6]|p|button|form|section)/i.test(block.content)) {
      changed = true;
      continue; // Skip corrupted block
    }

    // Try to parse JSON
    let parsed;
    try {
      parsed = JSON.parse(block.content);
    } catch (e) {
      // Invalid JSON — skip it
      changed = true;
      continue;
    }

    // Check for duplicate @type
    const type = parsed['@type'];
    if (!type) {
      cleanBlocks.push(block);
      continue;
    }

    if (seenTypes.has(type)) {
      changed = true;
      continue; // Skip duplicate
    }

    seenTypes.add(type);
    cleanBlocks.push(block);
  }

  if (!changed) return false;

  // Reconstruct: remove all existing JSON-LD blocks, re-insert clean ones
  // Remove all existing blocks in reverse order
  for (let i = blocks.length - 1; i >= 0; i--) {
    html = html.slice(0, blocks[i].start) + html.slice(blocks[i].end);
  }

  // Find insertion point: after last of these:
  // 1. existing JSON-LD block's closing </script> (already removed)
  // 2. after the last <meta ...> or <link ...> or <style> before </head>
  // Easiest: inject before </head>
  const cleanJSON = cleanBlocks.map(b => b.fullMatch).join('\n');

  if (html.includes('</head>')) {
    html = html.replace('</head>', cleanJSON + '\n</head>');
  } else if (html.includes('</title>')) {
    html = html.replace('</title>', '</title>\n' + cleanJSON);
  }

  fs.writeFileSync(filePath, html);
  return true;
}

function processDir(dir) {
  const entries = fs.readdirSync(dir, { withFileTypes: true });
  let fixed = 0;
  for (const e of entries) {
    const full = path.join(dir, e.name);
    if (e.isDirectory()) {
      if (!e.name.startsWith('_') && !e.name.startsWith('.')) {
        fixed += processDir(full);
      }
    } else if (e.name.endsWith('.html') && e.name !== 'index.html') {
      if (fixFile(full)) {
        console.log(`Schema fix: ${path.relative(process.cwd(), full)}`);
        fixed++;
      }
    }
  }
  return fixed;
}

// ── Entry ──

let targetDir;
if (fs.existsSync('_site')) {
  targetDir = '_site';
  console.log('Schema fix: Processing _site/ (build mode)');
} else {
  targetDir = path.join(__dirname, '..');
  console.log('Schema fix: Processing source directory (dev mode)');
}

const totalFixed = processDir(targetDir);
console.log(`Schema fix done: ${totalFixed} files fixed.`);
