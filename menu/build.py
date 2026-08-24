#!/usr/bin/env python3
# Builds web.html (artifact body) and print.html (full doc for PDF) from menu.json + assets.
import json, base64, subprocess, os

ROOT = os.path.dirname(os.path.abspath(__file__))
A = os.path.join(ROOT, "assets")
menu = json.load(open(os.path.join(ROOT, "menu.json")))
B = menu["brand"]

def b64(path):
    return base64.b64encode(open(path, "rb").read()).decode()

def img_uri(name, maxw=None, q=None):
    src = os.path.join(A, f"{name}.jpg")
    if maxw:
        out = os.path.join(A, f"web_{name}.jpg")
        if not os.path.exists(out):
            subprocess.run(["python3", "-c", f"""
from PIL import Image
im = Image.open({src!r}).convert('RGB')
w,h = im.size
if w > {maxw}:
    im = im.resize(({maxw}, round(h*{maxw}/w)), Image.LANCZOS)
im.save({out!r}, 'JPEG', quality={q}, optimize=True, progressive=True)
"""], check=True)
        src = out
    return "data:image/jpeg;base64," + b64(src)

def font_face(fam, weight, fname):
    return f"@font-face{{font-family:'{fam}';font-weight:{weight};font-style:normal;font-display:swap;src:url(data:font/woff2;base64,{b64(os.path.join(A,fname))}) format('woff2');}}"

def esc(s):
    return s.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")

def price_html(p):
    if p:
        return f'<span class="price"><span class="num">${esc(p)}</span></span>'
    return '<span class="price blank" aria-label="price to be added"></span>'

def item_html(it):
    return (f'<div class="item">'
            f'<div class="row1"><span class="name-en">{esc(it["en"])}</span>'
            f'<span class="leader"></span>{price_html(it["price"])}</div>'
            f'<div class="name-ar" dir="rtl" lang="ar">{esc(it["ar"])}</div>'
            f'<p class="desc-en">{esc(it["den"])}</p>'
            f'<p class="desc-ar" dir="rtl" lang="ar">{esc(it["dar"])}</p>'
            f'</div>')

def section_html(s, web=True):
    imgtag = ""
    if s["img"]:
        uri = img_uri(s["img"], 900, 72) if web else img_uri(s["img"])
        imgtag = f'<div class="band"><img src="{uri}" alt="{esc(s["en"])}" loading="lazy"></div>'
    note = ""
    if s.get("note_en"):
        note = (f'<div class="note"><span>{esc(s["note_en"])}</span>'
                f'<span dir="rtl" lang="ar">{esc(s["note_ar"])}</span></div>')
    items = "".join(item_html(i) for i in s["items"])
    return (f'<section class="menu-sec" id="{s["id"]}">'
            f'<header class="sec-head"><h2><span class="t-en">{esc(s["en"])}</span>'
            f'<span class="t-ar" dir="rtl" lang="ar">{esc(s["ar"])}</span>'
            f'<span class="t-script" dir="rtl" lang="ar" aria-hidden="true">{esc(s["script"])}</span></h2></header>'
            f'{imgtag}{note}<div class="items">{items}</div></section>')

# ---------------------------------------------------------------- shared css
SHARED = """
*{box-sizing:border-box;margin:0;padding:0}
img{max-width:100%;display:block}
h1,h2{text-wrap:balance}
.name-ar,.t-ar,.desc-ar{font-family:'Almarai',system-ui,sans-serif}
.t-script{font-family:'Aref Ruqaa',serif}
.price .num{font-variant-numeric:tabular-nums}
"""

NAV = "".join(
    f'<a href="#{s["id"]}"><span>{esc(s["en"])}</span><span class="n-ar" dir="rtl" lang="ar">{esc(s["ar"])}</span></a>'
    for s in menu["sections"])

HERO_LOCKUP = f"""
<div class="lockup">
  <div class="abbr">{B["abbr"]}</div>
  <h1><span class="h-en">{esc(B["name_en"])}</span><span class="h-ar" dir="rtl" lang="ar">{esc(B["name_ar"])}</span></h1>
  <div class="tag"><span>{esc(B["tagline_en"])}</span><span class="dot">·</span><span dir="rtl" lang="ar">{esc(B["tagline_ar"])}</span></div>
  <div class="sub t-script" dir="rtl" lang="ar">{esc(B["sub_ar"])}</div>
</div>"""

FOOTER = f"""
<footer class="foot">
  <div class="resv"><span>Reservations · WhatsApp&nbsp;81&nbsp;130&nbsp;345</span><span dir="rtl" lang="ar">للحجز · واتساب ٨١١٣٠٣٤٥</span></div>
  <div class="loc">Baissour · Aley District · Mount Lebanon — بيصور، قضاء عاليه، جبل لبنان</div>
</footer>"""

