# Direct Transaction Evidence Cards

Use this when a static/operator manual explains a workflow through screenshots, value chips, review cards, or flow-focused panels.

## Core lesson

If the copy names a business document, state change, or downstream effect, the manual needs direct evidence for that exact object. Do not use a nearby or adjacent screen as a proxy.

Examples of proxy failures to catch:

- Copy says a receipt was posted, but the screenshot shows only an order or a generic stock workspace.
- Copy explains stock balance, but the image shows a stock entry form rather than the balance/report where the quantity is checked.
- Copy says invoice/payment/outstanding changed, but the visible card lacks amount, status, document id, or party evidence.
- A flow card says `A -> B -> C`, but the focus-gallery skips B and relies on text alone.

## Production checklist

For every flow panel/review card:

1. List the named documents, reports, statuses, parties, items, amounts, quantities, and downstream checks in the copy.
2. For each named object, map one direct screenshot/card that visibly shows it or revise the copy to remove the claim.
3. If an adjacent screen is still useful context, label it as context only; do not let it stand in for the missing document/report.
4. Read back system state for state-changing demo flows before writing final values.
5. Sync both source/showable and public/deploy directories, then hash-check them before deployment.

## QA checklist

- A beginner can point to the screenshot that proves each document in the flow exists.
- Each state-changing transition has both a document/status evidence card and a downstream effect/check card when the manual asks the reader to verify the effect.
- No card uses a broader workspace, list, or adjacent transaction as the only proof for a specific document/report named in the text.
- If persona QA reports confusion between two transaction types, treat it as `REQUEST_CHANGES` until the screenshots and copy separate those objects.
