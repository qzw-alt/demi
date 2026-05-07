# OpenClaw -> Hermes Migration Notes

This document lists items that require manual attention after migration.

## PM2 / External Processes

Your PM2 processes (Discord bots, Telegram bots, etc.) are NOT affected
by this migration. They run independently and will continue working.
No action needed for PM2-managed processes.

## Archived Items (Manual Review Needed)

These OpenClaw configurations were archived because they don't have a
direct 1:1 mapping in Hermes. Review each file and recreate manually:

- **archive**: `/root/.hermes/migration/openclaw/20260417T204643/archive/workspace/IDENTITY.md` -- No direct Hermes destination; archived for manual review
- **archive**: `/root/.hermes/migration/openclaw/20260417T204643/archive/workspace/TOOLS.md` -- No direct Hermes destination; archived for manual review
- **archive**: `/root/.hermes/migration/openclaw/20260417T204643/archive/workspace/HEARTBEAT.md` -- No direct Hermes destination; archived for manual review
- **archive**: `/root/.hermes/migration/openclaw/20260417T204643/archive/workspace/memory` -- No direct Hermes destination; archived for manual review
- **plugins-config**: `/root/.hermes/migration/openclaw/20260417T204643/archive/plugins-config.json` -- Plugins config archived for manual review
- **plugins-config**: `/root/.hermes/migration/openclaw/20260417T204643/archive/extensions` -- Extensions directory archived
- **cron-jobs**: `/root/.hermes/migration/openclaw/20260417T204643/archive/cron-store` -- Cron job store archived
- **gateway-config**: `archive/gateway-config.json` -- Gateway config archived. Use 'hermes gateway' to configure.
- **full-providers**: `archive/model-aliases.json` -- Model aliases/catalog (1 entries) archived
- **deep-channels**: `archive/channels-deep-config.json` -- Deep channel config for 1 channels archived
- **browser-config**: `archive/browser-config.json` -- 
- **tools-config**: `archive/tools-config.json` -- Full tools config archived for reference
- **skills-config**: `archive/skills-registry-config.json` -- Skills registry config (0 entries) archived

## Conflicts (Existing Hermes Config Not Overwritten)

These items already existed in your Hermes config. Re-run with
`--overwrite` to force, or merge manually:

- **soul**: Target exists and overwrite is disabled
- **model-config**: Model already set and overwrite is disabled

## IMPORTANT: Archive the OpenClaw Directory

After migration, your OpenClaw directory still exists on disk with workspace
state files (todo.json, sessions, logs). If the Hermes agent discovers these
directories, it may read/write to them instead of the Hermes state, causing
confusion (e.g., cron jobs reading a different todo list than interactive sessions).

**Strongly recommended:** Run `hermes claw cleanup` to rename the OpenClaw
directory to `.openclaw.pre-migration`. This prevents the agent from finding it.
The directory is renamed, not deleted — you can undo this at any time.

If you skip this step and notice the agent getting confused about workspaces
or todo lists, run `hermes claw cleanup` to fix it.

## Hermes-Specific Setup

After migration, you may want to:
- Run `hermes claw cleanup` to archive the OpenClaw directory (prevents state confusion)
- Run `hermes setup` to configure any remaining settings
- Run `hermes mcp list` to verify MCP servers were imported correctly
- Run `hermes cron` to recreate scheduled tasks (see archived cron-store)
- Run `hermes gateway install` if you need the gateway service
- Review `~/.hermes/config.yaml` for any adjustments

