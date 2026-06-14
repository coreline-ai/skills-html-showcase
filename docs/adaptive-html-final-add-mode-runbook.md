# adaptive-html-final 신규 모드 추가 Runbook

> 목적: Registry 모듈화(B-full) 이후 신규 모드(18번째~)를 **드리프트 없이** 추가하는 절차다. 모드 결정표 데이터는 `skills/adaptive-html-final/modes/NN-<mode>.json` **단일 출처**이며, `validate_output.py`가 이를 읽는다(`_build_mode_template_contracts_from_registry`). 버전은 요청 시에만 올린다(기본 5.10.3 유지).

## 1. 핵심 원칙

- **결정표 데이터(vt/wg/toc/trigger/priority/label)는 mode JSON 1곳에서만 편집한다.** validator는 JSON을 읽으므로 Python dict를 직접 고치지 않는다.
- **줄일 수 없는 모드별 산출물은 따로 만든다:** layout HTML·recipe·example. 이건 자동화 대상이 아니다.
- **문서 결정표(SKILL §0.6·AGENTS §3·widget-system)는 여전히 손으로 갱신**하되, sync checker가 JSON과 불일치를 강제로 잡는다(생성이 아니라 검증).
- 추가 후 `check_mode_registry_sync.py` + 4대 검증이 OK여야 완료다.

## 2. 추가 절차 (10단계 이하)

1. **mode JSON 작성**: `modes/NN-<kebab-mode>.json` (NN=priority, kebab=mode id에서 `_html` 제거·`-`치환). 18번째면 `18-<name>.json`.
   - 필수 필드(18): `id, priority, label, layout_class, layout_file, recipe, triggers, required_blocks, layout_placeholders, primary_vt, vt_candidates, vt_markers, wg_candidates, wg_markers, toc_contract, quality_contract, examples, custom_contracts`.
   - `vt_markers`는 vt 템플릿 내부 **마커 정규식 토큰**(예: `\\bhm-grid\\b`), vt 이름이 아님.
   - `wg_markers`는 `wg_candidates` 각 항목 + `-`(예: `wg-02` → `wg-02-`).
   - `toc_contract.rule` = 분석성 모드면 `"always"`+`required_class`, 아니면 `"structural_h2_gte_4"`+`required_class:null`.
   - `quality_contract`는 현행 게이트가 강제하는 값만(`mode_depth_min_avg` 등). 발명 금지.
2. **layout 추가**: `assets/layouts/<layout_file>` + `layouts.css`에 `.layout-<name>` 표면 규칙. `layout_placeholders`는 이 파일의 실제 `{{대문자}}`와 일치해야 한다.
3. **recipe 추가**: `recipes/<recipe>.prompt.md` (파일명은 JSON `recipe`와 일치).
4. **문서 결정표 갱신**: `SKILL.md §0.6`·`AGENTS.md §3`·`references/widget-system.md` mode→wg 표에 새 행 추가(값은 JSON과 동일하게).
5. **manifest.modes 갱신**: `{ "id": ..., "layout": "<layout_file>" }` 추가(id+layout 최소 메타).
6. **(필요 시) custom gate**: 특수 의미 검증이 필요하면 `validate_output.py`에 함수 추가 + JSON `custom_contracts`에 함수명 선언(allowlisted dispatch).
7. **(필요 시) toc 필수 class**: 분석성 모드면 `analysis_toc_map_required_gate`의 `analysis_required`에 `layout-<name>: ('<toc-class>', '<issue-type>')` 추가 + JSON `toc_contract.required_class` 동일.
8. **example 작성**: `examples/NN_<name>_*.html` + `examples/index.html` 갤러리 카드. JSON `examples[].file`을 실제 파일로.
9. **sync 확인**: `python3 skills/adaptive-html-final/scripts/check_mode_registry_sync.py --skill-dir skills/adaptive-html-final` → OK.
10. **전체 검증 + 재패키징**: 아래 §4. 통과 후 `.skill` 재패키징(byte-match).

## 3. 무엇이 "불완전 추가"를 잡는가 (안전 매트릭스)

| 실수 | 잡는 게이트 |
|---|---|
| priority 중복/누락 | sync `registry_priority_not_contiguous` |
| 필수 필드 누락 | sync `registry_missing_field` |
| `primary_vt`/`wg`가 SKILL §0.6·widget과 불일치 | sync `decision_table_vs_registry`(decision_table_consistency_gate) |
| AGENTS §3 결정표 누락/불일치 | sync `agents_*_mismatch` / `agents_mode_set_mismatch` |
| manifest.modes 누락/불일치 | sync `manifest_modes_id_mismatch` / `manifest_layout_mismatch` |
| layout/recipe/example 파일 없음 | sync `registry_*_missing` |
| `vt_candidates[0]≠primary_vt`, `wg_markers` 파생 오류 | sync `vt_candidates_primary_mismatch` / `wg_markers_derivation_mismatch` |
| toc `required_class`가 게이트 매핑과 불일치 | sync `toc_required_class_mismatch` |
| **vt_marker가 실제 vt HTML과 안 맞음** | **`validate_output` (examples)** — `mode_primary_vt_missing`(예제 렌더에서 마커 미검출) |
| validator가 registry를 안 읽게 되돌림 | governance `validator ... sourced from the registry (build == live)` |

> 요지: 결정표 데이터 드리프트는 **sync checker**, vt 마커의 실제 적합성은 **examples validate**, 소스 배선은 **governance**가 강제한다. 한 곳이라도 빠지면 완료가 막힌다.

## 4. 필수 검증 명령 (repo 루트)

```bash
python3 skills/adaptive-html-final/scripts/check_mode_registry_sync.py --skill-dir skills/adaptive-html-final
python3 skills/adaptive-html-final/scripts/validate_output.py skills/adaptive-html-final/examples --skill-dir skills/adaptive-html-final
python3 skills/adaptive-html-final/scripts/quality_contract_check.py skills/adaptive-html-final/examples
python3 skills/adaptive-html-final/tests/test_governance_gates.py
python3 skills/adaptive-html-final/scripts/completion_check.py skills/adaptive-html-final/examples
# 모드 수가 늘면 governance count 동기화: manifest.quality.governance_count + README 표면
# 마지막: .skill 재패키징(zip 내부가 워킹트리와 byte-match)
```

## 5. 버전 정책

- 신규 모드 추가는 기능 변경이므로 릴리스 단위 bump 후보다. 단 **사용자 명시 승인 전까지 `5.10.3` 유지**, 변경은 `CHANGELOG.md ## Unreleased`에 기록한다([version-release-guide](adaptive-html-final-version-release-guide.md)).
