# Workflow Map / Detail Panel Height Sync

Use this when a static interactive manual has a two-column desktop shell: a workflow map or canvas on the left and a selected-flow/detail panel on the right. If the detail panel grows taller than the map, the layout stops reading as one selected-flow unit and users must visually reconcile two unrelated block heights.

## Pattern

- Treat the workflow map/canvas height as the source of truth for desktop layouts.
- Measure the rendered `.workflow-map` height after flow selection and after responsive/layout changes.
- Store the value as a CSS custom property on the shared shell, for example `--workflow-map-height`.
- Apply that value to `.detail-panel` `height` and `max-height`.
- Keep `overflow:auto` on the detail panel so long copy remains available without stretching the paired layout.
- Disable the sync in stacked/tablet/mobile layouts; use natural height instead.

Example CSS:

```css
.workflow-shell {
  display: grid;
  grid-template-columns: minmax(0, 1fr) minmax(320px, 420px);
}

.detail-panel {
  position: sticky;
  top: 78px;
  align-self: start;
  height: var(--workflow-map-height, auto);
  max-height: var(--workflow-map-height, calc(100vh - 96px));
  overflow: auto;
}

@media (max-width: 1280px) {
  .workflow-shell { grid-template-columns: 1fr; }
  .detail-panel {
    position: static;
    height: auto;
    max-height: none;
    overflow: visible;
  }
}
```

Example JS:

```js
const workflowShell = document.querySelector('.workflow-shell');
const workflowMap = document.querySelector('.workflow-map');

function syncWorkflowPanelHeight() {
  if (!workflowShell || !workflowMap) return;
  if (window.matchMedia('(max-width: 1280px)').matches) {
    workflowShell.style.removeProperty('--workflow-map-height');
    return;
  }
  const height = workflowMap.getBoundingClientRect().height;
  if (height > 0) workflowShell.style.setProperty('--workflow-map-height', `${Math.round(height)}px`);
}

function selectFlow(flowId) {
  // ...existing flow state updates...
  requestAnimationFrame(syncWorkflowPanelHeight);
}

window.addEventListener('resize', syncWorkflowPanelHeight);
if (window.ResizeObserver && workflowMap) {
  new ResizeObserver(syncWorkflowPanelHeight).observe(workflowMap);
}
requestAnimationFrame(syncWorkflowPanelHeight);
```

## Verification

Run a mechanical all-flow check at desktop widths above the stacked breakpoint and at least one stacked width below it.

Desktop invariant:

- For every selectable flow, `abs(round(detailPanel.height) - round(workflowMap.height)) <= 1`.
- `.detail-panel` computed `overflow-y` is `auto` or `scroll` when content is longer.
- The shell CSS variable is populated, e.g. `--workflow-map-height: 797px`.
- No console errors after switching all flows.
- A visual screenshot confirms the map and panel form a matched-height pair.

Stacked invariant:

- Below the breakpoint, the CSS variable is removed or ignored.
- `.detail-panel` returns to `height:auto`, `max-height:none`, and `overflow:visible`.
- Natural content height is allowed to differ from the map.

If a browser/tool probe against a deployed static host is blocked by approval gating, do not over-claim remote QA. Report local PASS, deployment uploaded, and remote QA incomplete unless another allowed browser-side or visual probe has actually run.