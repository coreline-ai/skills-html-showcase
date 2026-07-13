# Peer-executed manual production with controller verification

Use this pattern when manual production is both a project deliverable and a validation case for the deployable `manual-production` skill.

## Trigger

The user asks the main Hermes session to stop doing implementation directly and instead:

- check live peers,
- assign execution/production to the project peer,
- keep Hermes focused on independent verification, gate decisions, and skill-library improvement.

## Roles

| Role | Responsibility |
|---|---|
| Worker peer | Executes manual production: step plan, captures, videos/screenshots, review cards, workflow diagrams, user-facing HTML/assets. |
| Hermes controller | Sends ACK-first handoff, verifies routing/ACK, waits for closeout, performs independent QA, issues PASS/REQUEST_CHANGES/BLOCKED, promotes reusable lessons into skills/templates/scripts. |

## Handoff requirements

The controller handoff to the worker peer should include:

1. ACK-first role confirmation with cwd/summary.
2. Exact production slice and expected output files.
3. Required sequence: analysis → structuring → index connection → per-step production → verification.
4. Safety boundaries and forbidden side effects.
5. User-facing copy restrictions: no internal process/tool/peer/provisional language in the final HTML/manual.
6. Required closeout shape:
   - execution state,
   - created/modified files,
   - implemented business flow,
   - safety boundaries / deliberately not executed actions,
   - verification evidence,
   - reusable `manual-production` improvements to promote.

## Controller verification checklist

Before trusting the peer closeout:

- Confirm broker routing and ACK are from the intended peer, not a self-route or stale id.
- Inspect generated files and referenced assets.
- Open the primary HTML artifact and run browser smoke checks.
- Verify workflow-card or lesson-tab selection changes the embedded learning frame to the correct lesson; do not accept standalone lesson success alone.
- Verify review-card/lightbox behavior in the primary shell, not only standalone lessons.
- Check user-facing text for internal process/tool leakage.
- Re-read the produced lesson against any mid-flight user correction. If the user adds “beginner-first”, “less verbose”, “workflow-first”, etc., forward that requirement to the worker peer and verify it explicitly in the closeout.
- Apply `manual-verification` and issue exactly one gate verdict.
- When issuing PASS, state the bounded scope precisely: e.g. “PASS for safe screen-reading / workflow-orientation” versus “not a full create-and-convert walkthrough.”
- Promote durable findings to `manual-production`, `manual-verification`, references, templates, or scripts.

## Mid-flight user correction pattern

If the user corrects the manual style or audience after dispatching the peer, the controller should not silently keep the original scope. Send a short update to the worker peer with:

1. the corrected requirement,
2. examples of user-facing content that must appear,
3. how the worker should reflect it in closeout,
4. a note that the controller will gate on the corrected requirement.

Example: when the user says a manual is for beginners, require concept primers, first-use term explanations, danger/good pairs, and final review checks in the worker output.

## Pitfall

Do not let the controller resume implementation just because it can. Once this mode is active, the controller should only make direct edits for verification artifacts or skill-library updates unless the user explicitly re-authorizes implementation.