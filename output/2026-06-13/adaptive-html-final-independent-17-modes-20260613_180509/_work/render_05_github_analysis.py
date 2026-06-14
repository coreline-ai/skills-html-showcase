#!/usr/bin/env python3
"""Mode 05 / 17 — github_analysis (sequential). Topic: 경량 작업 큐(가칭 taskq/taskq) 도입 실사.
Layout: github-analysis.html (.layout-github) · auto · vt: hero-map(hm-grid) · wg: wg-11. FACT/INFERENCE/UNKNOWN 분리.
"""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _finalize import build_page, write_sources, h2, SKILL, ASSETS  # noqa: E402,F401

for _p in [SKILL/"SKILL.md", SKILL/"references/github-analysis-system.md", ASSETS/"layouts/github-analysis.html",
           ASSETS/"visual-html-templates/01-hero-map.html", ASSETS/"widget-templates/11-weekly-status.html"]:
    _p.read_text(encoding="utf-8")

TITLE = "경량 작업 큐 라이브러리 도입 실사 — taskq 분석"
DESC = "백그라운드 작업 큐 오픈소스 후보(taskq)를 사용·채택·감사 관점에서 평가한 github_analysis 리포트. 관측 사실·추론·확인 불가를 분리하고 도입 판단과 다음 행동을 제시한다."

header = '''
<header class="header github-header">
  <div class="kicker"><span class="kicker-text">GITHUB ANALYSIS · MODE 05 / 17 · 독립 빌드</span></div>
  <h1>경량 작업 큐 라이브러리 도입 실사</h1>
  <p class="sub">백그라운드 작업 큐 오픈소스 후보(가칭 <code>taskq/taskq</code>)를 "우리 서비스에 채택해도 되는가" 관점에서 평가한다. README 미화가 아니라 사용·운영·감사 의사결정을 돕는 실사 리포트다.</p>
  <div class="meta"><span>profile auto</span><span>layout github-analysis</span><span>분석 기준 2026-06-13</span><span>관측·추론·확인불가 분리</span></div>
  <div class="generated-row"><p class="generated-date">Generated · 2026-06-13 KST</p>
  <div class="lens-strip" aria-label="적용 렌즈"><span class="lens-strip-label">LENS</span><span class="lens-chip">FACT</span><span class="lens-chip">INFERENCE</span><span class="lens-chip">UNKNOWN</span><span class="lens-chip">유지보수</span><span class="lens-chip">도입 위험</span></div></div>
</header>'''

toc = '''
<nav class="toc-map github-question-toc" aria-label="GitHub 분석 목차"><div class="toc-pills">
  <a class="toc-pill" href="#s1"><b>01</b> 도입 판정</a><a class="toc-pill" href="#s2"><b>02</b> 저장소 한눈에</a>
  <a class="toc-pill" href="#s3"><b>03</b> 5분 도입 준비도</a><a class="toc-pill" href="#s4"><b>04</b> 살아있는 프로젝트인가</a>
  <a class="toc-pill" href="#s5"><b>05</b> 코드·파일 투어</a><a class="toc-pill" href="#s6"><b>06</b> 릴리스·활동 추이</a>
  <a class="toc-pill" href="#s7"><b>07</b> 보안·라이선스</a><a class="toc-pill" href="#s8"><b>08</b> 리스크 매트릭스</a>
  <a class="toc-pill" href="#s9"><b>09</b> 최종 의사결정</a><a class="toc-pill" href="#s10"><b>10</b> 출처 한계·확인 필요</a>
  <a class="toc-pill" href="#snext"><b>→</b> 다음 행동</a>
</div></nav>'''

s1 = f'''
<section id="s1" class="github-verdict summary-card">
  {h2("01","도입 판정","audit")}
  <p class="h2-sub">결론부터: 소규모~중간 트래픽 서비스에는 <strong>조건부 채택</strong>, 고신뢰 결제·정산 경로에는 <strong>보류</strong>. 판단 근거는 관측 신호와 확인 한계를 함께 본 결과다.</p>
  <div class="grid-3">
    <article class="score-card"><h3>FACT · 관측</h3><p>README에 재시도·지연 큐·우선순위 API가 문서화되어 있고, 예제와 빠른 시작 가이드가 제공된다. 라이선스 파일이 저장소 루트에 존재한다.</p></article>
    <article class="score-card"><h3>INFERENCE · 추론</h3><p>API 표면과 예제 구성으로 보아 단일 프로세스~중소 규모를 1차 타깃으로 설계된 것으로 보인다. 대규모 분산 보장은 핵심 목표가 아닌 듯하다.</p></article>
    <article class="score-card"><h3>UNKNOWN · 확인 필요</h3><p>실제 처리량·장애 복구 동작·메인테이너 응답 속도는 이 리포트만으로 단정할 수 없다. 도입 전 PoC와 직접 확인이 필요하다.</p></article>
  </div>
  <p>즉 "써볼 만한 후보지만, 임계 경로에 올리기 전 직접 검증이 필요한 단계"라는 판정이다. 아래 섹션은 이 판정의 근거를 신호별로 분해하며, 각 신호마다 관측된 사실과 추론, 그리고 아직 확인하지 못한 부분을 구분해 표시한다.</p>
</section>'''

