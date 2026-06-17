#!/usr/bin/env node
import fs from 'node:fs/promises';
import path from 'node:path';
import { pathToFileURL } from 'node:url';
import { chromium } from 'playwright';

const repo = path.resolve(path.dirname(new URL(import.meta.url).pathname), '..');
const outputRoot = path.join(repo, 'output', '2026-06-13', 'codex-5.10.3');
const indexPath = path.join(outputRoot, 'index.html');
const outDir = path.join(outputRoot, 'readme-captures', 'sepia');
const viewport = { width: 1280, height: 900 };
const clip = { x: 0, y: 0, width: 1280, height: 720 };

const html = await fs.readFile(indexPath, 'utf8');
const cardPattern = /<article class="card">([\s\S]*?)<\/article>/g;
const cards = [];
let match;
while ((match = cardPattern.exec(html))) {
  const card = match[1];
  const num = card.match(/<span class="num">([^<]+)<\/span>/)?.[1]?.trim();
  const mode = card.match(/<span class="mode">([^<]+)<\/span>/)?.[1]?.trim();
  const title = card.match(/<h2>([\s\S]*?)<\/h2>/)?.[1]?.replace(/<[^>]+>/g, '').replace(/\s+/g, ' ').trim();
  const href = card.match(/<a class="open" href="([^"]+)"/)?.[1]?.trim();
  if (num && mode && title && href?.endsWith('/index.html')) {
    cards.push({ num, mode, title, href });
  }
}

if (cards.length !== 17) {
  throw new Error(`Expected 17 linked mode cards, found ${cards.length}`);
}

await fs.mkdir(outDir, { recursive: true });

const browser = await chromium.launch({ headless: true });
const context = await browser.newContext({ viewport, deviceScaleFactor: 1, reducedMotion: 'reduce' });
const page = await context.newPage();
page.setDefaultTimeout(15000);

const manifest = [];
for (const card of cards) {
  const dirName = path.dirname(card.href);
  const htmlPath = path.join(outputRoot, card.href);
  await fs.access(htmlPath);
  const url = pathToFileURL(htmlPath).href;
  await page.goto(url, { waitUntil: 'load' });
  await page.evaluate(() => {
    const input = document.querySelector('#ahf-sepia');
    if (!input) throw new Error('Missing #ahf-sepia');
    for (const radio of document.querySelectorAll('input[name="ahf-theme"]')) radio.checked = false;
    input.checked = true;
    input.dispatchEvent(new Event('input', { bubbles: true }));
    input.dispatchEvent(new Event('change', { bubbles: true }));
  });
  await page.evaluate(async () => {
    window.scrollTo(0, 0);
    if (document.fonts?.ready) await document.fonts.ready;
    await new Promise((resolve) => requestAnimationFrame(() => requestAnimationFrame(resolve)));
  });
  const outName = `${dirName}.jpg`;
  const outPath = path.join(outDir, outName);
  await page.screenshot({ path: outPath, type: 'jpeg', quality: 86, clip });
  manifest.push({
    no: card.num,
    mode: card.mode,
    title: card.title,
    html: `${dirName}/index.html`,
    capture: `readme-captures/sepia/${outName}`,
    theme: 'sepia',
    viewport,
    clip,
  });
  console.log(`${manifest.length.toString().padStart(2, '0')}/17 ${outName}`);
}

await browser.close();
await fs.writeFile(
  path.join(outDir, 'capture-manifest.json'),
  JSON.stringify({ generated_at: new Date().toISOString(), theme: 'sepia', viewport, clip, count: manifest.length, captures: manifest }, null, 2) + '\n',
  'utf8',
);
console.log(`Wrote ${manifest.length} captures to ${path.relative(repo, outDir)}`);
