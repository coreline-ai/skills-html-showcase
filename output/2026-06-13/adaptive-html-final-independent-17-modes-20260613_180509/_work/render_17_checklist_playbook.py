#!/usr/bin/env python3
"""Mode 17 / 17 — checklist_playbook (sequential). Topic: 프로덕션 DB 스키마 마이그레이션 플레이북.
Layout: checklist-playbook.html (.layout-checklist) · auto · vt: checklist-flow(cf-item) · wg: wg-11.
"""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _finalize import build_page, write_sources, h2, SKILL, ASSETS  # noqa: E402,F401

for _p in [SKILL/"SKILL.md", SKILL/"references/layout-system.md", ASSETS/"layouts/checklist-playbook.html",
           ASSETS/"visual-html-templates/05-checklist-flow.html", ASSETS/"widget-templates/11-weekly-status.html"]:
    _p.read_text(encoding="utf-8")

TITLE = "프로덕션 DB 스키마 마이그레이션 플레이북"
DESC = "무중단으로 프로덕션 데이터베이스 스키마를 바꾸는 플레이북. 사전 점검·단계별 절차(expand-contract)·실패 모드·롤백·완료 기준을 체크리스트로 정리한 checklist_playbook."

header = '''
<header class="header checklist-header">
  <div class="kicker"><span class="kicker-text">PLAYBOOK · MODE 17 / 17 · 독립 빌드</span></div>
  <h1>프로덕션 DB 스키마 마이그레이션 플레이북</h1>
  <p class="sub">살아 있는 서비스의 데이터베이스 스키마를, 멈추지 않고 안전하게 바꾸는 절차. "한 번에 ALTER" 대신 단계로 나눠 언제든 되돌릴 수 있게 만든다.</p>
  <div class="meta"><span>profile auto</span><span>layout checklist-playbook</span><span>대상 백엔드·DBA</span><span>무중단 전제</span></div>
  <div class="generated-row"><p class="generated-date">Generated · 2026-06-13 KST</p>
  <div class="lens-strip" aria-label="적용 렌즈"><span class="lens-strip-label">LENS</span><span class="lens-chip">사전 점검</span><span class="lens-chip">단계 절차</span><span class="lens-chip">실패 모드</span><span class="lens-chip">롤백</span><span class="lens-chip">완료 기준</span></div></div>
</header>'''

toc = '''
<nav class="toc-map checklist-toc" aria-label="플레이북 목차"><div class="toc-pills">
  <a class="toc-pill" href="#s1"><b>01</b> 언제 쓰나</a><a class="toc-pill" href="#s2"><b>02</b> 사전 점검 게이트</a>
  <a class="toc-pill" href="#s3"><b>03</b> 단계별 절차</a><a class="toc-pill" href="#s4"><b>04</b> 무중단 전략</a>
  <a class="toc-pill" href="#s5"><b>05</b> 실패 모드</a><a class="toc-pill" href="#s6"><b>06</b> 롤백 계획</a>
  <a class="toc-pill" href="#s7"><b>07</b> 진행 상태판</a><a class="toc-pill" href="#s8"><b>08</b> 검증</a>
  <a class="toc-pill" href="#s9"><b>09</b> 완료 기준</a><a class="toc-pill" href="#snext"><b>→</b> 실행 시작</a>
</div></nav>'''

s1 = f'''
<section id="s1" class="summary-card">
  {h2("01","언제 쓰나","audit")}
  <p class="h2-sub">이 플레이북은 "다운타임 없이, 트래픽이 흐르는 중에" 스키마를 바꿔야 할 때를 위한 것이다. 점검 창을 잡을 수 있다면 더 단순한 방법도 있다.</p>
  <div class="grid-3">
    <article class="score-card"><h3>적용 상황</h3><p>컬럼 추가·삭제·타입 변경·NOT NULL 추가·인덱스 생성처럼, 큰 테이블에 적용하면 잠금·지연을 유발할 수 있는 변경.</p></article>
    <article class="score-card"><h3>전제</h3><p>무중단이 요구되고, 애플리케이션과 DB를 따로 배포할 수 있으며, 롤백 경로를 항상 확보해야 하는 환경.</p></article>
    <article class="score-card"><h3>핵심 원칙</h3><p>"한 번의 큰 변경" 대신 "되돌릴 수 있는 작은 단계들". 각 단계는 이전·다음 버전 코드와 모두 호환되어야 한다.</p></article>
  </div>
  <p>가장 중요한 전제는 <strong>"앱과 스키마가 항상 한 버전씩 어긋날 수 있다"</strong>는 것이다. 배포는 순간이 아니라 롤링으로 일어나므로, 마이그레이션 도중에는 구 버전 코드와 신 버전 코드가 동시에 같은 DB를 본다. 이 동시성을 견디는 설계가 무중단의 핵심이다.</p>
</section>'''

