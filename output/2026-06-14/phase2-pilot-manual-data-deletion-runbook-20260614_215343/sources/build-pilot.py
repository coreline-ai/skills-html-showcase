#!/usr/bin/env python3
from __future__ import annotations
import hashlib, json, re, shutil
from pathlib import Path
from html import escape

ROOT = Path(__file__).resolve().parents[4]
SKILL = ROOT / 'skills/adaptive-html-final'
OUT = Path(__file__).resolve().parents[1]
ASSETS = SKILL / 'assets'

CORE = ['theme.css','components.css','visual-components.css','layouts.css','print.css']
COND = ['widgets.css','visual-html.css','body-icons.css','editorial-patterns.css','shape-visuals.css','workflow-visuals.css','theme-dark.css']
INLINE = ['theme.css','components.css','visual-components.css','widgets.css','visual-html.css','body-icons.css','editorial-patterns.css','shape-visuals.css','workflow-visuals.css','layouts.css','print.css','theme-dark.css']

def read(p: Path) -> str:
    return p.read_text(encoding='utf-8')

def sha(text: str) -> str:
    return hashlib.sha256(text.encode('utf-8')).hexdigest()

manifest = json.loads(read(SKILL/'manifest.json'))
version = manifest['version']
icons = {item['id']: item['svg'] for item in json.loads(read(ASSETS/'body-icons.json'))}

def icon(icon_id: str) -> str:
    return f'<span class="body-icon body-icon--sm" aria-hidden="true">{icons[icon_id]}</span>'

def h2(n: int, icon_id: str, title: str, sub: str) -> str:
    return f'<h2>{icon(icon_id)}<span class="num">{n:02d}</span>{title}</h2>\n<p class="h2-sub">{sub}</p>'

def table(headers, rows, caption, cls='tbl mobile-card-table'):
    head = ''.join(f'<th scope="col">{escape(h)}</th>' for h in headers)
    body_rows = []
    for r in rows:
        cells = ''.join(f'<td data-label="{escape(headers[i])}">{cell}</td>' for i, cell in enumerate(r))
        body_rows.append(f'<tr>{cells}</tr>')
    return f'<div class="table-scroll"><table class="{cls}"><caption>{caption}</caption><thead><tr>{head}</tr></thead><tbody>{"".join(body_rows)}</tbody></table></div>'

# Evidence: read official files and hash them before body construction.
evidence_files = [
    'AGENTS.md',
    'skills/adaptive-html-final/SKILL.md',
    'skills/adaptive-html-final/modes/08-manual-analysis.json',
    'skills/adaptive-html-final/assets/base.html',
    'skills/adaptive-html-final/assets/layouts/manual-analysis.html',
    'skills/adaptive-html-final/assets/visual-html-templates/01-hero-map.html',
    'skills/adaptive-html-final/assets/widget-templates/04-module-map.html',
    'skills/adaptive-html-final/assets/widget-templates/13-annotated-flowchart.html',
    'skills/adaptive-html-final/assets/body-icons.json',
    'docs/adaptive-html-final-template-authoring-protocol.md',
]
evidence = {
    'profile': 'auto',
    'mode': 'manual_analysis',
    'topic': '고객 데이터 삭제 요청 운영 매뉴얼',
    'layout': 'manual-analysis.html',
    'primary_vt': 'hero-map',
    'wg': ['wg-04', 'wg-13'],
    'section_mapping': {
        'manual-verdict': 'vt hero-map + source status verdict',
        'role-router': 'manual role grid',
        'first-success': 'official wg-13 flow vocabulary adapted to first success',
        'reference-extract': 'official wg-04 module map vocabulary adapted to source bundle map',
        'task-recipes': '6-field mobile-card-table recipe matrix',
        'troubleshooting': '3 scenario 4-step manual trouble grid',
    },
    'files': []
}
for rel in evidence_files:
    p = ROOT / rel
    evidence['files'].append({'path': rel, 'sha256': hashlib.sha256(p.read_bytes()).hexdigest(), 'reason': 'Phase 2 pilot 공식 템플릿/계약 확인'})

hero_map = '''
<div class="vt-shell" aria-label="역할별 실행 지도">
  <div class="vt-frame">
    <div class="vt-demo">
      <div class="hm-grid">
        <article class="hm-card"><div class="vt-kicker">Request</div><h3>고객 요청을 접수한다</h3><p class="vt-text">지원 담당자는 티켓에 고객 식별자·요청 범위·본인 확인 상태를 분리해 기록한다. 확인되지 않은 요청은 삭제 큐에 넣지 않는다.</p></article>
        <article class="hm-card" style="--c:var(--vt-blue)"><div class="vt-kicker">Decision</div><h3>보류·중단 조건을 먼저 판정한다</h3><p class="vt-text">법적 보존·결제 분쟁·보안 조사 태그가 있으면 운영자가 즉시 STOP으로 전환하고 소유자 검토를 요청한다.</p></article>
        <article class="hm-card" style="--c:var(--vt-green)"><div class="vt-kicker">Proof</div><h3>삭제보다 증빙을 먼저 남긴다</h3><p class="vt-text">DB 작업 전후의 감사 로그, 고객 통지 초안, 롤백 불가 범위를 같은 티켓에 묶어 사후 추적을 가능하게 한다.</p></article>
      </div>
      <div class="hm-result"><b>판정: 자동 삭제가 아니라 역할별 승인 매뉴얼이 필요</b><span>요청 접수·보존 판정·삭제 실행·고객 통지의 책임자가 달라, 절차서 없이 처리하면 누락과 과삭제가 동시에 발생한다.</span></div>
    </div>
  </div>
</div>
'''

