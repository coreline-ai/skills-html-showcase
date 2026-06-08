# adaptive-html-final 최신 프로젝트 업데이트 상세 스킬 분석

- 분석 시각: 2026-06-08 08:13:10 KST
- 저장소: `/Users/iriver/hwan/projects/html-skills-doc`
- Git 상태: `main...origin/main`, working tree clean
- 기준 커밋: `c032466` (`Merge remote-tracking branch 'origin/main'`)
- 분석 대상 스킬: `skills/adaptive-html-final`
- 현재 manifest 버전: `5.9.1`

## 1. 한 줄 결론

`adaptive-html-final`은 최신 상태에서 단순 HTML 생성 스킬을 넘어, **16개 모드 라우터 + 8테마 CSS-only 렌더링 + vt/wg 템플릿 계약 + 자산 무결성 검증 + 정성 품질 게이트**를 가진 “검증 가능한 한국어 editorial HTML 생성 엔진”으로 진화했다. 다만 현재 worktree에는 정본 16예제와 별도로 과거 예제 및 오래된 output 스냅샷이 같이 남아 있어, **스킬 본체는 최신이나 일부 산출물 폴더는 최신 게이트 기준 재생성/정리가 필요**하다.

## 2. 최신 업데이트 핵심 요약

| 영역 | 현재 상태 | 분석 |
|---|---:|---|
| 버전 | `5.9.1` | 최신 manifest/SKILL.md/CHANGELOG는 5.9.1로 일치한다. |
| 모드 | 16개 | 기존 13모드에 `github_analysis`, `youtube_analysis`, `manual_analysis`가 추가되어 실사/영상/매뉴얼 분석까지 확장됐다. |
| 레이아웃 | 16개 | 각 모드가 독립 layout 파일을 갖는다. `github-analysis.html`, `youtube-analysis.html`, `manual-analysis.html` 포함. |
| 테마 | 8개 | `light`, `light2`, `white`, `dark`, `dark2`, `blue`, `skyblue`, `sepia`를 `name="ahf-theme"` 라디오로 무 JS 전환한다. |
| vt 템플릿 | 21종 | `visual-html-templates/01..21` 네이티브 HTML 도판. auto/diagram 프로파일에서 모드 1순위 vt 삽입이 계약화됐다. |
| wg 위젯 | 20종 | `widget-templates/01..20` CSS-only 위젯. auto/widget 프로파일에서 모드 권장 wg 사용이 계약화됐다. |
| body icons | 32종 | 직접 섹션 h2에 body-icon을 강제해 섹션 인지가 좋아졌다. |
| editorial patterns | 8종 | chronology/source/core-insight/accessibility-checklist 등 본문 구조 패턴이 정본화됐다. |
| soft shapes | 36종 | 장식 앵커용 8000x6000 SVG 도형 자산. |
| workflow visuals | 10종 | 워크플로우 대표 도판 자산. `workflow-` 네임스페이스 사용. |
| 검증 체계 | 3단 | `validate_output.py` + `quality_contract_check.py` + `test_governance_gates.py`를 `completion_check.py`로 묶는다. |

## 3. 아키텍처 변화 분석

### 3.1 13모드에서 16모드로 확장

현재 라우터는 다음 16개 모드를 지원한다.

1. `skill_audit`
2. `platform_blog`
3. `seo_dashboard`
4. `education_html`
5. `github_analysis`
6. `youtube_analysis`
7. `manual_analysis`
8. `expert_html`
9. `article_html`
10. `blog_writer`
11. `beginner_html`
12. `reference_html`
13. `comparison_html`
14. `case_study_html`
15. `landing_brief_html`
16. `checklist_playbook`

업데이트의 의미는 크다. `github_analysis`는 README 재요약이 아니라 저장소 채택/감사/실행 판단을 만드는 실사 리포트가 되었고, `youtube_analysis`는 영상 주장·근거·댓글·재사용 전략을 FACT/INFERENCE/UNKNOWN으로 분리한다. `manual_analysis`는 매뉴얼을 역할별 실행 경로, 안전 조건, 트러블슈팅, 운영 런북으로 재구성한다.

### 3.2 모드별 시각 계약 강화

`v5.9.0`에서 가장 큰 변화는 시각 요소가 “있으면 좋은 보강”에서 “검증 가능한 계약”으로 바뀐 점이다.

