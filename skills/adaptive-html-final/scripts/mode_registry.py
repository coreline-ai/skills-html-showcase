"""Mode registry loader for adaptive-html-final.

The 17 per-mode JSON files in `modes/NN-<mode>.json` are the single editable
surface for mode definitions.

B-lite (current): the registry is an *authoritative mirror* — it must stay
byte/semantic-equal to the existing canonical sources (`MODE_TEMPLATE_CONTRACTS`,
SKILL §0.6, references/widget-system.md). `validate_output.py` does NOT read this
registry yet; `check_mode_registry_sync.py` only verifies equality.

B-full (later, on demand): `validate_output.py` will set
`MODE_TEMPLATE_CONTRACTS = build_mode_template_contracts(skill_dir)` so the
registry becomes the executable source of truth. The deep-equal in the sync
checker is the no-regression proof that makes that swap safe.
"""
from __future__ import annotations

import json
from pathlib import Path

# Fields every mode JSON must carry (schema contract).
REQUIRED_FIELDS = (
    'id', 'priority', 'label', 'layout_class', 'layout_file', 'recipe',
    'triggers', 'required_blocks', 'layout_placeholders',
    'primary_vt', 'vt_candidates', 'vt_markers',
    'wg_candidates', 'wg_markers',
    'toc_contract', 'quality_contract', 'examples', 'custom_contracts',
)


def load_mode_registry(skill_dir) -> list[dict]:
    """Load all mode JSON files from `<skill_dir>/modes/`, sorted by priority."""
    modes_dir = Path(skill_dir) / 'modes'
    out: list[dict] = []
    for p in sorted(modes_dir.glob('*.json')):
        obj = json.loads(p.read_text(encoding='utf-8'))
        obj['_file'] = p.name
        out.append(obj)
    out.sort(key=lambda o: o.get('priority', 0))
    return out


def get_mode_by_id(registry: list[dict], mode_id: str):
    return next((m for m in registry if m.get('id') == mode_id), None)


def get_mode_by_layout_class(registry: list[dict], layout_class: str):
    return next((m for m in registry if m.get('layout_class') == layout_class), None)


def get_mode_by_priority(registry: list[dict], priority: int):
    return next((m for m in registry if m.get('priority') == priority), None)


def build_mode_template_contracts(skill_dir) -> dict:
    """Reconstruct the exact `MODE_TEMPLATE_CONTRACTS` dict from the registry.

    Shape matches `validate_output.MODE_TEMPLATE_CONTRACTS` exactly so a
    deep-equal comparison proves the registry mirrors the validator's contract
    data (vt markers are regex tokens, wg order preserved).
    """
    contracts: dict = {}
    for m in load_mode_registry(skill_dir):
        contracts[m['layout_class']] = {
            'mode': m['id'],
            'primary_vt': m['primary_vt'],
            'vt_markers': tuple(m['vt_markers']),
            # registry stores the full wg list as wg_candidates; the validator's
            # contract dict calls the same data recommended_wg.
            'recommended_wg': tuple(m['wg_candidates']),
        }
    return contracts
