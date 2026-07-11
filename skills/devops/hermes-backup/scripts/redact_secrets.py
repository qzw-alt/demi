#!/usr/bin/env python3
"""
Hermes backup secret redaction script.

Walks a directory tree, finds all github_pat_ and sk- tokens, and replaces them
with safe placeholders. Use this against /tmp/<backup-dir>/ AFTER rsync and
BEFORE `git add -A`.

Why this exists as a script (not inline Python):
  - Inline `python3 -c "..."` in terminal() breaks on f-strings with nested
    braces — the shell, terminal quoting, and Python all want to interpret them.
  - The skill walker + the per-file fallback both need to be re-runnable without
    re-typing the regex each session.

Usage:
  python3 redact_secrets.py <backup_dir>            # batch walker
  python3 redact_secrets.py <backup_dir> <file>     # single-file redaction (CJK / missed paths)

The single-file mode is what the length-gated scan in SKILL.md step 5 calls
when the walker missed a file. It always runs against the literal path,
no os.walk.

ARG-ORDER GOTCHA: single-file mode REQUIRES the backup directory as argv[1].
Passing only the file path will be misread as BATCH mode (1 positional arg
triggers `len(sys.argv) == 2`) and crash at `os.chdir(BACKUP_DIR)` with
`NotADirectoryError`. The script now validates this up front.
"""

import os
import re
import sys

# === RUNTIME MODES ===
# batch mode: walk the tree and redact in every file
# single mode: redact one specific file (for walker-missed CJK paths)
BATCH = len(sys.argv) == 2
SINGLE = len(sys.argv) == 3

if not (BATCH or SINGLE):
    print("Usage: redact_secrets.py <backup_dir> [<file>]", file=sys.stderr)
    print("  batch:    redact_secrets.py /tmp/<backup_dir>", file=sys.stderr)
    print("  single:   redact_secrets.py /tmp/<backup_dir> <relative_or_abs_file_path>", file=sys.stderr)
    sys.exit(1)

BACKUP_DIR = sys.argv[1]
# Validate BACKUP_DIR is actually a directory — guards against single-mode invocation
# that mistakenly passes the file path as argv[1] (would otherwise trigger batch
# mode and `os.chdir(file)` would crash with NotADirectoryError).
if not os.path.isdir(BACKUP_DIR):
    print(f"ERROR: backup_dir is not a directory: {BACKUP_DIR}", file=sys.stderr)
    sys.exit(2)

# === SKILL STEP 4: TRUNCATE config.yaml ===
# Run in both modes — config.yaml is always a single file at the root.
CONFIG = os.path.join(BACKUP_DIR, "config.yaml")
if os.path.isfile(CONFIG):
    with open(CONFIG, "r", encoding="utf-8") as f:
        content = f.read()

    def _truncate_cfg(match):
        full_key = match.group(1)
        if "..." in full_key or len(full_key) <= 15:
            return match.group(0)
        return f"api_key: sk-{full_key[3:9]}...{full_key[-4:]}"

    new = re.sub(r"api_key:\s*(sk-[a-zA-Z0-9_-]+)", _truncate_cfg, content)
    if new != content:
        with open(CONFIG, "w", encoding="utf-8") as f:
            f.write(new)
        print(f"config.yaml: truncated API keys")
        # Verify byte-level
        with open(CONFIG, "rb") as f:
            for i, line in enumerate(f, 1):
                if b"api_key:" in line and b"sk-" in line:
                    val = line.split(b":", 1)[1].strip()
                    truncated = b"..." in val
                    print(f"  Line {i}: {val[:20]} (len={len(val)}, truncated={truncated})")
                    if not truncated and len(val) > 14:
                        print(f"    WARNING: FULL KEY - hex: {val.hex()}")


# === REDACTION REGEXES ===
PAT_RE = re.compile(r"github_pat_[a-zA-Z0-9_-]{40,}")
PAT_PLACEHOLDER = "github...OKEN"
SK_RE = re.compile(r"sk-[a-zA-Z0-9_-]+")


def _truncate_sk(match):
    full = match.group(0)
    if "..." in full or len(full) <= 15:
        return full
    body = full[3:]
    return f"sk-{body[:6]}...{body[-4:]}"


def redact_file(path):
    """Redact PATs and sk- keys in one file. Returns (n_pat, n_sk) redactions."""
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as fh:
            content = fh.read()
    except (OSError, UnicodeError) as e:
        print(f"  WALKER SKIPPED {path}: {type(e).__name__}: {e}")
        return (0, 0)

    new = content
    new, np = PAT_RE.subn(PAT_PLACEHOLDER, new)
    new, ns = SK_RE.subn(_truncate_sk, new)
    if new != content:
        try:
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(new)
        except (OSError, UnicodeError) as e:
            print(f"  WALKER WRITE FAILED {path}: {type(e).__name__}: {e}")
            return (0, 0)
    return (np, ns)


# === BATCH MODE: WALK THE TREE ===
if BATCH:
    os.chdir(BACKUP_DIR)
    NOISE_DIRS = (
        "venv/", "website/", "node_modules/", "ui-tui/", "tests/",
        ".curator_backups/", ".git/",
    )
    INCLUDE_EXT = (
        ".json", ".yaml", ".yml", ".md", ".txt", ".py", ".sh",
        ".toml", ".conf", ".ini", ".env",
    )
    n_pat = n_sk = n_files = 0
    files_touched = []
    for root, dirs, files in os.walk("."):
        # Filter noise dirs OUT of recursion. The `any(n in f"{root}/{d}" for n in ...)`
        # guard is a known weak point: CJK paths can fail to match this filter and
        # get skipped silently. The single-file mode is the recovery path.
        dirs[:] = [d for d in dirs if not any(n in f"{root}/{d}" for n in NOISE_DIRS)]
        for f in files:
            if not f.endswith(INCLUDE_EXT):
                continue
            path = os.path.join(root, f)
            np, ns = redact_file(path)
            if np or ns:
                files_touched.append((path, np, ns))
                n_pat += np
                n_sk += ns
                n_files += 1
    print(f"\nWalker results:")
    print(f"  Total PAT redactions: {n_pat}")
    print(f"  Total sk- redactions: {n_sk}")
    print(f"  Files modified: {n_files}")
    for p, np, ns in files_touched:
        parts = []
        if np: parts.append(f"{np} PAT")
        if ns: parts.append(f"{ns} sk-")
        print(f"  {', '.join(parts):20s}  {p}")

# === SINGLE-FILE MODE: REDACT ONE PATH (CJK / missed files) ===
elif SINGLE:
    # os.path.join with an absolute second arg returns that absolute arg unchanged,
    # so this works for both relative ('./path/to/file') and absolute paths.
    target = os.path.join(BACKUP_DIR, sys.argv[2])
    if not os.path.isfile(target):
        print(f"ERROR: target file does not exist: {target}", file=sys.stderr)
        sys.exit(2)
    np, ns = redact_file(target)
    if np or ns:
        print(f"REDACTED: {target} ({np} PAT, {ns} sk-)")
    else:
        print(f"NO CHANGES: {target}")