s2 = f'''
<section id="s2" class="summary-card">
  {h2("02","사전 점검 게이트","check")}
  <p class="h2-sub">실행 전 통과해야 할 점검. 하나라도 PASS가 아니면 시작하지 않는다.</p>
  <section class="vt-shell" aria-label="마이그레이션 사전 점검">
    <div class="vt-frame"><div class="cf">
      <div class="cf-item"><span class="cf-check">✓</span><div><b>백업·복구 검증</b><p class="vt-text">최신 백업 존재 + 복원 리허설이 최근에 성공했는가</p></div><span class="cf-state">PASS</span></div>
      <div class="cf-item"><span class="cf-check">✓</span><div><b>변경 크기 측정</b><p class="vt-text">대상 테이블 행 수·잠금 영향을 스테이징에서 측정했는가</p></div><span class="cf-state">PASS</span></div>
      <div class="cf-item"><span class="cf-check">✓</span><div><b>롤백 경로</b><p class="vt-text">각 단계의 되돌리기 방법이 문서화되어 있는가</p></div><span class="cf-state">PASS</span></div>
      <div class="cf-item"><span class="cf-check">✓</span><div><b>관측·알림</b><p class="vt-text">쿼리 지연·잠금·복제 지연 대시보드와 경보가 준비됐는가</p></div><span class="cf-state">PASS</span></div>
    </div></div>
  </section>
  <p>네 게이트 중 가장 자주 건너뛰는 것은 "복원 리허설"이다. 백업이 있다는 것과 복원이 된다는 것은 다르다. 마이그레이션 전에 실제로 복원해 본 적이 없다면, 그 백업은 "있다고 믿는 백업"일 뿐이다. 시작 전 반드시 한 번 복원을 돌려 본다.</p>
</section>'''

s3 = f'''
<section id="s3" class="check-grid summary-card">
  {h2("03","단계별 절차","flow")}
  <p class="h2-sub">expand-contract(확장-수축) 패턴을 따른다. 추가는 먼저, 제거는 가장 마지막에.</p>
  <div class="card-grid">
    <article class="card-block"><h3>1. Expand</h3><p>새 컬럼/테이블을 <strong>nullable·기본값 있게</strong> 추가한다. 기존 코드는 모르고도 동작한다. 잠금이 짧은 연산만 사용.</p></article>
    <article class="card-block"><h3>2. Dual-write</h3><p>앱을 배포해 구·신 컬럼에 동시에 쓴다(읽기는 아직 구 컬럼). 신 컬럼이 채워지기 시작한다.</p></article>
    <article class="card-block"><h3>3. Backfill</h3><p>과거 행을 배치로 신 컬럼에 채운다. 작은 배치로 나눠 잠금·복제 지연을 피한다.</p></article>
    <article class="card-block"><h3>4. Switch read</h3><p>앱을 배포해 읽기를 신 컬럼으로 전환한다. 이 시점에 신 컬럼이 진실의 원천이 된다.</p></article>
    <article class="card-block"><h3>5. Contract</h3><p>안정화 기간을 둔 뒤, dual-write를 끄고 마지막에 구 컬럼을 제거한다. 되돌릴 수 없는 단계이므로 가장 늦게.</p></article>
  </div>
  <p>이 다섯 단계의 핵심은 "추가(expand)와 제거(contract) 사이에 충분한 시간"을 두는 것이다. 각 단계 사이에서 언제든 멈추고 이전으로 돌아갈 수 있으며, 비가역 연산(컬럼 제거)은 모든 게 안정된 마지막에만 한다. 절대 한 배포에서 추가와 제거를 함께 하지 않는다.</p>
</section>'''

