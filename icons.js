/* itconverts — minimal geometric line-icon set. window.ITCICON(name) -> svg string.
 * 24x24, 1.6 stroke, currentColor. Intentionally simple. */
(function (global) {
  'use strict';
  var P = {
    ruler: '<path d="M3 7h18v10H3z"/><path d="M7 7v3M11 7v5M15 7v3M19 7v5"/>',
    scale: '<path d="M12 4v16M7 20h10"/><path d="M5 8h14"/><path d="M5 8l-2 6a3 3 0 0 0 6 0L7 8M19 8l-2 6a3 3 0 0 0 6 0l-2-6"/>',
    thermometer: '<path d="M14 14V5a2 2 0 0 0-4 0v9a4 4 0 1 0 4 0z"/>',
    square: '<rect x="4" y="4" width="16" height="16" rx="1"/>',
    beaker: '<path d="M9 3h6M10 3v6l-5 9a1.5 1.5 0 0 0 1.3 2.2h11.4A1.5 1.5 0 0 0 19 18l-5-9V3"/><path d="M7.5 14h9"/>',
    gauge: '<path d="M4 18a8 8 0 1 1 16 0"/><path d="M12 18l4-5"/>',
    clock: '<circle cx="12" cy="12" r="8"/><path d="M12 8v4l3 2"/>',
    database: '<ellipse cx="12" cy="6" rx="7" ry="3"/><path d="M5 6v6c0 1.7 3.1 3 7 3s7-1.3 7-3V6M5 12v6c0 1.7 3.1 3 7 3s7-1.3 7-3v-6"/>',
    bolt: '<path d="M13 3 5 13h6l-1 8 8-10h-6z"/>',
    plug: '<path d="M9 3v5M15 3v5"/><path d="M7 8h10v3a5 5 0 0 1-10 0z"/><path d="M12 16v5"/>',
    fuel: '<path d="M5 21V5a2 2 0 0 1 2-2h6a2 2 0 0 1 2 2v16M4 21h12"/><path d="M7 9h6"/><path d="M15 8l3 3v6a2 2 0 0 0 2-2V9.8L17 7"/>',
    angle: '<path d="M4 20h16"/><path d="M4 20 18 6"/><path d="M9 20a5 5 0 0 1 1.5-3.5"/>',
    wave: '<path d="M3 12c2-6 4-6 6 0s4 6 6 0 4-6 6 0"/>',
    arrow: '<path d="M5 12h13M13 6l6 6-6 6"/>',
    wifi: '<path d="M2 8.5a16 16 0 0 1 20 0M5 12a11 11 0 0 1 14 0M8.5 15.5a6 6 0 0 1 7 0"/><circle cx="12" cy="19" r="1" fill="currentColor" stroke="none"/>',
    hash: '<path d="M5 9h14M5 15h14M10 4 8 20M16 4l-2 16"/>'
  };
  global.ITCICON = function (name) {
    var d = P[name] || P.square;
    return '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' + d + '</svg>';
  };
})(window);