- `diagram/auto` 출력은 모드별 1순위 `vt-` 템플릿을 최소 1회 포함해야 한다.
- `widget/auto` 출력은 모드 권장 `wg-` 위젯 중 최소 1개를 포함해야 한다.
- 직접 콘텐츠 섹션은 `.try`를 제외하고 카드 surface를 가져야 한다.
- 직접 섹션 첫 h2에는 body-icon이 있어야 한다.
- 같은 아이콘을 무의미하게 반복하면 다양성 게이트에서 실패한다.

이 변경은 사용자가 지적했던 “섹션만 가져다 붙인 결과”를 막는 방향으로 정확히 들어갔다. 즉 최신 스킬은 **모드별 템플릿이 실제 화면에서 식별되어야만 통과**하도록 설계됐다.

### 3.3 8테마 시스템 안정화

테마는 `theme-dark.css`가 print 뒤 맨 끝에 항상 인라인되는 방식이다. 코어 해시 대상에서는 제외되지만 출력에는 반드시 들어간다. 이 구조는 다음 장점이 있다.

- 라이트 기본 출력의 코어 해시 안정성 유지
- CSS-only 라디오 전환으로 외부/동작 JS 0 유지
- 다크/로즈/블루/스카이/세피아까지 확장 가능
- legacy `#theme-toggle` 제거

현재 테마 시스템은 기능적으로 강하지만, 오래된 output은 `theme-dark.css`가 인라인되지 않아 최신 validator에서 실패한다. 따라서 산출물 재생성 시 테마 슬롯 동기화가 필수다.

## 4. 최근 버전별 의미

### v5.9.1

- `wg-10` figure sheet를 모드 정본 데모 섹션 안에서만 full-width로 확장했다.
- 일반 본문에서의 `wg-10` 폭은 유지해 가독성 회귀를 피했다.
- `section.lead`가 prose `.lead` max-width를 상속해 직접 섹션 카드가 좁아지는 문제를 layout 쪽에서 보정했다.

### v5.9.0

- 카탈로그에서 검증된 반응형/폭/대비 보정을 실제 스킬 자산으로 reverse-sync했다.
- vt/wg 모바일 overflow, 카드 폭, 대비, wg-09/wg-07 동기화가 들어갔다.
- `direct_section_title_icon_policy_gate`, `body_icon_diversity_gate`, `mode_template_contract_gate`가 추가됐다.

### v5.8.1

- `generated-date` 긴 텍스트가 모바일 390px에서 가로 스크롤을 만드는 문제를 수정했다.
- core CSS가 변경되었으므로 이전 산출물의 inline hash는 최신 스킬과 불일치할 수 있다.

### v5.8.0

- `youtube_analysis`, `manual_analysis`가 섹션 수만 많고 본문 밀도가 낮아지는 문제를 막기 위해 깊이 계약을 추가했다.
- `mode_section_depth_too_thin`과 `profile_vt_template_missing` 게이트가 들어갔다.
- “블록 수 충족 != 완료”가 명문화됐다.

### v5.7.0

- 15번째 `youtube_analysis`, 16번째 `manual_analysis`가 추가됐다.
- 전용 layout, references, recipes, validator 계약이 생겼다.
- `quality_contract_check.py`가 추가되어 validator OK지만 붕어빵인 산출물을 막는다.

## 5. 검증 결과

### 5.1 스킬 게이트 자체

명령:

```bash
python3 skills/adaptive-html-final/tests/test_governance_gates.py
```

결과:

```text
77/77 checks passed
```

해석: 스킬의 validator/gate 함수 자체는 최신 회귀 테스트를 통과한다.

### 5.2 manifest 기준 정본 16예제

manifest에 명시된 16개 예제 + index + sources만 임시 폴더로 분리해 검증했다.

결과:

```text
HTML files: 17
OK
OK — quality contract guard passed (16 HTML content file(s))
```

해석: **정본 16모드 예제 세트는 최신 스킬 5.9.1 기준으로 validate/quality를 통과**한다.

### 5.3 전체 `skills/adaptive-html-final/examples/`

명령:

```bash
python3 skills/adaptive-html-final/scripts/completion_check.py skills/adaptive-html-final/examples
```

결과:

```text
완료 통합 검증: 2/3 통과 -> INCOMPLETE
```

