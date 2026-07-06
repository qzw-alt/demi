#!/usr/bin/env python3
"""
GSC token 升级: webmasters.readonly → webmasters (full)
跑这个脚本会:
1. 退现有 token
2. 启动 OAuth flow with full scope
3. 你手动授权后, 替换 token
"""

import os, sys
from pathlib import Path
from urllib.parse import urlparse, parse_qs
from google_auth_oauthlib.flow import Flow

CLIENT_SECRET_FILE = os.path.expanduser("~/.hermes/gsc/client_secret.json")
TOKEN_PATH = os.path.expanduser("~/.hermes/gsc/token.json")
# CRITICAL: 升级到 FULL scope
SCOPES = ["https://www.googleapis.com/auth/webmasters"]
REDIRECT_URI = "http://localhost"
VERIFIER_PATH = "/tmp/gsc_code_verifier_full.txt"


def main():
    if not Path(CLIENT_SECRET_FILE).exists():
        print(f"NOT_FOUND: {CLIENT_SECRET_FILE}")
        sys.exit(1)

    # 删除旧 token
    if Path(TOKEN_PATH).exists():
        Path(TOKEN_PATH).unlink()
        print(f"OLD_TOKEN_DELETED: {TOKEN_PATH}")

    flow = Flow.from_client_secrets_file(
        CLIENT_SECRET_FILE,
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI,
    )

    auth_url, _ = flow.authorization_url(
        access_type="offline",
        include_granted_scopes="true",
        prompt="consent",
    )
    Path(VERIFIER_PATH).write_text(flow.code_verifier)

    print("=" * 70)
    print("COPY_URL_TO_CHROME (FULL scope):")
    print("=" * 70)
    print(auth_url)
    print("=" * 70)
    print(f"VERIFIER_FILE: {VERIFIER_PATH}")

    callback = input("\n粘贴回调 URL 或 code:\n> ").strip()

    if "://" in callback:
        code = parse_qs(urlparse(callback).query).get("code", [None])[0]
    else:
        code = callback

    if not code:
        print("NO_CODE")
        sys.exit(1)

    flow.code_verifier = Path(VERIFIER_PATH).read_text().strip()
    print("FETCHING_TOKEN")
    flow.fetch_token(code=code)
    creds = flow.creds

    Path(TOKEN_PATH).parent.mkdir(parents=True, exist_ok=True)
    with open(TOKEN_PATH, "w") as f:
        f.write(creds.to_json())
    os.chmod(TOKEN_PATH, 0o600)
    Path(VERIFIER_PATH).unlink(missing_ok=True)
    
    # 验证
    with open(TOKEN_PATH) as f:
        import json as _j
        t = _j.load(f)
    scopes = t.get("scopes", [])
    print("TOKEN_SAVED")
    print(f"NEW_SCOPES: {scopes}")
    print(f"HAS_WEBMASTERS_FULL: {'YES' if 'https://www.googleapis.com/auth/webmasters' in scopes else 'NO'}")


if __name__ == "__main__":
    main()
