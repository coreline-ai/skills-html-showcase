#!/usr/bin/env python3
"""Mode 08 / 17 — manual_analysis (sequential). Topic: 사내 Kubernetes 운영 런북 역할별 재구성.
Layout: manual-analysis.html (.layout-manual) · auto · vt: hero-map(hm-grid) · wg: wg-16.
"""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _finalize import build_page, write_sources, h2, SKILL, ASSETS  # noqa: E402,F401

for _p in [SKILL/"SKILL.md", SKILL/"references/manual-analysis-system.md", ASSETS/"layouts/manual-analysis.html",
           ASSETS/"visual-html-templates/01-hero-map.html", ASSETS/"widget-templates/16-implementation-plan.html"]:
    _p.read_text(encoding="utf-8")

TITLE = "사내 Kubernetes 운영 런북 — 역할별 재구성"
DESC = "흩어진 사내 Kubernetes 운영 메모를 출처·버전·역할별 실행 경로·사전조건·작업 레시피·트러블슈팅·운영 런북·감사로 재구성한 manual_analysis 리포트."

header = '''
<header class="header manual-header">
  <div class="kicker"><span class="kicker-text">MANUAL ANALYSIS · MODE 08 / 17 · 독립 빌드</span></div>
  <h1>사내 Kubernetes 운영 런북, 역할별로 다시 쓰기</h1>
  <p class="sub">위키 곳곳에 흩어진 K8s 운영 메모를 "누가, 무엇을, 어떤 순서로, 무엇을 확인하며" 수행하는지로 재구성한다. 재요약이 아니라 실제로 따라 할 수 있는 실행 매뉴얼을 목표로 한다.</p>
  <div class="meta"><span>profile auto</span><span>layout manual-analysis</span><span>원문: 사내 위키 v다수(혼재)</span><span>미확인은 UNKNOWN</span></div>
  <div class="generated-row"><p class="generated-date">Generated · 2026-06-13 KST</p>
  <div class="lens-strip" aria-label="적용 렌즈"><span class="lens-strip-label">LENS</span><span class="lens-chip">역할별 경로</span><span class="lens-chip">사전조건</span><span class="lens-chip">안전</span><span class="lens-chip">트러블슈팅</span><span class="lens-chip">원문 근거</span></div></div>
</header>'''

toc = '''
<nav class="toc-map manual-reader-toc" aria-label="매뉴얼 분석 목차"><div class="toc-pills">
  <a class="toc-pill" href="#s1"><b>01</b> 재구성 판정</a><a class="toc-pill" href="#s2"><b>02</b> 출처·버전 스냅샷</a>
  <a class="toc-pill" href="#s3"><b>03</b> 역할별 라우터</a><a class="toc-pill" href="#s4"><b>04</b> 첫 성공 경로</a>
  <a class="toc-pill" href="#s5"><b>05</b> 사전조건·안전</a><a class="toc-pill" href="#s6"><b>06</b> 작업 레시피</a>
  <a class="toc-pill" href="#s7"><b>07</b> 레퍼런스 발췌</a><a class="toc-pill" href="#s8"><b>08</b> 의사결정 가이드</a>
  <a class="toc-pill" href="#s9"><b>09</b> 트러블슈팅</a><a class="toc-pill" href="#s10"><b>10</b> 운영 런북·감사</a>
  <a class="toc-pill" href="#snext"><b>→</b> 다음 행동·출처 한계</a>
</div></nav>'''

