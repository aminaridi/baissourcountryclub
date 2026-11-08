const { chromium } = require('playwright'); const path=require('path');
(async()=>{
  const b=await chromium.launch();
  const f=n=>'file://'+path.resolve('out',n);
  // printed PDFs + page PNGs
  for (const l of ['en','ar']) {
    const p=await b.newPage({viewport:{width:794,height:1123},deviceScaleFactor:2});
    await p.goto(f(`print_${l}.html`),{waitUntil:'networkidle'}); await p.waitForTimeout(1500);
    await p.pdf({path:`out/BCC_Grill_Menu_A4_${l.toUpperCase()}.pdf`,format:'A4',printBackground:true,preferCSSPageSize:true});
    await p.screenshot({path:`out/print_${l}_preview.png`,fullPage:true}); await p.close();
  }
  for (const n of ['tv_bi','tv_en','tv_ar']) {
    const p=await b.newPage({viewport:{width:1920,height:1080},deviceScaleFactor:1});
    await p.goto(f(n+'.html'),{waitUntil:'networkidle'}); await p.waitForTimeout(1500);
    await p.screenshot({path:`out/${n}.png`}); await p.close();
  }
  for (const n of ['phone_bi','phone_ar']) {
    const p=await b.newPage({viewport:{width:1080,height:1920},deviceScaleFactor:1});
    await p.goto(f(n+'.html'),{waitUntil:'networkidle'}); await p.waitForTimeout(1500);
    await p.screenshot({path:`out/${n}.png`,fullPage:true}); await p.close();
  }
  await b.close(); console.log('rendered');
})();