s2 = f'''
<section id="s2" class="repo-identity summary-card">
  {h2("02","저장소 한눈에","map")}
  <p class="h2-sub">무엇을 해결하는 라이브러리이고, 어디에 쓰라고 만들어졌는지를 세 축으로 요약한다.</p>
  <section class="vt-shell" aria-label="저장소 정체성 지도">
    <div class="vt-frame"><div class="vt-demo"><div class="hm-grid">
      <article class="hm-card"><div class="vt-kicker">Problem</div><h3>비동기 작업 처리</h3><p class="vt-text">요청-응답 밖에서 처리해야 하는 메일 발송·썸네일·정산 같은 작업.</p></article>
      <article class="hm-card" style="--c:var(--vt-blue)"><div class="vt-kicker">Approach</div><h3>큐 + 워커 모델</h3><p class="vt-text">작업을 직렬화해 백엔드(레디스 등)에 넣고 워커가 당겨 처리. 재시도·지연·우선순위 지원.</p></article>
      <article class="hm-card" style="--c:var(--vt-green)"><div class="vt-kicker">Fit</div><h3>중소 규모 우선</h3><p class="vt-text">셀프호스트 단일~소수 워커 환경에 적합. 초대규모 분산은 별도 검증 영역.</p></article>
    </div><div class="hm-result"><b>요약: "작은 운영 부담으로 비동기 작업을 다루는 큐"</b><span>화려한 분산 기능보다 도입 용이성에 무게가 실린 포지셔닝(INFERENCE).</span></div></div></div>
  </section>
  <p>정체성은 "가벼움"이다. 무거운 브로커나 복잡한 운영 없이 작업 큐를 붙이고 싶은 팀이 1차 사용자다. 이 포지셔닝이 우리 요구와 맞는지가 채택의 출발점이다. 만약 우리가 초당 수만 건의 분산 처리를 원한다면 이 도구는 처음부터 후보가 아니며, 그 경우엔 더 무거운 전용 브로커를 보는 편이 맞다.</p>
</section>'''

s3 = f'''
<section id="s3" class="quickstart-readiness summary-card">
  {h2("03","5분 도입 준비도","search")}
  <p class="h2-sub">처음 붙이는 데 드는 마찰을 점검한다. "예제대로 따라 하면 동작하는가"가 핵심이다.</p>
  <ul class="check-list">
    <li><strong>설치</strong> — 패키지 매니저 한 줄 설치로 추정(FACT: README 설치 섹션 존재). 별도 빌드 단계 불필요로 보임.</li>
    <li><strong>최소 예제</strong> — 큐 생성 → 작업 등록 → 워커 실행 3단계 예제가 제공된다(FACT).</li>
    <li><strong>백엔드 의존</strong> — 레디스 등 외부 스토어가 필요할 가능성이 높다(INFERENCE). 운영 시 이 의존성의 가용성이 곧 큐의 가용성이다.</li>
    <li><strong>로컬 검증</strong> — 도커로 백엔드를 띄워 예제를 돌려보는 PoC를 권장. 실패 주입 테스트까지 해봐야 한다.</li>
  </ul>
  <p>도입 마찰 자체는 낮아 보인다. 다만 "쉽게 붙는다"와 "안전하게 운영된다"는 다른 문제다. 예제는 정상 경로(happy path)만 보여주기 마련이므로, 워커가 죽거나 백엔드 연결이 끊겼을 때 작업이 유실되는지, 중복 실행되는지, 데드레터로 빠지는지를 PoC 단계에서 의도적으로 망가뜨려 확인해야 한다. 준비도 점수가 높다는 것은 "시작이 빠르다"는 뜻이지 "운영이 안전하다"는 보증이 아니다.</p>
</section>'''

