# -*- coding: utf-8 -*-
"""BCC Grill — staff manual content. Each block is (en, ar). Steps are lists of (en, ar).
Recipes marked CONFIRM are standard Lebanese snack-shop methods written for the grill lead to confirm or correct
on training day; the confirmed specs (burger line, interview answers) are used as-is."""

TITLE = ("BCC Grill — Team Manual", "BCC Grill — دليل الفريق")
SUB = ("How we cook, pack and serve every item · Version 1 · November 2026",
       "كيف منطبخ ومنوضّب ومنخدّم كل صنف · النسخة ١ · تشرين الثاني ٢٠٢٦")

SECTIONS = []

def sec(title, intro=None, blocks=None):
    SECTIONS.append({"title": title, "intro": intro, "blocks": blocks or []})

def recipe(name, yields, ingredients, steps, pack=None, tips=None, confirm=False, photo=True):
    return {"type": "recipe", "name": name, "yields": yields, "ingredients": ingredients, "steps": steps,
            "pack": pack, "tips": tips, "confirm": confirm, "photo": photo}

def text(title, paras):
    return {"type": "text", "title": title, "paras": paras}

def checklist(title, items):
    return {"type": "check", "title": title, "items": items}

# ---------------------------------------------------------------- 1 · Welcome & standards
sec(("1 · Welcome to BCC Grill", "١ · أهلاً بكم في BCC Grill"),
    ("BCC Grill is the take-away of Baissour Country Club. Same kitchen standards, smaller shop, faster food. Everything here is written so a new team member can make every item the same way, every time. Read it, then cook it with the grill lead before your first shift.",
     "BCC Grill هو التيك أواي تبع منتجع بيصور السياحي. نفس معايير المطبخ، محل أصغر، أكل أسرع. كل شي مكتوب هون ليقدر أي عضو جديد بالفريق يعمل كل صنف بنفس الطريقة كل مرة. اقراه، وبعدين اطبخو مع مسؤول المشاوي قبل أول شيفت."),
    [
      text(("Our four promises", "وعودنا الأربعة"), [
        ("We deliver to the whole area — hot, in the thermal bag, with the customer's pin on the map.", "منوصّل لكل المنطقة — سخن، بالشنطة الحرارية، ومع دبّوس الزبون ع الخريطة."),
        ("We are the go-to for families — a Family Box every day, kids' plates, clean and friendly.", "نحنا خيار العيلة — بوكس العيلة كل يوم، صحون للأولاد، نظافة وابتسامة."),
        ("Honest prices, best ingredients — meat is fresh daily, charcoal is real, bread is fresh.", "أسعار صادقة وأفضل مكوّنات — اللحمة طازة كل يوم، الفحم حقيقي، الخبز طازة."),
        ("No fake promises — we never say 'in 30 minutes'. We tell the customer a realistic time and we keep it.", "ما منوعد وعود فاضية — ما منقول أبداً 'خلال ٣٠ دقيقة'. منعطي الزبون وقت واقعي ومنلتزم فيه."),
      ]),
      text(("Standards that are not optional", "معايير مش اختيارية"), [
        ("Hands washed every 30 minutes and after touching raw meat, money or your phone. Gloves for building sandwiches; change them between raw and cooked.", "غسيل الإيدين كل ٣٠ دقيقة وبعد لمس اللحمة النيّة أو المصاري أو التلفون. كفوف لتركيب السندويشات؛ غيّرها بين النيّ والمطبوخ."),
        ("Burgers and kafta are cooked THROUGH. No pink, ever. Chicken to 75 °C in the thickest part — check with the probe.", "البرغر والكفتة مستويين منيح. ما في زهري أبداً. الدجاج لـ٧٥ درجة بأسمك نقطة — افحص بالميزان الحراري."),
        ("Target: a sandwich order ready in 8–10 minutes, a plate in 12–15, a farrouj that is already on the grill in 15. The kitchen screen turns amber at 10 minutes and red at 15.", "الهدف: طلب سندويش جاهز بـ٨–١٠ دقايق، صحن بـ١٢–١٥، فروج موجود أصلاً ع الفحم بـ١٥. شاشة المطبخ بتصير برتقالية بعد ١٠ دقايق وحمرا بعد ١٥."),
        ("Clean as you go. The counter the customer sees is spotless at all times.", "نضّف وإنت عم تشتغل. الكاونتر يلي بيشوفو الزبون نظيف دايماً."),
        ("One name for everything: 'take away', never 'to go'. Staff names stay off receipts, bags and social media.", "اسم واحد لكل شي: 'تيك أواي'، مش 'تو غو'. أسماء الموظفين ما بتنحط ع الفواتير أو الأكياس أو السوشيال ميديا."),
      ]),
      text(("The team and the stations", "الفريق والمحطات"), [
        ("GRILL — the manqal (charcoal) and the flat saj plate. Skewers, farrouj, burgers, kafta smash.", "المشاوي — المنقل (الفحم) والصاج المسطّح. السياخ، الفروج، البرغر، كفتة سماش."),
        ("LINE / PREP — builds every sandwich and plate, runs the fryer and the pan station (sawda, sujuk, makanek), keeps the hot-hold full.", "الخط / التحضير — بيركّب كل سندويش وصحن، بيشغّل القلاية ومحطة الطنجرة (سودة، سجق، مقانق)، وبيعبّي التسخين."),
        ("COUNTER + PACK — takes orders (counter, phone, WhatsApp, kitchen screen), packs every bag with the checklist, handles payment and rewards.", "الكاونتر + التوضيب — بياخد الطلبات (كاونتر، تلفون، واتساب، شاشة المطبخ)، بيوضّب كل كيس حسب اللائحة، بيعالج الدفع والمكافآت."),
        ("DRIVER — thermal bag, Google Maps pin, calls on arrival, exact change, Whish confirmation.", "السائق — شنطة حرارية، دبّوس Google Maps، بيتّصل عند الوصول، فراطة، تأكيد Whish."),
      ]),
    ])

# ---------------------------------------------------------------- 2 · Opening / closing
sec(("2 · Opening and closing", "٢ · الفتح والإغلاق"), None, [
    checklist(("Opening — prep starts 09:00, doors 11:00", "الفتح — التحضير الساعة ٩:٠٠، الباب ١١:٠٠"), [
        ("Light the charcoal at 10:15 so the bed is grey and even by 11:00. Saj plate on at 10:40, fryer to 180 °C at 10:45.", "ولّع الفحم الساعة ١٠:١٥ ليكون رمادي ومتساوي ع الـ١١:٠٠. الصاج ع الـ١٠:٤٠، القلاية ع ١٨٠ درجة ع الـ١٠:٤٥."),
        ("Skewer the day's kafta, taouk, djej meshwi, shi2af, lamb, orfali and veg. Label trays with time.", "اشكّ كفتة اليوم، الطاووق، الدجاج المشوي، الشقف، اللحمة، الأورفلي والخضرا. علّم الصواني بالوقت."),
        ("Sauces in squeeze bottles, dated: toum, toum mayo, special sauce, yogurt-tahini, harissa, cheese sauce.", "الصوصات بقناني ضغط ومؤرّخة: توم، مايونيز بالتوم، صوص خاص، لبن وطحينة، هريسة، صوص جبنة."),
        ("Cold case: dessert cups made and labelled, coleslaw, salads, drinks stocked and cold.", "الفيترين البارد: كاسات الحلو جاهزة ومعلّمة، كول سلو، سلطات، مشروبات معبّاية وباردة."),
        ("Packaging station full: bags, boxes, wraps, cups + lids, napkins, wet wipes, straws, spoons, bag cards, order stickers.", "محطة التوضيب معبّاية: أكياس، علب، لفافات، كاسات + غطايات، محارم، محارم مبلّلة، شاليمو، ملاعق، بطاقات الكيس، لاصقات الطلب."),
        ("Kitchen tablet on, logged in, sound on. Ready-board TV on. Phone charged, WhatsApp open.", "تابلت المطبخ شغّال ومسجّل دخول والصوت عالي. شاشة الجاهز شغّالة. التلفون مشحون والواتساب مفتوح."),
        ("Float in the drawer, Whish app logged in, card for the day's LBP rate written on the counter sign.", "الفراطة بالجارور، تطبيق Whish مسجّل دخول، سعر الليرة لليوم مكتوب ع لوحة الكاونتر."),
    ]),
    checklist(("Closing — last orders 23:00", "الإغلاق — آخر طلب ١١:٠٠ مساءً"), [
        ("Charcoal doused and covered. Saj scraped, oiled. Fryer oil filtered (changed every 3 days or sooner if dark).", "الفحم مطفّى ومغطّى. الصاج مكشوط ومزيّت. زيت القلاية مفلتر (بيتغيّر كل ٣ أيام أو قبل إذا اسودّ)."),
        ("All raw meat wrapped, dated, in the fridge below cooked items. Nothing raw stays on the line.", "كل اللحمة النيّة ملفوفة ومؤرّخة بالبراد تحت المطبوخ. ما في شي نيّ بيضل ع الخط."),
        ("Count dessert cups and salads; note what to make tomorrow on the prep sheet.", "عدّ كاسات الحلو والسلطات؛ سجّل شو لازم ينعمل بكرا ع ورقة التحضير."),
        ("Floors, counter, handles, tablet screen wiped. Bins out. Lights, gas, fryer off. Drawer counted.", "الأرض، الكاونتر، المقابض، شاشة التابلت ممسوحين. الزبالة برّا. الضو والغاز والقلاية مطفّيين. الجارور معدود."),
    ]),
])

