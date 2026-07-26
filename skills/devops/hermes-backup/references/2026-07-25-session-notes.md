# 2026-07-25 backup run notes

## Durable technique: protect housekeeping at the rsync boundary

The backup completed cleanly when `.gitignore` and `.gitattributes` were treated as repository housekeeping rather than source-mirror data:

1. Save tracked blobs from `HEAD` to a temporary housekeeping directory.
2. Add `--exclude='.gitignore'` and `--exclude='.gitattributes'` to `rsync --delete`.
3. Restore saved blobs immediately after rsync.
4. Still write the canonical `.gitignore` unconditionally after legacy-artifact cleanup.
5. Before commit, reject missing files or staged `D` / `??` status for either housekeeping file.

This is simpler and more deterministic than repeated checkout guards around rsync. The source directory remains untouched.

## Verification sequence used successfully

- Verified SSH by matching `successfully authenticated`, ignoring the command's non-zero-success convention.
- Verified canonical exclusion leaks were zero after rsync.
- Ran the standard redactor, followed by provider-aware redaction.
- Ran independent length-gated and all-file byte scans; both returned zero hits.
- Ran the same byte patterns against staged blobs after `git add -A`; zero hits.
- Skipped paths inside mode-`160000` gitlinks during working-tree and index scans.
- Re-ran the staged scan immediately before commit.
- After push, fetched `origin/master` and required equality among local `HEAD`, `origin/master`, and `git ls-remote` for `refs/heads/master`.
- Required a clean worktree after push, then removed the temporary clone.

## Observed redaction coverage gap

The primary `redact_secrets.py` walker again needed a complementary provider-aware pass for `tvly-` tokens. Keep `scripts/redact_providers.py` mandatory rather than optional whenever the full byte scan is part of the contract.
