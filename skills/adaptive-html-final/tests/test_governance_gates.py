#!/usr/bin/env python3
"""Self-test for the Phase 0 governance gates in scripts/validate_output.py.

Stdlib-only (no pytest). Run: python3 tests/test_governance_gates.py
Exit 0 = all pass, 1 = a gate regressed. Locks the final_20260604 merge-protection
gates so they can't silently break.
"""
from __future__ import annotations

import importlib.util
import sys
import tempfile as _tmp
from pathlib import Path

SKILL = Path(__file__).resolve().parent.parent
_spec = importlib.util.spec_from_file_location("validate_output", SKILL / "scripts" / "validate_output.py")
v = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(v)
_qspec = importlib.util.spec_from_file_location("quality_contract_check", SKILL / "scripts" / "quality_contract_check.py")
q = importlib.util.module_from_spec(_qspec)
sys.modules["quality_contract_check"] = q
_qspec.loader.exec_module(q)
_cspec = importlib.util.spec_from_file_location("completion_check", SKILL / "scripts" / "completion_check.py")
c = importlib.util.module_from_spec(_cspec)
sys.modules["completion_check"] = c
_cspec.loader.exec_module(c)

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
check("theme switcher gate flags 3 radios (8 required)", any(i["type"]=="theme_switcher_radio_count" for i in v.theme_switcher_contract_gate(ts_ok_html, theme_css)))
ts_ok5 = '''
<fieldset class="ahf-themebar" aria-label="테마 선택">
  <input type="radio" name="ahf-theme" id="ahf-light" checked><label for="ahf-light">라이트</label>
  <input type="radio" name="ahf-theme" id="ahf-light2"><label for="ahf-light2">라이트2</label>
  <input type="radio" name="ahf-theme" id="ahf-white"><label for="ahf-white">화이트</label>
  <input type="radio" name="ahf-theme" id="ahf-dark"><label for="ahf-dark">다크</label>
  <input type="radio" name="ahf-theme" id="ahf-dark2"><label for="ahf-dark2">다크2</label>
</fieldset>
'''
check("theme switcher gate flags 5 radios (8 required)", any(i["type"]=="theme_switcher_radio_count" for i in v.theme_switcher_contract_gate(ts_ok5, theme_css)))
ts_ok6 = ts_ok5.replace('</fieldset>', '  <input type="radio" name="ahf-theme" id="ahf-blue"><label for="ahf-blue">블루</label>\n</fieldset>')
check("theme switcher gate flags 6 radios (8 required)", any(i["type"]=="theme_switcher_radio_count" for i in v.theme_switcher_contract_gate(ts_ok6, theme_css)))
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
gov_bad_manifest = '{"version":"9.9.9","quality":{"governance_count":137,"governance_command":"python3 skills/adaptive-html-final/tests/test_governance_gates.py"}}'
with _tmp.TemporaryDirectory() as _td:
    _rr = v.Path(_td)
    (_rr / "README.md").write_text("│ tests # 거버넌스 게이트 (138/138)\n| 거버넌스 게이트 | `test_governance_gates.py` **138 / 138 통과** |\n> 🟢 **게이트 현황(v9.9.9)**: 거버넌스 `test_governance_gates.py` **138/138 통과**", encoding="utf-8")
    _gb = {i["type"] for i in v.manifest_governance_count_gate(gov_bad_manifest, _rr)}
    check("manifest governance-count gate catches README current-count drift",
          {"readme_current_gate_status_count_mismatch","readme_current_governance_table_count_mismatch","readme_current_tree_gate_count_mismatch"}.issubset(_gb))
