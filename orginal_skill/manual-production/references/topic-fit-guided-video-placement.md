# Topic-fit guided video placement for showable manuals

Use this when a manual has multiple lesson tabs or standalone pages that share nearby screenshots but teach different jobs.

## Rule

A video belongs to the lesson whose **job boundary** it teaches, not merely to any page that uses the same module or screenshots.

Do not reuse a broad workflow video for a narrow preparation/check lesson. If the learner clicked a narrow topic, the video must open on the same mental model and cover the same screens/checks as that topic.

## Example boundary pattern

- Broad transaction flow video: `Quotation → Sales Order → downstream boundary` belongs to the broad sales/selling-flow lesson.
- Preparation/check video: `Customer list → Item list → Not Saved quotation draft` belongs to the quotation-draft/readiness lesson.
- Master-data video: `Customer/Item/Supplier lists + detail screens` belongs to the master-data lesson, even if some of those screens support a sales lesson.

## Production steps

1. Build a placement map before rendering:
   - lesson/tab id
   - user-facing topic title
   - promised job/check
   - existing or new video path
   - whether the video is broad, narrow, or supporting-only
2. If an existing video is adjacent but broader than the tab, keep it in its broad topic and create a dedicated narrow video for the new tab.
3. Storyboard the narrow video around the tab promise:
   - first screen must match the lesson's starting check
   - middle steps must cover the visible evidence the lesson names
   - final step must stop at the lesson boundary, especially before risky actions such as Save/Submit/Cancel/Amend, posting, payment, stock movement, or external publication
4. Attach the video in both places if the same lesson exists as:
   - embedded primary-shell tab/template
   - standalone lesson page
5. Regenerate WebM/MP4/poster from the corrected source after copy changes. Do not edit HTML copy and leave stale rendered videos.

## Verification checklist

Record evidence under the project `qa/` directory.

- Static refs: every `<video>`, `<source>`, and poster path exists from each HTML entrypoint.
- Media metadata: `ffprobe` confirms duration, codec, resolution, and frame rate for every touched video.
- Browser smoke: open the primary shell, switch to the target tab, and confirm the loaded video `src`, duration, dimensions, ready state, and playback advancement.
- Standalone smoke: repeat for the standalone lesson if it exists.
- Contact sheet or representative frames: visually inspect sequence, screen movement, highlight target, popover copy, and final boundary.
- Content QA: the video claims only visible fields/states/actions, and the topic's broad/narrow scope matches the tab title.
- Forbidden/meta-term scan: visible tutorial text must not expose production terms such as QA, artifact, slice, staging, Driver.js, Playwright, ffmpeg, peer, handoff, or similar internal workflow words.

## Reporting

When reporting to the user, name the visible place where the change can be seen, not only the files changed. For example: `고객 요청/견적 → 견적 초안 준비 탭 now loads the Customer → Item → Not Saved quotation draft video.`