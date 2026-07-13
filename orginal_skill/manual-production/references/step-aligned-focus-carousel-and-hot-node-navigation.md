# Step-aligned focus carousel and hot-node navigation

Use this when a static/operator manual has one numbered focus screenshot per workflow step and the screenshot section becomes too long to read comfortably.

## Problem signal

- The workflow map, step list, and focus screenshot cards are correctly 1:1, but the page becomes a long vertical screenshot list.
- The reader has to scroll through many large screenshots to reach the next section.
- The user asks for slides, carousel behavior, or clicking a hot path/node to jump to the matching screenshot.

## Required pattern

1. Keep the step-count/focus-card invariant from `manual-verification` intact: one canonical workflow step still has one corresponding focus card.
2. Render the focus screenshot set as a single-slide carousel rather than a long grid/list.
3. Show only one focus card at a time.
4. Provide previous/next controls and a visible counter such as `3 / 8`.
5. Provide numbered dots/buttons matching the canonical step numbers.
6. Add `data-focus-step` or equivalent stable identifiers to:
   - numbered dots;
   - hot-path/hot-node cards;
   - static jump links, if present.
7. Clicking a hot-node/path item must set the carousel to the same numbered slide and update current-state styling on the dot, hot-node, and jump link.
8. Keyboard activation should work for hot-node/dot controls with Enter/Space.
9. Add enough `scroll-margin-top` or equivalent offset so sticky workflow navigation does not cover the carousel target after a hot-node click.
10. Preserve screenshot annotations/callouts and enlarged modal behavior; changing to carousel must not reduce evidence quality.

## Verification checklist

For each selectable flow:

- Step count equals focus-card count.
- Dot count equals focus-card count.
- Hot-node/path count equals focus-card count when hot-nodes represent steps.
- Exactly one focus card is visible at a time.
- Clicking step N hot-node activates slide N.
- Previous/next controls move to adjacent slides and wrap or clamp intentionally.
- All images load.
- Console/JS errors are zero.
- Forbidden internal/process terms are absent from visible user-facing copy.
- Visual QA confirms the carousel is not hidden under sticky navigation and remains understandable on representative desktop/mobile widths.

## Reporting

Report this as a layout/readability improvement, not as a change to workflow coverage. Include the deployment URL, content hash if available, and per-flow count/navigation QA.