# Quality Checklist

핵심 품질 게이트 체크리스트. 상세 CSS/레이아웃 게이트(semantic section grid, caption, .try 대비, --link-on-dark, blog counter, SERP 스타일, CSS 무결성, SVG 크기 등)는 `scripts/validate_output.py`가 자동 강제하므로, 여기서는 사람이 직접 확인해야 하는 항목과 자동 게이트의 의도를 함께 정리한다.
공통 게이트는 모든 모드에 적용하고, 모드별 게이트는 해당 모드일 때만 적용한다.
표기: 항목 끝의 `(auto)`는 `validate_output.py`가 정적으로 검사하는 게이트, `(auto+manual)`은 자동 검사하되 모바일/시각 판단은 사람이 보강해야 하는 게이트다.

## 공통 게이트 (전 모드)

- [ ] 요청 목적과 선택 모드가 일치한다.
- [ ] 선택 모드의 `assets/layouts/<layout>.html` 정보 구조를 실제 본문에 적용했다. `layout-*` 클래스만 붙인 자유형 `<main>`이 아니다.
- [ ] 선택 모드의 필수 블록이 모두 있다.
- [ ] 같은 모드의 기존 검수 예제 또는 지정 정답지보다 헤더·목차·섹션 밀도·결론 품질이 후퇴하지 않았다.
- [ ] `.mini-card`/`.col-list`가 대부분 섹션의 주 구조를 차지하지 않는다. 카드·표·vt·wg·체크리스트·원문 발췌가 섹션 목적별로 섞여 있다.
- [ ] “Generated example”, “전문 예제”, “예제 문서”, “기준 1/2/3”, `placeholder/TBD` 같은 임시 생성 문구가 없다.
- [ ] 마지막 결론은 해당 문서의 실제 판단·권고·다음 행동이며, “이것은 예제/샘플” 자기 설명이 아니다.
- [ ] 전문/데모/벤치마크 산출물은 `scripts/quality_contract_check.py <output_dir>`를 통과했다.
- [ ] 공통 디자인 토큰을 임의 변경하지 않았다(색/폭/간격 토큰은 theme.css `:root` 기준 유지).
- [ ] output HTML이 최신 CSS asset 합본을 사용한다. `sources/css-integrity.json`와 인라인 `adaptive-html-final-core-css-sha256` hash가 현재 skill asset hash와 일치한다. (auto)
- [ ] h1은 하나다. (auto)
- [ ] `<main id="main">`이 있어 skip link가 동작한다. (auto)
- [ ] h2/h3 계층이 자연스럽다(레벨 건너뛰기 없음).
- [ ] 주요 h2에 `.h2-sub` 또는 동등한 부제가 있다(모드 한정 권장: 공개 아티클·블로그·SEO·전문가 리포트 등 주요 h2에 권장, 전 모드 강제는 아님).
- [ ] `<p class="h2-sub">`가 `</h2>`로 잘못 닫히지 않았다. (auto)
- [ ] 본문 폭이 `--max-reading`(780px) 또는 `--max-wide`(1020px) 토큰값을 따른다.
- [ ] 모바일 1컬럼 전환이 가능하다.
- [ ] 모바일 390px 기준에서 제목, 표 캡션, 카드 텍스트가 잘리지 않는다.
- [ ] semantic section wrapper에 grid/card CSS가 직접 적용되지 않는다(`section.matrix`, `section.serp-preview`, `section.value-grid` 등에 `display:grid` 금지). grid는 내부 `.card-grid`/`.grid-2`/`.matrix:not(section)` wrapper에만 적용한다. (auto, 알려진 회귀 패턴 한정)
- [ ] section/card 내부 첫 h2/h3가 과도한 top margin을 만들지 않는다(`section>h2:first-child` margin reset 존재). (auto)
- [ ] 모든 table에는 visible `<caption>`이 있고, 음수 margin/absolute/overflow로 잘라내지 않는다. (auto)
- [ ] 4열 이상 모바일 표는 `.mobile-card-table` 또는 동등한 카드형 대체가 있고, 카드 모드에서 각 셀이 `data-label`로 헤더를 노출한다. (auto+manual)
- [ ] 긴 URL/코드/영문 토큰은 `overflow-wrap:anywhere` 등으로 본문 폭을 넘지 않는다.
- [ ] 검정 `.try` 섹션 안의 밝은 카드(`.box`/`.summary-card`/`.cta-box`/`.card-block`/`.mini-card`) 텍스트가 검정 섹션의 흐린 색을 상속받지 않고 `var(--ink)`/`var(--ink-soft)`로 되돌아간다. (auto)
- [ ] `.try`/`.try.soft-cta` 내부 태그 pill이 충분한 대비로 읽힌다(`color:var(--ink)` 복원). (auto)
- [ ] `.try`/`.try.soft-cta` 내부 링크가 충분한 대비로 읽힌다(`--link-on-dark` 토큰 사용). (auto)
- [ ] 시각 템플릿을 사용한 경우 → SVG 원본은 8000×6000 이상이고 `img width/height/alt`와 `figcaption`이 있다. (auto)
- [ ] 시각 템플릿을 사용한 경우 → SVG 내부 카드/텍스트가 캔버스 밖으로 나가지 않고 모바일에서 잘리지 않는다.
- [ ] 외부 사진/AI 이미지를 사용한 경우 → 출처·라이선스·생성 여부를 표시했고 사실 이미지처럼 오해되지 않는다.
- [ ] 확인되지 않은 최신 정보/수치/가격을 단정하지 않았다.
- [ ] 출처나 메타 정보를 추측하지 않았다.
- [ ] 출처가 많으면 본문 말미 출처 목록 또는 `sources/index.html` 허브로 분리했고, 허브를 쓰면 산출물에서 함께 생성했다.
- [ ] 외부 동작 JS를 사용하지 않는다(`<script type="application/ld+json">` 메타데이터는 허용). (auto)
- [ ] 로컬 참조(`img`/`a`/`link` 등)가 깨지지 않는다. (auto)
- [ ] JSON-LD가 있으면 valid JSON이다.

