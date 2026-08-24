#!/usr/bin/env python3
# BCC bilingual site: home + gallery + booking + directions pages, WhatsApp forms, hash router.
import json, base64, os, subprocess, shutil

ROOT = os.path.dirname(os.path.abspath(__file__))
A = os.path.join(ROOT, "assets")
S = json.load(open(os.path.join(ROOT, "site.json")))
B = S["brand"]
_uri_cache = {}

def esc(t): return t.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")

from PIL import Image, ImageOps, ImageEnhance, ImageFilter

def _touchup(im):
    im = ImageOps.autocontrast(im, cutoff=1)
    im = ImageEnhance.Color(im).enhance(1.06)
    im = ImageEnhance.Contrast(im).enhance(1.03)
    im = im.filter(ImageFilter.UnsharpMask(radius=1.0, percent=55, threshold=4))
    return im

DEPLOY = os.environ.get("BCC_DEPLOY") == "1"
DIST = os.path.join(ROOT, "dist")
if DEPLOY:
    os.makedirs(os.path.join(DIST, "assets", "i"), exist_ok=True)
    os.makedirs(os.path.join(DIST, "assets", "v"), exist_ok=True)

def uri(name, maxw=1400, q=74):
    if DEPLOY:
        # deploy mode: bigger, higher-quality files on disk, relative URLs
        maxw = min(maxw * 2, 2000)
        q = max(q, 80)
    key = (name, maxw, q)
    if key in _uri_cache: return _uri_cache[key]
    for ext, mime in ((".jpg","image/jpeg"), (".png","image/png")):
        p = os.path.join(A, name+ext)
        if os.path.exists(p):
            if ext == ".jpg":
                out = os.path.join(A, f"t{maxw}q{q}_{name}.jpg")
                if not os.path.exists(out):
                    im = Image.open(p).convert('RGB')
                    w, h = im.size
                    if w > maxw: im = im.resize((maxw, round(h*maxw/w)), Image.LANCZOS)
                    im = _touchup(im)
                    im.save(out, 'JPEG', quality=q, optimize=True, progressive=True)
                p = out
            if DEPLOY:
                fn = f"{name}_w{maxw}{ext}" if ext == ".jpg" else name + ext
                dst = os.path.join(DIST, "assets", "i", fn)
                if not os.path.exists(dst): shutil.copy2(p, dst)
                d = f"assets/i/{fn}"
            else:
                d = f"data:{mime};base64," + base64.b64encode(open(p,"rb").read()).decode()
            _uri_cache[key] = d
            return d
    raise FileNotFoundError(name)

def vid_uri(name):
    p = os.path.join(A, "videos", name + ".mp4")
    if not os.path.exists(p): return None
    if DEPLOY:
        dst = os.path.join(DIST, "assets", "v", name + ".mp4")
        if not os.path.exists(dst): shutil.copy2(p, dst)
        return f"assets/v/{name}.mp4"
    return "data:video/mp4;base64," + base64.b64encode(open(p, "rb").read()).decode()

def video_or_img(vname, iname, maxw, q, alt, cls_extra=""):
    v = vid_uri(vname)
    poster = uri(iname, maxw, q)
    if v:
        return (f'<video class="vmedia{cls_extra}" autoplay muted loop playsinline '
                f'poster="{poster}" src="{v}" aria-label="{esc(alt)}"></video>')
    return f'<img src="{poster}" alt="{esc(alt)}" loading="lazy">'

def LL(en, ar, tag="span", cls=""):
    return (f'<{tag} class="L en {cls}">{esc(en)}</{tag}>'
            f'<{tag} class="L ar {cls}" dir="rtl" lang="ar">{esc(ar)}</{tag}>')

def sec_head(d, h="h2"):
    return (f'<header class="sec-head"><{h}>'
            f'<span class="L en t-big">{esc(d["title_en"])}</span>'
            f'<span class="L ar t-big" dir="rtl" lang="ar">{esc(d["title_ar"])}</span>'
            f'<span class="t-script" dir="rtl" lang="ar" aria-hidden="true">{esc(d["script"])}</span>'
            f'</{h}></header>')

def lead(d):
    return (f'<p class="lead L en">{esc(d["lead_en"])}</p>'
            f'<p class="lead L ar" dir="rtl" lang="ar">{esc(d["lead_ar"])}</p>')

