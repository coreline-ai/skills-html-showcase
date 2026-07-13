# Pre-Capture Handoff and Closeout for Phase-Gated Manuals

Use this reference when a large manual package has reached a provisional, pre-capture state but live UI/runtime/media remain blocked.

## Trigger

Apply after a phase has produced manifest, lesson skeletons/drafts, glossary, QA docs, and optionally a static preview, but before live UI capture or final manual promotion.

## Required artifacts

Create or update these project files:

- `README.md` — concise current state, preview path, lesson range, blocked capture/media, not-final boundary.
- `HANDOFF.md` — what exists, stable checks, how to open preview, what not to claim, exact next unblock steps.
- `STATUS.md` — one-line status, artifact inventory, PASS checks, remaining blockers, next decision options.
- `qa/final-boundary-check.md` — no Docker/media, provisional-only preview, lesson status, risky/domain review boundary.
- `qa/phase-<n>-closeout.md` — phase summary, intentional non-work, validation commands, latest PASS outputs, remaining risks.

## Stable checks to record

Record exact commands and latest outputs, not paraphrases:

```bash
python /path/to/scripts/validate-manual-package.py manifest.yml
python /path/to/scripts/manifest_lint.py manifest.yml
python /path/to/scripts/glossary_coverage.py glossary.md tracks/<track>/*.md
```

For static preview packages, also run a recursive verification that checks:

- index exists and is non-empty;
- every expected lesson HTML exists and is non-empty;
- every preview page includes `PROVISIONAL / CAPTURE-BLOCKED / NOT FINAL`;
- no media artifacts exist under the preview;
- no embedded media refs are present;
- no final/completion language appears.

## What not to claim

Do not claim final manual completion, live UI truth, screenshot/video completion, domain validation, safe production execution, or capture readiness unless each item has direct evidence.

## Next decision options

Close with an explicit owner/oracle choice:

1. Start capture-lab unblocking later, beginning with daemon/app readiness and monitored stack boundaries.
2. Keep the package as a provisional source-only/manual-production test artifact.

## Pitfalls

- Do not create new lesson content during closeout; closeout should summarize and bound, not expand scope.
- Do not regenerate previews unless the phase explicitly authorizes it.
- Do not let a passing static preview imply live UI correctness.
- Keep historical mismatch/reconciliation notes, but mark them as historical once current checks pass.
