# Skill Marketplace Listing Copy for Manual Production

Use this when preparing a public marketplace/profile listing for the `manual-production` skill or a bundled manual-production/manual-verification package.

## Purpose

The listing should explain the skill as a reusable manual-production workflow, not as a one-off project story. Keep the tone practical and evidence-based: the skill helps agents create user-facing manuals grounded in real systems, with artifact packaging and verification boundaries.

## Recommended Korean Listing Structure

### 자기소개

Cover:

- The maker has worked on product manuals, operator guides, admin tutorials, onboarding docs, and static HTML manual packages.
- The work emphasized real user workflows rather than menu/feature lists.
- Typical targets include ERP/admin systems, CMS, dashboards, open-source products, and tools that require beginners to understand screens, terms, states, and outcomes together.
- The skill was created because AI often writes plausible but unverified manuals: imagined UI steps, menu-list documentation, missing beginner explanations, and unverified HTML/media packages.

Tone:

- Do not overclaim broad expertise or imply every manual is fully automated.
- Say the skill was built from repeated manual-production/verification work and failure modes.
- Prefer "실제 시스템 근거", "사용자 업무 흐름", "검증" over abstract productivity claims.

### 스킬소개

Cover these five blocks:

1. **Problem solved**
   - Prevents imagined manuals and shallow screen tours.
   - Forces artifact-format decisions before writing.
   - Separates user-facing copy from QA/status/handoff notes.
   - Requires verification instead of rounding file existence up to completion.

2. **Use environment**
   - Claude Code, ChatGPT/IDE agents, Hermes Agent, or any agent environment with file editing, browser/static checks, terminal/script execution, and optional screenshot/video tooling.

3. **Provided files**
   - `SKILL.md` for principles and workflow.
   - `references/` for detailed patterns such as static packages, beginner pages, workflow maps, videos, deployment QA.
   - `templates/` for manifests, lesson boundaries, handoff, review cards, and HTML shells.
   - `scripts/` for deterministic package/media/manifest checks.
   - Related `manual-verification` skill for independent QA.

4. **Result examples**
   - Static HTML manual package: `index.html`, `overview.html`, `lessons/`, `assets/`, `sources/`, `qa/`, `manifest.yml`, `STATUS.md`, `HANDOFF.md`.
   - Beginner system overview page.
   - Workflow-first operator guide.
   - Screenshot/video/review-card tutorial.
   - Handoff separating completed, verified, unresolved, out-of-scope, and not-verified items.

5. **One-line summary**
   - `manual-production` helps agents move from plausible prose to evidence-grounded, reader-facing manuals with package structure and verification discipline.

## Pitfalls for Marketplace Copy

- Do not turn the listing into a full manual for the skill.
- Do not paste the whole SKILL.md or long reference list.
- Do not describe internal Hermes/peer/Dynamic Workflow process unless the marketplace specifically asks for implementation details.
- Do not claim live UI/runtime/video verification unless the actual user task will perform those checks.
- Do not frame Markdown-only output as the default for "manual"; mention HTML/static package as the default for non-trivial operator manuals.

## Compact Reusable Answer Pattern

```markdown
# 자기소개

저는 AI 에이전트를 활용해 제품 매뉴얼, 운영자 가이드, 관리자 튜토리얼, 온보딩 문서, 정적 HTML 매뉴얼 패키지 등을 제작하고 검증해왔습니다. 단순 기능 설명보다 실제 사용자가 어떤 업무 흐름을 따라 이해하고 실행해야 하는지에 초점을 맞췄습니다.

이 스킬은 AI가 화면을 확인하지 않은 채 그럴듯한 매뉴얼을 쓰거나, 메뉴 목록을 문서처럼 나열하거나, 초보자에게 필요한 목적·용어·주의사항·성공 기준을 빠뜨리는 문제를 줄이기 위해 만들었습니다. 파일이 존재하는 것을 완료로 보지 않고, 실제 시스템 근거와 검증 기록을 함께 남기는 매뉴얼 제작 흐름을 목표로 합니다.

# 스킬소개

`manual-production`은 사용자용 매뉴얼, 운영자 가이드, 관리자 튜토리얼, 온보딩 문서, 정적 HTML 매뉴얼 패키지를 만들 때 사용하는 스킬입니다. 실제 화면·공식 문서·소스 근거를 바탕으로 업무 흐름을 정리하고, 독자가 무엇을 준비하고 어디를 확인하고 어떤 결과를 기대해야 하는지 설명하도록 돕습니다.

사용 환경은 Claude Code, ChatGPT 기반 에이전트, Hermes Agent, Cursor/IDE Agent 등 파일 작업과 브라우저/정적 검증을 수행할 수 있는 환경입니다.

제공 파일은 `SKILL.md`, 상황별 `references/`, 복사용 `templates/`, 검증용 `scripts/`, 그리고 독립 QA용 `manual-verification` 연계로 구성됩니다.

결과물 예시는 `index.html`, `overview.html`, `lessons/`, `assets/`, `sources/`, `qa/`, `manifest.yml`, `STATUS.md`, `HANDOFF.md`를 포함한 정적 매뉴얼 패키지, 초보자용 시스템 개요 페이지, workflow-first 운영자 가이드, 스크린샷/영상/review-card 기반 튜토리얼입니다.
```
