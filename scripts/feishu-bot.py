#!/usr/bin/env python3
"""
飞书机器人消息接收服务
接收飞书事件推送并处理
"""
import os
import json
import hmac
import hashlib
import base64
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
import urllib.request
import threading
import time

# 加载配置
CONFIG_FILE = os.path.expanduser("~/.config/feishu/.env")
config = {}

if os.path.exists(CONFIG_FILE):
    with open(CONFIG_FILE) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, value = line.split("=", 1)
                config[key] = value

APP_ID = config.get("FEISHU_APP_ID", "")
APP_SECRET = config.get("FEISHU_APP_SECRET", "")
ENCRYPT_KEY = config.get("FEISHU_ENCRYPT_KEY", "")
VERIFICATION_TOKEN = config.get("FEISHU_VERIFICATION_TOKEN", "")

def get_tenant_access_token():
    """获取tenant_access_token"""
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    data = json.dumps({"app_id": APP_ID, "app_secret": APP_SECRET}).encode()
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read().decode())
            return result.get("tenant_access_token")
    except Exception as e:
        print(f"[ERROR] 获取token失败: {e}")
        return None

def reply_message(chat_id, msg_id, content, token):
    """回复消息"""
    url = "https://open.feishu.cn/open-apis/im/v1/messages"
    payload = {
        "receive_id": chat_id,
        "msg_type": "text",
        "content": json.dumps({"text": content}),
        "reply_in_thread": False
    }
    if msg_id:
        payload["reply_message_id"] = msg_id
    
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {token}"},
        method="POST"
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read().decode())
            print(f"[REPLY] 回复结果: {result}")
            return result.get("code") == 0
    except Exception as e:
        print(f"[ERROR] 回复失败: {e}")
        return False

def process_message(event_data):
    """处理收到的消息"""
    message = event_data.get("message", {})
    sender = event_data.get("sender", {}).get("sender_id", {}).get("open_id", "")
    chat_id = message.get("chat_id", "")
    msg_id = message.get("message_id", "")
    msg_type = message.get("message_type", "")
    content = json.loads(message.get("content", "{}"))
    
    # 提取文本内容
    text = content.get("text", "")
    print(f"[MESSAGE] 收到消息: {text} from {sender}")
    
    # 保存到文件供AI读取
    msg_file = os.path.expanduser("~/.config/feishu/inbox.json")
    inbox = []
    if os.path.exists(msg_file):
        try:
            with open(msg_file) as f:
                inbox = json.load(f)
        except:
            inbox = []
    
    inbox.append({
        "time": datetime.now().isoformat(),
        "sender": sender,
        "chat_id": chat_id,
        "msg_id": msg_id,
        "text": text
    })
    
    # 只保留最近50条
    inbox = inbox[-50:]
    with open(msg_file, "w") as f:
        json.dump(inbox, f, indent=2, ensure_ascii=False)
    
    # 自动回复
    token = get_tenant_access_token()
    if token:
        reply_text = f"收到你的消息: {text[:100]}\n\n(我是AI助手，正在思考如何回复你...)"
        reply_message(chat_id, msg_id, reply_text, token)

class FeishuHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {format % args}")
    
    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length).decode('utf-8')
        
        try:
            data = json.loads(body)
            
            # 处理URL验证（首次配置时需要）
            if data.get("type") == "url_verification":
                challenge = data.get("challenge", "")
                print(f"[VERIFY] URL验证请求, challenge={challenge}")
                response = {"challenge": challenge}
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps(response).encode())
                return
            
            # 处理消息事件
            event_type = data.get("header", {}).get("event_type", "")
            
            if event_type == "im.message.receive_v1":
                event_data = data.get("event", {})
                # 在新线程中处理消息
                threading.Thread(target=process_message, args=(event_data,)).start()
            
            # 返回成功响应
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"code": 0}).encode())
            
        except Exception as e:
            print(f"[ERROR] 处理请求失败: {e}")
            self.send_response(500)
            self.end_headers()
    
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(b"Feishu Bot Server Running\n")

def main():
    port = int(os.getenv("FEISHU_BOT_PORT", "8080"))
    server = HTTPServer(('0.0.0.0', port), FeishuHandler)
    print(f"[START] 飞书机器人服务启动在端口 {port}")
    print(f"[INFO] 回调URL: http://YOUR_SERVER_IP:{port}/")
    
    # 在后台线程中启动服务器
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[STOP] 服务停止")
        server.shutdown()

if __name__ == "__main__":
    main()
