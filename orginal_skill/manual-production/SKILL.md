---
name: manual-production
description: Use when creating, auditing, or updating user-facing manuals, operator guides, admin tutorials, onboarding docs, workflow walkthroughs, or screen-recorded product guides from a real application or system.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [manuals, documentation, tutorials, operator-guides, product-guides, qa]
    related_skills: [manual-verification, dogfood, ocr-and-documents, verification-before-completion]
---

# Manual Production

## Overview

A useful manual is not a prose summary of what the author thinks the product does. It is an operating artifact grounded in the real system, written for a specific reader, and split into executable tasks.

Core rule: **inventory the real workflow before writing the manual, then verify the produced artifact with `manual-verification` before claiming it is ready.**

For flow-first manuals, a Workflow Map must show both levels of structure: the overall set of major flows and the selected individual flow's internal path. Do not rely only on a side detail panel or below-the-fold focus lesson to represent the selected flow. See `references/selected-flow-path-in-workflow-map.md`.

When the package includes standalone `lessons/*.html` pages, do not leave them as thin copies of the index/workflow cards. Use `references/static-standalone-lesson-depth.md`: each lesson must stand alone with purpose, audience, when-to-use, prerequisites, concrete operator checks, cautions, common mistakes, verification/readback, source links, next branch, and an explicit evidence boundary. If the UI exposes an impossible state, dead filter, missing route, broken media, stale label, or misleading control, do not document it as normal behavior. Flag it, fix it if in scope, or explicitly exclude it.

**Beginner-first rule:** A manual is for someone who does not yet know the system. Do not write compressed expert notes or a label index. Before a click path, explain what the workflow/object is, when the reader needs it, what input is required, what changes after the action, what visible state proves success, and what beginner mistake to avoid. Use first-appearance terminology explanations, plain Korean, everyday analogies, danger/good pairs, review checks, and concrete safe examples where useful.

**System overview page rule:** For non-trivial product/operator manuals, integrate the `html-for-beginners` teaching posture by adding a learner-facing `overview.html` / `system-overview.html` page, or a top-level “시스템 개요” section when intentionally single-page. Use `references/system-overview-page-for-beginners.md`. The overview must explain the product/system before workflows: what it is, who uses it, major parts, what data/work item moves through it, common beginner confusions, and how to read the manual. It needs a visual mental model (`.og-diagram`, flowchart, component map, lifecycle map, or screenshot) and beginner aids; it must not be a shallow product summary or internal architecture dump.

**Companion beginner page attachment rule:** During inventory, search for any already-created beginner/overview HTML or explanatory companion page before rebuilding or finalizing the package. If one exists and is still valid, attach it deliberately: link it from the top-level `index.html`, keep it as a first-read page such as `beginner.html`/`overview.html`, update `manifest`, `STATUS`, and `HANDOFF`, and run local-link plus `file://` browser smoke. If the user provided the companion HTML/source file, preserve that source as the content of truth: do not replace it with a shorter agent-authored summary or restyled rewrite; add only minimal package navigation/metadata needed for integration unless the user explicitly asks for editing. Do not orphan a separate beginner page just because the workflow map and standalone lessons were rebuilt. See `references/beginner-companion-page-attachment.md`.

**User-provided DESIGN.md retrofit rule:** If the user provides a `DESIGN.md` and asks to change an existing manual/package design, treat the file as the design contract and the existing manual as the content contract. Retrofit shared CSS/tokens first, preserve rich learner-facing pages and companion HTML, update manifest/status/handoff/QA with the design source, then verify rendered computed styles via browser smoke instead of relying on source inspection alone. Use `references/user-provided-design-md-retrofit.md`. Do not shorten or rewrite the manual unless the user asks for content editing.

**Portable-skill-first rule:** When a project such as Print Station or ERPNext is being used to develop this workflow, treat the project as a test case/exemplar for improving the deployable generic manual-production skill. User corrections, process changes, QA failures, and artifact requirements must be generalized into the skill/references/templates/scripts when reusable. Do not optimize only the current project's manual while leaving the portable workflow unchanged.

**Deployment-completeness rule:** If production exposes a reusable capability needed for deployable manuals, do not leave it as an implicit project convention. Turn it into the portable workflow as a dedicated skill, reference, template, script, or required sub-skill, then update `manual-production` so future runs call or apply it explicitly. Example: if reliable delivery requires independent QA, create/use `manual-verification` and make production invoke it; if future work reveals packaging, publishing, accessibility, localization, handoff, or media QA needs that are reusable, add the corresponding portable component and wire it into the production flow instead of relying on memory or ad-hoc notes. If the owner says each manual is being separately uploaded to Cloudflare and asks for an `onboarding` path or selector, build a central Cloudflare Pages hub instead of another isolated deploy: use `references/static-manual-onboarding-hub-cloudflare.md`, bundle public-reader manual packages under `/onboarding/manuals/<manual-id>/`, link existing external Pages manuals as cards, and exclude internal QA/source/handoff artifacts from the public package.

**Template-first consistency rule:** For showable operator-guide HTML, do not rely on ad-hoc page design from the current model/session. Use the reusable warm-ivory software-studio shell adapted from Refero Styles (`https://styles.refero.design/style/4e3b4717-84c8-4599-baaf-a343c3d619b6`) the way `html-for-beginners` uses `assets/template.html`: copy `templates/static-operator-guide-template.html` (or a stricter project-provided template), then apply `references/static-operator-guide-design-system.md` and `references/operator-guide-template-first-design-system.md`. The template supplies named regions, fixed component roles, flow/detail/carousel/review-card behavior, visible workflow connectors, screenshot-or-diagram focus cards, inline highlighter emphasis (`.og-hl`), and height-sync expectations; fill it with the target product's own workflows and evidence, not Cursor/Refero/ERPNext/Print Station example content. A simple hero/card/lesson-link package is only acceptable when intentionally scoped as a lightweight repo/docs reference or capture-blocked package.

**Accepted structure / visual-only refresh rule:** When an existing manual/package already has an owner-accepted information architecture or interaction model, a design refresh must keep that structure unchanged and alter only visual style tokens/components unless the owner explicitly requests a structural redesign. Treat the existing DOM/data/interaction semantics as the content contract: flow selectors, grouped menu/function nodes, selected-flow arrows/badges, detail panels, lesson states, modal behavior, and numbering semantics must remain equivalent. For example, if the accepted Workflow Map used grouped menu/function columns plus `from → to` edge steps, the refresh must preserve the `columns + nodes + flow.steps[from/to]` model and only restyle it with the new shell/tokens. Do not collapse it into top-level flow description cards merely because a generic template's sample `guideData` is flow-card based. QA must compare refreshed artifacts against the accepted prior artifact for interaction semantics before checking visual tokens.

**Workflow-visual minimum rule:** A showable operator guide must not present the Workflow Map as disconnected tiles or the Focus lesson as empty text blocks. If there is more than one flow/stage, draw visible connectors/arrow-badge paths between cards using the template's `.og-flow-connectors` layer or an equivalent SVG/canvas. Every Focus card must contain a real screenshot/crop when available; if screenshots are impossible for a repo/docs/config-only manual, render a learner-facing diagram, flowchart, or concept map (`.og-diagram`) that teaches the distinction/check for that step. Blank placeholders such as “screenshot here” fail production QA.

**Design-regression stop rule:** When a reviewer says the design gets worse after each correction, stop adding incremental CSS/JS patches. Treat this as an architecture/process failure, not another styling task. Re-open the baseline design contract, compare the current artifact against the template/reference at representative desktop widths (including 1280px), and either revert to a clean template copy or rebuild one coherent shell. Do not stack overrides for the same core classes (`.og-flow-board`, `.og-flow-connectors`, `.og-detail`, `.og-node`, `.og-diagram`, etc.) to satisfy isolated checks. Component existence is not enough: the map/detail relationship, arrow ownership, spacing, hierarchy, and focus visuals must look intentionally designed.

**REQUIRED SUB-SKILL:** After producing or materially editing any non-trivial manual, load and apply `manual-verification`. Manual production is incomplete until verification evidence is recorded or the final report explicitly says which verification pass is still incomplete.

**BEGINNER COMPREHENSION RULE:** For beginner/operator manuals, especially ERP/admin workflows, run an explicit persona comprehension loop before final deployment or closeout. Define role-specific newcomers, tell them which parts of the manual to read, test whether they can explain the operational flow and concrete screen/value evidence, then fix every failed understanding point before claiming completion. Use `references/beginner-comprehension-exam-loop.md`. If the owner says to continue until no improvement candidates remain, do not leave in-scope `PASS_BOUNDED` caveats; reopen/add work items until the known candidate list is empty for the covered beginner scope.

**REQUIRED WORK ORDER:** For showable manuals, work in this order and do not skip straight to screenshots or videos:

1. **Analysis** — understand audience, real jobs, product domain, available evidence, and excluded/risky workflows.
2. **Structuring** — map the overall business/workflow flow and step structure before writing UI copy. For ERP/admin products, produce real 업무 단위 flows such as lead-to-cash, procure-to-pay, stock movement, or master-data maintenance instead of a shallow screen tour.
3. **Index shell and system overview first** — create/update `index.html` as the central guide shell that shows the whole flow, lesson map, and where each step fits. For non-trivial systems, also add the beginner-facing system overview page/section before detailed lesson production.
4. **Step-by-step execution** — for each approved step/lesson, write a step plan first, then run production: screen capture, guided video, review-card content, and a business workflow diagram/flow map for that unit.
5. **Verification** — run `manual-verification` for the produced step and the overall index/flow integration before claiming it is useful or complete.

