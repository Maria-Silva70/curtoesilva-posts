const { chromium } = require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1350}});
for(const f of process.argv.slice(2)){await p.goto('file://'+f);await p.waitForTimeout(400);await p.screenshot({path:f.replace('.html','.jpg'),type:'jpeg',quality:92});}
await b.close();})();
