
const { chromium } = require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage();await p.goto('file:///home/claude/baissourcountryclub/grill-menu/manual/out/manual.html',{waitUntil:'networkidle'});await p.waitForTimeout(1500);
await p.pdf({path:'/home/claude/baissourcountryclub/grill-menu/manual/out/BCC_Grill_Team_Manual_EN_AR.pdf',format:'A4',printBackground:true,preferCSSPageSize:true});await b.close();console.log('pdf ok');})();