# ---------------------------------------------------------------- 3 · Base preps
sec(("3 · Base preps (made daily)", "٣ · التحضيرات الأساسية (كل يوم)"),
    ("These are the building blocks. Every item on the menu is one of these plus bread, plus the pack.",
     "هول هنّ الأساس. كل صنف ع المنيو هو واحد من هول + خبز + التوضيب."),
    [
      recipe(("Kafta mix", "خلطة الكفتة"), ("5 kg · ≈ 45 sandwich portions", "٥ كغ · ≈ ٤٥ حصة سندويش"),
        [("4 kg beef (20% fat) + 1 kg lamb, minced medium", "٤ كغ لحمة بقر (٢٠٪ دهن) + ١ كغ غنم، مفروم وسط"), ("600 g onion, grated and squeezed dry", "٦٠٠ غ بصل مبشور ومعصور"), ("1 big bunch parsley, fine", "ضمّة بقدونس كبيرة، ناعمة"), ("60 g salt · 15 g seven-spice · 10 g black pepper · 5 g cinnamon", "٦٠ غ ملح · ١٥ غ سبع بهارات · ١٠ غ فلفل أسود · ٥ غ قرفة")],
        [("Mix cold, by hand, just until even — over-mixing makes it rubbery.", "اعجن بارد باليد لحد ما تتجانس بس — العجن الزايد بيخلّيها مطاطية."),
         ("Portion: sandwich skewer 120 g, plate skewer 90 g (3 per plate), kafta smash ball 130 g. Weigh the first ten, then by eye.", "الحصص: سيخ سندويش ١٢٠ غ، سيخ صحن ٩٠ غ (٣ بالصحن)، كرة كفتة سماش ١٣٠ غ. وزّن أول عشرة، وبعدين بالعين."),
         ("Skewer flat and long, press the ends so it grips. Tray, cover, fridge. Use within the day.", "اشكّ مسطّح وطويل، اضغط الأطراف ليمسك. صينية، غطا، براد. استعمل خلال اليوم.")],
        confirm=True),
      recipe(("Shish taouk marinade", "تتبيلة الشيش طاووق"), ("3 kg chicken breast cubes · ≈ 25 skewers", "٣ كغ مكعبات صدر دجاج · ≈ ٢٥ سيخ"),
        [("3 kg breast, 3 cm cubes", "٣ كغ صدر، مكعبات ٣ سم"), ("400 g yogurt · 100 ml lemon · 80 ml oil · 60 g garlic paste", "٤٠٠ غ لبن · ١٠٠ مل حامض · ٨٠ مل زيت · ٦٠ غ معجون توم"), ("40 g salt · 15 g paprika · 10 g white pepper · 5 g ginger · 1 tbsp tomato paste", "٤٠ غ ملح · ١٥ غ بابريكا · ١٠ غ فلفل أبيض · ٥ غ زنجبيل · ملعقة معجون بندورة")],
        [("Marinate minimum 4 hours, best overnight.", "تبّل ٤ ساعات ع الأقل، والأفضل ليلة كاملة."), ("Skewer 120 g per sandwich skewer, 90 g per plate skewer.", "اشكّ ١٢٠ غ لسيخ السندويش، ٩٠ غ لسيخ الصحن."), ("Grill over medium coals 8–10 min, turning; probe 75 °C.", "اشوي ع فحم وسط ٨–١٠ دقايق مع التقليب؛ الحرارة ٧٥ درجة.")], confirm=True),
      recipe(("Djej meshwi marinade (boneless thigh)", "تتبيلة الدجاج المشوي (فخد بلا عضم)"), ("3 kg thigh", "٣ كغ فخد"),
        [("3 kg boneless thigh, skin off, cut in 3 pieces each", "٣ كغ فخد بلا عضم ولا جلد، كل واحد ٣ قطع"), ("150 ml lemon · 100 ml olive oil · 60 g garlic · 20 g dried oregano · 40 g salt · 10 g black pepper · 5 g sumac", "١٥٠ مل حامض · ١٠٠ مل زيت زيتون · ٦٠ غ توم · ٢٠ غ زعتر بري مجفّف · ٤٠ غ ملح · ١٠ غ فلفل أسود · ٥ غ سماق")],
        [("No yogurt — this is what makes it taste different from taouk.", "بلا لبن — هيدا يلي بيخلّي طعمتو مختلفة عن الطاووق."), ("Marinate 4 h+. Grill flat on the hot side of the coals 4–5 min a side until charred edges; probe 75 °C. Slice for sandwiches.", "تبّل ٤ ساعات+. اشوي مسطّح ع الجهة الحامية ٤–٥ دقايق كل وجه لحد ما تتحمّص الأطراف؛ ٧٥ درجة. قطّع للسندويش.")], confirm=True),
      recipe(("Lahmeh shi2af (beef cubes)", "لحمة شقف (مكعبات بقر)"), ("3 kg", "٣ كغ"),
        [("3 kg beef tenderloin/sirloin, 3 cm cubes", "٣ كغ فيليه/ستيك بقر، مكعبات ٣ سم"), ("100 ml oil · 50 ml lemon · 40 g salt · 15 g seven-spice · 10 g black pepper · 1 onion grated", "١٠٠ مل زيت · ٥٠ مل حامض · ٤٠ غ ملح · ١٥ غ سبع بهارات · ١٠ غ فلفل أسود · بصلة مبشورة")],
        [("Marinate 2 h+. Skewer with a piece of onion and tomato between cubes. Hot coals, 6–8 min, pink is OK ONLY for shi2af if the customer asks; default well done.", "تبّل ساعتين+. اشكّ مع قطعة بصل وبندورة بين المكعبات. فحم حامي، ٦–٨ دقايق، الزهري مسموح بس للشقف إذا طلب الزبون؛ الأساس مستوي.")], confirm=True),
      recipe(("Lamb kabab", "كباب لحمة غنم"), ("3 kg", "٣ كغ"),
        [("3 kg lamb shoulder/leg with some fat, 3 cm cubes", "٣ كغ كتف/فخد غنم مع شوي دهن، مكعبات ٣ سم"), ("Same marinade as shi2af + 5 g cinnamon", "نفس تتبيلة الشقف + ٥ غ قرفة")],
        [("Always well done (Amin's rule). 8–10 min over hot coals.", "دايماً مستوي منيح (قاعدة أمين). ٨–١٠ دقايق ع فحم حامي.")]),
      recipe(("Kabab orfali", "كباب أورفلي"), ("2 kg", "٢ كغ"),
        [("2 kg kafta mix (above) + 80 g toasted pine nuts + 10 g extra seven-spice + 5 g allspice + 1 tsp chilli flakes", "٢ كغ خلطة كفتة (فوق) + ٨٠ غ صنوبر محمّص + ١٠ غ سبع بهارات زيادة + ٥ غ بهار حلو + ملعقة صغيرة رقائق فليفلة")],
        [("Fold the nuts in last so they stay whole. Skewer 120 g. Grill as kafta.", "ضيف الصنوبر بالآخر ليضل صحيح. اشكّ ١٢٠ غ. اشوي متل الكفتة.")], confirm=True),
      recipe(("Vegetarian skewer", "سيخ خضرا"), ("per skewer", "للسيخ"),
        [("2 eggplant cubes, 2 onion petals, 2 cherry tomatoes, 2 pieces bell pepper, 1 red pepper, 2 mushrooms", "٢ مكعب باذنجان، ٢ ورقة بصل، ٢ بندورة كرزية، ٢ قطعة فليفلة، ١ فليفلة حمرا، ٢ فطر"), ("Brush: olive oil, salt, sumac, dried mint", "ادهن: زيت زيتون، ملح، سماق، نعنع يابس")],
        [("Grill 8 min turning until soft and charred. Vegan: serve with hummus or tahini, no yogurt.", "اشوي ٨ دقايق مع التقليب لحد ما تطرى وتتحمّص. نباتي: قدّم مع حمص أو طحينة، بلا لبن.")]),
      recipe(("Toum (garlic sauce)", "التوم"), ("2 kg", "٢ كغ"),
        [("300 g peeled garlic · 1.5 L neutral oil · 120 ml lemon · 15 g salt · 60 ml ice water", "٣٠٠ غ توم مقشّر · ١.٥ ل زيت نباتي · ١٢٠ مل حامض · ١٥ غ ملح · ٦٠ مل مي بارد")],
        [("Blend garlic + salt to a paste. Add oil in a thin stream alternating with lemon and water until thick and white.", "اطحن التوم + الملح لمعجون. ضيف الزيت خيط رفيع بالتناوب مع الحامض والمي لحد ما يصير تخين وأبيض."), ("Keeps 5 days in the fridge. Portion 30 g per sandwich, 60 g per plate; toum tub to sell = 250 ml.", "بيضل ٥ أيام بالبراد. الحصة ٣٠ غ للسندويش، ٦٠ غ للصحن؛ علبة التوم للبيع = ٢٥٠ مل.")]),
      recipe(("Toum mayo · Special sauce · Yogurt-tahini · Cheese sauce", "مايونيز بالتوم · الصوص الخاص · لبن وطحينة · صوص الجبنة"), ("each 1 L", "كل واحد ١ ل"),
        [("TOUM MAYO: 700 g mayo + 300 g toum.", "مايونيز بالتوم: ٧٠٠ غ مايونيز + ٣٠٠ غ توم."), ("SPECIAL SAUCE (djej meshwi): 600 g mayo + 200 g ketchup + 100 g pickle relish + 50 g mustard + 1 tbsp smoked paprika + 1 tbsp lemon.", "الصوص الخاص (الدجاج المشوي): ٦٠٠ غ مايونيز + ٢٠٠ غ كاتشب + ١٠٠ غ كبيس مفروم + ٥٠ غ خردل + ملعقة بابريكا مدخّنة + ملعقة حامض."), ("YOGURT-TAHINI: 600 g yogurt + 200 g tahini + 100 ml lemon + garlic + salt + dried mint.", "لبن وطحينة: ٦٠٠ غ لبن + ٢٠٠ غ طحينة + ١٠٠ مل حامض + توم + ملح + نعنع يابس."), ("CHEESE SAUCE: 500 ml milk + 400 g cheddar + 50 g butter + 30 g flour; keep warm on the hot-hold.", "صوص جبنة: ٥٠٠ مل حليب + ٤٠٠ غ شيدر + ٥٠ غ زبدة + ٣٠ غ طحين؛ خلّيه سخن ع التسخين.")],
        [("All in labelled squeeze bottles. Date on the bottle. 3 days max (cheese sauce: same day).", "كلها بقناني ضغط معلّمة. التاريخ ع القنينة. ٣ أيام حد أقصى (صوص الجبنة: نفس اليوم).")], confirm=True),
      recipe(("Hummus", "حمص"), ("≈ 3 kg", "≈ ٣ كغ"),
        [("1 kg dry chickpeas (≈ 2 kg cooked) · 700 g tahini · 150 ml lemon · 30 g salt · 20 g garlic · ice water", "١ كغ حمص حب ناشف (≈ ٢ كغ مطبوخ) · ٧٠٠ غ طحينة · ١٥٠ مل حامض · ٣٠ غ ملح · ٢٠ غ توم · مي بارد")],
        [("Soak overnight with a pinch of baking soda, boil until very soft, blend hot with tahini, lemon, salt, garlic; add ice water to a smooth cream.", "انقع ليلة مع رشّة كربونات، اسلق لحد ما يطرى كتير، اطحن سخن مع الطحينة والحامض والملح والتوم؛ ضيف مي بارد لحد ما يصير كريمي ناعم."), ("Side portion 200 g with olive oil. Plate portion 80 g.", "حصة الطبق الجانبي ٢٠٠ غ مع زيت زيتون. حصة الصحن ٨٠ غ.")]),
      recipe(("Salads: fattoush · tabbouleh · coleslaw · biwaz", "السلطات: فتوش · تبولة · كول سلو · بيواز"), ("daily", "يومي"),
        [("FATTOUSH: romaine, cucumber, tomato, radish, mint, purslane, toasted bread; dressing lemon, olive oil, sumac, pomegranate molasses. Dress at order time.", "فتوش: خس، خيار، بندورة، فجل، نعنع، بقلة، خبز محمّص؛ الصلصة حامض، زيت زيتون، سماق، دبس رمان. تتبّل وقت الطلب."), ("TABBOULEH: 4 bunches parsley fine, 1 bunch mint, 4 tomatoes small dice, 1 onion, 150 g fine bulgur soaked, lemon, olive oil, salt. Make twice a day.", "تبولة: ٤ ضمّات بقدونس ناعم، ضمّة نعنع، ٤ بندورات مكعبات صغيرة، بصلة، ١٥٠ غ برغل ناعم منقوع، حامض، زيت زيتون، ملح. بتنعمل مرتين باليوم."), ("COLESLAW: 2 kg cabbage + 400 g carrot shredded, 500 g mayo, 50 ml vinegar, 30 g sugar, salt. Rest 1 h.", "كول سلو: ٢ كغ ملفوف + ٤٠٠ غ جزر مبشور، ٥٠٠ غ مايونيز، ٥٠ مل خل، ٣٠ غ سكر، ملح. ارتاح ساعة."), ("BIWAZ: sliced onion rinsed, parsley, sumac, a little salt. Make fresh every 2 hours.", "بيواز: بصل شرائح مغسول، بقدونس، سماق، شوي ملح. اعملها طازة كل ساعتين.")],
        [("Salad side = 150 g in the PET cup with lid. Salad on a plate = 100 g.", "حصة السلطة الجانبية = ١٥٠ غ بكاسة PET مع غطا. السلطة بالصحن = ١٠٠ غ.")]),
      recipe(("Fries · batata harra · rice", "بطاطا · بطاطا حرّة · رز"), ("", ""),
        [("FRIES: frozen 9–10 mm, fryer at 180 °C, 3–3.5 min, shake, salt immediately. Never hold more than 5 minutes. Side = 180 g.", "بطاطا: مجلّدة ٩–١٠ مم، القلاية ١٨٠ درجة، ٣–٣.٥ دقايق، هزّ، ملح فوراً. ما تخلّيها أكتر من ٥ دقايق. الحصة = ١٨٠ غ."), ("BATATA HARRA: fried potato cubes tossed on the saj with garlic, coriander, chilli, lemon.", "بطاطا حرّة: مكعبات بطاطا مقلية ع الصاج مع توم وكزبرة وفليفلة وحامض."), ("RICE: vermicelli rice, 1 kg rice : 1.6 L water, toasted vermicelli, butter, salt. Hot-hold max 4 h.", "رز: رز بالشعيرية، ١ كغ رز : ١.٦ ل مي، شعيرية محمّصة، زبدة، ملح. التسخين ٤ ساعات حد أقصى.")],
        [], photo=False),
    ])

