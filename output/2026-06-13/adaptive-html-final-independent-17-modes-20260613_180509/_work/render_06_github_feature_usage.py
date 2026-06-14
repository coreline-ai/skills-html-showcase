#!/usr/bin/env python3
"""Mode 06 / 17 — github_feature_usage (sequential). Topic: 셀프호스트 업타임 모니터(가칭 upkeep).
Layout: github-feature-usage.html (.layout-github-feature) · auto · vt: hero-map(hm-grid) · wg: wg-14.
실제 캡처가 없어 '실제 화면'은 HTML/CSS 구조 패널로 표현하고 출처 한계에 명시한다.
"""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _finalize import build_page, write_sources, h2, SKILL, ASSETS  # noqa: E402,F401

for _p in [SKILL/"SKILL.md", SKILL/"references/github-feature-usage-system.md", ASSETS/"layouts/github-feature-usage.html",
           ASSETS/"visual-html-templates/01-hero-map.html", ASSETS/"widget-templates/14-feature-explainer.html"]:
    _p.read_text(encoding="utf-8")

TITLE = "셀프호스트 업타임 모니터 도입 가이드 — upkeep"
DESC = "셀프호스트 업타임·상태페이지 모니터링 도구(upkeep)가 무엇을 해주고 어떻게 쓰며 어디에 맞는지 기능 지도·화면 구조·사용자/관리자 기능·시작 방법으로 안내하는 github_feature_usage 가이드."

header = '''
<header class="header github-feature-header">
  <div class="kicker"><span class="kicker-text">FEATURE & USAGE · MODE 06 / 17 · 독립 빌드</span></div>
  <h1>셀프호스트 업타임 모니터 도입 가이드</h1>
  <p class="sub">오픈소스 업타임·상태페이지 모니터(가칭 <code>upkeep/upkeep</code>)가 "무엇을 해주고, 어떻게 쓰며, 어디에 맞는가"를 기능 지도와 화면 구조 중심으로 안내한다. 실사 경고체가 아니라 평가·온보딩 독자를 위한 안내체다.</p>
  <div class="meta"><span>profile auto</span><span>layout github-feature-usage</span><span>대상 운영·SRE 도입 검토자</span><span>화면은 구조 설명</span></div>
  <div class="generated-row"><p class="generated-date">Generated · 2026-06-13 KST</p>
  <div class="lens-strip" aria-label="적용 렌즈"><span class="lens-strip-label">LENS</span><span class="lens-chip">무엇을</span><span class="lens-chip">어떻게</span><span class="lens-chip">어디에 맞나</span><span class="lens-chip">화면</span><span class="lens-chip">시작 방법</span></div></div>
</header>'''

toc = '''
<nav class="toc-map feature-toc" aria-label="기능·도입 가이드 목차"><div class="toc-pills">
  <a class="toc-pill" href="#s1"><b>01</b> 한 줄 정체성</a><a class="toc-pill" href="#s2"><b>02</b> 개요 신호</a>
  <a class="toc-pill" href="#s3"><b>03</b> 기능 지도</a><a class="toc-pill" href="#s4"><b>04</b> 핵심 기능</a>
  <a class="toc-pill" href="#s5"><b>05</b> 기술 스택</a><a class="toc-pill" href="#s6"><b>06</b> 아키텍처</a>
  <a class="toc-pill" href="#s7"><b>07</b> 디렉터리 구조</a><a class="toc-pill" href="#s8"><b>08</b> 실제 화면</a>
  <a class="toc-pill" href="#s9"><b>09</b> 사용자·관리자 기능</a><a class="toc-pill" href="#s10"><b>10</b> 시작 방법·적합성</a>
  <a class="toc-pill" href="#snext"><b>→</b> 최종 정리·다음 행동</a>
</div></nav>'''