# ---------------------------------------------------------------- web
web_css = SHARED + """
:root{
  --paper:#FBF8F1; --ink:#1B1712; --muted:#71695B; --accent:#E08A12; --accent-ink:#9C5F07;
  --line:#E8E1CF; --card:#FFFFFF; --band-tint:rgba(224,138,18,.08); --hero-scrim:rgba(20,14,6,.46);
}
@media (prefers-color-scheme: dark){
  :root:not([data-theme="light"]){
    --paper:#161210; --ink:#EDE5D6; --muted:#A79C88; --accent:#F0A63C; --accent-ink:#F0A63C;
    --line:#2E272A; --card:#1F1A14; --band-tint:rgba(240,166,60,.10); --hero-scrim:rgba(10,7,3,.55);
  }
}
:root[data-theme="dark"]{
  --paper:#161210; --ink:#EDE5D6; --muted:#A79C88; --accent:#F0A63C; --accent-ink:#F0A63C;
  --line:#2E2720; --card:#1F1A14; --band-tint:rgba(240,166,60,.10); --hero-scrim:rgba(10,7,3,.55);
}
html{scroll-behavior:smooth}
@media (prefers-reduced-motion:reduce){html{scroll-behavior:auto}}
body{background:var(--paper);color:var(--ink);font-family:'Archivo',system-ui,sans-serif;line-height:1.5}
.hero{position:relative;min-height:340px;max-height:520px;height:52vh;overflow:hidden}
.hero img{width:100%;height:100%;object-fit:cover;position:absolute;inset:0}
.hero::after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(0,0,0,.12),var(--hero-scrim) 78%)}
.lockup{position:absolute;inset:auto 0 0 0;z-index:2;text-align:center;color:#FDF9F0;padding:0 20px 34px}
.lockup .abbr{font-weight:900;font-size:clamp(30px,5vw,44px);letter-spacing:.42em;margin-left:.42em}
.lockup h1{display:flex;flex-direction:column;gap:2px;margin:4px 0 8px}
.lockup .h-en{font-size:clamp(19px,2.6vw,26px);font-weight:700;letter-spacing:.02em}
.lockup .h-ar{font-family:'Almarai',sans-serif;font-weight:800;font-size:clamp(17px,2.3vw,23px)}
.lockup .tag{display:flex;gap:10px;justify-content:center;flex-wrap:wrap;font-size:13px;letter-spacing:.14em;text-transform:uppercase;opacity:.92}
.lockup .tag [lang=ar]{letter-spacing:0;text-transform:none;font-family:'Almarai',sans-serif}
.lockup .sub{color:#FFC46A;font-size:clamp(17px,2.4vw,24px);margin-top:10px;transform:rotate(-2deg)}
nav.chips{position:sticky;top:0;z-index:20;background:color-mix(in srgb,var(--paper) 88%,transparent);
  backdrop-filter:blur(8px);border-bottom:1px solid var(--line);display:flex;gap:4px;overflow-x:auto;
  padding:10px 16px;scrollbar-width:none}
nav.chips::-webkit-scrollbar{display:none}
nav.chips a{flex:0 0 auto;display:flex;flex-direction:column;align-items:center;gap:0;
  text-decoration:none;color:var(--ink);padding:6px 13px;border:1px solid var(--line);border-radius:999px;
  font-size:12.5px;font-weight:600;letter-spacing:.04em;background:var(--card);transition:border-color .15s}
nav.chips a .n-ar{font-size:11px;color:var(--muted);font-family:'Almarai',sans-serif}
nav.chips a:hover,nav.chips a:focus-visible{border-color:var(--accent)}
nav.chips a:focus-visible{outline:2px solid var(--accent);outline-offset:1px}
main{max-width:980px;margin:0 auto;padding:12px 22px 40px}
.menu-sec{padding:38px 0 8px}
.sec-head h2{display:flex;align-items:baseline;gap:14px;flex-wrap:wrap}
.t-en{font-size:clamp(24px,3.4vw,32px);font-weight:900;letter-spacing:.015em;text-transform:uppercase}
.t-ar{font-size:clamp(19px,2.6vw,25px);font-weight:800}
.t-script{color:var(--accent);font-size:clamp(20px,3vw,27px);transform:rotate(-4deg);display:inline-block;translate:0 -2px}
.band{margin:16px 0 6px;border-radius:14px;overflow:hidden;aspect-ratio:21/8}
.band img{width:100%;height:100%;object-fit:cover}
.note{display:flex;flex-direction:column;gap:3px;background:var(--band-tint);border-radius:10px;
  padding:10px 14px;margin:12px 0 4px;font-size:13.5px;color:var(--muted)}
.note [lang=ar]{font-family:'Almarai',sans-serif}
.items{display:grid;grid-template-columns:1fr 1fr;gap:26px 44px;padding:16px 0 8px}
@media (max-width:760px){.items{grid-template-columns:1fr}}
.row1{display:flex;align-items:baseline;gap:8px}
.name-en{font-weight:700;font-size:16.5px}
.leader{flex:1;border-bottom:2px dotted var(--line);translate:0 -4px;min-width:24px}
.price{white-space:nowrap;font-weight:700;font-size:15.5px}
.price .cur{font-size:10.5px;color:var(--muted);margin-left:4px;letter-spacing:.06em}
.price.blank{width:64px;border-bottom:2px dashed color-mix(in srgb,var(--accent) 55%,var(--paper));height:1em}
.name-ar{font-weight:800;font-size:15px;margin-top:1px}
.desc-en{color:var(--muted);font-size:13.5px;margin-top:4px}
.desc-ar{color:var(--muted);font-size:13px;margin-top:2px}
.foot{border-top:1px solid var(--line);margin-top:44px;padding:26px 20px 40px;text-align:center;
  display:flex;flex-direction:column;gap:10px}
.foot .resv{display:flex;gap:14px;justify-content:center;flex-wrap:wrap;font-weight:700;font-size:14.5px}
.foot .resv [lang=ar],.foot .disc [lang=ar]{font-family:'Almarai',sans-serif}
.foot .disc{display:flex;gap:12px;justify-content:center;flex-wrap:wrap;color:var(--accent-ink);font-size:12.5px}
.foot .loc{color:var(--muted);font-size:12px;letter-spacing:.05em}
"""

