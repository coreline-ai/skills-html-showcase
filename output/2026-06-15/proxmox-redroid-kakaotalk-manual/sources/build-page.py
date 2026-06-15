#!/usr/bin/env python3
# Proxmox + redroid 카카오톡 구축 매뉴얼 페이지 빌더 (manual_analysis 모드).
# 동일 모드 검증 예제(16_manual_product_runbook.html)의 head+inlined CSS+테마바 셸을
# byte 그대로 재사용하고 <main>/<title>/description 만 교체한다(코어 해시·폭·테마 계약 보존).
import re, html, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[4]
SHELL = ROOT / "skills/adaptive-html-final/examples/16_manual_product_runbook.html"
OUT = pathlib.Path(__file__).resolve().parents[1] / "index.html"

def esc(s):  # 코드/텍스트 HTML 이스케이프
    return html.escape(s.strip("\n"), quote=False)

# ---- body-icon SVG (assets/body-icons.json 정본, viewBox 0 0 40 40) ----
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

# ---- 코드 블록(원문 명령) ----
C_BASE = r"""sudo apt update && sudo apt upgrade -y
sudo apt install -y ca-certificates curl gnupg lsb-release vim unzip git \
  android-tools-adb android-tools-fastboot"""

C_DOCKER = r"""# 충돌 패키지 제거 후 Docker 공식 저장소 등록
sudo apt remove -y docker.io docker-compose podman-docker containerd runc || true
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc
sudo tee /etc/apt/sources.list.d/docker.sources <<EOF
Types: deb
URIs: https://download.docker.com/linux/ubuntu
Suites: $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}")
Components: stable
Architectures: $(dpkg --print-architecture)
Signed-By: /etc/apt/keyrings/docker.asc
EOF
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
sudo docker run hello-world           # 동작 확인
sudo usermod -aG docker $USER && newgrp docker   # (선택) 그룹 추가"""

C_KERNEL = r"""# binder/ashmem 등 redroid 필수 커널 기능 로드
sudo apt install -y linux-modules-extra-$(uname -r)
sudo modprobe binder_linux devices="binder,hwbinder,vndbinder"
sudo modprobe ashmem_linux || true     # 최신 커널은 memfd 사용 가능
lsmod | grep binder                    # 로드 확인

# 재부팅 후 자동 로드
echo "binder_linux" | sudo tee /etc/modules-load.d/redroid.conf
echo 'options binder_linux devices="binder,hwbinder,vndbinder"' \
  | sudo tee /etc/modprobe.d/redroid.conf"""

C_RUN = r"""sudo mkdir -p /opt/redroid/data && sudo chmod 777 /opt/redroid/data

# ADB 5555는 127.0.0.1 로만 바인딩(외부 노출 금지)
docker run -itd --name redroid12 --privileged --restart unless-stopped --pull always \
  -v /opt/redroid/data:/data \
  -p 127.0.0.1:5555:5555 \
  redroid/redroid:12.0.0_64only-latest \
  androidboot.redroid_width=720 \
  androidboot.redroid_height=1280 \
  androidboot.redroid_dpi=320 \
  androidboot.redroid_gpu_mode=guest

docker ps && docker logs -f redroid12"""

C_ADB = r"""# 로컬 PC에서 SSH 터널을 먼저 연다(포트를 인터넷에 직접 열지 않는다)
ssh -L 5555:127.0.0.1:5555 user@UBUNTU_VM_IP

# 다른 터미널에서 연결 + 화면
adb connect 127.0.0.1:5555
adb devices                 # 127.0.0.1:5555  device
scrcpy -s 127.0.0.1:5555"""

C_KAKAO = r"""# 단일 APK
adb install -r KakaoTalk.apk
# split APK( base + split_config.* )인 경우
adb install-multiple base.apk split_config.*.apk
# 실행 (패키지 ID: com.kakao.talk)
adb shell monkey -p com.kakao.talk -c android.intent.category.LAUNCHER 1"""

