#!/usr/bin/env python3
# redroid UI 자동화(uiautomator2/ADB/FastAPI) 구현 매뉴얼 (manual_analysis 모드).
# 검증된 동일 모드 예제(16_manual_product_runbook.html)의 head+inlined CSS+테마바 셸을
# byte 그대로 재사용하고 <main>/<title>/description 만 교체한다(코어 해시·폭·테마 계약 보존).
import re, html, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[4]
SHELL = ROOT / "skills/adaptive-html-final/examples/16_manual_product_runbook.html"
OUT = pathlib.Path(__file__).resolve().parents[1] / "index.html"

def esc(s):
    return html.escape(s.strip("\n"), quote=False)

IC = {
 "shield": '<path class="bi-line" d="M14 27h12M16 32h8"/><path class="bi-soft" d="M20 7c-6 0-10 4.4-10 9.7 0 3.7 2 6.2 4.5 8.1h11c2.5-1.9 4.5-4.4 4.5-8.1C30 11.4 26 7 20 7z"/><circle class="bi-accent" cx="20" cy="16" r="3"/>',
 "file": '<rect class="bi-fill" x="10" y="7" width="20" height="26" rx="3"/><path class="bi-line" d="M15 14h10M15 20h10M15 26h7"/><path class="bi-accent-line" d="M27 7v8h-8"/>',
 "people": '<circle class="bi-soft" cx="20" cy="14" r="6"/><path class="bi-fill" d="M10 32c1.5-7 18.5-7 20 0"/><circle class="bi-accent" cx="28" cy="15" r="2"/>',
 "check": '<circle class="bi-soft" cx="20" cy="20" r="13"/><path class="bi-accent-line" d="M13 20l5 5 10-11"/>',
 "warn": '<path class="bi-soft" d="M20 7l14 25H6L20 7z"/><path class="bi-accent-line" d="M20 16v8"/><circle class="bi-accent" cx="20" cy="29" r="2"/>',
 "checklist": '<rect class="bi-fill" x="8" y="8" width="24" height="24" rx="4"/><path class="bi-accent-line" d="M14 20l4 4 9-10"/><path class="bi-line" d="M14 29h14"/>',
 "diamond": '<path class="bi-soft" d="M20 8l12 12-12 12L8 20z"/><path class="bi-line" d="M14 20h12"/><path class="bi-accent-line" d="M22 16l4 4-4 4"/>',
 "nodes": '<rect class="bi-fill" x="7" y="9" width="8" height="8" rx="2"/><rect class="bi-soft" x="25" y="9" width="8" height="8" rx="2"/><rect class="bi-fill" x="16" y="24" width="8" height="8" rx="2"/><path class="bi-line" d="M15 13h10M29 17l-9 7M11 17l9 7"/><circle class="bi-accent" cx="20" cy="28" r="2"/>',
 "search": '<rect class="bi-fill" x="9" y="7" width="18" height="25" rx="3"/><path class="bi-line" d="M14 14h8M14 20h7M14 26h6"/><circle class="bi-accent" cx="29" cy="26" r="4"/><path class="bi-accent-line" d="M32 29l4 4"/>',
}
def icon(k):
    return f'<span class="body-icon body-icon--sm"><svg viewBox="0 0 40 40" aria-hidden="true">{IC[k]}</svg></span>'

# ---------- 코드 블록 ----------
C_CHECK = r"""docker ps                       # redroid12 가 Up 인지
docker logs -f redroid12
adb connect 127.0.0.1:5555
adb devices                     # 127.0.0.1:5555    device"""

C_INSTALL = r"""adb install -r KakaoTalk.apk
adb shell monkey -p com.kakao.talk -c android.intent.category.LAUNCHER 1
scrcpy -s 127.0.0.1:5555        # 화면을 보며 직접 로그인"""

C_PYENV = r"""sudo apt update && sudo apt install -y python3 python3-venv python3-pip android-tools-adb
mkdir -p ~/kakao-bot && cd ~/kakao-bot
python3 -m venv .venv && source .venv/bin/activate
pip install -U pip uiautomator2
adb connect 127.0.0.1:5555 && adb devices"""

C_SIZE = r"""adb shell wm size               # 예: Physical size: 720x1280
# 입력창 예: x=280, y=1230  /  전송버튼 예: x=675, y=1230
# 좌표는 해상도·카카오톡 UI·키보드 표시 여부에 따라 달라진다."""

