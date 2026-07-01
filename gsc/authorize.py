#!/usr/bin/env python3
"""GSC 授权 — Hermes 容器版 (PKCE code_verifier 文件持久化)"""
import os
import sys
from pathlib import Path
from urllib.parse import urlparse, parse_qs
from google_auth_oauthlib.flow import Flow

CLIENT_SECRET_FILE = "/home/ubuntu/.hermes/gsc/client_secret.json"
TOKEN_PATH = "/home/ubuntu/.hermes/gsc/token.json"
SCOPES = ["https://www.googleapis.com/auth/webmasters.readonly"]
REDIRECT_URI = "http://localhost"
VERIFIER_PATH = "/tmp/gsc_code_verifier.txt"


def main():
    if not Path(CLIENT_SECRET_FILE).exists():
        print(f"NOT_FOUND: {CLIENT_SECRET_FILE}")
        sys.exit(1)

    if Path(TOKEN_PATH).exists():
        print(f"TOKEN_EXISTS: {TOKEN_PATH}")
        if sys.stdin.isatty():
            ans = input("重新授权？(y/N): ").strip().lower()
            if ans != "y":
                print("已取消")
                return

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
    print("COPY_URL_TO_CHROME:")
    print("=" * 70)
    print(auth_url)
    print("=" * 70)
    print(f"VERIFIER_FILE: {VERIFIER_PATH}")

    if not sys.stdin.isatty():
        print("NON_INTERACTIVE_EXIT")
        sys.exit(0)

    callback = input("\n请粘贴回调 URL 或 code:\n> ").strip()

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
    creds = flow.credentials

    Path(TOKEN_PATH).parent.mkdir(parents=True, exist_ok=True)
    with open(TOKEN_PATH, "w") as f:
        f.write(creds.to_json())
    os.chmod(TOKEN_PATH, 0o600)
    Path(VERIFIER_PATH).unlink(missing_ok=True)

    print("TOKEN_SAVED")
    print(f"PATH: {TOKEN_PATH}")
    print(f"ACCESS_TOKEN_PREFIX: {creds.token[:30]}")
    print(f"HAS_REFRESH: {'YES' if creds.refresh_token else 'NO'}")
    print(f"EXPIRY: {creds.expiry}")


if __name__ == "__main__":
    main()
