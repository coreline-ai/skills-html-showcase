#!/usr/bin/env python3
"""Render mode 16 checklist_playbook only for sequential QA.

No previous HTML body is read; no shared/common generator is imported.
The script reads only checklist layout/recipe/references and checklist-relevant vt/wg templates.
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
OUT = ROOT / "pages" / "16_checklist_feature_flag_release_safety_playbook.html"
SOURCES = ROOT / "sources"
SNAP = SOURCES / "assets"

MODE_MATERIALS = [
    "SKILL.md",
    "recipes/checklist.prompt.md",
    "assets/layouts/checklist-playbook.html",
    "references/layout-system.md",
    "references/writing-system.md",
    "references/quality-gates.md",
    "references/body-icon-system.md",
    "references/visual-html-system.md",
    "references/widget-system.md",
    "assets/visual-html-templates/05-checklist-flow.html",
    "assets/visual-html-templates/06-quality-gate.html",
    "assets/visual-html-templates/14-process-swimlane.html",
    "assets/visual-html-templates/16-implementation-plan.html",
    "assets/visual-html-templates/18-triage-board.html",
    "assets/widget-templates/13-annotated-flowchart.html",
    "assets/widget-templates/19-feature-flag-editor.html",
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


def vt_checklist_flow() -> str:
    return '''<section class="vt-shell" aria-label="feature flag release checklist flow">
  <div class="vt-frame">
    <div class="cf"><div class="cf-item"><span class="cf-check">✓</span><div><b>owner 확인</b><p class="vt-text">플래그 책임자와 승인자가 명확해야 합니다.</p></div><span class="cf-state">PASS</span></div><div class="cf-item"><span class="cf-check">✓</span><div><b>rollback 경로</b><p class="vt-text">운영자가 즉시 off로 돌리는 방법을 알아야 합니다.</p></div><span class="cf-state">PASS</span></div><div class="cf-item"><span class="cf-check">✓</span><div><b>cleanup 이슈</b><p class="vt-text">100% 이후 제거할 코드와 설정을 미리 등록합니다.</p></div><span class="cf-state">PASS</span></div></div>
  </div>
</section>'''


def vt_quality_gate() -> str:
    return '''<section class="vt-shell" aria-label="feature flag release quality gate">
  <div class="vt-frame">
    <div><div class="qg-grid"><div class="qg-card"><b>기본값</b><p class="vt-text">평가 실패 시 안전한 default로 돌아감</p></div><div class="qg-card"><b>권한</b><p class="vt-text">대상 segment와 제외 조건 검증</p></div><div class="qg-card warn"><b>지표</b><p class="vt-text">확대/중단 기준이 숫자로 적힘</p></div><div class="qg-card block"><b>차단</b><p class="vt-text">owner·rollback 없으면 출시 금지</p></div></div><div class="qg-final">PRE-FLIGHT: 플래그를 켜기 전에 실패했을 때 누가 무엇을 끌지 먼저 확인</div></div>
  </div>
</section>'''


def vt_swimlane() -> str:
    return '''<section class="vt-shell" aria-label="feature flag release swimlane">
  <div class="vt-frame">
    <div class="swim"><div class="lane"><div class="lane-label">PM</div><div class="lane-step">목표·대상</div><div class="lane-step">승인 기준</div><div class="lane-step blank">—</div><div class="lane-step">고객 공지</div></div><div class="lane"><div class="lane-label">Eng</div><div class="lane-step">기본값</div><div class="lane-step">segment</div><div class="lane-step">rollback</div><div class="lane-step">cleanup PR</div></div><div class="lane"><div class="lane-label">QA</div><div class="lane-step">OFF 검증</div><div class="lane-step">ON 검증</div><div class="lane-step">경계값</div><div class="lane-step blank">—</div></div><div class="lane"><div class="lane-label">Ops</div><div class="lane-step blank">—</div><div class="lane-step">알림</div><div class="lane-step">모니터링</div><div class="lane-step">회고</div></div></div>
  </div>
</section>'''


def vt_implementation_plan() -> str:
    return '''<section class="vt-shell" aria-label="feature flag release implementation plan">
  <div class="vt-frame">
    <div class="plan-grid"><article class="milestone"><div class="vt-kicker">M0</div><b>등록</b><p class="vt-text">owner, default, expiry, metric을 등록합니다.</p></article><article class="milestone"><div class="vt-kicker">M1</div><b>내부 검증</b><p class="vt-text">직원·테스트 계정에서 OFF/ON 모두 확인합니다.</p></article><article class="milestone plan-risk"><div class="vt-kicker">M2</div><b>카나리</b><p class="vt-text">1%→5%→25%에서 지표를 확인합니다.</p></article><article class="milestone"><div class="vt-kicker">M3</div><b>정리</b><p class="vt-text">100% 안정 후 분기 코드와 설정을 제거합니다.</p></article></div>
  </div>
</section>'''


def vt_triage_board() -> str:
    return '''<section class="vt-shell" aria-label="feature flag triage board">
  <div class="vt-frame">
    <div class="board"><div class="board-col"><h3>출시 전</h3><div class="ticket">owner 누락 확인</div><div class="ticket">지표 기준 작성</div></div><div class="board-col"><h3>진행 중</h3><div class="ticket active">카나리 5% 관찰</div><div class="ticket active">지원팀 FAQ 준비</div></div><div class="board-col"><h3>완료</h3><div class="ticket">rollback runbook</div><div class="ticket">cleanup issue</div></div></div>
  </div>
</section>'''


def wg_flowchart() -> str:
    return '''<div class="wg-13-fc" aria-label="피처 플래그 출시 플로우차트">
  <h3 class="wg-13-h">플래그 출시 플로우 <span class="wg-13-sub">승인 전 점검 → 카나리 → 정리</span></h3>
  <div class="wg-13-flow"><a href="#flag-flow-start" class="wg-13-node wg-13-node--start"><span class="wg-13-step">시작</span>플래그 등록</a><span class="wg-13-arrow" aria-hidden="true">↓</span><a href="#flag-flow-gate" class="wg-13-node"><span class="wg-13-step">1</span>기본값·owner 확인</a><span class="wg-13-arrow" aria-hidden="true">↓</span><div class="wg-13-branch"><a href="#flag-flow-decide" class="wg-13-node wg-13-node--decide"><span class="wg-13-step">2</span>출시 기준 통과?</a><div class="wg-13-paths"><div class="wg-13-path wg-13-path--fail"><span class="wg-13-edge">아니오 → 실패 경로</span><a href="#flag-flow-stop" class="wg-13-node wg-13-node--fail"><span class="wg-13-step">!</span>출시 보류</a></div><div class="wg-13-path wg-13-path--ok"><span class="wg-13-edge">예 → 정상 경로</span><a href="#flag-flow-canary" class="wg-13-node"><span class="wg-13-step">3</span>카나리 확대</a><span class="wg-13-arrow" aria-hidden="true">↓</span><a href="#flag-flow-done" class="wg-13-node wg-13-node--end"><span class="wg-13-step">완료</span>cleanup 예약</a></div></div></div></div>
  <div class="wg-13-detail"><h4 class="wg-13-dh">단계 상세 <span class="wg-13-dnote">박스를 클릭하면 해당 단계 설명으로 이동합니다</span></h4><details id="flag-flow-gate" class="wg-13-acc" open><summary><span class="wg-13-tag">1단계</span>기본값·owner 확인</summary><div class="wg-13-body"><p>default는 안전값이어야 하며 owner와 승인자가 서로 달라야 합니다.</p></div></details><details id="flag-flow-decide" class="wg-13-acc"><summary><span class="wg-13-tag">2단계</span>출시 기준 판단</summary><div class="wg-13-body"><p>오류율, 전환율, 고객 문의 기준이 없으면 카나리로 넘어가지 않습니다.</p></div></details><details id="flag-flow-stop" class="wg-13-acc wg-13-acc--fail"><summary><span class="wg-13-tag wg-13-tag--fail">실패</span>출시 보류</summary><div class="wg-13-body"><p>누락 항목을 보완하고 새 승인 기록을 남긴 뒤 다시 시작합니다.</p></div></details><details id="flag-flow-canary" class="wg-13-acc"><summary><span class="wg-13-tag">3단계</span>카나리 확대</summary><div class="wg-13-body"><p>1% → 5% → 25% → 100%로 늘리며 각 단계마다 관찰 시간을 둡니다.</p></div></details><details id="flag-flow-done" class="wg-13-acc wg-13-acc--ok"><summary><span class="wg-13-tag wg-13-tag--ok">완료</span>cleanup 예약</summary><div class="wg-13-body"><p>100% 안정 후 분기 코드와 설정 제거 PR을 열어 플래그 수명을 닫습니다.</p></div></details></div>
</div>'''


def wg_flag_editor() -> str:
    return '''<div class="wg-19-editor" aria-label="피처 플래그 출시 토글 편집기">
  <header class="wg-19-head"><h3 class="wg-19-title">운영 토글 상태</h3><p class="wg-19-hint">토글은 시각 전환만 제공하며 저장·export는 JS가 필요한 점진 향상 영역입니다.</p></header>
  <ul class="wg-19-list"><li class="wg-19-row"><div class="wg-19-info"><span class="wg-19-key">release_safety_gate</span><span class="wg-19-desc">owner·rollback·metric 누락 시 출시 차단</span></div><span class="wg-19-env">prod</span><input class="wg-19-cb" type="checkbox" id="flag-safe-1" checked><label class="wg-19-toggle" for="flag-safe-1"><span class="wg-19-knob"></span><span class="wg-19-state wg-19-state--on">ON</span><span class="wg-19-state wg-19-state--off">OFF</span></label></li><li class="wg-19-row"><div class="wg-19-info"><span class="wg-19-key">canary_auto_expand</span><span class="wg-19-desc">지표 통과 시 자동 확대 후보</span><span class="wg-19-dep" role="note">⚠ 수동 승인 필요</span></div><span class="wg-19-env wg-19-env--stg">staging</span><input class="wg-19-cb" type="checkbox" id="flag-safe-2"><label class="wg-19-toggle" for="flag-safe-2"><span class="wg-19-knob"></span><span class="wg-19-state wg-19-state--on">ON</span><span class="wg-19-state wg-19-state--off">OFF</span></label></li><li class="wg-19-row"><div class="wg-19-info"><span class="wg-19-key">unowned_flag_rollout</span><span class="wg-19-desc">owner 없는 플래그 확대</span><span class="wg-19-dep wg-19-dep--warn" role="note">⚠ 출시 금지</span></div><span class="wg-19-env">prod</span><input class="wg-19-cb" type="checkbox" id="flag-safe-3"><label class="wg-19-toggle" for="flag-safe-3"><span class="wg-19-knob"></span><span class="wg-19-state wg-19-state--on">ON</span><span class="wg-19-state wg-19-state--off">OFF</span></label></li></ul>
  <footer class="wg-19-foot"><button class="wg-19-export" type="button" disabled aria-disabled="true">승인 로그 내보내기 (JS 필요)</button></footer>
</div>'''


def build_mapping() -> dict[str, str]:
    use_case = f'''{h2(1, "Use Case", "check", "이 플레이북은 기능 플래그를 켜기 전 PM, 엔지니어, QA, 온콜이 같은 기준으로 출시 가능 여부를 판단할 때 사용합니다.")}
<p>기능 플래그는 안전한 출시를 돕지만, owner와 rollback 기준 없이 켜면 운영 위험을 숨긴 조건문이 됩니다. 이 체크리스트는 플래그를 새로 만들 때, 카나리 비율을 올릴 때, 100% 전환 후 cleanup을 닫을 때 사용합니다.</p>
<div class="grid-2"><article class="mini-card"><h3>사용 시점</h3><p>새 플래그 등록, beta 확대, prod 25% 이상 전환, 100% 이후 코드 제거 전입니다.</p></article><article class="mini-card"><h3>사용자</h3><p>PM은 목표와 고객 공지를 확인하고, 엔지니어는 default·segment·rollback을 확인합니다. QA와 온콜은 실패 경로를 확인합니다.</p></article></div>
{wg_flag_editor()}
{vt_checklist_flow()}'''

    check_grid = f'''{h2(2, "Check Grid", "audit", "각 항목은 통과/실패를 판단할 수 있어야 하며, 확인 필요 항목은 출시 보류로 처리합니다.")}
<div class="grid"><article class="summary-card"><h3>기본값</h3><p><strong>통과:</strong> 평가 실패 시 안전한 OFF 또는 보수값으로 돌아갑니다. <strong>실패:</strong> 기본값이 기능 ON이거나 문서에 없습니다.</p></article><article class="summary-card"><h3>소유자</h3><p><strong>통과:</strong> 변경 승인자와 incident owner가 명시됩니다. <strong>실패:</strong> “팀 전체”처럼 책임이 흐립니다.</p></article><article class="summary-card"><h3>대상 segment</h3><p><strong>통과:</strong> 내부, beta, region, paid tier 등 조건이 재현 가능합니다. <strong>실패:</strong> 수동 쿼리 결과만 남아 있습니다.</p></article><article class="summary-card"><h3>관찰 지표</h3><p><strong>통과:</strong> 오류율, 전환율, 문의량 중 확대/중단 기준이 있습니다. <strong>실패:</strong> “문제 없으면 확대”만 적혀 있습니다.</p></article><article class="summary-card"><h3>rollback</h3><p><strong>통과:</strong> 누가 어디서 즉시 OFF로 돌릴지 알고 있습니다. <strong>실패:</strong> 배포 롤백만 유일한 대응입니다.</p></article><article class="summary-card"><h3>cleanup</h3><p><strong>통과:</strong> 100% 후 제거할 코드·설정·문서 이슈가 있습니다. <strong>실패:</strong> 완료 후 삭제 계획이 없습니다.</p></article></div>
{wg_flowchart()}
{vt_quality_gate()}
{vt_swimlane()}'''

    failure = f'''{h2(3, "Failure Modes", "warning", "플래그 사고는 대부분 토글 자체보다 책임, 관찰, 삭제 계획이 빠질 때 발생합니다.")}
<div class="card-grid"><article class="danger"><h3>owner 없는 확대</h3><p>누가 승인했는지 모르면 문제가 생겨도 되돌릴 사람이 없습니다. 확대 전에 owner와 backup owner를 모두 기록합니다.</p></article><article class="danger"><h3>segment 오해</h3><p>beta만 켠다고 생각했지만 region 또는 plan 조건이 겹쳐 더 넓게 노출될 수 있습니다. 대상 샘플을 검증합니다.</p></article><article class="danger"><h3>관찰 없는 100%</h3><p>지표 없이 전체 전환하면 성공처럼 보이다가 문의량 증가로 늦게 발견됩니다. 확대 단계별 관찰 시간을 둡니다.</p></article><article class="danger"><h3>영구 플래그화</h3><p>100% 이후 분기 코드가 남으면 제품 로직이 복잡해집니다. cleanup PR이 없으면 완료로 보지 않습니다.</p></article></div>
{vt_implementation_plan()}
{vt_triage_board()}'''

    done = f'''{h2(4, "Done Criteria", "success", "완료는 플래그가 켜진 상태가 아니라 안전하게 켜고, 관찰하고, 정리할 준비가 끝난 상태입니다.")}
<div class="card-grid"><article class="summary-card"><h3>출시 전 완료</h3><p>owner, default, segment, metric, rollback, cleanup issue가 모두 문서화되어 있습니다.</p></article><article class="summary-card"><h3>카나리 완료</h3><p>각 확대 단계에서 오류율·전환·문의량 기준을 확인했고, 보류 조건이 없었습니다.</p></article><article class="summary-card"><h3>운영 완료</h3><p>온콜이 즉시 OFF 경로를 알고 있으며 감사 로그에 변경 사유가 남습니다.</p></article><article class="summary-card"><h3>정리 완료</h3><p>100% 안정 이후 분기 코드와 설정 제거 PR이 머지되고 문서가 갱신됩니다.</p></article></div>'''

    return {
        "{{KICKER}}": "Checklist Playbook · Feature Flag Release",
        "{{TITLE}}": "Feature Flag Release Safety Playbook",
        "{{SUBTITLE}}": "기능 플래그를 켜기 전 owner, default, segment, metric, rollback, cleanup을 같은 기준으로 확인하는 운영 체크리스트입니다.",
        "{{META}}": '<div class="generated-row"><span>작성일 · 2026-06-07</span><span>mode · checklist_playbook</span><span>profile · auto</span><span>scope · release safety</span></div><div class="lens-strip"><span>use case</span><span>check grid</span><span>failure modes</span><span>done criteria</span></div>',
        "{{USE_CASE}}": use_case,
        "{{CHECK_GRID}}": check_grid,
        "{{FAILURE_MODES}}": failure,
        "{{DONE_CRITERIA}}": done,
        "{{SOURCE_NOTE}}": '<strong>Source note.</strong> 이 플레이북은 기능 플래그 출시 안전 점검을 위한 벤더 중립 운영 절차입니다. 실제 플래그 시스템의 권한 모델, 감사 로그, SDK 동작은 각 조직의 런북과 제품 문서로 확인해야 합니다.',
    }


def render() -> None:
    material_hashes = {}
    for rel in MODE_MATERIALS:
        p = SKILL / rel
        if not p.exists():
            raise FileNotFoundError(rel)
        material_hashes[rel] = sha_bytes(p)

    base = read(ASSETS / "base.html")
    layout = read(ASSETS / "layouts" / "checklist-playbook.html")
    for k, v in build_mapping().items():
        layout = layout.replace(k, v)
    remaining = sorted(set(re.findall(r"{{[A-Z0-9_]+}}", layout)))
    if remaining:
        raise RuntimeError(f"unfilled layout placeholders: {remaining}")

    css = {name: read(ASSETS / name) for name in CSS_ORDER}
    core_hash = hashlib.sha256("\n".join(css[name] for name in CORE).encode("utf-8")).hexdigest()
    css["theme.css"] = f"/* adaptive-html-final-core-css-sha256: {core_hash} */\n" + css["theme.css"]

    html = base
    html = html.replace("{{TITLE}}", "Feature Flag Release Safety Playbook")
    html = html.replace("{{DESCRIPTION}}", "checklist_playbook 모드로 작성한 기능 플래그 출시 안전 플레이북. Use Case, Check Grid, Failure Modes, Done Criteria를 포함합니다.")
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
        "mode16_material_sha256": material_hashes,
        "updated_at": datetime.now(timezone.utc).isoformat(),
    })
    integrity_path.write_text(json.dumps(prior, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    render()
    print(OUT)
