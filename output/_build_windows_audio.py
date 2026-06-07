#!/usr/bin/env python3
"""Assemble the Windows audio PCM/DAC reference page.

Reuses the validated golden reference page's <head>/CSS/theme-bar byte-for-byte
(so the core-CSS hash, theme-dark, profile-auto bundle, and all CSS gates pass)
and swaps only the <main> body content for the Windows audio topic.
"""
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parent
GOLDEN_DIR = ROOT / "adaptive-html-final-13-topics-20260605_083433"
GOLDEN_PAGE = GOLDEN_DIR / "pages" / "09-webhook-signature-verification-reference.html"
OUT_DIR = ROOT / "adaptive-html-final-windows-audio-pcm-reference-20260605"

MAIN_OPEN = '<main id="main" class="page-wide layout-reference">'

# Reusable body-icon SVG snippets (all carry aria-hidden="true" — decorative).
IC_BLOCKS = '<svg viewBox="0 0 40 40" aria-hidden="true"><rect class="bi-accent-box" x="8" y="10" width="6" height="6" rx="1.5"/><rect class="bi-soft" x="17" y="10" width="6" height="6" rx="1.5"/><rect class="bi-fill" x="26" y="10" width="6" height="6" rx="1.5"/><path class="bi-line" d="M9 23h22M9 28h17M9 33h12"/></svg>'
IC_LAYERS = '<svg viewBox="0 0 40 40" aria-hidden="true"><path class="bi-fill" d="M8 11l8-3 8 3 8-3v21l-8 3-8-3-8 3z"/><path class="bi-line" d="M16 8v21M24 11v21"/><path class="bi-accent-line" d="M12 22c4-6 10 3 16-4"/></svg>'
IC_SHIELD = '<svg viewBox="0 0 40 40" aria-hidden="true"><path class="bi-fill" d="M20 7l11 4v8c0 7-4.5 11.5-11 14-6.5-2.5-11-7-11-14v-8z"/><path class="bi-accent-line" d="M15 20l4 4 7-9"/></svg>'
IC_WARN = '<svg viewBox="0 0 40 40" aria-hidden="true"><path class="bi-soft" d="M20 7l14 25H6L20 7z"/><path class="bi-accent-line" d="M20 16v8"/><circle class="bi-accent" cx="20" cy="29" r="2"/></svg>'
IC_CODE = '<svg viewBox="0 0 40 40" aria-hidden="true"><rect class="bi-fill" x="7" y="9" width="26" height="22" rx="4"/><path class="bi-accent-line" d="M16 16l-5 4 5 4M24 16l5 4-5 4"/><path class="bi-line" d="M21 14l-3 12"/></svg>'
IC_NODES = '<svg viewBox="0 0 40 40" aria-hidden="true"><rect class="bi-fill" x="7" y="9" width="8" height="8" rx="2"/><rect class="bi-soft" x="25" y="9" width="8" height="8" rx="2"/><rect class="bi-fill" x="16" y="24" width="8" height="8" rx="2"/><path class="bi-line" d="M15 13h10M29 17l-9 7M11 17l9 7"/><circle class="bi-accent" cx="20" cy="28" r="2"/></svg>'
IC_CHECK = '<svg viewBox="0 0 40 40" aria-hidden="true"><rect class="bi-fill" x="8" y="8" width="24" height="24" rx="4"/><path class="bi-accent-line" d="M14 20l4 4 9-10"/><path class="bi-line" d="M14 29h14"/></svg>'
IC_FILE = '<svg viewBox="0 0 40 40" aria-hidden="true"><path class="bi-fill" d="M11 7h12l6 6v20H11z"/><path class="bi-line" d="M23 7v7h6M16 20h9M16 26h7"/><circle class="bi-accent" cx="15" cy="14" r="2"/></svg>'


def icon(svg):
    return f'<span class="body-icon body-icon--sm">{svg}</span>'


def h2(svg, no, text, key=False):
    keycls = ' is-key' if key else ''
    return f'<h2>{icon(svg)}<span class="no{keycls}">{no}</span>{text}</h2>'