C_ADBINPUT = r"""# 영문/숫자 테스트
adb shell input tap 280 1230    # 입력창
adb shell input text "hello-test"
adb shell input tap 675 1230    # 전송 버튼
# 한글은 adb shell input text 에서 깨지는 경우가 많다 -> uiautomator2 권장"""

C_TESTDEV = r"""# test_device.py
import uiautomator2 as u2

d = u2.connect("127.0.0.1:5555")
print(d.info)
d.app_start("com.kakao.talk")    # 카카오톡이 redroid 안에서 뜨면 성공"""

C_SENDCUR = r'''# send_current_room.py  (현재 열려 있는 채팅방에 전송)
import sys, time
import uiautomator2 as u2

DEVICE = "127.0.0.1:5555"

def send_message(message: str):
    d = u2.connect(DEVICE)
    d.app_start("com.kakao.talk")
    time.sleep(1)

    # 입력창 탐색(버전마다 다를 수 있어 실패 시 좌표로 보정)
    edit = d(className="android.widget.EditText")
    if edit.exists(timeout=3):
        edit.click()
        edit.set_text(message)
    else:
        d.click(280, 1230)       # 하단 입력창 좌표
        time.sleep(0.3)
        d.send_keys(message)

    time.sleep(0.5)
    d.click(675, 1230)           # 전송 버튼(본인 화면에 맞게 조정)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("사용법: python send_current_room.py '보낼 메시지'")
        sys.exit(1)
    send_message(sys.argv[1])'''

C_SENDROOM = r'''# send_to_room.py  (채팅방 이름으로 찾아 들어가 전송)
import sys, time
import uiautomator2 as u2

DEVICE = "127.0.0.1:5555"

def send_to_room(room_name: str, message: str):
    d = u2.connect(DEVICE)
    d.app_start("com.kakao.talk")
    time.sleep(2)

    # 채팅 탭
    if d(text="채팅").exists(timeout=2):
        d(text="채팅").click()
        time.sleep(1)

    # 검색 진입(content-desc/text 가 환경마다 달라 좌표 보정 필요할 수 있음)
    if d(descriptionContains="검색").exists(timeout=2):
        d(descriptionContains="검색").click()
    elif d(textContains="검색").exists(timeout=2):
        d(textContains="검색").click()
    else:
        d.click(670, 80)         # 상단 검색 아이콘 예상 좌표

    time.sleep(1)

    # 검색어 입력
    search_input = d(className="android.widget.EditText")
    if search_input.exists(timeout=3):
        search_input.set_text(room_name)
    else:
        d.send_keys(room_name)

    time.sleep(1.5)

    # 검색 결과에서 방 클릭
    if d(textContains=room_name).exists(timeout=5):
        d(textContains=room_name).click()
    else:
        raise RuntimeError(f"채팅방을 찾지 못했습니다: {room_name}")

    time.sleep(1)

    # 메시지 입력 + 전송
    edit = d(className="android.widget.EditText")
    if edit.exists(timeout=3):
        edit.click()
        edit.set_text(message)
    else:
        d.click(280, 1230)
        d.send_keys(message)
    time.sleep(0.5)
    d.click(675, 1230)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("사용법: python send_to_room.py '채팅방이름' '메시지'")
        sys.exit(1)
    send_to_room(sys.argv[1], sys.argv[2])'''

C_SERVER = r'''# server.py  (FastAPI 웹훅 -> 현재 채팅방 전송)
import time
import uiautomator2 as u2
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

DEVICE = "127.0.0.1:5555"
app = FastAPI()

class SendRequest(BaseModel):
    room: str | None = None
    message: str

def send_current_room(message: str):
    d = u2.connect(DEVICE)
    d.app_start("com.kakao.talk")
    time.sleep(1)
    edit = d(className="android.widget.EditText")
    if edit.exists(timeout=3):
        edit.click(); edit.set_text(message)
    else:
        d.click(280, 1230); d.send_keys(message)
    time.sleep(0.5)
    d.click(675, 1230)

@app.post("/send")
def send(req: SendRequest):
    if not req.message.strip():
        raise HTTPException(status_code=400, detail="message is empty")
    try:
        send_current_room(req.message)   # 1차: 현재 열린 방에만 발송
        return {"ok": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))'''

