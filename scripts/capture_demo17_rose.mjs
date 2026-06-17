#!/usr/bin/env node
import fs from 'node:fs/promises';
import path from 'node:path';
import { pathToFileURL } from 'node:url';
import { chromium } from 'playwright';

const repo = path.resolve(path.dirname(new URL(import.meta.url).pathname), '..');
const demoRoot = path.join(repo, 'output', '2026-06-15', 'demo17');
const outDir = path.join(demoRoot, 'readme-captures', 'rose');
const viewport = { width: 1280, height: 900 };
const clip = { x: 0, y: 0, width: 1280, height: 720 };

function modeName(dirName) {
  return dirName.replace(/^\d+_/, '').replace(/_[^_]+(?:-[^_]+)*$/, '');
}

async function exists(p) {
  try { await fs.access(p); return true; } catch { return false; }
}

const entries = (await fs.readdir(demoRoot, { withFileTypes: true }))
  .filter((d) => d.isDirectory() && /^\d{2}_/.test(d.name))
  .map((d) => d.name)
  .sort();

if (entries.length !== 17) {
  throw new Error(`Expected 17 demo directories, found ${entries.length}`);
}

await fs.mkdir(outDir, { recursive: true });

const browser = await chromium.launch({ headless: true });
const context = await browser.newContext({ viewport, deviceScaleFactor: 1, reducedMotion: 'reduce' });
const page = await context.newPage();
page.setDefaultTimeout(15000);

const manifest = [];
for (const dir of entries) {
  const htmlPath = path.join(demoRoot, dir, 'index.html');
  if (!(await exists(htmlPath))) throw new Error(`Missing HTML: ${htmlPath}`);
  const url = pathToFileURL(htmlPath).href;
  await page.goto(url, { waitUntil: 'load' });
  await page.evaluate(() => {
    const input = document.querySelector('#ahf-dark2');
    if (!input) throw new Error('Missing #ahf-dark2');
    for (const radio of document.querySelectorAll('input[name=\"ahf-theme\"]')) radio.checked = false;
    input.checked = true;
    input.dispatchEvent(new Event('input', { bubbles: true }));
    input.dispatchEvent(new Event('change', { bubbles: true }));
  });
  await page.evaluate(async () => {
    window.scrollTo(0, 0);
    if (document.fonts?.ready) await document.fonts.ready;
    await new Promise((resolve) => requestAnimationFrame(() => requestAnimationFrame(resolve)));
  });
  const outName = `${dir}.jpg`;
  const outPath = path.join(outDir, outName);
  await page.screenshot({ path: outPath, type: 'jpeg', quality: 86, clip });
  manifest.push({
    mode_dir: dir,
    mode: modeName(dir),
    html: `${dir}/index.html`,
    capture: `readme-captures/rose/${outName}`,
    theme: 'dark2/rose',
    viewport,
    clip,
  });
  console.log(`${manifest.length.toString().padStart(2, '0')}/17 ${outName}`);
}

await browser.close();
await fs.writeFile(path.join(outDir, 'capture-manifest.json'), JSON.stringify({ generated_at: new Date().toISOString(), theme: 'dark2/rose', viewport, clip, count: manifest.length, captures: manifest }, null, 2) + '\n', 'utf8');
console.log(`Wrote ${manifest.length} captures to ${path.relative(repo, outDir)}`);
