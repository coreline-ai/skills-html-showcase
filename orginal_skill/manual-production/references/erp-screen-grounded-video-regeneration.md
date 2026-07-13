# ERP Screen-Grounded Video Regeneration Pattern

Use this when a reviewer says a manual video is a “sample explanation” rather than a real feature/workflow explanation.

## Trigger

Apply this pattern when a rendered tutorial technically works but fails content review because it:

- explains a mock/sample table instead of the real application screen,
- narrates generic workflow ideas instead of visible field/value evidence,
- points at many areas without completing a concrete operator judgment,
- uses terms like “flow,” “representative path,” or “document relationship” without a next action.

## Correction pattern

1. **Do not start by re-rendering.** First write or update `shot_spec.yml`.
2. **Bind every scene to a real screenshot or live screen region.** For ERP/admin documents, split tall pages by operational regions such as Header, Details, Items, Totals, Activity, and Final Decision.
3. **Use the field/value/action contract:**
   - business purpose,
   - screen evidence,
   - visible field/value,
   - value impact,
   - next judgment/action.
4. **One scene, one judgment.** A comparison scene may use two values only when the judgment depends on comparing them, such as `Grand Total` vs `Outstanding Amount`.
5. **End with a reproducible operator decision.** Example shape: if `Outstanding Amount` is `0`, do not create a new payment entry; if supplier/item/amount differs, stop before payment confirmation.

## Practical rendering approach

For an owner-quality direction check, it is acceptable to create deterministic 1920×1080 scene frames from the real screenshot and assemble them into MP4 before investing in live OBS/websocket capture. Record the caveat clearly:

- `PASS_BOUNDED_FOR_OWNER_REVIEW` means the screen-grounded teaching direction and local playback were verified.
- It does **not** prove the final live OBS recording pipeline or public deployment.

This frame-first approach is useful when the immediate question is content quality, not capture mechanics.

## Verification checklist

- `shot_spec.yml` exists and has zero gate errors.
- Video is 45–90 seconds unless a different duration is justified.
- ffprobe confirms H.264, target resolution, duration, and framerate.
- Review page references are present; no missing `src`, `poster`, or image refs.
- Browser video smoke confirms `readyState`, duration, dimensions, and `media error: null`.
- Contact sheet visually confirms highlight alignment, readable captions, no black margins, and one primary focus per scene.
- Final report separates technical playback, teaching/content QA, owner-quality review, and public deployment status.

## Pitfalls

- Do not call a deterministic frame assembly “OBS proof.” It is a bounded content-quality POC unless OBS was actually run.
- Do not preserve old sample/mock wording after swapping in a real screenshot; every sentence must name a visible value or its consequence.
- Do not treat “screen recognition” as success. The user must be able to repeat the same business judgment on the real screen.
