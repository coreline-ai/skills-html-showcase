// Render-audit capture: load index + all pages at 1280 and 390, measure horizontal overflow,
// screenshot each, and write sources/render-audit.json in the schema completion_check.py expects.
import { chromium } from 'playwright';
import fs from 'fs';
import path from 'path';

const OUT = path.resolve(path.dirname(new URL(import.meta.url).pathname), '..');
const pagesDir = path.join(OUT, 'pages');
const shotsRel = 'sources/screenshots';
const shotsDir = path.join(OUT, shotsRel);
fs.mkdirSync(shotsDir, { recursive: true });

const htmls = ['index.html', ...fs.readdirSync(pagesDir).filter(f => f.endsWith('.html')).sort().map(f => 'pages/' + f)];
const viewports = [{ w: 1280, h: 900 }, { w: 390, h: 844 }];

const browser = await chromium.launch();
const perViewport = {};
const perPage = [];

for (const vp of viewports) {
  perViewport[vp.w] = { overflow_ok: true, worst: null, worst_scrollWidth: 0 };
}

for (const rel of htmls) {
  const fileUrl = 'file://' + path.join(OUT, rel);
  const entry = { page: rel, viewports: {} };
  for (const vp of viewports) {
    const page = await browser.newPage({ viewport: { width: vp.w, height: vp.h } });
    await page.goto(fileUrl, { waitUntil: 'load' });
    const m = await page.evaluate(() => ({
      scrollWidth: Math.max(document.documentElement.scrollWidth, document.body ? document.body.scrollWidth : 0),
      clientWidth: document.documentElement.clientWidth,
    }));
    const ok = m.scrollWidth <= m.clientWidth + 1; // 1px tolerance
    entry.viewports[vp.w] = { ...m, overflow_ok: ok };
    if (!ok) {
      perViewport[vp.w].overflow_ok = false;
      console.log(`OVERFLOW ${rel} @${vp.w}: scrollWidth=${m.scrollWidth} clientWidth=${m.clientWidth}`);
    }
    if (m.scrollWidth > perViewport[vp.w].worst_scrollWidth) {
      perViewport[vp.w].worst_scrollWidth = m.scrollWidth;
      perViewport[vp.w].worst = rel;
    }
    // screenshot (full page)
    const base = rel.replace(/[\/]/g, '_').replace(/\.html$/, '');
    const shot = `${shotsRel}/${base}-${vp.w}.png`;
    await page.screenshot({ path: path.join(OUT, shot), fullPage: true, animations: 'disabled' });
    await page.close();
  }
  perPage.push(entry);
}
await browser.close();

// Top-level render-audit.json (schema for completion_check.py): representative = index.html
const idx = perPage.find(p => p.page === 'index.html');
const audit = {
  generated_for: 'adaptive-html-final 17-mode independent build',
  representative: 'index.html',
  viewports: {
    '1280': {
      scrollWidth: idx.viewports[1280].scrollWidth,
      clientWidth: idx.viewports[1280].clientWidth,
      overflow_ok: perViewport[1280].overflow_ok,
      screenshot: `${shotsRel}/index-1280.png`,
    },
    '390': {
      scrollWidth: idx.viewports[390].scrollWidth,
      clientWidth: idx.viewports[390].clientWidth,
      overflow_ok: perViewport[390].overflow_ok,
      screenshot: `${shotsRel}/index-390.png`,
    },
  },
  all_pages_overflow_ok: { '1280': perViewport[1280].overflow_ok, '390': perViewport[390].overflow_ok },
  per_page: perPage,
};
fs.writeFileSync(path.join(OUT, 'sources/render-audit.json'), JSON.stringify(audit, null, 2) + '\n');
console.log(`render-audit written. 1280 ok=${perViewport[1280].overflow_ok} | 390 ok=${perViewport[390].overflow_ok} | shots=${htmls.length * 2}`);
