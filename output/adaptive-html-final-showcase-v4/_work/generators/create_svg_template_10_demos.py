from pathlib import Path
from html import escape
import math

ROOT = Path('output/adaptive-html-final-showcase')
MEDIA = ROOT / 'media' / 'svg-template-demos'
PAGES = ROOT / 'pages'
MEDIA.mkdir(parents=True, exist_ok=True)
PAGES.mkdir(parents=True, exist_ok=True)
W, H = 8000, 6000
ACCENT = '#e63946'
YELLOW = '#ffd400'
BLUE = '#3a6280'
GREEN = '#2a7d5a'
ORANGE = '#d99a38'
INK = '#1a1a1a'
SOFT = '#4a4a4a'
MUTE = '#7a7a7a'
LINE = '#d8d8d0'
BG = '#f5f5f0'
CARD = '#ffffff'


def esc(s):
    return escape(str(s), quote=True)


def txt(lines, x, y, size=100, fill=INK, weight=700, anchor='start', leading=1.25):
    if isinstance(lines, str):
        lines=[lines]
    out=[f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" font-weight="{weight}" text-anchor="{anchor}">']
    for i,line in enumerate(lines):
        dy=0 if i==0 else int(size*leading)
        out.append(f'<tspan x="{x}" dy="{dy}">{esc(line)}</tspan>')
    out.append('</text>')
    return '\n'.join(out)


def header(title, subtitle, kicker='SVG TEMPLATE DEMO'):
    return '\n'.join([
        f'<text x="560" y="620" font-size="118" fill="{ACCENT}" font-weight="950" letter-spacing="22">{esc(kicker)}</text>',
        txt(title, 560, 980, 285, INK, 950, leading=1.06),
        txt(subtitle, 570, 1280, 116, SOFT, 580, leading=1.25),
    ])


def base_svg(title, subtitle, body, footer='8000×6000 SVG · adaptive template demo'):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="title desc">
<title id="title">{esc(title)}</title>
<desc id="desc">{esc(subtitle)}</desc>
<style>
  text {{ font-family: Pretendard, -apple-system, BlinkMacSystemFont, "Noto Sans KR", Arial, sans-serif; }}
  .shadow {{ filter: drop-shadow(0 20px 32px rgba(26,26,26,.08)); }}
</style>
<rect width="8000" height="6000" fill="{BG}"/>
<circle cx="7230" cy="760" r="520" fill="#fce4e6" opacity="0.72"/>
<circle cx="650" cy="5350" r="760" fill="#f0f4f8" opacity="0.88"/>
{header(title, subtitle)}
{body}
<text x="7440" y="5600" font-size="84" text-anchor="end" fill="{MUTE}" font-weight="750">{esc(footer)}</text>
</svg>'''


def card(x,y,w,h,title,desc='',accent=ACCENT,rx=96):
    parts=[f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{CARD}" stroke="{LINE}" stroke-width="12" class="shadow"/>',
           f'<rect x="{x}" y="{y}" width="28" height="{h}" rx="14" fill="{accent}"/>',
           txt(title,x+110,y+165,112,INK,900)]
    if desc:
        if isinstance(desc,str): desc=[desc]
        parts.append(txt(desc,x+110,y+325,74,SOFT,560,leading=1.28))
    return '\n'.join(parts)


def pill(x,y,text,fill='#fff',stroke=LINE,color=SOFT):
    return f'<rect x="{x}" y="{y}" width="{len(text)*43+120}" height="118" rx="59" fill="{fill}" stroke="{stroke}" stroke-width="8"/><text x="{x+60}" y="{y+76}" font-size="58" fill="{color}" font-weight="800">{esc(text)}</text>'


def arrow(x1,y1,x2,y2,color=INK,w=16):
    angle=math.atan2(y2-y1,x2-x1)
    size=58
    p1=(x2-size*math.cos(angle)-size*.55*math.sin(angle), y2-size*math.sin(angle)+size*.55*math.cos(angle))
    p2=(x2-size*math.cos(angle)+size*.55*math.sin(angle), y2-size*math.sin(angle)-size*.55*math.cos(angle))
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{w}" stroke-linecap="round"/><polygon points="{x2},{y2} {p1[0]},{p1[1]} {p2[0]},{p2[1]}" fill="{color}"/>'


def svg_risk_heatmap():
    colors=['#eef7f1','#d8efdf','#ffe9a3','#f7c56b','#e63946']
    body=[]
    x0,y0=1160,1660; cell=610
    body.append(txt('가능성', x0+cell*2.5, y0-230, 100, INK, 900, anchor='middle'))
    body.append(txt('영향도', x0-360, y0+cell*2.5, 100, INK, 900, anchor='middle'))
    for r in range(5):
        for c in range(5):
            score=r+c
            fill=colors[min(4, max(0, score//2))]
            x=x0+c*cell; y=y0+(4-r)*cell
            body.append(f'<rect x="{x}" y="{y}" width="{cell-18}" height="{cell-18}" rx="48" fill="{fill}" stroke="#ffffff" stroke-width="10"/>')
            body.append(f'<text x="{x+cell/2}" y="{y+cell/2+32}" font-size="86" fill="{INK}" text-anchor="middle" font-weight="900">{r+1}×{c+1}</text>')
    risks=[('R1',x0+cell*3.5,y0+cell*.5,ACCENT),('R2',x0+cell*2.5,y0+cell*1.5,ORANGE),('R3',x0+cell*4.5,y0+cell*2.5,ACCENT),('R4',x0+cell*1.5,y0+cell*3.5,GREEN)]
    for label,x,y,col in risks:
        body.append(f'<circle cx="{x}" cy="{y}" r="95" fill="{col}" stroke="#fff" stroke-width="12"/>')
        body.append(txt(label,x,y+30,74,'#fff',950,anchor='middle'))
    body.append(card(4800,1780,2100,1850,'Risk Legend',['R1 법적 노출','R2 데이터 품질','R3 공급망','R4 운영 공백'],ACCENT))
    body.append(card(4800,3820,2100,900,'Decision Rule',['High 영역은 즉시 완화','Mid 영역은 owner 지정'],YELLOW))
    return base_svg('Risk Heatmap', '가능성×영향도 기반 리스크 우선순위 매트릭스', '\n'.join(body))


def svg_maturity_matrix():
    levels=['Nascent','Emerging','Defined','Managed','Pioneering']
    caps=['거버넌스','데이터','보안','운영','검증','교육']
    x0,y0=1360,1680; cw,ch=1030,500
    body=[]
    for i,l in enumerate(levels):
        body.append(txt(l,x0+i*cw+cw/2,y0-115,62,INK,850,anchor='middle'))
    for r,cap in enumerate(caps):
        body.append(txt(cap,x0-160,y0+r*ch+ch/2+24,76,INK,900,anchor='end'))
        for c in range(5):
            fill=['#fff','#f8f8f4','#eef7f1','#ffe9a3','#ffd400'][c]
            body.append(f'<rect x="{x0+c*cw}" y="{y0+r*ch}" width="{cw-22}" height="{ch-22}" rx="44" fill="{fill}" stroke="{LINE}" stroke-width="8"/>')
    markers=[(0,1),(1,2),(2,2),(3,3),(4,1),(5,2)]
    targets=[(0,3),(1,4),(2,4),(3,4),(4,3),(5,3)]
    for r,c in markers:
        body.append(f'<circle cx="{x0+c*cw+cw/2}" cy="{y0+r*ch+ch/2}" r="70" fill="{ACCENT}"/>')
        body.append(txt('현재',x0+c*cw+cw/2,y0+r*ch+ch/2+22,44,'#fff',900,anchor='middle'))
    for r,c in targets:
        body.append(f'<rect x="{x0+c*cw+cw/2-82}" y="{y0+r*ch+ch/2-62}" width="164" height="124" rx="62" fill="{INK}"/>')
        body.append(txt('목표',x0+c*cw+cw/2,y0+r*ch+ch/2+18,44,'#fff',900,anchor='middle'))
    body.append(card(870,4920,6060,420,'사용법',['행은 역량, 열은 성숙도입니다. 현재와 목표의 거리로 로드맵 우선순위를 정합니다.'],BLUE))
    return base_svg('Maturity Capability Matrix', '역량별 현재/목표 성숙도 차이를 한 장으로 진단', '\n'.join(body))


def svg_swimlane():
    lanes=['User','App','Auth Server','API']
    x0,y0=820,1620; lane_h=760; w=6400
    body=[]; cyl={}
    for i,lane in enumerate(lanes):
        y=y0+i*lane_h; cy=y+(lane_h-32)//2; cyl[lane]=cy
        body.append(f'<rect x="{x0}" y="{y}" width="{w}" height="{lane_h-32}" rx="72" fill="#fff" stroke="{LINE}" stroke-width="10"/>')
        body.append(f'<rect x="{x0}" y="{y}" width="760" height="{lane_h-32}" rx="72" fill="#f8f8f4" stroke="{LINE}" stroke-width="0"/>')
        body.append(txt(lane,x0+380,cy+24,86,INK,950,anchor='middle'))
    U,A,S,P=cyl['User'],cyl['App'],cyl['Auth Server'],cyl['API']
    # clean left-to-right staircase that visits every lane (User→App→Auth→App→API→App); label sits on the segment leaving each node
    seq=[(1,1700,U,'로그인 요청'),(2,2780,A,'인증 요청'),(3,3860,S,'토큰 발급'),(4,4940,A,'API 호출'),(5,6020,P,'응답'),(6,6700,A,'')]
    for k in range(len(seq)-1):
        n,x1,y1,label=seq[k]; _,x2,y2,_=seq[k+1]
        body.append(arrow(x1,y1,x2,y2,ACCENT if n in (1,4) else INK,14))
        if label: body.append(pill((x1+x2)//2-240,(y1+y2)//2-70,label,'#fff',LINE,SOFT))
    for n,x,y,_ in seq:
        body.append(f'<circle cx="{x}" cy="{y}" r="70" fill="{YELLOW}" stroke="{INK}" stroke-width="10"/>')
        body.append(txt(str(n),x,y+23,60,INK,950,anchor='middle'))
    return base_svg('Numbered Swimlane Request Flow', '행위자별 요청·응답 흐름을 번호 화살표로 설명', '\n'.join(body))


def svg_layered_arch():
    body=[]
    layers=[('Edge',1540,BLUE),('Application',2680,GREEN),('Data',3820,ORANGE)]
    for name,y,col in layers:
        body.append(f'<rect x="820" y="{y}" width="6360" height="880" rx="110" fill="#fff" stroke="{LINE}" stroke-width="12"/>')
        body.append(f'<text x="1120" y="{y+150}" font-size="86" fill="{col}" font-weight="950">{name}</text>')
    nodes=[('CDN',1900,1950,BLUE),('Gateway',3300,1950,BLUE),('Web App',1900,3090,GREEN),('API',3300,3090,GREEN),('Worker',4700,3090,GREEN),('Cache',2300,4230,ORANGE),('Database',4100,4230,ORANGE),('Object Store',5900,4230,ORANGE)]
    for title,x,y,col in nodes:
        body.append(card(x-440,y-180,880,360,title,'',col,70))
    for x1,y1,x2,y2 in [(2340,1950,2860,1950),(3300,2130,3300,2910),(2340,3090,2860,3090),(3740,3090,4260,3090),(3300,3270,2600,4050),(4700,3270,4100,4050),(5140,3090,5900,4050)]:
        body.append(arrow(x1,y1,x2,y2,INK,14))
    body.append(card(850,4920,6350,420,'Architecture Reading',['Boundary group은 책임 범위를, 번호형 path는 요청 흐름을 보여줍니다.'],ACCENT))
    return base_svg('Layered Architecture Flow', '서비스 노드와 경계 그룹을 함께 보여주는 아키텍처 SVG', '\n'.join(body))


def svg_roadmap():
    phases=['Assess','Design','Prototype','Scale','Operate']
    lanes=['Product','Data','Security']
    x0,y0=1020,1650; pw=1180; lh=760
    body=[]
    for i,p in enumerate(phases):
        x=x0+i*pw
        body.append(f'<rect x="{x}" y="{y0-220}" width="{pw-80}" height="160" rx="80" fill="{[ACCENT,BLUE,GREEN,ORANGE,YELLOW][i]}"/>')
        body.append(txt(p,x+(pw-80)/2,y0-115,70,'#fff' if i!=4 else INK,950,anchor='middle'))
    for r,lane in enumerate(lanes):
        y=y0+r*lh
        body.append(txt(lane,760,y+260,78,INK,950,anchor='end'))
        body.append(f'<line x1="{x0}" y1="{y+260}" x2="{x0+pw*5-80}" y2="{y+260}" stroke="{LINE}" stroke-width="16"/>')
        for i in range(5):
            x=x0+i*pw+420
            body.append(f'<circle cx="{x}" cy="{y+260}" r="72" fill="#fff" stroke="{[ACCENT,BLUE,GREEN,ORANGE,INK][i]}" stroke-width="18"/>')
            body.append(txt(str(i+1),x,y+285,58,INK,950,anchor='middle'))
    body.append(card(1080,4200,5840,760,'Milestone Rule',['각 phase는 산출물, owner, 검증 기준을 가져야 합니다.','lane은 조직/기술/보안처럼 병렬 책임을 보여줍니다.'],GREEN))
    return base_svg('Transformation Roadmap Swimlane', '단계와 책임 lane을 함께 표현하는 실행 로드맵', '\n'.join(body))


def svg_slope():
    body=[]
    x1,x2=1780,5800; y_top,y_bot=1700,4550
    body.append(txt('Before',x1,y_top-220,110,INK,950,anchor='middle'))
    body.append(txt('After',x2,y_top-220,110,INK,950,anchor='middle'))
    items=[('보안',82,94,ACCENT),('속도',66,88,GREEN),('비용',72,58,ORANGE),('품질',55,79,BLUE),('운영',40,72,INK)]
    for label,a,b,col in items:
        ya=y_bot-(a/100)*(y_bot-y_top); yb=y_bot-(b/100)*(y_bot-y_top)
        body.append(f'<line x1="{x1}" y1="{ya}" x2="{x2}" y2="{yb}" stroke="{col}" stroke-width="18" stroke-linecap="round" opacity="0.88"/>')
        body.append(f'<circle cx="{x1}" cy="{ya}" r="54" fill="{col}"/>')
        body.append(f'<circle cx="{x2}" cy="{yb}" r="54" fill="{col}"/>')
        body.append(txt(f'{label} {a}',x1-150,ya+24,64,INK,850,anchor='end'))
        body.append(txt(f'{b}',x2+140,yb+24,64,INK,850))
    body.append(card(2820,4620,2400,520,'When to use',['전후 변화, 순위 변화, 정책 효과를 한눈에 보여줄 때'],YELLOW))
    return base_svg('Slope Change Chart', '두 시점 사이의 변화 방향과 크기를 강조', '\n'.join(body))


def svg_small_multiples():
    body=[]
    x0,y0=760,1580; cw,ch=2100,980; gapx,gapy=260,240
    labels=['Korea','US','EU','Japan','India','Brazil']
    for i,label in enumerate(labels):
        col=i%3; row=i//3; x=x0+col*(cw+gapx); y=y0+row*(ch+gapy)
        body.append(f'<rect x="{x}" y="{y}" width="{cw}" height="{ch}" rx="90" fill="#fff" stroke="{LINE}" stroke-width="12"/>')
        body.append(txt(label,x+140,y+150,82,INK,950))
        # axes and sparkline
        body.append(f'<line x1="{x+160}" y1="{y+760}" x2="{x+1900}" y2="{y+760}" stroke="{LINE}" stroke-width="10"/>')
        pts=[]
        for k in range(7):
            px=x+220+k*260
            py=y+700-((math.sin((i+1)*.6+k*.7)+1)/2*360 + k*18)
            pts.append((px,py))
        d=' '.join(f'{px},{py}' for px,py in pts)
        body.append(f'<polyline points="{d}" fill="none" stroke="{[ACCENT,BLUE,GREEN,ORANGE,INK,YELLOW][i]}" stroke-width="18" stroke-linecap="round" stroke-linejoin="round"/>')
        for px,py in pts[-2:]: body.append(f'<circle cx="{px}" cy="{py}" r="34" fill="{ACCENT}"/>')
    return base_svg('Small Multiples Grid', '동일한 축과 카드로 여러 세그먼트의 패턴을 비교', '\n'.join(body))


def svg_component_anatomy():
    body=[]
    # central mock
    body.append(f'<rect x="2700" y="1900" width="2600" height="1500" rx="160" fill="#fff" stroke="{LINE}" stroke-width="16" class="shadow"/>')
    body.append(f'<rect x="3040" y="2260" width="1920" height="280" rx="72" fill="{YELLOW}" stroke="{INK}" stroke-width="12"/>')
    body.append(txt('Primary Action',4000,2445,100,INK,950,anchor='middle'))
    body.append(f'<rect x="3040" y="2740" width="1920" height="300" rx="60" fill="#f8f8f4" stroke="{LINE}" stroke-width="10"/>')
    body.append(txt('Input / property',4000,2935,82,SOFT,700,anchor='middle'))
    callouts=[('A','Container',1840,1880,3040,2260),('B','Label',5840,2220,4960,2380),('C','State',1840,3280,3040,2890),('D','Token',5900,3380,4960,3040)]
    for tag,label,x,y,tx,ty in callouts:
        body.append(arrow(x+220,y+70,tx,ty,ACCENT,10))
        body.append(f'<circle cx="{x}" cy="{y}" r="92" fill="{ACCENT}"/>')
        body.append(txt(tag,x,y+30,78,'#fff',950,anchor='middle'))
        body.append(txt(label,x+140,y+28,80,INK,900))
    body.append(card(1120,4200,5760,760,'Anatomy Card',['중앙 mock, A/B/C callout, 속성/상태 표를 조합합니다.','UI 컴포넌트뿐 아니라 API resource 설명에도 사용 가능합니다.'],BLUE))
    return base_svg('Component / API Anatomy', '중앙 객체와 콜아웃으로 구조를 설명하는 템플릿', '\n'.join(body))


def svg_value_map():
    body=[]
    # card height sized to content (was 3300 → mostly empty); keeps proportion balanced
    body.append(card(760,1860,2800,2280,'Customer Profile',['Jobs: 승인·검토·공유','Pains: 불확실성·반복 작업','Gains: 빠른 판단·증빙'],BLUE))
    body.append(card(4440,1860,2800,2280,'Value Map',['Products: 템플릿·자동 SVG','Pain relievers: 검수 게이트','Gain creators: 즉시 이해'],GREEN))
    for y in [2280,2760,3240,3720]:
        body.append(arrow(3600,y,4440,y,ACCENT,16))
    body.append(f'<circle cx="4000" cy="3000" r="340" fill="{YELLOW}" stroke="{INK}" stroke-width="16"/>')
    body.append(txt(['FIT'],4000,3035,150,INK,950,anchor='middle'))
    return base_svg('Value Proposition Map', '고객 문제와 제품 가치를 좌우로 매핑', '\n'.join(body))


def svg_editorial_hub():
    body=[]
    body.append(card(620,1660,3000,1600,'Featured Deep Dive',['메인 기사 요약','핵심 수치·출처·읽는 시간'],ACCENT))
    body.append(card(3900,1660,2920,760,'Morning Briefing',['오늘 꼭 알아야 할 5가지'],YELLOW))
    body.append(card(3900,2500,2920,760,'Data Wire',['차트·속보·업데이트'],BLUE))
    topics=[('AI','Policy'),('Security','Ops'),('Market','Signal'),('Research','Note')]
    x0,y0=620,3580
    for i,(a,b) in enumerate(topics):
        x=x0+i*1660
        body.append(card(x,y0,1460,880,a,[b,'3 links','updated today'],[ACCENT,BLUE,GREEN,ORANGE][i],70))
    body.append(f'<rect x="620" y="4860" width="6260" height="420" rx="110" fill="{INK}"/>')
    body.append(txt('Newsletter CTA · 한 번에 읽는 주간 브리핑',860,5125,110,'#fff',900))
    body.append(f'<rect x="5750" y="4960" width="920" height="220" rx="110" fill="{YELLOW}"/>')
    body.append(txt('구독',6210,5100,86,INK,950,anchor='middle'))
    return base_svg('Editorial Briefing Card Hub', '뉴스·리서치 허브용 카드 배치 템플릿', '\n'.join(body))

DEMOS=[
 ('01-risk-heatmap.svg', 'Risk Heatmap', svg_risk_heatmap, '리스크/정책/보안 우선순위 매트릭스'),
 ('02-maturity-capability-matrix.svg', 'Maturity Capability Matrix', svg_maturity_matrix, '성숙도·역량 진단'),
 ('03-swimlane-request-flow.svg', 'Numbered Swimlane Request Flow', svg_swimlane, 'API/OAuth/webhook 요청 흐름'),
 ('04-layered-architecture-flow.svg', 'Layered Architecture Flow', svg_layered_arch, '시스템/클라우드 아키텍처'),
 ('05-transformation-roadmap-swimlane.svg', 'Transformation Roadmap Swimlane', svg_roadmap, '전환 로드맵/실행계획'),
 ('06-slope-change-chart.svg', 'Slope Change Chart', svg_slope, '전후 변화/순위 변화'),
 ('07-small-multiples-grid.svg', 'Small Multiples Grid', svg_small_multiples, '여러 세그먼트 추세 비교'),
 ('08-component-api-anatomy.svg', 'Component/API Anatomy', svg_component_anatomy, '컴포넌트/API 구조 설명'),
 ('09-value-proposition-map.svg', 'Value Proposition Map', svg_value_map, '고객 문제와 제품 가치 매핑'),
 ('10-editorial-briefing-card-hub.svg', 'Editorial Briefing Card Hub', svg_editorial_hub, '뉴스 요약/브리핑 카드 허브'),
]

for filename,_,fn,_ in DEMOS:
    (MEDIA/filename).write_text(fn())

# Gallery page
cards=[]
for filename,title,_,desc in DEMOS:
    cards.append(f'''<article class="demo-card">
  <a href="../media/svg-template-demos/{filename}"><img src="../media/svg-template-demos/{filename}" width="8000" height="6000" alt="{esc(title)} SVG demo thumbnail"></a>
  <div class="demo-body"><div class="mode-label">SVG TEMPLATE</div><h3><a href="../media/svg-template-demos/{filename}">{esc(title)}</a></h3><p>{esc(desc)}</p><p><a class="open-link" href="../media/svg-template-demos/{filename}">SVG 직접 열기 →</a></p></div>
</article>''')

gallery=f'''<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>SVG 템플릿 10종 데모 갤러리</title>
<meta name="description" content="adaptive-html-final에 도입할 10가지 8000×6000 SVG 인포그래픽 템플릿 데모.">
<link rel="preconnect" href="https://cdn.jsdelivr.net">
<link href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.css" rel="stylesheet">
<style>
:root{{--bg:#f5f5f0;--ink:#1a1a1a;--soft:#4a4a4a;--mute:#7a7a7a;--line:#d8d8d0;--card:#fff;--accent:#e63946;--yellow:#ffd400;--serif:Georgia,serif;--sans:"Pretendard Variable",Pretendard,system-ui,sans-serif}}
*{{box-sizing:border-box}} body{{margin:0;background:var(--bg);color:var(--ink);font-family:var(--sans);line-height:1.75;letter-spacing:-.012em}} a{{color:inherit;text-underline-offset:3px}} .skip{{position:absolute;left:-999px;top:8px;background:#111;color:#fff;padding:10px 14px;border-radius:8px}}.skip:focus{{left:8px}} .page{{width:min(1180px,calc(100% - 44px));margin:0 auto;padding:58px 0 100px}} .header{{border-bottom:1px solid var(--line);padding-bottom:32px;margin-bottom:32px}} .kicker{{font-size:12px;letter-spacing:.18em;color:var(--accent);font-weight:900;text-transform:uppercase}} h1{{font-family:var(--serif);font-size:clamp(32px,4vw,48px);line-height:1.25;margin:12px 0}} .sub{{color:var(--soft);font-size:16px;max-width:860px}} .meta{{display:flex;gap:8px;flex-wrap:wrap;margin-top:20px}}.meta span{{border:1px solid var(--line);background:#fff;border-radius:999px;padding:5px 10px;font-size:12px;color:var(--mute)}} .grid{{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:18px}} .demo-card{{background:#fff;border:1px solid var(--line);border-radius:14px;overflow:hidden}} .demo-card img{{display:block;width:100%;height:auto;background:#f5f5f0;border-bottom:1px solid var(--line)}} .demo-body{{padding:18px 20px}} .mode-label{{font-size:11px;color:var(--accent);font-weight:900;letter-spacing:.14em}} h3{{margin:5px 0 6px;font-size:20px}} p{{color:var(--soft);font-size:14.5px;margin:0 0 10px}} .open-link{{font-weight:800;color:var(--accent)}} .nav{{display:flex;justify-content:space-between;font-size:13px;color:var(--mute);margin-bottom:24px}} .note{{background:#111;color:#fff;border-radius:14px;padding:24px;margin-top:32px}} .note p{{color:#ddd}} @media(max-width:760px){{.grid{{grid-template-columns:1fr}}.page{{width:min(100% - 32px,1180px);padding-top:38px}}}}
</style>
</head>
<body>
<a class="skip" href="#main">본문 바로가기</a>
<main id="main" class="page">
<nav class="nav"><a href="../index.html">← 쇼케이스 홈</a><span>10 SVG Template Demos · 8000×6000</span></nav>
<header class="header"><div class="kicker">Adaptive HTML Final · Visual Template Expansion</div><h1>SVG 템플릿 10종 데모 갤러리</h1><p class="sub">병렬 레퍼런스 조사 결과를 바탕으로 만든 실제 8000×6000 SVG 데모입니다. 각 카드는 직접 SVG 파일로 열 수 있습니다.</p><div class="meta"><span>총 10개 SVG</span><span>원본 8000×6000</span><span>외부 JS 없음</span><span>생성일 2026-05-30</span></div></header>
<section class="grid">
{''.join(cards)}
</section>
<section class="note"><h2>도입 우선순위</h2><p>1차 도입 추천: risk-heatmap, maturity-capability-matrix, swimlane-request-flow. 이후 architecture, roadmap, slope/small-multiples, anatomy/value/editorial hub 순서로 확장하면 됩니다.</p></section>
</main>
</body>
</html>'''
(PAGES/'15-svg-template-gallery.html').write_text(gallery)
print('created', PAGES/'15-svg-template-gallery.html')
for f,_,_,_ in DEMOS:
    print(f, (MEDIA/f).stat().st_size)
