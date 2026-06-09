#!/usr/bin/env node
import fs from 'node:fs';
import fsp from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { parseArgs } from 'node:util';
import { createHash } from 'node:crypto';
import { spawnSync } from 'node:child_process';
import { createRequire } from 'node:module';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
function discoverRepoRoot() {
  const scriptParent = path.resolve(__dirname, '..');
  if (fs.existsSync(path.join(scriptParent, 'output'))) return scriptParent;
  if (fs.existsSync(path.join(process.cwd(), 'output'))) return process.cwd();
  return scriptParent;
}

const REPO_ROOT = discoverRepoRoot();
const OUTPUT_ROOT = path.join(REPO_ROOT, 'output');
const require = createRequire(import.meta.url);

const TIMEOUTS = { nav: 30000, networkidle: 3000, fonts: 5000, imageDecode: 5000 };
const DEFAULTS = {
  formats: ['pdf', 'png', 'webp'],
  themes: ['light', 'light2', 'white', 'dark', 'dark2', 'blue', 'skyblue', 'sepia'],
  scale: 2,
  viewport: { width: 1280, height: 900 },
  webpQuality: 85,
  webpMaxEdge: 16383,
  pdfFormat: 'A4',
  pdfMargin: '12mm',
};
const RASTER_MAX = 16384;                 // scale downgrade threshold
const PNG_PIXEL_MAX = 300_000_000;          // hard safety guard for one full-page PNG
const VALID_FORMATS = new Set(['pdf', 'png', 'webp']);
const VALID_THEMES = new Set(['light', 'light2', 'white', 'dark', 'dark2', 'blue', 'skyblue', 'sepia']);
const VALID_SCALES = new Set([1, 2, 3]);
const CONTROL_HIDE = ['.ahf-themebar', '.reading-progress', '.skip', '.ahf-color-audit'];
const V2_FLAGS = [
  '--concurrency', '--pdf-media', '--pdf-themes', '--show-controls',
  '--offline', '--strict-fonts', '--webp-mode', '--pdf-format', '--pdf-margin',
  '--webp-quality', '--webp-max-edge',
];
const EXIT = { OK: 0, ARTIFACT_FAIL: 1, USAGE: 2, PRECONDITION: 3 };
const ERR = {
  RASTER: 'exceeds_raster_limit',
  INPUT_PX: 'input_pixel_limit',
  SHARP_NA: 'sharp_unavailable',
  NO_THEME: 'no_dom_radio',
  RENDER: 'render_failed',
  SHA: 'html_mutated',
  VALIDATE: 'validate_drift',
  NOT_IMPL: 'not_implemented_v1',
};
const SPEC = {
  formats: { type: 'string', default: DEFAULTS.formats.join(',') },
  themes: { type: 'string', default: DEFAULTS.themes.join(',') },
  scale: { type: 'string', default: String(DEFAULTS.scale) },
  viewport: { type: 'string', default: `${DEFAULTS.viewport.width}x${DEFAULTS.viewport.height}` },
  'require-webp': { type: 'boolean', default: false },
  clean: { type: 'boolean', default: false },
  help: { type: 'boolean', short: 'h', default: false },
};

class ExitError extends Error {
  constructor(message, code = EXIT.ARTIFACT_FAIL) {
    super(message);
    this.name = 'ExitError';
    this.code = code;
  }
}

function printHelp() {
  console.log(`Usage: node scripts/export_output.mjs <output_dir> [options]
  --formats <list>      pdf,png,webp (default: all)
  --themes <list>       light,light2,white,dark,dark2,blue,skyblue,sepia (DOM에 없는 테마는 skip)
  --scale <1|2|3>       PNG deviceScaleFactor request (default: 2)
  --viewport <WxH>      Chromium viewport (default: 1280x900)
  --require-webp        Treat sharp absence/webp failure as hard fail
  --clean               Safely remove requested export format directories first
  -h, --help            Show this help

V2 deferred flags intentionally rejected in v1: ${V2_FLAGS.join(', ')}
Examples:
  node scripts/export_output.mjs output/final_20260604
  node scripts/export_output.mjs output/final_20260604 --formats pdf,png --themes light,dark --scale 1`);
}

function parseList(raw, valid, label) {
  const list = String(raw)
    .split(',')
    .map((item) => item.trim())
    .filter(Boolean);
  if (list.length === 0) {
    throw new ExitError(`Invalid --${label}: empty list`, EXIT.USAGE);
  }
  const invalid = list.filter((item) => !valid.has(item));
  if (invalid.length > 0) {
    throw new ExitError(
      `Invalid --${label}: ${invalid.join(', ')}. Valid values: ${Array.from(valid).join(',')}`,
      EXIT.USAGE,
    );
  }
  return [...new Set(list)];
}

