/* Karo Convert — supporter.js
 * Lightweight identity + supporter state + activity history, persisted to
 * localStorage so it survives reloads and is shared across same-origin pages
 * (main site + calculator iframe). This is a front-end MOCK of social sign-in;
 * production would verify the OAuth token and payment server-side.
 * Exposes window.ITC_USER.
 */
(function (g) {
  'use strict';
  var UKEY = 'itc-user', HKEY = 'itc-history';
  function read(k, def) { try { var v = localStorage.getItem(k); return v ? JSON.parse(v) : def; } catch (e) { return def; } }
  function write(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) {} }

  var subs = [];
  function emit() { var u = current(); for (var i = 0; i < subs.length; i++) { try { subs[i](u); } catch (e) {} } }

  function current() { return read(UKEY, null); }
  function isSupporter() { var u = current(); return !!(u && u.supporter); }

  var PROV = {
    google: { name: 'Google', email: 'gmail.com', color: '#e2533b' },
    apple: { name: 'Apple', email: 'icloud.com', color: '#8a8f98' },
    microsoft: { name: 'Microsoft', email: 'outlook.com', color: '#3b82c4' }
  };

  function signIn(provider, opts) {
    opts = opts || {};
    var p = PROV[provider] || { name: provider, email: 'example.com' };
    var u = {
      provider: provider,
      providerName: p.name,
      name: opts.name || 'Member',
      email: opts.email || ('member@' + p.email),
      supporter: true,
      plan: opts.plan || 'Supporter',
      since: Date.now()
    };
    write(UKEY, u); emit(); return u;
  }
  function signOut() { try { localStorage.removeItem(UKEY); } catch (e) {} emit(); }

  function log(entry) {
    if (!isSupporter() || !entry) return;
    var h = read(HKEY, []);
    var last = h[0];
    if (last && last.t === entry.t && last.label === entry.label) return; // dedupe consecutive
    h.unshift({ t: entry.t, label: entry.label, detail: entry.detail || '', ts: Date.now() });
    if (h.length > 200) h = h.slice(0, 200);
    write(HKEY, h); emit();
  }
  function history() { return read(HKEY, []); }
  function clearHistory() { write(HKEY, []); emit(); }

  function subscribe(fn) { subs.push(fn); return function () { subs = subs.filter(function (s) { return s !== fn; }); }; }

  // keep tabs / iframe in sync
  if (g.addEventListener) g.addEventListener('storage', function (e) { if (e.key === UKEY || e.key === HKEY) emit(); });

  g.ITC_USER = {
    current: current, isSupporter: isSupporter, signIn: signIn, signOut: signOut,
    log: log, history: history, clearHistory: clearHistory, subscribe: subscribe, providers: PROV
  };
})(window);
