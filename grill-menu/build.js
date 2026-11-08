// Builds every BCC Grill menu piece from menu.json.
const fs = require('fs'); const path = require('path');
const M = JSON.parse(fs.readFileSync(path.join(__dirname, 'menu.json'), 'utf8'));
const OUT = path.join(__dirname, 'out');

const CH = '#2E2E30', LIME = '#8DC63F', CREAM = '#F4F3EE', GREY = '#58585B';
const AR_DIGITS = s => String(s).replace(/[0-9]/g, d => '٠١٢٣٤٥٦٧٨٩'[d]);
const price = (p, lang) => {
  if (typeof p === 'string') { // "13 · 7"
    return '<bdi dir="ltr">' + p.split('·').map(x => '$' + x.trim()).join(' · ') + '</bdi>';
  }
  const s = Number.isInteger(p) ? String(p) : p.toFixed(2).replace(/0$/, '');
  return '<bdi dir="ltr">$' + s + '</bdi>';
};
const t = (o, k, lang) => o[k + (lang === 'ar' ? 'Ar' : 'En')] ?? '';

const FONTS = `<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,700;12..96,800&family=Alexandria:wght@400;500;700;900&family=Rubik:wght@400;500;600;700&display=swap">`;

const BASE_CSS = `
*{box-sizing:border-box} body{margin:0;background:${CREAM};color:${CH};font-family:Rubik,'Helvetica Neue',Arial,sans-serif;-webkit-font-smoothing:antialiased}
.disp{font-family:'Bricolage Grotesque',sans-serif;font-weight:800;letter-spacing:-.03em}
.ar{font-family:Alexandria,Rubik,sans-serif;direction:rtl}
[dir=rtl] .disp{font-family:Alexandria,sans-serif;font-weight:900;letter-spacing:0}
[dir=rtl] body, [dir=rtl]{font-family:Alexandria,Rubik,sans-serif}
.pill{display:inline-block;background:${LIME};color:${CH};border-radius:999px;padding:.12em .55em;font-weight:800}
.tag{display:inline-block;font-size:.62em;font-weight:700;letter-spacing:.08em;text-transform:uppercase;border-radius:999px;padding:.15em .5em;vertical-align:middle;margin-inline-start:.4em}
.tag.new{background:${LIME};color:${CH}}
.pick{color:#3f7d1c;font-weight:900;margin-inline-end:.25em}
.panel{background:#fff;border-radius:12px;padding:.7em .9em;border:1px solid rgba(46,46,48,.08)}
.panel h4{margin:0 0 .35em;font-size:1.05em;display:flex;align-items:baseline;gap:.4em}
.panel .intro{font-size:.72em;opacity:.7;margin:0 0 .4em;line-height:1.3}
.prot{width:100%;border-collapse:collapse;font-size:.8em}
.prot th{font-weight:600;text-align:end;font-size:.85em;opacity:.65;padding:0 0 .2em}
.prot th:first-child{text-align:start}
.prot td{padding:.18em 0;border-top:1px solid rgba(46,46,48,.08)}
.prot td.u{text-align:end;font-weight:700;color:#3f7d1c;white-space:nowrap}
.adds{columns:2;column-gap:1em;font-size:.8em}
.adds div{display:flex;justify-content:space-between;gap:.5em;padding:.15em 0;break-inside:avoid;border-bottom:1px solid rgba(46,46,48,.08)}
.adds div b{color:#3f7d1c;font-weight:700;white-space:nowrap}
.steps{counter-reset:s;list-style:none;margin:0;padding:0;font-size:.8em;line-height:1.3}
.steps li{display:flex;gap:.5em;padding:.2em 0}
.steps li::before{counter-increment:s;content:counter(s);flex:none;width:1.5em;height:1.5em;border-radius:999px;background:${LIME};color:${CH};font-weight:800;display:inline-flex;align-items:center;justify-content:center;font-size:.9em} .tag.vg{background:transparent;color:#3f7d1c;border:1.5px solid #3f7d1c}
[dir=rtl] .tag{letter-spacing:0;text-transform:none}
.sec h3{margin:0 0 .25em;font-size:1.25em;display:flex;justify-content:space-between;align-items:baseline;gap:.5em}
.sec h3 .alt{font-size:.78em;font-weight:700;opacity:.8}
.sec .note{font-size:.72em;opacity:.7;margin:0 0 .5em}
.rule{height:4px;background:${LIME};border-radius:2px;margin:.2em 0 .55em}
.item{display:flex;justify-content:space-between;align-items:baseline;gap:.6em;padding:.32em 0;border-bottom:1px solid rgba(46,46,48,.12)}
.item:last-child{border-bottom:0}
.item .n{font-weight:600;line-height:1.15}
[dir=ltr] .alt.ar{text-align:left} .item .n .alt{display:block;font-size:.78em;font-weight:500;opacity:.75;margin-top:.1em}
.item .n .sub{display:block;font-size:.74em;font-weight:400;opacity:.7;margin-top:.12em}
.item .p{font-weight:800;color:#3f7d1c;white-space:nowrap;font-family:'Bricolage Grotesque',sans-serif;letter-spacing:-.02em}
[dir=rtl] .item .p{font-family:Alexandria,sans-serif}
.brand{display:flex;align-items:center;gap:.5em}
.brand img{height:1.6em;width:auto;display:block}
.brand .bcc{font-size:2.1em;line-height:1}
.brand .grill{font-size:.78em;background:${LIME};color:${CH};border-radius:999px;padding:.15em .55em}
.hero{position:relative;border-radius:14px;overflow:hidden;background:${CH}}
.hero img{width:100%;height:100%;object-fit:cover;display:block}
.hero .cap{position:absolute;left:0;right:0;bottom:0;padding:.6em .7em .55em;background:linear-gradient(to top,rgba(46,46,48,.92),rgba(46,46,48,0));color:${CREAM}}
.hero .cap .t{font-size:1em;display:flex;justify-content:space-between;gap:.5em;align-items:baseline}
.hero .cap .t .alt{font-size:.8em;opacity:.8}
.hero .cap .d{font-size:.66em;opacity:.85;margin-top:.15em;line-height:1.3}
.hero .pr{position:absolute;top:.6em;inset-inline-end:.6em;background:${LIME};color:${CH};border-radius:999px;padding:.15em .6em;font-size:1em}
.hero .nw{position:absolute;top:.6em;inset-inline-start:.6em;background:${CREAM};color:${CH};border-radius:999px;padding:.15em .55em;font-size:.6em;font-weight:800;letter-spacing:.08em}
.dark{background:${CH};color:${CREAM}} .dark .item{border-color:rgba(244,243,238,.14)} .dark .item .p{color:${LIME}} .dark .sec .note{opacity:.65}
.band{background:${LIME};color:${CH};border-radius:14px;padding:.8em 1em}
.box{background:#fff;border-radius:14px;padding:.8em 1em;border:1px solid rgba(46,46,48,.08)}
`;

