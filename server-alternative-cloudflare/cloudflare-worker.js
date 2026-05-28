// server/cloudflare-worker.js
// Alternative to the Vercel functions: ONE Cloudflare Worker that handles
// /create-checkout-session, /verify-session and /webhook.
// Cloudflare's free tier (100k requests/day) is plenty for a donation flow.
//
// Set secrets:  wrangler secret put STRIPE_SECRET_KEY
//               wrangler secret put STRIPE_WEBHOOK_SECRET   (only if you use the webhook)
//
// Uses Stripe's REST API via fetch (no Node SDK needed in Workers).

const STRIPE_API = 'https://api.stripe.com/v1';

function form(obj, prefix, out) {
  out = out || new URLSearchParams();
  for (const k in obj) {
    const key = prefix ? `${prefix}[${k}]` : k;
    const v = obj[k];
    if (v === undefined || v === null) continue;
    if (typeof v === 'object') form(v, key, out);
    else out.append(key, String(v));
  }
  return out;
}

async function stripe(env, path, params, method = 'POST') {
  const init = {
    method,
    headers: {
      'Authorization': 'Bearer ' + env.STRIPE_SECRET_KEY,
      'Content-Type': 'application/x-www-form-urlencoded'
    }
  };
  if (params && method === 'POST') init.body = form(params).toString();
  const r = await fetch(STRIPE_API + path, init);
  return r.json();
}

function cors(env) {
  return {
    'Access-Control-Allow-Origin': env.ALLOWED_ORIGIN || '*',
    'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type'
  };
}
const json = (data, env, status = 200) =>
  new Response(JSON.stringify(data), { status, headers: { 'Content-Type': 'application/json', ...cors(env) } });

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (request.method === 'OPTIONS') return new Response(null, { status: 204, headers: cors(env) });

    // POST /create-checkout-session
    if (url.pathname.endsWith('/create-checkout-session') && request.method === 'POST') {
      const body = await request.json().catch(() => ({}));
      let amount = parseInt(body.amount, 10);
      if (!Number.isFinite(amount)) amount = 100;
      amount = Math.max(100, Math.min(amount, 100000));
      const session = await stripe(env, '/checkout/sessions', {
        mode: 'payment',
        'line_items': [{
          quantity: 1,
          price_data: {
            currency: 'usd',
            unit_amount: amount,
            product_data: { name: 'itconverts — Go ad-free' }
          }
        }],
        customer_email: body.email || undefined,
        success_url: body.success_url || (url.origin + '/?paid=1&session_id={CHECKOUT_SESSION_ID}'),
        cancel_url: body.cancel_url || (url.origin + '/?paid=0'),
        'metadata[product]': 'itconverts-adfree'
      });
      if (session && session.url) return json({ url: session.url, id: session.id }, env);
      return json({ error: 'could-not-create-session' }, env, 500);
    }

    // GET /verify-session?session_id=...
    if (url.pathname.endsWith('/verify-session') && request.method === 'GET') {
      const sid = url.searchParams.get('session_id');
      if (!sid) return json({ supporter: false }, env, 400);
      const s = await stripe(env, '/checkout/sessions/' + encodeURIComponent(sid), null, 'GET');
      const paid = s && s.payment_status === 'paid';
      const dollars = s && s.amount_total ? s.amount_total / 100 : 0;
      return json({ supporter: !!paid, plan: paid ? ('$' + dollars + ' supporter') : '' }, env);
    }

    // POST /webhook  (optional). Verifying Stripe's signature in Workers needs
    // Web Crypto HMAC; see MONETIZATION.md. Returning 200 here as a stub.
    if (url.pathname.endsWith('/webhook') && request.method === 'POST') {
      return json({ received: true }, env);
    }

    return json({ error: 'not-found' }, env, 404);
  }
};
