const { chromium } = require('playwright');
const path = require('path'), fs = require('fs');
(async () => {
  const dir = path.resolve(process.argv[2]);
  const file = 'file://' + path.join(dir, 'index.html');
  const browser = await chromium.launch();
  const viewports = { '1280': 1280, '390': 390 };
  const audit = { generated_for: 'proxmox-redroid-kakaotalk-manual', viewports: {} };
  for (const [key, w] of Object.entries(viewports)) {
    const page = await browser.newPage({ viewport: { width: w, height: 900 }, deviceScaleFactor: 1 });
    await page.goto(file, { waitUntil: 'networkidle' });
    const m = await page.evaluate(() => ({
      scrollWidth: document.documentElement.scrollWidth,
      clientWidth: document.documentElement.clientWidth,
    }));
    const overflow_ok = m.scrollWidth <= m.clientWidth + 1;
    const shot = `sources/screenshots/${key}.png`;
    await page.screenshot({ path: path.join(dir, shot), fullPage: true });
    audit.viewports[key] = { scrollWidth: m.scrollWidth, clientWidth: m.clientWidth, overflow_ok, screenshot: shot };
    console.log(`${key}px: scrollWidth=${m.scrollWidth} clientWidth=${m.clientWidth} overflow_ok=${overflow_ok}`);
    await page.close();
  }
  fs.writeFileSync(path.join(dir, 'sources/render-audit.json'), JSON.stringify(audit, null, 2) + '\n');
  await browser.close();
  console.log('render-audit.json written');
})();
