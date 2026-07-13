# Beginner Companion Page Attachment

Use this when a manual package has a separate beginner-facing HTML explanation, overview, or first-read page in addition to a workflow map and detailed lessons.

## Why this exists

A common failure mode is to rebuild the main manual shell and `lessons/` pages, then forget a separately created beginner explanation. The result is technically correct but less useful for first-time readers because the mental-model layer is orphaned.

## Production checklist

1. **Inventory companion pages before finalizing**
   - Search the artifact root and previous accepted artifact versions for names such as `beginner.html`, `overview.html`, `system-overview.html`, `intro.html`, or Korean copy containing `초보`, `처음`, `개요`, `쉬운 설명`.
   - Decide whether the page is current, stale, or superseded. Do not blindly import tainted/rejected generated content.

2. **Attach deliberately**
   - Keep the beginner page near the package root unless the package already has a clear `pages/` convention.
   - Add a visible top-level CTA near the hero of `index.html`, before the workflow map, e.g. `처음이면 초보자용 설명부터 읽으세요`.
   - The beginner page should link back to `index.html` and forward to the relevant lessons.

3. **Preserve user-provided companion source**
   - If the user provides a specific HTML file or previously authored beginner page, treat that file as the content of truth.
   - Do **not** replace it with a shorter agent-authored explanation, summary page, or newly styled approximation just because the package shell was rebuilt.
   - Limit integration edits to packaging needs: navigation back to `index.html`, forward lesson links, relative asset/path fixes, title/manifest metadata, and QA notes.
   - Record the original source path and byte/line count or other identity evidence in `STATUS.md`, `HANDOFF.md`, and `qa/beginner-attachment-qa.md` so future agents can tell it was attached, not regenerated.
   - If the source seems stale or inconsistent, ask/flag before rewriting; do not silently “improve” it.

4. **Content boundary**
   - The companion page explains the system in plain language: what it is, who uses it, core terms, reading order, common mistakes, and stop criteria.
   - It should not replace standalone lesson depth. Lessons still need purpose, prerequisites, steps, cautions, readback, source evidence, next decision, and boundary.
   - It should not claim live deployment/UI success unless separately verified.

5. **Package metadata and handoff**
   - Add the companion page to the manifest, often as `secondary_entry` or equivalent.
   - Update `STATUS.md` and `HANDOFF.md` with the page path and verification boundary.
   - Add a QA note under `qa/`, such as `qa/beginner-attachment-qa.md`.

6. **Verification**
   - Run a static local-reference check over `index.html`, the beginner page, and lesson pages.
   - Open `index.html` via `file://` or the package's expected static-host path.
   - Verify the CTA is visible, click it, and confirm the beginner page heading, local links, and at least the key first-read sections render.

## Minimum evidence to record

```text
index.html includes href="beginner.html" or equivalent
local link check: errors 0
browser smoke: index CTA visible -> click -> beginner page opens
beginner page contains heading, plain-language summary, reading order/steps, and boundary
```

## Anti-patterns

- Orphaning a beginner page after a clean rebuild.
- Replacing a user-provided companion HTML with a new shorter explanation instead of attaching the provided source with minimal navigation/metadata integration.
- Treating an index workflow map as sufficient beginner explanation when the user explicitly asked for a separate beginner HTML explanation.
- Importing a stale previous-version page without checking it against the new package scope and source boundaries.
- Verifying only standalone lessons while the main `index.html` cannot reach the beginner page.