# ------------------------------------------------------------------ CSS
css = """
*{box-sizing:border-box;margin:0;padding:0}
img{max-width:100%;display:block}
:root{
  --paper:#FBF8F1; --ink:#1B1712; --muted:#6F6858; --accent:#E08A12; --accent-ink:#9C5F07;
  --line:#E8E1CF; --card:#FFFFFF; --tint:rgba(224,138,18,.08); --scrim:rgba(16,11,4,.45);
}
@media (prefers-color-scheme: dark){
  :root:not([data-theme="light"]){
    --paper:#161210; --ink:#EDE5D6; --muted:#A79C88; --accent:#F0A63C; --accent-ink:#F0A63C;
    --line:#2E2720; --card:#1F1A14; --tint:rgba(240,166,60,.10); --scrim:rgba(8,5,2,.55);
  }
}
:root[data-theme="dark"]{
  --paper:#161210; --ink:#EDE5D6; --muted:#A79C88; --accent:#F0A63C; --accent-ink:#F0A63C;
  --line:#2E2720; --card:#1F1A14; --tint:rgba(240,166,60,.10); --scrim:rgba(8,5,2,.55);
}
html{scroll-behavior:smooth}
@media (prefers-reduced-motion:reduce){html{scroll-behavior:auto}}
body{background:var(--paper);color:var(--ink);font-family:'Archivo',system-ui,sans-serif;line-height:1.55}
[data-lang="en"] .L.ar{display:none}
[data-lang="ar"] .L.en{display:none}
[data-lang="ar"] body{font-family:'Almarai','Archivo',sans-serif}
.L.ar{font-family:'Almarai',sans-serif}
.t-script{font-family:'Aref Ruqaa',serif;color:var(--accent)}
.page{display:none}.page.on{display:block}
/* top bar */
.bar{position:sticky;top:0;z-index:40;display:flex;align-items:center;gap:14px;
  padding:10px 18px;background:color-mix(in srgb,var(--paper) 90%,transparent);
  backdrop-filter:blur(10px);border-bottom:1px solid var(--line)}
.bar .logo{height:40px;width:auto;cursor:pointer}
.bar nav{display:flex;gap:2px;overflow-x:auto;flex:1;scrollbar-width:none}
.bar nav::-webkit-scrollbar{display:none}
.bar nav a{white-space:nowrap;text-decoration:none;color:var(--ink);font-size:13px;font-weight:600;
  padding:7px 11px;border-radius:999px;letter-spacing:.03em;cursor:pointer}
.bar nav a:hover,.bar nav a:focus-visible{background:var(--tint);outline:none}
.lang-btn{flex:0 0 auto;border:1.5px solid var(--accent);background:none;color:var(--accent-ink);
  font-weight:700;font-size:13px;padding:6px 14px;border-radius:999px;cursor:pointer;font-family:inherit}
.lang-btn:hover{background:var(--tint)}
/* hero */
.hero{position:relative;min-height:88vh;display:flex;align-items:flex-end;overflow:hidden}
.hero>img,.hero>video{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.hero>img{animation:kenburns 9s ease-out forwards}
@keyframes kenburns{from{transform:scale(1.09)}to{transform:scale(1)}}
.hero-inner>*{animation:riseup .8s ease-out backwards}
.hero-inner>*:nth-child(1){animation-delay:.15s}
.hero-inner>*:nth-child(2){animation-delay:.3s}
.hero-inner>*:nth-child(3){animation-delay:.5s}
.hero-inner>*:nth-child(4){animation-delay:.7s}
@keyframes riseup{from{opacity:0;transform:translateY(22px)}to{opacity:1;transform:none}}
.t-script{transition:transform .3s ease}
.sec-head:hover .t-script{transform:rotate(-7deg) scale(1.06)}
.wa-float{animation:floatpulse 3.2s ease-in-out infinite}
@keyframes floatpulse{0%,100%{box-shadow:0 8px 22px rgba(0,0,0,.25)}50%{box-shadow:0 8px 30px rgba(37,211,102,.45)}}
.gitem{transition:opacity .35s ease}
@media (prefers-reduced-motion:reduce){
  .hero>img,.hero-inner>*,.wa-float{animation:none}
}
.hero::after{content:"";position:absolute;inset:0;background:linear-gradient(185deg,rgba(0,0,0,.08) 30%,var(--scrim) 82%)}
.hero-inner{position:relative;z-index:2;color:#FDF9F0;padding:0 6vw 9vh;max-width:900px}
.kicker{font-size:13px;letter-spacing:.22em;text-transform:uppercase;opacity:.9;margin-bottom:14px}
[dir=rtl] .kicker{letter-spacing:.06em}
.hero h1 .t-h1{display:block;font-size:clamp(44px,7.5vw,92px);font-weight:900;line-height:1.02;letter-spacing:-.015em;text-wrap:balance}
[data-lang="ar"] .hero h1 .t-h1{letter-spacing:0;line-height:1.15}
.hero .sub{margin-top:18px;font-size:clamp(16px,1.9vw,20px);max-width:58ch;opacity:.95}
.cta-row{display:flex;gap:12px;margin-top:28px;flex-wrap:wrap}
.btn{display:inline-block;text-decoration:none;font-weight:700;font-size:15px;padding:13px 26px;
  border-radius:999px;transition:transform .15s ease;cursor:pointer;border:none;font-family:inherit}
.btn:hover{transform:translateY(-2px)}
.btn:focus-visible{outline:3px solid var(--accent);outline-offset:2px}
.btn-solid{background:var(--accent);color:#1D1405}
.btn-ghost{border:1.5px solid rgba(255,255,255,.85);color:#FDF9F0;background:none}
.btn-line{border:1.5px solid var(--accent);color:var(--accent-ink);background:none}
.btn-wa{background:#25D366;color:#062B12}
/* stats */
.stats{display:grid;grid-template-columns:repeat(4,1fr);border-bottom:1px solid var(--line)}
.stats>div{padding:26px 10px;text-align:center;border-inline-start:1px solid var(--line)}
.stats>div:first-child{border-inline-start:none}
.stats .num{font-weight:900;font-size:clamp(26px,4vw,40px);color:var(--accent-ink)}
.stats .lab{font-size:13px;color:var(--muted);margin-top:2px}
@media (max-width:700px){.stats{grid-template-columns:1fr 1fr}.stats>div:nth-child(3){border-inline-start:none}}
/* sections */
main{max-width:1120px;margin:0 auto;padding:0 22px}
section.block{padding:64px 0 30px}
.sec-head h2,.sec-head h1,.sec-head h3{display:flex;align-items:baseline;gap:16px;flex-wrap:wrap}
.t-big{font-size:clamp(30px,4.4vw,44px);font-weight:900;letter-spacing:.01em;text-transform:uppercase}
.L.ar.t-big{text-transform:none;letter-spacing:0}
.t-script{font-size:clamp(22px,3vw,30px);transform:rotate(-4deg);display:inline-block;translate:0 -2px}
.lead{font-size:clamp(16px,1.9vw,19px);max-width:72ch;margin-top:16px}
.lead.L.ar{line-height:1.9}
.rv{opacity:0;transform:translateY(18px);transition:opacity .6s ease,transform .6s ease}
.rv.in{opacity:1;transform:none}
@media (prefers-reduced-motion:reduce){.rv{opacity:1;transform:none;transition:none}}
/* venues */
.venues{display:flex;flex-direction:column;gap:34px;margin-top:30px}
.venueblock{background:var(--card);border:1px solid var(--line);border-radius:20px;overflow:hidden}
.vb-hero{position:relative;aspect-ratio:16/8;overflow:hidden}
.vb-hero img,.vb-hero video{width:100%;height:100%;object-fit:cover}
.vb-hero .vtag{position:absolute;top:16px;inset-inline-start:16px;background:rgba(20,14,5,.62);color:#FFD79A;
  font-size:12px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;padding:6px 13px;border-radius:999px;backdrop-filter:blur(4px)}
[data-lang="ar"] .vb-hero .vtag{letter-spacing:0}
.vb-body{padding:24px 26px 26px}
.vfacts{color:var(--accent-ink);font-size:13.5px;font-weight:700;margin-top:6px}
.vthumbs{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin-top:18px}
@media (max-width:760px){.vthumbs{grid-template-columns:repeat(2,1fr)}}
.vth{aspect-ratio:4/3;cursor:zoom-in;margin:0;background:var(--paper);border:1px solid var(--line);
  border-radius:11px;padding:6px;box-shadow:0 2px 10px rgba(0,0,0,.06)}
.vth img{width:100%;height:100%;object-fit:cover;transition:transform .4s ease;border-radius:6px}
.vth:hover img{transform:scale(1.05)}
.vopts{margin-top:4px}
@media (max-width:800px){.venues{gap:26px}}
.venue{background:var(--card);border:1px solid var(--line);border-radius:18px;overflow:hidden}
.venue .ph{aspect-ratio:4/3;overflow:hidden;position:relative}
.venue .ph img{width:100%;height:100%;object-fit:cover;transition:transform .5s ease}
.venue:hover .ph img{transform:scale(1.03)}
.venue .vtag{position:absolute;top:14px;inset-inline-start:14px;background:rgba(20,14,5,.62);color:#FFD79A;
  font-size:12px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;padding:6px 13px;border-radius:999px;backdrop-filter:blur(4px)}
[data-lang="ar"] .venue .vtag{letter-spacing:0}
.venue .pad{padding:20px 22px 24px}
.vname{display:flex;align-items:baseline;gap:12px;flex-wrap:wrap}
.vname .nm{font-size:24px;font-weight:900}
.vname .nm-ar{font-family:'Aref Ruqaa',serif;font-size:24px;color:var(--accent);transform:rotate(-3deg);display:inline-block}
.venue .desc,.vb-body .desc{color:var(--muted);font-size:15px;margin-top:10px}
.venue .duo{display:block;margin-top:0;aspect-ratio:16/9}
.venue .duo img{width:100%;height:100%;object-fit:cover}
/* features/quotes */
.feat{display:grid;grid-template-columns:1fr 1fr;gap:10px 34px;margin-top:30px}
@media (max-width:700px){.feat{grid-template-columns:1fr}}
.feat>div{display:flex;gap:10px;align-items:baseline;font-size:15.5px}
.feat .tick{color:var(--accent);font-weight:900}
.quotes{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin-top:34px}
@media (max-width:700px){.quotes{grid-template-columns:1fr}}
.quote{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:20px 22px;font-size:15px}
.quote::before{content:"\\201C";display:block;font-size:34px;line-height:.6;color:var(--accent);font-weight:900;margin-bottom:10px}
[data-lang="ar"] .quote::before{content:"\\201D"}
/* packages */
.t-mid{font-size:clamp(24px,3.2vw,32px);font-weight:900;text-transform:uppercase}
.L.ar.t-mid{text-transform:none}
.tiers{display:grid;grid-template-columns:repeat(3,1fr);gap:18px;margin-top:28px;align-items:stretch}
@media (max-width:860px){.tiers{grid-template-columns:1fr}}
.tier{background:var(--card);border:1px solid var(--line);border-radius:18px;padding:26px 24px;display:flex;flex-direction:column;transition:transform .2s ease,box-shadow .2s ease}
.tier:hover{transform:translateY(-4px);box-shadow:0 12px 28px rgba(0,0,0,.10)}
.tier.featured{border:2px solid var(--accent);position:relative}
.tier.featured::before{content:"★";position:absolute;top:-13px;inset-inline-start:24px;background:var(--accent);color:#1D1405;
  font-size:13px;font-weight:900;padding:2px 12px;border-radius:999px}
.ttag{font-size:11.5px;font-weight:700;letter-spacing:.09em;text-transform:uppercase;color:var(--muted)}
[data-lang="ar"] .ttag{letter-spacing:0}
.tname{display:flex;align-items:baseline;gap:10px;margin-top:8px;flex-wrap:wrap}
.tname .tn{font-size:23px;font-weight:900}
.tname .tn-ar{font-family:'Aref Ruqaa',serif;font-size:20px;color:var(--accent);transform:rotate(-3deg);display:inline-block}
.tprice{font-size:38px;font-weight:900;color:var(--accent-ink);margin-top:12px;font-variant-numeric:tabular-nums}
.tunit{font-size:12.5px;color:var(--muted);margin-top:2px}
.tlist{list-style:none;margin:18px 0 22px;display:flex;flex-direction:column;gap:9px;flex:1}
.tlist li{display:flex;gap:9px;align-items:baseline;font-size:14.5px}
.tlist .tick{color:var(--accent);font-weight:900}
.tier .btn{align-self:flex-start}
.subhead{font-size:15px;font-weight:900;letter-spacing:.08em;text-transform:uppercase;color:var(--accent-ink);margin-top:36px}
[data-lang="ar"] .subhead{letter-spacing:0}
.chips{display:flex;gap:10px;flex-wrap:wrap;margin-top:14px}
.chip{border:1.5px solid var(--line);background:var(--card);border-radius:999px;padding:9px 17px;font-size:14px}
.deals{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin-top:14px}
@media (max-width:800px){.deals{grid-template-columns:1fr}}
.deal{background:var(--tint);border-radius:16px;padding:20px 22px;display:flex;gap:16px;align-items:center}
.deal .dbig{font-size:30px;font-weight:900;color:var(--accent-ink);white-space:nowrap;font-variant-numeric:tabular-nums}
.deal .dtxt{font-size:13.5px}
/* calculator */
.radios{display:flex;flex-direction:column;gap:8px}
.cbx{display:flex;gap:10px;align-items:baseline;font-size:14.5px;cursor:pointer;
  border:1.5px solid var(--line);border-radius:10px;padding:10px 13px;background:var(--paper)}
.cbx:has(input:checked){border-color:var(--accent);background:var(--tint)}
.cbx input{accent-color:var(--accent);flex:0 0 auto;translate:0 1px;width:auto;border:none;background:none;padding:0}
.cal-total{display:flex;align-items:baseline;gap:16px;margin-top:24px;padding:18px 22px;
  background:var(--tint);border-radius:14px;flex-wrap:wrap}
.ct-lab{font-weight:700;font-size:14px;color:var(--accent-ink);text-transform:uppercase;letter-spacing:.07em}
[data-lang="ar"] .ct-lab{letter-spacing:0}
.ct-num{font-size:clamp(30px,4vw,42px);font-weight:900;color:var(--accent-ink);font-variant-numeric:tabular-nums;
  transition:transform .15s ease;display:inline-block}
.ct-num.bump{transform:scale(1.08)}
/* families / socials / gift */
.socgrid{display:grid;grid-template-columns:repeat(5,1fr);gap:14px;margin-top:26px}
@media (max-width:1000px){.socgrid{grid-template-columns:repeat(3,1fr)}}
@media (max-width:640px){.socgrid{grid-template-columns:repeat(2,1fr)}}
.soc{position:relative;display:block;border-radius:16px;overflow:hidden;aspect-ratio:9/14;text-decoration:none}
.soc-likes{position:absolute;top:12px;inset-inline-start:12px;z-index:2;background:rgba(20,14,5,.65);color:#FFD79A;
  font-weight:900;font-size:13px;padding:5px 12px;border-radius:999px;backdrop-filter:blur(4px)}
.soc-play{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);z-index:2;color:#fff;
  font-size:26px;background:rgba(20,14,5,.45);width:58px;height:58px;border-radius:50%;
  display:flex;align-items:center;justify-content:center;backdrop-filter:blur(3px);transition:transform .2s ease}
.soc:hover .soc-play{transform:translate(-50%,-50%) scale(1.12)}
.soc img{width:100%;height:100%;object-fit:cover;transition:transform .5s ease}
.soc:hover img{transform:scale(1.04)}
.soc::after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,transparent 35%,rgba(10,7,3,.65))}
.soc-lab{position:absolute;bottom:16px;inset-inline-start:20px;z-index:2;color:#FDF9F0;font-weight:900;font-size:19px}
.venue.nat-text{background:var(--tint);display:flex;align-items:center}
.venue.nat-text .desc{font-size:16px}
.gift{background:var(--tint);border-radius:18px;padding:34px 32px;border:1.5px dashed var(--accent)}
.gift-head{display:flex;align-items:baseline;gap:14px;flex-wrap:wrap}
.gift .gt{font-size:clamp(24px,3.2vw,32px);font-weight:900;text-transform:uppercase}
.gift .L.ar.gt{text-transform:none}
.gift .lead{margin-top:10px}
/* forms */
.formcard{background:var(--card);border:1px solid var(--line);border-radius:18px;padding:28px;margin-top:34px}
.formcard h3{font-size:20px;font-weight:900;margin-bottom:6px}
.formcard .fl{font-size:13px;font-weight:700;color:var(--accent-ink);letter-spacing:.05em;display:block;margin:16px 0 6px}
[data-lang="ar"] .formcard .fl{letter-spacing:0}
.fgrid{display:grid;grid-template-columns:1fr 1fr;gap:0 22px}
@media (max-width:700px){.fgrid{grid-template-columns:1fr}}
input,select,textarea{width:100%;background:var(--paper);border:1.5px solid var(--line);border-radius:10px;
  padding:11px 13px;font-size:15px;color:var(--ink);font-family:inherit}
input:focus,select:focus,textarea:focus{outline:none;border-color:var(--accent)}
textarea{min-height:84px;resize:vertical}
.form-note{font-size:13px;color:var(--muted);margin-top:14px}
/* chalets */
.chgrid{display:grid;grid-template-columns:repeat(3,1fr);gap:18px;margin-top:28px}
@media (max-width:900px){.chgrid{grid-template-columns:1fr 1fr}}
@media (max-width:620px){.chgrid{grid-template-columns:1fr}}
.chalet{background:var(--card);border:1px solid var(--line);border-radius:16px;overflow:hidden;
  transition:transform .2s ease,box-shadow .2s ease;display:flex;flex-direction:column}
.chalet:hover{transform:translateY(-4px);box-shadow:0 12px 28px rgba(0,0,0,.10)}
.chalet .ph{aspect-ratio:4/3;overflow:hidden}
.chalet img{width:100%;height:100%;object-fit:cover}
.chalet .pad{padding:16px 18px 20px;flex:1;display:flex;flex-direction:column}
.tagpill{display:inline-block;background:var(--tint);color:var(--accent-ink);font-size:11.5px;
  font-weight:700;letter-spacing:.08em;text-transform:uppercase;border-radius:999px;padding:4px 11px;margin-bottom:10px;align-self:flex-start}
[data-lang="ar"] .tagpill{letter-spacing:0}
.chalet h3.chname{display:flex;align-items:baseline;gap:10px;flex-wrap:wrap}
.chalet .cn{font-size:19px;font-weight:900}
.chalet .cn-ar{font-family:'Aref Ruqaa',serif;font-size:18px;color:var(--accent);transform:rotate(-3deg);display:inline-block}
.chalet .chsub{font-size:12.5px;color:var(--muted);text-transform:uppercase;letter-spacing:.07em;margin-top:3px}
[data-lang="ar"] .chalet .chsub{letter-spacing:0}
.chalet .facts{color:var(--accent-ink);font-size:12.5px;font-weight:600;margin-top:6px}
.chprice{margin-top:10px;font-size:14.5px;color:var(--accent-ink)}
.chprice b{font-size:19px;font-weight:900}
.chalet .desc{color:var(--muted);font-size:14px;margin-top:8px;flex:1}
.chalet .bk{margin-top:14px;align-self:flex-start;font-size:13.5px;padding:9px 18px}
.chnotes{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin-top:24px}
@media (max-width:800px){.chnotes{grid-template-columns:1fr 1fr}}
.chnotes>div{border:1px dashed var(--line);border-radius:12px;padding:12px 14px;font-size:13px;color:var(--muted)}
/* splits & strips */
.split{display:grid;grid-template-columns:1.1fr 1fr;gap:34px;align-items:center;margin-top:26px}
@media (max-width:800px){.split{grid-template-columns:1fr}}
.split .ph{border-radius:16px;overflow:hidden}
.points{margin-top:20px;display:flex;flex-direction:column;gap:10px}
.points>div{display:flex;gap:10px;align-items:baseline;font-size:15px}
.points .tick{color:var(--accent);font-weight:900}
.strip{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-top:18px}
.strip.strip4{grid-template-columns:repeat(4,1fr)}
@media (max-width:700px){.strip.strip4{grid-template-columns:1fr 1fr}}
.strip .ph{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:7px;
  box-shadow:0 3px 12px rgba(0,0,0,.07);overflow:hidden}
.strip .ph img{border-radius:6px}
.split .ph{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:9px;
  box-shadow:0 4px 18px rgba(0,0,0,.08)}
.split .ph img,.split .ph video{border-radius:9px;width:100%;display:block}
.vmedia{width:100%;height:100%;object-fit:cover;display:block}
.strip .ph{border-radius:12px;overflow:hidden;aspect-ratio:4/3}
.strip img{width:100%;height:100%;object-fit:cover}
.band{position:relative;border-radius:18px;overflow:hidden;margin-top:26px;min-height:340px;display:flex;align-items:flex-end}
.band>img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.band::after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,transparent 30%,rgba(10,7,3,.62))}
.band .cap{position:relative;z-index:2;color:#FDF9F0;padding:26px 30px}
.band .cap .q{font-family:'Aref Ruqaa',serif;font-size:clamp(22px,3vw,30px);color:#FFC46A}
/* gallery */
.gcats{display:flex;gap:8px;flex-wrap:wrap;margin-top:24px}
.gcats button{border:1.5px solid var(--line);background:var(--card);color:var(--ink);border-radius:999px;
  padding:8px 16px;font-size:13.5px;font-weight:700;cursor:pointer;font-family:inherit}
.gcats button.on{border-color:var(--accent);background:var(--tint);color:var(--accent-ink)}
.gwrap{columns:3;column-gap:14px;margin-top:24px}
@media (max-width:900px){.gwrap{columns:2}}
@media (max-width:560px){.gwrap{columns:1}}
.gitem{break-inside:avoid;margin-bottom:14px;cursor:zoom-in;position:relative;
  background:var(--card);border:1px solid var(--line);border-radius:12px;padding:8px;
  box-shadow:0 3px 14px rgba(0,0,0,.07)}
.gitem img{width:100%;transition:transform .4s ease;border-radius:6px;display:block}
.gitem:hover img{transform:scale(1.03)}
.gitem.hid{display:none}
.lightbox{position:fixed;inset:0;z-index:80;background:rgba(10,7,3,.92);display:none;align-items:center;justify-content:center;padding:4vmin;cursor:zoom-out}
.lightbox.on{display:flex}
.lightbox img{max-width:100%;max-height:100%;border-radius:8px}
/* directions */
.dgrid{display:grid;grid-template-columns:1.05fr 1fr;gap:34px;margin-top:30px;align-items:start}
@media (max-width:850px){.dgrid{grid-template-columns:1fr}}
.timegrid{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-top:8px}
@media (max-width:600px){.timegrid{grid-template-columns:1fr 1fr}}
.timegrid>div{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:16px 14px;text-align:center}
.timegrid .t{font-weight:900;font-size:20px;color:var(--accent-ink);font-variant-numeric:tabular-nums}
.timegrid .f{font-size:13.5px;color:var(--muted);margin-top:3px}
.routecard{background:var(--card);border:1px solid var(--line);border-radius:18px;padding:24px}
.routecard svg{width:100%;height:auto;display:block}
.route-line{font-size:15px;margin-top:18px;padding:14px 16px;background:var(--tint);border-radius:12px}
/* contact + footer */
.contact-grid{display:grid;grid-template-columns:1fr 1fr;gap:30px;margin-top:26px}
@media (max-width:800px){.contact-grid{grid-template-columns:1fr}}
.ccard{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:26px}
.ccard h3{font-size:16px;font-weight:800;margin-bottom:10px;color:var(--accent-ink);text-transform:uppercase;letter-spacing:.08em}
[data-lang="ar"] .ccard h3{letter-spacing:0}
.ccard p{font-size:15px;color:var(--muted)}
.wa-big{display:flex;align-items:center;gap:12px;margin-top:16px;font-weight:900;font-size:22px;color:var(--accent-ink);text-decoration:none}
.socials{display:flex;gap:12px;margin-top:16px;flex-wrap:wrap}
.socials a{color:var(--accent-ink);font-weight:700;font-size:14px;text-decoration:none;border:1.5px solid var(--line);padding:8px 16px;border-radius:999px}
.socials a:hover{border-color:var(--accent)}
footer{border-top:1px solid var(--line);margin-top:60px;padding:34px 22px 46px;text-align:center;color:var(--muted);font-size:13px}
footer .logo{height:54px;margin:0 auto 12px;width:auto}
.wa-float{position:fixed;inset-inline-end:20px;bottom:20px;z-index:50;background:#25D366;color:#062B12;
  width:58px;height:58px;border-radius:50%;display:flex;align-items:center;justify-content:center;
  box-shadow:0 8px 22px rgba(0,0,0,.25);text-decoration:none}
.wa-float svg{width:30px;height:30px}
.wa-float:hover{transform:scale(1.06)}
.pagehead{padding-top:52px}
"""

