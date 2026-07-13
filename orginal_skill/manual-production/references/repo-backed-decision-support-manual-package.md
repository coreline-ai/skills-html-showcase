# Repo-backed decision-support manual package

Use this pattern when building a public-reader static manual for an internal/repo-backed decision-support system such as market dashboards, research assistants, paper-trading labs, recommendation engines, or operations dashboards where the source repo is evidence but the manual must not mutate the source system.

## Trigger

- User asks for a detailed onboarding/operator manual for a repo-backed system.
- The system influences decisions (markets, finance, operations, risk, allocation, approvals) but the requested deliverable is a reader manual, not live execution.
- The user asks for concept + flow + cautions, beginner help, detailed lessons, or Dynamic Workflow closeout.
- The source repo may contain generated data, dirty files, or runtime artifacts that must remain untouched.

## Scope boundary

State this boundary before/inside the manual:

- The manual is for understanding, safe reading, and operational interpretation.
- It is not investment advice, professional advice, automated execution, production configuration, or order/transaction approval.
- Source JSON/data contracts are the source of truth; dashboards, Markdown, Telegram, cards, and reports are derived reader views unless the repo says otherwise.
- Stale/fallback/sample data must be visible to the reader. Teach users to check `generated_at`, `source_dates`, `stale`, fallback/sample labels, and source path before acting on a conclusion.
- Keep source repo edits out of scope unless explicitly requested. Write the manual package in a separate artifact directory and sync only the public-reader copy to the deploy repo.

## Recommended artifact structure

For a static package under a hub such as `/onboarding/manuals/<manual-id>/`:

```text
<manual-id>/
  index.html                 # workflow map / selected flow detail / lesson list
  beginner.html              # first-read concept primer
  overview.html              # system/data-flow mental model
  lessons/
    01-*.html ...            # standalone detailed lessons
  assets/
    style.css
    guide.js
  manifest.json
  STATUS.md                  # internal delivery state, not public-reader copy if excluded
  extras/source-map.md       # concise source evidence map
```

Keep a local source package and a public deploy copy synchronized. Example pattern:

```text
/Projects/research/<system>-manual-package-v1/                         # authoring source
/Projects/research/manual-onboarding-cloudflare/public/onboarding/manuals/<manual-id>/  # public copy
```

Do not use the application source repo as the manual output directory unless the user explicitly wants docs committed there.

## Content requirements

### `index.html`

Use a workflow map shaped around reader jobs, not repo modules. For decision-support systems, useful flows often include:

- daily/morning routine
- market or system signal reading
- portfolio/watchlist or candidate review
- prediction/feedback loop
- execution-boundary or closing-bet review
- dashboard/report interpretation

Each selected flow should show:

- representative path or sequence
- what input starts it
- what source/data it reads
- what evidence proves the state
- what stop condition or caution applies

### `beginner.html`

Do not compress this into summary cards. Include:

- what the system is and is not
- one-line mental model
- first-appearance term explanations for key English/acronym labels
- an everyday analogy
- dangerous interpretation vs good interpretation pairs
- stale/fallback/data-freshness section
- a small recap visual such as 4 panels when useful
- self-check questions

### `overview.html`

Explain the system before workflows:

- source data → analysis/signals → source-of-truth state → reports/dashboard → feedback loop
- source-of-truth vs derived view
- which artifacts are operational evidence and which are just display
- what is out of scope: real orders, API credentials, production setting changes, professional advice

### Standalone lessons

Each lesson must be independently useful, not a thin link target. Include:

- purpose and reader role
- concept and flow
- source evidence / files / views to check
- lesson-specific evidence prompt or readback checklist
- cautions and common mistakes
- beginner checklist
- previous/next navigation

For decision-support manuals, every page should repeat the relevant safety boundary: recommendation-only, no real execution, source freshness, and no professional advice.

## Verification checklist

Run both static and rendered checks:

- all local links resolve
- every page has language, charset, viewport, and title
- investment/professional-advice or real-execution warnings appear on all relevant pages
- stale/fallback/source-of-truth explanation appears in first-read pages and where decisions are taught
- every standalone lesson has lesson-specific evidence/readback, not generic boilerplate
- previous/next lesson navigation works
- workflow selector updates steps/checks/detail without console errors
- production URL smoke checks the hub card and at least one selected flow
- independent QA/refutation checks try to find missing warnings, thin lessons, stale data ambiguity, and broken source/deploy sync

## Dynamic Workflow closeout notes

When using Dynamic Workflow for this class of manual:

1. Inventory source repo read-only.
2. Produce authoring package and public deploy copy separately.
3. Verify locally with static checks and browser smoke.
4. Deploy only the public-reader directory/hub.
5. Run production smoke against the deployed URL.
6. Run independent QA/refutation; fix non-blocking content gaps if they are in scope.
7. Re-deploy after fixes and re-check representative pages.
8. Close the ledger only after `dw_closeout`, strict audit, and doctor pass.

If `dw_audit` requires side-effect metadata, record the approved boundary precisely: file edits in the manual artifact, network calls for deploy/smoke, and deploy to the intended static manual project. Do not broaden this into permission to edit the source application or execute real transactions/orders.

## Common pitfalls

- Editing the source repo while the user asked only for a manual.
- Treating a dashboard as the source of truth when it only displays JSON/report output.
- Hiding stale/sample/fallback data warnings in one page instead of teaching them where readers make decisions.
- Writing lesson pages that merely repeat index cards.
- Deploying the local authoring package but forgetting to sync the public hub copy.
- Verifying only local files and forgetting the production hub card/URL.
- Calling a decision-support page “operational” without explicitly saying it is not advice or execution.
