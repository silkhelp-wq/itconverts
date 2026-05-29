/* Karo Convert — payments.js  (window.ITC_PAY)
 * REAL ad-free entitlement, backed by Stripe. Replaces the old "signing in
 * instantly makes you a supporter" mock in supporter.js.
 *
 * Model (the important correction):
 *   - PAYING is what grants ad-free. Signing in does NOT.
 *   - We never trust the browser for supporter status. The flag is always
 *     re-verified against Stripe on the server (verify-session endpoint),
 *     so a user editing localStorage cannot fake ad-free.
 *   - No database required: Stripe Checkout is the source of truth. We store
 *     only the Checkout Session id locally and ask the server "is this paid?".
 *
 * Endpoints it talks to (you deploy these — see /server):
 *   POST {API_BASE}/create-checkout-session   -> { url }      (redirect here)
 *   GET  {API_BASE}/verify-session?session_id= -> { supporter:bool, plan }
 */
(function (g) {
  'use strict';
  var CFG = g.ITC_CONFIG || {};
  var API = (CFG.API_BASE || '').replace(/\/$/, '');     // e.g. "https://api.karoconvert.com" or "/api"
  var SKEY = 'itc-stripe-session';                       // stored Checkout Session id
  var ENTKEY = 'itc-entitlement';                        // cached {supporter, plan, ts} (cache only; server is truth)

  var state = read(ENTKEY, { supporter: false, plan: '' });
  var subs = [];
  function read(k, d) { try { var v = localStorage.getItem(k); return v ? JSON.parse(v) : d; } catch (e) { return d; } }
  function write(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) {} }
  function emit() { for (var i = 0; i < subs.length; i++) { try { subs[i](state); } catch (e) {} } }
  function setState(s) { state = s; write(ENTKEY, s); emit(); }

  function isSupporter() { return !!state.supporter; }
  function plan() { return state.plan || ''; }
  function subscribe(fn) { subs.push(fn); return function () { subs = subs.filter(function (s) { return s !== fn; }); }; }

  /* Step 1 — start a payment. amountCents is an integer (100 = $1.00). */
  function checkout(amountCents, opts) {
    opts = opts || {};
    if (!API) {
      alert('Payments are not configured yet (set ITC_CONFIG.API_BASE and deploy /server). See MONETIZATION.md.');
      return Promise.reject(new Error('no-api'));
    }
    var cents = Math.max(100, Math.round(amountCents || 100)); // Stripe minimum is $0.50; we floor at $1
    return fetch(API + '/create-checkout-session', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        amount: cents,
        // tie an optional identity to the payment so it can sync across devices later
        email: opts.email || null,
        success_url: location.origin + location.pathname + '?paid=1&session_id={CHECKOUT_SESSION_ID}',
        cancel_url: location.origin + location.pathname + '?paid=0'
      })
    })
      .then(function (r) { return r.json(); })
      .then(function (d) {
        if (d && d.url) { location.href = d.url; }      // -> Stripe-hosted checkout (card, Apple Pay, Google Pay)
        else { throw new Error(d && d.error ? d.error : 'checkout-failed'); }
      });
  }

  /* Step 2 — verify a session id against Stripe (server-side check).
     IMPORTANT: a negative result DOWNGRADES the cached state, so a user who
     hand-edits localStorage to supporter:true is corrected on the next load. */
  function verify(sessionId) {
    if (!API || !sessionId) { setState({ supporter: false, plan: '' }); return Promise.resolve(false); }
    return fetch(API + '/verify-session?session_id=' + encodeURIComponent(sessionId))
      .then(function (r) { return r.json(); })
      .then(function (d) {
        if (d && d.supporter) { setState({ supporter: true, plan: d.plan || 'Supporter' }); return true; }
        setState({ supporter: false, plan: '' });
        return false;
      })
      .catch(function () { return false; });   // network blip: keep last good state, don't punish a real supporter
  }

  /* Run on load: (a) handle the redirect back from Stripe, (b) re-verify any
     stored session so ad-free survives reloads but is always server-checked. */
  function init() {
    var qs = new URLSearchParams(location.search);
    if (qs.get('paid') === '1' && qs.get('session_id')) {
      var sid = qs.get('session_id');
      write(SKEY, sid);
      verify(sid).then(function () {
        // clean the URL so a refresh doesn't re-trigger
        history.replaceState({}, '', location.pathname);
      });
      return;
    }
    if (qs.get('paid') === '0') { history.replaceState({}, '', location.pathname); }
    var stored = read(SKEY, null);
    if (stored) { verify(stored); }                 // re-confirm with the server every load
    else { setState({ supporter: false, plan: '' }); } // no payment on record -> no ad-free, period
  }

  function reset() { try { localStorage.removeItem(SKEY); } catch (e) {} setState({ supporter: false, plan: '' }); }

  g.ITC_PAY = {
    isSupporter: isSupporter, plan: plan, subscribe: subscribe,
    checkout: checkout, verify: verify, reset: reset, init: init,
    configured: function () { return !!API; }
  };

  if (document.readyState !== 'loading') init();
  else document.addEventListener('DOMContentLoaded', init);
})(window);