# ---------------------------------------------------------------- 4 · The menu, item by item
PACK_SANDWICH = [("Wrap in the printed sandwich paper, fold ends, order sticker on the fold.", "لفّ بورق السندويش المطبوع، اطوي الأطراف، لاصقة الطلب ع الطيّة."),
                 ("Bag: sandwich + 2 napkins + wet wipe + pickles if asked + bag card.", "الكيس: السندويش + ٢ محرمة + محرمة مبلّلة + كبيس إذا طلب + بطاقة الكيس.")]
PACK_BURGER = [("Burger box. If 'veggies on the side': veg in the 250 ml PET cup with lid, inside the box.", "علبة البرغر. إذا 'الخضرا ع جنب': الخضرا بكاسة PET ٢٥٠ مل مع غطا جوّا العلبة."),
               ("Bag: box + 2 napkins + wet wipe + bag card. Fries box separate, on top.", "الكيس: العلبة + ٢ محرمة + محرمة مبلّلة + بطاقة الكيس. علبة البطاطا لحالها، فوق.")]
PACK_PLATE = [("Plate box: meat on bread, side and salad in their own cups, hummus 80 g cup, pickles + toum cup. Bread wrapped separately on top.", "علبة الصحن: اللحمة ع الخبز، الجانبي والسلطة بكاساتهن، كاسة حمص ٨٠ غ، كاسة كبيس + توم. الخبز ملفوف لحالو فوق."),
              ("Bag: 2 napkins per person, wet wipes, fork + spoon per person, bag card.", "الكيس: ٢ محرمة لكل شخص، محارم مبلّلة، شوكة + ملعقة لكل شخص، بطاقة الكيس.")]