# ------------------------------------------------------------------ JS
js = """
(function(){
  var root=document.documentElement;
  var saved=null; try{saved=localStorage.getItem('bcc-lang')}catch(e){}
  window.LANG='en';
  function applyLang(l){
    window.LANG=l;
    root.setAttribute('data-lang',l);
    root.setAttribute('dir', l==='ar'?'rtl':'ltr');
    root.setAttribute('lang', l==='ar'?'ar':'en');
    var b=document.getElementById('langbtn'); if(b) b.textContent = l==='ar' ? 'English' : 'عربي';
    try{localStorage.setItem('bcc-lang',l)}catch(e){}
  }
  applyLang(saved==='ar'?'ar':'en');
  document.getElementById('langbtn').addEventListener('click',function(){
    applyLang(root.getAttribute('data-lang')==='ar'?'en':'ar');
  });
  var PAGES=['home','gallery','booking','directions'];
  function show(page){
    PAGES.forEach(function(p){document.getElementById('pg-'+p).classList.toggle('on', p===page)});
    obs();
  }
  function route(){
    var h=(location.hash||'').replace('#','');
    if(PAGES.indexOf(h)>-1 && h!=='home'){ show(h); window.scrollTo(0,0); }
    else if(h && document.getElementById(h)){ show('home');
      var el=document.getElementById(h); if(el) el.scrollIntoView(); }
    else { show('home'); if(!h) window.scrollTo(0,0); }
  }
  window.addEventListener('hashchange',route);
  var io=null;
  function obs(){
    if(window.matchMedia('(prefers-reduced-motion: reduce)').matches || !('IntersectionObserver' in window)){
      document.querySelectorAll('.rv').forEach(function(el){el.classList.add('in')}); return;
    }
    if(!io){ io=new IntersectionObserver(function(es){es.forEach(function(e){
      if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target);}});},{threshold:.1}); }
    document.querySelectorAll('.page.on .rv:not(.in)').forEach(function(el){io.observe(el)});
  }
  route();
  /* gallery filter */
  document.querySelectorAll('.gcats button').forEach(function(b){
    b.addEventListener('click',function(){
      document.querySelectorAll('.gcats button').forEach(function(x){x.classList.remove('on')});
      b.classList.add('on');
      var c=b.getAttribute('data-cat');
      document.querySelectorAll('.gitem').forEach(function(g){
        var cats=g.getAttribute('data-cat').split(' ');
        g.classList.toggle('hid', c!=='all' && cats.indexOf(c)===-1);
      });
    });
  });
  /* lightbox */
  var lb=document.getElementById('lightbox'), lbi=document.getElementById('lightbox-img');
  var lbList=[], lbIdx=0;
  function lbShow(i){
    if(!lbList.length) return;
    lbIdx=(i+lbList.length)%lbList.length;
    lbi.src=lbList[lbIdx];
  }
  document.querySelectorAll('.gitem img, .vth img').forEach(function(im){
    im.parentElement.addEventListener('click',function(){
      var scope;
      if(im.closest('.gwrap')){
        scope=[].slice.call(document.querySelectorAll('.gwrap .gitem:not(.hid) img'));
      } else {
        var wrap=im.closest('.vthumbs');
        scope=wrap?[].slice.call(wrap.querySelectorAll('img')):[im];
      }
      lbList=scope.map(function(x){return x.src});
      lbShow(scope.indexOf(im));
      lb.classList.add('on');
    });
  });
  var lbTX=0, lbTY=0, lbSwiped=false;
  lb.addEventListener('touchstart',function(e){
    var t=e.touches[0]; lbTX=t.clientX; lbTY=t.clientY; lbSwiped=false;
  },{passive:true});
  lb.addEventListener('touchend',function(e){
    var t=e.changedTouches[0]; var dx=t.clientX-lbTX, dy=t.clientY-lbTY;
    if(Math.abs(dx)>40 && Math.abs(dx)>Math.abs(dy)*1.5){
      lbSwiped=true;
      lbShow(dx<0 ? lbIdx+1 : lbIdx-1);
    }
  },{passive:true});
  lb.addEventListener('click',function(){
    if(lbSwiped){lbSwiped=false; return;}
    lb.classList.remove('on'); lbi.src='';
  });
  document.addEventListener('keydown',function(e){
    if(!lb.classList.contains('on')) return;
    if(e.key==='Escape'){lb.classList.remove('on'); lbi.src='';}
    else if(e.key==='ArrowRight'){e.preventDefault(); lbShow(lbIdx+1);}
    else if(e.key==='ArrowLeft'){e.preventDefault(); lbShow(lbIdx-1);}
  });
  /* chalet preselect */
  document.querySelectorAll('[data-book]').forEach(function(b){
    b.addEventListener('click',function(){
      var v=b.getAttribute('data-book');
      var sel=document.getElementById('bk-chalet');
      if(sel) sel.value=v;
      location.hash='booking';
    });
  });
  /* whatsapp forms */
  function val(id){var e=document.getElementById(id);return e?e.value.trim():''}
  function selTxt(id){var e=document.getElementById(id);return e?e.options[e.selectedIndex].text:''}
  var BCC_EMAIL='BCC_EMAIL_ADDR';
  function emailAuto(subject,msg){
    /* background email copy via FormSubmit relay; silently skipped where network is restricted */
    try{
      fetch('https://formsubmit.co/ajax/'+BCC_EMAIL,{method:'POST',
        headers:{'Content-Type':'application/json','Accept':'application/json'},
        body:JSON.stringify({_subject:subject,message:msg})}).catch(function(){});
    }catch(e){}
  }
  function openWA(msg,subject){
    emailAuto(subject||'Website inquiry',msg);
    window.open('https://wa.me/WA_NUMBER?text='+encodeURIComponent(msg),'_blank');
  }
  function sendMail(subject,msg){
    location.href='mailto:'+BCC_EMAIL+'?subject='+encodeURIComponent(subject)+'&body='+encodeURIComponent(msg);
  }
  function bkMsg(){
    var ar = window.LANG==='ar';
    return ar
      ? 'مرحبا! بدي احجز شاليه:\\n• الاسم: '+val('bk-name')+'\\n• التلفون: '+val('bk-phone')+'\\n• الإيميل: '+val('bk-mail')+'\\n• الشاليه: '+selTxt('bk-chalet')+'\\n• الوصول: '+val('bk-in')+'\\n• المغادرة: '+val('bk-out')+'\\n• عدد الأشخاص: '+val('bk-guests')+(val('bk-notes')?'\\n• ملاحظات: '+val('bk-notes'):'')
      : 'Hello! I would like to book a chalet:\\n• Name: '+val('bk-name')+'\\n• Phone: '+val('bk-phone')+'\\n• Email: '+val('bk-mail')+'\\n• Chalet: '+selTxt('bk-chalet')+'\\n• Check-in: '+val('bk-in')+'\\n• Check-out: '+val('bk-out')+'\\n• Guests: '+val('bk-guests')+(val('bk-notes')?'\\n• Notes: '+val('bk-notes'):'');
  }
  var bkBtn=document.getElementById('bk-send');
  if(bkBtn) bkBtn.addEventListener('click',function(){ openWA(bkMsg(),'Chalet booking request — '+val('bk-name')); });
  var bkEm=document.getElementById('bk-email');
  if(bkEm) bkEm.addEventListener('click',function(){ sendMail('Chalet booking request — '+val('bk-name'), bkMsg()); });
  /* event calculator */
  function calCompute(){
    var pkg=document.querySelector('input[name="cal-pkg"]:checked');
    if(!pkg) return {total:0};
    var g=parseInt(val('cal-guests')||'0',10)||0;
    var base=parseInt(pkg.getAttribute('data-base'),10);
    var pp=parseInt(pkg.getAttribute('data-pp'),10);
    var billG=g; if(pp>0) billG=Math.max(g,100);
    var venue=base + pp*billG;
    var disc=0;
    if(document.getElementById('cal-weekday').checked) disc+=0.15;
    if(document.getElementById('cal-early').checked) disc+=0.10;
    venue=venue*(1-disc);
    var bar=parseInt(document.getElementById('cal-bar').value,10)||0;
    var extras=0;
    document.querySelectorAll('.cal-extra:checked').forEach(function(c){extras+=parseInt(c.getAttribute('data-price'),10)});
    var total=Math.round(venue + bar*Math.max(g,1) + extras);
    return {total:total,g:g,pkg:pkg.value,bar:bar,disc:disc};
  }
  function calRender(){
    var r=calCompute();
    var el=document.getElementById('cal-total');
    if(!el) return;
    el.textContent='≈ $'+r.total.toLocaleString('en-US');
    el.classList.remove('bump'); void el.offsetWidth; el.classList.add('bump');
  }
  var calWrap=document.getElementById('calculator');
  if(calWrap){
    calWrap.addEventListener('change',calRender);
    calWrap.addEventListener('input',calRender);
    calRender();
    function calMsg(){
      var r=calCompute();
      var pkgNames={space:'The Space (venue only)',table:'The Table (venue + catering)',atoz:'A to Z (fully planned)'};
      var barNames={0:'soft drinks only',15:'open bar',25:'premium bar'};
      var ex=[];
      document.querySelectorAll('.cal-extra:checked').forEach(function(c){
        ex.push(c.parentElement.textContent.trim().split('(')[0].trim());
      });
      var ar=window.LANG==='ar';
      var m=(ar?'مرحبا! جرّبت حاسبة المناسبات، هيدي خطتي:':'Hello! I tried the event calculator, here is my plan:')+'\\n'+
        (ar?'• الباقة: ':'• Package: ')+pkgNames[r.pkg]+'\\n'+
        (ar?'• الضيوف: ':'• Guests: ')+r.g+'\\n'+
        (ar?'• البار: ':'• Bar: ')+barNames[r.bar]+
        (ex.length?('\\n'+(ar?'• إضافات: ':'• Extras: ')+ex.join(', ')):'')+
        (r.disc?('\\n'+(ar?'• حسومات: ':'• Discounts: ')+Math.round(r.disc*100)+'%'):'')+'\\n'+
        (ar?'• التقدير المبدئي: ~$':'• Rough estimate: ~$')+r.total.toLocaleString('en-US')+'\\n'+
        (ar?'بحب ياخد عرض سعر رسمي 🙏':'I would love a proper quote please!');
      return m;
    }
    document.getElementById('cal-send').addEventListener('click',function(){ openWA(calMsg(),'Event plan from the website calculator'); });
    var calEm=document.getElementById('cal-email');
    if(calEm) calEm.addEventListener('click',function(){ sendMail('Event plan from the website calculator', calMsg()); });
  }
  function iqMsg(){
    var ar = window.LANG==='ar';
    return ar
      ? 'مرحبا! عندي استفسار عن مناسبة:\\n• الاسم: '+val('iq-name')+'\\n• التلفون: '+val('iq-phone')+'\\n• الإيميل: '+val('iq-mail')+'\\n• النوع: '+selTxt('iq-type')+'\\n• المكان: '+selTxt('iq-venue')+'\\n• التاريخ: '+val('iq-date')+'\\n• عدد المدعوين: '+val('iq-guests')+(val('iq-notes')?'\\n• تفاصيل: '+val('iq-notes'):'')
      : 'Hello! I would like to inquire about an event:\\n• Name: '+val('iq-name')+'\\n• Phone: '+val('iq-phone')+'\\n• Email: '+val('iq-mail')+'\\n• Event type: '+selTxt('iq-type')+'\\n• Venue: '+selTxt('iq-venue')+'\\n• Date: '+val('iq-date')+'\\n• Guests: '+val('iq-guests')+(val('iq-notes')?'\\n• Details: '+val('iq-notes'):'');
  }
  var iqBtn=document.getElementById('iq-send');
  if(iqBtn) iqBtn.addEventListener('click',function(){ openWA(iqMsg(),'Event inquiry — '+val('iq-name')); });
  var iqEm=document.getElementById('iq-email');
  if(iqEm) iqEm.addEventListener('click',function(){ sendMail('Event inquiry — '+val('iq-name'), iqMsg()); });
})();
""".replace("WA_NUMBER", B["whatsapp_number"]).replace("BCC_EMAIL_ADDR", B["email"])

