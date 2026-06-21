# orginal_skill 신규 모드 진입 추출 리포트 — 2026-06-21

작성 일시: `2026-06-21 KST`

이 문서는 `orginal_skill/`에 들어온 원본 스킬들을 `adaptive-html-final`의 신규 모드로 통합할 수 있는지 병렬 분석한 결과를 **모드 진입 스펙**으로 고정한다. 즉, 단순 감상평이 아니라 `modes/NN-*.json`에 들어갈 수 있는 필드, required block, layout/vt/wg 후보, custom gate, source snapshot 계약까지 추출한다.

> 현행 기준(2026-06-21 갱신): `adaptive-html-final`은 `skills/adaptive-html-final/manifest.json` 기준 **`5.10.6`, 공식 모드 `17개`, governance `176`**(작성 시점 5.10.5/162에서 갱신됨). 사용자 결정으로 business_plan(mode 18)은 **버전 업 없이 5.10.6에 병합**한다. ⚠️ 본 문서 §4.1의 business_plan required_blocks는 12개로 적혀 있으나 정본은 **13개**(스켈레톤 JSON·[implement_20260621_150500.md](../dev-plan/implement_20260621_150500.md) 기준).

---

## 1. 병렬 분석 범위

| 분석 축 | 담당 관점 | 읽은 원천 | 산출 초점 |
|---|---|---|---|
| 사업/운영/트렌드 계열 | bizplan · manual-production · x-ai-trend-collector | `orginal_skill/bizplan/`, `orginal_skill/manual-production/`, `orginal_skill/x-ai-trend-collector/` | 독립 모드 가치, 기존 17모드와 중복, 신규 entry 후보 |
| STORM 리서치 | storm-research | `orginal_skill/storm-research/` 전체 | 5영혼·모순지도·동료검토·출처 스냅샷 계약 |
| `.skill` 아카이브 | zip archive 분석 | `orginal_skill/*.skill` 6개 | 이미 흡수된 13모드와 새로 남는 후보 분리 |
| adaptive-html-final 계약 | 현재 스킬 정본 | `skills/adaptive-html-final/modes`, `manifest`, `SKILL`, add-mode runbook | 신규 모드 추가에 필요한 필드/파일/검증 순서 |

---

## 2. 최종 판정

| 우선순위 | 판정 | 후보 모드 | 원천 | 이유 |
|---:|---|---|---|---|
| P0 | **신규 모드 즉시 설계 후보** | `business_plan_html` | `bizplan` | `business-core.yaml`, 증거 태그, 출처대장, 재무/수치 일관성, 평가위원 시뮬레이션은 기존 `expert_html`로 강제할 수 없음 |
| P1 | **신규 모드 즉시 설계 후보** | `storm_research` | `storm-research` | 5관점 source-grounded research, contradiction map, peer-review blocker, provenance footer가 독립 정보 구조를 이룸 |
| P2 | **신규 모드 즉시 설계 후보** | `social_trend_dashboard` | `x-ai-trend-collector` | record schema, URL append/dedupe, metrics caveat, read-only collection 계약은 기존 `seo_dashboard`와 다름 |
| P3 | 조건부 신규 모드 | `operator_manual_html` | `manual-production` | 가치가 크지만 multi-page package, media/video, live UI verification 범위가 커서 1차는 `manual_analysis` 확장 또는 단일 HTML 운영자 가이드로 축소 필요 |
| P4 | 하위 프로파일 우선 | `skill_archive_migration` | `.skill` archives | 현재 `skill_audit`와 매우 가깝다. 반복 수요가 커질 때 별도 모드화 |
| P5 | 기존 모드 강화 | `blog_publication_pack` | blog-writer v1/v2 | `blog_writer` + `seo_dashboard` + `platform_blog` required block 강화가 우선 |
| P6 | 기존 모드 강화 | `beginner_deep_dive` | html-for-beginners | `beginner_html`의 PDF follow, 용어 첫 등장 풀이, 비유/함정/해결 게이트 강화로 충분 |