wg04 = '''
<section class="wg-04" aria-labelledby="wg-04-title-pilot">
  <header class="wg-04-head">
    <p class="wg-04-kicker">Source Bundle Map</p>
    <h2 id="wg-04-title-pilot" class="wg-04-title">원문 묶음 의존성 · 삭제 요청 처리 문서 5종</h2>
    <p class="wg-04-lead">노드는 원문 파일, 화살표는 실제 처리 순서에서 참조되는 방향입니다. <strong class="wg-04-crit-word">붉은 굵은 경로</strong>는 누락 시 과삭제 또는 미삭제가 발생하는 핵심 경로입니다.</p>
    <ul class="wg-04-legend" aria-label="범례">
      <li><span class="wg-04-lg wg-04-lg-entry" aria-hidden="true"></span> 접수 문서</li>
      <li><span class="wg-04-lg wg-04-lg-core" aria-hidden="true"></span> 운영 정본</li>
      <li><span class="wg-04-lg wg-04-lg-leaf" aria-hidden="true"></span> 증빙/통지</li>
      <li><span class="wg-04-lg wg-04-lg-crit" aria-hidden="true"></span> 핵심 경로</li>
    </ul>
  </header>
  <div class="wg-04-diagram">
    <svg viewBox="0 0 640 360" class="wg-04-svg" role="img" aria-labelledby="wg-04-pilot-t wg-04-pilot-d">
      <title id="wg-04-pilot-t">고객 데이터 삭제 요청 원문 의존성 다이어그램</title>
      <desc id="wg-04-pilot-d">support intake가 privacy deletion policy와 legal hold matrix를 참조하고, data job runbook과 audit log checklist로 이어지는 구조.</desc>
      <defs><marker id="wg-04-arrow-pilot" markerWidth="8" markerHeight="8" refX="7" refY="3" orient="auto"><path d="M0,0 L7,3 L0,6 Z" fill="var(--ink-mute)"></path></marker><marker id="wg-04-arrow-crit-pilot" markerWidth="9" markerHeight="9" refX="7" refY="3" orient="auto"><path d="M0,0 L7,3 L0,6 Z" fill="var(--accent)"></path></marker></defs>
      <g><path class="wg-04-edge wg-04-edge-crit" d="M120,70 L120,150" marker-end="url(#wg-04-arrow-crit-pilot)"></path><path class="wg-04-edge" d="M160,55 L310,150" marker-end="url(#wg-04-arrow-pilot)"></path><path class="wg-04-edge wg-04-edge-crit" d="M120,190 L120,270" marker-end="url(#wg-04-arrow-crit-pilot)"></path><path class="wg-04-edge" d="M310,190 L310,270" marker-end="url(#wg-04-arrow-pilot)"></path><path class="wg-04-edge" d="M310,190 L500,270" marker-end="url(#wg-04-arrow-pilot)"></path></g>
      <g class="wg-04-node wg-04-node-entry"><rect x="50" y="30" width="140" height="40" rx="8"></rect><text x="120" y="55">support intake</text></g>
      <g class="wg-04-node wg-04-node-core wg-04-node-crit"><rect x="45" y="150" width="150" height="40" rx="8"></rect><text x="120" y="175">privacy policy</text></g>
      <g class="wg-04-node wg-04-node-core"><rect x="235" y="150" width="150" height="40" rx="8"></rect><text x="310" y="175">legal hold</text></g>
      <g class="wg-04-node wg-04-node-leaf wg-04-node-crit"><rect x="45" y="270" width="150" height="40" rx="8"></rect><text x="120" y="295">data job</text></g>
      <g class="wg-04-node wg-04-node-leaf"><rect x="235" y="270" width="150" height="40" rx="8"></rect><text x="310" y="295">audit log</text></g>
      <g class="wg-04-node wg-04-node-leaf"><rect x="425" y="270" width="150" height="40" rx="8"></rect><text x="500" y="295">customer notice</text></g>
    </svg>
  </div>
  <div class="wg-04-path" role="note"><span class="wg-04-path-label">핵심 경로</span><span class="wg-04-path-chain"><code>intake</code> → <code>privacy</code> → <code>data job</code></span><span class="wg-04-path-note">이 경로의 근거가 빠지면 삭제 처리 완료 판정을 내리지 않는다.</span></div>
</section>
'''

