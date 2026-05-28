# itconverts — monetization & launch guide

This folder is the **prototype with real monetization wired in**. It's still the
plain HTML/CSS/JS design bundle (per the original README, you'd rebuild this in
your real framework eventually) — but the money parts now work and are tested.

## The three decisions we locked in
1. **Study search = curated sources only.** No AI. Results come *only* from a
   short allowlist of free, ad-free educational sites (Wikipedia, Wikibooks,
   Wiktionary). "Educational, nothing else" is enforced by *where we look*, not
   by judging each query. Cost: **$0** (runs in the browser, no API key).
2. **Ad-free = Stripe.** Paying removes ads. Stripe is the source of truth, so
   there's **no database** and **no account** required. Apple Pay / Google Pay
   come free inside Stripe Checkout.
3. **Saved searches = device-local.** Stored in the browser (localStorage), free
   for everyone, no login. Cross-device sync is a deliberate later step.

## Recommended launch path (the simplest way to go live)
**This repo is already in Vercel layout** — the app is `index.html` at the root and
the Stripe functions are in `/api`, so one free deploy serves the static site *and*
the functions on the same domain (`API_BASE` is just `"/api"`, no CORS to configure).

Do it in this order:
1. **Push this repo to GitHub** (commands are in the chat / `git` below).
2. **Import the repo into Vercel** (free Hobby plan) → it deploys in a minute and
   turns `/api/*.js` into serverless functions automatically. You get a live
   `*.vercel.app` URL. Add your custom domain when ready (free HTTPS).
3. **Add a Stripe account**, copy the test secret key, and set `STRIPE_SECRET_KEY`
   in Vercel → Settings → Environment Variables. Then set `ITC_CONFIG.API_BASE = "/api"`
   in `index.html`. Test the donate flow with card `4242 4242 4242 4242`, then switch
   to live keys.
4. **Submit `sitemap.xml` in Google Search Console** and let the ~10k words of guides
   get indexed (this is what brings the search traffic that ads monetise).
5. **Apply to AdSense** once the site is live with content and the legal pages. When
   approved, paste `ADSENSE_CLIENT` + `ADSENSE_SLOT` into `ITC_CONFIG`.

The Study search needs nothing — it already works from the browser.

*Alternative:* **Cloudflare Pages + Workers** (use
`server-alternative-cloudflare/cloudflare-worker.js`) is slightly cheaper at very high
scale with a faster CDN, but it's a bit more wiring. Vercel is the easier start.

## New / changed files
| File | What it does |
|---|---|
| `study-search.js` | Curated Wikimedia search + the host allowlist (the safety boundary). |
| `saved.js` | Device-local saved-searches store. |
| `payments.js` | Stripe checkout + verified ad-free entitlement (`ITC_PAY`). |
| `ads.js` | Drops AdSense into the existing slot; hides it for supporters. |
| `index.html` | The app (was itconverts.html): converter, calculator launcher, study search, payment wiring, donate modal. |
| `api/` | Stripe serverless endpoints (Vercel functions): create-checkout-session, verify-session, webhook. |
| `server-alternative-cloudflare/` | The same endpoints as one Cloudflare Worker (only if you choose Cloudflare). |
| `dev/` | The content generator + automated test harness (record — see DEVELOPMENT.md). |

Everything is driven by one config block at the top of `index.html`:
```js
window.ITC_CONFIG = { ADSENSE_CLIENT:"", ADSENSE_SLOT:"", API_BASE:"" /* , STUDY_LANG:"en" */ };
```
Empty fields = that feature stays in safe placeholder mode. The study search
works with all fields empty.

## How ads make money (and the honest numbers)
Ads pay per 1,000 pageviews (RPM). A bare converter is a **low-RPM, high-bounce**
profile — general utility sites realistically earn **~$0.20–$2.50 per 1,000
pageviews**. So this is a **volume game**: at ~$2 RPM, 100k pageviews ≈ ~$200/mo;
1M ≈ ~$2,000/mo. Converters *can* pull big search traffic, so it's viable — but
not from a small audience.