TITLE = "Windows 오디오 PCM·DAC 제어 레퍼런스"
DESC = "Windows에서 PCM을 DAC로 보내는 길 — WASAPI·ASIO·Kernel Streaming·WDM/WaveRT·APO를 목적별로 정리한 개발 레퍼런스다."

MAIN = f'''{MAIN_OPEN}
  <header class="header"><div class="kicker"><span class="kicker-text">REFERENCE MANUAL · WINDOWS AUDIO STACK</span></div><h1>{TITLE}</h1><p class="sub">Windows 앱은 안드로이드처럼 HAL을 직접 잡지 않는다. PCM은 Windows 오디오 스택 → 드라이버 → DAC를 거치며, 목적에 따라 WASAPI·ASIO·Kernel Streaming·WDM 드라이버로 갈린다.</p><div class="meta"><span>reference_html</span><span>reference-manual.html</span><span>profile auto</span><span>adaptive-html-final v5.2.2</span><span>무 JS</span></div><div class="generated-row"><p class="generated-date">Generated · 2026-06-05 KST</p><div class="lens-strip" aria-label="적용 렌즈"><span class="lens-strip-label">LENS</span><span class="lens-chip">WASAPI</span><span class="lens-chip">Exclusive</span><span class="lens-chip">ASIO</span><span class="lens-chip">WDK/WaveRT</span><span class="lens-chip">APO</span></div></div></header>

  <section class="summary-card">
    <div class="label">{icon(IC_BLOCKS)}Overview</div>
    <p><strong>“DAC의 HAL에 직접 접근해 PCM을 제어한다”는 표현은 Windows에서는 약간 다르다.</strong> 일반 앱은 DAC 하드웨어/HAL을 직접 잡지 않고 <em>앱 → Windows 오디오 엔진 → 드라이버 → DAC</em> 계층을 거쳐 PCM 스트림을 보낸다. 그래서 “무엇을 하고 싶은가”에 따라 API가 갈린다. 앱에서 PCM을 밀어 넣고 싶으면 <strong>WASAPI</strong>, bit-perfect/저지연이면 <strong>WASAPI Exclusive</strong> 또는 <strong>ASIO</strong>, 진짜 드라이버·버퍼를 제어하려면 <strong>WDK(PortCls/WaveRT)</strong>, 시스템 DSP를 넣으려면 <strong>APO</strong>다.</p>
  </section>

  <div class="core-insight"><blockquote>“Windows에서 PCM 제어의 시작점은 C++ WASAPI이고, HAL/드라이버급 제어는 C/C++ WDK 영역이다.”</blockquote><p>앱 레벨에서 오디오 장치로 PCM을 보내는 공식 기본 API는 WASAPI다. 더 낮은 지연이나 bit-perfect 출력이 필요하면 WASAPI Exclusive나 ASIO로 내려가고, DAC 드라이버 자체나 PCM pin/buffer를 만들고 싶으면 그때부터는 앱 언어 문제가 아니라 Windows 드라이버 개발(WDK + PortCls/WaveRT)이다. 같은 “PCM 제어”라는 말이 계층마다 전혀 다른 도구를 가리킨다.</p></div>

  <section class="vt-shell" aria-label="Windows 오디오 스택 계층 개요">
    <div class="vt-frame">
      <div class="ft"><article class="ft-card"><div class="ft-head"><span>Application</span><span>app</span></div><div class="ft-body"><p class="vt-text">PCM 버퍼를 만들어 오디오 endpoint로 보내는 WASAPI/ASIO/KS 클라이언트. 여기서 sample rate·bit depth·채널·버퍼를 결정한다.</p><div class="ft-note"><b>핵심</b><br>HAL을 직접 잡지 않는다 — 항상 API를 통해 스트림을 연다.</div></div></article><article class="ft-card"><div class="ft-head"><span>WASAPI / KS / ASIO</span><span>api</span></div><div class="ft-body"><p class="vt-text">앱과 엔진·드라이버 사이의 표준 인터페이스 계층. shared/exclusive, KS pin, ASIO callback이 여기에 속한다.</p><div class="ft-note"><b>핵심</b><br>Exclusive·ASIO는 믹서를 우회해 더 낮은 지연으로 직행한다.</div></div></article><article class="ft-card"><div class="ft-head"><span>Audio Engine + Service</span><span>engine</span></div><div class="ft-body"><p class="vt-text">shared mode에서 여러 앱 소리를 믹싱·리샘플링하고 APO(시스템 DSP)를 적용하는 계층.</p><div class="ft-note"><b>핵심</b><br>Exclusive로 열면 이 믹서·리샘플러를 건너뛴다.</div></div></article><article class="ft-card"><div class="ft-head"><span>PortCls / WaveRT</span><span>driver</span></div><div class="ft-body"><p class="vt-text">커널 오디오 드라이버. WaveRT는 오디오 엔진이 데이터 버퍼에 직접 접근하게 해 복사·매핑을 줄인다.</p><div class="ft-note"><b>핵심</b><br>드라이버급 PCM 제어는 C/C++ + WDK 영역이다.</div></div></article><article class="ft-card"><div class="ft-head"><span>USB DAC / I2S Codec</span><span>hardware</span></div><div class="ft-body"><p class="vt-text">실제 D/A 변환을 수행하는 하드웨어. USB DAC·PCIe 오디오·I2S 코덱·외장 DSP가 여기에 해당한다.</p><div class="ft-note"><b>핵심</b><br>지원하지 않는 포맷(예: 384kHz/32bit)으로는 스트림을 열 수 없다.</div></div></article></div>
    </div>
  </section>

  <section>
    {h2(IC_BLOCKS, 1, "빠른 레퍼런스 — 목적별 추천", key=True)}
    <p class="h2-sub">“무엇을 하고 싶은가”를 먼저 정하면 언어와 접근 방식이 거의 자동으로 정해진다.</p>
    <div class="tbl table-scroll">
      <table>
        <caption>목적별 추천 언어와 접근 방식</caption>
        <thead><tr><th>목적</th><th>추천 언어</th><th>접근 방식</th></tr></thead>
        <tbody>
          <tr><td>일반 PCM 재생/녹음 제어</td><td>C++</td><td>WASAPI</td></tr>
          <tr><td>저지연 / bit-perfect 출력</td><td>C++</td><td>WASAPI Exclusive Mode</td></tr>
          <tr><td>C#으로 빠르게 구현</td><td>C#</td><td>NAudio / CSCore의 WASAPI 래퍼</td></tr>
          <tr><td>Rust로 구현</td><td>Rust</td><td>windows-rs / cpal / wasapi crate</td></tr>
          <tr><td>프로 오디오 / DAC 저지연</td><td>C++</td><td>ASIO SDK / 제조사 ASIO 드라이버</td></tr>
          <tr><td>드라이버 레벨 PCM 제어</td><td>C / C++</td><td>WDK + WDM / PortCls / WaveRT miniport</td></tr>
          <tr><td>EQ·리버브·AGC 같은 시스템 DSP</td><td>C++ (COM)</td><td>APO, Audio Processing Object</td></tr>
        </tbody>
      </table>
    </div>
    <div class="good">
      <div class="label">가장 현실적인 답</div>
      <div class="name">대부분은 C++ WASAPI에서 시작한다</div>
      <p>앱에서 PCM을 직접 밀어 넣고 싶으면 <strong>C++ WASAPI Exclusive</strong>, DAC 드라이버나 PCM pin/buffer를 제어하려면 <strong>C/C++ WDK WaveRT/PortCls</strong>, 전문 오디오 장비처럼 저지연이 목적이면 <strong>ASIO</strong>다. 일반 USB DAC는 WASAPI Exclusive만으로 충분한 경우가 많다.</p>
    </div>
  </section>

  <section>
    {h2(IC_LAYERS, 2, "Windows 오디오 스택 계층")}
    <p class="h2-sub">vt-09 file-tour로 본 다섯 계층을 “어떤 책임을 지고, 어디서 신뢰·제어 경계가 바뀌는가”로 정리한다.</p>
    <p>Microsoft의 Windows Audio Architecture는 앱·오디오 엔진·서비스·드라이버·하드웨어 계층으로 나뉜다. 안드로이드처럼 앱이 HAL을 직접 잡고 DAC PCM을 제어하는 구조가 아니라, 앱은 항상 API를 통해 스트림을 열고 그 아래 계층이 믹싱·리샘플링·버퍼 매핑·D/A 변환을 나눠 맡는다.</p>
    <pre><code>Application
  ↓ WASAPI / KS / ASIO
Windows Audio Engine
  ↓
PortCls / WaveRT / Vendor Driver
  ↓
USB DAC / PCIe Audio / I2S Codec / DSP</code></pre>
    <div class="tbl table-scroll">
      <table>
        <caption>계층별 책임과 제어 가능 범위</caption>
        <thead><tr><th>계층</th><th>주요 API/구성</th><th>책임</th><th>앱에서 제어 가능?</th></tr></thead>
        <tbody>
          <tr><td>Application</td><td>WASAPI / ASIO / KS 클라이언트</td><td>PCM 버퍼 생성, 포맷·버퍼 크기 지정</td><td>전면 제어</td></tr>
          <tr><td>Audio Engine</td><td>오디오 엔진 + 서비스</td><td>믹싱·리샘플링·APO(shared mode)</td><td>Exclusive로 우회 가능</td></tr>
          <tr><td>Driver</td><td>PortCls / WaveRT / Vendor</td><td>커널 스트리밍, 버퍼 직접 매핑</td><td>드라이버 개발 시에만</td></tr>
          <tr><td>Hardware</td><td>USB DAC / I2S Codec</td><td>실제 D/A 변환, 지원 포맷 결정</td><td>제조사 SDK 한정</td></tr>
        </tbody>
      </table>
    </div>
  </section>

  <section>
    {h2(IC_CODE, 3, "WASAPI — 앱 레벨 PCM")}
    <p class="h2-sub">Windows에서 PCM 스트림을 오디오 장치로 보내는 공식 기본 API. 정석 언어는 C++이다.</p>
    <p>WASAPI는 애플리케이션이 오디오 endpoint device와 데이터 흐름을 관리하게 해주는 API다. C#도 가능하지만 내부적으로는 COM 기반 WASAPI를 감싸는 구조다. WASAPI로 앱이 제어할 수 있는 것은 다음과 같다.</p>
    <div class="card-grid">
      <article class="mini-card"><h3>Sample rate</h3><p>44.1kHz, 48kHz, 96kHz 등 — DAC가 지원하는 범위 안에서 지정.</p></article>
      <article class="mini-card"><h3>Bit depth</h3><p>16-bit, 24-bit, 32-bit float 등 출력 포맷.</p></article>
      <article class="mini-card"><h3>Channel</h3><p>stereo, 5.1, 7.1 등 채널 구성.</p></article>
      <article class="mini-card"><h3>PCM / latency buffer</h3><p>렌더·캡처 버퍼와 latency buffer 크기.</p></article>
      <article class="mini-card"><h3>Mode</h3><p>shared / exclusive 선택.</p></article>
      <article class="mini-card"><h3>Stream 방향</h3><p>render(재생) / capture(녹음) 스트림.</p></article>
    </div>
    <div class="tbl table-scroll">
      <table>
        <caption>WASAPI shared vs exclusive 요약</caption>
        <thead><tr><th>항목</th><th>Shared Mode</th><th>Exclusive Mode</th></tr></thead>
        <tbody>
          <tr><td>믹싱</td><td>다른 앱과 믹싱됨</td><td>장치 독점, 믹싱 없음</td></tr>
          <tr><td>리샘플링</td><td>엔진이 공통 포맷으로 변환</td><td>지정 포맷 그대로 출력</td></tr>
          <tr><td>지연(latency)</td><td>상대적으로 높음</td><td>낮게 설정 가능</td></tr>
          <tr><td>bit-perfect</td><td>보장 어려움</td><td>유리</td></tr>
          <tr><td>전제 조건</td><td>대부분 동작</td><td>DAC가 해당 포맷 지원해야 함</td></tr>
        </tbody>
      </table>
    </div>
  </section>

  <section>
    {h2(IC_SHIELD, 4, "WASAPI Exclusive — bit-perfect")}
    <p class="h2-sub">DAC에 원본 PCM을 그대로 보내 리샘플링을 피하고 싶을 때 쓰는 독점 모드.</p>
    <p>Exclusive Mode는 앱이 오디오 endpoint device를 <strong>독점</strong>해 사용하는 방식이다. Windows 믹서를 우회하고 다른 앱 소리와 믹싱되지 않으며, 지정한 sample rate·bit depth로 직접 출력하므로 bit-perfect 출력과 낮은 latency에 유리하다. 단, DAC가 해당 포맷을 지원해야 열 수 있다.</p>
    <div class="good">
      <div class="label">기대할 수 있는 것</div>
      <div class="name">믹서 우회 · 지정 포맷 직출력 · 낮은 지연</div>
      <p>Windows 믹서를 거치지 않고 앱이 정한 포맷으로 곧장 DAC에 보내므로, 음원 그대로의 bit-perfect 출력과 낮은 버퍼 지연을 얻을 수 있다.</p>
    </div>
    <div class="danger">
      <div class="label">제약</div>
      <div class="name">DAC 지원 포맷에 종속된다</div>
      <p>예를 들어 DAC가 384kHz/32bit를 지원하지 않으면 그 포맷으로는 스트림을 열 수 없다. Exclusive는 장치를 독점하므로 같은 시간에 다른 앱이 그 장치로 소리를 낼 수 없다는 점도 함께 고려한다.</p>
    </div>
  </section>

  <section>
    {h2(IC_NODES, 5, "ASIO — 프로 오디오 저지연")}
    <p class="h2-sub">DAW·실시간 이펙트·초저지연 녹음/재생처럼 프로 오디오급이 목적일 때.</p>
    <p>Steinberg의 ASIO는 잘 알려진 오디오 인터페이스 제조사들이 지원하며, 낮은 latency 때문에 프로 오디오 프로그램에서 널리 쓰인다. 일반적으로 C++ SDK + 제조사 드라이버 + ASIO callback 기반 PCM 처리 구조다.</p>
    <div class="card-grid">
      <article class="mini-card"><h3>C++ SDK</h3><p>Steinberg ASIO SDK 기반 구현이 기본.</p></article>
      <article class="mini-card"><h3>제조사 드라이버</h3><p>DAC/오디오 인터페이스가 제공하는 ASIO 드라이버에 의존.</p></article>
      <article class="mini-card"><h3>Callback 처리</h3><p>ASIO callback 기반으로 PCM 블록을 주고받음.</p></article>
      <article class="mini-card"><h3>Multi-channel I/O</h3><p>다채널 입출력과 낮은 latency가 강점.</p></article>
    </div>
    <div class="danger">
      <div class="label">주의</div>
      <div class="name">모든 DAC가 ASIO를 제대로 지원하진 않는다</div>
      <p>고급 오디오 인터페이스는 ASIO 드라이버를 제공하지만, 일반 USB DAC는 WASAPI Exclusive만으로 충분한 경우가 많다. ASIO 지원 여부는 장치/제조사에 종속된다.</p>
    </div>
  </section>

  <section>
    {h2(IC_LAYERS, 6, "WDK + PortCls / WaveRT — 드라이버 레벨")}
    <p class="h2-sub">“HAL 드라이버처럼 DAC 하드웨어를 직접 제어”는 앱 언어 문제가 아니라 Windows 드라이버 개발이다.</p>
    <p>이 경우 언어는 사실상 <strong>C / C++ + Windows Driver Kit(WDK)</strong>다. WDK는 Windows 드라이버를 개발·테스트·배포하는 도구다. 오디오 드라이버 영역은 WDM Audio Driver, PortCls, WaveRT miniport, AVStream, Kernel Streaming(KS), IOCTL, INF 설치, 드라이버 서명으로 들어간다.</p>
    <div class="term">
      <div class="label">PortCls</div>
      <span class="word">오디오 port-class driver</span>
      <p class="meaning">대부분의 generic kernel streaming filter 기능을 구현해 오디오 드라이버 개발을 단순화한다. WaveRT miniport driver의 핵심 인터페이스로는 <code>IMiniportWaveRT</code>가 쓰인다.</p>
    </div>
    <div class="term">
      <div class="label">WaveRT</div>
      <span class="word">오디오 엔진의 버퍼 직접 접근</span>
      <p class="meaning">오디오 엔진이 데이터 버퍼에 직접 접근하도록 해서 불필요한 복사와 매핑을 줄이는 구조다. 진짜 PCM 드라이버 제어를 하려면 이 영역으로 내려간다.</p>
    </div>
    <div class="tbl table-scroll">
      <table>
        <caption>드라이버 레벨에서 다루는 구성 요소</caption>
        <thead><tr><th>구성</th><th>역할</th><th>비고</th></tr></thead>
        <tbody>
          <tr><td>WDM Audio Driver</td><td>Windows 오디오 드라이버 모델</td><td>커널 모드</td></tr>
          <tr><td>PortCls</td><td>port-class driver, KS filter 기능</td><td>개발 단순화</td></tr>
          <tr><td>WaveRT Miniport</td><td><code>IMiniportWaveRT</code> 구현, 버퍼 직접 매핑</td><td>저지연 핵심</td></tr>
          <tr><td>AVStream / KS</td><td>커널 스트리밍, IOCTL 경로</td><td>pin/buffer 제어</td></tr>
          <tr><td>INF + 서명</td><td>설치 정보와 드라이버 서명</td><td>배포 필수</td></tr>
        </tbody>
      </table>
    </div>
  </section>

  <section>
    {h2(IC_BLOCKS, 7, "APO — 시스템 DSP")}
    <p class="h2-sub">안드로이드의 AudioEffect/DynamicsProcessing 같은 느낌으로 시스템 오디오에 DSP를 넣고 싶을 때.</p>
    <p>APO(Audio Processing Object)는 Windows 오디오 스트림에 소프트웨어 기반 DSP를 제공하는 <strong>COM 기반 객체</strong>다. graphic equalizer, reverb, tremolo, AEC, AGC 등이 예로 언급된다. 시스템 레벨 EQ·라우드니스 보정·AGC·노이즈 억제·공간 음향·드라이버에 붙는 효과는 C++ COM 기반 APO 영역이다.</p>
    <div class="danger">
      <div class="label">오해 주의</div>
      <div class="name">APO는 DAC 레지스터를 직접 제어하지 않는다</div>
      <p>APO는 “DAC 하드웨어 레지스터를 직접 제어”하는 것이 아니라 Windows 오디오 스트림 <strong>중간에서 DSP 처리</strong>를 하는 구조다. 하드웨어 직접 제어가 목적이라면 제조사 SDK 또는 커스텀 드라이버로 가야 한다.</p>
    </div>
  </section>

  <section>
    {h2(IC_CODE, 8, "언어별 현실성")}
    <p class="h2-sub">같은 목표라도 언어에 따라 도달 가능한 깊이가 다르다.</p>
    <div class="tbl table-scroll">
      <table>
        <caption>언어별 가능 범위와 추천 용도</caption>
        <thead><tr><th>언어</th><th>가능한 것</th><th>추천 라이브러리/도구</th><th>한계</th></tr></thead>
        <tbody>
          <tr><td>C++</td><td>WASAPI(shared/exclusive), MMDevice, DeviceTopology, KS, ASIO, APO, WDK driver</td><td>Core Audio API, ASIO SDK, WDK</td><td>가장 강력 — 사실상 전 영역</td></tr>
          <tr><td>C#</td><td>WASAPI 재생/녹음, exclusive, sample rate, PCM write, loopback, volume</td><td>NAudio, CSCore</td><td>드라이버/HAL 레벨은 부적합</td></tr>
          <tr><td>Rust</td><td>WASAPI backend, 저수준 COM 직접 호출</td><td>windows-rs, cpal, wasapi crate</td><td>문서·샘플이 C++ 중심이라 난이도↑</td></tr>
          <tr><td>Python</td><td>테스트용 재생/녹음, 일부 loopback</td><td>sounddevice, pyaudio, soundcard</td><td>bit-perfect/exclusive/드라이버는 비추천</td></tr>
        </tbody>
      </table>
    </div>
    <div class="faq">
      <div class="label">자주 나오는 질문</div>
      <dl>
        <dt>볼륨·mute·경로 같은 장치 제어는 어디서 하나?</dt>
        <dd>DeviceTopology / EndpointVolume API로 일부 가능하다. Core Audio API에는 MMDevice, WASAPI, DeviceTopology가 있고, DeviceTopology는 오디오 어댑터 내부 경로의 볼륨 컨트롤·multiplexer 같은 topology feature 접근에 쓰인다.</dd>
        <dt>C#만으로 bit-perfect 출력이 가능한가?</dt>
        <dd>NAudio/CSCore로 exclusive mode·sample rate 설정·PCM write까지는 가능하다. 다만 내부적으로 COM 기반 WASAPI를 감싸는 구조이고, 드라이버·HAL 레벨 제어는 부적합하다.</dd>
        <dt>DAC 하드웨어 레지스터를 직접 만질 수 있나?</dt>
        <dd>일반 앱에서는 불가능하다. 제조사 SDK 또는 커스텀 드라이버(WDK)가 필요하다.</dd>
      </dl>
    </div>
  </section>

  <section>
    {h2(IC_NODES, 9, "정리 — 하고 싶은 것 → 추천")}
    <p class="h2-sub">목적을 한 줄로 좁히면 선택은 거의 결정된다.</p>
    <div class="tbl table-scroll">
      <table>
        <caption>목적별 가능 여부와 추천 경로</caption>
        <thead><tr><th>하고 싶은 것</th><th>가능한가</th><th>추천</th></tr></thead>
        <tbody>
          <tr><td>PCM 데이터를 DAC로 직접 출력</td><td>가능</td><td>C++ WASAPI</td></tr>
          <tr><td>Windows 믹서 없이 출력</td><td>가능</td><td>WASAPI Exclusive</td></tr>
          <tr><td>저지연 오디오 출력</td><td>가능</td><td>WASAPI Exclusive 또는 ASIO</td></tr>
          <tr><td>DAC sample rate / bit depth 변경</td><td>가능</td><td>WASAPI Exclusive / ASIO</td></tr>
          <tr><td>DAC 볼륨·mute·경로 제어</td><td>일부 가능</td><td>DeviceTopology / EndpointVolume</td></tr>
          <tr><td>시스템 전체 EQ/DSP 삽입</td><td>가능</td><td>APO</td></tr>
          <tr><td>DAC 하드웨어 레지스터 직접 제어</td><td>일반 앱에선 불가</td><td>제조사 SDK 또는 커스텀 드라이버</td></tr>
          <tr><td>Windows 오디오 드라이버 직접 개발</td><td>가능</td><td>C/C++ + WDK + PortCls/WaveRT</td></tr>
        </tbody>
      </table>
    </div>
  </section>

  <section>
    {h2(IC_CHECK, 10, "권장 개발 경로")}
    <p class="h2-sub">가장 현실적인 단계는 위에서 아래로, 필요할 때만 내려가는 것이다.</p>
    <div class="tbl table-scroll">
      <table>
        <caption>단계별 목표와 사용 기술</caption>
        <thead><tr><th>단계</th><th>목표</th><th>사용 기술</th></tr></thead>
        <tbody>
          <tr><td>1단계</td><td>PCM 출력 테스트</td><td>C# NAudio 또는 C++ WASAPI</td></tr>
          <tr><td>2단계</td><td>bit-perfect / sample rate / buffer 제어</td><td>WASAPI Exclusive</td></tr>
          <tr><td>3단계</td><td>더 낮은 지연이 필요하면</td><td>ASIO</td></tr>
          <tr><td>4단계</td><td>시스템 DSP가 필요하면</td><td>APO</td></tr>
          <tr><td>5단계</td><td>진짜 DAC 드라이버 제어가 필요하면</td><td>WDK WaveRT/PortCls</td></tr>
        </tbody>
      </table>
    </div>
    <ol>
      <li>먼저 가장 쉬운 경로(C# NAudio / C++ WASAPI)로 소리가 나는지부터 확인한다.</li>
      <li>리샘플링·믹싱이 거슬리면 Exclusive로 올려 포맷을 고정한다.</li>
      <li>실시간성이 핵심이면 ASIO 지원 여부를 장치 기준으로 확인한다.</li>
      <li>시스템 전체 효과가 목적이면 드라이버가 아니라 APO를 먼저 검토한다.</li>
      <li>드라이버급 제어는 가장 마지막 — 서명·INF·배포까지 포함한 별도 프로젝트로 다룬다.</li>
    </ol>
  </section>

  <section class="try"><div class="label">NEXT ACTION</div><h2>바로 실행할 일</h2><ol><li>목표를 한 줄로 적는다 — “재생만”인지 “bit-perfect”인지 “드라이버 제어”인지.</li><li>대상 DAC가 지원하는 sample rate·bit depth·exclusive·ASIO 여부를 확인한다.</li><li>C++ WASAPI(또는 C# NAudio)로 최소 재생 PoC를 만든다.</li><li>지연/포맷 요구가 PoC를 넘어설 때만 Exclusive → ASIO → 드라이버로 단계적으로 내려간다.</li></ol></section>
  <aside class="source-note"><div class="label">Source Note</div><p>Windows 오디오 개발 레퍼런스 예시다. 실제 구현 시 Microsoft의 Core Audio(WASAPI)·WDK(PortCls/WaveRT)·APO 공식 문서와 Steinberg ASIO SDK, 그리고 대상 DAC 제조사 문서의 최신 내용을 확인해야 한다. 이 문서는 동작 JS 없이 CSS-only vt 구조로 작성되었다.</p></aside>
</main>'''


