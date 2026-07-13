# Static Workflow Map Detail Panels: Screenshots + Actual Values

Use this when a showable operator/manual page already has a high-level Workflow Map and the owner asks for a static replacement for video or a more concrete explanation below the map.

## Core rule

The Workflow Map explains the **basic flow**. The static detail area below it should not repeat that map in prose. It should make the selected flow understandable through:

- real application screenshots,
- visible highlights/callouts on those screenshots,
- concrete sample values from the demo/staging dataset,
- document/status transitions,
- business checks and downstream effects.

If the detail panel can be read without any actual document number, customer/vendor/item, quantity, amount, status, or screenshot evidence, it is still too abstract.

## Required panel structure

For each selectable flow, include:

1. **Flow-specific heading** — e.g. `<Flow name> — actual values / screen evidence` rather than a generic default heading.
2. **Flow-focused screenshot sequence** — not just one enlarged screenshot. When a flow spans multiple documents/screens, show 3–5 focused screenshots for that selected flow in the order a learner should compare them. Each card should have a highlight/callout, the screen's concrete values, and a short check line. A single primary screenshot is acceptable only for genuinely single-screen tasks.
3. **Actual value strip** — 3–5 chips using safe demo/staging values, such as:
   - document ID / order number / invoice number,
   - customer or supplier,
   - item/SKU/service,
   - quantity, amount, warehouse, date, status, balance, or projected result.
4. **Representative path card** — short path through the flow using the same values, framed as a representative/checking path rather than mandatory 1→N execution when real work can branch.
5. **Evidence cards** — 2–4 supporting screenshots for upstream/downstream screens or documents, each with a concise learner-facing note and visible highlight when teaching a specific check. If these evidence cards are doing the main teaching, promote them into the flow-focused sequence instead of hiding them as thumbnails.
6. **Check / caution / impact notes** — explain what the user should confirm, what mistake to avoid, and what changes downstream.

## Copy rules

- Do not narrate obvious UI layout. Replace “the selected card is highlighted” with the business meaning of the selected flow.
- Do not use internal production terms such as handoff, peer, fixture, source of truth, provisional, blocked, POC, Playwright, or ffmpeg in user-facing HTML.
- Use the same concrete values across heading, chips, screenshots, path cards, review cards, and modal/enlarged screenshot copy.
- If a screenshot does not visibly support a claimed field/status/amount, either change the screenshot, add a visible annotation, or rewrite the claim.
- Keep the static detail area synchronized with the selected map flow: heading, intro copy, tabs, stage content, examples, screenshots, and modal content should all change together.

## Verification checklist

Before PASS:

- [ ] Every flow selection updates the static detail heading and body.
- [ ] Multi-document flows render a flow-focused screenshot sequence for the selected flow, not just one enlarged screenshot plus tiny supporting thumbnails.
- [ ] Each focus screenshot has a visible highlight/callout, concrete value chips or adjacent values, and a check line tied to that exact screen.
- [ ] Every flow has at least one primary screenshot and supporting evidence screenshots.
- [ ] Screenshots load in the primary shell and enlarged/modal state if present.
- [ ] Each flow includes actual values, not placeholder-only examples.
- [ ] Actual values are consistent across chips, copy, screenshots, and downstream effect notes.
- [ ] No video elements remain if the owner explicitly pivoted from video to static.
- [ ] Console/runtime errors are zero for flow switching.
- [ ] User-facing forbidden/meta terms are absent.
- [ ] Public/deploy artifact is byte/hash-synchronized with the reviewed showable artifact before deployment.

## Pitfall

A common failure is to treat “static structure” as a text-only substitute for video. That misses the purpose. Static manual panels must preserve flow and emphasis by making real screen evidence spatially readable: screenshots, focus boxes, concrete field values, and the document/status consequences that a learner should verify.
