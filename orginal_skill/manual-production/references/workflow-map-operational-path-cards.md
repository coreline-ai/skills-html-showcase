# Workflow Map Operational Path Cards

Use this when a manual shell has workflow cards or a workflow map for ERP/admin/operator training.

## Core lesson

A workflow card must not merely answer “what is this workflow?” It should answer the operator’s practical question:

> “What arrives first, what document/screen do I use next, what does that produce, and where does the work go afterward?”

For each workflow card and its detail panel, show a concrete path:

```text
trigger/input → prerequisite/master data → transaction document(s) → downstream boundary → result/check
```

## Required card structure

For each business-unit flow, include:

- **Trigger/input** — request, PO, stock question, purchase need, support ticket, publishing need, etc.
- **Prerequisites** — master data, permissions, safe fixture, price list, warehouse, customer/supplier/item, policy values.
- **Primary transaction path** — the actual documents/screens used in order.
- **Downstream boundary** — where the flow hands off to billing, delivery, payment, inventory, approval, publishing, reporting, or another role.
- **Check/result** — status, outstanding amount, remaining delivery/billing, report/list evidence, public output, audit trail.
- **Risk boundary** — save/submit/cancel/amend, invoice/payment, delivery/stock, export/share, production publishing.

## Detail panel rule

`흐름 단계` / steps must be procedure-shaped, not definition-shaped.

Bad:

- “판매 흐름은 고객과 품목을 바탕으로 견적, 판매 주문, 청구, 결제 확인으로 이어지는 흐름입니다.”

Good:

- “고객이 견적을 요청했는지, 주문 확정 자료가 왔는지 먼저 구분합니다.”
- “Customer, Item, Price List 같은 기준값을 확인합니다.”
- “Quotation에서 품목, 수량, 단가, 유효일, 조건을 확인합니다.”
- “Sales Order에서 확정 주문의 납기, 수량, 금액, 상태를 읽습니다.”
- “Delivery Note / Sales Invoice / Payment Entry는 재고·회계 영향이 있는 후속 경계로 구분합니다.”

## Evidence escalation

If the current card text is shallow, do not only rewrite from intuition. Re-read project sources in this order:

1. Existing manual structuring docs / step plans.
2. Project README, STATUS, HANDOFF, or docs.
3. Upstream product README / DocType docs / official docs.
4. Live UI evidence when available.

Use upstream docs for conceptual path and live UI for final labels/screens.

## Verification checklist

After changing a workflow map:

- Static refs: no missing `src`, `href`, or `poster` assets.
- Visible-copy scan: no internal production/QA terms in user-facing HTML.
- Browser console: no JS errors.
- Selection sync: top nav, workflow map card, detail panel, lesson tabs, and selected lesson all change together.
- Representative flows: verify the changed flow plus at least adjacent flows affected by the same structure.
- Media preservation: existing video/poster/image refs, review cards, and screenshot modal/lightbox still work.
- Visual QA: long step sequences wrap or remain readable; cards are not clipped or reduced to ellipses.