s1 = f'''
<section id="s1" class="feature-verdict summary-card">
  {h2("01","한 줄 정체성","landing")}
  <p class="h2-sub">한 문장으로: "엔드포인트를 주기적으로 찔러보고, 죽으면 알리고, 공개 상태페이지로 보여주는" 셀프호스트 모니터다.</p>
  <div class="grid-3">
    <article class="score-card"><h3>무엇을</h3><p>HTTP·TCP·핑 체크로 서비스 가용성을 감시하고, 장애 시 슬랙·이메일·웹훅으로 알린다. 공개 상태페이지를 자동 생성한다.</p></article>
    <article class="score-card"><h3>누구에게</h3><p>SaaS·내부망을 직접 운영하며, 외부 모니터링 SaaS 대신 데이터를 자기 인프라에 두고 싶은 소규모 팀.</p></article>
    <article class="score-card"><h3>대안 대비</h3><p>상용 모니터링보다 기능은 적지만, 셀프호스트·단순 설치·낮은 비용이 강점이다. 대규모 APM 대체가 목적은 아니다.</p></article>
  </div>
  <p>즉 "가볍게 띄워서 우리 서비스가 살아있는지 확인하고, 고객에게 상태를 투명하게 보여주는" 도구다. 깊은 분산 추적이나 메트릭 상관 분석이 필요하면 이 도구가 아니라 다른 범주(APM·관측 가능성 플랫폼)를 봐야 한다.</p>
</section>'''

s2 = f'''
<section id="s2" class="feature-overview summary-card">
  {h2("02","개요 신호 — 한눈 요약","map")}
  <p class="h2-sub">도입 검토자가 가장 먼저 보는 세 가지를 지도로 묶었다.</p>
  <section class="vt-shell" aria-label="제품 개요 지도">
    <div class="vt-frame"><div class="vt-demo"><div class="hm-grid">
      <article class="hm-card"><div class="vt-kicker">Monitor</div><h3>가용성 체크</h3><p class="vt-text">HTTP/TCP/핑을 주기적으로 검사하고 응답시간을 기록.</p></article>
      <article class="hm-card" style="--c:var(--vt-blue)"><div class="vt-kicker">Alert</div><h3>장애 알림</h3><p class="vt-text">연속 실패 임계 초과 시 다채널 통지, 복구 시 해제 알림.</p></article>
      <article class="hm-card" style="--c:var(--vt-green)"><div class="vt-kicker">Publish</div><h3>상태페이지</h3><p class="vt-text">가동률·사건 이력을 공개 페이지로 자동 게시.</p></article>
    </div><div class="hm-result"><b>요약: 감시 → 알림 → 공개의 3단 루프</b><span>설치 한 번으로 모니터링과 대외 커뮤니케이션을 동시에 해결.</span></div></div></div>
  </section>
  <p>세 기능은 하나의 루프다. 감시가 신호를 만들고, 알림이 사람을 움직이고, 상태페이지가 고객 신뢰를 유지한다. 어느 하나만 쓰기보다 셋을 묶어 쓸 때 가치가 크다. 예를 들어 감시만 켜고 알림 라우팅을 비워 두면, 장애를 기록은 하되 아무도 모르는 상태가 된다. 반대로 상태페이지 없이 내부 감시만 하면 고객은 "지금 우리만 안 되는 건가"를 계속 문의하게 된다. 도입 시 세 기능을 같은 날 함께 설정하는 것을 권하는 이유다.</p>
</section>'''

s3 = f'''
<section id="s3" class="feature-map summary-card">
  {h2("03","기능 지도","compare")}
  <p class="h2-sub">제공 기능을 4개 묶음으로 나누고 각 기능의 한 줄 효용을 적었다.</p>
  <div class="card-grid">
    <article class="mini-card"><h3>모니터 종류</h3><p>HTTP(상태코드·키워드), TCP 포트, 핑, 인증서 만료 체크. 엔드포인트별 주기·타임아웃 설정.</p></article>
    <article class="mini-card"><h3>알림 채널</h3><p>슬랙·이메일·웹훅·텔레그램. 채널별로 어떤 모니터의 어떤 상태를 받을지 라우팅.</p></article>
    <article class="mini-card"><h3>상태페이지</h3><p>서비스 그룹별 가동률, 사건 타임라인, 예정 점검 공지. 도메인 연결과 테마 지정.</p></article>
    <article class="mini-card"><h3>운영</h3><p>유지보수 창(점검 중 알림 억제), 권한 분리, 데이터 보존 기간, 백업/복원.</p></article>
  </div>
  <p>핵심은 "모니터를 정의하고 → 알림을 라우팅하고 → 상태페이지에 노출"하는 한 줄기 흐름이다. 기능이 많아 보여도 이 줄기를 따라가면 설정 순서가 자연스럽게 잡힌다.</p>
</section>'''

