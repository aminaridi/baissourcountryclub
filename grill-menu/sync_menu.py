#!/usr/bin/env python3
"""BCC Grill — ONE menu, everywhere.

Edit grill-menu/menu.json, then run:  python3 grill-menu/sync_menu.py
It regenerates:
  • the MENU block inside docs/grill/index.html   (website ordering page)
  • the MENU block inside grill-menu/app-orders.html (ordering app — publish that file to the
    claude.ai artifact https://claude.ai/artifact/XTxWubQaqW8fzNhVNYxP2o afterwards)
  • the printed PDFs, TV boards and phone menu (node build.js + render.js) → docs/grill/menu/
Never edit a menu item in any of those files by hand.
"""
import json, re, subprocess, shutil, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent
M = json.loads((ROOT / 'menu.json').read_text(encoding='utf-8'))
js = lambda v: json.dumps(v, ensure_ascii=False)
clean = lambda t: re.sub(r'<[^>]+>', '', t or '').replace(' Large +$3.', '').replace(' كبير +٣$.', '').strip()
sec = lambda i: next(x for x in M['sections'] if x['id'] == i)
slug = lambda en: re.sub(r'[^a-z0-9]+', '', en.lower())[:14]
IDS = {'Kafta': 'kafta', 'Lamb kabab': 'lamb', 'Lahmeh sha2af': 'lahme', 'Shish taouk': 'taouk', 'Djej meshwi': 'djej',
       'Kabab orfali': 'orfali', 'Arayes': 'arayes', 'Vegetarian skewer': 'vegskewer'}
KIDS_W = "[C('side','Side','طبق جانبي',[['Small fries',0],['Cucumber & carrot sticks',0],['Small rice',0]]),C('drink','Drink','مشروب',[['Apple juice',0],['Orange juice',0],['Water',0]]),C('mods','Changes','تعديلات',[['Add cheese',0],['Add ketchup',0],['Cut in half',0]],{multi:true,optional:true})]"
KIDS_A = "[C('side', 'Side', [['Small fries', 0], ['Cucumber & carrot sticks', 0], ['Small rice', 0]]), C('drink', 'Drink', [['Apple juice', 0], ['Orange juice', 0], ['Water', 0]]), C('mods', 'Changes', [['Add cheese', 0], ['Add ketchup', 0], ['Cut in half', 0]], { multi: true, optional: true })]"
FAMILY_W = "[C('mix','Skewers','السياخ',[['4 kafta + 4 taouk',0],['All kafta',0],['All taouk',0],['Mixed with lamb',4]]),C('side','Two large sides (pick two)','طبقين جانبيين (اختار تنين)',SIDES,{multi:true,max:2,min:2}),C('salad','Two salads (pick two)','سلطتين (اختار تنين)',SALADS,{multi:true,max:2,min:2}),C('drink','Four drinks (pick up to four)','٤ مشروبات (لحد أربعة)',DRINKS,{multi:true,max:4}),C('sauce','Sauces (pick up to three)','الصوص (لحد تلاتة)',SAUCES,{multi:true,max:3})]"
FAMILY_A = "[C('mix', 'Skewers', [['4 kafta + 4 taouk', 0], ['All kafta', 0], ['All taouk', 0], ['Mixed with lamb', 4]]), C('side', 'Two large sides (pick two)', SIDES, { multi: true, max: 2, min: 2 }), C('salad', 'Two salads (pick two)', SALADS, { multi: true, max: 2, min: 2 }), C('drink', 'Four drinks (pick up to four)', DRINKS, { multi: true, max: 4 }), C('sauce', 'Sauces (pick up to three)', SAUCES, { multi: true, max: 3 })]"


def price_of(it):
    pr = it['price']
    return float(pr.split('·')[0]) if isinstance(pr, str) else pr


