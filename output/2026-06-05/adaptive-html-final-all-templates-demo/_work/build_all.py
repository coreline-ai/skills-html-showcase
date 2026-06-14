import hashlib,json,pathlib,re
SK=pathlib.Path("/Users/iriver/hwan/projects/html-skills-doc/skills/adaptive-html-final");A=SK/"assets"
OUT=pathlib.Path("/Users/iriver/hwan/projects/html-skills-doc/output/2026-06-05/adaptive-html-final-all-templates-demo")
CORE=['theme.css','components.css','visual-components.css','layouts.css','print.css']
EXTRA=['editorial-patterns.css','visual-html.css','widgets.css','body-icons.css','shape-visuals.css','workflow-visuals.css']
core={n:(A/n).read_text(encoding='utf-8') for n in CORE}
blob='\n'.join(core[n] for n in CORE);h=hashlib.sha256(blob.encode()).hexdigest()
extra='\n'.join((A/n).read_text(encoding='utf-8') for n in EXTRA)
dark=(A/'theme-dark.css').read_text(encoding='utf-8')
DEMOCSS=""".demo-toc{display:flex;flex-wrap:wrap;gap:8px;margin:18px 0 0}.demo-toc a{display:inline-flex;align-items:center;min-height:32px;padding:5px 12px;border:1px solid var(--line);border-radius:999px;background:var(--card);color:var(--ink-soft);font-size:12.5px;font-weight:700;text-decoration:none}.demo-toc a:hover{border-color:var(--accent);color:var(--accent)}
.tpl-demo{margin:22px 0;border:1px dashed var(--line);border-radius:14px;padding:14px 16px;background:var(--card)}
.tpl-label{display:inline-flex;align-items:center;gap:7px;font-family:var(--vt-mono,monospace);font-size:11.5px;font-weight:800;letter-spacing:.06em;text-transform:uppercase;color:var(--accent-2);margin:0 0 12px}.tpl-label::before{content:"";width:7px;height:7px;border-radius:2px;background:var(--accent)}
.icon-gallery{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:10px}.icon-cell{display:flex;align-items:center;gap:9px;border:1px solid var(--line);border-radius:11px;padding:10px 12px;background:var(--card)}.icon-cell b{font-size:12.5px;display:block}.icon-cell small{color:var(--ink-mute);font-size:11px}"""
def strip(html): return re.sub(r'^\s*<!--.*?-->\s*','',html,flags=re.S).strip()
def label(fn):
    s=fn.replace('.html','');m=re.match(r'(\d+)-(.+)',s);return (m.group(1)+' · '+m.group(2).replace('-',' ')) if m else s
