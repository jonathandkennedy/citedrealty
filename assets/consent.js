// CitedRealty cookie & pixel consent.
// Marketing pixels load ONLY after "Accept all". Choice stored in localStorage.
// Set your real IDs below; empty string = pixel never loads.
(function () {
  var PIXELS = {
    META_PIXEL_ID: "",        // e.g. "1234567890"
    GA4_ID: "",               // e.g. "G-XXXXXXX"
    GTM_ID: ""                // e.g. "GTM-XXXXXX" (use GTM *or* GA4, not both, ideally)
  };
  var KEY = "cr-consent";     // "all" | "essential"

  // Resolve path prefix so the privacy link works from /, /services/, /blog/, /audiences/
  var depth = (location.pathname.match(/\//g) || []).length - 1;
  var isSubdir = /\/(services|audiences|blog)\//.test(location.pathname);
  var root = isSubdir ? "../" : "";

  function loadPixels() {
    if (PIXELS.META_PIXEL_ID) {
      !function(f,b,e,v,n,t,s){if(f.fbq)return;n=f.fbq=function(){n.callMethod?
      n.callMethod.apply(n,arguments):n.queue.push(arguments)};if(!f._fbq)f._fbq=n;
      n.push=n;n.loaded=!0;n.version='2.0';n.queue=[];t=b.createElement(e);t.async=!0;
      t.src=v;s=b.getElementsByTagName(e)[0];s.parentNode.insertBefore(t,s)}(window,
      document,'script','https://connect.facebook.net/en_US/fbevents.js');
      window.fbq('init', PIXELS.META_PIXEL_ID);
      window.fbq('track', 'PageView');
    }
    if (PIXELS.GA4_ID) {
      var s = document.createElement('script');
      s.async = true; s.src = 'https://www.googletagmanager.com/gtag/js?id=' + PIXELS.GA4_ID;
      document.head.appendChild(s);
      window.dataLayer = window.dataLayer || [];
      window.gtag = function(){ window.dataLayer.push(arguments); };
      window.gtag('js', new Date());
      window.gtag('config', PIXELS.GA4_ID, { anonymize_ip: true });
    }
    if (PIXELS.GTM_ID) {
      (function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':new Date().getTime(),
      event:'gtm.js'});var f=d.getElementsByTagName(s)[0],j=d.createElement(s);j.async=true;
      j.src='https://www.googletagmanager.com/gtm.js?id='+i+'&l='+l;
      f.parentNode.insertBefore(j,f);})(window,document,'script','dataLayer',PIXELS.GTM_ID);
    }
  }

  function injectStyles() {
    var css = ''
      + '.cr-consent{position:fixed;left:14px;right:14px;bottom:14px;z-index:200;'
      + 'max-width:520px;margin:0 auto;background:var(--panel,#12121D);border:1px solid var(--line,#23233A);'
      + 'border-radius:16px;padding:20px 22px;box-shadow:0 20px 70px rgba(0,0,0,.35);'
      + 'font-family:Inter,system-ui,sans-serif;color:var(--text,#F0F0F8)}'
      + '.cr-consent p{margin:0 0 14px;font-size:13.5px;line-height:1.55;color:var(--muted,#9494AE)}'
      + '.cr-consent p b{color:var(--text,#F0F0F8)}'
      + '.cr-consent a{color:#C084FC;text-decoration:none}'
      + '.cr-consent .row{display:flex;gap:10px;flex-wrap:wrap}'
      + '.cr-consent button{cursor:pointer;font-family:inherit;font-weight:700;'
      + 'font-size:13.5px;border-radius:10px;padding:11px 18px;border:none}'
      + '.cr-accept{color:#fff;background:linear-gradient(120deg,#4F46E5,#8B5CF6 60%,#C084FC)}'
      + '.cr-essential{color:var(--text,#F0F0F8);background:none;border:1px solid var(--line,#23233A)!important}'
      + '@media(max-width:700px){.cr-consent{bottom:78px}}'; // clear the sticky mobile CTA
    var el = document.createElement('style');
    el.textContent = css;
    document.head.appendChild(el);
  }

  function showBanner() {
    if (document.querySelector('.cr-consent')) return;
    var el = document.createElement('div');
    el.className = 'cr-consent';
    el.setAttribute('role', 'dialog');
    el.setAttribute('aria-label', 'Cookie consent');
    el.innerHTML =
      '<p><b>Cookies, minus the mystery.</b> We use essential cookies to make the site work. ' +
      'With your OK, we also use analytics and advertising pixels to see what’s useful and ' +
      'reach people like you. Details in our <a href="' + root + 'privacy.html">privacy policy</a>.</p>' +
      '<div class="row">' +
      '<button type="button" class="cr-accept">Accept all</button>' +
      '<button type="button" class="cr-essential">Essentials only</button>' +
      '</div>';
    document.body.appendChild(el);
    el.querySelector('.cr-accept').addEventListener('click', function () {
      localStorage.setItem(KEY, 'all'); el.remove(); loadPixels();
    });
    el.querySelector('.cr-essential').addEventListener('click', function () {
      localStorage.setItem(KEY, 'essential'); el.remove();
    });
  }

  // Public API: footer "Cookie preferences" links call this to re-decide.
  window.crConsent = {
    open: function () { localStorage.removeItem(KEY); showBanner(); },
    status: function () { return localStorage.getItem(KEY); }
  };

  function init() {
    injectStyles();
    var choice = localStorage.getItem(KEY);
    if (choice === 'all') loadPixels();
    else if (choice !== 'essential') showBanner();
    // Wire any "Cookie preferences" links
    document.querySelectorAll('[data-cookie-prefs]').forEach(function (a) {
      a.addEventListener('click', function (e) { e.preventDefault(); window.crConsent.open(); });
    });
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
