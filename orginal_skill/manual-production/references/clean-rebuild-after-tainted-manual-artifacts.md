# Clean rebuild after a tainted manual artifact

Use this when a manual package has accumulated patches, visual regressions, stale generated content, or the owner explicitly says to ignore the existing version and rebuild a new one.

## Trigger signals

- Owner says “ignore the existing vN,” “clean rebuild,” or “vN+1로 다시 만들어.”
- A workflow map or guide shell technically renders but no longer matches the reference interaction pattern.
- Multiple CSS/JS override blocks have been appended to repair isolated QA findings.
- The current artifact mixes production notes, old shell assumptions, and new design rules.

## Required response

1. **Stop patching the tainted artifact.** Treat the old package as reference-only unless the owner explicitly allows harvesting pieces.
2. **Create a new versioned directory** such as `product-manual-package-v3`; do not overwrite the previous package.
3. **Rebuild the evidence map from source/docs/live evidence**, not from generated lesson copy in the old package.
4. **Write a manifest boundary** that records:
   - clean rebuild: true;
   - old artifact path ignored as input;
   - evidence sources used;
   - what is still not live-UI/runtime verified.
5. **Implement one coherent shell**, not a stack of late overrides. For workflow canvases, verify the desktop reference layout at representative widths before claiming PASS.
6. **Re-run verification from scratch**: static refs, file/browser smoke, visual QA, refutation QA, and handoff/status updates.

## Workflow-canvas specifics

If the correction involves a Print Station-style workflow canvas:

- Keep the primary desktop layout as a wide category-column canvas when the reference expects it. A responsive 3×2 wrap may pass DOM checks but fail visual intent.
- Numbered badges belong on connector arrows when numbers represent movement between nodes.
- Confirm `paths == badges == detail steps == checks` for every selectable flow.
- Confirm the selected-flow detail and lesson sections update with the same canonical step data.
- Record dense long arrows as a polish caveat only if badge order remains readable and does not imply ownership by the wrong node.

## Reporting boundary

Report the new artifact root and entry URL separately from the old package. Do not imply live runtime/admin UI verification unless the live system was actually started and tested.
