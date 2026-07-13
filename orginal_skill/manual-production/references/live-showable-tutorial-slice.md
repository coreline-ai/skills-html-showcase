# Live showable tutorial slice pattern

Use this when the owner clarifies that the desired deliverable is a showable tutorial artifact (HTML/screenshots/video), not a Markdown-heavy planning or provisional package.

## Core lesson

A phase-gated Markdown/pre-capture package can be useful supporting material, but it does not satisfy a showable tutorial goal. When the runtime becomes available, pivot to live UI capture and produce a small visible slice immediately.

## Minimal first slice

1. Verify the live app route returns a real page.
2. Log in only with approved/demo credentials.
3. Complete or bypass setup wizard with conservative demo values when safe:
   - language: English unless localization is being verified;
   - country/timezone/currency: match owner/project locale;
   - demo company and demo data only;
   - no production credentials or real business data.
4. Capture screenshots for:
   - login page;
   - setup wizard values;
   - post-setup home/workspace;
   - one or two safe navigation-only module/workspace screens.
5. Record a short navigation video if browser recording and ffmpeg are available; otherwise record exact blocker and setup path.
6. Build a showable HTML page embedding the screenshots/video under a clearly named directory such as `showable-artifacts/`.
7. Verify all media references exist, the HTML loads visually, and the live app still responds.
8. Update STATUS/HANDOFF so earlier Markdown/provisional material is explicitly demoted to supporting evidence, not the owner-facing deliverable.

## Safety boundaries

- Do not execute destructive ERP/accounting transactions in the first slice.
- Treat Accounting/Selling/Stock screens as navigation evidence only unless a safe fixture and domain boundary are explicitly approved.
- Do not claim final manual completion from a first slice.
- Keep credentials out of screenshots where possible; login screenshots should show pre-fill or non-secret/demo-only context.

## Verification checklist

- `showable-artifacts/index.html` exists and embeds actual captured media.
- Every `img`, `video`, `source`, and poster reference resolves to a non-empty file.
- At least one visual/browser QA pass confirms no broken images or obvious layout collapse.
- Short video has duration and plays in the HTML page.
- STATUS/HANDOFF distinguish:
  - showable artifact produced;
  - old Markdown package as supporting material;
  - not final/full manual;
  - remaining safe-fixture/domain/media expansion work.
