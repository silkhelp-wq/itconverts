# Karo Convert

A fast, free, mobile-first web app for students:

- **Universal converter** — type "100 km to miles" and get an instant answer (18 categories).
- **Scientific + graphing calculator** — opens in a modal anywhere, or standalone.
- **Study search** — a curated, ad-free educational search (Wikipedia, open textbooks,
  dictionaries) via the free Wikimedia APIs. No AI, no API key, $0 per query.
- **Ad-free** — an optional one-time Stripe donation removes ads (Stripe is the
  source of truth; no accounts, no database).
- **Content library** — ~10,000 words of original conversion + writing/citation guides
  (SEO + the basis for AdSense approval).

It's a **static site** (the tools run entirely in the browser) plus three small
**Vercel serverless functions** in `/api` for the Stripe checkout. Everything runs
on free tiers; the only cost is Stripe's per-transaction fee.

## Structure
```
index.html                     # the app (converter + calculator launcher + study search)
calculator.html                # scientific/graphing calculator
*.js                           # convert, mathcore, icons, study-search, saved, payments, ads, supporter, calc-modal
site.css / site.js             # shared chrome for the content pages
about/privacy/terms/contact.html
guides/                        # 9 conversion guides + hub
writing/                       # 10 writing & citation guides + hub
sitemap.xml / robots.txt
api/                           # Vercel serverless: create-checkout-session, verify-session, webhook
server-alternative-cloudflare/ # the same endpoints as one Cloudflare Worker (if you prefer CF)
package.json / vercel.json     # deploy config (stripe dependency for the functions)
.env.example                   # which env vars to set (set them in Vercel, not in a file)
MONETIZATION.md                # the full plan: ads, payments, hosting, launch checklist
DEVELOPMENT.md                 # how this was built + key decisions + test results
dev/                           # the content generator + the automated test harness (record)
```

## Deploy (Vercel — recommended)
1. Push this repo to GitHub (see the commands you were given, or below).
2. Import the repo at vercel.com (free Hobby plan). It deploys as a static site
   and turns `/api/*.js` into serverless functions automatically.
3. Add a custom domain in Vercel (free HTTPS).
4. Create a Stripe account, then in Vercel → Settings → Environment Variables set
   `STRIPE_SECRET_KEY` (start with the `sk_test_…` key).
5. In `index.html`, set `ITC_CONFIG.API_BASE = "/api"`. Test the donate flow with
   card `4242 4242 4242 4242`, then switch to live Stripe keys.
6. Submit `sitemap.xml` in Google Search Console; apply to AdSense once live; paste
   `ADSENSE_CLIENT` + `ADSENSE_SLOT` into `ITC_CONFIG` when approved.

Full step-by-step (and the honest revenue math) is in **MONETIZATION.md**.

## Before you publish — edit these placeholders
- `SITE` domain in `sitemap.xml` and `robots.txt` (currently `karoconvert.com`).
- Contact email in `contact.html`.
- Owner name + "Last updated" date in `privacy.html` and `terms.html`.
- The privacy/terms pages are starting templates, **not legal advice** — review for
  your jurisdiction, and enable an AdSense consent banner for EEA/UK visitors.

## Local preview (optional)
Any static server works for the front end, e.g.:
```bash
python3 -m http.server 8000      # then open http://localhost:8000
```
To test the Stripe functions locally you'd use the Vercel CLI: `npx vercel dev`.
