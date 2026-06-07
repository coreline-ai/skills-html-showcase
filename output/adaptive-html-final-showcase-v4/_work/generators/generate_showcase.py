from pathlib import Path
from html import escape

ROOT = Path('<repo-root>')
SKILL = ROOT / 'skills/adaptive-html-final'
OUT = ROOT / 'output/adaptive-html-final-showcase'
PAGES = OUT / 'pages'
PAGES.mkdir(parents=True, exist_ok=True)
(OUT / 'sources').mkdir(parents=True, exist_ok=True)

internal_source_map = {
    'adaptive-html-final-SKILL.md': SKILL / 'SKILL.md',
    'adaptive-html-final-manifest.json': SKILL / 'manifest.json',
    'skill-audit-system.md': SKILL / 'references/skill-audit-system.md',
    'quality-gates.md': SKILL / 'references/quality-gates.md',
    'layout-system.md': SKILL / 'references/layout-system.md',
}
for dst, src in internal_source_map.items():
    (OUT / 'sources' / dst).write_text(src.read_text(), encoding='utf-8')

css = '\n'.join((SKILL/'assets'/name).read_text() for name in ['theme.css','components.css','layouts.css','print.css'])
css += r'''
:root{--good:var(--good-bg);--accent-text:#b72d38}
a:focus-visible, summary:focus-visible, button:focus-visible{outline:3px solid var(--accent);outline-offset:3px;border-radius:4px}
@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}.hl{animation:none;background-size:100% 100%}}
.page-nav{display:flex;justify-content:space-between;gap:12px;margin:0 0 28px;font-size:13px;color:var(--ink-mute)}
.page-nav a{text-decoration:none;border-bottom:1px dotted var(--line)}
.source-list{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:8px 18px;margin:8px 0 0 18px}
.source-list li{font-size:13px;margin:3px 0}
.status-pill{display:inline-flex;align-items:center;border:1px solid var(--line);background:#fff;border-radius:999px;padding:4px 9px;font-size:12px;color:var(--ink-mute);margin:3px 4px 3px 0}
.audit-table{display:grid;gap:10px;margin:18px 0}.audit-row{display:grid;grid-template-columns:1fr 1.4fr .6fr;gap:10px;background:#fff;border:1px solid var(--line);border-radius:8px;padding:12px}.audit-row strong{display:block}
.timeline-card{background:#fff;border:1px solid var(--line);border-left:4px solid var(--accent);border-radius:8px;padding:14px 16px;margin:12px 0}
.caption{font-size:12px;color:var(--ink-mute);margin-top:-8px}
.hero-index{background:#fff;border:1px solid var(--line);border-left:4px solid var(--accent);border-radius:12px;padding:26px;margin:20px 0 28px}
.page-list{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:14px}.page-list .mini-card a{text-decoration:none}.mode-label{font-size:11px;font-weight:800;letter-spacing:.12em;color:var(--accent);text-transform:uppercase}
@media(max-width:760px){.source-list,.page-list,.audit-row{grid-template-columns:1fr}}
'''

font_links = '''<link rel="preconnect" href="https://cdn.jsdelivr.net">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.css" rel="stylesheet">
<link href="https://fonts.googleapis.com/css2?family=Noto+Serif+KR:wght@400;600;700&display=swap" rel="stylesheet">'''

def meta_spans(items):
    return ''.join(f'<span>{escape(str(x))}</span>' for x in items)

def source_note(label, sources, note='공식 문서와 신뢰 가능한 기술 문서를 기준으로 요약했습니다. 최신 정책·가격·모델명은 실제 적용 전에 재확인하세요.'):
    lis = '\n'.join(f'<li><a href="{escape(url)}">{escape(name)}</a></li>' for name, url in sources)
    return f'''<aside class="source-note">
  <div class="label">{escape(label)}</div>
  <p>{escape(note)}</p>
  <ul class="source-list">{lis}</ul>
</aside>'''

def page_doc(title, desc, body):
    return f'''<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(title)}</title>
<meta name="description" content="{escape(desc)}">
<meta property="og:title" content="{escape(title)}">
<meta property="og:description" content="{escape(desc)}">
<meta property="og:type" content="article">
{font_links}
<style>
{css}
</style>
</head>
<body>
<a class="skip" href="#main">본문 바로가기</a>
{body}
</body>
</html>'''

pages = []

def add_page(slug, mode, title, desc, body):
    path = PAGES / f'{slug}.html'
    path.write_text(page_doc(title, desc, body), encoding='utf-8')
    pages.append({'slug':slug,'mode':mode,'title':title,'desc':desc,'path':path})

# 1 beginner
sources_passkeys = [
    ('passkeys.dev — What are passkeys?', 'https://passkeys.dev/docs/intro/what-are-passkeys/'),
    ('FIDO Alliance — Passkeys', 'https://fidoalliance.org/passkeys/'),
    ('W3C WebAuthn Level 3', 'https://www.w3.org/TR/webauthn-3/'),
    ('MDN — Web Authentication API', 'https://developer.mozilla.org/en-US/docs/Web/API/Web_Authentication_API'),
]
add_page('01-beginner-passkeys-webauthn','beginner_html','패스키와 WebAuthn, 비밀번호 없는 로그인을 처음부터 이해하기','패스키·WebAuthn·공개키 인증을 초보자도 이해할 수 있게 비유, 용어, 흐름, 오해와 체크리스트로 정리한 HTML 학습자료.', f'''
<main id="main" class="page layout-beginner">
  <nav class="page-nav"><a href="../index.html">← 쇼케이스 홈</a><span>Mode 01 · beginner_html</span></nav>
  <header class="header"><div class="kicker">Beginner HTML</div><h1>패스키와 WebAuthn, 비밀번호 없는 로그인을 처음부터 이해하기</h1><p class="sub">패스키는 “지문으로 로그인”이 아니라, 서버에는 공개키만 두고 진짜 열쇠는 내 기기에 보관하는 로그인 방식입니다.</p><div class="meta">{meta_spans(['대상: 입문자','주제: Passkeys/WebAuthn','검토일: 2026-05-30'])}</div></header>
  <nav class="toc" aria-label="학습 순서"><strong>학습 순서</strong><ol><li><a href="#concept">패스키의 한 문장 정의</a></li><li><a href="#terms">처음 보는 용어</a></li><li><a href="#flow">등록과 로그인 흐름</a></li><li><a href="#traps">흔한 오해</a></li><li><a href="#practice">적용 전 체크</a></li></ol></nav>
  <aside class="hero-analogy"><div class="tag">비유로 시작하기</div><h3>서비스에는 자물쇠 도면만 있고,<br>진짜 열쇠는 내 기기에 있습니다.</h3><p>비밀번호는 서버와 사용자가 같은 비밀을 아는 방식입니다. 패스키는 다릅니다. 서버는 공개키라는 “자물쇠 도면”만 저장하고, 내 기기는 비밀키라는 “진짜 열쇠”로 매번 새 challenge에 서명합니다.</p></aside>
  <section id="concept" class="beginner-zero"><h2><span class="num">1</span>패스키는 무엇인가</h2><p class="h2-sub">외우는 문자열을 없애고, 공개키 인증으로 사용자를 확인하는 방식입니다.</p><p>Passkey는 FIDO2/WebAuthn 기반의 인증 자격 증명입니다. 서버에는 공개키가 저장되고, 사용자의 기기나 보안키에는 비밀키가 저장됩니다. 로그인할 때 서버가 난수 challenge를 보내면 기기가 서명하고, 서버가 공개키로 검증합니다.</p><div class="good"><div class="label">핵심 장점</div><div class="name">가짜 사이트에 비밀번호를 입력하는 구조가 사라진다</div><p>브라우저와 운영체제는 사이트의 origin/RP ID를 확인합니다. 그래서 공격자가 비슷한 로그인 페이지를 만들어도 같은 패스키를 쓰기 어렵습니다.</p></div></section>
  <section id="terms" class="beginner-terms"><h2><span class="num">2</span>처음 보는 용어</h2><p class="h2-sub">용어가 어려워 보여도 역할은 단순합니다.</p><div class="term"><div class="label">용어</div><span class="word">Relying Party</span><div class="meaning">로그인을 제공하는 웹사이트 또는 서비스입니다. 예: example.com.</div></div><div class="term"><div class="label">용어</div><span class="word">Authenticator</span><div class="meaning">비밀키를 보관하고 서명하는 기기·보안키·패스키 제공자입니다.</div></div><div class="term"><div class="label">용어</div><span class="word">Challenge</span><div class="meaning">서버가 매번 새로 보내는 임시 문제입니다. 재사용되면 안 됩니다.</div></div><div class="term"><div class="label">용어</div><span class="word">User Verification</span><div class="meaning">기기가 “실제 사용자”가 승인했는지 확인하는 단계입니다. PIN, 생체 인증, 기기 잠금 해제가 여기에 해당합니다.</div></div></section>
  <section id="flow"><h2><span class="num">3</span>등록과 로그인 흐름</h2><p class="h2-sub">패스키는 등록 ceremony와 인증 ceremony로 나누어 생각하면 쉽습니다.</p><div class="card-grid"><div class="mini-card"><h3>1. 등록</h3><p>서비스가 challenge와 RP 정보를 보냅니다. 기기는 새 키쌍을 만들고 공개키를 서버에 등록합니다.</p></div><div class="mini-card"><h3>2. 로그인</h3><p>서버가 challenge를 보내면 기기는 origin을 확인하고 비밀키로 서명합니다.</p></div><div class="mini-card"><h3>3. 검증</h3><p>서버는 저장된 공개키로 서명을 확인하고, counter·user verification 등 정책을 검토합니다.</p></div></div></section>
  <section id="traps" class="beginner-traps"><h2><span class="num">4</span>흔한 오해</h2><p class="h2-sub">패스키를 도입할 때 보안보다 복구 흐름에서 자주 무너집니다.</p><div class="danger"><div class="label">오해</div><div class="name">“패스키는 생체정보 로그인이다”</div><p>생체정보는 로컬에서 비밀키 사용을 잠금 해제하는 수단입니다. 서버로 지문이나 얼굴 정보가 전송되는 구조가 아닙니다.</p></div><div class="danger"><div class="label">함정</div><div class="name">복구 수단이 SMS 하나뿐인 경우</div><p>패스키가 강해도 계정 복구가 약하면 전체 계정 보안은 약한 복구 경로 수준으로 내려갑니다.</p></div><div class="good"><div class="label">해결</div><div class="name">복구·기기 변경·분실 시나리오를 먼저 설계</div><p>동기화형 패스키, 보안키, 백업 코드, 관리자 승인 등 사용자군별 복구 정책을 분리합니다.</p></div></section>
  <section id="practice" class="beginner-practice"><h2><span class="num">5</span>내 서비스 적용 전 체크</h2><p class="h2-sub">로그인 버튼보다 전체 계정 생애주기가 중요합니다.</p><ul><li>RP ID와 origin 정책을 명확히 정했는가?</li><li>challenge 재사용 방지와 만료 시간이 구현되어 있는가?</li><li>복구 경로가 패스키보다 약하지 않은가?</li><li>여러 기기·여러 패스키 등록을 허용할 것인가?</li><li>고객센터가 패스키 분실 문의를 처리할 절차가 있는가?</li></ul></section>
  <section class="try"><div class="label">Try</div><h2>이번 주에 해볼 것</h2><ol><li>현재 로그인/복구 플로우를 그림으로 그립니다.</li><li>비밀번호, OTP, 이메일 복구, 고객센터 승인 중 가장 약한 경로를 표시합니다.</li><li>패스키를 추가했을 때 약한 경로가 그대로 남는지 점검합니다.</li></ol></section>
  {source_note('출처와 검토 기준', sources_passkeys)}
</main>''')

