# Screen-Grounded Batch Video Regeneration

Use this when an existing set of guided/manual videos has already been accepted structurally, but the owner asks to regenerate the set under a stronger screen-grounded teaching standard.

## Trigger

Apply this pattern when:

- existing tutorial videos are too generic, slide-like, or weakly tied to visible screen evidence;
- the owner approves a better representative direction and asks to apply it to previously generated videos;
- multiple existing video filenames are already referenced by HTML pages and should remain stable;
- public deployment must wait until local regeneration and QA are complete.

## Regeneration contract

Before rendering the full batch, define the per-video contract:

1. **Stable output identity** — preserve existing video paths/filenames if HTML already points to them; move previous files to a dated or named backup directory first.
2. **Scene evidence** — each scene binds business purpose → actual screen region/frame → visible field/value → value impact → next judgment/action.
3. **Shot limits** — one or two focus points per scene; pause camera/frame before explaining.
4. **Topic split** — if some topics can use real submitted/document screenshots and others only have older guided frames, separate them and report the evidence-strength difference.
5. **Deployment boundary** — local regeneration PASS is not public deployment PASS. Re-deploy only after explicit approval when the target is externally visible.

## Deterministic frame pipeline

A reliable batch pattern is:

1. Build or update a machine-readable shot spec for each video.
2. Render each scene as local HTML that lays out the verified screen evidence plus a learner-facing explanation panel.
3. Use Playwright/Chromium to capture deterministic PNG frames from the HTML.
4. Use `ffmpeg` concat or image sequence assembly to produce MP4s.
5. Use `ffprobe` to verify codec, resolution, frame rate, duration, and stream health.
6. Produce contact sheets from representative frames for visual QA.
7. Verify the embedding HTML still references existing paths and has no missing assets.

This deterministic pipeline is acceptable when the goal is bounded owner review of screen-grounded explanation quality rather than proving live interaction fidelity. Do not claim it is a live OBS/browser recording unless live recording was actually run.

## Relative asset hardening

When Playwright renders temporary HTML from a generated/source directory, relative image/video paths can silently render as blank in exported frames.

Harden the render HTML by either:

- using absolute `file://` asset URLs, or
- injecting a `<base href="file:///ABSOLUTE/ARTIFACT/ROOT/">` element that points at the artifact root used by the final manual package.

Then regenerate at least one contact sheet and inspect it visually before trusting the batch.

## QA checklist

Minimum local PASS evidence:

- [ ] Previous videos/posters backed up before overwrite.
- [ ] Expected video count matches the approved scope.
- [ ] Output filenames still match existing HTML references.
- [ ] HTML/media reference scan reports zero missing files.
- [ ] `ffprobe` confirms all MP4s have expected codec/resolution/fps/duration.
- [ ] Contact sheet shows actual screen evidence, not blank panels or generic mock placeholders.
- [ ] At least one high-risk/transaction video is inspected individually, not only via the batch sheet.
- [ ] Browser playback smoke succeeds for at least one embedded video: ready state, duration, dimensions, and no media error.
- [ ] Final report separates local regeneration PASS from public deployment/release status.

## Reporting language

Be explicit about evidence strength:

- “Regenerated from real submitted document screenshots” for topics grounded in verified live/demo transaction evidence.
- “Regenerated from existing guided frames under v4 explanation layout” for topics without fresh live screenshots.
- “PASS_BOUNDED_LOCAL_REGENERATION” or equivalent for local replacement only.
- Avoid implying external publication until the deploy step has been approved and verified.
