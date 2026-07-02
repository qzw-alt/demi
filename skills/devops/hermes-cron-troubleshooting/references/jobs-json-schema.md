# jobs.json Schema — What Each Field Does at Runtime

The cron daemon reads `~/.hermes/cron/jobs.json` to construct every cron run. Knowing which fields are read **at runtime** (every tick) vs. **at creation only** (then ignored) is the difference between a 30-second repair and a mystery.

## File shape

```json
{
  "updated_at": "2026-07-02T...",
  "jobs": [
    { ...job1... },
    { ...job2... }
  ]
}
```

`jobs[]` is the array the daemon iterates. Each entry is a single job.

## Field-by-field

### Identity (rarely changes)

| Field         | Type   | When read    | Notes                                           |
|---------------|--------|--------------|-------------------------------------------------|
| `id`          | str    | creation     | The job_id. **Do not edit after creation.** Recreating loses history. |
| `name`        | str    | display only | Safe to rename. Doesn't affect matching.        |
| `created_at`  | ISO ts | creation     | Audit only.                                     |

### Core runtime fields (read every tick)

| Field        | Type        | When read        | Notes                                          |
|--------------|-------------|------------------|------------------------------------------------|
| `skills`     | list[str]   | **every run**    | Each name is resolved to `~/.hermes/skills/<name>/SKILL.md`. If any name fails to resolve, the cron fails with `skill-not-found` BEFORE the prompt is sent. |
| `skill`      | str         | **every run**    | Primary skill. Must also exist in `skills[]` (or be the same). |
| `prompt`     | str         | **every run**    | The full prompt template. Edit freely to fix spec drift (missing files, wrong branches, etc.). |
| `model`      | str         | **every run**    | e.g. `mini-max-m2.7`. Verify the model exists in `~/.hermes/config.yaml`. |
| `provider`   | str         | **every run**    | e.g. `custom:minimax_coding`. If your config.yaml uses a different name, the run errors. |
| `base_url`   | str\|null   | **every run**    | Optional override for the provider's API endpoint. |
| `schedule`   | object      | **every tick**   | `{kind: "cron", expr: "0 8 * * *", display: "0 8 * * *"}`. Edits take effect on the next daemon reload (usually within 1 minute). |
| `enabled`    | bool        | **every tick**   | If `false`, the job is skipped (no run, no error). |
| `state`      | str         | **every tick**   | Daemon-managed: `scheduled` / `running` / `paused`. Don't edit manually. |
| `paused_at`  | ISO ts\|null | **every tick**  | If set, the job is paused until `paused_at` is cleared (via `cronjob action=resume`). |
| `paused_reason` | str\|null | display only   | Free-text audit. |

### State-tracking fields (daemon-managed)

| Field                  | Notes                                            |
|------------------------|--------------------------------------------------|
| `last_run_at`          | ISO timestamp of the last attempted run.         |
| `last_status`          | `ok` / `error` / `null` (never run).             |
| `last_error`           | The exception text, if `last_status=error`.      |
| `last_delivery_error`  | If the run succeeded but delivery failed.        |
| `next_run_at`          | Computed from `schedule.expr` + now.             |
| `repeat`               | `{times: null|int, completed: int}`. `completed` increments on each successful run. |
| `fire_claim`           | Daemon token to prevent double-fire. Don't edit. |

### Delivery fields (read every run)

| Field      | Notes                                                     |
|------------|-----------------------------------------------------------|
| `deliver`  | `origin` (auto-deliver to current chat), `feishu`, `local` (save only), `all`, or `platform:chat_id:thread_id`. |
| `origin`   | `{platform, chat_id, chat_name, thread_id}`. Resolved when the job was created. If the chat was renamed or the bot was removed, update this manually. |

### Optional fields

| Field               | Notes                                                  |
|---------------------|--------------------------------------------------------|
| `script`            | Path to a shell script. If set + `no_agent=true`, the script runs verbatim and its stdout becomes the message. |
| `no_agent`          | If `true`, the LLM is skipped entirely; only `script` runs. |
| `enabled_toolsets`  | Restrict tools loaded for the agent (token optimization). |
| `workdir`           | Run the agent in this directory (loads project's CLAUDE.md / AGENTS.md). |
| `context_from`      | List of other job_ids whose latest output is injected as context. |

## Edit-in-place rules

1. **Safe to edit:** `skills`, `skill`, `prompt`, `model`, `provider`, `base_url`, `schedule.expr`, `enabled`, `deliver`, `origin.chat_id`.
2. **Edit-with-care:** `name` (display only, but if you have cronjob scripts that grep by name they'll break).
3. **Never edit:** `id`, `created_at`, `fire_claim`, `state`, `last_*` fields, `next_run_at`.
4. **Atomic write:** always use `json.dump(data, f, indent=2, ensure_ascii=False)` via Python. `patch` tool on this file desyncs nested indentation.

## Daemon reload behavior

Hermes' cron daemon polls `jobs.json` for changes (interval ~30s). An edit is picked up on the next poll. There's no need to restart the daemon. If you've been waiting >2 minutes and the new config isn't reflected in `cronjob list`, the daemon may be using a cached copy — check `ps aux | grep cron`.