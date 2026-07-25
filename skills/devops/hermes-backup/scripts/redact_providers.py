#!/usr/bin/env python3
"""
redact_providers.py — multi-prefix secret truncator for known-buggy walker
prefixes (specifically tvly-, glpat-, AIza, etc. that the bundled
redact_secrets.py walker does NOT cover).

Replaces the v1 inline snippet from 2026-07-19, which had two bugs:

  1. The body character class was `[a-zA-Z0-9_]+` (missing `-`), so on
     `tvly-dev-sAFTx-...` it matched only `tvly-dev` (8 chars), short-
     circuited the length gate, and silently reported "no change".

  2. The `\b` boundary at the start of the pattern broke at the first
     internal hyphen, which is the OPPOSITE of what we want for provider
     tokens like `tvly-dev-sAFTx-...` where the value begins after
     `tvly-` and contains hyphens throughout.

Fixes (verified 2026-07-24):

  - Body class is `[a-zA-Z0-9_-]+` (includes hyphen).
  - Start anchor is negative look-behind `(?<![\w-])` so the match begins
    only at a fresh word boundary, not after an internal hyphen.
  - Operates on a SINGLE file path (`argv[1]`), runs ALL known prefixes
    in one pass — no need to invoke per-prefix.

Usage:
    python3 redact_providers.py <path-to-file>

Verification recipe (after running):
    grep -nE 'tvly-[a-zA-Z0-9_-]{40,}' <path>   # should be 0 hits
    grep -nE 'sk-[a-zA-Z0-9_-]{40,}'  <path>    # should be 0 hits
    grep -nE 'AIza[A-Za-z0-9_-]{30,}' <path>    # should be 0 hits
    grep -nE 'glpat-[a-zA-Z0-9_-]{30,}' <path>  # should be 0 hits

Loop until all scans return zero hits.

WHY THIS EXISTS:
    bundled scripts/redact_secrets.py's regex list is hard-coded to
    (sk, github_pat_, gh[pousr]_). It misses tvly, glpat, AIza, xoxb,
    etc. — BOTH in batch and single-file modes (verified 2026-07-24).
    This script is the complementary pass that fills the gap.
"""

import re
import sys


# Prefixes known to leak in user-authored MEMORY.md / config files.
# Keep in sync with bundled scripts/redact_secrets.py's prefix list —
# when you add a prefix there, add it here too (the bundled script
# has the same coverage gap on tvly-/AIza/glpat).
PROVIDER_PREFIXES = [
    'tvly',          # Tavily (50+ char keys)
    'sk',            # OpenAI / Anthropic / DeepSeek (variable)
    'github_pat',    # GitHub fine-grained PAT (~111 chars)
    'ghp', 'gho', 'ghu', 'ghr', 'ghs',  # classic GitHub PATs
    'AIza',          # Google API keys (39 chars total)
    'glpat',         # GitLab PAT
    'xoxb', 'xoxp',  # Slack bot/user tokens
]

# Don't try to truncate very short literals — preserve documentation
# placeholders like `sk-xxx` and example field NAMES that aren't real
# secrets. `body` is the substring AFTER the `prefix-` separator.
MIN_BODY_LEN = 25


def _trunc_factory(prefix):
    """Build a truncator closure bound to a specific prefix."""
    plen = len(prefix)

    def _trunc(m):
        s = m.group(0)
        if '...' in s:
            return s
        body = s[plen + 1:]
        if len(body) < MIN_BODY_LEN:
            return s
        return f'{prefix}-{body[:6]}...{body[-4:]}'

    return _trunc


def redact_file(path):
    """Read, redact, and write back. Reports which prefixes were hit."""
    try:
        c = open(path, encoding='utf-8').read()
    except (OSError, UnicodeDecodeError) as e:
        print(f'SKIP {path}: {e}')
        return False
    except Exception as e:
        print(f'ERROR {path}: {e}')
        return False

    new = c
    counts = {}
    for pref in PROVIDER_PREFIXES:
        # (?<![\w-]) — not preceded by word char or hyphen (avoids matching
        # INSIDE `xxx-tvly-foo`). [a-zA-Z0-9_-]+ in body — include hyphen
        # so we capture `tvly-dev-sAFTx-...` as a single match.
        pat = re.compile(rf'(?<![\w-]){re.escape(pref)}-[a-zA-Z0-9_-]+')
        before = new
        new = pat.sub(_trunc_factory(pref), new)
        if new != before:
            counts[pref] = sum(1 for _ in pat.finditer(before))

    if new != c:
        open(path, 'w', encoding='utf-8').write(new)
        for pref, n in counts.items():
            print(f'  truncated {n} {pref}- token(s) in {path}')
        print(f'WRITTEN: {path}')
    else:
        print(f'UNCHANGED: {path}')
    return new != c


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: redact_providers.py <path-to-file>', file=sys.stderr)
        sys.exit(2)
    redact_file(sys.argv[1])
