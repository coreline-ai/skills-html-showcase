> ⚠️ **ARCHIVED — SUPERSEDED by v5.2.0.** 이 문서는 작성 당시 버전의 시점 고정(point-in-time) 리뷰/분석/계획 기록입니다. 현재 스킬은 **v5.2.0**이며, 여기서 지적된 항목 다수는 이미 해소·초과 달성되었습니다. 최신 사실 기준선은 게이트를 완전 통과한 `output/adaptive-html-final-13-topics-20260605_083433/`이고, 현행 문서는 루트 `README.md`·`AGENTS.md`·`Guide.md`입니다. 아카이브 색인: [`docs/archive/README.md`](README.md).

---

# 골든 사전 진단 (Phase 3.5)

신규 게이트(Phase 3: cross_leak/unfilled_placeholder + --profile) + 코어 해시 + 버전으로 v5/v6 골든을 실측. (실측일 기준)

## 확정 표 (골든 × 프로파일)

| 골든 | --profile | 1층 markup (cross_leak) | 2층 CSS 번들 | 3층 코어해시 | 버전 | 종합 |
|---|---|---|---|---|---|---|
| `output/.../showcase-v6` | `auto` | 비적용(skip) | core5 + widgets + visual-html | match `bd5665…` | 4.5.0 = 4.5.0 | **OK (0 issues)** |
| `output/.../showcase-v6` | `diagram` | **0** (wg- markup 0) | widgets.css 잔존(=슬림 아님) | match | match | **OK(markup)** 단 슬림 아님 |
| `output/.../showcase-v5` | `widget` | **0** (vt- markup 0) | widgets only | **mismatch** `541d5e…` ≠ `bd5665…` | **4.3.3 ≠ 4.5.0** | **FAILED (22 issues)** |

v5 실패 내역: `inline_css_hash_mismatch ×16`, `source_version_mismatch ×1`, `css_integrity_core_hash_mismatch ×1`, `css_integrity_asset_hash_mismatch ×2`, `output_css_snapshot_mismatch ×2`.

## 결론 (Phase 5 라벨링 입력 — 단방향)

1. **v6 = `auto` 골든(무변경).** 1층 cross_leak 비적용, 3층 해시·버전 통과. SHA256 회귀-0 기준선.
2. **`diagram` 골든 = 신규 슬림 재생성 필요.** v6는 markup상 vt-만(wg- 0)이라 1층은 통과하지만, widgets.css가 인라인된 **auto 번들**이라 "diagram 슬림"이 아니다. Phase 2 슬림 어셈블러(`/tmp/slim_assembler.py`)로 v6에서 widgets.css만 제거해 별도 산출(콘텐츠 무변경).
3. **v5 = `widget` 골든, 정합화 필요.** 1층 vt- 누수 0(통과)이나 코어해시·버전 드리프트(4.3.3/`541d5e…`)로 FAILED. Phase 5에서 4.6.0 코어로 sources/스냅샷/manifest 리프레시 + widgets.css 인라인 확인(콘텐츠 무변경, `<body>` diff 0).

분기: **라벨링(v6→auto)** vs **재생성(diagram 슬림)** vs **정합화(v5→widget)**.
