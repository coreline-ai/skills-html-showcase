# 📦 docs/archive — 시점 고정 기록 보관소

이 폴더는 `adaptive-html-final` 스킬이 **v5.2.0**에 도달하기까지의 리뷰·분석·병합·구현 계획 문서를 보관합니다.
모두 **작성 당시 버전의 시점 고정(point-in-time) 기록**이며, 여기서 제기된 지적·계획 항목은 대부분 이미 해소·초과 달성되었습니다.

> **현행 기준선 (Single Source of Truth)**
> - 스킬 본체: [`skills/adaptive-html-final/SKILL.md`](../../skills/adaptive-html-final/SKILL.md) (v5.2.0)
> - 결정론 진입점: [`AGENTS.md`](../../AGENTS.md)
> - 사용 가이드: [`Guide.md`](../../Guide.md)
> - 변경 이력: [`skills/adaptive-html-final/CHANGELOG.md`](../../skills/adaptive-html-final/CHANGELOG.md)
> - **게이트 완전 통과 캐노니컬 산출물**: `output/2026-06-05/adaptive-html-final-13-topics-20260605_083433/`
>   (현재 스킬 v5.2.0의 정적 품질 게이트 `validate_output.py`를 0 issue로 통과 — 빌드 완성도 검증 기준선)

## 보관 문서

| 문서 | 시점 버전 | 작성일 | 성격 | v5.2.0 기준 상태 |
|---|---|---|---|---|
| [`DESIGN_REVIEW_adaptive-html-final-v4.md`](DESIGN_REVIEW_adaptive-html-final-v4.md) | v4 | 2026-05-31 | 7-페르소나 디자인 품질 리뷰 (실측 렌더 26종) | 지적 사항 반영 완료 |
| [`REVIEW_adaptive-html-final-v4.3.3.md`](REVIEW_adaptive-html-final-v4.3.3.md) | v4.3.3 | 2026-05-31 | 6-전문가 병렬 리뷰 + 적대적 검증 | 반영 완료 |
| [`ANALYSIS_adaptive-html-final.md`](ANALYSIS_adaptive-html-final.md) | v4.5.0 | 2026-06-05 | 7-영역 정밀 분석 보고서 (v4.0.0 보고서 대체) | 이슈 19건 패치 완료 |
| [`MERGE_STRATEGY_final-20260604.md`](MERGE_STRATEGY_final-20260604.md) | v4.5.0→v5.0.0 | 2026-06-05 | final_20260604 섹션 병합 전략 (4-패널 평결) | 병합 완료 |
| [`implement_visual_profile_separation.md`](implement_visual_profile_separation.md) | v4.3.3→v4.6.0 | 2026-05-31 | 비주얼 프로파일(widget/diagram/auto) 분리 구현 계획 | 프로파일 5.x 출시 완료 |
| [`golden_prediagnosis.md`](golden_prediagnosis.md) | — | 골든 사전진단 (Phase 3.5) | 프로파일 게이트 검증 완료 |

## 왜 보관(archive)인가

이 문서들은 특정 버전을 대상으로 한 **리뷰/계획 산출물**입니다. "v5.2.0으로 갱신"하는 것은 의미가 없고(시점이 박제된 기록), 그렇다고 삭제하면 **품질 개선 의사결정의 근거 추적성**이 사라집니다. 따라서 루트를 현행 문서(README·AGENTS·Guide)만 남기도록 비우고, 과거 기록은 이 폴더에 시점 배지와 함께 보존합니다. git 이력에도 이동 내역이 남습니다.
