#!/bin/bash
# verify-daily-articles.sh — Daily watchdog for SEO article cron jobs.
#
# Purpose: distinguish cap-hit false positives from real cron failures in seconds.
# When a cron reports `last_status=error` but the article is actually live, this
# script is the fastest way to verify. Used in pair with the `[SHIPPED_OK]` token
# convention documented in the parent SKILL.md.
#
# Usage:
#   bash verify-daily-articles.sh
#   # or pass a specific date: bash verify-daily-articles.sh 2026-07-10
#
# Exit codes:
#   0 = both articles live, false positive (no action)
#   1 = at least one article NOT live, real failure (manual recovery needed)
#
# What it does:
#   1. Computes YESTERDAY's date (or uses the date arg).
#   2. Curl-HEADs the deterministic filename on each site:
#      - oriental-destiny.com: fate-YYYY-MM-DD.html (fixed convention)
#      - chinahospitalsguide.com: parses sitemap.xml for the most recent URL
#        containing YESTERDAY's date (slug varies daily)
#   3. Reports HTTP status for each, exits 0 if both 200, exits 1 if either fails.
#
# Customizing for new sites:
#   - For sites with fixed filename convention (e.g. `article-YYYY-MM-DD.html`),
#     add a new `curl` line and a new ERRORS+= check.
#   - For sites with slug-based naming, follow the chinahospitalsguide pattern:
#     parse sitemap.xml for <loc> containing the date.

set -u

YESTERDAY="${1:-$(date -d 'yesterday' +%Y-%m-%d 2>/dev/null || date -v-1d +%Y-%m-%d)}"

declare -a ERRORS=()

# --- Site 1: oriental-destiny (fixed filename: fate-YYYY-MM-DD.html) ---
OD_URL="https://oriental-destiny.com/fate-${YESTERDAY}.html"
OD_HTTP=$(curl -m 15 -s -o /dev/null -w "%{http_code}" -A "Mozilla/5.0" "$OD_URL" 2>&1)
if [ "$OD_HTTP" != "200" ]; then
    ERRORS+=("oriental-destiny $OD_URL → $OD_HTTP (expected 200)")
fi

# --- Site 2: chinahospitalsguide (slug varies, parse sitemap for date) ---
CHG_SITEMAP=$(curl -m 15 -fsSL -A "Mozilla/5.0" "https://chinahospitalsguide.com/sitemap.xml" 2>/dev/null)
CHG_YESTERDAY_URL=$(echo "$CHG_SITEMAP" | grep -oE "<loc>[^<]*${YESTERDAY}[^<]*</loc>" | head -1 | sed -E 's|</?loc>||g')
if [ -z "$CHG_YESTERDAY_URL" ]; then
    ERRORS+=("chinahospitalsguide sitemap missing YESTERDAY entry (date=${YESTERDAY})")
else
    CHG_HTTP=$(curl -m 15 -s -o /dev/null -w "%{http_code}" -A "Mozilla/5.0" "$CHG_YESTERDAY_URL" 2>&1)
    if [ "$CHG_HTTP" != "200" ]; then
        ERRORS+=("chinahospitalsguide $CHG_YESTERDAY_URL → $CHG_HTTP (expected 200)")
    fi
fi

# --- Report ---
if [ ${#ERRORS[@]} -eq 0 ]; then
    cat <<EOF
✅ Both daily articles live (date=${YESTERDAY})
- oriental-destiny: $OD_URL → 200
- chinahospitalsguide: $CHG_YESTERDAY_URL → 200

If the cron's last_status shows "error" but this reports ✅, the failure was a
cap-hit FALSE POSITIVE — the article shipped, but the agent loop threw
RuntimeError after the iteration cap. No manual recovery needed.
EOF
    exit 0
else
    {
        echo "🚨 **Daily Article Watchdog — REAL FAILURE** (date=${YESTERDAY})"
        echo ""
        echo "Articles NOT at HTTP 200:"
        for e in "${ERRORS[@]}"; do
            echo "- $e"
        done
        echo ""
        echo "**Action needed:**"
        echo "1. Run \`hermes cron list\` to see last_status of both crons"
        echo "2. Check ~/.hermes/cron/output/<job_id>/ for the corresponding day"
        echo "3. If article is on origin/<branch> but not live: GitHub Pages deploy lag, retry in 5min"
        echo "4. If article missing from disk: cap-safe recovery mode failed (Step 0 didn't catch partial state) — manual write + push required"
    }
    exit 1
fi