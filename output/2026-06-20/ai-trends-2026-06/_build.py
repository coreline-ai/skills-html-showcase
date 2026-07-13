#!/usr/bin/env python3
# 하이브리드 빌더: x-ai-trend-collector(웹검색 fallback 수집) -> adaptive-html-final 5.10.5 seo_dashboard.
# 검증된 seo 예제 scaffold(인라인 코어 CSS·해시·8테마바) 재사용, <main id="main">만 교체.
import json, re, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[3]
SKILL = ROOT / "skills/adaptive-html-final"
EX = SKILL / "examples/06_seo_prompt_engineering_dashboard.html"
OUT = pathlib.Path(__file__).resolve().parent / "index.html"
ICONS = {d["id"]: d["svg"] for d in json.load(open(SKILL/"assets/body-icons.json", encoding="utf-8"))}
def ic(k): return f'<span class="body-icon body-icon--sm">{ICONS[k]}</span>'
def a(url,label): return f'<a href="{url}">{label}</a>'
def h2(n,k,t): return f'<h2>{ic(k)}<span class="num">{n}</span>{t}</h2>'

# ── 수집 레코드 (x-ai-trend-collector 웹검색 fallback · views/likes=0 · 출처 정직) ──
REC = {
 "신규 모델·제품 출시": [
  ("Claude Fable 5 일반 공개","Anthropic","2026-06-09","앤트로픽이 프런티어 모델 Claude Fable 5를 공개했다. 100만 토큰·멀티모달을 지원하고 SW엔지니어링·과학에서 Opus 4.8을 능가하며, 사이버보안·생물 등 고위험 영역은 차단하는 안전장치를 뒀다.","https://techcrunch.com/2026/06/09/anthropic-released-claude-fable-5-its-most-powerful-model-publicly-days-after-warning-ai-is-getting-too-dangerous/"),
  ("MiniMax M3 오픈웨이트","MiniMax","2026-06-01","중국 MiniMax가 희소어텐션(MSA) 기반 오픈웨이트 모델 M3를 출시했다. 100만 토큰·네이티브 멀티모달·에이전트 코딩을 단일 구조로 지원하고 SWE-Bench Pro 59%로 GPT-5.5를 앞선다고 주장했다.","https://www.marktechpost.com/2026/06/01/minimax-releases-minimax-m3-with-msa-architecture-supporting-1m-token-context-native-multimodality-and-agentic-coding/"),
  ("GPT-5.5 Instant, ChatGPT 기본 전환","OpenAI","2026-05-05","오픈AI가 플래그십 GPT-5.5의 경량판 'Instant'를 무료 사용자에게 배포하며 ChatGPT 기본 모델로 전환했다. 고위험 주제 환각이 기존 대비 52.5% 줄었다는 내부 평가를 제시했다.","https://techcrunch.com/2026/05/05/openai-releases-gpt-5-5-instant-a-new-default-model-for-chatgpt/"),
  ("Qwen3.7-Max","Alibaba Qwen","2026-05-20","알리바바가 추론·에이전트 특화 Qwen3.7-Max를 발표했다. 100만 토큰 컨텍스트, Terminal-Bench 2.0·SWE-Bench Pro에서 Opus를 앞선다고 밝혔고 입력 100만 토큰당 2.5달러로 가격을 책정했다.","https://www.marktechpost.com/2026/05/21/qwen-introduces-qwen3-7-max-a-reasoning-agent-model-with-a-1m-token-context-window/"),
  ("Claude Mythos 5 한정 배포","Anthropic","2026-06-09","Fable 5 공개와 동시에 더 강력한 Mythos 5를 'Project Glasswing'으로 사전 승인 조직에만 한정 배포하며, 위험성 경고 직후 단계적 안전 공개 전략을 취했다.","https://www.infoq.com/news/2026/06/claude-5-release/"),
 ],
 "연구·논문·벤치마크": [
  ("Solution Investigator Agent","Marozzo·Liò","2026-06-11","LLM이 사용자가 준 가설을 성급히 채택하는 문제를 지적하고, 증거를 수집·가설 확률을 갱신하며 진단하는 에이전트를 제안했다. 표준 프롬프팅 대비 진단 정확도가 향상됐다.","https://arxiv.org/abs/2606.13220"),
  ("ReasonMaxxer — RL 추론의 희소성","Akgül 외","2026-05-07","RL의 추론 개선이 새 능력 학습이 아니라 토큰의 1~3%에만 작용하는 희소 정책 선택임을 보였다. 단일 GPU 수 분 학습만으로 전체 RL급 성능을 내며 학습 비용을 약 1/1000로 줄였다.","https://arxiv.org/abs/2605.06241"),
  ("ScaleLogic — 장기추론 스케일링","Wang 외","2026-05-07","합성 논리추론으로 RL 학습이 난이도에 따라 어떻게 확장되는지 분석했다. 스케일링 지수 γ가 1.04→2.60으로 증가해 장기추론 한계가 구조가 아닌 학습 방법론에서 비롯됨을 시사했다.","https://arxiv.org/abs/2605.06638"),
  ("Agentic RL 서베이","Cui 외","2026-05-15","LLM 에이전트형 강화학습의 개념·방법론·설계를 정리한 서베이다. 목표 설정·자기 성찰 등 자율 에이전트 역량을 위한 RL의 핵심 과제와 향후 방향을 제시했다.","https://arxiv.org/abs/2604.27859"),
  ("General AgentBench (CMU)","Li 외","2026-02-22","검색·코딩·추론·도구사용 전반의 LLM 에이전트를 평가하는 통합 프레임워크다. 순차 스케일링은 컨텍스트 한계, 병렬은 검증 격차 때문에 테스트타임 스케일링이 성능을 끌어올리지 못함을 발견했다.","https://arxiv.org/abs/2602.18998"),
 ],
 "산업·투자·기업": [
  ("AlphaSense 75억 달러 가치","AlphaSense","2026-06-03","기업용 AI 시장정보 플랫폼 AlphaSense가 75억 달러 가치로 3.5억 달러 그로스 라운드를 유치했다(Vitruvian·Accenture Ventures·JPMAM). 1분기 ARR 6억 달러를 돌파했다.","https://techstartups.com/2026/06/03/venture-capital-startup-funding-roundup-june-3-2026/"),
  ("Coralogix 시리즈 F 2억 달러","Coralogix","2026-06-03","AI 옵저버빌리티 기업 Coralogix가 2억 달러 시리즈 F를 유치해 포스트머니 16억 달러를 기록했다(Advent·CPP Investments·Greenfield, 매출 60%+ 성장).","https://techstartups.com/2026/06/03/venture-capital-startup-funding-roundup-june-3-2026/"),
  ("NVIDIA·IREN 최대 5GW 파트너십","NVIDIA","2026-05-07","NVIDIA와 IREN이 최대 5기가와트 규모 AI 인프라 배치 파트너십을 발표했다. NVIDIA는 5년간 주당 70달러에 최대 3천만 주(약 21억 달러)를 매입할 권리를 확보했다.","https://nvidianews.nvidia.com/news/nvidia-and-iren-announce-strategic-partnership-to-accelerate-deployment-of-up-to-5-gigawatts-of-ai-infrastructure"),
  ("Anthropic·OpenAI 엔터프라이즈 JV","TechCrunch","2026-05-04","같은 날 양사가 엔터프라이즈 AI 합작사를 출범했다. Anthropic JV는 15억 달러 가치(각 3억 출자), OpenAI JV는 100억 달러 가치에 19개 투자자로부터 40억 달러를 조달했다.","https://techcrunch.com/2026/05/04/anthropic-and-openai-are-both-launching-joint-ventures-for-enterprise-ai-services/"),
  ("Great American AI Act 2026 초안","Tech Policy Press","2026-06-04","초당적(Obernolte·Trahan) 269페이지 연방 AI 거버넌스 초안이 공개됐다. 연매출 5억 달러+ 프런티어 개발사에 투명성 보고·독립 감사를 의무화하는 첫 포괄적 연방안이다.","https://www.techpolicy.press/unpacking-the-great-american-artificial-intelligence-act-of-2026/"),
 ],
 "실용 도구·에이전트": [
  ("Claude for Small Business","Anthropic","2026-05-13","중소기업용 Claude를 출시했다. QuickBooks·HubSpot·Canva 등 커넥터와 급여 계획·월마감·인보이스 독촉 등 15개 즉시 실행형 에이전트 워크플로(스킬)를 제공한다.","https://www.anthropic.com/news/claude-for-small-business"),
  ("MCP 사양 릴리스 후보","Model Context Protocol","2026-05-21","2026-07-28 정식 발표를 목표로 한 MCP 사양 RC를 공개했다. 무상태(stateless) 코어, 샌드박스 iframe UI 'MCP Apps', Tasks·Extensions 프레임워크, OAuth 인가 강화가 핵심이다.","https://blog.modelcontextprotocol.io/posts/2026-07-28-release-candidate/"),
  ("Cursor Composer 2.5","Cursor","2026-05-18","코딩 에이전트 모델 Composer 2.5를 출시했다. 멀티파일 편집·터미널 실행·반복 디버깅 안정성을 높였고 SWE-Bench Multilingual 79.8%를 프리미엄 모델의 약 1/10 비용에 제공한다.","https://cursor.com/blog/composer-2-5"),
  ("Windows = AI 에이전트 OS (Build 2026)","Microsoft","2026-06-02","Build 2026에서 Windows를 AI 에이전트 빌드·실행 플랫폼으로 재정의했다. Development Skills·Developer Configurations 정식 출시, 실험적 Intelligent Terminal, 로컬 에이전트 추론을 공개했다.","https://redmondmag.com/articles/2026/06/02/microsoft-uses-build-2026-to-put-ai-agents-at-the-center-of-windows.aspx"),
  ("Opsera, Cursor 네이티브 에이전트","SD Times","2026-05-08","CI/CD용 AI 에이전트를 Cursor 네이티브 플러그인으로 출시했다 — Architecture Analyzer·Security/SQL Scanner·Compliance Auditor가 IDE 안에서 동작한다. 같은 주 Snyk-Claude 보안 통합도 발표됐다.","https://sdtimes.com/ai/may-8-2026-ai-updates-from-the-past-week-coder-agents-launch-snyk-claude-partnership-opsera-cursor-partnership-and-more/"),
 ],
}
ALL = [(cat,)+r for cat,rows in REC.items() for r in rows]
URLS = []
for *_, url in ALL:
    if url not in URLS: URLS.append(url)
