# ERP/Admin Beginner Operator-Guide Lessons

Use this reference when producing ERP/admin manuals for beginners, especially when the user expects Print Station-style operator guides rather than status artifacts.

## User-facing HTML boundary

Manual HTML must read as learner/operator guidance only. Keep these out of the tutorial page and place them in `STATUS.md`, `HANDOFF.md`, `qa/`, or `sources/` instead:

- phase/progress/status language
- future TODOs and blocked notes
- peer/Hermes/oracle/agent wording
- production implementation details such as browser automation, rendering, video conversion, capture scripts, or artifact provenance
- safety-fixture planning notes that are not directly useful to the learner

Before claiming a page is ready, scan visible text for internal/meta words such as `showable`, `artifact`, `slice`, `Playwright`, `ffmpeg`, `fixture`, `provisional`, `blocked`, `peer`, and `Hermes`.

## Beginner-first transaction lesson shape

For transaction-flow lessons, do not start with clicks. Use this order:

1. Concept primer — what the workflow/object is and when an operator uses it.
2. One-line mental model — e.g. Quotation = condition proposal; Sales Order = agreed order conditions fixed as the internal work basis.
3. First-appearance glossary — English UI label + Korean meaning + plain explanation.
4. Prerequisites — master data or roles needed before the screen makes sense.
5. Flow map — trigger → preparation → document/action → review → output/boundary.
6. Screen path / guided video — only after the concept primer.
7. Danger/good pair — common beginner mistake + safer habit.
8. Review checks — 3–5 visible things the learner can confirm on screen.

## Print Station-style lesson structure

For ERPNext-style showable pages, the stronger pattern is:

- workflow-first shell with topbar, summary cards, sticky topic pills, workflow map, detail panel, and learning frame
- each lesson has a Driver.js guided video, not only a raw navigation recording
- lesson body has a left video panel, right note-card stack, and three review cards below
- review cards use screenshot enlargement/lightbox so labels remain readable
- additional pages should preserve the shell pattern and update both the standalone page and the embedded template in the shell

If local `file://` rendering makes iframe-like learning frames blank, embed lesson templates directly or serve via local HTTP and verify visually.

## Safe evidence modes for ERP transaction screens

Prefer read-only existing demo records. If no suitable demo record exists, opening a New form without saving can be acceptable as screen-reading evidence, provided the page clearly does not claim to complete a transaction. Record it as `unsaved_form_capture` in QA evidence.

Never execute or imply completion of risky steps unless the fixture and approval are explicit:

- Save/Submit/Cancel/Amend for business documents
- Sales Invoice / Payment Entry execution
- stock mutation or reconciliation
- tax/accounting/legal/payroll advice

## Bounded prerequisite/readiness slices

For ERP transaction training, a useful next slice can be a prerequisite/readiness lesson rather than a new transaction execution. This is especially appropriate when Save/Submit/Cancel/Amend, invoice, payment, or stock posting is not approved.

Pattern:

1. State the operator goal as screen reading and pre-action recognition, not completion of a transaction.
2. Reuse existing verified screenshots when they visibly contain the needed fields; do not perform new live mutations just to make a tutorial feel complete.
3. Pair master-data list evidence with an unsaved/new-form screenshot when teaching preparation for a document. Example shape: Customer list → Item list → unsaved Quotation draft.
4. Write copy only against visible labels in the images. If the screenshot shows `Customer Name`, `Status`, `Customer Group`, `Territory`, `ID`, `Not Saved`, `Date`, `Valid Till`, `Company`, or `Items`, those labels can be taught; do not introduce adjacent invoice/payment/stock concepts except as explicit out-of-scope boundaries.
5. Mention Save/Submit only as a boundary or pre-action check unless the safe fixture and controller approval explicitly allow execution.
6. If no new guided video is needed, do not regenerate video just to satisfy a pattern. A coherent review-card lesson with annotated screenshots and modal-preserved callouts can be the smallest safe artifact.
7. When the manual has both a standalone lesson page and an embedded primary-shell template, update and verify both paths. Primary-shell tab switching, image loading, and modal annotation preservation are required checks.

## Verification checklist

- Visible-text forbidden/meta scan passes on standalone lesson, shell embedded template, and render composition.
- Required beginner aids are present for transaction-flow lessons.
- All media refs exist and are non-empty.
- Driver.js render composition has visual QA for highlight/popover alignment.
- Shell tab/card switching loads the correct embedded lesson.
- Review-card enlargement works in the standalone lesson.
- QA/status docs record caveats separately from user-facing HTML.