function brandMark(lang, cream) {
  const logo = cream ? 'img/logo-mark-cream.png' : 'img/logo-mark.png';
  return `<div class="brand"><img src="${logo}" alt=""><span class="disp bcc" style="font-family:'Bricolage Grotesque'">bcc</span><span class="disp grill" style="font-family:'Bricolage Grotesque'">grill</span></div>`;
}
function hero(s, lang, bilingual) {
  const alt = bilingual ? `<span class="alt ${lang === 'ar' ? '' : 'ar'}">${lang === 'ar' ? s.en : s.ar}</span>` : '';
  return `<div class="hero"><img src="img/${s.photo.replace('.jpg', '.jpg')}" alt="">${s.new ? `<div class="nw">${lang === 'ar' ? 'جديد' : 'NEW'}</div>` : ''}<div class="pr disp">${price(s.price)}</div><div class="cap"><div class="t"><span class="disp">${lang === 'ar' ? s.ar : s.en}</span>${alt}</div><div class="d">${t(s, 'desc', lang)}</div></div></div>`;
}
function tags(it, lang) {
  let h = '';
  if (it.new) h += `<span class="tag new">${lang === 'ar' ? 'جديد' : 'new'}</span>`;
  if (it.vegan) h += `<span class="tag vg">${lang === 'ar' ? 'نباتي' : 'vegan'}</span>`;
  return h;
}
function section(sec, lang, bilingual, opts = {}) {
  const name = lang === 'ar' ? sec.ar : sec.en;
  const alt = bilingual ? `<span class="alt ${lang === 'ar' ? '' : 'ar'}">${lang === 'ar' ? sec.en : sec.ar}</span>` : '';
  const note = t(sec, 'note', lang);
  const items = sec.items.map(it => {
    const altn = bilingual ? `<span class="alt ${lang === 'ar' ? '' : 'ar'}">${lang === 'ar' ? it.en : it.ar}</span>` : '';
    const sub = opts.noSub ? '' : (t(it, 'sub', lang) ? `<span class="sub">${t(it, 'sub', lang)}</span>` : '');
    const pk = it.pick ? `<span class="pick" title="your choice">▸</span>` : '';
    return `<div class="item"><div class="n">${pk}${lang === 'ar' ? it.ar : it.en}${tags(it, lang)}${altn}${sub}</div><div class="p">${price(it.price)}</div></div>`;
  }).join('');
  return `<div class="sec"><h3><span class="disp">${name}</span>${alt}</h3><div class="rule"></div>${note ? `<p class="note">${note}</p>` : ''}${items}</div>`;
}
function kiloBand(lang, bilingual, dark) {
  const K = M.kilo;
  const items = K.items.map(it => `<span style="white-space:nowrap"><b>${lang === 'ar' ? it.ar : it.en}</b> ${price(it.price)}</span>`).join(' <span style="opacity:.5">·</span> ');
  return `<div class="band"><div style="display:flex;justify-content:space-between;gap:1em;align-items:baseline;flex-wrap:wrap"><span class="disp" style="font-size:1.25em">${lang === 'ar' ? K.ar : K.en}${bilingual ? ` <span class="${lang === 'ar' ? '' : 'ar'}" style="font-size:.7em;font-weight:700;opacity:.8">${lang === 'ar' ? K.en : K.ar}</span>` : ''}</span><span style="font-weight:700;font-size:.9em">${items}</span></div><div style="font-size:.74em;margin-top:.35em;line-height:1.35;opacity:.9">${t(K, 'line', lang)} · <b>${t(K, 'sunday', lang)}</b></div></div>`;
}
const footer = (lang) => {
  const B = M.brand;
  return `<div style="display:flex;justify-content:space-between;gap:1em;align-items:flex-start;flex-wrap:nowrap"><div style="flex:none"><div class="disp" style="font-size:1.5em">WhatsApp · <bdi dir="ltr">${B.phone}</bdi></div><div style="font-size:.78em;opacity:.8;margin-top:.15em">${t(B, 'hours', lang)} · ${t(B, 'address', lang)}</div></div><div style="text-align:end;font-size:.78em;line-height:1.45"><div>${t(B, 'delivery', lang)}</div><div style="opacity:.8">${t(B, 'pay', lang)}</div><div><b>${B.web}</b> · Instagram <b>${B.instagram}</b></div><div style="opacity:.8"><bdi dir="ltr">${B.mapsShort}</bdi></div></div></div>`;
};

