# Showable guided manual baseline

Use this reference when producing a user-facing HTML/manual/tutorial package that should feel like a finished operator guide rather than a static draft. When this reference is exercised on a concrete project, treat the project as a skill-validation case: reusable lessons from owner feedback, QA failures, workflow gaps, or artifact requirements should be folded back into the portable manual-production workflow rather than remaining project-only notes.

If a project reveals a deployment requirement that is not yet covered—verification, packaging, publishing, accessibility, localization, handoff, media QA, or another repeatable concern—promote it into the portable skill package as a required sub-skill, reference, template, script, or CLI hook, then update `manual-production` to call it explicitly. The deployable skill package should accumulate the workflow needed to create manuals, not only the output from the current exemplar project.

Before building per-step pages, complete the manual-level work order:

1. analysis of the real jobs and evidence;
2. structuring of the overall workflow and step sequence;
3. `index.html` shell with the workflow map;
4. per-step plan → production of captures/video/review cards/workflow diagram;
5. verification of the step and shell integration.

Do not let the first deliverable become a shallow navigation tour. For ERP/operator guides, the central artifact is the 업무 단위 flow: what starts the work, what records are created/changed, what the operator checks, and what downstream screen/report confirms completion.

## Baseline structure

A complete showable guided manual uses three layers:

1. **Operator-guide shell**
   - `index.html` is the main guide shell.
   - Include topbar/hero, learner-facing summary cards, sticky topic or lesson pills, workflow map with active path, selected-lesson detail panel, populated learning frame, and common checks.
   - The workflow map must be grounded in actual 업무 단위 flow, not just a menu/screen list. Show how work moves from trigger/input to action, review/approval, output, and follow-up check.
   - Visible copy is for the learner/operator only.

2. **Guided lesson video**
   - Do not use a raw browser recording as the finished default.
   - Use a Driver.js-style guided recording: dim overlay, highlighted target, explanatory Korean popover, progress text such as `1 / 6`, deterministic automatic step changes, and no manual navigation buttons during recording.
   - Export MP4/WebM with poster frames; verify duration and resolution with `ffprobe`.

3. **Lesson review frame**
   - Each lesson frame should use a video-grid layout: video panel on the left and a right-side note-card stack, usually three cards.
   - Add a review-card grid below, usually three cards.
   - Each review card contains a focused screenshot/crop, title, plain-language explanation, and checklist bullets.
   - Review-card screenshots must support click-to-enlarge/lightbox behavior by default, so users can inspect labels and screen details without leaving the lesson. Tighter crops are still useful, but they do not replace enlargement when the artifact is interactive HTML.

## Recommended artifact structure

```text
manual-root/
  index.html                    # operator-guide shell
  lesson-<topic>.html            # lesson frame: video + notes + review cards
  render-<topic>/index.html      # Driver.js recording composition
  screenshots/...
  video/*-driverjs.webm
  video/*-driverjs.mp4
  video/*-driverjs-poster.png
```

## User-facing copy boundary

Manual HTML should explain:

- what the user sees;
- where to look or click;
- what the highlighted area means;
- what to check before continuing.

Manual HTML should not include:

- agent/peer progress;
- QA closeout/status;
- future-work plans;
- blocked/final/provisional labels;
- tooling names or generation details;
- implementation notes that the learner does not need.

Keep those in `STATUS.md`, `HANDOFF.md`, `qa/`, `sources/`, or worklogs.

## Verification checklist

Before claiming a guided manual package is ready:

- Open the shell in a browser.
- Verify topic switching changes active path, detail panel, and learning frame.
- Verify the learning frame contains video panel, note cards, and review cards.
- Verify each review-card screenshot opens in an enlargement/lightbox modal or equivalent zoom view, with keyboard/Escape or close-button dismissal and meaningful alt/caption text.
- Visually inspect Driver.js render compositions at representative steps, not only the first frame. Confirm each highlight is anchored to the actual UI target inside the displayed screenshot/video frame, with the popover and progress text visible.
- When the highlighted target is over an image or screenshot, compute hotspot rectangles relative to the rendered image's natural dimensions and `object-fit` offset/scale. Do not hard-code page coordinates unless the screenshot size and container mapping are fixed and verified.
- Save viewport screenshots for the inspected Driver.js steps, including at least one step per source screenshot/crop family, so highlight placement can be reviewed later.
- Verify local `src`, `poster`, and `href` references exist and are non-empty.
- Verify MP4/WebM duration and resolution with `ffprobe`.
- Scan visible text, excluding `script` and `style`, for internal/meta/process terms.
- Check for broken images, blank iframes, collapsed layout, tiny unreadable labels, and review cards that accidentally contain QA/status language.

## Origin note

This baseline was generalized from the Print Station admin manual pattern. Treat Print Station as an exemplar quality bar, not as a project-specific dependency.
