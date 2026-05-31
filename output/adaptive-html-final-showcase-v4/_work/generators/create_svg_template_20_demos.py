from pathlib import Path
from html import escape
import math, shutil

ROOTS = [Path('output/adaptive-html-final-showcase'), Path('output/adaptive-html-final-showcase-v2')]
SRC10 = Path('output/adaptive-html-final-showcase/media/svg-template-demos')
W,H=8000,6000
ACCENT='#e63946'; YELLOW='#ffd400'; BLUE='#3a6280'; GREEN='#2a7d5a'; ORANGE='#d99a38'; INK='#1a1a1a'; SOFT='#4a4a4a'; MUTE='#7a7a7a'; LINE='#d8d8d0'; BG='#f5f5f0'; CARD='#fff'

def esc(s): return escape(str(s), quote=True)
def txt(lines,x,y,size=100,fill=INK,weight=700,anchor='start',leading=1.25):
    if isinstance(lines,str): lines=[lines]
    out=[f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" font-weight="{weight}" text-anchor="{anchor}">']
    for i,line in enumerate(lines):
        out.append(f'<tspan x="{x}" dy="{0 if i==0 else int(size*leading)}">{esc(line)}</tspan>')
    out.append('</text>')
    return '\n'.join(out)
def header(title,subtitle,kicker='SVG TEMPLATE DEMO'):
    return '\n'.join([
        f'<text x="560" y="620" font-size="118" fill="{ACCENT}" font-weight="950" letter-spacing="22">{esc(kicker)}</text>',
        txt(title,560,980,285,INK,950,leading=1.06),
        txt(subtitle,570,1280,116,SOFT,580,leading=1.25),
    ])
def base_svg(title,subtitle,body,footer='8000×6000 SVG · adaptive template demo'):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="title desc">
<title id="title">{esc(title)}</title>
<desc id="desc">{esc(subtitle)}</desc>
<style>text{{font-family:Pretendard,-apple-system,BlinkMacSystemFont,"Noto Sans KR",Arial,sans-serif}}.shadow{{filter:drop-shadow(0 20px 32px rgba(26,26,26,.08))}}</style>
<rect width="8000" height="6000" fill="{BG}"/>
<circle cx="7230" cy="760" r="520" fill="#fce4e6" opacity=".72"/>
<circle cx="650" cy="5350" r="760" fill="#f0f4f8" opacity=".88"/>
{header(title,subtitle)}
{body}
<text x="7440" y="5600" font-size="84" text-anchor="end" fill="{MUTE}" font-weight="750">{esc(footer)}</text>
</svg>'''
def card(x,y,w,h,title,desc='',accent=ACCENT,rx=96,fill=CARD):
    parts=[f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{LINE}" stroke-width="12" class="shadow"/>',f'<rect x="{x}" y="{y}" width="28" height="{h}" rx="14" fill="{accent}"/>',txt(title,x+110,y+160,108,INK,900)]
    if desc:
        if isinstance(desc,str): desc=[desc]
        parts.append(txt(desc,x+110,y+315,72,SOFT,560,leading=1.28))
    return '\n'.join(parts)
def arrow(x1,y1,x2,y2,color=INK,w=16):
    ang=math.atan2(y2-y1,x2-x1); size=58
    p1=(x2-size*math.cos(ang)-size*.55*math.sin(ang), y2-size*math.sin(ang)+size*.55*math.cos(ang))
    p2=(x2-size*math.cos(ang)+size*.55*math.sin(ang), y2-size*math.sin(ang)-size*.55*math.cos(ang))
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{w}" stroke-linecap="round"/><polygon points="{x2},{y2} {p1[0]},{p1[1]} {p2[0]},{p2[1]}" fill="{color}"/>'
def pill(x,y,text,fill='#fff',stroke=LINE,color=SOFT):
    return f'<rect x="{x}" y="{y}" width="{len(text)*42+120}" height="112" rx="56" fill="{fill}" stroke="{stroke}" stroke-width="8"/><text x="{x+60}" y="{y+72}" font-size="56" fill="{color}" font-weight="850">{esc(text)}</text>'

# 11 Sankey / alluvial
def svg_sankey():
    body=[]; xs=[820,3180,5540]; ys=[[1700,2650,3600],[1850,3000,4050],[2050,3350]]
    labels=[['Input A','Input B','Input C'],['Segment 1','Segment 2','Segment 3'],['Outcome X','Outcome Y']]
    cols=[ACCENT,BLUE,GREEN]
    for ci,x in enumerate(xs):
        for i,y in enumerate(ys[ci]):
            body.append(card(x,y,1320,440,labels[ci][i],'',cols[ci],72))
    flows=[(2140,1920,3180,2070,ACCENT,70),(2140,2870,3180,3220,BLUE,110),(2140,3820,3180,4270,GREEN,55),(4500,2070,5540,2270,ACCENT,90),(4500,3220,5540,2270,BLUE,60),(4500,3220,5540,3570,BLUE,80),(4500,4270,5540,3570,GREEN,70)]
    for x1,y1,x2,y2,c,w in flows:
        body.append(f'<path d="M{x1} {y1} C {x1+520} {y1}, {x2-520} {y2}, {x2} {y2}" fill="none" stroke="{c}" stroke-width="{w}" stroke-linecap="round" opacity=".58"/>')
    body.append(card(900,4820,6000,420,'Use case',['유입→세그먼트→결과처럼 흐름의 크기와 이동 경로를 동시에 설명합니다.'],YELLOW))
    return base_svg('Sankey / Alluvial Flow', '범주 간 이동량과 전환 흐름을 두꺼운 곡선으로 표현', '\n'.join(body))

# 12 Treemap
def svg_treemap():
    body=[]; x0,y0=760,1620; w,h=6480,3300
    body.append(f'<rect x="{x0}" y="{y0}" width="{w}" height="{h}" rx="120" fill="#fff" stroke="{LINE}" stroke-width="14"/>')
    rects=[('Core',x0+80,y0+90,3000,1500,ACCENT),('Growth',x0+3160,y0+90,1880,1500,BLUE),('Ops',x0+5120,y0+90,1200,1500,GREEN),('Research',x0+80,y0+1670,1900,1380,ORANGE),('Infra',x0+2060,y0+1670,1700,1380,YELLOW),('Support',x0+3840,y0+1670,2480,1380,INK)]
    for name,x,y,rw,rh,c in rects:
        body.append(f'<rect x="{x}" y="{y}" width="{rw}" height="{rh}" rx="70" fill="{c}" opacity=".88"/>')
        body.append(txt(name,x+90,y+150,100,'#fff' if c!=YELLOW else INK,950))
        body.append(txt(f'{int(rw*rh/100000)} pts',x+90,y+300,72,'#fff' if c!=YELLOW else INK,750))
    body.append(card(960,5050,5900,320,'Portfolio rule',['면적은 규모, 색상은 우선순위, 라벨은 담당 영역을 의미합니다.'],BLUE))
    return base_svg('Treemap Priority Portfolio', '큰 영역과 작은 영역을 한눈에 비교하는 포트폴리오 맵', '\n'.join(body))

# 13 Radial ecosystem network
def svg_radial_network():
    body=[]; cx,cy=4000,3150; R=640
    nodes=[('Users',4000,1720,ACCENT),('Partners',5600,2300,BLUE),('Data',5740,3950,GREEN),('Ops',4000,4700,ORANGE),('Policy',2260,3950,INK),('Tools',2400,2300,ACCENT)]
    # spokes start at the circle perimeter so they never cross the center label
    for label,x,y,c in nodes:
        d=math.hypot(x-cx,y-cy)
        sx,sy=cx+(x-cx)/d*R, cy+(y-cy)/d*R
        body.append(f'<line x1="{sx:.0f}" y1="{sy:.0f}" x2="{x}" y2="{y}" stroke="{LINE}" stroke-width="18"/>')
    for label,x,y,c in nodes:
        body.append(card(x-520,y-220,1040,440,label,['role','signals'],c,80))
    # hub drawn last so the center sits cleanly on top of the spokes
    body.append(f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="{YELLOW}" stroke="{INK}" stroke-width="16"/>')
    body.append(txt(['Core','Platform'],cx,cy-30,120,INK,950,anchor='middle'))
    return base_svg('Radial Ecosystem Network', '중심 플랫폼과 주변 이해관계자 관계를 방사형으로 표현', '\n'.join(body))

# 14 Conversion funnel
def svg_funnel():
    body=[]; levels=[('Visit',6200,ACCENT),('Signup',5000,BLUE),('Activate',3800,GREEN),('Retain',2600,ORANGE),('Refer',1500,YELLOW)]
    y=1650
    for i,(label,width,c) in enumerate(levels):
        x=4000-width/2; h=560
        body.append(f'<path d="M{x} {y} H{x+width} L{x+width-260} {y+h} H{x+260} Z" fill="{c}" opacity=".9" stroke="#fff" stroke-width="14"/>')
        body.append(txt(label,4000,y+225,116,'#fff' if c!=YELLOW else INK,950,anchor='middle'))
        body.append(txt(f'{100-i*18}%',4000,y+380,76,'#fff' if c!=YELLOW else INK,850,anchor='middle'))
        y+=650
    body.append(card(1060,4950,5880,390,'Optimization rule',['각 단계의 전환율·이탈 사유·다음 실험을 함께 기록합니다.'],INK))
    return base_svg('Conversion Funnel', '방문부터 추천까지 단계별 전환과 이탈을 시각화', '\n'.join(body))

# 15 User journey map
def svg_journey():
    body=[]; stages=['Discover','Evaluate','Start','Use','Return']; x0,y0=800,1680; cw=1280; rh=560
    rows=['Action','Emotion','Pain','Opportunity']
    for i,s in enumerate(stages):
        x=x0+i*cw
        body.append(f'<rect x="{x}" y="{y0}" width="{cw-40}" height="3000" rx="80" fill="#fff" stroke="{LINE}" stroke-width="10"/>')
        body.append(f'<rect x="{x}" y="{y0}" width="{cw-40}" height="220" rx="80" fill="{[ACCENT,BLUE,GREEN,ORANGE,YELLOW][i]}"/>')
        body.append(txt(s,x+(cw-40)/2,y0+142,70,'#fff' if i!=4 else INK,950,anchor='middle'))
        for r,row in enumerate(rows):
            y=y0+330+r*rh
            body.append(f'<rect x="{x+80}" y="{y}" width="{cw-200}" height="{rh-80}" rx="50" fill="#f8f8f4" stroke="{LINE}" stroke-width="6"/>')
            body.append(txt(row,x+140,y+105,56,INK,900))
            body.append(txt('insight note',x+140,y+205,48,SOFT,560))
    return base_svg('User Journey Map', '사용자 단계별 행동·감정·Pain·기회를 정리', '\n'.join(body))

# 16 Service blueprint
def svg_blueprint():
    body=[]; lanes=['Customer action','Frontstage','Backstage','Systems','Metrics']; x0,y0=800,1580; w=6400; lh=620
    for r,lane in enumerate(lanes):
        y=y0+r*lh
        body.append(f'<rect x="{x0}" y="{y}" width="{w}" height="{lh-30}" rx="54" fill="#fff" stroke="{LINE}" stroke-width="10"/>')
        body.append(f'<rect x="{x0}" y="{y}" width="1160" height="{lh-30}" rx="54" fill="#f8f8f4"/>')
        body.append(txt(lane,x0+580,y+lh/2+18,66,INK,900,anchor='middle'))
        for c in range(4):
            body.append(f'<rect x="{x0+1320+c*1240}" y="{y+110}" width="940" height="250" rx="50" fill="{["#fffaf2","#eef7f1","#f0f4f8","#fff0ee"][c]}" stroke="{LINE}" stroke-width="6"/>')
            body.append(txt(f'Step {c+1}',x0+1400+c*1240,y+260,52,SOFT,760))
    body.append(f'<line x1="{x0}" y1="{y0+2*lh-30}" x2="{x0+w}" y2="{y0+2*lh-30}" stroke="{ACCENT}" stroke-width="18" stroke-dasharray="50 28"/>')
    body.append(txt('Line of visibility',x0+w-420,y0+2*lh-80,56,ACCENT,900,anchor='end'))
    return base_svg('Service Blueprint Lanes', '고객 경험과 내부 운영을 lane 구조로 연결', '\n'.join(body))

# 17 Attack chain control map
def svg_attack_chain():
    body=[]; steps=['Recon','Initial Access','Execute','Persist','Exfiltrate']; x0,y0=860,2200; gap=1320
    for i,s in enumerate(steps):
        x=x0+i*gap
        body.append(card(x,y0,1060,620,s,['threat step','controls below'],[ACCENT,ORANGE,BLUE,GREEN,INK][i],80))
        if i<4: body.append(arrow(x+1060,y0+310,x0+(i+1)*gap,y0+310,INK,14))
        body.append(f'<rect x="{x}" y="{y0+820}" width="1060" height="680" rx="72" fill="#eef7f1" stroke="{GREEN}" stroke-width="10"/>')
        body.append(txt(['Detect','Prevent','Recover'],x+110,y0+980,64,GREEN,900,leading=1.5))
    body.append(card(1040,4500,5920,520,'Control coverage',['공격 단계마다 예방·탐지·복구 통제를 나란히 배치해 공백을 찾습니다.'],YELLOW))
    return base_svg('Attack Chain Control Map', '공격 단계와 보안 통제 커버리지를 함께 표시', '\n'.join(body))

# 18 Dependency graph
def svg_dependency():
    body=[]; nodes=[('A',4000,1900,ACCENT),('B',2700,2700,BLUE),('C',5300,2700,GREEN),('D',2200,3900,ORANGE),('E',4000,4100,YELLOW),('F',5800,3900,INK),('G',4000,5050,BLUE)]
    edges=[('A','B'),('A','C'),('B','D'),('B','E'),('C','E'),('C','F'),('E','G'),('F','G')]
    crit={('A','C'),('C','F'),('F','G')}
    pos={n:(x,y,c) for n,x,y,c in nodes}
    # non-critical edges first, critical path (accent, thicker) drawn on top to match the legend
    for a,b in sorted(edges,key=lambda e:e in crit):
        x1,y1,_=pos[a]; x2,y2,_=pos[b]
        is_c=(a,b) in crit
        body.append(arrow(x1,y1+80,x2,y2-80, ACCENT if is_c else LINE, 26 if is_c else 12))
    for n,x,y,c in nodes:
        body.append(f'<circle cx="{x}" cy="{y}" r="180" fill="{c}" stroke="#fff" stroke-width="16" class="shadow"/>')
        body.append(txt(n,x,y+46,130,'#fff' if c!=YELLOW else INK,950,anchor='middle'))
    body.append(card(850,1650,1600,620,'Critical path',['A→C→F→G','blast radius high'],ACCENT))
    body.append(card(5550,1650,1600,620,'Owner view',['팀별 책임','변경 영향'],BLUE))
    return base_svg('Dependency Graph', '서비스·작업·모듈 의존성과 영향 경로를 표시', '\n'.join(body))

# 19 Taxonomy tree
def svg_taxonomy():
    body=[]; root=(4000,1700)
    body.append(card(3340,1500,1320,420,'Knowledge Base','root',ACCENT,80))
    cats=[('Policy',1700,2750,BLUE),('Product',4000,2750,GREEN),('Ops',6300,2750,ORANGE)]
    for label,x,y,c in cats:
        body.append(arrow(4000,1920,x,y-220,INK,12))
        body.append(card(x-520,y-220,1040,440,label,'category',c,80))
        for j in range(3):
            cx=x-620+j*620; cy=3900+j*80
            body.append(arrow(x,y,cx,cy-160,LINE,10))
            # h=420 (was 320): card() places title at y+160 and desc at y+315, so a 320-tall box pushed the 'topic' label below its bottom edge
            body.append(card(cx-260,cy-160,560,420,f'{label[:2]}-{j+1}','topic',c,52))
    body.append(card(980,4920,6000,420,'Taxonomy rule',['상위 개념 → 카테고리 → 토픽 → 문서로 이어지는 탐색 구조를 보여줍니다.'],YELLOW))
    return base_svg('Taxonomy Tree Map', '지식 분류 체계를 계층 트리로 표현', '\n'.join(body))

# 20 Evidence pyramid / causal loop hybrid
def svg_evidence_pyramid():
    body=[]; x=4000; y0=1650; levels=[('Meta analysis',1200,ACCENT),('Controlled study',2300,BLUE),('Case study',3400,GREEN),('Expert opinion',4500,ORANGE),('Anecdote',5600,YELLOW)]
    for i,(label,w,c) in enumerate(levels):
        y=y0+i*620; h=520
        body.append(f'<path d="M{x-w/2} {y+h} L{x+w/2} {y+h} L{x+w/2-260} {y} L{x-w/2+260} {y} Z" fill="{c}" stroke="#fff" stroke-width="12"/>')
        body.append(txt(label,x,y+325,92,'#fff' if c!=YELLOW else INK,950,anchor='middle'))
    # side cards moved up to the empty corners beside the apex so they never overlap the base tier
    body.append(card(680,1760,1760,700,'Confidence',['위로 갈수록','근거 강도 증가'],ACCENT))
    body.append(card(5560,1760,1760,700,'Use case',['리서치 요약','정책 판단'],BLUE))
    return base_svg('Evidence Pyramid', '근거 수준과 신뢰도를 계층형으로 설명', '\n'.join(body))

ADDITIONAL=[
 ('11-sankey-alluvial-flow.svg','Sankey / Alluvial Flow',svg_sankey,'범주 간 흐름과 전환량'),
 ('12-treemap-priority-portfolio.svg','Treemap Priority Portfolio',svg_treemap,'포트폴리오 규모·우선순위'),
 ('13-radial-ecosystem-network.svg','Radial Ecosystem Network',svg_radial_network,'생태계·이해관계자 네트워크'),
 ('14-conversion-funnel.svg','Conversion Funnel',svg_funnel,'전환 퍼널·이탈 분석'),
 ('15-user-journey-map.svg','User Journey Map',svg_journey,'사용자 여정·Pain·Opportunity'),
 ('16-service-blueprint-lanes.svg','Service Blueprint Lanes',svg_blueprint,'고객 경험과 내부 운영 lane'),
 ('17-attack-chain-control-map.svg','Attack Chain Control Map',svg_attack_chain,'공격 체인과 통제 커버리지'),
 ('18-dependency-graph.svg','Dependency Graph',svg_dependency,'의존성·영향 경로'),
 ('19-taxonomy-tree-map.svg','Taxonomy Tree Map',svg_taxonomy,'지식 분류·탐색 구조'),
 ('20-evidence-pyramid.svg','Evidence Pyramid',svg_evidence_pyramid,'근거 수준·신뢰도 계층'),
]
FIRST10=[
 ('01-risk-heatmap.svg','Risk Heatmap','리스크/정책/보안 우선순위 매트릭스'),('02-maturity-capability-matrix.svg','Maturity Capability Matrix','성숙도·역량 진단'),('03-swimlane-request-flow.svg','Numbered Swimlane Request Flow','API/OAuth/webhook 요청 흐름'),('04-layered-architecture-flow.svg','Layered Architecture Flow','시스템/클라우드 아키텍처'),('05-transformation-roadmap-swimlane.svg','Transformation Roadmap Swimlane','전환 로드맵/실행계획'),('06-slope-change-chart.svg','Slope Change Chart','전후 변화/순위 변화'),('07-small-multiples-grid.svg','Small Multiples Grid','여러 세그먼트 추세 비교'),('08-component-api-anatomy.svg','Component/API Anatomy','컴포넌트/API 구조 설명'),('09-value-proposition-map.svg','Value Proposition Map','고객 문제와 제품 가치 매핑'),('10-editorial-briefing-card-hub.svg','Editorial Briefing Card Hub','뉴스 요약/브리핑 카드 허브')]

def ensure_first10(media):
    if SRC10.exists():
        for fn,_,_ in FIRST10:
            src=SRC10/fn; dst=media/fn
            if src.exists() and not dst.exists(): shutil.copy2(src,dst)

def gallery_html():
    demos=FIRST10+[(fn,title,desc) for fn,title,_,desc in ADDITIONAL]
    cards=[]
    for fn,title,desc in demos:
        cards.append(f'''<article class="demo-card"><a href="../media/svg-template-demos/{fn}"><img src="../media/svg-template-demos/{fn}" width="8000" height="6000" alt="{esc(title)} SVG demo thumbnail"></a><div class="demo-body"><div class="mode-label">SVG TEMPLATE</div><h3><a href="../media/svg-template-demos/{fn}">{esc(title)}</a></h3><p>{esc(desc)}</p><p><a class="open-link" href="../media/svg-template-demos/{fn}">SVG 직접 열기 →</a></p></div></article>''')
    return f'''<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>SVG 템플릿 20종 데모 갤러리</title><meta name="description" content="adaptive-html-final에 도입할 20가지 8000×6000 SVG 인포그래픽 템플릿 데모."><link rel="preconnect" href="https://cdn.jsdelivr.net"><link href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.css" rel="stylesheet"><style>:root{{--bg:#f5f5f0;--ink:#1a1a1a;--soft:#4a4a4a;--mute:#7a7a7a;--line:#d8d8d0;--card:#fff;--accent:#e63946;--yellow:#ffd400;--sans:"Pretendard Variable",Pretendard,system-ui,sans-serif}}*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--ink);font-family:var(--sans);line-height:1.75;letter-spacing:-.012em}}a{{color:inherit;text-underline-offset:3px}}.skip{{position:absolute;left:-999px;top:8px;background:#111;color:#fff;padding:10px 14px;border-radius:8px}}.skip:focus{{left:8px}}.page{{width:min(1180px,calc(100% - 44px));margin:0 auto;padding:58px 0 100px}}.header{{border-bottom:1px solid var(--line);padding-bottom:32px;margin-bottom:32px}}.kicker{{font-size:12px;letter-spacing:.18em;color:var(--accent);font-weight:900;text-transform:uppercase}}h1{{font-size:clamp(32px,4vw,48px);line-height:1.25;margin:12px 0;font-family:Georgia,serif}}.sub{{color:var(--soft);font-size:16px;max-width:860px}}.meta{{display:flex;gap:8px;flex-wrap:wrap;margin-top:20px}}.meta span{{border:1px solid var(--line);background:#fff;border-radius:999px;padding:5px 10px;font-size:12px;color:var(--mute)}}.grid{{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:18px}}.demo-card{{background:#fff;border:1px solid var(--line);border-radius:14px;overflow:hidden}}.demo-card img{{display:block;width:100%;height:auto;background:#f5f5f0;border-bottom:1px solid var(--line)}}.demo-body{{padding:18px 20px}}.mode-label{{font-size:11px;color:var(--accent);font-weight:900;letter-spacing:.14em}}h3{{margin:5px 0 6px;font-size:20px}}p{{color:var(--soft);font-size:14.5px;margin:0 0 10px}}.open-link{{font-weight:800;color:var(--accent)}}.nav{{display:flex;justify-content:space-between;font-size:13px;color:var(--mute);margin-bottom:24px}}.note{{background:#111;color:#fff;border-radius:14px;padding:24px;margin-top:32px}}.note p{{color:#ddd}}@media(max-width:760px){{.grid{{grid-template-columns:1fr}}.page{{width:min(100% - 32px,1180px);padding-top:38px}}}}</style></head><body><a class="skip" href="#main">본문 바로가기</a><main id="main" class="page"><nav class="nav"><a href="../index.html">← 쇼케이스 홈</a><span>20 SVG Template Demos · 8000×6000</span></nav><header class="header"><div class="kicker">Adaptive HTML Final · Visual Template Expansion</div><h1>SVG 템플릿 20종 데모 갤러리</h1><p class="sub">기존 10종에 추가 10종을 더해 만든 실제 8000×6000 SVG 데모입니다. 각 카드는 직접 SVG 파일로 열 수 있습니다.</p><div class="meta"><span>총 20개 SVG</span><span>원본 8000×6000</span><span>외부 JS 없음</span><span>생성일 2026-05-30</span></div></header><section class="grid">{''.join(cards)}</section><section class="note"><h2>추가 10종</h2><p>Sankey, Treemap, Radial Network, Funnel, Journey Map, Service Blueprint, Attack Chain, Dependency Graph, Taxonomy Tree, Evidence Pyramid를 추가했습니다.</p></section></main></body></html>'''

for root in ROOTS:
    media=root/'media/svg-template-demos'; pages=root/'pages'
    media.mkdir(parents=True, exist_ok=True); pages.mkdir(parents=True, exist_ok=True)
    ensure_first10(media)
    for fn,_,func,_ in ADDITIONAL:
        (media/fn).write_text(func())
    (pages/'15-svg-template-gallery.html').write_text(gallery_html())
    print('updated', root)
    # update index link label if present
    idx=root/'index.html'
    if idx.exists():
        s=idx.read_text()
        if '15-svg-template-gallery.html' not in s:
            block='''\n  <section class="hero-index"><h2><span class="num">4</span>추가 데모: SVG 템플릿 20종 갤러리</h2><p class="h2-sub">리스크, 성숙도, 요청 흐름, 아키텍처, 로드맵 등 SVG 패턴 모음입니다.</p><p><a href="pages/15-svg-template-gallery.html"><strong>SVG 템플릿 20종 데모 갤러리 열기 →</strong></a></p><p>모든 SVG는 8000×6000 원본으로 생성되어 직접 열어볼 수 있습니다.</p></section>\n'''
            s=s.replace('  <section class="try"><div class="label">Verification</div>', block+'  <section class="try"><div class="label">Verification</div>')
        s=s.replace('SVG 템플릿 10종 데모 갤러리', 'SVG 템플릿 20종 데모 갤러리').replace('SVG 템플릿 10종 갤러리', 'SVG 템플릿 20종 갤러리').replace('총 10개 SVG', '총 20개 SVG')
        idx.write_text(s)
