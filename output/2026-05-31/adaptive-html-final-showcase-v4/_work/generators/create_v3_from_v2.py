from __future__ import annotations
from pathlib import Path
import hashlib, json, re, shutil
from html import escape

ROOT = Path('<repo-root>')
SKILL = ROOT / 'skills/adaptive-html-final'
SRC = ROOT / 'output/adaptive-html-final-showcase-v2'
OUT = ROOT / 'output/adaptive-html-final-showcase-v3'

if OUT.exists():
    shutil.rmtree(OUT)
shutil.copytree(SRC, OUT)
(OUT/'sources').mkdir(exist_ok=True)

# Sync current skill sources into output.
source_map = {
    'adaptive-html-final-SKILL.md': SKILL/'SKILL.md',
    'adaptive-html-final-manifest.json': SKILL/'manifest.json',
    'CHANGELOG.md': SKILL/'CHANGELOG.md',
    'quality-gates.md': SKILL/'references/quality-gates.md',
    'layout-system.md': SKILL/'references/layout-system.md',
    'visual-template-system.md': SKILL/'references/visual-template-system.md',
    'validate_output.py': SKILL/'scripts/validate_output.py',
}
for name, src in source_map.items():
    if src.exists():
        (OUT/'sources'/name).write_text(src.read_text(encoding='utf-8'), encoding='utf-8')

font_links = '''<link rel="preconnect" href="https://cdn.jsdelivr.net">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.css" rel="stylesheet">
<link href="https://fonts.googleapis.com/css2?family=Noto+Serif+KR:wght@400;600;700&display=swap" rel="stylesheet">'''

asset_names = ['theme.css','components.css','visual-components.css','layouts.css','print.css']
asset_texts = {name: (SKILL/'assets'/name).read_text(encoding='utf-8') for name in asset_names}
core_css = '\n'.join(asset_texts[name] for name in asset_names)
core_css_sha256 = hashlib.sha256(core_css.encode('utf-8')).hexdigest()
css_sources_dir = OUT/'sources'/'assets'
css_sources_dir.mkdir(parents=True, exist_ok=True)
for name, text_asset in asset_texts.items():
    (css_sources_dir/name).write_text(text_asset, encoding='utf-8')
(OUT/'sources'/'css-integrity.json').write_text(json.dumps({
    'core_css_sha256': core_css_sha256,
    'asset_order': asset_names,
    'asset_sha256': {name: hashlib.sha256(asset_texts[name].encode('utf-8')).hexdigest() for name in asset_names},
}, ensure_ascii=False, indent=2)+"\n", encoding='utf-8')
css = f'/* adaptive-html-final-core-css-sha256: {core_css_sha256} */\n' + core_css
css += r'''
/* ---- showcase v3 safety layer ---- */
a:focus-visible, summary:focus-visible, button:focus-visible{outline:3px solid var(--accent);outline-offset:3px;border-radius:4px}
@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}.hl{animation:none;background-size:100% 100%}}
.page-nav{display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:12px;margin:0 0 28px;font-size:13px;color:var(--ink-mute)}
.page-nav a{text-decoration:none;border-bottom:1px dotted var(--line)}
.page-nav a,.page-nav span{min-width:0;overflow-wrap:anywhere}
.source-list{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:8px 18px;margin:8px 0 0 18px;min-width:0}
.source-list li{font-size:13px;margin:3px 0;min-width:0}.source-list a{overflow-wrap:anywhere}
.status-pill{display:inline-flex;align-items:center;justify-content:center;border:1px solid var(--line);background:#fff;border-radius:999px;padding:4px 9px;font-size:12px;line-height:1.45;color:var(--ink-mute);margin:3px 4px 3px 0;text-align:center;white-space:normal}.tbl .status-pill,table .status-pill{white-space:nowrap;width:max-content;max-width:none;text-align:center;justify-content:center}
.audit-table{display:grid;gap:10px;margin:18px 0}.audit-row{display:grid;grid-template-columns:1fr 1.4fr .6fr;gap:10px;background:#fff;border:1px solid var(--line);border-radius:8px;padding:12px}.audit-row strong{display:block}
.timeline-card{background:#fff;border:1px solid var(--line);border-left:1px solid var(--line);border-radius:8px;padding:18px 22px 18px 40px;margin:12px 0;list-style-position:outside}.timeline-card>li{padding-left:4px;margin:12px 0}
.hero-index{background:#fff;border:1px solid var(--line);border-left:4px solid var(--accent);border-radius:12px;padding:26px;margin:20px 0 28px}
.page-list{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:14px}.page-list .mini-card a{text-decoration:none}.mode-label{font-size:11px;font-weight:800;letter-spacing:.12em;color:var(--accent);text-transform:uppercase}
.visual-demo{--max-wide:1120px}.visual-demo .visual-figure img{image-rendering:auto}
.gallery-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:18px;margin:24px 0}.gallery-card{background:var(--card);border:1px solid var(--line);border-radius:var(--radius-lg);overflow:hidden}.gallery-card .visual-figure{margin:0;border:0;border-radius:0;padding:12px}.gallery-card .visual-figure img{border-radius:8px}.gallery-card figcaption{font-size:12.5px}.gallery-body{padding:0 18px 18px}.gallery-body h3{margin:4px 0 6px;font-size:18px}.gallery-body p{font-size:14px}.gallery-body a{font-weight:800;color:var(--accent)}
@media(max-width:760px){.source-list,.page-list,.audit-row,.gallery-grid{grid-template-columns:1fr}.visual-demo{--max-wide:780px}.gallery-card .visual-figure{padding:10px}.timeline-card{padding:16px 14px 16px 34px}}
'''