gov_good_manifest = '{"version":"9.9.9","quality":{"governance_count":138,"governance_command":"python3 skills/adaptive-html-final/tests/test_governance_gates.py"}}'
with _tmp.TemporaryDirectory() as _td:
    _rr = v.Path(_td)
    (_rr / "README.md").write_text("│ tests # 거버넌스 게이트 (138/138)\n| 거버넌스 게이트 | `test_governance_gates.py` **138 / 138 통과** |\n> 🟢 **게이트 현황(v9.9.9)**: 거버넌스 `test_governance_gates.py` **138/138 통과**", encoding="utf-8")
    check("manifest governance-count gate passes matching current README surfaces",
          v.manifest_governance_count_gate(gov_good_manifest, _rr) == [])
with _tmp.TemporaryDirectory() as _td:
    _rr = v.Path(_td)
    _sd = _rr / "skills" / "adaptive-html-final"
    (_sd / "examples" / "sources").mkdir(parents=True)
    (_rr / "README.md").write_text("비주얼: profile=widget 또는 style=v5", encoding="utf-8")
    (_rr / "AGENTS.md").write_text("style=v6 is stale public prose", encoding="utf-8")
    (_sd / "SKILL.md").write_text("widget=v5 / diagram=v6", encoding="utf-8")
    (_sd / "manifest.json").write_text('{"profile_selection":"profile=widget|diagram|auto 또는 style=v5|v6"}', encoding="utf-8")
    (_sd / "examples" / "sources" / "adaptive-html-final-manifest.json").write_text('{"profile_selection":"style=v5|v6"}', encoding="utf-8")
    _alias_issues = v.deprecated_profile_alias_surface_gate(_rr, _sd)
    check("deprecated profile alias surface gate catches current-doc exposure",
          len([i for i in _alias_issues if i["type"] == "deprecated_profile_alias_surface"]) >= 5)
with _tmp.TemporaryDirectory() as _td:
    _rr = v.Path(_td)
    _sd = _rr / "skills" / "adaptive-html-final"
    (_sd / "examples" / "sources").mkdir(parents=True)
    clean = "프로파일은 profile=widget|diagram|auto만 현행 정본이다."
    (_rr / "README.md").write_text(clean, encoding="utf-8")
    (_rr / "AGENTS.md").write_text(clean, encoding="utf-8")
    (_sd / "SKILL.md").write_text(clean, encoding="utf-8")
    (_sd / "manifest.json").write_text('{"profile_selection":"profile=widget|diagram|auto"}', encoding="utf-8")
    (_sd / "examples" / "sources" / "adaptive-html-final-manifest.json").write_text('{"profile_selection":"profile=widget|diagram|auto"}', encoding="utf-8")
    check("deprecated profile alias surface gate passes canonical profile docs",
          v.deprecated_profile_alias_surface_gate(_rr, _sd) == [])
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
h2_order_bad = v.h2_icon_order_gate('<main id="main" class="page-wide layout-seo"><section><h2>검색 미리보기 <span class="body-icon"><svg aria-hidden="true"></svg></span></h2></section></main>')
check("h2 icon order gate catches title before icon",
      h2_order_bad and h2_order_bad[0]["type"]=="h2_icon_order_violation")
h2_order_bad_num = v.h2_icon_order_gate('<main id="main" class="page-wide layout-seo"><section><h2><span class="body-icon"><svg aria-hidden="true"></svg></span>검색 <span class="num">1</span></h2></section></main>')
check("h2 icon order gate catches num after title",
      h2_order_bad_num and h2_order_bad_num[0]["type"]=="h2_icon_order_violation")