function parseCli(argv) {
  for (const arg of argv) {
    const flag = arg.includes('=') ? arg.slice(0, arg.indexOf('=')) : arg;
    if (V2_FLAGS.includes(flag)) {
      throw new ExitError(`${flag} is not implemented in v1 (deferred)`, EXIT.USAGE);
    }
  }

  let parsed;
  try {
    parsed = parseArgs({ args: argv, options: SPEC, allowPositionals: true, strict: true });
  } catch (error) {
    throw new ExitError(`${error.message}\nUse --help for usage.`, EXIT.USAGE);
  }

  if (parsed.values.help) {
    return { help: true };
  }

  const outputDirArg = parsed.positionals[0];
  if (!outputDirArg) {
    throw new ExitError('Missing <output_dir>. Use --help for usage.', EXIT.USAGE);
  }
  if (parsed.positionals.length > 1) {
    throw new ExitError(`Unexpected positional arguments: ${parsed.positionals.slice(1).join(' ')}`, EXIT.USAGE);
  }

  const formats = parseList(parsed.values.formats, VALID_FORMATS, 'formats');
  const themes = parseList(parsed.values.themes, VALID_THEMES, 'themes');
  const scale = Number(parsed.values.scale);
  if (!Number.isInteger(scale) || !VALID_SCALES.has(scale)) {
    throw new ExitError('Invalid --scale. Use one of: 1,2,3', EXIT.USAGE);
  }

  const viewportMatch = /^([1-9]\d*)x([1-9]\d*)$/i.exec(String(parsed.values.viewport));
  if (!viewportMatch) {
    throw new ExitError('Invalid --viewport. Use format 1280x900', EXIT.USAGE);
  }
  const viewport = { width: Number(viewportMatch[1]), height: Number(viewportMatch[2]) };

  return {
    help: false,
    outputDirArg,
    formats,
    themes,
    scale,
    viewport,
    requireWebp: Boolean(parsed.values['require-webp']),
    clean: Boolean(parsed.values.clean),
    rawArgs: argv,
  };
}

async function realOutputDir(outputDirArg) {
  const abs = path.resolve(REPO_ROOT, outputDirArg);
  let stat;
  try {
    stat = await fsp.stat(abs);
  } catch {
    throw new ExitError(`Output directory not found: ${outputDirArg}`, EXIT.PRECONDITION);
  }
  if (!stat.isDirectory()) {
    throw new ExitError(`Output path is not a directory: ${outputDirArg}`, EXIT.PRECONDITION);
  }

  const [realDir, realOutputRoot] = await Promise.all([fsp.realpath(abs), fsp.realpath(OUTPUT_ROOT)]);
  assertInside(realDir, realOutputRoot, 'outputDir');
  return realDir;
}

function assertInside(childAbs, parentAbs, label = 'path') {
  const rel = path.relative(parentAbs, childAbs);
  if (rel === '' || (!rel.startsWith('..') && !path.isAbsolute(rel))) return;
  throw new ExitError(`${label} must stay inside ${parentAbs}: ${childAbs}`, EXIT.PRECONDITION);
}

async function collectPages(outputDir) {
  const pages = [];
  const addHtmlFiles = async (dir, prefix = '') => {
    let entries = [];
    try {
      entries = await fsp.readdir(dir, { withFileTypes: true });
    } catch (error) {
      if (error.code === 'ENOENT') return;
      throw error;
    }
    for (const entry of entries) {
      if (!entry.isFile()) continue;
      if (entry.name.startsWith('.')) continue;
      if (!entry.name.toLowerCase().endsWith('.html')) continue;
      const abs = path.join(dir, entry.name);
      const src = prefix ? `${prefix}/${entry.name}` : entry.name;
      const base = path.basename(entry.name, path.extname(entry.name));
      pages.push({
        src,
        abs,
        url: pathToFileURL(abs).href,
        slugBase: prefix === 'pages' ? `pages__${base}` : base,
      });
    }
  };

  await addHtmlFiles(outputDir);
  await addHtmlFiles(path.join(outputDir, 'pages'), 'pages');

  pages.sort((a, b) => {
    if (a.src === 'index.html') return -1;
    if (b.src === 'index.html') return 1;
    return a.src.localeCompare(b.src, 'en');
  });

  if (pages.length === 0) {
    throw new ExitError(`No HTML files found in ${outputDir} or ${path.join(outputDir, 'pages')}`, EXIT.PRECONDITION);
  }
  return pages;
}

async function cleanExports(outputDir, formats) {
  const exportsDir = path.join(outputDir, 'exports');
  await rejectSymlink(exportsDir, true);
  await fsp.mkdir(exportsDir, { recursive: true });
  for (const format of formats) {
    const target = path.join(exportsDir, format);
    assertInside(target, exportsDir, `exports/${format}`);
    await rejectSymlink(target, true);
    await fsp.rm(target, { recursive: true, force: true });
  }
}

async function rejectSymlink(target, allowMissing = false) {
  try {
    const stat = await fsp.lstat(target);
    if (stat.isSymbolicLink()) {
      throw new ExitError(`Refusing to operate on symlink: ${target}`, EXIT.PRECONDITION);
    }
  } catch (error) {
    if (error.code === 'ENOENT' && allowMissing) return;
    throw error;
  }
}

async function hashFile(abs) {
  const buffer = await fsp.readFile(abs);
  return createHash('sha256').update(buffer).digest('hex');
}