STYLE_RE = re.compile(r'<style>.*?</style>', re.S)
FONT_RE = re.compile(r'(<link rel="preconnect" href="https://cdn\.jsdelivr\.net">.*?<link href="https://fonts\.googleapis\.com[^>]+>)', re.S)

def replace_style(html: str) -> str:
    # normalize font block enough for pages that already contain it
    html = STYLE_RE.sub('<style>\n' + css + '\n</style>', html)
    return html

def update_versions(html: str) -> str:
    html = html.replace('쇼케이스 (v2)', '쇼케이스 (v3)')
    html = html.replace('쇼케이스 (v2)', '쇼케이스 (v3)')
    html = html.replace('adaptive-html-final v4.2.0', 'adaptive-html-final v4.3.3')
    html = html.replace('adaptive-html-final v4.3.1', 'adaptive-html-final v4.3.3')
    html = html.replace('adaptive-html-final v4.3.2', 'adaptive-html-final v4.3.3')
    html = html.replace('Adaptive HTML Final Showcase · v4.2.0', 'Adaptive HTML Final Showcase · v4.3.3')
    html = html.replace('Adaptive HTML Final Showcase · v4.3.2', 'Adaptive HTML Final Showcase · v4.3.3')
    html = html.replace('스킬 버전 v4.2.0', '스킬 버전 v4.3.3')
    html = html.replace('스킬 버전 v4.3.2', '스킬 버전 v4.3.3')
    html = html.replace('Visual Template System v4.2.0', 'Visual Template System v4.3.3')
    html = html.replace('Visual Template System v4.3.1', 'Visual Template System v4.3.3')
    html = html.replace('Visual Template System v4.3.2', 'Visual Template System v4.3.3')
    html = html.replace('v4.3.1 Visual Template System', 'v4.3.3 Visual Template System')
    html = html.replace('v4.3.2 Visual Template System', 'v4.3.3 Visual Template System')
    html = html.replace('v4.2.0의 Visual Template System', 'v4.3.3의 Visual Template System')
    html = html.replace('v4.3.1의 Visual Template System', 'v4.3.3의 Visual Template System')
    html = html.replace('v4.3.2의 Visual Template System', 'v4.3.3의 Visual Template System')
    html = html.replace('v4.2.0의 <code>scripts/render_visual_svg.py</code>', 'v4.3.3의 <code>scripts/render_visual_svg.py</code>')
    html = html.replace('v4.3.1의 <code>scripts/render_visual_svg.py</code>', 'v4.3.3의 <code>scripts/render_visual_svg.py</code>')
    html = html.replace('v4.3.2의 <code>scripts/render_visual_svg.py</code>', 'v4.3.3의 <code>scripts/render_visual_svg.py</code>')
    html = html.replace('CHANGELOG.md — v4.2.0 Visual Template System', 'CHANGELOG.md — v4.3.3 Responsive Polish Gate')
    html = html.replace('CHANGELOG.md — v4.3.1 Design Polish Regression Gate', 'CHANGELOG.md — v4.3.3 Responsive Polish Gate')
    html = html.replace('CHANGELOG.md — v4.3.2 Blog/SEO Polish Gate', 'CHANGELOG.md — v4.3.3 Responsive Polish Gate')
    return html