h2_order_ok = v.h2_icon_order_gate('<main id="main" class="page-wide layout-seo"><section><h2><span class="body-icon"><svg aria-hidden="true"></svg></span><span class="num">1</span>검색 미리보기</h2></section></main>')
check("h2 icon order gate passes body-icon-num-title", h2_order_ok == [])

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
_hdr_ok = '<main id="main" class="page-wide layout-expert"><header class="header"><p class="kicker">K</p><h1>T</h1><p class="sub">s</p><div class="meta"><span>m</span></div><div class="generated-row"><p class="generated-date">Generated</p><div class="lens-strip"><span>Lens</span></div></div></header><section class="try"><h2>x</h2></section></main>'
check("header gate passes canonical header(kicker.h1.sub.meta)", v.header_contract_gate(_hdr_ok) == [])
_hb = v.header_contract_gate('<main id="main" class="page-wide layout-expert"><header class="header"><h1>T</h1></header><section><h2>x</h2></section></main>')
check("header gate flags missing kicker/sub/meta/generated-row/lens-strip", {i.get("part") for i in _hb} >= {"kicker","sub","meta","generated-row","lens-strip"})
check("header gate flags missing header.header", v.header_contract_gate('<main id="main" class="page-wide layout-seo"><section><h2>x</h2></section></main>')[0]["type"]=="header_contract_missing_header")
check("header gate ignores non-layout pages", v.header_contract_gate('<main id="main" class="page-wide"><h1>x</h1></main>') == [])
check("closing recommendation silent when last section .try", v.closing_summary_recommendation(_hdr_ok) == [])
_nt = '<main id="main" class="page-wide layout-expert"><section><h2>a</h2></section><section><h2>b</h2></section></main>'
check("closing recommendation warns when last section not .try", v.closing_summary_recommendation(_nt) and v.closing_summary_recommendation(_nt)[0]["type"]=="closing_summary_recommended")

# SKILL.md header version must match manifest.version (prose drift guard — bumps repeatedly missed SKILL.md header).
_smv_bad = v.skill_md_version_mismatch('> Version 5.10.0 · note', '5.10.2')
check("skill_md version gate catches header drift", _smv_bad and _smv_bad[0]["type"]=="skill_md_version_mismatch")
check("skill_md version gate passes matching header", v.skill_md_version_mismatch('> Version 5.10.2 · note', '5.10.2') == [])
with _tmp.TemporaryDirectory() as _td:
    _root = v.Path(_td)
    (_root / 'bad.html').write_text('<main>Generated by adaptive-html-final 5.10.0</main>', encoding='utf-8')
    (_root / 'ok.html').write_text('<main>Generated by adaptive-html-final 9.9.9</main>', encoding='utf-8')
    _ovis = v.output_version_surface_issues(_root, '9.9.9')
    check("output visible-version gate catches stale meta/footer",
          any(i["type"]=="output_visible_version_stale" and i["actual"]=="5.10.0" for i in _ovis))
    (_root / 'bad.html').write_text('<style>/* adaptive-html-final 5.10.0 historical css comment */</style><main>Generated by adaptive-html-final 9.9.9</main>', encoding='utf-8')
    check("output visible-version gate ignores CSS comments and passes matching visible text",
          v.output_version_surface_issues(_root, '9.9.9') == [])
with _tmp.TemporaryDirectory() as _td:
    _sd = v.Path(_td) / 'skills' / 'adaptive-html-final'
    (_sd / 'references').mkdir(parents=True)
    (_td_root := v.Path(_td)).joinpath('README.md').write_text('examples/ # v5.10.0 현행 17모드 참조 예제 + index\n> 🟢 **게이트 현황(v5.10.0)**', encoding='utf-8')
    (_sd / 'manifest.json').write_text('{"version":"9.9.9","examples":{"purpose":"17모드 참조 예제 — 실제 코어 CSS 인라인(v5.10.0)"}}', encoding='utf-8')
    (_sd / 'references' / 'visual-html-system.md').write_text('현행 v5.10.0 기준\nv5.10.0 스킬 자산 기준의 17모드 레퍼런스', encoding='utf-8')
    _cvis = {i["type"] for i in v.current_version_surface_issues(_sd, '9.9.9')}
    check("current-version surface gate catches manifest/README/reference drift",
          {"manifest_examples_purpose_version_stale","readme_current_examples_version_stale","readme_gate_status_version_stale","visual_html_current_baseline_version_stale","visual_html_examples_version_stale"}.issubset(_cvis))