---

## 3. 기존 17모드와 중복/분리 매트릭스

| 후보 | 겹치는 기존 모드 | 겹치는 점 | 분리/통합 판단 |
|---|---|---|---|
| `business_plan_html` | `expert_html`, `comparison_html`, `checklist_playbook`, `landing_brief_html` | 리포트, 리스크, 비교표, 실행계획, 체크리스트, 피치 요약 | **분리**. 사업계획서의 공식 공고/평가기준/사업 코어/출처대장/재무 산식/평가위원 시뮬은 독립 계약 |
| `storm_research` | `expert_html`, `article_html`, `comparison_html`, `github_analysis`, `youtube_analysis` | 전문가 리포트, 장문 종합, 관점 충돌, source trust | **분리**. 5영혼 raw evidence → 모순 지도 → 종합 → peer review → provenance의 체인이 독립 계약 |
| `social_trend_dashboard` | `seo_dashboard`, `expert_html`, `comparison_html` | 대시보드, 트렌드 요약, 신호 비교 | **분리**. 소셜 record schema와 append/dedupe/update, metric caveat가 기존 모드에 없음 |
| `operator_manual_html` | `manual_analysis`, `education_html`, `beginner_html`, `checklist_playbook` | 매뉴얼, 사용법, 초보자 설명, 운영 절차 | **조건부 분리**. 실제 UI 근거·workflow map·lesson/media/review-card·verification 패키지까지 가면 별도 모드 가치 |
| `skill_archive_migration` | `skill_audit` | 스킬 분석, SKILL/manifest/reference 점검 | **하위 프로파일 우선**. `.skill` zip inventory와 migration matrix만 `skill_audit`에 보강 가능 |

---

## 4. 신규 모드 entry 후보

### 4.1 `business_plan_html` — 사업 논리/지원서 HTML 모드

| 필드 | 값 |
|---|---|
| 권장 파일 | `skills/adaptive-html-final/modes/18-business-plan.json` |
| label | `Business Plan HTML` |
| layout | `.layout-business-plan` / `assets/layouts/business-plan-report.html` |
| recipe | `recipes/business-plan.prompt.md` |
| trigger | `사업계획서`, `정부지원사업`, `R&D 계획서`, `투자 피치덱`, `제안서`, `공고문 분석`, `business-core`, `지원사업 신청서` |
| primary_vt | `implementation-plan` |
| vt 후보 | `implementation-plan`, `quality-gate`, `risk-matrix`, `timeline`, `comparison-cards`, `process-swimlane` |
| wg 후보 | `wg-16`, `wg-11`, `wg-13`, `wg-18`, `wg-14` |

#### Required blocks

| block | 목적 |
|---|---|
| `generated_row` | 생성일, 모드, profile, 문서 유형, 검증 상태 |
| `document_type_gate` | 정부지원/R&D/투자덱/제안서/내부 신사업 중 평가 논리 확정 |
| `notice_summary` | 공고/서식/자격/배점/제출 제약 요약 |
| `interview_findings` | 인터뷰 기반 확정 사실·가정·모호어 해소 |
| `research_evidence` | 시장/경쟁/기술/특허/논문 근거와 부정 근거 |
| `business_core` | `business-core.yaml` 요약, 문제→해결→제품→기술→시장→실행 논리 사슬 |
| `number_registry` | TAM/SAM/SOM, 가격, 고객수, 매출, 비용, 인력, 일정의 단일 수치 원장 |
| `market_finance_model` | 시장/재무 모델, 산식 기반 숫자와 가정 태그 |
| `template_mapping` | 공식 양식 항목 ↔ core 경로 ↔ 근거 ↔ 표현 |
| `risk_and_ip_paper_notes` | 특허/논문 예비 검토, 법률/제품 성능 한계 |
| `evaluator_scorecard` | 행정·기술·사업성·회의적 평가위원 시뮬레이션 |
| `submission_checklist` | 제출 전 필수서류·서명·분량·서식 체크 |

