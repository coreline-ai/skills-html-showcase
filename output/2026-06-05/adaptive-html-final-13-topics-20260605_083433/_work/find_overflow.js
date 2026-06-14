const { chromium } = require('./pw/node_modules/playwright');

const url = process.argv[2];
const width = Number(process.argv[3] || 390);
const height = Number(process.argv[4] || 900);

function cssPath(el) {
  const parts = [];
  while (el && el.nodeType === 1 && parts.length < 5) {
    let part = el.tagName.toLowerCase();
    if (el.id) part += `#${el.id}`;
    const cls = Array.from(el.classList || []).slice(0, 4);
    if (cls.length) part += '.' + cls.join('.');
    parts.unshift(part);
    el = el.parentElement;
  }
  return parts.join(' > ');
}

(async () => {
  const browser = await chromium.launch({
    headless: true,
    executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
  });
  const page = await browser.newPage({
    viewport: { width, height },
    colorScheme: 'light',
  });
  await page.goto(url, { waitUntil: 'networkidle' });
  await page.waitForSelector('main');
  const result = await page.evaluate((pathFnText) => {
    const cssPath = new Function('el', `return (${pathFnText})(el)`);
    const vw = window.innerWidth;
    const doc = document.documentElement;
    const items = [];
    for (const el of document.querySelectorAll('body *')) {
      const cs = getComputedStyle(el);
      if (cs.display === 'none' || cs.visibility === 'hidden') continue;
      const r = el.getBoundingClientRect();
      if (r.width <= 0 || r.height <= 0) continue;
      const overflowRight = r.right - vw;
      const overflowLeft = -r.left;
      if (overflowRight > 1 || overflowLeft > 1) {
        items.push({
          path: cssPath(el),
          left: Math.round(r.left),
          right: Math.round(r.right),
          width: Math.round(r.width),
          overflowRight: Math.round(overflowRight),
          overflowLeft: Math.round(overflowLeft),
          display: cs.display,
          overflowX: cs.overflowX,
          whiteSpace: cs.whiteSpace,
          text: (el.textContent || '').replace(/\s+/g, ' ').trim().slice(0, 120),
        });
      }
    }
    items.sort((a, b) => Math.max(b.overflowRight, b.overflowLeft) - Math.max(a.overflowRight, a.overflowLeft));
    return {
      viewport: vw,
      scrollWidth: doc.scrollWidth,
      bodyScrollWidth: document.body.scrollWidth,
      items: items.slice(0, 40),
    };
  }, cssPath.toString());
  console.log(JSON.stringify(result, null, 2));
  await browser.close();
})();
