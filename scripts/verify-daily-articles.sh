#!/bin/bash
# verify-daily-articles.sh — Daily watchdog for the two SEO article cron jobs.
# Runs at 10:00 (1h after each 8:00/9:00 cron). VERIFIES yesterday's articles are live.
# Strategy: silent on success (stdout captured by cron, no delivery); feishu_notify only on real failure.
#
# Why: Both crons (daily-oriental-destiny-article @ 8am, daily-chg-medical-news @ 9am) have a known
# pattern where the agent successfully commits+pushes+verifies HTTP 200, but the cron framework still
# marks the run as `last_status=error` because the agent loop threw a final RuntimeError after the cap
# fired (the article IS shipped, but the cron tool doesn't see the success). This watchdog is the
# independent source of truth — it curl-heads the last yesterday's articles and only warns when both
# are NOT 200.
#
# v1.0 / 2026-07-11 — created after cron false-positive on 2026-07-11 Betta ELEVATE + oriental-destiny cap-hit.

set -u

TODAY="$(date +%Y-%m-%d)"
YESTERDAY="$(date -d 'yesterday' +%Y-%m-%d 2>/dev/null || date -v-1d +%Y-%m-%d)"

# Sentinel URL list — yesterday's expected articles on each site.
# These change daily; the cron jobs decide what gets written. We just HEAD the previous day's URL.
# Both sites use fate/YYYY-MM-DD.html for oriental-destiny and YYYY-MM-DD-slug.html for chg.
# Instead of guessing today's slug, we HEAD yesterday's URL (which is the most recent deterministic
# article regardless of slug convention).

declare -a ERRORS=()

# --- Site 1: oriental-destiny (filename is fixed convention) ---
OD_URL="https://oriental-destiny.com/fate-${YESTERDAY}.html"
OD_HTTP=$(curl -m 15 -s -o /dev/null -w "%{http_code}" -A "Mozilla/5.0" "$OD_URL" 2>&1)
if [ "$OD_HTTP" != "200" ]; then
    ERRORS+=("oriental-destiny $OD_URL → $OD_HTTP (expected 200)")
fi

# --- Site 2: chinahospitalsguide (need to discover slug from sitemap) ---
# Step 1: parse the most recent <loc> ending in YESTERDAY's date
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
    # SUCCESS — both articles live. Cron framework's `last_status=error` was a false positive.
    # Output is captured but stays silent in no_agent mode.
    cat <<EOF
✅ Both daily articles live (yesterday=$YESTERDAY)
- oriental-destiny: $OD_URL → 200
- chinahospitalsguide: $CHG_YESTERDAY_URL → 200

If the cron's last_status shows "error" but this reports ✅, the failure was a cap-hit
FALSE POSITIVE — the article shipped, but the agent loop threw RuntimeError after the
iteration cap. No manual recovery needed.
EOF
    exit 0
else
    # FAILURE — at least one article is missing. Real failure, escalate.
    {
        echo "🚨 **Daily Article Watchdog — REAL FAILURE** (date=$YESTERDAY)"
        echo ""
        echo "Articles NOT at HTTP 200:"
        for e in "${ERRORS[@]}"; do
            echo "- $e"
        done
        echo ""
        echo "**Action needed:**"
        echo "1. Run \`hermes cron list\` to see last_status of both crons"
        echo "2. Check \`~/.hermes/cron/output/{c2aefdf3bada,fa7a29b3464e}/\` for the corresponding day"
        echo "3. If article is on origin/<branch> but not live: likely a GitHub Pages deploy lag, retry in 5min"
        echo "4. If article is missing from disk: cap-safe recovery mode failed (Step 0 didn't catch the partial state) — manual write + push required"
        echo ""
        echo "_Generated $(date '+%Y-%m-%d %H:%M:%S') Asia/Shanghai_"
    }
    exit 1
fi