C_OPS = r"""docker stop redroid12        # 중지
docker start redroid12       # 시작
docker restart redroid12     # 재시작
docker logs -f redroid12     # 로그
adb shell                    # Android 셸
docker exec -it redroid12 sh # 컨테이너 셸"""

C_BACKUP = r"""# 백업 (컨테이너 중지 후)
docker stop redroid12
sudo tar -czvf redroid-data-backup.tar.gz /opt/redroid/data
docker start redroid12

# 복원
docker stop redroid12
sudo rm -rf /opt/redroid/data && sudo mkdir -p /opt/redroid/data
sudo tar -xzvf redroid-data-backup.tar.gz -C /
docker start redroid12"""

C_DIAG_CT = r"""docker logs redroid12
dmesg -T | tail -100
lsmod | grep binder"""

C_DIAG_ADB = r"""docker ps && ss -lntp | grep 5555
adb kill-server && adb start-server
adb connect 127.0.0.1:5555"""

C_DIAG_KAKAO = r"""adb shell pm list packages | grep kakao
adb shell logcat | grep -i kakao"""

C_FINAL = r"""# Ubuntu VM
ssh user@UBUNTU_VM_IP
docker logs -f redroid12

# 로컬 PC
ssh -L 5555:127.0.0.1:5555 user@UBUNTU_VM_IP
adb connect 127.0.0.1:5555
scrcpy -s 127.0.0.1:5555
adb install -r KakaoTalk.apk
adb shell monkey -p com.kakao.talk -c android.intent.category.LAUNCHER 1"""

def pre(code):
    return f'<pre class="code">{esc(code)}</pre>'

