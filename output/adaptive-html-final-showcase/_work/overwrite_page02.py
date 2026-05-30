from pathlib import Path
from html import escape
ROOT = Path('/Users/hwanchoi/project_202605/skills-html-showcase')
page = ROOT/'output/adaptive-html-final-showcase/pages/02-expert-eu-ai-act-governance.html'
old = page.read_text()
head = old.split('<body>')[0]
# Fix the caption CSS that caused the clipped/weak table caption.
head = head.replace('.caption{font-size:12px;color:var(--ink-mute);margin-top:-8px}', '.caption{caption-side:top;text-align:left;font-size:13px;color:var(--ink);font-weight:800;margin:0;padding:0 0 8px}')
head = head.replace('<title>EU AI Act 기반 생성형 AI 거버넌스 실행 리포트</title>', '<title>EU AI Act 기반 생성형 AI 거버넌스 운영모델 상세 리포트</title>')
head = head.replace('EU AI Act와 GPAI 의무를 기준으로 생성형 AI 제품·조직이 준비해야 할 거버넌스 로드맵을 정리한 전문가 리포트.', 'EU AI Act와 GPAI 의무를 기준으로 생성형 AI 제품·조직의 운영모델, RACI, 리스크, 90일 로드맵, 감사 증빙을 상세 정리한 전문가 리포트.')

def spans(items):
    return ''.join(f'<span>{escape(x)}</span>' for x in items)