wg13 = '''
<section class="wg-13-fc" aria-label="첫 성공 삭제 요청 처리 플로우차트">
  <h3 class="wg-13-h">첫 성공 플로우 <span class="wg-13-sub">30분 안에 안전하게 대기열까지 올리는 경로</span></h3>
  <div class="wg-13-flow">
    <a href="#wg-13-s1" class="wg-13-node wg-13-node--start"><span class="wg-13-step">시작</span>티켓 접수</a><span class="wg-13-arrow" aria-hidden="true">↓</span>
    <a href="#wg-13-s2" class="wg-13-node"><span class="wg-13-step">1</span>본인 확인</a><span class="wg-13-arrow" aria-hidden="true">↓</span>
    <div class="wg-13-branch"><a href="#wg-13-s3" class="wg-13-node wg-13-node--decide"><span class="wg-13-step">2</span>STOP 조건?</a><div class="wg-13-paths"><div class="wg-13-path wg-13-path--fail"><span class="wg-13-edge">있음 → 보류</span><a href="#wg-13-fail" class="wg-13-node wg-13-node--fail"><span class="wg-13-step">!</span>소유자 검토</a></div><div class="wg-13-path wg-13-path--ok"><span class="wg-13-edge">없음 → 진행</span><a href="#wg-13-s4" class="wg-13-node"><span class="wg-13-step">3</span>삭제 대기열 등록</a><span class="wg-13-arrow" aria-hidden="true">↓</span><a href="#wg-13-s5" class="wg-13-node wg-13-node--end"><span class="wg-13-step">완료</span>증빙 체크</a></div></div></div>
  </div>
  <div class="wg-13-detail"><h4 class="wg-13-dh">단계 상세 <span class="wg-13-dnote">실패 분기는 Troubleshooting 섹션과 연결</span></h4>
    <details id="wg-13-s1" class="wg-13-acc"><summary><span class="wg-13-tag">접수</span>삭제 범위와 고객 식별자 분리</summary><div class="wg-13-body"><p>지원 담당자는 고객이 요청한 범위가 계정 전체인지, 특정 워크스페이스인지, 로그 보존 제외인지 분리해 적는다. 범위가 모호하면 대기열 등록 대신 고객 재확인을 요청한다.</p></div></details>
    <details id="wg-13-s2" class="wg-13-acc"><summary><span class="wg-13-tag">확인</span>본인 확인과 권한 검증</summary><div class="wg-13-body"><p>본인 확인 상태가 green이어야 다음 단계로 이동한다. 대리 요청이면 위임 증빙이 티켓 첨부에 있어야 하며, 없으면 승인자에게 이관한다.</p></div></details>
    <details id="wg-13-s3" class="wg-13-acc"><summary><span class="wg-13-tag">판정</span>법적 보존·분쟁·보안 조사 확인</summary><div class="wg-13-body"><p>legal hold, chargeback, incident investigation 태그가 하나라도 있으면 즉시 STOP이다. STOP은 거절이 아니라 소유자 검토 전까지 삭제 실행을 잠그는 상태다.</p></div></details>
    <details id="wg-13-fail" class="wg-13-acc wg-13-acc--fail"><summary><span class="wg-13-tag wg-13-tag--fail">보류</span>소유자 검토로 전환</summary><div class="wg-13-body"><p>지원 담당자는 티켓 상태를 owner-review로 바꾸고 누락된 근거를 체크리스트로 남긴다. 운영자는 데이터 작업을 실행하지 않으며, 법무/보안 담당자 결정 전까지 고객 통지를 발송하지 않는다.</p></div></details>
    <details id="wg-13-s4" class="wg-13-acc"><summary><span class="wg-13-tag">등록</span>삭제 대기열과 감사 로그 생성</summary><div class="wg-13-body"><p>운영자는 deletion-job dry-run 결과와 대상 count를 티켓에 붙인다. 예상 count와 티켓 범위가 다르면 실행을 취소하고 Reference Extract의 원문 근거를 다시 확인한다.</p></div></details>
    <details id="wg-13-s5" class="wg-13-acc wg-13-acc--ok"><summary><span class="wg-13-tag wg-13-tag--ok">완료</span>완료 기준과 고객 통지 확인</summary><div class="wg-13-body"><p>삭제 작업 ID, 감사 로그 URL, 고객 통지 초안이 모두 있으면 첫 성공 경로가 닫힌다. 실제 실행은 Operations Runbook의 릴리스 전 점검을 통과한 뒤에만 진행한다.</p></div></details>
  </div>
</section>
'''