def repair_known_html_typos(html: str) -> str:
    # Legacy generated pages may contain <p class="h2-sub">...</h2>, which the
    # browser auto-repairs unpredictably and can shift section rhythm.
    return re.sub(
        r'(<p\b[^>]*class=["\'][^"\']*\bh2-sub\b[^"\']*["\'][^>]*>(?:(?!</p>).)*?)</h2>',
        r'\1</p>',
        html,
        flags=re.I|re.S,
    )

def strip_tags(value: str) -> str:
    value = re.sub(r'<[^>]+>', '', value)
    return re.sub(r'\s+', ' ', value).strip()

def add_table_data_labels(html: str) -> str:
    def process_table(tm: re.Match) -> str:
        table = tm.group(0)
        header_row = re.search(r'<thead\b[^>]*>[\s\S]*?<tr\b[^>]*>([\s\S]*?)</tr>[\s\S]*?</thead>', table, re.I)
        if not header_row:
            header_row = re.search(r'<tr\b[^>]*>([\s\S]*?)</tr>', table, re.I)
        headers = []
        if header_row:
            headers = [strip_tags(c.group(2)) for c in re.finditer(r'<(th|td)\b[^>]*>([\s\S]*?)</\1>', header_row.group(1), re.I)]
        if not headers:
            return table
        def process_row(rm: re.Match) -> str:
            row = rm.group(0)
            idx = 0
            def cell_repl(cm: re.Match) -> str:
                nonlocal idx
                tag, attrs = cm.group(1), cm.group(2)
                label = headers[idx] if idx < len(headers) else ''
                idx += 1
                if 'data-label=' in attrs or not label:
                    return cm.group(0)
                return f'<{tag}{attrs} data-label="{escape(label)}">'
            return re.sub(r'<(td|th)\b([^>]*)>', cell_repl, row, flags=re.I)
        def tbody_repl(bm: re.Match) -> str:
            body = bm.group(0)
            return re.sub(r'<tr\b[^>]*>[\s\S]*?</tr>', process_row, body, flags=re.I)
        return re.sub(r'<tbody\b[^>]*>[\s\S]*?</tbody>', tbody_repl, table, flags=re.I)
    return re.sub(r'<table\b[^>]*>[\s\S]*?</table>', process_table, html, flags=re.I)

def apply_responsive_demo_patches(html: str, filename: str) -> str:
    if filename == '07-platform-rag-post-platforms.html':
        html = html.replace('<section class="platform-grid" id="s3">', '<section class="platform-cards-section" id="s3">')
        html = html.replace(
            '<p class="h2-sub">각 카드에 플랫폼별 추천 제목, 본문 구조, 태그를 정리했습니다. 그대로 발행 초안의 출발점으로 쓸 수 있습니다.</p>\n\n    <div class="platform-card">',
            '<p class="h2-sub">각 카드에 플랫폼별 추천 제목, 본문 구조, 태그를 정리했습니다. 그대로 발행 초안의 출발점으로 쓸 수 있습니다.</p>\n\n    <div class="platform-grid">\n    <div class="platform-card">',
        )
        html = html.replace(
            '\n  </section>\n\n  <section class="platform-comparison-table" id="s4">',
            '\n    </div>\n  </section>\n\n  <section class="platform-comparison-table" id="s4">',
            1,
        )
    if filename == '08-skill-audit-adaptive-html-final.html':
        html = html.replace(
            '    <h2 id="roadmap">5. 개선 권고</h2>',
            '  </section>\n\n  <section class="priority-roadmap" id="roadmap">\n    <h2>5. 개선 권고</h2>',
        )
    if filename == '12-landing-ai-knowledge-hub.html':
        html = html.replace(
            '      <table>\n        <thead>\n          <tr><th>단계</th><th>하는 일</th><th>누가 보나</th><th>결과</th></tr>',
            '      <table>\n        <caption>도구 승인 절차 요약</caption>\n        <thead>\n          <tr><th>단계</th><th>하는 일</th><th>누가 보나</th><th>결과</th></tr>',
        )
    if filename.startswith(('08-', '09-', '10-', '11-', '12-', '13-')):
        html = html.replace('<div class="tbl">', '<div class="tbl mobile-card-table">')
        html = add_table_data_labels(html)
    return html