sources = [
    ('EUR-Lex — Regulation (EU) 2024/1689', 'https://eur-lex.europa.eu/eli/reg/2024/1689/oj'),
    ('EU AI Act Service Desk — Implementation timeline', 'https://ai-act-service-desk.ec.europa.eu/en/ai-act/eu-ai-act-implementation-timeline'),
    ('European Commission — GPAI obligations', 'https://digital-strategy.ec.europa.eu/en/factpages/general-purpose-ai-obligations-under-ai-act'),
    ('European Commission — GPAI Code of Practice', 'https://digital-strategy.ec.europa.eu/en/policies/contents-code-gpai'),
]
source_lis = ''.join(f'<li><a href="{url}">{name}</a></li>' for name,url in sources)
body = f'''
<body>
<a class="skip" href="#main">본문 바로가기</a>
<main id="main" class="page-wide layout-expert">
  <nav class="page-nav"><a href="../index.html">← 쇼케이스 홈</a><span>Mode 02 · expert_html · revised</span></nav>
  <header class="header report-header">
    <div class="kicker">Expert Report</div>
    <h1>EU AI Act 기반 생성형 AI 거버넌스 운영모델 상세 리포트</h1>
    <p class="sub">생성형 AI 거버넌스는 정책 문서 한 장이 아니라, <strong>AI 인벤토리, 역할 분류, 위험 등급, 공급망 증빙, 사용자 고지, 사고 대응</strong>이 연결된 운영 체계입니다.</p>
    <div class="meta">{spans(['대상: AI 제품·법무·보안·데이터 리더','범위: EU AI Act·GPAI·고위험·투명성','검토일: 2026-05-30','주의: 법률 자문 아님'])}</div>
  </header>

  <section class="executive-summary">
    <h2><span class="num">1</span>Executive Summary</h2>
    <p class="h2-sub">지금 해야 할 일은 “법 조항 읽기”가 아니라 감사 가능한 운영 증거를 만드는 것입니다.</p>
    <p><strong>핵심 결론:</strong> EU AI Act 대응은 모델 하나를 심사하는 일이 아닙니다. 조직은 먼저 자신이 <em class="t">GPAI model provider</em>인지, 특정 목적의 <em class="t">AI system provider</em>인지, 또는 외부 시스템을 사용하는 <em class="t">deployer</em>인지 분류해야 합니다. 그 다음 사용 사례별로 금지 관행, 고위험 영역, 투명성 고지, 저작권·데이터 증빙, 사고 대응 의무를 연결해야 합니다.</p>
    <div class="summary-grid">
      <div class="mini-card"><h3>오늘</h3><p>AI 시스템 인벤토리, 소유자, 사용 목적, 모델 공급자를 한 표로 정리합니다.</p></div>
      <div class="mini-card"><h3>30일</h3><p>금지 관행·고위험·GPAI·투명성 의무를 use case 단위로 1차 분류합니다.</p></div>
      <div class="mini-card"><h3>90일</h3><p>증빙 저장소, 변경 승인, 평가 로그, 사고 대응 훈련을 출시 게이트에 넣습니다.</p></div>
    </div>
    <div class="danger"><div class="label">중요</div><div class="name">“우리는 모델을 직접 학습하지 않는다”는 면책이 아니다</div><p>외부 LLM을 API로 쓰더라도 제품 제공자나 배포자로서 사용자 고지, 위험관리, 공급망 증빙, 로그·사고 대응 책임이 남을 수 있습니다. 역할과 책임을 계약·제품·운영 문서에서 분리해야 합니다.</p></div>
  </section>

  <section class="decision-grid">
    <div class="decision-card"><h3>1. 역할 분류</h3><p>Provider, deployer, importer/distributor, product manufacturer를 분리합니다. 같은 조직도 제품별로 역할이 달라질 수 있습니다.</p></div>
    <div class="decision-card"><h3>2. 금지 관행 스크리닝</h3><p>조작, 취약성 악용, 사회적 점수화, 특정 생체·감정 인식 등 금지 또는 엄격 제한 영역을 기획 단계에서 제거합니다.</p></div>
    <div class="decision-card"><h3>3. GPAI 여부</h3><p>범용 모델을 제공하거나 fine-tuning·배포 형태로 통합하는지 확인하고, 기술문서·저작권 정책·학습 콘텐츠 요약 확보 여부를 봅니다.</p></div>
    <div class="decision-card"><h3>4. 고위험 도메인</h3><p>채용, 교육, 필수 서비스, 금융, 법집행, 공공 서비스 등은 “챗봇”이라는 UI보다 실제 의사결정 영향으로 판단합니다.</p></div>
    <div class="decision-card"><h3>5. 투명성 UX</h3><p>사용자가 AI와 상호작용 중임을 알 수 있는지, 합성 콘텐츠·자동화 의사결정·권고의 한계가 표시되는지 확인합니다.</p></div>
    <div class="decision-card"><h3>6. 증빙 운영</h3><p>평가 결과, 변경 이력, human oversight, incident log를 감사 가능한 위치에 저장합니다.</p></div>
  </section>

  <section class="architecture-map">
    <h2><span class="num">2</span>거버넌스 운영모델</h2>
    <p class="h2-sub">정책, 제품, 데이터, 모델, 보안, 법무가 같은 운영표를 봐야 합니다.</p>
    <p>아래 표는 최소 운영 체계입니다. 실제 조직에서는 각 행을 Jira epic, GRC control, 데이터 카탈로그, 모델 레지스트리, 보안 티켓으로 연결하는 것이 좋습니다. 핵심은 “문서가 있다”가 아니라 <span class="hl">출시 전후에 반복 가능한 절차와 증거가 남는다</span>는 점입니다.</p>
    <div class="tbl"><table><caption class="caption">AI 거버넌스 최소 운영 체계</caption><thead><tr><th scope="col">운영 영역</th><th scope="col">필수 산출물</th><th scope="col">소유자</th><th scope="col">감사 질문</th></tr></thead><tbody>
      <tr><td>AI 인벤토리</td><td>시스템명, 모델명, 공급자, 사용 목적, 사용자군, 배포 지역, 데이터 유형</td><td>AI PM / 데이터 거버넌스</td><td>현재 운영 중인 AI를 빠짐없이 설명할 수 있는가?</td></tr>
      <tr><td>역할·위험 분류</td><td>Provider/deployer 역할, 금지 관행, 고위험 여부, 투명성 의무, GPAI 관련성</td><td>법무 / 리스크</td><td>각 제품의 의무 근거가 문서화되어 있는가?</td></tr>
      <tr><td>GPAI 공급망</td><td>모델 카드, 기술문서, 저작권 정책, 학습 콘텐츠 요약, 안전 평가 자료 요청 기록</td><td>조달 / 법무 / 보안</td><td>외부 모델 공급자의 증빙을 계약상 요구했는가?</td></tr>
      <tr><td>데이터·저작권</td><td>학습·검색·로그 데이터 출처, 보존 기간, 삭제 절차, 저작권 리스크 검토</td><td>데이터 오너 / DPO</td><td>입력·출력·로그 데이터가 어떤 목적으로 저장되는가?</td></tr>
      <tr><td>평가·테스트</td><td>정확도, 안전성, 편향, 보안, prompt injection, hallucination, red-team 결과</td><td>ML / QA / 보안</td><td>출시 기준과 실패 기준이 수치·사례로 남아 있는가?</td></tr>
      <tr><td>Human Oversight</td><td>승인 단계, override, 이의제기, fallback, 담당자 escalation 경로</td><td>제품 / 운영</td><td>사용자가 AI 판단을 이해하고 거부할 수 있는가?</td></tr>
      <tr><td>모니터링·사고 대응</td><td>오류·피해·오남용 감지, 중단 절차, 사고 보고 템플릿, postmortem</td><td>SRE / 보안 / CS</td><td>사고 발생 시 누가 언제 무엇을 보고하는가?</td></tr>
      <tr><td>변경관리</td><td>모델 버전, 프롬프트, retrieval corpus, guardrail, 정책 변경 승인 로그</td><td>AI 플랫폼 / Change Advisory</td><td>모델·데이터 변경이 위험 재평가를 트리거하는가?</td></tr>
    </tbody></table></div>

    <h3>RACI 예시</h3>
    <div class="tbl"><table><caption class="caption">AI Act 대응 RACI 초안</caption><thead><tr><th scope="col">활동</th><th scope="col">Responsible</th><th scope="col">Accountable</th><th scope="col">Consulted</th><th scope="col">Informed</th></tr></thead><tbody>
      <tr><td>AI 인벤토리 유지</td><td>AI PM</td><td>AI Governance Lead</td><td>Data Owner, Security</td><td>Product Leadership</td></tr>
      <tr><td>위험 등급 판정</td><td>Legal/Risk</td><td>General Counsel</td><td>Product, Security, DPO</td><td>Business Owner</td></tr>
      <tr><td>모델 공급망 증빙</td><td>Procurement</td><td>Vendor Owner</td><td>Legal, Security</td><td>AI PM</td></tr>
      <tr><td>출시 전 평가</td><td>ML/QA</td><td>Product Owner</td><td>Security, Legal</td><td>Support, Sales</td></tr>
    </tbody></table></div>
  </section>

  <section class="risk-matrix">
    <h2><span class="num">3</span>리스크 매트릭스</h2>
    <p class="h2-sub">리스크는 법무 문서만이 아니라 제품 운영과 사용자 경험에서 발생합니다.</p>
    <div class="card-grid">
      <div class="mini-card risk-high"><h3>높음: 역할 오판</h3><p>제공자 의무를 deployer 수준으로만 처리하면 기술문서, 평가, 고지, 사고 대응 증빙이 누락됩니다.</p></div>
      <div class="mini-card risk-high"><h3>높음: 고위험 use case 미탐지</h3><p>채용·교육·금융·필수 서비스 의사결정에 영향을 주는데 일반 productivity tool로 분류하면 통제 공백이 생깁니다.</p></div>
      <div class="mini-card risk-mid"><h3>중간: GPAI 공급망 공백</h3><p>외부 모델 제공자의 문서·저작권 정책·안전 평가 자료를 확보하지 못하면 고객·감사 대응이 어렵습니다.</p></div>
      <div class="mini-card risk-mid"><h3>중간: 로그·보존 정책 부재</h3><p>사용자 입력과 출력이 어디에 저장되는지 불명확하면 개인정보·영업비밀·삭제 요청 대응이 취약합니다.</p></div>
      <div class="mini-card risk-mid"><h3>중간: Human oversight 형식화</h3><p>승인 버튼은 있지만 판단 근거·대안·이의제기 경로가 없으면 실질적 통제가 아닙니다.</p></div>
      <div class="mini-card risk-low"><h3>낮음: 문구 고지 누락</h3><p>챗봇/합성 콘텐츠 고지는 상대적으로 빨리 보완 가능하지만, UX·정책·로그와 함께 고쳐야 합니다.</p></div>
    </div>
  </section>

  <section class="priority-roadmap">
    <h2><span class="num">4</span>90일 실행 로드맵</h2>
    <p class="h2-sub">로드맵은 회의체 설립보다 출시 게이트에 어떤 증거를 요구할지로 설계합니다.</p>
    <div class="card-block"><div class="case-label">0–30일</div><h3>발견과 분류</h3><ul><li>운영 중·개발 중·실험 중 AI 시스템을 모두 인벤토리화합니다.</li><li>각 시스템의 모델 공급자, 데이터 유형, 사용자군, 의사결정 영향도를 기록합니다.</li><li>금지 관행과 고위험 도메인을 1차 스크리닝합니다.</li><li>외부 LLM·검색·자동화 도구의 공급망 증빙 요청 목록을 만듭니다.</li></ul></div>
    <div class="card-block"><div class="case-label">31–60일</div><h3>통제 설계</h3><ul><li>위험 등급별 출시 체크리스트를 정의합니다.</li><li>Human oversight, 사용자 고지, 이의제기, fallback UX를 제품에 반영합니다.</li><li>prompt injection, 데이터 유출, hallucination, bias 평가 케이스를 만듭니다.</li><li>모델·프롬프트·검색 corpus 변경관리 기준을 세웁니다.</li></ul></div>
    <div class="card-block"><div class="case-label">61–90일</div><h3>증빙과 훈련</h3><ul><li>평가 로그와 승인 기록을 중앙 저장소에 보관합니다.</li><li>사고 대응 playbook과 고객/감독기관 대응 템플릿을 만듭니다.</li><li>보안·법무·제품·CS가 참여하는 tabletop exercise를 실행합니다.</li><li>분기별 재분류와 공급망 문서 갱신 일정을 확정합니다.</li></ul></div>
  </section>

  <section class="validation-checklist">
    <h2><span class="num">5</span>감사 대응 검증 체크리스트</h2>
    <p class="h2-sub">감사자가 물을 질문에 제품팀이 바로 답할 수 있어야 합니다.</p>
    <div class="tbl"><table><caption class="caption">출시 전 AI Act readiness checklist</caption><thead><tr><th scope="col">질문</th><th scope="col">증거</th><th scope="col">통과 기준</th></tr></thead><tbody>
      <tr><td>이 AI 시스템의 목적과 사용자군은?</td><td>AI inventory record</td><td>제품·법무·보안이 같은 설명 사용</td></tr>
      <tr><td>우리의 법적 역할은?</td><td>role classification memo</td><td>provider/deployer 등 근거 포함</td></tr>
      <tr><td>고위험 또는 금지 영역과 연결되는가?</td><td>risk classification sheet</td><td>도메인·영향도·예외 판단 기록</td></tr>
      <tr><td>외부 모델 증빙은 확보했는가?</td><td>vendor evidence pack</td><td>기술문서·저작권·안전 자료 요청/수령 기록</td></tr>
      <tr><td>사용자가 AI 사용 사실과 한계를 아는가?</td><td>UX screenshot / copy review</td><td>고지, 불확실성, 책임 경계 표시</td></tr>
      <tr><td>모델 변경 시 재평가되는가?</td><td>change log / release gate</td><td>버전·프롬프트·corpus 변경 trigger 존재</td></tr>
      <tr><td>사고 발생 시 중단·보고할 수 있는가?</td><td>incident playbook</td><td>owner, SLA, escalation, postmortem 포함</td></tr>
    </tbody></table></div>
  </section>

  <section class="try"><div class="label">Final Recommendation</div><h2>이번 분기 안에 끝내야 할 세 가지</h2><ol><li><strong>AI 인벤토리:</strong> 모든 AI 시스템을 하나의 register로 모으고 owner를 지정합니다.</li><li><strong>출시 게이트:</strong> 위험 분류, 사용자 고지, 평가 로그, 공급망 증빙 없이는 배포하지 않는 기준을 세웁니다.</li><li><strong>증빙 저장소:</strong> 법무 문서, 평가 결과, 변경 이력, 사고 대응 기록을 감사 가능한 구조로 보관합니다.</li></ol></section>

  <aside class="source-note"><div class="label">공식 출처와 검토 기준</div><p>EU AI Act 원문, European Commission GPAI 자료, 구현 일정 자료를 기준으로 작성했습니다. 본 문서는 실무 검토용 요약이며 법률 자문이 아닙니다.</p><ul class="source-list">{source_lis}</ul></aside>
</main>
</body>
</html>
'''
page.write_text(head + body, encoding='utf-8')
print(page)
