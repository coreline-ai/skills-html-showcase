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

print(f"\n{_checks - _fails}/{_checks} checks passed")
sys.exit(1 if _fails else 0)
