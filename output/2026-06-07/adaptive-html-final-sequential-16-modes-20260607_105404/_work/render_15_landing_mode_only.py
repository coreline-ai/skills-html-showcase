#!/usr/bin/env python3
"""Render mode 15 landing_brief_html only for sequential QA.

No previous HTML body is read; no shared/common generator is imported.
The script reads only landing layout/recipe/references and landing-relevant vt/wg templates.
"""
from __future__ import annotations

import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[1]
SKILL = REPO / "skills" / "adaptive-html-final"
ASSETS = SKILL / "assets"
OUT = ROOT / "pages" / "15_landing_brief_launchbrief_studio.html"
SOURCES = ROOT / "sources"
SNAP = SOURCES / "assets"

MODE_MATERIALS = [
    "SKILL.md",
    "recipes/landing-brief.prompt.md",
    "assets/layouts/landing-brief.html",
    "references/layout-system.md",
    "references/writing-system.md",
    "references/quality-gates.md",
    "references/body-icon-system.md",
    "references/visual-html-system.md",
    "references/widget-system.md",
    "assets/visual-html-templates/01-hero-map.html",
    "assets/visual-html-templates/07-card-grid.html",
    "assets/visual-html-templates/19-feature-flag.html",
    "assets/visual-html-templates/21-soft-workflow-map.html",
    "assets/widget-templates/08-clickable-flow.html",
]
CSS_ORDER = [
    "theme.css", "components.css", "visual-components.css", "widgets.css", "visual-html.css",
    "body-icons.css", "editorial-patterns.css", "shape-visuals.css", "workflow-visuals.css",
    "layouts.css", "print.css", "theme-dark.css",
]
CORE = ["theme.css", "components.css", "visual-components.css", "layouts.css", "print.css"]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def sha_bytes(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


ICONS = {i["id"]: i["svg"] for i in json.loads(read(ASSETS / "body-icons.json"))}


def icon(name: str) -> str:
    return f'<span class="body-icon body-icon--sm">{ICONS[name]}</span>'


def h2(n: int, title: str, icon_name: str, sub: str) -> str:
    return f'<h2>{icon(icon_name)}<span class="num">{n}</span>{title}</h2>\n<p class="h2-sub">{sub}</p>'


def vt_hero_map() -> str:
    return '''<section class="vt-shell" aria-label="LaunchBrief Studio hero map">
  <div class="vt-frame">
    <div class="vt-demo"><div class="hm-grid"><article class="hm-card"><div class="vt-kicker">Problem</div><h3>출시 메시지가 흩어짐</h3><p class="vt-text">PRD, 릴리스 노트, 세일즈 문구, 고객 공지가 서로 다른 언어로 작성됩니다.</p></article><article class="hm-card" style="--c:var(--vt-blue)"><div class="vt-kicker">Map</div><h3>한 장의 판단 문서</h3><p class="vt-text">대상, 약속, 근거, 금지 표현, 다음 행동을 하나의 brief로 고정합니다.</p></article><article class="hm-card" style="--c:var(--vt-green)"><div class="vt-kicker">Action</div><h3>채널별 문구로 전환</h3><p class="vt-text">블로그, 앱스토어, 이메일, 세일즈 콜 스크립트로 안전하게 변환합니다.</p></article></div><div class="hm-result"><b>가치 제안: 출시 메시지를 “문장”이 아니라 “판단 가능한 brief”로 만듭니다.</b><span>작은 팀이 출시 전 마지막 48시간에 메시지 혼선을 줄이는 editorial landing 도구입니다.</span></div></div>
  </div>
</section>'''


def vt_card_grid() -> str:
    return '''<section class="vt-shell" aria-label="LaunchBrief Studio value card grid">
  <div class="vt-frame">
    <div class="cg-grid"><article class="cg-card"><em>01</em><b>Audience</b><p>누구에게 말하는지 고정</p></article><article class="cg-card"><em>02</em><b>Promise</b><p>무엇을 약속하는지 한 줄로</p></article><article class="cg-card"><em>03</em><b>Proof</b><p>근거와 제한을 함께 기록</p></article><article class="cg-card"><em>04</em><b>Risk</b><p>과장·금지 표현 차단</p></article><article class="cg-card"><em>05</em><b>Channel</b><p>채널별 문구 변환</p></article><article class="cg-card"><em>06</em><b>Review</b><p>승인 전 체크리스트</p></article></div>
  </div>
</section>'''


def vt_feature_flag() -> str:
    return '''<section class="vt-shell" aria-label="LaunchBrief rollout flags">
  <div class="vt-frame">
    <div class="flag-list"><div class="flag"><div><b>brief_first_review</b><p class="vt-text">문구 작성 전 판단 brief 필수</p></div><div class="flag-ctl"><span class="flag-state on">ON</span><span class="switch on" aria-hidden="true"></span></div></div><div class="flag"><div><b>channel_auto_expand</b><p class="vt-text">채널별 초안 자동 확장, 승인 전 제한</p></div><div class="flag-ctl"><span class="flag-state warn">WARN</span><span class="switch warn" aria-hidden="true"></span></div></div><div class="flag"><div><b>unreviewed_claims</b><p class="vt-text">검증 없는 효과 수치/비교 문구</p></div><div class="flag-ctl"><span class="flag-state off">OFF</span><span class="switch off" aria-hidden="true"></span></div></div></div>
  </div>
</section>'''


def vt_soft_workflow() -> str:
    return '''<section class="vt-shell" aria-label="LaunchBrief content workflow map">
  <div class="vt-frame">
    <div class="wf-board"><div class="wf-top"><span class="wf-newbadge">출시 메시지 파이프라인</span><div class="wf-aistack" aria-hidden="true"><span class="wf-aibadge">AI</span><span class="wf-bag">▣</span></div></div><div class="wf-map"><div class="wf-col"><article class="wf-card"><div class="wf-icon" aria-hidden="true">◉</div><strong>입력 수집</strong><p>기능 설명, 고객 문제, 지원팀 메모, 제약 조건을 한 곳에 모읍니다.</p></article><article class="wf-card"><div class="wf-icon" aria-hidden="true">▦</div><strong>판단 brief</strong><p>대상, 약속, 근거, 금지 표현을 먼저 고정합니다.</p></article><article class="wf-card"><div class="wf-icon" aria-hidden="true">▧</div><strong>초안 변환</strong><p>앱스토어, 블로그, 이메일, 릴리스 노트 문구로 나눕니다.</p></article></div><div class="wf-center"><div class="wf-codewin" aria-hidden="true"><span></span><span></span><span></span></div><div class="wf-dash" aria-hidden="true"><div class="wf-dashbar"></div><div class="wf-dashblock"></div></div><div class="wf-metrics"><div class="wf-metric"><b>1</b><span>brief</span></div><div class="wf-metric"><b>4</b><span>channels</span></div><div class="wf-metric"><b>6</b><span>checks</span></div></div><div class="wf-pipes" aria-hidden="true"><div class="wf-pipe"><i></i><span></span><span></span></div><div class="wf-pipe"><i></i><span></span><span></span></div><div class="wf-pipe"><i></i><span></span><span></span></div><div class="wf-pipe"><i></i><span></span><span></span></div></div></div><div class="wf-col"><article class="wf-card"><div class="wf-icon" aria-hidden="true">⌕</div><strong>과장 검토</strong><p>확인되지 않은 성과, 비교 우위, 법적 표현을 표시합니다.</p></article><article class="wf-card"><div class="wf-icon" aria-hidden="true">♟</div><strong>승인 라우팅</strong><p>제품, 마케팅, 지원, 법무 관점별 확인 항목을 분리합니다.</p></article><article class="wf-card"><div class="wf-icon" aria-hidden="true">▣</div><strong>출시 패키지</strong><p>채널별 초안과 최종 brief를 같이 보관합니다.</p></article></div></div><div class="wf-bottom" aria-hidden="true"><span class="wf-rail-short"></span><span class="wf-rail-long"></span><span class="wf-arrow"><i>→</i></span></div></div>
  </div>
</section>'''


def wg_clickable_flow() -> str:
    return '''<div class="wg-08-proto" aria-label="LaunchBrief 클릭형 화면 프로토타입">
  <div class="wg-08-bar"><span class="wg-08-title">LaunchBrief 작성 플로우 · 프로토타입</span><ol class="wg-08-steps" aria-label="진행 단계"><li><a href="#launchbrief-input">1 입력</a></li><li><a href="#launchbrief-brief">2 brief</a></li><li><a href="#launchbrief-pack">3 패키지</a></li></ol></div>
  <div class="wg-08-device"><div class="wg-08-viewport"><article id="launchbrief-input" class="wg-08-screen wg-08-screen--default" tabindex="-1" aria-label="화면 A: 출시 입력"><header class="wg-08-shead"><span class="wg-08-badge">화면 A</span><h3>출시 입력</h3></header><ul class="wg-08-list"><li><span>기능 요약</span><span class="wg-08-price">필수</span></li><li><span>대상 고객</span><span class="wg-08-price">필수</span></li><li><span>근거 자료</span><span class="wg-08-price">권장</span></li></ul><a class="wg-08-cta" href="#launchbrief-brief">brief 만들기 →</a></article><article id="launchbrief-brief" class="wg-08-screen" tabindex="-1" aria-label="화면 B: 판단 brief"><header class="wg-08-shead"><span class="wg-08-badge">화면 B</span><h3>판단 brief</h3></header><fieldset class="wg-08-pick"><legend class="wg-08-legend">검토할 기준</legend><label><span class="wg-08-dot" aria-hidden="true"></span>약속이 한 문장인가</label><label><span class="wg-08-dot" aria-hidden="true"></span>검증된 근거가 있는가</label><label><span class="wg-08-dot" aria-hidden="true"></span>금지 표현이 표시됐는가</label></fieldset><div class="wg-08-nav"><a class="wg-08-back" href="#launchbrief-input">← 뒤로</a><a class="wg-08-cta" href="#launchbrief-pack">채널 패키지 →</a></div></article><article id="launchbrief-pack" class="wg-08-screen" tabindex="-1" aria-label="화면 C: 출시 패키지"><header class="wg-08-shead"><span class="wg-08-badge wg-08-badge--ok">화면 C</span><h3>출시 패키지</h3></header><div class="wg-08-ok"><span class="wg-08-check" aria-hidden="true">✓</span><p>앱스토어, 블로그, 이메일, 릴리스 노트 초안이 같은 brief에서 생성됩니다.<br><span class="wg-08-order">검토 ID LB-20260607-015</span></p></div><a class="wg-08-back" href="#launchbrief-input">처음으로 돌아가기</a></article></div></div>
  <p class="wg-08-hint">상단 단계 또는 화면 내 버튼을 눌러 입력 → brief → 패키지 흐름을 확인합니다. (:target 기반)</p>
</div>'''


def build_mapping() -> dict[str, str]:
    hero = f'''{h2(1, "Hero", "landing", "LaunchBrief Studio는 출시 메시지를 빠르게 쓰는 도구가 아니라, 출시 전 팀의 판단을 한 장으로 정렬하는 도구입니다.")}
<p><strong>LaunchBrief Studio</strong>는 작은 제품팀이 출시 직전 흩어진 메시지를 하나의 brief로 고정하고, 그 brief에서 채널별 문구를 안전하게 뽑아내도록 돕는 editorial landing 도구입니다.</p>
<p>대상 독자는 기능은 준비됐지만 “무엇을 누구에게 어떤 근거로 말해야 하는가”에서 흔들리는 PM, 마케터, 창업팀입니다. 효과 수치나 비교 우위가 확인되지 않았다면 문구에 바로 쓰지 않고 확인 필요로 표시합니다.</p>
{vt_hero_map()}'''

    values = f'''{h2(2, "Value Props", "impact", "핵심 가치는 더 많은 문구가 아니라, 더 적은 혼선과 더 명확한 승인 기준입니다.")}
<div class="grid"><article class="mini-card"><h3>한 줄 약속 고정</h3><p>출시 메시지의 중심 문장을 먼저 정합니다. 팀원이 채널별 문구를 써도 같은 약속을 유지합니다.</p></article><article class="mini-card"><h3>근거와 제한 함께 기록</h3><p>무엇을 말할 수 있고 무엇은 아직 확인 필요인지 분리합니다. 과장 문구가 초안에 섞이는 것을 줄입니다.</p></article><article class="mini-card"><h3>채널별 초안 분리</h3><p>앱스토어, 블로그, 이메일, 릴리스 노트의 길이와 톤을 다르게 가져가되 같은 brief를 출처로 둡니다.</p></article><article class="mini-card"><h3>승인 경로 단순화</h3><p>제품, 마케팅, 지원, 법무가 서로 다른 파일을 보는 대신 같은 판단 문서를 기준으로 검토합니다.</p></article><article class="mini-card"><h3>금지 표현 표시</h3><p>확인되지 않은 수치, 경쟁사 비교, 법적 위험 문구를 승인 전 체크 항목으로 표시합니다.</p></article><article class="mini-card"><h3>출시 후 재사용</h3><p>한 번 만든 brief는 FAQ, 고객지원 답변, 회고 문서의 원본으로 재사용할 수 있습니다.</p></article></div>
{vt_card_grid()}'''

    how = f'''{h2(3, "How it works", "flow", "입력 → 판단 brief → 채널 패키지 → 검토 플래그의 흐름으로 출시 메시지를 정리합니다.")}
<div class="grid-2"><article class="summary-card"><h3>1. 입력을 모은다</h3><p>기능 요약, 고객 문제, 화면 변화, 제한 사항, 근거 자료를 한 곳에 모읍니다.</p></article><article class="summary-card"><h3>2. 판단을 고정한다</h3><p>대상, 약속, 근거, 금지 표현, 확인 필요 항목을 먼저 씁니다.</p></article><article class="summary-card"><h3>3. 채널별로 변환한다</h3><p>같은 brief를 앱스토어 문구, 블로그 도입부, 이메일 제목, 릴리스 노트로 나눕니다.</p></article><article class="summary-card"><h3>4. 검토 플래그로 닫는다</h3><p>승인된 주장만 ON, 확인 중인 주장은 WARN, 검증 없는 문구는 OFF로 표시합니다.</p></article></div>
{wg_clickable_flow()}
{vt_soft_workflow()}
{vt_feature_flag()}'''

    faq = f'''{h2(4, "FAQ", "question", "LaunchBrief Studio는 자동 카피라이터보다 출시 판단 문서에 가깝습니다.")}
<div class="grid-2"><article class="summary-card"><h3>카피를 자동으로 써주나요?</h3><p>초안은 만들 수 있지만 핵심은 자동 문구가 아니라 brief입니다. 확인된 근거와 금지 표현을 먼저 고정해야 안전합니다.</p></article><article class="summary-card"><h3>마케팅팀만 쓰나요?</h3><p>아닙니다. PM, 디자인, 고객지원, 세일즈가 같은 출시 약속을 공유해야 할 때 가장 유용합니다.</p></article><article class="summary-card"><h3>성과 수치를 넣어도 되나요?</h3><p>검증된 수치만 넣습니다. 확인되지 않은 효과, 비교 우위, 고객 수치는 확인 필요 상태로 남겨야 합니다.</p></article><article class="summary-card"><h3>작은 팀에도 필요한가요?</h3><p>작은 팀일수록 출시 직전 문구가 빠르게 바뀝니다. 한 장의 brief가 있으면 마지막 48시간의 혼선을 줄일 수 있습니다.</p></article></div>'''

    cta = f'''{h2(5, "CTA", "success", "다음 출시에서 바로 시작하려면 새 도구보다 먼저 하나의 brief 양식을 정하면 됩니다.")}
<div class="card-grid"><article class="summary-card"><h3>오늘 만들 brief</h3><p>대상 고객, 한 줄 약속, 검증된 근거, 금지 표현, 채널별 산출물을 한 화면에 적습니다.</p></article><article class="summary-card"><h3>첫 검토 기준</h3><p>확인되지 않은 성과 수치가 없는지, 고객에게 약속한 행동이 실제 제품에서 가능한지 확인합니다.</p></article><article class="summary-card"><h3>출시 후 재사용</h3><p>brief를 버리지 말고 FAQ, 고객지원 답변, 회고 문서의 기준으로 보관합니다.</p></article></div>'''

    return {
        "{{KICKER}}": "Landing Brief · Launch Messaging",
        "{{TITLE}}": "LaunchBrief Studio: 출시 메시지를 한 장의 판단 문서로",
        "{{SUBTITLE}}": "작은 팀이 기능 출시 전 대상, 약속, 근거, 금지 표현, 채널별 문구를 한 brief에서 정렬하도록 돕는 절제된 editorial landing입니다.",
        "{{META}}": '<div class="generated-row"><span>작성일 · 2026-06-07</span><span>mode · landing_brief_html</span><span>profile · auto</span><span>audience · small product teams</span></div><div class="lens-strip"><span>hero</span><span>value props</span><span>workflow</span><span>FAQ</span><span>CTA</span></div>',
        "{{HERO}}": hero,
        "{{VALUE_PROPS}}": values,
        "{{HOW_IT_WORKS}}": how,
        "{{FAQ}}": faq,
        "{{CTA}}": cta,
        "{{SOURCE_NOTE}}": '<strong>Source note.</strong> 이 랜딩 브리프는 특정 상용 제품의 실제 성과나 고객 수치를 주장하지 않는 컨셉 문서입니다. 효과 수치, 경쟁 제품 비교, 법적 표현은 실제 출시 전 별도 검증이 필요합니다.',
    }


def render() -> None:
    material_hashes = {}
    for rel in MODE_MATERIALS:
        p = SKILL / rel
        if not p.exists():
            raise FileNotFoundError(rel)
        material_hashes[rel] = sha_bytes(p)

    base = read(ASSETS / "base.html")
    layout = read(ASSETS / "layouts" / "landing-brief.html")
    for k, v in build_mapping().items():
        layout = layout.replace(k, v)
    remaining = sorted(set(re.findall(r"{{[A-Z0-9_]+}}", layout)))
    if remaining:
        raise RuntimeError(f"unfilled layout placeholders: {remaining}")

    css = {name: read(ASSETS / name) for name in CSS_ORDER}
    core_hash = hashlib.sha256("\n".join(css[name] for name in CORE).encode("utf-8")).hexdigest()
    css["theme.css"] = f"/* adaptive-html-final-core-css-sha256: {core_hash} */\n" + css["theme.css"]

    html = base
    html = html.replace("{{TITLE}}", "LaunchBrief Studio: 출시 메시지를 한 장의 판단 문서로")
    html = html.replace("{{DESCRIPTION}}", "landing_brief_html 모드로 작성한 LaunchBrief Studio 랜딩 브리프. Hero, Value Props, How it works, FAQ, CTA를 포함합니다.")
    html = html.replace("{{JSON_LD_BLOCK}}", "")
    html = html.replace("{{BODY}}", layout)
    html = html.replace("{{FOOTER}}", "")
    slot_map = {
        "{{THEME_CSS}}": css["theme.css"],
        "{{COMPONENTS_CSS}}": css["components.css"],
        "{{VISUAL_COMPONENTS_CSS}}": css["visual-components.css"],
        "{{WIDGETS_CSS}}": css["widgets.css"],
        "{{VISUAL_HTML_CSS}}": css["visual-html.css"],
        "{{BODY_ICONS_CSS}}": css["body-icons.css"],
        "{{EDITORIAL_PATTERNS_CSS}}": css["editorial-patterns.css"],
        "{{SHAPE_VISUALS_CSS}}": css["shape-visuals.css"],
        "{{WORKFLOW_VISUALS_CSS}}": css["workflow-visuals.css"],
        "{{LAYOUTS_CSS}}": css["layouts.css"],
        "{{PRINT_CSS}}": css["print.css"],
        "{{THEME_DARK_CSS}}": css["theme-dark.css"],
    }
    for slot, value in slot_map.items():
        html = html.replace(slot, value)
    if "{{" in html:
        raise RuntimeError("unfilled base placeholders")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(html, encoding="utf-8")

    SNAP.mkdir(parents=True, exist_ok=True)
    asset_sha = {}
    for name in CSS_ORDER:
        raw = read(ASSETS / name)
        (SNAP / name).write_text(raw, encoding="utf-8")
        asset_sha[name] = hashlib.sha256(raw.encode("utf-8")).hexdigest()
    (SOURCES / "profile.json").write_text(json.dumps({"profile": "auto"}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (SOURCES / "adaptive-html-final-manifest.json").write_text(json.dumps(json.loads(read(SKILL / "manifest.json")), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    integrity_path = SOURCES / "css-integrity.json"
    prior = {}
    if integrity_path.exists():
        try:
            prior = json.loads(integrity_path.read_text(encoding="utf-8"))
        except Exception:
            prior = {}
    prior.update({
        "core_css_sha256": core_hash,
        "asset_order": CORE,
        "asset_sha256": asset_sha,
        "profile": "auto",
        "mode15_material_sha256": material_hashes,
        "updated_at": datetime.now(timezone.utc).isoformat(),
    })
    integrity_path.write_text(json.dumps(prior, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    render()
    print(OUT)
