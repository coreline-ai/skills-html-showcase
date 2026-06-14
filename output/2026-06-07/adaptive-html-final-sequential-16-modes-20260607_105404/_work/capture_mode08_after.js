const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
const url = 'http://localhost:8080/output/adaptive-html-final-sequential-16-modes-20260607_105404/pages/08_expert_multi_agent_html_quality_gate_architecture.html';
const outDir = path.resolve('output/adaptive-html-final-sequential-16-modes-20260607_105404/sources/screenshots');
fs.mkdirSync(outDir,{recursive:true});
async function cap(width,height){
 const browser=await chromium.launch({headless:true});
 const page=await browser.newPage({viewport:{width,height},deviceScaleFactor:1});
 await page.goto(url,{waitUntil:'networkidle'});
 await page.emulateMedia({reducedMotion:'reduce'});
 const m=await page.evaluate(()=>{
  const $=(s,r=document)=>Array.from(r.querySelectorAll(s));
  const h2=$('#main h2');
  const numbered=h2.filter(x=>x.querySelector(':scope > .num, :scope > .no'));
  const icon=numbered.filter(x=>x.querySelector(':scope > .body-icon svg')).length;
  const direct=$('#main > section');
  const directBg=direct.filter(s=>getComputedStyle(s).backgroundColor !== 'rgba(0, 0, 0, 0)' && getComputedStyle(s).backgroundColor !== 'transparent').length;
  const visibleText=document.body.innerText;
  return {
   h1:$('h1').length, mainClass:document.querySelector('#main')?.className||'', themebar:!!document.querySelector('.ahf-themebar'), themeRadioCount:$('input[name="ahf-theme"]').length,
   generatedRow:!!document.querySelector('.generated-row'), lensStrip:!!document.querySelector('.lens-strip'),
   directSections:direct.length, directSectionWithBg:directBg, h2:h2.length, numberedH2:numbered.length, numberedIcon:icon, h2IconComplete: icon===numbered.length,
   directSectionFirstH2Icon:$('#main > section > h2').filter(x=>x.querySelector(':scope > .body-icon svg')).length,
   vtShells:$('.vt-shell').length, widgets:['wg-03','wg-04','wg-11','wg-12','wg-16','wg-17'].filter(c=>document.documentElement.innerHTML.includes(c)),
   tables:$('table').length, captions:$('caption').length, unsafeTables:$('table').filter(t=>!t.closest('.table-scroll')&&!t.classList.contains('mobile-card-table')).length,
   hasExecutive:visibleText.includes('Executive Summary'), hasRaci:visibleText.includes('RACI')||visibleText.includes('책임'), hasRisk:visibleText.includes('Risk Matrix'), hasRoadmap:visibleText.includes('90일'), hasValidation:visibleText.includes('Validation Checklist'),
   overflowX:document.documentElement.scrollWidth>window.innerWidth, scrollWidth:document.documentElement.scrollWidth, clientWidth:document.documentElement.clientWidth,
   textChars:visibleText.length
  };
 });
 const screenshot=path.join(outDir,`mode08-expert-after-${width}.png`);
 await page.screenshot({path:screenshot,fullPage:true});
 await browser.close();
 return {viewport:{width,height},screenshot,metrics:m};
}
(async()=>{
 const runs=[await cap(1280,900),await cap(390,900)];
 fs.writeFileSync('/tmp/ahf-mode08-after-metrics.json',JSON.stringify(runs,null,2));
 console.log(JSON.stringify(runs,null,2));
})();
