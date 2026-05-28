/* itconverts — site.js : shared chrome behaviour for standalone pages.
 * Theme toggle persists to the same key the app uses (itc-theme-c), so the
 * dark/light choice carries between the app and the content pages. */
(function () {
  'use strict';
  var sun = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="4.5"/><path d="M12 2v2M12 20v2M4 12H2M22 12h-2M5 5l1.5 1.5M17.5 17.5L19 19M19 5l-1.5 1.5M6.5 17.5L5 19"/></svg>';
  var moon = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.8A8 8 0 1 1 11.2 3a6.2 6.2 0 0 0 9.8 9.8z"/></svg>';
  function get() { try { return localStorage.getItem('itc-theme-c'); } catch (e) { return null; } }
  function apply(t) {
    document.documentElement.setAttribute('data-theme', t);
    var btn = document.getElementById('theme');
    if (btn) btn.innerHTML = (t === 'dark' ? sun : moon);
    try { localStorage.setItem('itc-theme-c', t); } catch (e) {}
  }
  function init() {
    apply(get() === 'light' ? 'light' : 'dark');   // default dark, matches the app
    var btn = document.getElementById('theme');
    if (btn) btn.addEventListener('click', function () {
      apply(document.documentElement.getAttribute('data-theme') === 'dark' ? 'light' : 'dark');
    });
    var y = document.getElementById('yr'); if (y) y.textContent = new Date().getFullYear();
  }
  if (document.readyState !== 'loading') init();
  else document.addEventListener('DOMContentLoaded', init);
})();
