# Arrow-Badge Workflow Canvas Pattern

Use this reference when a user-facing manual needs a Print Station-style workflow canvas where step numbers belong to the **movement between nodes**, not to the menu/function nodes themselves.

## Core principle

A workflow step is usually an edge: “what moves from this work object/screen to the next.” If the number is placed on the node, first-time readers can misread the number as a property of the menu/function. Prefer one separated arrow per step with the step number as a badge near the middle of that arrow.

## Production rules

1. Keep a single canonical `steps` array for each flow, e.g. `{ from, to, label, note, check }`.
2. Render each step as exactly one connector path from `from` to `to`.
3. Put the step badge on the connector, not inside the node.
4. Do not add `기준`/`결과` or similar node chips unless the design explicitly needs node-level roles. If roles are needed, label them semantically and keep them secondary to the connector sequence.
5. Use a simple legend such as `번호 · 화살표 흐름 단계` when the only encoded meaning is the numbered arrow sequence.
6. Describe the sequence as a representative/checking path, not an always-mandatory 1→N execution order. Add entry/branch/skip notes for real workflows that may start later or split.
7. Preserve flow-scoped sections below the canvas: changing the selected flow should update headings, intro copy, lesson tabs/stage, overview cards, variants, checks, and modal/media state.

## Implementation hints

- Use an SVG overlay for connectors so nodes remain regular DOM cards.
- Put the connector overlay and badge layer above the canvas/card stacking context (for example `.connectors { z-index: 20 }`, `.edge-badge { z-index: 30 }`, `.canvas { z-index: 1 }`, `.node { z-index: 2 }`, with `pointer-events: none` on the overlay). A badge child cannot visually escape a parent stacking context that sits behind the cards.
- For each edge, compute endpoints from the rendered node rectangles.
- Use cubic Bezier paths for readability. Common cases:
  - same-column movement: vertical curve between bottom/top or side anchors;
  - left-to-right movement: gentle horizontal curve from source right edge to target left edge;
  - right-to-left/backtracking movement: U-shaped or dipping curve to avoid crossing node text.
- Place the badge at the Bezier midpoint, not at an arbitrary fixed offset. A helper like `mid(p0,p1,p2,p3)` keeps badges attached to the visual path.
- Recompute paths and badges after flow switches and layout changes.

## Verification invariant

For every flow from the primary delivery shell:

```text
arrowPaths.length === arrowBadges.length === detailSteps.length
nodeStepChipElements.length === 0   # when using the arrow-badge-only pattern
badgeTexts == ["1", "2", ..., String(detailSteps.length)]
consoleErrors.length === 0
```

Also visually inspect at least one long/dense flow and one short flow. Dense connector lines may be a polish issue, but they must not imply that a number belongs to an unrelated inactive node.
