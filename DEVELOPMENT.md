# Development notes

A record of how itconverts was built and the decisions behind it, so the reasoning
lives with the code.

## Starting point
A high-fidelity design prototype ("Direction C — Bold": warm near-black canvas,
coral accent, Space Grotesk + Inter Tight) of a converter + calculator + an
"AI Study Helper" + a mock "Go ad-free / sign-in" flow. The original design handoff
is kept at `docs/DESIGN-HANDOFF.md`. The goal was to turn it into a real, launchable,
near-zero-cost product that earns via ads + optional donations.

## Key decisions

**Payments — Stripe, not "pay with Google/Apple/Microsoft".**
Those are sign-in (identity) providers, not website payment processors, and the
Apple/Google 15–30% cut applies only to native app-store apps, never to a website.
The donate flow uses **Stripe Checkout** (2.9% + 30¢, no monthly fee), which offers
Apple Pay / Google Pay as payment methods at no extra cost. Stripe is the source of
truth for ad-free status — **no database**: the browser stores only the Checkout
session id and the server re-checks it against Stripe on every load
(`api/verify-session.js`). A hand-edited localStorage flag is rejected because the
server, not the client, decides. (This was a real bug caught in testing: the first
version only *upgraded* to supporter and never downgraded — fixed in `payments.js`.)

**Study search — curated sources, no AI.**
Reframed from an LLM "study helper" (which costs money per query) to a refined search
that returns results **only** from a short allowlist of free, ad-free educational
sources (Wikipedia, Wikibooks, Wiktionary) via the public Wikimedia REST APIs, from
the browser. "Educational, nothing else" is enforced by *where it looks*, not by
judging each query. $0 per query, no API key, multilingual. The general web-search
APIs were ruled out: Google's Custom Search API is closing to new users (retires
Jan 2027), Bing's API shut down in 2025, and Brave dropped its free tier in Feb 2026.
See `study-search.js` (`ALLOW` list is the safety boundary).

**Saved searches — device-local, login-free.**
Stored in the browser (`saved.js`), free for everyone, no accounts. Cross-device sync
would need real accounts + a database (a deliberate later step). This also sidesteps
COPPA/GDPR obligations that would kick in the moment we collected data from minors.

**Ads — AdSense into the existing slot.**
`ads.js` fills the reserved `.promo-area` (kept that non-"ad" class name so ad-blocker
cosmetic filters don't collapse it) and hides it for supporters. The #1 AdSense
rejection reason is "thin content," so we built a real content library (below).

**Content — ~10,000 words, student-focused.**
9 conversion guides + 10 writing/citation guides + 2 hubs + 4 trust/legal pages, all
matching the app's design via `site.css`/`site.js`, with per-page SEO meta, Article +
FAQ structured data, `sitemap.xml` and `robots.txt`. Citation guides reflect the
current editions (APA 7, MLA 9, Chicago 18 — verified against university library
guides) and carry a visible "study aid, not the official manual" note. They cross-link
to the Study search ("find a source, then cite it").

## Testing (run from `dev/` — paths reference the original build sandbox)
- `dev/full.py` — 27 browser checks: study search across sources, HTML-stripped
  snippets, every result links to an educational host, save/persist/re-run, and the
  Stripe pay → verify → ad-free flow incl. the faked-localStorage rejection. (mocks
  Stripe + Wikimedia so it runs without live keys/network.)
- `dev/pages.py` — all 25 content pages: one H1 each, ad slot present, no mobile
  overflow, no JS errors, theme persists, FAQ works, and no broken internal links/assets.
- Plus a Node unit suite for `study-search.js` (allowlist blocks Amazon, random blogs,
  and lookalike domains like `wikipedia.org.evil.com`) and `saved.js`.
- `dev/generate_content_pages.py` — the generator that produced the content pages.

## Known notes
- A couple of original mock-identity bits (`supporter.js`, an inert provider-button
  handler) are still loaded but unused after going login-free; remove when porting to
  a real framework.
- The big result number can wrap on very narrow screens if the Space Grotesk web font
  fails to load; verify with the font served in production.
- At high traffic, proxy + cache the study search through a serverless function
  (Wikimedia asks for a descriptive User-Agent and rate-limits heavy use). Fine to
  launch client-side first.

## Stack
Static HTML/CSS/vanilla JS front end · Vercel serverless (Node) for Stripe · Stripe
Checkout · Wikimedia public APIs · Google AdSense. All on free tiers; only cost is
Stripe's per-transaction fee.