#### Custom gate 후보

| gate | 조건 |
|---|---|
| `business_plan_evidence_tag_gate` | `[사실] [추정] [가정] [목표] [확인 필요]` 중 필요한 태그가 핵심 주장에 표시됨 |
| `business_plan_number_consistency_gate` | TAM/SAM/SOM·가격·매출·비용·일정이 본문/표/원장 간 불일치 없음 |
| `business_plan_source_gate` | 핵심 통계에 출처 기관·발행일·기준시점·접근일·URL이 있음 |
| `business_plan_status_gate` | draft/verified/submission-ready 상태를 분리하고 과장하지 않음 |

#### 근거

- `orginal_skill/bizplan/SKILL.md:12-20` — 상품은 문장 채우기가 아니라 반론을 견디는 사업 논리이며, 모든 문서는 `business-core.yaml`에서 파생.
- `orginal_skill/bizplan/SKILL.md:24-32` — 7대 절대 규칙: AI 창작 금지, 사실/추정/가정/목표 분리, 출처 없는 핵심 통계 금지, 숫자 일관성.
- `orginal_skill/bizplan/SKILL.md:115-170` — 21단계 워크플로우와 최종 HTML 포함.

---

### 4.2 `storm_research` — STORM 다관점 리서치 HTML 모드

| 필드 | 값 |
|---|---|
| 권장 파일 | `skills/adaptive-html-final/modes/19-storm-research.json` |
| label | `STORM Research` |
| layout | `.layout-storm` / `assets/layouts/storm-research-report.html` |
| recipe | `recipes/storm-research.prompt.md` |
| trigger | `STORM 리서치`, `스톰 방법`, `다관점 딥리서치`, `5영혼으로 조사`, `여러 LLM으로 병렬 리서치`, `모순 지도 포함 리포트`, `출처 강제 리서치` |
| primary_vt | `process-swimlane` |
| vt 후보 | `process-swimlane`, `hero-map`, `risk-matrix`, `quality-gate`, `comparison-cards`, `checklist-flow`, `timeline` |
| wg 후보 | `wg-13`, `wg-14`, `wg-18`, `wg-11`, `wg-16`, `wg-04` |

#### Required blocks

| block | 목적 |
|---|---|
| `generated_row` | 생성일, mode/profile, topic, source count, soul count |
| `method_notice` | STORM 재해석 고지, 논문/도구 링크, 조직성 +25% / coverage +10% claim drift 방지 |
| `research_question` | 주제, 범위, 기간, 지역, 핵심 질문 |
| `perspective_router` | Skeptic/Economist/Historian/Academic/Futurist 또는 주제 맞춤 관점 |
| `soul_evidence_cards` | 5영혼 결과 카드: persona, llm, summary, 핵심 발견, source count |
| `source_map` | URL별 출처, 주장, soul, 날짜, source type |
| `contradiction_map` | consensus, contradiction table, blind spots, key tension |
| `synthesis_article` | lead + 본문 + 미해결 질문 + 인용 유지 |
| `peer_review_gate` | BLOCKER/MAJOR/MINOR, 재작업 여부 |
| `confidence_badges` | source diversity, citation, honesty, verdict |
| `unresolved_questions` | 남은 연구 질문과 추가 조사 방향 |
| `provenance_footer` | STORM 원논문/코드/도구/재해석 고지 |

#### Custom gate 후보

