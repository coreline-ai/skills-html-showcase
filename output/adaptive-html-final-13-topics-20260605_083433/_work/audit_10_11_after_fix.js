const { chromium } = require('./pw/node_modules/playwright');
const fs = require('fs');
const path = require('path');

const baseUrl = 'http://127.0.0.1:8770';
const outDir = path.resolve(__dirname, '../_visual-audit/fix-10-11');
fs.mkdirSync(outDir, { recursive: true });

const pages = [
  '10-vector-db-pgvector-search-engine-comparison',
  '11-reservation-reminder-delay-case-study',
];

const themes = ['light', 'white', 'dark'];
const viewports = [
  ['desktop', { width: 1440, height: 1200 }],
  ['mobile', { width: 390, height: 1100 }],
];

function rgbToLuminance(rgb) {
  const match = String(rgb).match(/rgba?\((\d+),\s*(\d+),\s*(\d+)/);
  if (!match) return null;
  const parts = match.slice(1, 4).map((n) => Number(n) / 255);
  const linear = parts.map((value) => (
    value <= 0.03928 ? value / 12.92 : ((value + 0.055) / 1.055) ** 2.4
  ));
  return 0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2];
}

function contrastRatio(fg, bg) {
  const a = rgbToLuminance(fg);
  const b = rgbToLuminance(bg);
  if (a == null || b == null) return null;
  const lighter = Math.max(a, b);
  const darker = Math.min(a, b);
  return (lighter + 0.05) / (darker + 0.05);
}

(async () => {
  const browser = await chromium.launch({ headless: true });
  const results = [];

  for (const pageSlug of pages) {
    for (const [viewportName, viewport] of viewports) {
      const context = await browser.newContext({ viewport });
      const page = await context.newPage();

      for (const theme of themes) {
        await page.goto(`${baseUrl}/pages/${pageSlug}.html`, { waitUntil: 'networkidle' });
        await page.evaluate((name) => {
          const input = document.querySelector(`#ahf-${name}`);
          if (!input) throw new Error(`missing theme input: ${name}`);
          input.checked = true;
          input.dispatchEvent(new Event('input', { bubbles: true }));
          input.dispatchEvent(new Event('change', { bubbles: true }));
        }, theme);
        await page.waitForTimeout(150);

        const metrics = await page.evaluate(() => {
          const root = document.documentElement;
          const body = document.body;
          const dt = document.querySelector('.dt-q');
          const dtItems = dt ? Array.from(dt.children).map((el) => {
            const r = el.getBoundingClientRect();
            return {
              tag: el.tagName,
              className: el.className,
              x: Math.round(r.x),
              y: Math.round(r.y),
              width: Math.round(r.width),
              height: Math.round(r.height),
            };
          }) : [];
          const tryEl = document.querySelector('.try');
          const tryStyle = tryEl ? getComputedStyle(tryEl) : null;
          const tryHeading = tryEl ? tryEl.querySelector('h2,h3') : null;
          const tryHeadingStyle = tryHeading ? getComputedStyle(tryHeading) : null;
          return {
            viewportWidth: window.innerWidth,
            scrollWidth: Math.max(root.scrollWidth, body.scrollWidth),
            overflowX: Math.max(root.scrollWidth, body.scrollWidth) - window.innerWidth,
            dtDisplay: dt ? getComputedStyle(dt).gridTemplateColumns : null,
            dtItems,
            tryBg: tryStyle ? tryStyle.backgroundColor : null,
            tryColor: tryStyle ? tryStyle.color : null,
            tryHeadingColor: tryHeadingStyle ? tryHeadingStyle.color : null,
          };
        });

        metrics.tryContrast = contrastRatio(metrics.tryColor, metrics.tryBg);
        metrics.tryHeadingContrast = contrastRatio(metrics.tryHeadingColor, metrics.tryBg);
        results.push({ page: pageSlug, viewport: viewportName, theme, ...metrics });

        await page.screenshot({
          path: path.join(outDir, `${pageSlug}__${viewportName}-${theme}.png`),
          fullPage: true,
        });
      }

      await context.close();
    }
  }

  await browser.close();

  const bad = results.filter((row) => {
    const hasOverflow = row.overflowX > 1;
    const badTryContrast = row.tryContrast != null && row.tryContrast < 4.5;
    const badHeadingContrast = row.tryHeadingContrast != null && row.tryHeadingContrast < 4.5;
    let badDecisionTree = false;
    if (row.page.startsWith('10') && row.viewport === 'desktop') {
      const cards = row.dtItems.filter((item) => String(item.className).includes('dt-card'));
      const arrows = row.dtItems.filter((item) => String(item.className).includes('dt-arrow'));
      badDecisionTree = row.dtItems.length !== 5 ||
        cards.length !== 3 ||
        arrows.length !== 2 ||
        new Set(cards.map((item) => item.y)).size !== 1 ||
        cards.some((item) => item.width <= 180) ||
        arrows.some((item) => item.width <= 40);
    }
    return hasOverflow || badTryContrast || badHeadingContrast || badDecisionTree;
  });

  console.log(JSON.stringify({ results, bad }, null, 2));
  if (bad.length) process.exit(1);
})();
