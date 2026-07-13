# Phase-Gated Tool Compatibility Hardening

Use this reference when a manual project has portable validation/packaging scripts, but the current project manifest is intentionally phase-gated or capture-blocked.

## Problem pattern

A reusable script may expect a final/static-package manifest shape while the active manual is still in inventory, outline, or capture-blocked production. Typical symptoms:

- validator expects final fields such as `steps_file`, `review_card`, or static asset paths that are not valid yet;
- static builder crashes on missing final-package keys;
- capture/media is blocked, but scaffolds, evidence maps, glossary checks, and risk metadata can still be verified.

Do not force a final-package shape just to satisfy a stale script. Do not create ad-hoc HTML/media as a workaround. Treat this as a tool-compatibility gap and preserve the phase-gated truth of the manual.

## Required project-side artifacts

Create concise project documents that separate current evidence from expected future tooling behavior:

1. `qa/tool-compatibility-targets.md`
   - list each script/tool;
   - record current observed behavior;
   - define expected behavior for phase-gated or pre-capture mode;
   - state what must not run yet, such as static preview, capture stack, or media generation.
2. `qa/package-checks.md` or equivalent
   - record pass/fail/error output from existing scripts without over-normalizing it;
   - distinguish schema mismatch from content failure.
3. `qa/phase-<phase>-check-log.md`
   - record stable checks that did run and passed;
   - record explicitly what was not run and why.
4. `sources/static-preview-readiness.md`
   - explain why preview was not generated if the builder is not compatible with the current manifest;
   - define the readiness criteria before preview generation is allowed.

## Stable-only checks before closeout

When capture/media/static preview are blocked, run only checks that match the current phase, for example:

- manifest/evidence/risk lints that understand capture-blocked status;
- glossary coverage against current lesson skeletons;
- file presence/non-empty checks for approved lesson IDs;
- safe-fixture field checks for risky lessons;
- absence checks for accidental media or preview output when those are disallowed.

## Closeout language

In the phase closeout, report tool compatibility as its own section:

- `Checks run` — commands and pass/fail summary.
- `Not run` — tools intentionally skipped or known incompatible.
- `Compatibility gaps` — what the portable skill/scripts should learn.
- `Suggested skill/tool patch` — concrete expected behavior, not just a complaint.

Use this phrasing to avoid misleading completion claims: a validator/schema failure can mean the reusable tool is stale relative to the phase-gated manifest, not that the manual content itself failed QA.

## Safety notes

- Do not start Docker/bench/browser capture stacks during a tool-hardening phase unless the gate explicitly authorizes runtime capture.
- Registry manifest availability proves an image tag exists; it is not the same as local pull, app-ready state, or UI capture readiness.
- If preview generation fails because a script expects final-package fields, remove partial preview output unless keeping it is explicitly useful for debugging.
