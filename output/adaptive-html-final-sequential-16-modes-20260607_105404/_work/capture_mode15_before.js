const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
const root = path.resolve('output/adaptive-html-final-sequential-16-modes-20260607_105404');
const htmlPath = path.join(root, 'pages', '15_landing_brief_launchbrief_studio.html');
const url = 'file://' + htmlPath;
const shotDir = path.join(root, 'sources', 'screenshots');
fs.mkdirSync(shotDir, { recursive: true });
async function collect(page, width) {
  return await page.evaluate((width) => {
    const main = document.querySelector('main');
    const bodyOnly = document.body.cloneNode(true);
    bodyOnly.querySelectorAll('style').forEach(n => n.remove());
    const sections = Array.from(document.querySelectorAll('main > section'));
    const h2s = Array.from(document.querySelectorAll('h2'));
    const directH2s = sections.map(s=>s.querySelector('h2')).filter(Boolean);
    const widgets = Array.from(new Set(Array.from(bodyOnly.querySelectorAll('[class]')).flatMap(el=>Array.from(el.classList)).filter(c=>/^wg-\d+/.test(c)).map(c=>c.match(/^wg-\d+/)[0]))).sort();
    return {
      width,
      title: document.title,
      h1: document.querySelectorAll('h1').length,
      mainClass: main ? main.className : null,
      themebar: !!document.querySelector('.ahf-themebar'),
      themeRadioCount: document.querySelectorAll('input[name="ahf-theme"]').length,
      contentSections: sections.length,
      h2: h2s.length,
      directH2: directH2s.length,
      numberedH2: h2s.filter(h=>h.querySelector('.num,.no')).length,
      numberedIcon: h2s.filter(h=>h.querySelector('.num,.no') && h.querySelector('.body-icon')).length,
      directH2Icon: directH2s.filter(h=>h.querySelector('.body-icon')).length,
      vtShells: bodyOnly.querySelectorAll('.vt-shell').length,
      widgets,
      tables: document.querySelectorAll('table').length,
      hero: !!document.querySelector('.hero-analogy'),
      valueGrid: !!document.querySelector('.value-grid'),
      howItWorks: !!document.querySelector('.how-it-works'),
      faq: !!document.querySelector('.faq'),
      cta: !!document.querySelector('.try'),
      sourceNote: !!document.querySelector('.source-note'),
      overflowX: document.documentElement.scrollWidth > document.documentElement.clientWidth + 1,
      scrollWidth: document.documentElement.scrollWidth,
      clientWidth: document.documentElement.clientWidth,
      textChars: document.body.innerText.replace(/\s+/g,' ').trim().length,
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
    await page.screenshot({path:path.join(shotDir,`mode15-landing-before-${suffix}.png`), fullPage:true});
    results.push(await collect(page,width));
    await page.close();
  }
  await browser.close();
  fs.writeFileSync('/tmp/ahf-mode15-before-metrics.json', JSON.stringify(results,null,2));
  console.log(JSON.stringify(results,null,2));
})();