원인:

`examples/`에는 manifest에 포함되지 않은 과거 예제 7개가 남아 있다.

- `01_beginner_learning_rag.html`
- `02_expert_mcp_gateway_report.html`
- `03_article_developer_blog_portfolio.html`
- `04_education_github_pages_course.html`
- `05_blog_local_automation_essay.html`
- `06_seo_docker_dashboard.html`
- `07_platform_ai_agent_adaptation.html`

이 파일들은 `vt-`, `wg-`, `theme-dark`, core hash marker가 없거나 부족해 최신 gate에서 실패한다. 따라서 현재 상태는 “정본 16예제 OK, examples 폴더 전체는 레거시 잔존 때문에 FAIL”로 보는 것이 맞다.

### 5.4 기존 output 폴더 상태

대표 output 검증 결과:

| output | 상태 | 주요 원인 |
|---|---|---|
| `output/adaptive-html-final-13-topics-20260605_083433` | FAIL, 193 issues | v5.2/v5.7 계열 산출물이라 최신 5.9.1 CSS/hash/theme/vt/wg 계약과 불일치 |
| `output/adaptive-html-final-sequential-16-modes-20260607_105404` | FAIL | source version `5.8.1`, 최신 `5.9.1` CSS/hash/theme-dark 스냅샷 불일치 |
| `output/adaptive-html-final-showcase-v4` | FAIL, 341 issues | v4 계열 산출물이라 body-icon, section surface, hash, theme 계약에서 대량 불일치 |

해석: output 폴더의 과거 쇼케이스는 “열람용 기록”으로는 가치가 있지만, 최신 스킬 검증 기준의 골든으로 쓰면 안 된다. 최신 기준 골든은 manifest 정본 16예제 또는 새로 재생성한 output이어야 한다.

## 6. 강점

1. **모드 분리도가 좋아졌다.** 16모드가 각각 layout/recipe/reference를 갖고, GitHub/YouTube/Manual처럼 입력 특성이 다른 모드도 품질 계약을 따로 가진다.
2. **시각 요소가 검증 가능해졌다.** vt/wg 사용이 정적 게이트로 잠겼기 때문에, 모드별 섹션이 실제 템플릿 수준으로 보이는지 추적할 수 있다.
3. **무 JS 원칙이 유지된다.** 8테마, 위젯, details/radio 기반 인터랙션 모두 CSS-only다.
4. **출력 재현성이 강화됐다.** core CSS hash, byte-for-byte inline, `sources/assets/*.css`, `css-integrity.json`, source manifest 동기화가 계약화됐다.
5. **품질 게이트가 정량화됐다.** placeholder, mini-card 반복, 얇은 섹션, vt 누락, h2 아이콘 누락 등을 자동으로 잡는다.

## 7. 2026-06-08 추가 예제 업데이트 기록

### 7.1 `10_comparison_message_queue.html` 비교 모드 본문 보정

- 대상 파일: `skills/adaptive-html-final/examples/10_comparison_message_queue.html`
- 대상 섹션: `4 선택 기준 — 무엇을 보고 고를까`
- 변경 내용: 핵심 3개 선택 기준 카드는 유지하고, 그 아래 래퍼 없는 보조 기준 5줄(`순서·중복 정확도`, `라우팅 복잡도`, `지연 민감도`, `클라우드 종속`, `팀 친숙도`)을 `table-scroll` + `table` 구조로 교체했다.
- 스킬 에셋 반영: `assets/editorial-patterns.css`에 `.criteria-table` 보조 기준 표 패턴을 추가했고, `assets/layouts/comparison-matrix.html`의 tradeoffs 섹션에 `data-ahf-pattern="criteria-table-preferred"`를 부여했다.
- 생성 규칙 반영: `SKILL.md`, `references/layout-system.md`, `references/quality-gates.md`에 `comparison_html` 보조 기준 4개 이상은 `.col-list`보다 `table.table.criteria-table`을 우선한다는 규칙을 추가했다.
- 카탈로그 싱크: `templates/final_20260604/index-all-templates-catalog.html`에 `.criteria-table` CSS와 변경 내역 행(`comparison_html · criteria table`)을 반영했다.
- 의도: 텍스트만 나열되어 보이던 보조 기준을 `기준 / 판단 포인트 / 유리한 후보 / 주의할 점` 컬럼으로 재구성해 비교 모드의 스캔성과 정보 구조를 높였다.
- 검증: 10번 단독 `validate_output.py` OK, 정본 17개 예제 세트 `validate_output.py` OK, 무 JS/금지 속성 검사 OK, `test_governance_gates.py` 77/77 OK.

