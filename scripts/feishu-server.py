#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
飞书消息接收与回复服务
保存到 ~/.hermes/scripts/feishu-server.py 并运行
"""

import os
import json
import urllib.request
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading

# ============ 配置 ============
APP_ID = "cli_a912890ce721dcee"
APP_SECRET = "4oGCUKGb30FEXb3SSiHU4xT2GzV4NFdM"
PORT = 8080
INBOX_FILE = os.path.expanduser("~/.config/feishu/inbox.json")
TOKEN_CACHE = {"token": None, "expire": 0}

# 确保目录存在
os.makedirs(os.path.dirname(INBOX_FILE), exist_ok=True)

def get_token():
    """获取 tenant_access_token"""
    import time
    now = time.time()
    if TOKEN_CACHE["token"] and now < TOKEN_CACHE["expire"]:
        return TOKEN_CACHE["token"]
    
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    data = json.dumps({"app_id": APP_ID, "app_secret": APP_SECRET}).encode()
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    
    with urllib.request.urlopen(req, timeout=30) as resp:
        result = json.loads(resp.read().decode())
        if result.get("code") == 0:
            TOKEN_CACHE["token"] = result["tenant_access_token"]
            TOKEN_CACHE["expire"] = now + result.get("expire", 7200) - 300
            return TOKEN_CACHE["token"]
    return None

def reply_message(chat_id, msg_id, text):
    """回复消息"""
    token = get_token()
    if not token:
        return False
    
    url = "https://open.feishu.cn/open-apis/im/v1/messages"
    payload = {
        "receive_id": chat_id,
        "msg_type": "text",
        "content": json.dumps({"text": text}),
        "reply_message_id": msg_id
    }
    
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {token}"}
    )
    
    with urllib.request.urlopen(req, timeout=30) as resp:
        result = json.loads(resp.read().decode())
        return result.get("code") == 0

def save_message(sender, chat_id, msg_id, text):
    """保存消息到 inbox"""
    inbox = []
    if os.path.exists(INBOX_FILE):
        try:
            with open(INBOX_FILE, 'r', encoding='utf-8') as f:
                inbox = json.load(f)
        except:
            inbox = []
    
    msg = {
        "time": datetime.now().isoformat(),
        "sender": sender,
        "chat_id": chat_id,
        "msg_id": msg_id,
        "text": text
    }
    inbox.append(msg)
    
    # 只保留最近100条
    inbox = inbox[-100:]
    
    with open(INBOX_FILE, 'w', encoding='utf-8') as f:
        json.dump(inbox, f, indent=2, ensure_ascii=False)
    
    return msg

class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {fmt % args}")
    
    def do_POST(self):
        content_len = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_len).decode('utf-8')
        
        try:
            data = json.loads(body)
            
            # URL 验证
            if data.get("type") == "url_verification":
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"challenge": data["challenge"]}).encode())
                print(f"[VERIFY] URL验证成功")
                return
            
            # 处理消息事件
            event_type = data.get("header", {}).get("event_type", "")
            
            if event_type == "im.message.receive_v1":
                event = data.get("event", {})
                message = event.get("message", {})
                sender = event.get("sender", {}).get("sender_id", {}).get("open_id", "unknown")
                
                chat_id = message.get("chat_id", "")
                msg_id = message.get("message_id", "")
                content = json.loads(message.get("content", "{}"))
                text = content.get("text", "")
                
                print(f"[RECV] 来自 {sender}: {text[:50]}")
                
                # 保存消息
                msg = save_message(sender, chat_id, msg_id, text)
                
                # 自动回复（可选）
                threading.Thread(target=self._auto_reply, args=(chat_id, msg_id, text)).start()
            
            # 返回成功
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"code": 0}).encode())
            
        except Exception as e:
            print(f"[ERROR] {e}")
            self.send_response(500)
            self.end_headers()
    
    def _auto_reply(self, chat_id, msg_id, text):
        """自动回复 - 这里可以改成调用AI"""
        # 简单回复，表示已收到
        reply_text = f"收到消息！\n你说：{text[:100]}\n\n（AI正在处理中，稍后回复你）"
        reply_message(chat_id, msg_id, reply_text)
        print(f"[REPLY] 已自动回复")
    
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.end_headers()
        
        # 显示最近的消息
        if os.path.exists(INBOX_FILE):
            with open(INBOX_FILE, 'r', encoding='utf-8') as f:
                inbox = json.load(f)
            self.wfile.write(f"最近 {len(inbox)} 条消息:\n\n".encode())
            for msg in inbox[-10:]:
                line = f"[{msg['time'][-8:]}] {msg['text'][:50]}...\n"
                self.wfile.write(line.encode())
        else:
            self.wfile.write(b"暂无消息\n")

def main():
    server = HTTPServer(('0.0.0.0', PORT), Handler)
    print(f"=" * 50)
    print(f"飞书机器人服务已启动")
    print(f"端口: {PORT}")
    print(f"回调URL: http://你的服务器IP:{PORT}/")
    print(f"消息收件箱: {INBOX_FILE}")
    print(f"=" * 50)
    print("按 Ctrl+C 停止服务")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n服务已停止")

if __name__ == "__main__":
    main()