If the current manual is only a navigation tour or generic feature list, treat it as insufficient for ERP/operator training until the actual business-unit flows are identified and represented as flow diagrams.

## Artifact Format Gate

Before producing a non-trivial manual, determine the delivery artifact. Do not silently choose a single Markdown file when the request could reasonably mean a manual package. For a concrete public-repo correction and package shape, see `references/repo-manual-package-correction-onyx.md`. If the owner rejects the existing generated package and asks for a new version/clean rebuild, stop patching the old artifact and follow `references/clean-rebuild-after-tainted-manual-artifacts.md`.

- If the user asks for a **document/runbook** or accepts a docs-only pass, Markdown can be the primary artifact.
- If the user asks for a **manual** for a product/operator audience and does not narrow the format, default to at least a static manual package: `index.html`, `lessons/`, `sources/`, `qa/`, `manifest`, `STATUS`, and `HANDOFF`.
- If the user asks for screenshots, videos, exact click paths, or UI training, live UI capture is required unless explicitly scoped as capture-blocked/provisional.
- When this choice materially changes effort or verification, ask the owner before writing lesson bodies. If the owner corrects the artifact target later, patch this skill/references so the same mistake does not repeat.

**Standalone lesson depth rule:** In a static manual package, `lessons/*.html` are not allowed to be thin link targets that only repeat the index card and list 3–5 bullets. If a page is called a lesson/detail module, it must add teaching depth beyond the index: purpose/when-to-use, prerequisites, concrete evidence/source paths or UI/status examples, step-by-step checks, common mistakes, verification/readback, and next decision/branch. For repo/docs-only products without screenshots, include diagrams/tables/code/config evidence and cite source files/docs; for live-UI manuals, include screenshot/video/review-card evidence. If the package intentionally wants only an index with short cards, do not create separate lesson pages or label them as detailed lessons.

**Rendered-markup hygiene rule:** Static packages often pass source/link checks while still showing raw HTML or Markdown to readers. Before closeout, inspect rendered visible text for literal `<a href=...>`, closing tags, `[label](url)`, unfilled template variables, source-map snippets, and TODO/progress language. Convert leaked markup into real anchors or learner-facing prose, then rerun local-link and browser smoke. See `manual-verification` `references/static-manual-package-verification.md`.

See `references/artifact-format-gate-public-repo-manuals.md`, `references/repo-manual-package-correction-onyx.md`, and `references/repo-docs-static-package-dw-closeout.md` for public GitHub/repo-backed static manual packages, flow-first grouped-node maps, Dynamic Workflow QA/remediation loops, and bounded not-run claim language.

## When to Use

Use this for:

- Product/admin/operator manuals
- User guides, onboarding guides, runbooks, SOPs, tutorials
- Beginner-oriented manuals where the reader needs concepts, terms, consequences, and safe habits explained before following UI steps
- Screen-recorded walkthroughs and review-card based learning material
- Existing manuals that need validation against the live product
- Markdown/admin manuals for public open-source products where official docs + repo configuration are the best available source for install/config/operations, **after the artifact-format gate confirms Markdown is the intended deliverable**
- Static manual packages for public repo products when the user likely expects an operator-facing package rather than a single document
- Repo-backed live/dashboard operator guides where source docs, handoffs, a current data contract, and a read-only dashboard screenshot must be converted into a beginner-safe operating manual; use `references/repo-backed-live-dashboard-operator-guide.md`.
- Repo-backed decision-support systems such as market/research/paper-trading dashboards where the manual must teach safe interpretation without source-repo edits, professional advice, real orders, or production configuration changes; use `references/repo-backed-decision-support-manual-package.md`.
- Converting scattered project knowledge into a teachable workflow

Do not use this for:

- Pure API docs with no user workflow; use code/documentation skills instead
- Marketing copy that does not teach operation
- One-page release notes or changelogs
- Fictional/manual mockups where no real behavior can be verified

## Production Flow

## Production Flow

### Phase-gated mode for large manuals

For large products or peer/oracle-run projects, use gates and stop after each closeout until the owner explicitly starts the next phase:

1. **Phase 1 Inventory** — sources, real/menu/workflow evidence, confirmed/inferred/unconfirmed states, exclusions, risks.
2. **Phase 2 Outline Gate** — bounded scope, audience track, lesson boundaries, capture needs, owner decisions. Do **not** write lesson bodies.
3. **Phase 3A Readiness/Slice** — capture-environment plan, manifest scaffold, and only non-risky first slices with `UI_CAPTURE_REQUIRED` markers.
4. **Phase 3B Production** — draft lessons and media only from verified UI/source evidence and safe fixtures.
5. **Phase 4 QA/Handoff** — separate technical QA, content QA, unresolved risks, and next tracks.

In gated mode, close each phase with evidence/sources, missing items, risks, skill/process feedback, and a stop line such as `STOP — awaiting gate verdict`. PASS for one phase does not authorize the next phase unless the owner says so.

**Oracle/default-forward rule:** if the user's stated goal is to complete the portable skill/manual and the remaining decisions have safe, reversible defaults, do not stall by asking the user to decide every detail. Set explicit defaults, record them in the manifest/worklog, list caveats and override points, then continue with the next gated instruction. Reserve user clarification for decisions that materially change scope, safety, or external side effects.

1. **Analyze the real work, not just screens**
   - Who performs the task?
   - What outcome do they need?
   - What upstream input starts the work and what downstream result proves it is done?
   - What vocabulary do they actually use?
   - What actions are risky, destructive, permissioned, or approval-gated?
   - For ERP/admin systems, identify actual 업무 단위 flows before selecting screens: e.g. quote/order/invoice, purchase request/order/receipt, stock transfer/count, customer/item/supplier maintenance, approval/reversal/audit.

2. **Structure the overall flow and step map before media**
   - Draw or describe the full workflow path first: trigger → preparation/master data → transaction/action → review/approval → output/report/audit.
   - Split the flow into teachable steps and record what each step proves.
   - Decide which steps become lessons, which become review cards, and which are excluded or require safe fixtures.
   - If you cannot explain the business flow without screenshots, pause production and continue analysis/structuring.

3. **Create or update the index shell and system overview before per-step production**
   - `index.html` should expose the overall workflow map, active path, lesson order, and selected-step detail before individual media is produced.
   - For non-trivial or unfamiliar systems, add `overview.html` / `system-overview.html` or a visible top-level “시스템 개요” section using `references/system-overview-page-for-beginners.md` before writing deep lesson bodies.
   - The overview is the reader's mental-model layer: what the system is, who uses it, major parts, what work/data moves through it, common beginner confusions, and how to read the workflow lessons.
   - The index is the learner's orientation layer; do not wait until the end to bolt it on.
   - A screen-tour index is not enough for ERP/manual work; it must show how the 업무 단위 moves across screens.
   - Workflow Map cards must show an operational path, not a definition. Each card/detail panel should answer: what input arrives first, which master data is needed, which documents/screens process it, where the work goes next, and what result/status/report proves it. If the card text could be the answer to “what is this flow?” rather than “how does this work move?”, re-read the project README/STATUS/HANDOFF, structuring docs, upstream product docs, and live UI evidence before rewriting. See `references/workflow-map-operational-path-cards.md`.

4. **Execute each step through plan → production → verification**
   - Write a step plan first: objective, trigger, input data, screens needed, capture list, video storyboard, review cards, workflow diagram node(s), risk/safe-fixture notes, and success check.
   - Production for that step includes screen captures, guided video, review-card copy/screenshots, and a business workflow diagram or flow-map segment.
   - Then verify that step with `manual-verification` before moving on or before claiming the slice is useful.

5. **Write the operating flow**
   - Use real labels from the product.
   - State prerequisites before steps.
   - Say what success looks like after each major action.
   - Keep internal jargon out unless the operator sees it on screen.
   - Use plain language; explain consequences, not implementation.

6. **Create media only after the flow is stable**
   - Capture from the real app/system, not reconstructed screenshots unless explicitly requested.
   - One video should teach one coherent job. If it needs many unrelated menus, split it.
   - Pair each media item with a review card: purpose, covered screens, exclusions, risk notes, and verification status.
   - If a reviewer says a guided video is too simple or unlikely to explain the workflow, stop treating it as a rendering/placement problem. Write a video-production plan first, then regenerate it as a teaching-depth clip using trigger → prerequisite data → visible evidence → consequence/branch → success/stop check. Use `references/guided-video-teaching-depth.md` and `references/manual-video-planner-checklist.md`.
  - If a reviewer says the video still feels like a rigid slide deck after teaching-depth work, run one representative OBS zoom/pan POC before regenerating the full set. Define the owner-facing review criteria first, record it as a workflow run with evidence, and ask for quality judgment on the POC. Use `references/obs-zoom-pan-video-pipeline.md`.
