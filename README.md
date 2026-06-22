<div align="center">

<img width="2752" height="1596" alt="똑똑한 HTML 요정 기능 소개" src="https://github.com/user-attachments/assets/18690d7b-ea95-430b-b450-7ae95a61999e" />

<img width="0" height="0" alt="뚝딱! 마법의 HTML 변신 도구" src="https://github.com/user-attachments/assets/73915e46-1a31-49b1-9023-dbd724c90534" />

<img width="0" height="0" alt="완벽한 HTML 변환 파이프라인 안내" src="https://github.com/user-attachments/assets/aad48544-f667-438a-a28b-5c55f38a1909" />

# 🎨 Adaptive HTML Final

[![skill](https://img.shields.io/badge/skill-adaptive--html--final-e63946)](skills/adaptive-html-final)
[![version](https://img.shields.io/badge/version-5.10.6-3178C6)](skills/adaptive-html-final/CHANGELOG.md)
[![modes](https://img.shields.io/badge/modes-18-2a7d5a)](#-17개-모드)
[![profiles](https://img.shields.io/badge/profiles-widget·diagram·auto-8a5e10)](#️-비주얼-프로파일)
[![themes](https://img.shields.io/badge/themes-8--theme-111827)](#-8-테마-시스템)
[![libraries](https://img.shields.io/badge/view%20widgets-20-e63946)](#️-비주얼-프로파일) [![svg→html](https://img.shields.io/badge/svg→html%20templates-21-d99a38)](#️-비주얼-프로파일)
[![governance](https://img.shields.io/badge/governance-199%2F199-2a7d5a)](#-품질-게이트--결정론)
[![lang](https://img.shields.io/badge/lang-한국어-0b7285)](#)
[![external JS](https://img.shields.io/badge/external%20JS-0-success)](#-품질-게이트--결정론)
[![cross-agent](https://img.shields.io/badge/cross--agent-AGENTS.md-6e40c9)](AGENTS.md)
[![python](https://img.shields.io/badge/SVG%20render-stdlib%20only-3776AB?logo=python&logoColor=white)](skills/adaptive-html-final/scripts/render_visual_svg.py)

**입력 자료를 18개 모드로 라우팅해 전문가급 한국어 HTML 콘텐츠를 만드는 단일 통합 스킬 — GitHub 저장소 실사·GitHub 기능/도입 가이드·YouTube 영상·매뉴얼 분석, 8-테마, 비주얼 프로파일(위젯형·도식형·자동) 선택**

URL·PDF·텍스트·메모·기술 문서·블로그 초안·`SKILL.md`/`.skill`·GitHub 저장소 URL·YouTube URL/자막·제품 매뉴얼을 받아 학습자료, 전문가 리포트, 저장소/영상/매뉴얼 분석, 아티클, 교육 모듈, 블로그 원고, SEO 대시보드, 플랫폼 변환, 스킬 감사, 레퍼런스, 비교, 케이스 스터디, 랜딩, 체크리스트로 변환합니다.

[Overview](#-overview) · [빠른 시작](#-빠른-시작) · [18개 모드](#-18개-모드) · [비주얼 프로파일](#️-비주얼-프로파일) · [8-테마](#-8-테마-시스템) · [쇼케이스](#️-쇼케이스-갤러리) · [v5.10.5 생성물](#v5105-demo17-rose-captures) · [v5.10.3 생성물](#v5103-codex-sepia-captures) · [아키텍처](#️-아키텍처--디자인-시스템) · [품질 게이트](#-품질-게이트--결정론) · [사용법](#-사용법)

</div>

> [!NOTE]
> **외부/동작 JS 0** · **결정론적 크로스-에이전트**(Claude Code · Codex · Gemini 동일 출력) · **자기방어 검증 게이트 199/199** · 입력→정보구조 재구성 파이프라인. 단순 변환기가 아니라, 무엇을 어떻게 보여줄지 **모드·레이아웃·프로파일을 결정표로 고정**해 생성합니다.

---

## ✨ 핵심 특징

| | |
|---|---|
| 🧭 **18개 모드 라우터** | 입력·목적을 분석해 `skill_audit`·`github_analysis`·`youtube_analysis`·`manual_analysis` 등 17개 정보 구조 중 하나로 자동 라우팅 |
| 🎚️ **3 비주얼 프로파일** | `widget`(CSS 위젯) · `diagram`(SVG→HTML 도식) · `auto`(둘 다, 기본). 코어는 100% 공유, 프로파일이 라이브러리만 게이트 |
| 🎨 **8-테마 스위처** | `light·light2·white·dark·dark2·blue·skyblue·sepia` — **무 JS** CSS-only 라디오 스위처 |
| 🧩 **시각 라이브러리** | CSS 뷰 위젯 `wg-` 20종 + SVG→HTML 템플릿 `vt-` 21종 + 본문 아이콘 `bi-` 32종 + soft-shape 36종 |
| 🛡️ **무 JS 원칙** | 출력에 외부/동작 JS 0. 상호작용은 전부 CSS-only(`:has()`·라디오·`details`). JSON-LD만 허용 |
| 🤖 **크로스-에이전트 결정론** | `AGENTS.md` 단일 진입점 + `modes/*.json` Registry로 어느 에이전트에서 돌려도 동일 결과 |
| ✅ **자기방어 게이트** | `validate_output.py`(구조·해시·계약) + `quality_contract_check.py`(붕어빵 차단) + 거버넌스 **199/199** |
| 🖨️ **PDF/PNG/WebP export** | `html-exporter`로 빌드타임 변환(테마별 캡처). 출력 HTML엔 JS 미삽입 |

---

## 📖 Overview

`adaptive-html-final`은 `html-for-beginners` → `adaptive-html-blog-writer` → `adaptive-html-learning-ultimate` 계열을 하나로 합친 **최종 통합본**입니다. 단순 HTML 변환기가 아니라, 입력을 분석해 **목적별 정보 구조**로 재구성하는 파이프라인을 실행합니다.

```text
┌──────────┐   ┌───────────────────────┐   ┌──────────────┐   ┌──────────┐   ┌──────────────┐
│ 입력 분석 │ ─▶│ 사실·해석·추론·확인필요 분류 │ ─▶│ 독자 수준 판단 │ ─▶│ 모드 선택 │ ─▶│ 레이아웃·프로파일 │
└──────────┘   └───────────────────────┘   └──────────────┘   └────┬─────┘   └──────┬───────┘
                                                                     │                │
                          ┌──────────────────────────────────────────┘                ▼
                          ▼                                              ┌─────────────────────────┐
              §0.6 결정표(단일 출처)                                       │ vt-/wg- 시각 라이브러리 + 8테마 │
              modes/NN-*.json Registry                                   │ 코어 CSS 인라인 + 해시 마커     │
                          │                                              └────────────┬────────────┘
                          ▼                                                           ▼
              검증 게이트(validate + quality + completion)  ─────────────▶  무 JS 단일 HTML
```

> [!TIP]
> 상세 규칙의 **단일 출처(SoT)** 는 스킬 본체입니다. 충돌 시 우선순위: `AGENTS.md` → `skills/adaptive-html-final/SKILL.md` → `references/*`.

---

## 🚀 빠른 시작

```bash
# 1) 저장소 클론 후 루트에서 로컬 미리보기
python3 -m http.server 8788
#   현행 18모드 참조 예제
#   → http://127.0.0.1:8788/skills/adaptive-html-final/examples/index.html

# 2) 현행 레퍼런스 검증 (마지막 줄 OK 여야 정상)
python3 skills/adaptive-html-final/scripts/validate_output.py \
  skills/adaptive-html-final/examples \
  --skill-dir skills/adaptive-html-final

# 3) 비주얼 인포그래픽 직접 렌더 (stdlib only, 오프라인)
python3 skills/adaptive-html-final/scripts/render_visual_svg.py brief.json output.svg
```

스킬로 콘텐츠를 생성할 때는 에이전트에게 이렇게 요청합니다:

```text
[입력 자료/URL/파일/주제]를 [목적/독자]용 [모드]로 만들어줘.
출력: 단일 HTML  ·  비주얼: profile=widget | diagram | auto  (미지정 시 auto)
반드시 포함: [목차·용어풀이·예시·리스크·FAQ·CTA 등]
주의: 최신 정보는 확인 필요 표시 · 외부 JS 금지 · 모바일 안전 표
```

---

## 📦 18개 모드

트리거가 겹치면 우선순위(`1=skill_audit … 17=checklist_playbook`)를 따릅니다. 결정표 단일 출처는 [`modes/NN-<mode>.json`](skills/adaptive-html-final/modes) Registry이며 `validate_output.py`가 직접 읽습니다.

| # | 모드 | 용도 (트리거 요약) | 레이아웃 | 1순위 vt-템플릿 |
|--:|---|---|---|---|
| 1 | 🔍 `skill_audit` | 스킬 분석·`SKILL.md` 개선·`.skill` 통합 | `.layout-audit` | `quality-gate` |
| 2 | 🪶 `platform_blog` | 티스토리·벨로그·네이버·워드프레스 플랫폼 변환 | `.layout-platform` | `card-grid` |
| 3 | 🔎 `seo_dashboard` | SEO·제목·메타·태그·검색 의도 | `.layout-seo` | `card-grid` |
| 4 | 🎓 `education_html` | 교육·강의·온보딩·실습·퀴즈 | `.layout-education` | `timeline` |
| 5 | 🐙 `github_analysis` | GitHub 저장소 실사(README·Issues·Releases·License) | `.layout-github` | `hero-map` |
| 6 | 🧰 `github_feature_usage` | GitHub 기능·사용법·도입 가이드(화면·스크린샷 중심) | `.layout-github-feature` | `hero-map` |
| 7 | ▶️ `youtube_analysis` | YouTube 영상 요약·자막·댓글·챕터·콘텐츠 갭 | `.layout-youtube` | `timeline` |
| 8 | 📕 `manual_analysis` | 매뉴얼·운영 절차서·트러블슈팅·제품 가이드 | `.layout-manual` | `hero-map` |
| 9 | 🧠 `expert_html` | 전문가 리포트·진단·아키텍처·리스크 | `.layout-expert` | `risk-matrix` |
| 10 | 📰 `article_html` | 공개 글·아티클·기사·GitHub Pages | `.layout-article` | `decision-tree` |
| 11 | ✍️ `blog_writer` | 블로그 글·포스팅·경험담·내 생각 | `.layout-blog` | `timeline` |
| 12 | 🌱 `beginner_html` | 초보자·쉽게·비유로·입문 | `.layout-beginner` | `concept-explainer` |
| 13 | 📚 `reference_html` | 레퍼런스·API 문서·치트시트·옵션표 | `.layout-reference` | `file-tour` |
| 14 | ⚖️ `comparison_html` | 비교·장단점·선택 기준 | `.layout-compare` | `comparison-cards` |
| 15 | 🧾 `case_study_html` | 사례 연구·회고·프로젝트 기록 | `.layout-case` | `incident-summary` |
| 16 | 🚀 `landing_brief_html` | 소개 페이지·랜딩·요약 페이지 | `.layout-landing` | `hero-map` |
| 17 | ✅ `checklist_playbook` | 체크리스트·운영 절차·플레이북 | `.layout-checklist` | `checklist-flow` |

> 전체 트리거·후순위 vt·권장 wg 매핑은 [`AGENTS.md` §3 결정표](AGENTS.md)와 [`SKILL.md` §0.6](skills/adaptive-html-final/SKILL.md) 참조.

---

## 🎚️ 비주얼 프로파일

스킬을 **기동할 때 비주얼 스타일을 고를 수 있습니다.** 코어(18모드 라우터·레이아웃·코어 CSS 5종)는 100% 공유하고, 프로파일이 *어느 라이브러리·삽입 단계·CSS 번들*을 쓸지만 게이트합니다. 세 프로파일 모두 **외부/동작 JS 0**.

<table>
<tr>
<td width="33%" align="center"><b>🧩 <code>widget</code></b></td>
<td width="33%" align="center"><b>📊 <code>diagram</code></b></td>
<td width="33%" align="center"><b>🔀 <code>auto</code> (기본)</b></td>
</tr>
<tr>
<td valign="top">CSS 뷰 위젯 <code>wg-01~20</code> — 탭·플로우·아코디언 등 <b>인터랙티브</b> 컴포넌트(CSS-only). 코어5 + <code>widgets.css</code>.</td>
<td valign="top">SVG→HTML 템플릿 <code>vt-</code> 21종 — 리스크 매트릭스·비교 카드·타임라인·soft workflow map 등 본문 삽입 <b>정적 도식</b>. 코어5 + <code>visual-html.css</code>.</td>
<td valign="top">둘 다(vt- 1순위 + wg- 보강). 현행 기본값이자 <b>회귀-0 기준선</b>. 코어5 + 두 라이브러리.</td>
</tr>
</table>

| 프로파일 | 라이브러리 (markup) | CSS 번들 |
|---|---|---|
| `widget` | CSS 뷰 위젯 `wg-` | 코어5 + `widgets.css` |
| `diagram` | SVG→HTML `vt-` | 코어5 + `visual-html.css` |
| `auto` (기본) | 둘 다 | 코어5 + `widgets.css` + `visual-html.css` |

```bash
adaptive-html-final  profile=widget     # CSS 위젯만
adaptive-html-final  profile=diagram    # SVG→HTML 도식만
adaptive-html-final  profile=auto       # 둘 다 (기본)
adaptive-html-final                     # 미지정 시 auto

# 검증기는 출력의 sources/profile.json 을 자동 인지(또는 --profile)해
# 교차 누수(diagram에 wg- / widget에 vt-)를 차단한다
python3 skills/adaptive-html-final/scripts/validate_output.py <output_dir> \
  --skill-dir skills/adaptive-html-final --profile diagram
```

> 🤖 **크로스-에이전트 결정론**: 인자가 명시되면 Claude Code·Codex·Gemini가 동일 결과를 낸다(정규화 `profile=` 우선, 무효 토큰은 `invalid_profile` 실패). 비대화형(AGENTS.md 경유)은 미지정 시 무조건 `auto`.

---

## 🎨 8-테마 시스템

상단 라디오 세그먼트 스위처(`name="ahf-theme"`)로 **무 JS** 즉시 전환. CSS-only `:has()` 토큰 오버라이드(`theme-dark.css`)로 동작합니다.

`🌕 light` · `⚪ light2` · `◽ white` · `🌑 dark` · `⬛ dark2` · `🔵 blue` · `🩵 skyblue` · `🟤 sepia`

> [!IMPORTANT]
> 8-테마 스위처는 `name="ahf-theme"` 라디오 8개 계약을 사용하며 legacy `#theme-toggle`은 금지입니다. 부분 테마 출력은 검증기 `theme_switcher_*` 게이트에서 실패합니다.

---

## 🖼️ 예제 (스킬 번들)

이 저장소가 소개하는 예제는 **스킬에 실제 포함된 현행 18모드 참조 예제**, 단 하나입니다 — [`skills/adaptive-html-final/examples/`](skills/adaptive-html-final/examples). v5.10.6 코어 자산으로 인라인되어 **8-테마·무 JS·검증 게이트(199/199)** 를 모두 통과한 자기완결 HTML이며, 각 모드의 정본 구조를 그대로 보여줍니다.

**▶ 예제 인덱스:** [`examples/index.html`](skills/adaptive-html-final/examples/index.html) · [라이브 열기](https://coreline-ai.github.io/skills-html-showcase/skills/adaptive-html-final/examples/index.html)

| # | 모드 | 예제 주제 | 열기 |
|--:|---|---|---|
| 01 | `beginner_html` | 패스키(Passkey)로 비밀번호 없이 로그인 | [source](skills/adaptive-html-final/examples/01_beginner_passkey_login.html) · [live](https://coreline-ai.github.io/skills-html-showcase/skills/adaptive-html-final/examples/01_beginner_passkey_login.html) |
| 02 | `expert_html` | 사내 LLM 게이트웨이 도입 타당성 진단 | [source](skills/adaptive-html-final/examples/02_expert_llm_gateway_report.html) · [live](https://coreline-ai.github.io/skills-html-showcase/skills/adaptive-html-final/examples/02_expert_llm_gateway_report.html) |
| 03 | `article_html` | 사이드 프로젝트가 이력서보다 강한 이유 | [source](skills/adaptive-html-final/examples/03_article_side_project_signal.html) · [live](https://coreline-ai.github.io/skills-html-showcase/skills/adaptive-html-final/examples/03_article_side_project_signal.html) |
| 04 | `education_html` | Git rebase 안전하게 쓰기 3일 워크숍 | [source](skills/adaptive-html-final/examples/04_education_git_rebase_workshop.html) · [live](https://coreline-ai.github.io/skills-html-showcase/skills/adaptive-html-final/examples/04_education_git_rebase_workshop.html) |
| 05 | `blog_writer` | 주 4일 딥워크 루틴 90일 실험기 | [source](skills/adaptive-html-final/examples/05_blog_deepwork_4day_retro.html) · [live](https://coreline-ai.github.io/skills-html-showcase/skills/adaptive-html-final/examples/05_blog_deepwork_4day_retro.html) |
| 06 | `seo_dashboard` | 프롬프트 엔지니어링 입문 글 SEO 설계 | [source](skills/adaptive-html-final/examples/06_seo_prompt_engineering_dashboard.html) · [live](https://coreline-ai.github.io/skills-html-showcase/skills/adaptive-html-final/examples/06_seo_prompt_engineering_dashboard.html) |
| 07 | `platform_blog` | 기술 회고 글을 4개 플랫폼으로 변환 | [source](skills/adaptive-html-final/examples/07_platform_tech_retro_adaptation.html) · [live](https://coreline-ai.github.io/skills-html-showcase/skills/adaptive-html-final/examples/07_platform_tech_retro_adaptation.html) |
| 08 | `skill_audit` | 사내 코드리뷰 봇 스킬 감사 리포트 | [source](skills/adaptive-html-final/examples/08_skill_audit_codereview_bot.html) · [live](https://coreline-ai.github.io/skills-html-showcase/skills/adaptive-html-final/examples/08_skill_audit_codereview_bot.html) |
| 09 | `reference_html` | 정규식(Regex) 실무 레퍼런스 | [source](skills/adaptive-html-final/examples/09_reference_regex.html) · [live](https://coreline-ai.github.io/skills-html-showcase/skills/adaptive-html-final/examples/09_reference_regex.html) |
| 10 | `comparison_html` | 메시지 큐 3종 비교 — Kafka·RabbitMQ·SQS | [source](skills/adaptive-html-final/examples/10_comparison_message_queue.html) · [live](https://coreline-ai.github.io/skills-html-showcase/skills/adaptive-html-final/examples/10_comparison_message_queue.html) |
| 11 | `case_study_html` | 검색 인덱스 장애 6시간 회고 | [source](skills/adaptive-html-final/examples/11_case_study_search_index_outage.html) · [live](https://coreline-ai.github.io/skills-html-showcase/skills/adaptive-html-final/examples/11_case_study_search_index_outage.html) |
| 12 | `landing_brief_html` | 온콜 피로도 관리 도구 PagerCalm 랜딩 | [source](skills/adaptive-html-final/examples/12_landing_pagercalm_brief.html) · [live](https://coreline-ai.github.io/skills-html-showcase/skills/adaptive-html-final/examples/12_landing_pagercalm_brief.html) |
| 13 | `checklist_playbook` | 데이터 마이그레이션 안전 플레이북 | [source](skills/adaptive-html-final/examples/13_checklist_data_migration.html) · [live](https://coreline-ai.github.io/skills-html-showcase/skills/adaptive-html-final/examples/13_checklist_data_migration.html) |
| 14 | `github_analysis` | GitHub 저장소 분석 리포트(fastapi-starter) | [source](skills/adaptive-html-final/examples/14_github_analysis_fastapi_starter.html) · [live](https://coreline-ai.github.io/skills-html-showcase/skills/adaptive-html-final/examples/14_github_analysis_fastapi_starter.html) |
| 15 | `youtube_analysis` | YouTube 분석 — 바이브코딩 영상 | [source](skills/adaptive-html-final/examples/15_youtube_vibecoding_gap.html) · [live](https://coreline-ai.github.io/skills-html-showcase/skills/adaptive-html-final/examples/15_youtube_vibecoding_gap.html) |
| 16 | `manual_analysis` | 제품 운영 매뉴얼 분석 | [source](skills/adaptive-html-final/examples/16_manual_product_runbook.html) · [live](https://coreline-ai.github.io/skills-html-showcase/skills/adaptive-html-final/examples/16_manual_product_runbook.html) |
| 17 | `github_feature_usage` | Coreline Auth 기능·사용 가이드 | [source](skills/adaptive-html-final/examples/17_github_feature_usage_coreline_auth.html) · [live](https://coreline-ai.github.io/skills-html-showcase/skills/adaptive-html-final/examples/17_github_feature_usage_coreline_auth.html) |

> 로컬 확인: 저장소 루트에서 `python3 -m http.server 8080` 후 `http://localhost:8080/skills/adaptive-html-final/examples/index.html`

---

<a id="v5105-demo17-rose-captures"></a>

## 🌹 v5.10.5 생성물 — demo17 로즈 캡쳐

오늘 pull된 `output/2026-06-15/demo17/` 17개 모드 결과물을 **로즈 테마(`dark2`)** 로 동일 규격 부분 캡쳐했습니다. 각 이미지를 클릭하면 해당 실제 HTML 결과물로 이동합니다.

- 캡쳐 규격: `1280×720` 부분 캡쳐 · viewport `1280×900` · theme radio `#ahf-dark2`
- 생성 스크립트: [`scripts/capture_demo17_rose.mjs`](scripts/capture_demo17_rose.mjs)
- 상위 목차: [`output/2026-06-15/demo17/index.html`](https://coreline-ai.github.io/skills-html-showcase/output/2026-06-15/demo17/index.html)
- 캡쳐 manifest: [`capture-manifest.json`](output/2026-06-15/demo17/readme-captures/rose/capture-manifest.json)

<table>
<tr>
<td width="33%" valign="top" align="center">
  <a href="https://coreline-ai.github.io/skills-html-showcase/output/2026-06-15/demo17/01_skill_audit_meeting-summary-bot-audit/index.html"><img src="output/2026-06-15/demo17/readme-captures/rose/01_skill_audit_meeting-summary-bot-audit.jpg" width="320" alt="01 스킬 감사 로즈 테마 부분 캡쳐"></a><br>
  <sub><a href="https://coreline-ai.github.io/skills-html-showcase/output/2026-06-15/demo17/01_skill_audit_meeting-summary-bot-audit/index.html"><b>01 · <code>skill_audit</code></b><br>회의록 자동 요약 봇 스킬 감사 리포트</a></sub>
</td>
<td width="33%" valign="top" align="center">
  <a href="https://coreline-ai.github.io/skills-html-showcase/output/2026-06-15/demo17/02_platform_blog_oss-release-platforms/index.html"><img src="output/2026-06-15/demo17/readme-captures/rose/02_platform_blog_oss-release-platforms.jpg" width="320" alt="02 플랫폼 블로그 로즈 테마 부분 캡쳐"></a><br>
  <sub><a href="https://coreline-ai.github.io/skills-html-showcase/output/2026-06-15/demo17/02_platform_blog_oss-release-platforms/index.html"><b>02 · <code>platform_blog</code></b><br>기술 회고 글을 4개 플랫폼으로 변환하기</a></sub>
</td>
<td width="33%" valign="top" align="center">
  <a href="https://coreline-ai.github.io/skills-html-showcase/output/2026-06-15/demo17/03_seo_dashboard_vector-db-seo/index.html"><img src="output/2026-06-15/demo17/readme-captures/rose/03_seo_dashboard_vector-db-seo.jpg" width="320" alt="03 SEO 대시보드 로즈 테마 부분 캡쳐"></a><br>
  <sub><a href="https://coreline-ai.github.io/skills-html-showcase/output/2026-06-15/demo17/03_seo_dashboard_vector-db-seo/index.html"><b>03 · <code>seo_dashboard</code></b><br>‘벡터 데이터베이스 입문’ 글 SEO 설계 대시보드</a></sub>
</td>
</tr>
<tr>
<td width="33%" valign="top" align="center">
  <a href="https://coreline-ai.github.io/skills-html-showcase/output/2026-06-15/demo17/04_education_html_k8s-intro-workshop/index.html"><img src="output/2026-06-15/demo17/readme-captures/rose/04_education_html_k8s-intro-workshop.jpg" width="320" alt="04 교육 모듈 로즈 테마 부분 캡쳐"></a><br>
  <sub><a href="https://coreline-ai.github.io/skills-html-showcase/output/2026-06-15/demo17/04_education_html_k8s-intro-workshop/index.html"><b>04 · <code>education_html</code></b><br>Kubernetes 입문 3일 워크숍</a></sub>
</td>
<td width="33%" valign="top" align="center">
  <a href="https://coreline-ai.github.io/skills-html-showcase/output/2026-06-15/demo17/05_github_analysis_sqlmodel-due-diligence/index.html"><img src="output/2026-06-15/demo17/readme-captures/rose/05_github_analysis_sqlmodel-due-diligence.jpg" width="320" alt="05 GitHub 분석 로즈 테마 부분 캡쳐"></a><br>
  <sub><a href="https://coreline-ai.github.io/skills-html-showcase/output/2026-06-15/demo17/05_github_analysis_sqlmodel-due-diligence/index.html"><b>05 · <code>github_analysis</code></b><br>tiangolo/sqlmodel 저장소 실사 리포트</a></sub>
</td>
<td width="33%" valign="top" align="center">
  <a href="https://coreline-ai.github.io/skills-html-showcase/output/2026-06-15/demo17/06_github_feature_usage_caddy-feature-usage/index.html"><img src="output/2026-06-15/demo17/readme-captures/rose/06_github_feature_usage_caddy-feature-usage.jpg" width="320" alt="06 GitHub 기능 가이드 로즈 테마 부분 캡쳐"></a><br>
  <sub><a href="https://coreline-ai.github.io/skills-html-showcase/output/2026-06-15/demo17/06_github_feature_usage_caddy-feature-usage/index.html"><b>06 · <code>github_feature_usage</code></b><br>Caddy 웹서버 기능·도입 가이드</a></sub>
</td>
</tr>
<tr>
<td width="33%" valign="top" align="center">
  <a href="https://coreline-ai.github.io/skills-html-showcase/output/2026-06-15/demo17/07_youtube_analysis_distsys-talk-analysis/index.html"><img src="output/2026-06-15/demo17/readme-captures/rose/07_youtube_analysis_distsys-talk-analysis.jpg" width="320" alt="07 YouTube 분석 로즈 테마 부분 캡쳐"></a><br>
  <sub><a href="https://coreline-ai.github.io/skills-html-showcase/output/2026-06-15/demo17/07_youtube_analysis_distsys-talk-analysis/index.html"><b>07 · <code>youtube_analysis</code></b><br>바이브코딩 영상은 실제로 팀 생산성을 올리는가</a></sub>
</td>
<td width="33%" valign="top" align="center">
  <a href="https://coreline-ai.github.io/skills-html-showcase/output/2026-06-15/demo17/08_manual_analysis_nginx-reverse-proxy-manual/index.html"><img src="output/2026-06-15/demo17/readme-captures/rose/08_manual_analysis_nginx-reverse-proxy-manual.jpg" width="320" alt="08 매뉴얼 분석 로즈 테마 부분 캡쳐"></a><br>
  <sub><a href="https://coreline-ai.github.io/skills-html-showcase/output/2026-06-15/demo17/08_manual_analysis_nginx-reverse-proxy-manual/index.html"><b>08 · <code>manual_analysis</code></b><br>Nginx 리버스 프록시 운영 매뉴얼</a></sub>
</td>
<td width="33%" valign="top" align="center">
  <a href="https://coreline-ai.github.io/skills-html-showcase/output/2026-06-15/demo17/09_expert_html_read-replica-feasibility/index.html"><img src="output/2026-06-15/demo17/readme-captures/rose/09_expert_html_read-replica-feasibility.jpg" width="320" alt="09 전문가 리포트 로즈 테마 부분 캡쳐"></a><br>
  <sub><a href="https://coreline-ai.github.io/skills-html-showcase/output/2026-06-15/demo17/09_expert_html_read-replica-feasibility/index.html"><b>09 · <code>expert_html</code></b><br>단일 DB → 읽기 복제본 도입 타당성 진단</a></sub>
</td>
</tr>
<tr>
<td width="33%" valign="top" align="center">
  <a href="https://coreline-ai.github.io/skills-html-showcase/output/2026-06-15/demo17/10_article_html_monorepo-argument/index.html"><img src="output/2026-06-15/demo17/readme-captures/rose/10_article_html_monorepo-argument.jpg" width="320" alt="10 아티클 로즈 테마 부분 캡쳐"></a><br>
  <sub><a href="https://coreline-ai.github.io/skills-html-showcase/output/2026-06-15/demo17/10_article_html_monorepo-argument/index.html"><b>10 · <code>article_html</code></b><br>왜 모노레포로 가는가 — 코드 공유의 무게중심</a></sub>
</td>
<td width="33%" valign="top" align="center">
  <a href="https://coreline-ai.github.io/skills-html-showcase/output/2026-06-15/demo17/11_blog_writer_side-project-12-retro/index.html"><img src="output/2026-06-15/demo17/readme-captures/rose/11_blog_writer_side-project-12-retro.jpg" width="320" alt="11 블로그 글 로즈 테마 부분 캡쳐"></a><br>
  <sub><a href="https://coreline-ai.github.io/skills-html-showcase/output/2026-06-15/demo17/11_blog_writer_side-project-12-retro/index.html"><b>11 · <code>blog_writer</code></b><br>사이드 프로젝트 12개 1년 회고: 무엇이 살아남았고 무엇이 사라졌나</a></sub>
</td>
<td width="33%" valign="top" align="center">
  <a href="https://coreline-ai.github.io/skills-html-showcase/output/2026-06-15/demo17/12_beginner_html_oauth-oidc-beginner/index.html"><img src="output/2026-06-15/demo17/readme-captures/rose/12_beginner_html_oauth-oidc-beginner.jpg" width="320" alt="12 초보자 학습 로즈 테마 부분 캡쳐"></a><br>
  <sub><a href="https://coreline-ai.github.io/skills-html-showcase/output/2026-06-15/demo17/12_beginner_html_oauth-oidc-beginner/index.html"><b>12 · <code>beginner_html</code></b><br>OAuth 2.0 / OIDC 처음 이해하기</a></sub>
</td>
</tr>
<tr>
<td width="33%" valign="top" align="center">
  <a href="https://coreline-ai.github.io/skills-html-showcase/output/2026-06-15/demo17/13_reference_html_http-status-reference/index.html"><img src="output/2026-06-15/demo17/readme-captures/rose/13_reference_html_http-status-reference.jpg" width="320" alt="13 레퍼런스 로즈 테마 부분 캡쳐"></a><br>
  <sub><a href="https://coreline-ai.github.io/skills-html-showcase/output/2026-06-15/demo17/13_reference_html_http-status-reference/index.html"><b>13 · <code>reference_html</code></b><br>HTTP 상태 코드 실무 레퍼런스</a></sub>
</td>
<td width="33%" valign="top" align="center">
  <a href="https://coreline-ai.github.io/skills-html-showcase/output/2026-06-15/demo17/14_comparison_html_rdbms-comparison/index.html"><img src="output/2026-06-15/demo17/readme-captures/rose/14_comparison_html_rdbms-comparison.jpg" width="320" alt="14 비교 매트릭스 로즈 테마 부분 캡쳐"></a><br>
  <sub><a href="https://coreline-ai.github.io/skills-html-showcase/output/2026-06-15/demo17/14_comparison_html_rdbms-comparison/index.html"><b>14 · <code>comparison_html</code></b><br>RDBMS 3종 선택 기준 — PostgreSQL vs MySQL vs SQLite</a></sub>
</td>
<td width="33%" valign="top" align="center">
  <a href="https://coreline-ai.github.io/skills-html-showcase/output/2026-06-15/demo17/15_case_study_html_double-billing-postmortem/index.html"><img src="output/2026-06-15/demo17/readme-captures/rose/15_case_study_html_double-billing-postmortem.jpg" width="320" alt="15 케이스 스터디 로즈 테마 부분 캡쳐"></a><br>
  <sub><a href="https://coreline-ai.github.io/skills-html-showcase/output/2026-06-15/demo17/15_case_study_html_double-billing-postmortem/index.html"><b>15 · <code>case_study_html</code></b><br>결제 이중 청구 장애 사후 분석</a></sub>
</td>
</tr>
<tr>
<td width="33%" valign="top" align="center">
  <a href="https://coreline-ai.github.io/skills-html-showcase/output/2026-06-15/demo17/16_landing_brief_html_oncallzero-landing/index.html"><img src="output/2026-06-15/demo17/readme-captures/rose/16_landing_brief_html_oncallzero-landing.jpg" width="320" alt="16 랜딩 브리프 로즈 테마 부분 캡쳐"></a><br>
  <sub><a href="https://coreline-ai.github.io/skills-html-showcase/output/2026-06-15/demo17/16_landing_brief_html_oncallzero-landing/index.html"><b>16 · <code>landing_brief_html</code></b><br>당번표·알림·에스컬레이션·회고를 한곳에서 자동화하는 팀 온콜 SaaS</a></sub>
</td>
<td width="33%" valign="top" align="center">
  <a href="https://coreline-ai.github.io/skills-html-showcase/output/2026-06-15/demo17/17_checklist_playbook_prod-index-playbook/index.html"><img src="output/2026-06-15/demo17/readme-captures/rose/17_checklist_playbook_prod-index-playbook.jpg" width="320" alt="17 체크리스트 로즈 테마 부분 캡쳐"></a><br>
  <sub><a href="https://coreline-ai.github.io/skills-html-showcase/output/2026-06-15/demo17/17_checklist_playbook_prod-index-playbook/index.html"><b>17 · <code>checklist_playbook</code></b><br>프로덕션 DB 인덱스 추가 안전 플레이북</a></sub>
</td>
<td width="33%"></td>
</tr>
</table>

<a id="v5103-codex-sepia-captures"></a>

## 🟤 v5.10.3 생성물 — codex-5.10.3 세피아 캡쳐

`http://localhost:8080/output/2026-06-13/codex-5.10.3/index.html`에 링크된 17개 모드 결과물을 **세피아 테마**로 동일 규격 부분 캡쳐했습니다. 각 이미지를 클릭하면 GitHub Pages에서 렌더링된 실제 HTML 결과물로 이동합니다.

- 버전 정보: `adaptive-html-final v5.10.3` · `Codex Output Index · 17 modes`
- 캡쳐 규격: `1280×720` 부분 캡쳐 · viewport `1280×900` · theme radio `#ahf-sepia`
- 생성 스크립트: [`scripts/capture_codex5103_sepia.mjs`](scripts/capture_codex5103_sepia.mjs)
- 기준 인덱스: [`output/2026-06-13/codex-5.10.3/index.html`](https://coreline-ai.github.io/skills-html-showcase/output/2026-06-13/codex-5.10.3/index.html)
- 캡쳐 manifest: [`capture-manifest.json`](output/2026-06-13/codex-5.10.3/readme-captures/sepia/capture-manifest.json)

<table>
<tr>
<td width="33%" valign="top" align="center">
  <a href="https://coreline-ai.github.io/skills-html-showcase/output/2026-06-13/codex-5.10.3/adaptive-html-final-single-01-skill-audit-20260613_193236/index.html"><img src="output/2026-06-13/codex-5.10.3/readme-captures/sepia/adaptive-html-final-single-01-skill-audit-20260613_193236.jpg" width="320" alt="01 skill_audit 세피아 테마 부분 캡쳐"></a><br>
  <sub><a href="https://coreline-ai.github.io/skills-html-showcase/output/2026-06-13/codex-5.10.3/adaptive-html-final-single-01-skill-audit-20260613_193236/index.html"><b>01 · <code>skill_audit</code></b><br>17모드 독립 생성 프롬프트 감사</a></sub>
</td>
<td width="33%" valign="top" align="center">
  <a href="https://coreline-ai.github.io/skills-html-showcase/output/2026-06-13/codex-5.10.3/adaptive-html-final-single-02-platform-blog-20260613_194351/index.html"><img src="output/2026-06-13/codex-5.10.3/readme-captures/sepia/adaptive-html-final-single-02-platform-blog-20260613_194351.jpg" width="320" alt="02 platform_blog 세피아 테마 부분 캡쳐"></a><br>
  <sub><a href="https://coreline-ai.github.io/skills-html-showcase/output/2026-06-13/codex-5.10.3/adaptive-html-final-single-02-platform-blog-20260613_194351/index.html"><b>02 · <code>platform_blog</code></b><br>AI 회의 액션 자동화 글의 플랫폼별 변환 전략</a></sub>
</td>
<td width="33%" valign="top" align="center">
  <a href="https://coreline-ai.github.io/skills-html-showcase/output/2026-06-13/codex-5.10.3/adaptive-html-final-single-03-seo-dashboard-20260613_194804/index.html"><img src="output/2026-06-13/codex-5.10.3/readme-captures/sepia/adaptive-html-final-single-03-seo-dashboard-20260613_194804.jpg" width="320" alt="03 seo_dashboard 세피아 테마 부분 캡쳐"></a><br>
  <sub><a href="https://coreline-ai.github.io/skills-html-showcase/output/2026-06-13/codex-5.10.3/adaptive-html-final-single-03-seo-dashboard-20260613_194804/index.html"><b>03 · <code>seo_dashboard</code></b><br>AI 회의록 자동화 글의 SEO 대시보드</a></sub>
</td>
</tr>
<tr>
<td width="33%" valign="top" align="center">
  <a href="https://coreline-ai.github.io/skills-html-showcase/output/2026-06-13/codex-5.10.3/adaptive-html-final-single-04-education-html-20260613_195414/index.html"><img src="output/2026-06-13/codex-5.10.3/readme-captures/sepia/adaptive-html-final-single-04-education-html-20260613_195414.jpg" width="320" alt="04 education_html 세피아 테마 부분 캡쳐"></a><br>
  <sub><a href="https://coreline-ai.github.io/skills-html-showcase/output/2026-06-13/codex-5.10.3/adaptive-html-final-single-04-education-html-20260613_195414/index.html"><b>04 · <code>education_html</code></b><br>Git Rebase 사고법 워크숍</a></sub>
</td>
<td width="33%" valign="top" align="center">
  <a href="https://coreline-ai.github.io/skills-html-showcase/output/2026-06-13/codex-5.10.3/adaptive-html-final-single-05-github-analysis-20260613_200411/index.html"><img src="output/2026-06-13/codex-5.10.3/readme-captures/sepia/adaptive-html-final-single-05-github-analysis-20260613_200411.jpg" width="320" alt="05 github_analysis 세피아 테마 부분 캡쳐"></a><br>
  <sub><a href="https://coreline-ai.github.io/skills-html-showcase/output/2026-06-13/codex-5.10.3/adaptive-html-final-single-05-github-analysis-20260613_200411/index.html"><b>05 · <code>github_analysis</code></b><br>coreline-ai/skills-html-showcase 실사 리포트</a></sub>
</td>
<td width="33%" valign="top" align="center">
  <a href="https://coreline-ai.github.io/skills-html-showcase/output/2026-06-13/codex-5.10.3/adaptive-html-final-single-06-github-feature-usage-20260613_201301/index.html"><img src="output/2026-06-13/codex-5.10.3/readme-captures/sepia/adaptive-html-final-single-06-github-feature-usage-20260613_201301.jpg" width="320" alt="06 github_feature_usage 세피아 테마 부분 캡쳐"></a><br>
  <sub><a href="https://coreline-ai.github.io/skills-html-showcase/output/2026-06-13/codex-5.10.3/adaptive-html-final-single-06-github-feature-usage-20260613_201301/index.html"><b>06 · <code>github_feature_usage</code></b><br>skills-html-showcase 기능·사용 가이드</a></sub>
</td>
</tr>
<tr>
<td width="33%" valign="top" align="center">
  <a href="https://coreline-ai.github.io/skills-html-showcase/output/2026-06-13/codex-5.10.3/adaptive-html-final-single-07-youtube-analysis-20260613_201813/index.html"><img src="output/2026-06-13/codex-5.10.3/readme-captures/sepia/adaptive-html-final-single-07-youtube-analysis-20260613_201813.jpg" width="320" alt="07 youtube_analysis 세피아 테마 부분 캡쳐"></a><br>
  <sub><a href="https://coreline-ai.github.io/skills-html-showcase/output/2026-06-13/codex-5.10.3/adaptive-html-final-single-07-youtube-analysis-20260613_201813/index.html"><b>07 · <code>youtube_analysis</code></b><br>AI 회의 액션 자동화 영상 분석</a></sub>
</td>
<td width="33%" valign="top" align="center">
  <a href="https://coreline-ai.github.io/skills-html-showcase/output/2026-06-13/codex-5.10.3/adaptive-html-final-single-08-manual-analysis-20260613_202323/index.html"><img src="output/2026-06-13/codex-5.10.3/readme-captures/sepia/adaptive-html-final-single-08-manual-analysis-20260613_202323.jpg" width="320" alt="08 manual_analysis 세피아 테마 부분 캡쳐"></a><br>
  <sub><a href="https://coreline-ai.github.io/skills-html-showcase/output/2026-06-13/codex-5.10.3/adaptive-html-final-single-08-manual-analysis-20260613_202323/index.html"><b>08 · <code>manual_analysis</code></b><br>결제 실패 급증 온콜 대응 매뉴얼</a></sub>
</td>
<td width="33%" valign="top" align="center">
  <a href="https://coreline-ai.github.io/skills-html-showcase/output/2026-06-13/codex-5.10.3/adaptive-html-final-single-09-expert-html-20260613_202824/index.html"><img src="output/2026-06-13/codex-5.10.3/readme-captures/sepia/adaptive-html-final-single-09-expert-html-20260613_202824.jpg" width="320" alt="09 expert_html 세피아 테마 부분 캡쳐"></a><br>
  <sub><a href="https://coreline-ai.github.io/skills-html-showcase/output/2026-06-13/codex-5.10.3/adaptive-html-final-single-09-expert-html-20260613_202824/index.html"><b>09 · <code>expert_html</code></b><br>AI 에이전트 릴리즈 게이트 아키텍처 진단</a></sub>
</td>
</tr>
<tr>
<td width="33%" valign="top" align="center">
  <a href="https://coreline-ai.github.io/skills-html-showcase/output/2026-06-13/codex-5.10.3/adaptive-html-final-single-10-article-html-20260613_203333/index.html"><img src="output/2026-06-13/codex-5.10.3/readme-captures/sepia/adaptive-html-final-single-10-article-html-20260613_203333.jpg" width="320" alt="10 article_html 세피아 테마 부분 캡쳐"></a><br>
  <sub><a href="https://coreline-ai.github.io/skills-html-showcase/output/2026-06-13/codex-5.10.3/adaptive-html-final-single-10-article-html-20260613_203333/index.html"><b>10 · <code>article_html</code></b><br>AI 시대의 개인 지식 금고가 팀의 의사결정 품질을 바꾸는 방식</a></sub>
</td>
<td width="33%" valign="top" align="center">
  <a href="https://coreline-ai.github.io/skills-html-showcase/output/2026-06-13/codex-5.10.3/adaptive-html-final-single-11-blog-writer-20260613_204015/index.html"><img src="output/2026-06-13/codex-5.10.3/readme-captures/sepia/adaptive-html-final-single-11-blog-writer-20260613_204015.jpg" width="320" alt="11 blog_writer 세피아 테마 부분 캡쳐"></a><br>
  <sub><a href="https://coreline-ai.github.io/skills-html-showcase/output/2026-06-13/codex-5.10.3/adaptive-html-final-single-11-blog-writer-20260613_204015/index.html"><b>11 · <code>blog_writer</code></b><br>아침 첫 45분을 화면 밖으로 옮겨본 7일</a></sub>
</td>
<td width="33%" valign="top" align="center">
  <a href="https://coreline-ai.github.io/skills-html-showcase/output/2026-06-13/codex-5.10.3/adaptive-html-final-single-12-beginner-html-20260613_204921/index.html"><img src="output/2026-06-13/codex-5.10.3/readme-captures/sepia/adaptive-html-final-single-12-beginner-html-20260613_204921.jpg" width="320" alt="12 beginner_html 세피아 테마 부분 캡쳐"></a><br>
  <sub><a href="https://coreline-ai.github.io/skills-html-showcase/output/2026-06-13/codex-5.10.3/adaptive-html-final-single-12-beginner-html-20260613_204921/index.html"><b>12 · <code>beginner_html</code></b><br>API가 뭐예요? 식당 주문으로 처음 이해하기</a></sub>
</td>
</tr>
<tr>
<td width="33%" valign="top" align="center">
  <a href="https://coreline-ai.github.io/skills-html-showcase/output/2026-06-13/codex-5.10.3/adaptive-html-final-single-13-reference-html-20260613_205733/index.html"><img src="output/2026-06-13/codex-5.10.3/readme-captures/sepia/adaptive-html-final-single-13-reference-html-20260613_205733.jpg" width="320" alt="13 reference_html 세피아 테마 부분 캡쳐"></a><br>
  <sub><a href="https://coreline-ai.github.io/skills-html-showcase/output/2026-06-13/codex-5.10.3/adaptive-html-final-single-13-reference-html-20260613_205733/index.html"><b>13 · <code>reference_html</code></b><br>HTTP Cache-Control 헤더 레퍼런스</a></sub>
</td>
<td width="33%" valign="top" align="center">
  <a href="https://coreline-ai.github.io/skills-html-showcase/output/2026-06-13/codex-5.10.3/adaptive-html-final-single-14-comparison-html-20260613_210355/index.html"><img src="output/2026-06-13/codex-5.10.3/readme-captures/sepia/adaptive-html-final-single-14-comparison-html-20260613_210355.jpg" width="320" alt="14 comparison_html 세피아 테마 부분 캡쳐"></a><br>
  <sub><a href="https://coreline-ai.github.io/skills-html-showcase/output/2026-06-13/codex-5.10.3/adaptive-html-final-single-14-comparison-html-20260613_210355/index.html"><b>14 · <code>comparison_html</code></b><br>SQLite vs DuckDB vs PostgreSQL 선택 매트릭스</a></sub>
</td>
<td width="33%" valign="top" align="center">
  <a href="https://coreline-ai.github.io/skills-html-showcase/output/2026-06-13/codex-5.10.3/adaptive-html-final-single-15-case-study-html-20260613_211157/index.html"><img src="output/2026-06-13/codex-5.10.3/readme-captures/sepia/adaptive-html-final-single-15-case-study-html-20260613_211157.jpg" width="320" alt="15 case_study_html 세피아 테마 부분 캡쳐"></a><br>
  <sub><a href="https://coreline-ai.github.io/skills-html-showcase/output/2026-06-13/codex-5.10.3/adaptive-html-final-single-15-case-study-html-20260613_211157/index.html"><b>15 · <code>case_study_html</code></b><br>결제 웹훅 중복 처리 장애 회고</a></sub>
</td>
</tr>
<tr>
<td width="33%" valign="top" align="center">
  <a href="https://coreline-ai.github.io/skills-html-showcase/output/2026-06-13/codex-5.10.3/adaptive-html-final-single-16-landing-brief-html-20260613_211157/index.html"><img src="output/2026-06-13/codex-5.10.3/readme-captures/sepia/adaptive-html-final-single-16-landing-brief-html-20260613_211157.jpg" width="320" alt="16 landing_brief_html 세피아 테마 부분 캡쳐"></a><br>
  <sub><a href="https://coreline-ai.github.io/skills-html-showcase/output/2026-06-13/codex-5.10.3/adaptive-html-final-single-16-landing-brief-html-20260613_211157/index.html"><b>16 · <code>landing_brief_html</code></b><br>AI 회의 액션 자동화 랜딩 브리프</a></sub>
</td>
<td width="33%" valign="top" align="center">
  <a href="https://coreline-ai.github.io/skills-html-showcase/output/2026-06-13/codex-5.10.3/adaptive-html-final-single-17-checklist-playbook-20260613_211157/index.html"><img src="output/2026-06-13/codex-5.10.3/readme-captures/sepia/adaptive-html-final-single-17-checklist-playbook-20260613_211157.jpg" width="320" alt="17 checklist_playbook 세피아 테마 부분 캡쳐"></a><br>
  <sub><a href="https://coreline-ai.github.io/skills-html-showcase/output/2026-06-13/codex-5.10.3/adaptive-html-final-single-17-checklist-playbook-20260613_211157/index.html"><b>17 · <code>checklist_playbook</code></b><br>온콜 장애 초동 대응 체크리스트 플레이북</a></sub>
</td>
<td width="33%"></td>
</tr>
</table>

---

## 🏗️ 아키텍처 & 디자인 시스템

### 🎨 디자인 시스템 (CSS 레이어)

```text
[ 코어 해시 5종 — 합본 SHA-256 마커 ]
theme.css              색/폰트/폭 토큰(:root) · skip · focus-visible · reduced-motion
components.css         term · analogy · danger · good · hero-analogy · try · tbl · faq · cta-box ...
visual-components.css  figure.visual-figure (8000×6000 SVG 삽입 셸)
layouts.css            18개 모드별 그리드/구조 (github 실사·기능가이드·youtube·manual 포함)
print.css              인쇄 대응(print-color-adjust · break-inside · reading-progress 숨김)

[ 조건부 / 후행 인라인 — 해시 비대상 ]
widgets.css            CSS 뷰 위젯 wg-01~20 (탭·플로우·아코디언, 무 JS)   ← widget/auto 프로파일
visual-html.css        SVG→HTML 템플릿 vt- 21종 (본문 삽입 도식)          ← diagram/auto 프로파일
body-icons.css         본문 아이콘 bi- 32종                              ← 프로파일 무관
editorial-patterns.css chronology/source/insight/a11y 등 본문 패턴 8종    ← 프로파일 무관
shape-visuals.css      soft-shape 36종                                  ← 프로파일 무관
workflow-visuals.css   workflow 도판 10종                               ← 프로파일 무관
theme-dark.css         CSS-only 8-테마 토큰 오버라이드 + 라디오 스위처      ← print 뒤 항상 인라인
```

> 코어 해시는 **5종**(theme·components·visual-components·layouts·print)의 합본 SHA-256(`adaptive-html-final-core-css-sha256` 마커)이며, 출력은 이 5종을 **byte-verbatim 인라인**해야 합니다.

### 📊 비주얼 템플릿 시스템 (v4.2+)

목적형 정보는 외부 사진 검색이 아니라 **8000×6000 SVG 인포그래픽**을 기본값으로 직접 생성합니다.

| 구성 | 내용 |
|---|---|
| `visual-templates/*.svg.tpl` | hero-map · card-grid · decision-tree · quality-gate · timeline · matrix · checklist-flow (7종) |
| `scripts/render_visual_svg.py` | visual brief(JSON) → 8000×6000 SVG 렌더러 (**stdlib only**, 오프라인 동작) |
| `schemas/visual-brief.schema.json` | 시각 템플릿 입력 스키마 |
| 출력 | risk-heatmap · sankey · treemap · user-journey 등 20+종 (8000×6000 캔버스) |

---

## 📁 프로젝트 구조

```text
skills-html-showcase/
├── skills/adaptive-html-final/        # 통합 스킬 + .skill 패키지
│   ├── SKILL.md                       # 라우터 · 워크플로우 · 품질 게이트 (단일 출처)
│   ├── manifest.json                  # name/version/modes/layouts/profiles/theme_system (v5.10.6 · 18모드)
│   ├── assets/                        # base.html · CSS 12종 · 위젯/도식/패턴/테마 자산 · 18개 레이아웃 골격
│   ├── modes/         (17)            # 모드 결정표 Registry (validator가 직접 읽는 실행 정본)
│   ├── references/    (19)            # 모드/레이아웃/글쓰기/SEO/감사/GitHub·YouTube·Manual·기능가이드 규칙
│   ├── recipes/       (17)            # 모드별 대표 프롬프트
│   ├── schemas/       (3)             # blog-meta · quality-report · visual-brief
│   ├── scripts/       (7)             # validate_output · quality_contract_check · completion_check ·
│   │                                  #   render_visual_svg · mode_registry · check_mode_registry_sync · body_icon_markup
│   ├── tests/                         # 거버넌스 게이트 (199/199) + 레이아웃/접근성 체크리스트
│   ├── visual-templates/ (7)          # 8000×6000 SVG 템플릿
│   ├── galleries/                     # body-icon / soft-shape 카탈로그
│   ├── examples/                      # v5.10.6 현행 18모드 참조 예제 + index + sources 스냅샷
│   └── template-catalog/             # final_20260604 기반 템플릿 HTML 정본 4종
├── skills/html-exporter/             # 재사용 export 스킬 (Playwright → PDF/PNG/WebP)
├── output/                            # 날짜별 산출물 아카이브 (독립 결과물 — 스킬 입력 아님)
│   └── YYYY-MM-DD/<산출물>/            # output/README.md 의 날짜 인덱스 참조
├── docs/
│   ├── screenshots/                   # 본 README용 쇼케이스 썸네일
│   ├── adaptive-html-final-template-authoring-protocol.md  # v5.10.6 작성 프로토콜
│   └── archive/                       # v4~v5.0 시점 고정 리뷰/분석/계획 기록 (SUPERSEDED)
├── dev-plan/                          # 단계별 구현 계획 + release-approval 기록
├── AGENTS.md                          # 크로스-에이전트 결정론 진입점
├── Guide.md                           # 사용 가이드
└── README.md                          # (루트는 README · AGENTS · Guide 3종 유지)
```

---

## ✅ 품질 게이트 & 결정론

모든 산출물이 통과해야 하는 최소 조건입니다(`validate_output.py` + `quality_contract_check.py` + `completion_check.py`).

- [x] 요청 목적과 선택 모드 일치 + 모드별 필수 블록 존재
- [x] `lang="ko"` · viewport · `<title>` · meta description · 헤더 generated-row/lens-strip
- [x] `h1` 정확히 1개 · 직접 섹션 h2 순서 `body-icon → (num/no) → title`
- [x] `#main` skip link target · `:focus-visible` · `prefers-reduced-motion`
- [x] 모바일 1컬럼 전환 · 표는 `.tbl`/`.table-scroll` 래퍼(가로 스크롤)
- [x] 8-테마 스위처는 `name="ahf-theme"` 라디오 8개 계약, legacy `#theme-toggle` 없음
- [x] **외부/동작 JS 0** · 코어 CSS byte-verbatim 인라인 + 해시 마커 일치
- [x] 모드별 1순위 vt / 권장 wg 사용(`mode_template_contract_gate`) · 붕어빵·얇은 문서 차단
- [x] 비주얼: 8000×6000 캔버스 · `figure`+`figcaption` · 의미 있는 `alt` · 캔버스 잘림 없음

### 검증 현황

| 검증 항목 | 결과 |
|---|---|
| 거버넌스 게이트 | `test_governance_gates.py` **199 / 199 통과** |
| 외부 동작 JS | **0건** |
| 코어 CSS 해시 | 5종 합본 SHA-256 byte-verbatim 인라인 일치 |
| skip link ↔ `#main` · 단일 `h1` | 17 / 17 레이아웃 계약 |
| manifest ↔ 결정표 ↔ Registry | 6자 정합(`check_mode_registry_sync.py`) |

> [!NOTE]
> 🟢 **게이트 현황(v5.10.6)**: 거버넌스 `test_governance_gates.py` **199 / 199 통과**. 검증기 `validate_output.py`는 18모드 계약(시각 정본·모드별 vt/wg·toc-map·무 JS·코어 해시·manifest/결정표/참조문서 자기정합·버전 표면·`.skill` byte-match)을 정적으로 강제합니다. 현행 18모드 레퍼런스는 `skills/adaptive-html-final/examples/`입니다.

```bash
# 현행 18모드 레퍼런스 검증 (저장소 루트에서)
python3 skills/adaptive-html-final/scripts/validate_output.py \
  skills/adaptive-html-final/examples \
  --skill-dir skills/adaptive-html-final          # → 마지막 줄 OK

python3 skills/adaptive-html-final/tests/test_governance_gates.py   # → 199/199 checks passed
python3 skills/adaptive-html-final/scripts/quality_contract_check.py skills/adaptive-html-final/examples
python3 skills/adaptive-html-final/scripts/completion_check.py     skills/adaptive-html-final/examples
```

> 🤖 **크로스-에이전트 결정론**: 모드·레이아웃·템플릿·위젯 선택은 추측하지 않고 [`AGENTS.md`](AGENTS.md) §3 결정표 + `modes/*.json` Registry를 그대로 따릅니다. `check_mode_registry_sync.py`가 결정표·Registry·`MODE_TEMPLATE_CONTRACTS`·`SKILL §0.6`·`widget-system`·`manifest` 6자 정합을 강제합니다.
>
> 참고: `output/`은 날짜별 **독립 테스트 결과물**이며 스킬 입력/정본이 아닙니다. v4~v5.0 시점 산출물은 코어 CSS 진화로 해시가 드리프트하면 현재 게이트에서 `FAILED`가 날 수 있습니다(시점 고정). 최신 기준선은 항상 `skills/adaptive-html-final/examples/`입니다.

---

## ⚡ 사용법

### 1) 스킬로 콘텐츠 생성 요청

```text
[입력 자료/URL/파일/주제]를 [목적/독자]용 [모드]로 만들어줘.
출력은 [단일 HTML / Markdown+HTML / 플랫폼별 원고]로 해줘.
비주얼: profile=widget | diagram | auto  (미지정 시 auto)
반드시 포함: [목차, 용어 풀이, 예시, 리스크, FAQ, CTA 등]
주의: [최신 정보는 확인 필요 표시, 외부 JS 금지, 모바일 안전 표]
```

### 2) 비주얼 인포그래픽 직접 렌더

```bash
# visual brief(JSON) → 8000×6000 SVG (stdlib only, 오프라인 동작)
python3 skills/adaptive-html-final/scripts/render_visual_svg.py brief.json output.svg
```

### 3) 쇼케이스 로컬에서 보기

```bash
python3 -m http.server 8080
# 스킬 번들 18모드 참조 예제 (현행 v5.10.6)
# → http://localhost:8080/skills/adaptive-html-final/examples/index.html
```

### 4) HTML → PDF/PNG/WebP export

완성된 `output/<dir>` HTML은 빌드 타임 도구로 PDF·테마별 PNG·WebP로 변환할 수 있습니다. 출력 HTML에는 JS를 삽입하지 않고, export 전후 HTML SHA와 `validate_output.py --json` 이슈 불변성을 manifest에 기록합니다.

```bash
npm install                                                    # 최초 1회
npm run export:output -- output/<생성한_산출물_디렉터리> --clean
```

| 항목 | v1 계약 |
|---|---|
| 엔진 | Playwright Chromium (`:has()` 테마·대형 SVG 충실도 유지) |
| WebP | `sharp` optional dependency. 없으면 webp skip, `--require-webp`면 실패 |
| 테마 | DOM radio `name="ahf-theme"`에 존재하는 테마만 캡처(`light,light2,white,dark,dark2,blue,skyblue,sepia`) |
| 산출물 | `<output_dir>/exports/{pdf,png,webp}/` + `exports/export-manifest.json` (`.gitignore`) |

> 재사용 스킬: [`skills/html-exporter`](skills/html-exporter/) — 다른 프로젝트에서도 동일한 export 절차를 적용할 때 사용합니다.

---

## 🗂️ 버전 히스토리

**현행 `v5.10.6`** — 시각 결함 하드닝(G1~G8). validate/quality/completion은 통과하지만 화면에 남던 누적 결함을 본체로 닫았다: 표 상태코드 줄바꿈(`.status-pill` 정본), `.try` 중첩 흰 카드 링크 저대비(`--link-on-dark`→`--accent-2`, 8테마 min 6.09:1), `source-preserve` 좌측 gutter(`.source-body-inner`), `mini-card` 첫 태그 리듬, `core-insight` 내부 제목 margin reset + red gradient 보존, `prefers-contrast` 단서(A5). 정적으로 못 잡던 결함은 검출 게이트로 승격 — G2 diagram 노드 박스 overlap·G3 inner-card 링크 대비 render-audit(`scripts/micro_layout_audit.mjs`) + G4~G8 정적 가드 + TOC/h2 anchor DOM 가드. 코어 CSS 직접 수정 → **코어 해시 `a73eb204`→`a64604d0`**·examples 18종 재인라인·.skill 재패키징. 거버넌스 **162→199/199**.

<details>
<summary><b>전체 버전 진화 펼치기 (v4.0 → v5.10.6)</b></summary>

<br>

| 버전 | 핵심 |
|---|---|
| `v4.0.0` | ultimate(13모드 라우터) + blog-writer 통합 · skip link 버그 수정 |
| `v4.1.0` | 7-전문가 분석 P0~P2 자동 패치 — 모드 ID 통일, recipes 13/13, 스키마 보강, 디자인 토큰 정리 |
| `v4.2.x` | **Visual Template System** — 8000×6000 SVG 인포그래픽 7종 + stdlib 렌더러 |
| `v4.3.3` | 13모드 전수 캡쳐 감사 기반 **반응형 폴리시** + 정적 게이트 |
| `v4.4.0` | **뷰 위젯 시스템** 편입 — CSS 뷰 위젯 `wg-01~20`(무 JS) + 위젯 정적 게이트 |
| `v4.5.0` | **SVG→HTML 템플릿** 편입(`vt-`) + 루트 `AGENTS.md` 결정론 진입점 + **비주얼 프로파일** 도입 |
| `v5.0.0` | 코어 프리미티브 업그레이드 + 토큰 전용 다크 테마 |
| `v5.1.0` | proper-black 다크 보정 — vt/wg 표면 색·CTA·회색 리터럴 토큰화 |
| `v5.2.0~5.2.3` | **CSS-only 테마 시스템** + 라디오 스위처 · 13-topics 전문가 보강 · 가독성 승격(조건부 자산, 코어 해시 불변) |
| `v5.3.0` | **GitHub Analysis 14번째 모드** |
| `v5.7.0` | **YouTube / Manual Analysis 15·16번째 모드** + 깊이 계약 |
| `v5.9.0~5.9.2` | 시각 정본 게이트 3종 + 카탈로그 reverse-sync · 외부 세리프 폰트 금지·toc-map 회귀 방지 |
| `v5.10.0` | **GitHub Feature-Usage 17번째 모드** + 스크린샷 갤러리·계약 게이트 |
| `v5.10.1` | 예제 정본화(부록 안티패턴 제거) + 자기정합 게이트 3종 |
| `v5.10.2` | `layout-github-feature` 단락 폭 회귀 수정 + R5 게이트 정밀화 |
| `v5.10.3` | 다크 대비·인쇄 가독·전 모드 page-wide 폭 정본 + 자기방어 게이트 6종 + 버전 표면/.skill byte-match + render-audit 완료 증빙 + 승인 없는 버전 bump 차단 |
| `v5.10.4` | **마이크로 레이아웃 정본 계약(M1·M4·M7·M10)** + 작성 프로토콜(M2·M3·M6·M9 정본 컴포넌트 규칙). 코어 해시 갱신·examples 재인라인·.skill 재패키징·17모드 benchmark/micro-layout completion 게이트. 거버넌스 162/162 |
| `v5.10.5` | **접근성·스코프 하드닝** — forced-colors 상태 단서(테마바·wg 선택/체크) + `.score`→`.tuner .score` 스코프 + vt 장식 글리프 `aria-hidden` + eval-rubric↔quality-report 스키마 연결. 조건부 자산만 변경·코어 해시 불변·examples 18종 재인라인. 거버넌스 162/162 |
| `v5.10.6` | **시각 결함 하드닝(G1~G8)** — 표 상태코드 nowrap(`.status-pill`)·`.try` 흰 카드 링크 대비(`--accent-2`)·`source-preserve` gutter·`mini-card` 리듬·`core-insight` reset·`prefers-contrast`(A5). 검출 게이트 신설(G2 노드 overlap·G3 링크 대비 render-audit + G4~G8 정적 + TOC/h2 DOM). 코어 해시 `a73eb204`→`a64604d0`·examples 18종 재인라인·.skill 재패키징. 거버넌스 162→199/199 |

</details>

> 전체 변경 이력: [`skills/adaptive-html-final/CHANGELOG.md`](skills/adaptive-html-final/CHANGELOG.md)

---

## 📚 문서

| 문서 | 내용 |
|---|---|
| [`AGENTS.md`](AGENTS.md) | 크로스-에이전트 결정론 진입점 — 모드 라우팅 결정표 · 버전 릴리스 정합 체크리스트 |
| [`skills/adaptive-html-final/SKILL.md`](skills/adaptive-html-final/SKILL.md) | 스킬 본체 — §0.6 결정표 · 워크플로우 · 품질 게이트 |
| [`Guide.md`](Guide.md) | 사용 가이드 |
| [`docs/adaptive-html-final-template-authoring-protocol.md`](docs/adaptive-html-final-template-authoring-protocol.md) | 공식 템플릿 기반 작성 프로토콜 (M1~M10 실패→정답) |
| [`references/`](skills/adaptive-html-final/references) | 모드·레이아웃·글쓰기·SEO·감사·GitHub/YouTube/Manual 규칙 19종 |
| [`CHANGELOG.md`](skills/adaptive-html-final/CHANGELOG.md) | 전체 변경 이력 |

---

## 📜 License

별도 라이선스가 지정되지 않았습니다. 사용 전 저장소 소유자(`coreline-ai`)에게 확인하세요.

<div align="center">
<sub>생성 도구: <code>adaptive-html-final</code> v5.10.6 · 18-mode · 8-theme · 3-profile editorial HTML engine · 무 JS · governance 199/199</sub>
</div>
