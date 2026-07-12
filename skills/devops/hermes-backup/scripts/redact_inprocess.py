#!/usr/bin/env python3
"""In-process secret redaction walker — works on the actual file tree, no shell.

Use this when the bundled `scripts/redact_secrets.py` is not available (e.g.,
the skill is not yet installed, or you need to run before the skill is
loaded), OR when you've identified that the walker missed files and want a
wider reach. Does not depend on shell quoting, so it runs cleanly from
execute_code().

Args (none): walks the working tree rooted at the parent of this file's containing
backup directory. Or pass a directory path as argv[1] to walk elsewhere.

Output: per-file summary printed to stdout. Writes modified files in place.

Why this exists alongside redact_secrets.py:
  - The bundled walker uses an explicit INCLUDE_EXT tuple. A backup with
    unexpected extensions (e.g. `.vue`, `.svelte`, `.astro`) may need a quick
    ad-hoc redaction while the skill is being patched.
  - Runs from execute_code() without shell-quoting f-string issues.
  - Uses os.walk directly (no `dirs[:]` filter that can silently drop CJK
    paths), so it has slightly different (and broader) coverage than the bundled
    walker.

Heuristic for "is this a file worth scanning?":
  - Skips binary bytes at start (NUL in first 8KB).
  - Otherwise always reads (decode errors are caught).
  - Scans for github_pat_[a-zA-Z0-9_-]{40,} and sk-[a-zA-Z0-9_-]+ patterns.

This script intentionally scans ALL file types (not just the bundled 22) —
the skip-list is a perf optimization. For a typical backup, the perf cost is
negligible and you get full coverage.
"""

import os
import re
import sys

PAT_RE = re.compile(r"github_pat_[a-zA-Z0-9_-]{40,}")
SK_RE = re.compile(r"sk-[a-zA-Z0-9_-]+")
PAT_PLACEHOLDER = "github...OKEN"


def truncate_sk(match):
    full = match.group(0)
    if "..." in full or len(full) <= 15:
        return full
    body = full[3:]
    return f"sk-{body[:6]}...{body[-4:]}"


def redact(path: str) -> tuple[int, int]:
    """Returns (n_pat, n_sk). Skips binaries. Returns (0,0) on any error."""
    try:
        with open(path, "rb") as fh:
            head = fh.read(8192)
            if b"\x00" in head:
                return (0, 0)
            fh.seek(0)
            raw = fh.read()
        try:
            content = raw.decode("utf-8")
        except UnicodeDecodeError:
            content = raw.decode("utf-8", errors="replace")
    except (OSError, IOError):
        return (0, 0)

    new = content
    new, np = PAT_RE.subn(PAT_PLACEHOLDER, new)
    new, ns = SK_RE.subn(truncate_sk, new)
    if new == content:
        return (0, 0)
    try:
        with open(path, "w", encoding="utf-8", errors="replace") as fh:
            fh.write(new)
        return (np, ns)
    except (OSError, IOError):
        return (0, 0)


def walk_dir(root: str, skip_dirs: set | None = None):
    skip_dirs = skip_dirs or {".git", ".curator_backups"}
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in skip_dirs]
        for fn in filenames:
            yield os.path.join(dirpath, fn)


def main():
    target = sys.argv[1] if len(sys.argv) > 1 else "."
    if not os.path.isdir(target):
        print(f"Not a directory: {target}", file=sys.stderr)
        sys.exit(2)
    n_pat = n_sk = n_files = 0
    files_touched = []
    for path in walk_dir(target):
        np, ns = redact(path)
        if np or ns:
            files_touched.append((path, np, ns))
            n_pat += np
            n_sk += ns
            n_files += 1
    print(f"\nIn-process walker results:")
    print(f"  PAT redactions: {n_pat}")
    print(f"  sk- redactions: {n_sk}")
    print(f"  Files modified: {n_files}")
    for p, np, ns in files_touched:
        parts = []
        if np:
            parts.append(f"{np} PAT")
        if ns:
            parts.append(f"{ns} sk-")
        print(f"  {', '.join(parts):20s}  {p}")


if __name__ == "__main__":
    main()
