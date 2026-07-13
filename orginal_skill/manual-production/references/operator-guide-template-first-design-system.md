# Operator guide template-first design system

Use this when producing showable/manual-package HTML where visual consistency matters across sessions, products, or agents.

## Lesson from the Onyx/ERPNext comparison

A manual-production skill that only contains principles and references can still produce visually inconsistent HTML: one session may generate a simple hero/card package while another produces a richer Print Station/ERPNext-style workflow guide. To keep outputs consistent, showable manuals need a **template-first contract** like `html-for-beginners`: a starter template, design tokens, named components, and verification expectations.

The current default shell uses the Refero/Cursor-derived **Warm ivory software studio** visual standard: parchment background, Inkwell text, Muted Stone secondary text, Onyx Outline orange accents used as outlines/links/connectors, compact 4px radii, and layered card elevation. Preserve that style through `references/static-operator-guide-design-system.md`; do not revert to a generic blue SaaS dashboard skin unless the user explicitly asks for a different brand skin.

## Required default for showable operator guides

When the user asks for a product/operator manual and does not explicitly request a plain Markdown/reference document, start from a reusable operator-guide shell rather than a blank HTML file.

The starter shell should include these named regions/components:

- `hero` / guide title / learner audience summary
- scope and evidence badges that are reader-facing, not internal process labels
- workflow map or canvas for the real job path
- selected-flow detail panel
- arrow-badge or clearly labeled step path when steps represent movement between nodes
- flow-aware lesson/focus section
- step-aligned focus cards or carousel when there are many screenshots/checks
- review/evidence cards with annotations, not plain crops when the card teaches recognition
- common checks / risk notes / success evidence
- source and QA boundary link area, with internal details kept in `STATUS.md`, `HANDOFF.md`, `qa/`, or `sources/`

## Template-first instruction to give agents/peers

Use wording like:

```text
Build this as a manual-production static operator guide. Do not start from a blank HTML file.
Use the operator-guide shell/design-system pattern: workflow map/canvas, selected detail panel, flow-aware lessons, step-aligned focus cards or carousel, annotated review/evidence cards, and learner-facing-only copy. Keep STATUS/HANDOFF/qa separate from the visible page.
```

For public repo products such as Onyx, adapt the components to the domain instead of copying ERP transaction labels. Replace ERP document numbers/amounts with operational evidence such as `.env` settings, compose profiles, auth mode, provider connection state, connector sync state, citation/search evidence, agent/action configuration, health endpoints, backup/upgrade checks, and runtime/UI boundaries.

## When a simpler static package is acceptable

A simpler hero + cards + lesson links package is acceptable only when one of these is true:

- The user explicitly asked for a lightweight repo/docs reference package.
- Live UI capture is not available and the phase is clearly marked as capture-blocked/provisional.
- The goal is package correction from Markdown-only to basic HTML, not final operator training.

Even then, record the boundary honestly: repo/docs evidence is not live UI capture, and static package smoke does not prove the manual teaches real screen operation.

## Rebuilds after user correction or skill update

When the user corrects the artifact shape (for example, "this should be a package, not Markdown") or says the manual skill has been modified and asks to remake it:

1. Start a fresh, version-separated package directory unless the user explicitly asks to overwrite the old one.
2. Re-load the relevant manual-production and manual-verification references before rebuilding.
3. Treat the rebuild as a Dynamic Workflow run when the user asks for DW or when the artifact has multiple phases: structure audit, package generation, refutation-first verification, and strict closeout.
4. Use the reusable operator-guide shell by default for showable HTML. Do not merely restyle the old lightweight package.
5. Keep the final verdict scoped: `PASS` for the static/template package can coexist with bounded caveats that runtime, UI capture, connectors, providers, or client installs were not executed.

## Verification checklist

- [ ] The output started from a reusable template/shell or explicitly recorded why a lightweight package was chosen.
- [ ] The visible page uses the same named component language across manuals instead of ad-hoc CSS for every session.
- [ ] The workflow map describes a real operational path, not a generic feature list.
- [ ] Detail/focus/review sections concretize the selected flow with domain-appropriate evidence.
- [ ] Internal process terms and QA notes stay out of learner-facing HTML.
- [ ] The final report distinguishes template/style consistency from content/evidence correctness.
- [ ] If this is a rebuild after correction, the old artifact, new artifact, changed basis, and remaining boundaries are all reported explicitly.