s4 = f'''
<section id="s4" class="core-capability summary-card">
  {h2("04","핵심 기능 — 모니터 정의","idea")}
  <p class="h2-sub">가장 자주 쓰는 기능을 펼쳐 본다. 설정 한 화면에서 끝나는 단순함이 이 도구의 강점이다.</p>
  <section class="wg-14" aria-labelledby="m06-wg14-title">
    <p class="wg-14-kicker">기능 안내 · 모니터</p>
    <h2 id="m06-wg14-title" class="wg-14-h">HTTP 모니터 정의</h2>
    <p class="wg-14-lead">URL·주기·성공 조건만 정하면 즉시 감시가 시작되고, 응답시간 그래프가 쌓입니다.</p>
    <div class="wg-14-tldr" role="note" aria-label="핵심 요약"><span class="wg-14-tldr-tag">TL;DR</span><p class="wg-14-tldr-body"><strong>URL + 주기 + 기대 상태코드</strong>만 입력하면 끝. 연속 실패 N회 시 알림이 발화하고 상태페이지에 반영됩니다.</p></div>
    <div class="wg-14-acc">
      <details class="wg-14-sec" open><summary class="wg-14-sum"><span class="wg-14-sum-no">01</span> 성공 조건 정의 <span class="wg-14-chev" aria-hidden="true"></span></summary><div class="wg-14-sec-body"><p>상태코드 범위(예: 200~299)와 응답 본문 키워드("ok")를 함께 검사할 수 있습니다. 둘 다 만족해야 정상으로 판정합니다.</p><ul class="wg-14-list"><li>상태코드·키워드·응답시간 임계 조합</li><li>리다이렉트 추적 on/off</li><li>인증 헤더·기본 인증 지원</li></ul></div></details>
      <details class="wg-14-sec"><summary class="wg-14-sum"><span class="wg-14-sum-no">02</span> 실패 판정과 알림 <span class="wg-14-chev" aria-hidden="true"></span></summary><div class="wg-14-sec-body"><ol class="wg-14-flow"><li><span class="wg-14-flow-n">1</span> 연속 실패 횟수가 임계(기본 3회)를 넘으면 DOWN으로 전환</li><li><span class="wg-14-flow-n">2</span> 라우팅 규칙에 맞는 채널로 알림 발화</li><li><span class="wg-14-flow-n">3</span> 정상 복구 시 UP 알림 + 사건 종료 기록</li></ol></div></details>
    </div>
  </section>
</section>'''

s5 = f'''
<section id="s5" class="tech-stack summary-card">
  {h2("05","기술 스택","code")}
  <p class="h2-sub">셀프호스트 운영 부담을 좌우하는 부분이다. 의존성이 적을수록 띄우기 쉽다.</p>
  <div class="table-scroll"><table>
    <caption>기술 스택 구성(일반적 셀프호스트 모니터 기준 추정)</caption>
    <thead><tr><th>레이어</th><th>구성</th><th>도입 시 함의</th></tr></thead>
    <tbody>
      <tr><th>런타임</th><td>단일 바이너리 또는 컨테이너</td><td>도커 한 줄로 기동 가능, 별도 런타임 설치 최소</td></tr>
      <tr><th>저장소</th><td>내장 경량 DB(SQLite 등) 또는 외부 DB</td><td>소규모는 내장으로 충분, 규모 커지면 외부 DB 권장</td></tr>
      <tr><th>UI</th><td>관리 대시보드 + 공개 상태페이지</td><td>관리자/공개 두 표면을 분리 운영</td></tr>
      <tr><th>통합</th><td>웹훅·슬랙·SMTP</td><td>기존 알림 채널에 쉽게 연결</td></tr>
    </tbody>
  </table></div>
  <p>핵심 매력은 "단일 바이너리/컨테이너 + 내장 DB"로 추정되는 낮은 운영 표면이다. 처음에는 내장 저장소로 시작하고, 모니터 수와 보존 기간이 늘면 외부 DB로 옮기는 경로가 자연스럽다. 정확한 스택은 저장소 문서로 확인한다.</p>
</section>'''

s6 = f'''
<section id="s6" class="architecture summary-card">
  {h2("06","아키텍처","flow")}
  <p class="h2-sub">데이터가 어디서 생겨 어디로 흐르는지 알면 장애 지점과 확장 지점이 보인다.</p>
  <section class="vt-shell" aria-label="아키텍처 흐름">
    <div class="vt-frame"><ol class="tl">
      <li class="tl-item"><b>스케줄러</b><p class="vt-text">등록된 모니터를 주기마다 큐에 넣는다.</p></li>
      <li class="tl-item"><b>체커 워커</b><p class="vt-text">엔드포인트를 실제로 호출하고 결과·응답시간을 기록.</p></li>
      <li class="tl-item"><b>판정·알림</b><p class="vt-text">연속 실패를 집계해 상태 전환·알림 발화.</p></li>
      <li class="tl-item"><b>표면</b><p class="vt-text">관리 대시보드와 공개 상태페이지가 같은 데이터를 읽어 표시.</p></li>
    </ol></div>
  </section>
  <p>병목과 단일 실패 지점은 대개 "체커 워커"와 "저장소"다. 모니터가 수백 개로 늘면 체크 주기가 밀리지 않는지, 저장소 쓰기가 버티는지를 본다. 셀프호스트인 만큼 이 도구의 가용성은 곧 우리가 띄운 호스트의 가용성이라는 점도 잊지 않는다.</p>
</section>'''