# ------------------------------------------------------------------ pieces
W=S["weddings"]; C=S["chalets"]; P=S["pool"]; R=S["restaurant"]; AR_=S["area"]
CT=S["contact"]; H=S["hero"]; IQ=S["inquiry"]; BK=S["booking"]; G=S["gallery"]; D=S["directions"]
PK=S["packages"]

tiers = ""
for t in PK["tiers"]:
    feat_cls = " featured" if t.get("featured") else ""
    rows = "".join(f'<li><span class="tick">✓</span>{LL(i["en"], i["ar"])}</li>' for i in t["items"])
    tiers += (f'<article class="tier{feat_cls} rv">'
              f'<div class="ttag">{LL(t["tag_en"], t["tag_ar"])}</div>'
              f'<div class="tname"><span class="tn">{esc(t["name_en"])}</span>'
              f'<span class="tn-ar" dir="rtl" lang="ar">{esc(t["name_ar"])}</span></div>'
              f'<div class="tprice">{esc(t["price"])}</div>'
              f'<div class="tunit">{LL(t["unit_en"], t["unit_ar"])}</div>'
              f'<ul class="tlist">{rows}</ul>'
              f'<a class="btn btn-line" href="#inquiry">{LL("Get a quote", "خود عرض سعر")}</a>'
              f'</article>')
