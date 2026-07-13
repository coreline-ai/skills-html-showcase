# Selected Flow Path in Workflow Maps

## Problem this prevents

A manual can look interactive because it has an overall set of workflow cards, while still failing the reader's mental model: selecting a flow changes a side detail or focus lesson, but the map itself never shows the selected flow's internal path.

For beginner/operator manuals, this is a production failure. A Workflow Map must answer two questions at the map level:

1. What are the major flows available?
2. When one flow is selected, what are the concrete steps inside that flow?

Showing only the overall flow list forces the reader to infer the individual path from distant detail text, which defeats the purpose of a map.

## Production rule

For any flow-first manual with two or more major flows:

- Keep the overall flow selector/card set.
- Render the selected flow's internal steps as a visible path in the primary Workflow Map: step boxes, arrows/connectors, badges, or a compact diagram.
- If the accepted/baseline design uses a grouped node canvas (for example category columns of menu/function nodes), the selected path must be expressed **inside that canvas**: selected-flow endpoints become active nodes, unrelated nodes are dimmed, connector paths are drawn between the participating nodes, and numbered badges sit on the connector path. Do not satisfy this requirement by adding a separate strip of selected-flow boxes below the real canvas while the canvas itself stays unchanged.
- A separate selected-flow strip is acceptable only when the map's intended structure is itself a strip/linear diagram and there is no richer grouped-node canvas to preserve.
- The selected-flow path must update together with:
  - active flow card
  - active/dim node states in the workflow canvas, when present
  - connector paths and connector badges, when present
  - detail panel title/summary/steps/checks
  - focus lesson heading/copy/media/diagram
  - any lesson tabs or review cards scoped to the selected flow
- Do not rely only on a side panel, below-the-fold focus section, or hidden state to represent the selected path.

## Minimum DOM/model contract

A robust implementation has one canonical flow data object per major flow:

```js
{
  id: 'governance',
  title: '승인과 거버넌스 보기',
  summary: '...',
  steps: ['요청 생성', '영향 확인', '승인/거절', '후속 처리'],
  checks: ['...'],
  path: ['Request', 'Board Review', 'Approve / Reject', 'Agent Wakeup', 'Audit Log']
}
```

The render function should update all flow-scoped surfaces from that same object. Avoid separate hard-coded lists for selector, detail panel, and focus lesson.

For grouped node canvases, prefer an endpoint model so the map can draw the selected path rather than only list labels:

```js
{
  nodes: [
    { id: 'request', group: 'approval', label: 'Request' },
    { id: 'board', group: 'approval', label: 'Board Review' },
    { id: 'decision', group: 'approval', label: 'Approve / Reject' },
    { id: 'activity', group: 'audit', label: 'Activity Log' }
  ],
  flows: {
    governance: {
      title: '승인과 거버넌스 보기',
      steps: [
        { from: 'request', to: 'board', label: 'Board Review' },
        { from: 'board', to: 'decision', label: 'Approve / Reject' },
        { from: 'decision', to: 'activity', label: 'Activity Log' }
      ]
    }
  }
}
```

Render from `steps[from/to]`: active nodes are the union of endpoints; connector paths and numbered badges are generated from the same steps; detail-panel bullets and mini-flow labels come from the same canonical list. This prevents the common regression where the selector/detail changes but the grouped canvas remains a static overview.

## QA signals

A production smoke should click at least one non-default flow and assert:

- selected-flow path container exists
- selected path title matches the clicked flow
- selected path step count is greater than 1
- step labels are flow-specific, not the default flow's labels
- active card, detail panel, and focus lesson all match the same selected flow
- console errors are zero
- desktop layout does not hide or clip the path

Example browser-side probe:

```js
document.querySelector('[data-flow="governance"]').click();
({
  selectedPanelExists: !!document.querySelector('#selectedFlowMap'),
  selectedTitle: document.querySelector('#selectedFlowMap h3')?.textContent,
  selectedSteps: [...document.querySelectorAll('#selectedFlowMap .flow-step span')].map(x => x.textContent),
  active: [...document.querySelectorAll('.flow-card.active')].map(x => x.dataset.flow),
  detail: document.querySelector('#dTitle')?.textContent,
  lesson: document.querySelector('#lessonTitle')?.textContent
})
```

PASS requires the selected-flow path to be visible in the map itself, not merely inferable from other page sections.