/* ---------- PRINTED A4, two pages ---------- */
function printedMenu(lang) {
  const dir = lang === 'ar' ? 'rtl' : 'ltr';
  const B = M.brand;
  const sec = id => M.sections.find(s => s.id === id);
  const css = BASE_CSS + `
  @page{size:A4;margin:0}
  html,body{width:210mm}
  .page{width:210mm;height:297mm;padding:8mm 11mm 7mm;position:relative;page-break-after:always;overflow:hidden;font-size:9.3pt;display:flex;flex-direction:column}
  .page:last-child{page-break-after:auto}
  .head{display:flex;justify-content:space-between;align-items:flex-end;gap:1em;padding-bottom:3mm;border-bottom:1.5px solid ${CH}}
  .head .right{text-align:end}
  .heroes{display:grid;grid-template-columns:repeat(2,1fr);gap:3mm;margin:3.5mm 0 3mm}
  .heroes .hero{height:39mm;font-size:9.3pt}
  .cols{display:grid;grid-template-columns:1fr 1fr;gap:5mm;flex:1}
  .cols .sec{margin-bottom:2.5mm}
  .foot{margin-top:auto;padding-top:3mm;border-top:1.5px solid ${CH}}
  .hero .cap{background:none;color:${CH};padding:1.6mm 2.4mm 1.8mm;text-shadow:0 0 2mm ${LIME},0 0 1mm ${LIME},0 0 .5mm ${LIME}}
  .hero .cap .t .alt{opacity:.75}
  .hero .cap .d{opacity:.9}
  .hero .nw{background:${CH};color:${CREAM}}
  .pagenum{position:absolute;bottom:4mm;inset-inline-end:11mm;font-size:7pt;opacity:.5}
  `;
  const head = `<div class="head"><div>${brandMark(lang)}<div class="${lang === 'ar' ? '' : 'ar'}" style="font-size:8.5pt;font-weight:700;margin-top:1.5mm;opacity:.85">${B.arLine}${lang === 'ar' ? '' : ' · ' + B.takeawayAr}</div></div><div class="right"><div class="disp" style="font-size:19pt">${lang === 'ar' ? 'منيو تيك أواي' : 'Take-away menu'}</div><div style="font-size:7.5pt;letter-spacing:${lang === 'ar' ? 0 : '.12em'};opacity:.7;margin-top:1mm">${t(B, 'prices', lang)}</div></div></div>`;

  const page1 = `<div class="page" dir="${dir}">${head}
    <div class="heroes">${M.signatures.map(s => hero(s, lang, false).replace('img/', 'img/print/')).join('')}</div>
    <div class="cols"><div>${section(sec('charcoal'), lang, false)}${section(sec('kids'), lang, false)}</div><div>${section(sec('snack'), lang, false)}${section(sec('burgers'), lang, false)}${section(sec('lean'), lang, false)}</div></div>
    <div class="foot">${footer(lang)}</div></div>`;

  const scan = lang === 'ar' ? 'امسح واطلب' : 'Scan to order';
  const up = v => v ? `<bdi dir="ltr">+$${v}</bdi>` : '—';
  const P = M.proteins, A = M.addons, O = M.order, R = M.rewards;
  const protPanel = `<div class="panel"><h4 class="disp"><span class="pick">▸</span>${t(P, 'title', lang)}</h4><p class="intro">${t(P, 'intro', lang)}</p><table class="prot"><tr><th>${lang === 'ar' ? 'البروتين' : 'Protein'}</th><th>${lang === 'ar' ? 'الزيادة' : 'Extra'}</th></tr>${P.items.map(x => `<tr><td>${lang === 'ar' ? x.ar : x.en}</td><td class="u">${up(x.up[0])}</td></tr>`).join('')}</table></div>`;
  const addPanel = `<div class="panel"><h4 class="disp">${t(A, 'title', lang)}</h4><p class="intro">${t(A, 'intro', lang)}</p><div class="adds">${A.items.map(x => `<div><span>${lang === 'ar' ? x.ar : x.en}</span><b><bdi dir="ltr">+$${x.price}</bdi></b></div>`).join('')}</div></div>`;
  const mealPanel = `<div class="panel"><h4 class="disp">${t(M.meal, 'title', lang)}</h4><div style="font-size:.8em;line-height:1.35;opacity:.9">${t(M.meal, 'text', lang)}</div><h4 class="disp" style="margin-top:.6em">${t(R, 'title', lang)}</h4><div style="font-size:.8em;line-height:1.35;opacity:.9">${t(R, 'text', lang)}</div></div>`;
  const steps = (lang === 'ar' ? O.stepsAr : O.stepsEn);
  const orderPanel = `<div class="panel"><h4 class="disp">${t(O, 'title', lang)}</h4><ol class="steps">${steps.map(x => `<li><span>${x}</span></li>`).join('')}</ol></div>`;
  const qrPanel = `<div class="panel dark" style="display:flex;flex-direction:column;align-items:center;justify-content:center;gap:2mm;text-align:center;background:${CH};color:${CREAM}"><div style="display:flex;gap:3mm"><div><div style="background:#fff;border-radius:2.5mm;padding:2mm;width:24mm;height:24mm"><img src="img/qr.png" style="width:100%;height:100%;display:block" alt="QR"></div><div class="disp" style="font-size:.95em;margin-top:1.5mm">${scan}</div><div style="font-size:.66em;opacity:.75">${B.web}</div></div><div><div style="background:#fff;border-radius:2.5mm;padding:2mm;width:24mm;height:24mm"><img src="img/qr_maps.png" style="width:100%;height:100%;display:block" alt="QR"></div><div class="disp" style="font-size:.95em;margin-top:1.5mm">${lang === 'ar' ? 'موقعنا' : 'Find us'}</div><div style="font-size:.66em;opacity:.75">Google Maps</div></div></div><div style="font-size:.75em;opacity:.85">Instagram ${B.instagram} · WhatsApp <bdi dir="ltr">${B.phone}</bdi></div></div>`;
  const page2 = `<div class="page" dir="${dir}">${head}
    <div class="cols" style="margin-top:3mm;flex:0 0 auto"><div>${section(sec('plates'), lang, false)}${section(sec('desserts'), lang, false)}</div>
    <div>${section(sec('sides'), lang, false)}${section(sec('drinks'), lang, false)}</div></div>
    <div style="margin-top:3mm">${kiloBand(lang, false)}</div>
    <div style="display:grid;grid-template-columns:1.15fr 1fr 1fr;gap:3mm;margin-top:3mm;font-size:8pt">${protPanel}${addPanel}${mealPanel}</div>
    <div style="display:grid;grid-template-columns:1fr 60mm;gap:3mm;margin-top:3mm;font-size:8pt;flex:0 0 auto">${orderPanel}${qrPanel}</div>
    <div class="foot">${footer(lang)}</div></div>`;
  return `<!doctype html><html lang="${lang}" dir="${dir}"><head><meta charset="utf-8">${FONTS}<style>${css}</style></head><body>${page1}${page2}</body></html>`;
}

