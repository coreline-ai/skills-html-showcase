#!/usr/bin/env node
/**
 * storm-research: report.json -> dist/<slug>/index.html (자체완결, 네트워크 무의존)
 *
 * 사용법:
 *   node build-report.mjs <report.json> [<output-root>]
 *   - output-root 기본값: 이 스크립트 기준 ../dist
 *   - 산출: <output-root>/<slug>/index.html  +  report.json 사본
 *
 * report.json 스키마: templates/report.schema.json 참조.
 */
import fs from 'node:fs';
import path from 'node:path';
import url from 'node:url';

const __dirname = path.dirname(url.fileURLToPath(import.meta.url));

// ---------- args ----------
const reportPath = process.argv[2];
if (!reportPath) { console.error('usage: node build-report.mjs <report.json> [output-root]'); process.exit(2); }
const outputRoot = process.argv[3] || path.resolve(__dirname, '..', 'dist');
const data = JSON.parse(fs.readFileSync(reportPath, 'utf8'));

// ---------- helpers ----------
const esc = (s='') => String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
const slugify = (s='') => String(s).toLowerCase()
  .replace(/[^\p{L}\p{N}]+/gu,'-').replace(/^-+|-+$/g,'').slice(0,60) || 'storm';

// 가벼운 마크다운 -> HTML (의존성 0). 표·인용·링크·리스트·코드·강조 지원.
function md(src='') {
  if (!src) return '';
  const lines = String(src).replace(/\r\n/g,'\n').split('\n');
  let out = [], i = 0;
  const inline = (t) => esc(t)
    .replace(/`([^`]+)`/g,'<code>$1</code>')
    .replace(/\*\*([^*]+)\*\*/g,'<strong>$1</strong>')
    .replace(/(?<!\*)\*(?!\*)([^*]+)\*/g,'<em>$1</em>')
    .replace(/\[([^\]]+)\]\((https?:\/\/[^\s)]+)\)/g,'<a href="$2" target="_blank" rel="noopener">$1</a>')
    // 대괄호 출처: [출처: http...] 형태도 링크화
    .replace(/\[(출처|source)\s*:\s*(https?:\/\/[^\]\s]+)([^\]]*)\]/gi,
      '<span class="cite">[$1: <a href="$2" target="_blank" rel="noopener">$2</a>$3]</span>')
    // 남은 bare URL
    .replace(/(?<!["=(>])(https?:\/\/[^\s<)]+)(?![^<]*<\/a>)/g,'<a href="$1" target="_blank" rel="noopener">$1</a>');

  while (i < lines.length) {
    let line = lines[i];

    if (/^\s*$/.test(line)) { i++; continue; }

    // heading
    let h = line.match(/^(#{1,6})\s+(.*)$/);
    if (h) { const lv = Math.min(h[1].length+2,6); out.push(`<h${lv}>${inline(h[2])}</h${lv}>`); i++; continue; }

    // hr
    if (/^\s*([-*_])\1{2,}\s*$/.test(line)) { out.push('<hr/>'); i++; continue; }

    // blockquote (연속)
    if (/^\s*>\s?/.test(line)) {
      let buf=[]; while (i<lines.length && /^\s*>\s?/.test(lines[i])) { buf.push(lines[i].replace(/^\s*>\s?/,'')); i++; }
      out.push(`<blockquote>${md(buf.join('\n'))}</blockquote>`); continue;
    }

    // table (pipe) — 헤더 + 구분선 + 행
    if (/^\s*\|.*\|\s*$/.test(line) && i+1<lines.length && /^\s*\|?[\s:|-]+\|?\s*$/.test(lines[i+1])) {
      const row = (l)=> l.trim().replace(/^\||\|$/g,'').split('|').map(c=>c.trim());
      const head = row(line); i+=2;
      let body=[]; while (i<lines.length && /^\s*\|.*\|\s*$/.test(lines[i])) { body.push(row(lines[i])); i++; }
      let t='<table><thead><tr>'+head.map(c=>`<th>${inline(c)}</th>`).join('')+'</tr></thead><tbody>';
      for (const r of body) t+='<tr>'+r.map(c=>`<td>${inline(c)}</td>`).join('')+'</tr>';
      t+='</tbody></table>'; out.push(t); continue;
    }

    // unordered list
    if (/^\s*[-*+]\s+/.test(line)) {
      let buf=[]; while (i<lines.length && /^\s*[-*+]\s+/.test(lines[i])) { buf.push(lines[i].replace(/^\s*[-*+]\s+/,'')); i++; }
      out.push('<ul>'+buf.map(b=>`<li>${inline(b)}</li>`).join('')+'</ul>'); continue;
    }
    // ordered list
    if (/^\s*\d+\.\s+/.test(line)) {
      let buf=[]; while (i<lines.length && /^\s*\d+\.\s+/.test(lines[i])) { buf.push(lines[i].replace(/^\s*\d+\.\s+/,'')); i++; }
      out.push('<ol>'+buf.map(b=>`<li>${inline(b)}</li>`).join('')+'</ol>'); continue;
    }

    // paragraph (연속 비빈 줄)
    let buf=[]; while (i<lines.length && !/^\s*$/.test(lines[i]) &&
      !/^(#{1,6})\s/.test(lines[i]) && !/^\s*>/.test(lines[i]) &&
      !/^\s*[-*+]\s/.test(lines[i]) && !/^\s*\d+\.\s/.test(lines[i]) &&
      !/^\s*\|.*\|\s*$/.test(lines[i])) { buf.push(lines[i]); i++; }
    out.push(`<p>${inline(buf.join(' '))}</p>`);
  }
  return out.join('\n');
}

// 모든 텍스트에서 URL 수집 (중복 제거)
function harvestUrls(...texts){
  const set=new Set();
  for (const t of texts) for (const m of String(t||'').matchAll(/https?:\/\/[^\s<)\]"']+/g)) set.add(m[0].replace(/[.,;]+$/,''));
  return [...set];
}

// ---------- data ----------
const topic = data.topic || '(제목 없음)';
const slug = data.slug || slugify(topic);
const genAt = data.generated_at || '';
const souls = data.souls || [];
const llmColor = { claude:'#C06A3B', codex:'#3B7A57', kimi:'#5A4FCF', opus:'#8A5CF6' };

const allSources = (data.all_sources && data.all_sources.length)
  ? data.all_sources
  : harvestUrls(
      ...souls.map(s=>s.markdown||''),
      data.synthesis||'', data.contradiction_map||'', data.peer_review||''
    );

const conf = data.confidence || {};

// ---------- HTML ----------
const soulCards = souls.map(s => {
  const color = llmColor[(s.llm||'').toLowerCase()] || '#666';
  return `
  <article class="soul" id="soul-${slugify(s.name)}">
    <header class="soul-h">
      <span class="soul-name">${esc(s.name)}</span>
      <span class="soul-persona">${esc(s.persona||'')}</span>
      <span class="llm-badge" style="--c:${color}">${esc(s.llm||'?')}</span>
    </header>
    ${s.summary ? `<p class="soul-sum">${esc(s.summary)}</p>` : ''}
    <div class="soul-body">${md(s.markdown||'_결과 없음_')}</div>
  </article>`;
}).join('\n');

const sourcesList = allSources.length
  ? '<ol class="refs">'+allSources.map(u=>`<li><a href="${esc(u)}" target="_blank" rel="noopener">${esc(u)}</a></li>`).join('')+'</ol>'
  : '<p class="muted">수집된 출처 없음.</p>';

const html = `<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>STORM · ${esc(topic)}</title>
<style>
:root{
  --bg:#fbfaf7; --fg:#1a1726; --muted:#6b6677; --line:#e7e3da;
  --accent:#3b4fd6; --accent2:#c0392b; --card:#ffffff; --ink:#0f0d18;
  --serif:"Iowan Old Style","Palatino Linotype",Palatino,Georgia,serif;
  --sans:-apple-system,BlinkMacSystemFont,"Segoe UI",Pretendard,"Apple SD Gothic Neo",sans-serif;
  --mono:"SF Mono",ui-monospace,Menlo,Consolas,monospace;
}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--fg);font-family:var(--sans);line-height:1.65;}
.wrap{max-width:880px;margin:0 auto;padding:0 24px 96px;}
header.top{padding:64px 0 28px;border-bottom:2px solid var(--ink);margin-bottom:8px;}
.kicker{font-family:var(--mono);font-size:12px;letter-spacing:.18em;text-transform:uppercase;color:var(--accent);}
h1{font-family:var(--serif);font-size:clamp(30px,5vw,46px);line-height:1.12;margin:.3em 0 .2em;letter-spacing:-.01em;}
.meta{font-family:var(--mono);font-size:12px;color:var(--muted);display:flex;gap:16px;flex-wrap:wrap;margin-top:10px;}
.meta b{color:var(--fg);font-weight:600;}
section{margin:52px 0;}
section > h2{font-family:var(--serif);font-size:26px;border-left:4px solid var(--accent);padding-left:14px;margin:0 0 18px;}
.lead{font-family:var(--serif);font-size:19px;color:#322e40;background:#fff;border:1px solid var(--line);border-radius:10px;padding:20px 24px;}
.toc{font-family:var(--mono);font-size:13px;display:flex;gap:8px 22px;flex-wrap:wrap;color:var(--muted);}
.toc a{color:var(--accent);text-decoration:none;}
.toc a:hover{text-decoration:underline;}
.soul{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:22px 24px;margin:16px 0;box-shadow:0 1px 0 rgba(0,0,0,.02);}
.soul-h{display:flex;align-items:baseline;gap:12px;flex-wrap:wrap;border-bottom:1px solid var(--line);padding-bottom:10px;margin-bottom:6px;}
.soul-name{font-family:var(--serif);font-size:20px;font-weight:700;}
.soul-persona{color:var(--muted);font-size:14px;}
.llm-badge{margin-left:auto;font-family:var(--mono);font-size:11px;text-transform:uppercase;letter-spacing:.08em;color:#fff;background:var(--c,#666);padding:3px 9px;border-radius:999px;}
.soul-sum{font-style:italic;color:#46414f;margin:.4em 0 .2em;}
.soul-body, .prose{font-size:15.5px;}
.cite{font-family:var(--mono);font-size:12px;color:var(--muted);}
.cite a{color:var(--accent);}
blockquote{border-left:3px solid var(--line);margin:1em 0;padding:.2em 1em;color:#4a4554;background:#faf8f4;}
table{border-collapse:collapse;width:100%;margin:1em 0;font-size:14px;}
th,td{border:1px solid var(--line);padding:8px 10px;text-align:left;vertical-align:top;}
th{background:#f4f1ea;font-family:var(--mono);font-size:12px;text-transform:uppercase;letter-spacing:.05em;}
code{font-family:var(--mono);font-size:.88em;background:#f1eee7;padding:1px 5px;border-radius:4px;}
a{color:var(--accent);}
hr{border:0;border-top:1px solid var(--line);margin:1.5em 0;}
.badges{display:flex;gap:10px;flex-wrap:wrap;margin:6px 0 16px;}
.badge{font-family:var(--mono);font-size:12px;border:1px solid var(--line);border-radius:8px;padding:8px 12px;background:#fff;}
.badge b{color:var(--accent);}
.verdict{font-family:var(--mono);font-size:13px;font-weight:600;padding:10px 14px;border-radius:8px;display:inline-block;}
.verdict.pass{background:#e8f3ec;color:#1d6b3f;border:1px solid #bcdcc8;}
.verdict.fail{background:#fbeae8;color:#a3271b;border:1px solid #e7c3bd;}
.refs{font-family:var(--mono);font-size:12.5px;line-height:1.9;color:var(--muted);word-break:break-all;}
.refs a{color:var(--accent);}
.muted{color:var(--muted);}
footer.prov{margin-top:64px;border-top:2px solid var(--ink);padding-top:20px;font-size:13px;color:var(--muted);}
footer.prov a{color:var(--accent);}
footer.prov .note{background:#fff;border:1px solid var(--line);border-radius:10px;padding:14px 18px;margin-top:12px;font-size:12.5px;line-height:1.7;}
</style>
</head>
<body>
<div class="wrap">
  <header class="top">
    <div class="kicker">STORM · Multi-Perspective Research</div>
    <h1>${esc(topic)}</h1>
    <div class="meta">
      ${genAt?`<span>생성 <b>${esc(genAt)}</b></span>`:''}
      <span>영혼 <b>${souls.length}</b></span>
      <span>출처 <b>${allSources.length}</b></span>
      <span>방법 <b>Stanford STORM (재해석)</b></span>
    </div>
  </header>

  <section>
    <div class="toc">
      <a href="#perspectives">① 다중 관점</a>
      <a href="#contradiction">② 모순 지도</a>
      <a href="#synthesis">③ 종합</a>
      <a href="#review">④ 동료 검토</a>
      <a href="#sources">⑤ 출처</a>
    </div>
  </section>

  <section id="perspectives">
    <h2>① 다중 관점 스캔 (5 영혼)</h2>
    ${soulCards || '<p class="muted">영혼 결과 없음.</p>'}
  </section>

  <section id="contradiction">
    <h2>② 모순 지도</h2>
    <div class="prose">${md(data.contradiction_map||'_모순 지도 없음_')}</div>
  </section>

  <section id="synthesis">
    <h2>③ 종합</h2>
    <div class="prose">${md(data.synthesis||'_종합 없음_')}</div>
  </section>

  <section id="review">
    <h2>④ 동료 검토 (Peer Review)</h2>
    <div class="badges">
      ${conf.source_diversity?`<span class="badge">출처 다양성 <b>${esc(conf.source_diversity)}</b></span>`:''}
      ${conf.citation?`<span class="badge">인용 충실도 <b>${esc(conf.citation)}</b></span>`:''}
      ${conf.honesty?`<span class="badge">확신 정직성 <b>${esc(conf.honesty)}</b></span>`:''}
    </div>
    ${conf.verdict?`<div class="verdict ${/통과|pass/i.test(conf.verdict)?'pass':'fail'}">${esc(conf.verdict)}</div>`:''}
    <div class="prose" style="margin-top:14px">${md(data.peer_review||'_검토 없음_')}</div>
  </section>

  <section id="sources">
    <h2>⑤ 통합 출처 (${allSources.length})</h2>
    ${sourcesList}
  </section>

  <footer class="prov">
    <div><b>출처 계보 / 정직성 고지</b></div>
    <div class="note">
      이 리포트는 Stanford <b>STORM</b> 방법론의 <b>재해석</b>이다 (재구현 아님).
      논문: <a href="https://arxiv.org/abs/2402.14207" target="_blank" rel="noopener">Shao et al., NAACL 2024</a> ·
      코드(MIT): <a href="https://github.com/stanford-oval/storm" target="_blank" rel="noopener">stanford-oval/storm</a> ·
      진짜 도구: <a href="https://storm.genie.stanford.edu" target="_blank" rel="noopener">storm.genie.stanford.edu</a>.<br/>
      논문 보고 수치는 <b>조직성 +25% / coverage +10%</b> (FreshWiki, outline-driven RAG 대비). "25% 더 똑똑"은 claim drift.<br/>
      생성: 5개 페르소나(영혼)를 claude/codex/kimi에 분산 → 딥리서치(출처 강제) → 모순 지도 → 종합 → 동료 검토.
    </div>
  </footer>
</div>
</body>
</html>`;

// ---------- write ----------
const outDir = path.join(outputRoot, slug);
fs.mkdirSync(outDir, { recursive: true });
const outHtml = path.join(outDir, 'index.html');
fs.writeFileSync(outHtml, html, 'utf8');
fs.writeFileSync(path.join(outDir, 'report.json'), JSON.stringify(data, null, 2), 'utf8');

console.log(outHtml);
console.error(`[build-report] wrote ${outHtml} (${(html.length/1024).toFixed(1)} KB, ${souls.length} souls, ${allSources.length} sources)`);