addons = "".join(f'<span class="chip rv">{LL(a["en"], a["ar"])}</span>' for a in PK["addons"])
deals = "".join(f'<div class="deal rv"><div class="dbig">{esc(d["big"])}</div><div class="dtxt">{LL(d["en"], d["ar"])}</div></div>' for d in PK["deals"])
packages_html = (f'<div class="pk" id="packages"><header class="sec-head" style="margin-top:52px"><h3>'
    f'<span class="L en t-mid">{esc(PK["title_en"])}</span>'
    f'<span class="L ar t-mid" dir="rtl" lang="ar">{esc(PK["title_ar"])}</span>'
    f'<span class="t-script" dir="rtl" lang="ar" aria-hidden="true">{esc(PK["script"])}</span></h3></header>'
    f'<p class="lead L en">{esc(PK["lead_en"])}</p><p class="lead L ar" dir="rtl" lang="ar">{esc(PK["lead_ar"])}</p>'
    f'<div class="tiers">{tiers}</div>'
    f'<h4 class="subhead">{LL(PK["addons_title_en"], PK["addons_title_ar"])}</h4>'
    f'<div class="chips">{addons}</div>'
    f'<h4 class="subhead">{LL(PK["deals_title_en"], PK["deals_title_ar"])}</h4>'
    f'<div class="deals">{deals}</div>'
    f'<p class="form-note">{LL(PK["note_en"], PK["note_ar"])}</p></div>')

nav = "".join(
    f'<a href="#{n["id"]}">{LL(n["en"], n["ar"])}</a>' for n in S["nav"])
stats = "".join(f'<div class="rv"><div class="num">{s["num"]}</div><div class="lab">{LL(s["en"], s["ar"])}</div></div>' for s in S["stats"])

venues = ""
for v in W["venues"]:
    thumbs = "".join(
        f'<figure class="vth"><img src="{uri(p, 620, 54)}" alt="{esc(v["name"])} venue" loading="lazy"></figure>'
        for p in v["photos"])
    venues += (f'<article class="venueblock rv">'
               f'<div class="vb-hero">{video_or_img(v.get("video") or "", v["hero"], 1300, 74, v["name"] + " venue")}'
               f'<span class="vtag">{LL(v["tag_en"], v["tag_ar"])}</span></div>'
               f'<div class="vb-body"><div class="vname"><span class="nm">{esc(v["name"])}</span>'
               f'<span class="nm-ar" dir="rtl" lang="ar">{esc(v["name_ar"])}</span></div>'
               f'<div class="vfacts">{LL(v["facts_en"], v["facts_ar"])}</div>'
               f'<p class="desc">{LL(v["desc_en"], v["desc_ar"])}</p>'
               f'<div class="vthumbs">{thumbs}</div></div>'
               f'</article>')
CEL = S["celebrations"]
cel_chips = "".join(f'<span class="chip rv">{LL(c["en"], c["ar"])}</span>' for c in CEL["chips"])
celebrations_html = (f'<div class="gift rv" style="margin-top:44px" id="celebrations">'
    f'<div class="gift-head"><span class="L en gt">{esc(CEL["title_en"])}</span>'
    f'<span class="L ar gt" dir="rtl" lang="ar">{esc(CEL["title_ar"])}</span>'
    f'<span class="t-script" dir="rtl" lang="ar" aria-hidden="true">{esc(CEL["script"])}</span></div>'
    f'{lead(CEL)}'
    f'<div class="chips" style="margin-top:16px">{cel_chips}</div>'
    f'<div class="cta-row" style="margin-top:20px"><a class="btn btn-solid" href="#inquiry">{LL(CEL["cta_en"], CEL["cta_ar"])}</a></div>'
    f'</div>')

venue_opts = "".join(f'<span class="chip rv">{LL(o["en"], o["ar"])}</span>' for o in W["venue_opts"])
venues += (f'<div class="vopts"><h4 class="subhead">{LL(W["venue_opts_title_en"], W["venue_opts_title_ar"])}</h4>'
           f'<div class="chips">{venue_opts}</div></div>')
moments = "".join(f'<figure class="vth"><img src="{uri(m, 620, 54)}" alt="Wedding moment at Baissour Country Club" loading="lazy"></figure>' for m in W["moments"])
venues += (f'<div class="vopts"><h4 class="subhead">{LL(W["moments_title_en"], W["moments_title_ar"])}</h4>'
           f'<div class="vthumbs" style="margin-top:14px">{moments}</div></div>')

feat = "".join(f'<div class="rv"><span class="tick">✓</span>{LL(f["en"], f["ar"])}</div>' for f in W["features"])
quotes = "".join(f'<div class="quote rv">{LL(q["en"], q["ar"])}</div>' for q in W["quotes"])

IQF = IQ["fields"]
iq_types = "".join(f'<option>{esc(t["en"])}</option>' for t in IQF["types"])
iq_types_ar = "".join(f'<option>{esc(t["ar"])}</option>' for t in IQF["types"])
iq_ven = "".join(f'<option>{esc(t["en"])}</option>' for t in IQF["venues"])
iq_ven_ar = "".join(f'<option>{esc(t["ar"])}</option>' for t in IQF["venues"])