s4 = f'''
<section id="s4" class="summary-card">
  {h2("04","무중단 전략의 핵심","idea")}
  <p class="h2-sub">왜 이렇게 번거롭게 나누는가? "롤링 배포 중 두 버전 공존"을 견디기 위해서다.</p>
  <div class="good"><span class="label">호환 규칙</span><p>모든 중간 단계의 스키마는 <strong>이전 버전 코드와 다음 버전 코드 둘 다</strong>와 호환되어야 한다. 그래서 컬럼 추가는 nullable로, 이름 변경은 "추가 후 이전" 두 단계로 나눈다.</p></div>
  <div class="danger"><span class="label">금지 패턴</span><p>한 배포에서 컬럼을 즉시 <code>NOT NULL</code>로 추가하거나, 이름을 바로 바꾸거나, 큰 테이블에 잠금이 긴 <code>ALTER</code>를 거는 것. 구 버전 코드가 깨지거나 잠금으로 서비스가 멈춘다.</p></div>
  <p>요약하면 무중단 마이그레이션은 "DB 변경"이 아니라 "앱 배포와 DB 변경의 안무(choreography)"다. 순서가 곧 안전이다. 추가→이중쓰기→백필→읽기전환→제거 순서를 지키면, 어느 시점에 배포가 절반만 진행돼 있어도 서비스가 깨지지 않는다.</p>
</section>'''

s5 = f'''
<section id="s5" class="failure-modes summary-card">
  {h2("05","실패 모드","warning")}
  <p class="h2-sub">마이그레이션이 사고로 번지는 전형적 경로. 미리 알면 대부분 피할 수 있다.</p>
  <div class="card-grid">
    <article class="mini-card"><span class="case-label">치명</span><h3>긴 잠금</h3><p>큰 테이블에 잠금이 긴 ALTER를 걸면 그 시간 동안 쓰기가 막혀 서비스가 멈춘다. online DDL·작은 배치로 회피.</p></article>
    <article class="mini-card"><span class="case-label">치명</span><h3>복제 지연 폭증</h3><p>대량 백필이 복제를 밀어내 읽기 복제본이 뒤처진다. 배치 크기·간격을 조절하고 지연을 모니터링.</p></article>
    <article class="mini-card"><span class="case-label">경고</span><h3>버전 불일치</h3><p>추가와 제거를 한 배포에 합치면 롤링 중 구 버전 코드가 깨진다. 단계를 절대 합치지 않는다.</p></article>
    <article class="mini-card"><span class="case-label">경고</span><h3>백필 중 불일치</h3><p>dual-write 없이 backfill만 하면, 백필 중 들어온 신규 쓰기가 누락된다. dual-write를 먼저 켠다.</p></article>
  </div>
  <p>네 실패 모드의 공통 뿌리는 "한꺼번에 하려는 조급함"이다. 잠금·복제 지연·버전 불일치 모두 "단계를 합치거나 배치를 키울 때" 터진다. 플레이북이 느려 보여도, 그 느림이 곧 안전이다.</p>
</section>'''

s6 = f'''
<section id="s6" class="summary-card">
  {h2("06","롤백 계획","security")}
  <p class="h2-sub">각 단계마다 "어떻게 되돌리나"를 미리 정한다. 롤백이 불가능한 지점을 명확히 안다.</p>
  <div class="table-scroll"><table>
    <caption>단계별 롤백 가능성</caption>
    <thead><tr><th>단계</th><th>롤백 방법</th><th>되돌리기</th></tr></thead>
    <tbody>
      <tr><th>Expand</th><td>추가한 컬럼 제거(아직 안 쓰임)</td><td>쉬움</td></tr>
      <tr><th>Dual-write</th><td>앱 이전 버전으로 롤백</td><td>쉬움</td></tr>
      <tr><th>Backfill</th><td>중단해도 안전(신 컬럼만 영향)</td><td>쉬움</td></tr>
      <tr><th>Switch read</th><td>읽기를 구 컬럼으로 되돌리는 배포</td><td>중간</td></tr>
      <tr><th>Contract</th><td>구 컬럼 이미 제거 — 백업 복원 필요</td><td>어려움(비가역)</td></tr>
    </tbody>
  </table></div>
  <p>표가 말하는 핵심은 "Contract 전까지는 모두 쉽게 되돌릴 수 있다"는 것이다. 그래서 읽기 전환(Switch read) 후 충분한 안정화 기간(며칠~주)을 두고, Contract는 "더 이상 구 컬럼을 아무도 안 본다"는 확신이 선 뒤에만 한다. 의심되면 Contract를 미룬다 — 미루는 비용은 작고, 잘못 제거한 비용은 백업 복원이다.</p>
</section>'''

