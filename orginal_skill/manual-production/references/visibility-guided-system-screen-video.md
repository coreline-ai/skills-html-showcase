# Visibility-Guided System-Screen Videos

Use this when a manual video uses a split layout: real application screen on the left and a learner explanation panel on the right.

## Core lesson

Do not interpret “left side is the system screenshot” as “no visual teaching aids.” The important boundary is **source truth**, not visual austerity:

- Left side must remain based on raw application screenshots or verified live captures.
- Right side remains the main explanatory panel.
- Left side may include concise learner-facing visual guidance when it improves readability.

## Allowed left-side guidance

Allowed when tied to visible screen evidence:

- zoom-in / zoom-out phases;
- pan or crop emphasis;
- dim overlay behind the target;
- focus rectangle or spotlight;
- cursor, pointer, ripple, or click marker;
- arrow pointing to the visible target;
- short callout label naming the visible value or area.

Keep callouts short. They should answer “where should I look?” not duplicate the right-panel lesson.

## Still forbidden

- Reusing an already-composited tutorial frame as the left source.
- Prior Driver.js popovers or previous explanation panels baked into the source screenshot.
- Contact sheets, posters, review-card images, or QA images as source evidence.
- Watermarks or production/debug labels.
- Long explanatory paragraphs on the left that compete with the right panel.
- Claims in callouts that are not visible in the left screenshot.

## Recommended render pattern

1. Build a shot spec before rendering: scene goal, raw screenshot path, visible value, focus target, right-panel purpose/impact/action.
2. Whitelist sources to raw screenshots/captures only.
3. Render each scene in short phases, for example:
   - full context frame;
   - slight zoom;
   - dim + focus box;
   - cursor/callout hold;
   - settle frame.
4. Keep total clip length in the planned teaching range; do not let motion replace instructional substance.
5. Generate contact sheets from representative guided frames, not only first frames.
6. Sync every delivery/staging path that may be reviewed.
7. Verify hashes and remote playback after deployment.

## QA checklist

- [ ] Source image path is a raw screenshot/live capture, not a composited tutorial artifact.
- [ ] Left guidance makes the target easier to see at normal viewing size.
- [ ] Callout/cursor/highlight points to the same visible value named in the right panel.
- [ ] Guidance does not hide the evidence needed to understand the screen.
- [ ] Right panel still carries the full purpose, impact, and next-action explanation.
- [ ] Contact sheet visually confirms the pattern across topics.
- [ ] Public/staging copies hash-match the regenerated local outputs before deployment.