# ---------------- website (bilingual data) ----------------
def w_item(id_, it, choices=None, tag=None, web_img=True):
    d, da = clean(it.get('descEn') or it.get('subEn', '')), clean(it.get('descAr') or it.get('subAr', ''))
    out = f"  {{id:{js(id_)},name:{js(it['en'])},ar:{js(it['ar'])},price:{price_of(it)}"
    if tag: out += f",tag:{js(tag)}"
    elif it.get('new'): out += ",tag:'new'"
    if d: out += f",desc:{js(d)},descAr:{js(da)}"
    if web_img and it.get('webPhoto'): out += f",img:{js(it['webPhoto'])}"
    if choices: out += f",choices:{choices}"
    return out + "},"


def website_menu(kilo_block):
    L = ["const MENU=[", " {id:'sig',name:'Signatures',ar:'المميّزين',items:["]
    for it in M['signatures']:
        if it['id'] == 'bcc': L.append(w_item('bccburger', it, "[MEALQ,VEG,BURGER_MODS,...MEAL_PICKS]", 'sig'))
        elif it['id'] == 'leb': L.append(w_item('lebburger', it, "[MEALQ,LEB_SIDE,C('mods','Changes','تعديلات',[['No pickles',0],['Extra ketchup',0],['Add fried egg',1]],{multi:true,optional:true}),...MEAL_PICKS]", 'new'))
        elif it['id'] == 'smash': L.append(w_item('smash', it, "SANDWICH", 'sig'))
        elif it['id'] == 'kfries': L.append(w_item('kfries', it, "[C('size','Size','الحجم',[['Regular',0],['Large (share)',3]]),C('protein','Meat','اللحمة',[['Kafta',0],['Shish taouk',0],['Mixed',.5]]),C('mods','Changes','تعديلات',[['No cheese sauce',0],['No sumac onion',0],['Extra toum',.5],['Extra spicy',0]],{multi:true,optional:true})]", 'sig'))
    L.append(" ]},")
    for sid in ('charcoal', 'snack'):
        c = sec(sid); L.append(f" {{id:{js(sid)},name:{js(c['en'])},ar:{js(c['ar'])},sub:{js(c.get('noteEn',''))},subAr:{js(c.get('noteAr',''))},items:[")
        for it in c['items']: L.append(w_item(IDS.get(it['en'], slug(it['en'])), it, "SANDWICH"))
        L.append(" ]},")
    c = sec('burgers'); L.append(f" {{id:'burgers',name:'Burgers',ar:'برغر',sub:{js(c['noteEn'])},subAr:{js(c['noteAr'])},items:[")
    for it in c['items']:
        if it['en'] == 'BCC Burger meal': L.append(w_item('bmeal', it, "[...MEAL,VEG,BURGER_MODS]"))
        else: L.append(w_item({'Kafta burger': 'kburger', 'Grilled chicken burger': 'gchicken', 'Veggie burger': 'veggie'}.get(it['en'], slug(it['en'])), it, "[MEALQ,VEG,BURGER_MODS,...MEAL_PICKS]"))
    L.append(" ]},")
    c = sec('kids'); L.append(f" {{id:'kids',name:'Kids',ar:'الأولاد',sub:{js(c['noteEn'])},subAr:{js(c['noteAr'])},items:[")
    for it in c['items']: L.append(w_item(slug(it['en']), it, KIDS_W))
    L.append(" ]},")
    c = sec('plates'); L.append(f" {{id:'plates',name:'Plates & boxes',ar:'صحون وبوكسات',sub:{js(c['noteEn'])},subAr:{js(c['noteAr'])},items:[")
    for it in c['items']:
        if it['en'] == 'Kabab plate': L.append(w_item('kplate', it, "[C('protein','Skewers','السياخ',[...PROT(2,.5),['Half and half',0]]),...PLATE]"))
        elif it['en'] == 'BCC mixed grill': L.append(w_item('mixed', it, "PLATE"))
        elif it['en'].startswith('Farrouj meshwi'): L.append(w_item('farrouj', it, "[C('size','Size','الحجم',[['Whole',0],['Half',-6]]),C('sauce','Sauces (pick up to two)','الصوص (لحد تنين)',SAUCES,{multi:true,max:2}),C('mods','Changes','تعديلات',[['Extra crispy',0],['Extra spicy',0],['No pickles',0],['Salad instead of fries',0]],{multi:true,optional:true})]"))
        elif it['en'] == 'Farrouj msa7ab': L.append(w_item('msahab', it, "[C('sauce','Sauces (pick up to two)','الصوص (لحد تنين)',SAUCES,{multi:true,max:2}),C('salad','Salad','سلطة',SALADS),C('mods','Changes','تعديلات',[['Extra crispy',0],['Extra spicy',0],['No pickles',0],['Salad instead of fries',0]],{multi:true,optional:true})]"))
        elif it['en'] == 'Mashawi Family Box': L.append(w_item('family', it, FAMILY_W, 'fam'))
    L.append(" ]},")
    L.append(kilo_block.rstrip('\n'))
    c = sec('lean'); L.append(f" {{id:'lean',name:'Light & Lean',ar:'خفيف وصحي',sub:{js(c['noteEn'])},subAr:{js(c['noteAr'])},items:[")
    for it in c['items']:
        if it['en'] == 'Salad & protein': L.append(w_item('saladpro', it, "[C('salad','Salad','السلطة',SALADS),C('protein','Protein','البروتين',PROT(1.5,.5)),C('double','Double the protein?','دبل البروتين؟',[['Single portion',0],['Double protein',3]],{msg:'Portion'})]", 'lean'))
        else: L.append(w_item('lettuce', it, "[C('filling','Protein or veggies','بروتين أو خضرا',[...PROT(1.5,.5),['Grilled veggies',0]])]", 'lean'))
    L.append(" ]},")
    c = sec('sides'); L.append(" {id:'sides',name:'Sides & sauces',ar:'مقبلات وصوص',items:[")
    for it in c['items']: L.append(w_item(slug(it['en']), it))
    L.append(" ]},")
    c = sec('desserts'); L.append(f" {{id:'dessert',name:{js(c['en'])},ar:{js(c['ar'])},sub:{js(c.get('noteEn',''))},subAr:{js(c.get('noteAr',''))},items:[")
    for it in c['items']: L.append(w_item(slug(it['en']), it))
    L.append(" ]},")
    c = sec('drinks'); L.append(" {id:'drinks',name:'Drinks',ar:'مشروبات',items:[")
    for it in c['items']:
        L.append(w_item('soft', it, "[C('kind','Which','أيا واحد',[['Pepsi',0],['7Up',0],['Mirinda',0],['Diet Pepsi',0]])]") if it['en'] == 'Soft drink' else w_item(slug(it['en']), it))
    L.append(" ]},")
    L.append("];")
    return '\n'.join(L)


