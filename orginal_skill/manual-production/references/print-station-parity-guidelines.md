# Print Station parity guidelines for user-facing manuals

Use this reference when producing showable tutorial/manual artifacts that should match the Print Station manual quality bar.

## Core correction learned

A user-facing manual is not a project status page. Do **not** put agent progress, peer messages, QA status, future work, blocked/final/provisional labels, tooling names, or production caveats into the HTML that an end user will read. Keep those in `STATUS.md`, `HANDOFF.md`, `qa/`, or `sources/` only.

Examples of manual-page text to avoid:
- `showable artifact`, `slice`, `phase`, `closeout`, `peer`, `Hermes`
- `Playwright`, `ffmpeg`, implementation/tooling details
- `아직 하지 않은 것`, `다음 단계`, `not final`, `provisional`, `blocked`
- future-production notes such as “later we will cover this with a safe fixture”

## Print Station quality bar

A Print Station-style manual page has three layers:

1. **Operator guide shell**
   - polished top/header area
   - summary cards
   - topic pills or lesson navigation
   - workflow map / current path
   - detail panel
   - embedded learning frame

2. **Driver.js guided video**
   - not raw screen recording only
   - step-by-step focus rectangles/highlights
   - explanatory popovers in Korean
   - progress indicator such as `1 / 6`
   - automatic step advancement for video capture
   - 16:9, preferably 1920×1080, exported to MP4 with a poster frame

3. **Lesson frame**
   - video panel on the left
   - three note cards on the right
   - three review cards below
   - each review card includes screenshot, title, explanation, and checklist bullets
   - review-card screenshots support click-to-enlarge/modal by default in interactive HTML

## Copy rules

Write for the learner/operator:
- what they see
- where they look
- what each area means
- what to check before proceeding

Do not write for the agent/operator team:
- what we completed
- what is pending
- how the artifact was generated
- what QA found
- which peer did the work

## Verification checklist

Before claiming a manual page is ready:
- scan visible HTML text for forbidden meta/process words
- verify all media/image references exist and are non-empty
- verify MP4/WebM duration and resolution with `ffprobe`
- open the HTML and visually check the shell, video panel, note cards, review cards, and topic switching
- visually inspect at least one Driver.js render page and confirm highlight + popover + step counter are visible

## Artifact organization pattern

Recommended structure:

```text
showable-artifacts/
  index.html                  # operator-guide shell
  lesson-start.html           # lesson frame
  navigation.html             # lesson frame
  render-start/index.html     # Driver.js capture composition
  render-navigation/index.html
  screenshots/...
  video/*-driverjs.webm
  video/*-driverjs.mp4
  video/*-driverjs-poster.png
```

Keep internal working notes out of these HTML pages unless they are hidden implementation comments and not visible to the reader.
