# ERP Workflow Map Shell Rework

Use this when a user says an ERP/manual index card is too abstract or only answers “what is this flow?” instead of showing how work moves through the system.

## Trigger

- Existing `index.html` or operator-guide shell has flow cards such as Sales, Buying, Stock, but the cards mostly define the concept.
- The user expects a Workflow Map to show the actual business path: what starts the work, which ERPNext documents/screens are used, where it goes next, what result/check proves progress, and which actions are risky.

## Rework pattern

### Card-to-canvas escalation

If the user rejects menu/card-first organization and provides a Print Station/PipeMaster-style workflow canvas as the standard, do not polish the existing cards. Rebuild the Workflow Map around **flow-first selection + category columns + node highlighting + numbered connections**:

- Start with workflow/data-flow choices, not menu explanations. Example ERP flows: `고객 요청/견적`, `주문 확정`, `납품/청구`, `구매 요청`, `입고/매입`, `재고 이동`.
- Keep all relevant menu/function nodes visible in categorized columns such as `기준 정보`, `판매 문서`, `구매 문서`, `재고 문서`, `회계/결제`, `조회/출력`.
- For the selected workflow, highlight participating nodes and dim non-participating nodes instead of hiding the rest of the map.
- Draw numbered SVG connector arrows between the selected workflow nodes so the user sees the order of movement across menus/documents.
- **Use one numbering system per workflow.** The top sequence, canvas arrow badges, workflow-node step chips, workflow aside steps, and per-step checks must share the same step count and order. Do not let a learner see 7 steps in the header, 9 arrows in the canvas, and 5 steps in the aside for the same flow.
- Prefer a single step data shape such as `{from, to, label, note, check}`:
  - top sequence renders from `step.label`;
  - SVG connector/badge renders from `step.from → step.to` in array order;
  - workflow-node chips are derived by grouping step indexes for every active endpoint, e.g. `nodeStepsFor(flow)` from `steps.flatMap([from,to])`;
  - workflow aside renders `step.label + step.note`;
  - checks render as “이 단계에서 확인할 것” from `step.check` using the same step number, not a separate competing list;
  - highlighted/active menu nodes are derived from `steps.flatMap(step => [step.from, step.to])`, not from a separate hand-maintained `nodes` list.
- Show step chips inside active workflow nodes when the canvas itself could otherwise look like a loose category board. Nodes that participate in multiple steps should show multiple chips; inactive/dimmed nodes should not carry misleading step chips.
- Treat **count consistency** and **content alignment** as separate gates. Equal counts prove the numbering system is synchronized; they do not prove the highlighted menus, connector path, node chips, and aside prose describe the same workflow.
- Do not make the numbered path sound like the only mandatory execution route. Label it as a representative/checking path, and add branch/entry examples for real work that starts later or skips earlier documents (for example, an existing customer order starting at Sales Order, or a receivables check starting at Sales Invoice/Payment Entry).
- Split the aside into two separate learner-facing panels: one for the selected workflow path and one for the selected menu/function node. Do not collapse menu definition and workflow explanation into one card.
- Keep lessons at workflow level. For Selling, the lesson should remain `고객 요청/견적 → Quotation → Sales Order → 납품/청구/결제 확인`, not a single-menu Quotation or Sales Order explainer.
- Preserve verified media and interactions while replacing the map shell: video/poster refs, review-card grid, screenshot enlargement modal, topbar/summary/common sections, and flow-to-lesson sync.

1. Read the project’s workflow structure sources before editing visible HTML.
   - Example ERPNext sources: `sources/erpnext-business-flow-structure.md`, step-plan YAML, and relevant track docs such as quotation/order, invoice/payment, purchase order, and stock entry notes.
   - Treat upstream/official docs as terminology support, but keep user-facing copy grounded in the project’s approved manual boundaries.
2. Rewrite each `flows.<key>` object as an operating path, not a definition:
   - `trigger_input`: e.g. customer quote request, customer PO, internal material need, item/warehouse movement need.
   - `prereq/master data`: Customer/Lead, Supplier, Item, Price List, Terms, Warehouse, delivery/payment basis.
   - `transaction documents`: Quotation, Sales Order, Material Request, Purchase Order, Stock Entry, etc.
   - `downstream boundary`: Delivery Note, Sales Invoice, Purchase Receipt, Purchase Invoice, Payment Entry, reports/lists.
   - `check/result`: status, remaining delivery, remaining billing, receivable/payable, stock balance, related reports.
   - `risk boundary`: Save/Submit/Delivery/Invoice/Payment/Stock changes affect operating data, stock, or accounting.
3. Add a compact visible mini-flow inside each card.
   - Shape: `trigger → document(s) → next/check`.
   - Keep it short enough for the card: e.g. `고객 견적 요청·PO → Quotation → Sales Order → 납품·청구·결제 확인`.