Two things to plan around:
- **AdSense's #1 rejection reason is "thin / low-value content."** A tool with no
  written content usually gets rejected. Add ~5–10 supporting pages (conversion
  guides, unit explainers) + Privacy / About / Contact before applying.
- **$1 donations lose ~33% to Stripe's 30¢ fixed fee.** Consider defaulting the
  donate amount to **$3**.

## Setup — going live (all tiers free except per-transaction Stripe fees)

### 1) Host the static site ($0)
Push this folder to **Cloudflare Pages**, **Netlify**, or **Vercel**. The
converter, calculator, and study search are all client-side, so hosting is free.

### 2) Stripe (ad-free payments)
1. Create a Stripe account; copy your **test** keys (`sk_test_…`) from the dashboard.
2. Stripe functions (in `/api`):
   - **Vercel (already wired):** the functions are in `/api`. Just set env
     `STRIPE_SECRET_KEY` in the Vercel dashboard; they deploy with the repo at
     `/api/create-checkout-session`, `/api/verify-session`, `/api/webhook`.
   - **Cloudflare Worker (alt):** deploy `server-alternative-cloudflare/cloudflare-worker.js`;
     `wrangler secret put STRIPE_SECRET_KEY`.
3. In `index.html`, set `ITC_CONFIG.API_BASE = "/api"` (the functions are on the
   same Vercel project, so a same-origin path is all you need).
4. In the Stripe Dashboard → Payment methods, **enable Google Pay** (Apple Pay is
   on by default). Test with card `4242 4242 4242 4242`.
5. Flip to live keys when ready. (Webhook is optional — `verify-session` already
   gates ad-free; add the webhook later if you want receipts/records.)

### 3) AdSense (display ads)
1. You need a **real, live domain** and to be **18+**.
2. Add the supporting content + legal pages mentioned above.
3. Apply at adsense.google.com (review: 24h–2 weeks; can be rejected for thin
   content). Once approved, create an ad unit.
4. Paste `ADSENSE_CLIENT` (`ca-pub-…`) and `ADSENSE_SLOT` into `ITC_CONFIG`. Ads
   appear in the reserved slot and auto-hide for supporters.

> **Content pages are now built** (the thin-content fix). See "Content pages" below.

## Content pages (the thin-content fix — now a full library)
The site now ships **25 pages of original content (~10,000 words)**, so it reads as
a real publication, not a bare tool:

- **Trust/legal:** `about.html`, `privacy.html`, `terms.html`, `contact.html`
- **Conversion guides** (`guides/`): a hub + **9 guides** — km↔miles, °C↔°F, kg↔lb,
  meters↔feet, inches↔cm, liters↔gallons, grams↔ounces, data units (decimal vs
  binary, bits vs bytes), cups↔ml. Each has the formula, worked examples, a
  reference table and an FAQ.
- **Writing & citation guides** (`writing/`): a hub + **10 guides** aimed at
  students writing essays, term papers and theses — APA/MLA/Chicago/Harvard
  compared, how to cite a website / Wikipedia / book / journal article,
  bibliography vs Works Cited vs References, thesis statements, structuring a
  paper, avoiding plagiarism, and evaluating sources. Reflects the **current
  editions (APA 7, MLA 9, Chicago 18)**, verified against university library
  guides. These cross-link to the Study search ("find a source, then cite it").
- **SEO:** `site.css` + `site.js` (shared chrome, theme), per-page titles/meta/
  canonical/Open Graph, Article + FAQ structured data, `sitemap.xml`, `robots.txt`.

Every page carries the same header (Converter · Guides · Writing) and footer, the
reserved ad slot, and respects ad-free (loads `payments.js` + `ads.js`). All 25
pages are tested: one H1 each, no JS errors, no mobile overflow, working theme +
FAQs, and **no broken internal links or assets**.