s7 = f'''
<section id="s7" class="directory summary-card">
  {h2("07","디렉터리 구조","file")}
  <p class="h2-sub">설정·데이터·백업이 어디에 사는지 알면 운영과 이전이 쉽다.</p>
  <section class="vt-shell" aria-label="디렉터리 투어">
    <div class="vt-frame"><div class="ft">
      <article class="ft-card"><div class="ft-head"><span>/data</span><span>state</span></div><div class="ft-body"><p class="vt-text">모니터·사건·DB 파일이 사는 영속 볼륨.</p><div class="ft-note"><b>운영 노트</b><br>컨테이너 재생성 시 반드시 볼륨 마운트로 보존.</div></div></article>
      <article class="ft-card"><div class="ft-head"><span>/config</span><span>setup</span></div><div class="ft-body"><p class="vt-text">알림 채널·SMTP·도메인 설정.</p><div class="ft-note"><b>운영 노트</b><br>비밀값은 환경변수/시크릿으로 주입, 평문 커밋 금지.</div></div></article>
      <article class="ft-card"><div class="ft-head"><span>/backups</span><span>safety</span></div><div class="ft-body"><p class="vt-text">정기 백업 산출물.</p><div class="ft-note"><b>운영 노트</b><br>복원 절차를 분기마다 실제로 리허설.</div></div></article>
    </div></div>
  </section>
  <p>가장 중요한 디렉터리는 <code>/data</code>다. 이 볼륨만 안전하게 보존·백업하면 컨테이너는 언제든 재생성할 수 있다. 도입 첫날 백업 경로와 복원 절차부터 정해 두는 것을 권한다.</p>
</section>'''

s8 = f'''
<section id="s8" class="feature-screens summary-card">
  {h2("08","실제 화면 (구조 설명)","experiment")}
  <p class="h2-sub">아래는 라이브 캡처가 아니라 주요 화면의 <strong>구조를 설명하는 패널</strong>이다. 각 화면이 무엇을 보여주는지 레이아웃 단위로 안내한다.</p>
  <div class="figure-screens-grid">
    <figure class="box"><div class="screen-frame"><div class="screen-bar"><span></span><span></span><span></span></div><div class="screen-body"><strong>모니터 목록</strong><p>각 행: 이름 · 상태(UP/DOWN) · 가동률 · 최근 응답시간 스파크라인. 상단에 전체 가동률 요약.</p></div></div><figcaption>대시보드 — 모니터 목록 화면의 정보 구조</figcaption></figure>
    <figure class="box"><div class="screen-frame"><div class="screen-bar"><span></span><span></span><span></span></div><div class="screen-body"><strong>모니터 상세</strong><p>응답시간 시계열 그래프, 사건 타임라인, 알림 발화 이력, 설정 편집 패널.</p></div></div><figcaption>대시보드 — 단일 모니터 상세의 정보 구조</figcaption></figure>
    <figure class="box"><div class="screen-frame"><div class="screen-bar"><span></span><span></span><span></span></div><div class="screen-body"><strong>공개 상태페이지</strong><p>서비스 그룹별 현재 상태, 90일 가동률 막대, 진행/과거 사건 목록.</p></div></div><figcaption>공개 — 고객이 보는 상태페이지의 정보 구조</figcaption></figure>
  </div>
  <p>세 화면은 같은 데이터의 다른 청중용 표현이다. 운영자는 목록·상세에서 깊이 보고, 고객은 상태페이지에서 "지금 괜찮은가"만 빠르게 확인한다. 실제 스크린샷은 저장소의 데모/문서에서 확인할 수 있다.</p>
</section>'''

