# Media QA Checklist

## Pre-capture gate

- [ ] Capture environment is app-ready in browser.
- [ ] Target version/source recorded.
- [ ] Demo fixture/sample data policy recorded.
- [ ] Risky actions resolved: demo capture / read-only / blocked.
- [ ] No real data visible.
- [ ] Media review card exists.

## Screenshot checks

- [ ] Text is readable.
- [ ] Browser/account/private data is hidden or safe.
- [ ] Labels match actual UI.
- [ ] Screenshot path is recorded in manifest/review card.

## Driver.js checks

- [ ] Selectors are verified in browser.
- [ ] Animations disabled or deterministic.
- [ ] Active step/popover verified before recording.
- [ ] Overlay does not hide critical UI.

## HyperFrames/video checks

- [ ] HyperFrames lint/inspect/snapshot completed if used.
- [ ] ffprobe metadata recorded.
- [ ] Keyframe/contact sheet reviewed.
- [ ] Playback verified in target lesson page if embedded.
- [ ] Content QA and technical QA are separately recorded.

## No-media state

If media is not produced, record:

```text
No screenshots/videos produced because: <reason>
Media status: blocked_until_capture_env_ready | not_required | blocked_until_safe_fixture
```
