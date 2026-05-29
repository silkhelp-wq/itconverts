/* Karo Convert — calc-modal.js
 * Injects a shared "Calculator" modal that embeds calculator.html in an iframe.
 * Any element with [data-open-calc] opens it. Esc / backdrop / close button dismiss.
 * Self-contained; no dependencies. Inherits each page's --accent if present. */
(function () {
  'use strict';
  if (window.__itcCalcModal) return; window.__itcCalcModal = true;

  var css = ''
    + '.itc-calc-ov{position:fixed;inset:0;z-index:9999;display:none;align-items:center;justify-content:center;'
    + 'background:rgba(8,9,12,.62);backdrop-filter:blur(4px);padding:24px}'
    + '.itc-calc-ov.on{display:flex;animation:itcfade .18s ease}'
    + '@keyframes itcfade{from{opacity:0}to{opacity:1}}'
    + '.itc-calc-sheet{position:relative;width:100%;max-width:440px;height:min(94vh,720px);transition:height .26s cubic-bezier(.2,.7,.3,1);'
    + 'background:#14110d;border-radius:20px;overflow:hidden;box-shadow:0 30px 80px rgba(0,0,0,.5);'
    + 'border:1px solid rgba(255,255,255,.08);animation:itcrise .22s cubic-bezier(.2,.7,.3,1)}'
    + '@keyframes itcrise{from{transform:translateY(14px)}to{transform:none}}'
    + '.itc-calc-sheet iframe{width:100%;height:100%;border:0;display:block;background:#14110d}'
    + '.itc-calc-sheet.graph{height:min(96vh,896px)}'
    + '.itc-calc-x{position:absolute;top:12px;right:12px;z-index:2;width:38px;height:38px;border-radius:11px;'
    + 'border:1px solid rgba(255,255,255,.16);background:rgba(20,24,30,.9);color:#e8eef5;cursor:pointer;'
    + 'display:flex;align-items:center;justify-content:center;font-size:20px;line-height:1}'
    + '.itc-calc-x:hover{background:rgba(40,46,56,.95)}'
    + '@media (max-width:520px){.itc-calc-ov{padding:0}.itc-calc-sheet{max-width:none;height:100vh;height:100dvh;border-radius:0;border:0}}';
  var st = document.createElement('style'); st.textContent = css; document.head.appendChild(st);

  var ov = document.createElement('div'); ov.className = 'itc-calc-ov'; ov.setAttribute('role', 'dialog'); ov.setAttribute('aria-label', 'Calculator');
  ov.innerHTML = '<div class="itc-calc-sheet"><button class="itc-calc-x" aria-label="Close calculator">\u2715</button></div>';
  var sheet = ov.querySelector('.itc-calc-sheet');
  var iframe = null;

  function open() {
    if (!iframe) { iframe = document.createElement('iframe'); iframe.title = 'Karo Convert calculator'; iframe.src = 'calculator.html'; sheet.appendChild(iframe); }
    ov.classList.add('on'); document.body.style.overflow = 'hidden';
  }
  function close() { ov.classList.remove('on'); document.body.style.overflow = ''; }

  ov.addEventListener('click', function (e) { if (e.target === ov) close(); });
  ov.querySelector('.itc-calc-x').addEventListener('click', close);
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && ov.classList.contains('on')) close(); });
  // calculator tells us which tab it's on so we can grow the modal for graphing
  window.addEventListener('message', function (e) { var d = e && e.data; if (d && d.type === 'itc-calc-mode') { sheet.classList.toggle('graph', d.mode === 'graph'); } });

  function wire() {
    var els = document.querySelectorAll('[data-open-calc]');
    for (var i = 0; i < els.length; i++) {
      if (els[i].__itcWired) continue; els[i].__itcWired = true;
      els[i].addEventListener('click', function (e) { e.preventDefault(); open(); });
    }
  }
  if (document.body) { document.body.appendChild(ov); wire(); }
  else { document.addEventListener('DOMContentLoaded', function () { document.body.appendChild(ov); wire(); }); }
  window.itcOpenCalc = open;
})();
