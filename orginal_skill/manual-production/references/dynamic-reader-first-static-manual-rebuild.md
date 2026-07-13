# Dynamic reader-first static manual rebuild

Use this when a manual artifact has drifted, the user rejects a shallow/repeated report, or the owner asks to re-plan with a specific model and Dynamic Workflow before rebuilding.

## Trigger signals

- The handoff/status document is stale or contradicts the current artifact.
- The user says the manual is not understandable to a human beginner.
- A previous report repeated work instead of reading the latest handoff/evidence.
- The owner requests a named model for planning or asks for Dynamic Workflow governance.
- Video/guided media has been abandoned and the replacement must stay static but still teach flow.

## Required controller sequence

1. **Read current handoff/status before speaking.** If handoff is stale, say that explicitly and use live artifact/evidence as source of truth. Do not repeat an old status as if current.
2. **Create a workflow run.** Use bounded work items such as:
   - `W000` reader-first replanning with the requested model.
   - `W001` artifact rebuild from the accepted plan.
   - `W002` human usability verification.
3. **Pin the reader promise.** A beginner should be able to say: which document/value they are looking at, what changed, what downstream check matters, and what not to misunderstand.
4. **Rebuild the static manual as flow evidence, not a flat document.** Each selected flow should have:
   - a beginner question,
   - real screenshot evidence with visible emphasis/callout,
   - concrete values such as document IDs, parties, items, quantities, statuses, or amounts,
   - representative path cards,
   - evidence screenshots/review cards,
   - notes for `what changed`, `what to check next`, and `common misunderstanding`.
5. **Verify human readability separately from technical rendering.** Check every flow selection changes the content, images load, concrete values are present, forbidden/internal terms are absent, console errors are zero, and the copy explains business meaning rather than visible UI mechanics.
6. **Synchronize delivery directories and update handoff.** If local/showable and deploy/public directories exist, hash-check that the accepted artifact is synchronized. Update handoff with model, workflow run path, hash/version, verification result, production-deploy boundary, and remaining approval gates.
7. **Report bounded status.** Separate local/staging PASS from production deployment. Do not imply Cloudflare or another public host was updated unless it was deployed and verified.

## Static-but-emphatic acceptance test

The result is acceptable only if the manual is static but not passive: flow map, path/arrow cues, screenshot callouts, value chips, review/evidence cards, jump/section affordances, and explicit downstream checks work together. A panel that repeats the high-level workflow without real screen values is still too abstract.

## Anti-patterns

- Answering from a compacted summary instead of reading/updating the handoff.
- Reporting a previous version after the user has asked to rebuild.
- Treating image load success as human comprehension.
- Calling a static replacement complete when it is just prose under a workflow map.
- Deploying or claiming production update before approval and public URL QA.
