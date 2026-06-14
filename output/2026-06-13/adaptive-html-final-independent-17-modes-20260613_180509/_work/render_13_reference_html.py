#!/usr/bin/env python3
"""Mode 13 / 17 — reference_html (sequential). Topic: cron 표현식 & 스케줄링 레퍼런스.
Layout: reference-manual.html (.layout-reference) · auto · vt: file-tour(ft-card) · wg: wg-14.
"""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _finalize import build_page, write_sources, h2, SKILL, ASSETS  # noqa: E402,F401

for _p in [SKILL/"SKILL.md", SKILL/"references/layout-system.md", ASSETS/"layouts/reference-manual.html",
           ASSETS/"visual-html-templates/09-file-tour.html", ASSETS/"widget-templates/14-feature-explainer.html"]:
    _p.read_text(encoding="utf-8")

TITLE = "cron 표현식 & 스케줄링 레퍼런스"
DESC = "cron 5필드 구문, 특수문자, 자주 쓰는 패턴, crontab·systemd timer·Kubernetes CronJob 비교, 타임존 함정과 디버깅까지 한 장으로 보는 스케줄링 레퍼런스 치트시트."

header = '''
<header class="header reference-header">
  <div class="kicker"><span class="kicker-text">REFERENCE · MODE 13 / 17 · 독립 빌드</span></div>
  <h1>cron 표현식 &amp; 스케줄링 레퍼런스</h1>
  <p class="sub">"분 시 일 월 요일" 다섯 칸의 의미부터, crontab·systemd·Kubernetes에서의 차이, 타임존 함정과 디버깅까지 — 자주 찾는 것만 한 장으로 모았다.</p>
  <div class="meta"><span>profile auto</span><span>layout reference-manual</span><span>치트시트</span><span>POSIX cron 기준</span></div>
  <div class="generated-row"><p class="generated-date">Generated · 2026-06-13 KST</p>
  <div class="lens-strip" aria-label="적용 렌즈"><span class="lens-strip-label">LENS</span><span class="lens-chip">구문</span><span class="lens-chip">패턴</span><span class="lens-chip">플랫폼 차이</span><span class="lens-chip">함정</span><span class="lens-chip">디버깅</span></div></div>
</header>'''

toc = '''
<nav class="toc-map reference-toc" aria-label="레퍼런스 목차"><div class="toc-pills">
  <a class="toc-pill" href="#s1"><b>01</b> 빠른 참조</a><a class="toc-pill" href="#s2"><b>02</b> 필드별 의미</a>
  <a class="toc-pill" href="#s3"><b>03</b> 특수문자</a><a class="toc-pill" href="#s4"><b>04</b> 플랫폼별 설정</a>
  <a class="toc-pill" href="#s5"><b>05</b> 자주 쓰는 패턴</a><a class="toc-pill" href="#s6"><b>06</b> 표현식 해설</a>
  <a class="toc-pill" href="#s7"><b>07</b> 타임존·환경 함정</a><a class="toc-pill" href="#s8"><b>08</b> 디버깅·검증</a>
  <a class="toc-pill" href="#s9"><b>09</b> 무엇을 쓸까</a><a class="toc-pill" href="#snext"><b>→</b> 적용 체크리스트</a>
</div></nav>'''

s1 = f'''
<section id="s1" class="quick-reference summary-card">
  {h2("01","빠른 참조","reference")}
  <p class="h2-sub">cron 한 줄은 다섯 칸의 시간 필드 + 실행할 명령으로 이뤄진다. 이 한 표가 90%를 설명한다.</p>
  <div class="table-scroll"><table>
    <caption>cron 5필드 구조와 허용 범위</caption>
    <thead><tr><th>위치</th><th>필드</th><th>허용 값</th><th>예</th></tr></thead>
    <tbody>
      <tr><th>1</th><td>분(minute)</td><td>0–59</td><td><code>0</code> = 정각</td></tr>
      <tr><th>2</th><td>시(hour)</td><td>0–23</td><td><code>2</code> = 새벽 2시</td></tr>
      <tr><th>3</th><td>일(day of month)</td><td>1–31</td><td><code>1</code> = 매월 1일</td></tr>
      <tr><th>4</th><td>월(month)</td><td>1–12</td><td><code>*</code> = 매월</td></tr>
      <tr><th>5</th><td>요일(day of week)</td><td>0–7 (0·7=일)</td><td><code>1</code> = 월요일</td></tr>
    </tbody>
  </table></div>
  <p>예를 들어 <code>0 2 * * 1</code>은 "매주 월요일 새벽 2시 0분"이다. 왼쪽부터 분·시·일·월·요일 순서이며, <code>*</code>는 "모든 값"을 뜻한다. 일과 요일을 둘 다 지정하면 대부분의 cron이 <strong>OR</strong>로 해석한다는 점만 기억하면 출발점으로 충분하다.</p>
</section>'''

