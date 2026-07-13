# Repo/docs static manual package + Dynamic Workflow closeout

Use when building a static operator/admin manual package from public repository files and docs, especially when live runtime or UI capture is out of scope.

## Package baseline

A bounded static package should include, at minimum:

- `index.html` as the primary learner shell.
- `overview.html` or equivalent system overview when the product is non-trivial.
- `lessons/*.html` with standalone teaching depth, not thin copies of index cards.
- `sources/source-map.md` or equivalent source/evidence map.
- `qa/` with non-empty machine-readable and human-readable QA evidence.
- `extras/` for glossary or supporting learner aids when useful.
- `manual-package.manifest.json` or equivalent manifest.
- `STATUS.md` and `HANDOFF.md` synced with the final verdict.

Empty `qa/` or `extras/` directories are a QA smell. Either populate them with real package evidence or remove/avoid the directory if it is not part of the contract.

## Workflow Map shape

For showable static manuals, avoid replacing the workflow map with disconnected flow-description cards. Prefer a flow-first grouped-node map:

1. Top flow selector lists the reader's 4-8 major intents.
2. The map groups concrete nodes/functions into meaningful categories such as preparation, execution base, agent/key setup, design selection, production/review, operation/extension.
3. Selecting a flow highlights participating nodes and dims unrelated nodes.
4. Connectors or arrow badges show node-to-node movement or checking order.
5. A detail panel explains the selected flow separately from node definitions.
6. A focus carousel/card set follows the selected flow; for repo/docs-only packages, use learner-facing diagrams, concept maps, config/source snippets, or tables when screenshots are unavailable.

The target is `flow-first grouped node map`, not `flow cards that merely describe each flow`.

## Dynamic Workflow evidence loop

Run the manual as a governed workflow, not a one-shot build:

1. Inventory repository/docs and define bounded static scope.
2. Build the static package.
3. Run independent manual QA/refutation.
4. Treat `REQUEST_CHANGES` as productive signal and remediate before closeout.
5. Re-validate package structure, content uniqueness, links, rendered HTML, and visible interaction state.
6. Run strict audit over workflow items and evidence paths.
7. Sync `STATUS.md` and `HANDOFF.md` after the audit, not before.

Useful QA checks:

- Count expected HTML files, flows, and nodes from the source data.
- Verify every `lessons/*.html` has non-generic common mistakes and next-judgment copy.
- Confirm `qa/` contains final QA manifest/results and remediation notes.
- Confirm `extras/` contains glossary/learner aids if present in package tree.
- Open `index.html` via `file://`, switch at least one non-default flow, and verify detail title, connector/badge count, focus counter, visible leaks, and console errors.
- Open overview and at least one lesson page via `file://`.

## Claim boundary

For repo/docs-only static packages, final reports must say what was and was not verified.

Allowed claims:

- Repository/docs evidence was inventoried.
- Static package files, links, and browser smoke passed.
- Flow map and lesson interactions worked locally.
- Dynamic Workflow strict audit passed for the recorded evidence.

Do **not** claim unless actually performed:

- Live runtime/install succeeded.
- Docker/container/app health was verified.
- Current UI labels were live-captured.
- Agent CLI authentication or artifact generation succeeded.
- External deployment happened.

Use a verdict such as `PASS_BOUNDED_STATIC_PACKAGE` when the package is ready for local owner review but runtime/deployment remain out of scope.