| gate | 조건 |
|---|---|
| `storm_soul_count_gate` | full 출력은 5 souls. solo/partial이면 partial notice 필수 |
| `storm_minimum_sources_gate` | 각 완료 soul source URL ≥ 3 권장, 전체 unique URL 기준 충족 |
| `storm_citation_label_gate` | 사실 주장에는 `[출처: URL]`, 예측/외삽에는 `[추론]` 라벨 |
| `storm_contradiction_gate` | consensus, contradiction table, blind spot, key tension 모두 존재 |
| `storm_peer_review_gate` | peer review BLOCKER가 있으면 최종 pass 표시 금지 |
| `storm_provenance_gate` | 재구현이 아니라 재해석임을 고지, STORM 효과 수치 정확 표기 |

#### Source snapshot 계약

| 경로 | 내용 |
|---|---|
| `sources/storm-report.json` | topic, slug, generated_at, souls, contradiction_map, synthesis, peer_review, confidence, all_sources |
| `sources/storm-results/Skeptic.md` 등 | 5영혼 raw markdown |
| `sources/storm-prompts/1..4.md` | scan/contradict/synthesis/review prompt snapshot + sha256 |
| `sources/storm-charters/*.md` | 5영혼 charter snapshot + sha256 |
| `sources/storm-evidence-map.json` | url, source_type, cited_by_soul, claim_excerpt, label, accessed_at |
| `sources/storm-quality.json` | soul count, source count, blocker count, contradiction completeness |

#### 근거

- `orginal_skill/storm-research/SKILL.md:18-23` — 하나의 주제를 5개 관점으로 출처 기반 딥리서치 후 HTML 리포트 생성.
- `orginal_skill/storm-research/SKILL.md:78-98` — 5영혼 병렬 dispatch, 모든 주장 `[출처: URL]`, 추측 `[추론]`, done + push.
- `orginal_skill/storm-research/SKILL.md:113-143` — 모순 지도 → 종합 → 동료 검토 → `report.json`/HTML.
- `orginal_skill/storm-research/SKILL.md:169-176` — 출처 없는 단언 금지, 동료 검토 없이 최종화 금지, STORM 효과 수치 drift 금지.

---

### 4.3 `social_trend_dashboard` — 소셜/AI 트렌드 대시보드 모드

| 필드 | 값 |
|---|---|
| 권장 파일 | `skills/adaptive-html-final/modes/20-social-trend-dashboard.json` |
| label | `Social Trend Dashboard` |
| layout | `.layout-trend` / `assets/layouts/social-trend-dashboard.html` |
| recipe | `recipes/social-trend-dashboard.prompt.md` |
| trigger | `AI 트렌드`, `X 트렌드`, `트위터 크롤링`, `소셜 피드 대시보드`, `records.json`, `최신 소식 대시보드` |
| primary_vt | `card-grid` |
| vt 후보 | `card-grid`, `timeline`, `risk-matrix`, `quality-gate`, `comparison-cards` |
| wg 후보 | `wg-11`, `wg-13`, `wg-18`, `wg-14`, `wg-02` |

#### Required blocks

| block | 목적 |
|---|---|
| `scope_brief` | 수집 주제, 기간, 대상 피드, 수집 개수 |
| `source_policy` | API/browser/provided/web search/public hydration 중 수집 경로와 한계 |
| `record_schema` | `cat`, `author`, `handle`, `date`, `summary`, `url`, `views`, `likes` |
| `collection_summary` | incoming/existing/added_net/total, append/update 상태 |
| `category_distribution` | 신규 모델·제품, 연구·논문, 업계·투자, 실무 팁·도구 |
| `top_signals` | 조회/좋아요/중요도 기준 상위 항목 |
| `evidence_cards` | 출처 링크와 caveat 포함 카드 |
| `dedupe_append_policy` | URL 기준 dedupe/update |
| `metric_caveats` | 숨김/반올림/미확인 metric은 0 또는 unknown 처리 |
| `verification_notes` | read-only, source link, no engagement 확인 |
| `next_actions` | 다음 수집/자동화/검증 제안 |

#### Custom gate 후보