4. Rewrite detail-panel sections:
   - `흐름 단계` should be a procedure in order, not concept definitions.
   - `확인 지점` should name concrete documents, statuses, residual quantities/amounts, and lists/reports.
   - `주의 경계` should be user-relevant risk, not project/QA/process language.
5. Apply the same philosophy to adjacent flows even if the primary complaint is Selling.
   - Buying: `필요 품목·수량 → Material Request → Purchase Order → 입고·매입·지급 확인`.
   - Stock: `Item·Warehouse → Stock Entry 또는 실사 조정 → 수량·창고·리포트 확인`.
6. Preserve previously verified shell behavior:
   - flow selection updates top strip, Workflow Map active card, detail panel, lesson tabs, and lesson stage together.
   - existing lesson video/poster/image refs remain unchanged.
   - review-card grid and lightbox/capture modal still work from the primary shell.

## Forbidden and low-value visible copy

For user-facing tutorial HTML, scan visible text separately from raw JS/CSS. Do not expose internal production or coordination language such as:

- `source of truth`, `internal`, `process`, `meta`, `프로세스`, `메타`
- `handoff`, `qa/`, `driverjs-frames`, `showable`, `artifact`, `slice`
- `provisional`, `blocked`, `peer`, `Hermes`

Raw code matches like JavaScript `.slice(...)` are not visible-copy failures, but visible HTML/text nodes are.

Also remove “obvious UI narration” that merely reads the layout back to the learner. Avoid phrases whose only job is to describe screen mechanics already visible in the page, such as:

- “먼저 고릅니다”, “선택한 흐름”, “아래 칸”, “왼쪽”, “오른쪽”, “패널”
- “나뉘어 있습니다”, “진하게 표시됩니다”, “버튼의 위치”, “클릭 경로”

Replace with business meaning and decision criteria:

- entry/branch/skip cases: where this work can start and what may be omitted;
- document/status consequences: what Submit, delivery, invoice, payment, receipt, or stock movement changes;
- concrete pre-action checks: customer/supplier, item, quantity, warehouse, price, terms, outstanding amount, stock balance;
- bounded language: “대표 확인 경로” rather than “must execute step 1→N”.

## Verification checklist

When a card board has been replaced by a canvas, add these checks to the normal shell checks:

- Confirm workflow selection pills exist and update the selected sequence, summary/detail title, highlighted node set, and lesson tabs.
- Confirm category columns render with the expected labels and that the total node count stays stable across flow changes.
- Confirm selected-flow nodes are highlighted and unrelated nodes are dimmed.
- Confirm numbered SVG paths/badges render after initial load and after at least one flow change; redraw on resize if the implementation computes DOM coordinates.
- Confirm numbering consistency for every workflow: `topSteps === arrowBadges === nodeChipsByStepSet === asideSteps`, and if checks are numbered, `checkRows` must match the same step count or be visibly unnumbered/common.
- Run content alignment QA, not just count QA: every highlighted/active node must be an endpoint of at least one rendered step (`activeNodes ⊆ steps.flatMap([from,to])`). Prefer deriving the highlighted node set directly from the step endpoints instead of maintaining a separate `nodes` array that can drift.
- Confirm every active workflow node has at least one visible step chip and that each chip number maps back to a real step endpoint pair. Multi-step nodes may have multiple chips; inactive nodes should not show path chips.
- If a node such as `Sales Invoice` or `Payment Entry` is highlighted, it must appear in the actual connector path and aside step sequence. If it is only a later/adjacent boundary, keep it dimmed and mention it as a separate follow-up boundary in copy instead of implying it participates in the selected path.
- Confirm branching/variant copy exists when the representative path could be mistaken for a compulsory linear procedure, and that it names realistic alternative start points or skip paths.
- Confirm the workflow aside and menu aside are separate, and clicking a node changes only the menu aside unless a workflow change is intended.

Before closeout:

- Serve/open the primary shell (`http://127.0.0.1:<port>/` or equivalent) and confirm 200 OK.
- Check all local `src`/`poster` refs; report total checked and missing count.
- Browser-smoke initial, primary reworked flow, and at least two adjacent flows:
  - summary title
  - top strip title/sequence
  - Workflow Map active card
  - detail title/badge/steps/checks
  - active lesson tab/stage
- For the primary flow, confirm existing video, poster, images, and review-card count are preserved.
- Click at least one review-card image from the primary shell and confirm modal opens with image and caption.
- Check browser console/JS errors.
- Run visible-copy forbidden-term scan.
- Save a QA note under the project’s `qa/` directory with changed files, sources read, verification results, and explicit caveats.

## Closeout caveats

- If the directory is not a git repository, say so and provide a change summary instead of pretending a diff exists.
- Do not round this into full Driver.js/video PASS unless representative video frames and highlight coordinates were freshly inspected.
- Report the bounded verdict: workflow-map shell/content synchronization and references/modal/copy checks only.