reader_toc = '''<span class="label">Reader Role Router · 필요한 섹션으로 바로 이동</span><p>역할별 첫 행동과 이관 기준을 먼저 찾고, 이후 레시피·트러블슈팅·감사 지적으로 내려갑니다.</p><div class="toc-pills"><a class="toc-pill" href="#source-version"><b>01</b>출처/버전</a><a class="toc-pill" href="#role-router"><b>02</b>역할 경로</a><a class="toc-pill" href="#first-success"><b>03</b>첫 성공</a><a class="toc-pill" href="#prerequisites-safety"><b>04</b>안전장치</a><a class="toc-pill" href="#task-recipes"><b>05</b>작업 레시피</a><a class="toc-pill" href="#reference-extract"><b>06</b>원문 추적</a><a class="toc-pill" href="#decision-guide"><b>07</b>진행/중단</a><a class="toc-pill" href="#troubleshooting"><b>08</b>복구</a><a class="toc-pill" href="#operations-runbook"><b>09</b>런북</a><a class="toc-pill" href="#manual-audit"><b>10</b>감사</a><a class="toc-pill" href="#next-actions"><b>11</b>다음 행동</a></div>'''

source_cards = '''
<div class="manual-reference-grid rail-cycle">
  <article class="manual-card mini-card"><span class="manual-label">FACT</span><h3>입력 원문 5종을 기준으로 재구성</h3><p>이번 파일은 고객 데이터 삭제 요청 처리에 필요한 내부 문서 5종을 하나의 실행 매뉴얼로 합친다. 입력 문서 밖의 실제 제품 버전, 법무 승인 상태, SLA 수치는 확인하지 않고 UNKNOWN으로 둔다.</p></article>
  <article class="manual-card mini-card"><span class="manual-label">OWNER</span><h3>지원·운영·법무/보안 책임 분리</h3><p>지원 담당자는 접수와 고객 커뮤니케이션을 맡고, 운영자는 dry-run과 실행 증빙을 맡는다. 법무/보안 소유자는 보존·분쟁·조사 조건을 판정해 STOP 해제 여부를 결정한다.</p></article>
  <article class="manual-card mini-card"><span class="manual-label">UNKNOWN</span><h3>승인 대기 항목을 실행 전 잠금</h3><p>보존 기간, 고객 통지 문구, deletion-job 권한 범위는 원문에 충분한 확정 정보가 없다. 이 항목은 다음 단계에서 소유자 검토가 끝나기 전까지 운영자가 실행 명령으로 옮기면 안 된다.</p></article>
</div>
'''

role_router = '''
<div class="manual-role-grid rail-cycle">
  <article class="manual-role mini-card"><span class="manual-label">Support</span><h3>고객 접수 담당자</h3><p>먼저 §03 첫 성공 경로의 본인 확인과 범위 분리를 수행한다. STOP 조건이 보이면 고객에게 완료 예정일을 약속하지 말고 §07 Decision Guide로 이관한다.</p><p>이관 기준은 본인 확인 실패, 요청 범위 불명확, 법적 보존 태그 확인, 대리 요청 증빙 누락이다.</p></article>
  <article class="manual-role mini-card"><span class="manual-label">Operator</span><h3>데이터 작업 운영자</h3><p>§05 Task Recipes의 dry-run과 감사 로그 생성만 먼저 실행한다. 실제 delete job은 §09 릴리스 전 점검과 소유자 승인 기록이 모두 붙은 뒤에만 허용된다.</p><p>대상 count가 티켓 범위와 다르면 실행자가 판단하지 않고 지원 담당자에게 범위 재확인을 요청한다.</p></article>
  <article class="manual-role mini-card"><span class="manual-label">Legal/Security</span><h3>보존·분쟁·조사 소유자</h3><p>§04 안전장치와 §07 중단 기준을 검토해 STOP 해제 여부를 기록한다. 해제 근거는 `legal-hold matrix §2` 또는 `security-investigation §4` 위치로 남긴다.</p><p>소유자 결정이 없으면 운영자는 삭제 명령을 실행하지 않는다. 이 원칙은 긴급 고객 요청보다 우선한다.</p></article>
</div>
'''

safety = '''
<div class="manual-audit-grid rail-cycle">
  <article class="manual-risk mini-card"><span class="manual-label">RISK</span><h3>법적 보존 태그</h3><p>고객 계정에 legal_hold=true가 있으면 삭제가 아니라 보존 검토 티켓으로 전환한다. 원문 `legal-hold-matrix.md §2`는 보존 해제 전 삭제 금지를 명시하지만, 해제 승인 양식은 비어 있어 UNKNOWN으로 남긴다.</p></article>
  <article class="manual-risk mini-card"><span class="manual-label">RISK</span><h3>결제 분쟁·환불 상태</h3><p>chargeback 또는 dispute 태그가 있으면 결제 증빙 보존 범위를 먼저 확인한다. 운영자는 고객 데이터 전체 삭제와 회계 로그 보존의 경계를 임의로 정하지 않는다.</p></article>
  <article class="manual-risk mini-card"><span class="manual-label">RISK</span><h3>보안 사고 조사</h3><p>security_investigation 태그가 있으면 삭제 요청을 incident owner에게 넘긴다. 조사 종료 여부가 원문에 없으면 완료 약속을 하지 않고 고객에게 검토 중 상태만 안내한다.</p></article>
  <article class="manual-safe mini-card"><span class="manual-label">SAFE</span><h3>dry-run 우선</h3><p>모든 삭제 job은 dry-run count와 대상 샘플 확인 후 실행한다. 이 단계는 고객 데이터 자체를 바꾸지 않지만, 대상 범위 오류를 가장 빨리 발견하는 안전장치다.</p></article>
</div>
'''