web = f"""<meta charset="utf-8">
<title>Baissour Country Club Menu</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Almarai:wght@400;800&family=Archivo:wght@400;600;700;900&family=Aref+Ruqaa:wght@400;700&display=swap">
<style>{web_css}</style>
<div class="hero"><img src="{img_uri('hero', 1344, 74)}" alt="Riverside terrace at Baissour Country Club">{HERO_LOCKUP}</div>
<nav class="chips" aria-label="Menu sections">{NAV}</nav>
<main>
{"".join(section_html(s, web=True) for s in menu["sections"])}
</main>
{FOOTER}
"""
open(os.path.join(ROOT, "web.html"), "w").write(web)

# ---------------------------------------------------------------- print
faces = "".join([
    font_face("Almarai", 400, "almarai-400.woff2"),
    font_face("Almarai", 800, "almarai-800.woff2"),
    font_face("Archivo", 400, "archivo-400.woff2"),
    font_face("Archivo", 700, "archivo-700.woff2"),
    font_face("Archivo", 900, "archivo-900.woff2"),
    font_face("Aref Ruqaa", 400, "arefruqaa-400.woff2"),
    font_face("Aref Ruqaa", 700, "arefruqaa-700.woff2"),
])

print_css = SHARED + faces + """
:root{--paper:#FFFFFF;--ink:#1B1712;--muted:#6E6759;--accent:#DB8709;--accent-ink:#9C5F07;--line:#E3DCC9;--band-tint:#FBF3E4}
@page{size:A4;margin:13mm 13mm 15mm}
body{background:var(--paper);color:var(--ink);font-family:'Archivo',sans-serif;line-height:1.42;font-size:10pt}
.cover{text-align:center;page-break-after:always;padding-top:2mm}
.cover .heroimg{border-radius:4mm;overflow:hidden;height:118mm}
.cover .heroimg img{width:100%;height:100%;object-fit:cover}
.cover .abbr{font-weight:900;font-size:30pt;letter-spacing:.4em;margin:14mm 0 2mm .4em}
.cover .h-en{font-size:15pt;font-weight:700;display:block}
.cover .h-ar{font-family:'Almarai',sans-serif;font-weight:800;font-size:14pt;display:block;margin-top:1mm}
.cover .tag{margin-top:4mm;font-size:9.5pt;letter-spacing:.16em;text-transform:uppercase;color:var(--muted)}
.cover .tag-ar{font-family:'Almarai',sans-serif;font-size:10pt;color:var(--muted);margin-top:1.5mm}
.cover .sub{font-family:'Aref Ruqaa',serif;color:var(--accent);font-size:16pt;margin-top:9mm;transform:rotate(-2deg)}
.cover .menu-word{margin-top:12mm;font-weight:900;font-size:13pt;letter-spacing:.5em;margin-left:.5em;text-transform:uppercase}
.menu-sec{page-break-inside:auto;padding-top:7mm}
.sec-head h2{display:flex;align-items:baseline;gap:5mm;border-bottom:.6pt solid var(--line);padding-bottom:2mm}
.t-en{font-size:16pt;font-weight:900;text-transform:uppercase;letter-spacing:.02em}
.t-ar{font-size:13pt;font-weight:800}
.t-script{color:var(--accent);font-size:14pt;transform:rotate(-4deg);display:inline-block}
.band{margin:4mm 0 2mm;border-radius:3mm;overflow:hidden;height:34mm;page-break-inside:avoid}
.band img{width:100%;height:100%;object-fit:cover}
.note{background:var(--band-tint);border-radius:2.5mm;padding:2.5mm 4mm;margin:3mm 0 1mm;font-size:8.4pt;color:var(--muted)}
.note span{display:block}
.note [lang=ar]{font-family:'Almarai',sans-serif;margin-top:.8mm}
.items{display:grid;grid-template-columns:1fr 1fr;gap:4.5mm 8mm;padding:4mm 0 2mm}
.item{page-break-inside:avoid}
.row1{display:flex;align-items:baseline;gap:2mm}
.name-en{font-weight:700;font-size:10.5pt}
.leader{flex:1;border-bottom:1pt dotted #C9C1AD;translate:0 -1mm;min-width:6mm}
.price{white-space:nowrap;font-weight:700;font-size:10pt}
.price .cur{font-size:6.5pt;color:var(--muted);margin-left:1mm;letter-spacing:.06em}
.price.blank{width:16mm;border-bottom:1pt dashed var(--accent);height:3.5mm}
.name-ar{font-weight:800;font-size:9.5pt}
.desc-en{color:var(--muted);font-size:8.2pt;margin-top:.8mm}
.desc-ar{color:var(--muted);font-size:8pt;margin-top:.4mm}
.foot{border-top:.6pt solid var(--line);margin-top:8mm;padding-top:5mm;text-align:center;page-break-inside:avoid}
.foot>div{margin-bottom:2mm}
.foot .resv{font-weight:700;font-size:10pt}
.foot .resv span{margin:0 3mm}
.foot .disc{color:var(--accent-ink);font-size:8.5pt}
.foot .disc span{margin:0 2mm}
.foot .loc{color:var(--muted);font-size:8pt;letter-spacing:.05em}
.foot [lang=ar]{font-family:'Almarai',sans-serif}
/* one full page per section */
.menu-sec{page-break-before:always;padding-top:0;display:flex;flex-direction:column;min-height:260mm}
.menu-sec:last-of-type{min-height:215mm}
.cover{page-break-after:avoid}
.sec-head h2{padding-bottom:3mm}
.t-en{font-size:20pt}
.t-ar{font-size:16pt}
.t-script{font-size:17pt}
.band{height:48mm;margin:4mm 0 2mm}
.note{font-size:9pt;padding:3mm 4.5mm;margin:3mm 0 0}
.items{flex:1;gap:4mm 9mm;padding:5mm 0 3mm;align-content:space-evenly}
.name-en{font-size:11.5pt}
.name-ar{font-size:10.5pt}
.desc-en{font-size:9pt;margin-top:1mm}
.desc-ar{font-size:8.8pt}
.price{font-size:11.5pt}
.price.blank{width:18mm}
.foot{margin-top:4mm}
"""

print_doc = f"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">
<title>Baissour Country Club — Menu</title><style>{print_css}</style></head><body>
<div class="cover">
  <div class="heroimg"><img src="{img_uri('hero')}" alt=""></div>
  <div class="abbr">{B["abbr"]}</div>
  <span class="h-en">{esc(B["name_en"])}</span>
  <span class="h-ar" dir="rtl" lang="ar">{esc(B["name_ar"])}</span>
  <div class="tag">{esc(B["tagline_en"])}</div>
  <div class="tag-ar" dir="rtl" lang="ar">{esc(B["tagline_ar"])}</div>
  <div class="sub" dir="rtl" lang="ar">{esc(B["sub_ar"])}</div>
  <div class="menu-word">The Menu · قائمة الطعام</div>
</div>
{"".join(section_html(s, web=False) for s in menu["sections"])}
{FOOTER}
</body></html>"""
open(os.path.join(ROOT, "print.html"), "w").write(print_doc)

print("web.html", len(web), "bytes;", "print.html", len(print_doc), "bytes")