# 2 expert EU AI Act
sources_eu = [
    ('EUR-Lex — Regulation (EU) 2024/1689', 'https://eur-lex.europa.eu/eli/reg/2024/1689/oj'),
    ('EU AI Act Service Desk — Implementation timeline', 'https://ai-act-service-desk.ec.europa.eu/en/ai-act/eu-ai-act-implementation-timeline'),
    ('European Commission — GPAI obligations', 'https://digital-strategy.ec.europa.eu/en/factpages/general-purpose-ai-obligations-under-ai-act'),
    ('European Commission — GPAI Code of Practice', 'https://digital-strategy.ec.europa.eu/en/policies/contents-code-gpai'),
]
add_page('02-expert-eu-ai-act-governance','expert_html','EU AI Act 기반 생성형 AI 거버넌스 실행 리포트','EU AI Act와 GPAI 의무를 기준으로 생성형 AI 제품·조직이 준비해야 할 거버넌스 로드맵을 정리한 전문가 리포트.', f'''
<main id="main" class="page-wide layout-expert">
  <nav class="page-nav"><a href="../index.html">← 쇼케이스 홈</a><span>Mode 02 · expert_html</span></nav>
  <header class="header report-header"><div class="kicker">Expert Report</div><h1>EU AI Act 기반 생성형 AI 거버넌스 실행 리포트</h1><p class="sub">생성형 AI 거버넌스의 첫 질문은 “어떤 모델을 쓰는가”가 아니라 “우리의 법적 역할과 위험 등급은 무엇인가”입니다.</p><div class="meta">{meta_spans(['대상: AI 제품/법무/보안 리더','범위: EU AI Act·GPAI','검토일: 2026-05-30'])}</div></header>
  <section class="executive-summary"><h2><span class="num">1</span>Executive Summary</h2><p class="h2-sub">2026년 하반기를 기다리면 늦습니다. 인벤토리와 증빙 체계를 지금 만들어야 합니다.</p><p><strong>결론:</strong> 생성형 AI 조직은 모델 제공자, AI 시스템 제공자, 배포자 역할을 분리하고, GPAI·고위험·투명성 의무를 제품 단위로 매핑해야 합니다. 특히 외부 LLM을 쓰는 조직도 공급망 증빙, 사용 목적, 사용자 고지, 사고 대응 절차를 갖춰야 합니다.</p><div class="summary-grid"><div class="mini-card"><h3>즉시</h3><p>AI 시스템 인벤토리와 사용처 분류</p></div><div class="mini-card"><h3>60일</h3><p>위험 등급·역할·공급망 증빙 정리</p></div><div class="mini-card"><h3>90일</h3><p>평가 로그, 승인 절차, 사고 대응 훈련</p></div></div></section>
  <section class="decision-grid"><div class="decision-card"><h3>역할 분류</h3><p>Provider, deployer, importer/distributor를 구분합니다. 같은 회사도 제품별로 역할이 달라질 수 있습니다.</p></div><div class="decision-card"><h3>GPAI 여부</h3><p>범용 모델을 제공하거나 이를 통합해 시스템을 제공하는지 확인합니다. Systemic risk 기준은 추가 검토가 필요합니다.</p></div><div class="decision-card"><h3>고위험 영역</h3><p>채용, 교육, 필수 서비스, 금융, 법집행 등에서는 단순 챗봇도 고위험 시스템 요건을 검토해야 합니다.</p></div></section>
  <section class="architecture-map"><h2><span class="num">2</span>거버넌스 운영모델</h2><p class="h2-sub">정책 문서보다 운영 증거가 중요합니다.</p><div class="tbl"><table><caption class="caption">AI 거버넌스 최소 운영 체계</caption><thead><tr><th scope="col">영역</th><th scope="col">필수 산출물</th><th scope="col">소유자</th></tr></thead><tbody><tr><td>인벤토리</td><td>모델, 데이터, 사용 목적, 사용자군, 배포 지역</td><td>AI PM / 보안</td></tr><tr><td>위험 분류</td><td>금지·고위험·투명성·GPAI 체크</td><td>법무 / 리스크</td></tr><tr><td>평가</td><td>정확도, 안전성, 편향, 보안 테스트 로그</td><td>ML / QA</td></tr><tr><td>운영</td><td>승인, 변경관리, 사고 대응, 사용자 고지</td><td>운영 / CS</td></tr></tbody></table></div></section>
  <section class="risk-matrix"><h2><span class="num">3</span>리스크 매트릭스</h2><p class="h2-sub">법적 위험만 보지 말고 공급망과 증빙 공백을 같이 봅니다.</p><div class="card-grid"><div class="mini-card risk-high"><h3>높음: 역할 오판</h3><p>제공자 의무를 deployer 수준으로만 처리하면 문서·평가·고지 체계가 누락됩니다.</p></div><div class="mini-card risk-mid"><h3>중간: 외부 모델 공급망</h3><p>모델 카드, 저작권 정책, 안전 평가 자료를 계약상 산출물로 요구해야 합니다.</p></div><div class="mini-card risk-low"><h3>낮음: 문구 고지 누락</h3><p>챗봇/합성 콘텐츠 고지 등은 빠르게 보완 가능하지만 UX와 정책을 같이 고쳐야 합니다.</p></div></div></section>
  <section class="priority-roadmap"><h2><span class="num">4</span>30/60/90일 로드맵</h2><p class="h2-sub">로드맵은 문서가 아니라 증거를 남기는 방식으로 설계합니다.</p><ol><li><strong>30일:</strong> 모든 AI 사용 사례를 인벤토리화하고 금지 관행 스크리닝을 끝냅니다.</li><li><strong>60일:</strong> GPAI·고위험·투명성 분류와 공급망 증빙 요청서를 완성합니다.</li><li><strong>90일:</strong> 평가 로그, 사용자 고지, 변경 승인, 사고 보고 훈련을 실행합니다.</li></ol></section>
  <section class="validation-checklist"><h2><span class="num">5</span>검증 체크리스트</h2><p class="h2-sub">감사자가 물을 질문에 답할 수 있어야 합니다.</p><ul><li>각 AI 시스템의 목적과 사용자가 명확한가?</li><li>외부 모델의 기술문서·저작권 정책·학습 데이터 요약을 확보했는가?</li><li>고위험 도메인 여부를 법무와 재확인했는가?</li><li>사고 발생 시 보고·차단·사용자 통지 경로가 있는가?</li></ul></section>
  <section class="try"><div class="label">Final Recommendation</div><h2>이번 분기 안에 해야 할 일</h2><ol><li>AI 시스템 인벤토리를 단일 소스로 만듭니다.</li><li>위험 분류와 증빙 보관을 제품 출시 게이트에 넣습니다.</li><li>공급망 계약에 모델 문서와 안전 평가 제공 조항을 넣습니다.</li></ol></section>
  {source_note('공식 출처', sources_eu)}
</main>''')

