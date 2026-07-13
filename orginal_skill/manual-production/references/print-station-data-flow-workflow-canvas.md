# Print Station/PipeMaster data-flow workflow canvas pattern

Use this when a user says the Workflow Map should follow the Print Station/PipeMaster sample rather than a normal card board.

## Core correction

Do **not** start by explaining menus one by one. Start with the real job/event flow, then show which functions/menus participate in that flow.

The target interaction model is:

1. **Flow-first selector** — the learner chooses a `data-flow`/job event such as:
   - 자재가 들어왔을 때
   - 자재가 나갔을 때
   - 새로 주문할 때
   - 고객 요청/견적
   - 주문 확정
   - 납품/청구
   - 구매 요청
   - 입고/매입
   - 재고 이동
2. **Function/menu inventory by category** — keep all relevant functions visible, grouped into columns. Examples:
   - Print Station/PipeMaster: 현황 조회, 작업 등록, 데이터 관리, AI/자동화, 팀 협업/저장
   - ERP/admin: 기준 정보, 판매 문서, 구매 문서, 재고 문서, 회계/결제, 조회/출력
3. **Flow participation state** — when a flow is selected:
   - participating menu/function nodes are highlighted;
   - non-participating nodes remain visible but dimmed;
   - the selected menu/function can have an additional selected ring.
4. **Menu-to-menu connectors** — draw one numbered arrow/curve for each step from the participating source node to the next node so the learner sees how the work moves, not merely which screens exist. Prefer the arrow-badge-only pattern: the number sits on the connector, not inside the node.
5. **Two kinds of detail** — keep these separate:
   - workflow detail: trigger, input, stages, checks, risk boundary;
   - menu/function detail: what this menu does and which flows use it.
6. **Flow-scoped lesson/video** — videos and lesson frames should follow the selected flow across multiple menus/functions. Do not make the video focus on one menu if the actual task crosses Quotation → Sales Order → Delivery Note/Sales Invoice → Payment Entry, or request → purchase order → receipt → invoice.

## Anti-patterns

- Rewriting card copy to mention input → output while retaining a simple grid of abstract cards.
- Putting bare step numbers or `기준`/`결과` chips inside nodes when the number actually describes the connector/transition.
- Treating Workflow Map as a menu glossary.
- Making a video for a single menu while the chosen job spans multiple screens.
- Mixing workflow explanation and menu explanation into one panel so the learner cannot tell “what job am I doing?” from “what does this screen do?”
- Hiding non-participating nodes completely; dimming is better because it teaches the whole operating surface and the selected path at the same time.

## Implementation checklist

- Data model includes `PACKAGES`/menu nodes with `id`, `cat`, `name`, `desc`, optional `tags`.
- Data model includes `WORKFLOWS`/flows with `id`, `name/label`, `summary/copy`, `nodes`, ordered `steps` or `edges`, checks, risks, default lesson.
- DOM has a column canvas, an SVG arrow overlay, flow selector pills/chips, workflow detail panel, and menu detail panel.
- Selecting a flow updates: active pill, sequence/strip, highlighted/dimmed nodes, arrows, workflow detail, default menu detail, lesson tabs, and learning stage.
- Selecting a menu updates only the menu detail/selected ring unless intentionally changing the flow.
- Arrow-badge-only mode has no node-step chip elements; verify connector paths, connector badges, and detail steps have the same count and sequential numbering. See `references/arrow-badge-workflow-canvas.md`.
- Verify with browser probes: node counts, active/dim counts, arrow count, flow state, menu state, lesson state, console errors.
- Visual QA must inspect the canvas: columns readable, dim/highlight legible, arrows visible, no major overlap, detail/menu cards populated.

## ERPNext mapping example

Flow `고객 요청/견적`:

- nodes: Lead, Customer, Item, Price List/Terms, Quotation, Sales Order, Delivery Note, Sales Invoice, Payment Entry, Reports/List
- edge/path: Lead → Customer → Item → Price List/Terms → Quotation → Sales Order → Delivery Note → Sales Invoice → Payment Entry → Reports/List
- lesson: selling-flow should teach the cross-menu flow, not only Quotation or Sales Order individually.

Flow `구매 요청`:

- nodes: Supplier, Item, Material Request, Purchase Order, Purchase Receipt, Purchase Invoice, Payment Entry, Reports/List
- edge/path: Supplier/Item → Material Request → Purchase Order → Purchase Receipt → Purchase Invoice → Payment Entry → Reports/List

## Verification note

A PASS for this pattern means the interaction model is present and verified from the primary `index.html` shell. It does not automatically prove all future videos have been re-authored to full flow scope; report video coverage separately if only the map shell changed.