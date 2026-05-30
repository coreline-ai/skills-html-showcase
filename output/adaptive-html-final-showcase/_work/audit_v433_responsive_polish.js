const { chromium } = require('playwright');
const fs = require('fs/promises');
const path = require('path');

const BASE = 'http://127.0.0.1:8778';
const OUT = path.resolve('output/adaptive-html-final-showcase-v3/qa-screenshots/v433-responsive-polish');
const pages = [
  ['index', '/index.html'],
  ['01-beginner', '/pages/01-beginner-passkeys-webauthn.html'],
  ['02-expert', '/pages/02-expert-eu-ai-act-governance.html'],
  ['03-article', '/pages/03-article-ai-agent-ux-trust.html'],
  ['04-education', '/pages/04-education-github-actions-security-ci.html'],
  ['05-blog', '/pages/05-blog-local-ai-workstation.html'],
  ['06-seo', '/pages/06-seo-rag-vs-finetuning.html'],
  ['07-platform', '/pages/07-platform-rag-post-platforms.html'],
  ['08-audit', '/pages/08-skill-audit-adaptive-html-final.html'],
  ['09-reference', '/pages/09-reference-openai-responses-api.html'],
  ['10-comparison', '/pages/10-comparison-postgresql-mysql-sqlite.html'],
  ['11-case', '/pages/11-case-cloudflare-thanksgiving-incident.html'],
  ['12-landing', '/pages/12-landing-ai-knowledge-hub.html'],
  ['13-checklist', '/pages/13-checklist-web-accessibility-release.html'],
  ['14-visual', '/pages/14-visual-template-system.html'],
  ['15-gallery', '/pages/15-svg-template-gallery.html'],
];

const viewports = [
  ['desktop', { width: 1440, height: 1200, deviceScaleFactor: 1 }],
  ['mobile390', { width: 390, height: 1200, isMobile: true, deviceScaleFactor: 2 }],
];

function slug(s){ return s.replace(/[^a-z0-9-]+/gi, '-').replace(/^-|-$/g, '').toLowerCase(); }