- If a reviewer asks to fix the shortcomings and regenerate only one video before scaling, prefer a scene-graph POC over another ad-hoc render tweak: write `shot_spec.yml`, create an editable `scene_graph.json`, bind each scene to source screenshot/evidence/focus/copy/layout, use multiple source screens when the lesson crosses states/documents, render one representative sample, inspect a contact sheet, run media/browser/hash checks, and report local regeneration separately from production deployment. Use `references/scene-graph-manual-video-poc.md`.
- If the reviewer concludes video is not suitable, pivot to a static-but-emphatic structure instead of making another video. Preserve the teaching value with a browser-native HTML artifact: workflow map, arrow-badge path, hot-path cards, severity/attention tags, jump links, margin-note style callouts, annotated screenshot/review cards, and click-to-focus detail panels. Adapt the useful pattern from “The unreasonable effectiveness of HTML”: replace skimmed prose/video with spatial, navigable, directly readable HTML where diffs/flows/call graphs become boxes, arrows, notes, and tags. Static does **not** mean flat prose; it must still show flow, emphasis, branch/start conditions, and checks.
- When a Workflow Map already explains the basic flow, the static detail panel below it must **concretize** that selected flow rather than repeat it: show real screenshots, visible highlights/callouts, document IDs, customer/vendor/item names, quantities/amounts/statuses, and downstream checks for that exact flow. Use `references/static-workflow-map-screen-value-panels.md`. If the panel has no actual values or screenshot evidence, treat it as too abstract even if the map itself is correct.
- If static flow cards/review panels name a specific document, report, status, quantity, amount, or downstream effect, include direct screenshot evidence for that exact object; do not substitute an adjacent screen/workspace as a proxy. For example, a receipt/stock-balance/payment claim needs its own visible document/report/effect card, not only the related order, entry, or workspace. This also applies to prerequisite/standards screens such as Item Price/Price List and Material Request: if they are named as a learner check, provide a direct screen evidence card rather than a workspace/proxy card. Use `references/direct-transaction-evidence-cards.md` and `references/beginner-comprehension-exam-loop.md`.
- If the manual tells beginners to read workflow numbers and focus screenshots in the same order, produce one numbered focus card per canonical workflow step for every selectable flow, or explicitly bound any omitted steps in learner-facing copy. Do not treat “a few key screenshots” as sufficient when the visible step sequence is longer; it creates a missing-evidence signal for beginners. After any single step-count/focus-card mismatch is found, audit all sibling flows and verify production after redeploy. See `manual-verification` `references/flow-step-focus-card-count-invariant.md`.
- If step-aligned focus cards make the page too long, do **not** reduce coverage back to a few screenshots. Keep the 1:1 step/card invariant and switch the focus area to a slide/carousel pattern: one visible card, numbered dots, previous/next controls, visible `N / total` counter, and hot-node/path clicks that activate the matching slide. Verify per-flow counts, single-visible-card behavior, hot-node → slide navigation, image load, console health, and sticky-nav scroll offset. Use `references/step-aligned-focus-carousel-and-hot-node-navigation.md`.
- If a desktop workflow shell uses a left workflow map/canvas plus a right selected-flow detail panel, keep the two columns visually paired. Measure the rendered workflow map height, store it as a CSS custom property on the shared shell, apply it to the detail panel `height`/`max-height`, keep the detail panel internally scrollable, and disable the sync in stacked layouts. Verify every selectable flow at desktop widths and at least one stacked width. Use `references/workflow-map-detail-panel-height-sync.md`.
- If screenshot/review-card annotations use `.shot-callout`-style overlays, size the callout to its text rather than the screenshot container. Avoid `top` + `bottom` or full `inset` vertical constraints on content callouts; use `bottom:auto`, `height:auto`, `width:fit-content`, and a bounded `max-width` so short Korean copy does not become a large panel that hides the screenshot. Verify rendered geometry across every selectable flow and modal/lightbox view after deployment. Use `references/screenshot-callout-fit-to-content.md`.
- If a manual needs inline emphasis inside learner-facing copy, use the highlighter underline pattern from `references/highlight-emphasis-patterns.md`: short concrete phrases only, `.og-hl` namespace, thin rounded underline, multi-line safe `box-decoration-break`, optional animation with reduced-motion support, and no hover-only meaning.
- If the user rejects the current manual/report as not understandable, or asks to re-plan with a specific model and Dynamic Workflow, restart as a governed reader-first rebuild rather than patching ad hoc: read/update handoff first, run a model-backed plan gate, rebuild from concrete screen/value evidence, verify human comprehension separately from rendering, sync staging/deploy directories, and report production deployment as a separate approval gate. Use `references/dynamic-reader-first-static-manual-rebuild.md`.
- For manual videos, explicitly plan the viewer target, use environment, behavior goal, 1–3 item scope, Must-Know/Nice-to-Know/Danger split, intro/preparation/main/caution/wrap-up structure, visible captions, and progress/chapter cues before rendering. The goal is fast clear understanding, not feature coverage or entertainment.
- When a reviewer reports generic narration, visually impossible focus, over-explanation, or failure to complete a user purpose, do not continue rendering. Create a `shot_spec.yml` first and apply `references/screen-grounded-purpose-complete-video-gates.md`: every scene must bind business purpose → visible screen evidence → visible field/value → value impact → next judgment/action. Block abstract phrases such as “대표 경로”, “문서 영향 관계”, “흐름을 확인”, or “상태를 파악” unless rewritten with actual visible field names, values, impact, and next action. If the failure is specifically that the clip feels like a sample/mock explanation rather than a real ERP/admin feature explanation, use `references/erp-screen-grounded-video-regeneration.md`: regenerate from real screen regions, verify the shot spec before rendering, and report deterministic frame-based MP4s as bounded owner-review POCs unless live OBS recording was actually run.
- When the owner accepts one stronger screen-grounded direction and asks to apply it to already generated videos, use `references/screen-grounded-batch-regeneration.md`: preserve existing filenames/HTML refs, back up previous assets, render deterministic Playwright HTML→PNG frames plus `ffmpeg` MP4s when live recording is not required, harden relative paths with absolute URLs or a `<base href="file:///...">`, verify metadata and missing refs, inspect contact sheets, and report local regeneration PASS separately from public deployment PASS.
- When the video layout separates a system screen on the left from explanatory steps on the right, apply `references/pure-system-left-video-contract.md`: the left side must be based on raw application screenshots, not a reused Driver.js frame, annotated review image, contact sheet, poster, or previously composited video frame. Keep the full learner explanation in the right panel, but if owner feedback asks for better visibility, the left screen may include learner-facing visual guidance such as zoom/pan, dimming, focus boxes, cursor indicators, arrows, or short callout labels as long as they point to visible screen evidence and do not replace the right-panel explanation. Do not use generic/repeated focus presets as a substitute for per-scene target planning: each scene must name the intended visible field/region and carry a target rectangle or validated selector/coordinate derived from the actual screenshot. Verify source paths against a raw-screenshot whitelist, inspect contact sheets with a strict frame-by-frame focus-placement gate (`PASS`, `BROAD`, `WRONG`), and hash-check any local staging/deploy copies so stale videos do not remain in review packages.
- When the owner explicitly approves risky/state-changing demo actions for a manual (Submit/Post/Pay/Issue/Receive/order/invoice/payment/stock workflows), follow `references/state-changing-demo-transaction-lessons.md`: restate the approved scope, create a safe fixture plan, execute only in demo/staging/local data, read back document state and side effects, capture visual evidence, then build the lesson/video from verified submitted-state evidence. Keep local execution PASS separate from public deployment PASS.

7. **Verify with `manual-verification`**
   - Load the `manual-verification` skill and run it as a separate QA pass.
   - Technical verification: assets load, routes open, videos play, screenshots match, no missing files, no console/runtime errors.
   - Visual/media verification: representative screenshots/video frames are inspected; guided highlights align with actual visible UI targets.
   - Content verification: route coverage, lesson boundaries, wording, reader usefulness, impossible states, missing steps, duplicate explanations.
   - Passing one pass does not imply passing the others.

8. **Report completion honestly**
   - Separate completed, changed, verified, unresolved, and out-of-scope items.
   - Include known product defects discovered while writing.
   - If a manual section depends on an unfixed product issue, mark it blocked or conditional.

## Gated Large Manual Workflow

For large manuals, do not run the whole workflow in one pass. Use phase gates:

1. **Phase 1 — Inventory only**: sources, menus/routes/states, workflow candidates, exclusions, risks, owner decisions. No final prose, bulk translation, screenshots, or videos.
2. **Phase 2 — Outline only**: audience, bounded scope, lesson boundaries, manifest draft, capture needs, unresolved decisions. No lesson body prose or media production.
3. **Phase 3 — Production**: selected lesson prose, screenshots/video, review cards, and static package generation from the approved outline.
4. **Phase 4 — QA / Handoff**: technical QA, content QA, corrections, unresolved risks, final delivery record.

After every phase closeout, stop for an explicit verdict. A PASS does not automatically authorize the next phase; wait for a separate start instruction. Closeout line for delegated work: `STOP — awaiting gate verdict`.

When operating as the oracle for a skill-test/manual-production run, avoid unnecessary owner-decision deadlocks. If the user has already stated the goal is to finish the distributable skill and exemplar manual, choose conservative defaults for version, audience, label policy, capture source, and risk handling; document those defaults and proceed to the next gated phase. Ask the user only when the decision is unsafe, irreversible, externally visible, or changes the promised scope.

## Grounding Rules

## Print Station parity rule for user-facing tutorial HTML

