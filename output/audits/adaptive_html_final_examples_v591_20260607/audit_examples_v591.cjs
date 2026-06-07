const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
const root = '/Users/hwanchoi/project_202606/skills-html-showcase';
const examplesDir = path.join(root, 'skills/adaptive-html-final/examples');
const outDir = path.join(root, 'output/audits/adaptive_html_final_examples_v591_20260607');
const shotDir = path.join(outDir, 'screenshots');
fs.mkdirSync(shotDir, { recursive: true });
const manifest = JSON.parse(fs.readFileSync(path.join(root,'skills/adaptive-html-final/manifest.json'),'utf8'));
const files = manifest.examples.files.filter(f => f.endsWith('.html') && f !== 'index.html');
function esc(s){return String(s).replace(/[&<>"']/g, c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));}
(async()=>{
  const browser = await chromium.launch({ headless: true });
  const results=[];
  for (const file of files) {
    for (const vp of [{name:'desktop', width:1280, height:1600},{name:'mobile', width:390, height:1200}]) {
      const page = await browser.newPage({ viewport: { width: vp.width, height: vp.height }, deviceScaleFactor: 1 });
      const url = `http://localhost:8080/skills/adaptive-html-final/examples/${file}?v=v591-audit-${Date.now()}`;
      let status='PASS', error='';
      try {
        await page.goto(url, { waitUntil: 'networkidle', timeout: 20000 });
        await page.evaluate(async()=>{ if (document.fonts && document.fonts.ready) await document.fonts.ready; });
        const metrics = await page.evaluate(() => {
          const vw = document.documentElement.clientWidth;
          const docSW = Math.max(document.documentElement.scrollWidth, document.body.scrollWidth);
          const main = document.querySelector('main#main');
          const mainRect = main ? main.getBoundingClientRect() : null;
          const sectionIssues = [];
          if (main) {
            [...main.children].forEach((el, i) => {
              if (el.tagName !== 'SECTION') return;
              const r = el.getBoundingClientRect();
              const ratio = mainRect && mainRect.width ? r.width / mainRect.width : 1;
              const h2 = el.querySelector(':scope > h2');
              if (ratio < 0.92 && !el.classList.contains('try')) {
                sectionIssues.push({index:i+1, cls:el.className, width:Math.round(r.width), mainWidth:Math.round(mainRect.width), ratio:+ratio.toFixed(3), title:h2 ? h2.innerText.trim().slice(0,80) : '(h2 없음)'});
              }
            });
          }
          const overflow = [...document.body.querySelectorAll('*')].map((el) => {
            const r = el.getBoundingClientRect();
            if (r.width <= 1 || r.height <= 1) return null;
            if (r.right > vw + 2 || r.left < -2) {
              const cs = getComputedStyle(el);
              return {tag:el.tagName.toLowerCase(), cls:el.className ? String(el.className).slice(0,120) : '', left:Math.round(r.left), right:Math.round(r.right), width:Math.round(r.width), display:cs.display, text:(el.innerText||'').trim().slice(0,80)};
            }
            return null;
          }).filter(Boolean).slice(0,12);
          const wg10 = [...document.querySelectorAll('.mode-template-contract .wg-10-sheet')].map(el => {
            const r = el.getBoundingClientRect();
            const parent = el.closest('.mode-template-contract');
            const pr = parent ? parent.getBoundingClientRect() : null;
            return {width:Math.round(r.width), parentWidth:pr?Math.round(pr.width):null, ratio:pr && pr.width ? +(r.width/pr.width).toFixed(3) : null};
          });
          const directSections = main ? [...main.children].filter(el=>el.tagName==='SECTION').length : 0;
          const h2MissingIcons = main ? [...main.querySelectorAll(':scope > section > h2')].filter(h2=>!h2.querySelector('.body-icon')).map(h2=>h2.innerText.trim().slice(0,80)) : [];
          const last = main ? [...main.children].filter(el=>el.tagName==='SECTION').pop() : null;
          const lastText = last ? (last.innerText || '').trim().slice(0,160) : '';
          return { vw, docSW, overflowX: docSW - vw, mainWidth: mainRect?Math.round(mainRect.width):0, directSections, sectionIssues, overflow, wg10, h2MissingIcons, lastClass:last?last.className:'', lastText };
        });
        const issues=[];
        if (metrics.overflowX > 2) issues.push(`horizontal overflow ${metrics.overflowX}px`);
        if (metrics.sectionIssues.length) issues.push(`narrow direct sections ${metrics.sectionIssues.length}`);
        if (metrics.h2MissingIcons.length) issues.push(`direct h2 icon missing ${metrics.h2MissingIcons.length}`);
        for (const w of metrics.wg10) {
          if (vp.name === 'desktop' && w.ratio !== null && w.ratio < 0.88) issues.push(`wg10 not full-width ratio ${w.ratio}`);
        }
        if (issues.length) status='FAIL';
        const shotName = `${file.replace(/\.html$/,'')}__${vp.name}.png`;
        await page.screenshot({ path: path.join(shotDir, shotName), fullPage: true });
        results.push({file, viewport:vp.name, width:vp.width, height:vp.height, status, issues, metrics, screenshot:`screenshots/${shotName}`});
      } catch(e) {
        status='ERROR'; error=e.stack||String(e);
        results.push({file, viewport:vp.name, width:vp.width, height:vp.height, status, issues:[error], metrics:null, screenshot:null});
      } finally {
        await page.close();
      }
    }
  }
  await browser.close();
  const pass = results.filter(r=>r.status==='PASS').length;
  const fail = results.length - pass;
  fs.writeFileSync(path.join(outDir,'audit.json'), JSON.stringify({generatedAt:new Date().toISOString(), manifestVersion:manifest.version, total:results.length, pass, fail, results}, null, 2));
  const rows = results.map(r=>`<tr class="${r.status==='PASS'?'ok':'bad'}"><td>${esc(r.file)}</td><td>${r.viewport} ${r.width}px</td><td>${r.status}</td><td>${esc((r.issues||[]).join('; ') || 'OK')}</td><td>${r.metrics?esc('main '+r.metrics.mainWidth+' / sections '+r.metrics.directSections+' / overflow '+r.metrics.overflowX+' / wg10 '+JSON.stringify(r.metrics.wg10)):'-'}</td><td>${r.screenshot?`<a href="${esc(r.screenshot)}">PNG</a>`:''}</td></tr>`).join('\n');
  const html = `<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>adaptive-html-final examples v5.9.1 audit</title><style>body{font-family:system-ui,-apple-system,sans-serif;margin:24px;background:#f7f7f4;color:#202020}h1{font-size:26px}table{width:100%;border-collapse:collapse;background:white}th,td{border:1px solid #d8d8d0;padding:8px;vertical-align:top;font-size:13px}th{background:#eee}.ok td:nth-child(3){color:#137333;font-weight:800}.bad td:nth-child(3){color:#b3261e;font-weight:800}code{background:#eee;padding:2px 4px;border-radius:4px}.summary{display:flex;gap:12px;margin:16px 0}.card{background:#fff;border:1px solid #ddd;padding:12px 14px;border-radius:12px}</style></head><body><h1>adaptive-html-final examples v5.9.1 캡쳐 감사</h1><div class="summary"><div class="card"><b>Manifest</b><br>${esc(manifest.version)}</div><div class="card"><b>Total</b><br>${results.length}</div><div class="card"><b>PASS</b><br>${pass}</div><div class="card"><b>FAIL</b><br>${fail}</div></div><p>검사 기준: 16모드 × 1280/390px, 가로 오버플로, 직접 섹션 가로폭, h2 body-icon, v5.9.1 <code>.mode-template-contract .wg-10-sheet</code> full-width 적용 확인.</p><table><thead><tr><th>파일</th><th>뷰포트</th><th>상태</th><th>이슈</th><th>메트릭</th><th>캡쳐</th></tr></thead><tbody>${rows}</tbody></table></body></html>`;
  fs.writeFileSync(path.join(outDir,'REPORT.html'), html);
  console.log(JSON.stringify({outDir, total:results.length, pass, fail}, null, 2));
  if (fail) process.exit(1);
})();