(async () => {
  await fs.mkdir(OUT, { recursive: true });
  const browser = await chromium.launch({ headless: true });
  const results = [];
  for (const [label, rel] of pages) {
    for (const [vpLabel, viewport] of viewports) {
      const page = await browser.newPage({ viewport });
      const url = BASE + rel;
      const errors = [];
      page.on('pageerror', e => errors.push(String(e)));
      page.on('console', msg => { if (msg.type() === 'error') errors.push(msg.text()); });
      const response = await page.goto(url, { waitUntil: 'networkidle', timeout: 20000 });
      await page.evaluate(() => document.fonts && document.fonts.ready ? document.fonts.ready : Promise.resolve()).catch(() => {});
      await page.waitForTimeout(250);
      const file = `${slug(label)}-${vpLabel}.png`;
      await page.screenshot({ path: path.join(OUT, file), fullPage: true, animations: 'disabled' });
      const metrics = await page.evaluate(({ label, vpLabel }) => {
        const rgba = (value) => {
          const m = String(value || '').match(/rgba?\(([^)]+)\)/);
          if (!m) return null;
          const p = m[1].split(',').map(v => Number(v.trim()));
          return { r:p[0]||0, g:p[1]||0, b:p[2]||0, a:p.length>3 ? p[3] : 1, raw:value };
        };
        const lum = ({r,g,b}) => {
          const f = v => { v /= 255; return v <= .03928 ? v/12.92 : Math.pow((v+.055)/1.055, 2.4); };
          return .2126*f(r)+.7152*f(g)+.0722*f(b);
        };
        const ratio = (c1,c2) => {
          if (!c1 || !c2) return null;
          const [a,b] = [lum(c1), lum(c2)].sort((x,y)=>y-x);
          return Math.round(((a+.05)/(b+.05))*100)/100;
        };
        const bgFor = (el) => {
          let n = el;
          while (n && n.nodeType === 1) {
            const bg = rgba(getComputedStyle(n).backgroundColor);
            if (bg && bg.a > .05) return bg;
            n = n.parentElement;
          }
          return rgba(getComputedStyle(document.body).backgroundColor) || {r:255,g:255,b:255,a:1,raw:'fallback'};
        };
        const textContrast = (sel) => {
          const el = document.querySelector(sel);
          if (!el) return null;
          const cs = getComputedStyle(el);
          const fg = rgba(cs.color);
          const bg = bgFor(el);
          const rect = el.getBoundingClientRect();
          return { selector: sel, color: fg?.raw, background: bg?.raw, ratio: ratio(fg,bg), text: (el.textContent||'').trim().slice(0,80), fontSize: cs.fontSize, fontWeight: cs.fontWeight, rect: {x:Math.round(rect.x),y:Math.round(rect.y),w:Math.round(rect.width),h:Math.round(rect.height)} };
        };
        const rects = sel => Array.from(document.querySelectorAll(sel)).map(el => {
          const r = el.getBoundingClientRect();
          return { x:Math.round(r.x), y:Math.round(r.y), w:Math.round(r.width), h:Math.round(r.height), text:(el.textContent||'').trim().slice(0,70) };
        });
        const main = document.querySelector('main');
        const tables = Array.from(document.querySelectorAll('table')).map((t, i) => ({
          i,
          caption: !!t.querySelector('caption'),
          captionText: (t.querySelector('caption')?.textContent || '').trim(),
          wrapperClass: t.closest('.tbl')?.className || '',
          firstDataLabel: t.querySelector('tbody td')?.getAttribute('data-label') || '',
        }));
        const execCards = rects('.executive-summary .card-grid > *');
        const execXs = [...new Set(execCards.map(r => r.x))];
        const grid = document.querySelector('.platform-grid');
        const roadmap = document.querySelector('section#roadmap.priority-roadmap');
        const timelineItems = rects('.timeline-card > li');
        return {
          label, vpLabel,
          title: document.title,
          h1: (document.querySelector('h1')?.textContent || '').trim(),
          scrollWidth: document.documentElement.scrollWidth,
          bodyScrollWidth: document.body.scrollWidth,
          innerWidth,
          overflowX: document.documentElement.scrollWidth > innerWidth + 1,
          mainClass: main?.className || '',
          sectionPlatformGridCount: document.querySelectorAll('section.platform-grid').length,
          platformGridParent: grid ? { tag: grid.parentElement.tagName, className: grid.parentElement.className, id: grid.parentElement.id } : null,
          tables,
          missingCaptionCount: tables.filter(t => !t.caption).length,
          desktopExecutiveSummaryColumns: execXs.length || null,
          executiveSummaryCards: execCards,
          roadmapIsDirectSection: !!roadmap && roadmap.parentElement === main,
          timelineItemCount: timelineItems.length,
          timelineItems,
          checks: {
            darkCtaLink: textContrast('.try.soft-cta a, .try a'),
            serpTitle: textContrast('.serp-title'),
            landingNextAction: textContrast('.try .cta-box p, .try .cta-box li, .try .cta-box'),
            h2Sub: textContrast('.h2-sub'),
          },
          blogCounter: (() => {
            const el = document.querySelector('.layout-blog article > section > h2');
            if (!el) return null;
            return getComputedStyle(el, '::before').content;
          })(),
          errors: [],
        };
      }, { label, vpLabel });
      const pass = [];
      const fail = [];
      if (!response || !response.ok()) fail.push(`HTTP ${response ? response.status() : 'no response'}`); else pass.push('HTTP OK');
      if (metrics.overflowX) fail.push(`horizontal overflow ${metrics.scrollWidth}/${metrics.innerWidth}`); else pass.push('no horizontal overflow');
      if (metrics.sectionPlatformGridCount) fail.push('section.platform-grid present');
      if (metrics.missingCaptionCount) fail.push(`${metrics.missingCaptionCount} table(s) missing caption`);
      if (label === '02-expert' && vpLabel === 'desktop' && metrics.desktopExecutiveSummaryColumns !== 2) fail.push(`executive summary columns=${metrics.desktopExecutiveSummaryColumns}`);
      if (label === '05-blog' && metrics.checks.darkCtaLink && metrics.checks.darkCtaLink.ratio < 4.5) fail.push(`dark CTA link ratio ${metrics.checks.darkCtaLink.ratio}`);
      if (label === '05-blog' && metrics.blogCounter && !/1/.test(metrics.blogCounter)) fail.push(`blog counter unexpected ${metrics.blogCounter}`);
      if (label === '07-platform' && (!metrics.platformGridParent || metrics.platformGridParent.tag !== 'SECTION' || metrics.platformGridParent.className !== 'platform-cards-section')) fail.push(`platform grid parent unexpected ${JSON.stringify(metrics.platformGridParent)}`);
      if (label === '08-audit' && !metrics.roadmapIsDirectSection) fail.push('roadmap section is not direct main child');
      if (label === '11-case' && metrics.timelineItemCount < 4) fail.push(`timeline step cards too few ${metrics.timelineItemCount}`);
      if (label === '12-landing' && metrics.checks.landingNextAction && metrics.checks.landingNextAction.ratio < 4.5) fail.push(`landing next-action ratio ${metrics.checks.landingNextAction.ratio}`);
      for (const t of metrics.tables) {
        if (vpLabel === 'mobile390' && t.wrapperClass.includes('mobile-card-table') && !t.firstDataLabel) fail.push(`mobile card table ${t.i} missing data-label`);
      }
      if (errors.length) fail.push(`console/page errors: ${errors.length}`);
      results.push({ label, rel, vpLabel, file, url, pass, fail, metrics, errors });
      await page.close();
    }
  }
  await browser.close();
  const report = { generatedAt: new Date().toISOString(), base: BASE, total: results.length, failed: results.filter(r => r.fail.length).length, results };
  await fs.writeFile(path.join(OUT, 'audit-report.json'), JSON.stringify(report, null, 2));

  const failures = results.filter(r => r.fail.length);
  const cards = results.map(r => `<article class="card ${r.fail.length ? 'fail' : 'pass'}"><a href="${r.file}"><img src="${r.file}" alt="${r.label} ${r.vpLabel} screenshot"></a><div><b>${r.label} · ${r.vpLabel}</b><p>${r.metrics.h1}</p><p>${r.fail.length ? 'FAIL: ' + r.fail.join(' · ') : 'PASS: ' + r.pass.slice(0,2).join(' · ')}</p></div></article>`).join('\n');
  const html = `<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>v4.3.3 QA Screenshots</title><style>body{font-family:-apple-system,BlinkMacSystemFont,'Pretendard',sans-serif;background:#f7f5ef;color:#20201d;margin:0;padding:28px}.wrap{max-width:1240px;margin:auto}.summary{background:#fff;border:1px solid #ddd8cb;border-left:5px solid ${failures.length?'#d64545':'#2b8a64'};border-radius:14px;padding:22px;margin-bottom:22px}.grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:16px}.card{background:#fff;border:1px solid #ddd8cb;border-radius:14px;overflow:hidden}.card img{display:block;width:100%;height:280px;object-fit:cover;object-position:top;border-bottom:1px solid #ddd8cb}.card div{padding:14px}.card p{margin:7px 0;color:#5c5b55;font-size:14px}.pass{box-shadow:0 0 0 3px rgba(43,138,100,.08)}.fail{box-shadow:0 0 0 3px rgba(214,69,69,.15)}a{color:#c63e52;font-weight:800}@media(max-width:760px){body{padding:14px}.grid{grid-template-columns:1fr}.card img{height:220px}}</style></head><body><main class="wrap"><section class="summary"><h1>adaptive-html-final v4.3.3 QA Screenshots</h1><p>총 ${results.length}개 캡쳐 · 실패 ${failures.length}개 · 기준: 1440px desktop + 390px mobile.</p><p><a href="audit-report.json">JSON 리포트 보기</a> · <a href="../../index.html">쇼케이스 홈</a></p></section><section class="grid">${cards}</section></main></body></html>`;
  await fs.writeFile(path.join(OUT, 'index.html'), html);
  console.log(JSON.stringify({ out: OUT, total: results.length, failed: failures.length, failures: failures.map(f => ({ label:f.label, viewport:f.vpLabel, fail:f.fail })) }, null, 2));
})();