s4 = f'''
<section id="s4" class="repo-health summary-card">
  {h2("04","살아있는 프로젝트인가","metric")}
  <p class="h2-sub">유지보수 신호를 상태판으로 본다. 아래 수치는 도입 판단을 돕기 위한 <strong>가정 시나리오</strong>이며 실제 저장소에서 직접 확인해야 한다(UNKNOWN).</p>
  <section class="wg-11" aria-labelledby="m05-ws-title">
    <header class="wg-11-head"><p class="wg-11-kicker">유지보수 신호 (확인 필요 가정치)</p><h2 id="m05-ws-title" class="wg-11-h">taskq 활동 상태 스냅샷</h2><p class="wg-11-lead">최근 커밋·이슈 응답·릴리스 주기를 한 화면으로. 실제 값은 GitHub에서 재확인.</p></header>
    <div class="wg-11-kpis">
      <div class="wg-11-kpi wg-11-kpi-good"><span class="wg-11-kpi-v">활발</span><span class="wg-11-kpi-l">최근 커밋</span></div>
      <div class="wg-11-kpi wg-11-kpi-prog"><span class="wg-11-kpi-v">중간</span><span class="wg-11-kpi-l">이슈 응답</span></div>
      <div class="wg-11-kpi wg-11-kpi-risk"><span class="wg-11-kpi-v wg-11-warn">1인</span><span class="wg-11-kpi-l">버스 팩터</span></div>
      <div class="wg-11-kpi"><span class="wg-11-kpi-v">?</span><span class="wg-11-kpi-l">SLA</span></div>
    </div>
    <h3 class="wg-11-h3">건전성 축 (정성 평가)</h3>
    <div class="wg-11-bars">
      <div class="wg-11-bar-row"><span class="wg-11-bar-label">문서화</span><div class="wg-11-track" role="img" aria-label="문서화 80퍼센트"><div class="wg-11-fill wg-11-fill-good" style="width:80%"></div></div><span class="wg-11-bar-pct">양호</span></div>
      <div class="wg-11-bar-row"><span class="wg-11-bar-label">테스트 가시성</span><div class="wg-11-track" role="img" aria-label="테스트 가시성 55퍼센트"><div class="wg-11-fill wg-11-fill-prog" style="width:55%"></div></div><span class="wg-11-bar-pct">보통</span></div>
      <div class="wg-11-bar-row"><span class="wg-11-bar-label">기여자 다양성</span><div class="wg-11-track" role="img" aria-label="기여자 다양성 30퍼센트, 리스크"><div class="wg-11-fill wg-11-fill-risk" style="width:30%"></div></div><span class="wg-11-bar-pct">주의</span></div>
    </div>
    <div class="wg-11-cols">
      <div class="wg-11-col wg-11-col-good"><h4 class="wg-11-col-h"><span class="wg-11-dot"></span>긍정</h4><ul class="wg-11-col-list"><li>예제·문서가 충실</li><li>API가 작고 일관적</li></ul></div>
      <div class="wg-11-col wg-11-col-prog"><h4 class="wg-11-col-h"><span class="wg-11-dot"></span>중립</h4><ul class="wg-11-col-list"><li>릴리스 주기 확인 필요</li><li>벤치마크 공개 여부 불명</li></ul></div>
      <div class="wg-11-col wg-11-col-risk"><h4 class="wg-11-col-h"><span class="wg-11-dot"></span>주의</h4><ul class="wg-11-col-list"><li>핵심 기여자 편중 <span class="wg-11-flag">버스 팩터</span></li></ul></div>
    </div>
  </section>
</section>'''

s5 = f'''
<section id="s5" class="code-tour summary-card">
  {h2("05","코드·파일 투어","file")}
  <p class="h2-sub">채택 시 우리가 읽고 고치게 될 핵심 파일을 미리 짚는다. 표면적이 작을수록 감사 비용이 낮다.</p>
  <section class="vt-shell" aria-label="핵심 파일 투어">
    <div class="vt-frame"><div class="ft">
      <article class="ft-card"><div class="ft-head"><span>queue.*</span><span>core</span></div><div class="ft-body"><p class="vt-text">작업 직렬화·등록·우선순위 로직의 중심.</p><div class="ft-note"><b>Review note</b><br>직렬화 포맷과 버전 호환 정책을 확인한다.</div></div></article>
      <article class="ft-card"><div class="ft-head"><span>worker.*</span><span>runtime</span></div><div class="ft-body"><p class="vt-text">작업 당김·재시도·실패 처리 루프.</p><div class="ft-note"><b>Review note</b><br>실패 시 재시도/데드레터 동작이 가장 중요한 감사 포인트.</div></div></article>
      <article class="ft-card"><div class="ft-head"><span>backend/*</span><span>adapter</span></div><div class="ft-body"><p class="vt-text">레디스 등 저장소 어댑터.</p><div class="ft-note"><b>Review note</b><br>연결 끊김·타임아웃 시 동작과 멱등성을 본다.</div></div></article>
    </div></div>
  </section>
  <p>가장 위험한 코드는 <code>worker</code>의 실패 처리다. "작업이 한 번만 실행되는가, 아니면 적어도 한 번인가"가 우리 도메인에서 허용되는지 반드시 확인해야 한다. 멱등하지 않은 작업(예: 결제 승인)에 at-least-once 큐를 쓰면 중복 실행 사고가 난다.</p>
</section>'''