| gate | 조건 |
|---|---|
| `trend_record_schema_gate` | records list와 필수 필드 존재 |
| `trend_url_dedupe_gate` | `url`이 dedupe key이며 중복 없음 |
| `trend_metric_honesty_gate` | metric이 없으면 0/unknown, 추정 수치 금지 |
| `trend_read_only_gate` | 좋아요/리포스트/팔로우/답글/DM/북마크 금지 고지 |
| `trend_no_js_chart_gate` | Chart.js 등 behavioral JS 없이 정적 CSS bar/card/table로 표현 |

#### 근거

- `orginal_skill/x-ai-trend-collector/SKILL.md:17-24` — Excel report + standalone dashboard, read-only core rule.
- `orginal_skill/x-ai-trend-collector/SKILL.md:48-57` — 공식/API, logged-in browser, provided data, web search, public hydration route.
- `orginal_skill/x-ai-trend-collector/SKILL.md:68-100` — record schema와 URL dedupe/metrics honesty/data-as-data 규칙.
- `orginal_skill/x-ai-trend-collector/SKILL.md:157-208` — append/update 출력과 검증 체크리스트.

---

### 4.4 `operator_manual_html` — 조건부 운영자 가이드 모드

| 필드 | 값 |
|---|---|
| 권장 파일 | `skills/adaptive-html-final/modes/21-operator-manual.json` 또는 `manual_analysis` 확장 |
| label | `Operator Manual HTML` |
| layout | `.layout-operator-manual` / `assets/layouts/operator-manual-guide.html` |
| recipe | `recipes/operator-manual.prompt.md` |
| trigger | `운영자 매뉴얼`, `사용자 매뉴얼 패키지`, `튜토리얼`, `온보딩 가이드`, `workflow map`, `screen-grounded guide` |
| primary_vt | `process-swimlane` |
| vt 후보 | `process-swimlane`, `checklist-flow`, `hero-map`, `quality-gate`, `file-tour` |
| wg 후보 | `wg-08`, `wg-13`, `wg-14`, `wg-16`, `wg-18`, `wg-11` |

#### Required blocks

`artifact_format_gate`, `audience_scope`, `source_hierarchy`, `workflow_inventory`, `system_overview`, `workflow_map`, `lesson_boundaries`, `step_evidence_cards`, `risk_safe_fixture`, `verification_record`, `handoff_boundary`

#### 통합 판단

이 후보는 기존 `manual_analysis`와 충돌한다. 첫 릴리스에서는 **별도 신규 모드보다 `manual_analysis`에 source hierarchy, workflow-first, capture_required, safe_fixture, verification_record 블록을 보강**하는 것이 안전하다. 별도 모드화는 live UI evidence와 media package까지 정본화할 때 진행한다.

#### 근거

- `orginal_skill/manual-production/SKILL.md:17-25` — 실제 workflow inventory 전 작성 금지, beginner-first rule.
- `orginal_skill/manual-production/SKILL.md:49-56` — Analysis → Structuring → index/system overview → step production → verification 순서.
- `orginal_skill/manual-production/SKILL.md:59-72` — Artifact format gate, static package 기본 구조.
- `orginal_skill/manual-production/SKILL.md:170-180` — manual-verification, 완료 보고 분리.

---

## 5. 신규 모드 추가 표면 체크리스트

`docs/adaptive-html-final-add-mode-runbook.md` 기준, 실제 추가 시 아래 표면을 한 세트로 갱신한다.

