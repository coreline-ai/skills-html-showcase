# HyperFrames + Driver.js Tutorial Video Pipeline

Use this reference when a manual needs guided tutorial videos, especially operator/admin walkthroughs.

## Tool roles

- **HyperFrames**: deterministic HTML/CSS/JS composition, timeline, layout lint/inspect/snapshot, base render.
- **Driver.js**: runtime guidance layer: highlight cutout, overlay, popover title/description, step progress.
- **Playwright**: real browser verification and recording, especially when Driver.js or real app pages are involved.
- **ffmpeg/ffprobe**: convert WebM to MP4, extract frames/contact sheets, verify duration/dimensions/fps.

## Prerequisites to expose to users

```bash
node --version
npm --version
npx --yes hyperframes@0.6.33 --help
npx --yes hyperframes@0.6.33 doctor
npx playwright --version
ffmpeg -version
ffprobe -version
```

If missing, the agent should guide installation using the user's OS/package manager. Do not silently skip video verification.

## Manifest-driven inputs

Keep the pipeline portable by reading from a manifest instead of hard-coding a product:

```yaml
videos:
  - id: basic-navigation
    lesson_id: V1-01
    title: "기본 화면 이동"
    mode: driverjs-browser-recording # or hyperframes-only
    viewport: { width: 1920, height: 1080 }
    duration_seconds: 18
    entrypoint: media/compositions/basic-navigation/index.html
    output: media/videos/basic-navigation.mp4
    poster: media/posters/basic-navigation.png
    contact_sheet: media/review/basic-navigation-contact-sheet.jpg
    forbidden_terms: [DB, API, cache]
    steps:
      - selector: '[data-tour="workspace"]'
        title: "Workspace"
        description: "업무 영역을 먼저 확인합니다."
```

## Deterministic Driver.js pattern

- Add stable selectors such as `data-tour="workspace"`.
- Use `animate: false`, `smoothScroll: false`, `allowClose: false`, `disableActiveInteraction: true`.
- Hide navigation buttons for recorded videos: `showButtons: []`.
- Drive active step from a timeline or deterministic timer.
- Expose probe handles such as `window.__operatorGuide` and `window.__syncOperatorGuide`.

## Verification gates

Minimum gates before claiming a video is done:

1. HyperFrames lint/inspect passes for composition-based videos.
2. Browser probe confirms Driver.js overlay/popover appears at representative times.
3. Browser console/page errors are empty.
4. ffprobe confirms MP4 duration, dimensions, fps, and codec.
5. Contact sheet/key frames are visually reviewed for clipping, unreadable text, wrong focus, and impossible states.
6. Lesson HTML embeds the actual MP4 and browser playback reports `readyState >= 2`, expected dimensions, `error === null`, and advancing `currentTime`.
7. Content QA confirms the video teaches the approved workflow, not just that it rendered.

## Keep project-specific

Do not put these in the portable skill unless manifest-parameterized:

- Login credentials and authentication flows.
- Product-specific routes and menu names.
- CSS selectors that only exist in one app.
- Fixture creation/destructive actions.
- Brand-specific visual style.
- Local filesystem paths.
