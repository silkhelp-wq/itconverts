#!/usr/bin/env python3
# build_pages.py — authoring tool (NOT a runtime dep). Emits plain static HTML
# pages into Karo Convert-build/ and Karo Convert-build/guides/.
import os, json, html
OUT = "/home/claude/Karo Convert-build"
SITE = "https://karoconvert.com"   # <-- replace with your real domain before deploy

def assets(depth):  # relative prefix from page to root
    return "../" * depth

def head(title, desc, depth, canonical, extra=""):
    p = assets(depth)
    return f"""<!DOCTYPE html>
<html lang="en" data-theme="dark">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="website">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="{canonical}">
<meta name="robots" content="index,follow">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Inter+Tight:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{p}site.css">
<script>window.ITC_CONFIG={{ADSENSE_CLIENT:"",ADSENSE_SLOT:"",API_BASE:""}};</script>
{extra}</head>
<body>"""

def header(depth, active=""):
    p = assets(depth)
    def cls(name): return "navlink active" if name == active else "navlink"
    return f"""<header><div class="hwrap">
  <a class="brand" href="{p}Karo Convert.html"><span class="b">⇄</span> Karo <em>Convert</em></a>
  <nav class="hnav">
    <a class="{cls('converter')}" href="{p}Karo Convert.html"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M7 10l-3 3 3 3M4 13h13M17 14l3-3-3-3M20 11H7"/></svg><span class="lbl">Converter</span></a>
    <a class="{cls('guides')}" href="{p}guides/"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><path d="M4 5h11a3 3 0 0 1 3 3v11a2 2 0 0 0-2-2H4z"/><path d="M20 5h-1a3 3 0 0 0-3 3v11"/></svg><span class="lbl">Guides</span></a>
    <a class="{cls('writing')}" href="{p}writing/"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><path d="M12 20h9"/><path d="M16.5 3.5a2.1 2.1 0 0 1 3 3L7 19l-4 1 1-4z"/></svg><span class="lbl">Writing</span></a>
    <button class="tbtn" id="theme" aria-label="Toggle theme"></button>
  </nav>
</div></header>"""

def promo():
    return """<div class="promo-area"><div class="promo-unit" id="promo"><div class="tag">Advertisement</div><div class="ph">Reserved slot — slim, labeled, and out of the way.</div></div></div>"""

def footer(depth):
    p = assets(depth)
    return f"""{promo()}
<footer><div class="footcol">
  <div class="footlinks">
    <a href="{p}Karo Convert.html">Converter</a>
    <a href="{p}guides/">Conversion guides</a>
    <a href="{p}about.html">About</a>
    <a href="{p}privacy.html">Privacy</a>
    <a href="{p}terms.html">Terms</a>
    <a href="{p}contact.html">Contact</a>
  </div>
  <div class="footnote">© <span id="yr"></span> Karo Convert — type anything, convert everything. A free tool for students everywhere. Karo Convert is not affiliated with the Wikimedia Foundation; study results link to Wikimedia projects under their respective licenses.</div>
</div></footer>
<script src="{p}payments.js"></script>
<script src="{p}ads.js"></script>
<script src="{p}site.js"></script>
</body></html>"""

def write(relpath, title, desc, body, depth, extra_head=""):
    canonical = f"{SITE}/{relpath}"
    doc = head(title, desc, depth, canonical, extra_head) + header(depth, ACTIVE.get(relpath, "")) + "\n<main><div class=\"wrap\">\n" + body + "\n</div></main>\n" + footer(depth)
    full = os.path.join(OUT, relpath)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, "w", encoding="utf-8").write(doc)
    print("wrote", relpath, f"({len(body)} chars body)")

ACTIVE = {"guides/index.html": "guides"}
def crumb(items):  # [(label, href|None)]
    parts = []
    for label, href in items:
        parts.append(f'<a href="{href}">{html.escape(label)}</a>' if href else html.escape(label))
    return '<div class="crumb">' + " / ".join(parts) + "</div>"

def cta(depth, msg="Try it now", sub="Convert anything in plain language — no menus, just type."):
    p = assets(depth)
    return f"""<div class="cta-box"><div class="t">{html.escape(msg)}<span>{html.escape(sub)}</span></div>
<a class="btn" href="{p}Karo Convert.html"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h13M13 6l6 6-6 6"/></svg> Open converter</a></div>"""

def faq_block(qa):
    items = "".join(f'<details><summary>{html.escape(q)}</summary><div class="ans">{a}</div></details>' for q, a in qa)
    return f'<h2>Frequently asked questions</h2><div class="faq">{items}</div>'

def jsonld(*objs):
    return "".join(f'<script type="application/ld+json">{json.dumps(o)}</script>\n' for o in objs)

def article_ld(name, desc, url):
    return {"@context":"https://schema.org","@type":"Article","headline":name,"description":desc,"mainEntityOfPage":url,"inLanguage":"en","publisher":{"@type":"Organization","name":"Karo Convert"}}