# ---------------- app (English labels) ----------------
MEALQ = "C('meal', 'Make it a meal', [['Burger only', 0], ['Meal: side + salad + drink', 3]])"
MP = "C('side', 'Meal side', SIDES, { optional: true, when: 'meal' }), C('salad', 'Meal salad', SALADS, { optional: true, when: 'meal' }), C('drink', 'Meal drink', DRINKS, { optional: true, when: 'meal' })"


def a_item(id_, it, choices=None, tag=None):
    d = clean(it.get('descEn') or it.get('subEn', ''))
    out = f"    {{ id: {js(id_)}, name: {js(it['en'])}, ar: {js(it['ar'])}, price: {price_of(it)}"
    if d: out += f", desc: {js(d)}"
    if tag: out += f", tag: {js(tag)}"
    elif it.get('new'): out += ", tag: 'New'"
    if it.get('webPhoto'): out += f", img: {js(it['webPhoto'])}"
    if choices: out += f", choices: {choices}"
    return out + " },"


def app_menu(kilo_block):
    L = ["const MENU = [", "  { id: 'sig', name: 'Signatures', ar: 'المميّزين', items: ["]
    for it in M['signatures']:
        if it['id'] == 'bcc': L.append(a_item('bccburger', it, f"[{MEALQ}, ...BURGER, {MP}]", 'Signature'))
        elif it['id'] == 'leb': L.append(a_item('lebburger', it, f"[{MEALQ}, C('veg', 'Coleslaw and pickles on the side?', [['Coleslaw and pickles in the bun', 0], ['Coleslaw and pickles on the side', 0]]), C('mods', 'Changes', [['No pickles', 0], ['Extra ketchup', 0], ['Add fried egg', 1]], {{ multi: true, optional: true }}), {MP}]", 'New'))
        elif it['id'] == 'smash': L.append(a_item('smash', it, "SANDWICH", 'Signature'))
        elif it['id'] == 'kfries': L.append(a_item('kfries', it, "[C('size', 'Size', [['Regular', 0], ['Large (share)', 3]]), C('protein', 'Meat', [['Kafta', 0], ['Shish taouk', 0], ['Mixed', 0.5]]), C('mods', 'Changes', [['No cheese sauce', 0], ['No sumac onion', 0], ['Extra toum', 0.5], ['Extra spicy', 0]], { multi: true, optional: true })]", 'Signature'))
    L.append("  ]},")
    for sid in ('charcoal', 'snack'):
        c = sec(sid); L.append(f"  {{ id: {js(sid)}, name: {js(c['en'])}, ar: {js(c['ar'])}, sub: {js(c.get('noteEn',''))}, items: [")
        for it in c['items']: L.append(a_item(IDS.get(it['en'], slug(it['en'])), it, "SANDWICH"))
        L.append("  ]},")
    c = sec('burgers'); L.append(f"  {{ id: 'burgers', name: 'Burgers', ar: 'برغر', sub: {js(c['noteEn'])}, items: [")
    for it in c['items']:
        if it['en'] == 'BCC Burger meal': L.append(a_item('bmeal', it, "[...MEAL, ...BURGER]"))
        else: L.append(a_item({'Kafta burger': 'kburger', 'Grilled chicken burger': 'gchicken', 'Veggie burger': 'veggie'}.get(it['en'], slug(it['en'])), it, f"[{MEALQ}, ...BURGER, {MP}]"))
    L.append("  ]},")
    c = sec('kids'); L.append(f"  {{ id: 'kids', name: 'Kids', ar: 'الأولاد', sub: {js(c['noteEn'])}, items: [")
    for it in c['items']: L.append(a_item(slug(it['en']), it, KIDS_A))
    L.append("  ]},")
    c = sec('plates'); L.append(f"  {{ id: 'plates', name: 'Plates & boxes', ar: 'صحون وبوكسات', sub: {js(c['noteEn'])}, items: [")
    for it in c['items']:
        if it['en'] == 'Kabab plate': L.append(a_item('kplate', it, "[C('protein', 'Skewers', [...PROT(2, 0.5), ['Half and half', 0]]), ...PLATE]"))
        elif it['en'] == 'BCC mixed grill': L.append(a_item('mixed', it, "PLATE"))
        elif it['en'].startswith('Farrouj meshwi'): L.append(a_item('farrouj', it, "[C('size', 'Size', [['Whole', 0], ['Half', -6]]), C('sauce', 'Sauces (pick up to two)', SAUCES, { multi: true, max: 2 }), C('mods', 'Changes', [['Extra crispy', 0], ['Extra spicy', 0], ['No pickles', 0], ['Salad instead of fries', 0]], { multi: true, optional: true })]"))
        elif it['en'] == 'Farrouj msa7ab': L.append(a_item('msahab', it, "[C('sauce', 'Sauces (pick up to two)', SAUCES, { multi: true, max: 2 }), C('salad', 'Salad', SALADS), C('mods', 'Changes', [['Extra crispy', 0], ['Extra spicy', 0], ['No pickles', 0], ['Salad instead of fries', 0]], { multi: true, optional: true })]"))
        elif it['en'] == 'Mashawi Family Box': L.append(a_item('family', it, FAMILY_A, 'Every day'))
    L.append("  ]},")
    L.append(kilo_block.rstrip('\n'))
    c = sec('lean'); L.append(f"  {{ id: 'lean', name: 'Light & Lean', ar: 'خفيف وصحي', sub: {js(c['noteEn'])}, items: [")
    for it in c['items']:
        if it['en'] == 'Salad & protein': L.append(a_item('saladpro', it, "[C('salad', 'Salad', SALADS), C('protein', 'Protein', [...PROT(1.5, 0.5), ['Double protein', 3]])]", 'Lean'))
        else: L.append(a_item('lettuce', it, "[C('filling', 'Protein or veggies', [...PROT(1.5, 0.5), ['Grilled veggies', 0]])]", 'Lean'))
    L.append("  ]},")
    c = sec('sides'); L.append("  { id: 'sides', name: 'Sides & sauces', ar: 'مقبلات وصوص', items: [")
    for it in c['items']: L.append(a_item(slug(it['en']), it))
    L.append("  ]},")
    c = sec('desserts'); L.append(f"  {{ id: 'dessert', name: {js(c['en'])}, ar: {js(c['ar'])}, sub: {js(c.get('noteEn',''))}, items: [")
    for it in c['items']: L.append(a_item(slug(it['en']), it))
    L.append("  ]},")
    c = sec('drinks'); L.append("  { id: 'drinks', name: 'Drinks', ar: 'مشروبات', items: [")
    for it in c['items']:
        L.append(a_item('soft', it, "[C('kind', 'Which', [['Pepsi', 0], ['7Up', 0], ['Mirinda', 0], ['Diet Pepsi', 0]])]") if it['en'] == 'Soft drink' else a_item(slug(it['en']), it))
    L.append("  ]},")
    L.append("];")
    return '\n'.join(L)