s2 = f'''
<section id="s2" class="ref-grid summary-card">
  {h2("02","필드별 의미와 주의점","note")}
  <p class="h2-sub">각 필드에는 헷갈리기 쉬운 함정이 하나씩 숨어 있다.</p>
  <div class="card-grid">
    <article class="mini-card"><h3>분·시</h3><p>가장 자주 쓰는 두 칸. "매시 정각"은 <code>0 * * * *</code>. 분을 비우고 시만 지정하는 실수가 잦다 — 분이 <code>*</code>면 그 시간대 매분 실행된다.</p></article>
    <article class="mini-card"><h3>일 vs 요일</h3><p>둘 다 지정하면 OR. <code>0 0 1 * 1</code>은 "1일 또는 월요일"이지 "1일이면서 월요일"이 아니다. 가장 흔한 오해.</p></article>
    <article class="mini-card"><h3>요일 숫자</h3><p>0과 7이 모두 일요일. 시스템마다 이름(SUN·MON) 허용 여부가 다르니 숫자가 안전하다.</p></article>
    <article class="mini-card"><h3>월</h3><p>1–12. 0이나 13은 오류. 일부 구현은 JAN·FEB 이름을 허용하지만 이식성을 위해 숫자 권장.</p></article>
  </div>
  <p>핵심 교훈은 "일과 요일의 OR"이다. "매월 1일이면서 월요일"처럼 AND 조건이 필요하면 cron 한 줄로는 표현할 수 없고, 스크립트 안에서 날짜를 다시 확인해야 한다.</p>
</section>'''

s3 = f'''
<section id="s3" class="patterns summary-card">
  {h2("03","특수문자 한눈에","code")}
  <p class="h2-sub">네 개의 특수문자만 알면 대부분의 스케줄을 표현할 수 있다.</p>
  <div class="table-scroll"><table>
    <caption>cron 특수문자와 의미</caption>
    <thead><tr><th>문자</th><th>의미</th><th>예</th><th>해석</th></tr></thead>
    <tbody>
      <tr><th><code>*</code></th><td>모든 값</td><td><code>* * * * *</code></td><td>매분</td></tr>
      <tr><th><code>,</code></th><td>목록</td><td><code>0 9,18 * * *</code></td><td>매일 9시·18시 정각</td></tr>
      <tr><th><code>-</code></th><td>범위</td><td><code>0 9-18 * * *</code></td><td>9시~18시 매시 정각</td></tr>
      <tr><th><code>/</code></th><td>간격(step)</td><td><code>*/15 * * * *</code></td><td>15분마다</td></tr>
    </tbody>
  </table></div>
  <p>조합하면 강력해진다. <code>0 9-18/3 * * 1-5</code>는 "평일 9시부터 18시까지 3시간 간격 정각"이다. step(<code>/</code>)은 범위나 <code>*</code>와 함께 써야 하며, 단독으로는 의미가 없다. 많은 cron이 <code>@daily</code>·<code>@hourly</code> 같은 매크로도 지원하지만, 이식성을 원하면 다섯 칸 표기를 쓰는 편이 안전하다.</p>
</section>'''