def faq_ld(qa):
    return {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":strip(a)}} for q,a in qa]}
def strip(s):
    import re; return re.sub(r"<[^>]+>","",s)

# ============================== TRUST PAGES ==============================
write("about.html", "About Karo Convert — a free converter & study tool for students",
  "Karo Convert is a fast, free, mobile-first unit converter, scientific calculator and educational search built for students of all ages, anywhere in the world.",
  f"""{crumb([("Home","Karo Convert.html"),("About",None)])}
<div class="page">
<div class="kicker">About</div>
<h1>A fast, free tool — built for students.</h1>
<p class="lede">Karo Convert turns everyday questions into instant answers: convert any units in plain language, run a scientific or graphing calculator, and search trusted educational sources — all on one quiet, fast page.</p>
<hr class="rule">
<h2>What Karo Convert does</h2>
<p>Three connected tools, no sign-up required:</p>
<ul>
<li><strong>Universal converter.</strong> Type something like <em>“100 km to miles”</em> or <em>“350 F to C”</em> and get the answer immediately. It covers length, mass, temperature, area, volume, speed, time, digital storage, energy, power, pressure, fuel economy, angle, frequency, force, data rate and number bases.</li>
<li><strong>Scientific &amp; graphing calculator.</strong> A full keypad with trigonometry, logarithms, powers and roots, plus a graphing mode you can pan and zoom.</li>
<li><strong>Study search.</strong> A refined search that returns results only from free, ad-free educational sources — Wikipedia, open textbooks and dictionaries — in many languages.</li>
</ul>
<h2>Who it’s for</h2>
<p>Students of every age, and anyone who needs a quick, reliable answer: a pupil checking homework, a home cook converting a recipe, a traveller reading road signs, a developer sizing a file. Because the study search uses sources that exist in hundreds of languages, it’s designed to be useful anywhere in the world.</p>
<h2>How it stays free</h2>
<p>The tools are built to cost almost nothing to run, so they can stay free for everyone. Two slim, clearly-labeled ad slots help cover the bills. If you’d rather not see them, a one-time donation removes ads on your device — that’s a thank-you, and it helps keep Karo Convert free for the students who rely on it.</p>
<h2>What we care about</h2>
<ul>
<li><strong>Accuracy.</strong> Conversions use exact, documented factors; the guides show the formulas so you can check the math yourself.</li>
<li><strong>Privacy.</strong> The tools run in your browser. There are no accounts, and your saved searches stay on your device. See our <a href="privacy.html">Privacy Policy</a>.</li>
<li><strong>Calm.</strong> No pop-ups, no walls of ads, no clutter — just the answer.</li>
</ul>
</div>
{cta(0)}""", 0,
  jsonld({"@context":"https://schema.org","@type":"AboutPage","name":"About Karo Convert","url":f"{SITE}/about.html"}))

write("privacy.html", "Privacy Policy — Karo Convert",
  "How Karo Convert handles your data: what’s stored on your device, how payments and ads work, and the choices you have. A clear, plain-language privacy policy.",
  f"""{crumb([("Home","Karo Convert.html"),("Privacy",None)])}
<div class="page">
<div class="kicker">Privacy</div>
<h1>Privacy Policy</h1>
<p class="lede">Plain language, because privacy shouldn’t need a law degree. Karo Convert is built to collect as little as possible.</p>
<p class="small muted"><strong>Last updated:</strong> [add date] · <strong>Owner:</strong> [your name / business] · This page is a starting template, not legal advice — review it for your jurisdiction before publishing.</p>
<hr class="rule">
<h2>The short version</h2>
<p>The converter, calculator and study search run in your browser. We don’t require an account, and we don’t build a profile of you. A few preferences are saved <strong>on your device only</strong>. Payments are handled by Stripe (we never see your card). Ads are served by Google AdSense, which may use cookies.</p>

<h2>What’s stored on your device</h2>
<p>Using your browser’s local storage — never sent to a server we control:</p>
<ul>
<li><strong>Theme</strong> (light or dark).</li>
<li><strong>Saved searches</strong> you choose to keep.</li>
<li><strong>Ad-free reference</strong> — a payment-session id used to confirm your ad-free status (see Payments).</li>
</ul>
<p>Clearing your browser data removes all of the above.</p>

<h2>Study search</h2>
<p>When you run a study search, your query is sent to the <strong>Wikimedia Foundation’s</strong> public APIs (Wikipedia, Wikibooks, Wiktionary) to fetch results, and is handled under <a href="https://foundation.wikimedia.org/wiki/Policy:Privacy_policy" target="_blank" rel="noopener noreferrer">Wikimedia’s privacy policy</a>. We do not store your searches on our servers; they are saved only on your device, and only if you tap “save”.</p>

<h2>Payments</h2>
<p>If you donate to go ad-free, payment is processed by <strong>Stripe</strong> under <a href="https://stripe.com/privacy" target="_blank" rel="noopener noreferrer">Stripe’s privacy policy</a>. We never receive or store your full card details. To keep ads off, we store a reference to your Stripe checkout session in your browser and re-check it with Stripe; we may also receive the email you provide at checkout.</p>

<h2>Advertising &amp; cookies</h2>
<p>We use <strong>Google AdSense</strong> to show ads. Third-party vendors, including Google, may use cookies or device identifiers to serve and measure ads based on your visits to this and other sites. You can learn how Google uses data at <a href="https://policies.google.com/technologies/partner-sites" target="_blank" rel="noopener noreferrer">policies.google.com/technologies/partner-sites</a>, control personalised ads in <a href="https://adssettings.google.com" target="_blank" rel="noopener noreferrer">Google Ad Settings</a>, and opt out of third-party ad cookies at <a href="https://www.aboutads.info/choices/" target="_blank" rel="noopener noreferrer">aboutads.info/choices</a>. If your visitors are in the EEA/UK, you must also show a compliant consent notice — configure this in your AdSense account.</p>

<h2>Analytics</h2>
<p>This site does not run its own analytics cookies by default. If you add an analytics tool, update this section to describe it.</p>

<h2>Children</h2>
<p>Karo Convert is intended to be safe for students of all ages. We do not knowingly collect personal information from anyone, including children — the tools work without entering any personal details. Please don’t type personal information into the search box. If you believe a child has provided personal data, contact us and we’ll remove it.</p>

<h2>Your choices</h2>
<ul>
<li>Clear your saved searches any time from the “Saved searches” panel, or by clearing your browser data.</li>
<li>Manage or block cookies in your browser settings.</li>
<li>Control ad personalisation via the links under “Advertising &amp; cookies”.</li>
</ul>

<h2>Changes</h2>
<p>We’ll update this page if our practices change, and revise the “Last updated” date above.</p>

<h2>Contact</h2>
<p>Questions about privacy? See our <a href="contact.html">Contact page</a>.</p>
</div>""", 0)

write("terms.html", "Terms of Use — Karo Convert",
  "The terms for using Karo Convert: acceptable use, accuracy disclaimers, donations, third-party links and liability. Plain-language terms of use.",
  f"""{crumb([("Home","Karo Convert.html"),("Terms",None)])}
<div class="page">
<div class="kicker">Terms</div>
<h1>Terms of Use</h1>
<p class="lede">The ground rules for using Karo Convert. By using the site, you agree to these terms.</p>
<p class="small muted"><strong>Last updated:</strong> [add date] · This is a starting template, not legal advice — review it for your jurisdiction before publishing.</p>
<hr class="rule">
<h2>Use of the service</h2>
<p>Karo Convert is provided for general, personal and educational use, free of charge. You may use it as much as you like. Please don’t misuse it — for example by attempting to break it, overload it, scrape it at scale, or use it for anything unlawful.</p>
<h2>Accuracy &amp; “as is”</h2>
<p>We work hard to keep conversions and calculations accurate, and we publish the formulas so you can verify them. Even so, the service is provided <strong>“as is”, without warranties of any kind</strong>. Results may contain errors or rounding, and unit definitions can vary by region. <strong>Do not rely on Karo Convert for decisions where an error could cause harm or loss</strong> — including medical, financial, legal, structural, scientific or other professional contexts. Always double-check critical figures with an authoritative source.</p>
<h2>Study search &amp; third-party links</h2>
<p>Study results and other outbound links point to third-party sites (such as Wikimedia projects). We don’t control and aren’t responsible for their content. Linked content is owned by its respective authors and provided under its own licenses.</p>
<h2>Donations</h2>
<p>Donations are a <strong>voluntary, one-time contribution</strong> to support the site, processed by Stripe. As a thank-you, donating removes ads on your device. Donations are generally non-refundable; if something went wrong with a payment, contact us and we’ll try to help.</p>
<h2>Limitation of liability</h2>
<p>To the fullest extent permitted by law, Karo Convert and its operator are not liable for any damages arising from your use of, or inability to use, the service.</p>
<h2>Changes</h2>
<p>We may update these terms; continued use after changes means you accept them.</p>
<h2>Contact</h2>
<p>See our <a href="contact.html">Contact page</a>.</p>
</div>""", 0)

write("contact.html", "Contact Karo Convert",
  "Get in touch with Karo Convert — questions, feedback, corrections, or a bug report. We read every message.",
  f"""{crumb([("Home","Karo Convert.html"),("Contact",None)])}
<div class="page">
<div class="kicker">Contact</div>
<h1>Get in touch</h1>
<p class="lede">Found a wrong number, want a new unit added, or just have feedback? We’d love to hear it.</p>
<hr class="rule">
<div class="callout">
<div class="lbl">Email</div>
<p style="margin:0"><a href="mailto:hello@karoconvert.com">hello@karoconvert.com</a> &nbsp;<span class="small muted">(replace with your real address)</span></p>
</div>
<p>A few things that help us help you faster:</p>
<ul>
<li><strong>Corrections:</strong> tell us the exact conversion (e.g. “50 miles to km”), what you got, and what you expected.</li>
<li><strong>Bugs:</strong> note your device and browser, and what you tapped just before it happened.</li>
<li><strong>Requests:</strong> the unit, category or feature you’d like to see.</li>
</ul>
<p class="muted small">We’re a small, free project, so replies may take a little time — but every message is read.</p>
</div>
{cta(0, "Meanwhile, give it a try", "Type any conversion and get an instant answer.")}""", 0)

# ============================== GUIDES HUB ==============================
GUIDES = [
  ("km-to-miles.html","ruler","Kilometers to miles","Convert km to miles, with the exact formula, a quick-reference table and race distances."),
  ("celsius-to-fahrenheit.html","temp","Celsius to Fahrenheit","The formula, key reference points, oven temperatures and worked examples."),
  ("kg-to-pounds.html","scale","Kilograms to pounds","Convert kg to lb (and stone), with a reference table and everyday examples."),
  ("meters-to-feet.html","ruler","Meters to feet","Convert metres to feet (and feet + inches), with a table and height examples."),
  ("inches-to-centimeters.html","ruler","Inches to centimeters","1 inch = 2.54 cm exactly — formula, table and screen/paper sizes."),
  ("liters-to-gallons.html","cup","Liters to gallons","US vs imperial gallons in litres, with a table and fuel examples."),
  ("grams-to-ounces.html","scale","Grams to ounces","Convert grams to ounces (weight, not fluid), with a kitchen-friendly table."),
  ("data-storage-units-explained.html","data","Data units explained","KB, MB, GB, TB — decimal vs binary, bits vs bytes, and why your drive looks smaller."),
  ("cups-to-milliliters.html","cup","Cups to milliliters","US, metric and UK cups in ml, plus tablespoons and teaspoons for cooking."),
]
ICONS = {
  "ruler":'<path d="M3 7l4-4 14 14-4 4z"/><path d="M7 7l1.5 1.5M10 10l1.5 1.5M13 13l1.5 1.5M16 16l1.5 1.5"/>',
  "temp":'<path d="M10 14V5a2 2 0 1 1 4 0v9a4 4 0 1 1-4 0z"/>',
  "scale":'<path d="M12 3v3M5 6h14M7 6l-3 7h6zM17 6l-3 7h6zM9 20h6M12 17v3"/>',
  "data":'<ellipse cx="12" cy="5" rx="8" ry="3"/><path d="M4 5v6c0 1.7 3.6 3 8 3s8-1.3 8-3V5M4 11v6c0 1.7 3.6 3 8 3s8-1.3 8-3v-6"/>',
  "cup":'<path d="M5 8h11v6a4 4 0 0 1-4 4H9a4 4 0 0 1-4-4z"/><path d="M16 9h2a2 2 0 0 1 0 4h-2"/><path d="M7 3v2M10 3v2M13 3v2"/>',
}
def gicon(k): return f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">{ICONS[k]}</svg>'

cards = "".join(f"""<a class="card" href="{slug}"><div class="ic">{gicon(ic)}</div><h3>{html.escape(t)}</h3><p>{html.escape(d)}</p></a>""" for slug,ic,t,d in GUIDES)
write("guides/index.html", "Conversion guides — clear explanations & reference tables | Karo Convert",
  "Step-by-step conversion guides with exact formulas, worked examples and quick-reference tables: km to miles, Celsius to Fahrenheit, kg to pounds, data units and more.",
  f"""{crumb([("Home","../Karo Convert.html"),("Guides",None)])}
<div class="page">
<div class="kicker">Guides</div>
<h1>Conversion guides</h1>
<p class="lede">Short, accurate explainers for the conversions people look up most — each with the exact formula, worked examples and a quick-reference table you can trust.</p>
</div>
<div class="cards">{cards}</div>
{cta(1)}""", 1)

# ============================== GUIDE PAGES ==============================
def table(caption, headers, rows):
    th = "".join(f"<th>{html.escape(h)}</th>" for h in headers)
    body = ""
    for r in rows:
        body += "<tr>" + "".join(f'<td class="num">{c}</td>' if i>0 else f"<td>{c}</td>" for i,c in enumerate(r)) + "</tr>"
    return f'<div class="tbl-wrap"><table><caption>{html.escape(caption)}</caption><thead><tr>{th}</tr></thead><tbody>{body}</tbody></table></div>'

# ---- km to miles ----
qa = [
 ("Is 1 km exactly 0.6214 miles?","Not exactly — that’s a rounded value. One kilometre equals <strong>0.62137119…</strong> miles, because a mile is defined as exactly 1,609.344 metres. For everyday use, 0.6214 (or even 0.62) is close enough."),
 ("How many kilometres are in a mile?","Exactly <strong>1.609344 km</strong>. So to go from miles to kilometres, multiply by about 1.609."),
 ("How far is a 5K in miles?","A 5-kilometre run is about <strong>3.11 miles</strong> (5 × 0.621371). A 10K is about 6.21 miles."),
 ("Is a marathon really 26.2 miles?","Yes — a marathon is 42.195 km, which is 26.219 miles, almost always written as 26.2.")
]
body = f"""{crumb([("Home","../Karo Convert.html"),("Guides","./"),("Kilometers to miles",None)])}
<article class="article">
<div class="kicker">Length</div>
<h1>Kilometers to miles: the simple conversion</h1>
<p class="lede">One kilometre is about 0.621 miles. Here’s the exact formula, why it works, and a table for the distances you’ll actually use.</p>

<div class="callout"><div class="lbl">Quick answer</div>
<p style="margin:0">Multiply kilometres by <strong>0.621371</strong> to get miles.</p></div>

<h2>The formula</h2>
<div class="formula">miles = kilometers × 0.621371</div>
<div class="formula">kilometers = miles × 1.609344</div>
<p>These factors aren’t arbitrary: since 1959 the international mile has been defined as exactly <strong>1,609.344 metres</strong>. A kilometre is 1,000 metres, so one kilometre is 1000 ÷ 1609.344 = 0.6213711922… of a mile.</p>

<h2>Worked examples</h2>
<ul>
<li><strong>100 km → miles:</strong> 100 × 0.621371 = <strong>62.14 miles</strong>.</li>
<li><strong>A 5K race:</strong> 5 × 0.621371 = <strong>3.11 miles</strong>.</li>
<li><strong>Speed, 100 km/h:</strong> the same factor applies — 100 km/h ≈ <strong>62.1 mph</strong>.</li>
</ul>

{table("Common distances", ["Kilometers","Miles"], [["1","0.621"],["5 (5K)","3.107"],["10 (10K)","6.214"],["21.0975 (half-marathon)","13.109"],["42.195 (marathon)","26.219"],["100","62.137"]])}

<h2>When you’ll use it</h2>
<p>Most countries post road distances and speed limits in kilometres, while the US and UK use miles — so this is the conversion travellers reach for most. Runners use it to compare race distances, and it’s handy any time a fitness app reports the “wrong” unit.</p>

{faq_block(qa)}
</article>
{cta(1, "Convert any distance instantly", "Type “50 miles to km” or any other units.")}"""
write("guides/km-to-miles.html","Kilometers to miles — exact formula, table & examples | Karo Convert",
  "Convert kilometers to miles with the exact factor (0.621371), the reverse formula, worked examples and a quick-reference table including 5K, 10K and marathon distances.",
  body, 1, jsonld(article_ld("Kilometers to miles","Convert km to miles with the exact formula and a reference table.",f"{SITE}/guides/km-to-miles.html"), faq_ld(qa)))

# ---- Celsius to Fahrenheit ----
qa = [
 ("What’s the quick formula for Celsius to Fahrenheit?","Multiply by 9, divide by 5, then add 32: <strong>°F = °C × 9/5 + 32</strong>. A rough shortcut is “double it and add 30”."),
 ("At what temperature do the two scales meet?","At <strong>−40°</strong>: −40°C equals −40°F. It’s the only point where the numbers are identical."),
 ("What is 98.6°F in Celsius?","About <strong>37°C</strong>, the usual figure for normal human body temperature."),
 ("What oven temperature is 180°C?","<strong>356°F</strong> — most recipes round it to 350°F, a very common baking temperature.")
]
body = f"""{crumb([("Home","../Karo Convert.html"),("Guides","./"),("Celsius to Fahrenheit",None)])}
<article class="article">
<div class="kicker">Temperature</div>
<h1>Celsius to Fahrenheit, made clear</h1>
<p class="lede">The formula has a multiply and an add — here’s why, plus the reference points and oven temperatures you’ll use most.</p>

<div class="callout"><div class="lbl">Quick answer</div>
<p style="margin:0"><strong>°F = (°C × 9/5) + 32</strong>. To reverse it: <strong>°C = (°F − 32) × 5/9</strong>.</p></div>

<h2>Why two steps?</h2>
<p>The scales differ in two ways. They start in different places — water freezes at 0°C but 32°F — which is the <strong>+32</strong>. And each Celsius degree is larger: there are 100 Celsius degrees between freezing and boiling, but 180 Fahrenheit degrees, a ratio of <strong>9/5</strong>. Adjust for size, then shift the start point.</p>

<h2>Worked examples</h2>
<ul>
<li><strong>25°C → °F:</strong> 25 × 9/5 = 45, + 32 = <strong>77°F</strong> (a warm day).</li>
<li><strong>350°F → °C:</strong> (350 − 32) × 5/9 = <strong>176.7°C</strong> (a common oven setting).</li>
<li><strong>Quick estimate of 22°C:</strong> double to 44, add 30 = ~74°F (actual 71.6°F).</li>
</ul>

{table("Reference points", ["Celsius","Fahrenheit","What it is"], [["−40","−40","Scales meet"],["0","32","Water freezes"],["20","68","Room temperature"],["37","98.6","Body temperature"],["100","212","Water boils (sea level)"],["180","356","Moderate oven"],["200","392","Hot oven"]])}

<h2>Where it comes up</h2>
<p>Weather and cooking are the big ones: the US reports temperatures and oven settings in Fahrenheit, while most of the world — and most science — uses Celsius. Knowing a few anchor points (0, 37, 100) lets you sanity-check any conversion at a glance.</p>

{faq_block(qa)}
</article>
{cta(1, "Convert any temperature", "Try “100 C to F” or “fever 38.5 C to F”.")}"""
write("guides/celsius-to-fahrenheit.html","Celsius to Fahrenheit — formula, oven temps & examples | Karo Convert",
  "Convert Celsius to Fahrenheit with the formula °F = °C × 9/5 + 32, key reference points (freezing, body temp, boiling), oven temperatures and worked examples.",
  body, 1, jsonld(article_ld("Celsius to Fahrenheit","Convert °C to °F with the formula and reference points.",f"{SITE}/guides/celsius-to-fahrenheit.html"), faq_ld(qa)))

# ---- kg to pounds ----
qa = [
 ("How many pounds is 1 kg?","One kilogram is about <strong>2.20462 pounds</strong>. The pound is defined as exactly 0.45359237 kg."),
 ("What is 70 kg in pounds?","70 × 2.20462 = about <strong>154.3 lb</strong>."),
 ("How do stones fit in?","In the UK, body weight is often given in stone: <strong>1 stone = 14 pounds = 6.35 kg</strong>. So 70 kg ≈ 11 stone 0.3 lb."),
 ("What’s the airline luggage limit of 23 kg in pounds?","About <strong>50.7 lb</strong> — which is why many airlines quote a 50 lb limit.")
]
body = f"""{crumb([("Home","../Karo Convert.html"),("Guides","./"),("Kilograms to pounds",None)])}
<article class="article">
<div class="kicker">Mass &amp; weight</div>
<h1>Kilograms to pounds (and stone)</h1>
<p class="lede">One kilogram is just over 2.2 pounds. Here’s the exact factor, a reference table, and how stones fit in.</p>

<div class="callout"><div class="lbl">Quick answer</div>
<p style="margin:0">Multiply kilograms by <strong>2.20462</strong> to get pounds. To reverse it, multiply pounds by <strong>0.453592</strong>.</p></div>

<h2>The formula</h2>
<div class="formula">pounds = kilograms × 2.20462</div>
<div class="formula">kilograms = pounds × 0.453592</div>
<p>The international avoirdupois pound is defined as exactly <strong>0.45359237 kg</strong>, so one kilogram is 1 ÷ 0.45359237 = 2.2046226… pounds.</p>

<h2>Worked examples</h2>
<ul>
<li><strong>70 kg → lb:</strong> 70 × 2.20462 = <strong>154.3 lb</strong>.</li>
<li><strong>A 3.5 kg newborn:</strong> 3.5 × 2.20462 = <strong>7.7 lb</strong> (about 7 lb 12 oz).</li>
<li><strong>23 kg suitcase:</strong> 23 × 2.20462 = <strong>50.7 lb</strong>.</li>
</ul>

{table("Common weights", ["Kilograms","Pounds","Stone · lb"], [["1","2.205","0 st 2.2"],["5","11.02","0 st 11.0"],["10","22.05","1 st 8.0"],["50","110.2","7 st 12.2"],["70","154.3","11 st 0.3"],["100","220.5","15 st 10.5"]])}

<h2>Where it comes up</h2>
<p>Most of the world weighs in kilograms; the US uses pounds, and the UK mixes pounds and stone for body weight. This conversion shows up with luggage limits, gym weights, recipes, and health and fitness apps.</p>

{faq_block(qa)}
</article>
{cta(1, "Convert any weight", "Try “150 lb to kg” or “2.5 kg to oz”.")}"""
write("guides/kg-to-pounds.html","Kilograms to pounds — exact formula, table & stone | Karo Convert",
  "Convert kilograms to pounds with the exact factor (2.20462), a reference table, stone conversions and everyday examples like body weight and luggage limits.",
  body, 1, jsonld(article_ld("Kilograms to pounds","Convert kg to lb with the exact formula and a reference table.",f"{SITE}/guides/kg-to-pounds.html"), faq_ld(qa)))

# ---- data units ----
qa = [
 ("Why does my 1 TB drive show about 931 GB?","Drive makers count in <strong>decimal</strong> (1 TB = 1,000,000,000,000 bytes), but operating systems often display <strong>binary</strong> units. 1,000,000,000,000 ÷ 1024³ = about <strong>931 GiB</strong>, so nothing is missing — it’s just two ways of counting."),
 ("What’s the difference between a bit and a byte?","A <strong>byte</strong> is 8 <strong>bits</strong>. Storage (files, drives) is measured in bytes; data-transfer speeds are usually measured in bits."),
 ("Why is my internet ‘100 Mbps’ but downloads show ~12 MB/s?","Because 100 megabits ÷ 8 = <strong>12.5 megabytes</strong> per second. Speeds are in bits, file sizes in bytes — divide by 8 to compare."),
 ("Should I use MB or MiB?","Use <strong>MB</strong> (decimal, 1000-based) for general and marketing contexts, and <strong>MiB</strong> (binary, 1024-based) when you need the exact memory/OS figure.")
]
body = f"""{crumb([("Home","../Karo Convert.html"),("Guides","./"),("Data units explained",None)])}
<article class="article">
<div class="kicker">Digital storage</div>
<h1>Data units explained: KB, MB, GB and TB</h1>
<p class="lede">Two counting systems and a bit-vs-byte mix-up cause most data-size confusion. Here’s the whole picture, clearly.</p>

<div class="callout"><div class="lbl">Quick answer</div>
<p style="margin:0">There are two systems. <strong>Decimal (SI):</strong> each step is ×1000 (kB, MB, GB, TB). <strong>Binary (IEC):</strong> each step is ×1024 (KiB, MiB, GiB, TiB). And remember: <strong>8 bits = 1 byte</strong>.</p></div>

<h2>Decimal vs binary</h2>
<p>Historically, “KB/MB/GB” were used loosely for both 1000- and 1024-based values, which is exactly why a drive’s size can look different in different places. The IEC introduced separate binary names (KiB, MiB, GiB) to remove the ambiguity.</p>

{table("Decimal — SI (×1000)", ["Unit","Equals","Bytes"], [["1 kilobyte (kB)","1,000 bytes","10³"],["1 megabyte (MB)","1,000 kB","10⁶"],["1 gigabyte (GB)","1,000 MB","10⁹"],["1 terabyte (TB)","1,000 GB","10¹²"]])}
{table("Binary — IEC (×1024)", ["Unit","Equals","Bytes"], [["1 kibibyte (KiB)","1,024 bytes","2¹⁰"],["1 mebibyte (MiB)","1,024 KiB","2²⁰"],["1 gibibyte (GiB)","1,024 MiB","2³⁰"],["1 tebibyte (TiB)","1,024 GiB","2⁴⁰"]])}

<h2>Bits vs bytes</h2>
<p>A <strong>bit</strong> is a single 1 or 0; a <strong>byte</strong> is eight bits. Storage is measured in bytes (with a capital B: MB, GB). Network and internet speeds are measured in bits (lower-case b: Mbps, Gbps). To convert a connection speed to a download rate, divide by 8:</p>
<div class="formula">100 Mbps ÷ 8 = 12.5 MB/s</div>

<h2>Worked example</h2>
<p>You buy a “2 TB” drive. That’s 2,000,000,000,000 bytes (decimal). Your operating system may report it in binary: 2,000,000,000,000 ÷ 1024³ ≈ <strong>1,862 GiB</strong> (about 1.82 TiB). Same drive, two labels.</p>

{faq_block(qa)}
</article>
{cta(1, "Convert any data size", "Karo Convert supports both SI and binary — try “5 GB to MB” or “1 TiB to GB”.")}"""
write("guides/data-storage-units-explained.html","Data units explained: KB, MB, GB, TB (decimal vs binary) | Karo Convert",
  "Understand digital storage units: decimal (SI, ×1000) vs binary (IEC, ×1024), bits vs bytes, why a 1 TB drive shows ~931 GB, and how to convert Mbps to MB/s.",
  body, 1, jsonld(article_ld("Data units explained","KB, MB, GB, TB — decimal vs binary and bits vs bytes.",f"{SITE}/guides/data-storage-units-explained.html"), faq_ld(qa)))

# ---- cups to ml ----
qa = [
 ("How many ml in a cup?","It depends on the cup. A <strong>US customary cup is 236.6 ml</strong>, a <strong>metric cup is 250 ml</strong>, and a <strong>US ‘legal’ cup is 240 ml</strong> (used on nutrition labels)."),
 ("Which cup do US recipes use?","US recipes use the <strong>US customary cup, 236.6 ml</strong>. Karo Convert uses this value too, so a result like “2 cups = 473.18 ml” matches."),
 ("How many ml in a tablespoon and teaspoon?","In the US system, <strong>1 tablespoon = 14.79 ml</strong> and <strong>1 teaspoon = 4.93 ml</strong>. There are 3 teaspoons in a tablespoon."),
 ("Do dry and liquid cups differ?","By volume they’re the same (a cup is a cup). The difference is in how you measure: level off dry ingredients, and read liquids at eye level.")
]
body = f"""{crumb([("Home","../Karo Convert.html"),("Guides","./"),("Cups to milliliters",None)])}
<article class="article">
<div class="kicker">Volume · cooking</div>
<h1>Cups to milliliters (without the guesswork)</h1>
<p class="lede">“A cup” isn’t one fixed size — it depends on the country. Here are the values that matter, and which one to use.</p>

<div class="callout"><div class="lbl">Quick answer</div>
<p style="margin:0"><strong>US customary cup = 236.6 ml</strong> · <strong>Metric cup = 250 ml</strong> · <strong>US legal cup = 240 ml</strong>. For US recipes, use 236.6 ml.</p></div>

<h2>Why there are several cups</h2>
<p>Different standards grew up in different places. US recipes use the customary cup (236.588 ml). Nutrition labels in the US use a rounded “legal” cup of 240 ml. Australia, New Zealand and much of the metric world use a 250 ml cup. The old UK imperial cup (284 ml) is now rarely used — modern UK recipes work in millilitres and grams.</p>

{table("Cup sizes", ["Cup type","Milliliters","Where it’s used"], [["US customary","236.6","US recipes"],["US legal","240","US nutrition labels"],["Metric","250","Australia, NZ, metric world"],["UK imperial (old)","284.1","Older UK recipes"]])}

<h2>Common amounts (US customary)</h2>
{table("Cooking conversions", ["Amount","Milliliters"], [["1 teaspoon (tsp)","4.93"],["1 tablespoon (tbsp)","14.79"],["¼ cup","59.1"],["⅓ cup","78.9"],["½ cup","118.3"],["1 cup","236.6"],["2 cups","473.2"]])}

<h2>Worked examples</h2>
<ul>
<li><strong>2 cups of milk (US):</strong> 2 × 236.588 = <strong>473.2 ml</strong>.</li>
<li><strong>¾ cup of water (US):</strong> 0.75 × 236.588 = <strong>177.4 ml</strong>.</li>
<li><strong>1 metric cup of flour:</strong> exactly <strong>250 ml</strong> by volume.</li>
</ul>

<h2>The practical tip</h2>
<p>Match the cup to the recipe’s origin. If a recipe is American, use 236.6 ml; if it’s Australian, use 250 ml. The difference (about 6%) is enough to matter in baking, where ratios count.</p>

{faq_block(qa)}
</article>
{cta(1, "Convert any cooking amount", "Try “2 cups to ml”, “1 tbsp to ml” or “350 F to C”.")}"""
write("guides/cups-to-milliliters.html","Cups to milliliters — US, metric & UK cups + tbsp/tsp | Karo Convert",
  "Convert cups to milliliters accurately: US customary (236.6 ml), US legal (240 ml), metric (250 ml) and UK cups, plus tablespoon and teaspoon conversions for cooking.",
  body, 1, jsonld(article_ld("Cups to milliliters","Convert cups to ml across US, metric and UK standards.",f"{SITE}/guides/cups-to-milliliters.html"), faq_ld(qa)))

# ---- meters to feet ----
qa=[("How many feet are in a metre?","One metre is about <strong>3.28084 feet</strong> — roughly 3 feet 3⅜ inches."),
("How do I write metres as feet and inches?","Multiply metres by 3.28084 for total feet, then multiply the decimal part by 12 for inches. Example: 1.8 m = 5.905 ft → <strong>5 ft 11 in</strong>."),
("What is 6 feet in metres?","6 × 0.3048 = <strong>1.83 m</strong>."),
("Is the conversion exact?","Yes — since 1959 a foot is defined as exactly 0.3048 m, so 1 m = 1 ÷ 0.3048 = 3.28084 ft.")]
write("guides/meters-to-feet.html","Meters to feet — exact formula, table & height examples | Karo Convert",
 "Convert meters to feet with the exact factor (3.28084), how to express metres as feet and inches, a reference table and everyday height examples.",
 f"""{crumb([("Home","../Karo Convert.html"),("Guides","./"),("Meters to feet",None)])}
<article class="article"><div class="kicker">Length</div>
<h1>Meters to feet (and feet + inches)</h1>
<p class="lede">One metre is about 3.28 feet. Here’s the exact formula, how to convert to feet and inches, and a quick table.</p>
<div class="callout"><div class="lbl">Quick answer</div><p style="margin:0">Multiply metres by <strong>3.28084</strong> to get feet. To reverse it, multiply feet by <strong>0.3048</strong>.</p></div>
<h2>The formula</h2><div class="formula">feet = meters × 3.28084</div><div class="formula">meters = feet × 0.3048</div>
<p>The foot has been defined as exactly 0.3048 metres since 1959, so one metre equals 1 ÷ 0.3048 = 3.2808399… feet.</p>
<h2>Feet and inches</h2>
<p>Heights are usually given in feet <em>and</em> inches. Take the total feet, keep the whole number, and multiply what’s left by 12 for the inches:</p>
<ul><li><strong>1.8 m</strong> → 1.8 × 3.28084 = 5.905 ft → <strong>5 ft 11 in</strong>.</li>
<li><strong>1.65 m</strong> → 5.413 ft → <strong>5 ft 5 in</strong>.</li></ul>
{table("Common heights & distances",["Meters","Feet","Feet + inches"],[["1","3.281","3 ft 3 in"],["1.65","5.413","5 ft 5 in"],["1.8","5.906","5 ft 11 in"],["2","6.562","6 ft 7 in"],["10","32.808","—"],["100","328.084","—"]])}
<h2>Where it comes up</h2><p>Heights (most of the world uses metres, the US uses feet and inches), ceilings and room sizes, and sports fields all mix the two systems.</p>
{faq_block(qa)}</article>
{cta(1,"Convert any length","Try “6 ft to m” or “2 m to inches”.")}""",1,
 jsonld(article_ld("Meters to feet","Convert metres to feet and feet + inches.",f"{SITE}/guides/meters-to-feet.html"),faq_ld(qa)))

# ---- inches to centimeters ----
qa=[("How many centimetres are in an inch?","Exactly <strong>2.54 cm</strong>. The inch has been defined as 2.54 cm since 1959, so the conversion is exact."),
("What is 5 ft 9 in in centimetres?","That’s 69 inches × 2.54 = <strong>175.3 cm</strong>."),
("How do I go from cm back to inches?","Multiply centimetres by <strong>0.393701</strong> (or divide by 2.54)."),
("How big is a 32-inch TV?","Its diagonal is 32 × 2.54 = <strong>81.3 cm</strong>.")]
write("guides/inches-to-centimeters.html","Inches to centimeters — exact 2.54 cm formula & table | Karo Convert",
 "Convert inches to centimeters with the exact factor (1 in = 2.54 cm), a reference table, and examples for height, screen sizes and paper.",
 f"""{crumb([("Home","../Karo Convert.html"),("Guides","./"),("Inches to centimeters",None)])}
<article class="article"><div class="kicker">Length</div>
<h1>Inches to centimeters</h1>
<p class="lede">One inch is exactly 2.54 centimetres — one of the few conversions with no rounding at all.</p>
<div class="callout"><div class="lbl">Quick answer</div><p style="margin:0">Multiply inches by <strong>2.54</strong> to get centimetres. To reverse it, multiply centimetres by <strong>0.393701</strong>.</p></div>
<h2>The formula</h2><div class="formula">centimeters = inches × 2.54</div><div class="formula">inches = centimeters × 0.393701</div>
<p>Because the inch is <em>defined</em> as 2.54 cm, this conversion is exact — there’s no approximation to worry about.</p>
<h2>Worked examples</h2><ul>
<li><strong>10 in → cm:</strong> 10 × 2.54 = <strong>25.4 cm</strong>.</li>
<li><strong>Height 5 ft 9 in:</strong> 69 in × 2.54 = <strong>175.3 cm</strong>.</li>
<li><strong>A4 paper width (8.27 in):</strong> ≈ <strong>21.0 cm</strong>.</li></ul>
{table("Quick reference",["Inches","Centimeters"],[["1","2.54"],["5","12.70"],["10","25.40"],["12 (1 foot)","30.48"],["24","60.96"],["36 (1 yard)","91.44"]])}
<h2>Where it comes up</h2><p>Screen sizes, paper, body height, and craft or DIY measurements often switch between inches and centimetres.</p>
{faq_block(qa)}</article>
{cta(1,"Convert any length","Try “175 cm to feet” or “12 in to cm”.")}""",1,
 jsonld(article_ld("Inches to centimeters","Convert inches to cm with the exact 2.54 factor.",f"{SITE}/guides/inches-to-centimeters.html"),faq_ld(qa)))

# ---- liters to gallons ----
qa=[("How many litres are in a gallon?","It depends which gallon. A <strong>US gallon is 3.785 litres</strong>; a <strong>UK (imperial) gallon is 4.546 litres</strong> — about 20% bigger."),
("Why are US and UK gallons different?","They’re two separate historical standards. The US kept an older wine gallon; the UK redefined its gallon in 1824. Always check which one a figure uses."),
("Which gallon should I use?","For US fuel economy, recipes, or anything American, use the <strong>US gallon</strong>. The UK now mostly uses litres, but older figures may be imperial gallons."),
("How do I convert litres to US gallons?","Multiply litres by <strong>0.264172</strong> (or divide by 3.785).")]
write("guides/liters-to-gallons.html","Liters to gallons — US vs imperial, formula & table | Karo Convert",
 "Convert liters to gallons accurately: US gallon (3.785 L) vs UK imperial gallon (4.546 L), the formulas, a reference table and fuel examples.",
 f"""{crumb([("Home","../Karo Convert.html"),("Guides","./"),("Liters to gallons",None)])}
<article class="article"><div class="kicker">Volume</div>
<h1>Liters to gallons: US vs imperial</h1>
<p class="lede">There are two gallons, and they differ by about 20%. Use the right one or your numbers will be off.</p>
<div class="callout"><div class="lbl">Quick answer</div><p style="margin:0"><strong>1 litre = 0.264 US gallons = 0.220 imperial gallons.</strong> US gallon = 3.785 L · imperial gallon = 4.546 L.</p></div>
<h2>The formulas</h2><div class="formula">US gallons = liters × 0.264172</div><div class="formula">imperial gallons = liters × 0.219969</div>
<h2>Worked examples</h2><ul>
<li><strong>50 L of fuel:</strong> 50 × 0.264172 = <strong>13.2 US gal</strong> (or 11.0 imperial gal).</li>
<li><strong>10 US gallons:</strong> 10 × 3.785412 = <strong>37.85 L</strong>.</li></ul>
{table("Litres to gallons",["Liters","US gallons","Imperial gallons"],[["1","0.264","0.220"],["5","1.321","1.100"],["10","2.642","2.200"],["20","5.283","4.399"],["50","13.209","10.998"]])}
<h2>Where it comes up</h2><p>Fuel economy (US mpg uses US gallons), recipes, and water volumes. Mixing the two gallons is a classic source of error in travel and cooking.</p>
{faq_block(qa)}</article>
{cta(1,"Convert any volume","Try “10 gallons to liters” or “2 cups to ml”.")}""",1,
 jsonld(article_ld("Liters to gallons","Convert litres to US and imperial gallons.",f"{SITE}/guides/liters-to-gallons.html"),faq_ld(qa)))

# ---- grams to ounces ----
qa=[("How many grams are in an ounce?","One ounce (weight) is about <strong>28.35 grams</strong>."),
("Is this the same as a fluid ounce?","No — be careful. A <strong>weight</strong> ounce (28.35 g) measures mass; a <strong>fluid</strong> ounce measures volume (about 29.6 ml in the US). They are different things."),
("What is 8 oz in grams?","8 × 28.349523 = <strong>226.8 g</strong> (about half a pound)."),
("How do I convert grams to ounces?","Multiply grams by <strong>0.035274</strong> (or divide by 28.35).")]
write("guides/grams-to-ounces.html","Grams to ounces — weight conversion, formula & table | Karo Convert",
 "Convert grams to ounces (weight, not fluid ounces) with the exact factor, a kitchen-friendly reference table and worked examples.",
 f"""{crumb([("Home","../Karo Convert.html"),("Guides","./"),("Grams to ounces",None)])}
<article class="article"><div class="kicker">Mass &amp; weight</div>
<h1>Grams to ounces</h1>
<p class="lede">One ounce is about 28.35 grams. Just don’t confuse it with the fluid ounce — that measures volume, not weight.</p>
<div class="callout"><div class="lbl">Quick answer</div><p style="margin:0">Multiply grams by <strong>0.035274</strong> to get ounces. To reverse it, multiply ounces by <strong>28.349523</strong>.</p></div>
<h2>The formula</h2><div class="formula">ounces = grams × 0.035274</div><div class="formula">grams = ounces × 28.349523</div>
<h2>Weight ounce vs fluid ounce</h2>
<p>This guide is about the <strong>avoirdupois ounce</strong>, a unit of <em>weight</em> (16 to a pound). A <strong>fluid ounce</strong> is a unit of <em>volume</em> used for liquids. A recipe asking for “8 oz of flour” means weight; “8 fl oz of milk” means volume — don’t swap them.</p>
<h2>Worked examples</h2><ul>
<li><strong>100 g → oz:</strong> 100 × 0.035274 = <strong>3.53 oz</strong>.</li>
<li><strong>250 g of butter:</strong> ≈ <strong>8.82 oz</strong>.</li>
<li><strong>1 pound:</strong> 16 oz = <strong>453.6 g</strong>.</li></ul>
{table("Kitchen reference",["Grams","Ounces"],[["1","0.035"],["10","0.353"],["28.35 (1 oz)","1.000"],["100","3.527"],["250","8.818"],["500","17.637"]])}
{faq_block(qa)}</article>
{cta(1,"Convert any weight","Try “16 oz to grams” or “2 kg to lb”.")}""",1,
 jsonld(article_ld("Grams to ounces","Convert grams to ounces (weight) with the exact factor.",f"{SITE}/guides/grams-to-ounces.html"),faq_ld(qa)))

# ============================== WRITING & CITATION PILLAR ==============================
def cite(style, ref, intext=""):
    it = f'<div class="it">{intext}</div>' if intext else ''
    return f'<div class="cite"><div class="style">{style}</div><div class="ref">{ref}</div>{it}</div>'

ACTIVE["writing/index.html"]="writing"
WRITING=[
 ("citation-styles-explained.html","APA vs MLA vs Chicago vs Harvard","Which style to use, the current editions, and the same source shown in each."),
 ("how-to-cite-a-website.html","How to cite a website","Website citations in APA, MLA and Chicago — including no author or no date."),
 ("how-to-cite-wikipedia.html","How to cite Wikipedia","Whether you should, how to do it properly, and the permanent-link trick."),
 ("how-to-cite-a-book.html","How to cite a book","Book citations in APA, MLA and Chicago, including chapters and editions."),
 ("how-to-cite-a-journal-article.html","How to cite a journal article","Journal articles in APA, MLA and Chicago, with the DOI explained."),
 ("bibliography-vs-works-cited-vs-references.html","Bibliography vs Works Cited vs References","What each list is called in each style — and the difference."),
 ("how-to-write-a-thesis-statement.html","How to write a thesis statement","A simple formula, plus weak-vs-strong examples you can copy."),
 ("how-to-structure-a-research-paper.html","How to structure a research paper","A clear outline for term papers: intro, body, conclusion, references."),
 ("how-to-avoid-plagiarism.html","How to avoid plagiarism","Quoting, paraphrasing and summarising — and exactly when to cite."),
 ("how-to-evaluate-sources.html","How to evaluate sources","A quick checklist for credible sources, and primary vs secondary."),
]
WICON='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 20h9"/><path d="M16.5 3.5a2.1 2.1 0 0 1 3 3L7 19l-4 1 1-4z"/></svg>'
wcards="".join(f"""<a class="card" href="{slug}"><div class="ic">{WICON}</div><h3>{html.escape(t)}</h3><p>{html.escape(d)}</p></a>""" for slug,t,d in WRITING)
write("writing/index.html","Writing & citation guides for students | Karo Convert",
 "Clear guides for student writing and research: how to cite sources in APA, MLA and Chicago, build a bibliography, write a thesis statement, structure a paper and avoid plagiarism.",
 f"""{crumb([("Home","../Karo Convert.html"),("Writing",None)])}
<div class="page"><div class="kicker">Writing &amp; citation</div>
<h1>Writing &amp; citation guides</h1>
<p class="lede">Practical help for term papers, essays and theses — how to cite your sources correctly, build a bibliography, sharpen a thesis statement, and write without plagiarising. Reflects the current editions: <strong>APA 7</strong>, <strong>MLA 9</strong> and <strong>Chicago 18</strong>.</p>
</div>
<div class="cards">{wcards}</div>
<p class="study-note" style="margin-top:18px">Tip: use the <a href="../Karo Convert.html#ask">Study search</a> to find trusted, ad-free sources, then come back here to cite them correctly.</p>
{cta(1,"Need a quick fact or conversion?","The converter and study search are a tap away.")}""",1)

WDISC='<hr class="rule"><p class="small muted">These guides explain the current editions in plain language and are a study aid, not official style manuals. For exact rules and edge cases, check your assignment brief and the official APA, MLA or Chicago guidance — and when in doubt, ask your instructor.</p>'

# 1 — citation styles explained
qa=[("Which citation style should I use?","Follow your assignment brief first. By discipline: <strong>APA</strong> for social sciences, education, nursing and business; <strong>MLA</strong> for English and the humanities; <strong>Chicago</strong> for history, the arts and publishing; <strong>Harvard</strong> is common in the UK and Australia."),
("Can I mix two styles in one paper?","No. Pick one and use it consistently — mixing styles is one of the most common reasons work gets marked down."),
("Is Chicago 17th still acceptable?","Chicago’s 18th edition (2024) is current, but many courses and journals still use the 17th. Use whichever your instructor or publisher specifies."),
("How do I cite AI tools like ChatGPT?","APA 7, MLA 9 and Chicago 18 all now give guidance for AI-generated content: name the tool as the source, give the version and date, and say how you used it. Always check your school’s own policy first.")]
write("writing/citation-styles-explained.html","APA vs MLA vs Chicago vs Harvard — which to use (2026) | Karo Convert",
 "Compare the main citation styles — APA 7, MLA 9, Chicago 18 and Harvard — with the disciplines that use each, in-text formats, and the same source shown side by side.",
 f"""{crumb([("Home","../Karo Convert.html"),("Writing","./"),("Citation styles explained",None)])}
<article class="article"><div class="kicker">Citation</div>
<h1>APA vs MLA vs Chicago vs Harvard</h1>
<p class="lede">Four common styles, four sets of rules. Here’s what each is for, how they differ, and the same source written in each.</p>
<h2>Why citation styles exist</h2>
<p>Citing sources does three jobs: it gives credit to the people whose ideas you used, it lets readers find those sources, and it protects you from <a href="how-to-avoid-plagiarism.html">plagiarism</a>. Different fields adopted different styles, but they all carry the same core information — author, date, title and where to find it — in a different order.</p>
{table("The main styles at a glance",["Style","Typical fields","In-text","List is called","Current edition"],[["APA","Social sciences, nursing, business","(Author, Year)","References","7th (2020)"],["MLA","English, humanities","(Author 23)","Works Cited","9th (2021)"],["Chicago (notes)","History, arts, publishing","Footnote¹","Bibliography","18th (2024)"],["Harvard","UK / Australia, many fields","(Author Year)","Reference list","No single manual"]])}
<h2>The same book in three styles</h2>
<p>Using an illustrative book — <em>The Origins of Language</em> by Jordan Smith, published by Aldridge Press in 2020:</p>
{cite("APA 7","Smith, J. (2020). <em>The origins of language</em>. Aldridge Press.","In-text: <code>(Smith, 2020)</code>")}
{cite("MLA 9","Smith, Jordan. <em>The Origins of Language</em>. Aldridge Press, 2020.","In-text: <code>(Smith 14)</code>")}
{cite("Chicago 18 (notes-bibliography)","Smith, Jordan. <em>The Origins of Language</em>. Chicago: Aldridge Press, 2020.","Note: <code>1. Jordan Smith, The Origins of Language (Chicago: Aldridge Press, 2020), 14.</code>")}
<h2>How to choose</h2>
<p>Check the assignment brief or syllabus first — it almost always names a style. If it doesn’t, use the discipline norm in the table above. Then be consistent from the first citation to the last.</p>
{faq_block(qa)}{WDISC}</article>
{cta(1,"Find sources to cite","Use the Study search for trusted, ad-free sources.","../Karo Convert.html#ask")}""".replace('href="../Karo Convert.html"><svg','href="../Karo Convert.html#ask"><svg') if False else f"""{crumb([("Home","../Karo Convert.html"),("Writing","./"),("Citation styles explained",None)])}
<article class="article"><div class="kicker">Citation</div>
<h1>APA vs MLA vs Chicago vs Harvard</h1>
<p class="lede">Four common styles, four sets of rules. Here’s what each is for, how they differ, and the same source written in each.</p>
<h2>Why citation styles exist</h2>
<p>Citing sources does three jobs: it gives credit to the people whose ideas you used, it lets readers find those sources, and it protects you from <a href="how-to-avoid-plagiarism.html">plagiarism</a>. Different fields adopted different styles, but they all carry the same core information — author, date, title and where to find it — in a different order.</p>
{table("The main styles at a glance",["Style","Typical fields","In-text","List is called","Current edition"],[["APA","Social sciences, nursing, business","(Author, Year)","References","7th (2020)"],["MLA","English, humanities","(Author 23)","Works Cited","9th (2021)"],["Chicago (notes)","History, arts, publishing","Footnote¹","Bibliography","18th (2024)"],["Harvard","UK / Australia, many fields","(Author Year)","Reference list","No single manual"]])}
<h2>The same book in three styles</h2>
<p>Using an illustrative book — <em>The Origins of Language</em> by Jordan Smith, published by Aldridge Press in 2020:</p>
{cite("APA 7","Smith, J. (2020). <em>The origins of language</em>. Aldridge Press.","In-text: <code>(Smith, 2020)</code>")}
{cite("MLA 9","Smith, Jordan. <em>The Origins of Language</em>. Aldridge Press, 2020.","In-text: <code>(Smith 14)</code>")}
{cite("Chicago 18 (notes-bibliography)","Smith, Jordan. <em>The Origins of Language</em>. Chicago: Aldridge Press, 2020.","Note: <code>1. Jordan Smith, The Origins of Language (Chicago: Aldridge Press, 2020), 14.</code>")}
<h2>How to choose</h2>
<p>Check the assignment brief or syllabus first — it almost always names a style. If it doesn’t, use the discipline norm in the table above. Then be consistent from the first citation to the last.</p>
{faq_block(qa)}{WDISC}</article>
{cta(1,"Find sources to cite","Use the Study search for trusted, ad-free sources.")}""",1,
 jsonld(article_ld("APA vs MLA vs Chicago vs Harvard","Compare the main citation styles and when to use each.",f"{SITE}/writing/citation-styles-explained.html"),faq_ld(qa)))

# 2 — cite a website
qa=[("What if the website has no author?","Start with the title of the page instead, then the date and site. In-text, use a short form of the title in quotation marks."),
("What if there’s no date?","Use <strong>(n.d.)</strong> — “no date” — in APA. In MLA, simply give the access date at the end."),
("Do I need the access date?","MLA recommends an access date for pages that may change. APA only includes a retrieval date for content designed to change (like a live map or wiki)."),
("How do I cite a page with a long messy URL?","Use the clean, canonical link to the page itself. You don’t need tracking parameters after the “?”.")]
write("writing/how-to-cite-a-website.html","How to cite a website — APA, MLA & Chicago examples | Karo Convert",
 "How to cite a website in APA 7, MLA 9 and Chicago 18, with examples and what to do when there is no author or no date.",
 f"""{crumb([("Home","../Karo Convert.html"),("Writing","./"),("Cite a website",None)])}
<article class="article"><div class="kicker">Citation</div>
<h1>How to cite a website</h1>
<p class="lede">Web pages are the most-cited — and most mis-cited — source. Here’s the format in three styles, plus how to handle a missing author or date.</p>
<h2>What you need</h2>
<p>Gather as many of these as exist: <strong>author</strong> (person or organisation), <strong>date</strong> published or updated, <strong>page title</strong>, <strong>site name</strong>, and the <strong>URL</strong>.</p>
<h2>Examples</h2>
{cite("APA 7","Rivera, M. (2024, June 12). How photosynthesis works. ScienceLearn. https://example.org/photosynthesis","In-text: <code>(Rivera, 2024)</code>")}
{cite("MLA 9","Rivera, Maria. “How Photosynthesis Works.” <em>ScienceLearn</em>, 12 June 2024, example.org/photosynthesis. Accessed 3 Mar. 2026.","In-text: <code>(Rivera)</code>")}
{cite("Chicago 18 (notes-bibliography)","Rivera, Maria. “How Photosynthesis Works.” ScienceLearn. June 12, 2024. https://example.org/photosynthesis.","Note: <code>1. Maria Rivera, “How Photosynthesis Works,” ScienceLearn, June 12, 2024, https://example.org/photosynthesis.</code>")}
<h2>No author or no date</h2>
<p>If there’s no author, lead with the page title. If there’s no date, APA uses <strong>(n.d.)</strong>; MLA relies on the access date. Never invent a date or author — leave it out and adjust the order.</p>
{faq_block(qa)}{WDISC}</article>
{cta(1,"Find a better source","The Study search returns trusted, ad-free pages you can cite.")}""",1,
 jsonld(article_ld("How to cite a website","Cite a website in APA, MLA and Chicago.",f"{SITE}/writing/how-to-cite-a-website.html"),faq_ld(qa)))

# 3 — cite wikipedia
qa=[("Can I cite Wikipedia in an academic paper?","Often you shouldn’t use it as a main source — many instructors treat encyclopedias as background, not evidence. The better move is to use Wikipedia to <em>find</em> reliable sources (check the references at the bottom of the article) and cite those directly."),
("If I do cite Wikipedia, how?","Cite the specific article and, importantly, link the <strong>permanent version</strong> so the page can’t change under your reader (see below)."),
("How do I get a Wikipedia article’s permanent link?","Open the article’s <em>View history</em> (or “Cite this page”) and copy the link to the dated version. APA recommends using this archived URL."),
("Does Wikipedia have an author?","Articles are written collectively, so there’s no single author. Begin the citation with the article title instead.")]
write("writing/how-to-cite-wikipedia.html","How to cite Wikipedia in APA & MLA (the right way) | Karo Convert",
 "Should you cite Wikipedia? How to do it properly in APA 7 and MLA 9, why you should link the permanent version, and the smarter way to use it for research.",
 f"""{crumb([("Home","../Karo Convert.html"),("Writing","./"),("Cite Wikipedia",None)])}
<article class="article"><div class="kicker">Citation</div>
<h1>How to cite Wikipedia (properly)</h1>
<p class="lede">First, a tip that will save your grade: use Wikipedia to <em>find</em> sources, then cite those. But if you do cite the article itself, here’s how to do it right.</p>
<h2>The smarter approach</h2>
<p>Encyclopedias — including Wikipedia — are usually <strong>background reading</strong>, not evidence. Scroll to the <strong>References</strong> at the bottom of any article: those are the books, papers and reports the article is built on. Read and cite <em>those</em> primary sources directly. (The <a href="../Karo Convert.html#ask">Study search</a> can help you find trusted sources to begin with.)</p>
<h2>If you cite the article anyway</h2>
<p>Because anyone can edit Wikipedia, link the <strong>permanent version</strong> you actually read — open “View history” and copy the dated link. That way your reader sees the same text you did.</p>
{cite("APA 7","Photosynthesis. (2024, March 5). In <em>Wikipedia</em>. https://en.wikipedia.org/w/index.php?title=Photosynthesis&amp;oldid=1212000000","In-text: <code>(“Photosynthesis,” 2024)</code>")}
{cite("MLA 9","“Photosynthesis.” <em>Wikipedia</em>, Wikimedia Foundation, 5 Mar. 2024, en.wikipedia.org/wiki/Photosynthesis.","In-text: <code>(“Photosynthesis”)</code>")}
<h2>Why the permanent link matters</h2>
<p>A normal Wikipedia URL always points to the <em>latest</em> version, which may change tomorrow. The permanent (oldid) link freezes the exact version — APA specifically recommends it for sources that update.</p>
{faq_block(qa)}{WDISC}</article>
{cta(1,"Find sources with the Study search","Trusted, ad-free educational sources — including Wikipedia.")}""",1,
 jsonld(article_ld("How to cite Wikipedia","Cite Wikipedia correctly in APA and MLA, and use it wisely.",f"{SITE}/writing/how-to-cite-wikipedia.html"),faq_ld(qa)))

# 4 — cite a book
qa=[("How do I cite a book with two or more authors?","APA lists up to 20 authors with an ampersand before the last; MLA lists the first author then “et al.” for three or more; Chicago lists all in the bibliography."),
("How do I cite one chapter from an edited book?","Cite the chapter author and title, then “In [Editor] (Ed.), <em>Book title</em> (pages). Publisher.” (APA), adapting for MLA or Chicago."),
("Do I include the edition?","Yes, if it isn’t the first — e.g. “(3rd ed.)” in APA, “3rd ed.” in MLA, after the title."),
("Do I need the city of publication?","APA and MLA no longer require the city. Chicago still includes it.")]
write("writing/how-to-cite-a-book.html","How to cite a book — APA, MLA & Chicago examples | Karo Convert",
 "How to cite a book in APA 7, MLA 9 and Chicago 18, including multiple authors, editions and chapters in an edited book.",
 f"""{crumb([("Home","../Karo Convert.html"),("Writing","./"),("Cite a book",None)])}
<article class="article"><div class="kicker">Citation</div>
<h1>How to cite a book</h1>
<p class="lede">The format that started it all. Here’s a book in three styles, plus the rules for editions and multiple authors.</p>
<h2>What you need</h2><p><strong>Author(s)</strong>, <strong>year</strong>, <strong>title</strong> (italicised), <strong>edition</strong> if not the first, and <strong>publisher</strong>.</p>
<h2>Examples</h2>
{cite("APA 7","Smith, J. (2020). <em>The origins of language</em> (2nd ed.). Aldridge Press.","In-text: <code>(Smith, 2020, p. 14)</code>")}
{cite("MLA 9","Smith, Jordan. <em>The Origins of Language</em>. 2nd ed., Aldridge Press, 2020.","In-text: <code>(Smith 14)</code>")}
{cite("Chicago 18 (notes-bibliography)","Smith, Jordan. <em>The Origins of Language</em>. 2nd ed. Chicago: Aldridge Press, 2020.","Note: <code>1. Jordan Smith, The Origins of Language, 2nd ed. (Chicago: Aldridge Press, 2020), 14.</code>")}
<h2>A chapter in an edited book (APA)</h2>
{cite("APA 7","Okafor, L. (2019). Tone systems. In R. Vance (Ed.), <em>Studies in phonology</em> (pp. 55–78). Beacon Academic.")}
{faq_block(qa)}{WDISC}</article>
{cta(1,"Need a quick fact?","The converter and study search are a tap away.")}""",1,
 jsonld(article_ld("How to cite a book","Cite a book in APA, MLA and Chicago.",f"{SITE}/writing/how-to-cite-a-book.html"),faq_ld(qa)))

# 5 — cite a journal article
qa=[("What is a DOI and do I need it?","A DOI is a permanent link to an article (it starts with 10.). Include it whenever one exists — APA and MLA format it as a full https://doi.org/… link."),
("What if there’s no DOI?","Give the database name or a stable URL instead. For print-only articles, the volume, issue and page numbers are enough."),
("What do volume and issue mean?","Journals are published in numbered volumes (often one per year), each split into issues. Both appear in the citation, e.g. <em>vol. 12, no. 3</em>."),
("How do I shorten three or more authors?","APA uses “First Author et al.” in-text; MLA does the same in both the in-text citation and (for 3+) the Works Cited entry.")]
write("writing/how-to-cite-a-journal-article.html","How to cite a journal article — APA, MLA, Chicago + DOI | Karo Convert",
 "How to cite a journal article in APA 7, MLA 9 and Chicago 18, with the DOI explained and what to do when there isn’t one.",
 f"""{crumb([("Home","../Karo Convert.html"),("Writing","./"),("Cite a journal article",None)])}
<article class="article"><div class="kicker">Citation</div>
<h1>How to cite a journal article</h1>
<p class="lede">Scholarly articles are the gold-standard source — and they have a precise citation format. Here it is, with the DOI demystified.</p>
<h2>What you need</h2><p><strong>Author(s)</strong>, <strong>year</strong>, <strong>article title</strong>, <strong>journal name</strong> (italicised), <strong>volume(issue)</strong>, <strong>page range</strong>, and a <strong>DOI</strong> if one exists.</p>
<h2>Examples</h2>
{cite("APA 7","Okafor, L., &amp; Bray, T. (2021). Vowel length in tonal languages. <em>Journal of Phonology, 12</em>(3), 210–235. https://doi.org/10.1234/jphon.2021.0123","In-text: <code>(Okafor &amp; Bray, 2021)</code>")}
{cite("MLA 9","Okafor, Lina, and Tom Bray. “Vowel Length in Tonal Languages.” <em>Journal of Phonology</em>, vol. 12, no. 3, 2021, pp. 210–35. <em>JSTOR</em>, https://doi.org/10.1234/jphon.2021.0123.","In-text: <code>(Okafor and Bray 221)</code>")}
{cite("Chicago 18 (author-date)","Okafor, Lina, and Tom Bray. 2021. “Vowel Length in Tonal Languages.” <em>Journal of Phonology</em> 12 (3): 210–35. https://doi.org/10.1234/jphon.2021.0123.","In-text: <code>(Okafor and Bray 2021, 221)</code>")}
<h2>The DOI</h2>
<p>A <strong>DOI</strong> (digital object identifier) is a permanent address for an article — it won’t break like an ordinary link. If the article has one, always include it as a full <code>https://doi.org/…</code> link.</p>
{faq_block(qa)}{WDISC}</article>
{cta(1,"Find sources","Use the Study search to start your research.")}""",1,
 jsonld(article_ld("How to cite a journal article","Cite a journal article in APA, MLA and Chicago.",f"{SITE}/writing/how-to-cite-a-journal-article.html"),faq_ld(qa)))

# 6 — bibliography vs works cited vs references
qa=[("Is a bibliography the same as a Works Cited?","Not quite. A <strong>Works Cited</strong> (MLA) or <strong>References</strong> (APA) lists only the sources you actually cited. A <strong>bibliography</strong> can also include background reading you consulted but didn’t cite."),
("What is an annotated bibliography?","A bibliography where each entry is followed by a short paragraph (the annotation) summarising and evaluating the source."),
("What does APA call its list?","<strong>References</strong>. MLA calls it <strong>Works Cited</strong>; Chicago calls it a <strong>Bibliography</strong> (notes style) or <strong>Reference list</strong> (author-date)."),
("Do I list sources I read but didn’t cite?","In a Works Cited or References list, no — only cited works. In a full bibliography, you may.")]
write("writing/bibliography-vs-works-cited-vs-references.html","Bibliography vs Works Cited vs References — the difference | Karo Convert",
 "Bibliography, Works Cited and References explained: what each source list is called in APA, MLA and Chicago, and the real difference between them.",
 f"""{crumb([("Home","../Karo Convert.html"),("Writing","./"),("Bibliography vs Works Cited",None)])}
<article class="article"><div class="kicker">Citation</div>
<h1>Bibliography vs Works Cited vs References</h1>
<p class="lede">Three names for the list at the end of your paper — but they don’t mean exactly the same thing. Here’s the difference.</p>
<h2>The quick distinction</h2>
<p>A <strong>Works Cited</strong> (MLA) or <strong>References</strong> (APA) list contains <em>only</em> the sources you cited in the text. A <strong>bibliography</strong> is broader: it can also include works you read for background but didn’t cite.</p>
{table("What each style calls the list",["Style","Name of the list","Includes"],[["APA","References","Only works cited"],["MLA","Works Cited","Only works cited"],["Chicago (notes)","Bibliography","Cited + sometimes consulted"],["Chicago (author-date)","Reference list","Only works cited"],["Harvard","Reference list","Only works cited"]])}
<h2>Annotated bibliography</h2>
<p>Some assignments ask for an <strong>annotated bibliography</strong>: each source is followed by a few sentences summarising what it says and judging how useful or reliable it is. It’s great practice for <a href="how-to-evaluate-sources.html">evaluating sources</a>.</p>
<h2>Formatting basics</h2>
<p>Whatever it’s called, the list is usually alphabetical by author’s last name, double-spaced, with a <em>hanging indent</em> (the first line flush left, later lines indented). Keep one consistent style throughout.</p>
{faq_block(qa)}{WDISC}</article>
{cta(1,"Cite a source correctly","See our citation guides for APA, MLA and Chicago.")}""",1,
 jsonld(article_ld("Bibliography vs Works Cited vs References","The difference between the source lists in each style.",f"{SITE}/writing/bibliography-vs-works-cited-vs-references.html"),faq_ld(qa)))

# 7 — thesis statement
qa=[("Where does the thesis statement go?","Usually at the <strong>end of your introduction</strong>, so readers know your argument before the body begins."),
("How long should it be?","Normally one or two sentences. It should be specific enough to preview your whole argument, not a vague topic."),
("What’s the difference between a topic and a thesis?","A topic is what you’re writing about (“social media and sleep”). A thesis takes a <em>position</em> on it (“Evening social-media use harms teenage sleep by delaying melatonin release”)."),
("Can my thesis change as I write?","Yes — it’s normal to refine it once your research and argument take shape. Update the statement to match your final paper.")]
write("writing/how-to-write-a-thesis-statement.html","How to write a thesis statement — formula & examples | Karo Convert",
 "Write a strong thesis statement using a simple formula, with weak-vs-strong examples and the three main types (argumentative, analytical, expository).",
 f"""{crumb([("Home","../Karo Convert.html"),("Writing","./"),("Thesis statement",None)])}
<article class="article"><div class="kicker">Writing</div>
<h1>How to write a thesis statement</h1>
<p class="lede">Your thesis is the one sentence your whole paper defends. Here’s a formula, and the difference between a weak and a strong one.</p>
<h2>A simple formula</h2>
<div class="formula">[specific topic] + [your claim] + [main reasons / how]</div>
<p>A good thesis is <strong>specific</strong>, <strong>arguable</strong> (someone could reasonably disagree) and <strong>focused</strong> enough to cover in your paper.</p>
<h2>Weak vs strong</h2>
<div class="callout"><div class="lbl">Weak</div><p style="margin:0">“Social media affects teenagers.” <span class="muted">— too vague, and no one would disagree.</span></p></div>
<div class="callout"><div class="lbl">Strong</div><p style="margin:0">“Evening social-media use harms teenage sleep by delaying melatonin release, so schools should teach screen-curfew habits.” <span class="muted">— specific, arguable, and previews the reasons.</span></p></div>
<h2>Three common types</h2>
<ul>
<li><strong>Argumentative:</strong> takes a side and defends it (most essays).</li>
<li><strong>Analytical:</strong> breaks a topic down and explains how the parts relate.</li>
<li><strong>Expository:</strong> explains a topic clearly without arguing a position.</li>
</ul>
<p>Place the finished statement at the end of your introduction, then make sure every body paragraph supports it — see <a href="how-to-structure-a-research-paper.html">how to structure a paper</a>.</p>
{faq_block(qa)}{WDISC}</article>
{cta(1,"Research your topic","Use the Study search to find trusted sources fast.")}""",1,
 jsonld(article_ld("How to write a thesis statement","A formula and examples for a strong thesis statement.",f"{SITE}/writing/how-to-write-a-thesis-statement.html"),faq_ld(qa)))

# 8 — structure a research paper
qa=[("What’s a basic research-paper structure?","Introduction (hook, background, thesis) → body paragraphs (one idea each, with evidence and analysis) → conclusion → reference list."),
("How long should each part be?","As a rough guide, the introduction and conclusion are about 10% each, leaving roughly 80% for the body. Follow any length rules in your brief."),
("What goes in a body paragraph?","Start with a topic sentence, give evidence (with a citation), explain how it supports your thesis, then link to the next point."),
("Should I write the introduction first?","Many writers draft it last, once they know exactly what the paper argues. An outline first, though, always helps.")]
write("writing/how-to-structure-a-research-paper.html","How to structure a research paper — outline & template | Karo Convert",
 "A clear structure for term papers and research papers: introduction with a thesis, evidence-based body paragraphs, a conclusion and references — with an outline you can reuse.",
 f"""{crumb([("Home","../Karo Convert.html"),("Writing","./"),("Structure a research paper",None)])}
<article class="article"><div class="kicker">Writing</div>
<h1>How to structure a research paper</h1>
<p class="lede">Most term papers follow the same skeleton. Get the structure right and the writing gets much easier.</p>
<h2>The standard shape</h2>
<ol>
<li><strong>Introduction</strong> — a hook, brief background, and your <a href="how-to-write-a-thesis-statement.html">thesis statement</a> at the end.</li>
<li><strong>Body paragraphs</strong> — one idea each: topic sentence → evidence (with a citation) → your analysis → a link to the next point.</li>
<li><strong>Counterargument</strong> (for argumentative papers) — fairly state an opposing view, then respond to it.</li>
<li><strong>Conclusion</strong> — restate the thesis in fresh words, draw the points together, and end with why it matters. Don’t add new evidence here.</li>
<li><strong>References / Works Cited</strong> — every source you cited, in one consistent style.</li>
</ol>
<h2>A reusable outline</h2>
<div class="formula">I. Introduction → thesis<br>II. Point 1 → evidence + analysis<br>III. Point 2 → evidence + analysis<br>IV. Point 3 → evidence + analysis<br>V. Counterargument + response<br>VI. Conclusion<br>VII. References</div>
<h2>Tips that save rewrites</h2>
<p>Outline before you draft. Make sure every paragraph supports the thesis — if one doesn’t, cut it or fix the thesis. Cite as you write so you never lose a source, and keep one citation style throughout. When you need a fact or figure, the <a href="../Karo Convert.html">converter</a> and <a href="../Karo Convert.html#ask">Study search</a> are a tap away.</p>
{faq_block(qa)}{WDISC}</article>
{cta(1,"Start your research","Find trusted, ad-free sources with the Study search.")}""",1,
 jsonld(article_ld("How to structure a research paper","An outline and template for term papers.",f"{SITE}/writing/how-to-structure-a-research-paper.html"),faq_ld(qa)))

# 9 — avoid plagiarism
qa=[("What counts as plagiarism?","Using someone else’s words, ideas, data or structure without crediting them — whether you meant to or not. Copying, close paraphrasing without a citation, and reusing your own past work without permission all count."),
("Do I cite when I paraphrase?","Yes. Putting an idea in your own words still requires a citation, because the idea isn’t yours. Only quoting needs quotation marks <em>and</em> a citation."),
("What is ‘common knowledge’ that I don’t cite?","Widely known, undisputed facts (e.g. “water boils at 100°C at sea level”). If it’s specific, surprising, or arguable, cite it."),
("Will paraphrasing avoid plagiarism on its own?","No — swapping a few words is “patchwriting” and still counts. True paraphrasing rewrites the idea fully <em>and</em> includes a citation.")]
write("writing/how-to-avoid-plagiarism.html","How to avoid plagiarism — quote, paraphrase & cite | Karo Convert",
 "Avoid plagiarism by knowing when to quote, paraphrase or summarise — and exactly when a citation is required, with the common-knowledge exception explained.",
 f"""{crumb([("Home","../Karo Convert.html"),("Writing","./"),("Avoid plagiarism",None)])}
<article class="article"><div class="kicker">Writing</div>
<h1>How to avoid plagiarism</h1>
<p class="lede">Most plagiarism is accidental — a missing citation or a too-close paraphrase. Here’s how to stay clear of it.</p>
<h2>The three ways to use a source</h2>
<ul>
<li><strong>Quote</strong> — use the exact words in quotation marks, with a citation. Best for precise wording or definitions; use sparingly.</li>
<li><strong>Paraphrase</strong> — restate one idea fully in your own words and sentence structure, with a citation.</li>
<li><strong>Summarise</strong> — condense a longer passage into the key point, in your own words, with a citation.</li>
</ul>
<p>The rule of thumb: <strong>if the idea, data or wording isn’t yours, cite it</strong> — even when you paraphrase.</p>
<h2>The traps</h2>
<p><strong>Patchwriting</strong> (swapping a few synonyms) is still plagiarism. So is forgetting the citation on a paraphrase, and <strong>self-plagiarism</strong> (reusing your own submitted work without permission). Read the source, then write the idea from memory in your own words to avoid copying its structure.</p>
<h2>The common-knowledge exception</h2>
<p>You don’t need to cite widely known, undisputed facts. But if a fact is specific, surprising or could be disputed, cite where you found it. When unsure, cite — it’s never wrong to give credit.</p>
{faq_block(qa)}{WDISC}</article>
{cta(1,"Cite your sources right","Browse our APA, MLA and Chicago guides.")}""",1,
 jsonld(article_ld("How to avoid plagiarism","Quote, paraphrase and cite correctly to avoid plagiarism.",f"{SITE}/writing/how-to-avoid-plagiarism.html"),faq_ld(qa)))

# 10 — evaluate sources
qa=[("What makes a source credible?","Check who wrote it and their expertise, whether it’s current, whether claims are backed by evidence, and whether it’s trying to inform rather than sell. A quick checklist is currency, relevance, authority, accuracy and purpose."),
("What’s the difference between primary and secondary sources?","A <strong>primary</strong> source is original or first-hand (data, a diary, an experiment, an artwork). A <strong>secondary</strong> source interprets or analyses primary ones (a review article, a textbook). Tertiary sources, like encyclopedias, summarise both."),
("Are scholarly sources always better?","For most academic work, peer-reviewed scholarly sources carry the most weight, but a reputable news outlet or government report can be exactly right depending on your question."),
("Is Wikipedia a reliable source?","It’s a great <em>starting point</em> to understand a topic and find references, but it’s tertiary — cite the primary and scholarly sources it points to instead.")]
write("writing/how-to-evaluate-sources.html","How to evaluate sources — a credibility checklist | Karo Convert",
 "Judge whether a source is credible with a simple checklist (currency, relevance, authority, accuracy, purpose), and learn the difference between primary and secondary sources.",
 f"""{crumb([("Home","../Karo Convert.html"),("Writing","./"),("Evaluate sources",None)])}
<article class="article"><div class="kicker">Research</div>
<h1>How to evaluate sources</h1>
<p class="lede">Good papers are built on good sources. Here’s a fast way to judge whether a source is worth citing.</p>
<h2>A five-point checklist</h2>
<ul>
<li><strong>Currency</strong> — is it recent enough for your topic?</li>
<li><strong>Relevance</strong> — does it actually address your question, at the right depth?</li>
<li><strong>Authority</strong> — who wrote it, and what’s their expertise? Who published it?</li>
<li><strong>Accuracy</strong> — are claims supported by evidence you can check?</li>
<li><strong>Purpose</strong> — is it meant to inform, or to sell or persuade?</li>
</ul>
<h2>Primary, secondary, tertiary</h2>
<p>A <strong>primary</strong> source is first-hand (raw data, a letter, an experiment). A <strong>secondary</strong> source analyses primary ones (a journal review, a textbook). A <strong>tertiary</strong> source summarises the field (an encyclopedia). Strong papers lean on primary and peer-reviewed secondary sources.</p>
<h2>Where the Study search fits</h2>
<p>The <a href="../Karo Convert.html#ask">Study search</a> deliberately returns results only from trusted, ad-free educational sources, so you start from solid ground. Use it to orient yourself, then follow the references to primary and scholarly work — and cite <em>those</em>.</p>
{faq_block(qa)}{WDISC}</article>
{cta(1,"Find credible sources","The Study search keeps you on trusted ground.")}""",1,
 jsonld(article_ld("How to evaluate sources","A credibility checklist and primary vs secondary sources.",f"{SITE}/writing/how-to-evaluate-sources.html"),faq_ld(qa)))

# ============================== robots + sitemap ==============================
pages = ["Karo Convert.html","about.html","privacy.html","terms.html","contact.html","guides/","writing/"] + ["guides/"+g[0] for g in GUIDES] + ["writing/"+w[0] for w in WRITING]
urls = "".join(f"  <url><loc>{SITE}/{p}</loc><changefreq>monthly</changefreq></url>\n" for p in dict.fromkeys(pages))
open(os.path.join(OUT,"sitemap.xml"),"w").write(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n')
open(os.path.join(OUT,"robots.txt"),"w").write(f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n")
print("wrote sitemap.xml + robots.txt")
print("DONE")
