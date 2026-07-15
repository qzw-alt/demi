# CJK-Path Walker Miss — Reproduction, Diagnosis, and Recovery

The `redact_secrets.py` batch walker uses `os.walk` with a `dirs[:]` filter
against the `NOISE_DIRS` set. Files in directories whose names contain
Chinese / Japanese / Korean (CJK) characters are silently skipped in
**~1/3 of backups** despite the walker reporting a clean run. This file
documents the reproduction, the manual verification recipe, and the
recovery procedure.

## Symptom

- Step 4 walker prints "Redacted N total" with N > 0 (no error).
- Step 5 length-gated scan finds 1+ real `sk-` tokens in files whose
  path contains CJK characters (e.g. `workspace/website/德米知识库/...`).
- The matched file appears in `git ls-files` (it WAS tracked) but
  the walker did not modify it.

## Reproduction recipe (2026-07-14)

1. Working tree contains `workspace/website/德米知识库/01-记忆系统/MEMORY.md`
   with a real 72-char Kimi key: `sk-kimi-i...NGGW` (between
   `sk-kimi-i` and `NGGW` is the unredacted middle).
2. Run `python3 scripts/redact_secrets.py /tmp/demi-backup` (batch mode).
3. Walker reports "Total sk- redactions: 580" but the CJK file is
   not in the touched-files list.
4. Run the length-gated scan from SKILL.md step 5:
   ```
   grep -rln -E "sk-[a-zA-Z0-9_-]{40,}" \
     --include='*.md' --include='*.json' --include='*.yaml' ... \
     . 2>/dev/null | grep -v 'hermes-agent/venv\|hermes-agent/website\|...'
   ```
5. Output: `./workspace/website/德米知识库/01-记忆系统/MEMORY.md`.

## Root cause (suspected, not fully isolated)

Three candidates, none confirmed:
- (a) The `dirs[:] = [d for d in dirs if not any(n in f"{root}/{d}" for n in NOISE_DIRS)]`
  filter uses string `in` on a path prefix, but Unicode normalization
  mismatches between the `root` string and the `d` segment can cause
  the filter to silently drop a CJK-named directory.
- (b) A `UnicodeDecodeError` in the file body is swallowed by the
  `except (OSError, UnicodeError)` clause in `redact_file()`.
- (c) The `os.walk` iteration missed the file for an unknown reason
  (perhaps due to a stale `dirs[:]` mutation from a prior callback).

## Recovery procedure (always works)

Single-file redaction, passing `<backup_dir> <file>` (NOT just `<file>`):

```bash
# Correct — passes backup dir as argv[1] and target file as argv[2]
python3 /home/ubuntu/.hermes/skills/devops/hermes-backup/scripts/redact_secrets.py \
  /tmp/demi-backup \
  "workspace/website/德米知识库/01-记忆系统/MEMORY.md"

# Output:
#   REDACTED: /tmp/demi-backup/workspace/website/德米知识库/01-记忆系统/MEMORY.md (0 PAT, 1 sk-)
```

Then re-run the step 5 length-gated scan. Loop until zero hits.

## Inline fallback (when the skill isn't installed)

```python
# /tmp/redact_one.py
import re, sys
p = sys.argv[1]
with open(p, "r", encoding="utf-8") as f:
    c = f.read()
out = re.sub(
    r"sk-[a-zA-Z0-9_-]+",
    lambda m: m.group(0) if "..." in m.group(0) or len(m.group(0)) <= 15
              else f"sk-{m.group(0)[3:9]}...{m.group(0)[-4:]}",
    c,
)
with open(p, "w", encoding="utf-8") as f:
    f.write(out)
print(f"redacted: {p}")
```

```bash
python3 /tmp/redact_one.py "/tmp/demi-backup/workspace/website/德米知识库/01-记忆系统/MEMORY.md"
```

## Verification after redaction

```bash
# Byte-level check on the matched line
python3 -c "
import re
with open('/tmp/demi-backup/workspace/website/德米知识库/01-记忆系统/MEMORY.md', 'r', encoding='utf-8') as f:
    c = f.read()
for m in re.finditer(r'sk-[a-zA-Z0-9_-]+', c):
    print(f'len={len(m.group(0))}: {m.group(0)}')
"
# Expected: all matches are <20 chars (truncated placeholder form).
```

## Confirmed reproduction history

| Date | File | Key length | Walker hit? |
|------|------|-----------|-------------|
| 2026-07-08 | `workspace/website/德米知识库/01-记忆系统/MEMORY.md` | unknown | No |
| 2026-07-13 | (implicit — skill revision) | — | — |
| 2026-07-14 | `workspace/website/德米知识库/01-记忆系统/MEMORY.md` | 72 chars (`sk-kimi-iGU...NGGW`) | No |

## Operational guidance

- **Plan for one CJK-path miss per backup.** The post-rsync step 5
  length-gated grep scan is the only reliable verification. If you
  skip it because the walker reported clean, you'll push a 72-char
  Kimi key in the next commit and trigger GitHub push protection.
- **Single-file redact is the recovery, not the workaround.** Treat
  it as a normal step, not a fallback. Budget 1-2 minutes per miss.
- **Track CJK-path files in your `git ls-files` baseline.** If you
  see `workspace/*中文*/**` in the tracked list, expect a miss on
  every run until the walker is fixed. The known CJK-path file
  locations should be in the redaction priority list.
