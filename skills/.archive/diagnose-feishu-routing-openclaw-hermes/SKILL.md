---
name: diagnose-feishu-routing-openclaw-hermes
description: Diagnose Feishu/Lark chat failures when Hermes and/or OpenClaw gateways may both be configured. Use for '飞书不能正常沟通', missing replies, wrong bot, or intermittent DM handling.
version: 1.0.0
author: Hermes Agent
license: MIT
---

# Diagnose Feishu routing issues across Hermes and OpenClaw

Use this when Feishu/Lark messages are not getting replies, replies are inconsistent, or the user may have multiple gateway stacks configured.

## Why this exists

A common failure mode is not a single broken bot, but configuration drift across two parallel systems:
- Hermes gateway using one Feishu app ID / secret
- OpenClaw gateway using a different Feishu app ID / secret
- OpenClaw pairing/allowlist allowing only an old Feishu open_id
- User talking to one bot while the other backend is actually running

This presents as 'can't communicate on Feishu' even when websocket connectivity is healthy.

## Investigation checklist

Follow in order.

### 1) Identify all Feishu configs
Check both stacks, not just one.

Read:
- `~/.hermes/.env`
- `~/.hermes/config.yaml`
- `/root/.openclaw/openclaw.json`
- `/root/.openclaw/credentials/feishu-default-allowFrom.json` if present
- `/root/.config/feishu/.env` and `/root/.config/feishu/server.log` if an old custom server may exist

What to compare:
- app IDs / app secrets
- connection mode (websocket vs webhook)
- DM policy / pairing policy
- home/default channel IDs
- allowlist / allowFrom values

### 2) Check which gateway is actually serving traffic
Use live process and port inspection, not assumptions.

Run:
- `hermes gateway status`
- `ps -ef | grep -E 'openclaw-gateway|hermes gateway run|/root/.local/bin/hermes' | grep -v grep`
- `ss -ltnp | grep -E '19433|8000|8080' || true`

Key interpretation:
- If `openclaw-gateway` owns the listen port, OpenClaw is the live chat path.
- Hermes may still be running in parallel, which can confuse debugging.
- Dual-running gateways are a red flag even if both look healthy.

### 3) Inspect logs for message receipt vs denial vs reply
Hermes logs to inspect:
- `~/.hermes/logs/agent.log`
- `~/.hermes/logs/errors.log`
- `~/.hermes/logs/gateway.log`

Search for:
- `Unauthorized user`
- `Received raw message`
- `Inbound dm message received`
- `Sending response`
- `authorized_error`
- `receive message loop exit`

Interpretation:
- `Received raw message` + `Sending response` means transport is basically working.
- `Unauthorized user: <open_id>` indicates allowlist/pairing mismatch.
- `authorized_error ... carry the API secret key in the Authorization header` points to provider/API auth failures that may break auxiliary features but are often not the root cause of missing inbound DM handling.
- `receive message loop exit` followed by reconnect usually indicates transient websocket churn, not necessarily the main issue.

### 4) Check OpenClaw pairing state
OpenClaw often stores the currently paired/allowed user separately.

Inspect:
- `/root/.openclaw/credentials/feishu-default-allowFrom.json`
- `/root/.openclaw/agents/main/sessions/sessions.json`

Important fields:
- allowed `open_id` values in `allowFrom`
- existing Feishu direct sessions like `agent:main:feishu:direct:<open_id>`

If the current user's open_id is missing from `allowFrom` and OpenClaw has `dmPolicy: pairing`, the user may be silently blocked from normal conversation.

### 5) Rule out stale custom Feishu servers
If `/root/.config/feishu/server.log` exists, read it.

A broken legacy script (for example a Python syntax error) may not be the active path, but it can mislead the operator into thinking 'the Feishu bot' is running when production traffic is actually handled elsewhere.

## Common root causes

### Root cause A: Dual-stack bot confusion
Symptoms:
- Hermes has one app ID, OpenClaw has another
- User talks to one Feishu bot but the other gateway is live
- Replies appear inconsistent or absent

Fix direction:
- Disable OpenClaw Feishu by setting `channels.feishu.enabled` to `false` in `/root/.openclaw/openclaw.json` when the goal is Hermes-only routing
- Verify the disabled state directly from config before declaring the cutover complete
- Keep the diagnosis focused on the active path; OpenClaw may still be running for other channels even after Feishu is disabled

### Root cause B: OpenClaw allowFrom/pairing mismatch
Symptoms:
- OpenClaw configured with `dmPolicy: pairing`
- `feishu-default-allowFrom.json` contains only an old open_id
- Logs show unauthorized or no session for current user

Fix direction:
- Add the current user open_id to allowFrom or re-run pairing
- Or temporarily relax policy for validation, then restore a controlled allowlist

### Root cause C: Hermes gateway was silently stopped by update/restart flow
Symptoms:
- `hermes gateway status` shows not running
- `~/.hermes/logs/update.log` contains lines like `Stopped 2 manual gateway process(es)` and `Restart manually: hermes gateway run`
- User reports Feishu suddenly has no response after an update or maintenance action

Fix direction:
- Restart Hermes explicitly with `hermes gateway run` if you need an immediate recovery
- For a durable fix, install the managed user service with `hermes gateway install`, then start it with `hermes gateway start`
- Verify persistence with:
  - `hermes gateway status`
  - `systemctl --user status hermes-gateway --no-pager --lines=20`
  - `systemctl --user is-enabled hermes-gateway`
  - `systemctl --user is-active hermes-gateway`
- If linger is reported enabled, the Hermes user service survives logout; prefer this over ad-hoc manual gateway processes
- Re-check status after restart before chasing auth or routing issues
- Treat this as a primary cause when Hermes is expected to handle Feishu traffic

### Root cause D: Model/provider auth errors are secondary noise
Symptoms:
- `authorized_error` / 401 in Hermes logs
- session summarization, vision, or auxiliary features failing
- but DM receive/send logs still show traffic flowing

Fix direction:
- Repair provider credentials separately
- Do not confuse this with the primary Feishu routing failure unless message handling itself is absent

## Decision rule

When both Hermes and OpenClaw are configured, assume the user wants one coherent Feishu path.

State the diagnosis in this order:
1. Which process is actually live
2. Whether the user is talking to the same bot that the live process is serving
3. Whether allowlist/pairing blocks the current user
4. Which auth/model issues are secondary vs primary

## Recommended final guidance to the user

Prefer a strong recommendation:
- 'Keep only Hermes' or
- 'Keep only OpenClaw'

Do not recommend leaving both Feishu stacks active unless the user explicitly needs that complexity and understands the routing consequences.