def build():
    text = GOLDEN_PAGE.read_text(encoding="utf-8")
    idx = text.index(MAIN_OPEN)
    prefix = text[:idx]
    # Swap title/description/og to the Windows-audio topic.
    prefix = prefix.replace("<title>Webhook 서명 검증 레퍼런스</title>", f"<title>{TITLE}</title>")
    prefix = prefix.replace(
        '<meta name="description" content="Webhook 요청이 실제 발신자에게서 왔고 중간에 변조되지 않았는지 확인하는 실무 레퍼런스다.">',
        f'<meta name="description" content="{DESC}">')
    prefix = prefix.replace(
        '<meta property="og:title" content="Webhook 서명 검증 레퍼런스">',
        f'<meta property="og:title" content="{TITLE}">')
    prefix = prefix.replace(
        '<meta property="og:description" content="Webhook 요청이 실제 발신자에게서 왔고 중간에 변조되지 않았는지 확인하는 실무 레퍼런스다.">',
        f'<meta property="og:description" content="{DESC}">')

    out_html = prefix + MAIN + "\n\n</body>\n</html>\n"

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / "index.html").write_text(out_html, encoding="utf-8")

    # Copy the validated sources/ snapshot (identical skill assets + profile auto).
    src_sources = GOLDEN_DIR / "sources"
    dst_sources = OUT_DIR / "sources"
    if dst_sources.exists():
        shutil.rmtree(dst_sources)
    shutil.copytree(src_sources, dst_sources)
    print("WROTE", OUT_DIR / "index.html")


if __name__ == "__main__":
    build()