When the requested deliverable is a user-facing tutorial/manual, match the Print Station quality bar rather than producing a simple stacked page or progress report. Load and follow `references/print-station-parity-guidelines.md`.

Required baseline:
- User-facing HTML contains only learner/operator guidance: what the user sees, where to look, what the screen means, and what to check.
- Keep work progress, peer/Hermes status, QA notes, future plans, blocked/final/provisional labels, and tool details out of the manual HTML. Put them in `STATUS.md`, `HANDOFF.md`, `qa/`, or `sources/` instead.
- A Print Station-style lesson needs the full pattern: operator-guide shell + Driver.js guided video + video panel + note-card stack + review-card grid + clickable screenshot review where practical.
- Do not treat raw Playwright navigation video or screenshot lists as equivalent to the Driver.js guided-video pattern. The video should include focus/highlight rectangles, explanatory popovers, and a step counter.
- Before completion, scan visible text for process/meta terms, verify media refs and video duration/resolution, open the page, test topic switching, and visually inspect at least one Driver.js render composition.

## Capture-blocked production rule

If the requested deliverable is a showable tutorial package (HTML/screenshots/videos) rather than a planning artifact, a blocked capture environment is not a reason to substitute Markdown-only output. First try to unblock/setup the runtime and capture environment; if the next action is heavy, unsafe, credentialed, or externally visible, request explicit approval. Only produce capture-blocked Markdown/provisional packages when the owner has accepted that as the phase goal.

## User-facing manual copy rule

Showable tutorial HTML/video pages are for the end user/operator, not for the owner/oracle. Keep progress, QA, limitations, phase status, and production-tool details in `STATUS.md`, `HANDOFF.md`, `qa/`, or `sources`, not in the manual page. Do not write phrases like `아직 하지 않은 것`, `다음 단계`, `showable artifact`, `slice`, `Playwright`, `ffmpeg`, `fixture`, `blocked`, `provisional`, `not final`, `Generated from`, or Hermes/peer process notes in user-facing manuals. Avoid narrating obvious UI mechanics that the rendered page already makes self-evident, such as “choose the button,” “the columns are divided by category,” “selected items are highlighted,” or “the right panel shows details.” Use copy for business meaning: entry points, branch/skip cases, document/status consequences, risky Submit/billing/payment/stock effects, and concrete checks before action. Use the Print Station pattern: actual screen evidence, what the user sees, where they click, what the visible control means, and operational boundaries only when user-relevant. If a workflow is not covered yet, omit it from the manual or link to another completed user-facing lesson; do not describe our plan to cover it later.

When correcting manual copy after owner feedback, treat it as a content cleanup pass: rewrite visible HTML headings/body text to learner-facing language, preserve working media/links, run a forbidden/meta-term scan on user-facing HTML, verify media references and video durations, then perform browser visual QA. Do not let STATUS/HANDOFF/qa language leak back into the tutorial pages.

See `references/user-facing-showable-manual-copy.md` for generic user-facing copy criteria, cleanup procedure, and a visible-text meta-term scan list. Project-specific correction examples in references are examples only; generalize the principle before applying it elsewhere.

## Guided tutorial baseline rule

If a showable manual page feels like an early static document, do not stop at typography or a shell redesign. The guided-manual baseline is: **operator-guide shell + guided/focused video + lesson video-grid/note-card layout + review-card grid**.

Required default structure:

1. Main `index.html` as the operator-guide shell: topbar, learner-facing summary cards, sticky topic pills, workflow map with active path, detail panel, populated learning stage, and common checks.
2. Each lesson page/learning frame uses the guided lesson pattern: video panel on the left, 3 stacked note cards on the right, and 3 review cards below with screenshots, titles, explanation, and checklist bullets.
3. Videos are not raw screen recordings by default. Use Driver.js-style step focus: dim overlay, highlighted target, Korean popover title/description, progress text, deterministic timed step changes, and no manual navigation buttons for recorded clips. The popover copy must match the visible frame evidence the same way review-card copy does: do not claim fields, columns, totals, dates, statuses, or actions that are not visible or not within the guided focus. If copy changes after content QA, regenerate the WebM/MP4/poster from the corrected tour source and re-check a step contact sheet before delivery.
4. Review cards are first-class learning material, not QA/status cards. They should summarize the real screen areas the user must recognize and what each area means. Review-card screenshots should not be plain cropped regions when the card teaches a specific recognition/check: add visible highlights, color emphasis, arrows, or short embedded callouts that point to the relevant screen area and explain what the learner should notice. The copy must be constrained to what the capture actually shows: do not claim a field, column, total, status, report area, or document state unless it is visible in the screenshot or intentionally described as off-screen/context. If the captured image is weaker than the intended explanation, either rewrite the review-card text to the visible evidence, adjust the highlight to the real target, or replace the screenshot. If the same screenshot can be enlarged in a modal/lightbox, the enlarged view must carry the same annotation or an equivalent learner-facing explanation; do not annotate only the thumbnail/card state. Keep overlays learner-facing and concise, and verify they do not obscure the evidence needed to understand the screen.
5. Preserve user-facing copy only; keep progress/status/QA elsewhere. Verify the learning stage visually — local `file://` iframes can render as blank, so use embedded templates or serve over local HTTP if needed.

**Flow-first workflow-map requirement:** For operator manuals, do not reduce a workflow map to feature cards or menu definitions. Start from the real job/data-flow, then group participating functions/menus into meaningful categories, highlight the current flow path, dim non-participating items, draw numbered menu-to-menu connectors where useful, and keep workflow-detail explanations separate from individual menu/function explanations. The numbered system must be unified per flow: top sequence, connector badges, workflow aside steps, step-specific checks, and lesson/media state all derive from one ordered step data source such as `{from, to, label, note, check}`. Prefer the Print Station-style **arrow-badge** pattern when the step number represents movement between nodes: one connector per step, the number badge near the connector midpoint, and no node-level step chips. Active/highlighted nodes should be derived from the same step endpoints unless they are explicitly separated as prerequisites/supporting references. Do not present the ordered path as the only mandatory 1→N execution route; describe it as a representative/checking path and add entry/branch/skip notes when real work may start from a later document or split into alternative paths. If the design explicitly keeps node markers, never leave first-time readers with bare numbers: label the chip role (for example result vs next-check basis), use color only as a supplement, and include a visible legend when color encodes meaning. Lesson/video scope should follow the selected flow or job, not a single menu screen. When the shell has a `Prerequisite`, `Workflow Lessons`, or similar learning section below the map, treat it as part of the same selected-flow state: heading, intro copy, tabs, generated overview, and stage content must update with the selected flow and must not retain default/sales-only wording for purchase, receipt, stock, or other non-default flows. Shared prerequisite lessons may remain, but frame them as supporting the current flow. Content QA must confirm that highlighted items, connectors/arrow badges, absence or semantics of node chips, branching copy, legend, lesson-section copy/tabs, and explanations describe the same flow before PASS; use `manual-verification`'s `references/workflow-map-content-qa.md`, `references/arrow-badge-workflow-map-qa.md`, `references/workflow-map-role-chip-and-copy-qa.md`, and `references/flow-aware-lesson-section-alignment.md` for the verification invariants.

See `references/static-operator-guide-design-system.md` for the fixed reusable component/classes/tokens, `references/operator-guide-template-first-design-system.md` for the template-first consistency contract, `references/visual-only-refresh-preserve-accepted-structure.md` for preserving an already accepted workflow/data/interaction model during style refreshes, `references/showable-guided-manual-baseline.md` for the generic baseline, `references/print-station-style-operator-guide-shell.md` as a style exemplar, `references/print-station-data-flow-workflow-canvas.md` as an interaction-pattern exemplar, `references/hyperframes-driverjs-video-pipeline.md` for the video pipeline, `references/topic-fit-guided-video-placement.md` for deciding when an adjacent existing video is too broad and a topic-specific guided video must be created, `references/guided-video-teaching-depth.md` for upgrading technically-correct but too-shallow Driver.js clips into 45–90 second operator teaching videos with trigger/prerequisite/evidence/consequence/stop-check structure, and `references/obs-zoom-pan-video-pipeline.md` for owner-reviewed OBS zoom/pan POCs when the existing guided-video style feels too rigid. Treat project-named references as examples to generalize from, not as product-specific requirements for unrelated manuals.

When the target-version UI is not available but the phase explicitly allows capture-independent work, keep moving without fabricating UI truth:

If the owner/oracle clarifies that the real deliverable is a showable artifact like a product tutorial page, a prior Markdown-heavy package or provisional static preview becomes supporting material only. Do not treat it as satisfying the goal. Once a live/demo runtime is available, pivot to a small visible slice:

1. Work from the live target UI and complete/bypass setup wizard safely with conservative demo values.
2. Capture actual screenshots of login/setup/home/navigation screens.
3. Build a showable HTML page under a clearly named artifact directory (for example, `showable-artifacts/`) that embeds the screenshots and, if available, a short video.
4. Verify embedded media references, browser rendering, and video metadata/playback.
5. Update STATUS/HANDOFF to explicitly demote earlier Markdown/provisional outputs to supporting evidence and to state that the first slice is not the full/final manual.

See `references/live-showable-tutorial-slice.md` for the concrete first-slice pattern.

