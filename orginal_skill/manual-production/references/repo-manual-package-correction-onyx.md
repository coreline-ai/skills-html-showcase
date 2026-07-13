# Repo manual package correction — Onyx session

Use this as a concrete reminder for public GitHub/open-source product manuals.

## What went wrong

A user asked for a manual for `https://github.com/onyx-dot-app/onyx`. The first response treated this as a Markdown admin manual and produced one `.md` file after reading the repo/docs. The user corrected the workflow: the agent should have first understood the product/manual structure and asked or selected the artifact shape before producing Markdown-only.

## Correct class-level behavior

For public repo manuals, do not equate “manual” with “Markdown document.” First decide the artifact target:

1. Markdown reference — acceptable only when the user explicitly wants docs text/reference.
2. Static manual package — default when the request is user/operator-facing and no live UI access has been approved.
3. Live UI captured tutorial package — required when the manual must teach actual UI clicks/screens, with screenshots/video/QA evidence.

If the user did not specify and the distinction affects output quality, ask. If an obvious default exists, state it and proceed with package structure, not a single `.md`.

## Better package shape used after correction

- `index.html` — showable manual entry point
- `lessons/*.html` — modular operator lessons
- `assets/` — CSS/JS
- `manual/` — Markdown source/reference material
- `sources/` — upstream docs/repo source map
- `evidence/` — verified repo/config evidence
- `qa/` — verification log, content boundary, runtime/UI gaps, browser smoke
- `manual-package.manifest.json` — honest claims such as `runtime_started=false`, `ui_capture=false`
- `STATUS.md`, `HANDOFF.md` — state, caveats, next branch

## Clean rebuild / v4 lesson from the later Onyx correction

When an Onyx-style public repo manual is rejected or the owner asks for a clean rebuilt version, do not keep patching the old package. Create a new versioned root such as `onyx-manual-package-v4/`, keep old versions read-only/reference-only, and rebuild from source-map evidence plus the shared static operator-guide template.

A robust static package shape for this class is:

- `index.html` — operator-guide shell and workflow map
- `overview.html` — beginner/system overview before workflows
- `beginner.html` — preserved first-read companion page when it already exists
- `lessons/01-*.html` … `lessons/NN-*.html` — standalone lessons, not thin card repeats
- `assets/style.css` — shared `og-*` shell and warm-ivory tokens
- `sources/source-map.md` — concise source/evidence map
- `qa/static-template-qa.json` and `qa/browser-smoke.md` — deterministic + browser evidence
- `manual-package.manifest.json`, `STATUS.md`, `HANDOFF.md`

For Refero/Cursor-style static operator guides, preserve the template contract explicitly: `--og-bg:#f7f7f4`, `--og-brand:#f54e00`, compact radius around `4px`, `og-*` sections, visible flow/focus/review structure, and flow-step/focus-card count alignment. Each standalone lesson should include purpose, when to use, prerequisites, ordered checks, common mistakes, readback/verification, evidence links, next judgment, and an explicit boundary for what was not runtime/live-UI verified.

During QA, inspect rendered visible text, not only source. A common failure is raw links or HTML leaking into the page, e.g. literal `<a href=...>` shown inside a lesson. Treat this as a user-facing defect; convert it to rendered anchors or plain learner copy and rerun local-link plus browser smoke.

## Verification expectation

Static package PASS requires at least:

- local HTML href/src resolution
- manifest smoke
- no user-facing false claims about runtime/UI verification
- rendered visible-text scan for raw markup/Markdown/template leakage
- compose/config syntax checks when the manual documents compose commands
- browser smoke of `index.html`, the overview/beginner page when present, and at least one lesson
- explicit boundary for deferred live UI capture

Do not call this a live UI manual unless the app was actually started and screens were captured.