/* ---------- TV BOARD 1920x1080 ---------- */
function tvBoard(lang, bilingual) {
  const dir = lang === 'ar' ? 'rtl' : 'ltr';
  const B = M.brand; const sec = id => M.sections.find(s => s.id === id);
  const css = BASE_CSS + `
  body{width:1920px;height:1080px;overflow:hidden;background:${CH};color:${CREAM}}
  .board{width:1920px;height:1080px;padding:38px 56px 32px;display:flex;flex-direction:column;gap:18px;font-size:19px}
  .head{display:flex;justify-content:space-between;align-items:center}
  .heroes{display:grid;grid-template-columns:repeat(4,1fr);gap:16px}
  .heroes .hero{height:196px;font-size:20px}
  .cols{display:grid;grid-template-columns:repeat(6,1fr);gap:22px;flex:1}
  .sec h3{font-size:25px} .sec .note{font-size:14px} .item{padding:5px 0} .item .n .sub{display:none} .item .n .alt{font-size:.74em}
  .rule{margin:4px 0 8px}
  .band{font-size:19px;padding:12px 22px;border-radius:16px}
  `;
  const head = `<div class="head"><div>${brandMark(lang, true)}<div class="${lang === 'ar' ? '' : 'ar'}" style="font-size:15px;font-weight:700;margin-top:6px;opacity:.85">${B.arLine} · ${B.takeawayAr}</div></div><div style="display:flex;align-items:center;gap:22px"><div style="text-align:end"><div class="disp" style="font-size:40px">WhatsApp · <bdi dir="ltr">${B.phone}</bdi></div><div style="font-size:16px;opacity:.85;margin-top:2px">${B.web} · Instagram ${B.instagram}</div><div style="font-size:13px;letter-spacing:${lang === 'ar' ? 0 : '.14em'};opacity:.6;margin-top:3px">${t(B, 'prices', lang)}</div></div><div style="background:#fff;border-radius:10px;padding:6px;width:92px;height:92px"><img src="img/qr.png" style="width:100%;height:100%;display:block"></div></div></div>`;
  const colsList = [
    section(sec('charcoal'), lang, bilingual),
    section(sec('snack'), lang, bilingual),
    section(sec('burgers'), lang, bilingual) + section(sec('kids'), lang, bilingual),
    section(sec('plates'), lang, bilingual, { noSub: true }),
    section(sec('lean'), lang, bilingual) + section(sec('sides'), lang, bilingual),
    section(sec('desserts'), lang, bilingual) + section(sec('drinks'), lang, bilingual),
  ];
  return `<!doctype html><html lang="${lang}" dir="${dir}"><head><meta charset="utf-8">${FONTS}<style>${css}</style></head><body class="dark"><div class="board dark">${head}<div class="heroes">${M.signatures.map(s => hero(s, lang, bilingual)).join('')}</div><div class="cols">${colsList.map(c => `<div>${c}</div>`).join('')}</div>${kiloBand(lang, bilingual, true)}</div></body></html>`;
}