TOTAL=len(ALL); NCAT=len(REC); NSRC=len(URLS)

CAT_ICON = {"신규 모델·제품 출시":"platform","연구·논문·벤치마크":"experiment","산업·투자·기업":"impact","실용 도구·에이전트":"api"}
CAT_NUM = {}

HEADER = (
'<header class="header"><div class="kicker"><span class="kicker-text">AI TREND DASHBOARD · x-ai-trend-collector × adaptive-html-final</span></div>'
'<h1>2026년 5~6월 AI 트렌드 대시보드</h1>'
'<p class="sub">최신 AI 트렌드를 모델·연구·산업·도구 네 카테고리로 수집·정리한 대시보드다. X/Twitter 직접 수집(API·로그인) 대신 <strong>공개 웹검색 fallback</strong>으로 모았으므로 모든 항목에 출처 링크를 달았고, 조회수·좋아요 같은 engagement 지표는 확인 불가라 <strong>0으로 표기(추정 금지)</strong>한다.</p>'
'<div class="meta"><span>seo_dashboard</span><span>seo-dashboard.html</span><span>profile auto</span><span>adaptive-html-final v5.10.5</span><span>무 JS</span></div>'
'<div class="generated-row"><p class="generated-date">생성 기준: 2026-06-20 KST · 수집 기간 2026-05-04~06-11 · 웹검색 fallback</p>'
'<div class="lens-strip" aria-label="수집 카테고리"><span class="lens-strip-label">CATS</span><span class="lens-chip">모델·제품</span><span class="lens-chip">연구·논문</span><span class="lens-chip">산업·투자</span><span class="lens-chip">도구·에이전트</span></div></div></header>'
)

