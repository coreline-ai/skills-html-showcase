# Screen-Grounded Purpose-Complete Video Gates

Use these gates when planning or regenerating manual/tutorial videos after a reviewer says the clip is too generic, too abstract, visually hard to follow, over-explanatory, or not purpose-complete.

The problem is usually not video rendering. The problem is whether each scene completes a user-facing business judgment from visible screen evidence.

## Core scene contract

Every scene must follow this chain:

```text
business purpose -> screen evidence -> visible value/input -> value impact -> next judgment/action
```

If `screen evidence` or `next judgment/action` is missing, the scene becomes generic narration.
If `value impact` is missing, the scene becomes screen reading.
If `business purpose` is missing, the scene sounds like the model explaining its own analysis process.

Weak pattern:

> Review the representative path and document impact relationship.

Why it fails:
- It does not tell the viewer what to do.
- It does not bind to a visible field/value.
- It has no next judgment or action.
- It sounds like internal analysis language.

Good pattern:

> To decide whether this Purchase Invoice still needs payment, compare the top `Paid` badge with `Outstanding Amount KRW 0.00`. Because the outstanding amount is zero, no additional payment entry is needed for this invoice.

Why it passes:
- Purpose: decide whether payment is still needed.
- Screen evidence: `Paid` badge and `Outstanding Amount` field.
- Visible values: `Paid`, `KRW 0.00`.
- Impact: no remaining unpaid balance.
- Next action: no additional payment entry is needed.

## 1. Evidence Binding Gate

Every narration sentence must bind to visible screen evidence.

Allowed:
- `Supplier` is `Zuckerman Security Ltd.`.
- `Outstanding Amount` is `KRW 0.00`, so there is no remaining payment amount.
- `Grand Total KRW 120.00` is the total amount on this invoice.
- If the intended evidence was an activity/history entry but the screenshot only shows a top status badge such as `Submitted`, rewrite the scene to the visible status badge instead of claiming an invisible activity record.

Blocked unless rewritten with visible field/value evidence:
- Understand the workflow.
- Review the document relationship.
- Check the representative path.
- Identify the necessary information.
- Use this for operations.

A sentence may include background only if the same scene also points to visible evidence and a next judgment/action.

## 2. Human Visual Limit Gate

A scene must be readable by a human watching at normal speed.

Minimum rules:
- One primary focus per scene; two at most if they are directly compared.
- Highlighted text must be enlarged or cropped enough to read.
- One scene should teach one judgment only.
- Do not explain multiple tiny table cells at once.
- Do not narrate the key judgment while the camera is moving; move first, stop, then explain.
- For tall ERP/admin screens, split by real screen regions such as `Header -> Details -> Items -> Totals -> Activity` instead of showing the full page while explaining everything.

Fail examples:
- Full-page ERP screenshot plus narration about supplier, items, totals, and activity all at once.
- A camera pan that explains the key field while the field is blurred or moving.
- A highlight box around a dense table while the narration names several different columns.

## 3. Purpose Completion Gate

A video must end with a concrete user capability, not a topic label.

Weak goal:

> Explain the Purchase Invoice screen.

Strong goal:

> The viewer can confirm supplier, billed item, total amount, outstanding amount, and decide whether additional payment is needed for a submitted Purchase Invoice.

Every video/shot spec should include a `completion_test` block, for example:

```yaml
completion_test:
  viewer_can_identify_supplier: true
  viewer_can_identify_invoice_id: true
  viewer_can_explain_paid_state: true
  viewer_can_find_outstanding_amount: true
  viewer_knows_next_action_if_outstanding_is_zero: true
```

Do not pass a video whose completion test only says the viewer can “understand the flow” or “recognize the screen.”

## 4. Anti-Generic Language Gate

Flag these phrases when they appear alone or without visible fields/values:

- 흐름을 확인합니다
- 대표 경로를 봅니다
- 문서 관계를 이해합니다
- 문서 영향 관계를 봅니다
- 상태를 파악합니다
- 필요한 정보를 확인합니다
- 업무에 활용할 수 있습니다
- 전체 구조를 이해합니다
- 기준을 살펴봅니다

Rewrite into field/value/action language:

- `Grand Total KRW 120.00` is the total billed amount on this invoice.
- `Outstanding Amount KRW 0.00` means there is no remaining payment amount.
- If supplier or item differs from the real transaction, stop before payment processing.

## 5. Over-Explanation Gate

Beginner-friendly does not mean encyclopedia-style explanation.

Bad:

> Purchase Invoice is an important document connecting purchasing transactions and accounting processes in ERPNext, and it participates in the organization's financial flow...

Better:

> This screen shows what the supplier billed and whether any payment remains.

Prefer judgment support over conceptual exposition. Explain only what helps the viewer decide the next action from the visible screen.

## Required intermediate artifact: shot_spec.yml

Before rendering a non-trivial manual video, produce a shot spec and gate it before video generation.

Recommended shape:

```yaml
video_goal: "Purchase Invoice paid-state check"
audience: "Beginner ERP operator"
completion_test:
  viewer_can_identify_supplier: true
  viewer_can_identify_invoice_id: true
  viewer_can_explain_paid_state: true
  viewer_can_find_outstanding_amount: true
  viewer_knows_next_action_if_outstanding_is_zero: true
scenes:
  - id: totals_paid_check
    purpose: "Decide whether additional payment is needed"
    visual_target:
      fields:
        - "Paid badge"
        - "Grand Total (KRW)"
        - "Outstanding Amount (KRW)"
    visible_values:
      - "Paid"
      - "Grand Total KRW 120.00"
      - "Outstanding Amount KRW 0.00"
    narration:
      ko: "Grand Total은 총 청구액이고, Outstanding Amount는 아직 지급해야 할 잔액입니다. 이 화면은 Outstanding Amount가 KRW 0.00이므로 추가 지급이 필요하지 않습니다."
    viewer_action: "Outstanding Amount가 0인지 확인한다."
    fail_if:
      - field_not_visible
      - no_next_action
      - abstract_language
      - too_many_focus_targets
      - narration_during_camera_motion
```

## Final success criterion

The success criterion is not a pretty video. It is:

> After watching, can the user reproduce the same judgment on the real screen?

If the answer is no, the video is still a recognition/sample clip, not a purpose-complete manual video.
