// test/flow.py — drives the real payment flow against the mock server.
import json, sys
from playwright.sync_api import sync_playwright

BASE = "http://localhost:8799/"
results = []
def check(name, cond, detail=""):
    results.append((("PASS" if cond else "FAIL"), name, str(detail)))

with sync_playwright() as p:
    b = p.chromium.launch(args=["--no-sandbox"])
    ctx = b.new_context(viewport={"width":420,"height":900})
    pg = ctx.new_page()
    errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.goto(BASE, wait_until="networkidle"); pg.wait_for_timeout(600)

    # 1. API configured + ad slot visible for anon (no payment)
    configured = pg.evaluate("window.ITC_PAY && ITC_PAY.configured()")
    check("ITC_PAY sees API base (configured)", configured is True, configured)
    ad1 = pg.eval_on_selector(".promo-area","el=>getComputedStyle(el).display")
    check("Ad slot visible before payment", ad1 != "none", ad1)
    sup0 = pg.evaluate("ITC_PAY.isSupporter()")
    check("Not a supporter at start", sup0 is False, sup0)

    # 2. Open donate modal, check pay label tracks amount
    pg.click(".gobtn"); pg.wait_for_timeout(300)
    lbl1 = pg.inner_text("#paybtn-lbl")
    check("Pay label shows $1 default", "$1" in lbl1, lbl1)
    pg.click('.plan[data-plan="custom"]'); pg.fill("#customval","5"); pg.wait_for_timeout(200)
    lbl2 = pg.inner_text("#paybtn-lbl")
    check("Pay label updates to custom $5", "$5" in lbl2, lbl2)
    pg.click('.plan[data-plan="donate"]'); pg.wait_for_timeout(150)
    lbl3 = pg.inner_text("#paybtn-lbl")
    check("Pay label back to $1", "$1" in lbl3, lbl3)

    # 3. Pay -> (mock Stripe) -> redirect back -> verify -> ad-free
    pg.click("#paybtn")
    pg.wait_for_url("**/?*", timeout=4000)          # came back from "Stripe"
    pg.wait_for_timeout(900)                         # let verify() resolve
    sup1 = pg.evaluate("ITC_PAY.isSupporter()")
    check("Supporter TRUE after verified payment", sup1 is True, sup1)
    ad2 = pg.eval_on_selector(".promo-area","el=>getComputedStyle(el).display")
    check("Ad slot hidden after payment", ad2 == "none", ad2)
    pill = pg.eval_on_selector_all(".adfreepill","els=>els.length")
    check("'Ad-free' indicator shown (paid, not signed in)", pill==1, f"count={pill}")
    clean = pg.evaluate("location.search")
    check("URL cleaned after redirect", clean=="", repr(clean))

    # 4. Persistence: reload with NO query -> still verified via stored session
    pg.goto(BASE, wait_until="networkidle"); pg.wait_for_timeout(900)
    sup2 = pg.evaluate("ITC_PAY.isSupporter()")
    check("Ad-free PERSISTS across reload (re-verified)", sup2 is True, sup2)
    ad3 = pg.eval_on_selector(".promo-area","el=>getComputedStyle(el).display")
    check("Ad slot still hidden after reload", ad3=="none", ad3)

    # 5. SECURITY: hand-edit localStorage to fake supporter w/ bad session -> server downgrades
    pg.evaluate("""() => {
        localStorage.setItem('itc-entitlement', JSON.stringify({supporter:true, plan:'HACKED'}));
        localStorage.setItem('itc-stripe-session', 'cs_FAKE_not_paid');
    }""")
    pg.goto(BASE, wait_until="networkidle"); pg.wait_for_timeout(900)
    supX = pg.evaluate("ITC_PAY.isSupporter()")
    check("Faked localStorage is REJECTED by server", supX is False, supX)
    adX = pg.eval_on_selector(".promo-area","el=>getComputedStyle(el).display")
    check("Ads RESTORED for unverified faker", adX!="none", adX)

    # 6. Sign-in is INDEPENDENT of ad-free (identity only)
    pg.evaluate("ITC_USER.signIn('google',{name:'Test',email:'t@gmail.com',plan:''})")
    pg.wait_for_timeout(400)
    supS = pg.evaluate("ITC_PAY.isSupporter()")
    check("Signing in does NOT grant ad-free", supS is False, supS)
    adS = pg.eval_on_selector(".promo-area","el=>getComputedStyle(el).display")
    check("Ads still shown for signed-in non-payer", adS!="none", adS)
    avatar = pg.eval_on_selector_all("#acctwrap .avatar","els=>els.length")
    check("Signed-in avatar appears", avatar==1, f"count={avatar}")

    check("No uncaught JS errors during flow", len(errs)==0, errs)
    b.close()

print(json.dumps([{"status":s,"test":t,"detail":d} for s,t,d in results], indent=1))
n=sum(1 for s,_,_ in results if s=="PASS"); print(f"\n{n}/{len(results)} PASSED")
sys.exit(0 if n==len(results) else 1)