S=[]
# 1 KPI (wg-11)
S.append(f'''<section id="section-01">{h2(1,"metric","한눈 요약")}
<p>2026년 5월 초~6월 중순 AI 트렌드를 카테고리별로 수집한 결과 요약이다. 수치는 수집된 항목 기준이며, engagement는 웹검색 한계로 집계하지 않았다.</p>
<section class="wg-11" aria-labelledby="wg-11-title"><header class="wg-11-head"><p class="wg-11-kicker">수집 상태 보드</p><h2 id="wg-11-title" class="wg-11-h">AI 트렌드 수집 · 2026-05~06</h2><p class="wg-11-lead">총 <strong>{TOTAL}건</strong> · {NCAT}개 카테고리 · 고유 출처 <strong>{NSRC}곳</strong> · 수집 경로: 공개 웹검색(읽기 전용)</p></header>
<div class="wg-11-kpis"><div class="wg-11-kpi wg-11-kpi-good"><span class="wg-11-kpi-v">{TOTAL}</span><span class="wg-11-kpi-l">수집 트렌드</span></div><div class="wg-11-kpi wg-11-kpi-prog"><span class="wg-11-kpi-v">{NCAT}</span><span class="wg-11-kpi-l">카테고리</span></div><div class="wg-11-kpi wg-11-kpi-good"><span class="wg-11-kpi-v">{NSRC}</span><span class="wg-11-kpi-l">고유 출처</span></div><div class="wg-11-kpi wg-11-kpi-risk"><span class="wg-11-kpi-v wg-11-warn">0</span><span class="wg-11-kpi-l">engagement(확인불가)</span></div></div></section></section>''')

