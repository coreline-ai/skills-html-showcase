# adaptive-html-final 17-mode sequential benchmark runbook

작성 일시: `2026-06-14 KST`
대상 스킬: `skills/adaptive-html-final` v5.10.4+

이 문서는 17개 공식 모드를 **서로 독립된 신규 주제**로 생성할 때 따라야 하는 순차 실행 절차다. 목표는 빠른 대량 생성이 아니라, 각 모드가 공식 layout/vt/wg/body-icon 자산을 실제로 읽고 적용했다는 증거를 남기는 것이다.

## 1. 원칙

1. 한 모드가 끝나기 전 다음 모드를 시작하지 않는다.
2. 이전 모드 HTML을 다음 모드의 구조·문체·주제 예시로 열람하지 않는다.
3. 다음 모드로 넘길 수 있는 정보는 `파일 경로`, `검증 OK 여부`, `index 링크 제목`뿐이다.
4. 각 모드는 신규 topic을 사용한다. 같은 주제의 변형 반복은 실패다.
5. 모든 모드는 `profile=auto`를 기본으로 하며, AGENTS.md §3 결정표의 layout/vt/wg를 따른다.
6. 텍스트-only 섹션도 `lede-note`, `source-note`, `core-insight`, `summary-card`, `impact-card`, `chron-card`, vt/wg 카드 중 하나로 감싼다.
7. 검증 OK와 사용자 눈검수 OK를 분리한다.

## 2. 공식 모드 순서

1. `skill_audit`
2. `platform_blog`
3. `seo_dashboard`
4. `education_html`
5. `github_analysis`
6. `github_feature_usage`
7. `youtube_analysis`
8. `manual_analysis`
9. `expert_html`
10. `article_html`
11. `blog_writer`
12. `beginner_html`
13. `reference_html`
14. `comparison_html`
15. `case_study_html`
16. `landing_brief_html`
17. `checklist_playbook`

## 3. 모드별 필수 산출물

각 페이지 `<page-stem>.html`마다 아래 파일을 저장한다.

```text
sources/modes/<page-stem>/mode-build-sheet.md
sources/modes/<page-stem>/build-evidence.json
```

### mode-build-sheet.md 필수 항목

| 항목 | 설명 |
|---|---|
| mode | 공식 mode id |
| topic | 해당 모드의 신규 독립 주제 |
| layout | 사용 layout 파일 |
| primary vt | 사용 1순위 vt 파일 |
| wg candidates | 사용한 wg 파일 목록 |
| body icons | 사용한 body-icon id 목록 |
| sections | h2 섹션 10개 이상 |
| template mapping | 섹션별 layout/vt/wg/editorial pattern 매핑 |
| visual risks | 폭·대비·rail·간격 리스크 |
| stop condition | 다음 모드로 넘어가기 전 중단 조건 |

### build-evidence.json 필수 항목

```json
{
  "mode": "manual_analysis",
  "topic": "...",
  "profile": "auto",
  "layout": "manual-analysis.html",
  "primary_vt": "hero-map",
  "page": "pages/08_manual_analysis_....html",
  "sections": ["..."],
  "section_mapping": {"01": "layout hero + vt hero-map"},
  "files": [
    {"path": "AGENTS.md", "sha256": "..."},
    {"path": "skills/adaptive-html-final/SKILL.md", "sha256": "..."},
    {"path": "skills/adaptive-html-final/assets/layouts/manual-analysis.html", "sha256": "..."}
  ]
}
```

`files`는 최소 5개 이상이어야 하며, 기록된 sha256은 현재 워킹트리 파일과 일치해야 한다.

## 4. benchmark-manifest.json

17개 페이지를 묶은 output은 아래 파일을 둔다.

```text
sources/benchmark-manifest.json
```

필수 항목:

```json
{
  "kind": "adaptive-html-final-17-mode-independent-benchmark",
  "profile": "auto",
  "mode_count": 17,
  "pages": [
    {"mode": "skill_audit", "topic": "...", "file": "pages/01_skill_audit_....html", "evidence": "sources/modes/01_skill_audit_.../build-evidence.json", "build_sheet": "sources/modes/01_skill_audit_.../mode-build-sheet.md"}
  ]
}
```

`completion_check.py`는 이 manifest가 있으면 page-level evidence와 build sheet 존재를 강제한다.

## 5. render/micro audit

브라우저 캡쳐 후 `sources/render-audit.json`에 아래를 포함한다.

```json
{
  "viewports": {"1280": {"overflow_ok": true}, "390": {"overflow_ok": true}},
  "micro_layout": {
    "all_ok": true,
    "checks": {
      "heading_badge_nowrap": true,
      "rail_color_variety": true,
      "rail_text_padding": true,
      "card_vertical_rhythm": true,
      "footer_centered": true,
      "no_noncanonical_classes": true
    }
  }
}
```

micro-layout 실패는 completion 실패다.

## 6. 검증 순서

각 모드 생성 후:

```bash
python3 skills/adaptive-html-final/scripts/validate_output.py <output_dir> --skill-dir skills/adaptive-html-final
python3 skills/adaptive-html-final/scripts/quality_contract_check.py <output_dir>
node scripts/render_audit_fulltest.mjs <output_dir>
python3 skills/adaptive-html-final/scripts/completion_check.py <output_dir>
```

전체 완료 후:

```bash
python3 skills/adaptive-html-final/tests/test_governance_gates.py
git diff --check
```

## 7. 수동 눈검수 이슈 반영 절차

1. 사용자가 지적한 위치를 page/section/viewport로 기록한다.
2. 단일 output patch로 끝내지 않고, 원인이 스킬 자산·작성 프로토콜·검증기 중 어디인지 분류한다.
3. 스킬 자산 문제면 asset 수정 + examples 재인라인 + `.skill` 재패키징을 수행한다.
4. 작성 프로토콜 문제면 protocol/runbook에 실패 예시와 올바른 처리 규칙을 추가한다.
5. 검증기 공백이면 악성 fixture를 먼저 만들고 실패를 확인한 뒤 gate를 추가한다.
6. 수정 후 render-audit 1280/390과 completion 4/4를 다시 실행한다.

## 8. 완료 보고 형식

| No | Mode | Topic | Sections | Build Sheet | Evidence | Validate | Quality | Completion | Browser | Manual QA |
|---:|---|---|---:|---|---|---|---|---|---|---|
| 1 | skill_audit | ... | 10+ | OK | OK | OK | OK | OK | OK | pending/OK |

Manual QA는 사용자가 실제로 승인한 뒤에만 OK로 쓴다.