recipes = table(
    ['목적','사전조건','절차','완료 기준','롤백','원문 근거'],
    [
        ['요청 접수 표준화','본인 확인 상태 green 또는 위임 증빙 첨부','티켓에 고객 ID·요청 범위·채널·접수자를 분리 기록하고 `delete-request` 라벨을 붙인다.','범위·신원·요청일·소유자가 모두 티켓 필드로 남는다.','필드 누락 시 고객 재확인으로 되돌리며 삭제 큐 등록은 취소한다.','support/deletion-intake.md §1'],
        ['보존 조건 판정','legal_hold·dispute·security 태그 조회 권한','태그 3종을 조회하고 하나라도 true이면 STOP 상태와 소유자 검토 링크를 남긴다.','STOP/GO 판정과 담당 소유자가 같은 티켓에 기록된다.','STOP 오판은 삭제 큐 제거 후 owner-review 상태로 되돌린다.','legal-hold-matrix.md §2'],
        ['삭제 dry-run','운영자 권한과 대상 범위 확정','deletion-job을 dry-run으로 실행하고 대상 count, 제외 테이블, 감사 로그 초안을 첨부한다.','count가 요청 범위와 일치하고 제외 사유가 문장으로 설명된다.','dry-run은 데이터 변경이 없으므로 티켓 상태만 intake-review로 되돌린다.','ops/deletion-job-runbook.md §3'],
        ['고객 통지 발송','실행 완료 ID와 감사 로그 URL 존재','고객에게 삭제 완료 범위와 보존 제외 범위를 구분해 안내한다.','통지문에 완료 시간·제외 범위·문의 경로가 포함된다.','잘못 발송한 통지는 정정 메일을 보내고 incident note에 남긴다.','support/customer-notice.md §2'],
    ],
    'Task Recipes · 고객 데이터 삭제 요청 처리 6필드 표준 레시피'
)

reference_extract = f'''
{wg04}
<div class="source-note lede-note"><p><strong>목록 밖 정보 제한:</strong> 이 pilot은 아래 원문 묶음만 FACT로 취급합니다. 실제 프로덕션 버전, 법무 승인 양식, SLA, 지역별 보존 기간은 입력에 없으므로 본문에서 확정하지 않습니다.</p></div>
<ul class="col-list">
  <li><strong>support/deletion-intake.md §1</strong> — 접수 필드와 본인 확인 상태.</li>
  <li><strong>legal-hold-matrix.md §2</strong> — legal hold, dispute, security 조사 STOP 조건.</li>
  <li><strong>ops/deletion-job-runbook.md §3</strong> — dry-run, 대상 count, 실행 전 체크.</li>
  <li><strong>ops/audit-log-checklist.md §1</strong> — 작업 ID, 로그 URL, 승인자 기록.</li>
  <li><strong>support/customer-notice.md §2</strong> — 고객 통지 필드와 정정 절차.</li>
</ul>
'''

decision = '''
<div class="manual-reference-grid rail-cycle">
  <article class="manual-card mini-card"><span class="manual-label">GO</span><h3>진행 가능</h3><p>본인 확인이 완료되고, 요청 범위가 계정/워크스페이스/로그 예외로 구분되며, STOP 태그가 없을 때만 삭제 대기열 등록을 허용한다. 이때도 실제 실행은 dry-run과 감사 로그 준비 후로 제한한다.</p></article>
  <article class="manual-card mini-card"><span class="manual-label">STOP</span><h3>즉시 중단</h3><p>legal hold, dispute, security investigation, 대리 요청 증빙 누락 중 하나라도 있으면 production delete job 금지다. 담당자는 고객에게 완료일을 약속하지 않고 소유자 검토 상태를 안내한다.</p></article>
  <article class="manual-card mini-card"><span class="manual-label">ESCALATE</span><h3>이관 필수</h3><p>요청 범위와 dry-run count가 맞지 않거나, 보존 제외 범위를 고객에게 설명할 수 없으면 운영자가 해석하지 않는다. 지원 담당자와 법무/보안 소유자가 같은 티켓에서 판정을 남겨야 한다.</p></article>
</div>
'''