After the first showable slice passes, improve legibility with a second read-only slice before attempting risky workflows: link a new page from the index, capture focused crops for sidebar/workspace/search areas, add a short navigation-only video, verify all HTML/media refs, and update STATUS/HANDOFF/live-capture logs. Treat broad full-page screenshots with tiny labels as acceptable context but not sufficient teaching detail. See `references/focused-showable-slice-expansion.md`.

When the target-version UI is not available but the phase explicitly allows capture-independent work, keep moving without fabricating UI truth:

- Draft only conceptual/operator onboarding content.
- Use `provisional_capture_blocked_skeleton` or equivalent status.
- Mark every screen path, button, label, state transition, selector, screenshot, and video need as `UI_CAPTURE_REQUIRED` until live target-version capture exists.
- Do not produce screenshots/videos/HTML output or final button-by-button instructions from repo/docs/config alone.
- For risky workflows (Submit/Cancel/Amend, stock mutation, invoice/payment, destructive/admin actions), add safe-fixture fields in the manifest: `safe_fixture_required: true`, `safe_fixture_available: false`, and `risk_handling: read_only_explanation_until_safe_fixture_ready`.
- Keep `risky_action` separate from `domain_expert_required`: a report may be interpretation-risky without mutating data; an invoice/payment flow may be both.
- Update glossary and risk register as new visible English labels or risk classes appear.
- Before closeout, run manifest lint plus a file/marker verification that checks expected lesson IDs, non-empty files, risky safe-fixture fields, capture markers, and absence of accidental media.

Use `templates/capture-blocked-lesson.md`, `templates/capture-lab-unblock.md`, and `references/capture-blocked-erp-manual-slice.md` for the concrete pattern.

## Evidence Hierarchy

For open-source or ERP-style products, treat evidence layers differently:

1. **Live UI with the target version/role** — final source of truth for user-facing steps and media.
2. **Menu/workspace configuration** — good for inventory and outline; not final UI truth.
3. **DocType/report/source definitions** — useful for feature candidates and field discovery; not a user workflow by itself.
4. **Official docs** — useful for concepts and terminology; cross-check against live UI because extraction/docs may be stale or incomplete.
5. **README/dev/infra docs** — use for setup/admin tracks, not ordinary operator lessons unless explicitly in scope.

Every inventory/lesson item should carry `confirmed`, `inferred`, or `unconfirmed`. Do not produce final user-facing step prose, translations, screenshots, or videos from inferred evidence alone; mark `UI_CAPTURE_REQUIRED` instead.

## Grounding Rules

| Situation | Required action |
| --- | --- |
| Public GitHub/open-source product manual requested without screenshots | First run the artifact-format gate: decide or ask whether the target is Markdown/admin reference, static manual package, or live UI captured tutorial. For Markdown/admin reference only, use official docs index + repo README/deployment/config/CLI files, validate documented compose/config combinations when possible, and report runtime as not run unless actually started. For static package, still produce `index.html`, `lessons/`, `sources/`, `qa/`, `manifest`, `STATUS`, and `HANDOFF` even if screenshots remain `UI_CAPTURE_REQUIRED`. See `references/open-source-repo-docs-admin-manual.md` and `references/artifact-format-gate-public-repo-manuals.md`. |
| UI has a filter/state/status that cannot happen | Hide/fix it if in scope; otherwise flag as product issue. Do not teach it as valid. |
| Manual text says a route/menu exists but UI differs | Re-check the live system and update the manual or inventory. |
| A generated video/render succeeds | Still do content QA; render success only proves media generation. |
| Existing docs conflict with current UI | Treat live verified behavior as source of truth, then note the drift. |
| Action changes production data | Stop and ask for safe fixture/staging/demo path. If the owner explicitly approves demo/staging/local execution, follow `references/state-changing-demo-transaction-lessons.md` and verify readback + side effects before producing user-facing lesson/video. |
| Reader needs a business decision, not a click path | Add decision note; do not bury it as a UI step. |
| Domain-risk areas appear (accounting, tax, legal, medical, payroll, security) | Gate before drafting: decide expert review required, general-feature-only, or excluded/localization out of scope. Do not treat translation as validation. |

## Evidence and Source Hierarchy

Default source priority for user-facing manuals:

1. **Live UI with the target role/version/data** — final source of truth for labels, available actions, states, and screenshots.
2. **Workspace/menu configuration** — good for initial structure inventory, but not final proof of user-visible behavior.
3. **Schema, DocType, report, page, or route definitions** — good for feature and field candidates; regroup into user workflows later.
4. **Public docs and README files** — useful for concepts and terminology; cross-check because extraction can omit content or mismatch titles.
5. **Developer/build/test files** — usually out of scope for operator manuals unless producing an admin/developer runbook.

Every inventory item should carry evidence status:

- `확인됨`: backed by a concrete live screen, source path, URL, command output, or captured artifact.
- `추정`: plausible from repo/docs/config but not yet live-UI verified.
- `미확인`: unresolved; move to gate questions, risks, or capture needs.

Menu/module inventory is a coverage aid, not the manual outline. Phase 2 must regroup internal menus, DocTypes, or components into reader jobs and workflows.

## Lesson Splitting Rules

Create lesson boundaries before writing lesson bodies. In outline-gated work, define only lesson id, title, audience, prerequisites, source evidence, capture needs, and excluded risks; do not draft user-facing step prose until the evidence and capture requirements for that lesson are satisfied.

Create a new lesson when:

- The reader changes goal or mental mode.
- A destructive, approval-gated, paid, or externally visible action begins.
- The workflow crosses from configuration to publishing, from admin to public output, or from creation to audit.
- The video would exceed a focused walkthrough and become a tour.
- A prerequisite or verification point deserves its own checkpoint.

Keep together when:

- Steps are always performed in one session.
- Splitting would force the reader to repeat context setup.
- The same route is used only as a brief confirmation screen.

## Manual Artifact Set

For non-trivial manuals, produce or update these artifacts. Use `references/phase-gated-erp-style-manuals.md` for a compact checklist and reusable template list when the product is a large ERP/open-source app.

- **Workflow inventory**: routes/menus/states/actions with document/omit/bug decisions.
- **Manual outline**: lesson list, reader goal, prerequisites, media needs.
- **Manual manifest**: machine-readable lesson list, assets, risks, and QA expectations.
- **Lesson content**: task-oriented steps and expected results.
- **Media assets**: screenshots, recordings, review cards, captions, alt text where needed.
- **Verification record**: technical, visual/media, and content QA results from `manual-verification` kept separate.
- **Handoff report**: completed/changed/verified/unresolved/out-of-scope/not-verified.

**Peer-executed production mode:** If the user says execution should be done by a peer and Hermes should focus on verification/skill improvement, this overrides oracle/default-forward production. For non-trivial manual-production or manual-skill dogfood work, treat peer-executed production as the preferred default whenever a suitable live project peer is available or discoverable; the user should not have to repeat “peer가 실행, Hermes가 검증” every time. Stop direct production work immediately, load `hermes-workflow-ops`, and treat the current session as controller/gate owner. Discover the live project peer, create/update a workflow run or equivalent durable status/evidence record, save the production handoff, send it ACK-first, verify broker routing/ACK, then wait for the peer closeout. Hermes should independently verify the artifacts, issue `PASS` / `REQUEST_CHANGES` / `BLOCKED`, and promote reusable findings into this skill package. Do not keep building the manual yourself unless the peer is unavailable, the user explicitly re-authorizes Hermes direct production, or a bounded controller-fallback is necessary after no ACK/closeout; in that fallback, record the missing peer response, preserve the original safe scope and no-deploy/no-mutation boundaries, verify the artifacts independently, and report `peer closeout not received; controller verified` as a caveat. See `references/peer-executed-production-controller-verification.md` and `hermes-workflow-ops` `references/controller-fallback-and-doc-sync.md`.

## Reusable Tooling and Deployment Boundaries

A deployable manual workflow normally needs more than this `SKILL.md`:

- **Skill**: judgment, phase gates, exclusions, and QA principles.
- **References**: checklists, tables, and review formats.
- **Templates**: copy-and-modify manifests, lesson pages, review cards, and HTML shells.
- **Scripts**: deterministic validation, packaging, asset checks, and static HTML probes.
- **Program/CLI**: only when multiple projects need the same workflow repeatedly.

When a new deployment requirement appears during manual production, classify it immediately:

| Requirement type | Portable form | Production integration |
| --- | --- | --- |
| Judgment/QA discipline | Separate required sub-skill | Add to `related_skills`, Overview, flow, and Quality Gates |
| Reusable checklist or standard | `references/*.md` | Link from the relevant phase and verification checklist |
| Reusable artifact shape | `templates/*` | Make the production step copy/fill the template |
| Deterministic check/build/package task | `scripts/*` | Add command to checks or phase closeout |
| Multi-project repeated workflow | Program/CLI | Document prerequisites and exact invocation |

Do not let deployment-critical needs remain only in an individual project's `STATUS.md`, `HANDOFF.md`, or worklog. If they are reusable, promote them into this skill package and make `manual-production` call them explicitly, the same way it calls `manual-verification` after production.

Keep project-specific capture automation out of the portable skill. Login flows, routes, selectors, fixtures, and recording choreography belong in the project repo or a project worklog unless they are parameterized by a manifest/config. Portable scripts should accept generic inputs such as `manual.yaml`, lesson Markdown, asset paths, and forbidden-term config.