# ---- release-safety gates: on-accent pairing / theme contrast / print ink / width canon / theme 8/8 / package ----
check("on-accent lint catches #fff on accent fill",
      v.on_accent_pairing_violations('x{background:var(--accent-2);color:#fff}','fx') and
      v.on_accent_pairing_violations('x{background:var(--accent-2);color:#fff}','fx')[0]["type"]=="on_accent_pairing_violation")
check("on-accent lint passes var(--on-accent) pairing",
      v.on_accent_pairing_violations('x{background:var(--accent-2);color:var(--on-accent)}','fx') == [])
check("theme contrast gate catches white-on-light-tint pair",
      v.theme_contrast_failures('--accent-2:#ff909a;\n--on-accent:#ffffff;','') and
      v.theme_contrast_failures('--accent-2:#ff909a;\n--on-accent:#ffffff;','')[0]["type"]=="theme_token_contrast_fail")
check("theme contrast gate passes REAL theme tokens (8 themes)",
      v.theme_contrast_failures(( SKILL/'assets/theme.css').read_text(encoding='utf-8'),
                                ( SKILL/'assets/theme-dark.css').read_text(encoding='utf-8')) == [])
check("print ink gate catches missing .try override",
      v.print_try_ink_missing('@media print{body{color:#111}}') and
      v.print_try_ink_missing('@media print{body{color:#111}}')[0]["type"]=="print_try_ink_missing")
check("print ink gate passes REAL print.css",
      v.print_try_ink_missing(( SKILL/'assets/print.css').read_text(encoding='utf-8')) == [])
check("width canon gate clean on REAL skeletons/examples/theme",
      v.layout_width_consistency_issues(SKILL) == [])
import zipfile as _zf, tempfile as _tf, json as _json, os as _os
_tmpzip = _os.path.join(_tf.gettempdir(), 'gov_pkg_stale.skill')
with _zf.ZipFile(_tmpzip,'w') as _z: _z.writestr('adaptive-html-final/manifest.json', _json.dumps({"version":"5.0.0"}))
check("package gate catches stale zip version",
      v.skill_package_version_issues(v.Path(_tmpzip),'9.9.9') and
      v.skill_package_version_issues(v.Path(_tmpzip),'9.9.9')[0]["type"]=="skill_package_version_stale")
with _zf.ZipFile(_tmpzip,'w') as _z: _z.writestr('adaptive-html-final/manifest.json', _json.dumps({"version":"9.9.9"}))
check("package gate passes matching zip version", v.skill_package_version_issues(v.Path(_tmpzip),'9.9.9') == [])
with _tmp.TemporaryDirectory() as _td:
    _sd = v.Path(_td) / 'adaptive-html-final'
    _sd.mkdir()
    (_sd / 'manifest.json').write_text('{"version":"9.9.9"}', encoding='utf-8')
    _pkg = v.Path(_td) / 'adaptive-html-final.skill'
    with _zf.ZipFile(_pkg,'w') as _z: _z.writestr('adaptive-html-final/manifest.json', '{"version":"5.10.0"}')
    check("package content gate catches stale same-path payload",
          v.skill_package_content_issues(_pkg, _sd) and v.skill_package_content_issues(_pkg, _sd)[0]["type"]=="skill_package_content_stale")
    with _zf.ZipFile(_pkg,'w') as _z: _z.writestr('adaptive-html-final/manifest.json', '{"version":"9.9.9"}')
    check("package content gate passes byte-matching payload", v.skill_package_content_issues(_pkg, _sd) == [])