s7 = f'''
<section id="s7" class="summary-card">
  {h2("07","진행 상태판","metric")}
  <p class="h2-sub">마이그레이션이 며칠~주에 걸치므로, 지금 어느 단계인지 한눈에 보이게 한다.</p>
  <section class="wg-11" aria-labelledby="m17-ws-title">
    <header class="wg-11-head"><p class="wg-11-kicker">마이그레이션 상태 · MIG-17</p><h2 id="m17-ws-title" class="wg-11-h">user 테이블 스키마 전환</h2><p class="wg-11-lead">읽기 전환까지 완료 · 안정화 관찰 중 · Contract 대기</p></header>
    <div class="wg-11-kpis">
      <div class="wg-11-kpi wg-11-kpi-good"><span class="wg-11-kpi-v">4/5</span><span class="wg-11-kpi-l">단계 완료</span></div>
      <div class="wg-11-kpi wg-11-kpi-prog"><span class="wg-11-kpi-v">관찰</span><span class="wg-11-kpi-l">안정화</span></div>
      <div class="wg-11-kpi wg-11-kpi-risk"><span class="wg-11-kpi-v wg-11-warn">대기</span><span class="wg-11-kpi-l">Contract</span></div>
      <div class="wg-11-kpi"><span class="wg-11-kpi-v">0</span><span class="wg-11-kpi-l">불일치</span></div>
    </div>
    <h3 class="wg-11-h3">단계 진척</h3>
    <div class="wg-11-bars">
      <div class="wg-11-bar-row"><span class="wg-11-bar-label">Expand·Dual-write</span><div class="wg-11-track" role="img" aria-label="확장 이중쓰기 100퍼센트"><div class="wg-11-fill wg-11-fill-good" style="width:100%"></div></div><span class="wg-11-bar-pct">완료</span></div>
      <div class="wg-11-bar-row"><span class="wg-11-bar-label">Backfill</span><div class="wg-11-track" role="img" aria-label="백필 100퍼센트"><div class="wg-11-fill wg-11-fill-good" style="width:100%"></div></div><span class="wg-11-bar-pct">완료</span></div>
      <div class="wg-11-bar-row"><span class="wg-11-bar-label">Switch read·안정화</span><div class="wg-11-track" role="img" aria-label="읽기 전환 안정화 60퍼센트"><div class="wg-11-fill wg-11-fill-prog" style="width:60%"></div></div><span class="wg-11-bar-pct">관찰</span></div>
    </div>
    <div class="wg-11-cols">
      <div class="wg-11-col wg-11-col-good"><h4 class="wg-11-col-h"><span class="wg-11-dot"></span>완료</h4><ul class="wg-11-col-list"><li>신 컬럼 추가·이중쓰기 <span class="wg-11-tk">MIG-1</span></li><li>전체 행 백필 <span class="wg-11-tk">MIG-2</span></li></ul></div>
      <div class="wg-11-col wg-11-col-prog"><h4 class="wg-11-col-h"><span class="wg-11-dot"></span>진행 중</h4><ul class="wg-11-col-list"><li>읽기 신 컬럼 전환 후 안정화 관찰 <span class="wg-11-tk">MIG-3</span></li></ul></div>
      <div class="wg-11-col wg-11-col-risk"><h4 class="wg-11-col-h"><span class="wg-11-dot"></span>대기</h4><ul class="wg-11-col-list"><li><strong>구 컬럼 제거</strong> — 안정화 확인 전 보류 <span class="wg-11-flag">비가역</span></li></ul></div>
    </div>
  </section>
</section>'''