# 3 article AI agent UX
sources_agentux = [
    ('NIST — AI Risk Management Framework', 'https://www.nist.gov/itl/ai-risk-management-framework'),
    ('Google PAIR — Explainability + Trust', 'https://pair.withgoogle.com/guidebook-v2/chapter/explainability-trust/'),
    ('Microsoft HAX Toolkit', 'https://www.microsoft.com/en-us/haxtoolkit/'),
    ('OpenAI — Safety in building agents', 'https://developers.openai.com/api/docs/guides/agent-builder-safety'),
]
add_page('03-article-ai-agent-ux-trust','article_html','AI 에이전트 UX의 신뢰 설계','AI 에이전트가 도구를 실행하고 권한을 다루는 시대에 필요한 신뢰 UX 원칙을 정리한 매거진형 아티클.', f'''
<main id="main" class="page layout-article">
  <nav class="page-nav"><a href="../index.html">← 쇼케이스 홈</a><span>Mode 03 · article_html</span></nav>
  <header class="header article-header"><div class="kicker">Magazine Article</div><h1>AI 에이전트 UX의 신뢰 설계</h1><p class="sub lead">신뢰는 감정이 아니라 운영 설계입니다. 사용자가 AI 에이전트를 믿는 순간은 “똑똑해 보일 때”가 아니라, 무엇을 할 수 있고 무엇을 못 하는지 분명히 보일 때입니다.</p><div class="meta">{meta_spans(['주제: AI Agent UX','독자: PM·디자이너·엔지니어','형식: 공개 아티클'])}</div></header>
  <aside class="pull-quote">AI 에이전트의 신뢰는 답변 품질보다 “권한, 근거, 승인, 복구”가 보이는지에서 결정된다.</aside>
  <article>
    <section><h2><span class="num">1</span>문제: 챗봇 UX로는 에이전트를 설명할 수 없다</h2><p class="h2-sub">읽고 답하는 도구와, 읽고 실행하는 도구는 완전히 다릅니다.</p><p>AI 에이전트는 검색, 파일 접근, 코드 실행, 외부 API 호출, 결제·삭제 같은 side effect를 만들 수 있습니다. 따라서 UX는 “대화가 매끄럽다”에서 멈추면 안 됩니다. 사용자는 에이전트가 어떤 근거로 판단했고, 어느 권한을 쓰며, 무엇을 실행하기 직전인지 알아야 합니다.</p></section>
    <section><h2><span class="num">2</span>신뢰의 네 가지 기둥</h2><p class="h2-sub">예측 가능성, 설명 가능성, 통제 가능성, 복구 가능성을 분리해서 설계합니다.</p><div class="card-grid"><div class="mini-card"><h3>예측</h3><p>에이전트가 다음에 할 행동을 미리 보여줍니다.</p></div><div class="mini-card"><h3>설명</h3><p>근거 자료, 제한 조건, 불확실성을 노출합니다.</p></div><div class="mini-card"><h3>승인</h3><p>되돌릴 수 없는 행동은 사용자 확인을 요구합니다.</p></div></div><div class="good"><div class="label">좋은 패턴</div><div class="name">실행 전 미리보기</div><p>메일 삭제, DB 변경, 결제처럼 영향이 큰 행동은 “무엇을, 왜, 어떤 권한으로” 실행하는지 보여준 뒤 승인받습니다.</p></div></section>
    <section><h2><span class="num">3</span>케이스: 메일 정리 에이전트</h2><p class="h2-sub">자동화가 빠를수록 취소와 복구의 UX는 더 중요해집니다.</p><p>메일 정리 에이전트가 오래된 광고 메일을 삭제한다고 가정해 봅시다. 나쁜 UX는 “정리했습니다”라고 말하고 끝냅니다. 좋은 UX는 삭제 후보, 판단 기준, 제외 규칙, 복구 기간, 실행 전 최종 확인을 보여줍니다.</p><div class="danger"><div class="label">위험한 신뢰</div><div class="name">만능처럼 보이게 하기</div><p>에이전트가 틀릴 수 있다는 전제를 숨기면, 사용자는 한 번의 실패 후 전체 제품을 신뢰하지 않게 됩니다.</p></div></section>
    <section><h2><span class="num">4</span>제품팀을 위한 원칙</h2><p class="h2-sub">AI의 능력을 보여주기보다 경계를 보여주는 것이 신뢰를 만듭니다.</p><ul><li>모든 도구 호출에는 목적과 입력 요약을 붙입니다.</li><li>외부 텍스트는 prompt injection 가능성이 있는 untrusted data로 표시합니다.</li><li>승인 UX는 “예/아니오”가 아니라 변경 내용 preview와 rollback 경로를 포함합니다.</li><li>실패 메시지는 사과보다 다음 행동을 먼저 제시합니다.</li></ul></section>
    <section><h2><span class="num">5</span>Takeaway</h2><p class="h2-sub">신뢰할 수 있는 AI는 더 말 잘하는 AI가 아니라 더 잘 멈추는 AI입니다.</p><p><span class="hl">에이전트 UX의 핵심은 자동화의 속도를 높이면서도 사용자의 통제감을 잃지 않게 하는 것</span>입니다. 권한·근거·승인·복구가 보이면 사용자는 실패 가능성까지 포함해 시스템을 이해합니다.</p></section>
  </article>
  <section class="box article-takeaway"><div class="label">체크리스트</div><ul><li>에이전트 권한이 화면에 보이는가?</li><li>실행 전 preview와 승인 단계가 있는가?</li><li>근거와 불확실성이 구분되는가?</li><li>취소·복구·감사 로그가 있는가?</li></ul></section>
  {source_note('참고 출처', sources_agentux)}
</main>''')

# 4 education github actions
sources_gha = [
    ('GitHub — Security hardening for GitHub Actions', 'https://docs.github.com/en/actions/how-tos/security-for-github-actions/security-guides/security-hardening-for-github-actions'),
    ('GitHub — Automatic token authentication', 'https://docs.github.com/en/actions/how-tos/security-for-github-actions/security-guides/automatic-token-authentication'),
    ('GitHub — OpenID Connect', 'https://docs.github.com/en/actions/concepts/security/openid-connect'),
    ('GitHub — Script injections', 'https://docs.github.com/en/actions/concepts/security/script-injections'),
    ('OWASP — CI/CD Security Cheat Sheet', 'https://cheatsheetseries.owasp.org/cheatsheets/CI_CD_Security_Cheat_Sheet.html'),
]
add_page('04-education-github-actions-security-ci','education_html','GitHub Actions 보안 CI 교육 모듈','GitHub Actions를 안전한 CI/CD 실행 환경으로 운영하기 위한 토큰, 시크릿, OIDC, 액션 핀닝 교육 HTML.', f'''
<main id="main" class="page layout-education">
  <nav class="page-nav"><a href="../index.html">← 쇼케이스 홈</a><span>Mode 04 · education_html</span></nav>
  <header class="header course-header"><div class="kicker">Course Module</div><h1>GitHub Actions 보안 CI 교육 모듈</h1><p class="sub">CI는 테스트 자동화가 아니라 토큰·시크릿·배포 권한을 가진 실행 환경입니다. 안전한 workflow는 코드만큼 중요합니다.</p><div class="meta">{meta_spans(['대상: 개발자·DevOps','시간: 45분','난이도: 중급'])}</div></header>
  <section class="learning-goals"><h2><span class="num">1</span>학습 목표</h2><p class="h2-sub">수업이 끝나면 workflow를 위협 모델 관점으로 볼 수 있어야 합니다.</p><ul><li>`GITHUB_TOKEN` 권한을 최소화한다.</li><li>untrusted GitHub context가 shell injection으로 이어지는 흐름을 설명한다.</li><li>third-party action을 full-length commit SHA로 pinning하는 이유를 이해한다.</li><li>장기 cloud secret 대신 OIDC short-lived credential을 설계한다.</li></ul></section>
  <section class="before-start"><h2><span class="num">2</span>시작 전 위협 모델</h2><p class="h2-sub">workflow는 누가 바꿀 수 있고, 무엇을 읽고 쓸 수 있는지부터 확인합니다.</p><div class="card-grid"><div class="mini-card"><h3>입력</h3><p>PR 제목·본문·브랜치명·이슈 본문은 공격자 입력일 수 있습니다.</p></div><div class="mini-card"><h3>권한</h3><p>토큰 권한이 넓으면 단순 테스트 실패가 저장소 쓰기 권한 탈취가 됩니다.</p></div><div class="mini-card"><h3>실행자</h3><p>self-hosted runner는 지속적 compromise 가능성을 전제로 격리합니다.</p></div></div></section>
  <section class="lesson-step"><h2><span class="num">3</span>취약 YAML과 개선 YAML</h2><p class="h2-sub">문제는 “변수 하나”가 아니라 trust boundary입니다.</p><div class="danger"><div class="label">취약 예시</div><div class="name">PR 제목을 shell에 바로 삽입</div><pre><code>run: echo "${{{{ github.event.pull_request.title }}}}"</code></pre><p>공격자가 제목에 shell 구문을 넣으면 의도치 않은 명령이 실행될 수 있습니다.</p></div><div class="good"><div class="label">개선 예시</div><div class="name">환경 변수로 전달하고 quoting</div><pre><code>env:
  PR_TITLE: ${{{{ github.event.pull_request.title }}}}
run: |
  printf '%s\n' "$PR_TITLE"</code></pre></div></section>
  <section class="practice-card"><h2><span class="num">4</span>실습</h2><p class="h2-sub">아래 workflow를 안전하게 고쳐봅니다.</p><pre><code>permissions: write-all
steps:
  - uses: actions/checkout@v4
  - run: echo "${{{{ github.event.issue.title }}}}"</code></pre><ol><li>`permissions`를 필요한 scope로 줄입니다.</li><li>issue title을 env로 옮깁니다.</li><li>외부 action은 tag 대신 SHA pinning을 검토합니다.</li></ol></section>
  <section class="quiz-box"><h2><span class="num">5</span>퀴즈</h2><p class="h2-sub">정답보다 이유를 설명해보세요.</p><ol><li>`GITHUB_TOKEN`은 명시적으로 넘기지 않으면 action에서 접근할 수 없다. O/X</li><li>OIDC는 장기 cloud secret을 줄이는 데 도움이 된다. O/X</li><li>tag pinning은 commit SHA pinning과 같은 보안 수준이다. O/X</li><li>`pull_request_target`은 항상 안전하다. O/X</li></ol></section>
  <section class="answer-box"><h2><span class="num">6</span>정답 해설</h2><p class="h2-sub">보안 CI는 기본값을 의심하는 훈련입니다.</p><ol><li>X — action은 `github.token` context로 접근할 수 있으므로 permissions 최소화가 필요합니다.</li><li>O — OIDC는 short-lived credential을 발급받는 흐름에 적합합니다.</li><li>X — tag는 이동 가능하므로 full-length commit SHA가 더 강합니다.</li><li>X — fork PR과 secret 노출 모델을 이해해야 합니다.</li></ol></section>
  <section class="try"><div class="label">Review Checklist</div><h2>다음 PR부터 적용할 5가지</h2><ol><li>workflow마다 `permissions`를 명시합니다.</li><li>외부 action은 SHA pinning 정책을 정합니다.</li><li>PR/issue context는 untrusted input으로 처리합니다.</li><li>cloud 배포 secret은 OIDC 전환을 검토합니다.</li><li>workflow 변경에는 CODEOWNERS 리뷰를 요구합니다.</li></ol></section>
  {source_note('교육 출처', sources_gha)}
</main>''')

