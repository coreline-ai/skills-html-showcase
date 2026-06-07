#!/usr/bin/env python3
"""Render mode 12 reference_html only for sequential QA.

No previous HTML body is read; no shared/common generator is imported.
The script reads only reference layout/recipe/references and reference-relevant vt/wg templates.
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
OUT = ROOT / "pages" / "12_reference_feature_flag_lifecycle_manual.html"
SOURCES = ROOT / "sources"
SNAP = SOURCES / "assets"

MODE_MATERIALS = [
    "SKILL.md",
    "recipes/reference.prompt.md",
    "assets/layouts/reference-manual.html",
    "references/layout-system.md",
    "references/writing-system.md",
    "references/quality-gates.md",
    "references/body-icon-system.md",
    "references/visual-html-system.md",
    "references/widget-system.md",
    "assets/visual-html-templates/09-file-tour.html",
    "assets/visual-html-templates/10-flowchart.html",
    "assets/visual-html-templates/07-card-grid.html",
    "assets/widget-templates/06-component-variants.html",
    "assets/widget-templates/14-feature-explainer.html",
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


def vt_file_tour() -> str:
    return '''<section class="vt-shell" aria-label="feature flag 파일 투어">
  <div class="vt-frame">
    <div class="ft"><article class="ft-card"><div class="ft-head"><span>flags.yml</span><span>contract</span></div><div class="ft-body"><p class="vt-text">flag key, owner, default, expiry, kill-switch 여부를 한 곳에 둡니다.</p><div class="ft-note"><b>Review note</b><br>owner와 expiry가 없으면 신규 플래그 등록을 막습니다.</div></div></article><article class="ft-card"><div class="ft-head"><span>segments.yml</span><span>target</span></div><div class="ft-body"><p class="vt-text">internal, beta, region, paid tier 같은 대상 조건을 분리합니다.</p><div class="ft-note"><b>Review note</b><br>개인정보 원문 대신 해시·속성명만 기록합니다.</div></div></article><article class="ft-card"><div class="ft-head"><span>flag-audit.log</span><span>proof</span></div><div class="ft-body"><p class="vt-text">누가 언제 비율을 바꿨는지, 어떤 지표를 확인했는지 남깁니다.</p><div class="ft-note"><b>Review note</b><br>감사 로그 없는 100% 전환은 승인하지 않습니다.</div></div></article></div>
  </div>
</section>'''


def vt_flowchart() -> str:
    return '''<section class="vt-shell" aria-label="flag lifecycle flowchart">
  <div class="vt-frame">
    <div class="fc"><div class="fc-node"><b>등록</b><p class="vt-text">owner·기본값·만료일</p></div><div class="fc-arrow">→</div><div class="fc-node"><b>내부</b><p class="vt-text">직원/테스트 계정만</p></div><div class="fc-arrow">→</div><div class="fc-node hot"><b>카나리</b><p class="vt-text">1%·5%·25%</p></div><div class="fc-arrow">→</div><div class="fc-node"><b>전체</b><p class="vt-text">지표 안정 후 100%</p></div><div class="fc-arrow">→</div><div class="fc-node"><b>삭제</b><p class="vt-text">코드·설정 제거</p></div></div>
  </div>
</section>'''


def vt_card_grid() -> str:
    return '''<section class="vt-shell" aria-label="reference quick map">
  <div class="vt-frame">
    <div class="cg-grid"><article class="cg-card"><em>01</em><b>Key</b><p>한 번 정하면 바꾸지 않는 식별자</p></article><article class="cg-card"><em>02</em><b>Default</b><p>평가 실패 시 돌아갈 안전값</p></article><article class="cg-card"><em>03</em><b>Owner</b><p>비율 변경과 삭제 책임자</p></article><article class="cg-card"><em>04</em><b>Segment</b><p>대상 사용자 조건 묶음</p></article><article class="cg-card"><em>05</em><b>Metric</b><p>진행·중단 판단 지표</p></article><article class="cg-card"><em>06</em><b>Expiry</b><p>코드 제거 예정일</p></article></div>
  </div>
</section>'''


def wg_component_variants() -> str:
    return '''<div class="wg-06-cs" aria-labelledby="flag-variant-title">
  <header class="wg-06-head"><p class="wg-06-kicker">COMPONENT CONTACT SHEET</p><h3 id="flag-variant-title" class="wg-06-h">플래그 상태 변형 매트릭스</h3><p class="wg-06-lead">운영 UI에서 같은 플래그라도 Draft, Canary, On, Retiring 상태에 따라 허용되는 버튼과 설명 문구가 달라집니다.</p></header>
  <fieldset class="wg-06-density"><legend class="wg-06-density-leg">배경 토글</legend><input type="radio" name="wg-06-flag-bg" id="wg-06-flag-bg-light" class="wg-06-bg-input" checked><label for="wg-06-flag-bg-light" class="wg-06-bg-label">라이트</label><input type="radio" name="wg-06-flag-bg" id="wg-06-flag-bg-dark" class="wg-06-bg-input"><label for="wg-06-flag-bg-dark" class="wg-06-bg-label">다크</label></fieldset>
  <div class="wg-06-sheet table-scroll"><table class="wg-06-table"><caption class="wg-06-cap">행 = 플래그 상태 · 열 = 운영자가 볼 기본 액션</caption><thead><tr><th scope="col" class="wg-06-rowhead">Status</th><th scope="col">Primary</th><th scope="col">Review</th><th scope="col">Blocked</th></tr></thead><tbody><tr><th scope="row" class="wg-06-rowhead">Draft</th><td><span class="wg-06-stack"><button type="button" class="wg-06-btn wg-06-btn--primary wg-06-md">검토 요청</button><span class="wg-06-statetag">owner required</span></span></td><td><span class="wg-06-stack"><button type="button" class="wg-06-btn wg-06-btn--secondary wg-06-md">초안 저장</button><span class="wg-06-statetag">safe</span></span></td><td><span class="wg-06-stack"><button type="button" class="wg-06-btn wg-06-btn--danger wg-06-md" disabled>롤아웃</button><span class="wg-06-statetag">missing expiry</span></span></td></tr><tr><th scope="row" class="wg-06-rowhead">Canary</th><td><span class="wg-06-stack"><button type="button" class="wg-06-btn wg-06-btn--primary wg-06-md wg-06-is-hover">25%로 확대</button><span class="wg-06-statetag">metric pass</span></span></td><td><span class="wg-06-stack"><button type="button" class="wg-06-btn wg-06-btn--secondary wg-06-md">지표 보기</button><span class="wg-06-statetag">watch</span></span></td><td><span class="wg-06-stack"><button type="button" class="wg-06-btn wg-06-btn--danger wg-06-md">즉시 OFF</button><span class="wg-06-statetag">kill switch</span></span></td></tr><tr><th scope="row" class="wg-06-rowhead">On</th><td><span class="wg-06-stack"><button type="button" class="wg-06-btn wg-06-btn--primary wg-06-md">삭제 PR 생성</button><span class="wg-06-statetag">cleanup</span></span></td><td><span class="wg-06-stack"><button type="button" class="wg-06-btn wg-06-btn--secondary wg-06-md wg-06-is-focus">감사 로그</button><span class="wg-06-statetag">focus ring</span></span></td><td><span class="wg-06-stack"><button type="button" class="wg-06-btn wg-06-btn--danger wg-06-md">되돌리기</button><span class="wg-06-statetag">rollback window</span></span></td></tr></tbody></table></div>
  <p class="wg-06-foot">이 매트릭스는 운영 버튼의 실제 서버 동작을 구현하지 않습니다. 레퍼런스 문서 안에서 상태별 허용 액션을 정적으로 비교하기 위한 무 JS contact sheet입니다.</p>
</div>'''


def wg_feature_explainer() -> str:
    return '''<div class="wg-14" aria-labelledby="flag-example-title">
  <p class="wg-14-kicker">기능 안내 · lifecycle API</p>
  <h3 id="flag-example-title" class="wg-14-h">플래그 등록부터 삭제까지의 최소 계약</h3>
  <p class="wg-14-lead">아래 예시는 특정 서비스의 실제 API가 아니라, 기능 플래그 문서에 포함해야 할 필드와 검증 흐름을 설명하는 의사 계약입니다.</p>
  <div class="wg-14-tldr" role="note" aria-label="핵심 요약"><span class="wg-14-tldr-tag">TL;DR</span><p class="wg-14-tldr-body"><strong>owner, default, expiry, metric, rollback</strong>이 없으면 플래그는 출시 장치가 아니라 임시 분기 코드가 됩니다.</p></div>
  <div class="wg-14-acc"><details class="wg-14-sec" open><summary class="wg-14-sum"><span class="wg-14-sum-no">01</span> 무엇을 문서화하나요 <span class="wg-14-chev" aria-hidden="true"></span></summary><div class="wg-14-sec-body"><p>플래그 이름보다 중요한 것은 누가 책임지고 언제 삭제할지입니다. 문서는 평가 조건, 기본값, 실패 시 행동, 삭제 예정일을 함께 적어야 합니다.</p><ul class="wg-14-list"><li>flag key와 owner를 분리합니다.</li><li>기본값은 장애 상황에서도 안전한 방향으로 둡니다.</li><li>cleanup issue를 등록 시점에 만듭니다.</li></ul></div></details><details class="wg-14-sec"><summary class="wg-14-sum"><span class="wg-14-sum-no">02</span> 어떤 순서로 적용하나요 <span class="wg-14-chev" aria-hidden="true"></span></summary><div class="wg-14-sec-body"><ol class="wg-14-flow"><li><span class="wg-14-flow-n">1</span> 등록: 소유자·만료일·지표 작성</li><li><span class="wg-14-flow-n">2</span> 내부 노출: 직원 계정으로 검증</li><li><span class="wg-14-flow-n">3</span> 카나리: 낮은 비율에서 지표 확인</li><li><span class="wg-14-flow-n">4</span> 정리: 100% 이후 분기 코드 제거</li></ol></div></details></div>
  <h3 class="wg-14-h3">설정 예시</h3><div class="wg-14-tabs"><input type="radio" name="wg-14-flag-tab" id="wg-14-flag-yml" class="wg-14-tab-in" checked><input type="radio" name="wg-14-flag-tab" id="wg-14-flag-cli" class="wg-14-tab-in"><input type="radio" name="wg-14-flag-tab" id="wg-14-flag-api" class="wg-14-tab-in"><div class="wg-14-tablist"><label class="wg-14-tab" for="wg-14-flag-yml">flags.yml</label><label class="wg-14-tab" for="wg-14-flag-cli">CLI</label><label class="wg-14-tab" for="wg-14-flag-api">HTTP</label></div><pre class="wg-14-code wg-14-code-yml"><code>key: checkout_new_summary
owner: growth-web
default: false
expiry: 2026-07-31
metric: checkout_error_rate
rollback: set false for all segments</code></pre><pre class="wg-14-code wg-14-code-cli"><code>$ flags create checkout_new_summary --owner growth-web
$ flags rollout checkout_new_summary --segment internal --percent 100
$ flags rollout checkout_new_summary --segment beta --percent 5</code></pre><pre class="wg-14-code wg-14-code-api"><code>POST /flags/checkout_new_summary/rollout
{
  "segment": "beta",
  "percent": 5,
  "reason": "metric gate passed for internal"
}</code></pre></div>
  <h3 class="wg-14-h3">자주 묻는 질문</h3><div class="wg-14-faq"><details class="wg-14-q"><summary class="wg-14-q-sum">플래그를 켜면 배포가 필요 없나요</summary><p class="wg-14-q-a">아닙니다. 코드는 이미 배포되어 있어야 합니다. 플래그는 배포된 코드의 실행 경로를 선택하는 운영 장치입니다.</p></details><details class="wg-14-q"><summary class="wg-14-q-sum">만료일이 왜 필요한가요</summary><p class="wg-14-q-a">만료일이 없으면 임시 분기가 영구 코드가 됩니다. 100% 전환 이후에는 코드와 설정을 제거해야 유지보수 비용이 줄어듭니다.</p></details></div>
</div>'''


def build_mapping() -> dict[str, str]:
    quick = f'''{h2(1, "Quick Reference", "reference", "기능 플래그를 만들기 전에 반드시 적어야 하는 필드와 운영 단계만 먼저 확인합니다.")}
<p>기능 플래그는 배포와 노출을 분리하는 장치입니다. 하지만 소유자, 기본값, 만료일, 롤백 기준이 없으면 안전장치가 아니라 오래 남는 조건문이 됩니다. 아래 표는 새 플래그를 등록할 때 빠르게 확인할 최소 계약입니다.</p>
<div class="table-scroll"><table><caption>Feature flag minimum contract</caption><thead><tr><th scope="col">항목</th><th scope="col">필수값</th><th scope="col">누락 시 판단</th></tr></thead><tbody><tr><th scope="row">key</th><td><code>domain_purpose_variant</code> 형태의 안정 식별자</td><td>이름 변경 가능성이 높으면 등록 보류</td></tr><tr><th scope="row">owner</th><td>팀 또는 책임자 한 곳</td><td>비율 변경과 삭제 책임 불명확</td></tr><tr><th scope="row">default</th><td>평가 실패 시 안전한 값</td><td>장애 시 사용자 노출 상태가 불명확</td></tr><tr><th scope="row">expiry</th><td>삭제 예정일과 cleanup 이슈</td><td>영구 조건문으로 남을 위험</td></tr><tr><th scope="row">metric</th><td>확대/중단 판단 지표</td><td>감으로 100% 전환할 위험</td></tr></tbody></table></div>
{vt_card_grid()}'''

    api = f'''{h2(2, "개념/API 항목", "api", "이 문서는 특정 벤더 API가 아니라 기능 플래그 시스템을 설계할 때 필요한 공통 개념 계약을 정리합니다.")}
<div class="card-grid"><article class="mini-card"><h3>Flag</h3><p>코드 분기를 제어하는 최상위 단위입니다. key, description, owner, default, expiry를 포함합니다.</p></article><article class="mini-card"><h3>Segment</h3><p>내부 사용자, 베타 고객, 지역, 요금제처럼 평가 대상을 묶는 조건입니다. 개인정보 원문 저장은 피합니다.</p></article><article class="mini-card"><h3>Rule</h3><p>어떤 segment에 어떤 variant를 몇 퍼센트로 줄지 정의합니다. 규칙 순서가 결과에 영향을 줄 수 있음을 문서화합니다.</p></article><article class="mini-card"><h3>Variant</h3><p>boolean이면 on/off, 실험이면 A/B/C 값을 가질 수 있습니다. variant 의미는 UI 문구와 동일해야 합니다.</p></article><article class="mini-card"><h3>Evaluation</h3><p>요청 컨텍스트를 받아 최종 variant를 반환하는 과정입니다. 실패하면 default로 돌아가야 합니다.</p></article><article class="mini-card"><h3>Audit</h3><p>생성, 비율 변경, 강제 OFF, 삭제를 누가 언제 왜 했는지 기록합니다. 운영 플래그의 신뢰 기반입니다.</p></article></div>
{wg_component_variants()}'''

    patterns = f'''{h2(3, "운영 패턴", "flow", "플래그는 만드는 것보다 안전하게 확대하고 제때 삭제하는 패턴이 중요합니다.")}
<div class="grid-2"><article class="summary-card"><h3>Safe default first</h3><p>기본값은 장애 상황에서도 안전한 방향이어야 합니다. 새 기능이 위험하면 기본값은 off, 보안 완화 기능이면 기본값을 더 보수적으로 둡니다.</p></article><article class="summary-card"><h3>Small canary</h3><p>내부 100% 다음 바로 전체 100%로 가지 않습니다. 1% 또는 낮은 beta 비율에서 오류율, 전환율, 고객 문의를 확인합니다.</p></article><article class="summary-card"><h3>Kill switch visible</h3><p>운영자가 즉시 끌 수 있는 경로를 문서 첫 화면에서 찾을 수 있어야 합니다. 숨겨진 설정 파일만 있으면 사고 대응이 늦습니다.</p></article><article class="summary-card"><h3>Cleanup by design</h3><p>100% 전환은 끝이 아닙니다. 분기 코드, 설정, 문서, 대시보드를 제거해야 플래그 생명주기가 닫힙니다.</p></article></div>
{vt_file_tour()}
{vt_flowchart()}'''

    examples = f'''{h2(4, "Examples", "code", "아래 예시는 구현 언어와 벤더에 묶이지 않는 의사 코드입니다. 실제 시스템에서는 인증, 감사, 실패 처리를 별도로 확인해야 합니다.")}
<div class="table-scroll"><table><caption>Rollout decision examples</caption><thead><tr><th scope="col">상황</th><th scope="col">권장 액션</th><th scope="col">문서에 남길 근거</th></tr></thead><tbody><tr><th scope="row">내부 검증 통과</th><td>beta 5% 카나리 시작</td><td>오류율 변화 없음, 주요 경로 수동 확인 완료</td></tr><tr><th scope="row">카나리 오류 증가</th><td>즉시 off 후 원인 분석</td><td>감사 로그에 중단 사유와 시간 기록</td></tr><tr><th scope="row">100% 안정 7일</th><td>cleanup PR 생성</td><td>분기 제거 범위, 삭제 대상 설정 파일 명시</td></tr></tbody></table></div>
<pre><code>function evaluateFlag(flag, context) {{
  if (!flag.enabled) return flag.defaultValue;
  const matchedRule = findFirstMatchingRule(flag.rules, context);
  if (!matchedRule) return flag.defaultValue;
  return pickVariant(matchedRule, context.stableUserId);
}}</code></pre>
{wg_feature_explainer()}'''

    checklist = f'''{h2(5, "적용 전 체크리스트", "check", "이 항목을 통과하지 못하면 플래그를 만들 수는 있어도 운영 가능한 상태라고 말하기 어렵습니다.")}
<div class="card-grid"><article class="summary-card"><h3>등록</h3><p>key, owner, default, expiry, metric, rollback 문장이 모두 적혀 있습니다.</p></article><article class="summary-card"><h3>노출</h3><p>internal, beta, paid, region 등 segment 정의가 개인정보 원문 없이 설명됩니다.</p></article><article class="summary-card"><h3>확대</h3><p>1% → 5% → 25% → 100% 같은 단계와 각 단계의 중단 기준이 있습니다.</p></article><article class="summary-card"><h3>관측</h3><p>오류율, 성능, 전환, 고객 문의 중 어떤 지표로 판단할지 정했습니다.</p></article><article class="summary-card"><h3>롤백</h3><p>운영자가 플래그를 즉시 off로 돌리는 경로와 감사 로그 위치를 압니다.</p></article><article class="summary-card"><h3>삭제</h3><p>100% 이후 코드 분기와 설정을 제거할 cleanup issue가 등록되어 있습니다.</p></article></div>'''

    return {
        "{{KICKER}}": "Reference Manual · Feature Flag Lifecycle",
        "{{TITLE}}": "Feature Flag Lifecycle Reference",
        "{{SUBTITLE}}": "기능 플래그를 등록, 카나리, 전체 전환, 삭제까지 운영 가능한 문서 계약으로 정리한 레퍼런스입니다.",
        "{{META}}": '<div class="generated-row"><span>작성일 · 2026-06-07</span><span>mode · reference_html</span><span>profile · auto</span><span>scope · vendor-neutral</span></div><div class="lens-strip"><span>quick reference</span><span>concept/API</span><span>patterns</span><span>examples</span></div>',
        "{{QUICK_REFERENCE}}": quick,
        "{{API_OR_CONCEPTS}}": api,
        "{{PATTERNS}}": patterns,
        "{{EXAMPLES}}": examples,
        "{{CHECKLIST}}": checklist,
        "{{SOURCE_NOTE}}": '<strong>Source note.</strong> 이 레퍼런스는 특정 SaaS나 오픈소스 라이브러리의 실제 API 문서가 아니라, 기능 플래그 생명주기를 문서화할 때 필요한 공통 계약을 정리한 벤더 중립 매뉴얼입니다. 실제 엔드포인트, SDK 시그니처, 권한 모델은 사용 중인 시스템 문서로 확인해야 합니다.',
    }


def render() -> None:
    material_hashes = {}
    for rel in MODE_MATERIALS:
        p = SKILL / rel
        if not p.exists():
            raise FileNotFoundError(rel)
        material_hashes[rel] = sha_bytes(p)

    base = read(ASSETS / "base.html")
    layout = read(ASSETS / "layouts" / "reference-manual.html")
    for k, v in build_mapping().items():
        layout = layout.replace(k, v)
    remaining = sorted(set(re.findall(r"{{[A-Z0-9_]+}}", layout)))
    if remaining:
        raise RuntimeError(f"unfilled layout placeholders: {remaining}")

    css = {name: read(ASSETS / name) for name in CSS_ORDER}
    core_hash = hashlib.sha256("\n".join(css[name] for name in CORE).encode("utf-8")).hexdigest()
    css["theme.css"] = f"/* adaptive-html-final-core-css-sha256: {core_hash} */\n" + css["theme.css"]

    html = base
    html = html.replace("{{TITLE}}", "Feature Flag Lifecycle Reference")
    html = html.replace("{{DESCRIPTION}}", "reference_html 모드로 작성한 기능 플래그 생명주기 레퍼런스. Quick Reference, 개념/API, 운영 패턴, 예시, 체크리스트를 포함합니다.")
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
        "mode12_material_sha256": material_hashes,
        "updated_at": datetime.now(timezone.utc).isoformat(),
    })
    integrity_path.write_text(json.dumps(prior, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    render()
    print(OUT)
