#!/usr/bin/env python3
"""
Send a text message to the Feishu home channel.
Verified: 2026-05-07 — works with execute_code (NOT terminal, security-scan blocks curl|python3).
Usage: python3 send_feishu_home.py "Your message here"
"""
import sys
import json
import urllib.request
import os

HOME_CHANNEL_ID = "oc_82a1a36b7bacddfbcae28d273674900a"

def get_feishu_credentials():
    env_vars = {}
    env_path = os.path.expanduser("~/.config/feishu/.env")
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if "=" in line and not line.startswith("#"):
                    k, v = line.split("=", 1)
                    env_vars[k] = v
    app_id = env_vars.get("FEISHU_APP_ID", "")
    app_secret = env_vars.get("FEISHU_APP_SECRET", "")
    if not app_id or not app_secret:
        raise ValueError("FEISHU_APP_ID or FEISHU_APP_SECRET not found in ~/.config/feishu/.env")
    return app_id, app_secret

def get_tenant_token(app_id, app_secret):
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    data = json.dumps({"app_id": app_id, "app_secret": app_secret}).encode()
    req = urllib.request.Request(url, data=data,
        headers={"Content-Type": "application/json"}, method="POST")
    with urllib.request.urlopen(req, timeout=30) as resp:
        result = json.loads(resp.read().decode())
    if result.get("code") != 0:
        raise Exception(f"Feishu auth failed: {result.get('msg')}")
    return result["tenant_access_token"]

def send_feishu_message(token, chat_id, message):
    url = "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=chat_id"
    payload = {
        "receive_id": chat_id,
        "msg_type": "text",
        "content": json.dumps({"text": message})
    }
    req = urllib.request.Request(url, data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {token}"},
        method="POST")
    with urllib.request.urlopen(req, timeout=30) as resp:
        result = json.loads(resp.read().decode())
    if result.get("code") != 0:
        raise Exception(f"Feishu send failed: {result.get('msg')}")
    return result.get("data", {}).get("message_id")

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 send_feishu_home.py \"Your message\"")
        sys.exit(1)
    message = sys.argv[1]
    app_id, app_secret = get_feishu_credentials()
    token = get_tenant_token(app_id, app_secret)
    msg_id = send_feishu_message(token, HOME_CHANNEL_ID, message)
    print(f"OK: message sent, ID={msg_id}")

if __name__ == "__main__":
    main()