def dual_select(idbase, opts_en, opts_ar):
    return (f'<select id="{idbase}" class="L en">{opts_en}</select>'
            f'<select id="{idbase}-ar-mirror" class="L ar" dir="rtl" onchange="document.getElementById(\'{idbase}\').selectedIndex=this.selectedIndex">{opts_ar}</select>')

# NOTE: to keep one source of truth, AR selects mirror into the EN select.
inquiry_form = f"""
<div class="formcard rv" id="inquiry">
  <h3>{LL(IQ["title_en"], IQ["title_ar"])} <span class="t-script" dir="rtl" lang="ar">{esc(IQ["script"])}</span></h3>
  <p class="form-note">{LL(IQ["lead_en"], IQ["lead_ar"])}</p>
  <div class="fgrid">
    <div><label class="fl">{LL(IQF["name_en"], IQF["name_ar"])}</label><input id="iq-name" autocomplete="name"></div>
    <div><label class="fl">{LL(IQF["phone_en"], IQF["phone_ar"])}</label><input id="iq-phone" type="tel" autocomplete="tel"></div>
    <div><label class="fl">{LL(IQF["emailaddr_en"], IQF["emailaddr_ar"])}</label><input id="iq-mail" type="email" autocomplete="email"></div>
    <div><label class="fl">{LL(IQF["type_en"], IQF["type_ar"])}</label>{dual_select("iq-type", iq_types, iq_types_ar)}</div>
    <div><label class="fl">{LL(IQF["venue_en"], IQF["venue_ar"])}</label>{dual_select("iq-venue", iq_ven, iq_ven_ar)}</div>
    <div><label class="fl">{LL(IQF["date_en"], IQF["date_ar"])}</label><input id="iq-date" type="date"></div>
    <div><label class="fl">{LL(IQF["guests_en"], IQF["guests_ar"])}</label><input id="iq-guests" type="number" min="10"></div>
  </div>
  <label class="fl">{LL(IQF["notes_en"], IQF["notes_ar"])}</label><textarea id="iq-notes"></textarea>
  <div class="cta-row"><button class="btn btn-wa" id="iq-send" type="button">{LL(IQF["submit_en"], IQF["submit_ar"])}</button>
  <button class="btn btn-line" id="iq-email" type="button">{LL(IQF["email_en"], IQF["email_ar"])}</button></div>
</div>"""

chcards = ""
for c in C["list"]:
    bookval = f'{c["name_en"]} ({c["sub_en"]})'
    chcards += (f'<article class="chalet rv"><div class="ph"><img src="{uri(c["img"], 640, 52)}" '
                f'alt="{esc(c["name_en"])}" loading="lazy"></div><div class="pad">'
                f'<span class="tagpill">{LL(c["tag_en"], c["tag_ar"])}</span>'
                f'<h3 class="chname"><span class="cn">{esc(c["name_en"])}</span>'
                f'<span class="cn-ar" dir="rtl" lang="ar">{esc(c["name_ar"])}</span></h3>'
                f'<div class="chsub">{LL(c["sub_en"], c["sub_ar"])}</div>'
                f'<div class="facts">{LL(c["facts_en"], c["facts_ar"])}</div>'
                f'<p class="desc">{LL(c["desc_en"], c["desc_ar"])}</p>'
                f'<div class="chprice"><span class="L en">from <b>${c["price"]}</b> / night</span>'
                f'<span class="L ar" dir="rtl" lang="ar">من <b>{c["price"]}$</b> / الليلة</span></div>'
                f'<button class="btn btn-line bk" type="button" data-book="{esc(bookval)}">{LL(C["cta_en"], C["cta_ar"])}</button>'
                f'</div></article>')
chnotes = "".join(f'<div class="rv">{LL(n["en"], n["ar"])}</div>' for n in C["notes"])
pool_pts = "".join(f'<div class="rv"><span class="tick">✓</span>{LL(p["en"], p["ar"])}</div>' for p in P["points"])
pool_rates = "".join(f'<div class="rv"><span class="tick">✓</span>{LL(r["en"], r["ar"])}</div>' for r in P["rates"])
pool_rates_html = (f'<div class="split" style="margin-top:34px">'
    f'<div>'
    f'<h3 class="vname rv"><span class="L en t-mid">{esc(P["rates_title_en"])}</span>'
    f'<span class="L ar t-mid" dir="rtl" lang="ar">{esc(P["rates_title_ar"])}</span></h3>'
    f'<p class="lead" style="margin-top:10px">{LL(P["rates_note_en"], P["rates_note_ar"])}</p>'
    f'<div class="points">{pool_rates}</div></div>'
    f'<div class="ph rv"><img src="{uri("pool_rates", 760, 62)}" alt="Baissour Country Club pool entrance rates" loading="lazy"></div>'
    f'</div>')

BKF = BK["fields"]
bk_opts = "".join(f'<option>{esc(c["name_en"])} ({esc(c["sub_en"])})</option>' for c in C["list"])
booking_form = f"""
<div class="formcard rv">
  <div class="fgrid">
    <div><label class="fl">{LL(BKF["name_en"], BKF["name_ar"])}</label><input id="bk-name" autocomplete="name"></div>
    <div><label class="fl">{LL(BKF["phone_en"], BKF["phone_ar"])}</label><input id="bk-phone" type="tel" autocomplete="tel"></div>
    <div><label class="fl">{LL(BKF["emailaddr_en"], BKF["emailaddr_ar"])}</label><input id="bk-mail" type="email" autocomplete="email"></div>
    <div><label class="fl">{LL(BKF["chalet_en"], BKF["chalet_ar"])}</label><select id="bk-chalet">{bk_opts}</select></div>
    <div><label class="fl">{LL(BKF["checkin_en"], BKF["checkin_ar"])}</label><input id="bk-in" type="date"></div>
    <div><label class="fl">{LL(BKF["checkout_en"], BKF["checkout_ar"])}</label><input id="bk-out" type="date"></div>
    <div><label class="fl">{LL(BKF["guests_en"], BKF["guests_ar"])}</label><input id="bk-guests" type="number" min="1" max="12"></div>
  </div>
  <label class="fl">{LL(BKF["notes_en"], BKF["notes_ar"])}</label><textarea id="bk-notes"></textarea>
  <div class="cta-row"><button class="btn btn-wa" id="bk-send" type="button">{LL(BKF["submit_en"], BKF["submit_ar"])}</button>
  <button class="btn btn-line" id="bk-email" type="button">{LL(BKF["email_en"], BKF["email_ar"])}</button></div>
</div>"""

FM=S["families"]; GS=S["giftshop"]; SO=S["socials"]; CAL=S["calculator"]; CL=CAL["labels"]; NAT=S["naturals"]

def nat_card(c):
    head = (f'<div class="pad"><div class="vname"><span class="nm">{esc(c["name"])}</span>'
            f'<span class="nm-ar" dir="rtl" lang="ar">{esc(c["name_ar"])}</span></div>'
            f'<p class="desc">{LL(c["desc_en"], c["desc_ar"])}</p></div>')
    if c.get("img"):
        ph = (f'<div class="ph"><img src="{uri(c["img"], 800, 55)}" alt="{esc(c["name"])} natural pool" loading="lazy">'
              f'<span class="vtag">{LL("Natural pool", "بركة طبيعية")}</span></div>')
        ph2 = f'<div class="ph duo"><img src="{uri(c["img2"], 800, 55)}" alt="" loading="lazy"></div>' if c.get("img2") else ""
        return f'<article class="venue rv">{ph}{head}{ph2}</article>'
    return (f'<article class="venue nat-text rv"><div class="pad">'
            f'<span class="tagpill">{LL("Natural pool", "بركة طبيعية")}</span>'
            f'<div class="vname"><span class="nm">{esc(c["name"])}</span>'
            f'<span class="nm-ar" dir="rtl" lang="ar">{esc(c["name_ar"])}</span></div>'
            f'<p class="desc">{LL(c["desc_en"], c["desc_ar"])}</p></div></article>')
nat_cards = "".join(nat_card(c) for c in NAT["cards"])
naturals_html = (f'<div class="pk" style="margin-top:46px"><header class="sec-head"><h3>'
    f'<span class="L en t-mid">{esc(NAT["title_en"])}</span>'
    f'<span class="L ar t-mid" dir="rtl" lang="ar">{esc(NAT["title_ar"])}</span>'
    f'<span class="t-script" dir="rtl" lang="ar" aria-hidden="true">{esc(NAT["script"])}</span></h3></header>'
    f'{lead(NAT)}<div class="venues">{nat_cards}</div></div>')

def a_img(name, fallback):
    return name if os.path.exists(os.path.join(A, name + ".jpg")) else fallback