MAIN = f'''<main id="main" class="page-wide layout-manual">
  <header class="header manual-header">
    <div class="kicker"><span class="kicker-text">MANUAL · PROXMOX + REDROID</span></div>
    <h1>Proxmox + redroid로 카카오톡 실행 환경 구축하기</h1>
    <p class="sub">Proxmox VE 위에 Ubuntu VM을 올리고, 그 안에서 Docker 기반 Android 컨테이너 redroid를 실행해 ADB·scrcpy로 카카오톡을 설치·원격 제어하는 전체 절차를 — 역할별 경로·작업 레시피·문제 해결·운영 런북으로 재구성한 구축 매뉴얼입니다.</p>
    <div class="generated-row"><p class="generated-date">source snapshot: 사용자 제공 구축 문서 · 기준 이미지: redroid 12.0.0_64only / Ubuntu Server 22.04~24.04</p><div class="lens-strip"><span class="lens-strip-label">Lens</span><span class="lens-chip">VM 격리</span><span class="lens-chip">보안(ADB 터널)</span><span class="lens-chip">Troubleshooting</span></div></div>
    <div class="meta"><span>mode: manual_analysis</span><span>layout: manual-analysis.html</span><span>profile: auto</span><span>adaptive-html-final v5.10.5</span><span>no behavioral JS</span></div>
  </header>

  <section class="manual-verdict"><h2>{icon("shield")}구축 결론</h2><p><strong>결론:</strong> Proxmox에 redroid를 직접 넣지 말고 <strong>Proxmox → Ubuntu VM → Docker → redroid → KakaoTalk</strong> 계층으로 올리는 구성이 가장 안정적입니다. VM으로 격리하면 Proxmox 스냅샷·백업을 그대로 쓸 수 있고, redroid 장애가 호스트에 미치는 영향을 줄입니다. ADB 5555 포트는 인터넷에 직접 열지 말고 <strong>LAN/VPN/SSH 터널 안에서만</strong> 사용합니다.</p></section>

  <nav class="toc-map manual-reader-toc" aria-label="구축 매뉴얼 목차"><span class="label">Reader Role Router</span><p>역할(처음 구축·운영·문제 해결)에 따라 필요한 섹션으로 바로 이동합니다.</p><div class="toc-pills"><a class="toc-pill" href="#man-source"><b>1</b>구성 &amp; 버전</a><a class="toc-pill" href="#man-role"><b>2</b>역할별 경로</a><a class="toc-pill" href="#man-safety"><b>4</b>사전조건·보안</a><a class="toc-pill" href="#man-task"><b>5</b>작업 레시피</a><a class="toc-pill" href="#man-trouble"><b>9</b>Troubleshooting</a></div></nav>

  <section class="source-version" id="man-source"><h2>{icon("file")}<span class="num is-key">1</span>구성 &amp; 버전 스냅샷</h2><p class="h2-sub">구축 대상과 권장 이미지 버전을 맨 앞에서 고정합니다 — redroid는 이미지 버전에 따라 동작이 달라지므로 버전 명시가 중요합니다.</p><div class="manual-reference-grid"><article class="manual-card"><span class="manual-label">구성요소</span><h3>스택</h3><p><strong>Proxmox VE</strong>(KVM VM·LXC 통합 가상화) 위 <strong>Ubuntu Server VM</strong>, 그 안에 <strong>Docker Engine</strong>, 그 위에 <strong>redroid</strong>(Linux에서 Android 인스턴스를 띄우는 Android-in-Cloud 컨테이너)와 <strong>KakaoTalk APK</strong>.</p></article><article class="manual-card"><span class="manual-label">권장 버전</span><h3>이미지</h3><p>Ubuntu Server <strong>22.04 / 24.04</strong>, redroid 이미지는 Android 8.1~16이 제공되지만 첫 구축은 공식 예제에 자주 쓰이는 <code>redroid/redroid:12.0.0_64only-latest</code>(Android 12 64bit)로 시작합니다.</p></article><article class="manual-card"><span class="manual-unknown">UNKNOWN</span><h3>확인 불가</h3><p>카카오톡 APK의 정확한 버전·split 구성, GMS 의존 기능(FCM 푸시 등)의 동작 여부는 실제 설치 전 확정할 수 없습니다. Source Limits에 두고 설치 후 확인합니다.</p></article></div></section>

  <section class="role-router" id="man-role"><h2>{icon("people")}<span class="num">2</span>역할별 경로 · Reader Role Router</h2><p class="h2-sub">같은 문서라도 역할마다 먼저 읽을 섹션이 다릅니다 — 역할별 진입점을 고정합니다.</p><div class="manual-role-grid"><article class="manual-role"><h3>처음 구축하는 사람</h3><p>VM 생성 → Docker → redroid 실행까지 한 번 성공하는 것이 목표. 권장 경로는 §3 첫 성공 경로 → §5 작업 레시피이며, 운영·백업 섹션은 첫 성공 이후로 미뤄도 됩니다.</p></article><article class="manual-role"><h3>운영 / 관리자</h3><p>보안(ADB 노출 금지)·커널 모듈·백업을 우선 확인. 권장 경로는 §4 사전조건·보안 → §10 운영 런북 → §5 레시피이며, 위험 작업 전 §4의 경고를 먼저 봅니다.</p></article><article class="manual-role"><h3>문제 해결 담당</h3><p>컨테이너·ADB·scrcpy·카카오톡 증상별로 진단합니다. §9 Troubleshooting의 4단 구조(증상→가능 원인→진단→복구)를 그대로 따르고, GPU/버전 선택은 §8을 참고합니다.</p></article></div><div class="vt-shell"><div class="vt-shell-head"><div><div class="vt-id">VT-01 HERO MAP</div><h2>구축 아키텍처 스택</h2><p>물리 서버부터 카카오톡까지의 계층 — 각 계층이 아래 계층을 격리합니다.</p></div><span class="vt-fit">stack map</span></div><div class="vt-frame"><div class="hm-grid"><div class="hm-card"><h3>Host</h3><p>물리 서버/미니PC + Proxmox VE</p></div><div class="hm-card"><h3>Guest</h3><p>Ubuntu Server VM + Docker Engine</p></div><div class="hm-card"><h3>App</h3><p>redroid Android 컨테이너 + KakaoTalk</p></div></div><div class="hm-result"><b>권장 구조</b><span>VM 격리로 Proxmox 스냅샷·백업 활용, redroid 장애의 호스트 영향 최소화.</span></div></div></div></section>

  <section class="first-success"><h2>{icon("check")}<span class="num">3</span>첫 성공 경로 · First Success Path</h2><p class="h2-sub">처음 구축자가 "되는 상태"를 한 번 경험하는 최단 3단계 — 각 단계에 성공 기준과 실패 분기를 붙입니다.</p><div class="manual-step-grid"><article class="manual-step"><span class="manual-safe">STEP 1</span><h3>Ubuntu VM + SSH</h3><p>Proxmox에서 q35·CPU host·4 Core·8GB·64GB·VirtIO(vmbr0)로 Ubuntu VM을 만들고 설치 중 OpenSSH를 켭니다. <strong>성공 기준:</strong> <code>ssh user@UBUNTU_VM_IP</code> 접속. 실패 시 네트워크 브리지·고정 IP를 먼저 확인합니다.</p></article><article class="manual-step"><span class="manual-safe">STEP 2</span><h3>Docker + 커널 + redroid</h3><p>Docker Engine 설치 → binder/ashmem 커널 모듈 로드 → redroid 컨테이너 실행. <strong>성공 기준:</strong> <code>docker ps</code>에 redroid12가 Up. 컨테이너가 바로 죽으면 §9-A(커널 모듈) 분기로 갑니다.</p></article><article class="manual-step"><span class="manual-safe">STEP 3</span><h3>ADB + scrcpy + 카카오톡</h3><p>SSH 터널 → <code>adb connect</code> → <code>scrcpy</code>로 화면을 띄우고 카카오톡 APK를 설치합니다. <strong>성공 기준:</strong> scrcpy 화면에 카카오톡 초기 화면. 검은 화면이면 §9-C(GPU 모드)로 갑니다.</p></article></div></section>

  <section class="prerequisites-safety" id="man-safety"><h2>{icon("warn")}<span class="num">4</span>사전조건 · 보안 · Prerequisites &amp; Safety</h2><p class="h2-sub">되돌리기 어려운 노출/권한 작업일수록 절차보다 "하기 전 조건"이 중요합니다 — 보안 경고를 실행 앞에 둡니다.</p><div class="tbl table-scroll mobile-card-table"><table class="table"><caption>권장 사양</caption><thead><tr><th>항목</th><th>권장값</th></tr></thead><tbody><tr><td data-label="항목">Proxmox 서버 CPU</td><td data-label="권장값">Intel/AMD x86_64</td></tr><tr><td data-label="항목">VM OS</td><td data-label="권장값">Ubuntu Server 22.04 / 24.04</td></tr><tr><td data-label="항목">VM CPU</td><td data-label="권장값">4 Core 이상</td></tr><tr><td data-label="항목">VM RAM</td><td data-label="권장값">6~8GB 이상</td></tr><tr><td data-label="항목">VM Disk</td><td data-label="권장값">64GB 이상</td></tr><tr><td data-label="항목">Network</td><td data-label="권장값">Bridge, 고정 IP 권장</td></tr><tr><td data-label="항목">접속 도구</td><td data-label="권장값">ADB, scrcpy</td></tr><tr><td data-label="항목">Android 이미지</td><td data-label="권장값">redroid Android 12 또는 14 64bit</td></tr></tbody></table></div><div class="manual-audit-grid"><article class="manual-card"><span class="manual-risk">보안 위험</span><h3>ADB 포트 노출 금지</h3><p>ADB 5555를 인터넷에 직접 열면 redroid 컨테이너나 호스트 OS가 침해될 수 있습니다(공식 경고). 반드시 <code>-p 127.0.0.1:5555:5555</code> 로컬 바인딩 + SSH 터널로만 접근합니다.</p></article><article class="manual-card"><span class="manual-risk">권한/커널</span><h3>privileged + 커널 모듈</h3><p>redroid는 <code>--privileged</code>와 Binder IPC, ashmem/memfd, IPv6, DMA-BUF 등 커널 기능이 필요합니다. <code>binder_linux</code> 미로드 상태로 실행하면 컨테이너가 즉시 종료됩니다.</p></article><article class="manual-card"><span class="manual-unknown">UNKNOWN</span><h3>가상환경 탐지</h3><p>카카오톡이 SIM 없음·GMS 없음·가상 환경을 탐지하거나 새 기기 로그인으로 보안 인증을 요구할 수 있습니다. 동작 여부는 설치 후에만 확인 가능합니다.</p></article></div></section>

  <section class="task-recipes" id="man-task"><h2>{icon("checklist")}<span class="num">5</span>작업 레시피 · Task Recipes</h2><p class="h2-sub">구축에 필요한 작업을 레시피로 식별하고, 각 레시피를 목적·사전조건·절차·완료 기준·롤백·근거 6필드로 닫습니다.</p><div class="vt-shell"><div class="vt-shell-head"><div><div class="vt-id">VT-05 CHECKLIST FLOW</div><h2>레시피 공통 체크</h2><p>모든 레시피는 목적·사전조건 확인 후 시작하고 완료 기준으로 닫습니다.</p></div><span class="vt-fit">checklist flow</span></div><div class="vt-frame"><div class="cf"><div class="cf-item"><span class="cf-check" aria-hidden="true">✓</span><b>목적·사전조건 확인</b><span class="cf-state">PASS</span></div><div class="cf-item"><span class="cf-check" aria-hidden="true">✓</span><b>privileged·커널 모듈</b><span class="cf-state">PASS</span></div><div class="cf-item"><span class="cf-check" aria-hidden="true">✓</span><b>완료 기준·롤백 기록</b><span class="cf-state">PASS</span></div></div></div></div><div class="tbl table-scroll mobile-card-table"><table class="table"><caption>작업 레시피 식별(6필드 중 5필드 요약 — 절차는 아래 코드)</caption><thead><tr><th>레시피</th><th>목적</th><th>사전조건</th><th>완료 기준</th><th>롤백</th></tr></thead><tbody><tr><td data-label="레시피">R1 기본 패키지 + Docker</td><td data-label="목적">컨테이너 런타임 확보</td><td data-label="사전조건">Ubuntu VM·SSH</td><td data-label="완료 기준"><code>docker run hello-world</code> 성공</td><td data-label="롤백">apt remove docker-ce</td></tr><tr><td data-label="레시피">R2 커널 모듈</td><td data-label="목적">binder/ashmem 로드</td><td data-label="사전조건">linux-modules-extra</td><td data-label="완료 기준"><code>lsmod | grep binder</code> 출력</td><td data-label="롤백">modprobe -r·conf 삭제</td></tr><tr><td data-label="레시피">R3 redroid 실행</td><td data-label="목적">Android 컨테이너 기동</td><td data-label="사전조건">R1·R2·데이터 디렉터리</td><td data-label="완료 기준"><code>docker ps</code> redroid12 Up</td><td data-label="롤백">docker rm -f redroid12</td></tr><tr><td data-label="레시피">R4 ADB + scrcpy</td><td data-label="목적">원격 접속·화면 제어</td><td data-label="사전조건">R3·SSH 터널</td><td data-label="완료 기준">adb devices = device</td><td data-label="롤백">adb disconnect</td></tr><tr><td data-label="레시피">R5 카카오톡 설치</td><td data-label="목적">APK 설치·실행</td><td data-label="사전조건">R4·공식 APK</td><td data-label="완료 기준">scrcpy에 카카오톡 화면</td><td data-label="롤백">adb uninstall com.kakao.talk</td></tr></tbody></table></div><h3>R1 — 기본 패키지 + Docker Engine</h3><p>근거: Docker 공식 문서(apt 저장소 등록 → docker-ce/containerd/compose-plugin 설치).</p>{pre(C_BASE)}{pre(C_DOCKER)}<h3>R2 — redroid 커널 모듈 준비</h3><p>근거: redroid 공식 deploy 문서(binderfs·ashmem/memfd·IPv6·DMA-BUF 필수). 재부팅 후 자동 로드까지 설정합니다.</p>{pre(C_KERNEL)}<h3>R3 — 데이터 디렉터리 + 컨테이너 실행</h3><p>근거: redroid 공식 quick start. <code>gpu_mode=guest</code>는 software rendering으로 가장 안정적인 기본값입니다(가속이 필요하면 host).</p>{pre(C_RUN)}<h3>R4 — ADB 연결 + scrcpy</h3>{pre(C_ADB)}<h3>R5 — 카카오톡 APK 설치 + 실행</h3><p>APK는 공식 경로(본인 기기 추출/공식 배포)에서 확보합니다. 패키지 ID는 <code>com.kakao.talk</code>.</p>{pre(C_KAKAO)}</section>

  <section class="reference-extract"><h2>{icon("file")}<span class="num">6</span>참조 근거 · Reference Extract</h2><p class="h2-sub">각 절차가 어느 공식 문서에서 왔는지 추적 가능해야 버전 갱신 시 따라갈 수 있습니다.</p><p>본문 절차는 아래 근거에 기반합니다. 이 목록에 없는 정보(정확한 APK 버전, 성능 수치, SLA)는 본문에 단정으로 등장하지 않습니다.</p><ul class="col-list"><li>redroid 공식 — 필수 커널 기능(binderfs·ashmem/memfd·IPv6·DMA-BUF)</li><li>redroid 공식 — ADB 포트 공용망 노출 경고</li><li>redroid 공식 — <code>gpu_mode</code> auto/host/guest 의미</li><li>redroid 공식 — GApps/MicroG/MindTheGapps로 GMS 추가</li><li>Docker 공식 — Ubuntu apt 저장소 설치 절차</li><li>카카오톡 — Google Play 패키지 ID <code>com.kakao.talk</code></li></ul></section>

  <section class="decision-guide"><h2>{icon("diamond")}<span class="num">7</span>선택 기준 · Decision Guide</h2><p class="h2-sub">구축 방식·GPU 모드·Android 버전을 무엇을 기준으로 고를지 정리합니다 — 기본값부터 시작하고 막힐 때만 바꿉니다.</p><div class="manual-reference-grid"><article class="manual-card"><h3>실행 위치</h3><p><strong>1순위 Ubuntu VM</strong>(안정·재현성·스냅샷). 2순위 Privileged LXC(binder·nesting·AppArmor가 얽혀 난이도 높음). 3순위 Host 직접 Docker. 서버 안정성을 보면 1순위가 가장 낫습니다.</p></article><article class="manual-card"><h3>GPU 모드</h3><p><strong>기본 guest</strong>(software rendering — 가장 안정적). scrcpy가 검은 화면/끊김이면 그대로 guest 유지가 정답이며, GPU 가속이 꼭 필요할 때만 host를 시도합니다. auto는 환경 자동 판단.</p></article><article class="manual-card"><h3>Android 버전</h3><p><strong>redroid 12로 시작</strong>. 카카오톡이 설치는 되는데 실행이 안 되면 14/15 이미지로 올리고, GMS 의존 기능이 필요하면 MicroG 또는 GApps 포함 구성을 검토합니다.</p></article></div></section>

  <section class="troubleshooting" id="man-trouble"><h2>{icon("warn")}<span class="num">8</span>Troubleshooting · 증상별 문제 해결</h2><p class="h2-sub">증상 → 가능 원인 → 진단 순서 → 복구의 4단 구조를 고정합니다 — 진단 없이 복구부터 시도하지 않습니다.</p><div class="manual-trouble-grid"><article class="manual-trouble manual-trouble-scenario"><h3>A. 컨테이너가 바로 종료됨</h3><p><strong>증상:</strong> <code>docker ps</code>에 redroid12가 보이지 않고 즉시 Exited.</p><p><strong>가능 원인:</strong> binder_linux 미로드, ashmem/memfd 문제, 커널 기능 부족, <code>--privileged</code> 누락.</p><p><strong>진단 순서:</strong> 로그·dmesg·모듈을 확인합니다.</p>{pre(C_DIAG_CT)}<p><strong>복구:</strong> 커널 모듈을 로드하고(§5 R2) privileged로 다시 실행합니다.</p></article><article class="manual-trouble manual-trouble-scenario"><h3>B. ADB 연결이 안 됨</h3><p><strong>증상:</strong> <code>adb devices</code>에 기기가 없거나 offline.</p><p><strong>가능 원인:</strong> 컨테이너 미기동, 5555 미바인딩, SSH 터널 미개방.</p><p><strong>진단 순서:</strong> 컨테이너·포트·터널을 확인합니다.</p>{pre(C_DIAG_ADB)}<p><strong>복구:</strong> SSH 터널 터미널을 열어둔 채 adb 서버를 재시작하고 다시 connect 합니다.</p></article><article class="manual-trouble manual-trouble-scenario"><h3>C. scrcpy 검은 화면 / 끊김</h3><p><strong>증상:</strong> 화면이 검게 나오거나 자주 끊깁니다.</p><p><strong>가능 원인:</strong> GPU 가속 모드(host)가 VM 환경과 맞지 않음.</p><p><strong>진단 순서:</strong> 현재 <code>gpu_mode</code> 확인 → guest로 재실행 필요 여부 판단.</p><p><strong>복구:</strong> 컨테이너를 지우고 <code>androidboot.redroid_gpu_mode=guest</code>(software rendering)로 §5 R3을 다시 실행합니다.</p></article><article class="manual-trouble manual-trouble-scenario"><h3>D. 설치는 됐는데 실행이 안 됨</h3><p><strong>증상:</strong> 설치는 완료됐지만 카카오톡이 뜨지 않거나 즉시 종료.</p><p><strong>가능 원인:</strong> APK 아키텍처 불일치, split APK 일부 누락, GMS 의존, 버전 호환성, 가상환경 탐지.</p><p><strong>진단 순서:</strong> 설치 여부·로그를 확인합니다.</p>{pre(C_DIAG_KAKAO)}<p><strong>복구:</strong> split APK 전체 설치 → redroid 12→14/15 → GMS 포함/ MicroG 순으로 단계적으로 시도합니다.</p></article></div></section>

  <section class="operations-runbook"><h2>{icon("nodes")}<span class="num">9</span>운영 런북 · Operations Runbook</h2><p class="h2-sub">일상 운영 명령과 백업·복원을 한곳에 모읍니다 — 장기 운영의 핵심은 백업입니다.</p><div class="manual-runbook-grid"><article class="manual-card"><h3>일상 운영</h3><p>중지·시작·재시작·로그·셸 진입을 컨테이너 단위로 수행합니다. Android 셸은 <code>adb shell</code>, 컨테이너 내부 셸은 <code>docker exec</code>로 들어갑니다.</p></article><article class="manual-card"><h3>1차 백업</h3><p>Proxmox 웹 UI에서 Ubuntu VM <strong>Snapshot</strong>을 만드는 것이 가장 간단하고 강력합니다. VM 전체가 한 번에 보존됩니다.</p></article><article class="manual-card"><h3>2차 백업</h3><p>컨테이너를 멈추고 <code>/opt/redroid/data</code>를 tar로 백업합니다. 복원은 같은 경로로 풀어 넣고 재시작합니다.</p></article></div><h3>운영 명령</h3>{pre(C_OPS)}<h3>백업 · 복원</h3>{pre(C_BACKUP)}</section>

  <section class="manual-audit"><h2>{icon("search")}<span class="num">10</span>운영 주의 · 한계 감사 · Cautions</h2><p class="h2-sub">매뉴얼대로 동작하더라도 카카오톡 특성상 남는 한계를 원인과 함께 기록합니다 — 메인 계정 사용은 권장하지 않습니다.</p><div class="tbl table-scroll mobile-card-table"><table class="table"><caption>카카오톡 사용 시 주의사항</caption><thead><tr><th>항목</th><th>설명</th></tr></thead><tbody><tr><td data-label="항목">전화번호 인증</td><td data-label="설명">redroid에는 SIM이 없어 실제 휴대폰 번호 인증이 필요</td></tr><tr><td data-label="항목">보안 인증</td><td data-label="설명">새 기기 로그인으로 감지될 수 있음</td></tr><tr><td data-label="항목">푸시 알림</td><td data-label="설명">GMS/FCM이 없으면 알림이 불안정할 수 있음</td></tr><tr><td data-label="항목">한글 입력</td><td data-label="설명">scrcpy 키보드 입력이 환경에 따라 불안정</td></tr><tr><td data-label="항목">메인 계정</td><td data-label="설명">장기 운영용 메인 계정 사용은 비권장</td></tr><tr><td data-label="항목">백업</td><td data-label="설명">Proxmox Snapshot + <code>/opt/redroid/data</code> 백업 권장</td></tr></tbody></table></div><p>redroid는 GMS 미포함 이미지가 일반적이며 Open GApps·MicroG·MindTheGapps로 GMS를 추가할 수 있습니다. 다만 카카오톡만 우선 테스트한다면 GMS 추가 전에 APK 직접 설치로 동작부터 확인하는 편이 좋습니다.</p><div class="wg-13-fc"><h3 class="wg-13-h">구축 흐름 <span class="wg-13-sub">권장 순서 요약</span></h3><div class="wg-13-flow"><a class="wg-13-node wg-13-node--start" href="#man-source"><span class="wg-13-step">START</span>Ubuntu VM</a><span class="wg-13-arrow" aria-hidden="true">↓</span><a class="wg-13-node wg-13-node--decide" href="#man-task"><span class="wg-13-step">BUILD</span>Docker + redroid</a><span class="wg-13-arrow" aria-hidden="true">↓</span><a class="wg-13-node wg-13-node--end" href="#man-trouble"><span class="wg-13-step">RUN</span>ADB·scrcpy·카카오톡</a></div></div></section>

  <section class="try"><h2>{icon("checklist")}<span class="num">11</span>Next Actions · 최종 실행 흐름</h2><p>아래는 구축이 끝난 뒤 매번 반복하는 최소 실행 흐름입니다. 처음부터 구축할 때는 §5 레시피 R1~R5를 순서대로 따른 뒤 이 흐름으로 운영합니다.</p>{pre(C_FINAL)}<ol><li>Ubuntu VM에 SSH 접속 후 <code>docker logs -f redroid12</code>로 기동 확인</li><li>로컬 PC에서 SSH 터널을 열고 <code>adb connect</code> → <code>scrcpy</code></li><li>카카오톡 APK 설치 후 <code>monkey</code>로 실행, scrcpy에서 전화번호 인증 진행</li><li>안정화되면 Proxmox Snapshot + <code>/opt/redroid/data</code> 백업으로 마무리</li></ol></section>

  <aside class="source-note"><strong>Source Limits:</strong> 이 매뉴얼은 사용자 제공 구축 문서를 역할별 실행 문서로 재구성한 것입니다. 정확한 카카오톡 APK 버전·split 구성, redroid 이미지 버전별 호환성, GMS 의존 기능의 실제 동작은 확인 불가/UNKNOWN으로 두며 실제 설치 환경에서 검증해야 합니다. APK는 반드시 공식 경로로 확보하고, ADB 포트는 인터넷에 직접 열지 않습니다.</aside>
</main>'''

shell = SHELL.read_text(encoding="utf-8")
# 1) <main>...</main> 교체
shell = re.sub(r'<main id="main".*?</main>', lambda m: MAIN, shell, count=1, flags=re.S)
# 2) title / description 교체
shell = shell.replace("<title>Manual Analysis · 제품 운영 매뉴얼</title>",
                      "<title>Proxmox + redroid 카카오톡 실행 환경 구축 매뉴얼</title>")
shell = shell.replace('<meta name="description" content="">',
                      '<meta name="description" content="Proxmox VE 위 Ubuntu VM에서 Docker 기반 Android 컨테이너 redroid를 실행하고 ADB·scrcpy로 카카오톡을 설치·제어하는 구축 매뉴얼 — 역할별 경로·작업 레시피·문제 해결·운영 런북.">')
OUT.write_text(shell, encoding="utf-8")
print("wrote", OUT, len(shell), "bytes")
print("main swapped:", "<main id=\"main\"" in shell, "| KakaoTalk verdict:", "구축 결론" in shell)