sec(("4 · Signatures", "٤ · المميّزين"), None, [
    recipe(("The BCC Burger — $6", "برغر BCC — $6"), ("1 burger", "برغر واحد"),
        [("150 g beef patty ball (80/20)", "كرة لحمة بقر ١٥٠ غ (٨٠/٢٠)"), ("1 slice cheddar", "شرحة شيدر"), ("Toum mayo 20 g · 2 thin pickle slices · 3 thin onion slivers · 1 tomato slice · 1 lettuce leaf", "مايونيز بالتوم ٢٠ غ · ٢ شرحة كبيس رفيعة · ٣ شرائح بصل رفيعة · شرحة بندورة · ورقة خس"), ("Sesame brioche bun, butter", "خبز بريوش بالسمسم، زبدة")],
        [("Toast the bun cut-side down on the saj with butter until golden.", "حمّص الخبز من الجهة المقطوعة ع الصاج مع زبدة لحد ما يذهّب."),
         ("Ball on the hot saj plate, press HARD with the smasher for 10 seconds — thin, wide, lacy edges. Salt + pepper.", "الكرة ع الصاج الحامي، اضغط بقوة بالمسطّح ١٠ ثواني — رفيعة، عريضة، أطراف مقرمشة. ملح + فلفل."),
         ("2–3 min until the top is grey, scrape and flip, cheddar on, 1–2 min. COOKED THROUGH — no pink.", "٢–٣ دقايق لحد ما يصير الوجه رمادي، اكشط واقلب، الشيدر فوق، ١–٢ دقيقة. مستوي منيح — ما في زهري."),
         ("Build bottom-up: bun · patty + cheese · lettuce · tomato · onion · 2 pickles · toum mayo on the top bun. Lid. Press 2 seconds.", "ركّب من تحت لفوق: خبز · القرص + الجبنة · خس · بندورة · بصل · ٢ كبيس · مايونيز بالتوم ع الخبز الفوقاني. غطّي. اضغط ثانيتين."),
         ("Ask every time: 'veggies on the burger or on the side?' Extra patty +$2.50, cheese +$0.50.", "اسأل كل مرة: 'الخضرا ع البرغر أو ع جنب؟' قرص زيادة +$2.50، جبنة +$0.50.")],
        pack=PACK_BURGER, tips=[("Flat saj plate ONLY. Never on the charcoal grate.", "الصاج المسطّح بس. أبداً مش ع شبك الفحم.")]),
    recipe(("Lebanese Burger — $7", "برغر لبناني — $7"), ("1 burger", "برغر واحد"),
        [("150 g patty from the LEBANESE mix: beef 80/20 medium grind, ketchup 1 tbsp per 600 g, seven-spice, onion + garlic powder, salt, pepper. Mixed 30 seconds only. Shaped wider than the bun, 1.5 cm, chilled 20 min.", "قرص ١٥٠ غ من الخلطة اللبنانية: بقر ٨٠/٢٠ فرم وسط، كاتشب ملعقة لكل ٦٠٠ غ، سبع بهارات، بودرة بصل + توم، ملح، فلفل. عجن ٣٠ ثانية بس. أعرض من الخبز، ١.٥ سم، براد ٢٠ دقيقة."), ("Ketchup · creamy coleslaw 55 g · spicy pickle slices · hot fries 50 g", "كاتشب · كول سلو كريمي ٥٥ غ · كبيس حار شرائح · بطاطا سخنة ٥٠ غ"), ("Sesame brioche", "بريوش بالسمسم")],
        [("Fry flat on the saj 3–4 min undisturbed, flip once, 2–3 min. Cooked through.", "اقلي مسطّح ع الصاج ٣–٤ دقايق بلا ما تلمسو، اقلب مرة، ٢–٣ دقايق. مستوي."),
         ("Toast the bun in the beef fat on the plate.", "حمّص الخبز بدهن اللحمة ع الصاج."),
         ("Build: base · patty · squeeze of ketchup · coleslaw · pickles · a handful of HOT fries · lid. Serve immediately.", "ركّب: القاعدة · القرص · كاتشب · كول سلو · كبيس · حفنة بطاطا سخنة · الغطا. قدّم فوراً."),
         ("Ask: 'coleslaw and pickles on the side?' The fries ALWAYS stay inside the bun.", "اسأل: 'الكول سلو والكبيس ع جنب؟' البطاطا دايماً بتضل جوّا الخبز.")],
        pack=PACK_BURGER),
    recipe(("BCC Kafta Smash — $6", "كفتة سماش — $6"), ("1 sandwich", "سندويش واحد"),
        [("130 g kafta ball", "كرة كفتة ١٣٠ غ"), ("Toum 30 g · pickled turnip · tomato slices · grilled onion", "توم ٣٠ غ · لفت مكبوس · شرائح بندورة · بصل مشوي"), ("Lebanese bread", "خبز عربي")],
        [("Smash the kafta thin on the saj, 2 min a side, cooked through.", "ارقّ الكفتة ع الصاج، دقيقتين كل وجه، مستوية."), ("Toum on the bread, kafta, turnip, tomato, onion that was grilled beside it. Roll tight, press on the saj 20 seconds to seal.", "توم ع الخبز، الكفتة، اللفت، البندورة، البصل يلي انشوى جنبها. لفّ محكم، اضغط ع الصاج ٢٠ ثانية ليسكّر.")], pack=PACK_SANDWICH),
    recipe(("Kafta Fries — $5 (large +$3)", "بطاطا كفتة — $5 (كبير +$3)"), ("1 regular", "واحد عادي"),
        [("Fries 180 g (large 300 g)", "بطاطا ١٨٠ غ (كبير ٣٠٠ غ)"), ("1 kafta skewer (or taouk) grilled, chopped", "سيخ كفتة (أو طاووق) مشوي، مقطّع"), ("Cheese sauce 50 g · toum 20 g · sumac onion · parsley", "صوص جبنة ٥٠ غ · توم ٢٠ غ · بصل بسماق · بقدونس")],
        [("Fries into the kraft bowl, chopped charcoal grilled kafta on top, cheese sauce, toum drizzle, sumac onion, parsley. Lid on last second.", "البطاطا بالوعاء الكرافت، الكفتة المشوية ع الفحم مقطّعة فوق، صوص الجبنة، رشّة توم، بصل بسماق، بقدونس. الغطا بآخر لحظة."), ("Fork in the bag. Napkins ×2, wet wipe.", "شوكة بالكيس. محارم ×٢، محرمة مبلّلة.")]),
])