async function shaPages(pages) {
  const map = {};
  for (const page of pages) {
    map[page.src] = await hashFile(page.abs);
  }
  return map;
}

async function shaTree(root) {
  try {
    const stat = await fsp.stat(root);
    if (!stat.isDirectory()) return null;
  } catch {
    return null;
  }
  const out = {};
  const walk = async (dir) => {
    const entries = await fsp.readdir(dir, { withFileTypes: true });
    entries.sort((a, b) => a.name.localeCompare(b.name, 'en'));
    for (const entry of entries) {
      const abs = path.join(dir, entry.name);
      if (entry.isDirectory()) {
        await walk(abs);
      } else if (entry.isFile()) {
        const rel = path.relative(root, abs).split(path.sep).join('/');
        out[rel] = await hashFile(abs);
      }
    }
  };
  await walk(root);
  return out;
}

function sameJson(a, b) {
  return JSON.stringify(a) === JSON.stringify(b);
}

function runValidateJson(outputDir) {
  const sourcesDir = path.join(outputDir, 'sources');
  if (!fs.existsSync(sourcesDir)) {
    return { ran: false, ok: null, issues: null, warnings: null, reason: 'no_sources_dir' };
  }

  const validateScript = path.join(REPO_ROOT, 'skills/adaptive-html-final/scripts/validate_output.py');
  const skillDir = path.join(REPO_ROOT, 'skills/adaptive-html-final');
  const result = spawnSync(
    'python3',
    [validateScript, outputDir, '--skill-dir', skillDir, '--json'],
    { cwd: REPO_ROOT, encoding: 'utf8', maxBuffer: 32 * 1024 * 1024 },
  );
  const stdout = result.stdout || '';
  const stderr = result.stderr || '';
  let parsed = null;
  try {
    parsed = JSON.parse(stdout);
  } catch {
    return {
      ran: true,
      ok: false,
      exitCode: result.status ?? 1,
      issues: [{ type: 'validate_command_failed', message: 'Could not parse validate_output.py --json stdout' }],
      warnings: [],
      stdout,
      stderr,
    };
  }
  return {
    ran: true,
    ok: Boolean(parsed.ok),
    exitCode: result.status ?? 0,
    issues: parsed.issues || [],
    warnings: parsed.warnings || [],
    parsed,
    stdout,
    stderr,
  };
}

async function proveUnchanged(outputDir, pages, beforeHtml, beforeSources, beforeValidate) {
  const afterHtml = await shaPages(pages);
  const htmlUnchanged = sameJson(beforeHtml, afterHtml);
  const afterSources = beforeSources ? await shaTree(path.join(outputDir, 'sources')) : null;
  const sourcesUnchanged = beforeSources ? sameJson(beforeSources, afterSources) : null;
  const afterValidate = beforeValidate?.ran ? runValidateJson(outputDir) : { ran: false, ok: null, issues: null };
  const validateIssuesUnchanged = beforeValidate?.ran
    ? sameJson(beforeValidate.issues || [], afterValidate.issues || [])
    : null;
  return {
    ok: htmlUnchanged && sourcesUnchanged !== false && validateIssuesUnchanged !== false,
    html_sha256_unchanged: htmlUnchanged,
    sources_sha256_unchanged: sourcesUnchanged,
    validate_issues_unchanged: validateIssuesUnchanged,
    html_sha256_after: afterHtml,
    sources_sha256_after: afterSources,
    validate_after: compactValidate(afterValidate),
  };
}

function compactValidate(validate) {
  if (!validate) return null;
  return {
    ran: Boolean(validate.ran),
    ok: validate.ok,
    exitCode: validate.exitCode ?? null,
    issues: validate.issues ?? null,
    warnings: validate.warnings ?? null,
    reason: validate.reason ?? null,
  };
}

async function withBrowser(fn) {
  let playwright;
  try {
    playwright = await import('playwright');
  } catch (error) {
    throw new ExitError(`Playwright is not installed. Run npm install. (${error.message})`, EXIT.PRECONDITION);
  }

  let browser;
  try {
    browser = await playwright.chromium.launch({ headless: true });
  } catch (error) {
    throw new ExitError(`Could not launch Chromium via Playwright: ${error.message}`, EXIT.PRECONDITION);
  }

  const closeAndExit = async (signal) => {
    console.error(`Received ${signal}; closing Chromium...`);
    try {
      await browser.close();
    } finally {
      process.exit(EXIT.PRECONDITION);
    }
  };
  const onSigint = () => void closeAndExit('SIGINT');
  const onSigterm = () => void closeAndExit('SIGTERM');
  process.once('SIGINT', onSigint);
  process.once('SIGTERM', onSigterm);

  try {
    return await fn(browser);
  } finally {
    process.off('SIGINT', onSigint);
    process.off('SIGTERM', onSigterm);
    await browser.close().catch(() => {});
  }
}

async function newExportContext(browser, opts, scale = 1) {
  return browser.newContext({
    viewport: opts.viewport,
    deviceScaleFactor: scale,
    reducedMotion: 'reduce',
    colorScheme: 'light',
  });
}