s9 = f'''
<section id="s9" class="user-features summary-card">
  {h2("09","사용자·관리자 기능 흐름","user")}
  <p class="h2-sub">두 역할의 전형적 흐름을 분리해 본다. 권한 경계가 곧 운영 안전선이다.</p>
  <div class="grid-2">
    <article class="card-block"><h3>관리자 흐름</h3><ol><li>설치·도메인 연결·SMTP 설정</li><li>모니터 등록 및 성공 조건 정의</li><li>알림 채널·라우팅 규칙 구성</li><li>상태페이지 그룹·테마 설정</li><li>점검 창·백업 정책 운영</li></ol></article>
    <article class="card-block"><h3>열람자(고객) 흐름</h3><ol><li>공개 상태페이지 방문</li><li>현재 서비스 상태 확인</li><li>진행 중 사건·예정 점검 열람</li><li>이메일 구독으로 사건 알림 수신</li></ol></article>
  </div>
  <p>관리자 화면과 공개 페이지를 분리한 덕에, 내부 운영 정보를 노출하지 않고도 고객에게 투명성을 줄 수 있다. 도입 시 "무엇을 공개하고 무엇을 숨길지"를 그룹 단위로 먼저 정하는 것이 좋다. 흔한 실수는 내부 전용 모니터(예: DB 백업 잡)를 공개 상태페이지에 그대로 노출해, 고객에게 불필요한 불안을 주는 것이다. 공개 그룹과 비공개 그룹을 처음부터 분리해 두면 이런 사고를 막을 수 있다.</p>
</section>'''

s10 = f'''
<section id="s10" class="getting-started summary-card">
  {h2("10","시작 방법 · 어디에 맞나","check")}
  <p class="h2-sub">5분 안에 띄우는 단계와, 우리 상황에 맞는지 판단 기준을 함께 둔다.</p>
  <ol class="practice-list">
    <li><strong>기동</strong> — 컨테이너 실행, <code>/data</code> 볼륨 마운트, 관리자 계정 생성.</li>
    <li><strong>첫 모니터</strong> — 우리 서비스 헬스 URL 등록, 주기 1분, 기대 코드 200.</li>
    <li><strong>알림 연결</strong> — 슬랙 웹훅 등록 후 강제 실패로 알림 발화 확인.</li>
    <li><strong>상태페이지</strong> — 서비스 그룹 만들고 도메인 연결, 공개 범위 설정.</li>
  </ol>
  <div class="grid-2">
    <article class="good"><span class="label">적합</span><p>소수 서비스를 셀프호스트로 운영하고, 데이터 주권·낮은 비용·간단함을 중시하는 팀.</p></article>
    <article class="danger"><span class="label">부적합</span><p>분산 추적·로그 상관·대규모 APM이 필요한 경우. 이 도구는 가용성 모니터링에 특화돼 있다.</p></article>
  </div>
</section>'''

snext = f'''
<section id="snext" class="try">
  {h2(None,"최종 정리 · 다음 행동","success")}
  <p>가볍게 도입해 "살아있는지 + 고객에게 보여주기"를 동시에 해결하려는 팀에게 잘 맞는다. 깊은 관측이 목표라면 범주가 다른 도구를 봐야 한다.</p>
  <div class="cta-box">
    <p><strong>도입 1일차 체크</strong></p>
    <ol><li>컨테이너 기동 + <code>/data</code> 볼륨·백업 경로 확정</li><li>핵심 서비스 3개 모니터 등록 + 슬랙 알림 검증</li><li>공개 상태페이지 그룹 설계(공개/비공개 경계)</li></ol>
    <div class="tag-list"><span class="tag">github_feature_usage</span><span class="tag">uptime</span><span class="tag">self-hosted</span><span class="tag">status-page</span></div>
  </div>
</section>'''

source_note = '<aside class="source-note"><p><strong>출처 한계.</strong> 본 가이드의 "실제 화면"은 라이브 스크린샷이 아니라 주요 화면의 정보 구조를 설명한 HTML 패널이다. 기술 스택·아키텍처·기능 세부는 일반적 셀프호스트 모니터의 구성을 바탕으로 한 설명이며, 정확한 버전·의존성·라이선스·성능 수치는 대상 저장소의 README·문서·데모에서 직접 확인해야 한다(확인 필요).</p></aside>'

body = ('<main id="main" class="page-wide layout-github-feature">' + header + toc + s1+s2+s3+s4+s5+s6+s7+s8+s9+s10+snext + source_note + '</main>')
out = build_page("pages/06_github_feature_usage_upkeep_monitor.html", title=TITLE, description=DESC, body=body)
write_sources()
print("WROTE", out)
