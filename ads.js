/* itconverts — ads.js
 * Drops Google AdSense into the EXISTING reserved slot (.promo-area > .promo-unit)
 * without renaming the class (ad-blockers collapse elements literally named
 * "ad/ads/advert", which would break layout — the README calls this out).
 *
 * Behaviour:
 *   - Supporters (ITC_PAY.isSupporter()) see NO ads; the slot is removed.
 *   - Everyone else gets one responsive display unit.
 *   - It reacts live to entitlement changes (pay -> ads vanish instantly).
 *
 * Setup: put your IDs in ITC_CONFIG (see the <head> of itconverts.html):
 *   window.ITC_CONFIG = { ADSENSE_CLIENT:'ca-pub-XXXXXXXXXXXXXXXX', ADSENSE_SLOT:'1234567890', ... }
 */
(function (g) {
  'use strict';
  var CFG = g.ITC_CONFIG || {};
  var CLIENT = CFG.ADSENSE_CLIENT || '';   // ca-pub-...
  var SLOT = CFG.ADSENSE_SLOT || '';       // numeric slot id from AdSense

  function supporter() { return g.ITC_PAY && g.ITC_PAY.isSupporter(); }

  // Inject the AdSense library once.
  var libLoaded = false;
  function loadLib() {
    if (libLoaded || !CLIENT) return;
    libLoaded = true;
    var s = document.createElement('script');
    s.async = true;
    s.crossOrigin = 'anonymous';
    s.src = 'https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=' + encodeURIComponent(CLIENT);
    document.head.appendChild(s);
  }

  function render() {
    var area = document.querySelector('.promo-area');
    if (!area) return;

    if (supporter()) { area.style.display = 'none'; return; }
    area.style.display = '';

    // Not configured yet -> leave the quiet placeholder that ships in the HTML.
    if (!CLIENT || !SLOT) return;

    var unit = area.querySelector('.promo-unit');
    if (!unit || unit.getAttribute('data-ad-ready') === '1') return;

    loadLib();
    // Replace placeholder contents with a real responsive ad, keep the label + box.
    unit.setAttribute('data-ad-ready', '1');
    unit.style.height = 'auto';
    unit.style.minHeight = '90px';
    var ph = unit.querySelector('.ph'); if (ph) ph.remove();
    var ins = document.createElement('ins');
    ins.className = 'adsbygoogle';
    ins.style.display = 'block';
    ins.style.width = '100%';
    ins.setAttribute('data-ad-client', CLIENT);
    ins.setAttribute('data-ad-slot', SLOT);
    ins.setAttribute('data-ad-format', 'auto');
    ins.setAttribute('data-full-width-responsive', 'true');
    unit.appendChild(ins);
    try { (g.adsbygoogle = g.adsbygoogle || []).push({}); } catch (e) {}
  }

  function start() {
    render();
    if (g.ITC_PAY && g.ITC_PAY.subscribe) g.ITC_PAY.subscribe(render); // pay -> hide ads live
  }

  if (document.readyState !== 'loading') start();
  else document.addEventListener('DOMContentLoaded', start);
})(window);
