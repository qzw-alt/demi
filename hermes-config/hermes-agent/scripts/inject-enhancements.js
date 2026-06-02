// Post-build injection: GA4 events, exit popup, risk banner, lead magnet
const fs = require('fs');
const path = require('path');

// Copy ga-events.js to _site/
fs.copyFileSync('scripts/ga-events.js', '_site/ga-events.js');
console.log('Copied ga-events.js to _site/');

// ── Exit Popup HTML + JS ──
const exitPopupHTML = `
<div id="exitPopup">
  <div class="exit-popup-content">
    <div class="exit-popup-icon">🏥</div>
    <h3 class="exit-popup-title">Before You Go...</h3>
    <p class="exit-popup-text">Finding the right hospital in China can be overwhelming. Let us help — free, no commitment.</p>
    <div class="exit-popup-urgency">
      <p>⏳ Most cases get a hospital match within 24 hours</p>
    </div>
    <a href="/contact-new.html" class="exit-popup-cta">Start Free Case Review</a>
    <br>
    <a href="#" class="exit-popup-dismiss" onclick="document.getElementById('exitPopup').style.display='none'; return false;">No thanks, I'll keep searching</a>
  </div>
</div>
<script>
(function(){
  var shown = sessionStorage.getItem('exitPopupShown');
  if (shown) return;
  var popup = document.getElementById('exitPopup');
  if (!popup) return;
  var fired = false;
  document.addEventListener('mouseout', function(e) {
    if (fired) return;
    if (e.clientY <= 0 && e.clientX > 0) {
      fired = true;
      sessionStorage.setItem('exitPopupShown', '1');
      popup.style.display = 'flex';
    }
  });
})();
</script>
`;

// ── Risk Banner HTML ──
const riskBannerHTML = `
<div class="risk-banner">
  <div class="risk-banner-inner">
    <div class="risk-banner-icon">🛡️</div>
    <div class="risk-banner-text">
      <strong>100% Independent Guidance</strong>
      <p>We are not affiliated with any hospital. We don't take commissions. Our only goal is finding the right care for you.</p>
    </div>
  </div>
</div>
`;

// ── Lead Magnet HTML (for blog posts) ──
const leadMagnetHTML = `
<div class="lead-magnet">
  <div class="lead-magnet-icon">📋</div>
  <h3 class="lead-magnet-title">Get Your Free Hospital Cost Comparison</h3>
  <p class="lead-magnet-desc">We'll match you with 2-3 top hospitals for your procedure, with pricing and English support details — all free.</p>
  <a href="/contact-new.html" class="lead-magnet-btn">Start Free Case Review</a>
</div>
`;

function processDir(dir) {
  const entries = fs.readdirSync(dir, { withFileTypes: true });
  for (const e of entries) {
    const full = path.join(dir, e.name);
    if (e.isDirectory()) {
      if (!e.name.startsWith('_') && !e.name.startsWith('.')) processDir(full);
    } else if (e.name.endsWith('.html')) {
      let html = fs.readFileSync(full, 'utf8');
      let changed = false;

      // 1. Inject GA4 events script before </body>
      if (!html.includes('ga-events.js') && html.includes('</body>')) {
        html = html.replace('</body>', '  <script src="/ga-events.js" defer></script>\n</body>');
        changed = true;
      }

      // 2. Inject exit popup before </body> (once per page)
      if (!html.includes('id="exitPopup"') && html.includes('</body>')) {
        html = html.replace('</body>', exitPopupHTML + '\n</body>');
        changed = true;
      }

      // 3. Inject risk banner before the first </section> or </main> on key pages
      const isKeyPage = /(index|about|services|pricing|contact|how-it-works|hospitals)\.html/.test(full);
      const isBlogArticle = /blog\/[^/]+\.html/.test(full) && !/blog\/(index\.html|index$)/.test(full);
      const isTreatment = /treatments\/[^/]+\.html/.test(full);

      if (isKeyPage && !html.includes('class="risk-banner"')) {
        // Insert before closing section or after a CTA section
        const target = html.includes('</section>') ? '</section>' : '</main>';
        const parts = html.split(target);
        if (parts.length >= 2) {
          // Insert before the last section on the page
          const lastIdx = html.lastIndexOf(target);
          html = html.substring(0, lastIdx) + riskBannerHTML + '\n' + target + html.substring(lastIdx + target.length);
          changed = true;
        }
      }

      // 4. Inject lead magnet at end of blog article content (before related links or footer)
      if (isBlogArticle && !html.includes('class="lead-magnet"')) {
        // Insert before </article> or before footer/related section
        if (html.includes('</article>')) {
          html = html.replace('</article>', leadMagnetHTML + '\n</article>');
          changed = true;
        } else if (html.includes('class="article-content"')) {
          // Find the end of article content
          html = html.replace(/(<div class="article-content"[^>]*>[\s\S]*?)(<\/div>\s*(?:<div class="related|<\/div>\s*$))/m,
            '$1' + leadMagnetHTML + '\n$2');
          changed = true;
        }
      }

      // 5. Inject lead magnet at end of treatment pages too
      if (isTreatment && !html.includes('class="lead-magnet"')) {
        if (html.includes('</article>')) {
          html = html.replace('</article>', leadMagnetHTML + '\n</article>');
          changed = true;
        } else if (html.includes('faq-item') && !html.includes('class="lead-magnet"')) {
          const lastFaq = html.lastIndexOf('</div>\n');
          if (lastFaq > 0) {
            // Insert after FAQ section
            html = html.substring(0, lastFaq) + leadMagnetHTML + '\n' + html.substring(lastFaq);
            changed = true;
          }
        }
      }

      if (changed) {
        fs.writeFileSync(full, html);
        console.log('Enhanced:', path.relative('_site', full));
      }
    }
  }
}

processDir('_site');
console.log('CRO enhancements injected.');
