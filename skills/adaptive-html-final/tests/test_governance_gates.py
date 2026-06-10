#!/usr/bin/env python3
"""Self-test for the Phase 0 governance gates in scripts/validate_output.py.

Stdlib-only (no pytest). Run: python3 tests/test_governance_gates.py
Exit 0 = all pass, 1 = a gate regressed. Locks the final_20260604 merge-protection
gates so they can't silently break.
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

SKILL = Path(__file__).resolve().parent.parent
_spec = importlib.util.spec_from_file_location("validate_output", SKILL / "scripts" / "validate_output.py")
v = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(v)

_checks = 0
_fails = 0


def check(name: str, cond: bool):
    global _checks, _fails
    _checks += 1
    if not cond:
        _fails += 1
        print(f"FAIL: {name}")
    else:
        print(f"ok:   {name}")


# Gate A+B+C: the shipped skill must be clean (no false positives).
asset_issue_types = {i["type"] for i in v.skill_asset_lint(SKILL)}
check("clean skill: no important_in_core_css", "important_in_core_css" not in asset_issue_types)
check("clean skill: no forbidden_report_font_token", "forbidden_report_font_token" not in asset_issue_types)
check("clean skill: no bare_callout_modifier", "bare_callout_modifier" not in asset_issue_types)

# Gate A: !important allowlist (2 sanctioned widgets.css cases; nothing else).
check("Gate A allows .wg-06-rowhead", v._important_allowlisted("widgets.css", ".wg-06-rowhead{text-align:left!important}"))
check("Gate A allows wg-11-grow width:0", v._important_allowlisted("widgets.css", "@keyframes wg-11-grow{from{width:0 !important}}"))
check("Gate A rejects rogue widgets !important", not v._important_allowlisted("widgets.css", ".wg-09-x{color:red!important}"))
check("Gate A rejects core !important", not v._important_allowlisted("theme.css", ".x{color:red!important}"))

# Gate C: bare callout compound modifier detection.
match = lambda s: [(m.group(1), m.group(2)) for m in v._CALLOUT_RE.finditer(s)]
check("Gate C catches .edge-gov-fnode.good", match(".edge-gov-fnode.good") == [(".edge-gov-fnode", "good")])
check("Gate C catches .vt-adapt-card.good", match(".vt-adapt-card.good") == [(".vt-adapt-card", "good")])
check("Gate C allowlists .vt-pill carrier", ".vt-pill" in v._CALLOUT_CARRIER_ALLOW)
check("Gate C ignores .term+.term sibling", match(".layout-beginner .term+.term") == [])
check("Gate C ignores comma callout list", match(".term,.analogy,.danger,.good") == [])

# Gate D: bespoke prefix denylist on output markup.
bad = v.bespoke_prefix_gate('<div class="vt-adapt-card"></div><span class="edge-gov-badge"></span><div class="widget-node"></div>')
check("Gate D flags bespoke vocab", bad and bad[0]["type"] == "bespoke_namespace_class" and bad[0]["count"] == 3)
clean = v.bespoke_prefix_gate('<div class="wg-11-col"></div><span class="vt-pill good"></span><figure class="shape-figure"></figure><span class="bi-line"></span>')
check("Gate D passes canonical classes", clean == [])

# Gate D (role=img): text-bearing container vs true figure.
buries = v.role_img_buries_text_gate('<div role="img" class="edge-gov-flow"><h3>Step</h3><p>x</p></div>')
check("role=img flags text-bearing div", buries and buries[0]["type"] == "role_img_buries_text")
fig = v.role_img_buries_text_gate('<figure role="img" aria-label="x"><img src="a.svg"></figure>')
check("role=img ignores <figure>", fig == [])
sib = v.role_img_buries_text_gate('<div role="img" aria-label="decorative anim"><span>slide</span><span>fade</span></div><p>실제 본문 단락은 형제 요소다</p>')
check("role=img ignores text-bearing sibling (subtree-scoped)", sib == [])

# Global no-JS gate: only JSON-LD scripts allowed; no draggable/contenteditable (anywhere, not just wg-/vt-).
g_inline = v.global_no_js_gate('<main><script>doThing()</script></main>')
check("global gate flags inline <script>", g_inline and g_inline[0]["type"] == "behavioral_script_global")
g_local = v.global_no_js_gate('<script src="./app.js"></script>')
check("global gate flags local-src <script>", any(i["type"] == "behavioral_script_global" for i in g_local))
g_jsonld = v.global_no_js_gate('<script type="application/ld+json">{"@context":"x"}</script>')
check("global gate allows JSON-LD", g_jsonld == [])
g_dnd = v.global_no_js_gate('<div draggable="true">x</div><p contenteditable="true">y</p>')
check("global gate flags draggable/contenteditable", any(i["type"] == "forbidden_primitive_global" for i in g_dnd))
g_clean = v.global_no_js_gate('<main id="main"><h1>clean</h1><p>no js</p></main>')
check("global gate passes clean markup", g_clean == [])

# Legacy theme-toggle gate: v5.2 uses radios name="ahf-theme"; the pre-5.2 #theme-toggle is deprecated.
t_id = v.legacy_theme_toggle_gate('<input type="checkbox" id="theme-toggle"><label for="theme-toggle">dark</label>')
check("legacy gate flags id=theme-toggle", t_id and t_id[0]["type"] == "legacy_theme_toggle")
t_sel = v.legacy_theme_toggle_gate('<style>:root:has(#theme-toggle:checked){--bg:#000}</style>')
check("legacy gate flags #theme-toggle selector", any(i["type"] == "legacy_theme_toggle" for i in t_sel))
t_ok = v.legacy_theme_toggle_gate('<input type="radio" name="ahf-theme" id="ahf-dark"><label for="ahf-dark">Dark</label>')
check("legacy gate passes ahf-theme switcher", t_ok == [])

# Theme switcher contract: theme CSS without the 3 visible radios is a real UI regression.
theme_css = '.ahf-themebar{}:root:has(#ahf-dark:checked){--bg:#000}'
ts_missing = v.theme_switcher_contract_gate('<main id="main"><h1>x</h1></main>', theme_css)
check("theme switcher gate flags missing radios", any(i["type"] == "theme_switcher_missing_fieldset" for i in ts_missing))
ts_ok_html = '''
<fieldset class="ahf-themebar" aria-label="테마 선택">
  <input type="radio" name="ahf-theme" id="ahf-light" checked><label for="ahf-light">라이트</label>
  <input type="radio" name="ahf-theme" id="ahf-white"><label for="ahf-white">화이트</label>
  <input type="radio" name="ahf-theme" id="ahf-dark"><label for="ahf-dark">다크</label>
</fieldset>
'''
check("theme switcher gate passes 3 radios", v.theme_switcher_contract_gate(ts_ok_html, theme_css) == [])
ts_ok5 = '''
<fieldset class="ahf-themebar" aria-label="테마 선택">
  <input type="radio" name="ahf-theme" id="ahf-light" checked><label for="ahf-light">라이트</label>
  <input type="radio" name="ahf-theme" id="ahf-light2"><label for="ahf-light2">라이트2</label>
  <input type="radio" name="ahf-theme" id="ahf-white"><label for="ahf-white">화이트</label>
  <input type="radio" name="ahf-theme" id="ahf-dark"><label for="ahf-dark">다크</label>
  <input type="radio" name="ahf-theme" id="ahf-dark2"><label for="ahf-dark2">다크2</label>
</fieldset>
'''
check("theme switcher gate passes 5 radios (light2/dark2)", v.theme_switcher_contract_gate(ts_ok5, theme_css) == [])
ts_ok6 = ts_ok5.replace('</fieldset>', '  <input type="radio" name="ahf-theme" id="ahf-blue"><label for="ahf-blue">블루</label>\n</fieldset>')
check("theme switcher gate passes 6 radios (+blue)", v.theme_switcher_contract_gate(ts_ok6, theme_css) == [])
ts_pair = '''
<fieldset class="ahf-themebar"><input type="radio" name="ahf-theme" id="ahf-light" checked><label for="ahf-light">라</label>
<input type="radio" name="ahf-theme" id="ahf-light2"><label for="ahf-light2">라2</label>
<input type="radio" name="ahf-theme" id="ahf-white"><label for="ahf-white">화</label>
<input type="radio" name="ahf-theme" id="ahf-dark"><label for="ahf-dark">다</label></fieldset>'''
check("theme switcher gate flags half-extended (4 radios / no dark2)", any(i["type"] in ("theme_switcher_radio_count","theme_switcher_extended_pair") for i in v.theme_switcher_contract_gate(ts_pair, theme_css)))

# GitHub-analysis visual contract: 14th mode must not regress to raw report markup.
github_bad = '<main id="main" class="page-wide layout-github"><header class="header github-header"><h1>x</h1></header><section><h2><span class="num">1</span>Raw</h2></section></main>'
gh_bad = v.github_analysis_visual_contract_gate(github_bad, '.layout-github .repo-card{}')
check("github visual gate catches raw header/icons/cards",
      {"github_header_generated_row_missing", "github_section_card_css_missing", "github_body_icons_css_missing", "github_numbered_heading_icon_missing"}.issubset({i["type"] for i in gh_bad}))
github_ok = '<main id="main" class="page-wide layout-github"><header class="header github-header"><div class="generated-row"><div class="lens-strip"></div></div><h1>x</h1></header><section><h2><span class="body-icon"><svg aria-hidden="true"></svg></span><span class="num">1</span>OK</h2></section></main>'
github_ok_css = '.layout-github>section{background:var(--card)}.body-icon{}'
check("github visual gate passes current contract", v.github_analysis_visual_contract_gate(github_ok, github_ok_css) == [])

# github_feature_usage(17th mode): feature/usage/adoption guide contract.
ghf_bad = '<main id="main" class="page-wide layout-github-feature"><header class="header"><h1>x</h1></header><section><h2>기능</h2><p>본문</p></section></main>'
ghf_bad_types = {i["type"] for i in v.github_feature_usage_contract_gate(ghf_bad, '.layout-github .repo-card{}')}
check("github_feature_usage gate catches missing card/icons/map/limits",
      {"github_feature_section_card_css_missing", "github_feature_body_icons_css_missing", "github_feature_map_or_screens_missing", "github_feature_source_limits_missing"}.issubset(ghf_bad_types))
ghf_ok = '<main id="main" class="page-wide layout-github-feature"><header class="header"><h1>x</h1></header><section class="feature-map"><h2><span class="body-icon"><svg aria-hidden="true"></svg></span>기능 지도</h2></section><aside class="source-note">출처 한계</aside></main>'
ghf_ok_css = '.layout-github-feature>section{background:var(--card)}.body-icon{}'
check("github_feature_usage gate passes feature-usage contract", v.github_feature_usage_contract_gate(ghf_ok, ghf_ok_css) == [])
check("github_feature_usage registered in MODE_TEMPLATE_CONTRACTS", v.MODE_TEMPLATE_CONTRACTS.get("layout-github-feature", {}).get("mode") == "github_feature_usage")

# YouTube/manual contract gates: new modes must be executable, source-bounded outputs.
youtube_bad = '<main id="main" class="page-wide layout-youtube"><h1>x</h1><section><h2>요약</h2><p>embed 없음</p></section></main>'
yt_bad = v.youtube_analysis_contract_gate(youtube_bad, '.layout-youtube>section{background:var(--card)}')
check("youtube contract gate catches missing evidence/limits", {"youtube_evidence_map_missing", "youtube_source_limits_missing", "youtube_observed_at_missing"}.issubset({i["type"] for i in yt_bad}))
youtube_ok = '<main id="main" class="page-wide layout-youtube"><h1>x</h1><section><h2>Video Evidence Map</h2><p>FACT: transcript에 있는 주장. INFERENCE: 댓글 반복 질문. observed_at: 2026-06-06. Source Limits: UNKNOWN 지표는 확인 필요.</p></section></main>'
check("youtube contract gate passes evidence/limits", v.youtube_analysis_contract_gate(youtube_ok, '.layout-youtube>section{background:var(--card)}') == [])
manual_bad = '<main id="main" class="page-wide layout-manual"><h1>x</h1><section><h2>요약</h2><p>절차만 있음</p></section></main>'
man_bad = v.manual_analysis_contract_gate(manual_bad, '.layout-manual>section{background:var(--card)}')
check("manual contract gate catches missing role/safety/troubleshooting", {"manual_role_router_missing", "manual_prerequisites_safety_missing", "manual_troubleshooting_missing"}.issubset({i["type"] for i in man_bad}))
manual_ok = '<main id="main" class="page-wide layout-manual"><h1>x</h1><section><h2>Source & Version Snapshot</h2><p>Reader Role Router: 관리자. Prerequisites/Safety: 권한 확인. Troubleshooting: 증상/원인/진단. Source Limits: UNKNOWN은 확인 불가.</p></section></main>'
check("manual contract gate passes executable manual", v.manual_analysis_contract_gate(manual_ok, '.layout-manual>section{background:var(--card)}') == [])

# Depth + profile-vt gates: anti wide-and-thin (the 8mode-demo youtube/manual failure).
thin_body = '<main id="main" class="page-wide layout-youtube"><h1>x</h1>' + ''.join(
    f'<section><h2>{i}</h2><p>한 문장 요약.</p></section>' for i in range(8)) + '</main>'
thin_page = '<html><body>' + thin_body + '</body></html>'
check("depth gate catches wide-and-thin mode page",
      any(i["type"] == "mode_section_depth_too_thin" for i in v.mode_depth_gate(thin_page)))
rich_page = '<html><body><main id="main" class="page-wide layout-youtube"><h1>x</h1>' + ''.join(
    f'<section><h2>{i}</h2><p>{"근거와 해석이 충분히 담긴 본문 문장. " * 30}</p></section>' for i in range(8)) + '</main></body></html>'
check("depth gate passes rich mode page", v.mode_depth_gate(rich_page) == [])
index_page = '<html><body><main id="main" class="page-wide"><h1>x</h1>' + '<h2>a</h2>' * 10 + '</body></html>'
check("depth gate skips non-mode (index) pages", v.mode_depth_gate(index_page) == [])
few_sections = '<html><body><main id="main" class="page-wide layout-landing"><h1>x</h1><section><h2>1</h2><p>짧음</p></section></main></body></html>'
check("depth gate skips few-section pages", v.mode_depth_gate(few_sections) == [])
no_vt = '<html><body><main id="main" class="page-wide layout-expert"><h1>x</h1><section><h2>1</h2><p>본문</p></section></main></body></html>'
check("profile-vt gate catches auto profile without vt-",
      any(i["type"] == "profile_vt_template_missing" for i in v.profile_vt_required_gate(no_vt, "auto")))
with_vt = no_vt.replace('<p>본문</p>', '<div class="vt-shell"><div class="rm-grid">x</div></div><p>본문</p>')
check("profile-vt gate passes when vt- present", v.profile_vt_required_gate(with_vt, "auto") == [])
check("profile-vt gate skips widget profile", v.profile_vt_required_gate(no_vt, "widget") == [])
check("profile-vt gate skips index pages", v.profile_vt_required_gate(index_page, "auto") == [])
# Anchor lock: the shipped 15/16 examples must satisfy the depth gate (anti-thin anchors).
for _ex in ("15_youtube_vibecoding_gap.html", "16_manual_product_runbook.html"):
    _t = (SKILL / "examples" / _ex).read_text(encoding="utf-8")
    check(f"example {_ex.split('_')[0]} satisfies depth gate", v.mode_depth_gate(_t) == [])

# Source-doc consistency gate: catches editorial drift the value/hash/count gates can't.
# 1) CHANGELOG duplicate version numbers (the v5.3.4-twice bug).
check("changelog dup-version gate catches a repeated version",
      v.changelog_duplicate_versions("## v5.3.4 (x)\n\n## v5.3.5\n\n## v5.3.4 (y)\n") == ["5.3.4"])
check("changelog dup-version gate passes a clean changelog",
      v.changelog_duplicate_versions("## v5.7.0\n\n## v5.6.0\n\n## v5.5.9\n") == [])
# 2) SKILL.md↔manifest examples-fidelity contradiction (경량 vs 풀 스킬급).
check("examples-fidelity gate catches 경량/풀스킬급 contradiction",
      v.examples_fidelity_conflict("examples = 16모드 경량 참조 예제", '"purpose":"16모드 풀 스킬급 참조 예제"') is True)
check("examples-fidelity gate passes when both say 풀 스킬급",
      v.examples_fidelity_conflict("examples = 16모드 풀 스킬급 참조 예제", '"purpose":"16모드 풀 스킬급 참조 예제"') is False)
# 3) manifest internal version staleness (SoT must not contradict itself).
stale_manifest = '{"version":"5.10.0","examples":{"version":"5.9.2"},"changes":["v5.9.2: old"],"releases":["v5.9.2: old"],"updated":"2026-06-07"}'
stale_types = {i["type"] for i in v.manifest_version_consistency_gate(stale_manifest, "## v5.10.0 (2026-06-09)\\n")}
check("manifest consistency gate catches stale examples/changes/releases/updated",
      {"manifest_examples_version_mismatch", "manifest_changes_version_stale", "manifest_releases_version_stale", "manifest_updated_before_changelog"}.issubset(stale_types))
clean_manifest = '{"version":"5.10.0","examples":{"version":"5.10.0"},"changes":["v5.10.0: ok"],"releases":["v5.10.0: ok"],"updated":"2026-06-09"}'
check("manifest consistency gate passes current-version fields",
      v.manifest_version_consistency_gate(clean_manifest, "## v5.10.0 (2026-06-09)\\n") == [])
# 4) §0.6 canonical decision table must match validator contracts and widget-system.md.
decision_fixture = '''
## 0.6 Canonical Decision Table (모드 → layout → vt-템플릿 → wg-위젯)

| Mode | Layout | vt-템플릿 (1순위→) | wg-위젯 (1순위→) |
|---|---|---|---|
| expert_html | expert-report.html | risk-matrix, raci | wg-03, wg-04 |

vt-템플릿 파일명은 `assets/visual-html-templates/NN-<name>.html`이다.
'''
bad_widget_fixture = '''
| Mode | 권장 위젯 | 쓰임 |
|---|---|---|
| expert_html | **04 Module Map**, 01, 03 | stale |

### 위젯 → 모드 역참조
'''
bad_contract_fixture = {
    "layout-expert": {"mode": "expert_html", "primary_vt": "quality-gate", "recommended_wg": ("wg-04",)}
}
decision_bad_types = {i["type"] for i in v.decision_table_consistency_gate(decision_fixture, bad_widget_fixture, bad_contract_fixture)}
check("decision-table gate catches validator/widget wg drift",
      {"validator_decision_table_mismatch", "widget_system_wg_mapping_mismatch"}.issubset(decision_bad_types))
current_decision_issues = v.decision_table_consistency_gate(
    (SKILL / "SKILL.md").read_text(encoding="utf-8"),
    (SKILL / "references" / "widget-system.md").read_text(encoding="utf-8"),
)
check("decision-table gate passes current §0.6/widget/validator mapping", current_decision_issues == [])
# 5) visual-html-system.md must not present historical v6/20-template wording as current.
stale_visual = '> 버전: 이 라이브러리 편입으로 스킬은 4.4.0 → **4.5.0**.\n- 모드별 실제 적용 갤러리: **`output/adaptive-html-final-showcase-v6`** — 20종 적용'
stale_visual_types = {i["type"] for i in v.visual_html_system_staleness_gate(stale_visual)}
check("visual-html staleness gate catches old version/gallery/count wording",
      {"visual_html_intro_version_stale", "visual_html_gallery_baseline_stale", "visual_html_template_count_stale"}.issubset(stale_visual_types))
check("visual-html staleness gate passes current reference doc",
      v.visual_html_system_staleness_gate((SKILL / "references" / "visual-html-system.md").read_text(encoding="utf-8")) == [])
# 6) Against the REAL skill: must be clean now (proves the source-doc fixes landed).
_doc_issues = v.skill_doc_consistency_gate(SKILL)
check("real skill doc-consistency gate is clean (no dup/stale/contradiction)",
      _doc_issues == [])
if _doc_issues:
    print("  detail:", _doc_issues)

# Global numbered-h2 body-icon contract (전 모드 공통, github 전용→전역 승격).
icon_bad = v.numbered_h2_body_icon_gate('<main id="main" class="page-wide layout-checklist"><section><h2><span class="num">1</span> 점검</h2></section></main>')
check("body-icon gate catches numbered h2 without icon", icon_bad and icon_bad[0]["type"] == "numbered_h2_missing_body_icon")
icon_ok = v.numbered_h2_body_icon_gate('<main id="main"><section><h2><span class="body-icon body-icon--sm"><svg aria-hidden="true"></svg></span><span class="num">1</span> 점검</h2></section></main>')
check("body-icon gate passes example-style h2 (icon+num)", icon_ok == [])
icon_plain = v.numbered_h2_body_icon_gate('<main id="main"><section><h2>번호 없는 제목</h2></section></main>')
check("body-icon gate ignores un-numbered h2", icon_plain == [])

# Global section-surface contract (>section:not(.try) card; .try hero 제외).
surf_css_ok = '.page-wide>section:not(.try):not(.no-surface),.page>article>section{background:var(--card);border:1px solid var(--line)}'
check("section-surface gate passes when unified surface CSS inlined",
      v.section_surface_contract_gate('<main id="main" class="page-wide layout-blog"><article><section><h2>x</h2></section></article></main>', surf_css_ok) == [])
surf_missing = v.section_surface_contract_gate('<main id="main" class="page-wide layout-checklist"><section><h2>x</h2></section></main>', '.ahf-themebar{}')
check("section-surface gate flags missing surface rule", surf_missing and surf_missing[0]["type"] == "section_surface_css_missing")
surf_nonlayout = v.section_surface_contract_gate('<main id="main" class="page-wide"><section><h2>catalog</h2></section></main>', '.ahf-themebar{}')
check("section-surface gate ignores non-layout (catalog/index) pages", surf_nonlayout == [])

# 강화된 section-surface: 직접 >section:not(.try) 카드 규칙 필수, article>section 우회는 불충분.
surf_direct = '.page-wide>section:not(.try){background:var(--card);border:1px solid var(--line)}'
check("section-surface gate passes direct :not(.try) card rule",
      v.section_surface_contract_gate('<main id="main" class="page-wide layout-checklist"><section class="risk-matrix"><h2>x</h2></section></main>', surf_direct) == [])
surf_bypass = '.page-wide>article>section{background:var(--card)}'  # 우회만 있음
check("section-surface gate now REJECTS article-only bypass",
      v.section_surface_contract_gate('<main id="main" class="page-wide layout-checklist"><section><h2>x</h2></section></main>', surf_bypass) and v.section_surface_contract_gate('<main id="main" class="page-wide layout-checklist"><section><h2>x</h2></section></main>', surf_bypass)[0]["type"]=="section_surface_css_missing")

# direct_section_h2_icon_gate: 직접 섹션 첫 h2는 body-icon 필수(번호 무관), .try 제외.
dsi_bad = v.direct_section_h2_icon_gate('<main id="main" class="page-wide layout-seo"><section class="serp-box"><h2>검색 미리보기</h2></section></main>')
check("direct-section h2 gate catches missing icon (numbered or not)", dsi_bad and dsi_bad[0]["type"]=="direct_section_h2_missing_body_icon")
dsi_ok = v.direct_section_h2_icon_gate('<main id="main" class="page-wide layout-seo"><section class="serp-box"><h2><span class="body-icon"><svg aria-hidden="true"></svg></span>검색 미리보기</h2></section></main>')
check("direct-section h2 gate passes icon-only (no num) section", dsi_ok == [])
dsi_try = v.direct_section_h2_icon_gate('<main id="main" class="page-wide layout-github"><section class="try"><h2>Next Actions</h2></section></main>')
check("direct-section h2 gate ignores .try hero", dsi_try == [])
dsi_nonlayout = v.direct_section_h2_icon_gate('<main id="main" class="page-wide"><section><h2>catalog</h2></section></main>')
check("direct-section h2 gate ignores non-layout pages", dsi_nonlayout == [])
dsi_nested_widget = v.direct_section_h2_icon_gate('<main id="main" class="page-wide layout-seo"><section><h2><span class="body-icon"><svg aria-hidden="true"></svg></span>검색 미리보기</h2><section class="wg-11"><h2>위젯 자체 제목</h2></section></section></main>')
check("direct-section h2 gate ignores nested widget sections", dsi_nested_widget == [])
dsi_article_bad = v.direct_section_h2_icon_gate('<main id="main" class="page-wide layout-blog"><article><section><h2>본문 섹션</h2></section></article></main>')
check("direct-section h2 gate catches article direct sections", dsi_article_bad and dsi_article_bad[0]["type"]=="direct_section_h2_missing_body_icon")

toc_bad = v.toc_map_contract_gate('<main id="main" class="page layout-blog"><nav class="toc-map"><a href="#a"><span>1</span>붙은 목차</a></nav></main>')
check("toc-map gate catches bare collapsed links", toc_bad and toc_bad[0]["type"]=="toc_map_contract_missing_pills")
toc_ok = v.toc_map_contract_gate('<main id="main" class="page layout-blog"><nav class="toc-map"><span class="label">글의 흐름</span><div class="toc-pills"><a class="toc-pill" href="#a"><b>1</b>첫 섹션</a></div></nav></main>')
check("toc-map gate accepts canonical chip nav", toc_ok == [])
expert_grid_bad = v.expert_decision_grid_section_gate('<main id="main" class="page-wide layout-expert"><section class="decision-grid"><h2><span class="body-icon"><svg aria-hidden="true"></svg></span>판단</h2></section></main>')
check("expert decision-grid gate catches direct section collision", expert_grid_bad and expert_grid_bad[0]["type"]=="expert_decision_grid_section_collision")
expert_grid_ok = v.expert_decision_grid_section_gate('<main id="main" class="page-wide layout-expert"><section class="decision-section"><div class="expert-inner-grid"><article>card</article></div></section></main>')
check("expert decision-grid gate accepts section plus inner grid", expert_grid_ok == [])
expert_val_bad = v.expert_validation_checklist_widget_gate('<main id="main" class="page-wide layout-expert"><section class="validation-checklist"><h2><span class="body-icon"><svg aria-hidden="true"></svg></span>검증</h2><section class="wg-03"><h3>패치 리뷰</h3></section></section></main>')
check("expert validation checklist gate catches wg-03/wg-17 misuse", expert_val_bad and expert_val_bad[0]["type"]=="expert_validation_widget_misuse")
expert_val_ok = v.expert_validation_checklist_widget_gate('<main id="main" class="page-wide layout-expert"><section class="validation-checklist"><h2><span class="body-icon"><svg aria-hidden="true"></svg></span>검증</h2><section class="vt-shell"><div class="qg-grid"></div></section><div class="validation-evidence-grid"></div></section><section class="wg-17"><h3>릴리즈 노트</h3></section></main>')
check("expert validation checklist gate accepts evidence/quality gate only", expert_val_ok == [])

# 고정 계약: 헤더 형태(필수) + 마무리 정리 섹션(권고).
_hdr_ok = '<main id="main" class="page-wide layout-expert"><header class="header"><p class="kicker">K</p><h1>T</h1><p class="sub">s</p><div class="meta"><span>m</span></div></header><section class="try"><h2>x</h2></section></main>'
check("header gate passes canonical header(kicker.h1.sub.meta)", v.header_contract_gate(_hdr_ok) == [])
_hb = v.header_contract_gate('<main id="main" class="page-wide layout-expert"><header class="header"><h1>T</h1></header><section><h2>x</h2></section></main>')
check("header gate flags missing kicker/sub/meta", {i.get("part") for i in _hb} >= {"kicker","sub","meta"})
check("header gate flags missing header.header", v.header_contract_gate('<main id="main" class="page-wide layout-seo"><section><h2>x</h2></section></main>')[0]["type"]=="header_contract_missing_header")
check("header gate ignores non-layout pages", v.header_contract_gate('<main id="main" class="page-wide"><h1>x</h1></main>') == [])
check("closing recommendation silent when last section .try", v.closing_summary_recommendation(_hdr_ok) == [])
_nt = '<main id="main" class="page-wide layout-expert"><section><h2>a</h2></section><section><h2>b</h2></section></main>'
check("closing recommendation warns when last section not .try", v.closing_summary_recommendation(_nt) and v.closing_summary_recommendation(_nt)[0]["type"]=="closing_summary_recommended")

print(f"\n{_checks - _fails}/{_checks} checks passed")
sys.exit(1 if _fails else 0)