/* ---------- PHONE IMAGE 1080 wide ---------- */
function phoneMenu(lang, bilingual) {
  const dir = lang === 'ar' ? 'rtl' : 'ltr';
  const B = M.brand; const sec = id => M.sections.find(s => s.id === id);
  const css = BASE_CSS + `
  body{width:1080px;font-size:30px;padding:0}
  .wrap{padding:56px 54px 64px;display:flex;flex-direction:column;gap:34px}
  .head{display:flex;justify-content:space-between;align-items:flex-end;gap:20px;padding-bottom:22px;border-bottom:3px solid ${CH}}
  .heroes{display:grid;grid-template-columns:1fr 1fr;gap:18px}
  .heroes .hero{height:330px;font-size:30px}
  .hero .cap .d{display:none}
  .sec h3{font-size:40px} .sec .note{font-size:22px} .item{padding:11px 0}
  .band{font-size:28px;padding:26px 30px;border-radius:22px}
  .box{font-size:24px;line-height:1.45;padding:26px 30px;border-radius:22px}
  .foot{padding-top:22px;border-top:3px solid ${CH}}
  `;
  const head = `<div class="head"><div>${brandMark(lang)}<div class="${lang === 'ar' ? '' : 'ar'}" style="font-size:24px;font-weight:700;margin-top:10px;opacity:.85">${B.arLine}</div></div><div style="text-align:end"><div class="disp" style="font-size:44px">${lang === 'ar' ? 'المنيو' : 'Menu'}</div><div style="font-size:20px;opacity:.7;margin-top:4px">${t(B, 'prices', lang)}</div></div></div>`;
  const secs = ['charcoal', 'snack', 'burgers', 'kids', 'plates', 'lean', 'sides', 'desserts', 'drinks'].map(id => section(sec(id), lang, bilingual)).join('');
  return `<!doctype html><html lang="${lang}" dir="${dir}"><head><meta charset="utf-8">${FONTS}<style>${css}</style></head><body><div class="wrap">${head}<div class="heroes">${M.signatures.map(s => hero(s, lang, bilingual)).join('')}</div>${secs}${kiloBand(lang, bilingual)}<div class="box"><b class="disp" style="font-size:1.2em">${t(M.meal, 'title', lang)}</b><div style="margin-top:.3em;opacity:.85">${t(M.meal, 'text', lang)}</div></div><div class="box"><b class="disp" style="font-size:1.2em">${t(M.order, 'title', lang)}</b><div style="margin-top:.3em;opacity:.85">${t(M.order, 'text', lang)}</div></div><div class="box dark" style="background:${CH};color:${CREAM};display:flex;gap:28px;align-items:center"><div style="background:#fff;border-radius:16px;padding:12px;width:220px;height:220px;flex:none"><img src="img/qr.png" style="width:100%;height:100%;display:block"></div><div><div class="disp" style="font-size:1.4em">${lang === 'ar' ? 'امسح واطلب' : 'Scan to order'}</div><div style="margin-top:.3em;opacity:.85">${B.web}</div><div style="margin-top:.5em;opacity:.85">Instagram ${B.instagram}</div><div style="margin-top:.2em;opacity:.85"><bdi dir="ltr">${B.mapsShort}</bdi></div></div></div><div class="foot">${footer(lang)}</div></div></body></html>`;
}

