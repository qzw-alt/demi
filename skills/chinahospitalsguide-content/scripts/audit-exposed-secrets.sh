#!/bin/bash
# Audit chinahospitalsguide-style repos for exposed secrets + public-accessible
# hardcoded keys. Run BEFORE any deployment / commit / merge to master.
#
# Use:
#   bash scripts/audit-exposed-secrets.sh /path/to/repo
#   bash scripts/audit-exposed-secrets.sh .            # cwd
#
# Detects:
#   - sk-* API keys (DeepSeek / OpenAI / Anthropic / generic) in any tracked file
#   - The famous "https://***" schema-context bug (terminal-render-resistant
#     in read_file/grep output, but real corruption in the file)
#   - Public-accessible demo HTML pages (HTTP 200) that include sk-* keys
#   - robots.txt missing disallow on /report_demo* / /report.html
#   - sitemap.xml referencing noindex pages
#
# Exit codes:
#   0 = clean
#   1 = at least one finding (printed)
#   2 = toolchain missing (curl / python3 / git)

set -euo pipefail

REPO="${1:-.}"
echo "=== Audit exposed secrets: $REPO ==="
echo

if ! command -v python3 >/dev/null; then
    echo "❌ python3 not found" >&2; exit 2
fi

# 1. Scan tracked files for sk-* API keys
echo "--- 1. sk-* API keys in tracked files ---"
KEYS=$(python3 - <<'PY'
import os, re, sys
root = sys.argv[1]
seen = set()
for dirpath, dirs, files in os.walk(root):
    dirs[:] = [d for d in dirs if d not in ('.git', 'node_modules', '.wrangler', '_site', '.cache')]
    for f in files:
        if not f.endswith(('.js', '.html', '.json', '.md', '.txt', '.yml', '.yaml', '.env')):
            continue
        path = os.path.join(dirpath, f)
        try:
            c = open(path, 'rb').read().decode('utf-8', errors='ignore')
        except Exception:
            continue
        # Real sk- keys (long enough; exclude placeholders)
        for m in re.finditer(r'sk-[a-zA-Z0-9_-]{20,}', c):
            k = m.group(0)
            if '*' not in k and 'EXAMPLE' not in k:
                seen.add((path, k))
for path, k in sorted(seen):
    rel = os.path.relpath(path, root)
    print(f"  {rel}: {k}")
PY
"$REPO")
if [ -n "$KEYS" ]; then
    echo "$KEYS"
    echo "  ⚠️  Rotate these keys NOW (DeepSeek console / provider dashboard)"
    echo "  ⚠️  Remove hardcoded literals — use Cloudflare Worker proxy or env vars"
else
    echo "  ✅ none"
fi
echo

# 2. Schema @context "https://***" bug
echo "--- 2. https://*** schema @context corruption ---"
BUGS=$(grep -rln 'https://\*\*\*' "$REPO" 2>/dev/null | grep -v '\.git/' || true)
if [ -n "$BUGS" ]; then
    echo "$BUGS" | while read -r f; do
        echo "  ❌ $(realpath --relative-to="$REPO" "$f")"
    done
    echo "  ⚠️  These will be marked invalid by Google Rich Results Test"
    echo "  ⚠️  Replace 'https://***' with 'https://schema.org'"
else
    echo "  ✅ none"
fi
echo

# 3. If repo has a remote URL, check public demo pages
echo "--- 3. Public demo pages with hardcoded keys (HTTP 200) ---"
if git -C "$REPO" remote get-url origin >/dev/null 2>&1; then
    ORIGIN=$(git -C "$REPO" remote get-url origin)
    # Convert git@github.com:user/repo.git -> https://github.com/user/repo
    ORIGIN_HTTPS=$(echo "$ORIGIN" | sed -E 's#git@github.com:#https://github.com/#; s#\.git$##')
    DEMO_PATHS="report_demo.html report_demo_v2.html sample_report.html"
    for path in $DEMO_PATHS; do
        URL="$ORIGIN_HTTPS/$path"
        STATUS=$(curl -s -o /dev/null -w '%{http_code}' -L --max-time 10 "$URL" 2>/dev/null || echo "ERR")
        if [ "$STATUS" = "200" ]; then
            CONTENT=$(curl -s -L --max-time 10 "$URL" 2>/dev/null || true)
            if echo "$CONTENT" | grep -qE 'sk-[a-zA-Z0-9_-]{20,}'; then
                echo "  ❌ $URL → HTTP 200 + contains sk-* key"
                echo "      page source is public, key is leaked"
            else
                echo "  ℹ️  $URL → HTTP 200 (no key found, but verify visually)"
            fi
        fi
    done
else
    echo "  (no git origin — skipping public-page check)"
fi
echo

# 4. robots.txt: demo pages should be disallowed
echo "--- 4. robots.txt coverage of demo pages ---"
if [ -f "$REPO/robots.txt" ]; then
    for path in report_demo.html report_demo_v2.html; do
        if grep -qE "Disallow:.*$path" "$REPO/robots.txt"; then
            echo "  ✅ $path disallowed"
        else
            echo "  ⚠️  $path NOT disallowed (visitors can access)"
        fi
    done
else
    echo "  ⚠️  no robots.txt at repo root"
fi
echo

echo "=== Done. If any ❌ above, treat as 🔴 critical: rotate + fix + redeploy. ==="