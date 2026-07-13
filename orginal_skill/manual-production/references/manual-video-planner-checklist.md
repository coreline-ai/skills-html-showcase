# Manual Video Planner Checklist

Use this when planning or regenerating user-facing manual/tutorial videos, especially when a reviewer says the video is too simple, too broad, or not fast enough to understand.

## Primary goal

A manual video exists to make the viewer understand and act as quickly and clearly as possible. Prioritize clarity, efficiency, and safe operation over entertainment.

## Planning fields to record before production

For each video, write these fields in the project plan before rendering:

- **Behavior goal**: after watching, what concrete action, judgment, or check can the user perform?
- **Target viewer**: beginner, intermediate, or expert; role and assumed technical level.
- **Use environment**: PC, mobile, kiosk/offline device, browser, age/accessibility constraints where relevant.
- **Scope**: one video should normally teach only 1–3 major functions or judgments. Split broad topics into a series.
- **Must-Know**: the minimum knowledge needed to complete the task safely.
- **Nice-to-Know**: optional context that helps understanding but must not crowd the main task.
- **Danger / caution**: common mistakes, risky actions, irreversible/state-changing steps, and stop boundaries.

## Recommended structure

1. **Intro, 0–10s** — title plus what the viewer will be able to do.
2. **Preparation** — prerequisites, role, safe/dummy data, environment, or screen state.
3. **Main body** — step explanation → screen demo/focus → visible result check.
4. **Caution and tips** — show or name a likely wrong path, then the correct check.
5. **Wrap-up** — summary, success check, stop boundary, and optional next lesson.

## Clarity heuristics

- **3-second rule**: each scene should reveal its core point within about 3 seconds.
- **Visual hierarchy**: make the most important item largest/clearest; supporting context stays smaller.
- **Repeat emphasis**: important checks should appear as overall context first, then focused highlight.
- **Captions are required**: support silent viewing and reduce reliance on narration.
- **Progress/chapter cues**: use a step counter, progress bar, chapter bar, or section labels for longer clips.
- **Terminology consistency**: explain specialist terms the first time they appear, then reuse the same label.
- **Accessibility**: readable fonts, high contrast, and do not use color as the only signal.

## Production workflow

1. Gather materials: product specs, existing manuals, live UI evidence, and actual user-test pain points.
2. Write scenario: user journey from problem recognition to successful completion.
3. Write script: concise spoken/caption copy; prefer short oral sentences.
4. Storyboard: scene-by-scene screen state, subtitle, focus/highlight, and result check.
5. Prepare capture: clean environment, dummy data, resolution, frame rate, and safe fixture/stop boundary.
6. Edit/render: synchronize video, captions, highlights, and timing.
7. Review: technical QA + visual QA + target-user comprehension check.

## Final QA checklist

- [ ] A beginner in the target environment can follow it.
- [ ] The video has one clear behavior goal and limited scope.
- [ ] Must-Know, Nice-to-Know, and Danger/caution are separated.
- [ ] Unnecessary explanation is removed.
- [ ] Important checks are visually emphasized enough.
- [ ] Captions are readable and aligned with the screen.
- [ ] Audio/narration, if present, matches the visible action.
- [ ] Duration is appropriate: usually under 3 minutes; split before exceeding 7 minutes.
- [ ] Brand/tone/visual conventions are consistent.
- [ ] Risky or state-changing steps have explicit safe fixture or stop-boundary handling.