with _tmp.TemporaryDirectory() as _td:
    _sd = v.Path(_td) / 'adaptive-html-final'
    _sd.mkdir()
    (_sd / 'manifest.json').write_text('{"version":"9.9.9"}', encoding='utf-8')
    (_sd / '.pytest_cache').mkdir()
    (_sd / '.pytest_cache' / 'CACHEDIR.TAG').write_text('cache noise', encoding='utf-8')
    (_sd / '__pycache__').mkdir()
    (_sd / '__pycache__' / 'x.cpython-314.pyc').write_bytes(b'cache noise')
    (_sd / '.DS_Store').write_bytes(b'cache noise')
    _pkg = v.Path(_td) / 'adaptive-html-final.skill'
    import zipfile as _zf
    with _zf.ZipFile(_pkg, 'w') as z:
        z.writestr('adaptive-html-final/manifest.json', '{"version":"9.9.9"}')
        z.writestr('adaptive-html-final/.pytest_cache/CACHEDIR.TAG', 'cache noise')
        z.writestr('adaptive-html-final/__pycache__/x.cpython-314.pyc', 'cache noise')
        z.writestr('adaptive-html-final/.DS_Store', 'cache noise')
    check("package content gate ignores cache and OS noise", v.skill_package_content_issues(_pkg, _sd) == [])
_t8 = ''.join(f'<input type="radio" name="ahf-theme" id="ahf-{x}"{" checked" if x=="light" else ""}><label for="ahf-{x}">{x}</label>' for x in ('light','light2','white','dark','dark2','blue','skyblue','sepia'))
_fs8 = '<fieldset class="ahf-themebar">'+_t8+'</fieldset>'
_style8 = '.ahf-themebar{display:flex}'
check("theme switcher gate passes full 8-radio bar", v.theme_switcher_contract_gate(_fs8, _style8) == [])
_t7 = _fs8.replace('<input type="radio" name="ahf-theme" id="ahf-sepia"><label for="ahf-sepia">sepia</label>','')
check("theme switcher gate flags 7-of-8 radios",
      any(i["type"] in ("theme_switcher_radio_count","theme_switcher_missing_radio") for i in v.theme_switcher_contract_gate(_t7, _style8)))

# ---- previously-uncovered page gates: minimal catch+pass pairs ----
check("widget_static_gate catches missing widgets css",
      any(i["type"]=="widget_css_not_inlined" for i in v.widget_static_gate('<div class="wg-01-card">x</div>','')))
check("widget_static_gate passes when wg css inlined",
      v.widget_static_gate('<div class="wg-01-card">x</div>','.wg-01{color:red}') == [])
check("visual_html_gate catches missing vt css",
      any(i["type"]=="visual_html_css_not_inlined" for i in v.visual_html_gate('<section class="vt-shell">x</section>','')))
check("visual_html_gate passes when vt css inlined",
      v.visual_html_gate('<section class="vt-shell">x</section>','.vt-shell{background:#fff}') == [])
check("cross_leak_gate flags wg markup under diagram profile",
      any(i["type"]=="cross_leak" for i in v.cross_leak_gate('<div class="wg-03-grid">x</div>','diagram')))
check("cross_leak_gate silent under auto profile", v.cross_leak_gate('<div class="wg-03-grid">x</div>','auto') == [])
_mtc_bad = '<main class="page-wide layout-expert"><section><h2>x</h2></section></main>'
check("mode_template_contract_gate flags missing primary vt+wg",
      {i["type"] for i in v.mode_template_contract_gate(_mtc_bad,'auto')} >= {"mode_primary_vt_missing","mode_recommended_wg_missing"})
_mtc_ok = '<main class="page-wide layout-expert"><section><h2>x</h2><div class="vt-shell"><div class="rm-grid">m</div></div><div class="wg-03-grid">w</div></section></main>'
check("mode_template_contract_gate passes primary vt + recommended wg", v.mode_template_contract_gate(_mtc_ok,'auto') == [])
_icon_bad = '<main id="main" class="page-wide layout-expert"><section class="x"><p>no h2</p></section></main>'
check("direct_section_title_icon gate flags h2-less direct section",
      any(i["type"]=="direct_section_h2_missing" for i in v.direct_section_title_icon_policy_gate(_icon_bad)))
