const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const root = path.resolve('output/adaptive-html-final-sequential-16-modes-20260607_105404');
const htmlPath = path.join(root, 'pages', '11_beginner_browser_cache_everyday_library.html');
const url = 'file://' + htmlPath;
const shotDir = path.join(root, 'sources', 'screenshots');
fs.mkdirSync(shotDir, { recursive: true });

async function collect(page, width) {
  return await page.evaluate((width) => {
    const bodyText = document.body.innerText.replace(/\s+/g, ' ').trim();
    const body = document.body;
    const main = document.querySelector('main');
    const contentSections = Array.from(document.querySelectorAll('main > section'));
    const h2s = Array.from(document.querySelectorAll('h2'));
    const directH2s = contentSections.map(s => s.querySelector('h2')).filter(Boolean);
    const bodyHtml = body.innerHTML;
    const bodyOnly = document.body.cloneNode(true);
    bodyOnly.querySelectorAll('style').forEach(n => n.remove());
    const bodyOnlyHtml = bodyOnly.innerHTML;
    const widgets = Array.from(new Set(Array.from(bodyOnly.querySelectorAll('[class]')).flatMap(el => Array.from(el.classList)).filter(c => /^wg-\d+/.test(c)).map(c => c.match(/^wg-\d+/)[0]))).sort();
    return {
      width,
      title: document.title,
      h1: document.querySelectorAll('h1').length,
      mainClass: main ? main.className : null,
      themebar: !!document.querySelector('.ahf-themebar'),
      themeRadioCount: document.querySelectorAll('input[name="ahf-theme"]').length,
      tocLinks: document.querySelectorAll('nav.toc a').length,
      heroAnalogy: !!document.querySelector('.hero-analogy'),
      contentSections: contentSections.length,
      directSectionSurfaceCandidate: contentSections.filter(s => !s.classList.contains('try')).length,
      h2: h2s.length,
      directH2: directH2s.length,
      numberedH2: h2s.filter(h => h.querySelector('.num,.no')).length,
      numberedIcon: h2s.filter(h => h.querySelector('.num,.no') && h.querySelector('.body-icon')).length,
      directH2Icon: directH2s.filter(h => h.querySelector('.body-icon')).length,
      vtShells: bodyOnly.querySelectorAll('.vt-shell').length,
      widgets,
      termCards: bodyOnly.querySelectorAll('.term').length,
      dangerCards: bodyOnly.querySelectorAll('.danger').length,
      summaryCards: bodyOnly.querySelectorAll('.summary-card').length,
      practice: !!document.querySelector('#practice'),
      finalChecklist: !!document.querySelector('#final-checklist'),
      sourceNote: !!document.querySelector('.source-note'),
      overflowX: document.documentElement.scrollWidth > document.documentElement.clientWidth + 1,
      scrollWidth: document.documentElement.scrollWidth,
      clientWidth: document.documentElement.clientWidth,
      textChars: bodyText.length,
      bodyIconSvgAriaHidden: Array.from(document.querySelectorAll('.body-icon svg')).every(svg => svg.getAttribute('aria-hidden') === 'true'),
      forbiddenScript: !!document.querySelector('script:not([type="application/ld+json"])'),
      bodyOnlyHtmlLength: bodyOnlyHtml.length,
    };
  }, width);
}

(async () => {
  const browser = await chromium.launch({ headless: true });
  const results = [];
  for (const [width, suffix] of [[1280, '1280'], [390, '390']]) {
    const page = await browser.newPage({ viewport: { width, height: 1200 }, deviceScaleFactor: 1 });
    await page.goto(url, { waitUntil: 'load' });
    await page.emulateMedia({ reducedMotion: 'reduce' });
    await page.screenshot({ path: path.join(shotDir, `mode11-beginner-after-${suffix}.png`), fullPage: true });
    results.push(await collect(page, width));
    await page.close();
  }
  await browser.close();
  fs.writeFileSync('/tmp/ahf-mode11-after-metrics.json', JSON.stringify(results, null, 2));
  console.log(JSON.stringify(results, null, 2));
})();