troubleshooting = '''
<div class="manual-trouble-grid rail-cycle">
  <article class="manual-trouble mini-card"><span class="manual-label">TROUBLE</span><h3>dry-run count가 요청 범위보다 크다</h3><p><strong>증상:</strong> deletion-job dry-run 대상이 티켓의 워크스페이스 수보다 많다. <strong>가능 원인:</strong> 고객 ID와 조직 ID를 혼동했거나 공유 리소스 포함 기준이 빠졌다.</p><p><strong>진단 순서:</strong> intake 필드, 대상 query, 제외 테이블을 순서대로 비교한다. <strong>복구:</strong> job을 실행하지 말고 티켓을 intake-review로 되돌린 뒤 범위를 재확인한다.</p></article>
  <article class="manual-trouble mini-card"><span class="manual-label">TROUBLE</span><h3>고객 통지와 감사 로그가 불일치한다</h3><p><strong>증상:</strong> 고객에게 안내한 완료 시간과 audit log의 작업 완료 시간이 다르다. <strong>가능 원인:</strong> 통지 초안을 먼저 발송했거나 재시도 job ID를 누락했다.</p><p><strong>진단 순서:</strong> audit log, notification draft, job retry history를 비교한다. <strong>복구:</strong> 정정 통지를 발송하고 incident note에 차이를 남긴다.</p></article>
  <article class="manual-trouble mini-card"><span class="manual-label">TROUBLE</span><h3>STOP 조건 해제 근거가 없다</h3><p><strong>증상:</strong> legal hold가 해제됐다고 말하지만 티켓에 승인자와 원문 위치가 없다. <strong>가능 원인:</strong> 슬랙 승인만 남고 문서 링크가 누락됐다.</p><p><strong>진단 순서:</strong> legal-hold matrix, 보안 조사 기록, 티켓 첨부를 확인한다. <strong>복구:</strong> 삭제 큐에서 제거하고 owner-review 상태로 되돌린다.</p></article>
</div>
'''

runbook = '''
<div class="manual-runbook-grid rail-cycle">
  <article class="manual-card mini-card"><span class="manual-label">Daily</span><h3>대기열과 STOP 티켓 점검</h3><p>매일 오전 삭제 대기열의 dry-run 미첨부 티켓과 STOP 해제 대기 티켓을 분리한다. 48시간 이상 소유자 응답이 없으면 고객 통지가 아니라 내부 이관 알림을 먼저 보낸다.</p></article>
  <article class="manual-card mini-card"><span class="manual-label">Weekly</span><h3>감사 로그 누락 점검</h3><p>주간 점검에서는 완료 티켓 중 job ID, audit URL, 고객 통지 링크가 빠진 항목을 찾는다. 누락이 2건 이상이면 레시피 교육이 아니라 절차 필드 자동화를 우선 검토한다.</p></article>
  <article class="manual-card mini-card"><span class="manual-label">Release</span><h3>삭제 job 변경 전 회귀 확인</h3><p>삭제 job query, 제외 테이블, 권한 정책이 바뀌면 dry-run fixture와 고객 통지 템플릿을 함께 검증한다. 쿼리만 통과하고 통지 문구가 뒤처지는 상태는 릴리스 금지다.</p></article>
</div>
'''

audit = '''
<div class="manual-audit-grid rail-cycle">
  <article class="manual-risk mini-card"><span class="manual-label">누락</span><h3>보존 해제 승인 양식 부재</h3><p>원문 `legal-hold-matrix.md §2`는 보존 조건은 제시하지만 해제 승인 양식의 필수 필드를 제공하지 않는다. 이 때문에 STOP 해제의 증빙 품질이 담당자마다 달라질 수 있다.</p></article>
  <article class="manual-risk mini-card"><span class="manual-label">모순</span><h3>고객 통지 시점의 표현 차이</h3><p>`customer-notice.md §2`는 실행 완료 후 통지라고 쓰지만, `deletion-job-runbook.md §3`은 dry-run 완료 후 고객 확인을 요구한다. 두 문서의 목적이 달라 보이므로 최종 통지와 사전 확인 문구를 분리해야 한다.</p></article>
  <article class="manual-unknown mini-card"><span class="manual-label">UNKNOWN</span><h3>SLA와 지역별 보존 기간 미확인</h3><p>입력 원문에는 고객에게 약속할 처리 기한과 지역별 법정 보존 기간이 없다. 매뉴얼 초안은 이를 확정하지 않고, 소유자 검토 항목으로 남긴다.</p></article>
</div>
'''

next_actions = '''
<h2 id="next-actions">''' + icon('check') + '''<span class="num is-key">12</span>Next Actions · 소유자 승인 전 마지막 잠금</h2>
<p class="h2-sub">이 매뉴얼은 실행 가능한 초안이지만, 실제 삭제 권한·법무 승인·고객 통지 문구는 소유자 확인이 끝나야 확정됩니다.</p>
<div class="card-grid rail-cycle">
  <article class="summary-card"><h3>1. STOP 해제 양식 확정</h3><p>법무/보안 소유자가 승인자, 승인 시각, 원문 위치, 해제 사유를 남기는 필수 필드를 정의한다. 이 양식이 없으면 삭제 큐 자동 등록을 열지 않는다.</p></article>
  <article class="summary-card"><h3>2. dry-run fixture 고정</h3><p>운영자는 정상 범위, 과대 범위, STOP 상태 계정 3개 fixture를 만들어 job 변경 때마다 실행한다. fixture 결과는 audit log checklist와 같은 티켓에 붙인다.</p></article>
  <article class="summary-card"><h3>3. 고객 통지 문구 분리</h3><p>사전 확인, 완료 통지, 정정 통지를 분리해 지원 담당자의 즉흥 문구를 줄인다. 보존 제외 범위는 법무 검토 문구를 그대로 사용한다.</p></article>
  <article class="summary-card"><h3>4. 첫 5건 운영 리허설</h3><p>실제 삭제 전 최근 5건을 대상으로 접수→판정→dry-run→통지 초안까지 리허설한다. 누락 필드가 반복되면 매뉴얼 보완보다 시스템 필드화를 먼저 한다.</p></article>
</div>
'''