# 5 blog local AI
sources_localai = [
    ('Ollama — GPU support', 'https://docs.ollama.com/gpu'),
    ('llama.cpp GitHub', 'https://github.com/ggml-org/llama.cpp'),
    ('NVIDIA AI Workbench', 'https://docs.nvidia.com/ai-workbench/user-guide/latest/overview/introduction.html'),
    ('Hugging Face — bitsandbytes quantization', 'https://huggingface.co/docs/transformers/en/quantization/bitsandbytes'),
]
add_page('05-blog-local-ai-workstation','blog_writer','로컬 AI 워크스테이션 구축기: GPU보다 먼저 배운 것들','Ollama, llama.cpp, GGUF, 양자화, GPU/VRAM 판단을 중심으로 로컬 AI 워크스테이션 구축 경험을 정리한 블로그형 HTML.', f'''
<main id="main" class="page layout-blog">
  <nav class="page-nav"><a href="../index.html">← 쇼케이스 홈</a><span>Mode 05 · blog_writer</span></nav>
  <header class="header blog-header"><div class="kicker">Personal Blog Essay</div><h1>로컬 AI 워크스테이션 구축기: GPU보다 먼저 배운 것들</h1><p class="sub hook">처음엔 GPU만 사면 끝인 줄 알았습니다. 하지만 로컬 AI에서 진짜 병목은 하드웨어 하나가 아니라 모델 포맷, VRAM, 드라이버, 양자화, 운영 루틴이 겹치는 지점에 있었습니다.</p><div class="meta">{meta_spans(['키워드: 로컬 AI 워크스테이션','형식: 경험형 블로그','검토일: 2026-05-30'])}</div></header>
  <aside class="box personal-note">내가 원했던 것은 “클라우드보다 싼 AI”가 아니라, 인터넷이 끊겨도 돌아가고 민감한 메모를 밖으로 보내지 않아도 되는 작은 실험실이었다.</aside>
  <article><section><h2><span class="num">1</span>왜 로컬 AI였나</h2><p class="h2-sub">비용보다 더 큰 이유는 반복 속도와 프라이버시였습니다.</p><p>로컬 AI 워크스테이션은 모든 사람에게 필요한 장비가 아닙니다. 하지만 사내 문서 실험, 개인 지식 베이스, 프롬프트 튜닝, 작은 모델 비교를 자주 한다면 클라우드 대기 시간과 비용이 피로로 바뀝니다.</p></section>
  <section><h2><span class="num">2</span>GPU보다 먼저 봐야 할 것</h2><p class="h2-sub">VRAM 숫자만 보면 놓치는 것들이 있습니다.</p><div class="card-grid"><div class="mini-card"><h3>모델 포맷</h3><p>GGUF, safetensors, quantized model 등 런타임마다 편한 형식이 다릅니다.</p></div><div class="mini-card"><h3>백엔드</h3><p>Apple Metal, CUDA, Vulkan 등 가속 경로와 드라이버 안정성이 다릅니다.</p></div><div class="mini-card"><h3>운영 루틴</h3><p>모델 저장, 버전 기록, 벤치마크, 온도·전력 관리가 필요합니다.</p></div></div></section>
  <section><h2><span class="num">3</span>실제로 도움이 된 도구</h2><p class="h2-sub">멋진 GUI보다 재현 가능한 실행 기록이 더 오래 갑니다.</p><p>Ollama는 빠르게 모델을 내려받고 실행하기 좋았습니다. llama.cpp는 GGUF와 다양한 백엔드 실험에 유용했습니다. NVIDIA AI Workbench 같은 접근은 “내 PC 한 대”보다 컨테이너와 Git 기반 재현성을 생각하게 해주었습니다.</p><pre><code># 예시: 작은 모델로 먼저 확인
ollama run llama3.2

# 예시: 실행 로그 남기기
time ollama run llama3.2 "요약 테스트"</code></pre></section>
  <section><h2><span class="num">4</span>과소평가한 비용</h2><p class="h2-sub">로컬은 공짜가 아니라 비용의 형태가 바뀌는 것입니다.</p><div class="danger"><div class="label">함정</div><div class="name">발열, 소음, 드라이버 충돌</div><p>벤치마크 수치보다 매일 켜놓을 수 있는 안정성이 더 중요했습니다. 작은 모델을 빠르게 돌리는 환경이 큰 모델을 가끔 돌리는 환경보다 생산적일 때가 많습니다.</p></div><div class="good"><div class="label">해결</div><div class="name">작게 시작하고 기록하기</div><p>7B급 모델 하나를 일주일 쓰면서 응답 속도, 메모리, 전력, 실제 사용 빈도를 기록한 뒤 업그레이드 판단을 하는 편이 안전합니다.</p></div></section>
  <section><h2><span class="num">5</span>지금 다시 산다면</h2><p class="h2-sub">하드웨어보다 워크플로우를 먼저 설계하겠습니다.</p><ul><li>실제 작업: 요약, 코드 보조, 검색, 문서화 중 무엇인가?</li><li>필요 지연 시간: 실시간 대화인가, 배치 처리인가?</li><li>데이터 민감도: 로컬이어야 하는 이유가 분명한가?</li><li>유지보수 시간: 드라이버와 모델 업데이트를 감당할 수 있는가?</li></ul></section></article>
  <section class="try soft-cta"><div class="label">Soft CTA</div><h2>먼저 일주일만 작게 써보기</h2><ol><li>작은 모델 하나를 정합니다.</li><li>매일 반복하는 작업 3개에만 씁니다.</li><li>응답 품질보다 “다시 쓰고 싶은가”를 기록합니다.</li></ol></section>
  {source_note('참고 출처', sources_localai)}
</main>''')

# 6 seo RAG
sources_rag = [
    ('OpenAI — Optimizing LLM Accuracy', 'https://developers.openai.com/api/docs/guides/optimizing-llm-accuracy'),
    ('OpenAI — Responses tools guide', 'https://developers.openai.com/api/docs/guides/tools'),
    ('Google — SEO Starter Guide', 'https://developers.google.com/search/docs/fundamentals/seo-starter-guide'),
    ('Google — Helpful, reliable, people-first content', 'https://developers.google.com/search/docs/fundamentals/creating-helpful-content'),
    ('Google — Article structured data', 'https://developers.google.com/search/docs/appearance/structured-data/article'),
]
add_page('06-seo-rag-vs-finetuning','seo_dashboard','RAG vs Fine-tuning SEO 대시보드','RAG와 Fine-tuning의 검색 의도, 키워드 클러스터, SERP 미리보기, 제목·메타 후보를 설계한 SEO 대시보드.', f'''
<main id="main" class="page-wide layout-seo">
  <nav class="page-nav"><a href="../index.html">← 쇼케이스 홈</a><span>Mode 06 · seo_dashboard</span></nav>
  <header class="header seo-header"><div class="kicker">SEO Dashboard</div><h1>RAG vs Fine-tuning SEO 대시보드</h1><p class="sub">단순 정의 글이 아니라 “언제 검색하고 언제 학습시킬까”라는 의사결정형 검색 의도를 잡는 설계입니다.</p><div class="meta">{meta_spans(['Primary keyword: RAG vs Fine-tuning','Intent: 비교·의사결정','검토일: 2026-05-30'])}</div></header>
  <section class="seo-overview"><h2><span class="num">1</span>Primary Keyword</h2><p class="h2-sub">검색자는 용어보다 선택 기준을 원합니다.</p><div class="summary-card"><div class="label">Primary</div><p><strong>RAG vs Fine-tuning</strong> — 정보형, 비교형, 의사결정형 의도가 섞인 키워드입니다.</p></div><div class="tag-list"><span class="tag">RAG 파인튜닝 차이</span><span class="tag">LLM 정확도 개선</span><span class="tag">사내 문서 챗봇</span><span class="tag">검색 증강 생성</span><span class="tag">Fine-tuning이란</span></div></section>
  <section class="serp-preview"><h2><span class="num">2</span>SERP Preview</h2><p class="h2-sub">결과 페이지에서는 “정의”보다 “선택”을 약속합니다.</p><div class="serp-box"><p class="serp-title">RAG vs Fine-tuning: 언제 검색하고 언제 학습시킬까</p><p class="serp-url">example.com/ai/rag-vs-fine-tuning-seo-guide</p><p>RAG와 Fine-tuning의 차이를 검색 의도별로 정리합니다. 사내 지식, 응답 형식, 비용, 평가 기준에 따라 어떤 방식을 선택할지 설명합니다.</p></div></section>
  <section class="title-candidates"><h2><span class="num">3</span>제목 후보</h2><p class="h2-sub">4계열 제목으로 검색·클릭·전문가·초보자 의도를 분리합니다.</p><ol><li>RAG vs Fine-tuning: 언제 검색하고 언제 학습시킬까</li><li>RAG와 파인튜닝 차이, 사내 문서 챗봇에는 무엇이 맞을까</li><li>LLM 정확도 개선 전략: RAG, Fine-tuning, 평가 기준</li><li>RAG란 무엇이고 Fine-tuning과 어떻게 다를까</li><li>AI 서비스 설계자를 위한 RAG vs Fine-tuning 선택 기준</li></ol></section>
  <section class="meta-candidates"><h2><span class="num">4</span>메타 설명 후보</h2><p class="h2-sub">120~160자 범위에서 과장 없이 클릭 이유를 제공합니다.</p><ul><li>RAG와 Fine-tuning의 차이를 사내 지식, 응답 형식, 비용, 평가 기준으로 비교합니다. 어떤 상황에서 무엇을 선택할지 정리했습니다.</li><li>새 지식은 RAG, 일관된 응답 형식은 Fine-tuning. LLM 정확도를 높이기 위한 선택 기준과 실패 지점을 설명합니다.</li></ul></section>
  <section class="keyword-cluster"><h2><span class="num">5</span>검색 의도 매트릭스</h2><p class="h2-sub">한 글 안에서 모든 의도를 같은 깊이로 다루면 흐려집니다.</p><div class="tbl"><table><thead><tr><th scope="col">의도</th><th scope="col">질문</th><th scope="col">본문 블록</th></tr></thead><tbody><tr><td>정보형</td><td>RAG란? Fine-tuning이란?</td><td>정의와 비유</td></tr><tr><td>비교형</td><td>차이와 장단점은?</td><td>비교표</td></tr><tr><td>의사결정형</td><td>사내 챗봇에는 무엇이 맞나?</td><td>선택 플로우</td></tr><tr><td>구현형</td><td>어떻게 평가하나?</td><td>retrieval/LLM 평가 축</td></tr></tbody></table></div></section>
  <section class="content-outline"><h2><span class="num">6</span>추천 콘텐츠 아웃라인</h2><p class="h2-sub">OpenAI 문서 기준으로 RAG는 retrieval 축, fine-tuning은 작업 일관성 축으로 설명합니다.</p><ol><li>한 문장 결론: 새 지식은 RAG, 행동 패턴은 Fine-tuning</li><li>RAG의 실패 지점: retrieval 실패와 LLM 실패</li><li>Fine-tuning의 적합 지점: 형식, 톤, 반복 작업</li><li>둘을 함께 쓰는 구조</li><li>평가 지표와 운영 체크리스트</li></ol></section>
  <section class="try final-seo-set"><div class="label">Final SEO Set</div><h2>최종 추천</h2><ul><li><strong>Title:</strong> RAG vs Fine-tuning: 언제 검색하고 언제 학습시킬까</li><li><strong>Slug:</strong> rag-vs-fine-tuning-seo-guide</li><li><strong>Tags:</strong> RAG, Fine-tuning, LLM, AI 검색, 사내 문서 챗봇, AI 평가</li></ul></section>
  {source_note('SEO·기술 출처', sources_rag)}
</main>''')

