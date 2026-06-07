const fs = require("fs");
const raw = fs.readFileSync(process.argv[2], "utf8");

// Simple search for fetchTime in the file
const ftIdx = raw.indexOf("fetchTime");
if (ftIdx === -1) { console.log("No fetchTime found"); process.exit(1); }

// Go back to find the opening " of the JS string (one that precedes the JSON's {)
let jsStrStart = ftIdx;
while (jsStrStart > 0) {
  if (raw[jsStrStart] === '"') {
    // Check this isn't an escaped quote (preceded by backslash)
    let bsCount = 0, p = jsStrStart - 1;
    while (p > 0 && raw[p] === '\\') { bsCount++; p--; }
    if (bsCount % 2 === 0) break; // unescaped quote
  }
  jsStrStart--;
}

// Find closing " of the JS string (unescaped)
let jsStrEnd = ftIdx, esc = false;
for (let i = jsStrStart + 1; i < raw.length; i++) {
  if (esc) { esc = false; continue; }
  if (raw[i] === '\\') { esc = true; continue; }
  if (raw[i] === '"') { jsStrEnd = i; break; }
}

// Extract the JS string content (between the opening and closing quotes)
const jsStr = raw.substring(jsStrStart + 1, jsStrEnd);
console.log("JS string length:", jsStr.length);

// Unescape: \\ -> placeholder, \" -> ", \n -> newline, then restore \\
const PH = '\x00';
const jsonStr = jsStr
  .replace(/\\\\/g, PH)
  .replace(/\\"/g, '"')
  .replace(/\\n/g, '\n')
  .replace(new RegExp(PH, 'g'), '\\');

try {
  const data = JSON.parse(jsonStr);
  const audits = data.audits || {};

  if (data.categories) {
    console.log("\n=== SCORES ===");
    for (const [k, v] of Object.entries(data.categories)) {
      console.log(k + ": " + Math.round(v.score * 100));
    }
  }

  const metrics = [
    ["largest-contentful-paint", "LCP"],
    ["total-blocking-time", "TBT"],
    ["cumulative-layout-shift", "CLS"],
    ["first-contentful-paint", "FCP"],
    ["speed-index", "Speed Index"],
    ["interactive", "TTI"]
  ];

  console.log("\n=== CORE WEB VITALS ===");
  for (const [id, label] of metrics) {
    const a = audits[id];
    if (a) console.log(label + ": " + (a.displayValue || "N/A") + " | score=" + Math.round((a.score||0)*100));
  }

  console.log("\n=== OPPORTUNITIES (with savings) ===");
  let oppCount = 0;
  for (const [id, a] of Object.entries(audits)) {
    let savings = [];
    if (a.details && a.details.overallSavingsMs) savings.push((a.details.overallSavingsMs/1000).toFixed(2) + "s");
    if (a.details && a.details.overallSavingsBytes) savings.push((a.details.overallSavingsBytes/1024).toFixed(0) + "KB");
    if (a.score !== null && a.score < 1 && savings.length > 0) {
      console.log((a.title||id) + ": " + (a.displayValue||"") + " [" + savings.join(", ") + "]");
      oppCount++;
    }
  }
  if (oppCount === 0) console.log("(none)");

  console.log("\n=== DIAGNOSTICS (score < 1) ===");
  let diagCount = 0;
  for (const [id, a] of Object.entries(audits)) {
    if (a.scoreDisplayMode === "diagnostic" && a.score !== null && a.score < 1 && a.score > 0) {
      console.log((a.title||id) + ": score=" + Math.round(a.score*100));
      diagCount++;
    }
  }
  if (diagCount === 0) console.log("(none)");

} catch(e) {
  console.log("Parse error:", e.message);
  // Find error position
  const posMatch = e.message.match(/position (\d+)/);
  if (posMatch) {
    const p = parseInt(posMatch[1]);
    console.log("Around error:", JSON.stringify(jsonStr.substring(Math.max(0, p - 40), p + 40)));
  }
}
