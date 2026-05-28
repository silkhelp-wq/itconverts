// server/vercel/api/verify-session.js
// Server-side check: "is this Checkout Session actually paid?"
// The browser stores only the session id and asks here on every load.
// Because the answer comes from Stripe (not the client), a user editing
// localStorage CANNOT fake ad-free. No database required — Stripe is truth.

const Stripe = require('stripe');
const stripe = new Stripe(process.env.STRIPE_SECRET_KEY);

const ALLOWED_ORIGIN = process.env.ALLOWED_ORIGIN || '*';

module.exports = async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', ALLOWED_ORIGIN);
  res.setHeader('Cache-Control', 'no-store');
  if (req.method === 'OPTIONS') return res.status(204).end();

  const sessionId = (req.query && req.query.session_id) || '';
  if (!sessionId) return res.status(400).json({ supporter: false, error: 'missing-session-id' });

  try {
    const session = await stripe.checkout.sessions.retrieve(sessionId);
    const paid = !!session && session.payment_status === 'paid';
    const dollars = session && session.amount_total ? (session.amount_total / 100) : 0;
    return res.status(200).json({
      supporter: paid,
      plan: paid ? ('$' + dollars + ' supporter') : ''
    });
  } catch (err) {
    // Unknown/invalid id -> not a supporter (don't leak details).
    return res.status(200).json({ supporter: false, plan: '' });
  }
};
