#!/usr/bin/env python3
"""Renders the bilingual BCC Grill team manual (EN left / AR right) to HTML, then PDF via Playwright."""
import html, subprocess, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from manual_content import TITLE, SUB, SECTIONS

OUT = Path(__file__).parent / 'out'; OUT.mkdir(exist_ok=True)
CH, LIME, CREAM = '#2E2E30', '#8DC63F', '#F4F3EE'
E = lambda s: html.escape(s)

CSS = f"""
@page{{size:A4;margin:14mm 12mm 16mm}}
*{{box-sizing:border-box}} body{{margin:0;font:10pt/1.4 Rubik,'Helvetica Neue',Arial,sans-serif;color:{CH};background:#fff}}
.ar{{font-family:Alexandria,Rubik,sans-serif;direction:rtl;text-align:right}}
.disp{{font-family:'Bricolage Grotesque',sans-serif;font-weight:800;letter-spacing:-.02em}}
.ar.disp{{font-family:Alexandria,sans-serif;font-weight:900;letter-spacing:0}}
.cover{{height:265mm;display:flex;flex-direction:column;justify-content:space-between;background:{CH};color:{CREAM};border-radius:6mm;padding:14mm;page-break-after:always}}
.cover .big{{font-size:34pt;line-height:1.05}}
.cover .ar.big{{font-size:30pt}}
.pill{{display:inline-block;background:{LIME};color:{CH};border-radius:999px;padding:.15em .7em;font-weight:800}}
h1.sec{{font-size:20pt;margin:0 0 2mm;padding-bottom:2mm;border-bottom:3px solid {LIME};display:grid;grid-template-columns:1fr 1fr;gap:6mm;page-break-before:always}}
h1.sec:first-of-type{{page-break-before:auto}}
.two{{display:grid;grid-template-columns:1fr 1fr;gap:6mm;align-items:start}}
.intro{{font-size:9.5pt;opacity:.85;margin:0 0 4mm}}
.block{{break-inside:avoid;margin:0 0 5mm;border:1px solid rgba(46,46,48,.12);border-radius:4mm;padding:3.5mm 4mm}}
.block h3{{margin:0 0 1.5mm;font-size:12.5pt}}
.block .yields{{font-size:8.5pt;opacity:.65;margin:0 0 2mm}}
.lbl{{font-size:7.5pt;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:#3f7d1c;margin:2mm 0 1mm}}
.ar .lbl{{letter-spacing:0}}
ul,ol{{margin:0;padding-inline-start:1.3em}} li{{margin:.15em 0}}
ol.steps li{{margin:.3em 0}}
.pack{{background:#F4F3EE;border-radius:3mm;padding:2mm 3mm;margin-top:2mm;font-size:9pt}}
.tip{{border-inline-start:3px solid {LIME};padding:1mm 3mm;margin-top:2mm;font-size:9pt}}
.confirm{{display:inline-block;background:#FBEFD6;color:#7a4b00;border-radius:999px;padding:.1em .6em;font-size:7.5pt;font-weight:700;margin-inline-start:.5em;vertical-align:middle}}
.photos{{display:grid;grid-template-columns:repeat(4,1fr);gap:2mm;margin-top:2.5mm}}
.ph{{aspect-ratio:4/3;border:1.5px dashed rgba(46,46,48,.3);border-radius:2.5mm;display:flex;align-items:center;justify-content:center;font-size:7.5pt;opacity:.6;text-align:center;padding:1mm}}
.check li{{list-style:none;position:relative;padding-inline-start:1.6em}}
.check li::before{{content:'';position:absolute;inset-inline-start:0;top:.25em;width:1em;height:1em;border:1.5px solid {CH};border-radius:.25em}}
.foot{{position:fixed;bottom:4mm;left:12mm;right:12mm;font-size:7.5pt;opacity:.55;display:flex;justify-content:space-between}}
"""
FONTS = '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,700;12..96,800&family=Alexandria:wght@400;500;700;900&family=Rubik:wght@400;500;600;700&display=swap">'

def li(pairs, cls=''):
    en = ''.join(f'<li>{E(a)}</li>' for a, _ in pairs); ar = ''.join(f'<li>{E(b)}</li>' for _, b in pairs)
    return en, ar

