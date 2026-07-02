// ===== GA4 EVENT TRACKING =====
// Centralized event tracking for chinahospitalsguide.com
// Requires gtag.js + dataLayer to be loaded (see <head> in each page).
// Author: Hermes (2026-07-02)
//
// Events tracked:
//   - scroll_depth (25/50/75/100) - engagement
//   - article_complete (100% scroll + 30s dwell) - engagement
//   - cta_click (CTA buttons + Contact links) - conversion
//   - outbound_click (external links) - engagement
//   - internal_click (internal navigation) - engagement
//   - newsletter_submit (Formspree forms) - conversion
//   - file_download (PDFs, docs) - engagement

(function() {
    'use strict';
    if (typeof gtag === 'undefined') return;

    var PAGE_TYPE = document.body.getAttribute('data-page-type')
        || (location.pathname.indexOf('/blog/') === 0 ? 'article'
            : (location.pathname.indexOf('/news/') === 0 ? 'news'
                : (location.pathname === '/' || location.pathname === '/index.html' ? 'home'
                    : (location.pathname.indexOf('/blog') === 0 ? 'blog_index' : 'other'))));

    // -------- 1. SCROLL DEPTH --------
    var scrollMarks = { '25': false, '50': false, '75': false, '100': false };
    var articleCompleteFired = false;
    var dwellStart = Date.now();
    var dwell30sFired = false;

    function trackScroll() {
        var docHeight = Math.max(document.body.scrollHeight, document.documentElement.scrollHeight);
        var winHeight = window.innerHeight;
        var scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        if (docHeight <= 0) return;
        var scrollPercent = Math.floor(((scrollTop + winHeight) / docHeight) * 100);
        for (var pct in scrollMarks) {
            if (!scrollMarks[pct] && scrollPercent >= parseInt(pct, 10)) {
                scrollMarks[pct] = true;
                gtag('event', 'scroll_depth', {
                    'event_category': 'engagement',
                    'event_label': pct + '%',
                    'page_type': PAGE_TYPE,
                    'page_path': location.pathname,
                    'value': parseInt(pct, 10)
                });
            }
        }
    }
    var scrollTimer = null;
    window.addEventListener('scroll', function() {
        if (scrollTimer) return;
        scrollTimer = setTimeout(function() { trackScroll(); scrollTimer = null; }, 150);
    }, { passive: true });
    window.addEventListener('load', trackScroll);

    // -------- 2. ARTICLE COMPLETE (100% scroll + 30s dwell) --------
    function maybeFireArticleComplete() {
        if (articleCompleteFired) return;
        if (!scrollMarks['100']) return;
        if (Date.now() - dwellStart < 30000) return;
        articleCompleteFired = true;
        gtag('event', 'article_complete', {
            'event_category': 'engagement',
            'event_label': 'read_full_article',
            'page_type': PAGE_TYPE,
            'page_path': location.pathname,
            'value': 1
        });
    }
    setInterval(maybeFireArticleComplete, 5000);
    // Also fire on unload if qualified
    window.addEventListener('beforeunload', function() {
        maybeFireArticleComplete();
    });

    // -------- 3. CTA CLICK + OUTBOUND/INTERNAL CLICK --------
    document.addEventListener('click', function(e) {
        var target = e.target.closest('a, button');
        if (!target) return;
        var href = target.getAttribute('href') || '';
        var text = (target.textContent || '').trim().substring(0, 80);

        // Primary CTA classes
        if (target.classList.contains('cta-button') || target.classList.contains('nav-cta')
            || target.classList.contains('btn-primary') || target.classList.contains('btn-cta')) {
            gtag('event', 'cta_click', {
                'event_category': 'conversion',
                'event_label': text,
                'cta_text': text,
                'cta_href': href,
                'page_type': PAGE_TYPE,
                'page_path': location.pathname
            });
            return;
        }

        // Contact / Start Here CTA (any link to contact page)
        if (href && (href.indexOf('contact.html') !== -1 || href.indexOf('contact-new') !== -1
            || href.indexOf('/contact') !== -1)) {
            gtag('event', 'cta_click', {
                'event_category': 'conversion',
                'event_label': 'Contact CTA',
                'cta_text': text,
                'cta_href': href,
                'page_type': PAGE_TYPE,
                'page_path': location.pathname
            });
            return;
        }

        // External (outbound) link
        if (href && (href.indexOf('http://') === 0 || href.indexOf('https://') === 0)
            && href.indexOf('chinahospitalsguide.com') === -1
            && href.indexOf('localhost') === -1) {
            gtag('event', 'outbound_click', {
                'event_category': 'engagement',
                'event_label': text,
                'outbound_url': href,
                'page_type': PAGE_TYPE,
                'page_path': location.pathname
            });
            return;
        }

        // Internal navigation (for article-to-article flow analysis)
        if (href && href.indexOf('#') !== 0 && href.indexOf('javascript') !== 0
            && (href.indexOf('/blog/') !== -1 || href.indexOf('.html') !== -1)) {
            gtag('event', 'internal_click', {
                'event_category': 'navigation',
                'event_label': text,
                'link_path': href,
                'page_type': PAGE_TYPE,
                'page_path': location.pathname
            });
        }
    }, true);

    // -------- 4. NEWSLETTER FORM SUBMIT (Formspree) --------
    document.addEventListener('submit', function(e) {
        var form = e.target;
        if (!form || form.tagName !== 'FORM') return;
        var action = form.getAttribute('action') || '';
        if (action.indexOf('formspree.io') !== -1) {
            gtag('event', 'newsletter_submit', {
                'event_category': 'conversion',
                'event_label': 'Newsletter Signup',
                'form_action': action,
                'page_type': PAGE_TYPE,
                'page_path': location.pathname,
                'value': 1
            });
        }
    }, true);

    // -------- 5. FILE DOWNLOADS (PDFs / docs) --------
    document.addEventListener('click', function(e) {
        var target = e.target.closest('a');
        if (!target) return;
        var href = target.getAttribute('href') || '';
        if (/\.(pdf|doc|docx|xls|xlsx|zip|rar)(\?|$)/i.test(href)) {
            gtag('event', 'file_download', {
                'event_category': 'engagement',
                'event_label': href.split('/').pop(),
                'file_url': href,
                'page_type': PAGE_TYPE,
                'page_path': location.pathname
            });
        }
    }, true);

})();