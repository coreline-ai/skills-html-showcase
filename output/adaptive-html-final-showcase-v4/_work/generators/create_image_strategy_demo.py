from pathlib import Path
from html import escape

ROOT = Path('output/adaptive-html-final-showcase')
PAGES = ROOT / 'pages'
MEDIA = ROOT / 'media'
MEDIA.mkdir(parents=True, exist_ok=True)

W, H = 8000, 6000

def tspan_lines(lines, x, y, size=130, fill='#1a1a1a', weight=600, leading=1.25, anchor='start'):
    out = [f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" font-weight="{weight}" text-anchor="{anchor}">']
    for i, line in enumerate(lines):
        dy = 0 if i == 0 else size * leading
        out.append(f'<tspan x="{x}" dy="{dy}">{escape(line)}</tspan>')
    out.append('</text>')
    return '\n'.join(out)

def card(x,y,w,h,title,lines,accent='#e63946',tag=None):
    parts = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="120" fill="#ffffff" stroke="#d8d8d0" stroke-width="14"/>',
             f'<rect x="{x}" y="{y}" width="26" height="{h}" rx="13" fill="{accent}"/>']
    if tag:
        parts.append(f'<text x="{x+120}" y="{y+170}" font-size="88" fill="{accent}" font-weight="900" letter-spacing="10">{escape(tag)}</text>')
        title_y = y+350
    else:
        title_y = y+210
    parts.append(tspan_lines([title], x+120, title_y, size=150, fill='#1a1a1a', weight=900))
    parts.append(tspan_lines(lines, x+120, title_y+250, size=104, fill='#4a4a4a', weight=520, leading=1.33))
    return '\n'.join(parts)