Use scripts for repeatable checks and packaging, not for hiding judgment. A script can prove links, assets, and console health; it cannot prove the lesson is useful to the reader. Always keep technical, visual/media, and content verification separate, and use `manual-verification` as the required post-production QA skill for non-trivial manuals.

### Tool compatibility hardening in gated projects

When reusable validators or static builders do not match the active phase-gated manifest, do **not** reshape the project into a final-package schema just to appease the tool, and do **not** generate ad-hoc previews/media as a workaround. Record the mismatch as a tool-compatibility gap, keep the manual's current evidence/status model intact, and run only stable checks that fit the current phase.

For this situation, create project-side artifacts such as `qa/tool-compatibility-targets.md`, `qa/package-checks.md`, `qa/phase-<phase>-check-log.md`, and `sources/static-preview-readiness.md`. The closeout should separate: checks run, tools intentionally not run, compatibility gaps, and suggested skill/script patches. See `references/phase-gated-tool-compatibility-hardening.md`.

When patched tooling later becomes available, validate it without weakening the phase gate:

- Run the validator first and record the exact mode, e.g. `PASS manual package validation (phase-gated-pre-capture)`.
- Generate static output only if the builder explicitly supports a provisional/capture-blocked mode and emits a visible `PROVISIONAL / CAPTURE-BLOCKED / NOT FINAL` banner.
- Treat static preview output as structural/package QA only, not final manual production.
- Verify preview layout recursively, because builders may place lessons under subdirectories such as `preview-static/lessons/V1-XX.html` rather than beside `index.html`.
- Check that every expected lesson HTML exists, every page has the provisional banner, no media files or embedded media refs were produced, and no final/completion language appears.
- If glossary checkers disagree across script revisions, record the stricter missing-label list as glossary review/reconciliation input instead of silently claiming it disappeared.

## Capture-Blocked Production Slices

When the approved next phase asks for production while capture/media remains blocked, keep producing only capture-independent conceptual/operator content. Use `templates/capture-blocked-lesson.md` for each lesson. Required rules:

- Mark status as provisional, e.g. `provisional_conceptual_draft`.
- Keep source evidence tiered: `live_ui`, `workspace_config`, `doctype_source`, `official_docs`, `owner_decision`, or `unverified`.
- UI-specific procedure, button labels, selector paths, and screenshots stay `UI_CAPTURE_REQUIRED` until live target-version evidence exists.
- Medium-risk business flows may need both `risky_action: true` and `domain_expert_required: true`; a single risk boolean is too coarse for ERP manuals.
- Separate conceptual flow from executable steps. Do not turn source/doctypes into final click paths.
- Use `templates/content-checklist.md` and `templates/media-checklist.md` to record promotion gates and capture-blocked media state.

Before capture/media, stable checks should normally include:

```bash
python3 scripts/manifest_lint.py manifest.yml
python3 scripts/validate-manual-package.py manifest.yml
python3 scripts/glossary_coverage.py glossary.md tracks/**/*.md
python3 scripts/build-evidence-map.py manifest.yml /tmp/evidence-map-check.md
```

Treat glossary coverage as a terminology linter, not content QA; list false positives explicitly even when the check passes. If different tool revisions or reviewers produce stricter missing-label findings, record them in a glossary review/reconciliation note and either patch the glossary conservatively or mark intentional exclusions.

Provisional static preview is allowed only after the builder has been validated against the active schema mode. It must render an obvious `PROVISIONAL / CAPTURE-BLOCKED / NOT FINAL` banner and be recorded as non-final package QA, not as manual completion. The expected layout is `preview-static/index.html` plus per-lesson pages under `preview-static/lessons/<LESSON_ID>.html`; recursive checks are required because top-level `*.html` only sees the index page.

## Capture Lab Unblock Runbook

Capture planning and capture unblocking are different artifacts. When a runtime is unavailable or too heavy, create `sources/capture-lab-unblock.md` from `templates/capture-lab-unblock.md`. Record exact evidence for CLI installed, daemon/service reachable, image/artifact manifest, local pull, config render, monitored start, app-ready check, and stop/report. Registry manifest availability is not a successful local pull/run. If a stack is started, close out background state before reporting unless the owner explicitly asks to keep it running.

## Media Production Prerequisites

Use media tooling only after the lesson boundary and evidence are stable. If the manual requires guided videos, record these prerequisites in the project README and tell the user how to install them:

- **Node.js / npm** for portable render tooling.
- **HyperFrames CLI** for deterministic HTML/CSS/JS video compositions: default command `npx --yes hyperframes@0.6.33 ...`.
- **Driver.js** when the tutorial needs step-by-step focus overlays/popovers on real or mock UI screens.
- **Playwright/Chromium** when Driver.js overlays or real pages must be browser-recorded instead of relying on static HyperFrames snapshots.
- **ffmpeg / ffprobe** for MP4 conversion, frame extraction, contact sheets, and media metadata verification.

Portable skill assets may include templates and scripts for these tools, but project-specific login flows, selectors, fixtures, route lists, and capture choreography must live in the target project or worklog unless parameterized by a manifest.

Recommended generic video pipeline:

1. Lesson manifest defines title, target route/screen, selectors or `data-tour` hooks, copy, media paths, and risks.
2. HTML/HyperFrames composition renders the stable base scene and timeline.
3. Driver.js provides the guidance layer for highlights/popovers when needed.
4. **Playwright browser recording** is used for runtime overlays or real UI capture. When the reviewer is judging camera movement rather than live interaction fidelity, a bounded OBS `image_source` POC from a verified 1920×1080 frame is acceptable before investing in live-capture automation.
5. **ffmpeg** converts/transcodes and extracts review frames/contact sheets.
6. Technical QA checks video metadata, browser playback, missing assets, console errors, and forbidden internal terms.
7. Content QA checks whether the video teaches the right operation and avoids impossible states.

## Content Style

For beginner/operator manuals, load and apply `references/beginner-friendly-manual-patterns.md` before writing user-facing copy. If the artifact is a `beginner.html`, `overview.html`, or first-read companion page, also deliberately import the teaching posture of `html-for-beginners`: concept primer, one-line mental model, first-use term explanations, everyday analogy, danger/good pairs, a visual recap such as a 4-panel HTML/CSS knowledge comic when helpful, and concrete review questions. A hero plus a few summary cards is not an acceptable beginner companion page unless the owner explicitly scopes it as a lightweight teaser.

- Prefer the reader's operational vocabulary over internal architecture terms.
- Use direct task names: “상품 배너 등록하기” beats “Banner CMS Management”.
- Explain why/when before how if the action has consequences.
- Add first-use explanations for English acronyms, ERP DocTypes, statuses, permissions, and domain terms: English label + Korean meaning + plain meaning.
- Use everyday analogies and danger/good pairs when a concept or mistake is not obvious to a beginner.
- End lessons with concrete review checks or takeaways so the reader knows what to verify next.
- Do not invent features, edge cases, or states to make the manual look complete.
- Do not include backend details unless the operator must know them to do the job.
- Use screenshots/video as evidence, not decoration.

## Quality Gates

Before saying the manual is done, load and apply `manual-verification`. Minimum production-side checks before handoff to verification:

- [ ] Reader/job/scope are explicit.
- [ ] For non-trivial product/operator manuals, a learner-facing system overview page or top-level section exists before detailed lessons and follows `references/system-overview-page-for-beginners.md`.
- [ ] Beginner-first aids are present where needed: concept primer, first-use terminology explanations, plain-language consequence notes, danger/good pairs, and review checks.
- [ ] Real system inventory exists or was consciously scoped out.
- [ ] Every documented menu/route/control has evidence or is marked unresolved.
- [ ] Impossible/dead states are removed, fixed, or reported.
- [ ] Risky actions are marked with prerequisites and safe-data guidance.
- [ ] User-facing copy is separated from QA/status/handoff notes.
- [ ] Any user-provided `DESIGN.md` used to retrofit the package has been treated as the design contract without replacing existing manual content; shared CSS/tokens were updated, manifest/status/handoff/QA record the design source, and representative pages have browser-computed style evidence. Use `references/user-provided-design-md-retrofit.md`.
- [ ] Any newly discovered reusable deployment requirement was promoted into the portable skill package as a skill/reference/template/script/CLI hook, or explicitly recorded as not reusable.
- [ ] For Cloudflare/manual-onboarding hub deploys, first-read companion pages (`beginner.html`, `overview.html`, etc.) are copied, linked from the manual entry page, listed in manifest/handoff, and verified by local + production HTTP/browser smoke; representative multi-column Workflow Maps are checked for clipping/scroll reachability as described in `references/static-manual-onboarding-hub-cloudflare.md`.
- [ ] If this package previously passed under older manual skills/templates, the refreshed-skill regression gate has been run via `manual-verification` `references/refreshed-skill-regression-qa.md`; old PASS is treated as historical until renewed static/browser/refutation evidence exists.
- [ ] If lesson content is available both as standalone pages and embedded inside a primary `index.html` shell, shared interactive behavior works in the primary shell too; do not verify only the standalone page.
- [ ] For split-screen videos, left-side evidence is verified as a raw application screenshot/live-capture source with no baked-in prior tutorial popover, prior explanation panel, watermark, contact sheet, poster, review-card image, or previously composited frame. Learner-facing guidance added during the current render—zoom, dimming, focus boxes, cursor markers, arrows, or short callout labels—is allowed when it improves readability, points to visible evidence, and does not replace the right-panel explanation.
- [ ] For repo-backed decision-support systems (markets, research assistants, paper-trading, recommendation/risk dashboards), source repo edits are explicitly out of scope unless requested; the package teaches source-of-truth JSON/data contracts, stale/fallback checks, advice/execution boundaries, and safe interpretation. Use `references/repo-backed-decision-support-manual-package.md`.
- [ ] Beginner comprehension exam has been run for role-specific newcomer personas; failures were converted into content/screenshot fixes or explicitly excluded from scope. Use `references/beginner-comprehension-exam-loop.md`.
- [ ] If the owner asked to continue until no improvement candidates remain, there are no known in-scope manual-content candidates left; `PASS_BOUNDED` is not used for fixable gaps inside the promised beginner workflow scope.
- [ ] `manual-verification` result is recorded as PASS, REQUEST_CHANGES, or incomplete with exact missing evidence.
- [ ] Final report separates completed, changed, verified, unresolved, out-of-scope, and not-verified.

