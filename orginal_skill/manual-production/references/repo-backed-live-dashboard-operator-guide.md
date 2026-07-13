# Repo-backed live dashboard operator guide

Use this pattern when the manual target is an internal/technical operations dashboard where the strongest evidence is a combination of:

- project handoff/README/docs that define the system and operating boundaries;
- a current data contract or fixture JSON that supplies real visible values;
- a locally built dashboard or static app that can be screenshotted/read in the browser;
- explicit safety boundaries such as paper/read-only/simulation mode.

## Production pattern

1. **Read the operating contract before writing copy**
   - Load project `HANDOFF.md`, `README`, domain docs, and the current contract/fixture JSON.
   - Extract the actual operating modes, safety flags, data freshness fields, instruments/entities, account/ledger scope, and dashboard section names.
   - Separate current fact from future capability. Do not imply live execution/order submission unless the contract says it is enabled and was verified.

2. **Build/run only the lowest-risk surface needed for evidence**
   - Prefer the read-only dashboard build or static preview.
   - Start a local server only long enough to capture current sections and values.
   - If the source repo is not being changed, verify and report that boundary separately from manual package changes.

3. **Capture one full dashboard screenshot plus targeted meaning**
   - A full-page screenshot is useful as evidence, but it is not the lesson by itself.
   - Convert dashboard sections into operator concepts: current state, strategy/criteria, safety gates, audit/ledger, candidates/logs, readiness.
   - Quote representative visible values from the screenshot/contract so the reader can practice recognizing real state.

4. **Make the manual reader-first, not developer-first**
   - Add `overview.html` for the system mental model before deep lessons.
   - Add `beginner.html` with concept primer, term cards, analogies, danger/good pairs, visual recap/diagram/comic, and self-check questions.
   - Keep repo filenames, internal modules, APIs, and JSON keys out of the user-facing copy unless the operator actually needs them.

5. **Use Workflow Map as an operations model**
   - Group nodes by the real operating lifecycle, e.g. market/input → strategy/decision → safety gate → record/artifact → dashboard/operator review.
   - Define selectable flows that match operator questions such as “what happened today?”, “why is this only paper?”, “what criteria made this a candidate?”, “is the data fresh?”, “what is still blocked before real use?”
   - For every flow, keep the canonical step count aligned with detail checks and focus cards/carousel slides.

6. **Write deep lessons from source + visible evidence**
   - Lessons should explain operating principle, daily run flow, dashboard reading, strategy criteria, and safety/readiness when those are the true operator jobs.
   - Cite source docs/contract in status/qa/sources, but write the lesson in plain operator language.
   - State adjacent out-of-scope work explicitly: real-money execution, cron enabling, broker credentials, financial advice, or production mutation.

7. **Package and deploy without leaking internal artifacts**
   - Copy only public reader files into the onboarding/static host package.
   - Register the manual in the hub, deploy, then verify the public URL separately from local files.
   - Keep `qa/`, `status.md`, and source notes in the source package when useful, but do not expose internal worklogs unless intentionally public.

## Anti-patterns

- Treating a dashboard screenshot as self-explanatory.
- Writing investment/trading advice instead of explaining how to read a paper/simulation dashboard.
- Claiming runtime/live-order readiness from repo docs alone.
- Omitting beginner explanation because the source project is technical.
- Reusing generic “architecture” language instead of visible operator checks and actual current values.

## Closeout language

Separate these claims:

- source repo changed vs manual package changed;
- docs/contract/dashboard evidence used;
- local dashboard build/screenshot verified;
- public manual URL verified;
- runtime/live execution not performed or out of scope.