s1 = f'''
<section id="s1" class="manual-verdict summary-card">
  {h2("01","재구성 판정","audit")}
  <p class="h2-sub">현재 원문은 "정보는 있으나 실행 순서가 없는" 상태다. 명령어 조각은 많지만 누가 언제 어떤 전제로 쓰는지가 빠져 있어, 신규 담당자가 따라 하기 어렵다.</p>
  <div class="grid-3">
    <article class="score-card"><h3>강점</h3><p>실제 운영에서 쓰는 명령·매니페스트 예시가 풍부하다. 현장 지식이 메모 형태로 남아 있다.</p></article>
    <article class="score-card"><h3>결함</h3><p>역할 구분·사전조건·롤백·안전 경고가 빠져 있다. 위험한 명령과 일상 명령이 같은 비중으로 나열돼 있다.</p></article>
    <article class="score-card"><h3>판정</h3><p><strong>재구성 필요.</strong> 역할 라우터 + 6필드 레시피 + 트러블슈팅 4단 구조로 다시 쓰면 온보딩·사고 대응 시간이 크게 준다.</p></article>
  </div>
  <p>핵심은 "명령을 모으는 것"이 아니라 "안전하게 실행하는 순서를 부여하는 것"이다. 아래는 원문을 역할과 절차 중심으로 재배치한 결과다.</p>
</section>'''

s2 = f'''
<section id="s2" class="source-version summary-card">
  {h2("02","출처·버전 스냅샷 (Source & Version)","source")}
  <p class="h2-sub">무엇을 근거로 재구성했고, 무엇이 불확실한지 먼저 못 박는다.</p>
  <div class="table-scroll"><table>
    <caption>원문 출처·버전 상태</caption>
    <thead><tr><th>출처</th><th>상태</th><th>비고</th></tr></thead>
    <tbody>
      <tr><th>위키 "K8s 배포"</th><td>최신 추정</td><td>명령 예시 다수, 최종 수정일 확인 필요</td></tr>
      <tr><th>위키 "장애 대응"</th><td>혼재</td><td>구버전 클러스터 기준 절차가 섞여 있음(stale 의심)</td></tr>
      <tr><th>클러스터 버전</th><td>UNKNOWN</td><td>문서마다 다르게 기재 — 실제 <code>kubectl version</code>으로 확정 필요</td></tr>
      <tr><th>권한/SLA</th><td>UNKNOWN</td><td>원문에 명시 없음 — 추정하지 않음</td></tr>
    </tbody>
  </table></div>
  <p>특히 "장애 대응" 문서는 오래된(stale) 절차가 섞여 있어, 본 재구성에서는 각 항목의 <strong>원문 위치와 확인 필요 여부</strong>를 함께 표기했다. 버전·권한·SLA처럼 원문에 없는 값은 UNKNOWN으로 두고 추정하지 않는다.</p>
</section>'''

s3 = f'''
<section id="s3" class="role-router summary-card">
  {h2("03","역할별 라우터 (Reader Role Router)","user")}
  <p class="h2-sub">읽는 사람이 누구냐에 따라 시작점이 다르다. 역할별 권장 읽기 순서와 이관 기준을 정의한다.</p>
  <div class="card-grid">
    <article class="mini-card"><h3>신규 온보딩</h3><p>§4 첫 성공 경로 → §5 사전조건 → §6 레시피 순. 위험 명령은 멘토 동석 전까지 실행 금지.</p></article>
    <article class="mini-card"><h3>온콜 대응자</h3><p>§9 트러블슈팅 → §10 운영 런북 직행. 증상으로 진입해 4단 절차를 따른다.</p></article>
    <article class="mini-card"><h3>플랫폼 엔지니어</h3><p>§6 레시피 + §8 의사결정 가이드 중심. 롤백·영향 범위를 먼저 본다.</p></article>
    <article class="mini-card"><h3>리뷰어/리드</h3><p>§2 출처·§10 감사 중심. 문서 정합성과 위험 명령 가드를 점검한다.</p></article>
  </div>
  <p><strong>이관 기준</strong>: 온콜이 15분 내 완화에 실패하면 플랫폼 엔지니어로, 데이터 손실 위험이 보이면 즉시 리드로 에스컬레이션한다. 역할 경계를 명시해 "내 일이 아닌 줄 알았다"는 공백을 없앤다.</p>
</section>'''