## Common Pitfalls

1. **Writing before inventory.** This creates polished fiction. Inventory first.
2. **Treating source metadata as final UI truth.** Repository workspace/menu JSON, route definitions, and public docs are useful inventory sources, but final user-facing steps need live UI verification for the target version and role.
3. **Letting menu structure become the manual outline.** Menus show coverage; manuals should follow user goals and operational workflows that may cross modules.
4. **Treating implementation names as user concepts.** Menus, statuses, and labels must match what the reader sees.
5. **Documenting impossible cases.** If a state cannot occur, remove it from UI/filter options or flag it; do not teach it.
6. **Confusing media QA with manual QA.** A video can render perfectly while teaching the wrong route.
7. **Treating topic fit as teaching depth.** A video can be correctly attached to the right lesson but still be too shallow if it only points at fields. For ERP/admin manuals, content QA must ask whether the clip teaches trigger, prerequisite data, document/status consequence, branch/exception, and success check. If the answer is mostly “it identifies screen areas,” report it as a recognition slice, not a sufficient workflow lesson.
8. **Overloading one lesson.** If a video needs many unrelated menus, split the lesson.
8. **Skipping public/output verification.** For CMS/admin work, verify the reader's final visible result, not only the admin form.
9. **Hiding uncertainty.** Manuals are operational artifacts; unresolved product questions belong in the handoff.
10. **Expanding safe screen-reading into risky workflow teaching without a fixture plan.** For ERP transaction manuals, a prerequisite/readiness slice can be complete without Save/Submit or new captures: use verified master-data/list screenshots plus an unsaved form screenshot, annotate what is visible, and report adjacent transaction execution as out of scope unless explicitly approved. Once explicitly approved, do not jump straight to a video: write a fixture plan, execute in demo/staging/local data, read back IDs/statuses/ledger-or-stock effects, capture submitted evidence, then produce the lesson/video and state whether it is local-only or deployed.
11. **Blurring regulated-domain guidance.** Accounting, tax, payroll, legal, healthcare, security, and similar domains may need expert/source validation; do not turn generic UI instructions into authoritative professional advice.
12. **Deploying from memory instead of the accepted staging/version.** In peer-gated manual work, do not “fix” the public package back to an earlier accepted invariant during deploy. If the latest handoff says arrow-midpoint badges, do not reintroduce node chips; if it says a staging directory is ready, deploy it unchanged and verify the requested production tokens/visual state. For Cloudflare Pages, also verify the active Wrangler account before project creation/deploy: `Project not found` under a different account is not permission to create a replacement project if the goal is to preserve an existing production URL. See `references/static-manual-cloudflare-pages-deployment.md`.

13. **Over-claiming repo/docs-only manuals.** For a public open-source product manual built from official docs and repository files, verify documented commands/configuration syntactically where possible, but do not claim live install/runtime/UI PASS unless the stack was actually started and health/browser/API checks passed. Use `references/open-source-repo-docs-admin-manual.md`.

14. **Letting the generic template degrade into disconnected cards.** Template-first does not mean “copy the CSS and fill text only.” For showable operator guides, the Workflow Map must retain visible connector paths/arrow badges between flows, and Focus lesson cards must contain a real screenshot/crop or an explanatory diagram/flowchart/concept map. A text-only placeholder is a QA failure, especially for repo/docs-only products where a concept diagram is the correct substitute for unavailable screenshots.

15. **Fixing selected-flow visibility with the wrong layer.** If the accepted design is a grouped node canvas, do not add a separate selected-flow strip and leave the canvas static. The selected flow must be visible in the canvas itself through active/dim nodes, connector paths, and numbered connector badges. Use `references/selected-flow-path-in-workflow-map.md` and verify against `manual-verification` `references/selected-flow-path-qa.md`.

16. **Accumulating correction patches until the design collapses.** If every new instruction appends another CSS/JS override block, the artifact may pass mechanical checks while getting visually worse. Stop, identify the baseline design, remove duplicate overrides, and rebuild the component composition cleanly. At common desktop widths such as 1280px, map/detail pairing, connector readability, active/inactive balance, and focus-card usefulness must be visually inspected before PASS.

17. **Continuing to patch after the owner asks for a clean rebuild.** A rejected or tainted generated package is not a base to keep repairing. Create a new versioned package, rebuild from source/evidence rather than old generated copy, record the old package as ignored input, and run full static/browser/visual/refutation QA from scratch. See `references/clean-rebuild-after-tainted-manual-artifacts.md`.

- `references/repo-backed-live-dashboard-operator-guide.md` — pattern for internal/repo-backed operations dashboards: combine handoff/README/domain docs, current data contracts, local dashboard screenshots, beginner pages, workflow-map lifecycle grouping, safety boundaries, hub deployment, and honest source-vs-manual closeout.
- `references/workflow-first-validation-lessons.md`
- `references/workflow-map-operational-path-cards.md` — how to turn ERP/admin Workflow Map cards from abstract flow definitions into trigger → prerequisite → transaction → downstream boundary → result/check operational paths, with verification steps.

### References

- `references/open-source-repo-docs-admin-manual.md` — pattern for Markdown/admin manuals for public GitHub projects using official docs, repo config, compose validation, and honest not-run runtime boundaries.
- `references/erp-beginner-operator-guide-lessons.md` — ERP/admin beginner operator-guide pattern: user-facing-only HTML boundary, beginner-first transaction lesson order, Print Station-style shell + Driver.js + review cards, safe unsaved-form evidence, and verification checklist.
- `references/skill-marketplace-listing-copy.md` — concise Korean marketplace/profile listing pattern for explaining the manual-production skill: 자기소개, 스킬소개, supported environments, provided files, result examples, and overclaiming pitfalls.

