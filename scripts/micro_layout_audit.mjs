// micro_layout_audit.mjs — v5.10.6 시각결함 하드닝 render-audit 생산자 (G2·G3)
//
// 정적으로 못 잡는 render-only 결함을 Playwright로 측정해 render-audit.json의
// micro_layout.checks에 node_overlap_ok·inner_card_link_contrast_ok를 채운다.
// 검증기(completion_check.py)는 이 JSON만 읽고 Playwright를 직접 구동하지 않는다(무 JS 불변).
//
// usage:
//   node scripts/micro_layout_audit.mjs <output_dir|html_file> [--merge]
//   --merge : output_dir/sources/render-audit.json 의 micro_layout.checks 에 결과를 병합
//
// 측정:
//   G2 node_overlap_ok            : diagram 노드(.wg-04-node, [class*="-node"], figure svg <g>/<rect>) 박스 쌍이
//                                   임계(>4px×4px) 이상 겹치면 false.
//   G3 inner_card_link_contrast_ok: .try 내부 흰 카드(.box/.summary-card/.cta-box/.card-block/.mini-card) 링크의
//                                   렌더 색 대 유효 배경 대비가 AA(4.5:1, 대형 3:1) 미만이면 false.
import { chromium } from 'playwright';
import fs from 'node:fs/promises';
import path from 'node:path';
import { pathToFileURL } from 'node:url';

const targetArg = process.argv[2];
const doMerge = process.argv.includes('--merge');
if (!targetArg) {
  console.error('usage: node scripts/micro_layout_audit.mjs <output_dir|html_file> [--merge]');
  process.exit(2);
}
const target = path.resolve(targetArg);
const stat = await fs.stat(target);

// 측정 대상 페이지 수집
let files = [];
if (stat.isFile()) {
  files = [target];
} else {
  // index.html ∪ pages/*.html ∪ 형제 *.html 을 항상 합집합으로 수집(중복 제거).
  // 단일 페이지(index.html만 존재)는 1개 그대로, 다중 페이지 디렉터리는 전부 검사 → index만 검사하는 false-green 차단.
  const seen = new Set();
  const add = (p) => { if (!seen.has(p)) { seen.add(p); files.push(p); } };
  const idx = path.join(target, 'index.html');
  if (await fs.access(idx).then(() => true).catch(() => false)) add(idx);
  const pagesDir = path.join(target, 'pages');
  if (await fs.access(pagesDir).then(() => true).catch(() => false)) {
    for (const n of (await fs.readdir(pagesDir)).filter(n => n.endsWith('.html')).sort()) add(path.join(pagesDir, n));
  }
  for (const n of (await fs.readdir(target)).filter(n => n.endsWith('.html')).sort()) add(path.join(target, n));
}
console.error(`[micro-audit] ${files.length} page(s) to audit: ${files.map(f => path.basename(f)).join(', ')}`);

const OVERLAP_PX = 4; // 임계: 겹침 영역 변이 4px 초과면 결함

const browser = await chromium.launch({ headless: true });
const failures = [];
let nodeOverlapOk = true;
let contrastOk = true;

