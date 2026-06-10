// Inject correct schema.org JSON-LD based on page type
// Only ADDS missing schema — does not remove existing blocks
const fs = require('fs');
const path = require('path');

const BASE = 'https://chinahospitalsguide.com';

// ── Schema Templates ──

function medicalBusinessSchema() {
  return {
    "@context": "https://schema.org",
    "@type": "MedicalBusiness",
    "name": "China Hospitals Guide",
    "url": BASE,
    "logo": `${BASE}/og-image.webp`,
    "image": `${BASE}/og-image.webp`,
    "description": "Independent medical travel coordination for international patients seeking hospital treatment in China. Hospital matching, cost comparison, and pre-arrival planning.",
    "telephone": "+86-135-2200-5627",
    "email": "contact@chinahospitalsguide.com",
    "areaServed": {
      "@type": "Country",
      "name": "China"
    },
    "sameAs": [
      "https://www.facebook.com/chinahospitalsguide",
      "https://twitter.com/chinahospitals"
    ]
  };
}

function webSiteSchema() {
  return {
    "@context": "https://schema.org",
    "@type": "WebSite",
    "name": "China Hospitals Guide",
    "url": BASE,
    "potentialAction": {
      "@type": "SearchAction",
      "target": {
        "@type": "EntryPoint",
        "urlTemplate": `${BASE}/hospitals.html?search={search_term_string}`
      },
      "query-input": "required name=search_term_string"
    }
  };
}

function webPageSchema(url, title, description) {
  return {
    "@context": "https://schema.org",
    "@type": "WebPage",
    "name": title || "China Hospitals Guide",
    "url": url || BASE,
    "description": description || "Find and prepare for hospital treatment in China — independent guidance for international patients.",
    "publisher": {
      "@type": "Organization",
      "name": "China Hospitals Guide",
      "url": BASE,
      "logo": {
        "@type": "ImageObject",
        "url": `${BASE}/og-image.webp`
      }
    }
  };
}

function offerSchema(name, price, description) {
  return {
    "@context": "https://schema.org",
    "@type": "Offer",
    "name": name,
    "price": price,
    "priceCurrency": "USD",
    "description": description,
    "url": `${BASE}/pricing.html`,
    "seller": {
      "@type": "Organization",
      "name": "China Hospitals Guide",
      "url": BASE
    }
  };
}

// ── Page Classification ──

function classifyPage(filePath) {
  const name = path.basename(filePath);

  if (name === 'index.html') return 'homepage';
  if (name === 'pricing.html') return 'pricing';
  if (name === 'hospitals.html') return 'hospitals';
  if (name === 'services.html') return 'services';
  if (name === 'contact.html' || name === 'contact-new.html') return 'contact';
  if (name === 'about.html') return 'about';
  if (name === 'how-it-works.html') return 'howitworks';

  const dir = path.dirname(filePath);
  if (dir.includes('blog') && name !== 'index.html') return 'blog';
  if (dir.includes('news') && name !== 'index.html' && name !== 'template-news-article.html') return 'news';
  if (dir.includes('treatments') && name !== 'index.html') return 'treatment';
  if (dir.includes('stories') && name !== 'index.html') return 'story';
  if (dir.includes('course')) return 'course';

  return 'page';
}

// ── Process ──

function processDir(dir) {
  const entries = fs.readdirSync(dir, { withFileTypes: true });
  for (const e of entries) {
    const full = path.join(dir, e.name);
    if (e.isDirectory()) {
      if (!e.name.startsWith('_') && !e.name.startsWith('.')) processDir(full);
    } else if (e.name.endsWith('.html')) {
      let html = fs.readFileSync(full, 'utf8');
      let changed = false;
      const pageType = classifyPage(full);
      const relPath = path.relative('_site', full).replace(/\\/g, '/');
      const pageUrl = `${BASE}/${relPath}`.replace('/index.html', '/');

      // Extract existing title/description for WebPage schema
      const titleMatch = html.match(/<title>([^<]+)<\/title>/);
      const descMatch = html.match(/<meta\s+name=["']description["']\s+content=["']([^"']+)["']/i);
      const pageTitle = titleMatch ? titleMatch[1].trim() : '';
      const pageDesc = descMatch ? descMatch[1].trim() : '';

      // Check what schema already exists
      const hasOrganization = /"@type"\s*:\s*"Organization"/i.test(html);
      const hasMedicalBusiness = /"@type"\s*:\s*"MedicalBusiness"/i.test(html);
      const hasWebSite = /"@type"\s*:\s*"WebSite"/i.test(html);
      const hasWebPage = /"@type"\s*:\s*"WebPage"/i.test(html);
      const hasOffer = /"@type"\s*:\s*"Offer"/i.test(html);

      // Build list of schema blocks to inject
      const schemas = [];

      switch (pageType) {
        case 'homepage':
          if (!hasMedicalBusiness) schemas.push(medicalBusinessSchema());
          if (!hasWebSite) schemas.push(webSiteSchema());
          break;

        case 'pricing':
          if (!hasOffer) {
            schemas.push(offerSchema(
              'Hospital Match & Plan',
              '49',
              '3-5 hospital options matched to your case and budget, with cost range and city comparison.'
            ));
            schemas.push(offerSchema(
              'Pre-Arrival Coordination',
              '399',
              'Hospital phone contact, appointment coordination, medical record preparation, and airport pickup arrangement.'
            ));
          }
          if (!hasWebPage) schemas.push(webPageSchema(pageUrl, pageTitle, pageDesc));
          break;

        case 'hospitals':
        case 'services':
        case 'about':
        case 'howitworks':
          if (!hasWebPage && pageDesc) {
            schemas.push(webPageSchema(pageUrl, pageTitle, pageDesc));
          }
          break;

        case 'blog':
        case 'news':
        case 'treatment':
        case 'story':
          // These typically already have Article/NewsArticle/MedicalWebPage schema
          // Only add WebPage as parent if completely missing
          if (!hasWebPage && !hasOrganization && pageDesc) {
            schemas.push(webPageSchema(pageUrl, pageTitle, pageDesc));
          }
          break;

        case 'course':
          if (!hasWebPage && pageDesc) {
            schemas.push(webPageSchema(pageUrl, pageTitle, pageDesc));
          }
          break;

        case 'page':
          if (!hasWebPage && !hasOrganization && pageDesc) {
            schemas.push(webPageSchema(pageUrl, pageTitle, pageDesc));
          }
          break;
      }

      if (schemas.length > 0) {
        const jsonBlocks = schemas.map(s => `<script type="application/ld+json">\n${JSON.stringify(s, null, 2)}\n</script>`).join('\n');

        // Inject after existing schema blocks or before </head>
        const lastScriptMatch = html.match(/<script type="application\/ld\+json">[\s\S]*?<\/script>/g);
        if (lastScriptMatch && lastScriptMatch.length > 0) {
          const lastBlock = lastScriptMatch[lastScriptMatch.length - 1];
          html = html.replace(lastBlock, lastBlock + '\n' + jsonBlocks);
        } else if (html.includes('</head>')) {
          html = html.replace('</head>', jsonBlocks + '\n</head>');
        } else if (html.includes('</title>')) {
          html = html.replace('</title>', '</title>\n' + jsonBlocks);
        }

        fs.writeFileSync(full, html);
        changed = true;
      }

      if (changed) {
        const shortPath = path.relative('_site', full);
        console.log(`Schema: ${shortPath} [${pageType}] +${schemas.map(s => s['@type']).join(', ')}`);
      }
    }
  }
}

processDir('_site');
console.log('Schema injection done.');
