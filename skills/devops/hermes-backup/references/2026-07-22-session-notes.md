# 2026-07-22 session notes

Textbook execution of the 2026-07-21 workflow. All documented mitigations held.
No new failure modes; this note records what was CONFIRMED rather than what was fixed.

## Confirmed reproductions (no new fix needed)

| Pattern | Reproduction count | Behavior confirmed |
|---|---|---|
| CJK walker miss on `workspace/website/德米知识库/01-记忆系统/MEMORY.md` | 7th time | Single-file `redact_secrets.py <dir> <file>` redacted a real 72-char `sk-kim...NGGW` key (terminal display trap — looked truncated but was full 72 chars in the file) |
| `tvly-` walker miss on the 3 canonical MEMORY.md files | 4th time | All 3 files redacted via `/tmp/redact_prefix.py tvly <path>` after `redact_secrets.py` reported clean |
| rsync --delete wipes working-tree `.gitignore` | 7th time | Unconditional `cat > .gitignore <<EOF` at end of step 3 recovered cleanly; pre-rsync and step-3-top guards insufficient alone |
| PAT-in-cron-prompt Case A (dead `github...Q5`, HTTP 401) | 6th time | SSH path used; cron prompt still embeds the dead token |
| Heavy-dir leak through short exclude list | every run | hermes-agent/venv (607M today, was 456M on 2026-07-09), website (27M), tests (32M), ui-tui (3.7M) all present in working tree; .gitignore template catches them |
| AIza key hit inside submodule (`workspace/oriental-destiny/config.real.js`) | 1st time confirmation | Verified `git show :path` returns `fatal: Pathspec ... is in submodule` — confirms 2026-07-19 pitfall holds; no redaction needed for parent commit |

## Staged-blob scan (added 2026-07-21) — confirmed working

The post-`git add -A` defense-in-depth scan ran clean today:
```bash
git diff --cached --name-only | xargs -I{} sh -c 'git show ":{}" 2>/dev/null | grep -E "sk-[a-zA-Z0-9_-]{40,}|tvly-[a-zA-Z0-9_-]{40,}|github_pat_[a-zA-Z0-9_-]{40,}|gh[pousr]_[a-zA-Z0-9]{40,}|AIza[0-9A-Za-z_-]{30,}" && echo "IN: {}"'
```
Zero hits. This proves the working-tree redaction + .gitignore approach actually gets the staged index clean — not just the filesystem. Keep this scan in step 6.

## Submodule handling — refined today

When step-5 byte scan flagged `workspace/oriental-destiny/config.real.js` containing `AIzaSy...`:
1. First instinct was to redact it. Resisted.
2. Verified with `git check-ignore` — got `fatal: Pathspec 'config.real.js' is in submodule 'workspace/oriental-destiny'` (not "ignored")
3. Confirmed via `git ls-files --stage | awk '$1=="160000"'` that hermes-agent and workspace/oriental-destiny are the two submodules
4. Confirmed via `git show :workspace/oriental-destiny/config.real.js` that the staged-blob index does NOT contain the submodule-internal file

Decision: do NOT modify the submodule's working tree copy of `config.real.js`. The leak exists in `~/.hermes/workspace/oriental-destiny/` source, not in the parent repo's commit. (Whether the submodule itself leaks is a separate concern tracked via the gitlink SHA.)

Updated the SKILL.md pitfall to clarify: leave submodule-internal scan hits alone, verify with `git check-ignore` (returns "is in submodule") or `git ls-files --stage`, and don't waste cycles investigating them.

## Cron-prompt delivery format

Today's prompt required: "输出中文简报：认证方式、结果、远程提交哈希、敏感扫描结果" (Chinese brief: auth method, result, remote commit hash, secret scan results).

Delivered exactly that — Chinese, four required fields in order, lead sentence is the action item (rewrite cron prompt), body is the report. Confirms the 2026-07-21 pitfall "Cron-prompt delivery format is part of the contract".

## Numbers worth noting

- hermes-agent/venv grew from 456M (2026-07-09) → 607M (today) — likely a new package or upgrade. Still saved from commit by .gitignore.
- Working-tree changes today: 24 files, +1378 / −128 (smallest in a while — quiet day)
- Heavy-dir leak remains the dominant blocker; .gitignore remains the primary defense.

## No new pitfalls introduced

This run is a clean confirmation that the 2026-07-21 hardened workflow holds. The user has not yet rewritten the cron prompt to remove the embedded dead PAT — that's the only outstanding action item, and it has been escalated in 6 consecutive delivery responses without effect.