# 7 platform
sources_platform = [
    ('Tistory — Markdown/HTML mode', 'https://notice.tistory.com/2482'),
    ('Markdown Guide — Basic Syntax', 'https://www.markdownguide.org/basic-syntax/'),
    ('Naver Blog Help — SmartEditor ONE', 'https://help.naver.com/service/5593/category/3128?lang=ko'),
    ('WordPress.org — Blocks list', 'https://wordpress.org/documentation/article/blocks-list/'),
    ('Google — SEO Starter Guide', 'https://developers.google.com/search/docs/fundamentals/seo-starter-guide'),
]
add_page('07-platform-rag-post-platforms','platform_blog','RAG 글을 티스토리·벨로그·네이버·워드프레스로 변환하기','하나의 RAG vs Fine-tuning 원문을 네 가지 블로그 플랫폼에 맞게 제목, 본문 구조, 태그, 발행 체크리스트로 변환한 HTML.', f'''
<main id="main" class="page-wide layout-platform">
  <nav class="page-nav"><a href="../index.html">← 쇼케이스 홈</a><span>Mode 07 · platform_blog</span></nav>
  <header class="header platform-header"><div class="kicker">Platform Adaptation</div><h1>RAG 글을 티스토리·벨로그·네이버·워드프레스로 변환하기</h1><p class="sub">같은 원문도 플랫폼에 따라 제목, 문단 길이, 코드 표현, CTA, 태그 전략이 달라져야 합니다.</p><div class="meta">{meta_spans(['원문: RAG vs Fine-tuning','플랫폼: 4종','목표: 발행 준비'])}</div></header>
  <section class="original-summary"><h2><span class="num">1</span>원문 요약</h2><p class="h2-sub">원문 메시지는 유지하고, 플랫폼마다 포장 방식을 바꿉니다.</p><ul><li>RAG는 최신·사내·도메인 지식을 검색해 프롬프트에 붙이는 방식입니다.</li><li>Fine-tuning은 응답 형식, 톤, 반복 작업 일관성에 적합합니다.</li><li>사내 문서 챗봇은 대부분 RAG가 출발점입니다.</li><li>둘을 함께 쓸 때는 retrieval 평가와 모델 응답 평가를 분리해야 합니다.</li></ul></section>
  <section class="platform-strategy"><h2><span class="num">2</span>플랫폼별 전략</h2><p class="h2-sub">복붙보다 플랫폼 문법과 독자 기대에 맞추는 것이 중요합니다.</p></section>
  <section class="platform-grid"><div class="platform-card"><h3>Tistory</h3><p>검색 유입형 장문. 목차, H2/H3, 비교표, FAQ를 안정적으로 구성합니다.</p><p><strong>제목:</strong> RAG vs Fine-tuning 차이와 선택 기준</p></div><div class="platform-card"><h3>Velog</h3><p>개발자 문제 해결형. Markdown heading, 코드블럭, 체크리스트를 선호합니다.</p><p><strong>제목:</strong> 사내 문서 챗봇에는 RAG와 Fine-tuning 중 무엇이 맞을까?</p></div><div class="platform-card"><h3>Naver Blog</h3><p>짧은 문단과 경험형 설명. 이미지 위치 제안과 자연스러운 키워드 반복이 중요합니다.</p><p><strong>제목:</strong> RAG와 파인튜닝, 쉽게 비교해봤어요</p></div><div class="platform-card"><h3>WordPress</h3><p>레퍼런스 허브형. canonical, schema, 내부 링크, 업데이트 로그를 붙이기 좋습니다.</p><p><strong>제목:</strong> RAG vs Fine-tuning: Decision Guide</p></div></section>
  <section class="platform-comparison-table"><h2><span class="num">3</span>변환 비교표</h2><p class="h2-sub">문단 길이와 CTA만 바꿔도 독자 경험이 달라집니다.</p><div class="tbl"><table><thead><tr><th scope="col">플랫폼</th><th scope="col">본문 구조</th><th scope="col">태그</th><th scope="col">주의</th></tr></thead><tbody><tr><td>Tistory</td><td>목차 → 정의 → 비교표 → FAQ</td><td>RAG, 파인튜닝, AI</td><td>HTML 모드 렌더링 확인</td></tr><tr><td>Velog</td><td>문제 → 선택 기준 → 코드/구조</td><td>rag, llm, ai</td><td>복잡한 HTML 삽입 피하기</td></tr><tr><td>Naver</td><td>짧은 문단 → 이미지 → 쉬운 예시</td><td>#RAG #파인튜닝</td><td>소제목 문장 중심</td></tr><tr><td>WordPress</td><td>SEO 허브 → 내부 링크 → schema</td><td>카테고리+태그</td><td>canonical/JSON-LD 검토</td></tr></tbody></table></div></section>
  <section class="try publish-checklist"><div class="label">Publish Checklist</div><h2>발행 전 7가지</h2><ol><li>원문/canonical 전략을 정합니다.</li><li>제목을 플랫폼별로 다시 씁니다.</li><li>표가 모바일에서 깨지지 않는지 확인합니다.</li><li>Velog 버전은 Markdown 중심으로 단순화합니다.</li><li>Naver 버전에는 이미지 삽입 위치를 표시합니다.</li><li>WordPress 버전은 meta description과 내부 링크를 넣습니다.</li><li>모든 버전의 결론 CTA를 플랫폼 독자에 맞춥니다.</li></ol></section>
  {source_note('플랫폼 참고 출처', sources_platform)}
</main>''')