## 모드별 조건부 게이트

- [ ] 블로그/아티클/SEO이면 → 제목, 메타 설명, 태그 또는 키워드가 있다.
- [ ] `blog_writer`이면 → 본문 section h2에 번호 badge 또는 동등한 진행 표시가 있다(`.layout-blog article>section>h2:first-child::before` counter). (auto)
- [ ] `seo_dashboard`이면 → SERP Preview 제목이 literal Google blue(`#1a0dab`)/Arial/과대 크기 고정이 아니라 페이지 디자인과 균형을 이룬다. (auto)
- [ ] `platform_blog`이면 → `.platform-grid`는 section 자체가 아니라 내부 wrapper(`:not(section)`)에만 적용했다. (auto)
- [ ] 교육용이면 → 퀴즈와 정답(해설)이 있다.
- [ ] 전문가용이면 → executive summary, 운영모델/RACI 또는 동등한 실행 구조, 리스크 매트릭스, 로드맵, 검증 기준이 모두 있다.
- [ ] 전문가용이면 → 각 핵심 섹션이 1~2문장 요약만으로 끝나지 않고 의사결정에 필요한 근거·담당·산출물·검증 방법을 포함한다.
- [ ] `comparison_html`이면 → `.winners:not(section)`/`.tradeoffs:not(section)` 의미형 블록이 h3와 ul을 서로 다른 grid column으로 찢지 않는다. (auto)
- [ ] `case_study_html`이면 → timeline section과 timeline card의 left rule이 중복되지 않으며, 순서형 목록에는 굵은 accent left rule을 추가하지 않는다. (auto)
- [ ] 스킬 감사이면 → 개선본 SKILL.md까지 포함한다.


## youtube_analysis / manual_analysis / github_feature_usage

- [ ] youtube_analysis는 Video Evidence Map, Source Limits, FACT/INFERENCE/UNKNOWN, observed_at를 포함한다.
- [ ] youtube_analysis는 iframe/embed/autoplay를 포함하지 않는다.
- [ ] manual_analysis는 Source & Version Snapshot, Reader Role Router, Prerequisites/Safety, Troubleshooting, Source Limits를 포함한다.
- [ ] manual_analysis의 stale/누락/모순 지적은 원문 근거 또는 확인 불가 라벨을 가진다.
- [ ] github_feature_usage는 positioning, feature toc(`toc-map feature-toc`), 기능 지도(카드 4+), 시작 방법(단계형), 적합/부적합, 도입 전 확인, Source Limits를 포함한다.
- [ ] github_feature_usage의 버전·라이선스·성능 수치는 입력에 없으면 UNKNOWN으로 남긴다(실사 어조 아님 — 안내체).
