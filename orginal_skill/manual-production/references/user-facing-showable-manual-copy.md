# User-facing showable manual copy: Print Station → ERPNext lesson

Use this reference when producing HTML/video tutorial manuals from live UI captures.

## What the user corrected

The user wanted a Print Station-style deliverable: a user-visible tutorial package with HTML, screenshots, and video. A Markdown-heavy pre-capture package was not acceptable as the main deliverable when the requested outcome was “보여줄 수 있는 튜토리얼 산출물”. If the runtime/capture environment is blocked, the correct sequence is to unblock/setup the environment first, asking for approval when needed, not to substitute planning docs.

The user also corrected the copy style: the manual HTML must not contain the agent’s work progress, future plans, blocked/final status, or peer/Hermes discussion. Those belong in STATUS/HANDOFF/qa/sources, not in the user-facing manual.

## Print Station criteria to reuse

- Treat the artifact as an operator/user manual, not an implementation report.
- Use actual live UI evidence: real route/screen, screenshots, video, review images.
- Explain what the user sees, where they click, and what a visible control means.
- Organize by the user’s mental model and workflow, not by internal route names or production phases.
- Keep implementation/tooling terms out of the manual page: DB/API/cache/Vercel equivalents include Playwright, ffmpeg, artifact, showable, slice, provisional, blocked, not final, Generated from.
- Keep status/QA/future-work/progress in non-user-facing docs.
- If a workflow is not covered yet, omit it or link only to another completed user-facing lesson; do not add “아직 하지 않은 것”, “다음 단계”, or “이후 튜토리얼은…” sections inside the manual.
- User-relevant safety boundaries are okay when phrased as manual guidance, e.g. “이 튜토리얼은 기본 탐색 안내이며 회계·세무 판단은 다루지 않습니다.” Avoid owner/oracle wording like “safe fixture required before future capture”.

## Cleanup and verification procedure

When the owner corrects the manual for sounding like project/status work, clean only the user-facing manual pages and keep QA/status/handoff notes in `STATUS.md`, `HANDOFF.md`, `qa/`, or `sources/`:

1. Read every HTML page that a user will open; do not rely only on generated previews or prior status docs.
2. Rewrite headings and body copy around the user's mental model: what they see, where to click, what the visible control means, and what the lesson covers.
3. Replace progress/process wording with learner-facing scope wording. Example: `학습 범위: 이 장은 ... 설명합니다` is acceptable; `아직 하지 않은 것`, `다음 showable slice`, and tooling notes are not.
4. Preserve screenshots, video sources, and links unless they are broken; this task is copy hygiene, not a media rebuild.
5. Run a deterministic forbidden/meta-term scan across user-facing HTML plus an asset reference check.
6. Open the pages in a browser and visually confirm they read like a manual, media renders, and no broken layout or internal-process copy is visible.

## Visible-text scan terms

Before claiming a tutorial page is user-facing, scan visible text for meta/process terms such as:

```text
showable
artifact
slice
Playwright
ffmpeg
fixture
아직 하지
다음 단계
not final
provisional
blocked
Generated from
STOP
peer
Hermes
이후 튜토리얼
안전 fixture
```

False positives in file paths can be tolerated only if not visible to the user, but prefer user-facing filenames too when feasible.

## Corrected ERPNext example

Bad user-facing copy:

```text
Playwright 화면 녹화 후 ffmpeg로 MP4 변환했습니다.
Selling 워크스페이스에는 Customer, Quotation, Sales Order, Sales Invoice 등이 보입니다. 이후 튜토리얼은 안전 fixture에서만 거래 흐름을 다뤄야 합니다.
5. 아직 하지 않은 것
Generated from live ERPNext UI capture · not final manual
```

Better user-facing copy:

```text
영상에서는 로그인 후 Home, Accounting, Selling 워크스페이스로 이동하는 기본 흐름을 보여줍니다.
Selling 워크스페이스에서는 Customer, Quotation, Sales Order, Sales Invoice처럼 판매 업무에 연결되는 메뉴를 볼 수 있습니다.
ERPNext v15 기본 화면 튜토리얼
```