async function gotoStable(page, url) {
  await page.goto(url, { waitUntil: 'load', timeout: TIMEOUTS.nav });
  await waitStable(page);
  await hideControls(page);
  await waitStable(page);
}

async function waitStable(page) {
  await page.waitForLoadState('networkidle', { timeout: TIMEOUTS.networkidle }).catch(() => {});

  await Promise.race([
    page.evaluate(async () => {
      if (document.fonts?.ready) {
        await document.fonts.ready.catch(() => {});
      }
      return true;
    }).catch(() => false),
    delay(TIMEOUTS.fonts, false),
  ]);

  await Promise.race([
    page.evaluate(async () => {
      const images = Array.from(document.images || []);
      await Promise.allSettled(images.map(async (img) => {
        if (!img.complete) {
          await new Promise((resolve) => {
            const done = () => resolve(true);
            img.addEventListener('load', done, { once: true });
            img.addEventListener('error', done, { once: true });
            setTimeout(done, 1000);
          });
        }
        if (typeof img.decode === 'function') {
          await img.decode().catch(() => {});
        }
      }));
      return true;
    }).catch(() => false),
    delay(TIMEOUTS.imageDecode, false),
  ]);

  await page.evaluate(() => new Promise((resolve) => requestAnimationFrame(() => requestAnimationFrame(resolve)))).catch(() => {});
  await page.evaluate(() => document.documentElement.getBoundingClientRect().height).catch(() => {});
}

function delay(ms, value = undefined) {
  return new Promise((resolve) => setTimeout(() => resolve(value), ms));
}

async function hideControls(page) {
  const selector = CONTROL_HIDE.join(',');
  const css = `${selector}{display:none!important;visibility:hidden!important;pointer-events:none!important;}`;
  await page.addStyleTag({ content: css }).catch(() => {});
}

async function measureScrollHeight(browser, pageMeta, opts) {
  const context = await newExportContext(browser, opts, 1);
  try {
    const page = await context.newPage();
    await gotoStable(page, pageMeta.url);
    const themes = await detectThemes(page, opts.themes);
    const signals = await collectPageSignals(page);
    const metrics = await getPageMetrics(page, 1);
    return { ...metrics, ...themes, ...signals };
  } finally {
    await context.close().catch(() => {});
  }
}

async function getPageMetrics(page, scale) {
  const base = await page.evaluate(() => {
    const doc = document.documentElement;
    const body = document.body;
    const width = Math.ceil(Math.max(
      doc?.scrollWidth || 0,
      body?.scrollWidth || 0,
      doc?.clientWidth || 0,
      window.innerWidth || 0,
    ));
    const height = Math.ceil(Math.max(
      doc?.scrollHeight || 0,
      body?.scrollHeight || 0,
      doc?.clientHeight || 0,
      window.innerHeight || 0,
    ));
    return { scroll_width: width, scroll_height: height };
  });
  const pixelWidth = Math.ceil(base.scroll_width * scale);
  const pixelHeight = Math.ceil(base.scroll_height * scale);
  const raw = pixelWidth * pixelHeight * 4;
  return {
    ...base,
    pixel_width: pixelWidth,
    pixel_height: pixelHeight,
    raw_rgba_bytes_estimate: raw,
    est_pipeline_peak_bytes_estimate: Math.round(raw * 2.5),
  };
}

async function detectThemes(page, candidates = DEFAULTS.themes) {
  return page.evaluate((themes) => {
    const present = themes.filter((theme) => Boolean(document.querySelector(`input[type="radio"][name="ahf-theme"]#ahf-${theme}`)));
    const allThemeRadios = Array.from(document.querySelectorAll('input[type="radio"][name="ahf-theme"]'))
      .map((radio) => radio.id?.replace(/^ahf-/, ''))
      .filter(Boolean);
    const cssText = Array.from(document.querySelectorAll('style'))
      .map((style) => style.textContent || '')
      .join('\n');
    let theme_selector_style = 'none';
    if (cssText.includes(':root:has(')) theme_selector_style = 'root-has';
    else if (cssText.includes('body:has(')) theme_selector_style = 'body-has';
    else if (allThemeRadios.length > 0) theme_selector_style = 'radio';
    return {
      themes_present: present,
      all_theme_radios: allThemeRadios,
      themes_skipped: themes.filter((theme) => !present.includes(theme)),
      theme_selector_style,
    };
  }, candidates);
}