def render_block(b):
    if b['type'] == 'text':
        en = ''.join(f'<li>{E(a)}</li>' for a, _ in b['paras']); ar = ''.join(f'<li>{E(x)}</li>' for _, x in b['paras'])
        return f'<div class="block"><div class="two"><div><h3 class="disp">{E(b["title"][0])}</h3><ul>{en}</ul></div><div class="ar"><h3 class="disp ar">{E(b["title"][1])}</h3><ul>{ar}</ul></div></div></div>'
    if b['type'] == 'check':
        en, ar = li(b['items'])
        return f'<div class="block"><div class="two"><div><h3 class="disp">{E(b["title"][0])}</h3><ul class="check">{en}</ul></div><div class="ar"><h3 class="disp ar">{E(b["title"][1])}</h3><ul class="check">{ar}</ul></div></div></div>'
    # recipe
    conf = '<span class="confirm">CONFIRM WITH GRILL LEAD</span>' if b['confirm'] else ''
    conf_ar = '<span class="confirm">يتأكّد مع مسؤول المشاوي</span>' if b['confirm'] else ''
    ing_en, ing_ar = li(b['ingredients']); st_en, st_ar = li(b['steps'])
    def side(lang):
        i = 0 if lang == 'en' else 1
        L = ['Ingredients & portions', 'Steps', 'Pack it', 'Tip'] if lang == 'en' else ['المكوّنات والحصص', 'الخطوات', 'التوضيب', 'نصيحة']
        h = f'<h3 class="disp{" ar" if lang=="ar" else ""}">{E(b["name"][i])}{conf if lang=="en" else conf_ar}</h3>'
        if b['yields'][i]: h += f'<div class="yields">{E(b["yields"][i])}</div>'
        if b['ingredients']: h += f'<div class="lbl">{L[0]}</div><ul>{ing_en if lang=="en" else ing_ar}</ul>'
        if b['steps']: h += f'<div class="lbl">{L[1]}</div><ol class="steps">{st_en if lang=="en" else st_ar}</ol>'
        if b['pack']: h += f'<div class="pack"><div class="lbl" style="margin-top:0">{L[2]}</div>' + ''.join(f'<div>· {E(p[i])}</div>' for p in b['pack']) + '</div>'
        if b['tips']: h += ''.join(f'<div class="tip">{E(t[i])}</div>' for t in b['tips'])
        return f'<div class="{"ar" if lang=="ar" else ""}">{h}</div>'
    photos = ''
    if b['photo']:
        n = min(4, max(2, len(b['steps'])))
        photos = '<div class="photos">' + ''.join(f'<div class="ph">📷 Step {k+1} · خطوة {k+1}<br>photo on training day</div>' for k in range(n)) + '</div>'
    return f'<div class="block"><div class="two">{side("en")}{side("ar")}</div>{photos}</div>'

body = [f'<div class="cover"><div><div class="pill">BCC GRILL · TEAM MANUAL</div><div class="disp big" style="margin-top:10mm">{E(TITLE[0])}</div><div class="disp big ar" style="margin-top:3mm">{E(TITLE[1])}</div></div>'
        f'<div><div>{E(SUB[0])}</div><div class="ar">{E(SUB[1])}</div><div style="margin-top:8mm;font-size:9pt;opacity:.8">English on the left · Arabic on the right · Items marked CONFIRM are standard methods to be confirmed or corrected by the grill lead on training day · Photo boxes are filled on training day.<br><span class="ar" style="display:block;margin-top:1mm">الإنكليزي ع اليسار · العربي ع اليمين · الأصناف المعلّمة "يتأكّد" طرق قياسية بيأكّدها أو بيصحّحها مسؤول المشاوي يوم التدريب · مربّعات الصور بتتعبّى يوم التدريب.</span></div></div></div>']
for s in SECTIONS:
    body.append(f'<h1 class="sec"><span class="disp">{E(s["title"][0])}</span><span class="disp ar">{E(s["title"][1])}</span></h1>')
    if s['intro']: body.append(f'<div class="two"><p class="intro">{E(s["intro"][0])}</p><p class="intro ar">{E(s["intro"][1])}</p></div>')
    body += [render_block(b) for b in s['blocks']]
body.append(f'<div class="foot"><span>BCC Grill · Team Manual v1 · Nov 2026</span><span>Internal — not for customers</span></div>')
doc = f'<!doctype html><html lang="en"><head><meta charset="utf-8">{FONTS}<style>{CSS}</style></head><body>{"".join(body)}</body></html>'
(OUT / 'manual.html').write_text(doc, encoding='utf-8')
js = f"""
const {{ chromium }} = require('playwright');
(async()=>{{const b=await chromium.launch();const p=await b.newPage();await p.goto('file://{OUT}/manual.html',{{waitUntil:'networkidle'}});await p.waitForTimeout(1500);
await p.pdf({{path:'{OUT}/BCC_Grill_Team_Manual_EN_AR.pdf',format:'A4',printBackground:true,preferCSSPageSize:true}});await b.close();console.log('pdf ok');}})();
"""
(OUT / 'render.js').write_text(js)
subprocess.run(['node', str(OUT / 'render.js')], check=True)
