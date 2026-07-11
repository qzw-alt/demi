# Secret Redaction Verification — Recipes

How to tell, byte-for-byte, whether a `sk-...` or `github_pat_...` string in a tracked file is a real unredacted key or an already-truncated placeholder.

## The disambiguation problem

The terminal truncates long strings in the middle with `...`. Both of these look identical when printed:

| Source on disk                     | What terminal displays           |
|------------------------------------|----------------------------------|
| `sk-kimi-iGu...NGGW` (75 chars, real key) | `sk-kimi-iGu...NGGW` |
| `sk-kimi-iGu...NGGW` (18 chars, already truncated) | `sk-kimi-iGu...NGGW` |

Both contain `sk-`, both have `...` in the middle, both have a `NGGW` tail. The terminal cannot distinguish them. GitHub's secret scanner distinguishes them by full-string match — the first one triggers push protection, the second one doesn't.

## Reliable recipes

### 1. Byte-level inspection with `xxd`

When `grep -rn "sk-[a-zA-Z0-9_-]{40,}"` flags a line, hex-dump the line to see exactly what's there:

```bash
grep -n -E "sk-[a-zA-Z0-9_-]{40,}" path/to/file | head -1 | xxd
```

Look at the byte count between `sk-` and the next whitespace or CJK character (each Chinese character is 3 bytes in UTF-8). A real key will have 50+ contiguous ASCII bytes; a truncated placeholder has 15-20.

Worked example from session (Kimi key):
```
00000000: 2d20 2a2a 4b69 6d69 2041 5049 2028 322e  - **Kimi API (2.
00000010: 3529 2a2a 3a20 736b 2d6b 696d 692d 6947  5)**: sk-kimi-iG
00000020: 7556 6a32 334d 676b 7a35 5a53 4b6b 5739  uVj23Mgkz5ZSKkW9
00000030: 7664 6b56 5467 3650 5159 3546 496c 7054  vdkVTg6PQY5FIlpT
00000040: 6950 6e38 7279 6872 4741 386a 4f34 5579  iPn8ryhrGA8jO4Uy
00000050: 5657 7265 6474 4566 6244 4e47 4757 efbc  VWredtEfbDNGGW..
00000060: 88e6 96b0 e985 8de7 bdae e4b8 ad       ..............
```

The `sk-` to `NGGW` span is 75 bytes (`75` ASCII chars), followed by CJK bytes (`efbc 88` = `（`). Real key, must redact.

### 2. Python byte-level check

When you have several candidate lines, a Python loop is faster than repeated `xxd`:

```python
with open(path, 'rb') as f:
    for i, line in enumerate(f, 1):
        if b'sk-' in line:
            # Find the sk- prefix and the next non-key byte
            idx = line.find(b'sk-')
            tail = line[idx:]
            # ASCII alphanumeric/dash/underscore = part of the key
            key_bytes = b''
            for b in tail:
                if b in b'sk-' or (0x30 <= b <= 0x39) or (0x41 <= b <= 0x5a) or (0x61 <= b <= 0x7a) or b == 0x5f:
                    key_bytes += bytes([b])
                else:
                    break
            # Strip the leading 'sk-' to get the body length
            body_len = len(key_bytes) - 3
            print(f"  line {i}: body_len={body_len}, truncated={'...' in key_bytes.decode('latin-1', errors='replace')}")
            if body_len > 30 and b'...' not in key_bytes:
                print(f"    REAL KEY ({body_len} bytes): {key_bytes.decode('latin-1', errors='replace')}")
```

### 3. Truncation script that handles both cases correctly

When the truncation regex is applied, it must:
- Skip lines that already contain `...` (already truncated)
- Match only against the unredacted source, not after a first-pass replacement

```python
import re

def truncate_kimi(match):
    full = match.group(1)
    if '...' in full:
        return match.group(0)            # already truncated, leave alone
    if len(full) <= 15:
        return match.group(0)            # already short
    return f"sk-{full[3:11]}...{full[-4:]}"  # body[0:8] + tail[-4:]

# IMPORTANT: re.sub against the ORIGINAL content, not a previously-mutated string.
# Also: match only the [a-zA-Z0-9_-]+ run, stopping at CJK/punctuation — otherwise
# the regex consumes the next Chinese character (UTF-8 non-ASCII) and the "..." marker
# ends up in the middle of the replacement.
content_new = re.sub(
    r'(sk-kimi-[a-zA-Z0-9_-]{30,})',  # 30+ chars guarantees a real key, not a placeholder
    truncate_kimi,
    content
)
```

The 30+ char gate (instead of 40+) is the right floor for *Kimi/Moonshot* keys because they're ~75 chars; for OpenAI/Anthropic keys, 40+ is appropriate. The crucial part is checking `if '...' in full: return match.group(0)` BEFORE attempting replacement.

### 4. After redaction — verify byte lengths

```bash
# Print all remaining sk-... lines with byte count
python3 -c "
import sys
for path in sys.argv[1:]:
    with open(path, 'rb') as f:
        for i, line in enumerate(f, 1):
            if b'sk-' in line and (b':' in line or b'=' in line):
                idx = line.find(b'sk-')
                key_run = b''
                for b in line[idx:]:
                    if b in b'sk-' or (0x30 <= b <= 0x39) or (0x41 <= b <= 0x5a) or (0x61 <= b <= 0x7a) or b == 0x5f:
                        key_run += bytes([b])
                    else:
                        break
                body = key_run[3:]
                truncated = b'...' in key_run
                print(f'{path}:{i} body={len(body)} truncated={truncated}')
                if len(body) > 20 and not truncated:
                    print(f'  ⚠ REAL KEY STILL PRESENT: {key_run.decode()}')
" path/to/file1 path/to/file2 ...
```

Expected output after successful redaction: every `sk-` line shows `body <= 15 truncated=True`. Any line showing `body > 20 truncated=False` is a leak that must be fixed before commit.

## Decision table

| `grep` matched? | `xxd` shows full key bytes? | Action |
|-----------------|------------------------------|--------|
| No | n/a | Nothing to do |
| Yes | No (line has `...` and short body) | Already truncated — leave alone |
| Yes | Yes (line has `...` but body is 50+ bytes before the `...`) | **Real key in disguise** — redact immediately |
| Yes | Yes (no `...` anywhere, body is 50+ bytes) | Real key — redact |

## Pitfall: terminal output is not a verification

`echo "$line"`, `print(line)`, `cat`, and `head -1 file | grep ...` all flow through the terminal's truncation layer. The ONLY reliable checks are byte-level (xxd, Python bytes, `wc -c` on the matched substring). Never trust terminal display to confirm a key is safe.