slots = {
    'KICKER': 'MANUAL ANALYSIS · PHASE 2 PILOT',
    'TITLE': '고객 데이터 삭제 요청 운영 매뉴얼',
    'SUBTITLE': '지원·운영·법무/보안이 같은 티켓에서 삭제 요청을 접수, 판정, dry-run, 통지까지 안전하게 처리하도록 역할별 실행 경로와 중단 기준을 고정합니다.',
    'META': '<span>mode: manual_analysis</span><span>layout: manual-analysis.html</span><span>profile: auto</span><span>adaptive-html-final v%s</span><span>generated: 2026-06-14</span><span>no behavioral JS</span>' % version,
    'VERDICT': h2(1,'decision','Manual Verdict · 자동 삭제 금지, 증빙 우선 처리','삭제 요청은 고객 응대가 아니라 데이터·법무·보안 경계가 만나는 운영 절차입니다. 첫 화면에서 GO/STOP과 책임자를 먼저 분리합니다.') + hero_map,
    'READER_TOC': reader_toc,
    'SOURCE_VERSION': h2(2,'source','Source & Version · 원문 묶음과 확인 불가 항목','입력 원문, 소유자, 승인 상태를 분리해 실제 FACT와 UNKNOWN을 구분합니다.') + source_cards,
    'ROLE_ROUTER': h2(3,'user','Reader Role Router · 역할별 첫 행동','지원·운영·법무/보안 담당자가 처음 읽을 섹션과 이관 기준을 빠르게 찾습니다.') + role_router,
    'FIRST_SUCCESS': h2(4,'flow','First Success Path · 30분 안에 안전하게 대기열까지','처음 처리하는 담당자가 실제 삭제 실행 전까지 무엇을 완료해야 하는지 플로우로 고정합니다.') + wg13,
    'PREREQUISITES_SAFETY': h2(5,'security','Prerequisites & Safety · 실행 전 중단 조건','권한·보존·분쟁·조사 상태를 먼저 확인해 과삭제와 근거 없는 완료 약속을 막습니다.') + safety,
    'TASK_RECIPES': h2(6,'check','Task Recipes · 반복 작업 4종 6필드 표준','절차는 목적·사전조건·절차·완료 기준·롤백·원문 근거 6필드로만 발행합니다.') + recipes,
    'REFERENCE_EXTRACT': h2(7,'file','Reference Extract · 원문 추적 지도','어떤 문서가 어떤 판단에 쓰이는지 의존성 지도로 보여주고, 목록 밖 정보는 확정하지 않습니다.') + reference_extract,
    'DECISION_GUIDE': h2(8,'decision','Decision Guide · GO/STOP/ESCALATE 기준','담당자가 고객 압박이나 내부 편의로 실행 여부를 즉흥 판단하지 않도록 판정 질문과 이관 기준을 고정합니다.') + decision,
    'TROUBLESHOOTING': h2(9,'warning','Troubleshooting · 증상별 복구','문제가 발생했을 때 증상→가능 원인→진단 순서→복구의 4단 구조로 되돌립니다.') + troubleshooting,
    'OPERATIONS_RUNBOOK': h2(10,'timeline','Operations Runbook · 일일/주간/릴리스 전 점검','단건 처리 뒤에도 대기열, 감사 로그, job 변경을 주기적으로 점검해 운영 품질을 유지합니다.') + runbook,
    'MANUAL_AUDIT': h2(11,'audit','Manual Audit · 원문 자체의 결함과 보완 요청','매뉴얼이 실제 운영에 들어가기 전에 원문의 누락·모순·UNKNOWN을 소유자에게 되돌립니다.') + audit,
    'NEXT_ACTIONS': next_actions,
    'SOURCE_NOTE': '<p><strong>Source Limits:</strong> source snapshot 2026-06-14 · manual status: draft/owner review. 입력 원문은 support/deletion-intake.md, legal-hold-matrix.md, ops/deletion-job-runbook.md, ops/audit-log-checklist.md, support/customer-notice.md로 제한했습니다. 실제 제품 버전, 권한 정책, SLA, 지역별 법무 문구는 확인 불가(UNKNOWN)이며 소유자 검토 후 확정해야 합니다.</p>'
}

