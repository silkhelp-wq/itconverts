// server/vercel/api/webhook.js
// OPTIONAL. The ad-free gate works without this (verify-session covers it).
// A webhook is the right place to: record each donation, email a receipt,
// or — if you add real accounts later — write a per-user entitlement row.
//
// Stripe signs webhooks; we verify the signature against the RAW body, so
// disable Vercel's body parser for this route.

const Stripe = require('stripe');
const stripe = new Stripe(process.env.STRIPE_SECRET_KEY);

module.exports.config = { api: { bodyParser: false } };

function readRaw(req) {
  return new Promise((resolve, reject) => {
    let data = '';
    req.on('data', (c) => (data += c));
    req.on('end', () => resolve(data));
    req.on('error', reject);
  });
}

module.exports = async function handler(req, res) {
  if (req.method !== 'POST') return res.status(405).end();
  const sig = req.headers['stripe-signature'];
  let event;
  try {
    const raw = await readRaw(req);
    event = stripe.webhooks.constructEvent(raw, sig, process.env.STRIPE_WEBHOOK_SECRET);
  } catch (err) {
    console.error('Webhook signature verification failed:', err.message);
    return res.status(400).send(`Webhook Error: ${err.message}`);
  }

  if (event.type === 'checkout.session.completed') {
    const session = event.data.object;
    // e.g. save { email: session.customer_details?.email, amount: session.amount_total, id: session.id }
    console.log('✅ ad-free purchased:', session.id, session.amount_total);
    // TODO (only if/when you add accounts): upsert entitlement keyed by email/user.
  }

  return res.status(200).json({ received: true });
};
