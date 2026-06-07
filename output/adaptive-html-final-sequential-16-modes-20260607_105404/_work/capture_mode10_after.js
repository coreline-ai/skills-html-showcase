const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
const url = 'http://localhost:8080/output/adaptive-html-final-sequential-16-modes-20260607_105404/pages/10_blog_four_days_with_ai_review_notes.html';
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
  const articleSections=$('#main > article > section');
  const directMainSections=$('#main > section');
  const allContentSections=$('#main > article > section, #main > section');
  const surfaced=allContentSections.filter(s=>{
    const cs=getComputedStyle(s);
    return cs.backgroundColor !== 'rgba(0, 0, 0, 0)' && cs.backgroundColor !== 'transparent';
  }).length;
  const text=document.body.innerText;
  return {
   h1:$('h1').length,
   mainClass:document.querySelector('#main')?.className||'',
   themebar:!!document.querySelector('.ahf-themebar'), themeRadioCount:$('input[name="ahf-theme"]').length,
   generatedRow:!!document.querySelector('.generated-row'), lensStrip:!!document.querySelector('.lens-strip'), tocLinks:$('.toc-map a[href^="#"]').length,
   articleSections:articleSections.length, directMainSections:directMainSections.length, contentSections:allContentSections.length, contentSectionsWithBg:surfaced,
   h2:h2.length, numberedH2:numbered.length, numberedIcon:icon, h2IconComplete: icon===numbered.length,
   vtShells:$('.vt-shell').length, widgets:['wg-17'].filter(c=>bodyHtml.includes(c)), personalNote:!!document.querySelector('.personal-note'), softCta:!!document.querySelector('.soft-cta'), sourceNote:!!document.querySelector('.source-note'),
   hasTitleCandidates:text.includes('제목 후보'), hasMetaDescription:text.includes('메타 설명'), hasTags:text.includes('태그:'), hasHook:text.includes('프롬프트를 계속 늘리는데도'), hasCta:text.includes('오늘 바로 남길 리뷰 노트'),
   overflowX:document.documentElement.scrollWidth>window.innerWidth, scrollWidth:document.documentElement.scrollWidth, clientWidth:document.documentElement.clientWidth,
   textChars:text.length
  };
 });
 const screenshot=path.join(outDir,`mode10-blog-after-${width}.png`);
 await page.screenshot({path:screenshot,fullPage:true});
 await browser.close();
 return {viewport:{width,height},screenshot,metrics:m};
}
(async()=>{
 const runs=[await cap(1280,900),await cap(390,900)];
 fs.writeFileSync('/tmp/ahf-mode10-after-metrics.json',JSON.stringify(runs,null,2));
 console.log(JSON.stringify(runs,null,2));
})();