_icon_ok = '<main id="main" class="page-wide layout-expert"><section class="x"><h2><span class="body-icon"><svg aria-hidden="true"></svg></span>t</h2></section></main>'
check("direct_section_title_icon gate passes icon h2", v.direct_section_title_icon_policy_gate(_icon_ok) == [])
_same_icon_h2 = '<h2><span class="body-icon"><svg aria-hidden="true"><path d="M1 1"/></svg></span>t%d</h2>'
_div_bad = '<main class="page-wide layout-expert">' + ''.join('<section>'+(_same_icon_h2 % i)+'</section>' for i in range(7)) + '</main>'
check("body_icon_diversity gate flags one-svg-everywhere",
      any(i["type"]=="body_icon_diversity_too_low" for i in v.body_icon_diversity_gate(_div_bad)))
_unique_icon_h2 = '<h2><span class="body-icon"><svg aria-hidden="true"><path d="M1 %d"/></svg></span>t%d</h2>'
_div_ok = '<main class="page-wide layout-expert">' + ''.join('<section>'+(_unique_icon_h2 % (i,i))+'</section>' for i in range(7)) + '</main>'
check("body_icon_diversity gate passes distinct icons", v.body_icon_diversity_gate(_div_ok) == [])
_toc_bad = '<main class="page-wide layout-github"><section><h2>x</h2></section></main>'
check("analysis_toc_map gate flags missing github question toc",
      any(i["type"]=="github_analysis_toc_map_missing" for i in v.analysis_toc_map_required_gate(_toc_bad)))
_toc_ok = '<main class="page-wide layout-github"><nav class="toc-map github-question-toc"><div class="toc-pills"><a class="toc-pill" href="#a"><b>1</b>q</a></div></nav></main>'
check("analysis_toc_map gate passes canonical chip toc", v.analysis_toc_map_required_gate(_toc_ok) == [])
_toc_long_bad = '<main class="page-wide layout-expert">' + ''.join(f'<section><h2><span class="body-icon"><svg aria-hidden="true"></svg></span>s{i}</h2></section>' for i in range(4)) + '</main>'
check("toc-required gate flags non-analysis h2>=4 without toc-map",
      any(i["type"]=="toc_map_required_missing" for i in v.analysis_toc_map_required_gate(_toc_long_bad)))
_toc_short_ok = '<main class="page-wide layout-landing"><section><h2>a</h2></section><section><h2>b</h2></section><section><h2>c</h2></section></main>'
check("toc-required gate ignores short non-analysis page", v.analysis_toc_map_required_gate(_toc_short_ok) == [])
_long_token = 'A'*76 + '_token'
check("long-token gate flags unprotected prose token",
      any(i["type"]=="long_token_overflow_unprotected" for i in v.unprotected_long_token_gate(f'<main class="page-wide layout-expert"><section><h2>x</h2><p>{_long_token}</p></section></main>', '')))
check("long-token gate ignores protected code/pre/a/table tokens",
      v.unprotected_long_token_gate(f'<main class="page-wide layout-expert"><section><h2>x</h2><pre>{_long_token}</pre><a href="#">{_long_token}</a><code>{_long_token}</code></section></main>', '') == [])
check("R4 table gate catches unwrapped table",
      any(i["type"]=="table_no_mobile_safe_wrapper" for i in v.table_mobile_wrapper_gate('<table><caption>c</caption><tr><td>x</td></tr></table>')))
check("R4 table gate accepts .tbl wrapper",
      v.table_mobile_wrapper_gate('<div class="tbl"><table><caption>c</caption><tr><td>x</td></tr></table></div>') == [])

