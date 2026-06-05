<div align="center">

<img width="2752" height="1536" alt="뚝딱! 마법의 HTML 변신 도구" src="https://github.com/user-attachments/assets/73915e46-1a31-49b1-9023-dbd724c90534" />

<img width="0" height="0" alt="완벽한 HTML 변환 파이프라인 안내" src="https://github.com/user-attachments/assets/aad48544-f667-438a-a28b-5c55f38a1909" />

# 🎨 Adaptive HTML Final

[![skill](https://img.shields.io/badge/skill-adaptive--html--final-e63946)](skills/adaptive-html-final)
[![version](https://img.shields.io/badge/version-5.2.0-3178C6)](skills/adaptive-html-final/CHANGELOG.md)
[![modes](https://img.shields.io/badge/modes-13-2a7d5a)](#-13개-모드)
[![profiles](https://img.shields.io/badge/profiles-widget·diagram·auto-8a5e10)](#️-비주얼-프로파일)
[![themes](https://img.shields.io/badge/themes-light·white·dark-111827)](#-최근-업데이트)
[![libraries](https://img.shields.io/badge/view%20widgets-20-e63946)](#️-비주얼-프로파일) [![svg→html](https://img.shields.io/badge/svg→html%20templates-21-d99a38)](#️-비주얼-프로파일)
[![lang](https://img.shields.io/badge/lang-한국어-0b7285)](#)
[![external JS](https://img.shields.io/badge/external%20JS-0-success)](#-품질-게이트)
[![cross-agent](https://img.shields.io/badge/cross--agent-AGENTS.md-6e40c9)](AGENTS.md)
[![python](https://img.shields.io/badge/SVG%20render-stdlib%20only-3776AB?logo=python&logoColor=white)](skills/adaptive-html-final/scripts/render_visual_svg.py)

**입력 자료를 13개 모드로 라우팅해 전문가급 한국어 HTML 콘텐츠를 만드는 단일 통합 스킬 — 3-테마(라이트·화이트·다크)와 비주얼 프로파일(위젯형·도식형·자동) 선택**

URL·PDF·텍스트·메모·기술 문서·블로그 초안·`SKILL.md`/`.skill`을 받아 학습자료, 전문가 리포트, 아티클, 교육 모듈, 블로그 원고, SEO 대시보드, 플랫폼 변환, 스킬 감사, 레퍼런스, 비교, 케이스 스터디, 랜딩, 체크리스트로 변환합니다.

[Overview](#-overview) · [최근 업데이트](#-최근-업데이트) · [모드](#-13개-모드) · [비주얼 프로파일](#️-비주얼-프로파일) · [쇼케이스 갤러리](#️-쇼케이스-갤러리) · [스킬 구조](#️-스킬-구조) · [사용법](#-사용법)

</div>

---

## 📖 Overview

`adaptive-html-final`은 `html-for-beginners` → `adaptive-html-blog-writer` → `adaptive-html-learning-ultimate` 계열을 하나로 합친 **최종 통합본**입니다. 단순 HTML 변환기가 아니라, 입력을 분석해 **목적별 정보 구조**로 재구성하는 파이프라인을 실행합니다.

```text
┌──────────┐   ┌─────────────────────┐   ┌────────────┐   ┌──────────┐
│ 입력 분석 │ ─▶│ 사실/해석/추론/확인필요 │ ─▶│ 독자 수준 판단 │ ─▶│ 모드 선택 │
└──────────┘   └─────────────────────┘   └────────────┘   └────┬─────┘
                                                                │
   ┌────────────┐   ┌──────────────────┐   ┌────────────┐   ┌──▼───────┐
   │ 파일/링크 제시 │◀─ │ 품질 게이트 검수    │◀─ │ editorial 렌더 │◀─ │ 레이아웃 선택 │
   └────────────┘   └──────────────────┘   └────────────┘   └──────────┘
```

| 원칙 | 내용 |
|---|---|
| 사실성 | 확인되지 않은 최신 정보·수치·가격·날짜는 단정하지 않고 `확인 필요`로 표시 |
| 무 JS | 외부/동작 JavaScript 미사용 (JSON-LD 메타데이터만 허용) |
| 단일 HTML | 코어 CSS(theme·components·visual-components·layouts·print)와 조건부 자산을 inline으로 포함한 자기완결 HTML + 합본 해시 마커 |
| **3-테마** | `#ahf-light` / `#ahf-white` / `#ahf-dark` 라디오 세그먼트 스위처 기반 CSS-only 테마. 기본 라이트, 완전 화이트, proper-black 다크 |
| **비주얼 프로파일** | 기동 시 `widget`(인터랙티브 위젯) / `diagram`(SVG→HTML 도식) / `auto`(둘 다, 기본) 선택 — 코어 공유, 프로파일이 라이브러리만 게이트 |
| **두 위젯 라이브러리** | CSS 뷰 위젯 `wg-01~20`(인터랙션) + SVG→HTML 템플릿 `vt-` 21종(본문 삽입 도식), 둘 다 무 JS·네임스페이스 격리 |
| 크로스-에이전트 결정론 | 루트 [`AGENTS.md`](AGENTS.md)가 결정론 진입점 — Claude Code·Codex·Gemini가 동일 인자로 동일 출력. 정적 게이트 `validate_output.py --profile` |
| 접근성 | `lang="ko"` · skip link(`#main`) · 단일 `h1` · `:focus-visible` · `prefers-reduced-motion` · AA 대비 |
| editorial DNA | 오프화이트 배경, Pretendard + Noto Serif KR, 의미 박스, h2 빨간 원번호 |

---

## 🆕 최근 업데이트

`adaptive-html-final`은 2026-06-05 기준 **v5.2.0**으로 갱신되었습니다. 핵심은 "기존 13모드/3프로파일 구조는 유지하면서, 실제 브라우저 캡처에서 발견된 가독성·레이아웃 회귀를 스킬 자산에 직접 반영"한 것입니다.

| 영역 | 변경 내용 |
|---|---|
| 3-테마 시스템 | `assets/theme-dark.css`에 라이트(크림 기본)·화이트(순백)·다크(proper-black) 토큰을 통합하고, `#theme-toggle` 체크박스를 `name="ahf-theme"` 라디오 3-세그먼트로 교체. 전부 `:has()` 기반 무 JS |
| 모바일 테마바 | 모바일에서는 `.ahf-themebar`를 문서 흐름 안의 static 컨트롤로 전환해 표·체크리스트·메타 칩을 가리지 않도록 보정 |
| CSS 무결성 | 출력 폴더의 `sources/assets/*.css`, `sources/css-integrity.json`, `sources/adaptive-html-final-manifest.json`을 현재 스킬 자산과 동기화. 코어 해시는 `78f7c0f836948338a066ddc3392ecddecdba4f437e6d19ec05059c168b6ca19c` |
| 검증기 강화 | `scripts/validate_output.py`가 source manifest 내용 불일치, stale CSS snapshot, legacy `#theme-toggle`, 외부/동작 JS, table caption, h1/#main 구조를 더 엄격히 검사 |
| 실제 화면 검증 | Playwright 기준 390px 모바일 / 1440px 데스크톱, 라이트·화이트·다크 조합으로 주요 페이지를 재촬영하고 가로 넘침·텍스트 대비·테마 컨트롤 겹침을 확인 |

### 이번 회귀 수정 내역

| 대상 | 수정 |
|---|---|
| `wg-01` three-code-approaches | 카드 가로 넘침과 코드 줄 잘림을 막도록 코드 블록 wrapping/overflow 규칙 보강 |
| `wg-12` postmortem timeline | `SEV-2` 칩 대비를 `--link-on-dark` 배경 + dark text로 보정, 표 body row header가 전역 `th` 다크 스타일을 먹어 검은 칸으로 튀는 문제 수정 |
| `wg-16` implementation-plan | 출시 계획 표 row header 텍스트가 안 보이던 문제를 `background:var(--card)`/테마 추종 스타일로 보정 |
| `vt-02` decision-tree | 3카드 + 2화살표 구조를 5컬럼으로 고정해 comparison 모드의 의사결정 트리가 깨지던 문제 수정 |
| `vt-21` soft-workflow-map | 다크모드에서 카드 제목·본문 대비가 낮아지는 케이스를 보정 |
| `.try` final action | comparison/case 모드의 마지막 실행 섹션이 라이트/화이트에서도 검은 패널로 보이던 문제를 테마 추종 카드로 조정 |
| `.table-scroll` | 모바일 표 폭이 문서 전체를 밀어내지 않도록 `max-width:100%`와 수평 스크롤 래퍼 규칙 추가 |

### 최신 로컬 산출물

이번 점검의 최신 13개 주제 산출물은 [`output/adaptive-html-final-13-topics-20260605_083433/`](output/adaptive-html-final-13-topics-20260605_083433/)에 있습니다.

| 항목 | 값 |
|---|---|
| 프로파일 | `auto` |
| 스킬 버전 | `5.2.0` |
| HTML 수 | `index.html` + 13개 페이지 |
| 검증 | `validate_output.py`: `OK`, `test_governance_gates.py`: `24/24 checks passed` |
| 화면 감사 | `_visual-audit/fix-10-11/`, `_visual-audit/fix-wg12/`에 브라우저 캡처 저장 |

```bash
# 최신 산출물 검증
python3 skills/adaptive-html-final/scripts/validate_output.py \
  output/adaptive-html-final-13-topics-20260605_083433 \
  --skill-dir skills/adaptive-html-final

# 로컬 브라우저 확인
python3 -m http.server 8770 -d output/adaptive-html-final-13-topics-20260605_083433
# → http://127.0.0.1:8770/index.html
```

---

## 📦 13개 모드

요청에서 여러 트리거가 감지되면 우선순위가 높은 모드가 선택되며, 사용자가 모드를 명시하면 그 지시가 우선합니다.

| # | Mode | 언제 쓰나 | Layout |
|--:|---|---|---|
| 1 | `skill_audit` | SKILL.md/.skill 분석·개선·통합 | `skill-audit-report.html` |
| 2 | `platform_blog` | 티스토리·벨로그·네이버·워드프레스 변환 | `platform-adaptation.html` |
| 3 | `seo_dashboard` | 제목·메타·태그·검색 의도 설계 | `seo-dashboard.html` |
| 4 | `education_html` | 강의·온보딩·실습·퀴즈 | `course-module.html` |
| 5 | `expert_html` | 전문가 리포트·아키텍처·리스크 진단 | `expert-report.html` |
| 6 | `article_html` | 공개 아티클·매거진형 글 | `magazine-article.html` |
| 7 | `blog_writer` | 블로그 글·포스팅·경험담 | `personal-blog-essay.html` |
| 8 | `beginner_html` | 초보자 설명·비유·용어 풀이 | `beginner-learning.html` |
| 9 | `reference_html` | 레퍼런스·매뉴얼·API 문서 | `reference-manual.html` |
| 10 | `comparison_html` | 비교·장단점·선택 기준 | `comparison-matrix.html` |
| 11 | `case_study_html` | 사례 연구·회고·프로젝트 기록 | `case-study.html` |
| 12 | `landing_brief_html` | 소개·랜딩·요약 페이지 | `landing-brief.html` |
| 13 | `checklist_playbook` | 체크리스트·운영 절차·플레이북 | `checklist-playbook.html` |

---

## 🖼️ 쇼케이스 갤러리

13개 모드를 **각각 다른 주제**로 실행해 만든 실제 결과물입니다. 모든 페이지는 스킬의 editorial 디자인 시스템을 inline으로 포함한 독립 실행 HTML이며, 품질 게이트 적대적 검증을 거쳤습니다. (스크린샷·링크는 canonical [`adaptive-html-final-showcase-v4`](https://coreline-ai.github.io/skills-html-showcase/output/adaptive-html-final-showcase-v4) 기준 · 13개 모드 데모) — 프로파일별 골든은 위 [비주얼 프로파일](#️-비주얼-프로파일) 참조(widget=v5 · auto=v6 · diagram=슬림). 최신 로컬 검증 산출물은 [`adaptive-html-final-13-topics-20260605_083433`](output/adaptive-html-final-13-topics-20260605_083433/)입니다.

<table>
<tr>
<td width="50%"><a href="https://coreline-ai.github.io/skills-html-showcase/output/adaptive-html-final-showcase-v4/pages/01-beginner-passkeys-webauthn.html"><img src="docs/screenshots/01-beginner.png" width="100%" alt="beginner_html"></a><br><b>01 · <code>beginner_html</code></b><br>패스키와 WebAuthn, 비밀번호 없는 로그인 입문</td>
<td width="50%"><a href="https://coreline-ai.github.io/skills-html-showcase/output/adaptive-html-final-showcase-v4/pages/02-expert-eu-ai-act-governance.html"><img src="docs/screenshots/02-expert.png" width="100%" alt="expert_html"></a><br><b>02 · <code>expert_html</code></b><br>EU AI Act 기반 생성형 AI 거버넌스 리포트</td>
</tr>
<tr>
<td width="50%"><a href="https://coreline-ai.github.io/skills-html-showcase/output/adaptive-html-final-showcase-v4/pages/03-article-ai-agent-ux-trust.html"><img src="docs/screenshots/03-article.png" width="100%" alt="article_html"></a><br><b>03 · <code>article_html</code></b><br>AI 에이전트 UX의 신뢰 설계 (매거진 아티클)</td>
<td width="50%"><a href="https://coreline-ai.github.io/skills-html-showcase/output/adaptive-html-final-showcase-v4/pages/04-education-github-actions-security-ci.html"><img src="docs/screenshots/04-education.png" width="100%" alt="education_html"></a><br><b>04 · <code>education_html</code></b><br>GitHub Actions 보안 CI 교육 모듈 (퀴즈 포함)</td>
</tr>
<tr>
<td width="50%"><a href="https://coreline-ai.github.io/skills-html-showcase/output/adaptive-html-final-showcase-v4/pages/05-blog-local-ai-workstation.html"><img src="docs/screenshots/05-blog.png" width="100%" alt="blog_writer"></a><br><b>05 · <code>blog_writer</code></b><br>로컬 AI 워크스테이션 구축기 (경험담)</td>
<td width="50%"><a href="https://coreline-ai.github.io/skills-html-showcase/output/adaptive-html-final-showcase-v4/pages/06-seo-rag-vs-finetuning.html"><img src="docs/screenshots/06-seo.png" width="100%" alt="seo_dashboard"></a><br><b>06 · <code>seo_dashboard</code></b><br>RAG vs Fine-tuning SEO 대시보드</td>
</tr>
<tr>
<td width="50%"><a href="https://coreline-ai.github.io/skills-html-showcase/output/adaptive-html-final-showcase-v4/pages/07-platform-rag-post-platforms.html"><img src="docs/screenshots/07-platform.png" width="100%" alt="platform_blog"></a><br><b>07 · <code>platform_blog</code></b><br>RAG 글을 4개 플랫폼용으로 변환</td>
<td width="50%"><a href="https://coreline-ai.github.io/skills-html-showcase/output/adaptive-html-final-showcase-v4/pages/08-skill-audit-adaptive-html-final.html"><img src="docs/screenshots/08-skill-audit.png" width="100%" alt="skill_audit"></a><br><b>08 · <code>skill_audit</code></b><br>adaptive-html-final 스킬 자체 감사 리포트</td>
</tr>
<tr>
<td width="50%"><a href="https://coreline-ai.github.io/skills-html-showcase/output/adaptive-html-final-showcase-v4/pages/09-reference-openai-responses-api.html"><img src="docs/screenshots/09-reference.png" width="100%" alt="reference_html"></a><br><b>09 · <code>reference_html</code></b><br>OpenAI Responses API 실무 레퍼런스</td>
<td width="50%"><a href="https://coreline-ai.github.io/skills-html-showcase/output/adaptive-html-final-showcase-v4/pages/10-comparison-postgresql-mysql-sqlite.html"><img src="docs/screenshots/10-comparison.png" width="100%" alt="comparison_html"></a><br><b>10 · <code>comparison_html</code></b><br>PostgreSQL vs MySQL vs SQLite 선택 기준</td>
</tr>
<tr>
<td width="50%"><a href="https://coreline-ai.github.io/skills-html-showcase/output/adaptive-html-final-showcase-v4/pages/11-case-cloudflare-thanksgiving-incident.html"><img src="docs/screenshots/11-case-study.png" width="100%" alt="case_study_html"></a><br><b>11 · <code>case_study_html</code></b><br>Cloudflare 2023 보안 사고 회고</td>
<td width="50%"><a href="https://coreline-ai.github.io/skills-html-showcase/output/adaptive-html-final-showcase-v4/pages/12-landing-ai-knowledge-hub.html"><img src="docs/screenshots/12-landing.png" width="100%" alt="landing_brief_html"></a><br><b>12 · <code>landing_brief_html</code></b><br>사내 AI 지식 허브 랜딩 브리프</td>
</tr>
<tr>
<td width="50%"><a href="https://coreline-ai.github.io/skills-html-showcase/output/adaptive-html-final-showcase-v4/pages/13-checklist-web-accessibility-release.html"><img src="docs/screenshots/13-checklist.png" width="100%" alt="checklist_playbook"></a><br><b>13 · <code>checklist_playbook</code></b><br>웹 접근성 배포 전 30분 체크리스트</td>
<td width="50%" valign="top"><br><b>＋ 추가 데모</b><br>· <a href="https://coreline-ai.github.io/skills-html-showcase/output/adaptive-html-final-showcase-v4/pages/14-visual-template-system.html">14 · Visual Template System</a> (8000×6000 SVG 인포그래픽)<br>· <a href="https://coreline-ai.github.io/skills-html-showcase/output/adaptive-html-final-showcase-v4/pages/15-svg-template-gallery.html">15 · SVG 템플릿 20종 갤러리</a><br>· <a href="https://coreline-ai.github.io/skills-html-showcase/output/final_20260604/index.html">final_20260604 · Skill Template HTML</a> (스킬 적용용 단일 템플릿 HTML)</td>
</tr>
</table>

> 💡 로컬에서 렌더된 모습으로 직접 보려면: `python3 -m http.server 8788` 실행 후 `http://127.0.0.1:8788/output/adaptive-html-final-showcase-v4/index.html`

---

## 🎚️ 비주얼 프로파일

스킬을 **기동할 때 비주얼 스타일을 고를 수 있습니다.** 코어(13모드 라우터·레이아웃·코어 CSS 5종)는 100% 공유하고, 프로파일이 *어느 라이브러리·삽입 단계·CSS 번들*을 쓸지만 게이트합니다. 세 프로파일 모두 **외부/동작 JS 0**.

<table>
<tr>
<td width="33%" align="center"><b>🧩 <code>widget</code> (= <code>style=v5</code>)</b></td>
<td width="33%" align="center"><b>📊 <code>diagram</code> (= <code>style=v6</code>)</b></td>
<td width="33%" align="center"><b>🔀 <code>auto</code> (기본)</b></td>
</tr>
<tr>
<td><a href="https://coreline-ai.github.io/skills-html-showcase/output/adaptive-html-final-showcase-v5/pages/04-education-postgres-indexing.html"><img src="docs/screenshots/profile-widget.png" width="100%" alt="widget profile"></a></td>
<td><a href="https://coreline-ai.github.io/skills-html-showcase/output/adaptive-html-final-showcase-diagram/pages/10-message-queue-kafka-rabbitmq-sqs.html"><img src="docs/screenshots/profile-diagram.png" width="100%" alt="diagram profile"></a></td>
<td><a href="https://coreline-ai.github.io/skills-html-showcase/output/adaptive-html-final-showcase-v6/pages/02-realtime-inventory-sync-operating-model.html"><img src="docs/screenshots/profile-auto.png" width="100%" alt="auto profile"></a></td>
</tr>
<tr>
<td valign="top">CSS 뷰 위젯 <code>wg-01~20</code> — 탭·플로우·아코디언 등 <b>인터랙티브</b> 컴포넌트(CSS-only). 코어5 + <code>widgets.css</code>.</td>
<td valign="top">SVG→HTML 템플릿 <code>vt-</code> 21종 — 리스크 매트릭스·비교 카드·타임라인·soft workflow map 등 본문 삽입 <b>정적 도식</b>. 코어5 + <code>visual-html.css</code>.</td>
<td valign="top">둘 다(vt- 1순위 + wg- 보강). 현행 기본값이자 <b>회귀-0 기준선</b>. 코어5 + 두 라이브러리.</td>
</tr>
</table>

| 프로파일 | 별칭 | 라이브러리 (markup) | CSS 번들 | 골든 쇼케이스 |
|---|---|---|---|---|
| `widget` | `style=v5` | CSS 뷰 위젯 `wg-` | 코어5 + `widgets.css` | [`showcase-v5`](https://coreline-ai.github.io/skills-html-showcase/output/adaptive-html-final-showcase-v5) (정합화) |
| `diagram` | `style=v6` | SVG→HTML `vt-` | 코어5 + `visual-html.css` | [`showcase-diagram`](https://coreline-ai.github.io/skills-html-showcase/output/adaptive-html-final-showcase-diagram) (슬림) |
| `auto` (기본) | — | 둘 다 | 코어5 + `widgets.css` + `visual-html.css` | [`showcase-v6`](https://coreline-ai.github.io/skills-html-showcase/output/adaptive-html-final-showcase-v6) |

```bash
# 기동 인자로 선택 (별칭 v5/v6도 수용 · 미지정 시 auto)
adaptive-html-final  profile=widget      # 또는 style=v5
adaptive-html-final  profile=diagram     # 또는 style=v6
adaptive-html-final                      # 기본 auto

# 검증기는 출력의 sources/profile.json 을 자동 인지(또는 --profile)해
# 교차 누수(diagram에 wg- / widget에 vt-)를 차단한다
python3 skills/adaptive-html-final/scripts/validate_output.py <output_dir> \
  --skill-dir skills/adaptive-html-final --profile diagram
```

> 🤖 **크로스-에이전트 결정론**: 인자가 명시되면 Claude Code·Codex·Gemini가 동일 결과를 낸다(정규화 `profile=` 우선, 무효 토큰은 `invalid_profile` 실패). 비대화형(AGENTS.md 경유)은 미지정 시 무조건 `auto`. 분리 설계·검증 계획은 [`implement_visual_profile_separation.md`](implement_visual_profile_separation.md).

---

## 🏗️ 스킬 구조

### 디자인 시스템 (CSS 레이어)

```text
theme.css        색/폰트/폭 토큰(:root) · skip · focus-visible · reduced-motion   ← 코어 해시
components.css    term · analogy · danger · good · hero-analogy · try · tbl · faq · cta-box ...  ← 코어 해시
visual-components.css   figure.visual-figure (8000×6000 SVG 삽입 셸)               ← 코어 해시 · v4.2
layouts.css       13개 모드별 그리드/구조 (+ 39개 레이아웃 전용 클래스)              ← 코어 해시
print.css         인쇄 대응(print-color-adjust · break-inside)                    ← 코어 해시
widgets.css       CSS 뷰 위젯 wg-01~20 (탭·플로우·아코디언, 무 JS)  ← v4.4 · widget/auto 프로파일 조건부 인라인
visual-html.css   SVG→HTML 템플릿 vt- 21종 (본문 삽입 도식)        ← v4.5+ · diagram/auto 프로파일 조건부 인라인
body-icons.css    본문 아이콘 bi- 32종                                      ← 프로파일 무관 장식 자산
editorial-patterns.css  chronology/source/insight/a11y 등 본문 패턴 8종      ← 프로파일 무관 구조 자산
shape-visuals.css · workflow-visuals.css  soft-shape 36종 + workflow 도판 10종 ← 프로파일 무관 시각 앵커
theme-dark.css    CSS-only 3-테마 토큰 오버라이드 + 라디오 세그먼트 스위처       ← v5.2 · print 뒤 항상 인라인(코어 해시 제외)
```

> 코어 해시는 **5종**(theme·components·visual-components·layouts·print)의 합본 SHA-256(`adaptive-html-final-core-css-sha256` 마커)이며, `widgets.css`·`visual-html.css`·`theme-dark.css`는 해시 대상이 아닌 조건부/후행 인라인 자산이다.

### 비주얼 템플릿 시스템 (v4.2+)

목적형 정보는 외부 사진 검색이 아니라 **8000×6000 SVG 인포그래픽**을 기본값으로 직접 생성합니다.

| 구성 | 내용 |
|---|---|
| `visual-templates/*.svg.tpl` | hero-map · card-grid · decision-tree · quality-gate · timeline · matrix · checklist-flow (7종) |
| `scripts/render_visual_svg.py` | visual brief(JSON) → 8000×6000 SVG 렌더러 (**stdlib only**, 오프라인 동작) |
| `schemas/visual-brief.schema.json` | 시각 템플릿 입력 스키마 |
| 데모 | SVG 템플릿 [20종 갤러리](https://coreline-ai.github.io/skills-html-showcase/output/adaptive-html-final-showcase-v4/pages/15-svg-template-gallery.html) (risk-heatmap, sankey, treemap, user-journey 등) |

---

## 📁 프로젝트 구조

```text
skills-html-showcase/
├── skills/adaptive-html-final/        # 통합 스킬 + .skill 패키지
│   ├── SKILL.md                       # 라우터 · 워크플로우 · 품질 게이트
│   ├── manifest.json                  # name/version/modes/layouts/profiles/theme_system (v5.2.0)
│   ├── assets/                        # base.html · CSS · 위젯/도식/패턴/테마 자산 · 13개 레이아웃 골격
│   ├── references/                    # 모드/레이아웃/글쓰기/SEO/플랫폼/감사/비주얼 규칙
│   ├── recipes/       (13)            # 13개 모드별 대표 프롬프트
│   ├── schemas/       (3)             # blog-meta · quality-report · visual-brief
│   ├── tests/                         # 품질/레이아웃/시각회귀/접근성/거버넌스 게이트
│   ├── visual-templates/ (7)         # 8000×6000 SVG 템플릿
│   ├── scripts/                       # render_visual_svg.py · validate_output.py 등
│   └── examples/      (8)            # 예시 결과물
├── output/
│   ├── adaptive-html-final-showcase-v4/   # 13모드 쇼케이스 (canonical 13-mode 데모)
│   │   ├── pages/     (15)            # 13모드 + 비주얼 데모 + SVG 갤러리
│   │   └── media/svg-template-demos/ (20)  # 8000×6000 SVG 데모
│   ├── adaptive-html-final-13-topics-20260605_083433/ # v5.2.0 3-테마 검증 산출물
│   └── (playwright/ · qa-screenshots/ 는 .gitignore)
├── docs/screenshots/  (13)           # 본 README용 쇼케이스 썸네일
├── demo/ · orginal_skill/            # 이전 계열 데모 · 원본 스킬
├── ANALYSIS_adaptive-html-final.md   # 7-전문가 정밀 분석 보고서
└── Guide.md                          # 사용 가이드
```

---

## 🔬 스킬 상세 분석

[`ANALYSIS_adaptive-html-final.md`](ANALYSIS_adaptive-html-final.md) — 7개 전문가 에이전트 병렬 분해 + 쟁점 적대적 검증 + 교차 통합 감사로 도출한 정밀 분석 보고서입니다.

### 검증으로 입증된 강점

| 항목 | 결과 |
|---|---|
| skip link ↔ `<main id="main">` | **13 / 13** (접근성 회귀 가드로 고정) |
| 단일 `h1` 원칙 | 13 / 13 |
| 외부 동작 JS | **0건** |
| 미정의 CSS 클래스 | **0개** (레이아웃↔CSS 차집합 0) |
| manifest ↔ 디스크 레이아웃 매핑 | 차집합 0 |
| recipes 커버리지 | 13 / 13 모드 |
| blog-writer 상세 규칙 흡수 | 8 / 8 (제목 4계열·도입부 3유형·본문 밀도·톤 매핑·100점·메타·플랫폼·박스) |

### 버전 진화

| 버전 | 핵심 |
|---|---|
| `v4.0.0` | ultimate(13모드 라우터) + blog-writer(블로그/SEO 규칙) **통합** · skip link 버그 수정 |
| `v4.1.0` | 7-전문가 분석 P0~P2 자동 패치 — 모드 ID 통일, recipes 13/13, 스키마 보강, 디자인 토큰 정리(AA 대비·print·reduced-motion) |
| `v4.2.x` | **Visual Template System** 도입 — 8000×6000 SVG 인포그래픽 7종 + stdlib 렌더러 + quality-gate 레이아웃 보정 |
| `v4.3.3` | 13모드 전수 캡쳐 감사 기반 **반응형 폴리시** — dark CTA 대비, 플랫폼 그리드, 모바일 표 밀도, case timeline 구조 + 정적 게이트 |
| `v4.4.0` | **뷰 위젯 시스템** 편입 — CSS 뷰 위젯 `wg-01~20`(무 JS, `widgets.css` + 위젯 템플릿) + 위젯 정적 게이트, 전문가 리뷰 P0/P1 마감 |
| `v4.5.0` | **SVG→HTML 템플릿** 편입(`vt-` 20종, `visual-html.css`) + **하네스 정형화**(루트 `AGENTS.md` 결정론 진입점) + **비주얼 프로파일**(`widget`·`diagram`·`auto`) 도입 — 검증기 `--profile`·교차 누수 게이트·`profiles` 매니페스트 |
| `v5.0.0` | 코어 프리미티브 업그레이드 + 토큰 전용 다크 테마 도입. CTA/SERP/platform primitive를 기존 정본 클래스 안에서 강화 |
| `v5.1.0` | proper-black 다크 보정. vt/wg 표면 색, CTA 태그, 회색 리터럴 토큰화, OS/토글 조합 회귀를 실제 캡처로 검증 |
| `v5.2.0` | **CSS-only 3-테마 시스템**(라이트·화이트·다크) + 라디오 세그먼트 스위처. CSS snapshot/source manifest/legacy toggle 검증 강화, `wg-12`·`wg-16`·`vt-02`·`vt-21`·`.try` 회귀 패치 |

> 전체 변경 이력: [`skills/adaptive-html-final/CHANGELOG.md`](skills/adaptive-html-final/CHANGELOG.md) · 프로파일 분리 계획: [`implement_visual_profile_separation.md`](implement_visual_profile_separation.md)

---

## ✅ 품질 게이트

모든 산출물이 통과해야 하는 최소 조건입니다. (`tests/quality-checklist.md`, `tests/accessibility-checklist.md`)

- [x] 요청 목적과 선택 모드 일치 + 모드별 필수 블록 존재
- [x] `lang="ko"` · viewport · `<title>` · meta description
- [x] `h1` 정확히 1개 · 주요 `h2`에 `.h2-sub`(모드 한정 권장)
- [x] `#main` skip link target · `:focus-visible` · `prefers-reduced-motion`
- [x] 모바일 1컬럼 전환 · 표는 `.tbl` 래퍼(가로 스크롤)
- [x] 3-테마 스위처는 `name="ahf-theme"` 라디오 계약을 사용하고 legacy `#theme-toggle` 없음
- [x] 외부/동작 JS 0 · 확인되지 않은 최신 정보 단정 금지 · 출처 추측 금지
- [x] 교육용=퀴즈+정답 · 전문가용=리스크+검증 · 블로그/SEO=제목+메타+태그 · 감사=개선본
- [x] 비주얼: 8000×6000 캔버스 · `figure`+`figcaption` · 의미 있는 `alt` · 캔버스 잘림 없음

---

## ⚡ 사용법

### 스킬로 콘텐츠 생성 요청

```text
[입력 자료/URL/파일/주제]를 [목적/독자]용 [모드]로 만들어줘.
출력은 [단일 HTML / Markdown+HTML / 플랫폼별 원고]로 해줘.
비주얼: profile=widget | diagram | auto  (또는 style=v5 | v6, 미지정 시 auto)
반드시 포함: [목차, 용어 풀이, 예시, 리스크, FAQ, CTA 등]
주의: [최신 정보는 확인 필요 표시, 외부 JS 금지, 모바일 안전 표]
```

`profile=widget`은 탭·플로우 같은 인터랙티브 위젯(`wg-`)을, `profile=diagram`은 본문 삽입 도식(`vt-`)을, `auto`(기본)는 둘 다 적용합니다. 자세한 선택 규칙은 [비주얼 프로파일](#️-비주얼-프로파일) 참조.

### 비주얼 인포그래픽 직접 렌더

```bash
# visual brief(JSON) → 8000×6000 SVG (stdlib only, 오프라인 동작)
python3 skills/adaptive-html-final/scripts/render_visual_svg.py brief.json output.svg
```

### 쇼케이스 로컬에서 보기

```bash
# 저장소 루트에서
python3 -m http.server 8788
# canonical v4 쇼케이스
# → http://127.0.0.1:8788/output/adaptive-html-final-showcase-v4/index.html

# 최신 v5.2.0 13-topic 산출물
# → http://127.0.0.1:8788/output/adaptive-html-final-13-topics-20260605_083433/index.html
```

---

## 📜 License

별도 라이선스가 지정되지 않았습니다. 사용 전 저장소 소유자(`coreline-ai`)에게 확인하세요.

<div align="center">
<sub>생성 도구: <code>adaptive-html-final</code> v5.2.0 · 13-mode · 3-theme · 3-profile editorial HTML engine</sub>
</div>
