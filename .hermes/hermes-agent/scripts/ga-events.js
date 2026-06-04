// GA4 Custom Events — China Hospitals Guide
// Tracks: CTA clicks, form interactions, scroll depth, outbound links
(function() {
  if (typeof gtag !== 'function') return;

  // Debounce helper
  function debounce(fn, ms) {
    let timer;
    return function(...args) {
      clearTimeout(timer);
      timer = setTimeout(() => fn.apply(this, args), ms);
    };
  }

  // ── CTA Button Click Tracking ──
  document.addEventListener('click', function(e) {
    var el = e.target.closest('a');
    if (!el) return;

    var href = el.getAttribute('href') || '';
    var text = (el.textContent || '').trim();
    var classes = el.className || '';

    // Classify the CTA
    var ctaType = 'other';
    if (classes.includes('cta-button') || classes.includes('cta-btn') ||
        classes.includes('submit-btn') || classes.includes('nav-cta')) {
      ctaType = 'primary_cta';
    } else if (classes.includes('view-details-btn')) {
      ctaType = 'hospital_detail';
    } else if (classes.includes('lead-magnet-btn') || classes.includes('download-btn')) {
      ctaType = 'lead_magnet';
    } else if (href.includes('wa.me') || href.includes('api.whatsapp.com')) {
      ctaType = 'whatsapp';
    } else if (href.includes('t.me')) {
      ctaType = 'telegram';
    } else if (href.includes('paypal.com')) {
      ctaType = 'paypal';
    }

    if (ctaType !== 'other' || el.getAttribute('data-track') !== null) {
      gtag('event', 'cta_click', {
        cta_type: ctaType,
        cta_text: text.substring(0, 80),
        cta_url: href.substring(0, 200),
        page_location: location.pathname
      });
    }

    // Outbound link tracking
    if (href.startsWith('http') && !href.includes(location.hostname)) {
      gtag('event', 'outbound_link', {
        link_url: href.substring(0, 200),
        link_text: text.substring(0, 80),
        page_location: location.pathname
      });
    }
  });

  // ── Form Interaction Tracking ──
  var formTracked = new WeakSet();
  var formFieldsTouched = {};

  document.addEventListener('focusin', function(e) {
    var field = e.target.closest('input, textarea, select');
    if (!field || !field.form) return;
    if (formTracked.has(field.form)) return;

    // First field focus = form_start
    var formId = field.form.id || field.form.getAttribute('name') || 'unnamed_form';
    formTracked.add(field.form);
    formFieldsTouched[formId] = 0;

    gtag('event', 'form_start', {
      form_id: formId,
      page_location: location.pathname
    });
  });

  document.addEventListener('change', function(e) {
    var field = e.target.closest('input, textarea, select');
    if (!field || !field.form) return;
    var formId = field.form.id || field.form.getAttribute('name') || 'unnamed_form';
    formFieldsTouched[formId] = (formFieldsTouched[formId] || 0) + 1;
  });

  document.addEventListener('submit', function(e) {
    var form = e.target.closest('form');
    if (!form) return;
    var formId = form.id || form.getAttribute('name') || 'unnamed_form';
    gtag('event', 'form_submit', {
      form_id: formId,
      fields_touched: formFieldsTouched[formId] || 0,
      page_location: location.pathname
    });
  });

  // ── Scroll Depth Tracking ──
  var scrollMarks = [25, 50, 75, 100];
  var scrollFired = {};
  var onScroll = debounce(function() {
    var docH = document.documentElement.scrollHeight - window.innerHeight;
    if (docH <= 0) return;
    var pct = Math.round((window.scrollY / docH) * 100);
    scrollMarks.forEach(function(mark) {
      if (pct >= mark && !scrollFired[mark]) {
        scrollFired[mark] = true;
        gtag('event', 'scroll_depth', {
          depth: mark,
          page_location: location.pathname
        });
      }
    });
  }, 300);

  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('load', function() { onScroll(); });

  // ── Case Review Form Success Tracking ──
  // The contact-new.html form calls EmailJS and shows #formSuccess
  var successObserver = new MutationObserver(function(mutations) {
    mutations.forEach(function(m) {
      if (m.target.id === 'formSuccess' && m.target.style.display !== 'none') {
        gtag('event', 'conversion', {
          send_to: 'G-RVYZENK472',
          event_category: 'form',
          event_label: 'case_review_submitted',
          page_location: location.pathname
        });
        // Also fire standard generate_lead
        gtag('event', 'generate_lead', {
          page_location: location.pathname
        });
        successObserver.disconnect();
      }
    });
  });

  var formSuccess = document.getElementById('formSuccess');
  if (formSuccess) {
    successObserver.observe(formSuccess, { attributes: true, attributeFilter: ['style', 'class'] });
  }

  // ── Page engagement timer ──
  var startTime = Date.now();
  window.addEventListener('beforeunload', function() {
    var seconds = Math.round((Date.now() - startTime) / 1000);
    if (seconds >= 10) {
      gtag('event', 'engagement_time', {
        seconds: seconds,
        page_location: location.pathname
      });
    }
  });

  console.log('[CHG] GA4 events initialized');
})();
