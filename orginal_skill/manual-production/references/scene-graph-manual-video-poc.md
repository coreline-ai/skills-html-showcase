# Scene-Graph Manual Video POC Pattern

Use this when a manual/tutorial video remains too rigid, slide-like, generic, or visually repetitive after basic Driver.js/static-render improvements, and the owner asks for a small regenerated sample before committing to a full batch.

The reusable lesson: a stronger manual video is not mainly a better render script. It needs an editable **scene model** that binds each scene to purpose, source evidence, layout, focus target, copy, and verification gates.

## When to apply

Apply this pattern when:

- Existing clips technically render but feel like repetitive slides.
- One screenshot/source is being reused for scenes that should show different document states or screens.
- The user asks to fix shortcomings and regenerate **one representative video** before scaling.
- You need a bridge between simple Playwright/ffmpeg renders and a fuller Remotion/TTS/SRT production system.

Do not apply this as a full-batch default. First create one representative POC, verify it, then ask/record whether the direction should expand.

## Required artifacts

Create these before or alongside rendering:

1. `shot_spec.yml` — user goal, audience, completion test, scene list, quality gates.
2. `scene_graph.json` — editable scene model, not just generated HTML.
3. Render source, e.g. `index.html` or a Remotion composition.
4. Contact sheet/key frames for visual QA.
5. Verification note/evidence record.

A minimal scene object should carry:

```json
{
  "id": "submitted_state_check",
  "layout": "status_gate",
  "source": "submitted-document-screenshot.png",
  "purpose": "Decide whether the document is ready for the next workflow step",
  "visible_evidence": ["Submitted badge", "Document ID"],
  "focus": { "x": 0.42, "y": 0.18, "w": 0.22, "h": 0.10 },
  "copy": {
    "heading": "Submitted 상태 확인",
    "body": "상단 상태가 Submitted이면 다음 문서로 넘어갈 수 있습니다. Draft이면 먼저 제출 상태를 확인해야 합니다."
  },
  "viewer_action": "상태 배지와 문서 번호를 확인한다",
  "fail_if": ["field_not_visible", "generic_copy", "wrong_source_screen"]
}
```

## Production rules

- Preserve existing public filenames and HTML references if the sample is replacing a currently linked video; keep old outputs backed up separately.
- Use multiple source screenshots/screens when scenes discuss different states, downstream documents, or reports. Do not reuse a single source screenshot for every scene if the explanation crosses documents.
- Vary layouts only when the variation improves teaching: e.g. lens/crop for small fields, comparison for before/after or document relationship, status gate for a state decision, closing check for operator stop/continue criteria.
- Keep the left/system side grounded in real screenshot/live-capture evidence. Current-render callouts, dimming, arrows, cursor markers, and focus boxes are allowed if they point to visible evidence and do not replace the explanatory panel.
- Replace internal layout labels or production terms before rendering user-facing frames. Terms such as `POC`, `scene graph`, `handoff`, `internal`, `blocked`, `peer`, renderer names, or workflow run labels should not appear in the learner-facing video.
- If using deterministic Playwright HTML -> PNG frames -> ffmpeg MP4, report it as a bounded deterministic POC. Do not imply it has the same fidelity as live recording, TTS, or Remotion unless those were actually used.

## Verification gates

Run these before reporting success:

1. **Schema/artifact gate** — `shot_spec.yml` and `scene_graph.json` exist and describe the rendered scenes.
2. **Source gate** — every scene uses the intended raw/source screenshot for its state/document; no scene falls back silently to the wrong generic source.
3. **Focus gate** — contact sheet/key frames show the focus/crop target on the actual field or region claimed by the copy.
4. **Copy gate** — visible user-facing text contains no internal process terms and no abstract claims without visible evidence.
5. **Media gate** — `ffprobe` confirms codec, resolution, FPS, and duration; browser playback reports ready state, dimensions, and no error.
6. **Sync gate** — if copied into a public/staging package, hash-check the showable artifact and deploy package copy so stale videos are not served.
7. **Deployment boundary gate** — local regeneration PASS is not production deployment PASS. State clearly whether public hosting was updated.

## Reporting shape

Report conservatively:

- What changed in the sample.
- Where the regenerated sample lives.
- What was verified.
- What improved compared with the previous version.
- What remains out of scope: full batch conversion, production deployment, live recording, narration/TTS/SRT, or Remotion migration.

Suggested status labels:

- `LOCAL_VIDEO_REGENERATED_NOT_DEPLOYED`
- `POC_VERIFIED_LOCAL_ONLY`
- `READY_FOR_OWNER_DIRECTION_ON_BATCH_EXPANSION`

## Scaling decision

Only after the owner accepts the representative sample should you regenerate the rest of the batch. When scaling, turn the one-off scene graph into a manifest-driven generator rather than copy-pasting per-video scripts.