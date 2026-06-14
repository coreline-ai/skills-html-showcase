"""B-lite sync checker for the mode registry (authoritative mirror).

Verifies that `modes/NN-<mode>.json` stays consistent with the existing canonical
sources WITHOUT modifying the validator:

  1. invariants            : count == 17, priority 1..N contiguous, ids unique
  2. DEEP-EQUAL (core)     : build_mode_template_contracts(registry) == validate_output.MODE_TEMPLATE_CONTRACTS
  3. doc agreement         : registry agrees with SKILL §0.6 + widget-system.md
                             (reuses validate_output.decision_table_consistency_gate)
  4. manifest.modes        : same id set + same layout file basename
  5. referenced files      : layout_file / recipe / examples exist
  6. toc required_class     : matches analysis_toc_map_required_gate's mapping (parsed from source)

Exit 0 when fully in sync; exit 1 with an issue list otherwise.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import validate_output as v          # noqa: E402
import mode_registry as reg          # noqa: E402


def _skill_vt_candidates(skill_md: str) -> dict:
    """Parse SKILL.md §0.6 vt column into mode -> ordered [vt names]."""
    m = re.search(
        r'## 0\.6[\s\S]*?\| Mode \| Layout \| vt-템플릿[^\n]*\|\n\|[-| ]+\|\n(?P<body>[\s\S]*?)(?:\n\n|vt-템플릿 파일명)',
        skill_md)
    if not m:
        return {}
    out = {}
    for line in m.group('body').splitlines():
        if not line.startswith('|') or line.startswith('|---'):
            continue
        cells = [c.strip() for c in line.strip('|').split('|')]
        if len(cells) < 4:
            continue
        out[cells[0]] = list(v._split_decision_cell(cells[2]))
    return out


def _agents_mode_table(agents_md: str) -> dict:
    """Parse AGENTS.md §3 routing table into mode -> {layout_class, layout_file,
    primary_vt, wg}. Direct parse (no marker block needed) — closes the AGENTS
    decision-table drift gap that the §0.6/widget gates don't cover."""
    out = {}
    for line in agents_md.splitlines():
        if not line.startswith('| `'):
            continue
        cells = [c.strip() for c in line.strip('|').split('|')]
        if len(cells) < 6:
            continue
        mode = cells[0].strip('` ')
        lc = cells[2].strip('`. ')
        lf = cells[3].strip('` ')
        vt_cell = cells[4]
        bold = re.search(r'\*\*([a-z][a-z-]+)\*\*', vt_cell)  # primary vt is bolded
        vt_first = bold.group(1) if bold else re.split(r'→', vt_cell)[0].strip(' *`')
        wg = tuple(re.findall(r'wg-\d{2}', cells[5]))
        out[mode] = {'layout_class': lc, 'layout_file': lf, 'primary_vt': vt_first, 'wg': wg}
    return out


def _gate_toc_required_map(skill_dir: Path) -> dict:
    """Parse the `analysis_required = { 'layout-x': ('class', 'issue'), ... }` block
    from validate_output.py so the expected toc class is sourced from the gate, not
    hardcoded here."""
    src = (skill_dir / 'scripts' / 'validate_output.py').read_text(encoding='utf-8')
    block = re.search(r'analysis_required\s*=\s*\{(?P<body>[\s\S]*?)\}', src)
    if not block:
        return {}
    return dict(re.findall(r"'(layout-[a-z-]+)':\s*\('([a-z-]+)'", block.group('body')))