for (const f of files) {
  const page = await browser.newPage({ viewport: { width: 1280, height: 900 }, deviceScaleFactor: 1 });
  await page.emulateMedia({ reducedMotion: 'reduce' });
  await page.goto(pathToFileURL(f).href, { waitUntil: 'load' });

  // ── G2: diagram 노드 박스 겹침 ───────────────────────────────────────────
  const boxes = await page.$$eval(
    '.wg-04-node, [class*="-node"], figure svg g, figure svg rect',
    (els) => els
      .filter((e) => {
        const r = e.getBoundingClientRect();
        return r.width > 1 && r.height > 1;
      })
      .map((e) => {
        const r = e.getBoundingClientRect();
        return { x: r.x, y: r.y, w: r.width, h: r.height, tag: e.tagName.toLowerCase(), cls: e.getAttribute('class') || '' };
      })
  );
  for (let i = 0; i < boxes.length; i++) {
    for (let j = i + 1; j < boxes.length; j++) {
      const a = boxes[i], b = boxes[j];
      // 부모-자식(중첩 svg <g> 안의 <rect>)은 정상 포함이므로 제외: 한쪽이 다른쪽을 거의 완전히 포함하면 skip
      const ox = Math.max(0, Math.min(a.x + a.w, b.x + b.w) - Math.max(a.x, b.x));
      const oy = Math.max(0, Math.min(a.y + a.h, b.y + b.h) - Math.max(a.y, b.y));
      if (ox <= OVERLAP_PX || oy <= OVERLAP_PX) continue;
      const minArea = Math.min(a.w * a.h, b.w * b.h);
      const overlapArea = ox * oy;
      if (overlapArea >= 0.92 * minArea) continue; // containment(포함) — 결함 아님
      nodeOverlapOk = false;
      failures.push({ check: 'node_overlap_ok', file: path.basename(f), detail: `nodes overlap ${Math.round(ox)}x${Math.round(oy)}px (${a.cls || a.tag} ∩ ${b.cls || b.tag})` });
    }
  }

  // ── G3: .try 내부 흰 카드 링크 대비 ──────────────────────────────────────
  const links = await page.$$eval(
    '.try :is(.box,.summary-card,.cta-box,.card-block,.mini-card) a',
    (els) => els.map((a) => {
      const cs = getComputedStyle(a);
      let bg = 'rgba(0, 0, 0, 0)';
      let node = a;
      while (node) {
        const b = getComputedStyle(node).backgroundColor;
        if (b && b !== 'rgba(0, 0, 0, 0)' && b !== 'transparent') { bg = b; break; }
        node = node.parentElement;
      }
      const fs = parseFloat(cs.fontSize) || 16;
      const bold = (parseInt(cs.fontWeight, 10) || 400) >= 700;
      const large = fs >= 24 || (fs >= 18.66 && bold);
      return { color: cs.color, bg, large };
    })
  );
  const parse = (s) => {
    const m = s.match(/rgba?\(([^)]+)\)/);
    if (!m) return [0, 0, 0, 1];
    const p = m[1].split(',').map((x) => parseFloat(x.trim()));
    return [p[0] || 0, p[1] || 0, p[2] || 0, p[3] === undefined ? 1 : p[3]];
  };
  const lum = ([r, g, b]) => {
    const f = (v) => { v /= 255; return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); };
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b);
  };
  const ratio = (fg, bg) => {
    const [fr, fg_, fb, fa] = parse(fg);
    let [br, bgc, bb] = parse(bg);
    // 링크색에 알파가 있으면 배경 위로 합성
    const cr = fa * fr + (1 - fa) * br, cg = fa * fg_ + (1 - fa) * bgc, cb = fa * fb + (1 - fa) * bb;
    const l1 = lum([cr, cg, cb]), l2 = lum([br, bgc, bb]);
    const hi = Math.max(l1, l2), lo = Math.min(l1, l2);
    return (hi + 0.05) / (lo + 0.05);
  };
  for (const lk of links) {
    const r = ratio(lk.color, lk.bg);
    const min = lk.large ? 3.0 : 4.5;
    if (r < min) {
      contrastOk = false;
      failures.push({ check: 'inner_card_link_contrast_ok', file: path.basename(f), detail: `link ${lk.color} on ${lk.bg} = ${r.toFixed(2)}:1 < ${min}` });
    }
  }
  await page.close();
}
await browser.close();

const checks = { node_overlap_ok: nodeOverlapOk, inner_card_link_contrast_ok: contrastOk };
const result = { generated_at: new Date().toISOString(), pages: files.map((f) => path.basename(f)), micro_layout_checks: checks, failures };
console.log(JSON.stringify(result, null, 2));

if (doMerge && stat.isDirectory()) {
  const auditPath = path.join(target, 'sources', 'render-audit.json');
  let audit = {};
  try { audit = JSON.parse(await fs.readFile(auditPath, 'utf-8')); } catch { audit = {}; }
  audit.micro_layout = audit.micro_layout || { checks: {} };
  audit.micro_layout.checks = { ...(audit.micro_layout.checks || {}), ...checks };
  audit.micro_layout.all_ok = Object.values(audit.micro_layout.checks).every((v) => v === true);
  await fs.mkdir(path.dirname(auditPath), { recursive: true });
  await fs.writeFile(auditPath, JSON.stringify(audit, null, 2), 'utf-8');
  console.error(`merged micro_layout.checks → ${auditPath}`);
}

process.exit(failures.length ? 1 : 0);
