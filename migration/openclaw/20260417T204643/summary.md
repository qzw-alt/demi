# OpenClaw -> Hermes Migration Report

- Timestamp: 20260417T204643
- Mode: execute
- Source: `/root/.openclaw`
- Target: `/root/.hermes`

## Summary

- migrated: 14
- archived: 13
- skipped: 22
- conflict: 2
- error: 0

## What Was Not Fully Brought Over

- `/root/.openclaw/workspace/AGENTS.md` -> `(n/a)`: No workspace target was provided
- `/root/.openclaw/openclaw.json` -> `/root/.hermes/.env`: No Hermes-compatible messaging settings found
- `/root/.openclaw/openclaw.json` -> `/root/.hermes/.env`: No allowlisted Hermes-compatible secrets found
- `/root/.openclaw/openclaw.json` -> `/root/.hermes/.env`: No Discord settings found
- `/root/.openclaw/openclaw.json` -> `/root/.hermes/.env`: No Slack settings found
- `/root/.openclaw/openclaw.json` -> `/root/.hermes/.env`: No WhatsApp settings found
- `/root/.openclaw/openclaw.json` -> `/root/.hermes/.env`: No Signal settings found
- `/root/.openclaw/openclaw.json` -> `/root/.hermes/config.yaml`: No TTS configuration found in OpenClaw config
- `/root/.openclaw/exec-approvals.json` -> `/root/.hermes/config.yaml`: No allowlist patterns found
- `(n/a)` -> `/root/.hermes/skills/openclaw-imports`: No shared OpenClaw skills directories found
- `(n/a)` -> `/root/.hermes/tts`: Source directory not found
- `/root/.openclaw/openclaw.json` -> `(n/a)`: Selected Hermes-compatible values were extracted; raw OpenClaw config was not copied.
- `/root/.openclaw/memory/main.sqlite` -> `(n/a)`: Contains secrets, binary state, or product-specific runtime data
- `/root/.openclaw/credentials` -> `(n/a)`: Contains secrets, binary state, or product-specific runtime data
- `/root/.openclaw/devices` -> `(n/a)`: Contains secrets, binary state, or product-specific runtime data
- `/root/.openclaw/identity` -> `(n/a)`: Contains secrets, binary state, or product-specific runtime data
- `(n/a)` -> `(n/a)`: No MCP servers found in OpenClaw config
- `(n/a)` -> `(n/a)`: No hooks configuration found
- `(n/a)` -> `(n/a)`: No approvals configuration found
- `(n/a)` -> `(n/a)`: No memory backend configuration found
- `(n/a)` -> `(n/a)`: No UI/identity configuration found
- `(n/a)` -> `(n/a)`: No logging/diagnostics configuration found
- `/root/.openclaw/workspace/SOUL.md` -> `/root/.hermes/SOUL.md`: Target exists and overwrite is disabled
- `/root/.openclaw/openclaw.json` -> `/root/.hermes/config.yaml`: Model already set and overwrite is disabled