s4 = f'''
<section id="s4" class="examples summary-card">
  {h2("04","플랫폼별 설정 파일","file")}
  <p class="h2-sub">같은 "새벽 2시 실행"이라도 어디에 적느냐에 따라 파일과 형식이 다르다.</p>
  <section class="vt-shell" aria-label="플랫폼별 스케줄 설정 투어">
    <div class="vt-frame"><div class="ft">
      <article class="ft-card"><div class="ft-head"><span>crontab -e</span><span>classic</span></div><div class="ft-body"><p class="vt-text">사용자별 crontab. <code>0 2 * * * /path/job.sh</code> 한 줄.</p><div class="ft-note"><b>주의</b><br>실행 환경의 PATH가 로그인 셸과 다르다.</div></div></article>
      <article class="ft-card"><div class="ft-head"><span>*.timer</span><span>systemd</span></div><div class="ft-body"><p class="vt-text"><code>OnCalendar&#61;*-*-* 02:00:00</code> + 짝이 되는 .service.</p><div class="ft-note"><b>주의</b><br>cron보다 로깅·의존성·재시도가 강력.</div></div></article>
      <article class="ft-card"><div class="ft-head"><span>CronJob</span><span>k8s</span></div><div class="ft-body"><p class="vt-text"><code>schedule: "0 2 * * *"</code>로 파드를 주기 실행.</p><div class="ft-note"><b>주의</b><br>concurrencyPolicy·실패 보존 개수 설정 필수.</div></div></article>
    </div></div>
  </section>
  <p>형식은 달라도 시간 표현의 뿌리는 같은 cron 구문이다(systemd만 OnCalendar라는 자체 문법). 따라서 cron 다섯 칸을 익혀 두면 세 환경 모두에 빠르게 적응할 수 있다. 차이는 "시간 표현"보다 "로깅·재시도·동시 실행 제어"에 있다.</p>
</section>'''

s5 = f'''
<section id="s5" class="patterns summary-card">
  {h2("05","자주 쓰는 패턴","check")}
  <p class="h2-sub">복사해서 바로 쓰는 실전 패턴 모음. 의도를 함께 적었다.</p>
  <div class="table-scroll"><table>
    <caption>실전 cron 패턴 모음</caption>
    <thead><tr><th>목적</th><th>표현식</th><th>설명</th></tr></thead>
    <tbody>
      <tr><th>매일 새벽 배치</th><td><code>0 3 * * *</code></td><td>매일 03:00 — 트래픽 낮은 시간</td></tr>
      <tr><th>5분마다 헬스체크</th><td><code>*/5 * * * *</code></td><td>5분 간격 반복</td></tr>
      <tr><th>평일 업무 시작</th><td><code>0 9 * * 1-5</code></td><td>월–금 09:00</td></tr>
      <tr><th>매월 1일 정산</th><td><code>0 0 1 * *</code></td><td>매월 1일 자정</td></tr>
      <tr><th>매주 일요일 정리</th><td><code>30 4 * * 0</code></td><td>일요일 04:30</td></tr>
      <tr><th>15분마다 업무시간</th><td><code>*/15 9-18 * * 1-5</code></td><td>평일 9–18시 15분 간격</td></tr>
    </tbody>
  </table></div>
  <p>패턴을 고를 때 한 가지만 기억하자 — <strong>배치는 트래픽이 낮고 서로 겹치지 않는 시각</strong>에 둔다. 모든 배치를 <code>0 0 * * *</code>(자정)에 몰면 자원 경합이 생긴다. 분 단위를 분산(<code>0</code>, <code>10</code>, <code>20</code> …)시키는 것만으로도 부하가 평탄해진다.</p>
</section>'''

