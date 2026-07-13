# Pure System-Left Video Contract

Use this when a manual/tutorial video uses a split layout: system screen on the left and learner explanation on the right.

## Trigger

Apply this when the owner says the left side should be the 업무화면/system screen and the right side should be step explanation, or when prior generated videos reused screenshots that already contained guidance overlays.

## Contract

- **Left side = pure application/system screenshot only.**
- **Right side = all step explanation, purpose, value, impact, and next action.**
- Do not reuse any image/frame on the left if it already contains:
  - Driver.js popovers or step counters
  - explanatory callouts, captions, badges, watermarks, or learner panels
  - highlight rectangles/arrows added by a previous manual/video pass
  - contact sheets, posters, or frames extracted from an already-composited video
  - prior review-card or tutorial screenshots with annotations baked in

If the left screenshot needs visual focus, prefer cropping/zooming a raw system screenshot rather than adding learner-facing annotations onto the screenshot itself. Keep explicit teaching text in the right panel.

## Source hygiene checks

Before rendering:

1. Create or update a shot spec that records each scene's image source.
2. Whitelist raw source directories such as `screenshots/**` or another project-specific raw-capture directory.
3. Block generated/composited directories and filenames such as `driverjs`, `video-frames`, `contact`, `poster`, `screen-grounded`, `review`, or prior `scene-*` outputs unless they are explicitly raw captures.
4. Fail fast if any source image is missing or comes from a generated/composited directory.

## Staging/deploy copy checks

When existing filenames are preserved, source replacement alone may not update every place the user reviews:

- compare the canonical artifact directory, local public/staging deploy directories, and any checked-in/deploy package separately;
- copy or sync regenerated MP4s and posters into each local staging package that the user may open;
- verify hashes/mtimes match between canonical and staging copies;
- keep public deployment separate from local staging sync and do not imply external deployment until it is explicitly run and verified.

## Visual QA

For the contact sheet or browser frame, pass only if:

- the left panel shows an unannotated system screen;
- no Driver.js popover, tutorial badge, watermark, or preexisting explanatory overlay is visible inside the left screenshot;
- the right panel contains the learner-facing explanation;
- the final report says whether the public URL was deployed or only local/staging artifacts were updated.