def base_svg(title, subtitle, body):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="title desc">
<title id="title">{escape(title)}</title>
<desc id="desc">{escape(subtitle)}</desc>
<style>
  text {{ font-family: Pretendard, -apple-system, BlinkMacSystemFont, "Noto Sans KR", Arial, sans-serif; }}
  .small {{ font-size: 92px; fill: #7a7a7a; font-weight: 650; }}
  .hair {{ stroke:#d8d8d0; stroke-width:10; }}
</style>
<rect width="8000" height="6000" fill="#f5f5f0"/>
<circle cx="7200" cy="740" r="520" fill="#fce4e6" opacity="0.8"/>
<circle cx="680" cy="5350" r="720" fill="#f0f4f8" opacity="0.95"/>
<text x="560" y="620" font-size="122" fill="#e63946" font-weight="900" letter-spacing="22">ADAPTIVE HTML IMAGE SYSTEM</text>
{tspan_lines([title], 560, 980, size=300, fill='#1a1a1a', weight=900, leading=1.08)}
{tspan_lines([subtitle], 570, 1280, size=118, fill='#4a4a4a', weight=560, leading=1.28)}
{body}
<text x="7440" y="5600" font-size="84" text-anchor="end" fill="#7a7a7a" font-weight="700">8000×6000 SVG · scalable infographic</text>
</svg>'''

# 1. Strategy map
body1 = []
body1.append('<line x1="920" y1="2780" x2="7080" y2="2780" class="hair"/>')
for cx, label in [(1700,'01'),(4000,'02'),(6300,'03')]:
    body1.append(f'<circle cx="{cx}" cy="2780" r="170" fill="#e63946"/>')
    body1.append(f'<text x="{cx}" y="2835" font-size="150" text-anchor="middle" fill="#fff" font-weight="900">{label}</text>')
body1.append(card(520, 1660, 1960, 1360, '찾기', ['실제 장소·인물·제품은', '공개 라이선스 이미지를 우선', '출처·라이선스·대체텍스트 기록'], '#e63946', 'SOURCE'))
body1.append(card(3020, 1660, 1960, 1360, '만들기', ['추상 개념·프로세스·비교는', 'SVG 인포그래픽으로 직접 생성', '8000×6000 원본 캔버스 유지'], '#3a6280', 'CREATE'))
body1.append(card(5520, 1660, 1960, 1360, '검증하기', ['모바일 390px, 색 대비,', '텍스트 가독성, 사실성,', '라이선스 증빙을 통과해야 삽입'], '#2a7d5a', 'VERIFY'))
body1.append(card(720, 3540, 6560, 1120, '추천 결론', ['가장 안전한 기본값은 “사진은 필요한 경우에만 찾고, 핵심 설명은 벡터 인포그래픽으로 만든다”입니다.', '현재 스킬의 editorial 레이아웃에는 장식 사진보다 구조도·흐름도·비교표형 이미지가 더 잘 맞습니다.'], '#1a1a1a'))
(MEDIA/'image-strategy-map-8000x6000.svg').write_text(base_svg('섹션 이미지는 찾기보다 설계가 먼저입니다', '사진·인포그래픽·AI 생성 이미지를 목적별로 나누는 3단계 운영안', '\n'.join(body1)))

# 2. Mode map
modes = [
('beginner', '비유 일러스트', '개념을 생활 장면으로'),
('expert', '운영모델 지도', 'RACI·리스크·로드맵'),
('article', '에디토리얼 키비주얼', '주장과 분위기 형성'),
('education', '학습 경로도', '목표→실습→퀴즈'),
('blog', '개인 경험 장면', '문제 상황을 감각화'),
('seo', 'SERP/키워드 맵', '검색 의도 구조화'),
('platform', '플랫폼 카드', '채널별 변환 차이'),
('audit', '진단 대시보드', '점수·결함·개선안'),
('reference', '개념/API 지도', '탐색 가능한 구조'),
('comparison', '선택 매트릭스', '승자·트레이드오프'),
('case', '타임라인', '사건→결정→결과'),
('landing', '가치 제안 그림', '문제·해결·CTA'),
('checklist', '운영 체크 플로우', '조건·증빙·완료')]
body2=[]
cols=4; x0=430; y0=1540; cw=1680; ch=650; gapx=170; gapy=190
for i,(mode,typ,desc) in enumerate(modes):
    col=i%cols; row=i//cols
    x=x0+col*(cw+gapx); y=y0+row*(ch+gapy)
    w=cw
    if i==12:
        x=x0; y=y0+3*(ch+gapy); w=3530
    accent=['#e63946','#3a6280','#2a7d5a','#d99a38'][i%4]
    body2.append(f'<rect x="{x}" y="{y}" width="{w}" height="{ch}" rx="86" fill="#fff" stroke="#d8d8d0" stroke-width="12"/>')
    body2.append(f'<circle cx="{x+150}" cy="{y+165}" r="72" fill="{accent}"/>')
    body2.append(f'<text x="{x+150}" y="{y+190}" font-size="76" fill="#fff" text-anchor="middle" font-weight="900">{i+1}</text>')
    body2.append(f'<text x="{x+270}" y="{y+154}" font-size="78" fill="#e63946" font-weight="900" letter-spacing="2">{escape(mode)}</text>')
    body2.append(tspan_lines([typ], x+270, y+315, size=102, fill='#1a1a1a', weight=900))
    body2.append(tspan_lines([desc], x+270, y+455, size=72, fill='#4a4a4a', weight=560))
body2.append('<rect x="430" y="5020" width="7140" height="12" rx="6" fill="#d8d8d0" opacity="0.55"/>')
body2.append('<text x="430" y="5220" font-size="82" fill="#7a7a7a" font-weight="700">모든 카드는 6000px 캔버스 안쪽에 배치되어 HTML figure 하단에서 잘리지 않습니다.</text>')
(MEDIA/'mode-visual-map-8000x6000.svg').write_text(base_svg('13개 모드별 최적 이미지 타입', '모드마다 장식 이미지가 아니라 정보 구조를 보강하는 시각물을 붙입니다', '\n'.join(body2)))

# 3. Decision tree
body3=[]
body3.append(card(580, 1580, 2500, 900, '현실 이미지가 필요한가?', ['제품 사진, 실제 인물, 장소,', '뉴스 현장처럼 현실성이 핵심이면', '라이선스 이미지 검색'], '#e63946', 'Q1'))
body3.append(card(4920, 1580, 2500, 900, '개념 설명이 핵심인가?', ['프로세스, 비교, 정책, 구조라면', '직접 만든 인포그래픽이 더 명확'], '#3a6280', 'Q2'))
body3.append('<path d="M3080 2030 C3700 2030 4300 2030 4920 2030" fill="none" stroke="#1a1a1a" stroke-width="18" stroke-linecap="round"/>')
body3.append('<polygon points="4900,2030 4720,1930 4720,2130" fill="#1a1a1a"/>')
body3.append(card(580, 3040, 2020, 1040, 'SOURCE', ['Unsplash/Pexels/Openverse/', 'Wikimedia 등에서 검색', '출처와 라이선스 기록'], '#e63946'))
body3.append(card(2990, 3040, 2020, 1040, 'SVG INFOGRAPHIC', ['8000×6000 캔버스', '텍스트 적음, 구조 선명', '모바일에서도 축소 가독성'], '#2a7d5a'))
body3.append(card(5400, 3040, 2020, 1040, 'AI GENERATED', ['현실성보다 메타포가 필요할 때', '브랜드/인물/사실 혼동 금지', '검수 후 사용'], '#d99a38'))
for x1,x2 in [(1580,1580),(4000,4000),(6410,6410)]:
    body3.append(f'<path d="M{x1} 2480 L{x2} 3040" fill="none" stroke="#d8d8d0" stroke-width="16" stroke-linecap="round"/>')
body3.append(card(1220, 4460, 5560, 720, '자동 판단 규칙', ['사진은 신뢰를 만들고, 인포그래픽은 이해를 만듭니다. 전문가/교육/레퍼런스/비교 모드는 기본적으로 인포그래픽 우선입니다.'], '#1a1a1a'))
(MEDIA/'image-decision-tree-8000x6000.svg').write_text(base_svg('섹션 이미지 선택 의사결정 트리', '이미지를 찾을지 만들지 판단하는 운영 규칙', '\n'.join(body3)))

# 4. Quality gate
body4=[]
checks=[
('해상도', '원본 8000×6000 SVG 또는 고해상도 래스터'),
('가독성', '축소 후에도 제목·화살표·핵심 수치가 보임'),
('정확성', '수치·인용·현실 묘사는 출처 기반'),
('접근성', 'alt, figcaption, 색 대비, 텍스트 대체'),
('라이선스', 'URL, 저작자, 라이선스, 수정 여부 기록'),
('모바일', '390px에서 잘림 없이 object-fit/overflow 검증')]
# Balanced 2×3 grid + one substantial yellow preflight panel. Avoid skinny bottom banners.
x0=560; y0=1580; cw=3340; ch=700; gapx=300; gapy=190
for i,(k,v) in enumerate(checks):
    col=i%2; row=i//2
    x=x0+col*(cw+gapx); y=y0+row*(ch+gapy)
    accent=['#2a7d5a','#3a6280','#d99a38','#e63946','#1a1a1a','#2a7d5a'][i]
    body4.append(f'<rect x="{x}" y="{y}" width="{cw}" height="{ch}" rx="104" fill="#ffffff" stroke="#d8d8d0" stroke-width="12"/>')
    body4.append(f'<rect x="{x}" y="{y}" width="30" height="{ch}" rx="15" fill="{accent}"/>')
    body4.append(f'<circle cx="{x+210}" cy="{y+190}" r="92" fill="{accent}"/>')
    body4.append(f'<path d="M{x+160} {y+190} L{x+198} {y+232} L{x+285} {y+136}" fill="none" stroke="#fff" stroke-width="32" stroke-linecap="round" stroke-linejoin="round"/>')
    body4.append(f'<text x="{x+360}" y="{y+185}" font-size="126" fill="#1a1a1a" font-weight="950">{escape(k)}</text>')
    body4.append(f'<text x="{x+360}" y="{y+330}" font-size="82" fill="#4a4a4a" font-weight="620">{escape(v)}</text>')
    body4.append(f'<text x="{x+360}" y="{y+500}" font-size="66" fill="#7a7a7a" font-weight="650">검수 후 삽입 · 모바일 확인 · 출처 기록</text>')
# Yellow preflight card inspired by the attached yellow background, but with enough height and footer clearance.
y=4300
body4.append('<rect x="560" y="4300" width="6880" height="760" rx="128" fill="#ffd400" stroke="#1a1a1a" stroke-width="18"/>')
body4.append('<rect x="560" y="4300" width="38" height="760" rx="19" fill="#e63946"/>')
body4.append('<circle cx="6950" cy="4560" r="190" fill="#fff4a3" opacity="0.8"/>')
body4.append('<text x="780" y="4555" font-size="170" fill="#1a1a1a" font-weight="950">삽입 전 필수 검수</text>')
body4.append('<text x="780" y="4755" font-size="96" fill="#1a1a1a" font-weight="720">예쁜 이미지보다 “오해 없이 바로 이해되는 이미지”가 우선입니다.</text>')
body4.append('<text x="780" y="4925" font-size="78" fill="#5a3a00" font-weight="700">8000×6000 · alt · figcaption · source · mobile 390px · no overflow</text>')
body4.append('<text x="7200" y="4990" font-size="82" text-anchor="end" fill="#1a1a1a" font-weight="900">PRE-FLIGHT</text>')
(MEDIA/'image-quality-gate-8000x6000.svg').write_text(base_svg('이미지 품질 게이트', '섹션 이미지 삽입 전 반드시 확인해야 하는 6가지 기준', '\n'.join(body4)))

# 5. Section pattern
body5=[]
body5.append('<rect x="580" y="1540" width="6840" height="3940" rx="140" fill="#fff" stroke="#d8d8d0" stroke-width="16"/>')
steps=[('H2', '섹션 제목', 1040, 2100),('SUB', '한 줄 목적', 2640, 2100),('VISUAL', '인포그래픽', 4240, 2100),('BODY', '해설 본문', 5840, 2100)]
for i,(tag,label,cx,cy) in enumerate(steps):
    body5.append(f'<circle cx="{cx}" cy="{cy}" r="230" fill="{["#e63946","#3a6280","#2a7d5a","#d99a38"][i]}"/>')
    body5.append(f'<text x="{cx}" y="{cy-20}" font-size="102" text-anchor="middle" fill="#fff" font-weight="900">{tag}</text>')
    body5.append(f'<text x="{cx}" y="{cy+110}" font-size="78" text-anchor="middle" fill="#fff" font-weight="700">{escape(label)}</text>')
    if i<3:
        body5.append(f'<path d="M{cx+300} {cy} L{steps[i+1][2]-300} {cy}" stroke="#1a1a1a" stroke-width="18" stroke-linecap="round"/>')
        body5.append(f'<polygon points="{steps[i+1][2]-290},{cy} {steps[i+1][2]-460},{cy-90} {steps[i+1][2]-460},{cy+90}" fill="#1a1a1a"/>')
body5.append(card(980, 2860, 2720, 1120, '본문 앞 이미지', ['복잡한 개념은 본문 전에 배치', '독자가 구조를 먼저 본 뒤', '문장을 읽게 만듭니다.'], '#3a6280'))
body5.append(card(4300, 2860, 2720, 1120, '본문 중 이미지', ['비교·리스크·절차처럼', '읽다가 판단이 필요한 지점에', '보조 시각물을 넣습니다.'], '#2a7d5a'))
body5.append(tspan_lines(['권장 HTML 패턴: figure → img → figcaption → 설명 본문 → 체크리스트'], 1160, 4600, size=136, fill='#1a1a1a', weight=900))
(MEDIA/'section-image-pattern-8000x6000.svg').write_text(base_svg('섹션마다 같은 삽입 패턴을 씁니다', '현재 레이아웃을 해치지 않는 이미지 위치와 역할', '\n'.join(body5)))

# Extract existing style from revised page and append visual styles
src = (PAGES/'02-expert-eu-ai-act-governance.html').read_text()
style = src.split('<style>',1)[1].split('</style>',1)[0]
custom_css = r'''
.figure-wide{background:var(--card);border:1px solid var(--line);border-radius:var(--radius-lg);padding:14px;margin:22px 0 28px;overflow:hidden}
.figure-wide img{display:block;width:100%;height:auto;border-radius:8px;background:#f5f5f0;border:1px solid var(--line)}
.figure-wide figcaption{font-size:13px;color:var(--ink-mute);line-height:1.65;margin:10px 4px 0}
.visual-rule-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px;margin:18px 0}
.visual-rule{background:var(--card);border:1px solid var(--line);border-radius:var(--radius-md);padding:18px;border-top:4px solid var(--accent)}
.visual-rule h3{margin:0 0 8px;font-size:16px}.visual-rule p{font-size:14px;margin:0}
.pipeline{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px;margin:18px 0}.pipeline .mini-card{min-height:156px}
@media(max-width:760px){.visual-rule-grid,.pipeline{grid-template-columns:1fr}.figure-wide{padding:10px;margin-left:-2px;margin-right:-2px}.figure-wide figcaption{font-size:12.5px}}
'''

html = f'''<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>섹션별 이미지 전략 데모 · Adaptive HTML Final</title>
<meta name="description" content="현재 adaptive-html-final 레이아웃에 섹션별 고해상도 이미지와 8000×6000 SVG 인포그래픽을 삽입하는 전략 데모.">
<meta property="og:title" content="섹션별 이미지 전략 데모">
<meta property="og:description" content="이미지 검색, SVG 인포그래픽 생성, AI 이미지 생성의 하이브리드 운영안을 HTML로 검증한 데모.">
<meta property="og:type" content="article">
<link rel="preconnect" href="https://cdn.jsdelivr.net">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.css" rel="stylesheet">
<link href="https://fonts.googleapis.com/css2?family=Noto+Serif+KR:wght@400;600;700&display=swap" rel="stylesheet">
<style>
{style}
{custom_css}
</style>
</head>
<body>
<a class="skip" href="#main">본문 바로가기</a>
<main id="main" class="page-wide layout-expert">
  <nav class="page-nav"><a href="../index.html">← 쇼케이스 홈</a><span>Image Strategy Demo · 8000×6000 SVG</span></nav>
  <header class="header report-header">
    <div class="kicker">Visual System Demo</div>
    <h1>섹션별 이미지 삽입 전략: 찾을 것과 만들 것을 분리하기</h1>
    <p class="sub">현재 레이아웃은 텍스트 구조가 강하므로, 이미지는 장식보다 <strong>이해·판단·검증을 돕는 인포그래픽</strong> 중심으로 넣는 편이 가장 좋습니다. 이 데모는 8000×6000 SVG 원본 이미지를 실제 HTML 섹션마다 삽입한 예시입니다.</p>
    <div class="meta"><span>권장 방식: 하이브리드</span><span>원본 이미지: 8000×6000 SVG</span><span>외부 JS 없음</span><span>검토일: 2026-05-30</span></div>
  </header>

  <figure class="figure-wide">
    <img src="../media/image-strategy-map-8000x6000.svg" width="8000" height="6000" alt="이미지 소싱, 인포그래픽 생성, 품질 검증으로 이어지는 섹션 이미지 운영 전략 맵">
    <figcaption>Hero visual. 섹션 이미지는 먼저 목적을 정하고, 현실 사진·인포그래픽·AI 생성 이미지 중 하나를 선택한 뒤 검증 게이트를 통과시킵니다.</figcaption>
  </figure>

  <section id="recommendation">
    <h2><span class="num">1</span>가장 좋은 방식</h2>
    <p class="h2-sub">현재 스킬 레이아웃에는 “사진 많이 넣기”보다 “설명형 인포그래픽 + 필요한 경우 사진”이 더 잘 맞습니다.</p>
    <div class="executive-summary">
      <div class="label">Recommended Operating Model</div>
      <p><strong>기본값은 SVG 인포그래픽 생성</strong>입니다. 전문가 리포트, 교육, 레퍼런스, 비교, 체크리스트처럼 구조 이해가 중요한 모드는 직접 만든 고해상도 벡터 이미지가 가장 안정적입니다. 현실성이 필요한 아티클/블로그/뉴스형 섹션만 라이선스 이미지를 찾고, 추상 개념은 AI 이미지보다 도식화된 인포그래픽으로 처리하는 것이 좋습니다.</p>
    </div>
    <div class="visual-rule-grid">
      <div class="visual-rule"><h3>찾아 넣기</h3><p>실제 사람, 장소, 제품, 사건 사진이 필요할 때. 출처와 라이선스 증빙이 필수입니다.</p></div>
      <div class="visual-rule"><h3>만들어 넣기</h3><p>절차, 비교, 정책, 리스크, 학습 구조는 SVG 인포그래픽으로 직접 생성합니다.</p></div>
      <div class="visual-rule"><h3>AI 생성</h3><p>메타포·컨셉 이미지가 필요하지만 사실 이미지처럼 오해되면 안 되는 경우에만 사용합니다.</p></div>
    </div>
  </section>

  <section id="mode-map">
    <h2><span class="num">2</span>13개 모드별 이미지 타입 매핑</h2>
    <p class="h2-sub">모드마다 적합한 시각물은 다릅니다. 같은 예쁜 이미지를 반복하면 정보 구조가 약해집니다.</p>
    <figure class="figure-wide">
      <img src="../media/mode-visual-map-8000x6000.svg" width="8000" height="6000" decoding="async" alt="13개 HTML 생성 모드별 최적 이미지 타입 매핑 인포그래픽">
      <figcaption>모드별 이미지 매핑. beginner는 비유 일러스트, expert는 운영모델 지도, comparison은 선택 매트릭스, checklist는 운영 체크 플로우가 적합합니다.</figcaption>
    </figure>
    <div class="tbl"><table><caption class="caption">모드별 권장 이미지 정책</caption><thead><tr><th>모드 그룹</th><th>우선 이미지</th><th>피해야 할 이미지</th></tr></thead><tbody>
      <tr><td>전문가/감사/비교</td><td>리스크 맵, RACI, 판단 매트릭스, 로드맵</td><td>의미 없는 추상 배경, 장식성 사진</td></tr>
      <tr><td>교육/초보자/레퍼런스</td><td>개념도, 단계도, 예제 흐름, API 구조도</td><td>텍스트가 많은 스크린샷, 설명 없는 아이콘</td></tr>
      <tr><td>아티클/블로그/랜딩</td><td>키비주얼, 상황 이미지, 한 장 요약 카드</td><td>본문 내용과 무관한 스톡 사진</td></tr>
      <tr><td>SEO/플랫폼/체크리스트</td><td>대시보드, 카드 그리드, 발행 체크 플로우</td><td>출처 없는 뉴스 썸네일, 과도한 UI 모사</td></tr>
    </tbody></table></div>
  </section>

  <section id="decision-tree">
    <h2><span class="num">3</span>찾을지 만들지 결정하는 규칙</h2>
    <p class="h2-sub">이미지를 무조건 검색하지 말고, 섹션의 역할을 기준으로 선택합니다.</p>
    <figure class="figure-wide">
      <img src="../media/image-decision-tree-8000x6000.svg" width="8000" height="6000" decoding="async" alt="현실 이미지가 필요한지 개념 설명이 필요한지에 따라 소스 이미지, SVG 인포그래픽, AI 생성 이미지를 선택하는 의사결정 트리">
      <figcaption>Decision tree. 현실성이 핵심이면 소스 이미지를 찾고, 개념 이해가 핵심이면 SVG 인포그래픽을 만들며, 메타포가 필요할 때만 AI 생성 이미지를 사용합니다.</figcaption>
    </figure>
    <div class="good"><div class="label">GOOD DEFAULT</div><div class="name">전문가 문서에는 사진보다 구조도가 더 강합니다</div><p>EU AI Act, 보안 사고, API 레퍼런스, SEO 대시보드처럼 독자가 판단해야 하는 문서에서는 “멋진 사진”보다 “한눈에 판단 가능한 구조도”가 훨씬 유용합니다.</p></div>
  </section>

  <section id="section-pattern">
    <h2><span class="num">4</span>섹션 삽입 패턴</h2>
    <p class="h2-sub">현재 레이아웃을 유지하려면 이미지 위치도 규칙화해야 합니다.</p>
    <figure class="figure-wide">
      <img src="../media/section-image-pattern-8000x6000.svg" width="8000" height="6000" decoding="async" alt="H2, 섹션 부제, 인포그래픽, 본문 해설 순서로 이미지를 삽입하는 HTML 섹션 패턴">
      <figcaption>Section pattern. 권장 순서는 H2 → h2-sub → figure → figcaption → 본문입니다. 본문을 읽기 전에 구조를 먼저 보여주는 방식입니다.</figcaption>
    </figure>
    <div class="pipeline">
      <div class="mini-card"><h3>1. H2</h3><p>섹션 목적을 명확히 씁니다.</p></div>
      <div class="mini-card"><h3>2. Visual</h3><p>핵심 구조를 한 장으로 보여줍니다.</p></div>
      <div class="mini-card"><h3>3. Caption</h3><p>이미지가 말하는 결론을 한 문장으로 고정합니다.</p></div>
      <div class="mini-card"><h3>4. Body</h3><p>그림을 근거로 상세 설명합니다.</p></div>
    </div>
  </section>

  <section id="quality">
    <h2><span class="num">5</span>품질 게이트</h2>
    <p class="h2-sub">이미지는 예쁜지보다 안전하게 이해되는지가 중요합니다.</p>
    <figure class="figure-wide">
      <img src="../media/image-quality-gate-8000x6000.svg" width="8000" height="6000" decoding="async" alt="해상도, 가독성, 정확성, 접근성, 라이선스, 모바일 검증으로 구성된 이미지 품질 게이트">
      <figcaption>Quality gate. 8000×6000 원본, 모바일 390px 축소, alt/figcaption, 출처/라이선스, 색 대비를 모두 확인해야 합니다.</figcaption>
    </figure>
    <div class="danger"><div class="label">주의</div><div class="name">AI 생성 이미지는 사실 이미지처럼 쓰면 안 됩니다</div><p>뉴스, 규제, 사건, 제품 스크린샷처럼 사실성이 중요한 섹션에는 AI 생성 이미지를 사용하지 않는 편이 안전합니다. 그런 경우에는 공식 이미지, 공개 라이선스 이미지, 직접 만든 도식이 더 적합합니다.</p></div>
  </section>

  <section id="workflow">
    <h2><span class="num">6</span>실제 작업 절차</h2>
    <p class="h2-sub">앞으로 페이지를 만들 때 이 순서로 자동화하면 됩니다.</p>
    <div class="tbl"><table><caption class="caption">섹션 이미지 자동화 워크플로우</caption><thead><tr><th>단계</th><th>작업</th><th>산출물</th></tr></thead><tbody>
      <tr><td>1. 섹션 분석</td><td>H2, h2-sub, 핵심 주장, 데이터 유무를 추출</td><td>visual_brief.json</td></tr>
      <tr><td>2. 이미지 타입 결정</td><td>photo / infographic / AI concept 중 선택</td><td>visual_plan.md</td></tr>
      <tr><td>3. 생성 또는 검색</td><td>SVG 생성, 라이선스 이미지 검색, AI 이미지 생성</td><td>8000×6000 원본 이미지</td></tr>
      <tr><td>4. 접근성 작성</td><td>alt, figcaption, source-note 작성</td><td>HTML figure 블록</td></tr>
      <tr><td>5. 렌더 검증</td><td>390px/1280px에서 잘림, 대비, 로딩 확인</td><td>검수 로그 및 스크린샷</td></tr>
    </tbody></table></div>
  </section>

  <div class="try">
    <div class="label">Final Recommendation</div>
    <h2>최종 추천: “SVG 인포그래픽 우선 + 필요한 경우 라이선스 사진 + 제한적 AI 이미지”</h2>
    <ol>
      <li><strong>전문가/교육/레퍼런스/비교/체크리스트</strong>는 8000×6000 SVG 인포그래픽을 기본값으로 둡니다.</li>
      <li><strong>아티클/블로그/랜딩</strong>은 키비주얼이 필요할 때만 사진 또는 AI 컨셉 이미지를 사용합니다.</li>
      <li><strong>모든 이미지</strong>에는 alt, figcaption, 출처/생성 방식, 모바일 검증 결과를 남깁니다.</li>
    </ol>
  </div>

  <div class="source-note">
    <div class="label">Image source policy</div>
    <p>이 데모의 이미지는 외부 사진을 사용하지 않고 로컬에서 생성한 8000×6000 SVG 인포그래픽입니다. 실제 사진을 사용할 경우 Unsplash/Pexels/Openverse/Wikimedia Commons 등에서 라이선스를 확인하고, 가능하면 출처를 남기는 방식을 권장합니다.</p>
  </div>

  <footer><p>Adaptive HTML Final Showcase · Image Strategy Demo · Generated 2026-05-30</p></footer>
</main>
</body>
</html>
'''
(PAGES/'14-image-strategy-demo.html').write_text(html)
print('created', PAGES/'14-image-strategy-demo.html')
for p in sorted(MEDIA.glob('*.svg')):
    print(p.name, p.stat().st_size)