| 순서 | 파일/표면 | 작업 |
|---:|---|---|
| 1 | `skills/adaptive-html-final/modes/NN-<mode>.json` | 18개 필드 작성 |
| 2 | `assets/layouts/<layout>.html` | layout skeleton + placeholder |
| 3 | `assets/layouts.css` | `.layout-<name>` 표면/반응형 |
| 4 | `recipes/<mode>.prompt.md` | 모드별 작성 프롬프트 |
| 5 | `SKILL.md` | frontmatter, Identity count, §0.6 결정표, 트리거, 필수 블록 |
| 6 | `AGENTS.md` | §3 결정표, 모드 수 표면, §8 reference index |
| 7 | `manifest.json` | `modes[]`, `layouts[]`, `examples`, `quality.governance_count` |
| 8 | `references/mode-selection.md` | 우선순위/충돌 처리 |
| 9 | `references/layout-system.md` | mode table/core blocks/layout-first |
| 10 | `references/widget-system.md` | mode→wg / wg→mode |
| 11 | `references/writing-system.md`, `quality-gates.md` | 모드별 작성·완료 기준 |
| 12 | 신규 reference | 예: `references/business-plan-system.md`, `storm-research-system.md`, `social-trend-dashboard-system.md` |
| 13 | `validate_output.py` | custom semantic gate가 필요할 때만 |
| 14 | `completion_check.py` | benchmark 모드 수가 늘면 17 하드코딩 제거/갱신 |
| 15 | `tests/test_governance_gates.py` | count/range/fixture/custom gate 갱신 |
| 16 | `README.md`, `Guide.md`, `docs/*17-mode*` | 현행 모드 수와 게이트 수 표면 정합 |
| 17 | `examples/NN_*.html`, `examples/index.html` | 신규 reference example |
| 18 | `examples/sources/*` | manifest/css/profile snapshots |
| 19 | `skills/adaptive-html-final.skill` | 재패키징 + byte-match |

---

## 6. 검증 명령

신규 모드 구현 후 완료 기준은 아래 순서다.

```bash
python3 skills/adaptive-html-final/scripts/check_mode_registry_sync.py --skill-dir skills/adaptive-html-final
python3 skills/adaptive-html-final/scripts/validate_output.py skills/adaptive-html-final/examples --skill-dir skills/adaptive-html-final
python3 skills/adaptive-html-final/scripts/quality_contract_check.py skills/adaptive-html-final/examples
python3 skills/adaptive-html-final/tests/test_governance_gates.py
python3 skills/adaptive-html-final/scripts/completion_check.py skills/adaptive-html-final/examples
git diff --check
```

신규 output 산출물은 추가로 `scripts/render_audit_fulltest.mjs <output_dir>` 후 `completion_check.py <output_dir>` 순서로 검증한다.

---

## 7. 구현 추천 순서

1. **1차 릴리스 후보**: `business_plan_html` 단일 모드만 추가한다. 가장 차별점이 크고 `adaptive-html-final`의 전문가 리포트/증거 표현과 잘 맞는다.
2. **2차 릴리스 후보**: `storm_research`를 추가한다. source snapshot과 custom gate 설계가 먼저 필요하다.
3. **3차 릴리스 후보**: `social_trend_dashboard`를 추가한다. 원본 수집/엑셀 생성은 외부 전처리로 두고, AHF는 records 기반 무-JS HTML renderer로 정의한다.
4. **보강 항목**: `manual_analysis`, `skill_audit`, `blog_writer`, `beginner_html`에 각각 operator workflow, archive inventory, publication pack, beginner deep-dive gate를 추가한다.

---

## 8. 완료 판정

이번 추출 단계에서 신규 모드로 **바로 설계 가능한 entry 3개**와 **조건부/보강 후보 4개**를 분리했다. 기계가 읽을 수 있는 후보 목록은 `docs/orginal-skill-new-mode-entry-candidates-20260621.json`, copy-ready registry skeleton은 `docs/orginal-skill-mode-entry-skeletons-20260621.json`에 별도로 고정했다.

- 신규 모드 즉시 후보: `business_plan_html`, `storm_research`, `social_trend_dashboard`
- 조건부 신규 후보: `operator_manual_html`
- 기존 모드 보강 후보: `skill_archive_migration`, `blog_publication_pack`, `beginner_deep_dive`

실제 구현은 버전/릴리스 승인과 registry/examples/governance 동기화가 필요하므로 이 문서는 **신규 모드 진입 전 설계 입력**으로 사용한다.
