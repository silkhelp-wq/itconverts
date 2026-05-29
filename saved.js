/* Karo Convert — saved.js   (window.ITC_SAVED)
 * Device-local "save this search for later". No account, no server, no cost —
 * stored in this browser only (localStorage). Available to EVERYONE, signed in
 * or not, donor or not. (Cross-device sync would need real accounts + a database;
 * that's a deliberate later step.)
 */
(function (g) {
  'use strict';
  var KEY = 'itc-saved-searches';
  var subs = [];
  function read() { try { var v = localStorage.getItem(KEY); return v ? JSON.parse(v) : []; } catch (e) { return []; } }
  function write(v) { try { localStorage.setItem(KEY, JSON.stringify(v)); } catch (e) {} emit(); }
  function emit() { var l = list(); for (var i = 0; i < subs.length; i++) { try { subs[i](l); } catch (e) {} } }

  function idOf(query, lang) { return (String(query).trim().toLowerCase()) + '|' + (lang || 'en'); }
  function list() { return read(); }
  function has(query, lang) { var id = idOf(query, lang); return read().some(function (e) { return e.id === id; }); }

  function add(entry) {
    entry = entry || {};
    var q = String(entry.query || '').trim(); if (!q) return null;
    var lang = entry.lang || 'en';
    var id = idOf(q, lang);
    var arr = read().filter(function (e) { return e.id !== id; }); // de-dupe; move to top
    var rec = { id: id, query: q, lang: lang, ts: Date.now() };
    arr.unshift(rec);
    if (arr.length > 100) arr = arr.slice(0, 100);
    write(arr);
    return rec;
  }
  function toggle(entry) { var lang = (entry && entry.lang) || 'en'; if (has(entry.query, lang)) { remove(idOf(entry.query, lang)); return false; } add(entry); return true; }
  function remove(id) { write(read().filter(function (e) { return e.id !== id; })); }
  function clear() { write([]); }
  function subscribe(fn) { subs.push(fn); return function () { subs = subs.filter(function (s) { return s !== fn; }); }; }

  if (g.addEventListener) g.addEventListener('storage', function (e) { if (e.key === KEY) emit(); });

  g.ITC_SAVED = { list: list, has: has, add: add, toggle: toggle, remove: remove, clear: clear, subscribe: subscribe };
})(window);
