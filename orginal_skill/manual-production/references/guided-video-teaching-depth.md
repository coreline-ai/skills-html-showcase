# Guided Video Teaching Depth for Operator Manuals

Use this reference when a guided tutorial video technically renders and is attached to the right lesson, but the owner or reviewer says it feels too simple, shallow, or unlikely to explain the workflow.

## Core distinction

A topic-fit video can still be too shallow.

- **Recognition clip**: points at screens, fields, rows, buttons, or panels.
- **Teaching clip**: explains the work situation, why the screen matters, what evidence the operator checks, what can go wrong, and where the safe boundary is.

Do not round a recognition clip up to a workflow lesson just because Driver.js highlights are aligned and media files pass ffprobe.

## Required plan before remaking videos

Before regenerating media, write a short video-production plan under the project `sources/` or `qa/` area. For every video, define:

1. **Lesson role** — what job or bounded check the video teaches.
2. **Target depth** — recognition, readiness check, document-chain reading, or transaction execution.
3. **Final boundary** — what the video intentionally does not do.
4. **Scene list** — 8–10 scenes for a normal teaching clip.
5. **Acceptance criteria** — duration, visual evidence, stop checks, and forbidden actions.

## Five-question scene test

Every teaching-depth guided video should answer these five questions across the storyboard:

1. **Trigger** — what work situation starts this check?
2. **Prerequisite data** — which existing record, master data, workspace, or input must be trusted first?
3. **Visible evidence** — which field, row, status, amount, date, or document state proves the point in the captured screen?
4. **Consequence / branch** — what goes wrong if this is wrong, or where does the operator go next?
5. **Success / stop check** — what can the operator safely conclude at the end, and what action remains out of scope?

If a video mostly answers “where is this on the screen?”, classify it as recognition-only.

## Planning checklist for efficient manual videos

The primary goal of a manual video is fast, clear understanding. Prioritize clarity and efficiency over entertainment.

Before building the clip, record these fields in the project video plan:

- **Behavior goal**: what concrete action or judgment the viewer can perform after watching.
- **Target viewer**: beginner, intermediate, or expert; assumed device/environment such as PC, mobile, or offline equipment.
- **Scope**: one video should normally teach only 1–3 major functions or judgments. Split into a series when the topic is too broad.
- **Must-Know**: the minimum the viewer must understand to operate safely.
- **Nice-to-Know**: useful context that should not crowd the core lesson.
- **Danger / caution**: risky actions, common mistakes, and stop boundaries.

Recommended structure:

1. **Intro, 0–10s** — title plus what the viewer will be able to do.
2. **Preparation, if needed** — prerequisites, dummy data, role, environment, or safety assumptions.
3. **Main steps** — step explanation → screen demo/focus → visible result check.
4. **Caution and tips** — common failure or wrong path, then correct check.
5. **Wrap-up** — summary, success check, and next lesson/adjacent workflow.

Production heuristics:

- Apply the **3-second rule**: each scene should reveal its key point within about 3 seconds.
- Use visual hierarchy: make the most important item largest/clearest; keep supporting context smaller.
- Repeat important actions/checks as **overall context → focused highlight** when possible.
- Provide visible captions/subtitles, especially for silent viewing.
- Add progress, chapter, or step indicators for longer clips.
- Use consistent terminology; explain specialist terms the first time they appear.
- Preserve accessibility: strong contrast, readable type, color not as the only signal.
- Version reusable video templates and keep common assets modular.

## Pacing defaults

- Target duration: **45–90 seconds** for a bounded teaching clip.
- Scene count: **8–10 scenes**.
- Scene duration: about **5–7 seconds**.
- Shorter 10–20 second clips are acceptable only as quick recognition/supporting media, not as the primary workflow lesson.
- Full manual videos should usually stay under **3 minutes** when possible; split rather than stretching beyond 7 minutes.

## Driver.js usage

Driver.js is acceptable, but use it as a focus layer, not the lesson itself.

Bad popover pattern:

> This is Customer Name. This is Status. This is Items.

Better popover pattern:

> Customer is the counterparty that later flows into quotation, order, and invoice documents. Compare status, group, territory, and ID before using it; if this is wrong, every downstream document can point to the wrong customer.

Composition side cards should also carry learner context such as `상황`, `왜 중요한가`, `확인 기준`, or `다음 판단` so the video does not rely entirely on a small highlight rectangle.

## ERP/admin boundaries

For ERP/admin manuals, explicitly separate these levels:

- screen recognition,
- prerequisite/readiness check,
- document-chain reading,
- transaction execution,
- posting/payment/accounting/stock mutation.

When the safe fixture does not authorize state changes, keep the video at recognition/readiness/document-chain reading and state the stop boundary in the final scene. Do not imply Save, Submit, Cancel, Amend, invoice, payment, or stock posting happened.

## Verification checklist

A teaching-depth video can pass only when:

- A written plan exists before the regenerated media.
- Duration is roughly 45–90 seconds, unless explicitly support-only.
- Contact sheet shows the planned 8–10 scenes.
- Popovers explain operational meaning, not only UI location.
- The final scene states success and stop boundary.
- Visual QA confirms the popover claims match visible pixels.
- Technical QA confirms media metadata, refs, browser playback, and console health.
- The final report separates `technical/placement PASS` from `teaching-depth PASS`.

## Reporting language

Be precise:

- `PASS for topic placement` means the right video is attached to the right lesson.
- `PASS for teaching-depth guided clip` means the clip also teaches trigger, prerequisite, visible evidence, consequence/branch, and stop check.
- `Not a full transaction walkthrough` should remain explicit when the clip does not execute the workflow end-to-end.
