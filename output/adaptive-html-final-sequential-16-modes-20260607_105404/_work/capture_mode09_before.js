const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
const url = 'http://localhost:8080/output/adaptive-html-final-sequential-16-modes-20260607_105404/pages/09_article_judgment_log_over_prompt.html';
const outDir = path.resolve('output/adaptive-html-final-sequential-16-modes-20260607_105404/sources/screenshots');
fs.mkdirSync(outDir,{recursive:true});
async function cap(width,height){
 const browser=await chromium.launch({headless:true});
 const page=await browser.newPage({viewport:{width,height},deviceScaleFactor:1});
 await page.goto(url,{waitUntil:'networkidle'});
 await page.emulateMedia({reducedMotion:'reduce'});
 const m=await page.evaluate(()=>{
  const $=(s,r=document)=>Array.from(r.querySelectorAll(s));
  const bodyHtml=document.body.innerHTML;
  const h2=$('#main h2');
  const numbered=h2.filter(x=>x.querySelector(':scope > .num, :scope > .no'));
  const icon=numbered.filter(x=>x.querySelector(':scope > .body-icon svg')).length;
  const sections=$('#main section, #main article > section');
  return {
   h1:$('h1').length, mainClass:document.querySelector('#main')?.className||'', themebar:!!document.querySelector('.ahf-themebar'), themeRadioCount:$('input[name="ahf-theme"]').length,
   sections:sections.length, h2:h2.length, numberedH2:numbered.length, numberedIcon:icon, h2IconComplete: icon===numbered.length,
   articleSections:$('#main > article > section').length, vtShells:$('.vt-shell').length,
   widgets:['wg-02','wg-04','wg-07','wg-09','wg-10','wg-13','wg-14'].filter(c=>bodyHtml.includes(c)),
   pullQuote:!!document.querySelector('.pull-quote'), takeaway:!!document.querySelector('.article-takeaway'), related:!!document.querySelector('.related-list'),
   overflowX:document.documentElement.scrollWidth>window.innerWidth, scrollWidth:document.documentElement.scrollWidth, clientWidth:document.documentElement.clientWidth,
   textChars:document.body.innerText.length
  };
 });
 const screenshot=path.join(outDir,`mode09-article-before-${width}.png`);
 await page.screenshot({path:screenshot,fullPage:true});
 await browser.close();
 return {viewport:{width,height},screenshot,metrics:m};
}
(async()=>{
 const runs=[await cap(1280,900),await cap(390,900)];
 fs.writeFileSync('/tmp/ahf-mode09-before-metrics.json',JSON.stringify(runs,null,2));
 console.log(JSON.stringify(runs,null,2));
})();