def tdir(d): return [(p.name,strip(p.read_text(encoding='utf-8'))) for p in sorted((A/d).glob('*.html'))]
def tpls(items): return '\n'.join(f'<div class="tpl-demo"><div class="tpl-label">{label(fn)}</div>\n{html}\n</div>' for fn,html in items)
icons=json.load(open(A/"body-icons.json"));shapes=json.load(open(A/"shape-catalog.json"));flows=json.load(open(A/"workflow-catalog.json"))
icon_html='<div class="icon-gallery">'+''.join(f'<div class="icon-cell"><span class="body-icon">{it["svg"]}</span><span><b>{it["label"]}</b><small>{it["id"]}</small></span></div>' for it in icons)+'</div>'
shape_html='<div class="shape-grid">'+''.join(f'<figure class="shape-figure"><img class="shape-img" src="assets/shape-svgs/{s["id"]}.svg" alt="{s["label"]} 도형" width="8000" height="6000" loading="lazy"><figcaption>{s["label"]} · {s["id"]}</figcaption></figure>' for s in shapes)+'</div>'
flow_html='<div class="workflow-grid">'+''.join(f'<figure class="workflow-figure"><img class="workflow-img" src="assets/workflow-svgs/{w["id"]}.svg" alt="{w["label"]} 도판" width="8000" height="6000" loading="lazy"><figcaption>{w["label"]} · {w["id"]}</figcaption></figure>' for w in flows)+'</div>'
def section(num,anchor,title,inner): return f'<section id="{anchor}"><h2><span class="no">{num}</span>{title}</h2>\n{inner}\n</section>'
toggle='<fieldset class="ahf-themebar" aria-label="테마 선택"><input type="radio" name="ahf-theme" id="ahf-light" checked><label for="ahf-light">라이트</label><input type="radio" name="ahf-theme" id="ahf-white"><label for="ahf-white">화이트</label><input type="radio" name="ahf-theme" id="ahf-dark"><label for="ahf-dark">다크</label></fieldset>'
body=f"""{toggle}
<div class="reading-progress" aria-hidden="true"></div><a class="skip" href="#main">본문 바로가기</a>
<main id="main" class="page-wide layout-reference">
  <header class="header"><div class="kicker"><span class="kicker-text">Adaptive HTML Final · v5.1 · 전체 템플릿</span></div>
    <h1>전체 템플릿 데모 · 다크/화이트 테마</h1>
    <p class="sub">스킬의 모든 템플릿 시스템과 콜아웃/컴포넌트를 한 페이지에. 우상단 버튼 또는 OS 설정으로 다크/화이트 양방향 전환.</p>
    <div class="meta"><span>editorial 8</span><span>vt 21</span><span>widget 20</span><span>body-icon 32</span><span>shape 36</span><span>workflow 10</span></div>
    <nav class="demo-toc"><a href="#callouts">콜아웃</a><a href="#editorial">Editorial 8</a><a href="#vt">Visual HTML 21</a><a href="#widgets">위젯 20</a><a href="#icons">아이콘 32</a><a href="#shapes">Shape 36</a><a href="#flows">워크플로우 10</a></nav></header>
  {section(1,'callouts','콜아웃 & 컴포넌트','<div class="term"><p><strong>용어</strong> term.</p></div><div class="analogy"><p><strong>비유</strong> analogy.</p></div><div class="danger"><p><strong>주의</strong> danger.</p></div><div class="good"><p><strong>권장</strong> good.</p></div><div class="lede-note"><span class="label">Goal</span><p>lede-note.</p></div><blockquote class="pull-quote">pull-quote 인용.</blockquote><div class="table-scroll"><table class="tbl"><caption>표</caption><thead><tr><th scope="col">항목</th><th scope="col">상태</th></tr></thead><tbody><tr><th scope="row">예시</th><td><span class="status-pill">상태</span></td></tr></tbody></table></div><section class="try"><div class="label">CTA</div><h3>.try 다크 CTA</h3><p><span class="tag">alpha</span> <span class="tag">beta</span></p></section>')}
  {section(2,'editorial','Editorial 패턴 8종',tpls(tdir('editorial-pattern-templates')))}
  {section(3,'vt','Visual HTML 템플릿 21종 (vt-)',tpls(tdir('visual-html-templates')))}
  {section(4,'widgets','뷰 위젯 20종 (wg-)',tpls(tdir('widget-templates')))}
  {section(5,'icons','본문 아이콘 32종 (bi-)',icon_html)}
  {section(6,'shapes','Soft-shape 도형 36종',shape_html)}
  {section(7,'flows','워크플로우 도판 10종',flow_html)}
  <aside class="source-note"><div class="label">데모</div><p>adaptive-html-final v5.1 전체 템플릿 쇼케이스.</p></aside>
</main>"""
html=f"<!doctype html>\n<html lang=\"ko\">\n<head>\n<meta charset=\"utf-8\">\n<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n<title>전체 템플릿 데모 · 다크/화이트 · v5.1</title>\n<style>\n/* adaptive-html-final-core-css-sha256: {h} */\n{blob}\n{extra}\n/* theme-dark */\n{dark}\n{DEMOCSS}\n</style>\n</head>\n<body>\n{body}\n</body>\n</html>\n"
(OUT/"index.html").write_text(html,encoding='utf-8')
print("rebuilt",len(html)//1024,"KB")