# Update all existing HTML style and version wording.
for html_path in [OUT/'index.html'] + sorted((OUT/'pages').glob('*.html')):
    text = html_path.read_text(encoding='utf-8')
    text = repair_known_html_typos(update_versions(replace_style(text)))
    text = apply_responsive_demo_patches(text, html_path.name)
    # page14 image demo: use wide layout and eager/async loading for deterministic screenshots.
    if html_path.name == '14-visual-template-system.html':
        text = text.replace('<main id="main" class="page layout-article">', '<main id="main" class="page-wide layout-article visual-demo">')
        text = text.replace(' loading="lazy"', ' decoding="async"')
        text = text.replace('<a href="./13-checklist-web-accessibility-release.html">← 이전: 웹 접근성 배포 전 30분 체크리스트</a>\n    <span aria-hidden="true"> · </span>\n    <a href="../index.html">쇼케이스 홈</a>\n    <span aria-hidden="true"> · </span>\n    <span>추가 데모 (마지막)</span>', '<a href="./13-checklist-web-accessibility-release.html">← 이전: 웹 접근성 배포 전 30분 체크리스트</a>\n    <span aria-hidden="true"> · </span>\n    <a href="../index.html">쇼케이스 홈</a>\n    <span aria-hidden="true"> · </span>\n    <a href="./15-svg-template-gallery.html">다음: SVG 템플릿 20종 갤러리 →</a>')
    # Avoid stale caption class on table captions; component .caption is safe, but semantic caption does not need the class.
    text = text.replace('<caption class="caption">', '<caption>')
    html_path.write_text(text, encoding='utf-8')

# Rebuild page15 gallery using common CSS + visual figures.
def gallery_page() -> str:
    media_dir = OUT/'media/svg-template-demos'
    svgs = sorted(media_dir.glob('*.svg'))
    cards=[]
    for p in svgs:
        stem = p.stem
        title = re.sub(r'^\d+-', '', stem).replace('-', ' ').title().replace('Api', 'API')
        rel = f'../media/svg-template-demos/{p.name}'
        cards.append(f'''<article class="gallery-card">
  <figure class="visual-figure">
    <a href="{rel}"><img src="{rel}" width="8000" height="6000" decoding="async" alt="{escape(title)} 8000×6000 SVG 템플릿 미리보기"></a>
    <figcaption><strong>{escape(title)}</strong> — 8000×6000 SVG 원본 데모. 클릭하면 SVG를 직접 엽니다.</figcaption>
  </figure>
  <div class="gallery-body"><div class="mode-label">SVG TEMPLATE</div><h3><a href="{rel}">{escape(title)}</a></h3><p>섹션별 설명형 인포그래픽으로 재사용 가능한 벡터 템플릿입니다.</p></div>
</article>''')
    return f'''<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>SVG 템플릿 20종 데모 갤러리 · v3</title>
<meta name="description" content="adaptive-html-final v4.3.3 레이아웃 안전 규칙을 적용한 20가지 8000×6000 SVG 인포그래픽 템플릿 데모.">
<meta property="og:title" content="SVG 템플릿 20종 데모 갤러리 · v3">
<meta property="og:description" content="공통 CSS, visual-figure, figcaption, 8000×6000 SVG 규칙을 적용한 SVG 템플릿 갤러리.">
<meta property="og:type" content="article">
{font_links}
<style>
{css}
</style>
</head>
<body>
<a class="skip" href="#main">본문 바로가기</a>
<main id="main" class="page-wide layout-article visual-demo">
  <nav class="page-nav" aria-label="페이지 이동"><a href="./14-visual-template-system.html">← 이전: 섹션별 이미지 전략 데모</a><a href="../index.html">쇼케이스 홈</a></nav>
  <header class="header article-header">
    <div class="kicker">Additional Demo · v4.3.3 Safe Gallery</div>
    <h1>SVG 템플릿 20종 데모 갤러리</h1>
    <p class="sub">기존 10종과 추가 10종을 모두 공통 스킬 CSS와 <code>figure.visual-figure</code> 패턴으로 다시 배치했습니다. 모든 SVG는 8000×6000 원본입니다.</p>
    <div class="meta"><span>총 20개 SVG</span><span>원본 8000×6000</span><span>figcaption 적용</span><span>v3 layout-safe</span></div>
  </header>
  <section><h2><span class="num">1</span>템플릿 카드</h2><p class="h2-sub">클릭하면 각 SVG 원본을 직접 열 수 있습니다.</p><div class="gallery-grid">{''.join(cards)}</div></section>
  <section class="source-note"><div class="label">생성 및 검수 기준</div><p>v3에서는 독립 CSS를 제거하고 스킬 공통 CSS, visual figure 구조, 390px/1280px 렌더링 검증 기준을 적용했습니다.</p><ul class="source-list"><li><a href="../sources/visual-template-system.md">visual-template-system.md</a></li><li><a href="../sources/quality-gates.md">quality-gates.md</a></li><li><a href="../sources/validate_output.py">validate_output.py</a></li></ul></section>
</main>
</body>
</html>'''