fs.mkdirSync(OUT, { recursive: true });
const W = (n, h) => fs.writeFileSync(path.join(OUT, n), h);
W('print_en.html', printedMenu('en')); W('print_ar.html', printedMenu('ar'));
W('tv_bi.html', tvBoard('en', true)); W('tv_en.html', tvBoard('en', false)); W('tv_ar.html', tvBoard('ar', false));
W('phone_bi.html', phoneMenu('en', true)); W('phone_ar.html', phoneMenu('ar', false));

/* ---------- A6 BAG CARD (front: QR + order; back: favourites + rewards) ---------- */
function bagCard(lang) {
  const dir = lang === 'ar' ? 'rtl' : 'ltr'; const B = M.brand; const R = M.rewards;
  const css = BASE_CSS + `
  @page{size:105mm 148mm;margin:0} html,body{width:105mm}
  .card{width:105mm;height:148mm;padding:7mm;page-break-after:always;display:flex;flex-direction:column;gap:3mm;font-size:8.5pt;position:relative;overflow:hidden}
  .card:last-child{page-break-after:auto}
  .front{background:${CH};color:${CREAM}}
  .qrbox{background:#fff;border-radius:4mm;padding:4mm;width:62mm;height:62mm;margin:2mm auto}
  .big{font-size:20pt;line-height:1.05}
  .fav{display:flex;justify-content:space-between;gap:2mm;padding:1.4mm 0;border-bottom:1px solid rgba(46,46,48,.12);font-size:8.5pt}
  .fav b{color:#3f7d1c}
  `;
  const favs = [...M.signatures.slice(0, 4).map(s => [lang === 'ar' ? s.ar : s.en, price(s.price)]),
    ...['Kafta', 'Shish taouk', 'Basterma'].map(n => { const it = M.sections.flatMap(x => x.items).find(i => i.en === n); return [lang === 'ar' ? it.ar : it.en, price(it.price)]; }),
    [lang === 'ar' ? M.kilo.ar : M.kilo.en, lang === 'ar' ? 'من $19' : 'from $19']];
  const front = `<div class="card front" dir="${dir}">${brandMark(lang, true)}<div class="${lang === 'ar' ? '' : 'ar'}" style="font-size:8pt;opacity:.85">${B.arLine}</div>
    <div class="disp big" style="margin-top:3mm">${lang === 'ar' ? 'امسح واطلب' : 'Scan to order'}</div>
    <div style="font-size:8.5pt;opacity:.85;line-height:1.35">${lang === 'ar' ? 'المنيو كامل، اطلب أونلاين، حطّ دبّوس بيتك ع الخريطة — ومنوصّل لكل المنطقة.' : 'Full menu, order online, pin your door on the map — we deliver across the area.'}</div>
    <div class="qrbox"><img src="img/qr.png" style="width:100%;height:100%;display:block" alt="QR"></div>
    <div style="text-align:center;font-size:8pt;opacity:.8">${B.web}</div>
    <div style="margin-top:auto;display:flex;justify-content:space-between;align-items:flex-end;gap:2mm"><div><div class="disp" style="font-size:13pt">WhatsApp · <bdi dir="ltr">${B.phone}</bdi></div><div style="font-size:7.5pt;opacity:.8">${t(B, 'hours', lang)} · ${t(B, 'address', lang)}</div></div><div style="font-size:7.5pt;opacity:.8;text-align:end">Instagram<br>${B.instagram}</div></div></div>`;
  const back = `<div class="card" dir="${dir}">${brandMark(lang)}<div class="disp" style="font-size:13pt;margin-top:1mm">${lang === 'ar' ? 'المفضّلة' : 'Favourites'}</div>
    <div>${favs.map(([n, p]) => `<div class="fav"><span>${n}</span><b>${p}</b></div>`).join('')}</div>
    <div class="band" style="padding:2.5mm 3mm;margin-top:1mm"><div class="disp" style="font-size:10pt">${t(R, 'title', lang)}</div><div style="font-size:7.8pt;line-height:1.35">${t(R, 'text', lang)}</div></div>
    <div style="margin-top:auto;display:flex;gap:3mm;align-items:center"><div style="background:#fff;border:1px solid rgba(46,46,48,.12);border-radius:3mm;padding:1.5mm;width:20mm;height:20mm"><img src="img/qr_maps.png" style="width:100%;height:100%;display:block"></div><div style="font-size:7.8pt;line-height:1.35"><b>${lang === 'ar' ? 'موقعنا على Google Maps' : 'Find us on Google Maps'}</b><br>${t(B, 'address', lang)}<br>${t(B, 'delivery', lang)}</div></div></div>`;
  return `<!doctype html><html lang="${lang}" dir="${dir}"><head><meta charset="utf-8">${FONTS}<style>${css}</style></head><body>${front}${back}</body></html>`;
}
W('card_en.html', bagCard('en')); W('card_ar.html', bagCard('ar'));

// img symlink for out/
try { fs.symlinkSync(path.join(__dirname, 'img'), path.join(OUT, 'img')); } catch (e) {}
console.log('built');
