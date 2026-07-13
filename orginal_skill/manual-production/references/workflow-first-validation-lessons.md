# Workflow-First Manual Validation Lessons

Use this reference when a concrete project is being used to harden the deployable `manual-production` workflow.

## Lessons captured

1. **A polished screen tour can still fail the manual goal.**
   - If the manual promises business-operation training, login/setup/sidebar/search/workspace orientation is only prerequisite content.
   - PASS requires actual job flows: trigger/input → prerequisites/master data → action/transaction → review/approval → output/report → success check.

2. **Keep onboarding slices, but demote them when needed.**
   - Existing orientation lessons should not be discarded if they have good screenshots/video.
   - Reclassify them as “기초 준비 / 화면 읽기 / 선행 학습” and connect them to the first real workflow lesson.

3. **Analysis/structuring must reach the primary shell before more capture.**
   - A separate structure document is not enough.
   - `index.html` or the main delivery shell must show the real workflow map before per-step media production continues.

4. **Verify the entry page, not only standalone lesson pages.**
   - A common failure is adding a behavior such as review-card lightbox to standalone lesson pages while the primary shell embeds only the lesson body and omits the shared modal/script.
   - Required interactions must be tested from the page the user actually opens.

5. **Record rework as skill validation, not project failure.**
   - When a validation project exposes a missing production rule, promote the rule into `manual-production`/`manual-verification` and reuse existing assets as evidence or prerequisites.

## Recommended response to this failure mode

- Mark verdict as `REQUEST_CHANGES`, not PASS.
- Preserve useful assets: screenshots, videos, Driver.js QA frames, review-card content.
- Rebuild the main shell around real business-unit flows.
- Fix primary-shell interactions.
- Produce the next step only after a step plan with: `business_flow`, `operator_goal`, `trigger_input`, `prerequisites`, `screens_to_capture`, `video_storyboard`, `review_cards`, `workflow_diagram_nodes`, `risk_boundary`, `safe_fixture_required`, `success_check`, `verification_required`.
