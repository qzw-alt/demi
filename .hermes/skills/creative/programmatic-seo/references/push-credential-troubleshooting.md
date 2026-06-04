# Git Push Credential Troubleshooting

When the cron job commits a daily article but the push to GitHub fails, the most common cause is missing or masked credentials. This file is the recovery recipe.

## Symptoms

```
fatal: Authentication failed for 'https://github.com/qzw-alt/chinahospitalsguide.git/'
fatal: could not read Username for 'https://github.com': No such device or address
```

## Diagnostic steps (in order)

1. **Check the remote URL format**:
   ```bash
   git remote -v
   ```
   - **Good**: `https://ghp_xxxxxxxxxxxx@github.com/owner/repo.git` (PAT embedded)
   - **Bad**: `https://github.com/owner/repo.git` (no PAT — will fail from cron)
   - **Bad**: `https://github...MbQ5@github.com/...` (truncated / masked — agent cannot read the real value)

2. **Check `~/.git-credentials`**:
   ```bash
   cat ~/.git-credentials
   ```
   If the file shows `https://github...MbQ5@github.com` (truncated by the sandbox), the cron runner has masked the credential for security — the agent cannot extract the real token.

3. **Check environment variables**:
   ```bash
   env | grep -iE "github|gh_|token"
   ```
   Look for `GITHUB_TOKEN`, `GH_TOKEN`, `GH_PAT`.

4. **Check for `gh` CLI**:
   ```bash
   which gh && gh auth status
   ```
   If installed and authenticated, `gh` can do the push via a different code path that bypasses the masked `~/.git-credentials`.

## Why this happens in the cron sandbox

The cron runner's security policy treats credential files as secrets and masks them when the agent reads them. This is intentional — it prevents the agent from exfiltrating tokens. The side effect is that the agent cannot use the credential even when it exists.

The fix is upstream: add a working `GITHUB_TOKEN` (or equivalent) to the cron job's environment, or update the remote URL in the repo's `.git/config` to embed the PAT directly. Neither of these is something the agent can do during a cron run.

## What the agent should do when push fails

The article, sitemap entry, and news index card are all already on local `master` in a clean commit. **Do not redo research or writing** — that's the worst-case response. Instead:

1. Verify the local commit is intact:
   ```bash
   cd /home/ubuntu/.hermes/workspace/website
   git log -1 --oneline
   git status  # should be clean
   ```
2. List the un-pushed commits:
   ```bash
   git log origin/master..HEAD --oneline
   ```
3. Report the failure in the cron output with: article title, commit hash, and the recovery command the human operator can run from a shell with a working credential:
   ```bash
   cd /home/ubuntu/.hermes/workspace/website
   git push origin master
   ```

## Verified failures

- **2026-06-03 cron run (chinahospitalsguide.com)**: Local commit succeeded, push failed with masked `~/.git-credentials`. The 2026-06-02 article (HARMONi-6 ivonescimab) was also still un-pushed from the previous run, so this is a recurring failure mode for that repo. The fix needs to happen in cron job config (add `GITHUB_TOKEN` env var), not in the agent workflow.
- **2026-06-04 cron run (chinahospitalsguide.com)**: Same pattern. Local `master` was 1 commit ahead of `origin/master` (the 2026-06-03 Hainan article, still un-pushed). The 2026-06-04 article research was completed (Pakistani CAR-T patient at Jiahui, source vir.com.vn + jiahui.com) but the article was not written before the session ended — no new commit was added. This is a budget exhaustion case (research took more calls than planned), not an auth failure. Recovery: write the article in the next cron run from the research notes still in conversation history, or re-research from the two URLs above.

## Reference

This is a class-level problem for any cron job that pushes to a git remote. It is not specific to chinahospitalsguide.com — the same trap could affect oriental-destiny.com if its cron ever loses the embedded PAT in `.git/config`.
