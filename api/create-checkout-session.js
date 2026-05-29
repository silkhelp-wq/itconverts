// server/vercel/api/create-checkout-session.js
// Creates a Stripe Checkout Session for a one-time "Go ad-free" donation.
// The amount is dynamic ($1 preset or a custom amount the user typed).
// Stripe's hosted page automatically offers card + Apple Pay + Google Pay
// (enable Google Pay once in your Stripe Dashboard; Apple Pay is on by default).
//
// Free to run on Vercel's Hobby tier. Set STRIPE_SECRET_KEY in env.

const Stripe = require('stripe');
const stripe = new Stripe(process.env.STRIPE_SECRET_KEY);

const ALLOWED_ORIGIN = process.env.ALLOWED_ORIGIN || '*';

module.exports = async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', ALLOWED_ORIGIN);
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  if (req.method === 'OPTIONS') return res.status(204).end();
  if (req.method !== 'POST') return res.status(405).json({ error: 'method-not-allowed' });

  try {
    const body = typeof req.body === 'string' ? JSON.parse(req.body || '{}') : (req.body || {});
    // Validate amount server-side. Never trust the client number blindly.
    let amount = parseInt(body.amount, 10);
    if (!Number.isFinite(amount)) amount = 100;
    amount = Math.max(100, Math.min(amount, 100000)); // clamp $1 .. $1,000

    const session = await stripe.checkout.sessions.create({
      mode: 'payment',
      // Omitting payment_method_types lets Stripe present every method you've
      // enabled in the Dashboard (card, Apple Pay, Google Pay, Link, …).
      line_items: [{
        quantity: 1,
        price_data: {
          currency: 'usd',
          unit_amount: amount,
          product_data: {
            name: 'Karo Convert — Go ad-free',
            description: 'Removes ads and unlocks saved history. Thank you for supporting a free tool.'
          }
        }
      }],
      customer_email: body.email || undefined,
      // {CHECKOUT_SESSION_ID} is substituted by Stripe on redirect.
      success_url: body.success_url || 'https://example.com/?paid=1&session_id={CHECKOUT_SESSION_ID}',
      cancel_url: body.cancel_url || 'https://example.com/?paid=0',
      metadata: { product: 'Karo Convert-adfree' }
    });

    return res.status(200).json({ url: session.url, id: session.id });
  } catch (err) {
    console.error('create-checkout-session error:', err);
    return res.status(500).json({ error: 'could-not-create-session' });
  }
};