s6 = f'''
<section id="s6" class="release-roadmap summary-card">
  {h2("06","릴리스·활동 추이","timeline")}
  <p class="h2-sub">버전 흐름은 프로젝트의 성숙도와 호환성 정책을 보여준다. 아래는 일반적 OSS 성숙 곡선에 비춘 해석이다.</p>
  <section class="vt-shell" aria-label="릴리스 활동 타임라인">
    <div class="vt-frame"><ol class="tl">
      <li class="tl-item"><b>초기</b><p class="vt-text">핵심 큐·워커 API 확립. 잦은 파괴적 변경 가능성(0.x 단계 추정).</p></li>
      <li class="tl-item"><b>안정화</b><p class="vt-text">백엔드 어댑터·재시도 정책 확장. 문서 정비.</p></li>
      <li class="tl-item"><b>1.0 이후</b><p class="vt-text">SemVer 준수 여부가 채택 안정성의 핵심 지표(확인 필요).</p></li>
      <li class="tl-item"><b>현재</b><p class="vt-text">활동 자체는 관측되나 릴리스 주기·LTS 정책은 미확인(UNKNOWN).</p></li>
    </ol></div>
  </section>
  <p>채택 안정성의 핵심은 "버전 0.x인가 1.x 이상인가"다. 0.x라면 파괴적 변경을 각오하고 버전을 고정(pin)해야 한다. 이 정보는 릴리스 노트와 태그에서 직접 확인한다.</p>
</section>'''

s7 = f'''
<section id="s7" class="security-license summary-card">
  {h2("07","보안·라이선스","security")}
  <p class="h2-sub">법무·보안 통과 여부를 가른다. 라이선스와 의존성 취약점은 코드 품질과 별개의 게이트다.</p>
  <div class="card-grid">
    <article class="mini-card"><h3>라이선스</h3><p>루트에 라이선스 파일 존재(FACT). 정확한 종류(MIT/Apache 등)와 상업적 사용 조건은 파일 원문으로 확인 필요.</p></article>
    <article class="mini-card"><h3>의존성</h3><p>외부 백엔드·직렬화 라이브러리 의존이 예상된다. 의존성 트리의 알려진 취약점 스캔이 도입 전 필수.</p></article>
    <article class="mini-card"><h3>공급망</h3><p>릴리스 서명·체크섬 제공 여부 미확인(UNKNOWN). 패키지 무결성 검증 절차를 도입 파이프라인에 둔다.</p></article>
  </div>
  <div class="danger"><span class="label">게이트</span><p>라이선스가 우리 배포 모델과 호환되지 않으면 코드 품질이 아무리 좋아도 채택 불가다. 이 확인을 가장 먼저, 그리고 법무와 함께 한다.</p></div>
</section>'''

s8 = f'''
<section id="s8" class="risk-matrix summary-card">
  {h2("08","리스크 매트릭스","warning")}
  <p class="h2-sub">도입 시 마주칠 위험을 가능성·영향으로 정렬한다. 상단 두 줄이 의사결정의 핵심이다.</p>
  <div class="table-scroll"><table>
    <caption>taskq 도입 리스크 — 가능성·영향·완화</caption>
    <thead><tr><th>리스크</th><th>가능성</th><th>영향</th><th>완화책</th></tr></thead>
    <tbody>
      <tr><th>중복 실행(at-least-once)</th><td>중</td><td>높음</td><td>작업 멱등화 + 처리 키 중복 차단</td></tr>
      <tr><th>버스 팩터(1인 유지보수)</th><td>중</td><td>높음</td><td>버전 고정 + 포크 대비 + 내부 이해도 확보</td></tr>
      <tr><th>백엔드 장애 전파</th><td>중</td><td>중</td><td>백엔드 HA + 워커 재연결·백오프 점검</td></tr>
      <tr><th>버전 파괴적 변경</th><td>중</td><td>중</td><td>SemVer 확인 + 의존성 pin + 업그레이드 테스트</td></tr>
    </tbody>
  </table></div>
  <p>가장 비싼 위험은 "중복 실행 × 비멱등 작업"의 조합이다. 우리 작업이 멱등하지 않다면, 큐 선택보다 작업 설계(멱등 키, 중복 차단)를 먼저 해결해야 한다.</p>
</section>'''