(OUT/'pages/15-svg-template-gallery.html').write_text(gallery_page(), encoding='utf-8')

# Index polish and page15 discoverability.
idx = OUT/'index.html'
text = idx.read_text(encoding='utf-8')
text = text.replace('v4.2.0 Visual Template System', 'v4.3.3 Visual Template System')
text = text.replace('v4.3.1 Visual Template System', 'v4.3.3 Visual Template System')
text = text.replace('v4.3.2 Visual Template System', 'v4.3.3 Visual Template System')
text = text.replace('CHANGELOG.md (v4.0.0 → v4.2.0)', 'CHANGELOG.md (v4.0.0 → v4.3.3)')
text = text.replace('CHANGELOG.md (v4.0.0 → v4.3.1)', 'CHANGELOG.md (v4.0.0 → v4.3.3)')
text = text.replace('CHANGELOG.md (v4.0.0 → v4.3.2)', 'CHANGELOG.md (v4.0.0 → v4.3.3)')
text = text.replace('13개 모드 전체 HTML 쇼케이스', '13개 모드 전체 HTML 쇼케이스 v3')
text = text.replace('품질 게이트 적대적 검증을 거쳤습니다.', 'v3 레이아웃 안전·디자인 폴리시 패치와 자동 검증 게이트를 적용했습니다.')
text = text.replace('<span>13개 모드 HTML</span>', '<span>13개 모드 HTML</span><span>v3 layout-safe</span>')
if '15-svg-template-gallery.html' not in text:
    insert = '''
  <section class="hero-index">
    <h2><span class="num">4</span>추가 데모: SVG 템플릿 20종 갤러리</h2>
    <p class="h2-sub">v3 공통 CSS와 visual-figure 패턴으로 다시 정리한 SVG 템플릿 갤러리입니다.</p>
    <p><a href="pages/15-svg-template-gallery.html"><strong>SVG 템플릿 20종 데모 갤러리 열기 →</strong></a></p>
  </section>
'''
    text = text.replace('  <section class="try"><div class="label">Verification</div>', insert + '  <section class="try"><div class="label">Verification</div>')
else:
    # If a link exists, make label v3-aware.
    text = text.replace('SVG 템플릿 20종 데모 갤러리 열기', 'SVG 템플릿 20종 v3 데모 갤러리 열기')
if '15-svg-template-gallery.html' not in text:
    block='''
  <section id="svg-gallery" class="hero-index">
    <h2><span class="num">5</span>추가 데모 · SVG 템플릿 20종 갤러리</h2>
    <p class="h2-sub">v3 공통 CSS와 <code>figure.visual-figure</code> 패턴으로 다시 정리한 20개 SVG 템플릿 데모입니다.</p>
    <p><a href="pages/15-svg-template-gallery.html"><strong>SVG 템플릿 20종 v3 데모 갤러리 열기 →</strong></a></p>
  </section>
'''
    text = text.replace('  <section id="verify">', block + '\n  <section id="verify">')
# Add validation note if missing.
if 'validate_output.py' not in text:
    text = text.replace('</ul>\n  </section>\n\n  <section class="try"><div class="label">Verification</div>', '</ul>\n    <p><a href="sources/validate_output.py"><strong>v3 정적 검증 스크립트 보기 →</strong></a></p>\n  </section>\n\n  <section class="try"><div class="label">Verification</div>')
idx.write_text(text, encoding='utf-8')

print(f'created {OUT}')
print('html', len(list(OUT.glob('*.html'))) + len(list((OUT/'pages').glob('*.html'))))