s4 = f'''
<section id="s4" class="first-success summary-card">
  {h2("04","첫 성공 경로","map")}
  <p class="h2-sub">신규 담당자가 "30분 안에 안전하게 한 번 성공"하는 경로를 지도로 제시한다.</p>
  <section class="vt-shell" aria-label="첫 성공 경로 지도">
    <div class="vt-frame"><div class="vt-demo"><div class="hm-grid">
      <article class="hm-card"><div class="vt-kicker">접속</div><h3>안전한 읽기 권한</h3><p class="vt-text">읽기 전용 컨텍스트로 클러스터 상태를 먼저 관찰한다.</p></article>
      <article class="hm-card" style="--c:var(--vt-blue)"><div class="vt-kicker">관찰</div><h3>현재 상태 파악</h3><p class="vt-text">파드·디플로이·이벤트를 조회해 정상 기준선을 익힌다.</p></article>
      <article class="hm-card" style="--c:var(--vt-green)"><div class="vt-kicker">실행</div><h3>저위험 작업 1건</h3><p class="vt-text">스테이징에서 롤아웃 재시작 같은 되돌리기 쉬운 작업으로 시작.</p></article>
    </div><div class="hm-result"><b>원칙: 읽기 → 관찰 → 되돌리기 쉬운 실행</b><span>첫 작업은 반드시 롤백 가능한 것으로 고른다.</span></div></div></div>
  </section>
  <p>첫 성공의 목표는 "무언가를 고치는 것"이 아니라 "안전하게 한 사이클을 도는 감각"을 얻는 것이다. 위험한 명령(삭제·스케일 0·노드 드레인)은 이 단계 이후, 사전조건을 갖춘 뒤에만 다룬다.</p>
</section>'''

s5 = f'''
<section id="s5" class="prerequisites-safety summary-card">
  {h2("05","사전조건 · 안전 (Prerequisites & Safety)","security")}
  <p class="h2-sub">실행 전 갖춰야 할 것과, 절대 하지 말아야 할 것을 분리한다. 안전 경고는 명령과 같은 비중으로 둔다.</p>
  <div class="good"><span class="label">사전조건</span><p>올바른 컨텍스트(<code>kubectl config current-context</code>)와 네임스페이스 확인, 변경 작업 전 현재 매니페스트 백업, 스테이징 우선 검증, 변경 알림 채널 공지.</p></div>
  <div class="danger"><span class="label">위험 — 가드 필요</span><p><code>delete</code>·<code>scale --replicas=0</code>·노드 드레인·PVC 삭제는 데이터·가용성에 직접 영향. 프로덕션 컨텍스트에서는 2인 확인(four-eyes) 없이 실행 금지. 원문에 이 경고가 없던 항목은 본 재구성에서 추가했다.</p></div>
  <p>안전의 핵심은 "되돌릴 수 있는가"다. 되돌리기 어려운 명령은 항상 백업·확인·승인 세 가지를 통과한 뒤 실행한다. 이 규칙 하나가 대부분의 운영 사고를 막는다.</p>
</section>'''