# 2 방법·한계
S.append(f'''<section id="section-02">{h2(2,"note","수집 방법과 한계")}
<p>이 대시보드는 x-ai-trend-collector 스킬의 <strong>웹검색 fallback 경로</strong>로 만들어졌다. X/Twitter API 자격증명이나 로그인 브라우저 세션이 없는 환경이라, 타임라인을 직접 크롤하지 않고 공개 웹검색 결과가 가리키는 출처(공식 발표·뉴스·arXiv 등)를 정직하게 수집했다.</p>
<div class="lede-note"><div class="label">정직성 고지</div><p>① 모든 항목에 <strong>실제 출처 URL</strong>을 달았다(스니펫 기반일 수 있어 정밀도를 과장하지 않는다). ② 조회수·좋아요는 인증 수집이 아니라 확인 불가이므로 <strong>0으로 표기하고 추정하지 않았다</strong>. ③ "X 글을 직접 크롤했다"거나 "engagement 상위"라고 주장하지 않는다. ④ 일부 항목은 본 에이전트 지식 시점 이후의 웹검색 결과이므로, 사실 확인은 각 출처 링크로 직접 검증하길 권한다.</p></div></section>''')

# 3~6 카테고리 cg-grid
def cards(cat):
    out=[]
    for i,(c,title,author,date,summary,url) in enumerate([r for r in ALL if r[0]==cat],1):
        out.append(f'<article class="cg-card"><em>{date} · {author}</em><b>{title}</b><p>{summary} {a(url,"출처 ↗")}</p></article>')
    return '<section class="vt-shell"><div class="vt-frame"><div class="cg-grid">'+''.join(out)+'</div></div></section>'

cat_secs=[("신규 모델·제품 출시",3,"신규 모델·제품 출시","모델·플래그십·오픈웨이트 출시 흐름. 100만 토큰·멀티모달·에이전트 코딩이 공통 키워드다."),
          ("연구·논문·벤치마크",4,"연구·논문·벤치마크","에이전트형 RL·추론 효율화·평가 프레임워크가 두드러진다 — '학습 방법'이 핵심 화두다."),
          ("산업·투자·기업",5,"산업·투자·기업","엔터프라이즈 AI·옵저버빌리티 펀딩과 데이터센터(GW)·연방 거버넌스 초안이 동시 진행 중이다."),
          ("실용 도구·에이전트",6,"실용 도구·에이전트","코딩 에이전트·MCP·에이전트 OS 등 '도구가 에이전트로' 이동하는 신호가 뚜렷하다.")]
MODELS_TABLE = ('<div class="tbl table-scroll"><table><caption>신규 플래그십/오픈웨이트 모델 비교 — 공개 발표 기준(출처별 주장치, 교차검증 아님)</caption>'
 '<thead><tr><th>모델</th><th>주체·공개</th><th>컨텍스트</th><th>내세운 강점(주장)</th><th>비고</th></tr></thead><tbody>'
 '<tr><td>Claude Fable 5</td><td>Anthropic · 2026-06-09</td><td>100만 토큰</td><td>SW엔지니어링·과학에서 Opus 4.8 능가</td><td>고위험 영역 응답 차단</td></tr>'
 '<tr><td>MiniMax M3</td><td>MiniMax · 2026-06-01</td><td>100만 토큰</td><td>SWE-Bench Pro 59%(GPT-5.5 상회 주장)</td><td>오픈웨이트·MSA 구조</td></tr>'
 '<tr><td>GPT-5.5 Instant</td><td>OpenAI · 2026-05-05</td><td>—</td><td>고위험 환각 52.5%↓(내부 평가)</td><td>ChatGPT 무료 기본</td></tr>'
 '<tr><td>Qwen3.7-Max</td><td>Alibaba · 2026-05-20</td><td>100만 토큰</td><td>Terminal-Bench/SWE-Bench Pro Opus 상회 주장</td><td>입력 100만 토큰당 $2.5</td></tr>'
 '</tbody></table></div><p>표의 성능 수치는 각 발표사의 주장이며 독립 교차검증이 아니다 — 벤치마크는 출처 링크에서 직접 확인을 권한다.</p>')