with _tmp.TemporaryDirectory() as _td:
    _root = v.Path(_td)
    _raw = _root / 'raw.html'
    _raw_sections = ''.join(
        '<section><h2><span class="body-icon"><svg aria-hidden="true"></svg></span>Raw</h2>'
        '<p>a</p><p>b</p><div>c</div><li>d</li></section>'
        for _ in range(5)
    )
    _raw.write_text(f'<body><main class="page-wide layout-expert">{_raw_sections}</main></body>', encoding='utf-8')
    check("quality raw-section gate catches raw p/div/li synthesis",
          any(i.code=="raw_section_synthesis_overuse" for i in q.check_html(_raw)))
    _ok = _root / 'ok.html'
    _ok_sections = ''.join(
        '<section><h2><span class="body-icon"><svg aria-hidden="true"></svg></span>Card</h2>'
        '<div class="card-grid"><article class="card-block"><p>a</p></article></div></section>'
        for _ in range(5)
    )
    _ok.write_text(f'<body><main class="page-wide layout-expert">{_ok_sections}</main></body>', encoding='utf-8')
    check("quality raw-section gate accepts canonical components", q.check_html(_ok) == [])

with _tmp.TemporaryDirectory() as _td:
    _root = v.Path(_td)
    (_root / 'sources').mkdir()
    check("completion render-audit fails missing artifact on normal output", c.check_render_audit(_root) is False)
    (_root / 'sources' / 'screenshots').mkdir()
    (_root / 'sources' / 'screenshots' / '1280.png').write_bytes(b'png')
    (_root / 'sources' / 'screenshots' / '390.png').write_bytes(b'png')
    (_root / 'sources' / 'render-audit.json').write_text('{"viewports":{"1280":{"scrollWidth":1280,"clientWidth":1280,"overflow_ok":true,"screenshot":"sources/screenshots/1280.png"},"390":{"scrollWidth":390,"clientWidth":390,"overflow_ok":true,"screenshot":"sources/screenshots/390.png"}}}', encoding='utf-8')
    check("completion render-audit passes overflow_ok screenshots", c.check_render_audit(_root) is True)
    (_root / 'sources' / 'render-audit.json').write_text('{"viewports":{"1280":{"scrollWidth":1290,"clientWidth":1280,"overflow_ok":false,"screenshot":"sources/screenshots/1280.png"},"390":{"scrollWidth":390,"clientWidth":390,"overflow_ok":true,"screenshot":"sources/screenshots/390.png"}}}', encoding='utf-8')
    check("completion render-audit fails overflow false", c.check_render_audit(_root) is False)

with _tmp.TemporaryDirectory() as _td:
    import subprocess as _sp
    _repo = v.Path(_td)
    _sd = _repo / 'skills' / 'adaptive-html-final'
    _sd.mkdir(parents=True)
    (_sd / 'manifest.json').write_text('{"version":"9.9.8"}', encoding='utf-8')
    _sp.run(['git', 'init', '-q'], cwd=_repo, check=True)
    _sp.run(['git', 'add', 'skills/adaptive-html-final/manifest.json'], cwd=_repo, check=True)
    _sp.run(['git', '-c', 'user.name=test', '-c', 'user.email=test@example.com',
             'commit', '-q', '-m', 'baseline'], cwd=_repo, check=True)
    (_sd / 'manifest.json').write_text('{"version":"9.9.9"}', encoding='utf-8')
    _unauth = v.version_release_approval_issues(_repo, _sd, '9.9.9')
    check("version release gate blocks manifest bump without approval",
          _unauth and _unauth[0]["type"] == "version_bump_without_release_approval")
    (_repo / 'dev-plan').mkdir()
    (_repo / 'dev-plan' / 'release-approval-v9.9.9.md').write_text('# approved\n', encoding='utf-8')
    check("version release gate allows approved manifest bump",
          v.version_release_approval_issues(_repo, _sd, '9.9.9') == [])

_manifest_quality = __import__("json").loads((SKILL / "manifest.json").read_text(encoding="utf-8")).get("quality") or {}
check("manifest quality.governance_count matches this self-test count",
      _manifest_quality.get("governance_count") == _checks + 1)

print(f"\n{_checks - _fails}/{_checks} checks passed")
sys.exit(1 if _fails else 0)
