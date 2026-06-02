const sharp = require('sharp');
const fs = require('fs');
const path = require('path');

const dirs = ['images', 'images/hospitals'];

async function convert(dir) {
  const files = fs.readdirSync(dir).filter(f => /\.(jpg|jpeg|png)$/i.test(f));
  for (const file of files) {
    const input = path.join(dir, file);
    const output = path.join(dir, file.replace(/\.(jpg|jpeg|png)$/i, '.webp'));
    if (fs.existsSync(output)) continue; // skip already converted
    try {
      await sharp(input).webp({ quality: 80 }).toFile(output);
      const inSize = fs.statSync(input).size;
      const outSize = fs.statSync(output).size;
      console.log(`${input} → ${output} (${(inSize/1024).toFixed(0)}KB → ${(outSize/1024).toFixed(0)}KB, -${((1-outSize/inSize)*100).toFixed(0)}%)`);
    } catch (err) {
      console.error(`Failed: ${input}`, err.message);
    }
  }
}

(async () => {
  for (const dir of dirs) {
    if (fs.existsSync(dir)) await convert(dir);
  }
  console.log('Done.');
})();