- `manual-verification` — required post-production QA skill for user-facing manuals, tutorial HTML, screenshots, videos, links, visual highlights, content usefulness, and delivery reporting.
- `references/system-overview-page-for-beginners.md` — beginner-facing system overview page pattern adapted from `html-for-beginners`: mental model, roles, component/data lifecycle diagram, danger/good pairs, reading order, and verification checklist.
- `references/beginner-companion-page-attachment.md` — attach separately created beginner/overview HTML pages to the package root/index, update manifest/status/handoff, and verify local links plus `file://` navigation so first-read material is not orphaned.
- `references/beginner-friendly-manual-patterns.md` — adapted beginner-learning patterns from `html-for-beginners`: concept primer, term explanations, analogies, danger/good pairs, review checks, and anti-compression copy rules.
- `references/workflow-inventory-template.md` — route/menu/state inventory table.
- `references/content-verification-checklist.md` — content QA pass.
- `references/technical-verification-checklist.md` — asset/runtime/media QA pass.
- `references/review-card-template.md` — media/manual review card format.
- `references/manual-phase-gates.md` — phase-gated inventory/outline/draft/QA workflow, evidence status rules, and large ERP/open-source manual checklist.
- `references/oracle-default-forward-gating.md` — how the oracle should set conservative defaults instead of stalling on every owner-decision candidate.
- `references/large-open-source-product-inventory.md` — Phase 1 checklist for large OSS/ERP-style systems.
- `references/risky-action-policy.md` — safe fixture vs read-only vs blocked rules for state-changing workflows.
- `references/state-changing-demo-transaction-lessons.md` — owner-approved demo/staging/local execution pattern for submitted transaction manuals: fixture plan, unique markers, readback/state/side-effect verification, visual evidence, guided video generation, and local-vs-deployed boundary.
- `references/capture-blocked-erp-manual-slice.md` — how to keep ERP/manual production moving when capture lab is blocked without inventing UI truth.
- `references/phase-gated-tool-compatibility-hardening.md` — how to handle stale/incompatible validators or static builders without warping a phase-gated manual.
- `references/pre-capture-handoff-closeout.md` — handoff/status/final-boundary closeout pattern for provisional pre-capture manual packages.
- `references/live-showable-tutorial-slice.md` — pivot pattern when the owner wants a Print-Station-like showable HTML/screenshots/video tutorial rather than Markdown-only planning artifacts.
- `references/focused-showable-slice-expansion.md` — second-slice pattern for improving showable tutorial readability with focused crops, navigation-only video, and artifact/ref verification.
- `references/showable-guided-manual-baseline.md` — generic baseline for finished showable manuals: operator-guide shell, Driver.js guided video, lesson video-grid/note-card layout, review-card grid, and verification checklist.
- `references/erp-workflow-first-showable-manuals.md` — ERP/admin manual pattern for analysis → structuring → index workflow map → per-step plan/production/verification, with 업무 단위 flow examples and step-plan fields.
- `references/erp-workflow-map-shell-rework.md` — how to fix an ERP/manual index shell when Workflow Map cards are too abstract or the user asks for a Print Station-style canvas: rewrite as flow-first choices, category columns, highlighted/dimmed menu nodes, numbered SVG connections, split workflow/menu asides, preserved media/modal sync, and visible-copy verification.
- `references/flow-aware-lesson-section-alignment.md` — keep prerequisite/workflow lesson sections synchronized with the selected workflow map state so heading, copy, tabs, generated overview, branch notes, media, and modal behavior all describe the same flow.
- `references/static-manual-cloudflare-pages-deployment.md` — clean public packaging and Cloudflare Pages deployment pattern for showable static manuals, including referenced-asset-only export, production URL verification, workflow-tab smoke, modal/media check, and console check.
- `references/static-manual-onboarding-hub-cloudflare.md` — central `/onboarding/` Cloudflare Pages hub pattern for selecting among multiple static manuals, bundling public-reader packages under `/onboarding/manuals/<manual-id>/`, linking existing external Pages manuals, excluding internal QA/source/handoff files, and verifying local/remote links before closeout.
- `manual-verification` `references/workflow-map-role-chip-and-copy-qa.md` — role-labeled node chips, color legend, connector badge placement, operator-facing copy, and no-obvious-UI narration checks for workflow canvases.
- `references/print-station-style-operator-guide-shell.md` — Print Station-derived exemplar for operator-guide shell plus Driver.js guided video, lesson video-grid/note cards, review-card grid, screenshot enlargement, and visual QA checks.
- `references/topic-fit-guided-video-placement.md` — video-to-lesson placement rule: create a dedicated guided video when the lesson/tab topic is narrower than an adjacent broad workflow or master-data video, then verify with contact sheets, playback smoke, refs, and metadata.
- `references/manual-video-planner-checklist.md` — planning and QA checklist for clear, efficient manual videos: behavior goal, target/environment, limited scope, Must/Nice/Danger split, intro→preparation→main→caution→wrap-up structure, captions, chapter/progress cues, and final comprehension checks.
- `references/obs-zoom-pan-video-pipeline.md` — workflow-ops POC pattern for OBS-controlled zoom/pan tutorial videos when Driver.js/static guided clips feel too rigid; includes architecture, motion defaults, evidence layout, and five-stage QA.
- `references/scene-graph-manual-video-poc.md` — representative-sample pattern for improving rigid/manual videos with `shot_spec.yml`, editable scene graph JSON, per-scene source/focus/copy/layout binding, contact-sheet QA, media/browser/hash verification, and local-vs-deployed reporting boundaries.
- `references/screen-grounded-batch-regeneration.md` — batch regeneration pattern for already-referenced manual videos: preserve filenames, back up old outputs, render deterministic Playwright HTML→PNG frames plus ffmpeg MP4s, harden relative asset paths, inspect contact sheets, and keep local regeneration PASS separate from deployment PASS.
- `references/visibility-guided-system-screen-video.md` — split-screen manual video pattern where the left side stays raw-screen-sourced but may add zoom, dimming, focus boxes, cursor markers, arrows, or short callouts to improve learner visibility while the right panel carries the full explanation.
- `references/arrow-badge-workflow-canvas.md` — preferred workflow-canvas pattern when step numbers belong to connector arrows rather than node chips; includes production rules and verification invariants.
- `references/static-workflow-map-screen-value-panels.md` — static detail-panel pattern for turning a high-level Workflow Map into concrete learner understanding with real screenshots, highlights, document IDs, parties, items, quantities/amounts/statuses, and downstream checks.
- `references/direct-transaction-evidence-cards.md` — direct-evidence rule for transaction manuals: every named document/report/status/effect needs its own visible screenshot/card, not an adjacent screen used as a proxy.
- `references/step-aligned-focus-carousel-and-hot-node-navigation.md` — carousel pattern for long step-aligned focus screenshot sets: keep 1:1 workflow-step coverage while showing one slide at a time, with numbered dots, hot-node/path navigation, keyboard activation, sticky-nav offset, and per-flow QA checks.
- `references/workflow-map-detail-panel-height-sync.md` — CSS/JS/QA pattern for matching desktop workflow-map and detail-panel heights with a shell CSS variable while preserving natural stacked/mobile layout.
- `references/screenshot-callout-fit-to-content.md` — CSS/QA pattern for screenshot annotation callouts that should fit text content (`bottom:auto`, `height:auto`, `width:fit-content`) instead of stretching over the screenshot and hiding evidence.
- `references/dynamic-reader-first-static-manual-rebuild.md` — governed rebuild pattern for stale/failed manual artifacts: read handoff first, use requested-model planning in Dynamic Workflow, rebuild static panels from concrete screen/value evidence, run human-usability QA, sync delivery directories, and keep production deployment approval-gated.

- `references/highlight-emphasis-patterns.md` — inline highlighter underline emphasis pattern from the provided samples: thin rounded marker underline, color variants, animation/reduced-motion rules, usage boundaries, and QA checklist.
- `references/static-operator-guide-design-system.md` — reusable design tokens, class names, component roles, interaction invariants, and QA checklist for consistent showable operator-guide HTML across products.
- `templates/static-operator-guide-template.html` — generic copy-and-fill `index.html` starter with hero, visible workflow connectors/arrow-badge map, selected detail panel, flow-aware focus carousel, screenshot-or-diagram focus cards, inline `.og-hl` highlighter emphasis, review cards, responsive layout, and map/detail height sync.
- `assets/highlight-samples.html` and `assets/highlight-combined.html` — source visual samples for the `.og-hl` inline highlighter pattern.
- `templates/workflow-first-index-shell.html` — older starter shell for ERP/admin showable manuals where `index.html` must present business-unit workflow cards before prerequisite lesson media; prefer the static operator guide template for new generic manuals unless a project already uses this shell.
- `templates/manual-manifest.example.yaml` — manifest starter for lesson boundaries, assets, risks, and QA needs.
- `references/peer-executed-production-controller-verification.md` — when execution is delegated to a project peer and Hermes acts as controller/gate/skill-improvement owner.

- `templates/lesson-boundary.example.yaml` — YAML skeleton for phase-gated lesson boundaries.
- `templates/capture-blocked-lesson.md` — Markdown lesson skeleton for provisional drafts when live UI/media are blocked.
- `templates/capture-lab-unblock.md` — runbook template for moving from blocked runtime to verified app-ready capture lab.
- `templates/media-review-card.example.yaml` — YAML skeleton for media review cards.
- `templates/glossary-template.md` — bilingual UI-label glossary starter.
- `templates/content-checklist.md` — content QA checklist starter.
- `templates/media-checklist.md` — media QA checklist starter.
- `templates/tool-compatibility-targets.md` — planning sheet for validating patched portable manual tools against a project package.
- `templates/capture-next-checklist.md` — next executable capture checks from daemon reachability through stop/report.
- `templates/HANDOFF.md` — phase-gated pre-capture handoff template with checks, preview path, and what-not-to-claim boundaries.
- `templates/final-boundary-check.md` — standard pre-final boundary QA artifact before live UI capture/media promotion.
- `templates/phase-3-closeout.md` — final pre-capture phase closeout template: status, inventory, PASS checks, non-work, blockers, and next options.
- `templates/video-manifest.example.yaml` — manifest starter for guided tutorial videos.
- `templates/driverjs-tour.example.yaml` — Driver.js guided tour starter.
- `templates/hyperframes-storyboard.example.yaml` — HyperFrames storyboard starter.
- `templates/capture-blocked-lesson.md` — provisional lesson skeleton for capture-blocked manual production.
- `templates/capture-lab-unblock.md` — runbook template for blocked local capture environments.
- `scripts/validate-manual-package.py` — generic package/asset/forbidden-term validator.

- `templates/capture-lab-unblock.md` — runbook skeleton for moving from blocked capture planning to daemon/pull/config/start/ready/stop evidence.
- `templates/content-checklist.md` — reusable content QA checklist for provisional-to-final promotion.
- `templates/media-checklist.md` — reusable media QA checklist, including capture-blocked reporting.
- `scripts/validate-manual-package.py` — generic package/asset/forbidden-term validator.
- `scripts/manifest_lint.py` — conservative manifest/evidence/risk/QA linter.
- `scripts/add-lessons-to-manifest.py` — helper to insert conservative lesson records while preserving lesson-id order.
- `scripts/build-evidence-map.py` — generate a Markdown evidence-tier matrix from phase-gated manifests.
- `scripts/build-static-manual.py` — manifest-driven static HTML packager; supports provisional/capture-blocked preview banners.
- `scripts/check-video-prereqs.py` — generic prerequisite checker for video tooling.
- `scripts/verify-video-artifact.py` — ffprobe/html-reference checks for rendered tutorial videos.
- `scripts/verify-preview-package.py` — recursive provisional preview checker for banners, lesson pages, media refs, and final-language patterns.
- `scripts/media_probe.py` — ffprobe plus optional key-frame/contact-sheet generation.
- `scripts/glossary_coverage.py` — terminology coverage heuristic for English UI labels in lessons.