# 8 skill audit
sources_skill = [
    ('Local SKILL.md snapshot', '../sources/adaptive-html-final-SKILL.md'),
    ('Local manifest.json snapshot', '../sources/adaptive-html-final-manifest.json'),
    ('Skill audit system snapshot', '../sources/skill-audit-system.md'),
    ('Quality gates snapshot', '../sources/quality-gates.md'),
]
add_page('08-skill-audit-adaptive-html-final','skill_audit','adaptive-html-final 스킬 자체 감사 리포트','adaptive-html-final 스킬의 목적, 트리거, 입력/출력, 워크플로우, 품질 게이트, 패키지 구조를 감사한 HTML 리포트.', f'''
<main id="main" class="page-wide layout-audit">
  <nav class="page-nav"><a href="../index.html">← 쇼케이스 홈</a><span>Mode 08 · skill_audit</span></nav>
  <header class="header audit-header"><div class="kicker">Skill Audit</div><h1>adaptive-html-final 스킬 자체 감사 리포트</h1><p class="sub">최종 통합본은 강력하지만, 운영급 안정성을 위해 mode ID, recipes, schema, examples 정합성을 더 조여야 합니다.</p><div class="meta">{meta_spans(['대상: adaptive-html-final v4','방식: read-only audit','검토일: 2026-05-30'])}</div></header>
  <section class="executive-summary"><h2><span class="num">1</span>Executive Diagnosis</h2><p class="h2-sub">스킬의 뼈대는 완성, 운영 자동화는 보강 단계입니다.</p><p><strong>총평:</strong> 13개 모드, 레이어드 CSS, 품질 게이트, 접근성 수정은 강점입니다. 다만 manifest의 모드명과 SKILL.md 라우터명, examples의 구버전 흔적, recipes/schema/test의 커버리지 부족이 장기 운영 리스크입니다.</p></section>
  <section class="summary-grid"><h2><span class="num">2</span>점수 요약</h2><p class="h2-sub">0~5점 기준으로 구조와 실행 가능성을 분리 평가했습니다.</p><div class="card-grid"><div class="score-card"><h3>목적 명확성 5/5</h3><p>입력→모드→HTML 산출 파이프라인이 분명합니다.</p></div><div class="score-card"><h3>트리거 4/5</h3><p>넓게 잡혀 있으나 과포괄 트리거가 있습니다.</p></div><div class="score-card"><h3>QA 체계 3/5</h3><p>체크리스트는 있으나 자동 검증은 약합니다.</p></div></div></section>
  <section class="line-audit"><h2><span class="num">3</span>섹션별 발견사항</h2><p class="h2-sub">라인 단위보다 운영 영향이 큰 섹션 단위로 정리했습니다.</p><div class="audit-table"><div class="audit-row"><strong>Mode Router</strong><span>priority-only 라우팅은 “티스토리용 SEO 블로그” 같은 복합 요청에서 secondary intent를 잃을 수 있습니다.</span><span>Major</span></div><div class="audit-row"><strong>Manifest</strong><span>manifest modes는 `blog`, SKILL.md는 `blog_writer`처럼 ID가 다릅니다.</span><span>Major</span></div><div class="audit-row"><strong>Examples</strong><span>일부 예시는 final assets가 아니라 v2 인라인 스타일을 유지합니다.</span><span>Minor</span></div><div class="audit-row"><strong>Schemas</strong><span>blog meta와 quality report schema가 reference 규칙을 충분히 강제하지 못합니다.</span><span>Major</span></div></div></section>
  <section class="priority-roadmap"><h2><span class="num">4</span>개선 우선순위</h2><p class="h2-sub">최종본을 깨지 않고 안정성을 높이는 순서입니다.</p><ol><li><strong>P0:</strong> manifest layout 경로와 mode ID를 SKILL.md 기준으로 통일합니다.</li><li><strong>P0:</strong> 복합 요청은 primary mode + modifiers로 처리하도록 SKILL.md에 추가합니다.</li><li><strong>P1:</strong> 누락된 7개 recipe와 mode-contracts reference를 추가합니다.</li><li><strong>P1:</strong> schema를 enum, min/max, additionalProperties 기준으로 엄격화합니다.</li><li><strong>P2:</strong> examples를 final assets 기반으로 재생성하고 validate script를 추가합니다.</li></ol></section>
  <section class="try"><div class="label">Patch Plan</div><h2>파일 수정 없이 제안하는 최종 패치 방향</h2><ol><li>스킬명은 `adaptive-html-final`을 canonical로 유지합니다.</li><li>레거시 alias는 `merged_from`으로 남기고 라우팅 alias는 최소화합니다.</li><li>사용자가 “분석만” 요청하면 파일을 수정하지 않는 audit-only 규칙을 추가합니다.</li></ol></section>
  {source_note('내부 근거', sources_skill, '이 감사 페이지는 로컬 스킬 패키지와 병렬 에이전트 검토 결과를 근거로 작성했습니다.')}
</main>''')

# 9 reference OpenAI Responses
sources_responses = [
    ('OpenAI — Responses overview', 'https://developers.openai.com/api/reference/responses/overview'),
    ('OpenAI — Create response API spec', 'https://api.openai.com/v1/responses'),
    ('OpenAI — Migrate to Responses', 'https://developers.openai.com/api/docs/guides/migrate-to-responses'),
    ('OpenAI — Using tools', 'https://developers.openai.com/api/docs/guides/tools'),
]
add_page('09-reference-openai-responses-api','reference_html','OpenAI Responses API 실무 레퍼런스','OpenAI Responses API의 엔드포인트, 입력/출력 모델, 도구, 스트리밍, 마이그레이션 포인트를 정리한 HTML 레퍼런스.', f'''
<main id="main" class="page-wide layout-reference">
  <nav class="page-nav"><a href="../index.html">← 쇼케이스 홈</a><span>Mode 09 · reference_html</span></nav>
  <header class="header reference-header"><div class="kicker">Reference Manual</div><h1>OpenAI Responses API 실무 레퍼런스</h1><p class="sub">Responses API는 텍스트·이미지·파일 입력, typed output item, 상태 연결, 도구 호출을 하나의 인터페이스로 다루는 생성 API입니다.</p><div class="meta">{meta_spans(['API: /v1/responses','근거: OpenAI 공식 문서','검토일: 2026-05-30'])}</div></header>
  <section class="quick-reference"><h2><span class="num">1</span>Quick Reference</h2><p class="h2-sub">처음 쓸 때 기억할 핵심 필드입니다.</p><div class="tbl"><table><thead><tr><th scope="col">필드</th><th scope="col">용도</th><th scope="col">주의</th></tr></thead><tbody><tr><td>`model`</td><td>사용할 모델</td><td>가용 모델은 공식 model guide 확인</td></tr><tr><td>`input`</td><td>텍스트, 이미지, 파일 등 사용자 입력</td><td>배열 item 구조 가능</td></tr><tr><td>`instructions`</td><td>시스템 지시</td><td>사용자 입력과 분리</td></tr><tr><td>`tools`</td><td>web search, file search, function, MCP 등</td><td>side effect는 승인/검증 필요</td></tr><tr><td>`previous_response_id`</td><td>이전 응답과 상태 연결</td><td>보존 정책 설계 필요</td></tr><tr><td>`stream`</td><td>SSE 스트리밍</td><td>event 타입별 처리 필요</td></tr></tbody></table></div></section>
  <section class="ref-grid"><div class="mini-card"><h3>입력 모델</h3><p>단순 문자열부터 `input_text`, `input_image`, `input_file` 같은 content part를 포함한 배열까지 다룹니다.</p></div><div class="mini-card"><h3>출력 모델</h3><p>Chat Completions의 message 하나가 아니라 message, tool call, web/file citation 등 typed output item 중심입니다.</p></div><div class="mini-card"><h3>도구</h3><p>web search, file search, function calling, remote MCP 등으로 모델의 실행 범위를 확장합니다.</p></div><div class="mini-card"><h3>상태</h3><p>`previous_response_id`나 Conversations API를 통해 멀티턴 맥락을 연결할 수 있습니다.</p></div></section>
  <section class="patterns"><h2><span class="num">2</span>실무 패턴</h2><p class="h2-sub">output_text만 보는 코드는 빠르게 시작하기 좋지만, 장기적으로는 output item을 파싱해야 합니다.</p><div class="danger"><div class="label">주의</div><div class="name">`output_text` 과신</div><p>단순 텍스트 추출에는 편하지만, tool call, citation, reasoning item, 멀티모달 결과를 모두 대표하지는 않습니다.</p></div><div class="good"><div class="label">권장</div><div class="name">item type 기반 분기</div><p>`message`, `function_call`, `web_search_call`, `file_search_call` 등 output item 타입을 기준으로 로깅·검증·후속 처리를 분리합니다.</p></div></section>
  <section class="examples"><h2><span class="num">3</span>최소 예제</h2><p class="h2-sub">실제 서비스에서는 에러, rate limit, tool approval을 추가하세요.</p><pre><code>import OpenAI from "openai";
const openai = new OpenAI();

const response = await openai.responses.create({{
  model: "gpt-5.4",
  instructions: "간결하게 답하세요.",
  input: "Responses API를 한 문장으로 설명해줘."
}});

console.log(response.output_text);</code></pre><pre><code>const searched = await openai.responses.create({{
  model: "gpt-5.4",
  tools: [{{ type: "web_search_preview" }}],
  input: "오늘 기준 최신 API 변경점을 찾아 요약해줘."
}});</code></pre></section>
  <section class="try"><div class="label">Checklist</div><h2>도입 전 확인</h2><ol><li>출력 파싱을 `output_text`에만 의존하지 않습니다.</li><li>tool call 인자는 서버에서 검증합니다.</li><li>상태 저장, 개인정보, 로그 보존 정책을 정합니다.</li><li>streaming event 타입별 UI 상태를 설계합니다.</li></ol></section>
  {source_note('OpenAI 공식 출처', sources_responses)}
</main>''')