s6 = f'''
<section id="s6" class="task-recipes summary-card">
  {h2("06","작업 레시피 (6필드 표준)","check")}
  <p class="h2-sub">자주 쓰는 작업을 목적·사전조건·절차·완료 기준·롤백·원문 근거 6필드로 표준화했다.</p>
  <div class="card-grid">
    <article class="card-block"><h3>레시피 A · 디플로이 롤아웃 재시작</h3><ul><li><strong>목적</strong> 설정 갱신 반영을 위한 무중단 재시작</li><li><strong>사전조건</strong> 올바른 컨텍스트·네임스페이스 확인</li><li><strong>절차</strong> <code>kubectl rollout restart deploy/&lt;name&gt;</code> → 상태 관찰</li><li><strong>완료 기준</strong> 신규 파드 Ready, 오류율 정상</li><li><strong>롤백</strong> <code>kubectl rollout undo</code></li><li><strong>원문 근거</strong> 위키 "K8s 배포" §재시작</li></ul></article>
    <article class="card-block"><h3>레시피 B · 수평 스케일 조정</h3><ul><li><strong>목적</strong> 트래픽 증가 대응</li><li><strong>사전조건</strong> 리소스 쿼터·노드 여유 확인</li><li><strong>절차</strong> <code>kubectl scale deploy/&lt;name&gt; --replicas=N</code></li><li><strong>완료 기준</strong> 목표 replica Ready, HPA 충돌 없음</li><li><strong>롤백</strong> 이전 replica 수로 복귀</li><li><strong>원문 근거</strong> 위키 "K8s 배포" §스케일</li></ul></article>
    <article class="card-block"><h3>레시피 C · 설정/시크릿 갱신</h3><ul><li><strong>목적</strong> ConfigMap/Secret 변경 반영</li><li><strong>사전조건</strong> 변경 전 현재 값 백업</li><li><strong>절차</strong> apply → 대상 디플로이 재시작</li><li><strong>완료 기준</strong> 신규 값 로드 확인</li><li><strong>롤백</strong> 백업 값 재적용</li><li><strong>원문 근거</strong> 위키 "K8s 배포" §설정</li></ul></article>
    <article class="card-block"><h3>레시피 D · 롤아웃 상태 점검</h3><ul><li><strong>목적</strong> 배포 진행/정체 확인</li><li><strong>사전조건</strong> 읽기 권한</li><li><strong>절차</strong> <code>kubectl rollout status</code> + 이벤트 조회</li><li><strong>완료 기준</strong> 진행 완료 또는 원인 식별</li><li><strong>롤백</strong> 해당 없음(읽기)</li><li><strong>원문 근거</strong> 위키 "장애 대응" §확인</li></ul></article>
  </div>
</section>'''

s7 = f'''
<section id="s7" class="reference-extract summary-card">
  {h2("07","레퍼런스 발췌","reference")}
  <p class="h2-sub">자주 찾는 조회 명령을 빠른 참조로 모았다. 모두 읽기 전용이라 안전하다.</p>
  <div class="table-scroll"><table>
    <caption>자주 쓰는 조회 명령 빠른 참조</caption>
    <thead><tr><th>목적</th><th>명령</th><th>볼 것</th></tr></thead>
    <tbody>
      <tr><th>파드 상태</th><td><code>kubectl get pods -n &lt;ns&gt;</code></td><td>Running/CrashLoopBackOff 분포</td></tr>
      <tr><th>최근 이벤트</th><td><code>kubectl get events --sort-by=.lastTimestamp</code></td><td>스케줄링·OOM·이미지 풀 실패</td></tr>
      <tr><th>로그</th><td><code>kubectl logs &lt;pod&gt; --previous</code></td><td>재시작 직전 오류</td></tr>
      <tr><th>리소스 사용</th><td><code>kubectl top pod -n &lt;ns&gt;</code></td><td>CPU/메모리 압박</td></tr>
    </tbody>
  </table></div>
  <p>조회 명령부터 손에 익히는 것이 안전 운영의 출발이다. 변경 전후로 같은 조회를 돌려 "무엇이 달라졌는지"를 항상 눈으로 확인하는 습관을 권한다.</p>
</section>'''