C_UVICORN = r'''uvicorn server:app --host 127.0.0.1 --port 8080
# 테스트
curl -X POST http://127.0.0.1:8080/send \
  -H "Content-Type: application/json" \
  -d '{"message":"웹훅 자동 발송 테스트입니다"}' '''

C_CRON = r"""crontab -e
# 매일 09:00 "나와의 채팅"에 발송 (해당 방이 열려 있을 때 가장 안정적)
0 9 * * * cd /home/USER/kakao-bot && . .venv/bin/activate && python send_current_room.py "오늘 알림입니다" """

C_FAIL = r'''d.screenshot("failed.png")   # 실패 시 화면 저장(원인 추적용)'''

C_RES = r"""androidboot.redroid_width=720
androidboot.redroid_height=1280
androidboot.redroid_dpi=320      # 해상도 고정 -> 좌표 자동화가 덜 깨짐"""

def pre(c):
    return f'<pre class="code">{esc(c)}</pre>'

MAIN = f'''<main id="main" class="page-wide layout-manual">
  <header class="header manual-header">
    <div class="kicker"><span class="kicker-text">MANUAL · REDROID UI 자동화</span></div>
    <h1>redroid 카카오톡 UI 자동화 — uiautomator2로 메시지 자동 발송</h1>
    <p class="sub">카카오톡 공식 API가 아니라, redroid 안의 카카오톡 앱을 ADB·uiautomator2로 조작해 메시지를 자동 발송하는 방법을 — 역할별 경로·구현 레시피·문제 해결·운영 안정화로 재구성한 구현 매뉴얼입니다.</p>
    <div class="generated-row"><p class="generated-date">source snapshot: 사용자 제공 구현 문서 · 기반: Proxmox+redroid 구축 환경 · uiautomator2 / FastAPI</p><div class="lens-strip"><span class="lens-strip-label">Lens</span><span class="lens-chip">점진 구현</span><span class="lens-chip">보안(로컬)</span><span class="lens-chip">운영 안정성</span></div></div>
    <div class="meta"><span>mode: manual_analysis</span><span>layout: manual-analysis.html</span><span>profile: auto</span><span>adaptive-html-final v5.10.5</span><span>no behavioral JS</span></div>
  </header>

  <section class="manual-verdict"><h2>{icon("shield")}구현 결론</h2><p><strong>결론:</strong> 카카오톡 자동 발송은 공식 API가 아니라 <strong>redroid 안 카카오톡 앱을 ADB/uiautomator2로 조작</strong>하는 방식이 현실적입니다. 처음부터 "채팅방 검색 + 전송"을 만들지 말고, <strong>① 현재 열린 채팅방에 자동 전송</strong>부터 성공시킨 뒤 검색·큐·재시도·웹훅을 붙입니다. 발송 서버는 Ubuntu VM 안에서 <code>127.0.0.1:5555</code>로 redroid에 접속해 실행하고, ADB 포트는 인터넷에 직접 열지 않습니다.</p></section>

  <nav class="toc-map manual-reader-toc" aria-label="UI 자동화 매뉴얼 목차"><span class="label">Reader Role Router</span><p>역할(구현·운영·디버깅)에 따라 필요한 섹션으로 바로 이동합니다.</p><div class="toc-pills"><a class="toc-pill" href="#man-source"><b>1</b>도구 &amp; 구조</a><a class="toc-pill" href="#man-role"><b>2</b>역할별 경로</a><a class="toc-pill" href="#man-safety"><b>4</b>사전 준비·보안</a><a class="toc-pill" href="#man-task"><b>5</b>구현 레시피</a><a class="toc-pill" href="#man-trouble"><b>9</b>Troubleshooting</a></div></nav>

  <section class="source-version" id="man-source"><h2>{icon("file")}<span class="num is-key">1</span>도구 &amp; 권장 구조</h2><p class="h2-sub">자동화에 쓰는 도구와 발송 파이프라인을 먼저 고정합니다 — UI 자동화는 도구·해상도에 따라 동작이 달라지므로 구조를 앞에서 못 박습니다.</p><div class="manual-reference-grid"><article class="manual-card"><span class="manual-label">도구</span><h3>제어 스택</h3><p><strong>ADB</strong>(기기 제어), <strong>uiautomator2</strong>(Python에서 Android UI 조작), <strong>Appium UiAutomator2 드라이버</strong>(네이티브 앱 자동화), <strong>scrcpy</strong>(화면 미러링·수동 로그인). 한글 입력 안정성 때문에 핵심 조작은 uiautomator2로 합니다.</p></article><article class="manual-card"><span class="manual-label">권장 구조</span><h3>발송 서버</h3><p>Ubuntu VM 안에 <code>kakao-bot</code>(Python·ADB·uiautomator2·FastAPI/cron)를 두고, <code>127.0.0.1:5555</code> ADB로 redroid의 카카오톡을 조작합니다. 외부 노출 없이 VM 내부에서 도는 것이 가장 단순합니다.</p></article><article class="manual-card"><span class="manual-unknown">UNKNOWN</span><h3>확인 불가</h3><p>카카오톡 버전별 UI 셀렉터(텍스트·content-desc)와 입력창/전송 버튼 좌표는 환경마다 달라 설치 후 실측해야 합니다. 본문 좌표는 720×1280 예시값입니다.</p></article></div></section>

  <section class="role-router" id="man-role"><h2>{icon("people")}<span class="num">2</span>역할별 경로 · Reader Role Router</h2><p class="h2-sub">구현·운영·디버깅 역할마다 먼저 볼 섹션이 다릅니다 — 진입점을 고정합니다.</p><div class="manual-role-grid"><article class="manual-role"><h3>구현 개발자</h3><p>현재방 전송 → 채팅방 검색 → 웹훅 순으로 만듭니다. 권장 경로는 §3 첫 성공 → §5 구현 레시피이며, 좌표·셀렉터 판단은 §7을 참고합니다.</p></article><article class="manual-role"><h3>운영 담당자</h3><p>큐·로그·재시도·해상도 고정·systemd로 안정화합니다. 권장 경로는 §10 운영 안정화 → §5 R5(웹훅)·R6(cron)이며, 동시 발송은 반드시 큐로 직렬화합니다.</p></article><article class="manual-role"><h3>디버깅 담당자</h3><p>한글 입력·채팅방 탐색 실패·좌표 어긋남을 진단합니다. §9 Troubleshooting의 4단 구조를 따르고, 실패 시 스크린샷(§10)을 먼저 확보합니다.</p></article></div><div class="vt-shell"><div class="vt-shell-head"><div><div class="vt-id">VT-01 HERO MAP</div><h2>자동 발송 파이프라인</h2><p>외부 요청이 redroid 카카오톡 전송까지 가는 경로 — 각 단계가 다음 단계를 격리합니다.</p></div><span class="vt-fit">pipeline map</span></div><div class="vt-frame"><div class="hm-grid"><div class="hm-card"><h3>Trigger</h3><p>외부 웹앱 / cron → POST /send</p></div><div class="hm-card"><h3>Worker</h3><p>FastAPI → Queue → uiautomator2</p></div><div class="hm-card"><h3>Target</h3><p>redroid KakaoTalk (127.0.0.1:5555)</p></div></div><div class="hm-result"><b>운영형 목표</b><span>요청을 큐로 직렬화하고, 실패는 스크린샷·로그로 추적하며 재시도합니다.</span></div></div></div></section>

  <section class="first-success"><h2>{icon("check")}<span class="num">3</span>첫 성공 경로 · First Success Path</h2><p class="h2-sub">"현재 열린 채팅방에 한 줄을 자동 전송"하는 최단 경로 — 검색·큐·웹훅은 모두 그 다음입니다.</p><div class="manual-step-grid"><article class="manual-step"><span class="manual-safe">STEP 1</span><h3>연결 확인 + 로그인</h3><p>redroid 기동·ADB 연결을 확인하고 scrcpy로 카카오톡에 직접 로그인합니다. <strong>성공 기준:</strong> <code>adb devices</code>에 device, scrcpy에 카카오톡 화면.</p></article><article class="manual-step"><span class="manual-safe">STEP 2</span><h3>채팅방 수동 오픈</h3><p>"나와의 채팅"을 열어 입력창이 보이는 상태로 둡니다. <strong>성공 기준:</strong> 하단 입력창 노출. 사람이 방을 열어두고 스크립트는 입력·전송만 맡는 것이 가장 안정적입니다.</p></article><article class="manual-step"><span class="manual-safe">STEP 3</span><h3>Python으로 전송</h3><p>uiautomator2로 입력창을 찾아 메시지를 넣고 전송 버튼을 누릅니다. <strong>성공 기준:</strong> 채팅방에 메시지 도착. 실패하면 §9-A(한글)·§7(좌표)로 분기합니다.</p></article></div></section>

  <section class="prerequisites-safety" id="man-safety"><h2>{icon("warn")}<span class="num">4</span>사전 준비 · 보안 · Prerequisites &amp; Safety</h2><p class="h2-sub">자동화 전에 연결·로그인·Python 환경을 확정하고, ADB 노출 경고를 실행 앞에 둡니다.</p><h3>연결 상태 확인 + 카카오톡 설치/로그인</h3>{pre(C_CHECK)}{pre(C_INSTALL)}<h3>Python 환경(uiautomator2)</h3>{pre(C_PYENV)}<div class="manual-audit-grid"><article class="manual-card"><span class="manual-risk">보안 위험</span><h3>ADB 포트 노출 금지</h3><p>ADB 5555를 인터넷에 직접 열면 외부에서 접근 가능한 위험 서비스로 분류됩니다. 발송 서버는 VM 내부에서 <code>127.0.0.1:5555</code>로만 접속하고, 원격 접근이 필요하면 SSH 터널/VPN을 씁니다.</p></article><article class="manual-card"><span class="manual-risk">계정 위험</span><h3>반복·비정상 패턴</h3><p>가상 환경 로그인은 보호/재인증이 뜰 수 있고, 반복 발송은 계정 제한 사유가 될 수 있습니다. 먼저 "나와의 채팅"으로만 테스트합니다.</p></article><article class="manual-card"><span class="manual-unknown">UNKNOWN</span><h3>UI 변경</h3><p>카카오톡 업데이트 후 버튼 위치·텍스트·content-desc가 바뀔 수 있어 셀렉터/좌표는 깨질 수 있습니다. 좌표는 본인 화면에서 실측합니다.</p></article></div></section>

  <section class="task-recipes" id="man-task"><h2>{icon("checklist")}<span class="num">5</span>구현 레시피 · Task Recipes</h2><p class="h2-sub">구현 단위를 레시피로 식별하고, 각 레시피를 목적·사전조건·절차(코드)·완료 기준·롤백·근거로 닫습니다.</p><div class="vt-shell"><div class="vt-shell-head"><div><div class="vt-id">VT-05 CHECKLIST FLOW</div><h2>레시피 진행 체크</h2><p>현재방 전송이 통과해야 검색·웹훅으로 넘어갑니다.</p></div><span class="vt-fit">checklist flow</span></div><div class="vt-frame"><div class="cf"><div class="cf-item"><span class="cf-check" aria-hidden="true">✓</span><b>연결 테스트(R2)</b><span class="cf-state">PASS</span></div><div class="cf-item"><span class="cf-check" aria-hidden="true">✓</span><b>현재방 전송(R3)</b><span class="cf-state">PASS</span></div><div class="cf-item"><span class="cf-check" aria-hidden="true">✓</span><b>검색·웹훅(R4·R5)</b><span class="cf-state">NEXT</span></div></div></div></div><div class="tbl table-scroll mobile-card-table"><table class="table"><caption>구현 레시피 식별(절차는 아래 코드)</caption><thead><tr><th>레시피</th><th>목적</th><th>사전조건</th><th>완료 기준</th><th>롤백</th></tr></thead><tbody><tr><td data-label="레시피">R2 연결 테스트</td><td data-label="목적">uiautomator2 연결</td><td data-label="사전조건">Python 환경·adb</td><td data-label="완료 기준">카카오톡 app_start</td><td data-label="롤백">스크립트 제거</td></tr><tr><td data-label="레시피">R3 현재방 전송</td><td data-label="목적">열린 방에 발송</td><td data-label="사전조건">방 수동 오픈</td><td data-label="완료 기준">메시지 도착</td><td data-label="롤백">전송 중단</td></tr><tr><td data-label="레시피">R4 채팅방 검색 전송</td><td data-label="목적">방 이름으로 진입</td><td data-label="사전조건">R3 성공</td><td data-label="완료 기준">대상 방 도착</td><td data-label="롤백">현재방 방식 회귀</td></tr><tr><td data-label="레시피">R5 웹훅(FastAPI)</td><td data-label="목적">HTTP로 발송</td><td data-label="사전조건">R3 성공·로컬 바인딩</td><td data-label="완료 기준">200 OK + 도착</td><td data-label="롤백">서버 종료</td></tr><tr><td data-label="레시피">R6 정기 발송(cron)</td><td data-label="목적">스케줄 발송</td><td data-label="사전조건">방 열림 유지</td><td data-label="완료 기준">정시 도착</td><td data-label="롤백">crontab 제거</td></tr></tbody></table></div><h3>R2 — 연결 테스트</h3>{pre(C_TESTDEV)}<h3>R3 — 현재 열린 채팅방에 전송 (가장 안정적인 첫 단계)</h3>{pre(C_SENDCUR)}<p>실행: <code>python send_current_room.py "테스트 메시지입니다"</code></p><h3>R4 — 채팅방 이름으로 찾아 전송</h3>{pre(C_SENDROOM)}<p>실행: <code>python send_to_room.py "나와의 채팅" "자동 발송 테스트입니다"</code></p><h3>R5 — FastAPI 웹훅</h3><p>설치: <code>pip install fastapi uvicorn</code>. 외부 시스템이 HTTP로 호출하면 발송됩니다(1차는 현재 열린 방에만).</p>{pre(C_SERVER)}{pre(C_UVICORN)}<h3>R6 — cron 정기 발송</h3>{pre(C_CRON)}</section>

  <section class="reference-extract"><h2>{icon("file")}<span class="num">6</span>참조 근거 · Reference Extract</h2><p class="h2-sub">각 도구의 역할 근거를 분리해 둬야 UI/버전 변경 시 추적이 됩니다.</p><p>본문 절차는 아래 도구·문서 근거에 기반합니다. 이 목록에 없는 정보(정확한 셀렉터, 카카오톡 버전 동작)는 본문에 단정으로 등장하지 않습니다.</p><ul class="col-list"><li>uiautomator2 — Python에서 Android UI 자동 조작</li><li>Appium UiAutomator2 드라이버 — 네이티브 앱 자동화</li><li>scrcpy — Android 화면 미러링·키보드/마우스 제어</li><li>redroid — Linux host에서 다중 Android 인스턴스</li><li>ADB 포트 노출 — 외부 접근 가능 위험 서비스</li></ul></section>

  <section class="decision-guide"><h2>{icon("diamond")}<span class="num">7</span>선택 기준 · Decision Guide</h2><p class="h2-sub">입력 방식·방 진입·발송 모델을 무엇으로 고를지 정리합니다 — 단순한 쪽부터 시작합니다.</p><div class="manual-reference-grid"><article class="manual-card"><h3>입력: ADB vs uiautomator2</h3><p>영문/숫자만이면 <code>adb shell input</code>도 되지만, <strong>한글은 깨지기 쉬워 uiautomator2의 set_text</strong>를 씁니다. 좌표 확인은 <code>adb shell wm size</code>로.</p></article><article class="manual-card"><h3>방 진입: 현재방 vs 검색</h3><p><strong>현재방 전송이 1순위</strong>(사람이 열어둠 → 가장 안정). 검색 자동화(R4)는 셀렉터가 깨질 위험이 있어 현재방이 통과한 뒤 추가합니다.</p></article><article class="manual-card"><h3>발송: 동기 vs 큐</h3><p>요청이 한 번에 여러 개면 UI가 꼬입니다. <strong>큐(SQLite/Redis)에 쌓고 Worker가 1개씩 순차 처리</strong>합니다. 동시 발송은 피합니다.</p></article></div><h3>좌표 확인(필요 시)</h3>{pre(C_SIZE)}{pre(C_ADBINPUT)}</section>

  <section class="troubleshooting" id="man-trouble"><h2>{icon("warn")}<span class="num">8</span>Troubleshooting · 증상별 문제 해결</h2><p class="h2-sub">증상 → 가능 원인 → 진단 순서 → 복구의 4단 구조를 고정합니다 — UI 자동화는 진단 없이 좌표부터 만지면 더 깨집니다.</p><div class="manual-trouble-grid"><article class="manual-trouble manual-trouble-scenario"><h3>A. 한글이 입력되지 않음/깨짐</h3><p><strong>증상:</strong> 영문은 들어가는데 한글이 빈칸이거나 깨짐.</p><p><strong>가능 원인:</strong> <code>adb shell input text</code>의 한글 미지원, IME 미설정.</p><p><strong>진단 순서:</strong> 영문 입력 정상 여부 → uiautomator2 <code>set_text</code> 대체 가능 여부 확인.</p><p><strong>복구:</strong> ADB input 대신 uiautomator2 <code>edit.set_text(message)</code>를 사용합니다(§5 R3).</p></article><article class="manual-trouble manual-trouble-scenario"><h3>B. 채팅방을 찾지 못함</h3><p><strong>증상:</strong> <code>send_to_room.py</code>가 RuntimeError(채팅방 못 찾음).</p><p><strong>가능 원인:</strong> 검색 아이콘 content-desc 변경, 방 이름 부분 불일치, 로딩 지연.</p><p><strong>진단 순서:</strong> 채팅 탭 진입 여부 → 검색창 노출 → <code>textContains</code> 매칭 → 대기 시간.</p><p><strong>복구:</strong> 검색 좌표를 실측 보정하고 <code>time.sleep</code>를 늘리거나, 안정화 전까지 현재방 전송(R3)으로 회귀합니다.</p></article><article class="manual-trouble manual-trouble-scenario"><h3>C. 좌표가 어긋나 엉뚱한 곳 클릭</h3><p><strong>증상:</strong> 입력/전송이 빈 곳을 누름.</p><p><strong>가능 원인:</strong> 해상도/DPI 변경, 키보드 표시 여부에 따른 좌표 이동.</p><p><strong>진단 순서:</strong> <code>adb shell wm size</code> → 키보드 상태 → 현재 좌표 비교.</p><p><strong>복구:</strong> redroid 해상도를 고정(§10)하고 좌표 대신 가능한 한 UI 셀렉터(EditText)를 우선합니다.</p></article><article class="manual-trouble manual-trouble-scenario"><h3>D. 동시 요청에 UI가 꼬임</h3><p><strong>증상:</strong> 여러 요청이 겹치면 다른 방에 발송되거나 멈춤.</p><p><strong>가능 원인:</strong> 단일 UI를 동시 조작, 앱 상태 경합.</p><p><strong>진단 순서:</strong> 동시 요청 수 → 큐 유무 → Worker 동시성 확인.</p><p><strong>복구:</strong> 큐에 저장하고 Worker가 1건씩 순차 처리하도록 직렬화합니다(§10).</p></article></div></section>

  <section class="operations-runbook"><h2>{icon("nodes")}<span class="num">9</span>운영 안정화 · Operations Runbook</h2><p class="h2-sub">자동화는 "되는 것"보다 "안 깨지게 운영하는 것"이 어렵습니다 — 단계적 테스트·큐·로그·해상도 고정이 핵심입니다.</p><div class="manual-runbook-grid"><article class="manual-card"><h3>단계적 테스트</h3><p>바로 사람에게 보내지 말고 ① 나와의 채팅 → ② 테스트 1:1 → ③ 내부 테스트방 → ④ 실제 운영 순으로 올립니다.</p></article><article class="manual-card"><h3>큐 + 로그</h3><p>요청을 SQLite/Redis 큐에 저장하고 Worker가 1건씩 처리합니다. 발송시각·방명·메시지 일부·성공/실패·실패 사유·스크린샷 경로를 남깁니다.</p></article><article class="manual-card"><h3>좌표 고정 + 서비스화</h3><p>redroid 해상도를 고정해 좌표 자동화가 덜 깨지게 하고, 최종에는 systemd 서비스로 올려 자동 재시작·로그를 확보합니다.</p></article></div><h3>실패 스크린샷 / 해상도 고정</h3>{pre(C_FAIL)}{pre(C_RES)}</section>

  <section class="manual-audit"><h2>{icon("search")}<span class="num">10</span>중요한 한계 · 감사</h2><p class="h2-sub">UI 자동화는 공식 발송 API가 아니므로 구조적 한계를 원인과 함께 기록합니다 — 메인 계정 상시 운영은 권장하지 않습니다.</p><div class="tbl table-scroll mobile-card-table"><table class="table"><caption>redroid UI 자동화의 한계</caption><thead><tr><th>문제</th><th>설명</th></tr></thead><tbody><tr><td data-label="문제">UI 변경</td><td data-label="설명">카카오톡 업데이트로 버튼 위치·텍스트가 바뀔 수 있음</td></tr><tr><td data-label="문제">한글 입력</td><td data-label="설명">ADB 기본 입력은 한글이 불안정 → uiautomator2 사용</td></tr><tr><td data-label="문제">로그인 유지</td><td data-label="설명">가상 환경이라 계정 보호·재인증이 뜰 수 있음</td></tr><tr><td data-label="문제">알림/푸시</td><td data-label="설명">GMS/FCM 미구성 시 푸시가 불안정</td></tr><tr><td data-label="문제">계정 제한</td><td data-label="설명">반복·비정상 발송 패턴은 제한될 수 있음</td></tr><tr><td data-label="문제">다중 요청</td><td data-label="설명">동시에 보내면 UI 상태가 꼬임 → 큐 직렬화</td></tr></tbody></table></div><div class="wg-13-fc"><h3 class="wg-13-h">추천 구현 순서 <span class="wg-13-sub">단순 → 운영형</span></h3><div class="wg-13-flow"><a class="wg-13-node wg-13-node--start" href="#man-task"><span class="wg-13-step">START</span>현재방 전송</a><span class="wg-13-arrow" aria-hidden="true">↓</span><a class="wg-13-node wg-13-node--decide" href="#man-task"><span class="wg-13-step">ADD</span>검색 + 웹훅</a><span class="wg-13-arrow" aria-hidden="true">↓</span><a class="wg-13-node wg-13-node--end" href="#man-trouble"><span class="wg-13-step">OPS</span>큐·로그·재시도</a></div></div></section>

  <section class="try"><h2>{icon("checklist")}<span class="num">11</span>Next Actions · 추천 구현 순서</h2><p>처음부터 완전 자동화하지 말고 아래 순서로, 각 단계가 통과한 뒤 다음을 붙입니다. 운영형으로 가면 FastAPI → Queue → Sender Worker → uiautomator2 → redroid KakaoTalk → 로그/스크린샷/재시도 구조가 됩니다.</p><ol><li>redroid에 카카오톡 설치 → 로그인 → scrcpy로 수동 발송 확인</li><li>채팅방을 열어둔 상태에서 Python(uiautomator2)으로 입력/전송(R3)</li><li>실패 시 스크린샷 저장 → 채팅방 검색 자동화(R4) 추가</li><li>FastAPI 웹훅(R5) → cron 정기 발송(R6) 연결</li><li>큐·로그·재시도 추가 → systemd 서비스화</li></ol></section>

  <aside class="source-note"><strong>Source Limits:</strong> 이 매뉴얼은 사용자 제공 구현 문서를 역할별 실행 문서로 재구성한 것입니다. redroid UI 자동화는 카카오톡 공식 API가 아니며, UI 셀렉터·좌표·계정 정책·푸시 동작은 카카오톡 버전과 환경에 따라 달라져 확인 불가/UNKNOWN으로 둡니다. 반복·대량 발송은 계정 제한 사유가 될 수 있으므로 "나와의 채팅" 테스트부터 단계적으로 진행하고, 자동화 사용은 본인 책임 범위에서 합니다.</aside>
</main>'''

shell = SHELL.read_text(encoding="utf-8")
shell = re.sub(r'<main id="main".*?</main>', lambda m: MAIN, shell, count=1, flags=re.S)
shell = shell.replace("<title>Manual Analysis · 제품 운영 매뉴얼</title>",
                      "<title>redroid 카카오톡 UI 자동화 매뉴얼 (uiautomator2·FastAPI)</title>")
shell = shell.replace('<meta name="description" content="">',
                      '<meta name="description" content="redroid 안의 카카오톡 앱을 ADB·uiautomator2로 조작해 메시지를 자동 발송하는 구현 매뉴얼 — 현재방 전송부터 채팅방 검색·FastAPI 웹훅·cron·큐/로그/재시도 운영화까지.">')
OUT.write_text(shell, encoding="utf-8")
print("wrote", OUT, len(shell), "bytes | main swapped:", "구현 결론" in shell)