s9 = f'''
<section id="s9" class="decision-tree summary-card">
  {h2("09","최종 의사결정","decision")}
  <p class="h2-sub">도메인 특성에 따라 결론이 갈린다. 한 가지 정답이 아니라 조건부 권고다.</p>
  <div class="grid-2">
    <article class="good"><span class="label">채택 권고</span><p>내부 알림·썸네일·리포트 생성처럼 <strong>멱등하거나 재실행이 안전한</strong> 비동기 작업. 도입 마찰이 낮아 빠르게 가치를 본다.</p></article>
    <article class="danger"><span class="label">보류 권고</span><p>결제 승인·정산처럼 <strong>중복 실행이 곧 사고</strong>인 경로. 멱등 설계와 exactly-once 보장을 먼저 해결하기 전에는 올리지 않는다.</p></article>
  </div>
  <p>요약하면 "라이브러리 자체는 합격선, 적용 범위가 결론을 결정한다." 같은 도구라도 어디에 쓰느냐에 따라 채택과 보류가 동시에 정답일 수 있다.</p>
</section>'''

s10 = f'''
<section id="s10" class="summary-card">
  {h2("10","출처 한계 · 확인 필요","source")}
  <p class="h2-sub">이 리포트가 무엇을 단정하지 않는지 명시한다. 아래 항목은 도입 전 반드시 직접 확인한다(UNKNOWN).</p>
  <ul class="check-list">
    <li><strong>정량 지표</strong> — 스타·커밋 빈도·이슈 응답 시간·테스트 커버리지의 실제 수치는 GitHub에서 직접 확인.</li>
    <li><strong>실행 보장</strong> — at-least-once / exactly-once 여부와 데드레터 동작은 코드와 테스트로 검증.</li>
    <li><strong>성능</strong> — 처리량·지연은 공개 벤치마크가 아닌 우리 환경 PoC로 측정.</li>
    <li><strong>라이선스 원문</strong> — 정확한 라이선스 종류와 조건은 파일 원문 + 법무 검토.</li>
  </ul>
  <p>이 리포트는 "무엇을 확인해야 하는지의 지도"이지 "확인을 끝낸 결론"이 아니다. 관측 신호는 합리적이지만, 임계 경로 채택은 위 확인을 통과한 뒤에만 한다.</p>
</section>'''

snext = f'''
<section id="snext" class="try">
  {h2(None,"다음 행동","landing")}
  <p>판단을 행동으로 옮긴다. PoC와 확인 항목을 1주 안에 닫는 것을 권한다.</p>
  <div class="cta-box">
    <p><strong>1주 도입 검증 플랜</strong></p>
    <ol><li>도커로 백엔드 + taskq 예제 구동, 실패 주입(워커 강제 종료) 후 재시도 동작 관찰.</li><li>at-least-once 여부 확인 → 비멱등 작업이면 멱등 키 설계.</li><li>라이선스·의존성 취약점 스캔 + 법무 확인.</li><li>버전 고정 정책과 업그레이드 테스트 절차 합의.</li></ol>
    <div class="tag-list"><span class="tag">github_analysis</span><span class="tag">due-diligence</span><span class="tag">task-queue</span><span class="tag">조건부 채택</span></div>
  </div>
</section>'''

source_note = '<aside class="source-note"><p><strong>출처·범위.</strong> 본 리포트는 작업 큐 오픈소스 채택 의사결정을 돕기 위한 실사 템플릿을 가상의 후보 저장소(taskq/taskq)에 적용한 구조적 평가다. 별점·커밋·라이선스 종류 등 정량·법적 사실은 실제 GitHub 저장소와 라이선스 원문에서 직접 확인해야 하며, 본 문서의 신호 해석은 그 확인을 대체하지 않는다.</p></aside>'

body = ('<main id="main" class="page-wide layout-github">' + header + toc + s1+s2+s3+s4+s5+s6+s7+s8+s9+s10+snext + source_note + '</main>')
out = build_page("pages/05_github_analysis_taskq_due_diligence.html", title=TITLE, description=DESC, body=body)
write_sources()
print("WROTE", out)
