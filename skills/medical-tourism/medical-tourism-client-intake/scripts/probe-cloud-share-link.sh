#!/usr/bin/env bash
# probe-cloud-share-link.sh — Diagnose whether a patient-sent cloud share link is alive,
# without downloading the file.
#
# Usage:  ./probe-cloud-share-link.sh "<URL>"
#
# Output: prints redirect chain, final HTTP code, content-type, response size,
# and a verdict line for the agent to relay to the user.
#
# Pairs with: medical-tourism-client-intake skill — "云盘链接诊断三步法" section.
#
# Tested against: Sinosend (sinosend.com), Wetransfer, Google Drive share links,
# Dropbox, pstmrk.it / mailchi.mp email-tracking wrappers.

set -u

URL="${1:-}"
if [[ -z "$URL" ]]; then
  echo "Usage: $0 <URL>" >&2
  exit 2
fi

UA='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'

echo "============================================================"
echo "STEP 1: HEAD request (no body, follows redirects)"
echo "============================================================"
curl -sS -I -L -A "$UA" --max-time 20 "$URL"
echo ""

echo "============================================================"
echo "STEP 2: First hop only (no redirect follow) — see if tracker is dead"
echo "============================================================"
FIRST=$(curl -sS -i --max-time 15 "$URL" | head -20)
echo "$FIRST"
echo ""

echo "============================================================"
echo "STEP 3: Follow all redirects — final URL, code, content-type, size"
echo "============================================================"
curl -sS -o /dev/null -L -A "$UA" \
  -w 'final_url=%{url_effective}\nhttp_code=%{http_code}\nnum_redirects=%{num_redirects}\ncontent_type=%{content_type}\ncontent_length=%{size_download}\ntime_total=%{time_total}s\n' \
  --max-time 30 "$URL"
echo ""

echo "============================================================"
echo "STEP 4 (if size <= 10 KB): Inspect body — could be Vue splash / login shell"
echo "============================================================"
BODY_SIZE=$(curl -sS -o /dev/null -L -A "$UA" --max-time 20 -w '%{size_download}' "$URL")
if [[ "$BODY_SIZE" -le 10240 ]]; then
  echo "Body size = $BODY_SIZE bytes — likely not the real file. First 800 chars:"
  curl -sS -L -A "$UA" --max-time 20 "$URL" | head -c 800
  echo ""
fi
echo ""

echo "============================================================"
echo "VERDICT (suggested phrasing for the agent to relay to the user)"
echo "============================================================"
FINAL_CODE=$(curl -sS -o /dev/null -L -A "$UA" --max-time 30 -w '%{http_code}' "$URL")
if [[ "$FINAL_CODE" == "200" && "$BODY_SIZE" -gt 10240 ]]; then
  echo "  Link appears ALIVE — real file body returned."
elif [[ "$FINAL_CODE" == "404" ]]; then
  echo "  Link is DEAD — 404 (file expired or character lost in copy)."
elif [[ "$FINAL_CODE" == "200" && "$BODY_SIZE" -le 10240 ]]; then
  echo "  Link returns 200 but only a small body — likely a JS splash/login shell."
  echo "  curl can't render JS; the link MAY work in a real browser but agent can't confirm."
else
  echo "  Final HTTP $FINAL_CODE — diagnose manually."
fi