#!/usr/bin/env python3
"""Provjera sajta: HTML, kontrast (WCAG), overflow, konzola, eksterni zahtjevi, zabranjene rijeci."""
import json, re, sys
from playwright.sync_api import sync_playwright

BASE = "http://127.0.0.1:8099"
ROUTES = ["/", "/en/"]
WIDTHS = [320, 360, 390, 414, 500, 768, 1024, 1280, 1440, 1920]

BANNED = ["Problemi sa kojima", "Zvuči poznato", "Pet koraka", "bez iznenađenja",
          "Dokazi", "Ovo nije marketinški", "Pitanja koja mi", "Ishod", "Outcome",
          "lokalno, bez clouda", "local, no cloud", "FAQPage",
          "Five steps", "Sound familiar", "Evidence", "For you", "Za tebe"]

# --- kontrast ---
def lum(c):
    def f(v):
        v /= 255.0
        return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
    return 0.2126 * f(c[0]) + 0.7152 * f(c[1]) + 0.0722 * f(c[2])

def ratio(fg, bg):
    l1, l2 = lum(fg), lum(bg)
    hi, lo = max(l1, l2), min(l1, l2)
    return (hi + 0.05) / (lo + 0.05)

def parse_rgb(s):
    m = re.findall(r"[\d.]+", s or "")
    return tuple(float(x) for x in m[:3]) if len(m) >= 3 else None

def eff_bg(page, el):
    """Nadji prvu neprovidnu pozadinu iduci ka roditelju."""
    return page.evaluate("""(el) => {
        let n = el;
        while (n && n !== document.documentElement) {
            const bg = getComputedStyle(n).backgroundColor;
            const a = bg.match(/[\\d.]+/g);
            if (a && (a.length < 4 || parseFloat(a[3]) > 0.5)) return bg;
            n = n.parentElement;
        }
        return getComputedStyle(document.body).backgroundColor;
    }""", el)

CONTRAST_JS = """() => {
  const out = [];
  const sels = ['h1','h2','h3','p','a','span','b','strong','li','em','summary','dt','dd','label'];
  document.querySelectorAll(sels.join(',')).forEach(el => {
    const t = (el.textContent || '').trim();
    if (!t || el.children.length > 0) return;
    const r = el.getBoundingClientRect();
    if (r.width < 2 || r.height < 2) return;
    const cs = getComputedStyle(el);
    if (cs.visibility === 'hidden' || cs.display === 'none' || parseFloat(cs.opacity) < 0.15) return;
    out.push({tag: el.tagName, cls: el.className || '', txt: t.slice(0, 40),
              fg: cs.color, size: parseFloat(cs.fontSize), weight: cs.fontWeight,
              bg: null, sel: el});
  });
  return out.map(({sel, ...r}) => r);
}"""

report = {}
with sync_playwright() as p:
    b = p.chromium.launch()
    for route in ROUTES:
        for scheme in ("light", "dark"):
            ctx = b.new_context(viewport={"width": 1440, "height": 900}, color_scheme=scheme)
            pg = ctx.new_page()
            errs, ext = [], []
            pg.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)
            pg.on("pageerror", lambda e: errs.append(str(e)))
            pg.on("request", lambda r: ext.append(r.url) if not r.url.startswith(BASE) and not r.url.startswith("data:") else None)
            pg.goto(BASE + route, wait_until="networkidle")
            key = f"{route}|{scheme}"

            # kontrast
            items = pg.evaluate(CONTRAST_JS)
            fails = []
            for it in items:
                bg = pg.evaluate("""(sel) => {
                    let n = document.querySelectorAll(sel.tagName.toLowerCase() + (sel.cls ? '.' + String(sel.cls).trim().split(/\\s+/).join('.') : ''))[0];
                }""", {"tagName": it["tag"], "cls": it["cls"]}) if False else None
            # jednostavnije: ponovo uzmi bg preko handle-a
            handles = pg.query_selector_all("h1,h2,h3,p,a,span,b,strong,li,em,summary,dt,dd,label")
            for h in handles:
                r = h.bounding_box()
                if not r or r["width"] < 2 or r["height"] < 2:
                    continue
                info = h.evaluate("""(el) => {
                    const t = (el.textContent || '').trim();
                    if (!t || el.children.length > 0) return null;
                    const cs = getComputedStyle(el);
                    if (cs.visibility === 'hidden' || cs.display === 'none') return null;
                    return {fg: cs.color, size: parseFloat(cs.fontSize), weight: cs.fontWeight, txt: t.slice(0, 36)};
                }""")
                if not info:
                    continue
                bg = eff_bg(pg, h)
                fg_c, bg_c = parse_rgb(info["fg"]), parse_rgb(bg)
                if not fg_c or not bg_c:
                    continue
                cr = ratio(fg_c, bg_c)
                large = info["size"] >= 24 or (info["size"] >= 18.66 and int(info["weight"] or 400) >= 700)
                need = 3.0 if large else 4.5
                if cr < need:
                    fails.append((round(cr, 2), need, info["txt"], info["fg"], bg))

            report[key] = {
                "console_errors": errs,
                "external_requests": sorted(set(ext)),
                "contrast_failures": fails,
                "contrast_checked": len(handles),
                "banned": [w for w in BANNED if w in pg.content()],
                "title": pg.title(),
                "h1": (pg.query_selector("h1").inner_text() if pg.query_selector("h1") else None),
                "sections": pg.eval_on_selector_all("main section[id]", "els => els.map(e => e.id)"),
                "nav_links": pg.eval_on_selector_all(".nav-links a", "els => els.map(e => e.textContent.trim())"),
                "cards": pg.eval_on_selector_all(".card", "e => e.length"),
                "svc_cards": pg.eval_on_selector_all(".svc-card", "e => e.length"),
                "how_items": pg.eval_on_selector_all(".how-item", "e => e.length"),
            }
            ctx.close()

    # overflow sweep
    ov = {}
    ctx = b.new_context()
    pg = ctx.new_page()
    for route in ROUTES:
        pg.goto(BASE + route, wait_until="load")
        for w in WIDTHS:
            pg.set_viewport_size({"width": w, "height": 800})
            pg.wait_for_timeout(80)
            sw, cw = pg.evaluate("[document.documentElement.scrollWidth, document.documentElement.clientWidth]")
            if sw > cw + 1:
                ov[f"{route}@{w}"] = sw - cw
    ctx.close()
    b.close()

print(json.dumps({"report": report, "overflow": ov}, ensure_ascii=False, indent=2))