s8 = f'''
<section id="s8" class="decision-guide summary-card">
  {h2("08","의사결정 가이드","decision")}
  <p class="h2-sub">"재시작할까 롤백할까 스케일할까"를 빠르게 가르는 분기다. 망설임이 곧 장애 시간이다.</p>
  <div class="grid-2">
    <article class="good"><span class="label">롤아웃 재시작</span><p>설정/시크릿을 방금 바꿨고, 코드 변경은 없을 때. 가장 가볍고 안전한 1차 시도.</p></article>
    <article class="good"><span class="label">롤백(undo)</span><p>직전 배포 이후 오류율이 급등했을 때. 원인 분석보다 복구가 우선이면 즉시 undo.</p></article>
    <article class="good"><span class="label">스케일 조정</span><p>리소스 압박·트래픽 급증이 명확할 때. 노드 여유를 먼저 확인.</p></article>
    <article class="danger"><span class="label">멈추고 에스컬레이션</span><p>데이터 손실·다중 서비스 영향이 보이면 단독 판단 금지. 즉시 상위로.</p></article>
  </div>
  <p>원칙은 "되돌리기 쉬운 것부터." 재시작 → 롤백 → 스케일 순으로 시도하되, 데이터·가용성에 비가역 영향이 보이면 즉시 멈추고 사람을 부른다.</p>
</section>'''

s9 = f'''
<section id="s9" class="troubleshooting summary-card">
  {h2("09","트러블슈팅 (증상→원인→진단→복구)","warning")}
  <p class="h2-sub">증상으로 진입해 4단계로 좁힌다. 온콜이 가장 먼저 펼치는 섹션이다.</p>
  <div class="card-grid">
    <article class="card-block"><h3>증상 1 · CrashLoopBackOff</h3><ol><li><strong>증상</strong> 파드가 반복 재시작</li><li><strong>가능 원인</strong> 잘못된 설정·시작 명령·의존 서비스 부재</li><li><strong>진단</strong> <code>logs --previous</code> + <code>describe pod</code> 이벤트</li><li><strong>복구</strong> 설정 수정 후 재배포, 직전 배포면 롤백</li></ol></article>
    <article class="card-block"><h3>증상 2 · Pending(스케줄 안 됨)</h3><ol><li><strong>증상</strong> 파드가 Pending에 머무름</li><li><strong>가능 원인</strong> 리소스 부족·노드 셀렉터·PVC 미바인딩</li><li><strong>진단</strong> <code>describe pod</code>의 이벤트, 노드 리소스 확인</li><li><strong>복구</strong> 리소스 요청 조정 또는 노드 증설</li></ol></article>
    <article class="card-block"><h3>증상 3 · 5xx 급증</h3><ol><li><strong>증상</strong> 서비스 5xx 비율 상승</li><li><strong>가능 원인</strong> 신규 배포 회귀·의존성 장애·리소스 압박</li><li><strong>진단</strong> 배포 시점 상관, 오류 로그, <code>top pod</code></li><li><strong>복구</strong> 의심 배포 롤백, 필요 시 스케일 업</li></ol></article>
  </div>
  <p>세 증상 모두 진단은 "로그 + describe 이벤트 + 배포 시점 상관"의 조합으로 시작한다. 원인을 모를 때도 복구(롤백)는 먼저 할 수 있다 — 복구와 원인 분석을 분리하는 것이 평균 복구 시간을 줄이는 핵심이다.</p>
</section>'''

