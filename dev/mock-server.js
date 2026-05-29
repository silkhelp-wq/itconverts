// test/mock-server.js — serves the build + a fake Stripe API so we can drive
// the REAL client flow (create session -> redirect -> verify -> ad-free) without
// live keys. The only thing NOT exercised is Stripe's own hosted page (their UI).
const http = require('http');
const fs = require('fs');
const path = require('path');
const url = require('url');

const ROOT = path.join(__dirname, '..');           // Karo Convert-build/
const PAID_ID = 'cs_test_mock_123';                  // pretend this session is paid
const TYPES = { '.html':'text/html', '.js':'text/javascript', '.css':'text/css' };

function send(res, code, body, type) {
  res.writeHead(code, { 'Content-Type': type || 'text/plain', 'Access-Control-Allow-Origin': '*' });
  res.end(body);
}

const server = http.createServer((req, res) => {
  const u = url.parse(req.url, true);

  // --- fake Stripe API ---
  if (u.pathname === '/api/create-checkout-session' && req.method === 'POST') {
    let body = ''; req.on('data', c => body += c); req.on('end', () => {
      let success = 'http://localhost:%PORT%/?paid=1&session_id={CHECKOUT_SESSION_ID}';
      try { const j = JSON.parse(body || '{}'); if (j.success_url) success = j.success_url; } catch (e) {}
      // simulate Stripe substituting the real session id, then redirecting back
      const redirect = success.replace('{CHECKOUT_SESSION_ID}', PAID_ID);
      send(res, 200, JSON.stringify({ url: redirect, id: PAID_ID }), 'application/json');
    });
    return;
  }
  if (u.pathname === '/api/verify-session' && req.method === 'GET') {
    const paid = u.query.session_id === PAID_ID;
    send(res, 200, JSON.stringify({ supporter: paid, plan: paid ? '$1 supporter' : '' }), 'application/json');
    return;
  }

  // --- static files ---
  let p = u.pathname === '/' ? '/Karo Convert.html' : u.pathname;
  const fp = path.join(ROOT, p);
  if (!fp.startsWith(ROOT) || !fs.existsSync(fp)) return send(res, 404, 'not found');
  let data = fs.readFileSync(fp);
  const ext = path.extname(fp);
  if (ext === '.html') {
    // inject the test API base so the client talks to our fake Stripe
    data = data.toString().replace('API_BASE:       ""', 'API_BASE: "/api"');
  }
  send(res, 200, data, TYPES[ext] || 'application/octet-stream');
});

const PORT = process.env.PORT || 8799;
server.listen(PORT, () => console.log('mock server on http://localhost:' + PORT));
