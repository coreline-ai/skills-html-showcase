# Capture Lab Unblock Runbook

Use this when a manual needs screenshots/video from a local app but the capture lab is not ready.

## Current blocked evidence

Record exact command output, not a paraphrase:

```text
{{docker_or_runtime_version}}
{{daemon_or_service_error}}
{{image_manifest_or_artifact_check}}
```

Interpretation:

- Runtime CLI installed: {{yes/no}}
- Runtime daemon/service reachable: {{yes/no}}
- Target image/build artifact exists remotely: {{yes/no/unknown}}
- Local pull/run verified: {{yes/no}}
- App ready for capture: {{yes/no}}
- Background services started by this phase: {{none/list}}

## Next checks once runtime is available

### 1. Daemon/service reachable

```bash
{{runtime}} --version
{{runtime}} info
{{runtime}} ps
```

### 2. Pull/build-only check

```bash
{{runtime}} pull {{target_image_tag}}
{{runtime}} image inspect {{target_image_tag}}
```

Do not call this app-ready; it only proves local image availability.

### 3. Compose/project prep only

```bash
{{prepare_project_commands}}
{{runtime_compose}} config > /tmp/{{project}}-compose-config.yml
```

Verify the rendered config pins the intended version/tag.

### 4. Stack start — only when monitored

```bash
{{runtime_compose}} up -d
{{runtime_compose}} ps
{{runtime_compose}} logs --tail=200 {{readiness_service}}
```

Start only if you can monitor readiness and stop/report state before closeout.

### 5. App-ready check

```bash
curl -I --max-time 10 {{local_url}} || true
curl -L --max-time 20 {{local_url}} | head -n 20
```

Record version/source evidence if visible.

### 6. Stop/report

```bash
{{runtime_compose}} ps
{{runtime_compose}} down
{{runtime_compose}} ps
```

Report containers/processes, ports, volumes, and whether screenshots/videos were produced.

## Fallback criteria

Fallback is allowed only after recording exact blocker evidence.

Allowed:

1. Alternate local target-version install.
2. Official/demo instance only if target version is verified, or content is explicitly generic/non-final.
3. Continue capture-independent conceptual drafts with `UI_CAPTURE_REQUIRED` and no media.

Not allowed:

- Treat latest/other-version UI as target-version proof.
- Produce final UI steps from source/docs only.
- Capture real operational data.
- Leave background services running silently.
