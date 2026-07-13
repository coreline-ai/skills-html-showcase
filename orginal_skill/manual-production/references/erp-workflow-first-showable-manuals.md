# ERP workflow-first showable manuals

Use this reference when an ERP/admin tutorial is becoming a shallow screen tour. The manual must teach the actual work unit, not merely where menus and filters are.

## Required order

```text
analysis
→ structuring: overall business flow and step structure
→ index.html shell: workflow map and lesson sequence
→ per-step execution
   step plan
   → production: capture, guided video, review-card content, workflow diagram
   → verification
```

Do not begin with more screenshots or videos until the workflow structure is clear.

## What analysis must answer

For each workflow, identify:

- trigger/input: what starts the work;
- prerequisites/master data: customer, supplier, item, warehouse, company, roles;
- transaction/action: what document or operation is created/changed;
- review/approval/status boundary: Draft, Submit, Cancel, Amend, permissions;
- output/report: what confirms the work is complete;
- risk boundary: accounting, tax, stock mutation, export, external visibility, or destructive action;
- safe fixture requirement: whether demo/disposable data is required before capture.

## Index shell requirement

`index.html` is not a decorative landing page added at the end. Build or revise it before per-step production so the learner sees:

- the overall 업무 단위 workflow map;
- where each lesson sits in the workflow;
- upstream prerequisites and downstream checks;
- risky boundaries that require safe fixture or expert review;
- active path highlighting for the selected step.

A menu list, module tour, or generic navigation map is insufficient for ERP/operator training.

## Per-step plan template

```yaml
step_id:
title:
business_flow:
operator_goal:
trigger_input:
prerequisites:
screens_to_capture:
video_storyboard:
review_cards:
workflow_diagram_nodes:
risk_boundary:
safe_fixture_required:
success_check:
verification_required:
```

## ERP workflow examples

### Master data maintenance

```text
company/organization baseline
→ Customer / Supplier / Item / Warehouse check
→ required fields for downstream work
→ confirm values are selectable in transaction screens
```

### Selling / lead-to-cash

```text
customer + item prepared
→ Quotation optional/required decision
→ Sales Order confirmation
→ delivery or billing trigger
→ Sales Invoice
→ Payment Entry
→ receivable/status/report check
```

### Buying / procure-to-pay

```text
need for item/quantity
→ Material Request optional/required decision
→ Purchase Order
→ Purchase Receipt
→ Purchase Invoice
→ payable/stock/status check
```

### Stock movement and adjustment

```text
item + warehouse baseline
→ stock need or discrepancy identified
→ Stock Entry for movement/receipt/issue
→ Stock Reconciliation only after count/approval
→ stock balance/report check
```

### Document status control

```text
Draft saved
→ review
→ Submit creates operational/accounting/stock impact
→ downstream document/report check
→ Cancel/Amend only with safe fixture and approval boundary
```

## Review-card and workflow diagram pairing

Each review card should teach one recognizable screen area or decision point in the business flow. Pair it with the workflow diagram node it supports. Review cards must not become QA/status cards, and they should support click-to-enlarge/lightbox behavior in interactive HTML.

## Verification expectations

Before claiming a step is useful, `manual-verification` should confirm:

- the index workflow map and lesson sequence match the business flow;
- each step follows trigger → action → check, not screen → description;
- capture/video/review-card/workflow diagram all point to the same workflow node;
- risky Submit/Cancel/Amend, invoice/payment, stock mutation, and export actions are bounded;
- shallow navigation-only slices are labeled as orientation/supporting material, not the main business manual.
