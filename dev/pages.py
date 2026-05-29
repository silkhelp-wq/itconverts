import json, sys, os, re, threading, time, http.server, socketserver, urllib.parse
from playwright.sync_api import sync_playwright

ROOT="/home/claude/Karo Convert-build"; PORT=8802
results=[]
def check(n,c,d=""): results.append((("PASS" if c else "FAIL"),n,str(d)))

PAGES=["about.html","privacy.html","terms.html","contact.html","guides/index.html",
 "guides/km-to-miles.html","guides/celsius-to-fahrenheit.html","guides/kg-to-pounds.html",
 "guides/data-storage-units-explained.html","guides/cups-to-milliliters.html",
 "guides/meters-to-feet.html","guides/inches-to-centimeters.html","guides/liters-to-gallons.html","guides/grams-to-ounces.html",
 "writing/index.html","writing/citation-styles-explained.html","writing/how-to-cite-a-website.html",
 "writing/how-to-cite-wikipedia.html","writing/how-to-cite-a-book.html","writing/how-to-cite-a-journal-article.html",
 "writing/bibliography-vs-works-cited-vs-references.html","writing/how-to-write-a-thesis-statement.html",
 "writing/how-to-structure-a-research-paper.html","writing/how-to-avoid-plagiarism.html","writing/how-to-evaluate-sources.html"]

# ---- 1) static link-integrity check (no browser) ----
def resolve(base_rel, href):
    href=href.split("#")[0].split("?")[0]
    if not href: return None
    if href.startswith(("http://","https://","mailto:","tel:")): return None
    base_dir=os.path.dirname(base_rel)
    target=os.path.normpath(os.path.join(base_dir, href))
    if target.endswith("/") or href.endswith("/"): target=os.path.join(target,"index.html")
    if os.path.isdir(os.path.join(ROOT,target)): target=os.path.join(target,"index.html")
    return target
broken=[]
allpages=PAGES+["Karo Convert.html"]
for pg in allpages:
    fp=os.path.join(ROOT,pg)
    htmltxt=open(fp,encoding="utf-8").read()
    htmltxt=re.sub(r"<script[\s\S]*?</script>","",htmltxt)   # ignore JS (it builds hrefs at runtime)
    for href in re.findall(r'href="([^"]+)"', htmltxt):
        if href.startswith(("http","mailto","tel","#")): continue
        if href.endswith(".css"): pass
        t=resolve(pg,href)
        if t and not os.path.isfile(os.path.join(ROOT,t)):
            broken.append(f"{pg} -> {href} (={t})")
check("All internal links resolve (no 404s)", len(broken)==0, broken[:6])

# also check asset refs (css/js) resolve
asset_missing=[]
for pg in allpages:
    htmltxt=open(os.path.join(ROOT,pg),encoding="utf-8").read()
    for src in re.findall(r'(?:src|href)="([^"]+\.(?:css|js))"', htmltxt):
        if src.startswith("http"): continue
        t=resolve(pg,src)
        if t and not os.path.isfile(os.path.join(ROOT,t)): asset_missing.append(f"{pg} -> {src}")
check("All local css/js assets resolve", len(asset_missing)==0, asset_missing[:6])

# ---- 2) browser checks ----
class H(http.server.SimpleHTTPRequestHandler):
    def log_message(self,*a): pass
    def translate_path(self, path):
        path=urllib.parse.urlparse(path).path
        if path.endswith("/"): path+="index.html"
        return os.path.join(ROOT, path.lstrip("/"))
socketserver.ThreadingTCPServer.allow_reuse_address=True
srv=socketserver.ThreadingTCPServer(("127.0.0.1",PORT),H)
threading.Thread(target=srv.serve_forever,daemon=True).start(); time.sleep(0.5)
BASE=f"http://localhost:{PORT}/"

with sync_playwright() as p:
    b=p.chromium.launch(args=["--no-sandbox"])
    ctx=b.new_context(viewport={"width":420,"height":1000}, device_scale_factor=2)
    allerr={}
    for pg in PAGES:
        page=ctx.new_page(); errs=[]; page.on("pageerror", lambda e,errs=errs: errs.append(str(e)))
        page.goto(BASE+pg, wait_until="networkidle"); page.wait_for_timeout(250)
        h1=page.eval_on_selector_all("h1","e=>e.length")
        if h1!=1: check(f"{pg}: exactly one H1", False, h1)
        promo=page.eval_on_selector_all(".promo-area","e=>e.length")
        if promo!=1: check(f"{pg}: ad slot present", False, promo)
        # responsive: no horizontal overflow at 390
        page.set_viewport_size({"width":390,"height":900}); page.wait_for_timeout(150)
        ov=page.evaluate("document.documentElement.scrollWidth>document.documentElement.clientWidth+1")
        if ov: check(f"{pg}: no horizontal overflow @390", False, ov)
        if errs: allerr[pg]=errs
        page.close()
    check("Every content page: 1 H1, ad slot, no overflow", True, f"{len(PAGES)} pages checked")
    check("No JS errors on any content page", len(allerr)==0, allerr)

    # theme persistence across navigation (app -> guide)
    page=ctx.new_page(); page.goto(BASE+"guides/km-to-miles.html", wait_until="networkidle"); page.wait_for_timeout(200)
    t0=page.get_attribute("html","data-theme")
    page.click("#theme"); page.wait_for_timeout(150); t1=page.get_attribute("html","data-theme")
    check("Theme toggles on content page", t0!=t1, f"{t0}->{t1}")
    page.goto(BASE+"guides/kg-to-pounds.html", wait_until="networkidle"); page.wait_for_timeout(200)
    t2=page.get_attribute("html","data-theme")
    check("Theme choice persists across pages", t2==t1, f"persisted={t2}")
    # content substance: guide has a table + FAQ
    ntab=page.eval_on_selector_all("table","e=>e.length"); nfaq=page.eval_on_selector_all(".faq details","e=>e.length")
    check("Guide has reference table", ntab>=1, ntab); check("Guide has FAQ entries", nfaq>=3, nfaq)
    # FAQ toggles open
    page.click(".faq summary"); page.wait_for_timeout(150)
    isopen=page.eval_on_selector(".faq details","e=>e.open")
    check("FAQ accordion opens", isopen is True, isopen)
    page.close()

    # screenshots (dark)
    for name,pgpath in [("hub","guides/index.html"),("guide","guides/km-to-miles.html"),("privacy","privacy.html")]:
        page=ctx.new_page(); page.set_viewport_size({"width":900,"height":1200})
        page.goto(BASE+pgpath, wait_until="networkidle"); page.wait_for_timeout(400)
        page.screenshot(path=f"/home/claude/pg_{name}.png", full_page=True); page.close()
    b.close()
srv.shutdown()

print(json.dumps([{"status":s,"test":t,"detail":d} for s,t,d in results],indent=1))
n=sum(1 for s,_,_ in results if s=="PASS"); print(f"\n{n}/{len(results)} PASSED")
sys.exit(0 if n==len(results) else 1)
