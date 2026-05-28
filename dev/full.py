import json, sys, threading, time, http.server, socketserver, os, urllib.parse
from playwright.sync_api import sync_playwright

ROOT = "/home/claude/itconverts-build"
PORT = 8801
PAID_ID = "cs_test_mock_123"

# ---- in-process server: static files + mock Stripe API (no shell backgrounding) ----
class H(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass
    def _json(self, obj, code=200):
        b = json.dumps(obj).encode()
        self.send_response(code); self.send_header("Content-Type","application/json")
        self.send_header("Access-Control-Allow-Origin","*"); self.send_header("Content-Length",str(len(b)))
        self.end_headers(); self.wfile.write(b)
    def do_GET(self):
        u = urllib.parse.urlparse(self.path)
        if u.path == "/api/verify-session":
            q = urllib.parse.parse_qs(u.query); paid = q.get("session_id",[""])[0] == PAID_ID
            return self._json({"supporter":paid, "plan":"$1 supporter" if paid else ""})
        path = "/itconverts.html" if u.path == "/" else u.path
        fp = os.path.join(ROOT, path.lstrip("/"))
        if not os.path.isfile(fp): self.send_response(404); self.end_headers(); return
        data = open(fp,"rb").read()
        if fp.endswith(".html"):
            data = data.replace(b'API_BASE:       ""', b'API_BASE: "/api"')
        ctype = "text/html" if fp.endswith(".html") else ("text/javascript" if fp.endswith(".js") else "application/octet-stream")
        self.send_response(200); self.send_header("Content-Type",ctype); self.send_header("Content-Length",str(len(data)))
        self.end_headers(); self.wfile.write(data)
    def do_POST(self):
        u = urllib.parse.urlparse(self.path)
        if u.path == "/api/create-checkout-session":
            ln = int(self.headers.get("Content-Length",0)); body = self.rfile.read(ln).decode() if ln else "{}"
            success = "http://localhost:%d/?paid=1&session_id={CHECKOUT_SESSION_ID}" % PORT
            try:
                j = json.loads(body); success = j.get("success_url", success)
            except: pass
            return self._json({"url": success.replace("{CHECKOUT_SESSION_ID}", PAID_ID), "id": PAID_ID})
        self.send_response(404); self.end_headers()

socketserver.ThreadingTCPServer.allow_reuse_address = True
srv = socketserver.ThreadingTCPServer(("127.0.0.1", PORT), H)
threading.Thread(target=srv.serve_forever, daemon=True).start()
time.sleep(0.6)
BASE = "http://localhost:%d/" % PORT

# ---- mock Wikimedia REST responses (per host, to verify interleaving + labels) ----
def wiki_pages(host):
    if "wikibooks" in host:
        return {"pages":[{"id":11,"key":"Algebra","title":"Algebra (textbook)","excerpt":"An open <span class='searchmatch'>textbook</span>","description":"open book","thumbnail":None}]}
    if "wiktionary" in host:
        return {"pages":[{"id":21,"key":"photosynthesis","title":"photosynthesis","excerpt":"<b>definition</b> of the word","description":"noun","thumbnail":None}]}
    return {"pages":[
        {"id":1,"key":"Photosynthesis","title":"Photosynthesis","excerpt":"<span class='searchmatch'>Photosynthesis</span> is the process used by plants","description":"biological process","thumbnail":{"url":"//upload.wikimedia.org/x.jpg","width":48,"height":48}},
        {"id":2,"key":"Chlorophyll","title":"Chlorophyll","excerpt":"green pigment","description":"pigment","thumbnail":None}
    ]}

results = []
def check(n, c, d=""): results.append((("PASS" if c else "FAIL"), n, str(d)))

with sync_playwright() as p:
    b = p.chromium.launch(args=["--no-sandbox"])
    ctx = b.new_context(viewport={"width":430,"height":1000}, device_scale_factor=2)
    pg = ctx.new_page()
    errs=[]; pg.on("pageerror", lambda e: errs.append(str(e)))

    # intercept Wikimedia search calls
    def handle_wiki(route):
        host = urllib.parse.urlparse(route.request.url).hostname
        route.fulfill(status=200, content_type="application/json",
                      headers={"Access-Control-Allow-Origin":"*"}, body=json.dumps(wiki_pages(host)))
    ctx.route("**/w/rest.php/v1/search/page*", handle_wiki)

    pg.goto(BASE, wait_until="networkidle"); pg.wait_for_timeout(600)

    # ---- A. Rename + structure ----
    h2 = pg.inner_text(".ask-top h2")
    check("Section renamed to 'Study search'", h2.strip()=="Study search", h2)
    check("No 'AI' chip remains", pg.eval_on_selector_all(".ai-chip","e=>e.length")==0)
    check("Language picker present", pg.eval_on_selector_all("#asklang","e=>e.length")==1)
    check("Saved-searches button present", pg.eval_on_selector_all("#savedbtn","e=>e.length")==1)

    # ---- B. Run a curated search ----
    pg.fill("#askq","photosynthesis"); pg.press("#askq","Enter")
    pg.wait_for_selector(".result", timeout=4000); pg.wait_for_timeout(300)
    nres = pg.eval_on_selector_all(".result","e=>e.length")
    check("Results render (interleaved across sources)", nres>=3, f"{nres} cards")
    titles = pg.eval_on_selector_all(".result .rtitle","els=>els.map(e=>e.textContent)")
    check("Wikipedia result present", any("Photosynthesis"==t for t in titles), titles)
    check("Wikibooks result present", any("textbook" in t for t in titles), titles)
    first_site = pg.eval_on_selector(".result .rsite","e=>e.textContent")
    check("Source label shown on card", first_site in ("Wikipedia","Wikibooks","Wiktionary"), first_site)
    snip = pg.eval_on_selector(".result .rsnip","e=>e.textContent")
    check("Snippet is plain text (HTML stripped)", "<" not in snip and len(snip)>0, snip)
    # all result links must be educational hosts
    hrefs = pg.eval_on_selector_all(".result .rtitle","els=>els.map(e=>e.getAttribute('href'))")
    eduhosts = ("wikipedia.org","wikibooks.org","wiktionary.org")
    check("Every result links to an educational host", all(any(h in u for h in eduhosts) for u in hrefs), hrefs)

    # ---- C. Save flow (device-local) ----
    pg.click("#savethis"); pg.wait_for_timeout(200)
    saved_on = pg.eval_on_selector("#savethis","e=>e.classList.contains('on')")
    check("Save toggles ON", saved_on is True, saved_on)
    cnt = pg.inner_text("#savedbtn-lbl")
    check("Saved count shows (1)", "(1)" in cnt, cnt)
    pg.click("#savedbtn"); pg.wait_for_timeout(300)  # open saved modal
    entry = pg.eval_on_selector_all("#ov-history .hentry","e=>e.length")
    check("Saved modal lists the search", entry==1, f"{entry} entries")
    entry_q = pg.eval_on_selector("#ov-history .hl","e=>e.textContent")
    check("Saved entry shows the query", "photosynthesis" in entry_q.lower(), entry_q)
    # re-run from saved
    pg.click("#ov-history .hl"); pg.wait_for_timeout(700)
    check("Re-run from saved repopulates input", pg.input_value("#askq")=="photosynthesis", pg.input_value("#askq"))
    # persistence across reload
    pg.goto(BASE, wait_until="networkidle"); pg.wait_for_timeout(500)
    check("Saved searches persist across reload", "(1)" in pg.inner_text("#savedbtn-lbl"), pg.inner_text("#savedbtn-lbl"))

    # ---- D. Payment flow (the one I owe) ----
    ad1 = pg.eval_on_selector(".promo-area","e=>getComputedStyle(e).display")
    check("Ad slot visible before payment", ad1!="none", ad1)
    pg.click(".gobtn"); pg.wait_for_timeout(300)
    check("Pay label shows $1", "$1" in pg.inner_text("#paybtn-lbl"), pg.inner_text("#paybtn-lbl"))
    check("No sign-in buttons in modal (login-free)", pg.eval_on_selector_all(".prov","e=>e.length")==0)
    pg.click("#paybtn"); pg.wait_for_url("**/?*", timeout=5000); pg.wait_for_timeout(900)
    sup1 = pg.evaluate("ITC_PAY.isSupporter()")
    check("Supporter TRUE after verified payment", sup1 is True, sup1)
    ad2 = pg.eval_on_selector(".promo-area","e=>getComputedStyle(e).display")
    check("Ads hidden after payment", ad2=="none", ad2)
    check("'Ad-free' indicator shown", pg.eval_on_selector_all(".adfreepill","e=>e.length")==1)
    check("URL cleaned", pg.evaluate("location.search")=="", repr(pg.evaluate("location.search")))

    # persistence + security (re-verified server-side)
    pg.goto(BASE, wait_until="networkidle"); pg.wait_for_timeout(900)
    check("Ad-free persists across reload", pg.evaluate("ITC_PAY.isSupporter()") is True)
    pg.evaluate("""()=>{localStorage.setItem('itc-entitlement',JSON.stringify({supporter:true,plan:'HACK'}));localStorage.setItem('itc-stripe-session','cs_FAKE');}""")
    pg.goto(BASE, wait_until="networkidle"); pg.wait_for_timeout(900)
    check("Faked localStorage REJECTED by server", pg.evaluate("ITC_PAY.isSupporter()") is False, pg.evaluate("ITC_PAY.isSupporter()"))
    check("Ads restored for faker", pg.eval_on_selector(".promo-area","e=>getComputedStyle(e).display")!="none")

    # ---- E. screenshots ----
    srv_paid = pg.goto(BASE+"?study=1", wait_until="networkidle")
    pg.evaluate("localStorage.clear()"); pg.goto(BASE, wait_until="networkidle"); pg.wait_for_timeout(400)
    pg.fill("#askq","photosynthesis"); pg.press("#askq","Enter"); pg.wait_for_selector(".result"); pg.wait_for_timeout(400)
    pg.screenshot(path="/home/claude/shot_study.png", full_page=True)
    pg.click(".gobtn"); pg.wait_for_timeout(300)
    pg.screenshot(path="/home/claude/shot_donate.png", full_page=True)

    check("No uncaught JS errors", len(errs)==0, errs)
    b.close()

srv.shutdown()
print(json.dumps([{"status":s,"test":t,"detail":d} for s,t,d in results], indent=1))
n=sum(1 for s,_,_ in results if s=="PASS"); print(f"\n{n}/{len(results)} PASSED")
sys.exit(0 if n==len(results) else 1)