sec(("5 · Charcoal grilled sandwiches", "٥ · سندويشات مشوية على الفحم"),
    ("All charcoal sandwiches: grill the skewer, open the bread, sauce first, meat, toppings, roll tight, 20 seconds on the saj to seal, wrap. Ask: bread · 2 sauces · any changes.",
     "كل سندويشات الفحم: اشوي السيخ، افتح الخبز، الصوص أول، اللحمة، الإضافات، لفّ محكم، ٢٠ ثانية ع الصاج ليسكّر، لفّ بالورق. اسأل: الخبز · صوصين · أي تعديل."),
    [
      recipe(("Kafta — $5", "كفتة — $5"), ("", ""), [("1 kafta skewer 120 g · toum · biwaz · pickles · grilled tomato", "سيخ كفتة ١٢٠ غ · توم · بيواز · كبيس · بندورة مشوية")], [("Grill 6–8 min turning. Toum on bread, kafta off the skewer, biwaz, pickles, tomato. Roll.", "اشوي ٦–٨ دقايق مع التقليب. توم ع الخبز، الكفتة عن السيخ، بيواز، كبيس، بندورة. لفّ.")], pack=PACK_SANDWICH),
      recipe(("Lamb kabab — $5.50", "كباب لحمة — $5.50"), ("", ""), [("1 lamb skewer 120 g · hummus 40 g · grilled tomato · onion · parsley", "سيخ غنم ١٢٠ غ · حمص ٤٠ غ · بندورة مشوية · بصل · بقدونس")], [("Well done, 8–10 min. Hummus on the bread, lamb, tomato, onion, parsley.", "مستوي منيح، ٨–١٠ دقايق. حمص ع الخبز، اللحمة، بندورة، بصل، بقدونس.")], pack=PACK_SANDWICH),
      recipe(("Lahmeh shi2af — $5.50", "لحمة شقف — $5.50"), ("", ""), [("1 beef skewer 120 g · hummus · grilled tomato & onion · parsley · pickles", "سيخ بقر ١٢٠ غ · حمص · بندورة وبصل مشويين · بقدونس · كبيس")], [("6–8 min. Hummus, beef, grilled veg, parsley, pickles.", "٦–٨ دقايق. حمص، اللحمة، الخضرا المشوية، بقدونس، كبيس.")], pack=PACK_SANDWICH),
      recipe(("Shish taouk — $5", "شيش طاووق — $5"), ("", ""), [("1 taouk skewer 120 g · toum 30 g · pickles · fries 60 g", "سيخ طاووق ١٢٠ غ · توم ٣٠ غ · كبيس · بطاطا ٦٠ غ")], [("Grill to 75 °C. Toum generously on the bread, taouk, pickles, a line of hot fries. Roll and seal.", "اشوي لـ٧٥ درجة. توم بكرم ع الخبز، الطاووق، الكبيس، خط بطاطا سخنة. لفّ وسكّر.")], pack=PACK_SANDWICH),
      recipe(("Djej meshwi — $5", "دجاج مشوي — $5"), ("", ""), [("Grilled thigh 120 g sliced · fries 60 g · toum 20 g · special sauce 20 g · lettuce · pickles", "فخد مشوي ١٢٠ غ شرائح · بطاطا ٦٠ غ · توم ٢٠ غ · صوص خاص ٢٠ غ · خس · كبيس")], [("Toum AND special sauce on the bread, chicken, fries, lettuce, pickles. Roll and seal.", "توم والصوص الخاص ع الخبز، الدجاج، البطاطا، الخس، الكبيس. لفّ وسكّر.")], pack=PACK_SANDWICH),
      recipe(("Kabab orfali — $5", "كباب أورفلي — $5"), ("", ""), [("1 orfali skewer 120 g · biwaz · tomato · hummus or toum", "سيخ أورفلي ١٢٠ غ · بيواز · بندورة · حمص أو توم")], [("Grill as kafta. Build like the kafta sandwich.", "اشوي متل الكفتة. ركّب متل سندويش الكفتة.")], pack=PACK_SANDWICH),
      recipe(("Arayes — $5", "عرايس — $5"), ("", ""), [("1 Lebanese bread · 120 g kafta · 40 g shredded cheese", "خبز عربي · ١٢٠ غ كفتة · ٤٠ غ جبنة مبشورة")], [("Open the bread, spread kafta thin to the edges, cheese, close. Brush with oil. Grill over medium coals 3–4 min a side until crisp and the kafta is cooked through. Cut in 4.", "افتح الخبز، افرد الكفتة رفيعة للأطراف، جبنة، سكّر. ادهن زيت. اشوي ع فحم وسط ٣–٤ دقايق كل وجه لحد ما يقرمش وتستوي الكفتة. قطّع ٤.")], pack=[("Wrap, then box so it stays crisp. Yogurt-tahini cup on the side.", "لفّ، وبعدين علبة ليضل مقرمش. كاسة لبن وطحينة ع جنب.")]),
      recipe(("Vegetarian skewer — $5", "سيخ خضرا — $5"), ("", ""), [("1 veg skewer · hummus or tahini 40 g · biwaz · lettuce", "سيخ خضرا · حمص أو طحينة ٤٠ غ · بيواز · خس")], [("Grill 8 min. Hummus on the bread, veg, biwaz, lettuce. Vegan — no yogurt, no toum mayo.", "اشوي ٨ دقايق. حمص ع الخبز، الخضرا، بيواز، خس. نباتي — بلا لبن، بلا مايونيز.")], pack=PACK_SANDWICH),
    ])

sec(("6 · Snack sandwiches (pan station)", "٦ · سندويشات سناك (محطة الطنجرة)"),
    ("One burner, one sauté pan, hot-hold. Counter person steps back to this station at rush.",
     "عين غاز وحدة، طنجرة قلي وحدة، تسخين. موظف الكاونتر بيرجع ع هالمحطة وقت الضغط."),
    [
      recipe(("Basterma — $5.50", "بسترما — $5.50"), ("", ""), [("60 g bought basterma, thin slices · tomato slices · pickles · 1 tsp olive oil", "٦٠ غ بسترما جاهزة شرائح رفيعة · شرائح بندورة · كبيس · ملعقة صغيرة زيت زيتون")], [("Cold-assembled, no cooking: lay the slices flat on the bread, tomato, pickles, a thread of olive oil. Roll. Warm 15 seconds on the saj only if the customer asks.", "بلا طبخ: افرد الشرائح ع الخبز، بندورة، كبيس، خيط زيت زيتون. لفّ. سخّن ١٥ ثانية ع الصاج بس إذا طلب الزبون.")], pack=PACK_SANDWICH),
      recipe(("Sawda djej — $5", "سودة دجاج — $5"), ("", ""), [("150 g chicken livers, cleaned · 1 tbsp oil · 1 tsp garlic · 1 tbsp pomegranate molasses · lemon · salt · pepper", "١٥٠ غ سودة دجاج منظّفة · ملعقة زيت · ملعقة صغيرة توم · ملعقة دبس رمان · حامض · ملح · فلفل")], [("Hot pan, oil, livers 3 min until browned outside and just cooked, garlic 30 s, molasses + lemon, toss. Onto bread with biwaz and pickles.", "طنجرة حامية، زيت، السودة ٣ دقايق لحد ما تتحمّر برّا وتستوي، التوم ٣٠ ثانية، دبس الرمان + الحامض، قلّب. ع الخبز مع بيواز وكبيس.")], pack=PACK_SANDWICH, confirm=True),
      recipe(("Sujuk — $5", "سجق — $5"), ("", ""), [("150 g sujuk sliced · tomato · pickles · toum", "١٥٠ غ سجق شرائح · بندورة · كبيس · توم")], [("Dry pan 3–4 min until the fat renders and edges crisp. Add diced tomato 1 min. Onto bread with toum and pickles.", "طنجرة بلا زيت ٣–٤ دقايق لحد ما يذوب الدهن وتقرمش الأطراف. ضيف بندورة مكعبات دقيقة. ع الخبز مع توم وكبيس.")], pack=PACK_SANDWICH),
      recipe(("Makanek — $5", "مقانق — $5"), ("", ""), [("150 g lamb makanek · 1 tbsp pomegranate molasses · lemon · pine nuts (optional)", "١٥٠ غ مقانق غنم · ملعقة دبس رمان · حامض · صنوبر (اختياري)")], [("Pan 5–6 min turning until browned through, molasses + lemon to glaze. Onto bread with pickles and a little toum.", "طنجرة ٥–٦ دقايق مع التقليب لحد ما تتحمّر وتستوي، دبس الرمان + الحامض للتغليف. ع الخبز مع كبيس وشوي توم.")], pack=PACK_SANDWICH),
      recipe(("Sandwich batata — $4.50", "سندويش بطاطا — $4.50"), ("", ""), [("Fries 120 g · coleslaw 50 g · pickles · toum or ketchup", "بطاطا ١٢٠ غ · كول سلو ٥٠ غ · كبيس · توم أو كاتشب")], [("Hot fries straight from the fryer, salt, onto the bread with coleslaw, pickles and the sauce the customer picks. Roll and seal.", "بطاطا سخنة من القلاية، ملح، ع الخبز مع كول سلو وكبيس والصوص يلي بيختارو الزبون. لفّ وسكّر.")], pack=PACK_SANDWICH, photo=False),
    ])

