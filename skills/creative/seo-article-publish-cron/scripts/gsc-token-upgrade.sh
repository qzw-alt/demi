#!/usr/bin/env bash
# GSC Token Upgrade — webmasters.readonly → webmasters (full)
# Verified 2026-07-06 (oriental-destiny.com session).
#
# WHY: GSC reads via webmasters.readonly work (summary / top queries / pages /
# opportunities / trends). GSC writes (sitemap.submit + URL Inspection index)
# require webmasters (full scope). The token that ships with this profile is
# readonly. Use this script to upgrade ONCE, then keep the new token.
#
# After upgrade:
# - ~/.hermes/bin/gsc-od-daily (oriental-destiny monitor) — works as-is
# - ~/.hermes/bin/gsc-bulk-index (write 70+ URLs into URL Inspection queue) —
#   see references/gsc-bulk-index.md for the script
# - ~/.hermes/bin/gsc-submit-sitemap (one-shot sitemap submission) — see
#   references/gsc-submit-sitemap.md

set -e

TOK="${HOME}/.hermes/gsc/token.json"
SECRET="${HOME}/.hermes/gsc/client_secret.json"
SCOPE="https://www.googleapis.com/auth/webmasters"
REDIRECT="http://localhost"
VERIFIER="/tmp/gsc_code_verifier_upgrade.txt"

if [ ! -f "$SECRET" ]; then
  echo "MISSING: $SECRET"
  exit 1
fi

# Back up the existing readonly token
if [ -f "$TOK" ]; then
  cp "$TOK" "${TOK}.readonly.bak"
  echo "Backed up readonly token to ${TOK}.readonly.bak"
fi

# Check for python + google-auth
if ! /home/ubuntu/.hermes/hermes-agent/venv/bin/python3 -c "import google.oauth2.credentials" 2>/dev/null; then
  echo "MISSING: google-auth-oauthlib in hermes-agent venv"
  echo "Install with: /home/ubuntu/.hermes/hermes-agent/venv/bin/pip install google-auth-oauthlib google-api-python-client"
  exit 1
fi

# Write the one-shot upgrade script (avoids quoting pain in this bash file)
cat > /tmp/gsc_upgrade_inner.py <<'PYEOF'
import os, sys
from pathlib import Path
from urllib.parse import urlparse, parse_qs
from google_auth_oauthlib.flow import Flow

CLIENT_SECRET = os.path.expanduser("~/.hermes/gsc/client_secret.json")
TOKEN_PATH = os.path.expanduser("~/.hermes/gsc/token.json")
SCOPES = ["https://www.googleapis.com/auth/webmasters"]
REDIRECT_URI = "http://localhost"
VERIFIER_PATH = "/tmp/gsc_code_verifier_upgrade.txt"

if Path(TOKEN_PATH).exists():
    Path(TOKEN_PATH).unlink()
    print(f"OLD_TOKEN_DELETED: {TOKEN_PATH}")

flow = Flow.from_client_secrets_file(CLIENT_SECRET, scopes=SCOPES, redirect_uri=REDIRECT_URI)
auth_url, _ = flow.authorization_url(access_type="offline", include_granted_scopes="true", prompt="consent")
Path(VERIFIER_PATH).write_text(flow.code_verifier)

print("=" * 70)
print("COPY THIS URL TO CHROME — log in as the site owner, click Allow:")
print("=" * 70)
print(auth_url)
print("=" * 70)

callback = input("\nPaste the full callback URL (or just the code) here:\n> ").strip()
if "://" in callback:
    code = parse_qs(urlparse(callback).query).get("code", [None])[0]
else:
    code = callback

if not code:
    print("NO_CODE — abort")
    sys.exit(1)

flow.code_verifier = Path(VERIFIER_PATH).read_text().strip()
flow.fetch_token(code=code)
creds = flow.credentials

Path(TOKEN_PATH).parent.mkdir(parents=True, exist_ok=True)
with open(TOKEN_PATH, "w") as f:
    f.write(creds.to_json())
os.chmod(TOKEN_PATH, 0o600)
Path(VERIFIER_PATH).unlink(missing_ok=True)

# Verify
import json as _j
with open(TOKEN_PATH) as f:
    t = _j.load(f)
scopes = t.get("scopes", [])
print("=" * 70)
print(f"TOKEN_SAVED: {TOKEN_PATH}")
print(f"NEW_SCOPES: {scopes}")
print(f"HAS_WEBMASTERS_FULL: {'YES' if 'https://www.googleapis.com/auth/webmasters' in scopes else 'NO'}")
print(f"HAS_REFRESH: {'YES' if t.get('refresh_token') else 'NO'}")
print("=" * 70)
print("You can now run gsc-submit-sitemap and gsc-bulk-index without 403s.")
PYEOF

echo "Opening browser flow..."
/home/ubuntu/.hermes/hermes-agent/venv/bin/python3 /tmp/gsc_upgrade_inner.py

echo ""
echo "Verify: cat $TOK | python3 -c 'import json,sys; print(json.load(sys.stdin)[\"scopes\"])'"
echo "Backup at: ${TOK}.readonly.bak  (delete after you've confirmed the new token works)"