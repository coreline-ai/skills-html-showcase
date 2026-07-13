# Beginner system overview page pattern

Use this when a manual targets readers who do not already understand the product/system as a whole. This adapts the teaching patterns from `html-for-beginners` into operator manuals without importing its one-off article template or visual style.

## Purpose

Before the reader enters workflow lessons, give them a mental model of the system: what it is, who uses it, what parts exist, what moves through it, and where beginner mistakes happen. This page prevents the manual from becoming a set of disconnected procedures.

## Required artifact

For non-trivial product/operator manuals, add a learner-facing system overview page, normally one of:

- `overview.html` or `system-overview.html` linked from `index.html` before workflow lessons; or
- an explicit “시스템 개요” top-level section in `index.html` only when the package is intentionally single-page.

Do not hide this in `STATUS.md`, `HANDOFF.md`, `sources/`, or `qa/`; it is learner-facing content.

## Required beginner structure

Use this shape unless the domain calls for a stricter project template:

1. **먼저, 이 시스템이 뭔가?** — plain-language description in 2–4 paragraphs.
2. **한 줄 정신 모델** — one memorable sentence or analogy, using `.og-hl` sparingly for the key distinction.
3. **누가 무엇을 하는가** — role/persona cards: operator/admin/approver/customer/internal service as applicable.
4. **큰 부품 지도** — diagram/flowchart/concept map of the system parts. For repo/docs products, use components such as app server, database, search/vector store, connector, provider, auth, CLI/desktop, health/backup; for ERP/admin products, use master data, transaction documents, approvals, reports, public output.
5. **무엇이 흘러가는가** — data/work item lifecycle from input → processing → result/check. Prefer concrete nouns over architecture jargon.
6. **초보자가 헷갈리는 경계** — danger/good pairs for common confusions: demo vs production, config vs app setting, auth vs model provider, sync success vs answer quality, draft vs submitted, screen visible vs business confirmed.
7. **이 매뉴얼을 읽는 순서** — how the overview connects to the workflow map and lesson pages.
8. **확인 질문** — 3–5 questions the beginner should be able to answer before starting workflow lessons.

## Evidence rules

- Use verified product docs/source/UI evidence; do not invent architecture.
- For public repo/docs-only manuals, cite source paths or official docs for each major component.
- If live UI was not run, say so in the evidence boundary outside learner copy or in a small source-boundary section; do not imply screenshot/UI verification.
- First appearances of acronyms and domain terms must include English/Korean/plain-language explanations.
- Use everyday analogies only to clarify relationships; do not replace source evidence with metaphor.

## Visual requirements

- Keep the operator-guide design system (`og-*`, `--og-*`) rather than copying the `html-for-beginners` red/off-white article skin.
- Include at least one visual mental model: `.og-diagram`, flowchart, component map, lifecycle map, or annotated screenshot if available.
- Avoid a page of prose only. Use cards/callouts/tables sparingly, with prose doing the explaining.
- Optional 4-panel HTML/CSS knowledge comic is allowed when useful, but do not make it mandatory for operational manuals unless the owner asks for that style.

## Verification checklist

- [ ] `index.html` links to the overview before deep lessons, or the single-page overview section is visible before workflow detail.
- [ ] The overview explains what the system is, who uses it, major parts, work/data lifecycle, common beginner confusions, and reading order.
- [ ] It contains a visual mental model, not text only.
- [ ] It uses beginner-friendly term explanations and danger/good pairs where needed.
- [ ] It does not leak production process notes, peer/Hermes terms, or unsupported runtime claims.
- [ ] Workflow lessons do not duplicate the entire overview; they build on it with bounded task detail.