sec(("7 · Burgers and Kids", "٧ · البرغر والأولاد"), None, [
    recipe(("BCC Burger meal — $9", "وجبة برغر BCC — $9"), ("", ""), [("BCC Burger + side + salad + drink", "برغر BCC + طبق جانبي + سلطة + مشروب")], [("Make the burger as in §4. Side in its box, salad in a PET cup, drink from the cold case. Ask which of each.", "اعمل البرغر متل §٤. الجانبي بعلبتو، السلطة بكاسة PET، المشروب من البراد. اسأل عن كل واحد.")], pack=PACK_BURGER, photo=False),
    recipe(("Kafta burger — $5.50", "برغر كفتة — $5.50"), ("", ""), [("130 g kafta patty · toum mayo · pickles · brioche", "قرص كفتة ١٣٠ غ · مايونيز بالتوم · كبيس · بريوش")], [("Flat patty on the saj 3 min a side, cooked through. Toum mayo both buns, patty, pickles.", "قرص مسطّح ع الصاج ٣ دقايق كل وجه، مستوي. مايونيز بالتوم ع الخبزتين، القرص، الكبيس.")], pack=PACK_BURGER),
    recipe(("Grilled chicken burger — $5", "برغر دجاج مشوي — $5"), ("", ""), [("1 taouk-marinated breast 130 g, flattened · toum mayo · lettuce · tomato · brioche", "صدر دجاج متبّل طاووق ١٣٠ غ مرقوق · مايونيز بالتوم · خس · بندورة · بريوش")], [("Saj plate 4 min a side to 75 °C. Toum mayo, lettuce, chicken, tomato.", "الصاج ٤ دقايق كل وجه لـ٧٥ درجة. مايونيز بالتوم، خس، الدجاج، بندورة.")], pack=PACK_BURGER),
    recipe(("Veggie burger — $5", "برغر نباتي — $5"), ("12 patties", "١٢ قرص"), [("500 g cooked chickpeas · 200 g fine bulgur soaked · 1 onion · 1 carrot grated · parsley · 2 tbsp flour · cumin · seven-spice · salt · 1 egg (omit for vegan)", "٥٠٠ غ حمص مطبوخ · ٢٠٠ غ برغل ناعم منقوع · بصلة · جزرة مبشورة · بقدونس · ملعقتين طحين · كمون · سبع بهارات · ملح · بيضة (بلا بيضة للنباتي)")], [("Pulse coarse, shape 110 g patties, chill 30 min. Saj with oil 3–4 min a side. Build with hummus, lettuce, tomato, pickles.", "اطحن خشن، شكّل أقراص ١١٠ غ، براد ٣٠ دقيقة. الصاج مع زيت ٣–٤ دقايق كل وجه. ركّب مع حمص، خس، بندورة، كبيس.")], pack=PACK_BURGER, confirm=True),
    recipe(("Kids — burger · taouk · kafta — $5", "الأولاد — برغر · طاووق · كفتة — $5"), ("", ""), [("Kids burger: 90 g plain patty, ketchup, plain bun. Kids taouk / kafta: 1 small skewer 70 g, bread, toum on the side.", "برغر الأولاد: قرص سادة ٩٠ غ، كاتشب، خبز سادة. طاووق / كفتة الأولاد: سيخ صغير ٧٠ غ، خبز، توم ع جنب."), ("Side: small fries OR cucumber & carrot sticks OR small rice. Drink: apple or orange juice box, or water.", "الجانبي: بطاطا صغيرة أو أصابع خيار وجزر أو رز صغير. المشروب: عصير تفاح أو برتقال علبة، أو مي.")], [("Cut in half if asked. Nothing spicy. Ask about allergies when a parent orders.", "قطّع نصّين إذا طلبوا. ما في شي حار. اسأل عن الحساسية لما يطلب الأهل.")], pack=[("Kids box + juice + small napkins + a sticker if we have them.", "علبة أولاد + عصير + محارم صغيرة + ستيكر إذا في.")]),
])

