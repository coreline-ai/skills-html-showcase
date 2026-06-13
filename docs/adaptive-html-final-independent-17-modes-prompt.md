# adaptive-html-final 17모드 독립 생성 프롬프트

목표: 최신 `adaptive-html-final` 스킬로 공식 17개 모드별 HTML을 **서로 독립적으로** 생성한다. 각 모드는 다른 주제, 본문 섹션 10개 이상.

## 필수 원칙

1. 버전 변경 금지. 버전은 `skills/adaptive-html-final/manifest.json`에서 읽는다.
2. 반드시 순서대로 읽는다: `AGENTS.md` → `skills/adaptive-html-final/SKILL.md` → 필요한 references/assets.
3. `profile=auto` 사용.
4. 이전 모드 HTML을 다음 모드의 구조·문체·템플릿으로 참조하지 않는다.
5. 한 번에 복붙 생성 금지. **1모드 생성 → 검증 → 보고 → 다음 모드** 순서로 진행한다.
6. 모든 섹션은 view/card surface로 감싼다.
7. 섹션 h2는 `body-icon → 번호/라벨 → 제목` 순서를 지킨다.
8. 최신 헤더를 사용한다: 생성일, 렌즈/관점, 8테마 스위처 포함.
9. 최신 목차 템플릿을 사용한다. 단순 텍스트 나열 금지, 링크 동작 필수.
10. 같은 카드/리스트 반복 금지. 모드별 layout, vt, wg를 정보 구조에 맞게 섞는다.
11. 1280px/390px에서 overflow와 마지막 섹션 대비를 확인한다.
12. placeholder 문구 금지: `전문 예제`, `기준 1`, `Generated example`, `샘플 텍스트` 등.

## 공식 모드 순서

1. skill_audit
2. platform_blog
3. seo_dashboard
4. education_html
5. github_analysis
6. github_feature_usage
7. youtube_analysis
8. manual_analysis
9. expert_html
10. article_html
11. blog_writer
12. beginner_html
13. reference_html
14. comparison_html
15. case_study_html
16. landing_brief_html
17. checklist_playbook

## 출력

- 폴더: `output/adaptive-html-final-independent-17-modes-YYYYMMDD_HHMMSS/`
- 페이지: `pages/NN_<mode>_<topic_slug>.html`
- 인덱스: `index.html`

## 모드별 시작 전 계획표

| 항목 | 내용 |
|---|---|
| mode |  |
| topic |  |
| layout |  |
| primary vt |  |
| wg |  |
| 10 sections |  |
| pattern mix |  |
| risks |  |

## 모드별 검증

```bash
python3 skills/adaptive-html-final/scripts/validate_output.py <output_dir> --skill-dir skills/adaptive-html-final
python3 skills/adaptive-html-final/scripts/quality_contract_check.py <output_dir>
```

## 전체 완료 검증

```bash
python3 skills/adaptive-html-final/scripts/completion_check.py <output_dir>
python3 skills/adaptive-html-final/tests/test_governance_gates.py
git diff --check
```

## 모드별 보고 형식

```md
## NN / 17 완료 — <mode>

| 항목 | 결과 |
|---|---|
| 주제 |  |
| 파일 |  |
| 섹션 수 |  |
| layout |  |
| vt/wg |  |
| validate | OK |
| quality | OK |
| 링크 |  |

다음 모드는 새 독립 빌드로 진행.
```

## 절대 금지

- 이전 HTML 복사/참조
- 17개를 같은 틀로 찍어내기
- 검증 없이 완료 보고
- 최신 assets 미확인
- 임시 mini-card/col-list 반복
- 버전 임의 변경
