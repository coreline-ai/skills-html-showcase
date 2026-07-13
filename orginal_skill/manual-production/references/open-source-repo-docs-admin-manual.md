# Open-source repo/docs admin manual pattern

Use this when the user asks for a manual for a public GitHub project and the requested deliverable is a Markdown/admin/operator manual rather than a fully captured showable UI package.

## Intent

Produce a useful, source-grounded manual without pretending that repo/docs inspection is live UI verification. This is appropriate for installation, configuration, admin, CLI, and operational overview manuals where official docs and repository files are authoritative enough for the phase.

## Evidence order for this mode

1. Official product docs and docs index (`llms.txt`, docs sitemap, or equivalent) for current concepts and supported feature lists.
2. Repository README and deployment docs for install paths and product framing.
3. Deployment/config files for exact commands, service names, ports, env vars, overlays, and defaults.
4. CLI/package README files for command names and environment variables.
5. Live UI/browser capture only if the deliverable claims exact screen paths, screenshots, or button-by-button workflows.

Mark any exact UI path as unverified unless live UI was opened or official docs explicitly state it.

## Recommended workflow

1. Clone or inspect the repository at the requested URL.
2. Read the README, deployment README, compose/helm/config templates, CLI/Desktop docs if present, and the official docs index.
3. Pull the minimum official docs needed for the manual: welcome/overview, quickstart, deployment, resourcing, configuration, auth, model provider setup, connectors, core features, CLI/Desktop.
4. Draft for the named reader, not for the codebase: what it is, which deployment mode to choose, prerequisites, install, first login, provider setup, data connection, daily use, admin operations, backup/upgrade/troubleshooting.
5. Verify commands syntactically where possible without starting heavy services. For Docker Compose projects, run `docker compose ... config --quiet` for documented compose file combinations. This proves compose syntax/merge validity only; do not claim runtime PASS unless containers were actually started and health-checked.
6. Run Markdown QA: balanced fences, no empty headings, paths/commands visible, no secrets, and final report clearly separates verified vs not run.

## Docker Compose validation pattern

For repo-backed manuals that document compose overlays, validate the combinations you mention, for example:

```bash
cd <repo>/deployment/docker_compose
docker compose -f docker-compose.yml -f docker-compose.onyx-lite.yml config --quiet
docker compose -f docker-compose.yml -f docker-compose.onyx-lite.yml -f docker-compose.dev.yml config --quiet
docker compose -f docker-compose.yml -f docker-compose.dev.yml config --quiet
```

Only report this as `compose config validation: PASS`. Do **not** imply the app is installed, migrated, healthy, or accessible unless `docker compose up`, service health checks, and browser/API smoke were run.

## Output boundary

For this mode, a Markdown manual may be enough if the user simply asked for “manual” and did not request a showable tutorial package. State the artifact path and the exact verification performed. If screenshots/videos or exact UI walkthrough are required later, promote the work to normal manual-production with live UI capture and `manual-verification` visual QA.

## Pitfalls

- Do not copy upstream docs wholesale. Condense into an operator flow and cite/reference official docs.
- Do not trust web extraction formatting for commands without checking repo files; extracted docs may duplicate tokens or collapse spacing.
- Do not run large local stacks by default just to write a first manual. Validate config first, then ask/continue only if runtime verification is part of scope.
- Do not expose or invent credentials. Use placeholders and point to where the user creates API keys/tokens.
- Keep install/runtime verification claims separate from documentation QA claims.