s6 = ('<section id="s6" class="examples summary-card">' + h2("06","표현식 해설 — 플랫폼별 예","experiment") + '''
  <p class="h2-sub">"평일 새벽 2시"를 세 플랫폼에서 각각 어떻게 적는지 탭으로 비교한다.</p>
  <section class="wg-14" aria-labelledby="m13-wg14-title">
    <p class="wg-14-kicker">스케줄 표현 · 평일 02:00</p>
    <h2 id="m13-wg14-title" class="wg-14-h">같은 일정, 세 가지 표기</h2>
    <p class="wg-14-lead">시간 표현의 뿌리는 cron이지만, systemd는 자체 문법을 씁니다.</p>
    <div class="wg-14-tldr" role="note" aria-label="핵심 요약"><span class="wg-14-tldr-tag">TL;DR</span><p class="wg-14-tldr-body"><strong>crontab과 k8s는 동일한 cron 5필드</strong>를 쓰고, systemd만 <code>OnCalendar</code> 문법으로 같은 시각을 표현합니다.</p></div>
    <h3 class="wg-14-h3">설정 예시</h3>
    <div class="wg-14-tabs">
      <input type="radio" name="m13-tab" id="m13-tab-cron" class="wg-14-tab-in" checked>
      <input type="radio" name="m13-tab" id="m13-tab-systemd" class="wg-14-tab-in">
      <input type="radio" name="m13-tab" id="m13-tab-k8s" class="wg-14-tab-in">
      <div class="wg-14-tablist">
        <label class="wg-14-tab" for="m13-tab-cron">crontab</label>
        <label class="wg-14-tab" for="m13-tab-systemd">systemd</label>
        <label class="wg-14-tab" for="m13-tab-k8s">k8s CronJob</label>
      </div>
      <pre class="wg-14-code wg-14-code-yml"><code># 평일(월-금) 새벽 2시
0 2 * * 1-5 /opt/jobs/nightly.sh</code></pre>
      <pre class="wg-14-code wg-14-code-cli"><code># /etc/systemd/system/nightly.timer
[Timer]
OnCalendar&#61;Mon..Fri 02:00:00
Persistent=true</code></pre>
      <pre class="wg-14-code wg-14-code-api"><code>schedule: "0 2 * * 1-5"
concurrencyPolicy: Forbid
successfulJobsHistoryLimit: 3</code></pre>
    </div>
    <h3 class="wg-14-h3">자주 묻는 질문</h3>
    <div class="wg-14-faq">
      <details class="wg-14-q"><summary class="wg-14-q-sum">systemd OnCalendar가 cron보다 나은 점은</summary><p class="wg-14-q-a">놓친 실행 보정(<code>Persistent</code>), 의존성, 자체 로깅(journalctl)이 강점입니다.</p></details>
      <details class="wg-14-q"><summary class="wg-14-q-sum">k8s에서 동시 실행을 막으려면</summary><p class="wg-14-q-a"><code>concurrencyPolicy: Forbid</code>로 이전 작업이 안 끝나면 새 실행을 건너뜁니다.</p></details>
    </div>
  </section>
</section>''')

s7 = f'''
<section id="s7" class="patterns summary-card">
  {h2("07","타임존·환경 함정","warning")}
  <p class="h2-sub">cron 사고의 대부분은 구문이 아니라 "어떤 시간대·어떤 환경에서 실행되는가"에서 난다.</p>
  <div class="card-grid">
    <article class="mini-card"><span class="case-label">치명</span><h3>타임존</h3><p>cron은 보통 시스템 로컬 시간대로 동작한다. UTC 서버에 한국 시간 기준으로 적으면 9시간 어긋난다. 컨테이너는 기본 UTC인 경우가 많다.</p></article>
    <article class="mini-card"><span class="case-label">치명</span><h3>PATH·환경변수</h3><p>cron은 최소 환경에서 실행된다. 셸에서 되던 명령이 cron에선 "command not found"가 나면 PATH 문제다. 절대경로를 쓴다.</p></article>
    <article class="mini-card"><span class="case-label">경고</span><h3>겹침 실행</h3><p>이전 작업이 안 끝났는데 다음 주기가 오면 중복 실행된다. 락 파일이나 concurrency 정책으로 막는다.</p></article>
    <article class="mini-card"><span class="case-label">경고</span><h3>DST</h3><p>서머타임 전환일에는 특정 시각이 건너뛰거나 두 번 올 수 있다. 중요 배치는 UTC 기준으로 둔다.</p></article>
  </div>
  <p>실무 원칙 하나로 요약하면 <strong>"명령은 절대경로로, 시간은 UTC로, 겹침은 락으로"</strong>다. 이 세 가지만 지켜도 cron 사고의 대부분이 사라진다.</p>
</section>'''

