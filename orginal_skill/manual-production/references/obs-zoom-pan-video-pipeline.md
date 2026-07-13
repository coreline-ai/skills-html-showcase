# OBS Zoom/Pan Video Pipeline for Manual Tutorials

Use this reference when Driver.js-style static highlights technically pass but the owner says the video still feels like a slide deck, not a guided screen explanation. The goal is to test whether camera movement improves comprehension before regenerating a full video set.

## When to choose this pipeline

Use OBS zoom/pan when:

- The important learning moment is spatial: start from the full screen, move into a status/amount/record area, then return to context.
- A reviewer explicitly asks for smoother movement, readable zoom, or a more natural screen-recording feel.
- Driver.js popovers are correct but visually too rigid or visually tiring.
- You need a reproducible local POC before committing to all lesson videos.

Do not replace teaching design with camera motion. The storyboard still needs trigger, prerequisite, visible evidence, consequence/branch, and success/stop checks.

## Workflow-ops shape

Treat the first OBS attempt as a workflow run, not an ad-hoc recording:

```text
.hermes/workflows/<topic>-obs-zoom-pan-poc-<timestamp>/
  state.json
  handoff.md
  decisions.md
  evidence/
    verification.md
    ffprobe-*.json
    contact-sheet.png
  logs/
```

Record:

- POC scope and the reviewer questions being tested.
- Exact tool versions and commands used.
- Source page/image path, output video path, poster/contact sheet path.
- Technical QA result, visual QA result, and what remains owner-judged.

## Recommended architecture

1. Build a stable 1920×1080 tutorial frame or live browser scene.
2. Capture or feed it into OBS as a scene source.
3. Control scene-item transforms with `obs-websocket` from Python.
4. Use smooth easing for position/scale changes.
5. Record to MOV/MP4, then transcode to web-friendly H.264 MP4 if needed.
6. Extract poster/contact sheet with `ffmpeg` for visual QA.
7. Serve a review page with video, contact sheet, and explicit review criteria.

For a bounded POC, it is acceptable to render a verified HTML frame to an image first, then use OBS `image_source` for deterministic zoom/pan. This isolates the camera-motion question from browser-rendering variability. If the final production requirement is live UI interaction, run a second POC with the live capture path after the camera style is approved.

## Motion defaults for a first POC

- Canvas/output: 1920×1080, 30 fps.
- Start with 2–3 seconds of full-screen context.
- Use cosine/ease-in-out transitions, not linear jumps.
- Keep each focus phase around 3–5 seconds for readability.
- Zoom only enough to make the text/check area readable; avoid aggressive scale changes.
- End with a zoom-out/context hold so the viewer can re-orient.

Example phase sequence:

```text
overview hold → zoom into status/check area → zoom into identifier/amount/date → pan to related evidence → zoom out → final hold
```

## Five-stage QA

Before asking the owner to judge quality, record these separately:

1. **Technical QA** — OBS started, websocket responds, recording file exists, ffprobe metadata correct, browser playback succeeds.
2. **Placement QA** — camera visits the intended screen regions in the intended order, and every highlight aligns to the actual visible row, cell, card, control, or diagram region. Prefer DOM/CSS-derived outlines or generated scene overlays over hand-tuned floating boxes when the source is HTML.
3. **Visual QA** — text remains readable, motion is not dizzying, important context is not cropped too early, and camera transforms do not introduce black margins or hide the explanatory caption.
4. **Teaching QA** — movement supports the planned teaching point; it does not merely decorate the screen. A zoom/pan clip still fails if it only moves between highlighted areas without explaining why the viewer should care, what decision they can make, or when they should stop.
5. **Operator QA** — owner or target reviewer decides whether this direction is better than the previous video style.

Use precise verdicts such as `PASS_BOUNDED_FOR_USER_REVIEW`; do not claim full pipeline success when only a POC proved camera motion.

## Teaching-first revision pattern after owner feedback

If the owner says the OBS POC is "just zooming in/out" or that highlights are not aligned, revise the representative POC before scaling to all videos:

1. Write a short teaching revision plan: behavior goal, target viewer, scope, Must-Know / Nice-to-Know / Danger, and a 6–8 scene storyboard.
2. Replace arbitrary overlay coordinates with region-based highlights: full row, specific ID/status/value cell, right-side explanation card, caution card, or other learner-facing evidence region. If using HTML frames, generate scene-specific screenshots with CSS state classes so the highlight geometry is tied to the rendered DOM.
3. Add visible scene captions that teach operational meaning: trigger/context, what the highlighted evidence proves, what downstream decision follows, and the stop boundary. Do not narrate obvious UI mechanics.
4. Keep the camera movement context-preserving. When captions and surrounding evidence matter, use a mild push-in/pan rather than an aggressive crop that makes the highlight readable but removes the explanation. Black margins or missing captions are visual QA failures.
5. Verify with a contact sheet before presenting the new review page: highlights should align, captions should be visible in each sampled frame, and the sheet should show a teaching sequence rather than only camera motion.

## Common pitfalls

- **Starting with tool installation instead of review criteria.** Define what the POC must prove first: smoother entry from whole screen, readable zoom, less dizziness, and whether it beats the existing style.
- **Treating a successful render as teaching success.** Motion can pass technical QA while still teaching nothing.
- **Using camera movement as a substitute for instruction.** If the clip only zooms into boxes, it is still a recognition clip. Add scene captions that explain evidence, consequence, branch/next decision, and stop checks.
- **Hand-tuned highlight boxes drifting off target.** Misaligned boxes damage trust. Anchor highlights to actual DOM regions, scene screenshots, or measured element rectangles; verify with a contact sheet at the final video resolution.
- **Over-zooming until the explanation disappears.** A readable cell is not enough if the caption, row relationship, or right-side decision card is cropped away. Prefer mild context-preserving motion when teaching text and surrounding evidence are part of the point.
- **Regenerating every lesson before owner review.** Make one representative POC first, then scale only after approval.
- **Hard-coding session routes/selectors into the skill.** Keep project-specific choreography in the project run folder; keep this reference generic.
- **Letting tool details leak into the learner manual.** OBS, websocket, ffmpeg, and workflow-run notes belong in evidence/handoff, not user-facing tutorial pages.
