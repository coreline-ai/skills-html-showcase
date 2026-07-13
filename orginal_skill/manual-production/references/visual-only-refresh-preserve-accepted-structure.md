# Visual-only refresh: preserve accepted manual structure

## Trigger
Use this when an existing manual/package has already reached an owner-accepted information architecture or interaction model, and the owner asks for a design refresh, visual redesign, style update, template migration, or clean rebuild that does **not** explicitly request a structural redesign.

## Core rule
A visual refresh changes the surface style, not the accepted interaction semantics.

Preserve the prior artifact's reader-facing structure:

- flow selectors and tab behavior
- grouped menu/function/workflow nodes
- node ids and node grouping/columns
- selected-flow active/support/dim semantics
- connector/arrow-badge placement semantics
- numbering meaning, especially whether numbers belong to arrows/edges rather than cards/nodes
- detail panels and lesson sections derived from the same ordered step source
- modal, carousel, and review-card behavior where already accepted

Change only the visual layer unless the owner explicitly asks for a different structure:

- tokens, colors, typography, spacing, borders, shadows, radius
- CSS class styling or visual shell wrappers
- component polish that does not change what the reader must understand or click

## Failure pattern from Onyx v4
An accepted v3 manual used:

```js
window.ONYX_GUIDE_DATA = {
  flows: [
    {
      steps: [
        { from_: "goal-lite", to: "docker-env", label: "...", note: "...", check: "..." }
      ]
    }
  ],
  columns: [
    {
      title: "배포 구성",
      nodes: [
        { id: "docker-env", title: ".env / compose", desc: "..." }
      ]
    }
  ]
}
```

The rebuild incorrectly copied a generic template's flow-card sample model:

```js
var guideData = [
  { id: "lite", title: "Lite 평가 배포", summary: "...", steps: ["..."] }
]
```

That regressed the manual from a grouped node map with selected node-to-node arrows into high-level flow description cards — the exact problem the earlier version had already corrected.

## Correct repair pattern
Keep the accepted data/interaction model and apply new visual tokens around it:

1. Extract the accepted prior artifact's data model and DOM/interaction contract.
2. Identify which parts are content/structure semantics vs visual style.
3. Replace only the style layer with the new design system tokens.
4. Preserve the step source of truth; e.g. edge objects `{from_, to, label, note, check}` remain edge objects.
5. Ensure visible numbering still represents the same thing as before; if numbers were arrow-badge steps, do not turn them into flow-card or node chips.
6. Run semantic regression QA against the accepted version, not just token/component existence checks.

## QA checklist

- [ ] Previous accepted artifact inspected for interaction semantics.
- [ ] New artifact preserves the accepted data model shape where relevant.
- [ ] If previous map used grouped columns/nodes, new map still shows grouped columns/nodes.
- [ ] If previous steps were `from -> to` edges, new steps are still edge objects and all endpoints resolve to visible nodes.
- [ ] Number badges retain their original meaning and placement class: edge midpoint vs node/card marker.
- [ ] Detail panel, lesson heading, focus/mini-flow state derive from the selected flow's ordered step data.
- [ ] Old generic-template sample markers that imply the wrong structure are absent.
- [ ] Visual tokens from the new design are present.
- [ ] Browser smoke confirms switching at least one non-default flow updates active nodes, edge badges, detail, and lesson state.

## Reporting boundary
If this repair happens after a workflow closeout, record it as an owner-feedback correction or regression fix rather than pretending it belonged to the original PASS. Update package `STATUS.md`, `HANDOFF.md`, and QA evidence separately.