async function collectPageSignals(page) {
  return page.evaluate(() => {
    const urls = new Set();
    const maybeAdd = (raw) => {
      if (!raw) return;
      const value = String(raw).trim().replace(/^['"]|['"]$/g, '');
      if (!/^https?:\/\//i.test(value)) return;
      if (/(font|fonts|googleapis|gstatic|jsdelivr|pretendard|noto|woff|woff2|ttf|otf)/i.test(value)) {
        urls.add(value);
      }
    };

    for (const link of Array.from(document.querySelectorAll('link[rel~="stylesheet"], link[rel~="preload"]'))) {
      maybeAdd(link.href);
    }
    const cssText = Array.from(document.querySelectorAll('style'))
      .map((style) => style.textContent || '')
      .join('\n');
    for (const match of cssText.matchAll(/@import\s+(?:url\()?['"]?([^'";)\s]+)['"]?\)?/gi)) {
      maybeAdd(match[1]);
    }
    for (const match of cssText.matchAll(/url\(['"]?([^)'"]+)['"]?\)/gi)) {
      maybeAdd(match[1]);
    }
    const external_font_requests = Array.from(urls).sort();
    return {
      external_font_requests,
      fonts_fallback: external_font_requests.length > 0 ? 'external-fonts-detected' : 'system-or-inline-fonts-only',
    };
  });
}

async function applyTheme(page, theme) {
  const ok = await page.evaluate((id) => {
    const radio = document.querySelector(`input[type="radio"][name="ahf-theme"]#ahf-${id}`);
    if (!radio) return false;
    radio.checked = true;
    return radio.checked === true;
  }, theme);
  if (!ok) return false;
  await waitStable(page);
  return true;
}

function chooseEffectiveScale(baseMetrics, requestedScale) {
  let scale = requestedScale;
  while (scale > 1 && (baseMetrics.scroll_width * scale > RASTER_MAX || baseMetrics.scroll_height * scale > RASTER_MAX)) {
    scale -= 1;
  }
  const pixelCount = baseMetrics.scroll_width * scale * baseMetrics.scroll_height * scale;
  const softRasterLimitExceeded = baseMetrics.scroll_width * scale > RASTER_MAX || baseMetrics.scroll_height * scale > RASTER_MAX;
  const exceeds = pixelCount > PNG_PIXEL_MAX;
  return {
    scale,
    scale_degraded: scale !== requestedScale,
    exceeds,
    soft_raster_limit_exceeded: softRasterLimitExceeded,
  };
}


function artifactFile(exportsDir, format, slugBase, theme = null) {
  const suffix = theme ? `__${theme}` : '';
  return path.join(exportsDir, format, `${slugBase}${suffix}.${format}`);
}

function relativeArtifactPath(outputDir, absPath) {
  return path.relative(path.join(outputDir, 'exports'), absPath).split(path.sep).join('/');
}

function tempFor(finalPath) {
  const ext = path.extname(finalPath);
  const stem = finalPath.slice(0, -ext.length);
  return `${stem}.part-${process.pid}-${Date.now()}-${Math.random().toString(16).slice(2)}${ext}`;
}

async function atomicArtifact(tmpPath, finalPath) {
  await fsp.mkdir(path.dirname(finalPath), { recursive: true });
  await fsp.rename(tmpPath, finalPath);
}

async function fileBytes(absPath) {
  const stat = await fsp.stat(absPath);
  return stat.size;
}

function failedArtifact(error, extra = {}) {
  return { status: 'failed', error, ...extra };
}

function skippedArtifact(skipped_reason, extra = {}) {
  return { status: 'skipped', skipped_reason, ...extra };
}

async function exportPngForPage(browser, pageMeta, outputDir, opts, pageRecord) {
  const artifacts = {};
  const exportsDir = path.join(outputDir, 'exports');
  const baseMeasure = await measureScrollHeight(browser, pageMeta, opts);
  const { scale, scale_degraded, exceeds, soft_raster_limit_exceeded } = chooseEffectiveScale(baseMeasure, opts.scale);
  const preflight = {
    scroll_width: baseMeasure.scroll_width,
    scroll_height: baseMeasure.scroll_height,
    scale_requested: opts.scale,
    scale_used: scale,
    scale_degraded,
    soft_raster_limit_exceeded,
    png_pixel_max: PNG_PIXEL_MAX,
    pixel_width: Math.ceil(baseMeasure.scroll_width * scale),
    pixel_height: Math.ceil(baseMeasure.scroll_height * scale),
    raw_rgba_bytes_estimate: Math.ceil(baseMeasure.scroll_width * scale) * Math.ceil(baseMeasure.scroll_height * scale) * 4,
  };
  preflight.est_pipeline_peak_bytes_estimate = Math.round(preflight.raw_rgba_bytes_estimate * 2.5);

  pageRecord.themes_present = baseMeasure.themes_present;
  pageRecord.themes_skipped = baseMeasure.themes_skipped;
  pageRecord.all_theme_radios = baseMeasure.all_theme_radios;
  pageRecord.theme_selector_style = baseMeasure.theme_selector_style;
  pageRecord.external_font_requests = baseMeasure.external_font_requests;
  pageRecord.fonts_fallback = baseMeasure.fonts_fallback;
  pageRecord.preflight = preflight;

  for (const skipped of baseMeasure.themes_skipped) {
    artifacts[skipped] = skippedArtifact(ERR.NO_THEME, { theme: skipped });
  }

  const captureThemes = baseMeasure.themes_present.length > 0 ? baseMeasure.themes_present : [null];
  if (exceeds) {
    for (const theme of captureThemes) {
      artifacts[theme || 'default'] = failedArtifact(ERR.RASTER, {
        theme,
        scale_requested: opts.scale,
        scale_used: scale,
        scale_degraded,
        width: preflight.pixel_width,
        height: preflight.pixel_height,
      });
    }
    return artifacts;
  }

  const context = await newExportContext(browser, opts, scale);
  try {
    const page = await context.newPage();
    await gotoStable(page, pageMeta.url);
    for (const theme of captureThemes) {
      const key = theme || 'default';
      try {
        if (theme) {
          const ok = await applyTheme(page, theme);
          if (!ok) {
            artifacts[key] = skippedArtifact(ERR.NO_THEME, { theme });
            continue;
          }
        }
        const finalPath = artifactFile(exportsDir, 'png', pageMeta.slugBase, theme);
        const tmpPath = tempFor(finalPath);
        await page.screenshot({ path: tmpPath, fullPage: true, animations: 'disabled' });
        await atomicArtifact(tmpPath, finalPath);
        artifacts[key] = {
          status: 'ok',
          path: relativeArtifactPath(outputDir, finalPath),
          bytes: await fileBytes(finalPath),
          width: preflight.pixel_width,
          height: preflight.pixel_height,
          theme,
          scale_requested: opts.scale,
          scale_used: scale,
          scale_degraded,
          raw_rgba_bytes_estimate: preflight.raw_rgba_bytes_estimate,
          est_pipeline_peak_bytes_estimate: preflight.est_pipeline_peak_bytes_estimate,
        };
      } catch (error) {
        artifacts[key] = failedArtifact(ERR.RENDER, { theme, message: error.message });
      }
    }
  } finally {
    await context.close().catch(() => {});
  }
  return artifacts;
}

async function exportPdf(browser, pageMeta, outputDir, opts) {
  const exportsDir = path.join(outputDir, 'exports');
  const finalPath = artifactFile(exportsDir, 'pdf', pageMeta.slugBase, null);
  const tmpPath = tempFor(finalPath);
  const context = await newExportContext(browser, opts, 1);
  try {
    const page = await context.newPage();
    await gotoStable(page, pageMeta.url);
    await page.emulateMedia({ media: 'print' });
    await waitStable(page);
    await page.pdf({
      path: tmpPath,
      printBackground: true,
      preferCSSPageSize: true,
      format: DEFAULTS.pdfFormat,
      margin: {
        top: DEFAULTS.pdfMargin,
        right: DEFAULTS.pdfMargin,
        bottom: DEFAULTS.pdfMargin,
        left: DEFAULTS.pdfMargin,
      },
    });
    await atomicArtifact(tmpPath, finalPath);
    return {
      status: 'ok',
      path: relativeArtifactPath(outputDir, finalPath),
      bytes: await fileBytes(finalPath),
      media: 'print',
      theme: null,
      format: DEFAULTS.pdfFormat,
      margin: DEFAULTS.pdfMargin,
    };
  } catch (error) {
    await fsp.rm(tmpPath, { force: true }).catch(() => {});
    return failedArtifact(ERR.RENDER, { media: 'print', theme: null, message: error.message });
  } finally {
    await context.close().catch(() => {});
  }
}

async function loadSharp() {
  try {
    const mod = await import('sharp');
    const sharp = mod.default || mod;
    if (typeof sharp.concurrency === 'function') sharp.concurrency(1);
    if (typeof sharp.cache === 'function') sharp.cache(false);
    return sharp;
  } catch {
    return null;
  }
}

async function exportWebpFromPng(sharp, outputDir, pngArtifact, webpPath) {
  if (!pngArtifact || pngArtifact.status !== 'ok') {
    return skippedArtifact('png_source_unavailable', { source_status: pngArtifact?.status || null });
  }

  const pngPath = path.join(outputDir, 'exports', pngArtifact.path);
  const tmpPath = tempFor(webpPath);
  try {
    const input = sharp(pngPath, { limitInputPixels: false, sequentialRead: true });
    const metadata = await input.metadata();
    const sourceWidth = metadata.width || pngArtifact.width || 0;
    const sourceHeight = metadata.height || pngArtifact.height || 0;
    const maxEdge = Math.max(sourceWidth, sourceHeight);
    const downscaled = maxEdge > DEFAULTS.webpMaxEdge;
    const ratio = downscaled ? DEFAULTS.webpMaxEdge / maxEdge : 1;

    let pipeline = sharp(pngPath, { limitInputPixels: false, sequentialRead: true });
    if (downscaled) {
      pipeline = pipeline.resize({
        width: DEFAULTS.webpMaxEdge,
        height: DEFAULTS.webpMaxEdge,
        fit: 'inside',
        withoutEnlargement: true,
        kernel: 'lanczos3',
      });
    }
    if (typeof pipeline.withIccProfile === 'function') {
      pipeline = pipeline.withIccProfile('srgb');
    } else if (typeof pipeline.withMetadata === 'function') {
      pipeline = pipeline.withMetadata();
    }
    pipeline = pipeline.webp({
      quality: DEFAULTS.webpQuality,
      smartSubsample: true,
      effort: 6,
      alphaQuality: 100,
    });

    await fsp.mkdir(path.dirname(webpPath), { recursive: true });
    await pipeline.toFile(tmpPath);
    const outputMeta = await sharp(tmpPath, { limitInputPixels: false, sequentialRead: true }).metadata();
    await atomicArtifact(tmpPath, webpPath);
    return {
      status: 'ok',
      path: relativeArtifactPath(outputDir, webpPath),
      bytes: await fileBytes(webpPath),
      source_path: pngArtifact.path,
      source_width: sourceWidth,
      source_height: sourceHeight,
      output_width: outputMeta.width || Math.round(sourceWidth * ratio),
      output_height: outputMeta.height || Math.round(sourceHeight * ratio),
      webp_quality: DEFAULTS.webpQuality,
      webp_mode: downscaled ? 'downscaled' : 'full',
      webp_downscaled: downscaled,
      webp_downscale_ratio: Number(ratio.toFixed(3)),
      theme: pngArtifact.theme,
    };
  } catch (error) {
    await fsp.rm(tmpPath, { force: true }).catch(() => {});
    const type = /pixel|limitInputPixels|Input image exceeds/i.test(error.message) ? ERR.INPUT_PX : ERR.RENDER;
    return failedArtifact(type, { source_path: pngArtifact.path, message: error.message, theme: pngArtifact.theme });
  }
}

async function exportWebpForPage(sharp, pageRecord, outputDir, opts) {
  const webpArtifacts = {};
  const exportsDir = path.join(outputDir, 'exports');
  const pngArtifacts = pageRecord.artifacts.png || {};
  if (!sharp) {
    for (const [theme, pngArtifact] of Object.entries(pngArtifacts)) {
      if (pngArtifact.status === 'ok') {
        webpArtifacts[theme] = skippedArtifact(ERR.SHARP_NA, { source_path: pngArtifact.path, theme: pngArtifact.theme });
      } else if (pngArtifact.status === 'skipped') {
        webpArtifacts[theme] = skippedArtifact(pngArtifact.skipped_reason, { theme: pngArtifact.theme });
      } else {
        webpArtifacts[theme] = skippedArtifact('png_source_unavailable', { source_status: pngArtifact.status, theme: pngArtifact.theme });
      }
    }
    return webpArtifacts;
  }

  for (const [theme, pngArtifact] of Object.entries(pngArtifacts)) {
    if (pngArtifact.status !== 'ok') {
      webpArtifacts[theme] = pngArtifact.status === 'skipped'
        ? skippedArtifact(pngArtifact.skipped_reason, { theme: pngArtifact.theme })
        : skippedArtifact('png_source_unavailable', { source_status: pngArtifact.status, theme: pngArtifact.theme });
      continue;
    }
    const webpPath = artifactFile(exportsDir, 'webp', pageRecord.slugBase, pngArtifact.theme);
    webpArtifacts[theme] = await exportWebpFromPng(sharp, outputDir, pngArtifact, webpPath);
  }
  return webpArtifacts;
}

function getPackageVersion(name) {
  try {
    return require(`${name}/package.json`).version;
  } catch {
    return null;
  }
}

async function writeManifestAtomic(outputDir, manifest) {
  const exportsDir = path.join(outputDir, 'exports');
  await fsp.mkdir(exportsDir, { recursive: true });
  const finalPath = path.join(exportsDir, 'export-manifest.json');
  const tmpPath = tempFor(finalPath);
  await fsp.writeFile(tmpPath, `${JSON.stringify(manifest, null, 2)}\n`, 'utf8');
  await atomicArtifact(tmpPath, finalPath);
}

function summarize(manifest) {
  const counts = { ok: 0, failed: 0, skipped: 0 };
  for (const page of manifest.pages) {
    for (const artifact of page.artifacts.pdf || []) {
      if (artifact.status in counts) counts[artifact.status] += 1;
    }
    for (const group of ['png', 'webp']) {
      for (const artifact of Object.values(page.artifacts[group] || {})) {
        if (artifact.status in counts) counts[artifact.status] += 1;
      }
    }
  }
  manifest.summary = counts;
  return counts;
}

function hasRequiredFailures(manifest, opts) {
  let failed = false;
  let webpProblem = false;

  if (manifest.html_sha256_unchanged === false || manifest.sources_sha256_unchanged === false || manifest.validate_issues_unchanged === false) {
    failed = true;
  }

  for (const page of manifest.pages) {
    for (const artifact of page.artifacts.pdf || []) {
      if (artifact.status === 'failed' && opts.formats.includes('pdf')) failed = true;
    }
    for (const artifact of Object.values(page.artifacts.png || {})) {
      if (artifact.status === 'failed' && (opts.formats.includes('png') || opts.formats.includes('webp'))) failed = true;
    }
    for (const artifact of Object.values(page.artifacts.webp || {})) {
      if (artifact.status === 'failed' || artifact.status === 'skipped') webpProblem = true;
    }
  }

  if (opts.requireWebp && opts.formats.includes('webp') && webpProblem) failed = true;
  return failed;
}

async function buildManifestBase(outputDir, pages, opts, browserVersion, beforeHtml, beforeSources, beforeValidate) {
  return {
    generated_at: new Date().toISOString(),
    tool: 'scripts/export_output.mjs',
    tool_version: '0.1.0',
    node_version: process.version,
    playwright_version: getPackageVersion('playwright'),
    chromium_version: browserVersion,
    sharp_version: getPackageVersion('sharp'),
    input_dir: path.relative(REPO_ROOT, outputDir).split(path.sep).join('/'),
    command_args: opts.rawArgs,
    html_count: pages.length,
    html_sha256_before: beforeHtml,
    sources_sha256_before: beforeSources,
    validate_before: compactValidate(beforeValidate),
    html_sha256_unchanged: null,
    sources_sha256_unchanged: null,
    validate_issues_unchanged: null,
    formats_requested: opts.formats,
    themes_requested: opts.themes,
    viewport: opts.viewport,
    scale: opts.scale,
    concurrency: 1,
    pdf: { media: 'print', format: DEFAULTS.pdfFormat, margin: DEFAULTS.pdfMargin },
    webp: { quality: DEFAULTS.webpQuality, max_edge: DEFAULTS.webpMaxEdge, mode: 'downscale' },
    summary: { ok: 0, failed: 0, skipped: 0 },
    pages: pages.map((page) => ({
      src: page.src,
      slugBase: page.slugBase,
      url: page.url,
      html_sha256_before: beforeHtml[page.src],
      html_sha256_after: null,
      themes_present: [],
      themes_skipped: [],
      all_theme_radios: [],
      theme_selector_style: null,
      external_font_requests: [],
      fonts_fallback: null,
      preflight: null,
      artifacts: { pdf: [], png: {}, webp: {} },
      errors: [],
    })),
  };
}

async function runExport(opts) {
  const outputDir = await realOutputDir(opts.outputDirArg);
  if (opts.clean) {
    await cleanExports(outputDir, opts.formats);
  }
  const pages = await collectPages(outputDir);
  const beforeHtml = await shaPages(pages);
  const beforeSources = await shaTree(path.join(outputDir, 'sources'));
  const beforeValidate = runValidateJson(outputDir);
  let manifest;

  const sharp = opts.formats.includes('webp') ? await loadSharp() : null;

  await withBrowser(async (browser) => {
    manifest = await buildManifestBase(outputDir, pages, opts, browser.version(), beforeHtml, beforeSources, beforeValidate);
    for (let i = 0; i < pages.length; i += 1) {
      const pageMeta = pages[i];
      const pageRecord = manifest.pages[i];
      try {
        if (opts.formats.includes('pdf')) {
          pageRecord.artifacts.pdf.push(await exportPdf(browser, pageMeta, outputDir, opts));
        }
        if (opts.formats.includes('png') || opts.formats.includes('webp')) {
          pageRecord.artifacts.png = await exportPngForPage(browser, pageMeta, outputDir, opts, pageRecord);
        }
        if (opts.formats.includes('webp')) {
          pageRecord.artifacts.webp = await exportWebpForPage(sharp, pageRecord, outputDir, opts);
        }
      } catch (error) {
        pageRecord.errors.push({ error: ERR.RENDER, message: error.message });
      }
    }
  });

  const proof = await proveUnchanged(outputDir, pages, beforeHtml, beforeSources, beforeValidate);
  manifest.html_sha256_unchanged = proof.html_sha256_unchanged;
  manifest.sources_sha256_unchanged = proof.sources_sha256_unchanged;
  manifest.validate_issues_unchanged = proof.validate_issues_unchanged;
  manifest.sources_sha256_after = proof.sources_sha256_after;
  manifest.validate_after = proof.validate_after;
  for (const pageRecord of manifest.pages) {
    pageRecord.html_sha256_after = proof.html_sha256_after[pageRecord.src];
  }
  if (!proof.html_sha256_unchanged) manifest.pages[0]?.errors.push({ error: ERR.SHA, message: 'HTML SHA changed during export' });
  if (proof.validate_issues_unchanged === false) manifest.pages[0]?.errors.push({ error: ERR.VALIDATE, message: 'validate_output.py issues changed during export' });

  summarize(manifest);
  await writeManifestAtomic(outputDir, manifest);

  const manifestPath = path.join(path.relative(REPO_ROOT, outputDir), 'exports/export-manifest.json').split(path.sep).join('/');
  console.log(`Export manifest: ${manifestPath}`);
  console.log(`Summary: ok=${manifest.summary.ok} failed=${manifest.summary.failed} skipped=${manifest.summary.skipped}`);
  if (!sharp && opts.formats.includes('webp')) {
    console.warn(`Warning: sharp unavailable; webp artifacts skipped${opts.requireWebp ? ' (required)' : ''}.`);
  }

  return hasRequiredFailures(manifest, opts) ? EXIT.ARTIFACT_FAIL : EXIT.OK;
}

async function main() {
  let opts;
  try {
    opts = parseCli(process.argv.slice(2));
    if (opts.help) {
      printHelp();
      return EXIT.OK;
    }
    return await runExport(opts);
  } catch (error) {
    if (error instanceof ExitError) {
      console.error(error.message);
      if (error.code === EXIT.USAGE) console.error('Use --help for usage.');
      return error.code;
    }
    console.error(error.stack || error.message);
    return EXIT.ARTIFACT_FAIL;
  }
}

const exitCode = await main();
process.exitCode = exitCode;