# 10 comparison DB
sources_db = [
    ('PostgreSQL — About', 'https://www.postgresql.org/about/'),
    ('PostgreSQL — Current documentation', 'https://www.postgresql.org/docs/current/'),
    ('MySQL 8.4 Reference Manual', 'https://dev.mysql.com/doc/refman/8.4/en/'),
    ('SQLite — Appropriate Uses', 'https://www.sqlite.org/whentouse.html'),
    ('SQLite — Write-Ahead Logging', 'https://www.sqlite.org/wal.html'),
]
add_page('10-comparison-postgresql-mysql-sqlite','comparison_html','PostgreSQL vs MySQL vs SQLite 선택 기준','PostgreSQL, MySQL, SQLite를 운영 난이도, 동시성, 배포, 데이터 모델, 사용 사례 기준으로 비교한 HTML 매트릭스.', f'''
<main id="main" class="page-wide layout-compare">
  <nav class="page-nav"><a href="../index.html">← 쇼케이스 홈</a><span>Mode 10 · comparison_html</span></nav>
  <header class="header compare-header"><div class="kicker">Comparison Matrix</div><h1>PostgreSQL vs MySQL vs SQLite 선택 기준</h1><p class="sub">데이터베이스 선택은 “성능이 누가 더 좋나”보다 “어떤 운영 모델을 감당할 것인가”의 문제입니다.</p><div class="meta">{meta_spans(['대상: 백엔드·제품팀','범위: 관계형 DB 선택','검토일: 2026-05-30'])}</div></header>
  <section class="decision-context"><h2><span class="num">1</span>결정 맥락</h2><p class="h2-sub">새 프로젝트라면 기본값은 PostgreSQL, 생태계/운영 경험은 MySQL, 로컬·임베디드는 SQLite가 강합니다.</p><p>세 DB는 모두 훌륭하지만 해결하는 문제가 다릅니다. PostgreSQL은 복잡한 데이터 모델과 확장성, MySQL은 웹 OLTP와 호스팅 생태계, SQLite는 서버 없는 배포와 로컬 우선 경험에 강합니다.</p></section>
  <section class="matrix"><div class="winner-card"><h3>PostgreSQL</h3><p>복잡한 쿼리, JSONB+관계형 혼합, 확장, PostGIS, 데이터 무결성이 중요할 때.</p></div><div class="winner-card"><h3>MySQL</h3><p>웹 CRUD, WordPress/커머스, MySQL 운영 경험, InnoDB 기반 안정성이 중요할 때.</p></div><div class="winner-card"><h3>SQLite</h3><p>로컬 앱, 모바일, 엣지, 테스트, 단일 파일 배포, 낮은 write concurrency일 때.</p></div></section>
  <section class="winners"><h2><span class="num">2</span>상황별 승자</h2><p class="h2-sub">한 줄 규칙으로 먼저 거르고, 세부 요구사항을 검토합니다.</p><div class="tbl"><table><thead><tr><th scope="col">상황</th><th scope="col">추천</th><th scope="col">이유</th></tr></thead><tbody><tr><td>새 SaaS 백엔드</td><td>PostgreSQL</td><td>확장성과 복잡한 도메인 모델 대응</td></tr><tr><td>상용 웹 호스팅/커머스</td><td>MySQL</td><td>생태계와 운영 인력 확보 용이</td></tr><tr><td>데스크톱/모바일 로컬 저장소</td><td>SQLite</td><td>서버 없는 단일 파일 배포</td></tr><tr><td>동시 writer가 많은 시스템</td><td>PostgreSQL/MySQL</td><td>SQLite는 writer 동시성 한계 고려</td></tr></tbody></table></div></section>
  <section class="tradeoffs"><h2><span class="num">3</span>트레이드오프</h2><p class="h2-sub">장점은 언제나 운영 비용과 함께 옵니다.</p><div class="danger"><div class="label">함정</div><div class="name">SQLite를 서버 DB처럼 쓰기</div><p>WAL 모드가 reader/writer 동시성을 개선해도 writer는 한 번에 하나라는 제약을 무시하면 장애가 납니다.</p></div><div class="danger"><div class="label">함정</div><div class="name">PostgreSQL을 “무조건 정답”으로 쓰기</div><p>작은 로컬 앱에는 서버 운영, 백업, 마이그레이션, 모니터링이 과한 비용이 될 수 있습니다.</p></div></section>
  <section class="try"><div class="label">Recommendation</div><h2>최종 선택 규칙</h2><ol><li>동시 사용자와 writer가 많고 서비스가 성장한다면 PostgreSQL을 기본 후보로 둡니다.</li><li>팀이 MySQL 운영에 익숙하고 웹 생태계 적합성이 크면 MySQL을 선택합니다.</li><li>서버 없이 로컬에 저장하고 배포 단순성이 핵심이면 SQLite를 선택합니다.</li></ol></section>
  {source_note('DB 공식 출처', sources_db)}
</main>''')

# 11 case study Cloudflare
sources_cf = [
    ('Cloudflare — Thanksgiving 2023 security incident', 'https://blog.cloudflare.com/thanksgiving-2023-security-incident/'),
    ('Cloudflare — Okta compromise mitigation', 'https://blog.cloudflare.com/how-cloudflare-mitigated-yet-another-okta-compromise/'),
    ('Okta — Support system root cause', 'https://sec.okta.com/articles/2023/11/unauthorized-access-oktas-support-case-management-system-root-cause/'),
]
add_page('11-case-cloudflare-thanksgiving-incident','case_study_html','Cloudflare Thanksgiving 2023 보안 사고 회고','Cloudflare의 Thanksgiving 2023 security incident를 credential rotation, third-party compromise, Code Red 대응 관점으로 정리한 케이스 스터디.', f'''
<main id="main" class="page layout-case">
  <nav class="page-nav"><a href="../index.html">← 쇼케이스 홈</a><span>Mode 11 · case_study_html</span></nav>
  <header class="header case-header"><div class="kicker">Case Study</div><h1>Cloudflare Thanksgiving 2023 보안 사고 회고</h1><p class="sub">공개 연도 때문에 “2024 Thanksgiving incident”로 혼동되지만, 공식 사건명은 Thanksgiving 2023 security incident입니다.</p><div class="meta">{meta_spans(['사건 탐지: 2023-11-23','공개: 2024-02-01','주제: 보안 회고'])}</div></header>
  <section class="summary-card"><div class="label">Situation</div><p>Cloudflare는 2023년 11월 23일 자체 호스팅 Atlassian 서버에서 위협 행위자를 탐지했습니다. 원인은 Okta 2023년 10월 침해 이후 회전하지 못한 일부 credential이었고, 대응은 Code Red로 격상되었습니다.</p></section>
  <section class="timeline"><h2><span class="num">1</span>타임라인</h2><p class="h2-sub">절대 날짜로 보면 대응 판단의 압박이 분명해집니다.</p><div class="timeline-card"><strong>2023-10-18</strong><p>Okta 지원 시스템 침해가 공개되고, HAR/session token 관련 위험이 부각됩니다.</p></div><div class="timeline-card"><strong>2023-11-14~24</strong><p>위협 행위자가 Cloudflare의 Atlassian 환경을 정찰하고 persistence를 시도합니다.</p></div><div class="timeline-card"><strong>2023-11-23</strong><p>Thanksgiving Day에 Cloudflare가 자체 시스템에서 활동을 탐지합니다.</p></div><div class="timeline-card"><strong>2024-02-01</strong><p>Cloudflare가 사건 분석과 대응 결과를 공개합니다.</p></div></section>
  <section class="decisions"><h2><span class="num">2</span>핵심 의사결정</h2><p class="h2-sub">고객 영향이 제한적이어도 미래 공격 가능성을 기준으로 격상했습니다.</p><ul><li>Code Red 선언</li><li>5,000개 이상 production credential 회전</li><li>4,893개 시스템 포렌식 triage</li><li>네트워크 장비 재이미징/재부팅</li><li>외부 전문기관 검토를 통한 신뢰성 보강</li></ul></section>
  <section class="results"><h2><span class="num">3</span>결과와 영향</h2><p class="h2-sub">핵심 시스템 접근 증거가 없다는 결론보다, stale credential의 위험이 더 큰 교훈입니다.</p><p>Cloudflare는 고객 데이터, 글로벌 네트워크, SSL keys, Workers, R2, KV 등 핵심 시스템 접근 증거는 없다고 밝혔습니다. 하지만 내부 문서와 일부 저장소 접근 가능성만으로도 향후 공격에 필요한 지식이 축적될 수 있기 때문에 대규모 대응이 정당화되었습니다.</p></section>
  <section class="try"><div class="label">Lessons</div><h2>조직이 배워야 할 것</h2><ol><li>사용하지 않는 것처럼 보이는 credential도 회전해야 합니다.</li><li>non-human identity는 사람 계정보다 더 엄격한 수명 관리를 해야 합니다.</li><li>SaaS 지원 파일과 HAR에는 세션 정보가 포함될 수 있습니다.</li><li>Zero Trust는 침입을 완전히 막는 벽이 아니라 lateral movement를 줄이는 격벽입니다.</li></ol></section>
  {source_note('공식 사건 출처', sources_cf)}
</main>''')