def replace_block(path, head, builder, kilo_head):
    s = path.read_text(encoding='utf-8')
    start = s.index(head); end = s.index('\n];', start) + 3
    old = s[start:end]
    ks = old.index(kilo_head)
    # kilo block: from kilo_head to the next top-level section head
    rest = old[ks:]
    m = re.search(r"\n\s*\{\s*id:\s*'(lean|sides)'", rest)
    kilo = rest[:m.start() + 1]
    s = s[:start] + builder(kilo) + s[end:]
    path.write_text(s, encoding='utf-8')
    print('updated', path.relative_to(REPO))


replace_block(REPO / 'docs/grill/index.html', 'const MENU=[', website_menu, " {id:'kilo'")
replace_block(ROOT / 'app-orders.html', 'const MENU = [', app_menu, "  { id: 'kilo'")

# printed / TV / phone
if '--no-render' not in sys.argv:
    subprocess.run(['node', 'build.js'], cwd=ROOT, check=True)
    subprocess.run(['node', 'render.js'], cwd=ROOT, check=True)
    out = ROOT / 'out'; dst = REPO / 'docs/grill/menu'; dst.mkdir(parents=True, exist_ok=True)
    for a, b in [('BCC_Grill_Menu_A4_EN.pdf', 'BCC-Grill-Menu-EN.pdf'), ('BCC_Grill_Menu_A4_AR.pdf', 'BCC-Grill-Menu-AR.pdf'),
                 ('tv_bi.png', 'BCC-Grill-TV-Board.png'), ('tv_en.png', 'BCC-Grill-TV-Board-EN.png'), ('tv_ar.png', 'BCC-Grill-TV-Board-AR.png'),
                 ('phone_bi.png', 'BCC-Grill-Menu-Phone.png'), ('phone_ar.png', 'BCC-Grill-Menu-Phone-AR.png')]:
        shutil.copy(out / a, dst / b)
    print('rendered → docs/grill/menu/')
print('done — commit & push, then publish grill-menu/app-orders.html to the ordering-app artifact')
