# Screenshot callouts should fit the text, not the container

Use this when a static/manual HTML artifact places explanatory callouts over screenshots or review-card images.

## Problem signal

A small callout with little text still consumes a large rectangle and hides the screenshot behind it. This is common with absolutely positioned overlays when the CSS sets both a vertical start and end constraint, for example `top: 14px` plus `bottom: 14px` or `inset: 14px ... 14px ...`.

In CSS absolute positioning, setting both `top` and `bottom` gives the element a computed height based on the containing block. The callout may look like a fixed panel even if the content is short.

## Production pattern

For learner-facing screenshot annotations, default to content-sized callouts unless the design intentionally needs a full-height side panel:

```css
.shot-callout {
  position: absolute;
  top: 14px;
  bottom: auto;
  width: fit-content;
  max-width: min(56%, 420px);
  height: auto;
  overflow-wrap: break-word;
}

/* In larger modal/lightbox contexts, the max width may be slightly wider. */
.capture-modal .shot-callout {
  max-width: min(56%, 460px);
}
```

Adjust the exact `top`, side offset, and `max-width` to the artifact, but keep the invariant: **do not constrain both vertical edges for a text callout.**

## Verification checklist

- Inspect real rendered geometry, not just CSS source.
- For each representative flow/screenshot, compute or visually confirm:
  - callout height is near the text content height;
  - callout does not cover the main field/value/row it explains;
  - callout width wraps readable Korean text without turning into a narrow column;
  - modal/lightbox views preserve the same annotation behavior.
- A useful smoke metric for normal screenshot overlays: `calloutHeight / screenshotHeight` should usually stay below about `0.20` unless the callout is intentionally long.
- If the page has multiple selectable flows or carousels, verify every flow after one mismatch is found; this layout bug often repeats across generated cards.

## Do not

- Do not reduce step/card coverage to make the page shorter; use carousel/navigation patterns when coverage is the issue.
- Do not move the explanation into hidden QA/status notes; the learner still needs the annotation, just sized correctly.
- Do not accept local-only CSS verification when the artifact is deployed; run the same geometry/visual check on the production URL before PASS.
