const { chromium } = require('playwright');
const fs = require('fs');
(async () => {
  const url = 'http://localhost:8080/output/adaptive-html-final-sequential-16-modes-20260607_105404/pages/04_education_postgres_query_plan_workshop.html';
  const browser = await chromium.launch({headless: true});
  const results = {};
  for (const [label, width, height] of [['1280',1280,1600], ['390',390,1600]]) {
    const page = await browser.newPage({viewport:{width,height}, deviceScaleFactor:1});
    await page.goto(url, {waitUntil:'networkidle'});
    await page.screenshot({path:`/tmp/ahf-mode04-before-${label}.png`, fullPage:true});
    results[label] = await page.evaluate(() => {
      const body = document.body;
      const main = document.querySelector('main');
      const h2s = [...document.querySelectorAll('main > section > h2, main > article > section > h2')];
      const tables = [...document.querySelectorAll('table')];
      const tableUnsafe = tables.filter(t => !t.closest('.table-scroll') && !t.className.includes('mobile-card') && !t.className.includes('final-matrix')).length;
      const directSections = [...document.querySelectorAll('main > section')];
      const nonTry = directSections.filter(s => !s.classList.contains('try'));
      const surface = nonTry.filter(s => {
        const cs = getComputedStyle(s);
        return cs.backgroundColor !== 'rgba(0, 0, 0, 0)' && cs.borderTopWidth !== '0px';
      });
      return {
        title: document.title,
        h1: document.querySelectorAll('h1').length,
        themeInputs: document.querySelectorAll('input[name="ahf-theme"]').length,
        themebar: !!document.querySelector('.ahf-themebar'),
        bodyScrollWidth: body.scrollWidth,
        bodyClientWidth: body.clientWidth,
        overflow: body.scrollWidth > body.clientWidth + 2,
        mainClass: main?.className || null,
        directSections: directSections.length,
        nonTrySections: nonTry.length,
        surfaceSections: surface.length,
        directH2: h2s.length,
        h2WithNum: h2s.filter(h => h.querySelector('.num,.no')).length,
        h2WithIcon: h2s.filter(h => h.querySelector('.body-icon')).length,
        h2Titles: h2s.map(h => h.innerText.replace(/\s+/g,' ').trim()).slice(0,20),
        vtShells: document.querySelectorAll('.vt-shell').length,
        vtTimeline: document.querySelectorAll('.tl,.tl-item').length,
        vtChecklist: document.querySelectorAll('.cf,.cf-item').length,
        vtConcept: document.querySelectorAll('.concept-ring,.concept-step').length,
        wg06: document.querySelectorAll('[class*="wg-06-"]').length,
        wg13: document.querySelectorAll('[class*="wg-13-"]').length,
        wg14: document.querySelectorAll('[class*="wg-14-"]').length,
        wg15: document.querySelectorAll('[class*="wg-15-"]').length,
        tableCount: tables.length,
        tableUnsafe,
        sourceNote: !!document.querySelector('.source-note'),
        textLength: (main?.innerText || '').length
      };
    });
    await page.close();
  }
  await browser.close();
  fs.writeFileSync('/tmp/ahf-mode04-before-metrics.json', JSON.stringify(results, null, 2));
})();
