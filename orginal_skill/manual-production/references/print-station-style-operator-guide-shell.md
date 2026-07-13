# Print Station-style operator guide baseline

Use this when a tutorial HTML page feels like an early static document even though the user expects a polished, showable operator guide like the Print Station admin manual.

**Current baseline:** Print Station style means the full learning package, not just a nicer shell: `operator-guide shell` + `Driver.js guided video` + `video-grid/note-card lesson layout` + `review-card grid` + `review-card screenshot enlargement/lightbox`.

## Trigger signals

- User says the HTML feels too early, too flat, or unlike the previous Print Station manual.
- The page is a vertical stack of headings, screenshots, and video with little navigational structure.
- There are multiple lessons/slices, but no central guide shell tying them together.

## Default artifact structure

Treat this as the default for Print Station-quality showable manuals:

```txt
index.html
  └─ operator-guide shell
      ├─ topbar / hero actions
      ├─ learner-facing summary cards
      ├─ sticky topic pills
      ├─ workflow map with active path
      ├─ detail panel with learner steps
      └─ learning frame
          ├─ lesson video panel
          ├─ right-side note-card stack, usually 3 cards
          └─ review-card grid, usually 3 cards

lesson-*.html
  ├─ video-grid
  │   ├─ video-panel: Driver.js guided MP4/WebM
  │   └─ note-stack: 3 learner notes/warnings
  └─ review-grid: 3 review cards with screenshot + title + explanation + checklist

render-*/index.html
  └─ deterministic Driver.js recording composition
      ├─ real captured screenshot or faithful screen scene
      ├─ data-tour hotspots/selectors
      ├─ dim overlay + highlighted target
      ├─ Korean popover title/description
      ├─ progress text such as 1 / 6
      └─ timed automatic step changes for recording
```

A shell without Driver.js-guided video and review cards is incomplete for this baseline.

## Target shell structure

A Print Station-style operator guide shell usually has:

1. **Topbar / hero** — clear manual title, short learner-facing promise, small actions such as video jump and print.
2. **Status or summary cards** — what the learner is viewing, how to use the guide, what success/confirmation means.
3. **Sticky task/topic pills** — one pill per lesson/workflow, with selected state.
4. **Workflow map** — grouped columns that show the operating path, not just a menu list.
5. **Active path highlighting** — selected lesson highlights only relevant nodes and numbers them in order.
6. **Detail panel** — selected lesson title, explanation, CTA, and 3–5 learner steps.
7. **Learning frame/stage** — selected lesson's video, screenshots, and explanations appear in one stable area.
8. **Common check section** — reusable checks the operator should apply across lessons.

Do not confuse this with owner/QA status cards. All visible copy must remain learner-facing.

## Lesson frame requirements

Each lesson should look and behave like a Print Station lesson page:

- **Video panel**: embedded MP4/WebM with poster, controls, and 16:9 aspect ratio.
- **Guided video content**: Driver.js-style step focus is the default, not an optional polish step. Raw browser navigation recordings are acceptable only as temporary source evidence, not the finished lesson video.
- **Note-card stack**: three short learner-facing cards beside the video. Use these for what to watch, how to interpret the screen, and safety/confirmation notes.
- **Review-card grid**: three cards below the video with focused screenshots/crops, title, plain-language explanation, and checklist bullets. These are user learning cards, not QA cards.
- **Screenshot enlargement**: provide click-to-enlarge/lightbox behavior for review-card screenshots by default in interactive HTML. Do not downgrade this to “only if labels are small”; the learner should be able to inspect the source screen detail whenever a review card is used. Include close/Escape behavior and useful alt/caption text.

## Driver.js recording requirements

For guided videos:

1. Add stable `data-tour` targets or hotspot overlays.
2. Configure Driver.js deterministically: `animate:false`, `smoothScroll:false`, `allowClose:false`, `disableActiveInteraction:true`, hidden navigation buttons, visible progress text.
3. Step copy must be user-facing Korean: what the highlighted area means and what the user should notice.
4. Drive steps from a timer or timeline so recording is reproducible.
5. Verify browser probe/visual QA shows overlay, highlight, popover, and progress text.
6. Use `ffprobe` to confirm MP4/WebM duration, dimensions, and video stream.

See `hyperframes-driverjs-video-pipeline.md` for the generic pipeline.

## Implementation notes

- Preserve existing lesson pages, but use `index.html` as the guide shell.
- If local `file://` rendering makes an `<iframe>` learning frame appear blank, do **not** leave a large empty frame. Either:
  - embed lesson content via `<template>` blocks and swap the active template with JavaScript, or
  - serve the directory over local HTTP and verify the iframe visually.
- Keep a standalone lesson page only if useful for direct links/printing; the primary entry should be the shell.
- Broad full-screen screenshots are okay as context, but pair them with focused crops for labels and menu structure.
- Avoid internal terms in shell labels: no `showable`, `artifact`, `slice`, `phase`, `blocked`, `fixture`, `Playwright`, `ffmpeg`, `peer`, or `Hermes` in visible manual copy.

## Verification checklist

Run both structural and user-facing checks:

- Open the shell in a browser and verify:
  - topbar, summary cards, pills, workflow map, detail panel, learning stage, and common checks render;
  - topic/workflow switching uses one coherent shell state: the sticky flow navigation, workflow map active card, detail panel, lesson tabs, and learning stage all update together;
  - the sticky flow navigation is not just category labels; it shows the selected workflow's path/sequence at a glance while still allowing the learner to switch workflows;
  - when a selected workflow has no produced media lesson yet, the learning stage shows a learner-facing concept/orientation panel or a clearly related completed lesson without future-work/process wording;
  - the learning stage contains a video-grid, note-card stack, and review-card grid when the selected lesson has produced media;
  - videos show Driver.js-style overlay/focus/popover/progress, not only a raw screen recording;
  - review cards contain screenshots, user-facing headings, explanation, and checklist bullets;
  - every review-card screenshot can be clicked/tapped to open an enlarged view or lightbox, and can be closed without breaking the lesson state;
  - the learning stage is populated, not blank;
  - media plays or at least exposes browser video controls;
  - no broken image/media refs or layout collapse.
- Scan visible text, excluding `<script>` and `<style>`, for internal/meta terms.
- Verify all `src`, `poster`, and local `href` references exist and are non-empty.
- Use `ffprobe`/metadata checks for MP4/WebM durations when videos are included.

## Common pitfalls

- **Shell-only imitation.** Topbar/pills/map without Driver.js-guided videos and review cards is still an early draft, not the Print Station baseline.
- **Raw navigation video.** A plain Playwright/browser recording can prove capture works, but the user-facing lesson video should have step focus and explanations.
- **Review cards as status cards.** Review cards should teach screen recognition and checks; do not put QA, progress, or future-work notes there.
- **Leaving progress language in user HTML.** Put QA, caveats, phase status, and next-work plans in `STATUS.md`, `HANDOFF.md`, `qa/`, or `sources/` only.
- **Documenting future work.** If a workflow is not taught yet, omit it or link only to a completed learner-facing lesson.
- **Iframe blankness.** A shell with a blank learning frame looks less complete than a simple page. Always visually inspect the frame area.
- **Over-dense maps.** If the map becomes crowded, reduce active nodes per lesson, raise the responsive breakpoint, or move the detail panel below the map.
- **Tiny UI labels.** Use focused crops or lightbox/zoom patterns rather than relying only on broad screenshots.