s10 = f'''
<section id="s10" class="operations-runbook summary-card">
  {h2("10","운영 런북 · 매뉴얼 감사","search")}
  <p class="h2-sub">정례 운영 작업의 도입 계획과, 원문 매뉴얼의 결함을 위치 근거와 함께 지적한다.</p>
  <section class="wg-16" aria-labelledby="m08-wg16-title">
    <header class="wg-16-head"><p class="wg-16-kicker">운영 정착 계획 · OPS-08</p><h2 id="m08-wg16-title" class="wg-16-h">런북 표준화 90일 계획</h2><p class="wg-16-lead">흩어진 메모를 <strong>역할별 실행 문서</strong>로 표준화하고 위험 명령 가드를 정착시킵니다.</p></header>
    <div class="wg-16-panel">
      <h3 class="wg-16-h3">마일스톤</h3>
      <ol class="wg-16-ms">
        <li class="wg-16-ms-item wg-16-done"><div class="wg-16-ms-mark"><span class="wg-16-ms-node"></span></div><div class="wg-16-ms-card"><div class="wg-16-ms-top"><span class="wg-16-ms-name">M0 · 원문 수집·출처 표기</span><span class="wg-16-badge wg-16-bd-done">완료</span></div><p class="wg-16-ms-desc">흩어진 문서를 모으고 stale 항목을 표시.</p></div></li>
        <li class="wg-16-ms-item wg-16-active"><div class="wg-16-ms-mark"><span class="wg-16-ms-node"></span></div><div class="wg-16-ms-card"><div class="wg-16-ms-top"><span class="wg-16-ms-name">M1 · 6필드 레시피화 (0~30일)</span><span class="wg-16-badge wg-16-bd-active">진행 중</span></div><p class="wg-16-ms-desc">핵심 작업 10건을 6필드 레시피로 전환.</p></div></li>
        <li class="wg-16-ms-item"><div class="wg-16-ms-mark"><span class="wg-16-ms-node"></span></div><div class="wg-16-ms-card"><div class="wg-16-ms-top"><span class="wg-16-ms-name">M2 · 위험 가드 정착 (31~60일)</span><span class="wg-16-badge">예정</span></div><p class="wg-16-ms-desc">비가역 명령에 2인 확인·백업 절차 의무화.</p></div></li>
        <li class="wg-16-ms-item"><div class="wg-16-ms-mark"><span class="wg-16-ms-node"></span></div><div class="wg-16-ms-card"><div class="wg-16-ms-top"><span class="wg-16-ms-name">M3 · 분기 감사 (61~90일)</span><span class="wg-16-badge">예정</span></div><p class="wg-16-ms-desc">문서-실제 정합성 분기 점검 정례화.</p></div></li>
      </ol>
    </div>
  </section>
  <div class="danger"><span class="label">매뉴얼 감사 — 지적 3건(원문 위치 근거)</span><p>① 위키 "장애 대응" §노드 드레인: 백업·확인 경고 없음(stale, 구버전 절차) — 원문 근거 위치 명시 후 가드 추가 필요. ② "K8s 배포" §스케일: 리소스 쿼터 확인 단계 누락. ③ 클러스터 버전이 문서마다 모순 — 실제 버전으로 단일화 필요(확인 불가 항목 UNKNOWN 처리).</p></div>
</section>'''

snext = f'''
<section id="snext" class="try">
  {h2(None,"다음 행동 · 출처 한계","landing")}
  <p>재구성의 가치는 "신규 담당자가 사고 없이 첫 작업을 끝내고, 온콜이 증상으로 바로 진입"하는 데 있다. 아래를 1차로 닫는다.</p>
  <div class="cta-box">
    <p><strong>실행 플랜</strong></p>
    <ol><li>위험 명령(delete·scale 0·드레인)에 2인 확인 가드 즉시 도입.</li><li>핵심 작업 10건을 6필드 레시피로 전환, 원문 위치 링크 부착.</li><li>클러스터 실제 버전 확정 후 문서 모순 해소.</li></ol>
    <div class="tag-list"><span class="tag">manual_analysis</span><span class="tag">kubernetes</span><span class="tag">runbook</span><span class="tag">역할별</span></div>
  </div>
</section>'''

source_note = '<aside class="source-note"><p><strong>출처 한계.</strong> 본 재구성의 원문은 사내 위키의 혼재된 운영 메모이며, 클러스터 버전·권한·SLA는 문서마다 다르거나 누락돼 UNKNOWN으로 두었다. stale로 표시한 절차는 구버전 기준일 가능성이 있어 실제 환경에서 재확인이 필요하다. 명령 예시는 일반 <code>kubectl</code> 패턴이며 사내 정책(승인·백업)이 우선한다.</p></aside>'

body = ('<main id="main" class="page-wide layout-manual">' + header + toc + s1+s2+s3+s4+s5+s6+s7+s8+s9+s10+snext + source_note + '</main>')
out = build_page("pages/08_manual_analysis_k8s_runbook.html", title=TITLE, description=DESC, body=body)
write_sources()
print("WROTE", out)
