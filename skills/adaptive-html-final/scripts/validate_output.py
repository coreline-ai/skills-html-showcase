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
    """Profile resolution priority: --profile arg (1st) -> sources/profile.json (2nd) -> None (fallback).

    Accepts canonical names or style aliases (v5/v6). Invalid/out-of-range tokens append an
    'invalid_profile' issue and resolve to None (no silent auto fallback). Returns one of
    VALID_PROFILES or None.
    """
    if profile_arg:
        p = str(profile_arg).strip().lower()
        p = _STYLE_ALIAS.get(p, p)
        if p in VALID_PROFILES:
            return p
        issues.append({'type': 'invalid_profile', 'source': '--profile', 'value': str(profile_arg)})
        return None
    pj = root / 'sources' / 'profile.json'
    if pj.exists():
        try:
            v = json.loads(pj.read_text(encoding='utf-8')).get('profile')
            v = _STYLE_ALIAS.get(str(v).strip().lower(), str(v).strip().lower()) if v is not None else None
            if v in VALID_PROFILES:
                return v
            issues.append({'type': 'invalid_profile', 'source': 'sources/profile.json', 'value': v})
        except Exception as e:
            issues.append({'type': 'profile_json_parse_error', 'detail': str(e)})
    return None


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


def validate(root: Path, skill_dir: Path | None = None, profile: str | None = None) -> dict:
    issues = []
    warnings = []
    declared_profile = _resolve_profile(profile, root, issues)
    expected_css_hash = None
    expected_asset_hashes = None
    asset_order = ['theme.css', 'components.css', 'visual-components.css', 'layouts.css', 'print.css']
    if skill_dir:
        asset_paths = [skill_dir/'assets'/name for name in asset_order]
        if all(p.exists() for p in asset_paths):
            asset_texts = {name: (skill_dir/'assets'/name).read_text(encoding='utf-8') for name in asset_order}
            core_css = '\n'.join(asset_texts[name] for name in asset_order)
            expected_css_hash = hashlib.sha256(core_css.encode('utf-8')).hexdigest()
            expected_asset_hashes = {name: hashlib.sha256(asset_texts[name].encode('utf-8')).hexdigest() for name in asset_order}
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
                sv = json.loads(skill_manifest.read_text()).get('version')
                ov = json.loads(output_manifest.read_text()).get('version')
                if sv != ov:
                    issues.append({'type': 'source_version_mismatch', 'skill_version': sv, 'output_source_version': ov})
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
                    for name, digest in expected_asset_hashes.items():
                        if data.get('asset_sha256', {}).get(name) != digest:
                            issues.append({'type': 'css_integrity_asset_hash_mismatch', 'asset': name})
                    for name in asset_order:
                        snap = root/'sources/assets'/name
                        if not snap.exists():
                            issues.append({'type': 'missing_output_css_snapshot', 'asset': name})
                        else:
                            snap_hash = hashlib.sha256(snap.read_text(encoding='utf-8').encode('utf-8')).hexdigest()
                            if snap_hash != expected_asset_hashes[name]:
                                issues.append({'type': 'output_css_snapshot_mismatch', 'asset': name})
                except Exception as e:
                    issues.append({'type': 'css_integrity_parse_error', 'detail': str(e)})
    return {'root': str(root), 'profile': declared_profile, 'html_count': len(htmls), 'issues': issues, 'warnings': warnings, 'ok': not issues}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('output_dir', type=Path)
    ap.add_argument('--skill-dir', type=Path)
    ap.add_argument('--json', action='store_true')
    ap.add_argument('--profile', default=None, help='widget|diagram|auto (or style alias v5|v6). 미지정 시 sources/profile.json → 폴백(교차 게이트 미적용)')
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
