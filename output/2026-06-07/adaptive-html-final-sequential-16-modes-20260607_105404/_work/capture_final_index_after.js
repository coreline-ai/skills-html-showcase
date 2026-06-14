const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
const root = path.resolve('output/adaptive-html-final-sequential-16-modes-20260607_105404');
const url = 'file://' + path.join(root, 'index.html');
const shotDir = path.join(root, 'sources', 'screenshots');
fs.mkdirSync(shotDir, { recursive: true });
async function collect(page, width) {
  return await page.evaluate((width) => {
    const sections = Array.from(document.querySelectorAll('main > section'));
    const h2s = Array.from(document.querySelectorAll('h2'));
    return {
      width,
      title: document.title,
      h1: document.querySelectorAll('h1').length,
      mainClass: document.querySelector('main')?.className || null,
      themeRadioCount: document.querySelectorAll('input[name="ahf-theme"]').length,
      themebar: !!document.querySelector('.ahf-themebar'),
      directSections: sections.length,
      h2: h2s.length,
      directH2Icon: sections.map(s=>s.querySelector('h2')).filter(Boolean).filter(h=>h.querySelector('.body-icon')).length,
      linksToPages: document.querySelectorAll('a[href^="pages/"]').length,
      overflowX: document.documentElement.scrollWidth > document.documentElement.clientWidth + 1,
      scrollWidth: document.documentElement.scrollWidth,
      clientWidth: document.documentElement.clientWidth,
      coreHash: (document.querySelector('style')?.textContent.match(/adaptive-html-final-core-css-sha256:\s*([0-9a-f]{64})/)||[])[1] || null,
      forbiddenScript: !!document.querySelector('script:not([type="application/ld+json"])'),
    };
  }, width);
}
(async()=>{
  const browser = await chromium.launch({headless:true});
  const results=[];
  for (const [width,suffix] of [[1280,'1280'],[390,'390']]) {
    const page = await browser.newPage({viewport:{width,height:1200}, deviceScaleFactor:1});
    await page.goto(url,{waitUntil:'load'});
    await page.emulateMedia({reducedMotion:'reduce'});
    await page.screenshot({path:path.join(shotDir,`final-index-after-${suffix}.png`), fullPage:true});
    results.push(await collect(page,width));
    await page.close();
  }
  await browser.close();
  fs.writeFileSync(path.join(root,'sources','final-index-visual-contract-evidence.json'), JSON.stringify(results,null,2));
  console.log(JSON.stringify(results,null,2));
})();