sec(("8 · Plates, farrouj and the Family Box", "٨ · الصحون والفروج وبوكس العيلة"), None, [
    recipe(("Kabab plate — $9 · BCC mixed grill — $12", "صحن كباب — $9 · مشاوي BCC — $12"), ("", ""), [("Kabab plate: 3 skewers of the customer's choice (lamb/shi2af +$2), or half and half. Mixed grill: 1 kafta + 1 lamb + 1 taouk.", "صحن كباب: ٣ سياخ ع ذوق الزبون (غنم/شقف +$2)، أو نص ونص. المشاوي: كفتة + لحمة + طاووق."), ("Side 180 g · salad 100 g · hummus 80 g · bread · grilled tomato & onion · pickles + toum", "جانبي ١٨٠ غ · سلطة ١٠٠ غ · حمص ٨٠ غ · خبز · بندورة وبصل مشويين · كبيس + توم")], [("Grill skewers together, lamb first (longest). Slide onto a half bread in the plate box so the bread soaks the juice.", "اشوي السياخ سوا، الغنم أول (الأطول). زحلقها ع نص خبزة بعلبة الصحن ليشرب الخبز العصارة."), ("Ask: salad · side · bread · 2 sauces.", "اسأل: سلطة · جانبي · خبز · صوصين.")], pack=PACK_PLATE),
    recipe(("Farrouj meshwi 3al fa7m — $13 whole / $7 half", "فروج مشوي ع الفحم — $13 كامل / $7 نص"), ("", ""), [("Whole chicken 1.2 kg, spatchcocked, marinated overnight: lemon, garlic, oil, paprika, seven-spice, salt, pepper", "فروج ١.٢ كغ مفتوح ع الظهر، متبّل ليلة: حامض، توم، زيت، بابريكا، سبع بهارات، ملح، فلفل"), ("Toum 60 g · pickles · fries 180 g · bread", "توم ٦٠ غ · كبيس · بطاطا ١٨٠ غ · خبز")], [("Start whole chickens at 10:45 and keep 2–3 going at all times on the cooler side of the coals, skin up first, turn every 10 min, 35–45 min total, probe 75 °C at the thigh.", "ابدأ الفراريج الساعة ١٠:٤٥ وخلّي ٢–٣ دايماً ع الجهة الأبرد من الفحم، الجلد لفوق أول، اقلب كل ١٠ دقايق، ٣٥–٤٥ دقيقة، ٧٥ درجة عند الفخد."), ("Finish 2 min on the hot side for colour. Cut in 4 (half = 2 pieces). Fries fresh at order time.", "خلّص دقيقتين ع الجهة الحامية للون. قطّع ٤ (النص = قطعتين). البطاطا طازة وقت الطلب.")], pack=[("Farrouj box with bread under the chicken, fries box separate, toum + pickles cups. Napkins ×4, wet wipes ×2, fork + knife.", "علبة الفروج مع الخبز تحت الدجاج، علبة البطاطا لحالها، كاسات توم + كبيس. محارم ×٤، محارم مبلّلة ×٢، شوكة + سكين.")]),
    recipe(("Farrouj msa7ab — $15", "فروج مسحّب — $15"), ("", ""), [("Whole chicken boned and flattened (bone out, skin on), same marinade", "فروج كامل بلا عضم ومسحّب (مع الجلد)، نفس التتبيلة")], [("Grill flat under a weight (brick in foil) skin down 12 min, flip 10 min, probe 75 °C. Slice in strips on the bread.", "اشوي مسطّح تحت تقل (حجر ملفوف بقصدير) الجلد لتحت ١٢ دقيقة، اقلب ١٠ دقايق، ٧٥ درجة. قطّع أصابع ع الخبز.")], pack=PACK_PLATE),
    recipe(("Mashawi Family Box — $26 · every day", "بوكس مشاوي العيلة — $26 · كل يوم"), ("feeds 4", "لـ٤ أشخاص"), [("8 skewers (4 kafta + 4 taouk default; all kafta / all taouk / mixed with lamb +$4) · 4 breads · hummus 250 g · 2 large sides 300 g · 2 salads 250 g · 4 drinks · 3 sauces", "٨ سياخ (٤ كفتة + ٤ طاووق أساسي؛ كلها كفتة / كلها طاووق / مشكّل مع غنم +$4) · ٤ خبزات · حمص ٢٥٠ غ · طبقين كبار ٣٠٠ غ · سلطتين ٢٥٠ غ · ٤ مشروبات · ٣ صوصات")], [("Grill in two rounds so nothing waits more than 5 minutes. Into the Family Box on bread, sides and salads in large cups.", "اشوي ع جولتين ليما يستنّى شي أكتر من ٥ دقايق. بالبوكس ع الخبز، الجانبي والسلطات بكاسات كبيرة.")], pack=[("Family Box + drinks bag + 8 napkins + 4 wet wipes + 4 forks + 4 spoons + bag card. Tape the box.", "بوكس العيلة + كيس المشروبات + ٨ محارم + ٤ محارم مبلّلة + ٤ شوك + ٤ ملاعق + بطاقة الكيس. لزّق العلبة.")]),
    recipe(("Mashawi by the kilo", "مشاوي بالكيلو"), ("", ""), [("Mixed $26 · kafta $20 · taouk $19 · lamb $32 — raw weight. Raw marinated kit −25%. ½ kg and 2 kg. Sunday Kilo Day: mixed kilo $33 with the works.", "مشكّل $26 · كفتة $20 · طاووق $19 · غنم $32 — الوزن نيّ. نيّ ومتبّل −٢٥٪. نص كيلو وكيلوين. أحد الكيلو: كيلو مشكّل $33 مع كل شي.")], [("Weigh raw in front of the customer at the counter. Grilled: comes with bread, biwaz, grilled tomato & onion. Order by 18:00 for same-evening kilos.", "وزّن نيّ قدّام الزبون ع الكاونتر. المشوي: مع خبز، بيواز، بندورة وبصل مشويين. الطلب قبل الـ٦ مساءً لكيلو نفس السهرة.")], pack=[("Kilo tray, bread wrapped, biwaz cup, sauces. Raw kit: vacuum bag or sealed tub, ice pack, cooking card.", "صينية الكيلو، الخبز ملفوف، كاسة بيواز، صوصات. النيّ: كيس مفرّغ أو علبة مسكّرة، كيس تلج، بطاقة طريقة الشوي.")]),
])

sec(("9 · Light & Lean, sides, dessert cups, drinks", "٩ · خفيف وصحي، المقبلات، كاسات الحلو، المشروبات"), None, [
    recipe(("Salad & protein — $7 · Protein lettuce wrap — $6", "سلطة مع بروتين — $7 · لفّة خس مع بروتين — $6"), ("", ""), [("Any salad 250 g + 1 grilled skewer of the customer's choice sliced on top (lamb/shi2af +$1.50, orfali +$0.50, double +$3). Lemon + olive oil on the side. Lettuce wrap: 2 romaine leaves, protein or grilled veg, biwaz, yogurt-tahini cup.", "أي سلطة ٢٥٠ غ + سيخ مشوي ع ذوق الزبون شرائح فوق (غنم/شقف +$1.50، أورفلي +$0.50، دبل +$3). حامض + زيت زيتون ع جنب. لفّة الخس: ورقتين خس، بروتين أو خضرا مشوية، بيواز، كاسة لبن وطحينة.")], [("Grilled, never fried. Sauces always on the side in cups.", "مشوي، مش مقلي أبداً. الصوصات دايماً ع جنب بكاسات.")], pack=[("Salad bowl with lid, dressing cup, fork, napkins.", "وعاء سلطة مع غطا، كاسة صلصة، شوكة، محارم.")], photo=False),
    recipe(("Dessert cups — made every morning", "كاسات الحلو — بتنعمل كل صباح"), ("20 cups each", "٢٠ كاسة لكل نوع"),
        [("RIZ B'HALIB $2.50: 2 L milk, 200 g short rice, 200 g sugar, 2 tbsp orange-blossom water, pistachio on top.", "رز بحليب $2.50: ٢ ل حليب، ٢٠٠ غ رز قصير، ٢٠٠ غ سكر، ملعقتين ماء زهر، فستق حلبي فوق."), ("MHALABIYA $2.50: 2 L milk, 160 g cornflour, 200 g sugar, 2 tbsp rose water, pistachio.", "مهلبية $2.50: ٢ ل حليب، ١٦٠ غ نشا، ٢٠٠ غ سكر، ملعقتين ماء ورد، فستق حلبي."), ("CHOCOLATE MOUSSE $3: 500 g dark chocolate melted, 1 L cream whipped, 100 g sugar; hazelnut crumble on top.", "موس شوكولا $3: ٥٠٠ غ شوكولا غامقة دايبة، ١ ل كريمة مخفوقة، ١٠٠ غ سكر؛ بندق مطحون فوق.")],
        [("Portion into the 200 ml cups, lid, date sticker, cold case. 2 days max. Count at closing.", "وزّع بكاسات ٢٠٠ مل، غطا، لاصقة تاريخ، الفيترين البارد. يومين حد أقصى. عدّ عند الإغلاق."), ("Grab-and-go: nothing is made to order. Every dessert goes out with a spoon + napkin.", "جاهز للأخذ: ما في شي بينعمل ع الطلب. كل حلو بيطلع مع ملعقة + محرمة.")]),
    recipe(("Sides and drinks", "المقبلات والمشروبات"), ("", ""), [("Fries $2 · hummus $2.50 · fattoush $3 · tabbouleh $3 · coleslaw $2.50 · batata harra $3 · toum tub $3 · extra bread $1", "بطاطا $2 · حمص $2.50 · فتوش $3 · تبولة $3 · كول سلو $2.50 · بطاطا حرّة $3 · علبة توم $3 · خبز زيادة $1"), ("Soft drink $1.50 · water $1 · ayran $1.50 · fresh lemonade with mint $2.50 (squeezed to order: 2 lemons, 25 g sugar, mint, ice, 300 ml)", "مشروب غازي $1.50 · مي $1 · عيران $1.50 · ليموناضة بالنعنع $2.50 (معصورة ع الطلب: ٢ حامض، ٢٥ غ سكر، نعنع، تلج، ٣٠٠ مل)")], [("Every can or bottle goes out with a straw. Cold drinks in their own bag so they don't warm the food.", "كل تنكة أو قنينة بتطلع مع شاليمو. المشروبات الباردة بكيس لحالها ليما تسخّن الأكل.")], photo=False),
])

