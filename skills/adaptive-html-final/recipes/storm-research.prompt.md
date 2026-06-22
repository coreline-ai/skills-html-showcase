# recipe: storm_research (다관점 STORM 리서치 리포트)

STORM(Synthesis of Topic Outlines through Retrieval and Multi-perspective questioning) 방법을 단일 HTML 리서치 리포트로 정본화한다. 코어 CSS 무변경(기존 vt-/wg- 재사용) → 코어 해시 `a64604d0` 불변, 버전 5.10.6 유지(additive).

## 언제 쓰나 (triggers)
"STORM 리서치", "다관점 딥리서치", "5영혼으로 조사", "여러 LLM으로 병렬 리서치", "모순 지도 포함 리포트", "출처 강제 리서치", `/storm-research`.

## 4-프롬프트 방법론 (orginal_skill/storm-research/prompts 정본)
1. **multi-perspective-scan** — 연구 질문을 5관점(회의주의자·경제학자·역사학자·학자·미래학자, D-고정)으로 분기해 각 관점의 핵심 질문·예상 발견을 수집. 모든 발견은 `[출처:URL]` 또는 출처원장 행으로 근거화한다(무출처 단언 금지).
2. **contradiction-map** — 관점 간 **합의 지점**과 **모순/긴장/충돌 지점**을 함께 매핑한다. 단일관점 나열은 STORM을 무의미화하므로 금지(`storm_contradiction_gate`).
3. **synthesis** — 모순을 해소하지 않고 보존한 채 종합 기사(synthesis_article)를 쓴다. 신뢰도/근거 라벨(`[사실]`/`[추정]`/`[확인 필요]` 또는 confidence high/medium/low) ≥3·≥2종.
4. **peer-review** — 동료검토 게이트: verdict(통과/조건부/반려) + source-bias-transfer·over-association 점검 흔적을 남긴다(`storm_peer_review_gate`).

## 필수 블록 (13)
generated_row · method_notice · research_question · perspective_router · soul_evidence_cards · source_map · contradiction_map · synthesis_article · peer_review_gate · confidence_badges · unresolved_questions · provenance_footer · next_research_actions.

## 정본 컴포넌트 (신규 CSS 없음 · 코어 해시 불변)
- **레이아웃**: `assets/layouts/storm-research-report.html` — `<main id="main" class="page layout-storm">`. **`page-wide` 금지**(theme.css 60rem 등재=코어 변경 유발). 제네릭 `page` 카드 surface 상속.
- **primary_vt**: `process-swimlane`(vt 마커 `.swim`/`.lane-step`) — 4단계 리서치 파이프라인(scan→contradict→synthesize→peer-review)을 레인으로 1회 이상.
- **vt 후순위**: hero-map, risk-matrix, quality-gate, comparison-cards, checklist-flow, timeline.
- **wg**: wg-13(모순 흐름)·wg-14(관점 발견)·wg-18(미해결 트리아지)·wg-11(검토 상태)·wg-16(후속 액션)·wg-04(출처 시점).
- 표=`.tbl`/`.table-scroll`+caption, 상태칩=`.status-pill`, body-icon은 `assets/body-icons.json` 32종에서만, 8테마 라디오 필수, 코어 CSS byte-verbatim 인라인 + `adaptive-html-final-core-css-sha256` 마커.
- TOC: `toc-map storm-question-toc`(toc-pills + `a.toc-pill>b`), plain-text TOC 금지.

## custom gate 6종 (악성 fixture 선실패 → 정상 통과)
storm_soul_count_gate(≥4 관점) · storm_minimum_sources_gate(출처 ≥5) · storm_citation_label_gate(라벨 ≥3·≥2종) · storm_contradiction_gate(합의+모순) · storm_peer_review_gate(verdict+편향 점검) · storm_provenance_gate(발행처/기준시점/접근일/URL ≥3).

## 산출 시 sources 스냅샷
output 산출물은 `sources/`에 storm-report.json·결과/프롬프트/charter·evidence-map·quality 스냅샷 + profile.json(profile=auto) + css-integrity + render-audit를 남긴다(examples 기준선 예외 제외).
