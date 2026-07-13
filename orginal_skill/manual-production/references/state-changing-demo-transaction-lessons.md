# State-changing demo transaction lessons

Use this reference when an operator manual needs to move beyond read-only explanation into submitted demo transactions such as ERP orders, delivery notes, invoices, payments, stock entries, approvals, or other state-changing records.

## Trigger

Apply when the owner explicitly approves previously excluded risky actions, for example:

- create/submit order, invoice, payment, stock, approval, or posting documents
- capture the submitted state for a manual or guided video
- demonstrate status/ledger/stock effects in a demo or staging system

Do **not** infer approval from a request to improve a manual video. Approval must cover the state-changing class of action or the exact documents/workflows.

## Required sequence

1. **Restate the approved scope** in the worklog/report before acting: environment, company/site/tenant, document classes, and whether external deployment is included.
2. **Confirm the environment is safe**: demo/staging/local, not production; identifiable test parties/items/warehouses/accounts; no real customer/vendor/payment data.
3. **Write a fixture plan first**: document types, test entities, intended amounts/quantities, required accounts/modes of payment, rollback/cleanup expectations, and stop conditions.
4. **Execute with unique markers** in titles, remarks, reference numbers, or comments so generated records are searchable later.
5. **Read back from the system of record**, not just the browser page. Verify document IDs, `docstatus`/status, key totals, outstanding amounts, percent billed/delivered/received, and stock/ledger side effects when relevant.
6. **Capture visual evidence after readback**: representative submitted Desk/admin pages plus contact sheets. Visual evidence supports the readback; it does not replace it.
7. **Convert the result into a manual lesson only after execution evidence passes**. User-facing copy should teach consequence and stop checks, not celebrate that the agent ran a script.
8. **Regenerate guided video from the final lesson copy**, then verify metadata, playback, contact sheet, visible document IDs/statuses, missing refs, console errors, and forbidden internal terms.
9. **Separate local/demo PASS from public deployment PASS**. A new lesson/video is not public until the static package is rebuilt, redeployed, and remotely smoke-tested.

## Manual-video checklist for submitted transaction demos

A transaction execution video should show:

- beginner behavior goal: what the viewer can explain or safely check afterward
- Must-Know: which records change stock, ledger, outstanding amounts, approval state, or external visibility
- Danger: do not follow in production without approved data and authority
- one coherent flow, normally 1–3 core judgments plus supporting evidence
- visible document IDs/statuses or a linked table under the video
- stop criteria before Submit/Post/Pay/Issue/Receive
- summary that distinguishes UI navigation from business-state mutation

## Evidence bundle

For each run, keep:

- fixture plan under `sources/`
- execution/readback log under `qa/`
- screenshots of submitted records under `qa/.../screenshots/`
- contact sheet for screenshots and video frames
- video metadata from `ffprobe`
- browser smoke output for the final lesson page
- STATUS/HANDOFF/state update that says whether the lesson is local-only or deployed

## Common pitfalls

- **Treating submitted screenshots as enough.** Always read back record state and side effects from the app/database/API.
- **Hiding state mutation behind a tutorial.** The manual page should say what changed and where to verify it.
- **Forgetting payment references.** Many ERP/payment systems require reference number/date or account-specific fields before payment entries submit.
- **Mixing demo execution PASS with deployment PASS.** If the lesson/video was added after the last deployment, say so explicitly.
- **Using scaled contact sheets as exact evidence.** Contact sheets prove visual coverage; exact IDs/statuses belong in readback logs and individual screenshots.