# ---------------------------------------------------------------- 10 · Packing
sec(("10 · Packing every order", "١٠ · توضيب كل طلب"),
    ("The counter+pack person owns the bag. Read the ticket, pack, tick, sticker, bag card, close.",
     "موظف الكاونتر والتوضيب مسؤول عن الكيس. اقرا الطلب، وضّب، علّم، لاصقة، بطاقة الكيس، سكّر."),
    [
      checklist(("In EVERY bag", "بكل كيس"), [
        ("Order sticker with the order number and the customer's first name on the bag and on every box.", "لاصقة الطلب مع رقم الطلب واسم الزبون الأول ع الكيس وع كل علبة."),
        ("Napkins: 2 per sandwich/burger, 4 per plate, 8 per Family Box.", "محارم: ٢ لكل سندويش/برغر، ٤ لكل صحن، ٨ لبوكس العيلة."),
        ("1 wet wipe per person.", "محرمة مبلّلة لكل شخص."),
        ("A straw with every can or bottle. A spoon + napkin with every dessert cup. Fork (+ knife for farrouj) with every plate, bowl and Kafta Fries.", "شاليمو مع كل تنكة أو قنينة. ملعقة + محرمة مع كل كاسة حلو. شوكة (+ سكين للفروج) مع كل صحن ووعاء وبطاطا كفتة."),
        ("Plates and boxes: pickles + toum cup, bread wrapped separately on top.", "الصحون والبوكسات: كاسة كبيس + توم، الخبز ملفوف لحالو فوق."),
        ("One bag card (QR to order · favourites · rewards) in every bag.", "بطاقة كيس وحدة (QR للطلب · المفضّلة · المكافآت) بكل كيس."),
        ("Hot and cold never touch: drinks and dessert cups in their own bag. Fries on top, boxes flat, sauces upright.", "السخن والبارد ما بيتلامسوا: المشروبات وكاسات الحلو بكيس لحالهن. البطاطا فوق، العلب مسطّحة، الصوصات واقفة."),
        ("Delivery: the whole order goes into the thermal bag the moment it is closed — never on the counter waiting.", "التوصيل: كل الطلب بيفوت ع الشنطة الحرارية لحظة ما يتسكّر — أبداً مش ع الكاونتر ناطر."),
      ]),
      text(("Why the bag card matters", "ليش بطاقة الكيس مهمة"), [
        ("It is our cheapest advertising: the QR brings the customer back to the full menu and online ordering, and the rewards line gives them a reason to give us their number next time.", "هي أرخص إعلان عنّا: الـ QR بيرجّع الزبون للمنيو الكامل والطلب أونلاين، وسطر المكافآت بيعطيه سبب يعطينا رقمو المرة الجاي."),
      ]),
    ])

# ---------------------------------------------------------------- 11 · Service, upsell, rewards, complaints, delivery
sec(("11 · Service scripts", "١١ · عبارات الخدمة"), None, [
    text(("At the counter", "ع الكاونتر"), [
        ("'Ahla w sahla b BCC Grill! Shou bte2mor?' — smile, eye contact, phone away.", "'أهلا وسهلا بـ BCC Grill! شو بتأمر؟' — ابتسامة، تواصل بالعين، التلفون بعيد."),
        ("Repeat the order back. Confirm bread, sauces, changes, veggies on/side. Give the time: 'ready in about 10 minutes'.", "عيد الطلب. أكّد الخبز، الصوص، التعديلات، الخضرا فوق/جنب. عطي الوقت: 'جاهز بحوالي ١٠ دقايق'."),
        ("Always ask for the phone number: 'Your number for the rewards? You get a point per dollar.'", "اسأل دايماً عن الرقم: 'رقمك للمكافآت؟ بتاخد نقطة لكل دولار.'"),
    ]),
    text(("The three upsell questions (ask them, every order)", "أسئلة الزيادة التلاتة (اسألها بكل طلب)"), [
        ("1 · 'Make it a meal for $3 more — side, salad and a drink?'", "١ · 'عملها وجبة بـ$3 زيادة — جانبي وسلطة ومشروب؟'"),
        ("2 · 'Anything to drink? Fresh lemonade with mint is $2.50.'", "٢ · 'شي تشربو؟ الليموناضة بالنعنع بـ$2.50.'"),
        ("3 · 'A dessert cup for after? Riz b'halib or chocolate mousse.' — and for burgers: 'extra patty for $2.50?'", "٣ · 'كاسة حلو لبعدين؟ رز بحليب أو موس شوكولا.' — وللبرغر: 'قرص زيادة بـ$2.50؟'"),
        ("Never push twice. One question each, then thank them.", "ما تلحّ مرتين. سؤال واحد لكل شي، وبعدين اشكرو."),
    ]),
    text(("Phone & WhatsApp orders", "طلبات التلفون والواتساب"), [
        ("'BCC Grill, marhaba!' Take: name · phone · delivery or take away · landmark (or ask them to send their location pin) · items with every choice · payment (cash or Whish).", "'BCC Grill، مرحبا!' خود: الاسم · الرقم · توصيل أو تيك أواي · أقرب معلم (أو اطلب منّن يبعتوا موقعهن) · الأصناف مع كل اختيار · الدفع (كاش أو Whish)."),
        ("Repeat it all back, give the total and a realistic time. Type it into the kitchen screen immediately.", "عيد كل شي، عطي المجموع ووقت واقعي. دخّلو ع شاشة المطبخ فوراً."),
        ("Website orders arrive on the kitchen screen AND on WhatsApp. Reply from the template: 'Shukran [name]! Order #[n] confirmed — [time] minutes. Total $[x], [cash/Whish].'", "طلبات الموقع بتوصل ع شاشة المطبخ وع الواتساب. ردّ من القالب: 'شكراً [الاسم]! الطلب #[n] مؤكّد — [الوقت] دقيقة. المجموع $[x]، [كاش/Whish].'"),
    ]),
    text(("BCC Rewards", "مكافآت BCC"), [
        ("1 point per $1 of the total. 50 points = $5 off the next order, online or at the counter. Points live on the phone number; the customer can see them on the website under 'My orders'.", "نقطة لكل $1 من المجموع. ٥٠ نقطة = $5 خصم ع الطلب الجاي، أونلاين أو بالمحل. النقاط ع رقم التلفون؛ الزبون بيشوفها ع الموقع تحت 'طلباتي'."),
        ("At the counter: type the phone in the counter screen, add the points for a cash order, or redeem 50 for $5. Tell them the balance: 'You have 38 points — 12 more and the next $5 is on us.'", "ع الكاونتر: اكتب الرقم بشاشة الكاونتر، زيد النقاط لطلب الكاش، أو استبدل ٥٠ بـ$5. خبّرن الرصيد: 'معك ٣٨ نقطة — ١٢ كمان والـ$5 الجاية علينا.'"),
    ]),
    text(("When something goes wrong", "لما يصير غلط"), [
        ("Listen fully. Apologise once, sincerely: 'You're right, I'm sorry.' Never argue about whose fault.", "اسمع للآخر. اعتذر مرة بصدق: 'معك حق، آسف.' ما تتجادل مين الغلطان."),
        ("Fix it now: remake the item, or refund the item, or add a free dessert cup. Wrong or late delivery: the delivery fee is refunded without being asked.", "صلّحها هلق: عيد الصنف، أو رجّع حقّو، أو ضيف كاسة حلو ببلاش. توصيل غلط أو متأخر: رسم التوصيل بيرجع بلا ما يطلب."),
        ("Write it on the shift sheet (what, who, how fixed). Anything about money over $10 or a health complaint: call Amin before the customer leaves.", "سجّلها ع ورقة الشيفت (شو، مين، كيف انصلّحت). أي شي عن مصاري فوق $10 أو شكوى صحية: اتّصل بأمين قبل ما يمشي الزبون."),
    ]),
    text(("Driver protocol", "بروتوكول السائق"), [
        ("Check the bag against the ticket before leaving. Thermal bag zipped. Open the Google Maps pin from the order.", "تأكّد من الكيس مقابل الطلب قبل ما تمشي. الشنطة الحرارية مسكّرة. افتح دبّوس Google Maps من الطلب."),
        ("Call on arrival, not from the road. Hand over with 'Sahtein!' Exact change ready; Whish: confirm the payment arrived before you leave.", "اتّصل عند الوصول، مش من الطريق. سلّم بـ'صحتين!' الفراطة جاهزة؛ Whish: تأكّد إنو الدفعة وصلت قبل ما تمشي."),
        ("Back at the shop tap 'Delivered' on the kitchen screen.", "لما ترجع ع المحل كبس 'تمّ التوصيل' ع شاشة المطبخ."),
    ]),
])
