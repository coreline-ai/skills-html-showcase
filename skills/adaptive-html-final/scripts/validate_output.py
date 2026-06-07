#!/usr/bin/env python3
"""Validate adaptive-html-final HTML output folders.

Static gate for generated showcase/output directories. It intentionally avoids
external dependencies so it can run in constrained Codex environments.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path


class MiniHTML(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tags: list[tuple[str, dict[str, str]]] = []
        self.stack: list[tuple[str, dict[str, str]]] = []
        self.h1 = 0
        self.main_id = False
        self.figures: list[dict] = []
        self._cur_figure = None
        self.local_refs: list[tuple[str, str]] = []
        self.external_scripts: list[str] = []
        self.styles: list[str] = []
        self._in_style = False

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.tags.append((tag, attrs))
        self.stack.append((tag, attrs))
        if tag == 'h1':
            self.h1 += 1
        if tag == 'main' and attrs.get('id') == 'main':
            self.main_id = True
        if tag == 'style':
            self._in_style = True
        if tag == 'script' and attrs.get('src', '').startswith(('http://', 'https://')):
            self.external_scripts.append(attrs['src'])
        if tag == 'figure':
            self._cur_figure = {'class': attrs.get('class', ''), 'img': None, 'figcaption': False}
        if tag == 'figcaption' and self._cur_figure is not None:
            self._cur_figure['figcaption'] = True
        if tag == 'img':
            if attrs.get('src') and not attrs['src'].startswith(('http://', 'https://', 'data:')):
                self.local_refs.append(('img', attrs['src']))
            if self._cur_figure is not None:
                self._cur_figure['img'] = attrs
        if tag in ('a', 'link', 'source', 'video', 'audio'):
            key = 'href' if tag in ('a', 'link') else 'src'
            val = attrs.get(key)
            if val and not val.startswith(('http://', 'https://', 'mailto:', 'tel:', '#', 'data:', 'javascript:')):
                self.local_refs.append((tag, val))

    def handle_endtag(self, tag):
        if tag == 'style':
            self._in_style = False
        if tag == 'figure' and self._cur_figure is not None:
            self.figures.append(self._cur_figure)
            self._cur_figure = None
        # best effort stack pop
        for i in range(len(self.stack)-1, -1, -1):
            if self.stack[i][0] == tag:
                del self.stack[i:]
                break

    def handle_data(self, data):
        if self._in_style:
            self.styles.append(data)


def local_path(base_html: Path, ref: str) -> Path | None:
    ref = ref.split('#', 1)[0].split('?', 1)[0]
    if not ref:
        return None
    return (base_html.parent / ref).resolve()


def svg_size(path: Path):
    try:
        root = ET.parse(path).getroot()
        w = root.attrib.get('width')
        h = root.attrib.get('height')
        vb = root.attrib.get('viewBox')
        def num(x):
            return float(re.sub(r'[^0-9.]+', '', x or '0') or 0)
        if w and h:
            return num(w), num(h)
        if vb:
            parts = [float(x) for x in re.split(r'[ ,]+', vb.strip())]
            if len(parts) == 4:
                return parts[2], parts[3]
    except Exception:
        return None
    return None


def widget_static_gate(text: str, style: str) -> list[dict]:
    """Static gate for output pages that embed view widgets (wg- classes).

    Mirrors tests/widget-checklist.md. Only runs when a wg- class is present in
    the page. Returns a list of issue dicts to merge into the page issues. Uses
    only the stdlib (regex over the raw HTML + collected inline <style> text).
    """
    issues: list[dict] = []
    # Detect a widget class inside any class="..."/class='...' attribute.
    has_widget = False
    for cm in re.finditer(r'class\s*=\s*("[^"]*"|\'[^\']*\')', text, re.I):
        if re.search(r'\bwg-', cm.group(1)):
            has_widget = True
            break
    if not has_widget:
        return issues
    # (a) widgets.css must be inlined: look for a known namespaced selector
    #     (e.g. ".wg-01") or the widgets.css header marker ("widget templates").
    if not (re.search(r'\.wg-\d{2}\b', style) or 'widget templates' in style.lower()):
        issues.append({'type': 'widget_css_not_inlined'})
    # (b) no ".wg-" selector leakage outside the wg-<id>- (2-digit) namespace.
    leaks = sorted({
        sm.group(0)
        for sm in re.finditer(r'\.wg-[A-Za-z0-9_-]+', style)
        if not re.match(r'\.wg-\d{2}(?![0-9])', sm.group(0))
    })
    if leaks:
        issues.append({'type': 'widget_selector_namespace_leak', 'detail': leaks})
    # (c) no behavioral <script> in the widget area (application/ld+json is allowed).
    behavioral_scripts = 0
    for sm in re.finditer(r'<script\b([^>]*)>', text, re.I):
        attrs = sm.group(1)
        tm = re.search(r'type\s*=\s*("[^"]*"|\'[^\']*\'|[^\s>]+)', attrs, re.I)
        stype = tm.group(1).strip('\'"').lower() if tm else ''
        if stype != 'application/ld+json':
            behavioral_scripts += 1
    if behavioral_scripts:
        issues.append({'type': 'widget_behavioral_script', 'detail': behavioral_scripts})
    # (d) no forbidden interaction primitives (draggable=/contenteditable=).
    forbidden = sorted({
        fm.group(1).lower()
        for fm in re.finditer(r'\b(draggable|contenteditable)\s*=', text, re.I)
    })
    if forbidden:
        issues.append({'type': 'widget_forbidden_primitive', 'detail': forbidden})
    return issues


def visual_html_gate(text: str, style: str) -> list[dict]:
    """Static gate for SVG->HTML view-template pages (vt- classes).

    Only runs when a vt template class (vt-shell / vt-frame) is used in the
    page. Returns a list of issue dicts to merge into the page issues. Uses
    only the stdlib (regex over the raw HTML + collected inline <style> text).
    """
    issues: list[dict] = []
    # Detect a vt template class (vt-shell / vt-frame) inside any
    # class="..."/class='...' attribute. Mirrors widget_static_gate.
    has_vt = False
    first_vt_pos = None
    for cm in re.finditer(r'class\s*=\s*("[^"]*"|\'[^\']*\')', text, re.I):
        if re.search(r'\b(vt-shell|vt-frame)\b', cm.group(1)):
            has_vt = True
            first_vt_pos = cm.start()
            break
    if not has_vt:
        return issues
    # (a) visual-html.css must be inlined: look for a known namespaced rule
    #     (".vt-shell{" or ".vt-frame{") inside the inline <style> text.
    if not re.search(r'\.(?:vt-shell|vt-frame)\s*\{', style):
        issues.append({'type': 'visual_html_css_not_inlined'})
    # (b) no behavioral <script> on the page (application/ld+json is allowed).
    behavioral_scripts = 0
    for sm in re.finditer(r'<script\b([^>]*)>', text, re.I):
        attrs = sm.group(1)
        tm = re.search(r'type\s*=\s*("[^"]*"|\'[^\']*\'|[^\s>]+)', attrs, re.I)
        stype = tm.group(1).strip('\'"').lower() if tm else ''
        if stype != 'application/ld+json':
            behavioral_scripts += 1
    if behavioral_scripts:
        issues.append({'type': 'visual_html_behavioral_script', 'detail': behavioral_scripts})
    # (c) no forbidden interaction primitives (draggable=/contenteditable=) in
    #     the vt template area (from the first vt class to end of document).
    vt_area = text[first_vt_pos:]
    forbidden = sorted({
        fm.group(1).lower()
        for fm in re.finditer(r'\b(draggable|contenteditable)\s*=', vt_area, re.I)
    })
    if forbidden:
        issues.append({'type': 'visual_html_forbidden_primitive', 'detail': forbidden})
    return issues


VALID_PROFILES = ('widget', 'diagram', 'auto')
_STYLE_ALIAS = {'v5': 'widget', 'v6': 'diagram'}


def _resolve_profile(profile_arg, root: Path, issues: list):
    """Profile resolution priority: --profile arg (1st) -> sources/profile.json (2nd).

    Accepts canonical names or style aliases (v5/v6). Invalid/out-of-range tokens append an
    'invalid_profile' issue and resolve to None (no silent auto fallback). `sources/profile.json`
    is mandatory for deterministic outputs; when --profile and profile.json are both present,
    they must agree after alias normalization. Returns one of VALID_PROFILES or None.
    """
    pj = root / 'sources' / 'profile.json'
    file_profile = None
    if pj.exists():
        try:
            v = json.loads(pj.read_text(encoding='utf-8')).get('profile')
            file_profile = _STYLE_ALIAS.get(str(v).strip().lower(), str(v).strip().lower()) if v is not None else None
            if file_profile not in VALID_PROFILES:
                issues.append({'type': 'invalid_profile', 'source': 'sources/profile.json', 'value': v})
                file_profile = None
        except Exception as e:
            issues.append({'type': 'profile_json_parse_error', 'detail': str(e)})
    else:
        issues.append({'type': 'missing_profile_json',
                       'detail': '결정론 출력은 sources/profile.json에 profile=widget|diagram|auto를 기록해야 한다.'})

    if profile_arg:
        p = str(profile_arg).strip().lower()
        p = _STYLE_ALIAS.get(p, p)
        if p in VALID_PROFILES and file_profile and p != file_profile:
            issues.append({'type': 'profile_mismatch',
                           'source': '--profile vs sources/profile.json',
                           'arg': p,
                           'profile_json': file_profile})
        if p in VALID_PROFILES:
            return p
        issues.append({'type': 'invalid_profile', 'source': '--profile', 'value': str(profile_arg)})
        return None
    return file_profile


def cross_leak_gate(text: str, declared_profile) -> list:
    """Always-on cross-leak gate keyed by the DECLARED profile (markup classes only — 1층).

    diagram: no wg-NN markup. widget: no vt-<a-z> markup (whitelist frozen empty). auto/None: skip.
    CSS-bundle inclusion (2층) is a separate lint/warn, NOT this gate. Core hash (3층) is elsewhere.
    """
    issues = []
    if declared_profile not in ('widget', 'diagram'):
        return issues  # auto / None: cross-leak gate not applicable
    tokens = set()
    for cv in re.findall(r'class\s*=\s*"([^"]*)"', text, re.I) + re.findall(r"class\s*=\s*'([^']*)'", text, re.I):
        tokens.update(cv.split())
    if declared_profile == 'diagram':
        for t in sorted(t for t in tokens if re.match(r'wg-\d{2}', t, re.I)):
            issues.append({'type': 'cross_leak', 'profile': 'diagram', 'found': t})
    else:  # widget — vt- markup must be 0 (whitelist frozen empty)
        whitelist = set()
        for t in sorted(t for t in tokens if re.match(r'vt-[a-z]', t, re.I) and t.lower() not in whitelist):
            issues.append({'type': 'cross_leak', 'profile': 'widget', 'found': t})
    return issues


# ---- Phase 0 governance gates (final_20260604 merge-protection lints) ----

# Gate A: zero !important across skill CSS, except 2 sanctioned widgets.css cases.
IMPORTANT_LINT_ASSETS = [
    'theme.css', 'components.css', 'visual-components.css', 'layouts.css', 'print.css',
    'editorial-patterns.css', 'visual-html.css', 'shape-visuals.css',
    'workflow-visuals.css', 'body-icons.css', 'widgets.css', 'theme-dark.css',
]


def _mask_css_comments(text: str) -> str:
    """Blank out /* ... */ comments while preserving line count/numbers, so the asset
    lints never false-fire on prose inside a comment (e.g. a note mentioning !important)."""
    return re.sub(r'/\*.*?\*/', lambda m: re.sub(r'[^\n]', ' ', m.group(0)), text, flags=re.S)


def _important_allowlisted(asset_name: str, line: str) -> bool:
    """Sanctioned widgets.css cases: .wg-06-rowhead text-align + @keyframes wg-11-grow width:0."""
    if asset_name != 'widgets.css':
        return False
    if '.wg-06-rowhead' in line:
        return True
    if re.search(r'width\s*:\s*0\s*!important', line):
        return True
    return False


# Gate C: bare callout class (.good/.danger/.term/.analogy) reused as a compound state
# modifier outside components.css. .vt-pill is pre-existing/sanctioned (shipped before this gate).
_CALLOUT_RE = re.compile(r'(\.[\w-]+)\.(good|danger|term|analogy)(?![\w-])')
_CALLOUT_CARRIER_ALLOW = {'.vt-pill'}

# Gate D: page-invented class vocabularies that must never appear in canonical skill output.
# Each verified to have 0 occurrences in skill/assets/, so denying them cannot break a
# legitimately generated page. Canonical output uses wg-/vt-(canonical)/wf-(vt-21)/
# workflow-/shape-/bi-/editorial names only.
BESPOKE_CLASS_PREFIXES = (
    'vt-adapt-', 'vt-flow-', 'vt-file-', 'vt-soft-', 'vt-risk-', 'vt-triage-',
    'vt-concept-', 'vt-compare-', 'vt-check-', 'vt-qg-', 'vt-ticket', 'vt-raci',
    'vt-swimlane', 'vt-fill', 'vt-flag',
    'edge-gov-', 'edge-status-', 'edge-ticket', 'edge-flag', 'edge-failure',
    'module-node', 'module-edge',
    'final-softshape', 'final-body-icon', 'final-hero-map', 'final-vt-',
    'static-flow-', 'new-template-', 'imported-toc-',
    'landing-action-', 'seo-result-', 'seo-snippet-', 'seo-rule-', 'seo-variant',
    'platform-conversion-', 'platform-branch-', 'platform-transform-',
    'platform-title-', 'platform-mini-',
    'access-check-', 'access-release', 'access-pass', 'access-fail',
    'token-swatch', 'token-chip', 'token-rhythm',
    'pattern-shell', 'pattern-nav', 'pattern-head', 'pattern-meta', 'pattern-hero-note',
    'widget-',
)


def bespoke_prefix_gate(text: str) -> list:
    """Reject page-invented class vocabularies in output markup."""
    issues = []
    tokens = set()
    for cv in re.findall(r'class\s*=\s*"([^"]*)"', text, re.I) + re.findall(r"class\s*=\s*'([^']*)'", text, re.I):
        tokens.update(cv.split())
    bad = sorted({t for t in tokens if t.startswith(BESPOKE_CLASS_PREFIXES)})
    if bad:
        issues.append({'type': 'bespoke_namespace_class', 'count': len(bad), 'detail': bad[:40],
                       'note': '페이지 발명 어휘는 정본 접두사로 개명 후에만 병합(§3.2). 정식 출력에 등장 금지.'})
    return issues


def global_no_js_gate(text: str) -> list:
    """Invariant #1 enforced GLOBALLY (not only inside wg-/vt- areas): the only allowed
    <script> is type=application/ld+json; no event handler attributes, javascript: href,
    draggable/contenteditable anywhere."""
    issues = []
    bad_scripts = 0
    for sm in re.finditer(r'<script\b([^>]*)>', text, re.I):
        tm = re.search(r'type\s*=\s*("[^"]*"|\'[^\']*\'|[^\s>]+)', sm.group(1), re.I)
        stype = tm.group(1).strip('\'"').lower() if tm else ''
        if stype != 'application/ld+json':
            bad_scripts += 1
    if bad_scripts:
        issues.append({'type': 'behavioral_script_global', 'count': bad_scripts,
                       'note': '무 JS 불변식: <script>는 application/ld+json(JSON-LD)만 허용.'})
    forbidden = sorted({fm.group(1).lower() for fm in re.finditer(r'\b(draggable|contenteditable)\s*=', text, re.I)})
    if forbidden:
        issues.append({'type': 'forbidden_primitive_global', 'detail': forbidden})
    handlers = sorted({fm.group(1).lower() for fm in re.finditer(r'\s(on[a-z][a-z0-9_-]*)\s*=', text, re.I)})
    if handlers:
        issues.append({'type': 'event_handler_global', 'detail': handlers,
                       'note': '무 JS 불변식: onclick/onload 등 인라인 이벤트 핸들러 금지.'})
    if re.search(r'\bhref\s*=\s*["\']\s*javascript:', text, re.I):
        issues.append({'type': 'javascript_href_global',
                       'note': '무 JS 불변식: href="javascript:..." 금지.'})
    return issues


def legacy_theme_toggle_gate(text: str) -> list:
    """v5.2 ships one theme contract: radios name="ahf-theme" (#ahf-light/#ahf-white/#ahf-dark).
    The pre-5.2 single `#theme-toggle` checkbox is deprecated — flag it so stale theme markup
    can't silently ship inside a 5.2 package."""
    if re.search(r'''id\s*=\s*["']theme-toggle["']|#theme-toggle\b''', text):
        return [{'type': 'legacy_theme_toggle',
                 'note': 'legacy #theme-toggle 테마 토글 감지. v5.2는 라디오 name="ahf-theme"(light/white/dark) 단일 계약.'}]
    return []


def theme_switcher_contract_gate(text: str, style: str) -> list:
    """When the v5.2+ theme CSS is inlined, the visible CSS-only switcher must ship too.

    A past regression in the GitHub-analysis output inlined theme-dark.css but omitted
    the #ahf-light/#ahf-white/#ahf-dark radio markup, leaving users unable to change
    light/white/dark modes even though the stylesheet existed. Keep the contract
    explicit so a CSS-only "support" claim cannot pass without the control surface.
    """
    has_theme_css = '.ahf-themebar' in style or '#ahf-dark:checked' in style or 'name=ahf-theme' in style
    if not has_theme_css:
        return []
    issues = []
    if not re.search(r'<fieldset\b[^>]*class=["\'][^"\']*\bahf-themebar\b', text, re.I):
        issues.append({'type': 'theme_switcher_missing_fieldset'})
    _radio_n = len(re.findall(r'<input\b[^>]*name=["\']ahf-theme["\']', text, re.I))
    if _radio_n < 3:
        issues.append({'type': 'theme_switcher_radio_count',
                       'detail': 'name="ahf-theme" 라디오는 최소 3개(light/white/dark)여야 하며 확장 테마(light2/dark2/blue …)를 추가할 수 있다.'})
    # 5-radio 확장 테마(light2/dark2)를 쓰면 둘 다 있어야 한다(반쪽 확장 금지).
    _has_l2 = bool(re.search(r'id=["\']ahf-light2["\']', text, re.I))
    _has_d2 = bool(re.search(r'id=["\']ahf-dark2["\']', text, re.I))
    if _has_l2 != _has_d2:
        issues.append({'type': 'theme_switcher_extended_pair',
                       'detail': '확장 테마는 light2·dark2를 함께 제공해야 한다.'})
    for _id in ('ahf-light', 'ahf-white', 'ahf-dark'):
        if not re.search(r'<input\b[^>]*id=["\']' + re.escape(_id) + r'["\'][^>]*name=["\']ahf-theme["\']', text, re.I) \
           and not re.search(r'<input\b[^>]*name=["\']ahf-theme["\'][^>]*id=["\']' + re.escape(_id) + r'["\']', text, re.I):
            issues.append({'type': 'theme_switcher_missing_radio', 'id': _id})
        if not re.search(r'<label\b[^>]*for=["\']' + re.escape(_id) + r'["\']', text, re.I):
            issues.append({'type': 'theme_switcher_missing_label', 'for': _id})
    if not re.search(r'<input\b(?=[^>]*id=["\']ahf-light["\'])(?=[^>]*name=["\']ahf-theme["\'])(?=[^>]*\bchecked\b)', text, re.I):
        issues.append({'type': 'theme_switcher_light_not_default'})
    return issues


def github_analysis_visual_contract_gate(text: str, style: str) -> list:
    """GitHub-analysis outputs must follow the current showcase visual contract.

    This protects the 14th mode from drifting back to a raw report: latest header
    rhythm (generated-row/lens-strip), section-card shell, and body icons before
    numbered headings are all required for `.layout-github`.
    """
    body_only = re.sub(r'<style\b[^>]*>[\s\S]*?</style>', '', text, flags=re.I)
    if not re.search(r'<main\b[^>]*class=["\'][^"\']*\blayout-github\b', body_only, re.I):
        return []
    issues = []
    if 'generated-row' not in body_only or 'lens-strip' not in body_only:
        issues.append({'type': 'github_header_generated_row_missing'})
    if '.layout-github>section' not in style.replace(' ', ''):
        issues.append({'type': 'github_section_card_css_missing'})
    if '.body-icon' not in style:
        issues.append({'type': 'github_body_icons_css_missing'})
    h2s = re.findall(r'<h2\b[^>]*>[\s\S]*?</h2>', body_only, re.I)
    numbered = [h for h in h2s if re.search(r'<span\b[^>]*class=["\'][^"\']*\bnum\b', h, re.I)]
    missing_icon = [h[:120] for h in numbered if not re.search(r'<span\b[^>]*class=["\'][^"\']*\bbody-icon\b', h, re.I)]
    if missing_icon:
        issues.append({'type': 'github_numbered_heading_icon_missing',
                       'count': len(missing_icon),
                       'detail': missing_icon[:5]})
    return issues


def youtube_analysis_contract_gate(text: str, style: str) -> list:
    """YouTube-analysis outputs must expose evidence, limits, and no-embed contracts."""
    body_only = re.sub(r'<style\b[^>]*>[\s\S]*?</style>', '', text, flags=re.I)
    if not re.search(r'<main\b[^>]*class=["\'][^"\']*\blayout-youtube\b', body_only, re.I):
        return []
    issues = []
    if '.layout-youtube>section' not in style.replace(' ', ''):
        issues.append({'type': 'youtube_section_card_css_missing'})
    if re.search(r'<iframe\b|youtube\.com/embed|youtu\.be/[^\s"\']+[?&]autoplay', body_only, re.I):
        issues.append({'type': 'youtube_embed_or_autoplay_forbidden'})
    if not re.search(r'Video Evidence Map|영상\s*근거|근거\s*지도|타임스탬프', body_only, re.I):
        issues.append({'type': 'youtube_evidence_map_missing'})
    if not re.search(r'Source Limits|출처\s*한계|확인\s*필요|확인\s*불가', body_only, re.I):
        issues.append({'type': 'youtube_source_limits_missing'})
    found = sum(1 for pat in (r'\bFACT\b|사실', r'\bINFERENCE\b|추론', r'\bUNKNOWN\b|확인\s*불가|확인\s*필요') if re.search(pat, body_only, re.I))
    if found < 2:
        issues.append({'type': 'youtube_fact_inference_unknown_labels_missing', 'count': found})
    if not re.search(r'observed_at|분석\s*기준\s*시각|분석\s*기준일', body_only, re.I):
        issues.append({'type': 'youtube_observed_at_missing'})
    return issues


def manual_analysis_contract_gate(text: str, style: str) -> list:
    """Manual-analysis outputs must be role-based, executable, and source-bounded."""
    body_only = re.sub(r'<style\b[^>]*>[\s\S]*?</style>', '', text, flags=re.I)
    if not re.search(r'<main\b[^>]*class=["\'][^"\']*\blayout-manual\b', body_only, re.I):
        return []
    issues = []
    if '.layout-manual>section' not in style.replace(' ', ''):
        issues.append({'type': 'manual_section_card_css_missing'})
    required = [
        ('manual_source_version_missing', r'Source\s*&\s*Version|출처.*버전|버전.*출처|source snapshot'),
        ('manual_role_router_missing', r'Reader\s*Role\s*Router|역할별|독자\s*경로|role router'),
        ('manual_prerequisites_safety_missing', r'Prerequisites|Safety|사전조건|안전|권한|위험'),
        ('manual_troubleshooting_missing', r'Troubleshooting|트러블슈팅|문제\s*해결|증상|원인|진단'),
        ('manual_source_limits_missing', r'Source\s*Limits|출처\s*한계|확인\s*불가|UNKNOWN'),
    ]
    for typ, pat in required:
        if not re.search(pat, body_only, re.I):
            issues.append({'type': typ})
    if re.search(r'\bstale\b|오래된|모순', body_only, re.I) and not re.search(r'근거|원문|위치|확인\s*불가', body_only, re.I):
        issues.append({'type': 'manual_audit_claim_without_source'})
    return issues


def numbered_h2_body_icon_gate(text: str) -> list:
    """전 모드 공통 시각 정본: 번호 칩(.num/.no)을 단 섹션 h2는 body-icon도 함께 단다.
    16개 예제가 numbered h2에 body-icon을 ~100% 적용하는 정본을 성문화(github 전용 계약의 전역화).
    마크업 레벨 검사(인라인 <style>은 제외)."""
    body = re.sub(r'<style\b[^>]*>[\s\S]*?</style>', '', text, flags=re.I)
    issues = []
    for m in re.finditer(r'<h2\b[^>]*>([\s\S]*?)</h2>', body, re.I):
        inner = m.group(1)
        if re.search(r'class\s*=\s*["\'][^"\']*\b(?:num|no)\b', inner) and 'body-icon' not in inner:
            issues.append({'type': 'numbered_h2_missing_body_icon',
                           'h2': re.sub(r'<[^>]+>', '', inner).strip()[:60],
                           'detail': '번호 단 섹션 h2는 body-icon→번호→제목 정본을 따른다(예제 전 모드 공통).'})
    return issues


def section_surface_contract_gate(text: str, style: str) -> list:
    """전 모드 공통: layout-* 콘텐츠 페이지의 주요 섹션은 통일된 card/view surface 위에 둔다.
    정적 검사 — 통일 섹션 surface 규칙(>section:not(.try) 또는 >article>section의 card 배경)이
    인라인 CSS에 존재하는지로 회귀를 막는다. .try(검정 hero)는 제외. github 전용 surface 계약의 전역 승격."""
    if not re.search(r'<main\b[^>]*class\s*=\s*["\'][^"\']*\blayout-[a-z-]+', text, re.I):
        return []
    norm = re.sub(r'\s+', '', style)
    # 직접 섹션 규칙 .page(-wide)?>section:not(.try) 카드 규칙이어야 한다 — article>section 우회나 :not([class])로는 불충분(직접 섹션이 class 있어도 카드여야 함).
    if re.search(r'\.page(-wide)?>section:not\(\.try\)[^{]*\{[^}]*background:var\(--card\)', norm):
        return []
    return [{'type': 'section_surface_css_missing',
             'detail': '직접 섹션 통일 surface(.page-wide>section:not(.try) card 규칙) 미인라인 — class 무관 직접 섹션 카드 계약 위반.'}]


MODE_DEPTH_MIN_AVG = 400   # visible chars per h2 section on mode pages
MODE_DEPTH_MIN_H2 = 6      # gate only fires on many-section mode pages


def _visible_body_text(text: str) -> str:
    """Visible prose of the page body: <body> without <style>/<script>, tags stripped,
    whitespace collapsed. Used by the depth gate."""
    body = re.search(r'<body\b[^>]*>([\s\S]*?)</body>', text, re.I)
    body = body.group(1) if body else text
    body = re.sub(r'<style\b[^>]*>[\s\S]*?</style>', '', body, flags=re.I)
    body = re.sub(r'<script\b[^>]*>[\s\S]*?</script>', '', body, flags=re.I)
    return re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', body)).strip()


def mode_depth_gate(text: str) -> list:
    """Anti wide-and-thin gate. Mode pages (main.layout-*) with many h2 sections must
    carry per-section prose. Catches the v5.7.0 failure mode where youtube/manual
    filled 12-13 section skeletons with ~300 visible chars per section while passing
    every structural gate (SKILL.md §4 정량 하한의 정적 근사)."""
    body_only = re.sub(r'<style\b[^>]*>[\s\S]*?</style>', '', text, flags=re.I)
    if not re.search(r'<main\b[^>]*class=["\'][^"\']*\blayout-[a-z]', body_only, re.I):
        return []
    h2 = len(re.findall(r'<h2\b', body_only, re.I))
    if h2 < MODE_DEPTH_MIN_H2:
        return []
    visible = len(_visible_body_text(text))
    avg = visible // h2
    if avg < MODE_DEPTH_MIN_AVG:
        return [{'type': 'mode_section_depth_too_thin', 'h2_count': h2,
                 'visible_chars': visible, 'avg_per_h2': avg, 'min_avg': MODE_DEPTH_MIN_AVG,
                 'detail': '섹션 수 대비 본문이 얇다(넓고 얇은 출력). SKILL.md §4 정량 하한 미달 — 섹션을 줄이거나 각 섹션의 근거·해석을 채워 재생성한다.'}]
    return []


def profile_vt_required_gate(text: str, profile: str | None) -> list:
    """§0.6 계약: diagram/auto 프로파일 출력은 모드 페이지마다 vt- 템플릿을 최소 1회
    삽입해야 한다. index/galleries(layout- 없는 main)는 대상이 아니다."""
    if profile not in ('diagram', 'auto'):
        return []
    body_only = re.sub(r'<style\b[^>]*>[\s\S]*?</style>', '', text, flags=re.I)
    if not re.search(r'<main\b[^>]*class=["\'][^"\']*\blayout-[a-z]', body_only, re.I):
        return []
    if re.search(r'class=["\'][^"\']*\bvt-[a-z]', body_only, re.I):
        return []
    return [{'type': 'profile_vt_template_missing', 'profile': profile,
             'detail': 'diagram/auto 프로파일 모드 페이지에 vt- 템플릿이 없다. §0.6 해당 모드 행의 1순위 vt-템플릿을 최소 1회 삽입한다.'}]


def _inner_html(text: str, open_end: int, tag: str) -> str:
    """Inner HTML of the element whose opening tag ends at open_end, by balancing nested
    <tag>/</tag>. Falls back to a bounded window if the tag never closes (malformed)."""
    depth = 1
    window = text[open_end:open_end + 20000]
    for mm in re.finditer(r'<(/?)' + re.escape(tag) + r'\b', window, re.I):
        depth += -1 if mm.group(1) else 1
        if depth == 0:
            return window[:mm.start()]
    return window[:1800]


def role_img_buries_text_gate(text: str) -> list:
    """role="img" on a text-bearing container (not figure/img/svg) prunes its text from
    assistive tech. Generalizes the wf-board-specific check to any bespoke container.
    Scopes the text scan to the element's OWN subtree (balanced tags) so a decorative
    container with text-bearing *siblings* is not false-flagged."""
    issues = []
    for m in re.finditer(r'<(div|section|article|ul|ol|nav|aside)\b([^>]*)\brole\s*=\s*["\']img["\']([^>]*)>', text, re.I):
        attrs = m.group(2) + m.group(3)
        if 'wf-board' in attrs:  # already covered by the specific soft-workflow gate
            continue
        inner = _inner_html(text, m.end(), m.group(1))
        if re.search(r'<(?:h[2-6]|p|li|strong)\b', inner, re.I):
            cls = re.search(r'class\s*=\s*("[^"]*"|\'[^\']*\')', attrs, re.I)
            issues.append({'type': 'role_img_buries_text', 'el': m.group(1).lower(),
                           'class': cls.group(1).strip('\'"') if cls else '',
                           'detail': '텍스트 포함 컨테이너에 role="img" → 스크린리더가 텍스트를 prune. role 제거, 장식 요소만 aria-hidden.'})
            break
    return issues


def skill_asset_lint(skill_dir: Path) -> list:
    """Merge-protection lints on the skill's own CSS assets (run when --skill-dir given).
    Asset-level issues (no 'page' key). Protects the final_20260604 section merge."""
    issues = []
    assets = skill_dir / 'assets'
    # Comment-masked text per CSS asset (so lints never false-fire on prose in /* */).
    masked = {p.name: _mask_css_comments(p.read_text(encoding='utf-8')) for p in assets.glob('*.css')}
    # Gate A: zero !important (2 sanctioned widgets.css cases allowlisted).
    bad_imp = []
    for name in IMPORTANT_LINT_ASSETS:
        if name not in masked:
            continue
        for i, line in enumerate(masked[name].splitlines(), 1):
            if '!important' in line and not _important_allowlisted(name, line):
                bad_imp.append({'asset': name, 'line': i, 'text': line.strip()[:120]})
    if bad_imp:
        issues.append({'type': 'important_in_core_css', 'count': len(bad_imp), 'detail': bad_imp[:30]})
    # Gate B: forbidden page-local font token --report-sans/--report-serif.
    bad_tok = []
    for name, text in sorted(masked.items()):
        for i, line in enumerate(text.splitlines(), 1):
            if re.search(r'--report-(?:sans|serif)\b', line):
                bad_tok.append({'asset': name, 'line': i})
    if bad_tok:
        issues.append({'type': 'forbidden_report_font_token', 'count': len(bad_tok), 'detail': bad_tok[:30],
                       'note': '--report-* 토큰은 스킬에 미정의 → var(--sans)/var(--serif)로 재작성.'})
    # Gate C: bare callout class as compound modifier outside components.css.
    bad_callout = []
    for name, text in sorted(masked.items()):
        if name == 'components.css':
            continue
        for sm in re.finditer(r'([^{}]+)\{', text):
            selector = sm.group(1)
            for cm in _CALLOUT_RE.finditer(selector):
                if cm.group(1) in _CALLOUT_CARRIER_ALLOW:
                    continue
                bad_callout.append({'asset': name, 'selector': ' '.join(selector.split())[-80:],
                                    'modifier': cm.group(0)})
    if bad_callout:
        issues.append({'type': 'bare_callout_modifier', 'count': len(bad_callout), 'detail': bad_callout[:30],
                       'note': '비콜아웃 셀렉터의 베어 .good/.danger/.term/.analogy 수식자 금지 → 네임스페이스형(--ok/--done)으로 개명.'})
    return issues


def changelog_duplicate_versions(changelog_text: str) -> list:
    """Pure correctness: a CHANGELOG must not repeat a version header. Returns the
    list of versions that appear more than once (in file order, de-duplicated)."""
    seen, dups, out = set(), set(), []
    for ver in re.findall(r'(?m)^##\s+v(\d+\.\d+\.\d+)\b', changelog_text):
        if ver in seen and ver not in dups:
            dups.add(ver); out.append(ver)
        seen.add(ver)
    return out


def examples_fidelity_conflict(skill_md: str, manifest_json: str) -> bool:
    """Pure correctness: SKILL.md and manifest must not describe the examples with
    opposite fidelity adjectives (one '경량/lightweight', the other '풀 스킬급/full
    skill-grade'). This is the SKILL.md↔manifest contradiction that no other gate saw.
    Intentionally NOT a length/trigger heuristic — only a same-subject contradiction."""
    def fid(text):
        light = bool(re.search(r'경량\s*참조\s*예제|light\s*weight|lightweight', text, re.I))
        full = bool(re.search(r'풀\s*스킬급|full[-\s]*skill[-\s]*grade', text, re.I))
        return light, full
    s_light, s_full = fid(skill_md)
    m_light, m_full = fid(manifest_json)
    return (s_light and m_full) or (s_full and m_light)


def skill_doc_consistency_gate(skill_dir: Path) -> list:
    """Source-doc correctness gate (run when --skill-dir given). Catches the editorial
    drift the value/hash/count gates structurally cannot: duplicate CHANGELOG versions
    and SKILL.md↔manifest examples-fidelity contradiction. No length/trigger rules."""
    issues = []
    changelog = skill_dir / 'CHANGELOG.md'
    if changelog.exists():
        for ver in changelog_duplicate_versions(changelog.read_text(encoding='utf-8')):
            issues.append({'type': 'changelog_duplicate_version', 'version': ver})
    skill_md_p, manifest_p = skill_dir / 'SKILL.md', skill_dir / 'manifest.json'
    if skill_md_p.exists() and manifest_p.exists():
        if examples_fidelity_conflict(skill_md_p.read_text(encoding='utf-8'),
                                      manifest_p.read_text(encoding='utf-8')):
            issues.append({'type': 'examples_fidelity_contradiction',
                           'detail': 'SKILL.md와 manifest가 examples를 경량 vs 풀 스킬급으로 상반 서술.'})
    return issues


def _direct_child_blocks(html: str, tag: str):
    """Yield (attrs, inner_html) for direct child blocks of `tag` in an HTML fragment.

    Regex-only gates previously treated nested widget `<section>` blocks as if
    they were direct layout sections. The visual contract is intentionally
    scoped to `main > section` and `main > article > section`; widgets nested
    inside those sections keep their own namespace/title system.
    """
    depth = 0
    tag_l = tag.lower()
    void_tags = {'area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'}
    token_re = re.compile(r'<(/?)([a-zA-Z][\w:-]*)([^>]*)>', re.I)
    for m in token_re.finditer(html):
        closing = bool(m.group(1))
        name = m.group(2).lower()
        attrs = m.group(3) or ''
        self_closing = attrs.rstrip().endswith('/') or name in void_tags
        if not closing and name == tag_l and depth == 0:
            yield attrs, _inner_html(html, m.end(), tag_l)
        if closing:
            depth = max(depth - 1, 0)
        elif not self_closing:
            depth += 1


def direct_section_h2_icon_gate(text: str) -> list:
    """전 모드 공통: layout-*의 직접 콘텐츠 섹션 첫 h2는 body-icon을 가진다.

    범위는 `main > section` 및 `main > article > section`이다. 위젯/비주얼 템플릿이
    콘텐츠 섹션 내부에 자체 `<section>`을 쓰는 것은 별도 네임스페이스 계약이므로
    여기서 직접 섹션으로 오판하지 않는다.
    """
    body = re.sub(r'<style\b[^>]*>[\s\S]*?</style>', '', text, flags=re.I)
    main_open = re.search(r'<main\b([^>]*)>', body, re.I)
    if not main_open or not re.search(r'class\s*=\s*["\'][^"\']*\blayout-[a-z-]+', main_open.group(1), re.I):
        return []
    main_inner = _inner_html(body, main_open.end(), 'main')
    candidates = list(_direct_child_blocks(main_inner, 'section'))
    for _article_attrs, article_inner in _direct_child_blocks(main_inner, 'article'):
        candidates.extend(_direct_child_blocks(article_inner, 'section'))
    issues = []
    for attrs, inner in candidates:
        cm = re.search(r'class\s*=\s*["\']([^"\']*)', attrs)
        cls = cm.group(1) if cm else ''
        if 'try' in cls.split():
            continue
        h2 = re.search(r'<h2\b[^>]*>([\s\S]*?)</h2>', inner, re.I)
        if h2 and 'body-icon' not in h2.group(1):
            issues.append({'type': 'direct_section_h2_missing_body_icon',
                           'h2': re.sub(r'<[^>]+>', '', h2.group(1)).strip()[:50],
                           'detail': '직접 콘텐츠 섹션 첫 h2는 body-icon→(num)→title 정본을 따른다(아이콘 필수).'})
    return issues




def toc_map_contract_gate(text: str) -> list:
    """toc-map 목차는 정본 chip-nav 구조를 써야 한다.

    `.toc-map` 안에 bare `<a>`만 넣으면 CSS가 `.toc-pill`에 걸리지 않아
    번호와 텍스트가 붙은 밑줄 링크로 렌더링된다. 정본은
    `.toc-map` + `.toc-pills` + `a.toc-pill > b` 구조다.
    """
    body = re.sub(r'<style\b[^>]*>[\s\S]*?</style>', '', text, flags=re.I)
    issues = []
    for m in re.finditer(r'<(?P<tag>section|nav|div|ol|ul)\b(?P<attrs>[^>]*)class\s*=\s*["\'][^"\']*\btoc-map\b[^"\']*["\'][^>]*>', body, re.I):
        inner = _inner_html(body, m.end(), m.group('tag').lower())
        if 'toc-pills' not in inner or 'toc-pill' not in inner:
            issues.append({'type': 'toc_map_contract_missing_pills',
                           'detail': 'toc-map은 .toc-pills 래퍼와 a.toc-pill 항목을 써야 한다. bare <a><span>…</span> 구조는 목차가 붙어 보이는 회귀를 만든다.'})
            continue
        bad_links = re.findall(r'<a\b(?![^>]*class\s*=\s*["\'][^"\']*\btoc-pill\b)', inner, re.I)
        if bad_links:
            issues.append({'type': 'toc_map_contract_bare_link',
                           'detail': 'toc-map 내부 링크는 모두 class="toc-pill"이어야 한다.'})
        if re.search(r'<a\b[^>]*class\s*=\s*["\'][^"\']*\btoc-pill\b[^>]*>(?![\s\S]*?<b>)', inner, re.I):
            issues.append({'type': 'toc_map_contract_missing_number_badge',
                           'detail': 'toc-pill은 번호 배지 <b>N</b>를 포함해야 한다.'})
    return issues




def expert_decision_grid_section_gate(text: str) -> list:
    """Expert layout regression guard: `.decision-grid` is an inner grid helper, not a direct section class.

    If a direct expert section uses class `decision-grid`, the global grid selector can turn
    the whole section into columns and push content into the first column, causing large blank
    space and mobile overflow. Use `section.decision-section` + inner `.expert-inner-grid` or
    `div.decision-grid` instead.
    """
    body = re.sub(r'<style\b[^>]*>[\s\S]*?</style>', '', text, flags=re.I)
    main_open = re.search(r'<main\b([^>]*)>', body, re.I)
    if not main_open or not re.search(r'class\s*=\s*["\'][^"\']*\blayout-expert\b', main_open.group(1), re.I):
        return []
    main_inner = _inner_html(body, main_open.end(), 'main')
    for attrs, _inner in _direct_child_blocks(main_inner, 'section'):
        cm = re.search(r'class\s*=\s*["\']([^"\']*)', attrs)
        cls = cm.group(1).split() if cm else []
        if 'decision-grid' in cls:
            return [{'type': 'expert_decision_grid_section_collision',
                     'detail': 'layout-expert 직접 section에 decision-grid class 금지. section은 decision-section, grid는 내부 wrapper(.expert-inner-grid/div.decision-grid)에 둔다.'}]
    return []


def expert_validation_checklist_widget_gate(text: str) -> list:
    """Expert validation checklist is an evidence/checklist section, not a PR/release section.

    `wg-03`(Annotated PR) and `wg-17`(PR Writeup) are valid expert widgets, but nesting
    them inside `.validation-checklist` makes the completion-evidence section render as
    a long code-review/release-note block. Keep those widgets in their own review/release
    sections and keep validation to evidence matrix / quality-gate / checklist content.
    """
    body = re.sub(r'<style\b[^>]*>[\s\S]*?</style>', '', text, flags=re.I)
    main_open = re.search(r'<main\b([^>]*)>', body, re.I)
    if not main_open or not re.search(r'class\s*=\s*["\'][^"\']*\blayout-expert\b', main_open.group(1), re.I):
        return []
    main_inner = _inner_html(body, main_open.end(), 'main')
    issues = []
    for attrs, inner in _direct_child_blocks(main_inner, 'section'):
        cm = re.search(r'class\s*=\s*["\']([^"\']*)', attrs)
        cls = cm.group(1).split() if cm else []
        if 'validation-checklist' not in cls:
            continue
        if re.search(r'class\s*=\s*["\'][^"\']*\bwg-(?:03|17)\b', inner, re.I):
            issues.append({'type': 'expert_validation_widget_misuse',
                           'detail': 'layout-expert .validation-checklist 안에 wg-03/wg-17 금지. 검증 섹션은 완료 기준·명령 증빙·렌더 증빙·판정 전용으로 유지한다.'})
    return issues


def header_contract_gate(text: str) -> list:
    """고정 계약(필수): layout-* 콘텐츠 페이지는 상단에 정본 <header class="header">를 갖는다 —
    kicker + h1(1) + sub + meta. generated-row는 권고. 헤더 형태를 고정해 모드·내용 무관하게
    시작부가 일관되게 보이도록(자유 본문 앞 불변부)."""
    if not re.search(r'<main\b[^>]*class\s*=\s*["\'][^"\']*\blayout-[a-z-]+', text, re.I):
        return []
    body = re.sub(r'<style\b[^>]*>[\s\S]*?</style>', '', text, flags=re.I)
    hm = re.search(r'<header\b[^>]*class\s*=\s*["\'][^"\']*\bheader\b', body, re.I)
    if not hm:
        return [{'type': 'header_contract_missing_header', 'detail': '정본 <header class="header"> 없음(헤더 형태 고정 위반).'}]
    gt = body.find('>', hm.start())
    header_inner = _inner_html(body, gt + 1, 'header')
    issues = []
    for name, pat in (('kicker', r'class\s*=\s*["\'][^"\']*\bkicker\b'),
                      ('sub', r'class\s*=\s*["\'][^"\']*\bsub\b'),
                      ('meta', r'class\s*=\s*["\'][^"\']*\bmeta\b')):
        if not re.search(pat, header_inner, re.I):
            issues.append({'type': 'header_contract_missing_part', 'part': name,
                           'detail': '정본 헤더 고정: kicker·h1·sub·meta 필요 — .%s 누락.' % name})
    if not re.search(r'<h1\b', header_inner, re.I):
        issues.append({'type': 'header_contract_missing_part', 'part': 'h1', 'detail': '정본 헤더에 h1 누락.'})
    return issues


def closing_summary_recommendation(text: str) -> list:
    """권고(warning, 강제 아님): layout-* 페이지의 마지막 직접 섹션은 정리/Next-Actions(.try) 형태를 권한다.
    마무리 섹션 형태 일관성 권고 — 없어도 실패는 아님."""
    if not re.search(r'<main\b[^>]*class\s*=\s*["\'][^"\']*\blayout-[a-z-]+', text, re.I):
        return []
    body = re.sub(r'<style\b[^>]*>[\s\S]*?</style>', '', text, flags=re.I)
    mo = re.search(r'<main\b[^>]*>', body, re.I)
    if not mo:
        return []
    main_inner = _inner_html(body, mo.end(), 'main')
    secs = list(_direct_child_blocks(main_inner, 'section'))
    if not secs:
        return []
    cm = re.search(r'class\s*=\s*["\']([^"\']*)', secs[-1][0])
    if not cm or 'try' not in cm.group(1).split():
        return [{'type': 'closing_summary_recommended',
                 'detail': '마지막 정리 섹션(.try Next Actions) 권고 — 마무리 일관성(권고, 강제 아님).'}]
    return []


def validate(root: Path, skill_dir: Path | None = None, profile: str | None = None) -> dict:
    issues = []
    warnings = []
    declared_profile = _resolve_profile(profile, root, issues)
    expected_css_hash = None
    expected_asset_hashes = None
    all_skill_css_hashes = None
    asset_texts = {}
    asset_order = ['theme.css', 'components.css', 'visual-components.css', 'layouts.css', 'print.css']
    conditional_order = ['widgets.css', 'visual-html.css', 'body-icons.css', 'editorial-patterns.css', 'shape-visuals.css', 'workflow-visuals.css', 'theme-dark.css']
    if skill_dir:
        asset_paths = [skill_dir/'assets'/name for name in asset_order]
        if all(p.exists() for p in asset_paths):
            asset_texts = {name: (skill_dir/'assets'/name).read_text(encoding='utf-8') for name in asset_order}
            core_css = '\n'.join(asset_texts[name] for name in asset_order)
            expected_css_hash = hashlib.sha256(core_css.encode('utf-8')).hexdigest()
            expected_asset_hashes = {name: hashlib.sha256(asset_texts[name].encode('utf-8')).hexdigest() for name in asset_order}
            # All CSS assets (core + conditional) for snapshot/recorded-hash currency checks.
            all_skill_css_hashes = dict(expected_asset_hashes)
            for _name in conditional_order:
                _p = skill_dir/'assets'/_name
                if _p.exists():
                    all_skill_css_hashes[_name] = hashlib.sha256(_p.read_text(encoding='utf-8').encode('utf-8')).hexdigest()
        else:
            warnings.append({'type': 'missing_skill_css_assets', 'asset_order': asset_order})
    htmls = sorted(root.glob('*.html')) + sorted((root/'pages').glob('*.html'))
    for html in htmls:
        rel = str(html.relative_to(root))
        text = html.read_text(encoding='utf-8', errors='replace')
        parser = MiniHTML(); parser.feed(text)
        if re.search(r'<p\b[^>]*class=["\'][^"\']*\bh2-sub\b[^"\']*["\'][^>]*>(?:(?!</p>).)*?</h2>', text, re.I|re.S):
            issues.append({'page': rel, 'type': 'h2_sub_closed_as_h2'})
        if re.search(r'<section\b[^>]*class=["\'][^"\']*\bplatform-grid\b', text, re.I):
            issues.append({'page': rel, 'type': 'platform_grid_used_as_section'})
        for tm in re.finditer(r'<table\b[^>]*>[\s\S]*?</table>', text, re.I):
            if '<caption' not in tm.group(0).lower():
                issues.append({'page': rel, 'type': 'table_missing_caption'})
        if parser.h1 != 1:
            issues.append({'page': rel, 'type': 'h1_count', 'detail': parser.h1})
        if not parser.main_id:
            issues.append({'page': rel, 'type': 'missing_main_id'})
        if parser.external_scripts:
            issues.append({'page': rel, 'type': 'external_script', 'detail': parser.external_scripts})
        style = '\n'.join(parser.styles)
        if expected_css_hash:
            m = re.search(r'adaptive-html-final-core-css-sha256:\s*([a-f0-9]{64})', style)
            if not m:
                issues.append({'page': rel, 'type': 'missing_inline_css_hash_marker'})
            elif m.group(1) != expected_css_hash:
                issues.append({'page': rel, 'type': 'inline_css_hash_mismatch', 'expected': expected_css_hash, 'actual': m.group(1)})
            for name in asset_order:
                if asset_texts.get(name) and asset_texts[name] not in style:
                    issues.append({'page': rel, 'type': 'inline_core_css_not_verbatim', 'asset': name,
                                   'detail': '코어 CSS는 asset 원문을 byte-for-byte 인라인해야 한다.'})
        if skill_dir:
            theme_dark_path = skill_dir / 'assets' / 'theme-dark.css'
            if theme_dark_path.exists():
                theme_dark_text = theme_dark_path.read_text(encoding='utf-8')
                if theme_dark_text not in style:
                    issues.append({'page': rel, 'type': 'theme_dark_css_not_inlined',
                                   'detail': 'theme-dark.css는 print.css 뒤 맨끝에 항상 원문 인라인해야 한다.'})
            profile_assets = {
                'widget': {'required': ['widgets.css'], 'forbidden': ['visual-html.css']},
                'diagram': {'required': ['visual-html.css'], 'forbidden': ['widgets.css']},
                'auto': {'required': ['widgets.css', 'visual-html.css'], 'forbidden': []},
            }.get(declared_profile)
            if profile_assets:
                for name in profile_assets['required']:
                    p = skill_dir / 'assets' / name
                    if p.exists() and p.read_text(encoding='utf-8') not in style:
                        issues.append({'page': rel, 'type': 'profile_required_css_not_inlined',
                                       'profile': declared_profile, 'asset': name})
                for name in profile_assets['forbidden']:
                    p = skill_dir / 'assets' / name
                    if p.exists() and p.read_text(encoding='utf-8') in style:
                        issues.append({'page': rel, 'type': 'profile_forbidden_css_inlined',
                                       'profile': declared_profile, 'asset': name})
        if re.search(r'(?:caption|\.caption)[^{]*\{[^}]*margin-[^:]+:\s*-', style, re.I|re.S) or re.search(r'(?:caption|\.caption)[^{]*\{[^}]*margin\s*:[^;}]*-', style, re.I|re.S):
            issues.append({'page': rel, 'type': 'caption_negative_margin'})
        # Known old regression: semantic section wrapper classes must not be direct grid/card selectors.
        old_grid = re.search(r'\.risk-matrix\s*,\s*\.priority-roadmap[^{]+\{[^}]*display\s*:\s*grid', style, re.S)
        if old_grid:
            issues.append({'page': rel, 'type': 'semantic_section_grid_selector'})
        if 'section>h2:first-child' not in style:
            issues.append({'page': rel, 'type': 'missing_section_first_heading_margin_reset'})
        for m in re.finditer(r'([^{}]+)\{([^{}]*)\}', style, re.S):
            selector = ' '.join(m.group(1).split())
            body = m.group(2)
            if 'display:grid' in body.replace(' ', '') and ('.winners:not(section)' in selector or '.tradeoffs:not(section)' in selector):
                issues.append({'page': rel, 'type': 'winners_tradeoffs_heading_grid_regression', 'selector': selector})
        if re.search(r'\.layout-case\s+\.timeline\s*\{[^}]*border-left\s*:\s*(?!0)', style, re.S):
            issues.append({'page': rel, 'type': 'case_timeline_duplicate_left_rule'})
        if re.search(r'\.timeline-card\s*\{[^}]*border-left\s*:\s*(?:[2-9]|\d{2,})px', style, re.S):
            issues.append({'page': rel, 'type': 'timeline_card_heavy_left_rule'})
        if '.try .summary-card' not in style or not re.search(r'\.try\s+\.summary-card\s+p[\s\S]*?color\s*:\s*var\(--ink-soft\)', style):
            issues.append({'page': rel, 'type': 'missing_try_nested_card_contrast_reset'})
        if '.try .tag' not in style or not re.search(r'\.try(?:\.soft-cta)?\s+\.tag[\s\S]*?color\s*:\s*var\(--ink\)', style):
            issues.append({'page': rel, 'type': 'missing_try_tag_contrast_reset'})
        if '--link-on-dark' not in style or not re.search(r'\.try(?:\.soft-cta)?\s+a[\s\S]*?color\s*:\s*var\(--link-on-dark\)', style):
            issues.append({'page': rel, 'type': 'missing_try_dark_link_contrast_reset'})
        if '.layout-blog article>section>h2:first-child::before' not in style:
            issues.append({'page': rel, 'type': 'missing_blog_section_counter'})
        if re.search(r'\.layout-seo\s+\.serp-title\s*\{[^}]*#1a0dab', style, re.I|re.S) or re.search(r'\.layout-seo\s+\.serp-title\s*\{[^}]*Arial', style, re.I|re.S):
            issues.append({'page': rel, 'type': 'seo_serp_title_literal_google_style'})
        if re.search(r'\.layout-platform\s+\.platform-grid\s*\{[^}]*display\s*:\s*grid', style, re.I|re.S):
            issues.append({'page': rel, 'type': 'platform_grid_selector_allows_section_grid'})
        for wg_issue in widget_static_gate(text, style):
            wg_issue['page'] = rel
            issues.append(wg_issue)
        for vt_issue in visual_html_gate(text, style):
            vt_issue['page'] = rel
            issues.append(vt_issue)
        for cl_issue in cross_leak_gate(text, declared_profile):
            cl_issue['page'] = rel
            issues.append(cl_issue)
        for bp_issue in bespoke_prefix_gate(text):
            bp_issue['page'] = rel
            issues.append(bp_issue)
        for js_issue in global_no_js_gate(text):
            js_issue['page'] = rel
            issues.append(js_issue)
        for tg_issue in legacy_theme_toggle_gate(text):
            tg_issue['page'] = rel
            issues.append(tg_issue)
        for ts_issue in theme_switcher_contract_gate(text, style):
            ts_issue['page'] = rel
            issues.append(ts_issue)
        for gh_issue in github_analysis_visual_contract_gate(text, style):
            gh_issue['page'] = rel
            issues.append(gh_issue)
        for yt_issue in youtube_analysis_contract_gate(text, style):
            yt_issue['page'] = rel
            issues.append(yt_issue)
        for man_issue in manual_analysis_contract_gate(text, style):
            man_issue['page'] = rel
            issues.append(man_issue)
        for icon_issue in numbered_h2_body_icon_gate(text):
            icon_issue['page'] = rel
            issues.append(icon_issue)
        for surf_issue in section_surface_contract_gate(text, style):
            surf_issue['page'] = rel
            issues.append(surf_issue)
        for dsi_issue in direct_section_h2_icon_gate(text):
            dsi_issue['page'] = rel
            issues.append(dsi_issue)
        for hdr_issue in header_contract_gate(text):
            hdr_issue['page'] = rel
            issues.append(hdr_issue)
        for cls_warn in closing_summary_recommendation(text):
            cls_warn['page'] = rel
            warnings.append(cls_warn)
        for toc_issue in toc_map_contract_gate(text):
            toc_issue['page'] = rel
            issues.append(toc_issue)
        for expert_grid_issue in expert_decision_grid_section_gate(text):
            expert_grid_issue['page'] = rel
            issues.append(expert_grid_issue)
        for expert_val_issue in expert_validation_checklist_widget_gate(text):
            expert_val_issue['page'] = rel
            issues.append(expert_val_issue)
        for dp_issue in mode_depth_gate(text):
            dp_issue['page'] = rel
            issues.append(dp_issue)
        for vtm_issue in profile_vt_required_gate(text, declared_profile):
            vtm_issue['page'] = rel
            issues.append(vtm_issue)
        for ri_issue in role_img_buries_text_gate(text):
            ri_issue['page'] = rel
            issues.append(ri_issue)
        ph = sorted(set(re.findall(r'\{\{[A-Z_]+\}\}', text)))
        if ph:
            issues.append({'page': rel, 'type': 'unfilled_placeholder', 'found': ph})
        # Body icon gate: if body icons (bi-/.body-icon) are used, their CSS must be inlined
        # and the icon SVGs must be decorative (aria-hidden). No-JS is covered by external_script.
        if re.search(r'class=["\'][^"\']*\bbody-icon\b', text) or re.search(r'class=["\']bi-(?:line|soft|fill|accent|dot)', text):
            if '.body-icon' not in style:
                issues.append({'page': rel, 'type': 'body_icons_css_not_inlined'})
            for m in re.finditer(r'<span\b[^>]*class=["\'][^"\']*\bbody-icon\b[^>]*>\s*<svg\b([^>]*)>', text, re.I):
                if 'aria-hidden' not in m.group(1).lower():
                    issues.append({'page': rel, 'type': 'body_icon_not_aria_hidden'})
                    break
        # Editorial pattern gate: if a pattern block is used, its CSS must be inlined.
        # Standalone-token match (lookbehind/lookahead exclude prefixed classes like wg-17-ba).
        if re.search(r'class=["\'][^"\']*(?<![\w-])(?:chron-list|source-preserve|core-insight|conn-grid|impact-grid|ba|ba-col|ba-arrow|ba-label|a11y-check|a11y-grid)(?![\w-])', text):
            if not re.search(r'\.(?:chron-list|source-preserve|core-insight|conn-grid|impact-grid|a11y-check)\b', style):
                issues.append({'page': rel, 'type': 'editorial_patterns_css_not_inlined'})
        # body_only = markup with inline <style> stripped — scan <img> here so example markup inside CSS
        # comments (e.g. an <img class="…-img" src="…"> usage example) can't false-fire the img gates.
        body_only = re.sub(r'<style\b[^>]*>.*?</style>', '', text, flags=re.I | re.S)
        # Soft-shape gate (8817): when shape figures are used, enforce CSS inlined + non-empty alt + namespace.
        # SVG existence / 8000x6000 / figcaption are covered by broken_local_ref + the visual-figure gate below.
        if re.search(r'class=["\'][^"\']*\bshape-(?:figure|img|lead|grid)\b', body_only):
            if not re.search(r'\.shape-(?:figure|img)\b', style):
                issues.append({'page': rel, 'type': 'shape_visuals_css_not_inlined'})
            for im in re.finditer(r'<img\b[^>]*\bclass=["\'][^"\']*\bshape-img\b[^"\']*["\'][^>]*>', body_only, re.I):
                am = re.search(r'\balt\s*=\s*("[^"]*"|\'[^\']*\')', im.group(0), re.I)
                if not am or not am.group(1).strip('\'"').strip():
                    issues.append({'page': rel, 'type': 'shape_img_missing_alt',
                                   'detail': '도형 img는 시각 앵커이므로 빈 alt 금지(핵심 정보는 HTML 텍스트로 두되 alt는 도형 의미를 적는다).'})
                    break
            leaks = sorted({m.group(0) for m in re.finditer(r'\.shape-[A-Za-z0-9_-]+', style)
                            if not re.match(r'\.shape-(?:figure|img|lead|grid|lead-body)(?![\w-])', m.group(0))})
            if leaks:
                issues.append({'page': rel, 'type': 'shape_selector_namespace_leak', 'detail': leaks})
        # Soft workflow map gate (vt-21): if .wf-board markup is used, lock accessibility + no raster + mobile collapse.
        if re.search(r'class=["\'][^"\']*\bwf-board\b', text):
            if '.wf-board' not in style:
                issues.append({'page': rel, 'type': 'soft_workflow_css_not_inlined'})
            fm = re.search(r'<\w+\b[^>]*\bclass=["\'][^"\']*\bwf-board\b[^"\']*["\'][^>]*>', text, re.I)
            # role="img" on the text-bearing frame prunes card/metric text from assistive tech → forbid.
            if fm and re.search(r'role\s*=\s*["\']img["\']', fm.group(0), re.I):
                issues.append({'page': rel, 'type': 'soft_workflow_role_img_buries_text',
                               'detail': 'wf-board(실제 텍스트 포함)에 role="img" → 스크린리더가 카드/지표 텍스트를 prune. role 제거, 장식 요소만 aria-hidden.'})
            for deco in ('wf-codewin', 'wf-dash', 'wf-pipes', 'wf-bottom'):
                dm = re.search(r'<\w+\b[^>]*\bclass=["\'][^"\']*\b' + deco + r'\b[^"\']*["\'][^>]*>', text, re.I)
                if dm and 'aria-hidden' not in dm.group(0).lower():
                    issues.append({'page': rel, 'type': 'soft_workflow_deco_not_aria_hidden', 'el': deco})
                    break
            wf_area = text[fm.start():fm.start() + 3500] if fm else ''
            if re.search(r'<img\b[^>]*\.(?:png|jpe?g|webp|gif)\b', wf_area, re.I):
                issues.append({'page': rel, 'type': 'soft_workflow_raster_image',
                               'detail': 'soft workflow map은 순수 HTML+CSS(SVG-first·자기완결). 내부 raster <img> 금지.'})
            if '.wf-map{grid-template-columns:1fr}' not in style.replace(' ', '').replace('\n', ''):
                issues.append({'page': rel, 'type': 'soft_workflow_map_no_mobile_collapse',
                               'detail': '모바일에서 .wf-map이 1컬럼으로 접히지 않음. @media max-width에 .wf-map{grid-template-columns:1fr} 필요.'})
        # Soft workflow SVG gate (8819): when workflow 도판 figures are used, enforce CSS inlined + non-empty alt
        # + namespace + 8000x6000 resolution. Uses figure.workflow-figure (NOT visual-figure) so figcaption은 권장(강제 아님).
        # img는 body_only에서 스캔(CSS 주석 속 예시 <img> 오발동 차단).
        if re.search(r'class=["\'][^"\']*\bworkflow-(?:figure|img|lead|grid)\b', body_only):
            if not re.search(r'\.workflow-(?:figure|img)\b', style):
                issues.append({'page': rel, 'type': 'workflow_visuals_css_not_inlined'})
            alt_bad = False
            for im in re.finditer(r'<img\b[^>]*\bclass=["\'][^"\']*\bworkflow-img\b[^"\']*["\'][^>]*>', body_only, re.I):
                tag = im.group(0)
                am = re.search(r'\balt\s*=\s*("[^"]*"|\'[^\']*\')', tag, re.I)
                if not alt_bad and (not am or not am.group(1).strip('\'"').strip()):
                    issues.append({'page': rel, 'type': 'workflow_img_missing_alt',
                                   'detail': '워크플로우 도판 img는 시각 대표물이라 빈 alt 금지(핵심 정보는 HTML 텍스트·figcaption으로, alt는 도판 의미를 적는다).'})
                    alt_bad = True
                sm = re.search(r'\bsrc\s*=\s*("[^"]*"|\'[^\']*\')', tag, re.I)
                src = sm.group(1).strip('\'"') if sm else ''
                p = local_path(html, src)
                if p is not None and p.suffix.lower() == '.svg' and p.exists():
                    size = svg_size(p)
                    if not size or size[0] < 8000 or size[1] < 6000:
                        issues.append({'page': rel, 'type': 'workflow_svg_too_small_or_invalid', 'src': src, 'size': size})
                        break
            leaks = sorted({m.group(0) for m in re.finditer(r'\.workflow-[A-Za-z0-9_-]+', style)
                            if not re.match(r'\.workflow-(?:figure|img|grid|lead|lead-body)(?![\w-])', m.group(0))})
            if leaks:
                issues.append({'page': rel, 'type': 'workflow_selector_namespace_leak', 'detail': leaks})
        # --- Regression gates (lock in fixes so the same defects can't recur) ---
        # R1: platform-grid is a card grid (div) — must hold .platform-card directly,
        #     NOT be misused as a section wrapper (heading/intro/card-grid inside → broken grid).
        for m in re.finditer(r'class=["\'][^"\']*\bplatform-grid\b[^"\']*["\']', text):
            after = text[m.end():m.end() + 500]
            if re.search(r'^\s*>?\s*<h2\b', after) or re.search(r'<h2\b', after[:220]) or 'card-grid' in after[:500] or 'h2-sub' in after[:300]:
                issues.append({'page': rel, 'type': 'platform_grid_wrapper_misuse',
                               'detail': 'platform-grid(div)에 카드 직접 대신 heading/intro/card-grid 래핑 → grid 깨짐. 래퍼는 <section>으로, .platform-grid는 카드 직접 자식만.'})
                break
        # R2/R3 gate on wg-03 MARKUP usage (class="wg-03-…"), not on the inlined CSS text
        # (widgets.css inlined by widget/auto profiles contains .wg-03-… selectors even when unused).
        if re.search(r'class=["\'][^"\']*\bwg-03-(?:code|diff|row|grid)\b', text):
            # R2: wg-03 diff code must reset the generic code{} (light bg) or code goes invisible on the dark diff.
            if '.wg-03-diff code' not in style and not re.search(r'\.wg-03-code\{[^}]*background\s*:\s*none', style):
                issues.append({'page': rel, 'type': 'wg03_diff_code_bg_not_reset',
                               'detail': '다크 diff 코드가 코어 code{background} 에 덮여 안 보임. .wg-03-diff code{background:none} 리셋 필요.'})
            # R3: wg-03 diff/notes columns must be equal height (stretch), not start (gap).
            gm = re.search(r'\.wg-03-grid\{[^}]*\}', style)
            if gm and 'align-items:stretch' not in gm.group(0).replace(' ', ''):
                issues.append({'page': rel, 'type': 'wg03_grid_not_stretch',
                               'detail': 'diff(좌)/notes(우) 높이 불일치(틈). .wg-03-grid{align-items:stretch} 필요.'})
        # R4: tables (min-width:420px) must be mobile-safe (wrapped in .table-scroll or a responsive table).
        for m in re.finditer(r'<table\b[^>]*>', text):
            pre = text[max(0, m.start() - 120):m.start()]
            cls = m.group(0)
            if 'table-scroll' not in pre and 'final-matrix' not in cls and 'mobile-card' not in cls:
                issues.append({'page': rel, 'type': 'table_no_mobile_safe_wrapper',
                               'detail': 'table{min-width:420px}이라 390px에서 넘침. .table-scroll로 감싸거나 반응형 표(mobile-card/final-matrix) 사용.'})
                break
        # R5: wide-report layouts must carry the prose width override (else body prose is capped at ~2/3).
        wide = re.search(r'class=["\'][^"\']*\blayout-(expert|github|youtube|manual|compare|seo|platform|landing|case|checklist|reference|audit|skill-audit)\b', text)
        if wide and '.page-wide>section>p' in style:
            if 'max-width:60rem' not in style.replace(' ', ''):
                issues.append({'page': rel, 'type': 'wide_layout_prose_cap_missing',
                               'detail': '넓은 레이아웃 본문이 46rem(섹션 2/3)로 좁음. .page-wide.layout-*>section>p{max-width:60rem} 오버라이드 필요.'})
        for tag, ref in parser.local_refs:
            p = local_path(html, ref)
            if p is not None and not p.exists():
                issues.append({'page': rel, 'type': 'broken_local_ref', 'tag': tag, 'ref': ref})
        for fig in parser.figures:
            cls = fig.get('class','')
            if 'visual-figure' in cls or 'figure-wide' in cls:
                img = fig.get('img')
                if not img:
                    issues.append({'page': rel, 'type': 'visual_figure_missing_img'})
                    continue
                for attr in ('src','alt','width','height'):
                    if not img.get(attr):
                        issues.append({'page': rel, 'type': 'visual_img_missing_attr', 'attr': attr, 'src': img.get('src')})
                if not fig.get('figcaption'):
                    issues.append({'page': rel, 'type': 'visual_figure_missing_figcaption', 'src': img.get('src')})
                src = img.get('src','')
                p = local_path(html, src)
                if p and p.suffix.lower() == '.svg' and p.exists():
                    size = svg_size(p)
                    if not size or size[0] < 8000 or size[1] < 6000:
                        issues.append({'page': rel, 'type': 'svg_too_small_or_invalid', 'src': src, 'size': size})
    if skill_dir:
        skill_manifest = skill_dir/'manifest.json'
        output_manifest = root/'sources/adaptive-html-final-manifest.json'
        if skill_manifest.exists() and output_manifest.exists():
            try:
                sm = json.loads(skill_manifest.read_text())
                om = json.loads(output_manifest.read_text())
                sv, ov = sm.get('version'), om.get('version')
                if sv != ov:
                    issues.append({'type': 'source_version_mismatch', 'skill_version': sv, 'output_source_version': ov})
                elif json.dumps(sm, sort_keys=True) != json.dumps(om, sort_keys=True):
                    issues.append({'type': 'source_manifest_content_mismatch',
                                   'note': '버전은 같으나 source manifest 내용이 현재 manifest.json과 다름(예: theme_system 누락 / 구버전 dark_theme 잔존).'})
            except Exception as e:
                issues.append({'type': 'manifest_parse_error', 'detail': str(e)})
        elif skill_manifest.exists():
            warnings.append({'type': 'missing_output_source_manifest'})
        css_integrity = root/'sources/css-integrity.json'
        if expected_css_hash and expected_asset_hashes:
            if not css_integrity.exists():
                issues.append({'type': 'missing_css_integrity_manifest'})
            else:
                try:
                    data = json.loads(css_integrity.read_text(encoding='utf-8'))
                    if data.get('core_css_sha256') != expected_css_hash:
                        issues.append({'type': 'css_integrity_core_hash_mismatch', 'expected': expected_css_hash, 'actual': data.get('core_css_sha256')})
                    if data.get('asset_order') != asset_order:
                        issues.append({'type': 'css_integrity_asset_order_mismatch', 'expected': asset_order, 'actual': data.get('asset_order')})
                    # Core-5 recorded hashes are the canonical contract — must match exactly.
                    for name, digest in expected_asset_hashes.items():
                        if data.get('asset_sha256', {}).get(name) != digest:
                            issues.append({'type': 'css_integrity_asset_hash_mismatch', 'asset': name})
                    # Any OTHER recorded asset hash (conditional: widgets/visual-html/theme-dark/...) must
                    # also match the current skill — a stale recorded hash means a stale embedded asset.
                    if all_skill_css_hashes:
                        for name, recorded in (data.get('asset_sha256') or {}).items():
                            if name in expected_asset_hashes:
                                continue
                            if name in all_skill_css_hashes and recorded != all_skill_css_hashes[name]:
                                issues.append({'type': 'css_integrity_conditional_hash_mismatch', 'asset': name})
                    # Core-5 snapshot files are mandatory and must match.
                    for name in asset_order:
                        snap = root/'sources/assets'/name
                        if not snap.exists():
                            issues.append({'type': 'missing_output_css_snapshot', 'asset': name})
                        else:
                            snap_hash = hashlib.sha256(snap.read_text(encoding='utf-8').encode('utf-8')).hexdigest()
                            if snap_hash != expected_asset_hashes[name]:
                                issues.append({'type': 'output_css_snapshot_mismatch', 'asset': name})
                    # Conditional snapshot files are optional, but if present must match the current skill
                    # (catches a stale snapshot like a pre-5.2 #theme-toggle theme-dark.css).
                    if all_skill_css_hashes:
                        for name in conditional_order:
                            snap = root/'sources/assets'/name
                            if snap.exists() and name in all_skill_css_hashes:
                                snap_hash = hashlib.sha256(snap.read_text(encoding='utf-8').encode('utf-8')).hexdigest()
                                if snap_hash != all_skill_css_hashes[name]:
                                    issues.append({'type': 'output_css_snapshot_mismatch', 'asset': name})
                except Exception as e:
                    issues.append({'type': 'css_integrity_parse_error', 'detail': str(e)})
        # Phase 0 merge-protection lints on the skill's own CSS assets.
        for a_issue in skill_asset_lint(skill_dir):
            issues.append(a_issue)
        # Source-doc correctness (duplicate CHANGELOG versions, SKILL↔manifest contradiction).
        for d_issue in skill_doc_consistency_gate(skill_dir):
            issues.append(d_issue)
    return {'root': str(root), 'profile': declared_profile, 'html_count': len(htmls), 'issues': issues, 'warnings': warnings, 'ok': not issues}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('output_dir', type=Path)
    ap.add_argument('--skill-dir', type=Path)
    ap.add_argument('--json', action='store_true')
    ap.add_argument('--profile', default=None, help='widget|diagram|auto (or style alias v5|v6). sources/profile.json 필수, 둘 다 지정 시 일치해야 함')
    ns = ap.parse_args()
    result = validate(ns.output_dir.resolve(), ns.skill_dir.resolve() if ns.skill_dir else None, ns.profile)
    if ns.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"HTML files: {result['html_count']}")
        print('OK' if result['ok'] else 'FAILED')
        for issue in result['issues']:
            print('ISSUE', issue)
        for warning in result['warnings']:
            print('WARN', warning)
    return 0 if result['ok'] else 1

if __name__ == '__main__':
    raise SystemExit(main())