fam_pts = "".join(f'<div class="rv"><span class="tick">✓</span>{LL(p["en"], p["ar"])}</div>' for p in FM["points"])
families_html = (f'<section class="block" id="families">{sec_head(FM)}{lead(FM)}'
    f'<div class="strip strip4" style="margin-top:26px">'
    f'<div class="ph rv">{video_or_img("kidspark", "kidspark_1", 620, 54, "Kids playground in the park — slide, swings and little tables on the lawn")}</div>'
    f'<div class="ph rv"><img src="{uri("soc_fb_24", 620, 54)}" alt="Ducks by the river at Baissour Country Club" loading="lazy"></div>'
    f'<div class="ph rv"><img src="{uri("ducks_2", 620, 54)}" alt="The club geese" loading="lazy"></div>'
    f'<div class="ph rv"><img src="{uri("soc_fb_21", 620, 54)}" alt="Bonfire nights" loading="lazy"></div>'
    f'</div><div class="feat" style="margin-top:26px">{fam_pts}</div>'
    f'<div class="gift rv" style="margin-top:34px;display:flex;flex-wrap:wrap;align-items:center;gap:18px;justify-content:space-between">'
    f'<div style="flex:1 1 420px">'
    f'<div class="kicker" style="margin-bottom:6px">{LL(FM["ad"]["kicker_en"], FM["ad"]["kicker_ar"])}</div>'
    f'<div class="gift-head"><span class="L en gt" style="font-size:clamp(20px,2.6vw,27px)">{esc(FM["ad"]["title_en"])}</span>'
    f'<span class="L ar gt" dir="rtl" lang="ar" style="font-size:clamp(20px,2.6vw,27px)">{esc(FM["ad"]["title_ar"])}</span></div>'
    f'<p class="lead" style="margin-top:8px">{LL(FM["ad"]["text_en"], FM["ad"]["text_ar"])}</p></div>'
    f'<a class="btn btn-solid" href="#celebrations" style="flex:0 0 auto">{LL(FM["ad"]["cta_en"], FM["ad"]["cta_ar"])}</a>'
    f'</div></section>')

soc_cards = "".join(
    f'<a class="soc rv" href="{c["url"]}" target="_blank" rel="noopener">'
    f'<img src="{uri(c["img"], 480, 52)}" alt="{esc(c["cap_en"])}">'
    f'<span class="soc-likes">♥ {esc(c["likes"])}</span>'
    f'<span class="soc-lab">{LL(c["cap_en"], c["cap_ar"])}</span>'
    f'<span class="soc-play">▶</span></a>'
    for c in SO["cards"])
socials_html = (f'<section class="block" id="socials">{sec_head(SO)}{lead(SO)}'
    f'<div class="socgrid">{soc_cards}</div></section>')

giftshop_html = (f'<section class="block" id="giftshop"><div class="gift rv">'
    f'<div class="gift-head"><span class="L en gt">{esc(GS["title_en"])}</span>'
    f'<span class="L ar gt" dir="rtl" lang="ar">{esc(GS["title_ar"])}</span>'
    f'<span class="t-script" dir="rtl" lang="ar" aria-hidden="true">{esc(GS["script"])}</span></div>'
    f'{lead(GS)}</div></section>')

cal_extras = "".join(
    f'<label class="cbx"><input type="checkbox" class="cal-extra" data-price="{e["price"]}" id="cal-{e["id"]}">'
    f'<span>{LL(e["en"], e["ar"])}</span></label>' for e in CAL["extras"])
calculator_html = f"""
<div class="formcard calc rv" id="calculator">
  <h3><span class="L en">{esc(CAL["title_en"])}</span><span class="L ar" dir="rtl" lang="ar">{esc(CAL["title_ar"])}</span>
  <span class="t-script" dir="rtl" lang="ar">{esc(CAL["script"])}</span></h3>
  <p class="form-note">{LL(CAL["lead_en"], CAL["lead_ar"])}</p>
  <div class="fgrid">
    <div>
      <label class="fl">{LL(CL["package_en"], CL["package_ar"])}</label>
      <div class="radios">
        <label class="cbx"><input type="radio" name="cal-pkg" value="space" data-base="4500" data-pp="0"><span>The Space — $4,500</span></label>
        <label class="cbx"><input type="radio" name="cal-pkg" value="table" data-base="0" data-pp="40" checked><span>The Table — $40/guest</span></label>
        <label class="cbx"><input type="radio" name="cal-pkg" value="atoz" data-base="0" data-pp="60"><span>A to Z — $60/guest</span></label>
      </div>
      <label class="fl">{LL(CL["guests_en"], CL["guests_ar"])}</label>
      <input id="cal-guests" type="number" min="30" max="600" value="150">
      <label class="fl">{LL(CL["bar_en"], CL["bar_ar"])}</label>
      <select id="cal-bar">
        <option value="0">{esc(CL["bar_none_en"])} · {esc(CL["bar_none_ar"])}</option>
        <option value="15">{esc(CL["bar_open_en"])} · {esc(CL["bar_open_ar"])}</option>
        <option value="25">{esc(CL["bar_prem_en"])} · {esc(CL["bar_prem_ar"])}</option>
      </select>
    </div>
    <div>
      <label class="fl">{LL(CL["extras_en"], CL["extras_ar"])}</label>
      <div class="radios">{cal_extras}</div>
      <label class="fl">{LL(CL["deals_en"], CL["deals_ar"])}</label>
      <div class="radios">
        <label class="cbx"><input type="checkbox" id="cal-weekday"><span>{LL(CL["weekday_en"], CL["weekday_ar"])}</span></label>
        <label class="cbx"><input type="checkbox" id="cal-early"><span>{LL(CL["early_en"], CL["early_ar"])}</span></label>
      </div>
    </div>
  </div>
  <div class="cal-total"><span class="ct-lab">{LL(CL["total_en"], CL["total_ar"])}</span>
    <span class="ct-num" id="cal-total">$0</span></div>
  <p class="form-note">{LL(CL["note_en"], CL["note_ar"])}</p>
  <div class="cta-row"><button class="btn btn-wa" id="cal-send" type="button">{LL(CL["send_en"], CL["send_ar"])}</button>
  <button class="btn btn-line" id="cal-email" type="button">{LL(CL["email_en"], CL["email_ar"])}</button></div>
</div>"""

# gallery items (exclude tiny/low-quality)
import glob as _g
TAHANI = {3,4,6,7,8,9,10,11,12}
DRAJ = {2}
cat_over = {"restaurant_gallery-5":"nature","restaurant_gallery-6":"nature",
            "about_family":"nature","home_gallery-4":"nature","home_gallery-5":"nature",
            "events_weddings_gallery-5":"pool draj","restaurant_gallery-4":"food",
            "ducks_1":"nature family","ducks_2":"nature family","kidspark_1":"family"}
for _n in TAHANI: cat_over[f"events_weddings_gallery-{_n}"] = "weddings tahani"
for _n in DRAJ: cat_over[f"events_weddings_gallery-{_n}"] = "weddings draj"
for _n in ["soc_ig_16"]: cat_over[_n] = "weddings draj"
for _n in ["soc_fb_02","soc_fb_08","soc_fb_09","soc_fb_11","soc_fb_13","soc_fb_14","soc_fb_15","soc_fb_16","soc_fb_17","soc_fb_22","soc_ig_15"]:
    cat_over[_n] = "weddings tahani"
for _n in ["soc_fb_03","soc_fb_04","soc_fb_05","soc_fb_06","soc_fb_07","soc_ig_17"]: cat_over[_n] = "weddings"
for _n in ["soc_fb_18","soc_fb_25","soc_fb_26","soc_fb_27","soc_fb_28"]: cat_over[_n] = "food"
for _n in ["soc_fb_21","soc_fb_23","soc_ig_03"]: cat_over[_n] = "nature"
cat_over["tannour_1"] = "nature"
cat_over["soc_fb_24"] = "nature family"
for _n in ["soc_ig_01","soc_ig_02","soc_ig_07"]: cat_over[_n] = "chalets"
cat_over["soc_fb_20"] = "pool"
cat_over["pool_rates"] = "pool"
exclude = {"home_gallery-1","home_gallery-2","chalets_chalet-large_gallery-1","chalets_chalet-small_gallery-2","events_weddings_gallery-1","soc_fb_00"}
gitems = ""
for f in sorted(_g.glob(os.path.join(A,"*.jpg"))):
    n = os.path.basename(f)[:-4]
    import re as _re
    if _re.match(r'[wt]\d+q\d+_', n) or n.startswith("vid_") or n in exclude: continue
    if n.startswith("food_"): cat="food"
    elif n.startswith("events_"): cat="weddings"
    elif n.startswith("chalets_"): cat="chalets"
    elif n.startswith("pool_"): cat="pool"
    elif n.startswith("restaurant_"): cat="restaurant"
    else: cat="nature"
    cat = cat_over.get(n, cat)
    gitems += f'<figure class="gitem" data-cat="{cat}"><img src="{uri(n, 620, 54)}" alt="" loading="lazy"></figure>'
gcats = f'<button class="on" data-cat="all">{LL(G["all_en"], G["all_ar"])}</button>' + "".join(
    f'<button data-cat="{c["id"]}">{LL(c["en"], c["ar"])}</button>' for c in G["cats"])

times = "".join(f'<div class="rv"><div class="t">{t["time"]}</div><div class="f">{LL(t["from_en"], t["from_ar"])}</div></div>' for t in D["times"])
route_svg = """
<svg viewBox="0 0 460 300" role="img" aria-label="Route sketch from Beirut to Baissour">
  <path d="M60 20 C40 90 55 190 40 285" fill="none" stroke="var(--line)" stroke-width="3"/>
  <path d="M105 300 C140 240 150 200 210 170 C280 135 300 150 355 120" fill="none" stroke="var(--accent)" stroke-width="4" stroke-linecap="round" stroke-dasharray="1 9"/>
  <circle cx="105" cy="295" r="7" fill="var(--ink)"/>
  <text x="122" y="299" font-size="15" font-weight="700" fill="var(--ink)" font-family="Archivo,sans-serif">Beirut</text>
  <circle cx="210" cy="170" r="5" fill="var(--muted)"/>
  <text x="224" y="175" font-size="13" fill="var(--muted)" font-family="Archivo,sans-serif">Aley</text>
  <path d="M340 132 l15 -24 15 24 z" fill="none" stroke="var(--muted)" stroke-width="2.5"/>
  <path d="M368 132 l12 -19 12 19 z" fill="none" stroke="var(--muted)" stroke-width="2.5"/>
  <circle cx="355" cy="120" r="9" fill="var(--accent)"/>
  <text x="300" y="98" font-size="16" font-weight="900" fill="var(--ink)" font-family="Archivo,sans-serif">Baissour</text>
  <text x="296" y="160" font-size="12" fill="var(--muted)" font-family="Archivo,sans-serif">river valley · بيصور</text>
  <text x="30" y="40" font-size="12" fill="var(--muted)" font-family="Archivo,sans-serif" transform="rotate(78 30 40)">Mediterranean</text>
</svg>"""

