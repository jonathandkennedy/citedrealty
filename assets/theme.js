// CitedRealty light/dark theme switch.
// Load this synchronously in <head> so the saved theme applies before first paint.
// Default (no choice stored) = LIGHT ("day mode"); dark is the toggle.
(function () {
  var KEY = 'cr-theme';
  var saved = localStorage.getItem(KEY);
  if (saved !== 'dark') document.documentElement.setAttribute('data-theme', 'light');

  function paint(btn) {
    var light = document.documentElement.getAttribute('data-theme') === 'light';
    btn.textContent = light ? '☾' : '☀'; // ☾ in light (go dark), ☀ in dark (go light)
    btn.setAttribute('aria-label', light ? 'Switch to dark mode' : 'Switch to light mode');
  }

  function init() {
    var btns = document.querySelectorAll('.theme-toggle');
    btns.forEach(function (btn) {
      paint(btn);
      btn.addEventListener('click', function () {
        var next = document.documentElement.getAttribute('data-theme') === 'light' ? 'dark' : 'light';
        if (next === 'light') document.documentElement.setAttribute('data-theme', 'light');
        else document.documentElement.removeAttribute('data-theme');
        localStorage.setItem(KEY, next);
        btns.forEach(paint);
      });
    });
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
