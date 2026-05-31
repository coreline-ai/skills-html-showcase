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


def validate(root: Path, skill_dir: Path | None = None) -> dict:
    issues = []
    warnings = []
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
    return {'root': str(root), 'html_count': len(htmls), 'issues': issues, 'warnings': warnings, 'ok': not issues}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('output_dir', type=Path)
    ap.add_argument('--skill-dir', type=Path)
    ap.add_argument('--json', action='store_true')
    ns = ap.parse_args()
    result = validate(ns.output_dir.resolve(), ns.skill_dir.resolve() if ns.skill_dir else None)
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
