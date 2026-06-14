import { chromium } from 'playwright';
import fs from 'node:fs/promises';
import path from 'node:path';
import { pathToFileURL } from 'node:url';

const target = process.argv[2];
if (!target) { console.error('usage: node scripts/render_audit_fulltest.mjs <output_dir>'); process.exit(2); }
const root = path.resolve(target);
const shotDir = path.join(root, 'sources', 'screenshots');
await fs.mkdir(shotDir, { recursive: true });
const files = [path.join(root, 'index.html')];
const pagesDir = path.join(root, 'pages');
for (const name of (await fs.readdir(pagesDir)).filter(n => n.endsWith('.html')).sort()) files.push(path.join(pagesDir, name));
const browser = await chromium.launch({ headless: true });
const audit = { generated_at: new Date().toISOString(), viewports: {}, pages: {} };
for (const width of [1280, 390]) {
  let allOk = true, maxScroll = 0, maxClient = 0;
  for (const f of files) {
    const page = await browser.newPage({ viewport: { width, height: 900 }, deviceScaleFactor: 1 });
    await page.emulateMedia({ reducedMotion: 'reduce' });
    await page.goto(pathToFileURL(f).href, { waitUntil: 'load' });
    await page.locator('body').waitFor({ state: 'visible', timeout: 5000 }).catch(() => {});
    const dims = await page.evaluate(() => ({
      scrollWidth: document.scrollingElement.scrollWidth,
      clientWidth: document.documentElement.clientWidth,
      scrollHeight: document.scrollingElement.scrollHeight,
      title: document.title
    }));
    const ok = dims.scrollWidth <= dims.clientWidth + 1;
    allOk &&= ok; maxScroll = Math.max(maxScroll, dims.scrollWidth); maxClient = Math.max(maxClient, dims.clientWidth);
    const rel = path.relative(root, f);
    const key = rel.replace(/[^a-zA-Z0-9가-힣_-]+/g, '_').replace(/^_+|_+$/g, '');
    const shotName = rel === 'index.html' ? `${width}.png` : `${key}_${width}.png`;
    await page.screenshot({ path: path.join(shotDir, shotName), fullPage: true });
    audit.pages[rel] ??= {};
    audit.pages[rel][String(width)] = { ...dims, overflow_ok: ok, screenshot: `sources/screenshots/${shotName}` };
    await page.close();
  }
  audit.viewports[String(width)] = { scrollWidth: maxScroll, clientWidth: maxClient || width, overflow_ok: allOk, screenshot: `sources/screenshots/${width}.png` };
}
await browser.close();
await fs.writeFile(path.join(root, 'sources', 'render-audit.json'), JSON.stringify(audit, null, 2));
console.log(JSON.stringify({ target: root, pages: files.length, viewports: audit.viewports }, null, 2));