def check(skill_dir) -> list[dict]:
    skill_dir = Path(skill_dir).resolve()
    issues: list[dict] = []
    registry = reg.load_mode_registry(skill_dir)

    # --- 1. invariants ---
    n = len(registry)
    if n != len(v.MODE_TEMPLATE_CONTRACTS):
        issues.append({'type': 'registry_count_mismatch',
                       'registry': n, 'contracts': len(v.MODE_TEMPLATE_CONTRACTS)})
    pris = sorted(m.get('priority') for m in registry)
    if pris != list(range(1, n + 1)):
        issues.append({'type': 'registry_priority_not_contiguous', 'priorities': pris})
    ids = [m.get('id') for m in registry]
    if len(set(ids)) != len(ids):
        issues.append({'type': 'registry_duplicate_id', 'ids': ids})
    for m in registry:
        missing = [f for f in reg.REQUIRED_FIELDS if f not in m]
        if missing:
            issues.append({'type': 'registry_missing_field', 'id': m.get('id'), 'missing': missing})
    # Downstream sections assume every required field exists; if any is missing the
    # registry is structurally invalid, so report and stop before field-access crashes.
    if any(it['type'] == 'registry_missing_field' for it in issues):
        return issues

    # --- 2. DEEP-EQUAL against the validator's contract dict (the no-regression proof) ---
    built = reg.build_mode_template_contracts(skill_dir)
    if built != v.MODE_TEMPLATE_CONTRACTS:
        for k in sorted(set(built) | set(v.MODE_TEMPLATE_CONTRACTS)):
            if built.get(k) != v.MODE_TEMPLATE_CONTRACTS.get(k):
                issues.append({'type': 'registry_contract_mismatch', 'layout_class': k,
                               'registry': built.get(k), 'validator': v.MODE_TEMPLATE_CONTRACTS.get(k)})

    # --- 3. registry agrees with SKILL §0.6 + widget-system.md (reuse existing gate) ---
    skill_md = (skill_dir / 'SKILL.md').read_text(encoding='utf-8')
    widget_md = (skill_dir / 'references' / 'widget-system.md').read_text(encoding='utf-8')
    for it in v.decision_table_consistency_gate(skill_md, widget_md, built):
        it = dict(it)
        it['source'] = 'decision_table_vs_registry'
        issues.append(it)

    # --- 3b. registry internal consistency (candidate lists vs primary/markers) ---
    for m in registry:
        vc = m.get('vt_candidates') or []
        if not vc or vc[0] != m.get('primary_vt'):
            issues.append({'type': 'vt_candidates_primary_mismatch', 'id': m['id'],
                           'primary_vt': m.get('primary_vt'), 'vt_candidates_head': vc[:1]})
        expect_wgm = [w + '-' for w in (m.get('wg_candidates') or [])]
        if list(m.get('wg_markers') or []) != expect_wgm:
            issues.append({'type': 'wg_markers_derivation_mismatch', 'id': m['id'],
                           'wg_markers': m.get('wg_markers'), 'expected': expect_wgm})

    # --- 3c. vt_candidates (full ordered list) == SKILL §0.6 vt column ---
    skill_vt = _skill_vt_candidates(skill_md)
    for m in registry:
        want = skill_vt.get(m['id'])
        if want is not None and list(m.get('vt_candidates') or []) != want:
            issues.append({'type': 'vt_candidates_vs_skill_mismatch', 'id': m['id'],
                           'registry': m.get('vt_candidates'), 'skill_0_6': want})

    # --- 3d. AGENTS.md §3 routing table <-> registry (direct parse, closes AGENTS gap) ---
    agents_path = skill_dir.parent.parent / 'AGENTS.md'
    if agents_path.exists():
        agents = _agents_mode_table(agents_path.read_text(encoding='utf-8'))
        by_id = {m['id']: m for m in registry}
        if set(agents) != set(by_id):
            issues.append({'type': 'agents_mode_set_mismatch',
                           'only_agents': sorted(set(agents) - set(by_id)),
                           'only_registry': sorted(set(by_id) - set(agents))})
        for mid, a in agents.items():
            m = by_id.get(mid)
            if not m:
                continue
            if a['layout_class'] != m['layout_class']:
                issues.append({'type': 'agents_layout_class_mismatch', 'id': mid,
                               'agents': a['layout_class'], 'registry': m['layout_class']})
            if a['layout_file'] != Path(m['layout_file']).name:
                issues.append({'type': 'agents_layout_file_mismatch', 'id': mid,
                               'agents': a['layout_file'], 'registry': Path(m['layout_file']).name})
            if a['primary_vt'] != m['primary_vt']:
                issues.append({'type': 'agents_primary_vt_mismatch', 'id': mid,
                               'agents': a['primary_vt'], 'registry': m['primary_vt']})
            if a['wg'] != tuple(m.get('wg_candidates') or ()):
                issues.append({'type': 'agents_wg_mismatch', 'id': mid,
                               'agents': a['wg'], 'registry': tuple(m.get('wg_candidates') or ())})

    # --- 4. manifest.modes <-> registry ---
    manifest = json.loads((skill_dir / 'manifest.json').read_text(encoding='utf-8'))
    man = {e['id']: e['layout'] for e in manifest.get('modes', [])}
    reg_layout = {m['id']: Path(m['layout_file']).name for m in registry}
    if set(man) != set(reg_layout):
        issues.append({'type': 'manifest_modes_id_mismatch',
                       'only_manifest': sorted(set(man) - set(reg_layout)),
                       'only_registry': sorted(set(reg_layout) - set(man))})
    for mid in sorted(set(man) & set(reg_layout)):
        if man[mid] != reg_layout[mid]:
            issues.append({'type': 'manifest_layout_mismatch', 'id': mid,
                           'manifest': man[mid], 'registry': reg_layout[mid]})

    # --- 5. referenced files exist ---
    for m in registry:
        if not (skill_dir / m['layout_file']).exists():
            issues.append({'type': 'registry_layout_file_missing', 'id': m['id'], 'file': m['layout_file']})
        if not (skill_dir / m['recipe']).exists():
            issues.append({'type': 'registry_recipe_missing', 'id': m['id'], 'file': m['recipe']})
        for ex in m.get('examples', []):
            if ex.get('file') and not (skill_dir / ex['file']).exists():
                issues.append({'type': 'registry_example_missing', 'id': m['id'], 'file': ex['file']})

    # --- 6. toc_contract.required_class matches the gate's analysis_required mapping ---
    gate_map = _gate_toc_required_map(skill_dir)
    for m in registry:
        lc = m['layout_class']
        rc = (m.get('toc_contract') or {}).get('required_class')
        rule = (m.get('toc_contract') or {}).get('rule')
        if lc in gate_map:
            if rc != gate_map[lc]:
                issues.append({'type': 'toc_required_class_mismatch', 'id': m['id'],
                               'registry': rc, 'gate': gate_map[lc]})
            if rule != 'always':
                issues.append({'type': 'toc_rule_should_be_always', 'id': m['id'], 'rule': rule})
        elif rc is not None:
            issues.append({'type': 'toc_required_class_unexpected', 'id': m['id'], 'registry': rc})

    return issues


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--skill-dir', default='.')
    args = ap.parse_args()
    issues = check(args.skill_dir)
    if issues:
        print('FAILED — mode registry sync issues (%d):' % len(issues))
        for it in issues:
            print('  ', it)
        sys.exit(1)
    print('OK — mode registry in sync (deep-equal + §0.6/widget + manifest + files + toc).')
    sys.exit(0)


if __name__ == '__main__':
    main()
