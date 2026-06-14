const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const url = 'http://localhost:8080/output/adaptive-html-final-sequential-16-modes-20260607_105404/pages/07_manual_analysis_oncall_incident_runbook.html';
const outDir = path.resolve('output/adaptive-html-final-sequential-16-modes-20260607_105404/sources/screenshots');
fs.mkdirSync(outDir, { recursive: true });

async function capture(width, height, name) {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage({ viewport: { width, height }, deviceScaleFactor: 1 });
  await page.goto(url, { waitUntil: 'networkidle' });
  await page.emulateMedia({ reducedMotion: 'reduce' });
  const metrics = await page.evaluate(() => {
    const $ = (s, r=document) => Array.from(r.querySelectorAll(s));
    const directSections = $('#main > section');
    const directH2 = $('#main > section > h2');
    const h2Icon = directH2.filter(h => !!h.querySelector(':scope > .body-icon svg')).length;
    const numbered = directH2.filter(h => !!h.querySelector(':scope > .num, :scope > .no')).length;
    const tocLinks = $('.toc-map a[href^="#"]');
    const tocTargetsOk = tocLinks.every(a => !!document.querySelector(a.getAttribute('href')));
    const tables = $('table');
    const unsafeTables = tables.filter(t => !t.closest('.table-scroll') && !t.classList.contains('mobile-card-table')).length;
    const classes = document.documentElement.innerHTML;
    const roleCards = $('.manual-role').length;
    const troubleCards = $('.manual-trouble').length;
    const auditCards = $('#manual-audit .manual-audit-grid .manual-card').length;
    const recipeRows = $('#recipes table tbody tr').length;
    const radios = $('input[name="ahf-theme"]').map(x => x.id);
    return {
      title: document.title,
      h1: $('h1').length,
      mainClass: document.querySelector('#main')?.className || null,
      themebar: !!document.querySelector('.ahf-themebar'),
      themeRadioCount: radios.length,
      themeRadios: radios,
      generatedRow: !!document.querySelector('.generated-row'),
      lensStrip: !!document.querySelector('.lens-strip'),
      directSections: directSections.length,
      directH2: directH2.length,
      numberedH2: numbered,
      h2Icon,
      h2IconComplete: directH2.length === h2Icon,
      h2Sub: $('#main > section > .h2-sub').length,
      tocLinks: tocLinks.length,
      tocTargetsOk,
      vtShells: $('.vt-shell').length,
      widgets: ['wg-04','wg-11','wg-13','wg-16','wg-18'].filter(c => classes.includes(c)),
      roleCards,
      recipeRows,
      troubleCards,
      auditCards,
      sourceLimits: document.body.innerText.includes('Source Limits') && document.body.innerText.includes('확인하지 못한 항목'),
      unknownCount: (document.body.innerText.match(/UNKNOWN|확인 불가/g) || []).length,
      tables: tables.length,
      captions: $('caption').length,
      unsafeTables,
      overflowX: document.documentElement.scrollWidth > window.innerWidth,
      scrollWidth: document.documentElement.scrollWidth,
      clientWidth: document.documentElement.clientWidth,
      bodyTextChars: document.body.innerText.length,
    };
  });
  const screenshot = path.join(outDir, `mode07-manual-after-${width}.png`);
  await page.screenshot({ path: screenshot, fullPage: true });
  await browser.close();
  return { viewport: { width, height }, screenshot, metrics };
}

(async () => {
  const runs = [];
  runs.push(await capture(1280, 900, 'desktop'));
  runs.push(await capture(390, 900, 'mobile'));
  fs.writeFileSync('/tmp/ahf-mode07-after-metrics.json', JSON.stringify(runs, null, 2));
  console.log(JSON.stringify(runs, null, 2));
})();