wa = B["whatsapp_link"]
wa_svg = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2Zm5.3 14.2c-.2.6-1.3 1.2-1.8 1.2-.5.1-1 .2-3.3-.7-2.8-1.1-4.6-4-4.7-4.2-.1-.2-1.1-1.5-1.1-2.9s.7-2 1-2.3c.2-.3.5-.3.7-.3h.5c.2 0 .4 0 .6.5l.9 2.1c.1.2.1.4 0 .6l-.4.6-.5.5c-.2.2-.3.4-.1.7.2.3.8 1.4 1.8 2.2 1.3 1.1 2.3 1.5 2.6 1.6.3.2.5.1.7-.1l1-1.2c.2-.3.5-.2.8-.1l2 1c.3.1.5.2.6.4 0 .1 0 .7-.3 1.4Z"/></svg>'

# ------------------------------------------------------------------ assemble
html = f"""<meta charset="utf-8">
<title>Baissour Country Club</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="Baissour Country Club — chalets, mountain pool, riverside restaurant and two signature wedding venues in Mount Lebanon, 45 minutes from Beirut.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Almarai:wght@400;700;800&family=Archivo:wght@400;600;700;900&family=Aref+Ruqaa:wght@400;700&display=swap">
<style>{css}</style>

<div class="bar">
  <a href="#home"><img class="logo" src="{uri('shared_logo-color')}" alt="Baissour Country Club logo"></a>
  <nav aria-label="Sections">{nav}</nav>
  <button id="langbtn" class="lang-btn" type="button">عربي</button>
</div>

<div class="page on" id="pg-home">
<div class="hero">
  {video_or_img('hero_nature', 'tannour_1', 1920, 78, 'Al Tannour natural pool and waterfall at Baissour Country Club')}
  <div class="hero-inner">
    <div class="kicker">{LL(H["kicker_en"], H["kicker_ar"])}</div>
    <h1><span class="L en t-h1">{esc(H["h1_en"])}</span><span class="L ar t-h1" dir="rtl" lang="ar">{esc(H["h1_ar"])}</span></h1>
    <p class="sub">{LL(H["sub_en"], H["sub_ar"])}</p>
    <div class="cta-row">
      <a class="btn btn-solid" href="#weddings">{LL(H["cta1_en"], H["cta1_ar"])}</a>
      <a class="btn btn-ghost" href="#booking">{LL(H["cta2_en"], H["cta2_ar"])}</a>
    </div>
  </div>
</div>
<div class="stats">{stats}</div>
<main>
<section class="block" id="weddings">
  {sec_head(W)}
  {lead(W)}
  <div class="venues">{venues}</div>
  <div class="feat">{feat}</div>
  {celebrations_html}
  {packages_html}
  {calculator_html}
  <div class="quotes">{quotes}</div>
  {inquiry_form}
</section>
<section class="block" id="chalets">
  {sec_head(C)}
  {lead(C)}
  <div class="chgrid">{chcards}</div>
  <div class="chnotes">{chnotes}</div>
</section>
<section class="block" id="pool">
  {sec_head(P)}
  <div class="split">
    <div class="ph rv">{video_or_img('pool', 'events_weddings_gallery-5', 1100, 74, 'The pool at Baissour Country Club')}</div>
    <div>{lead(P)}<div class="points">{pool_pts}</div></div>
  </div>
  <div class="strip">
    <div class="ph rv"><img src="{uri('pool_gallery-2', 620, 54)}" alt="Pool deck" loading="lazy"></div>
    <div class="ph rv"><img src="{uri('pool_gallery-5', 620, 54)}" alt="Pool at night" loading="lazy"></div>
    <div class="ph rv"><img src="{uri('restaurant_gallery-6', 620, 54)}" alt="The river through the forest" loading="lazy"></div>
  </div>
  {pool_rates_html}
  {naturals_html}
</section>
{families_html}
<section class="block" id="restaurant">
  {sec_head(R)}
  <div class="split">
    <div>{lead(R)}
      <div class="cta-row" style="margin-top:24px">
        <a class="btn btn-solid" href="{B["menu_link"]}" target="_blank" rel="noopener">{LL(R["cta_en"], R["cta_ar"])}</a>
      </div>
    </div>
    <div class="ph rv"><img src="{uri('restaurant_hero', 940, 55)}" alt="The restaurant at Baissour Country Club" loading="lazy"></div>
  </div>
  <div class="strip strip4">
    <div class="ph rv"><img src="{uri('soc_fb_26', 620, 54)}" alt="Fresh tabbouleh and mezze" loading="lazy"></div>
    <div class="ph rv"><img src="{uri('soc_fb_25', 620, 54)}" alt="Lebanese spread" loading="lazy"></div>
    <div class="ph rv"><img src="{uri('soc_fb_18', 620, 54)}" alt="Flambé at the kitchen" loading="lazy"></div>
    <div class="ph rv"><img src="{uri('soc_fb_28', 620, 54)}" alt="Lunch by the river" loading="lazy"></div>
  </div>
</section>
{socials_html}
<section class="block" id="area">
  {sec_head(AR_)}
  {lead(AR_)}
  <div class="band rv"><img src="{uri('about_family', 1200, 56)}" alt="The river at Baissour" loading="lazy">
    <div class="cap"><div class="q" dir="rtl" lang="ar">{esc(AR_["quote_ar"])}</div>
    <div class="L en">{esc(AR_["quote_en"])}</div><div class="L ar" dir="rtl" lang="ar">&nbsp;</div></div></div>
</section>
{giftshop_html}
<section class="block" id="contact">
  {sec_head(CT)}
  <div class="contact-grid">
    <div class="ccard rv">
      <h3>{LL("Talk to us", "احكينا")}</h3>
      <p>{LL(CT["lead_en"], CT["lead_ar"])}</p>
      <a class="wa-big" href="{wa}" target="_blank" rel="noopener">{wa_svg} {B["whatsapp_display"]}</a>
      <div class="socials">
        <a href="{B["instagram"]}" target="_blank" rel="noopener">Instagram</a>
        <a href="{B["facebook"]}" target="_blank" rel="noopener">Facebook</a>
        <a href="mailto:{B["email"]}">{LL("Email", "إيميل")}</a>
        <a href="{B["menu_link"]}" target="_blank" rel="noopener">{LL("Menu", "المنيو")}</a>
      </div>
    </div>
    <div class="ccard rv">
      <h3>{LL("Getting here", "كيف توصل")}</h3>
      <p>{LL(CT["directions_en"], CT["directions_ar"])}</p>
      <p style="margin-top:12px;font-weight:700">{LL(CT["address_en"], CT["address_ar"])}</p>
      <div class="cta-row" style="margin-top:16px"><a class="btn btn-line" href="#directions">{LL("Maps & directions", "الخريطة والطريق")}</a></div>
    </div>
  </div>
</section>
</main>
</div>

<div class="page" id="pg-gallery">
<main class="pagehead">
  <section class="block">
    {sec_head(G, "h1")}
    {lead(G)}
    <div class="gcats">{gcats}</div>
    <div class="gwrap">{gitems}</div>
  </section>
</main>
</div>

<div class="page" id="pg-booking">
<main class="pagehead">
  <section class="block">
    {sec_head(BK, "h1")}
    {lead(BK)}
    {booking_form}
    <div class="chnotes">{chnotes}</div>
  </section>
</main>
</div>

<div class="page" id="pg-directions">
<main class="pagehead">
  <section class="block">
    {sec_head(D, "h1")}
    {lead(D)}
    <div class="dgrid">
      <div>
        <div class="timegrid">{times}</div>
        <p class="form-note">{LL(D["times_note_en"], D["times_note_ar"])}</p>
        <div class="route-line">{LL(D["route_en"], D["route_ar"])}</div>
        <div class="cta-row" style="margin-top:20px">
          <a class="btn btn-solid" href="{D["maps_url"]}" target="_blank" rel="noopener">{LL(D["maps_en"], D["maps_ar"])}</a>
          <a class="btn btn-line" href="{D["waze_url"]}" target="_blank" rel="noopener">{LL(D["waze_en"], D["waze_ar"])}</a>
        </div>
        <p class="form-note" style="margin-top:16px">{LL(CT["address_en"], CT["address_ar"])}</p>
      </div>
      <div class="routecard rv">{route_svg}</div>
    </div>
  </section>
</main>
</div>

<div class="lightbox" id="lightbox" role="dialog" aria-label="Photo"><img id="lightbox-img" alt=""></div>

<footer>
  <img class="logo" src="{uri('shared_logo-color')}" alt="">
  <div>{LL(B["name_en"], B["name_ar"])} — {LL(B["tagline_en"], B["tagline_ar"])}</div>
  <div style="margin-top:8px">© {LL("Baissour Country Club. All rights reserved.", "منتجع بيصور السياحي. جميع الحقوق محفوظة.")}</div>
</footer>

<a class="wa-float" href="{wa}" target="_blank" rel="noopener" aria-label="WhatsApp">{wa_svg}</a>
<script>{js}</script>
"""
open(os.path.join(DIST if DEPLOY else ROOT, "index.html"), "w").write(html)
print("index.html", len(html), "bytes")
