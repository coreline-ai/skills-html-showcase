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
const microChecks = {
  heading_badge_nowrap: true,
  rail_color_variety: true,
  rail_text_padding: true,
  card_vertical_rhythm: true,
  footer_centered: true,
  no_noncanonical_classes: true
};
const microFailures = [];
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
    const micro = await page.evaluate(() => {
      const failures = [];
      const checks = {
        heading_badge_nowrap: true,
        rail_color_variety: true,
        rail_text_padding: true,
        card_vertical_rhythm: true,
        footer_centered: true,
        no_noncanonical_classes: true
      };

      const badClasses = Array.from(document.querySelectorAll('.template-card-head,.source-preserve-static'));
      if (badClasses.length) {
        checks.no_noncanonical_classes = false;
        failures.push(`noncanonical_classes:${badClasses.length}`);
      }

      const badges = Array.from(document.querySelectorAll('h2 .num, h2 .no'));
      for (const badge of badges) {
        const cs = getComputedStyle(badge);
        const r = badge.getBoundingClientRect();
        if (cs.whiteSpace !== 'nowrap' || r.height > 46) {
          checks.heading_badge_nowrap = false;
          failures.push(`heading_badge_nowrap:${badge.textContent.trim()}`);
          break;
        }
      }

      const railCandidates = Array.from(document.querySelectorAll([
        '.lede-note',
        '.source-note',
        '.summary-card',
        '.impact-card',
        '.chron-card',
        '.tl-item',
        '.vt-note',
        '.vt-panel',
        '.vt-card',
        '.cmp-card',
        '[class*="rail"]'
      ].join(',')));
      const railColors = [];
      for (const el of railCandidates) {
        const cs = getComputedStyle(el);
        const leftWidth = parseFloat(cs.borderLeftWidth || '0');
        if (leftWidth >= 3) {
          railColors.push(cs.borderLeftColor);
          const rect = el.getBoundingClientRect();
          const first = Array.from(el.children).find(child => child.getBoundingClientRect().width > 0);
          const textInset = first ? first.getBoundingClientRect().left - rect.left : parseFloat(cs.paddingLeft || '0');
          const padLeft = parseFloat(cs.paddingLeft || '0');
          if (Math.max(textInset, padLeft) < 14) {
            checks.rail_text_padding = false;
            failures.push(`rail_text_padding:${el.className}`);
            break;
          }
        }
      }
      const uniqueRailColors = new Set(railColors.filter(Boolean));
      if (railColors.length >= 4 && uniqueRailColors.size < 3) {
        checks.rail_color_variety = false;
        failures.push(`rail_color_variety:${uniqueRailColors.size}/${railColors.length}`);
      }

      const rhythmPairs = Array.from(document.querySelectorAll('.cmp-card .vt-kicker, .cmp-card .kicker, .vt-card .vt-kicker'));
      for (const kicker of rhythmPairs) {
        const next = kicker.nextElementSibling;
        if (!next) continue;
        const kr = kicker.getBoundingClientRect();
        const nr = next.getBoundingClientRect();
        const gap = nr.top - kr.bottom;
        if (gap < 6) {
          checks.card_vertical_rhythm = false;
          failures.push(`card_vertical_rhythm:${kicker.textContent.trim()}`);
          break;
        }
      }

      for (const footer of Array.from(document.querySelectorAll('body > footer.source-note, body > footer'))) {
        const r = footer.getBoundingClientRect();
        const vw = document.documentElement.clientWidth || window.innerWidth;
        if (r.left < 8 || r.right > vw - 8) {
          checks.footer_centered = false;
          failures.push(`footer_centered:${Math.round(r.left)}-${Math.round(r.right)}/${vw}`);
          break;
        }
      }

      return { checks, failures };
    });
    for (const [key, value] of Object.entries(micro.checks || {})) {
      if (value !== true) microChecks[key] = false;
    }
    for (const failure of micro.failures || []) {
      microFailures.push(`${path.relative(root, f)}@${width}:${failure}`);
    }
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
audit.micro_layout = {
  all_ok: Object.values(microChecks).every(Boolean),
  checks: microChecks,
  failures: microFailures
};
await fs.writeFile(path.join(root, 'sources', 'render-audit.json'), JSON.stringify(audit, null, 2));
console.log(JSON.stringify({ target: root, pages: files.length, viewports: audit.viewports }, null, 2));