s8 = f'''
<section id="s8" class="examples summary-card">
  {h2("08","디버깅·검증","search")}
  <p class="h2-sub">"왜 안 돌았지?"를 빠르게 좁히는 점검 순서다.</p>
  <ul class="check-list">
    <li><strong>표현식 검증</strong> — 사람이 읽기 전에, 표현식이 "다음에 언제 실행되는지"를 계산해 의도와 맞는지 확인한다(온라인/CLI 파서 활용).</li>
    <li><strong>실행 여부 로그</strong> — 시스템 cron 로그(예: <code>/var/log/syslog</code>)나 systemd <code>journalctl</code>로 트리거 자체가 됐는지 본다.</li>
    <li><strong>환경 재현</strong> — 의심되면 <code>env -i /bin/sh -c '명령'</code>처럼 최소 환경에서 직접 실행해 PATH 문제를 재현한다.</li>
    <li><strong>출력 보존</strong> — 명령 끝에 <code>&gt;&gt; /var/log/job.log 2&gt;&amp;1</code>로 표준출력·에러를 남겨 실패 원인을 확보한다.</li>
  </ul>
  <p>디버깅의 핵심은 "트리거됐는가"와 "실행 중 실패했는가"를 분리하는 것이다. 로그에 트리거 기록이 없으면 표현식·타임존 문제, 트리거는 됐는데 결과가 없으면 PATH·권한·명령 자체의 문제다.</p>
</section>'''

s9 = f'''
<section id="s9" class="patterns summary-card">
  {h2("09","무엇을 쓸까 — 선택 기준","compare")}
  <p class="h2-sub">cron이 늘 정답은 아니다. 환경과 요구에 따라 더 나은 선택이 있다.</p>
  <div class="table-scroll"><table class="table criteria-table">
    <caption>스케줄러 선택 기준</caption>
    <thead><tr><th>기준</th><th>판단 포인트</th><th>유리한 선택</th><th>주의할 점</th></tr></thead>
    <tbody>
      <tr><th>단순 주기 작업</th><td>로깅·재시도 요구 낮음</td><td>crontab</td><td>환경·타임존 직접 관리</td></tr>
      <tr><th>로깅·의존성 필요</th><td>실패 추적·놓친 실행 보정</td><td>systemd timer</td><td>유닛 2개(timer+service) 작성</td></tr>
      <tr><th>컨테이너 환경</th><td>쿠버네티스 운영 중</td><td>k8s CronJob</td><td>동시성·히스토리 정책 필수</td></tr>
      <tr><th>분산·워크플로</th><td>의존 그래프·재시도·백필</td><td>워크플로 엔진</td><td>cron보다 운영 복잡도↑</td></tr>
    </tbody>
  </table></div>
  <p>요약하면 "단순하면 cron, 운영성이 필요하면 systemd/k8s, 의존 그래프가 있으면 워크플로 엔진"이다. cron의 장점은 단순함이므로, 재시도·의존성·백필이 필요해지는 순간이 다른 도구로 옮길 신호다.</p>
</section>'''

snext = f'''
<section id="snext" class="try">
  {h2(None,"적용 체크리스트","landing")}
  <p>cron 한 줄을 운영에 올리기 전, 아래 네 가지만 확인하면 흔한 사고를 피할 수 있다.</p>
  <div class="cta-box">
    <p><strong>배포 전 점검</strong></p>
    <ol><li>표현식을 파서로 검증해 "다음 실행 시각"이 의도와 같은가.</li><li>명령은 절대경로인가, 실행 환경의 PATH를 가정하지 않는가.</li><li>시간대가 UTC인가, 로컬인가 — 명시적으로 확인했는가.</li><li>겹침 실행을 락/concurrency로 막았는가, 출력을 로그로 남기는가.</li></ol>
    <div class="tag-list"><span class="tag">cron</span><span class="tag">scheduling</span><span class="tag">systemd</span><span class="tag">kubernetes</span></div>
  </div>
</section>'''

source_note = '<aside class="source-note"><p><strong>범위.</strong> 본 치트시트는 POSIX/Vixie cron 표준 동작을 기준으로 한다. 일부 구현(예: 특정 배포판·언어 라이브러리)은 초(second) 필드 추가나 매크로 지원 등 확장 동작이 있으니, 사용하는 환경의 문서로 확정한다. systemd OnCalendar는 cron과 별도 문법이다.</p></aside>'

body = ('<main id="main" class="page-wide layout-reference">' + header + toc + s1+s2+s3+s4+s5+s6+s7+s8+s9+snext + source_note + '</main>')
out = build_page("pages/13_reference_html_cron_scheduling.html", title=TITLE, description=DESC, body=body)
write_sources()
print("WROTE", out)
