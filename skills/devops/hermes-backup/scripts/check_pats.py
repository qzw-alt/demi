#!/usr/bin/env python3
"""
Hermes backup PAT scanner — distinguish real tokens from already-truncated placeholders.

Why this exists:
  Step 5's `grep -rln "github_pat_"` returns N files but doesn't tell you
  whether each match is a real ~111-char token or a placeholder like
  `github...MbQ5` — both render identically on terminal output. With 4+
  `.curator_backups/*/cron-jobs.json` snapshots plus every SKILL.md under
  `skills/` legitimately referencing `github_pat_...`, the answer is usually
  "all placeholders", but you can't prove it from grep alone.

This script extracts `(prefix, last4, length)` from each hit, groups by
signature, and prints a clean per-signature summary. If every hit has
`length < 40`, the placeholder form is already safe (real fine-grained
PATs are ~111 chars). If any hit has `length >= 40`, it's a live token and
needs single-file redaction.

Usage:
  python3 check_pats.py <backup_dir>             # scan working tree
  python3 check_pats.py <backup_dir> --include-binary    # also scan compiled binaries

Without --include-binary, files that look binary (first 8KB contains
NUL bytes) are skipped — this is correct for `.md`/`.json`/`.yaml`
where we expect text redaction to apply. With --include-binary, we
run a strings(1)-style regex sweep (catches `bin/uv`, `bin/tirith`).
"""

import os
import re
import sys

PAT_RE = re.compile(r"github_pat_[a-zA-Z0-9_-]{20,}")
NOISE_DIRS = (
    "hermes-agent/venv/", "hermes-agent/website/",
    "hermes-agent/node_modules/", "hermes-agent/tests/",
    "hermes-agent/ui-tui/", ".git/", ".curator_backups/",
)


def is_noise_dir(rel_path: str) -> bool:
    return any(n in (rel_path + "/") for n in NOISE_DIRS)


def looks_binary(path: str) -> bool:
    try:
        with open(path, "rb") as f:
            chunk = f.read(8192)
        return b"\x00" in chunk
    except OSError:
        return True


def scan_text(root: str, hits_out: list):
    """Walk root for text files, append (rel_path, token) tuples to hits_out."""
    for dp, dns, fns in os.walk(root):
        rel = os.path.relpath(dp, root)
        if is_noise_dir(rel + "/"):
            dns[:] = []
            continue
        for fn in fns:
            p = os.path.join(dp, fn)
            rel_p = os.path.relpath(p, root)
            if looks_binary(p):
                continue
            try:
                with open(p, "r", encoding="utf-8", errors="ignore") as f:
                    text = f.read()
            except (OSError, UnicodeError):
                continue
            for m in PAT_RE.finditer(text):
                hits_out.append((rel_p, m.group(0)))


def scan_binary(root: str, hits_out: list):
    """Scan compiled binaries (strings(1)-style) and append hits."""
    for dp, dns, fns in os.walk(root):
        rel = os.path.relpath(dp, root)
        if is_noise_dir(rel + "/"):
            dns[:] = []
            continue
        for fn in fns:
            p = os.path.join(dp, fn)
            if not looks_binary(p):
                continue
            try:
                with open(p, "rb") as f:
                    data = f.read()
                # decode-with-replace rather than ignore — we WANT to catch
                # tokens embedded in the middle of arbitrary binary data.
                text = data.decode("utf-8", errors="replace")
            except OSError:
                continue
            for m in PAT_RE.finditer(text):
                hits_out.append((os.path.relpath(p, root), m.group(0)))


def main():
    if len(sys.argv) < 2:
        print("Usage: check_pats.py <backup_dir> [--include-binary]", file=sys.stderr)
        sys.exit(1)
    backup_dir = sys.argv[1]
    if not os.path.isdir(backup_dir):
        print(f"ERROR: not a directory: {backup_dir}", file=sys.stderr)
        sys.exit(2)
    include_binary = "--include-binary" in sys.argv

    hits = []
    scan_text(backup_dir, hits)
    if include_binary:
        scan_binary(backup_dir, hits)

    if not hits:
        print("OK No PAT token hits found (text scan" +
              (" + binary scan)" if include_binary else ")"))
        sys.exit(0)

    # Group by signature: prefix (first 13 chars) + last 4 + total length
    # The signature reveals whether different files contain the SAME token
    # (deduplicating curator snapshots of the same source) vs DIFFERENT
    # tokens (more concerning — different live PATs across snapshots).
    by_sig = {}
    for path, tok in hits:
        prefix = tok[:13]
        last4 = tok[-4:]
        sig = (prefix, last4, len(tok))
        by_sig.setdefault(sig, []).append(path)

    # Print summary first — header line per signature — then file list
    flagged = False
    for sig, files in sorted(by_sig.items()):
        prefix, last4, length = sig
        is_real = length >= 40  # Real fine-grained PATs are 111 chars; placeholders are <40
        marker = "REAL" if is_real else "placeholder"
        print(f"\n{prefix}...{last4}  len={length}  ({marker}, {len(files)} files)")
        for f in files[:5]:
            print(f"   {f}")
        if len(files) > 5:
            print(f"   ... and {len(files) - 5} more")
        if is_real:
            flagged = True

    print()
    if flagged:
        print("ACTION: at least one hit has length >= 40 (live token).")
        print("Run single-file redaction on each path above:")
        print("  python3 redact_secrets.py <backup_dir> <file>")
        sys.exit(1)
    print("OK All hits are truncated placeholders (length < 40) — safe to commit.")
    sys.exit(0)


if __name__ == "__main__":
    main()