> The citation guides are a study aid and say so on every page — they're not a
> substitute for the official manuals, and each tells students to follow their
> brief / instructor. Good practice, and it keeps the content trustworthy.

**Before you publish, edit these placeholders:**
- `SITE` domain in `sitemap.xml` and `robots.txt` (currently `itconverts.example`).
- Contact email in `contact.html` (and the `mailto:` link).
- Owner name + "Last updated" date in `privacy.html` and `terms.html`.
- The privacy/terms text is a **starting template, not legal advice** — review it
  for your jurisdiction (and add a consent banner via AdSense if you serve EEA/UK).
- Already done: the app is `index.html` at the root and all internal links point to it.

### 4) Study search
Works out of the box — no key, no server. It calls Wikimedia's public REST API
from the browser. Set `STUDY_LANG` for a different default language; the in-page
picker covers 12 languages.
- **Scale caveat:** Wikimedia asks for a descriptive `User-Agent` and rate-limits
  heavy use. Browsers can't set `User-Agent`, so for high traffic, proxy the
  search through a tiny serverless function (same pattern as `/api`) that adds
  the header and caches popular queries. Fine to launch client-side first.
- **Add sources later:** extend the `SOURCES` array in `study-search.js`
  (Wikiversity, Wikisource, etc.) and the `ALLOW` list.

## Test status (run: `python3 test/full.py` and `node` the unit script)
- ✅ **Converter / calculator / theme / mobile** — 14 checks (original prototype).
- ✅ **Study search + saved searches** — 27 browser checks: rename, language
  picker, curated results across 3 sources, HTML-stripped snippets, *every result
  links to an educational host*, save/persist/re-run, plus the security check that
  a faked `localStorage` supporter flag is rejected server-side.
- ✅ **Study-search logic** — 28 unit checks incl. allowlist blocks Amazon, random
  blogs, and lookalike domains (`wikipedia.org.evil.com`).
- ⚠️ **Not exercisable here:** live AdSense fill (needs approval + domain), a real
  Stripe charge (needs live keys + Stripe's hosted page), and live Wikimedia calls
  (blocked in the build sandbox — mocked in tests). The *code paths* around all
  three are tested with mocks.

## Launch checklist
- [ ] Pick fastest-dollar (donations only, skip AdSense) **or** ad-revenue (content is ready → apply).
- [ ] Buy a domain; deploy this folder to Cloudflare Pages / Vercel / Netlify (HTTPS).
- [x] Repo is in Vercel layout — `index.html` at root, functions in `/api`. **Done.**
- [ ] Stripe: create account → set `STRIPE_SECRET_KEY` in Vercel → set `API_BASE="/api"` → enable Google Pay → test `4242…` → go live.
- [ ] Change donate default to $3 (edit the `$1` plan button) to beat the fixed fee.
- [x] Privacy / About / Terms / Contact pages — **built** (fill in email, owner, dates).
- [x] Supporting content for AdSense — **built**: 9 conversion guides + 10 writing/citation guides + 2 hubs (~10k words).
- [ ] Set your real domain in `sitemap.xml` + `robots.txt`; submit sitemap in Google Search Console.
- [ ] (Ad path) Apply to AdSense → paste `ADSENSE_CLIENT` / `ADSENSE_SLOT`.
- [ ] (If you add accounts later) revisit COPPA/GDPR before collecting any data from minors.
- [ ] Decide if/when to proxy + cache the study search (only needed at scale).

## Notes
- The header "Go ad-free" button shows as an icon only on screens ≤430px (by design).
- A couple of bits of the original mock identity code (`supporter.js`, an empty
  provider-button handler) are still loaded but inert — harmless; remove when you
  port to your real framework.
- The big result number can wrap on very narrow screens **when the Space Grotesk
  web font fails to load**; verify once the font is served in production.