s8 = f'''
<section id="s8" class="summary-card">
  {h2("08","검증","success")}
  <p class="h2-sub">각 단계 후 "정말 안전한가"를 확인하는 검증 항목. 통과해야 다음 단계로 간다.</p>
  <ul class="check-list">
    <li><strong>Expand 후</strong> — 기존 기능 회귀 없음(신 컬럼은 무시되므로 영향 0이어야 정상). 잠금 시간이 임계 이하였는지 확인.</li>
    <li><strong>Backfill 중</strong> — 복제 지연이 임계 이하 유지. 신규 쓰기가 dual-write로 누락 없이 반영되는지 표본 비교.</li>
    <li><strong>Switch read 후</strong> — 구·신 컬럼 값 일치율 100% 확인(불일치 0). 읽기 경로 오류율 정상.</li>
    <li><strong>Contract 전</strong> — 구 컬럼 참조가 코드·쿼리·리포트 어디에도 없는지 정적 검색 + 모니터링으로 확인.</li>
  </ul>
  <p>가장 중요한 검증은 "Switch read 후 값 일치율"이다. 구·신 컬럼이 100% 일치하지 않으면 backfill이나 dual-write에 구멍이 있다는 뜻이고, 그 상태로 Contract하면 데이터를 잃는다. 일치율이 1건이라도 어긋나면 Contract를 멈추고 원인을 찾는다.</p>
</section>'''

s9 = f'''
<section id="s9" class="summary-card">
  {h2("09","완료 기준","reference")}
  <p class="h2-sub">"끝났다"를 선언하는 조건. 아래가 모두 충족돼야 마이그레이션을 닫는다.</p>
  <div class="table-scroll"><table>
    <caption>마이그레이션 완료 기준</caption>
    <thead><tr><th>기준</th><th>조건</th><th>증빙</th></tr></thead>
    <tbody>
      <tr><th>데이터</th><td>구·신 컬럼 값 일치율 100%</td><td>일치 검증 리포트</td></tr>
      <tr><th>코드</th><td>구 컬럼 참조 0</td><td>정적 검색 + 쿼리 로그</td></tr>
      <tr><th>안정화</th><td>읽기 전환 후 무사고 기간 경과</td><td>대시보드 N일 추이</td></tr>
      <tr><th>정리</th><td>구 컬럼 제거 + 문서 갱신</td><td>마이그레이션 PR·런북 업데이트</td></tr>
    </tbody>
  </table></div>
  <p>완료의 마지막 항목은 "문서 갱신"이다. 스키마는 바뀌었는데 ERD·런북·온보딩 문서가 구 컬럼을 가리키면, 다음 사람이 혼란에 빠진다. 마이그레이션은 구 컬럼을 지운 순간이 아니라, 그 변경이 문서에 반영된 순간 진짜로 끝난다.</p>
</section>'''

snext = f'''
<section id="snext" class="try">
  {h2(None,"실행 시작","landing")}
  <p>플레이북은 읽는 게 아니라 따라 하는 것이다. 다음 순서로 실제 마이그레이션을 시작한다.</p>
  <div class="cta-box">
    <p><strong>시작 체크</strong></p>
    <ol><li>사전 점검 게이트 4종 PASS 확인(특히 복원 리허설).</li><li>expand-contract 5단계를 별도 배포로 계획 — 추가와 제거를 절대 합치지 않는다.</li><li>각 단계 검증 항목을 통과해야 다음으로, Contract는 안정화 확인 후에만.</li><li>진행 상태판으로 "지금 어느 단계인지"를 팀이 공유.</li></ol>
    <div class="tag-list"><span class="tag">checklist_playbook</span><span class="tag">db-migration</span><span class="tag">expand-contract</span><span class="tag">무중단</span></div>
  </div>
</section>'''

source_note = '<aside class="source-note"><p><strong>범위.</strong> 본 플레이북은 관계형 DB의 무중단 스키마 마이그레이션 일반 원칙(expand-contract, dual-write, backfill)을 정리한 것이다. 구체적 DDL 동작·온라인 DDL 지원 여부는 DB 엔진·버전마다 다르므로, 실제 적용 전 사용하는 엔진의 문서와 스테이징 측정으로 확인한다.</p></aside>'

body = ('<main id="main" class="page-wide layout-checklist">' + header + toc + s1+s2+s3+s4+s5+s6+s7+s8+s9+snext + source_note + '</main>')
out = build_page("pages/17_checklist_playbook_db_schema_migration.html", title=TITLE, description=DESC, body=body)
write_sources()
print("WROTE", out)