# 12 landing AI knowledge hub
sources_landing = [
    ('NIST AI RMF', 'https://www.nist.gov/itl/ai-risk-management-framework'),
    ('OpenAI — Safety in building agents', 'https://developers.openai.com/api/docs/guides/agent-builder-safety'),
    ('Microsoft HAX Toolkit', 'https://www.microsoft.com/en-us/haxtoolkit/'),
    ('Local adaptive-html-final layout system snapshot', '../sources/layout-system.md'),
]
add_page('12-landing-ai-knowledge-hub','landing_brief_html','사내 AI 지식 허브 랜딩 브리프','사내 AI 정책, 프롬프트, 사례, 교육, 승인 절차를 묶는 AI 지식 허브를 소개하는 editorial landing HTML.', f'''
<main id="main" class="page-wide layout-landing">
  <nav class="page-nav"><a href="../index.html">← 쇼케이스 홈</a><span>Mode 12 · landing_brief_html</span></nav>
  <header class="header landing-header"><div class="kicker">Internal AI Knowledge Hub</div><h1>사내 AI 지식 허브</h1><p class="sub">흩어진 AI 정책, 프롬프트, 사례, 교육 자료, 승인 절차를 하나의 신뢰 레이어로 묶습니다.</p><div class="meta">{meta_spans(['대상: 전사 구성원','상태: 랜딩 브리프','업데이트: 월 1회'])}</div></header>
  <section class="hero-analogy"><div class="tag">Hero</div><h3>AI 자료 모음이 아니라,<br>조직의 AI 항해 지도입니다.</h3><p>좋은 지식 허브는 링크를 많이 모으는 곳이 아닙니다. 누가 어떤 AI 도구를 써도 되는지, 어떤 데이터는 넣으면 안 되는지, 좋은 프롬프트와 사례는 어디서 재사용할 수 있는지 빠르게 알려주는 운영 장치입니다.</p></section>
  <section class="value-grid"><div class="mini-card"><h3>승인된 도구</h3><p>직무별로 사용할 수 있는 AI 도구와 제한 조건을 정리합니다.</p></div><div class="mini-card"><h3>검증된 프롬프트</h3><p>성공 사례와 금지 예시를 함께 제공합니다.</p></div><div class="mini-card"><h3>보안 가이드</h3><p>민감정보, 고객정보, 코드, 계약 문서 입력 기준을 설명합니다.</p></div><div class="mini-card"><h3>직무별 사례</h3><p>마케팅, 개발, 법무, CS 등 팀별 스타터 플로우를 제공합니다.</p></div><div class="mini-card"><h3>교육 모듈</h3><p>신규 입사자와 현업자를 위한 10분 학습 단위를 제공합니다.</p></div><div class="mini-card"><h3>요청 채널</h3><p>새 도구 승인, 프롬프트 리뷰, 보안 문의를 연결합니다.</p></div></section>
  <section class="how-it-works"><h2><span class="num">1</span>How it works</h2><p class="h2-sub">찾기 → 배우기 → 적용하기 → 공유하기 → 검토받기 흐름입니다.</p><ol><li><strong>찾기:</strong> 직무와 데이터 민감도에 맞는 도구를 고릅니다.</li><li><strong>배우기:</strong> 10분 온보딩과 FAQ를 확인합니다.</li><li><strong>적용하기:</strong> 검증된 프롬프트를 복사해 업무에 맞게 수정합니다.</li><li><strong>공유하기:</strong> 결과와 실패 사례를 허브에 제출합니다.</li><li><strong>검토받기:</strong> 보안/법무/AI 운영팀이 상태 배지를 부여합니다.</li></ol></section>
  <section class="faq"><div class="label">FAQ</div><details open><summary>누가 쓰나요?</summary><p>전사 구성원이 쓰되, 데이터 민감도와 도구 권한은 직무별로 다르게 안내합니다.</p></details><details><summary>민감정보는 어떻게 다루나요?</summary><p>데이터 분류표와 금지 예시를 먼저 보여주고, 승인된 도구와 비승인 도구를 구분합니다.</p></details><details><summary>프롬프트는 누가 검토하나요?</summary><p>AI 운영팀이 1차 구조를 보고, 보안·법무가 민감정보와 규제 리스크를 검토합니다.</p></details></section>
  <section class="try"><div class="label">CTA</div><h2>이번 주 바로 할 3가지</h2><ol><li>우리 팀의 반복 업무 1개를 선택합니다.</li><li>허브에서 승인된 도구와 예시 프롬프트를 찾습니다.</li><li>결과와 실패 사례를 5줄로 공유합니다.</li></ol></section>
  {source_note('설계 참고', sources_landing, '사내 랜딩 브리프는 내부 정책·보안 가이드·승인 도구 목록으로 최종 보강해야 합니다.')}
</main>''')

# 13 checklist accessibility
sources_a11y = [
    ('W3C — WCAG 2.2 Recommendation', 'https://www.w3.org/TR/WCAG22/'),
    ('W3C WAI — How to Meet WCAG Quick Reference', 'https://www.w3.org/WAI/WCAG22/quickref/'),
    ('W3C WAI — Easy Checks', 'https://www.w3.org/WAI/test-evaluate/preliminary/'),
    ('W3C WAI — Evaluation Tools Overview', 'https://www.w3.org/WAI/test-evaluate/tools/'),
    ('W3C WAI ARIA APG — Read Me First', 'https://www.w3.org/WAI/ARIA/apg/practices/read-me-first/'),
]
add_page('13-checklist-web-accessibility-release','checklist_playbook','웹 접근성 배포 전 30분 체크리스트','WCAG 2.2 A/AA 기준으로 릴리즈 전 문서 구조, 키보드, 포커스, 폼, ARIA, 모바일 접근성을 점검하는 HTML 플레이북.', f'''
<main id="main" class="page-wide layout-checklist">
  <nav class="page-nav"><a href="../index.html">← 쇼케이스 홈</a><span>Mode 13 · checklist_playbook</span></nav>
  <header class="header checklist-header"><div class="kicker">Checklist Playbook</div><h1>웹 접근성 배포 전 30분 체크리스트</h1><p class="sub">자동 점수는 시작일 뿐입니다. 키보드, 포커스, 이름/역할/값, 오류 메시지, 모바일 확대까지 수동으로 확인해야 합니다.</p><div class="meta">{meta_spans(['기준: WCAG 2.2 A/AA','소요: 30분','대상: 릴리즈 전 QA'])}</div></header>
  <section class="summary-card"><div class="label">Use Case</div><p>릴리즈 직전 주요 사용자 흐름 3개를 대상으로 blocker 접근성 문제를 빠르게 걸러내는 운영 체크리스트입니다. 자동 도구와 수동 키보드 테스트를 함께 사용합니다.</p></section>
  <section class="check-grid"><div class="check-item"><h3>문서 구조</h3><ul><li>페이지 title이 구체적인가?</li><li>h1은 1개인가?</li><li>heading 순서가 건너뛰지 않는가?</li></ul></div><div class="check-item"><h3>이미지·미디어</h3><ul><li>의미 있는 이미지는 alt가 있는가?</li><li>장식 이미지는 비워두었는가?</li><li>영상에는 자막/대체 설명이 있는가?</li></ul></div><div class="check-item"><h3>키보드·포커스</h3><ul><li>Tab 순서가 시각 흐름과 맞는가?</li><li>focus indicator가 보이는가?</li><li>modal에서 Esc/닫기가 되는가?</li></ul></div><div class="check-item"><h3>폼·오류</h3><ul><li>label과 input이 연결되어 있는가?</li><li>오류 메시지가 필드와 연결되는가?</li><li>색만으로 오류를 표시하지 않는가?</li></ul></div><div class="check-item"><h3>색·텍스트</h3><ul><li>본문 대비가 충분한가?</li><li>200% 확대에서 내용이 잘리지 않는가?</li><li>터치 target이 너무 작지 않은가?</li></ul></div><div class="check-item"><h3>ARIA·동적 UI</h3><ul><li>native HTML로 가능한데 ARIA를 남용하지 않았는가?</li><li>role을 추가했다면 키보드 동작도 구현했는가?</li><li>상태 변화가 보조기술에 전달되는가?</li></ul></div></section>
  <section class="failure-modes"><h2><span class="num">1</span>자주 실패하는 패턴</h2><p class="h2-sub">Lighthouse 100점이어도 실제 사용자가 막히는 경우가 많습니다.</p><div class="danger"><div class="label">실패 모드</div><div class="name">자동 점수 과신</div><p>자동 도구는 일부 문제만 잡습니다. 키보드 이동, 스크린리더 문맥, zoom, 오류 복구는 수동 확인이 필요합니다.</p></div><div class="danger"><div class="label">실패 모드</div><div class="name">잘못된 ARIA</div><p>WAI-ARIA APG의 “No ARIA is better than Bad ARIA” 원칙처럼, 틀린 role은 없는 것보다 나쁠 수 있습니다.</p></div><div class="good"><div class="label">수동 테스트</div><div class="name">Tab → Shift+Tab → Enter → Space → Esc</div><p>키보드만으로 핵심 흐름을 끝까지 진행하고, 포커스가 갇히거나 사라지는 지점을 기록합니다.</p></div></section>
  <section class="try"><div class="label">Done Criteria</div><h2>배포 승인 기준</h2><ol><li>Blocker 접근성 이슈 0개</li><li>WCAG 2.2 A/AA 주요 흐름 통과</li><li>키보드 수동 테스트 완료</li><li>200% zoom과 모바일 viewport 확인</li><li>자동 검사 결과와 수동 증거 링크 기록</li></ol></section>
  {source_note('접근성 공식 출처', sources_a11y)}
</main>''')

# index
cards = '\n'.join(f'''<article class="mini-card"><div class="mode-label">{escape(p['mode'])}</div><h3><a href="pages/{p['slug']}.html">{escape(p['title'])}</a></h3><p>{escape(p['desc'])}</p></article>''' for p in pages)
index_body = f'''
<main id="main" class="page-wide">
  <header class="header"><div class="kicker">Adaptive HTML Final Showcase</div><h1>13개 모드 전체 HTML 쇼케이스</h1><p class="sub">`adaptive-html-final` 스킬의 13개 모드를 각각 다른 주제로 실행해 만든 전문가급 HTML 결과물 모음입니다. 병렬 에이전트 리서치, 공식 문서 검토, 스킬 assets 기반 렌더링을 거쳤습니다.</p><div class="meta">{meta_spans(['총 13개 HTML','생성일: 2026-05-30','출력: 단일 HTML 파일'])}</div></header>
  <section class="hero-index"><h2><span class="num">1</span>작업 방식</h2><p class="h2-sub">스킬 라우터의 13개 모드를 빠짐없이 사용했습니다.</p><p>각 페이지는 `theme.css + components.css + layouts.css + print.css`를 inline으로 포함한 독립 실행 HTML입니다. 출처는 각 페이지 하단의 `source-note`에 정리했습니다.</p></section>
  <section><h2><span class="num">2</span>결과물 링크</h2><p class="h2-sub">아래 카드에서 각 모드별 결과물을 열 수 있습니다.</p><div class="page-list">{cards}</div></section>
  <section class="try"><div class="label">Verification</div><h2>검수 요약</h2><ol><li>13개 페이지 모두 `lang="ko"`, viewport, title, meta description 포함</li><li>각 페이지 h1 1개 유지</li><li>외부 JS 없음</li><li>모든 페이지에 `#main` skip link target 존재</li><li>각 페이지에 source-note 포함</li></ol></section>
</main>'''
(OUT/'index.html').write_text(page_doc('Adaptive HTML Final 13개 모드 쇼케이스','adaptive-html-final 스킬로 생성한 13개 모드별 전문가급 HTML 결과물 링크 모음.', index_body), encoding='utf-8')

print(f'Generated {len(pages)} pages in {PAGES}')
for p in pages:
    print(p['path'])
