# Flow-aware lesson section alignment

Use this when an operator-guide `index.html` has both a flow-first workflow map and a lesson/prerequisite area below it.

## Problem signal

The workflow map changes by selected flow, but the lesson section still reads like a static default lesson, often sales-only. Examples:

- A heading such as “prerequisites and selling flow” remains while purchase, receipt, or stock flow is selected.
- The map/detail panels update, but lesson heading/copy/tabs keep the previous flow’s framing.
- A generated overview uses canonical step data, but the section intro still claims a fixed Quotation → Sales Order path.

This is a content bug even if the page renders correctly.

## Production rule

Treat the lesson/prerequisite section as part of the selected workflow state.

For every flow change, align:

1. Section heading and intro copy.
2. Lesson tabs and default active lesson.
3. Generated overview cards.
4. Review/check copy.
5. Any preserved media framing.

Shared prerequisite lessons may remain, but frame them as supporting the current flow. If a preserved lesson is specific to sales basics, keep it available for sales-adjacent learning but do not make it the default for purchase, receipt, stock, or other non-sales flows.

## Implementation pattern

- Keep one canonical flow object with `label`, `copy`, `steps`, `variants`, `risks`, `lessons`, and `defaultLesson`.
- Add a function such as `lessonIntro(flow)` that derives the section intro from the selected flow.
- Generate overview cards from the selected flow’s `steps`, `variants`, and checks.
- On `selectFlow`, update map, detail panel, menu detail, lesson tabs, default lesson, and lesson stage together.
- Preserve working media and modal code; only change default lesson routing and learner-facing framing when possible.

## Copy guidance

Good lesson-section copy explains business meaning:

- starting condition or document
- representative checking path
- branch/start-later cases
- downstream document, stock, payment, or reporting effects
- what to compare before Submit/invoice/payment/stock actions

Avoid visible-UI narration:

- “selected flow shows on the right”
- “click the tab below”
- “highlighted items are shown”
- “left/right panel”

Avoid authoring/internal language:

- source of truth, internal, process/meta, handoff, QA path, artifact, slice, provisional, blocked, peer/Hermes

## Verification checklist

For each flow:

- Heading contains or clearly matches the selected flow label.
- Intro copy uses the selected flow’s start/end documents or business state.
- Default tab is not stale from another flow.
- Generated overview contains the selected flow’s steps/variants/checks.
- No non-sales flow defaults to a sales-only lesson unless explicitly framed as shared sales basics and not the primary overview.
- Workflow map counts still align: top sequence, connector badges, aside steps, and check rows.
- Active nodes have role-labeled chips; inactive nodes do not retain stale chips.
- Existing videos, posters, screenshots, review cards, and modal behavior still work from the primary shell.
- Visible-text scan for internal terms and obvious UI narration returns zero hits for the configured patterns.