## 8. 취약점과 리스크

### P0 — 레거시 예제 파일이 전체 examples 검증을 깨뜨림

정본 16예제는 OK지만, `examples/` 전체를 대상으로 하면 과거 예제 7개 때문에 `completion_check.py`가 FAIL이다. 이 상태는 CI나 사용자가 폴더 전체를 검증할 때 혼란을 만든다.

권장 조치:

- 레거시 예제를 `examples/archive/`로 이동하고 validator 대상에서 제외
- 또는 최신 5.9.1 자산으로 재인라인
- 또는 manifest 밖 예제도 `validate_output.py`가 의도적으로 검사할지 정책 결정

### P1 — README와 manifest 버전 불일치

`manifest.json`은 `5.9.1`이지만 README 일부 배지/문구는 `5.7.0`, 하단 문구는 `5.2.3`을 가리킨다. 사용자는 README를 먼저 보므로 최신 상태 판단에 혼선이 생긴다.

권장 조치:

- README version badge를 `5.9.1`로 갱신
- “최신 업데이트” 섹션에 v5.8.0~v5.9.1 요약 추가
- 하단 생성 도구 문구의 13-mode/3-theme 표현 제거

### P1 — 과거 output이 최신 골든처럼 보임

`output/adaptive-html-final-13-topics-20260605_083433`는 제목이 16모드 신규 주제 쇼케이스지만, 최신 5.9.1 validator 기준으로는 193개 이슈가 있다. 사용자가 이 파일을 최신 골든으로 오해할 가능성이 있다.

권장 조치:

- output index에 “archived / generated with v5.x” 표시
- 최신 5.9.1 기준 16모드 output을 새 폴더로 재생성
- README의 라이브 링크를 최신 통과 산출물로 교체

### P2 — AGENTS.md와 최신 SKILL.md 사이 우선순위는 맞지만 과거 설명 흔적 주의

현재 AGENTS.md는 16모드와 5.9.1을 반영하고 있다. 다만 과거 산출물 설명/골든 설명에서는 v5.2.3 기준이 남아 있어, 운영자는 “골든”이라는 단어를 볼 때 버전 기준을 확인해야 한다.

## 9. 권장 후속 작업

1. `examples/` 정리
   - manifest 밖 7개 레거시 예제 이동 또는 재인라인
   - 목표: `python3 skills/adaptive-html-final/scripts/completion_check.py skills/adaptive-html-final/examples` 3/3 통과

2. README 최신화
   - version badge: `5.9.1`
   - modes/themes/examples 설명: 16모드, 8테마, 정본 16예제
   - v5.8.0~v5.9.1 업데이트 요약 추가

3. 최신 output 재생성
   - 새 폴더 예: `output/adaptive-html-final-16-modes-v591-YYYYMMDD_HHMMSS`
   - 정본 16모드 기준으로 생성
   - `completion_check.py` + 1280/390 캡처 확인

4. 과거 output 아카이브 표기
   - v4/v5.2/v5.8 계열 output은 `archive` 또는 README에서 “historical”로 분류
   - 최신 검증 대상과 열람용 기록을 분리

## 10. 최종 판정

현재 프로젝트의 최신 스킬 본체는 구조적으로 강해졌고, `5.9.1` 기준 정본 16예제는 검증 가능하다. 특히 v5.8~v5.9 계열 업데이트는 사용자가 반복해서 지적한 “템플릿 수준이 아니라 섹션 나열처럼 보이는 문제”, “모바일/다크/폭/대비 회귀”, “얇은 youtube/manual 문서”를 직접 겨냥한다.

다만 repository 전체 관점에서는 아직 정리 과제가 있다. **스킬 엔진은 최신이고 강하지만, examples/output 문서 표면에는 과거 산출물이 섞여 있어 최신 검증 기준과 충돌한다.** 따라서 다음 패치의 목표는 기능 추가가 아니라 “최신 정본만 통과하고 과거 기록은 명확히 아카이브되는 상태”로 만드는 것이다.