for cat,num,title,lead in cat_secs:
    extra = MODELS_TABLE if cat=="신규 모델·제품 출시" else ""
    S.append(f'<section id="section-0{num}">{h2(num,CAT_ICON[cat],title)}<p>{lead}</p>{cards(cat)}{extra}</section>')

# 7 관전 포인트
S.append(f'''<section id="section-07">{h2(7,"idea","핵심 관전 포인트")}
<p>네 카테고리를 가로지르면 2026년 5~6월의 신호가 세 갈래로 모인다.</p>
<div class="summary-card"><div class="label">① 컨텍스트·에이전트가 표준</div><p>모델 출시(Fable 5·M3·Qwen3.7-Max)는 100만 토큰 컨텍스트와 에이전트 코딩을 기본값처럼 내세운다. 도구(Cursor Composer 2.5·MCP·Windows 에이전트 OS)도 같은 방향 — '대화'에서 '실행 에이전트'로 이동.</p></div>
<div class="summary-card"><div class="label">② "학습 방법"이 연구 화두</div><p>연구는 더 큰 모델이 아니라 RL 효율화(ReasonMaxxer 비용 ~1/1000)·장기추론 스케일링·에이전트 평가(General AgentBench)로 무게가 옮겨갔다 — 추론·에이전트 역량을 어떻게 싸게 학습시키느냐가 쟁점.</p></div>
<div class="summary-card"><div class="label">③ 자본·인프라·규제 동시 가속</div><p>엔터프라이즈 JV·옵저버빌리티 펀딩과 5GW급 데이터센터 투자가 몰리는 동시에, 첫 포괄적 연방 AI 거버넌스 초안(Great American AI Act)이 투명성·감사를 요구하기 시작했다.</p></div></section>''')

# 8 출처
src_lis=''.join(f'<li>{a(u,u.split("//")[-1][:70])}</li>' for u in URLS)
S.append(f'''<section id="section-08">{h2(8,"reference","출처")}
<aside class="source-note"><div class="label">{ic("reference")}Source Note · x-ai-trend-collector 웹검색 fallback</div><p>X/Twitter 직접 수집이 불가해 공개 웹검색으로 수집했다. 아래는 고유 출처 {NSRC}곳이며, 각 트렌드 카드의 "출처 ↗" 링크와 동일하다. engagement(조회·좋아요)는 확인 불가로 전 항목 0으로 표기했다.</p>
<ol>{src_lis}</ol></aside></section>''')

MAIN_INNER = HEADER + TOC if False else HEADER  # placeholder; TOC built below
TOC_ITEMS=[("한눈 요약","section-01"),("수집 방법과 한계","section-02"),("신규 모델·제품 출시","section-03"),("연구·논문·벤치마크","section-04"),("산업·투자·기업","section-05"),("실용 도구·에이전트","section-06"),("핵심 관전 포인트","section-07"),("출처","section-08")]
TOC=('<nav class="toc-map" aria-label="문서 목차"><span class="label">문서 목차</span><p>카테고리별 수집 트렌드와 관전 포인트를 chip-nav로 이동합니다.</p><div class="toc-pills">'
     +''.join(f'<a class="toc-pill" href="#{sid}"><b>{i+1}</b>{t}</a>' for i,(t,sid) in enumerate(TOC_ITEMS))+'</div></nav>')
MAIN_INNER = HEADER + TOC + ''.join(S)

# records.json 저장(provenance)
recs=[{"cat":c,"author":au,"handle":"","date":dt,"summary":sm,"url":ur,"views":0,"likes":0} for (c,ti,au,dt,sm,ur) in ALL]
(pathlib.Path(__file__).resolve().parent/"sources/records.json").write_text(json.dumps(recs,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")

ex=EX.read_text(encoding="utf-8")
new=re.sub(r'(<main\s+id="main"[^>]*>)[\s\S]*(</main>)', lambda m: m.group(1)+MAIN_INNER+m.group(2), ex, count=1)
OUT.write_text(new,encoding="utf-8")
vis=re.sub(r'\s+',' ',re.sub(r'<[^>]+>',' ',re.sub(r'<style[\s\S]*?</style>','',MAIN_INNER))).strip()
print("빌드 완료:",OUT,"| 크기:",len(new),"| 섹션:",len(S),"| 트렌드:",TOTAL,"| 출처:",NSRC,"| 본문:",len(vis),"자")
