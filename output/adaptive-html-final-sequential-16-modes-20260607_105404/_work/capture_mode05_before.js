const { chromium } = require('playwright');
const fs = require('fs');
(async () => {
  const url = 'http://localhost:8080/output/adaptive-html-final-sequential-16-modes-20260607_105404/pages/05_github_analysis_skills_html_showcase_due_diligence.html';
  const browser = await chromium.launch({headless: true});
  const results = {};
  for (const [label, width, height] of [['1280',1280,1600], ['390',390,1600]]) {
    const page = await browser.newPage({viewport:{width,height}, deviceScaleFactor:1});
    await page.goto(url, {waitUntil:'networkidle'});
    await page.screenshot({path:`/tmp/ahf-mode05-before-${label}.png`, fullPage:true});
    results[label] = await page.evaluate(() => {
      const body = document.body;
      const main = document.querySelector('main');
      const h2s = [...document.querySelectorAll('main > section > h2, main > article > section > h2')];
      const tables = [...document.querySelectorAll('table')];
      const tableUnsafe = tables.filter(t => !t.closest('.table-scroll') && !t.className.includes('mobile-card') && !t.className.includes('final-matrix')).length;
      const directSections = [...document.querySelectorAll('main > section')];
      const semanticGridSections = [...document.querySelectorAll('main > section')].filter(s => getComputedStyle(s).display.includes('grid')).map(s => s.className);
      return {
        title: document.title,
        h1: document.querySelectorAll('h1').length,
        themeInputs: document.querySelectorAll('input[name="ahf-theme"]').length,
        themebar: !!document.querySelector('.ahf-themebar'),
        overflow: body.scrollWidth > body.clientWidth + 2,
        bodyScrollWidth: body.scrollWidth,
        bodyClientWidth: body.clientWidth,
        mainClass: main?.className || null,
        directSections: directSections.length,
        directH2: h2s.length,
        h2WithNum: h2s.filter(h => h.querySelector('.num,.no')).length,
        h2WithIcon: h2s.filter(h => h.querySelector('.body-icon')).length,
        directH2IconOrder: h2s.every(h => {
          const kids = [...h.children].map(el => el.className || el.tagName);
          return kids[0]?.includes('body-icon') && kids[1]?.includes('num');
        }),
        h2Titles: h2s.map(h => h.innerText.replace(/\s+/g,' ').trim()).slice(0,20),
        tocLinks: document.querySelectorAll('.github-question-toc a,.toc a').length,
        generatedRow: !!document.querySelector('.generated-row'),
        lensStrip: !!document.querySelector('.lens-strip'),
        vtShells: document.querySelectorAll('.vt-shell').length,
        heroMap: document.querySelectorAll('.hm-grid,.hm-card,.hm-result').length,
        qualityGate: document.querySelectorAll('.qg-grid,.qg-card,.qg-final').length,
        fileTour: document.querySelectorAll('.ft,.ft-card,.ft-note').length,
        riskMatrix: document.querySelectorAll('.rm-grid,.rm-cell,.rm-risk').length,
        decisionTree: document.querySelectorAll('.dt-q,.dt-card,.dt-options').length,
        checklistFlow: document.querySelectorAll('.cf,.cf-item').length,
        wg11: document.querySelectorAll('[class*="wg-11-"]').length,
        wg04: document.querySelectorAll('[class*="wg-04-"]').length,
        wg14: document.querySelectorAll('[class*="wg-14-"]').length,
        wg16: document.querySelectorAll('[class*="wg-16-"]').length,
        factCount: (main?.innerText.match(/FACT/g)||[]).length,
        inferenceCount: (main?.innerText.match(/INFERENCE/g)||[]).length,
        unknownCount: (main?.innerText.match(/UNKNOWN|확인 불가/g)||[]).length,
        tableCount: tables.length,
        tableUnsafe,
        semanticGridSections,
        sourceNote: !!document.querySelector('.source-note'),
        textLength: (main?.innerText || '').length
      };
    });
    await page.close();
  }
  await browser.close();
  fs.writeFileSync('/tmp/ahf-mode05-before-metrics.json', JSON.stringify(results, null, 2));
})();