layout = read(ASSETS/'layouts/manual-analysis.html')
# Add official header generated-row/lens before meta while preserving layout skeleton.
layout = layout.replace('<div class="meta">{{META}}</div>', '<div class="generated-row"><p class="generated-date">source snapshot: 2026-06-14 · manual status: draft/owner review</p><div class="lens-strip"><span class="lens-strip-label">Lens</span><span class="lens-chip">Role</span><span class="lens-chip">Safety</span><span class="lens-chip">Troubleshooting</span></div></div><div class="meta">{{META}}</div>')
ids = {
    'manual-verdict':'manual-verdict','source-version':'source-version','role-router':'role-router','first-success':'first-success','prerequisites-safety':'prerequisites-safety','task-recipes':'task-recipes','reference-extract':'reference-extract','decision-guide':'decision-guide','troubleshooting':'troubleshooting','operations-runbook':'operations-runbook','manual-audit':'manual-audit','try':'next-actions'
}
for cls, idv in ids.items():
    layout = layout.replace(f'<section class="{cls}">', f'<section id="{idv}" class="{cls}">')
for k,v in slots.items():
    layout = layout.replace('{{'+k+'}}', v)
body = layout
footer = '<footer class="source-note"><p><strong>Generated by adaptive-html-final v%s.</strong> Phase 2 pilot output · profile=auto · official layout/vt/wg/body-icon assets read and recorded in sources/build-evidence.json.</p></footer>' % version

# CSS inline, verbatim. Core marker is first comment in style.
asset_text = {name: read(ASSETS/name) for name in INLINE}
core_css = '\n'.join(asset_text[name] for name in CORE)
core_hash = sha(core_css)
css_slots = {name: asset_text[name] for name in INLINE}
base = read(ASSETS/'base.html')
replacements = {
    'TITLE': slots['TITLE'],
    'DESCRIPTION': '고객 데이터 삭제 요청을 역할별 실행 매뉴얼로 재구성한 adaptive-html-final v5.10.4 Phase 2 pilot 산출물.',
    'THEME_CSS': '/* adaptive-html-final-core-css-sha256: %s */\n%s' % (core_hash, asset_text['theme.css']),
    'COMPONENTS_CSS': asset_text['components.css'],
    'VISUAL_COMPONENTS_CSS': asset_text['visual-components.css'],
    'WIDGETS_CSS': asset_text['widgets.css'],
    'VISUAL_HTML_CSS': asset_text['visual-html.css'],
    'BODY_ICONS_CSS': asset_text['body-icons.css'],
    'EDITORIAL_PATTERNS_CSS': asset_text['editorial-patterns.css'],
    'SHAPE_VISUALS_CSS': asset_text['shape-visuals.css'],
    'WORKFLOW_VISUALS_CSS': asset_text['workflow-visuals.css'],
    'LAYOUTS_CSS': asset_text['layouts.css'],
    'PRINT_CSS': asset_text['print.css'],
    'THEME_DARK_CSS': asset_text['theme-dark.css'],
    'JSON_LD_BLOCK': '',
    'BODY': body,
    'FOOTER': footer,
}
html = base
for k,v in replacements.items():
    html = html.replace('{{'+k+'}}', v)
html = re.sub(r'\n{4,}', '\n\n\n', html)
(OUT/'index.html').write_text(html, encoding='utf-8')

# Source artifacts.
(OUT/'sources/profile.json').write_text(json.dumps({'profile':'auto'}, ensure_ascii=False, indent=2), encoding='utf-8')
(OUT/'sources/adaptive-html-final-manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2)+"\n", encoding='utf-8')
for name in INLINE:
    shutil.copyfile(ASSETS/name, OUT/'sources/assets'/name)
asset_hashes = {name: sha(asset_text[name]) for name in INLINE}
css_integrity = {
    'profile':'auto',
    'core_css_sha256': core_hash,
    'asset_order': CORE,
    'conditional_asset_order': COND,
    'inline_order': INLINE,
    'asset_sha256': asset_hashes,
    'note': 'Phase 2 pilot generated from current skills/adaptive-html-final/assets; CSS in HTML is verbatim asset blocks.'
}
(OUT/'sources/css-integrity.json').write_text(json.dumps(css_integrity, ensure_ascii=False, indent=2)+"\n", encoding='utf-8')
evidence['html_sha256'] = hashlib.sha256((OUT/'index.html').read_bytes()).hexdigest()
(OUT/'sources/build-evidence.json').write_text(json.dumps(evidence, ensure_ascii=False, indent=2)+"\n", encoding='utf-8')
(OUT/'sources/fresh-generation-rule.json').write_text(json.dumps({'fresh_run': True, 'reused_previous_pages': False, 'mode_scope': 'manual_analysis', 'profile': 'auto'}, ensure_ascii=False, indent=2)+"\n", encoding='utf-8')
print(OUT)
print('core', core_hash)
